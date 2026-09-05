#
# This file is part of LUNA.
#
# Copyright (c) 2026 the luna-ss contributors
# SPDX-License-Identifier: BSD-3-Clause
""" Gen2 (SuperSpeedPlus, 128b/132b) block-level physical machinery.

Stage-A architecture (doc/gen2_design.md SS1/SS2/SS4): the proven 32-bit
Gen1 link+protocol core is kept intact and clocked at the Gen2 operating
point; this module provides the Gen2 wire dialect around it:

* ``Gen2BlockTransmitter`` -- block-level ordered-set generation
  (TSEQ/TS1/TS2 with their SYNC cadences, SDS on idle-mode entry, SKP OS
  scheduling at the 1-per-40-blocks average [6.4.3.3]) and the data-block
  path fed by an internal 32->64 packet bridge: the Gen1 link layer's
  transmit stream is captured per packet (whole packets buffered so DPPs
  are wire-contiguous [7.2.1.2]), its K-code framing symbols are mapped
  to the Gen2 Table 6-2 framing symbols, a DATA-type header grows the
  DPHSTART framing and its TWO 2-byte length-field replicas (the
  24-byte Figure 7-4 format) [7.2.1.1] (our
  device never emits deferred DPHs), and packets burst out at the 64-bit
  beat rate with Gen2 Idle Symbols (5Ah! [7.1.2]) as filler.

* ``Gen2BlockReceiver`` -- block classification (control blocks: TS1/TS2/
  TSEQ consecutive-detection with the symbol-14/15 exclusion and
  SYNC-transparency rules [7.5.4.8.2], SDS detection; SKP never reaches
  the MAC -- the PHY strips it) and the reverse data path: a
  byte-granular grammar engine walks the data-block symbol stream
  (framing may land at any symbol offset once DPH length replicas are in
  play), translates Gen2 framing back into the Gen1 K-coded wire dialect
  the 32-bit core speaks, drops the DPH length replicas, tracks DPP
  extents by the DPH length field, and synthesizes Gen1 logical idle
  toward the core when nothing is in flight.

The PIPE-boundary beat convention matches the silicon-proven gw_usb3
datapath (pinned by sim_gen2_oracle, design note SS9.1): a 132-bit block
crosses as two 64-bit beats (three for the 24-symbol SKP OS), block_head
0x3 data / 0xC control, start_block on the first beat, symbol 0 of a
beat in bits [56:64].  Scrambling is wholly the PHY's at Gen2; this
module deals in clear symbols.

Throughput note (stage A): the RX grammar engine processes 4 symbols per
cycle against a wire that can deliver 8; an input queue absorbs bursts
(bounded by NumP flow control).  Whole-idle beats never occupy queue
slots individually: they are RUN-COMPRESSED at the enqueue side (one
counted entry per idle run, order-preserving via a 1-deep skid) and
replayed or bulk-discarded at the load side -- queue-entry arrival is
then O(constructs), so the engine's drain always outruns the wire and
the level stays bounded by the constructs in flight (bug #43: the
previous per-beat idle enqueue ratcheted the level up by every
construct, unboundedly).  A level debug tap is provided for the sizing
verdict.
"""

from amaranth import *
from amaranth.lib.fifo import SyncFIFO

from ...stream import USBRawSuperSpeedStream

from gw_usb3.tables import BlockType, BLOCK_CONTROL, BLOCK_DATA


# Gen2 Table 6-2 framing symbols.
G2_SHP  = int(BlockType.SHPS)     # 0x9A start header packet
G2_DPHP = int(BlockType.DPHPS)    # 0x95 non-deferred Gen2 DPH start
G2_SDP  = int(BlockType.SDPS)     # 0x96 start data packet payload
G2_END  = int(BlockType.ENDS)     # 0x65 DPP end
G2_EDB  = int(BlockType.EDBS)     # 0x69 DPP abort
G2_SLC  = int(BlockType.SLCS)     # 0x4B start link command
G2_EPF  = int(BlockType.EPFS)     # 0x36 end packet framing
G2_IDL  = int(BlockType.LIS)      # 0x5A Gen2 logical Idle Symbol

# Ordered-set identifier symbols.
TS1_ID  = int(BlockType.TS1)      # 0x1E
TS2_ID  = int(BlockType.TS2)      # 0x2D
TSEQ_ID = int(BlockType.TSEQ)     # 0x87
SDS_ID  = int(BlockType.SDS)      # 0xE1
SKP_SYM = int(BlockType.SKP)      # 0xCC
SKPEND  = int(BlockType.SKPEND)   # 0x33

# Gen1 K-code byte values (ctrl=1 in the 32-bit core's dialect).
K_SHP, K_EPF, K_SDP, K_END, K_EDB, K_SLC = 0xFB, 0xF7, 0x5C, 0xFD, 0x7C, 0xFE

# Gen1 -> Gen2 framing symbol translation (TX direction).
K_TO_G2 = {
    K_SHP: G2_SHP,
    K_EPF: G2_EPF,
    K_SDP: G2_SDP,
    K_END: G2_END,
    K_EDB: G2_EDB,
    K_SLC: G2_SLC,
}

IDLE_BEAT = int.from_bytes(bytes([G2_IDL] * 8), "big")

# Gen1 HPSTART word as it appears on the 32-bit stream (little-endian
# symbol order: byte 0 transmitted first).
HPSTART_WORD = int.from_bytes(bytes([K_SHP, K_SHP, K_SHP, K_EPF]),
                              "little")


def syms_to_beat(syms):
    """Pack eight symbol constants into a 64-bit beat value."""
    return int.from_bytes(bytes(syms), "big")


def syms_to_block(syms):
    """Pack sixteen symbol constants into a 128-bit block value
    (width-program core_width=128: one beat = one whole block;
    symbol 0 in the TOP byte, matching ``syms_to_beat``)."""
    return int.from_bytes(bytes(syms), "big")


IDLE_BLOCK = int.from_bytes(bytes([G2_IDL] * 16), "big")

# Gen1 HPSTART as it appears in the LOW half of the first 64-bit
# link-stream word at words=2 ([HPSTART|DW0]).
HPSTART_HALF = HPSTART_WORD


class Gen2TxBridge(Elaboratable):
    """Per-packet 32->64 transmit bridge (stage A).

    Captures whole packets from the Gen1 transmit stream (packets are
    delimited by the ``first`` markers the emitters place on packet
    starts and on every logical-idle filler word), maps the Gen1 K-code
    framing to Gen2 symbols at enqueue time, converts a DATA-type header
    to DPHSTART framing with the two 2-byte length-field replicas
    appended,
    and serves complete packets to the block transmitter one 8-symbol
    beat at a time, gaplessly.
    """

    def __init__(self, depth=512, words=1):
        # Width program (usb3_design.md 13.5): ``words=2`` captures the
        # 64-bit link stream and serves whole 128-bit blocks (1 beat =
        # 1 block at 78.125).  The wide grammar is SIMPLER in places:
        # the DPH decision needs no patch dance (HPSTART and dw0 share
        # the first word), and the [DW3|DPPSTART] word of a data header
        # takes a single-cycle 12-byte append with the length-replica
        # pair spliced between the halves.
        self._depth = depth
        self._words = words

        self.sink         = USBRawSuperSpeedStream(payload_words=4 * words)

        # Beat interface toward the block transmitter.
        self.beat_request = Signal()    # i: emit one data beat now
        self.beat_data    = Signal(64 * words)  # o: content or idle fill
        # A packet is straddling the current block boundary: its first
        # beat has been served but its final (eop) beat has not.  The
        # scheduler defers SKP OS insertion while set -- "SKP Ordered
        # Sets shall not be inserted within any packet" [6.4.3.3].
        self.pkt_in_flight = Signal()

        # Debug.
        self.packets_buffered = Signal(8)

    def elaborate(self, platform):
        m = Module()

        if self._words == 2:
            return self._elaborate_wide(m)

        sink = self.sink

        # FIFO entries: {eop, beat[63:0]}.
        m.submodules.fifo = fifo = DomainRenamer({"sync": "ss"})(
            SyncFIFO(width=65, depth=self._depth))

        # ── symbol translation ────────────────────────────────────────
        #
        # Bytes following an EPF within the same word are the Gen1
        # transmitter's post-packet IDL filler (unaligned DPP tails,
        # FINISH_DPP): they must become Gen2 Idle Symbols (5Ah), not
        # 00h.  EPF mid-packet (HPSTART/DPPSTART/LCSTART) is always the
        # word's last byte, so this never touches packet content.
        word_syms = []
        after_epf = C(0, 1)
        for i in range(4):
            sym = Signal(8, name=f"txsym{i}")
            byte_val = sink.data.word_select(i, 8)
            is_epf = sink.ctrl[i] & (byte_val == K_EPF)
            with m.If(after_epf):
                m.d.comb += sym.eq(G2_IDL)
            with m.Elif(sink.ctrl[i]):
                with m.Switch(byte_val):
                    for k, g2 in K_TO_G2.items():
                        with m.Case(k):
                            m.d.comb += sym.eq(g2)
                    with m.Default():
                        m.d.comb += sym.eq(G2_IDL)
            with m.Else():
                m.d.comb += sym.eq(byte_val)
            word_syms.append(sym)
            after_epf = after_epf | is_epf

        # ── enqueue: byte-granular packet capture ─────────────────────
        #
        # ``acc`` is a top-aligned 6-byte buffer (byte 0 -- first on the
        # wire -- in bits [40:48]).  Words append 4 bytes; the DPH
        # replica pair appends 4; whenever 8 bytes are available a beat
        # is written.  After the replica-pair insertion the byte phase
        # re-aligns (20+4) --
        # legal at Gen2 (framing is grammar-recognized, not aligned).

        in_packet   = Signal()
        byte_index  = Signal(11)          # byte position within packet
        is_dph      = Signal()            # HPSTART seen; awaiting dw0
        dph         = Signal()            # confirmed DATA-type header
        dw1_len     = Signal(16)          # dw1[16:32] = DPP length field

        acc     = Signal(48)
        acc_cnt = Signal(range(7))        # 0/2/4/6 bytes

        pkts_in  = Signal()
        pkts_out = Signal()
        with m.If(pkts_in & ~pkts_out):
            m.d.ss += self.packets_buffered.eq(self.packets_buffered + 1)
        with m.Elif(pkts_out & ~pkts_in):
            m.d.ss += self.packets_buffered.eq(self.packets_buffered - 1)

        word_is_idle  = (sink.data == 0) & (sink.ctrl == 0)
        starts_packet = sink.first & ~word_is_idle
        word_bytes    = Cat(word_syms[3], word_syms[2],
                            word_syms[1], word_syms[0])   # 32b, byte0 high

        # Padded flush beat for the current accumulator content.
        pad_beat = Signal(64)
        m.d.comb += pad_beat.eq(Const(IDLE_BEAT, 64))
        with m.Switch(acc_cnt):
            with m.Case(2):
                m.d.comb += pad_beat[48:64].eq(acc[32:48])
            with m.Case(4):
                m.d.comb += pad_beat[32:64].eq(acc[16:48])
            with m.Case(6):
                m.d.comb += pad_beat[16:64].eq(acc[0:48])

        def close_packet():
            """Flush the open packet with an eop-marked beat."""
            with m.If(acc_cnt != 0):
                m.d.comb += [
                    fifo.w_data.eq(Cat(pad_beat, C(1, 1))),
                    fifo.w_en.eq(1),
                    pkts_in.eq(1),
                ]
            with m.Else():
                m.d.comb += [
                    fifo.w_data.eq(Cat(Const(IDLE_BEAT, 64), C(1, 1))),
                    fifo.w_en.eq(1),
                    pkts_in.eq(1),
                ]
            m.d.ss += [in_packet.eq(0), acc.eq(0), acc_cnt.eq(0)]

        def append_bytes(n_bytes, payload):
            """Append 2 or 4 bytes (as a Value, byte 0 in the top bits)
            to the accumulator, emitting a beat when 8 are available."""
            width = 8 * n_bytes
            for cnt in (0, 2, 4, 6):
                total = cnt + n_bytes
                with m.If(acc_cnt == cnt):
                    if total < 8:
                        # accumulate only
                        m.d.ss += [
                            acc[48 - 8 * total:48 - 8 * cnt]
                                .eq(payload[0:width]),
                            acc_cnt.eq(total),
                        ]
                    else:
                        spill = total - 8            # 0 or 2 bytes
                        keep  = n_bytes - spill      # bytes into the beat
                        beat = Signal(64, name=f"beat_c{cnt}")
                        m.d.comb += beat.eq(Const(IDLE_BEAT, 64))
                        if cnt:
                            m.d.comb += beat[64 - 8 * cnt:64] \
                                .eq(acc[48 - 8 * cnt:48])
                        m.d.comb += beat[64 - 8 * (cnt + keep):64 - 8 * cnt]\
                            .eq(payload[width - 8 * keep:width])
                        m.d.comb += [
                            fifo.w_data.eq(Cat(beat, C(0, 1))),
                            fifo.w_en.eq(1),
                        ]
                        if spill:
                            m.d.ss += [
                                acc.eq(0),
                                acc[48 - 8 * spill:48]
                                    .eq(payload[0:8 * spill]),
                                acc_cnt.eq(spill),
                            ]
                        else:
                            m.d.ss += [acc.eq(0), acc_cnt.eq(0)]

        with m.FSM(domain="ss", name="enq_fsm"):

            with m.State("RUN"):
                m.d.comb += sink.ready.eq(fifo.w_rdy)

                with m.If(sink.valid & fifo.w_rdy):

                    with m.If(sink.first & in_packet):
                        # Packet boundary (idle filler or next packet's
                        # start): close the open packet first.  A new
                        # packet's start word is replayed next cycle.
                        close_packet()
                        with m.If(starts_packet):
                            m.d.comb += sink.ready.eq(0)

                    with m.Elif(starts_packet):
                        # Open a new packet with this word.
                        m.d.ss += [
                            in_packet.eq(1),
                            byte_index.eq(4),
                            is_dph.eq(sink.data == HPSTART_WORD),
                            dph.eq(0),
                        ]
                        append_bytes(4, word_bytes)

                    with m.Elif(in_packet):
                        # Continuation word.

                        # DPH decision on dw0 (bytes 4-7): patch the
                        # buffered HPSTART framing (still in acc --
                        # acc_cnt is 4 here, no beat written yet) to
                        # DPHSTART.
                        with m.If(is_dph & (byte_index == 4)):
                            m.d.ss += is_dph.eq(0)
                            with m.If(sink.data[0:5] == 8):   # DATA type
                                m.d.ss += [
                                    dph.eq(1),
                                    # patch acc bytes 0-2: 9A -> 95
                                    acc[40:48].eq(G2_DPHP),
                                    acc[32:40].eq(G2_DPHP),
                                    acc[24:32].eq(G2_DPHP),
                                ]

                        # Latch dw1's length field as it passes.
                        with m.If(byte_index == 8):
                            m.d.ss += dw1_len.eq(sink.data[16:32])

                        append_bytes(4, word_bytes)
                        m.d.ss += byte_index.eq(byte_index + 4)

                        # After byte 19 of a DATA-type header (HPSTART +
                        # 3 DWs + crc16/lcw = 20 bytes), insert the TWO
                        # 2-byte length replicas -- the 24-byte
                        # non-deferred Gen2 DPH of Figure 7-4
                        # [7.2.1.1].  (Bug #48: a single replica made
                        # every device DPH 22 bytes; the real xHC
                        # parsed our DPPSTART framing as the second
                        # replica -- "the two length field replica is
                        # not identical" [7.2.4.1.6] -- and rejected
                        # the DP: descriptor read/8 EPROTO -71 at
                        # stable 10G U0, sim-green because the bench
                        # host shared the misreading.)
                        with m.If(dph & (byte_index == 16)):
                            m.next = "REPLICA"

                    # (bare idle filler with no packet open: dropped.)

            with m.State("REPLICA"):
                m.d.comb += sink.ready.eq(0)
                with m.If(fifo.w_rdy):
                    # replica x2 = length field, LSB first, twice.
                    # 20 header bytes + 4 = 24: the DPP framing that
                    # follows re-aligns to the word phase.
                    append_bytes(4, Cat(dw1_len[8:16], dw1_len[0:8],
                                        dw1_len[8:16], dw1_len[0:8]))
                    m.d.ss += [byte_index.eq(byte_index + 4), dph.eq(0)]
                    m.next = "RUN"

        # NOTE on the DPHSTART patch window: the packet's first beat is
        # only written once 8 bytes are available, i.e. together with
        # dw0's word -- at which point the patch above has already
        # rewritten the framing bytes in ``acc`` *this same cycle*.
        # Since both are m.d.ss assignments to different bits the patch
        # must instead override the beat being written: handled by
        # patching the outgoing beat combinationally below.
        #
        # (The append_bytes(4) call for dw0 emits the packet's first
        # beat from acc[..] -- which still holds the unpatched 9A
        # symbols.  Rewrite them on the way out.)
        patch_beat = Signal()
        m.d.comb += patch_beat.eq(
            in_packet & is_dph & (byte_index == 4) & sink.valid
            & fifo.w_rdy & (sink.data[0:5] == 8))
        with m.If(patch_beat & fifo.w_en):
            m.d.comb += [
                fifo.w_data[56:64].eq(G2_DPHP),
                fifo.w_data[48:56].eq(G2_DPHP),
                fifo.w_data[40:48].eq(G2_DPHP),
            ]

        # ── drain: gapless per-packet bursting ───────────────────────
        #
        # ``beat_data`` is presented from a 1-deep PREFETCH register
        # (156.25 timing: the FIFO's read data otherwise reaches the
        # scheduler's tx_data mux and the PIPE adapter's capture
        # registers in one hop).  Gaplessness holds: a packet's first
        # beat is prefetched only once the WHOLE packet is queued
        # (packets_buffered accounting), so mid-packet refills always
        # find the FIFO ready and the head register refills on the same
        # cycle it is consumed.
        head_v    = Signal()
        head_data = Signal(64)
        head_eop  = Signal()
        mid_pkt   = Signal()      # head held a non-final beat: continue

        m.d.comb += self.beat_data.eq(
            Mux(head_v, head_data, Const(IDLE_BEAT, 64)))

        consume = self.beat_request & head_v

        # Packet-straddle tracking for the SKP scheduler: in flight from
        # the first served beat of a packet until its eop beat is served.
        with m.If(consume):
            m.d.ss += self.pkt_in_flight.eq(~head_eop)
        with m.If(~head_v | consume):
            with m.If(fifo.r_rdy
                      & (mid_pkt | (self.packets_buffered != 0))):
                m.d.ss += [
                    head_v   .eq(1),
                    head_data.eq(fifo.r_data[0:64]),
                    head_eop .eq(fifo.r_data[64]),
                    mid_pkt  .eq(~fifo.r_data[64]),
                ]
                m.d.comb += [
                    fifo.r_en.eq(1),
                    pkts_out .eq(fifo.r_data[64]),
                ]
            with m.Else():
                m.d.ss += head_v.eq(0)

        return m


    def _elaborate_wide(self, m):
        """ The words=2 bridge: 64-bit link words in, 128-bit block
        beats out.  Enqueue grammar (byte positions within a packet):

          word 0 [HPSTART|DW0]  -- the DPH decision AND the framing
                                   patch happen at capture (dw0 rides
                                   the same word);
          word 1 [DW1|DW2]      -- dw1's length field latched;
          word 2 [DW3|DPPSTART] (data header) -- a single 12-byte
                                   append: DW3, the length-replica pair,
                                   DPPSTART.  24-byte Gen2 DPH + framing
                                   = 28 bytes: payload runs at byte
                                   phase 12 of the 16-byte beats;
                 [DW3|pad]      (other headers) -- only the DW3 half is
                                   appended; the transmitter's trailing
                                   half-beat pad is DROPPED (the close
                                   flush pads with Gen2 idle).
          further words          -- payload, 8 bytes each; post-END
                                   filler becomes Gen2 idle via the
                                   terminator-qualified EPF rule below.
        """
        sink = self.sink

        # FIFO entries: {eop, block[127:0]}.
        m.submodules.fifo = fifo = DomainRenamer({"sync": "ss"})(
            SyncFIFO(width=129, depth=self._depth))

        # ── symbol translation (8 lanes) ──────────────────────────────
        #
        # The Gen1->Gen2 K mapping as at words=1; the POST-PACKET filler
        # rule is qualified: only bytes following an EPF whose PRECEDING
        # symbol is END or EDB (a packet terminator) become Gen2 Idle --
        # a framing EPF (HPSTART/DPPSTART/LCSTART, preceded by
        # SHP/SDP/SLC) may now sit mid-word with real content after it.
        # The terminator can end exactly at a word boundary (EPF at
        # byte 0 of the next word): track the last symbol's
        # END/EDB-ness across words.
        prev_was_term = Signal()   # last byte of the previous word

        word_syms = []
        after_end_epf = C(0, 1)
        prev_term = prev_was_term
        for i in range(8):
            sym = Signal(8, name=f"txsym{i}")
            byte_val = sink.data.word_select(i, 8)
            is_epf  = sink.ctrl[i] & (byte_val == K_EPF)
            is_term = sink.ctrl[i] & ((byte_val == K_END)
                                      | (byte_val == K_EDB))
            with m.If(after_end_epf):
                m.d.comb += sym.eq(G2_IDL)
            with m.Elif(sink.ctrl[i]):
                with m.Switch(byte_val):
                    for k, g2 in K_TO_G2.items():
                        with m.Case(k):
                            m.d.comb += sym.eq(g2)
                    with m.Default():
                        m.d.comb += sym.eq(G2_IDL)
            with m.Else():
                m.d.comb += sym.eq(byte_val)
            word_syms.append(sym)
            after_end_epf = after_end_epf | (is_epf & prev_term)
            prev_term = is_term
        with m.If(sink.valid & sink.ready):
            m.d.ss += prev_was_term.eq(
                sink.ctrl[7] & ((sink.data[56:64] == K_END)
                                | (sink.data[56:64] == K_EDB)))

        # ── enqueue: byte-granular capture into 16-byte beats ────────
        #
        # ``acc`` is a top-aligned 12-byte buffer (byte 0 in bits
        # [88:96]); appends are 4, 8 or 12 bytes; whenever 16 are
        # available a block is written (at most one w_en per cycle:
        # 12 + 12 = 24 -> one block + 8 spill).
        in_packet  = Signal()
        byte_index = Signal(11)
        dph        = Signal()
        dw1_len    = Signal(16)

        acc     = Signal(96)
        acc_cnt = Signal(range(13))       # 0/4/8/12

        pkts_in  = Signal()
        pkts_out = Signal()
        with m.If(pkts_in & ~pkts_out):
            m.d.ss += self.packets_buffered.eq(self.packets_buffered + 1)
        with m.Elif(pkts_out & ~pkts_in):
            m.d.ss += self.packets_buffered.eq(self.packets_buffered - 1)

        word_is_idle  = (sink.data == 0) & (sink.ctrl == 0)
        starts_packet = sink.first & ~word_is_idle
        # Byte 0 first-on-the-wire = TOP byte of the packed value.
        word_bytes = Cat(*reversed(word_syms))              # 64b
        low_bytes  = Cat(*reversed(word_syms[0:4]))         # 32b (syms 0-3)
        high_bytes = Cat(*reversed(word_syms[4:8]))         # 32b (syms 4-7)

        # Padded flush beat for the current accumulator content.
        pad_beat = Signal(128)
        m.d.comb += pad_beat.eq(Const(IDLE_BLOCK, 128))
        with m.Switch(acc_cnt):
            for cnt in (4, 8, 12):
                with m.Case(cnt):
                    m.d.comb += pad_beat[128 - 8 * cnt:128] \
                        .eq(acc[96 - 8 * cnt:96])

        def close_packet():
            m.d.comb += [
                fifo.w_data.eq(Cat(pad_beat, C(1, 1))),
                fifo.w_en.eq(1),
                pkts_in.eq(1),
            ]
            m.d.ss += [in_packet.eq(0), acc.eq(0), acc_cnt.eq(0)]

        def append_bytes(n_bytes, payload):
            """Append 4, 8 or 12 bytes (byte 0 in the top bits),
            emitting a block when 16 are available."""
            width = 8 * n_bytes
            for cnt in (0, 4, 8, 12):
                total = cnt + n_bytes
                with m.If(acc_cnt == cnt):
                    if total < 16:
                        m.d.ss += [
                            acc[96 - 8 * total:96 - 8 * cnt]
                                .eq(payload[0:width]),
                            acc_cnt.eq(total),
                        ]
                    else:
                        spill = total - 16
                        keep  = n_bytes - spill
                        beat = Signal(128, name=f"wbeat_c{cnt}_{n_bytes}")
                        m.d.comb += beat.eq(Const(IDLE_BLOCK, 128))
                        if cnt:
                            m.d.comb += beat[128 - 8 * cnt:128] \
                                .eq(acc[96 - 8 * cnt:96])
                        m.d.comb += \
                            beat[128 - 8 * (cnt + keep):128 - 8 * cnt] \
                            .eq(payload[width - 8 * keep:width])
                        m.d.comb += [
                            fifo.w_data.eq(Cat(beat, C(0, 1))),
                            fifo.w_en.eq(1),
                        ]
                        if spill:
                            m.d.ss += [
                                acc.eq(0),
                                acc[96 - 8 * spill:96]
                                    .eq(payload[0:8 * spill]),
                                acc_cnt.eq(spill),
                            ]
                        else:
                            m.d.ss += [acc.eq(0), acc_cnt.eq(0)]

        m.d.comb += sink.ready.eq(fifo.w_rdy)

        with m.If(sink.valid & fifo.w_rdy):

            with m.If(sink.first & in_packet):
                # Packet boundary: close the open packet; a new
                # packet's start word replays next cycle (not consumed).
                close_packet()
                with m.If(starts_packet):
                    m.d.comb += sink.ready.eq(0)

            with m.Elif(starts_packet):
                is_hp = sink.data[0:32] == HPSTART_HALF
                is_dp = is_hp & (sink.data[32:37] == 8)     # DATA type
                m.d.ss += [
                    in_packet.eq(1),
                    byte_index.eq(8),
                    dph.eq(is_dp),
                ]
                # The DPHSTART patch at capture: framing symbols 0-2
                # become 95h for a data header.
                patched = Signal(64)
                m.d.comb += patched.eq(word_bytes)
                with m.If(is_dp):
                    m.d.comb += [
                        patched[56:64].eq(G2_DPHP),
                        patched[48:56].eq(G2_DPHP),
                        patched[40:48].eq(G2_DPHP),
                    ]
                append_bytes(8, patched)

            with m.Elif(in_packet):
                with m.If(byte_index == 8):
                    m.d.ss += dw1_len.eq(sink.data[16:32])
                    append_bytes(8, word_bytes)
                with m.Elif(dph & (byte_index == 16)):
                    # [DW3|DPPSTART] + the replica pair in one go.
                    rep = Cat(dw1_len[8:16], dw1_len[0:8],
                              dw1_len[8:16], dw1_len[0:8])
                    m.d.ss += dph.eq(0)
                    append_bytes(12, Cat(high_bytes, rep, low_bytes))
                with m.Elif(~dph & (byte_index == 16)):
                    # Final header word of a non-data packet: only the
                    # DW3 half is content; the pad half is dropped.
                    append_bytes(4, low_bytes)
                with m.Else():
                    append_bytes(8, word_bytes)
                m.d.ss += byte_index.eq(byte_index + 8)

            # (bare idle filler with no packet open: dropped.)

        # ── drain: gapless per-packet bursting (as at words=1) ───────
        head_v    = Signal()
        head_data = Signal(128)
        head_eop  = Signal()
        mid_pkt   = Signal()

        m.d.comb += self.beat_data.eq(
            Mux(head_v, head_data, Const(IDLE_BLOCK, 128)))

        consume = self.beat_request & head_v

        with m.If(consume):
            m.d.ss += self.pkt_in_flight.eq(~head_eop)
        with m.If(~head_v | consume):
            with m.If(fifo.r_rdy
                      & (mid_pkt | (self.packets_buffered != 0))):
                m.d.ss += [
                    head_v   .eq(1),
                    head_data.eq(fifo.r_data[0:128]),
                    head_eop .eq(fifo.r_data[128]),
                    mid_pkt  .eq(~fifo.r_data[128]),
                ]
                m.d.comb += [
                    fifo.r_en.eq(1),
                    pkts_out .eq(fifo.r_data[128]),
                ]
            with m.Else():
                m.d.ss += head_v.eq(0)

        return m


class Gen2BlockTransmitter(Elaboratable):
    """Gen2 block scheduler + ordered-set generator (stage A).

    Emits 128b/132b blocks on the 64-bit PIPE per the LTSSM's requests:
    TSEQ bursts (SYNC every 16,384), TS1/TS2 bursts (SYNC every 32,
    burst_complete every 16 -- the Gen1 TSTransceiver cadence the LTSSM
    expects), a single SDS on idle-mode entry, then data blocks from the
    TX bridge with SKP OS inserted at the 1-per-40-blocks average
    [6.4.3.3].  Symbols 14/15 of TS ordered sets are transmitted as
    identifier symbols (receivers must exclude them from matching; the
    DC-balance variant is a Phase-5 refinement).
    """

    def __init__(self, *, tseq_count=524288, ts_per_burst=16,
                 sync_every_ts=32, sync_every_tseq=16384,
                 skp_interval=40, words=1):
        self._tseq_count      = tseq_count
        self._ts_per_burst    = ts_per_burst
        self._sync_every_ts   = sync_every_ts
        self._sync_every_tseq = sync_every_tseq
        self._skp_interval    = skp_interval
        # Width program (usb3_design.md 13.3): ``words=2`` emits ONE
        # whole 128-bit block per beat at the pclk/2 core clock; the
        # 24-symbol SKP OS goes out as one full beat plus a HALF beat
        # (symbols 16-23 in the data register's TOP lanes -- the lanes
        # symbols 0-7 of a normal beat occupy) flagged ``tx_halfbeat``.
        # The pacing reference stays in PHY-word (64-bit) units: a full
        # beat supplies 2 words, a halfbeat 1.
        self._words = words

        # Stream from the link layer (through the physical layer).
        self.sink             = USBRawSuperSpeedStream(payload_words=4 * words)

        # LTSSM controls.
        self.send_tseq_burst  = Signal()
        self.send_ts1_burst   = Signal()
        self.send_ts2_burst   = Signal()
        self.idle_mode        = Signal()   # SDS-once + data blocks
        self.request_hot_reset      = Signal()
        self.request_no_scrambling  = Signal()

        self.burst_complete   = Signal()   # strobe (TS cadence)

        # PIPE block interface.
        self.tx_data          = Signal(64 * words)
        self.tx_head          = Signal(4)
        self.tx_start         = Signal()
        self.tx_valid         = Signal()
        if words == 2:
            self.tx_halfbeat  = Signal()

        # PHY TX gearbox FIFO occupancy (TxFifoWrNum): the closed-loop
        # pacing reference (bug #44; see the pacing section below).
        self.tx_fifo_level    = Signal(5)

        # Debug.
        self.packets_buffered = Signal(8)

    def elaborate(self, platform):
        m = Module()

        if self._words == 2:
            return self._elaborate_wide(m)

        # The bridge is held in reset while any training-class burst
        # runs: training means the link is (re)training, and every
        # packet the bridge holds -- complete queued packets AND a
        # partial capture cut mid-construct by the link layer's
        # ResetInserter discipline -- belongs to the dead link session.
        # The historical bridge carried a truncated LC fragment across
        # the retrain and flushed it (close-on-next-``first``, padded
        # with Gen2 idle) onto the fresh link AHEAD of the header
        # sequence advertisement; the fragment [SLC SLC SLC EPF][5A x4]
        # even aliases a REPLICA-VALID link command (both halves
        # 0x5A5A) (test_gen2_tx_seams red).  Retransmission of real
        # headers is the LINK layer's job [7.2.4.1.x rule 7]; the
        # bridge copy is a stale duplicate.  The level-held reset also
        # swallows any skid-stage residue that drains in while the
        # retrain runs.
        training = (self.send_tseq_burst | self.send_ts1_burst
                    | self.send_ts2_burst)
        m.submodules.bridge = bridge = \
            ResetInserter({"ss": training})(Gen2TxBridge())
        m.d.comb += [
            bridge.sink.stream_eq(self.sink),
            self.packets_buffered.eq(bridge.packets_buffered),
        ]

        # Block kinds.
        K_TSEQ, K_TS1, K_TS2, K_SYNC, K_SDS, K_SKP, K_DATA = range(7)

        kind      = Signal(range(7))
        beat_idx  = Signal(2)              # 0/1 (0/1/2 for SKP)
        os_count  = Signal(range(max(self._tseq_count, 65536) + 1))
        sync_gap  = Signal(range(self._sync_every_tseq + 1))
        skp_gap   = Signal(range(2 * self._skp_interval + 1))

        # SDS arming is LEVEL-based [7.5.4.10: a single SDS before the
        # first data block]: armed out of reset and re-armed by any
        # training-class block we transmit (training implies the data
        # stream ended); consumed when the SDS block is emitted.  The
        # historical idle-mode EDGE detector had two request-seam
        # hazards (test_gen2_tx_seams red): a 1-cycle idle_mode blip
        # re-armed it mid-U0 (a spurious SDS inside the data stream),
        # and an arm coinciding with an inactive cycle was killed by
        # the state wipe below (no SDS at all -- the write-ordering
        # coincidence that happened to mask the blip re-arm).
        sds_pending = Signal(init=1)

        # Registered activity gate (156.25: the LTSSM burst-request seam
        # registers otherwise reach the scheduler/bridge FIFO controls
        # through this OR in one hop).  One cycle of TX start/stop
        # latency against microsecond burst tolerances.
        active = Signal()
        m.d.ss += active.eq(self.send_tseq_burst | self.send_ts1_burst |
                            self.send_ts2_burst | self.idle_mode)

        # TS/TSEQ mode tracking (counter resets on changes).
        mode = Signal(2)   # 0 none/idle, 1 tseq, 2 ts1, 3 ts2
        new_mode = Signal(2)
        m.d.comb += new_mode.eq(
            Mux(self.send_tseq_burst, 1,
                Mux(self.send_ts1_burst, 2,
                    Mux(self.send_ts2_burst, 3, 0))))

        # TS blocks' symbol 5 configuration (link functionality bits:
        # bit0 reset, bit2 loopback, bit3 disable scrambling).
        ts_config = Signal(8)
        m.d.comb += ts_config.eq(Cat(self.request_hot_reset, C(0, 2),
                                     self.request_no_scrambling, C(0, 4)))

        def ts_beat0(ident):
            base = [ident] * 8
            base[4] = 0
            base[5] = 0
            out = Signal(64, name=f"ts{ident:02x}_beat0")
            m.d.comb += out.eq(Const(syms_to_beat(base), 64))
            # symbol 5 sits at bits [16:24]
            m.d.comb += out[16:24].eq(ts_config)
            return out

        TSEQ_BEAT0 = Const(syms_to_beat(
            [TSEQ_ID] * 4 + [0, 0] + [TSEQ_ID] * 2), 64)
        TSEQ_BEAT1 = Const(syms_to_beat([TSEQ_ID] * 8), 64)
        TS1_BEAT1  = Const(syms_to_beat([TS1_ID] * 8), 64)
        TS2_BEAT1  = Const(syms_to_beat([TS2_ID] * 8), 64)
        SYNC_BEAT  = Const(syms_to_beat([0x00, 0xFF] * 4), 64)
        SDS_BEAT0  = Const(syms_to_beat([SDS_ID] * 4 + [0x55] * 4), 64)
        SDS_BEAT1  = Const(syms_to_beat([0x55] * 8), 64)
        SKP_BEAT01 = Const(syms_to_beat([SKP_SYM] * 8), 64)
        SKP_BEAT2  = Const(syms_to_beat(
            [SKP_SYM] * 4 + [SKPEND, 0, 0, 0]), 64)

        # ── TX beat pacing (the PHY gearbox rate match) ──────────────
        #
        # 64-bit beats at 156.25 MHz supply payload at exactly 10.0
        # Gb/s, but the 128b/132b wire carries only 128 payload bits per
        # 132 wire bits: an unpaced stream overflows the PHY's 32-deep
        # TX gearbox FIFO after ~7 us.  The session-13 OPEN-LOOP pacing
        # (one dead beat per 16 blocks) matched the long-term rates
        # EXACTLY -- and that exactness was bug #44: with supply == 
        # drain, the FIFO level stays wherever the stream-start race
        # left it (0..2 beats), so the PHY's TxGearbox132 rides its
        # UNDERFLOW boundary permanently.  Whenever the supply-gap and
        # drain-gap phases misaligned, the FIFO ran empty mid-block and
        # the gearbox serialized stale bits: intermittent device->host
        # corruption, dependent on per-boot phase luck (silicon: ~5
        # host-initiated recoveries/s at Gen2 U0 with ZERO inbound
        # header CRC errors; some boots reached descriptor reads with
        # EPROTO -71, others died in the port-config/hot-reset windows).
        # The vendor MAC runs this FIFO NEAR-FULL, closed-loop on
        # TxFifoWrNum -- the PHY's TX path is only silicon-proven in
        # that regime.
        #
        # Closed loop: stream gaplessly (supply rate 1.0 > wire drain
        # 0.9697, the FIFO fills monotonically) until ``tx_fifo_level``
        # reaches PACE_THRESHOLD, then insert dead beats at block
        # boundaries while it stays there.  Steady state hovers at the
        # threshold (16 +2/-2 with the ~2-cycle TxFifoWrNum register
        # lag): never empty (16-beat cushion), never full (32-cap
        # headroom).  Guarded by tests/test_gen2_pacing.py and the
        # link sims' FIFO model (prefill + zero-starvation asserts);
        # TxFifoWrNum probes confirm on silicon.
        PACE_THRESHOLD = 16
        pace_due = Signal()
        m.d.comb += pace_due.eq(self.tx_fifo_level >= PACE_THRESHOLD)

        # The emission gate stays up mid-block even if ``active`` blips
        # low (DRAIN-SAFE: a request-seam gap must never truncate a
        # 132-bit block on the PIPE -- the PHY gearbox would emit a
        # malformed block and desynchronize the host's receiver; the
        # block boundary arm below is only reachable with ``active``
        # high, so a true stop quiesces at the next boundary).
        with m.If((active | (beat_idx != 0))
                  & ~(pace_due & (beat_idx == 0))):
            m.d.comb += self.tx_valid.eq(1)

            with m.If(beat_idx == 0):
                # ── block boundary: choose and start the next block ──
                m.d.comb += self.tx_start.eq(1)
                m.d.ss += beat_idx.eq(1)

                with m.If(new_mode != mode):
                    m.d.ss += [mode.eq(new_mode), os_count.eq(0),
                               sync_gap.eq(0)]

                # Any training-class block (re-)arms the single SDS for
                # the next data-stream start.
                with m.If(new_mode != 0):
                    m.d.ss += sds_pending.eq(1)

                # SKP OS first when scheduled -- but NEVER inside a
                # packet ("SKP Ordered Sets shall not be inserted within
                # any packet" [6.4.3.3]; the real xHC rejects the split
                # DP -- session-13 bench finding, descriptor read
                # error -71).  While a packet straddles the boundary the
                # gap keeps accumulating and the SKP goes out at the
                # first legal boundary (the spec allows buffering up to
                # three SKP OS, and our interval counter serves the same
                # averaging purpose).
                with m.If((skp_gap >= self._skp_interval)
                          & ~bridge.pkt_in_flight):
                    m.d.ss += [kind.eq(K_SKP), skp_gap.eq(0)]
                    m.d.comb += [self.tx_head.eq(BLOCK_CONTROL),
                                 self.tx_data.eq(SKP_BEAT01)]
                with m.Else():
                    with m.If(skp_gap < (self._skp_interval * 2)):
                        m.d.ss += skp_gap.eq(skp_gap + 1)

                    with m.If(new_mode == 1):        # TSEQ
                        with m.If(sync_gap >= self._sync_every_tseq):
                            m.d.ss += [kind.eq(K_SYNC), sync_gap.eq(0)]
                            m.d.comb += [self.tx_head.eq(BLOCK_CONTROL),
                                         self.tx_data.eq(SYNC_BEAT)]
                        with m.Else():
                            m.d.ss += [kind.eq(K_TSEQ),
                                       sync_gap.eq(sync_gap + 1)]
                            m.d.comb += [self.tx_head.eq(BLOCK_CONTROL),
                                         self.tx_data.eq(TSEQ_BEAT0)]

                    with m.Elif((new_mode == 2) | (new_mode == 3)):
                        with m.If(sync_gap >= self._sync_every_ts):
                            m.d.ss += [kind.eq(K_SYNC), sync_gap.eq(0)]
                            m.d.comb += [self.tx_head.eq(BLOCK_CONTROL),
                                         self.tx_data.eq(SYNC_BEAT)]
                        with m.Else():
                            m.d.ss += sync_gap.eq(sync_gap + 1)
                            m.d.comb += self.tx_head.eq(BLOCK_CONTROL)
                            with m.If(new_mode == 2):
                                m.d.ss += kind.eq(K_TS1)
                                m.d.comb += self.tx_data.eq(
                                    ts_beat0(TS1_ID))
                            with m.Else():
                                m.d.ss += kind.eq(K_TS2)
                                m.d.comb += self.tx_data.eq(
                                    ts_beat0(TS2_ID))

                    with m.Elif(self.idle_mode):
                        with m.If(sds_pending):
                            m.d.ss += [kind.eq(K_SDS), sds_pending.eq(0)]
                            m.d.comb += [self.tx_head.eq(BLOCK_CONTROL),
                                         self.tx_data.eq(SDS_BEAT0)]
                        with m.Else():
                            m.d.ss += kind.eq(K_DATA)
                            m.d.comb += [
                                self.tx_head.eq(BLOCK_DATA),
                                self.tx_data.eq(bridge.beat_data),
                                bridge.beat_request.eq(1),
                            ]

            with m.Else():
                # ── continuation beat(s) ─────────────────────────────
                with m.Switch(kind):
                    with m.Case(K_TSEQ):
                        m.d.comb += [self.tx_head.eq(BLOCK_CONTROL),
                                     self.tx_data.eq(TSEQ_BEAT1)]
                    with m.Case(K_TS1):
                        m.d.comb += [self.tx_head.eq(BLOCK_CONTROL),
                                     self.tx_data.eq(TS1_BEAT1)]
                    with m.Case(K_TS2):
                        m.d.comb += [self.tx_head.eq(BLOCK_CONTROL),
                                     self.tx_data.eq(TS2_BEAT1)]
                    with m.Case(K_SYNC):
                        m.d.comb += [self.tx_head.eq(BLOCK_CONTROL),
                                     self.tx_data.eq(SYNC_BEAT)]
                    with m.Case(K_SDS):
                        m.d.comb += [self.tx_head.eq(BLOCK_CONTROL),
                                     self.tx_data.eq(SDS_BEAT1)]
                    with m.Case(K_SKP):
                        m.d.comb += self.tx_head.eq(BLOCK_CONTROL)
                        with m.If(beat_idx == 1):
                            m.d.comb += self.tx_data.eq(SKP_BEAT01)
                        with m.Else():
                            m.d.comb += self.tx_data.eq(SKP_BEAT2)
                    with m.Case(K_DATA):
                        m.d.comb += [
                            self.tx_head.eq(BLOCK_DATA),
                            self.tx_data.eq(bridge.beat_data),
                            bridge.beat_request.eq(1),
                        ]

                last_beat = Signal()
                m.d.comb += last_beat.eq(
                    Mux(kind == K_SKP, beat_idx == 2, beat_idx == 1))

                with m.If(last_beat):
                    m.d.ss += beat_idx.eq(0)

                    # Ordered-set accounting at block end.
                    with m.If(kind == K_TSEQ):
                        with m.If(os_count + 1 == self._tseq_count):
                            m.d.comb += self.burst_complete.eq(1)
                            m.d.ss += os_count.eq(0)
                        with m.Else():
                            m.d.ss += os_count.eq(os_count + 1)
                    with m.Elif((kind == K_TS1) | (kind == K_TS2)):
                        with m.If(os_count + 1 == self._ts_per_burst):
                            m.d.comb += self.burst_complete.eq(1)
                            m.d.ss += os_count.eq(0)
                        with m.Else():
                            m.d.ss += os_count.eq(os_count + 1)
                with m.Else():
                    m.d.ss += beat_idx.eq(beat_idx + 1)

        with m.Elif(active):
            # Rate-matching gap: hold the block boundary while the PHY
            # FIFO sits at the pacing threshold (tx_valid stays low;
            # the FIFO drains toward the cushion).
            pass

        with m.Else():
            # True stop (reachable only at a block boundary, see the
            # drain-safe gate above): clear the schedule state.
            # ``sds_pending`` is NOT touched here -- it is owned by the
            # level-based arming above (the historical clear raced the
            # same-cycle edge arm; write order decided who won).
            m.d.ss += [beat_idx.eq(0), mode.eq(0), os_count.eq(0),
                       sync_gap.eq(0), skp_gap.eq(0)]

        return m


    def _elaborate_wide(self, m):
        """ The words=2 scheduler: one whole block per beat.  All the
        words=1 scheduling decisions (mode tracking, SYNC cadence, SKP
        interval with the in-flight deferral, the level-armed single
        SDS, the drain-safe emission gate, the #44 closed-loop pacing)
        carry over -- only the beat sequencing changes: every block is
        a single beat, except the 24-symbol SKP OS = one beat plus a
        ``tx_halfbeat``-flagged half.
        """
        training = (self.send_tseq_burst | self.send_ts1_burst
                    | self.send_ts2_burst)
        m.submodules.bridge = bridge = \
            ResetInserter({"ss": training})(Gen2TxBridge(words=2))
        m.d.comb += [
            bridge.sink.stream_eq(self.sink),
            self.packets_buffered.eq(bridge.packets_buffered),
        ]

        K_SKP_TAIL = 1     # scheduler sub-state: SKP halfbeat pending

        skp_tail  = Signal()   # the halfbeat is the next emission
        os_count  = Signal(range(max(self._tseq_count, 65536) + 1))
        sync_gap  = Signal(range(self._sync_every_tseq + 1))
        skp_gap   = Signal(range(2 * self._skp_interval + 1))

        sds_pending = Signal(init=1)

        active = Signal()
        m.d.ss += active.eq(self.send_tseq_burst | self.send_ts1_burst |
                            self.send_ts2_burst | self.idle_mode)

        mode = Signal(2)
        new_mode = Signal(2)
        m.d.comb += new_mode.eq(
            Mux(self.send_tseq_burst, 1,
                Mux(self.send_ts1_burst, 2,
                    Mux(self.send_ts2_burst, 3, 0))))

        ts_config = Signal(8)
        m.d.comb += ts_config.eq(Cat(self.request_hot_reset, C(0, 2),
                                     self.request_no_scrambling, C(0, 4)))

        def ts_block(ident):
            base = [ident] * 16
            base[4] = 0
            base[5] = 0
            out = Signal(128, name=f"ts{ident:02x}_blk")
            m.d.comb += out.eq(Const(syms_to_block(base), 128))
            # symbol 5 sits at bits [80:88] (symbol 0 = top byte).
            m.d.comb += out[80:88].eq(ts_config)
            return out

        TSEQ_BLK = Const(syms_to_block(
            [TSEQ_ID] * 4 + [0, 0] + [TSEQ_ID] * 10), 128)
        SYNC_BLK = Const(syms_to_block([0x00, 0xFF] * 8), 128)
        SDS_BLK  = Const(syms_to_block([SDS_ID] * 4 + [0x55] * 12), 128)
        SKP_BLK  = Const(syms_to_block([SKP_SYM] * 16), 128)
        # The halfbeat's 8 symbols ride the TOP lanes (the same lanes a
        # normal beat's symbols 0-7 use); the low half is idle fill.
        SKP_TAIL_BLK = Const(syms_to_block(
            [SKP_SYM] * 4 + [SKPEND, 0, 0, 0] + [G2_IDL] * 8), 128)

        # ── the #44 closed-loop pacing, in PHY-word units ────────────
        # A full beat supplies 2 words to the PHY FIFO, a halfbeat 1;
        # the threshold keeps its word units (16 of 32).
        PACE_THRESHOLD = 16
        pace_due = Signal()
        m.d.comb += pace_due.eq(self.tx_fifo_level >= PACE_THRESHOLD)

        # Drain-safe gate: the SKP halfbeat must follow its beat (a
        # pacing gap between them would leave a malformed OS if the
        # LTSSM stopped): ``skp_tail`` keeps emission up like a
        # mid-block beat at words=1.
        with m.If((active | skp_tail) & ~(pace_due & ~skp_tail)):
            m.d.comb += self.tx_valid.eq(1)

            with m.If(skp_tail):
                # ── the SKP OS tail half ──
                m.d.comb += [
                    self.tx_head.eq(BLOCK_CONTROL),
                    self.tx_data.eq(SKP_TAIL_BLK),
                    self.tx_halfbeat.eq(1),
                    # No tx_start: the halfbeat extends the SKP block.
                ]
                m.d.ss += skp_tail.eq(0)

            with m.Else():
                # ── block boundary: choose and emit a whole block ──
                m.d.comb += self.tx_start.eq(1)

                with m.If(new_mode != mode):
                    m.d.ss += [mode.eq(new_mode), os_count.eq(0),
                               sync_gap.eq(0)]
                with m.If(new_mode != 0):
                    m.d.ss += sds_pending.eq(1)

                def os_tick(per_burst):
                    with m.If(os_count + 1 == per_burst):
                        m.d.comb += self.burst_complete.eq(1)
                        m.d.ss += os_count.eq(0)
                    with m.Else():
                        m.d.ss += os_count.eq(os_count + 1)

                with m.If((skp_gap >= self._skp_interval)
                          & ~bridge.pkt_in_flight):
                    m.d.ss += [skp_tail.eq(1), skp_gap.eq(0)]
                    m.d.comb += [self.tx_head.eq(BLOCK_CONTROL),
                                 self.tx_data.eq(SKP_BLK)]
                with m.Else():
                    with m.If(skp_gap < (self._skp_interval * 2)):
                        m.d.ss += skp_gap.eq(skp_gap + 1)

                    with m.If(new_mode == 1):        # TSEQ
                        with m.If(sync_gap >= self._sync_every_tseq):
                            m.d.ss += sync_gap.eq(0)
                            m.d.comb += [self.tx_head.eq(BLOCK_CONTROL),
                                         self.tx_data.eq(SYNC_BLK)]
                        with m.Else():
                            m.d.ss += sync_gap.eq(sync_gap + 1)
                            m.d.comb += [self.tx_head.eq(BLOCK_CONTROL),
                                         self.tx_data.eq(TSEQ_BLK)]
                            os_tick(self._tseq_count)

                    with m.Elif((new_mode == 2) | (new_mode == 3)):
                        with m.If(sync_gap >= self._sync_every_ts):
                            m.d.ss += sync_gap.eq(0)
                            m.d.comb += [self.tx_head.eq(BLOCK_CONTROL),
                                         self.tx_data.eq(SYNC_BLK)]
                        with m.Else():
                            m.d.ss += sync_gap.eq(sync_gap + 1)
                            m.d.comb += self.tx_head.eq(BLOCK_CONTROL)
                            with m.If(new_mode == 2):
                                m.d.comb += self.tx_data.eq(
                                    ts_block(TS1_ID))
                            with m.Else():
                                m.d.comb += self.tx_data.eq(
                                    ts_block(TS2_ID))
                            os_tick(self._ts_per_burst)

                    with m.Elif(self.idle_mode):
                        with m.If(sds_pending):
                            m.d.ss += sds_pending.eq(0)
                            m.d.comb += [self.tx_head.eq(BLOCK_CONTROL),
                                         self.tx_data.eq(SDS_BLK)]
                        with m.Else():
                            m.d.comb += [
                                self.tx_head.eq(BLOCK_DATA),
                                self.tx_data.eq(bridge.beat_data),
                                bridge.beat_request.eq(1),
                            ]

        with m.Elif(active):
            # Rate-matching gap (the FIFO drains toward the cushion).
            pass

        with m.Else():
            m.d.ss += [skp_tail.eq(0), mode.eq(0), os_count.eq(0),
                       sync_gap.eq(0), skp_gap.eq(0)]

        return m


class Gen2BlockReceiver(Elaboratable):
    """Gen2 block-level receiver (stage A).

    Classifies control blocks (TS1/TS2/TSEQ consecutive detection with
    symbol-14/15 exclusion and SYNC transparency; SDS detection) and
    translates the data-block symbol stream back into the Gen1 32-bit
    K-coded dialect for the unmodified link core.
    """

    def __init__(self, queue_depth=1024, out_depth=512, words=1):
        # Width program (usb3_design.md 13.5): ``words=2`` receives one
        # whole 128-bit block per beat (assembly trivializes), queues
        # 128-bit entries, walks them as FOUR 4-symbol quarters (the
        # grammar engine is unchanged), and presents the translated
        # stream as 64-bit beats through a 2:1 output packer.  The #43
        # queue-bound argument re-derives: entry arrival is still
        # O(constructs) (idle runs compress whole blocks), while the
        # engine's absolute drain per cycle is unchanged against a core
        # clock at HALF the rate -- the bound doubles, the default
        # depth keeps 4x headroom, and the sim asserts the level.
        self._queue_depth = queue_depth
        self._out_depth   = out_depth
        self._words       = words

        # PIPE block interface.
        self.rx_data      = Signal(64 * words)
        self.rx_head      = Signal(4)
        self.rx_start     = Signal()
        self.rx_valid     = Signal()

        # Ordered-set detection (Gen1 TSTransceiver-compatible strobes).
        self.tseq_detected = Signal()
        self.ts1_detected  = Signal()
        self.ts2_detected  = Signal()
        self.hot_reset_requested     = Signal()
        self.loopback_requested      = Signal()
        self.no_scrambling_requested = Signal()
        self.sds_detected  = Signal()   # strobe
        self.data_mode     = Signal()   # sticky: SDS seen, no TS since

        # Translated Gen1-dialect stream toward the link core.
        self.source        = USBRawSuperSpeedStream(payload_words=4 * words)

        # Debug (prunable bring-up taps).
        self.queue_level   = Signal(16)
        self.debug_state   = Signal(3)
        self.debug_have    = Signal()
        self.debug_wen     = Signal()
        self.debug_out_lvl = Signal(16)

    def elaborate(self, platform):
        m = Module()

        # Width-derived shapes.
        BEAT_W  = 64 * self._words        # queue/engine beat width
        HALVES  = 2 * self._words         # 4-symbol steps per beat
        IDLE_W  = IDLE_BLOCK if self._words == 2 else IDLE_BEAT

        # ── PIPE input registers ─────────────────────────────────────
        # The whole receiver works from a locally registered copy of the
        # PIPE RX beat (156.25 timing: the adapter's output registers
        # otherwise reach the enqueue idle-compare and the block
        # classifier in one routed hop).  One beat of RX latency is
        # immaterial everywhere downstream.
        rx_data  = Signal(64 * self._words)
        rx_head  = Signal(4)
        rx_start = Signal()
        rx_valid = Signal()
        m.d.ss += [
            rx_data .eq(self.rx_data),
            rx_head .eq(self.rx_head),
            rx_start.eq(self.rx_start),
            rx_valid.eq(self.rx_valid),
        ]

        # ── block assembly ────────────────────────────────────────────
        block_done = Signal()
        block_ctl  = Signal()
        b0 = Signal(64)
        b1 = Signal(64)

        if self._words == 2:
            # One beat = one whole block (start on every beat).
            with m.If(rx_valid & rx_start):
                m.d.comb += [
                    block_done.eq(1),
                    b0.eq(rx_data[64:128]),   # symbols 0-7 (top lanes)
                    b1.eq(rx_data[0:64]),     # symbols 8-15
                    block_ctl.eq(rx_head == BLOCK_CONTROL),
                ]
        else:
            beat0_data = Signal(64)
            have_beat0 = Signal()
            with m.If(rx_valid):
                with m.If(rx_start):
                    m.d.ss += [beat0_data.eq(rx_data), have_beat0.eq(1)]
                with m.Elif(have_beat0):
                    m.d.ss += have_beat0.eq(0)
                    m.d.comb += [
                        block_done.eq(1),
                        b0.eq(beat0_data),
                        b1.eq(rx_data),
                        block_ctl.eq(rx_head == BLOCK_CONTROL),
                    ]

        syms = [Signal(8, name=f"blk_sym{i}") for i in range(16)]
        for i in range(8):
            m.d.comb += syms[i].eq(b0[8 * (7 - i):8 * (8 - i)])
            m.d.comb += syms[8 + i].eq(b1[8 * (7 - i):8 * (8 - i)])

        def all_id(ident, indices):
            return Cat(*[syms[i] == ident for i in indices]).all()

        # TS matching: identifier symbols only, EXCLUDE symbols 14/15
        # [7.5.4.8.2]; symbol 4 is 0, symbol 5 carries configuration.
        core = [0, 1, 2, 3, 6, 7, 8, 9, 10, 11, 12, 13]
        is_ts1  = all_id(TS1_ID, core)
        is_ts2  = all_id(TS2_ID, core)
        is_tseq = all_id(TSEQ_ID, [0, 1, 2, 3]) & ~is_ts1 & ~is_ts2
        is_sync = ((syms[0] == 0x00) & (syms[1] == 0xFF)) | \
                  ((syms[0] == 0xFF) & (syms[1] == 0x00))
        is_sds  = all_id(SDS_ID, [0, 1, 2, 3])

        ts1_run  = Signal(range(9))
        ts2_run  = Signal(range(9))
        tseq_run = Signal(range(33))

        # Default: strobes idle; classification below overrides.
        m.d.ss += [self.ts1_detected.eq(0), self.ts2_detected.eq(0),
                   self.tseq_detected.eq(0), self.sds_detected.eq(0)]

        with m.If(block_done & block_ctl):
            with m.If(is_ts1):
                m.d.ss += [ts2_run.eq(0), tseq_run.eq(0),
                           self.data_mode.eq(0)]
                with m.If(ts1_run == 7):
                    m.d.ss += [self.ts1_detected.eq(1), ts1_run.eq(0)]
                with m.Else():
                    m.d.ss += ts1_run.eq(ts1_run + 1)
            with m.Elif(is_ts2):
                m.d.ss += [ts1_run.eq(0), tseq_run.eq(0),
                           self.data_mode.eq(0)]
                with m.If(ts2_run == 7):
                    m.d.ss += [self.ts2_detected.eq(1), ts2_run.eq(0)]
                with m.Else():
                    m.d.ss += ts2_run.eq(ts2_run + 1)
                m.d.ss += [
                    self.hot_reset_requested    .eq(syms[5][0]),
                    self.loopback_requested     .eq(syms[5][2]),
                    self.no_scrambling_requested.eq(syms[5][3]),
                ]
            with m.Elif(is_tseq):
                m.d.ss += [ts1_run.eq(0), ts2_run.eq(0),
                           self.data_mode.eq(0)]
                with m.If(tseq_run == 31):
                    m.d.ss += [self.tseq_detected.eq(1), tseq_run.eq(0)]
                with m.Else():
                    m.d.ss += tseq_run.eq(tseq_run + 1)
            with m.Elif(is_sync):
                # SYNC does not break TS consecutiveness [7.5.4.8.2].
                pass
            with m.Elif(is_sds):
                m.d.ss += [self.sds_detected.eq(1), self.data_mode.eq(1),
                           ts1_run.eq(0), ts2_run.eq(0), tseq_run.eq(0)]
        with m.Elif(block_done):
            # Data blocks break TS runs (SYNC/SKP do not).
            m.d.ss += [ts1_run.eq(0), ts2_run.eq(0), tseq_run.eq(0)]

        # ── data path: beat queue with idle RUN COMPRESSION ─────────
        #
        # Entries are 65 bits: {is_run, payload}.  A beat entry
        # (is_run=0) carries one non-idle 64-bit beat; a RUN entry
        # (is_run=1) carries a count of 1..RUN_MAX consecutive
        # whole-idle beats in payload[0:8].
        #
        # Bug #43 (the queue RATCHET): the historical scheme enqueued
        # every idle beat unless the engine was FULLY drained, and the
        # load-point discard drains at most ONE beat per cycle -- the
        # same rate idle beats arrive at mid-U0 (the Gen2 wire delivers
        # a data beat nearly every pclk).  The backlog therefore never
        # drained: every construct (boundary-stepped at ~1.3 sym/cycle
        # against an 8 sym/cycle wire) ratcheted the level up by ~5-8
        # beats FOREVER, unboundedly delaying delivery and finally
        # overflowing the queue (silent beat loss) under construct-dense
        # traffic.  Compressing idle runs makes queue-entry arrival
        # O(constructs) instead of O(beats): the drain always wins and
        # the level stays bounded by the handful of constructs in
        # flight.
        #
        # Order is exactly preserved: pending idles are flushed as one
        # run entry AHEAD of the non-idle beat that ends the run (that
        # beat parks one cycle in a 1-deep skid: the run flush owns the
        # write port; the skid can never deepen, because a new run can
        # only begin after an idle beat -- which needs no write slot --
        # retires the skid first).  Whole-idle beats can be construct
        # PAYLOAD (an all-5Ah DPP span), so runs are REPLAYED beat by
        # beat to the engine whenever it is mid-construct; only runs
        # met in SEARCH are discarded (whole run, one cycle).  A
        # mid-construct run that never sees a terminating non-idle beat
        # (corrupt wire) still flushes via the RUN_MAX cap.
        m.submodules.queue = queue = DomainRenamer({"sync": "ss"})(
            SyncFIFO(width=BEAT_W + 1, depth=self._queue_depth))

        engine_busy = Signal()   # grammar engine mid-construct
        beat_is_idle = rx_data == Const(IDLE_W, BEAT_W)
        beat_is_data = rx_valid & (rx_head == BLOCK_DATA) \
            & self.data_mode

        # (``queue_drained`` also covers the read-side prefetch skid --
        # a pending construct beat there means an incoming all-idle beat
        # may be construct PAYLOAD and must never be discarded.)
        queue_drained = Signal()

        RUN_MAX = 255
        pend_idles = Signal(range(RUN_MAX + 1))   # idles awaiting a run
        run_left   = Signal(8)    # load-side run replay (declared here
                                  # for the all_empty term; logic below)
        sk_valid   = Signal()     # 1-deep enqueue skid
        sk_data    = Signal(BEAT_W)

        # Nothing anywhere in the RX path: the incoming idle beat is
        # provably inter-packet and carries no information.
        all_empty = Signal()
        m.d.comb += all_empty.eq(queue_drained & ~sk_valid
                                 & (pend_idles == 0) & (run_left == 0))

        incoming_idle = beat_is_data & beat_is_idle
        incoming_beat = beat_is_data & ~beat_is_idle

        with m.If(incoming_beat & (pend_idles != 0)):
            # Flush the pending idle run ahead of this beat; the beat
            # parks in the (provably empty) skid.
            m.d.comb += [
                queue.w_data.eq(Cat(pend_idles,
                                    Const(0, BEAT_W - 8), C(1, 1))),
                queue.w_en.eq(1),
            ]
            m.d.ss += [pend_idles.eq(0), sk_valid.eq(1),
                       sk_data.eq(rx_data)]
        with m.Elif(sk_valid):
            m.d.comb += [
                queue.w_data.eq(Cat(sk_data, C(0, 1))),
                queue.w_en.eq(1),
            ]
            with m.If(incoming_beat):
                m.d.ss += sk_data.eq(rx_data)      # skid stays occupied
            with m.Elif(incoming_idle):
                m.d.ss += [sk_valid.eq(0),
                           pend_idles.eq(pend_idles + 1)]
            with m.Else():
                m.d.ss += sk_valid.eq(0)
        with m.Elif(incoming_beat):
            m.d.comb += [
                queue.w_data.eq(Cat(rx_data, C(0, 1))),
                queue.w_en.eq(1),
            ]
        with m.Elif(incoming_idle):
            with m.If(~engine_busy & all_empty):
                pass                    # provably inter-packet: dropped
            with m.Elif(pend_idles == RUN_MAX):
                # Cap flush (also the liveness bound for a construct
                # stalled on an idle span with no terminator).
                m.d.comb += [
                    queue.w_data.eq(Cat(Const(RUN_MAX, 8),
                                        Const(0, BEAT_W - 8),
                                        C(1, 1))),
                    queue.w_en.eq(1),
                ]
                m.d.ss += pend_idles.eq(1)
            with m.Else():
                m.d.ss += pend_idles.eq(pend_idles + 1)

        # Outside the data-block stream (training, link down) the
        # compressor state is stale: clear it.  (Last assignment wins.)
        with m.If(~self.data_mode):
            m.d.ss += [pend_idles.eq(0), sk_valid.eq(0)]

        m.d.comb += [
            self.queue_level.eq(queue.level),
            self.debug_wen.eq(queue.w_en),
        ]

        # ── grammar engine v2: bulk/boundary stepping ────────────────
        #
        # v1 walked 4 symbols per cycle through four CHAINED next-state
        # slots; the serial state/count recurrence across the slots was
        # the 156.25-blocking timing cone even with registered emissions
        # (16 LUT levels into the state/count regs).  v2 removes the
        # chaining entirely by splitting the grammar into:
        #
        #   * BULK steps -- states that pass symbols without per-symbol
        #     decisions (DPP payload, header body, LC body, aligned idle
        #     runs in SEARCH) consume a whole aligned 4-symbol half in
        #     one cycle with a single parallel count/position update;
        #   * BOUNDARY steps -- construct boundaries (start symbols,
        #     framing, header tail, terminators, the replica skip)
        #     consume ONE symbol per cycle with the v1 per-symbol
        #     logic, unchained.
        #
        # Boundaries cost O(1) cycles per construct against O(len/4)
        # bulk cycles, so the sustained rate stays ~4 symbols/cycle for
        # payload traffic; nothing downstream is cycle-exact and byte
        # order is identical to v1.
        ST_SEARCH, ST_FRAME, ST_HDR, ST_SKIP, ST_DPP, ST_TERM, ST_LC = \
            range(7)
        FR_HP, FR_DPH, FR_DPP, FR_LC = range(4)

        state    = Signal(range(7))
        fr_kind  = Signal(2)
        fr_pos   = Signal(2)
        count    = Signal(range(1024 + 8 + 1))
        hdr_pos  = Signal(range(17))
        hdr_data = Signal()          # dw0 said DATA-type
        dpp_len  = Signal(16)
        term_edb = Signal()

        # ``half`` indexes the 4-symbol steps of the current beat: two
        # at words=1, four (quarters) at words=2.
        half     = Signal(range(HALVES)) if HALVES > 2 else Signal()
        sub      = Signal(2)   # symbol position within the step
        cur_beat = Signal(BEAT_W)
        have_cur = Signal()

        # Step h covers symbols 4h..4h+3; symbol 0 is the beat's TOP
        # byte, so step h's symbol i sits at byte (HALVES*4 - 1) -
        # (4h + i) from the bottom.
        eng_syms = [Signal(8, name=f"eng_sym{i}") for i in range(4)]
        n_syms = 4 * HALVES
        with m.Switch(half):
            for h in range(HALVES):
                with m.Case(h):
                    for i in range(4):
                        pos = n_syms - 1 - (4 * h + i)
                        m.d.comb += eng_syms[i].eq(
                            cur_beat[8 * pos:8 * pos + 8])

        cur_sym = Signal(8)
        with m.Switch(sub):
            for j in range(4):
                with m.Case(j):
                    m.d.comb += cur_sym.eq(eng_syms[j])

        advance     = Signal()   # the walk executes this cycle
        can_bulk    = Signal()   # aligned 4-symbol step available
        half_done   = Signal()   # this cycle finishes the current half
        search_exit = Signal()   # this cycle's walk left ST_SEARCH

        m.d.comb += half_done.eq(advance & (can_bulk | (sub == 3)))
        with m.If(advance & ~half_done):
            m.d.ss += sub.eq(sub + 1)

        # Whole-idle beats are DISCARDED at the load point when the
        # engine is between constructs: they carry no information, and
        # consuming them at the full beat rate keeps the queue bounded
        # while the link idles.  Mid-construct all-idle beats (e.g. a
        # payload of 5A bytes) are never discarded: the state gate plus
        # the ``search_exit`` qualifier guard them -- the qualifier
        # covers the same-cycle race where the walk just left SEARCH
        # into a construct but the registered state still reads SEARCH
        # (a v1 latent hazard, fixed here).
        # Read-side prefetch (2 deep): the queue's r_en/level otherwise
        # sit in the walk's advance cone (a reported 156.25 path).  The
        # refill decision uses only the REGISTERED occupancy, so the
        # FIFO handshake is decoupled from the walk entirely; the head
        # can never starve (a beat is consumed at most every other
        # cycle -- two halves per beat -- while the refill runs every
        # cycle with one cycle of lag).
        qs_data = [Signal(BEAT_W + 1, name=f"qs_data{i}") for i in range(2)]
        qs_head = Signal()      # read slot pointer
        qs_tail = Signal()      # write slot pointer
        qs_cnt  = Signal(2)
        qs_pop  = Signal()
        qs_push = Signal()
        qh_valid = qs_cnt != 0
        qh_data  = Signal(BEAT_W + 1)

        m.d.comb += [
            qs_push.eq(queue.r_rdy & (qs_cnt < 2)),
            queue.r_en.eq(qs_push),
            queue_drained.eq(~queue.r_rdy & (qs_cnt == 0)),
            qh_data.eq(Mux(qs_head, qs_data[1], qs_data[0])),
        ]
        with m.If(qs_push & ~qs_pop):
            m.d.ss += qs_cnt.eq(qs_cnt + 1)
        with m.Elif(qs_pop & ~qs_push):
            m.d.ss += qs_cnt.eq(qs_cnt - 1)

        # Ring-pointer data movement: the pop (which sits in the walk's
        # advance cone) touches only the 1-bit head pointer; the data
        # registers are written by the push side alone.
        with m.If(qs_push):
            with m.If(qs_tail):
                m.d.ss += qs_data[1].eq(queue.r_data)
            with m.Else():
                m.d.ss += qs_data[0].eq(queue.r_data)
            m.d.ss += qs_tail.eq(~qs_tail)
        with m.If(qs_pop):
            m.d.ss += qs_head.eq(~qs_head)

        load_is_run = qh_data[BEAT_W]        # idle-run entry (count)
        run_count   = qh_data[0:8]

        # Per-step idle flags, precomputed at beat load (the bulk
        # eligibility's all-idle test otherwise closes a combinational
        # loop cur_beat -> compare -> half_done -> cur_beat load enable).
        # Flag h covers symbols 4h..4h+3 = the (HALVES-1-h)'th 32-bit
        # slice from the bottom.
        h_idle = Signal(HALVES)
        load_h_idle = [
            qh_data[32 * (HALVES - 1 - h):32 * (HALVES - h)]
            == Const(IDLE_BEAT & 0xFFFFFFFF, 32)
            for h in range(HALVES)
        ]

        # Idle-run replay: while ``run_left`` is nonzero the load stage
        # synthesizes whole-idle beats instead of reading the queue.  A
        # run (or its remainder) met while the engine is in SEARCH is
        # discarded in ONE cycle -- the fast drain that keeps the queue
        # bounded (bug #43).  The ``search_exit`` qualifier guards the
        # same-cycle race exactly as for beat entries: a walk that just
        # left SEARCH into a construct must not discard idle beats that
        # may be its payload.
        IDLE_ALL = Const(IDLE_W, BEAT_W)
        H_ALL    = Const((1 << HALVES) - 1, HALVES)

        with m.If(~have_cur):
            with m.If(run_left != 0):
                with m.If(state == ST_SEARCH):
                    m.d.ss += run_left.eq(0)              # discard rest
                with m.Else():
                    m.d.ss += [cur_beat.eq(IDLE_ALL),
                               h_idle.eq(H_ALL), run_left.eq(run_left - 1),
                               have_cur.eq(1), half.eq(0), sub.eq(0)]
            with m.Elif(qh_valid):
                with m.If(load_is_run & (state == ST_SEARCH)):
                    m.d.comb += qs_pop.eq(1)              # whole run
                with m.Elif(load_is_run):
                    m.d.ss += [cur_beat.eq(IDLE_ALL),
                               h_idle.eq(H_ALL),
                               run_left.eq(run_count - 1),
                               have_cur.eq(1), half.eq(0), sub.eq(0)]
                    m.d.comb += qs_pop.eq(1)
                with m.Else():
                    m.d.ss += [cur_beat.eq(qh_data[0:BEAT_W]),
                               h_idle.eq(Cat(*load_h_idle)),
                               have_cur.eq(1), half.eq(0), sub.eq(0)]
                    m.d.comb += qs_pop.eq(1)
        with m.Elif(half_done):
            m.d.ss += sub.eq(0)
            with m.If(half != HALVES - 1):
                m.d.ss += half.eq(half + 1)
            with m.Elif(run_left != 0):
                with m.If((state == ST_SEARCH) & ~search_exit):
                    m.d.ss += [run_left.eq(0), have_cur.eq(0)]
                with m.Else():
                    m.d.ss += [cur_beat.eq(IDLE_ALL),
                               h_idle.eq(H_ALL), run_left.eq(run_left - 1),
                               half.eq(0)]
            with m.Elif(qh_valid & load_is_run):
                with m.If((state == ST_SEARCH) & ~search_exit):
                    m.d.comb += qs_pop.eq(1)              # whole run
                    m.d.ss += have_cur.eq(0)
                with m.Else():
                    m.d.ss += [cur_beat.eq(IDLE_ALL),
                               h_idle.eq(H_ALL),
                               run_left.eq(run_count - 1),
                               half.eq(0)]
                    m.d.comb += qs_pop.eq(1)
            with m.Elif(qh_valid):
                m.d.ss += [cur_beat.eq(qh_data[0:BEAT_W]),
                           h_idle.eq(Cat(*load_h_idle)),
                           half.eq(0)]
                m.d.comb += qs_pop.eq(1)
            with m.Else():
                m.d.ss += have_cur.eq(0)

        # Output collector FIFO (translated Gen1 words + K flags).
        m.submodules.out_fifo = out_fifo = DomainRenamer({"sync": "ss"})(
            SyncFIFO(width=36, depth=self._out_depth))

        col_data = Signal(32)
        col_ctrl = Signal(4)
        col_cnt  = Signal(range(5))

        # Per-lane emissions toward the pipeline stage: bulk steps fill
        # all four lanes; boundary steps use lane 0 only.
        emit_en   = Signal(4)
        emit_byte = [Signal(8, name=f"emit_byte{i}") for i in range(4)]
        emit_k    = Signal(4)

        # Bulk eligibility, all from registered state (no chaining).
        # The all-idle test uses the flags precomputed at beat load.
        idle_half = Signal()
        m.d.comb += idle_half.eq(h_idle.bit_select(half, 1))
        m.d.comb += can_bulk.eq((sub == 0) & (
            ((state == ST_DPP) & (count > 4)) |
            ((state == ST_LC) & (count == 4)) |
            ((state == ST_HDR) & (hdr_pos <= 11)) |
            ((state == ST_SEARCH) & idle_half)))

        with m.If(advance & can_bulk):
            with m.Switch(state):

                with m.Case(ST_SEARCH):
                    # Aligned all-idle half: consumed silently.
                    pass

                with m.Case(ST_HDR):
                    # Four header bytes at once, positional captures in
                    # parallel: lane j carries header byte hdr_pos+j, so
                    # the dw0 type test lands at hdr_pos==0 (lane 0) and
                    # the dw1 length bytes at absolute positions 6/7.
                    m.d.comb += emit_en.eq(0b1111)
                    for j in range(4):
                        m.d.comb += emit_byte[j].eq(eng_syms[j])
                    m.d.ss += hdr_pos.eq(hdr_pos + 4)
                    with m.If(hdr_pos == 0):
                        with m.If(eng_syms[0][0:5] == 8):    # DATA type
                            m.d.ss += hdr_data.eq(1)
                    for j in range(4):
                        if 6 - j >= 0:
                            with m.If(hdr_pos == 6 - j):
                                m.d.ss += dpp_len[0:8].eq(eng_syms[j])
                        with m.If(hdr_pos == 7 - j):
                            m.d.ss += dpp_len[8:16].eq(eng_syms[j])

                with m.Case(ST_DPP):
                    m.d.comb += emit_en.eq(0b1111)
                    for j in range(4):
                        m.d.comb += emit_byte[j].eq(eng_syms[j])
                    m.d.ss += count.eq(count - 4)

                with m.Case(ST_LC):
                    m.d.comb += emit_en.eq(0b1111)
                    for j in range(4):
                        m.d.comb += emit_byte[j].eq(eng_syms[j])
                    m.d.ss += [count.eq(0), state.eq(ST_SEARCH)]

        with m.Elif(advance):
            # Boundary step: exactly one symbol, v1 logic unchained.
            s = cur_sym
            with m.Switch(state):

                with m.Case(ST_SEARCH):
                    with m.If(s == G2_IDL):
                        pass
                    with m.Elif((s == G2_SHP) | (s == G2_DPHP)):
                        m.d.comb += [emit_en.eq(1),
                                     emit_byte[0].eq(K_SHP),
                                     emit_k[0].eq(1), search_exit.eq(1)]
                        m.d.ss += [state.eq(ST_FRAME), fr_pos.eq(1),
                                   fr_kind.eq(Mux(s == G2_DPHP,
                                                  FR_DPH, FR_HP))]
                    with m.Elif(s == G2_SDP):
                        m.d.comb += [emit_en.eq(1),
                                     emit_byte[0].eq(K_SDP),
                                     emit_k[0].eq(1), search_exit.eq(1)]
                        m.d.ss += [state.eq(ST_FRAME), fr_pos.eq(1),
                                   fr_kind.eq(FR_DPP)]
                    with m.Elif(s == G2_SLC):
                        m.d.comb += [emit_en.eq(1),
                                     emit_byte[0].eq(K_SLC),
                                     emit_k[0].eq(1), search_exit.eq(1)]
                        m.d.ss += [state.eq(ST_FRAME), fr_pos.eq(1),
                                   fr_kind.eq(FR_LC)]
                    # anything else: dropped (corruption between
                    # packets; the constructs themselves are CRC- or
                    # count-guarded).

                with m.Case(ST_FRAME):
                    # Framing continuation (symbols 1,2 repeat the
                    # start symbol, symbol 3 is EPF).  The expected
                    # byte is emitted regardless of the received
                    # value: single-corrupt-symbol tolerance [7.3.3]
                    # -- gross corruption yields a construct the
                    # link core rejects by CRC.
                    with m.If(fr_pos == 3):
                        m.d.comb += [emit_en.eq(1),
                                     emit_byte[0].eq(K_EPF),
                                     emit_k[0].eq(1)]
                        with m.Switch(fr_kind):
                            with m.Case(FR_HP, FR_DPH):
                                m.d.ss += [state.eq(ST_HDR),
                                           hdr_pos.eq(0), hdr_data.eq(0)]
                            with m.Case(FR_DPP):
                                m.d.ss += [
                                    state.eq(ST_DPP),
                                    count.eq(dpp_len + 4),  # payload+CRC32
                                ]
                            with m.Case(FR_LC):
                                m.d.ss += [state.eq(ST_LC), count.eq(4)]
                    with m.Else():
                        start_map = Signal(8)
                        with m.Switch(fr_kind):
                            with m.Case(FR_HP, FR_DPH):
                                m.d.comb += start_map.eq(K_SHP)
                            with m.Case(FR_DPP):
                                m.d.comb += start_map.eq(K_SDP)
                            with m.Case(FR_LC):
                                m.d.comb += start_map.eq(K_SLC)
                        m.d.comb += [emit_en.eq(1),
                                     emit_byte[0].eq(start_map),
                                     emit_k[0].eq(1)]
                        m.d.ss += fr_pos.eq(fr_pos + 1)

                with m.Case(ST_HDR):
                    # Header tail bytes (positions 12..15 -- the body is
                    # bulk-stepped) and any unaligned leading bytes.
                    m.d.comb += [emit_en.eq(1), emit_byte[0].eq(s)]
                    m.d.ss += hdr_pos.eq(hdr_pos + 1)
                    with m.If(hdr_pos == 0):
                        with m.If(s[0:5] == 8):    # DATA type
                            m.d.ss += hdr_data.eq(1)
                    with m.If(hdr_pos == 6):
                        m.d.ss += dpp_len[0:8].eq(s)
                    with m.If(hdr_pos == 7):
                        m.d.ss += dpp_len[8:16].eq(s)
                    with m.If(hdr_pos == 15):
                        # A non-deferred Gen2 DPH (DPHSTART framing)
                        # carries TWO 2-byte length replicas (the
                        # 24-byte Figure 7-4 format [7.2.1.1]):
                        # swallow all four bytes.  (Bug #48 companion
                        # fix; replica-match validation [7.2.4.1.6
                        # rule 2a -> Recovery] is parked as a
                        # conformance follow-up.)
                        with m.If(hdr_data & (fr_kind == FR_DPH)):
                            m.d.ss += [state.eq(ST_SKIP), count.eq(4)]
                        with m.Else():
                            m.d.ss += state.eq(ST_SEARCH)

                with m.Case(ST_SKIP):
                    m.d.ss += count.eq(count - 1)
                    with m.If(count == 1):
                        m.d.ss += state.eq(ST_SEARCH)

                with m.Case(ST_DPP):
                    m.d.comb += [emit_en.eq(1), emit_byte[0].eq(s)]
                    m.d.ss += count.eq(count - 1)
                    with m.If(count == 1):
                        m.d.ss += [state.eq(ST_TERM), fr_pos.eq(0)]

                with m.Case(ST_TERM):
                    # DPPEND / DPPABORT framing (4 symbols).
                    with m.If(fr_pos == 3):
                        m.d.comb += [emit_en.eq(1),
                                     emit_byte[0].eq(K_EPF),
                                     emit_k[0].eq(1)]
                        m.d.ss += state.eq(ST_SEARCH)
                    with m.Else():
                        first_edb = (fr_pos == 0) & (s == G2_EDB)
                        m.d.comb += [
                            emit_en.eq(1),
                            emit_byte[0].eq(Mux(
                                Mux(fr_pos == 0, first_edb, term_edb),
                                K_EDB, K_END)),
                            emit_k[0].eq(1),
                        ]
                        m.d.ss += fr_pos.eq(fr_pos + 1)
                        with m.If(fr_pos == 0):
                            m.d.ss += term_edb.eq(first_edb)

                with m.Case(ST_LC):
                    m.d.comb += [emit_en.eq(1), emit_byte[0].eq(s)]
                    m.d.ss += count.eq(count - 1)
                    with m.If(count == 1):
                        m.d.ss += state.eq(ST_SEARCH)

        # ── emission pipeline stage (156.25 MHz timing cut) ──────────
        #
        # The walk's emissions are registered before the collector's
        # gather/merge/FIFO-write cone: the path is elastic end-to-end
        # (out_fifo absorbs the extra cycle of emission latency by
        # design; nothing downstream is cycle-exact), and byte ORDER is
        # fully preserved -- entries are consumed strictly in advance
        # order, and the partial-word idle flush below waits for this
        # stage to drain first.
        r_valid     = Signal()
        r_emit_en   = Signal(4)
        r_emit_byte = Signal(32)
        r_emit_k    = Signal(4)

        # Registered FIFO headroom: keeps the out_fifo level comparator
        # out of the advance/walk cone.  Margin: at most one write per
        # cycle and one cycle of staleness mean the level can exceed the
        # snapshot by two at the write -- far inside the 8-entry band.
        out_ok = Signal()
        m.d.ss += out_ok.eq(out_fifo.level < (self._out_depth - 8))

        any_emit  = emit_en.any()
        r_consume = Signal()
        m.d.comb += r_consume.eq(r_valid & out_ok)

        with m.If(advance):
            m.d.ss += [
                r_valid.eq(any_emit),
                r_emit_en.eq(emit_en),
                r_emit_byte.eq(Cat(*emit_byte)),
                r_emit_k.eq(emit_k),
            ]
        with m.Elif(r_consume):
            m.d.ss += r_valid.eq(0)

        m.d.comb += engine_busy.eq((state != ST_SEARCH) | have_cur
                                   | r_valid | (col_cnt != 0))
        m.d.comb += [
            self.debug_state.eq(state),
            self.debug_have.eq(have_cur),
            self.debug_out_lvl.eq(out_fifo.level),
        ]

        # Advance whenever we hold symbols and the emission stage can
        # accept the walk's output (stage empty, or draining this cycle).
        m.d.comb += advance.eq(have_cur & (~r_valid | out_ok))

        # ── output collector: pack emitted bytes into words ──────────
        new_bytes = Signal(3)
        m.d.comb += new_bytes.eq(sum(r_emit_en[i] for i in range(4)))

        # Gather the (up to 4) registered bytes, in slot order.
        gathered = [Signal(9, name=f"gath{i}") for i in range(4)]
        for i in range(4):
            sel = Signal(9, name=f"gsel{i}")
            m.d.comb += sel.eq(0)
            prior = Const(0, 3)
            for j in range(4):
                with m.If(r_emit_en[j] & (prior == i)):
                    m.d.comb += sel.eq(Cat(r_emit_byte.word_select(j, 8),
                                           r_emit_k[j]))
                prior = prior + r_emit_en[j]
            m.d.comb += gathered[i].eq(sel)

        total = Signal(4)
        m.d.comb += total.eq(col_cnt + new_bytes)

        # Merge collector residue + new bytes (up to 7 bytes).
        merged_d = [Signal(8, name=f"m_d{i}") for i in range(7)]
        merged_k = [Signal(name=f"m_k{i}") for i in range(7)]
        for i in range(7):
            if i < 4:
                with m.If(i < col_cnt):
                    m.d.comb += [
                        merged_d[i].eq(col_data.word_select(i, 8)),
                        merged_k[i].eq(col_ctrl[i]),
                    ]
            idx = Signal(3, name=f"m_idx{i}")
            m.d.comb += idx.eq(i - col_cnt)
            with m.If(i >= col_cnt):
                with m.Switch(idx):
                    for j in range(4):
                        with m.Case(j):
                            m.d.comb += [
                                merged_d[i].eq(gathered[j][0:8]),
                                merged_k[i].eq(gathered[j][8]),
                            ]

        with m.If(r_consume & (new_bytes != 0)):
            with m.If(total >= 4):
                m.d.comb += [
                    out_fifo.w_data.eq(Cat(
                        merged_d[0], merged_d[1], merged_d[2], merged_d[3],
                        merged_k[0], merged_k[1], merged_k[2],
                        merged_k[3])),
                    out_fifo.w_en.eq(1),
                ]
                m.d.ss += col_cnt.eq(total - 4)
                for i in range(3):
                    with m.If(i < (total - 4)):
                        m.d.ss += [
                            col_data.word_select(i, 8).eq(merged_d[4 + i]),
                            col_ctrl[i].eq(merged_k[4 + i]),
                        ]
            with m.Else():
                m.d.ss += col_cnt.eq(total)
                for i in range(4):
                    with m.If((i >= col_cnt) & (i < total)):
                        gidx = Signal(3, name=f"c_idx{i}")
                        m.d.comb += gidx.eq(i - col_cnt)
                        with m.Switch(gidx):
                            for j in range(4):
                                with m.Case(j):
                                    m.d.ss += [
                                        col_data.word_select(i, 8)
                                            .eq(gathered[j][0:8]),
                                        col_ctrl[i].eq(gathered[j][8]),
                                    ]
        with m.Elif((col_cnt != 0) & (state == ST_SEARCH) & ~r_valid
                    & out_ok):
            # A completed construct left a partial word behind (odd
            # DPP lengths): flush it padded with Gen1 logical idle --
            # only once the emission stage has drained, so the pad can
            # never overtake in-flight construct bytes.
            flush_d = Signal(32)
            flush_k = Signal(4)
            for i in range(4):
                with m.If(i < col_cnt):
                    m.d.comb += [
                        flush_d.word_select(i, 8)
                            .eq(col_data.word_select(i, 8)),
                        flush_k[i].eq(col_ctrl[i]),
                    ]
            m.d.comb += [
                out_fifo.w_data.eq(Cat(flush_d, flush_k)),
                out_fifo.w_en.eq(1),
            ]
            m.d.ss += col_cnt.eq(0)

        # ── source stream: translated words, idle fill otherwise ─────
        #
        # The stream toward the link core is presented from a REGISTER
        # stage (156.25 timing: out_fifo's read data and level compare
        # otherwise fan combinationally into every link-layer receiver
        # cone -- crc16/crc32/lc_detector).  The load decision uses the
        # cycle-T view; safety of the one-cycle-stale idle decision: an
        # idle word is only synthesized when the engine was FULLY drained
        # at T (no queued beats, no in-flight emissions, no collector
        # residue), so the earliest possible next construct word reaches
        # the FIFO at T+1 and is presented at T+2 -- the idle can never
        # split a construct (the DPP-follows-DPH rule the Gen1 framers
        # depend on).
        if self._words == 1:
            o_valid = Signal()
            o_data  = Signal(32)
            o_ctrl  = Signal(4)
            o_take  = Signal()
            m.d.comb += o_take.eq(~o_valid | self.source.ready)

            with m.If(o_take):
                with m.If(out_fifo.r_rdy):
                    m.d.ss += [
                        o_valid.eq(1),
                        o_data.eq(out_fifo.r_data[0:32]),
                        o_ctrl.eq(out_fifo.r_data[32:36]),
                    ]
                    m.d.comb += out_fifo.r_en.eq(1)
                with m.Elif(self.data_mode & ~engine_busy):
                    # Synthesized Gen1 logical idle: the partner is in
                    # its data-block stream (post-SDS); the wire between
                    # packets carries Gen2 Idle Symbols.  NB: while the
                    # engine is mid-construct (a construct tail
                    # momentarily dips the output rate below one word
                    # per cycle) the stream goes INVALID instead -- an
                    # idle word spliced mid-packet would make the Gen1
                    # core's framers bail (the DPP must immediately
                    # follow its DPH).
                    m.d.ss += [o_valid.eq(1), o_data.eq(0), o_ctrl.eq(0)]
                with m.Else():
                    m.d.ss += o_valid.eq(0)

            m.d.comb += [
                self.source.valid.eq(o_valid),
                self.source.data.eq(o_data),
                self.source.ctrl.eq(o_ctrl),
            ]
        else:
            # ── words=2: a 2:1 output packer ─────────────────────────
            #
            # The collector emits 32-bit words at <= 1/cycle; the wide
            # source presents 64-bit beats (at most every other cycle
            # under saturation -- the wide link receivers tolerate
            # valid gaps anywhere).  A solo word is flushed with an
            # idle high half ONLY when the whole engine is quiescent
            # (fifo empty + engine drained): mid-construct it would
            # splice idle into a packet, so the beat waits for its
            # pair instead.  Constructs may thus land at either beat
            # half downstream -- exactly the offsets-0/4 machinery the
            # words=2 framers implement.
            pend_v = Signal()
            pend_d = Signal(32)
            pend_c = Signal(4)
            o_valid = Signal()
            o_data  = Signal(64)
            o_ctrl  = Signal(8)
            o_take  = Signal()
            quiescent = Signal()
            m.d.comb += [
                o_take.eq(~o_valid | self.source.ready),
                quiescent.eq(self.data_mode & ~engine_busy),
            ]

            with m.If(o_take):
                with m.If(pend_v & out_fifo.r_rdy):
                    m.d.ss += [
                        o_valid.eq(1),
                        o_data.eq(Cat(pend_d, out_fifo.r_data[0:32])),
                        o_ctrl.eq(Cat(pend_c, out_fifo.r_data[32:36])),
                        pend_v.eq(0),
                    ]
                    m.d.comb += out_fifo.r_en.eq(1)
                with m.Elif(pend_v & quiescent):
                    # Solo flush: idle high half (safe -- see above).
                    m.d.ss += [
                        o_valid.eq(1),
                        o_data.eq(Cat(pend_d, Const(0, 32))),
                        o_ctrl.eq(Cat(pend_c, Const(0, 4))),
                        pend_v.eq(0),
                    ]
                with m.Elif(out_fifo.r_rdy):
                    m.d.ss += [
                        pend_v.eq(1),
                        pend_d.eq(out_fifo.r_data[0:32]),
                        pend_c.eq(out_fifo.r_data[32:36]),
                        o_valid.eq(0),
                    ]
                    m.d.comb += out_fifo.r_en.eq(1)
                with m.Elif(quiescent):
                    # Whole synthesized idle beat (as at words=1).
                    m.d.ss += [o_valid.eq(1), o_data.eq(0), o_ctrl.eq(0)]
                with m.Else():
                    m.d.ss += o_valid.eq(0)

            m.d.comb += [
                self.source.valid.eq(o_valid),
                self.source.data.eq(o_data),
                self.source.ctrl.eq(o_ctrl),
            ]

        return m
