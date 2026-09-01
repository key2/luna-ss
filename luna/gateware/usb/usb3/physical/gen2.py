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
  DPHSTART framing and its 2-byte length-field replica [7.2.1.1] (our
  device never emits deferred DPHs), and packets burst out at the 64-bit
  beat rate with Gen2 Idle Symbols (5Ah! [7.1.2]) as filler.

* ``Gen2BlockReceiver`` -- block classification (control blocks: TS1/TS2/
  TSEQ consecutive-detection with the symbol-14/15 exclusion and
  SYNC-transparency rules [7.5.4.8.2], SDS detection; SKP never reaches
  the MAC -- the PHY strips it) and the reverse data path: a
  byte-granular grammar engine walks the data-block symbol stream
  (framing may land at any symbol offset once DPH length replicas are in
  play), translates Gen2 framing back into the Gen1 K-coded wire dialect
  the 32-bit core speaks, drops the DPH length replica, tracks DPP
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
(bounded by NumP flow control) and whole-idle beats are dropped at the
input whenever the engine is drained, which is the steady-state U0
condition.  A level debug tap is provided for the Phase-5 sizing
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


class Gen2TxBridge(Elaboratable):
    """Per-packet 32->64 transmit bridge (stage A).

    Captures whole packets from the Gen1 transmit stream (packets are
    delimited by the ``first`` markers the emitters place on packet
    starts and on every logical-idle filler word), maps the Gen1 K-code
    framing to Gen2 symbols at enqueue time, converts a DATA-type header
    to DPHSTART framing with the 2-byte length-field replica appended,
    and serves complete packets to the block transmitter one 8-symbol
    beat at a time, gaplessly.
    """

    def __init__(self, depth=512):
        self._depth = depth

        self.sink         = USBRawSuperSpeedStream()   # from the arbiter

        # Beat interface toward the block transmitter.
        self.beat_request = Signal()    # i: emit one data beat now
        self.beat_data    = Signal(64)  # o: packet content or idle fill
        # A packet is straddling the current block boundary: its first
        # beat has been served but its final (eop) beat has not.  The
        # scheduler defers SKP OS insertion while set -- "SKP Ordered
        # Sets shall not be inserted within any packet" [6.4.3.3].
        self.pkt_in_flight = Signal()

        # Debug.
        self.packets_buffered = Signal(8)

    def elaborate(self, platform):
        m = Module()
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
        # replica appends 2; whenever 8 bytes are available a beat is
        # written.  After a replica insertion the byte phase is +2 --
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
                        # 3 DWs + crc16/lcw = 20 bytes), insert the
                        # 2-byte length replica [7.2.1.1].
                        with m.If(dph & (byte_index == 16)):
                            m.next = "REPLICA"

                    # (bare idle filler with no packet open: dropped.)

            with m.State("REPLICA"):
                m.d.comb += sink.ready.eq(0)
                with m.If(fifo.w_rdy):
                    # replica = length field, LSB first.
                    append_bytes(2, Cat(dw1_len[8:16], dw1_len[0:8]))
                    m.d.ss += [byte_index.eq(byte_index + 2), dph.eq(0)]
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
                 skp_interval=40):
        self._tseq_count      = tseq_count
        self._ts_per_burst    = ts_per_burst
        self._sync_every_ts   = sync_every_ts
        self._sync_every_tseq = sync_every_tseq
        self._skp_interval    = skp_interval

        # Stream from the link layer (through the physical layer).
        self.sink             = USBRawSuperSpeedStream()

        # LTSSM controls.
        self.send_tseq_burst  = Signal()
        self.send_ts1_burst   = Signal()
        self.send_ts2_burst   = Signal()
        self.idle_mode        = Signal()   # SDS-once + data blocks
        self.request_hot_reset      = Signal()
        self.request_no_scrambling  = Signal()

        self.burst_complete   = Signal()   # strobe (TS cadence)

        # PIPE block interface.
        self.tx_data          = Signal(64)
        self.tx_head          = Signal(4)
        self.tx_start         = Signal()
        self.tx_valid         = Signal()

        # Debug.
        self.packets_buffered = Signal(8)

    def elaborate(self, platform):
        m = Module()

        m.submodules.bridge = bridge = Gen2TxBridge()
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
        sds_pending = Signal()
        idle_prev = Signal()

        # Registered activity gate (156.25: the LTSSM burst-request seam
        # registers otherwise reach the scheduler/bridge FIFO controls
        # through this OR in one hop).  One cycle of TX start/stop
        # latency against microsecond burst tolerances.
        active = Signal()
        m.d.ss += active.eq(self.send_tseq_burst | self.send_ts1_burst |
                            self.send_ts2_burst | self.idle_mode)

        # Arm the single SDS whenever idle-mode is (re-)entered
        # [7.5.4.10: a single SDS before the first data block].
        m.d.ss += idle_prev.eq(self.idle_mode)
        with m.If(self.idle_mode & ~idle_prev):
            m.d.ss += sds_pending.eq(1)

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
        # 132 wire bits: the PHY's 32-deep TX gearbox FIFO gains one
        # queued beat every 33 cycles and overflows after ~7 us of
        # sustained streaming -- far shorter than any training sequence.
        # One dead beat (tx_valid low) at a block boundary every 16
        # blocks (32 beats + 1 gap = 33 cycles = 16 x 132 wire bits at
        # 10 GT/s) matches the rates EXACTLY; a 24-symbol/3-beat SKP OS
        # block carries the same 0.4 ns per-block deficit, so counting
        # it as one block keeps the ratio exact.  Guarded by
        # tests/test_gen2_pacing.py against the FIFO model; TxFifoWrNum
        # probes confirm on silicon.
        pace_cnt = Signal(range(16))
        pace_due = Signal()

        with m.If(active & ~(pace_due & (beat_idx == 0))):
            m.d.comb += self.tx_valid.eq(1)

            with m.If(beat_idx == 0):
                # ── block boundary: choose and start the next block ──
                m.d.comb += self.tx_start.eq(1)
                m.d.ss += beat_idx.eq(1)

                with m.If(new_mode != mode):
                    m.d.ss += [mode.eq(new_mode), os_count.eq(0),
                               sync_gap.eq(0)]

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

                    # Pacing accounting: one gap after every 16th block.
                    m.d.ss += pace_cnt.eq(pace_cnt + 1)
                    with m.If(pace_cnt == 15):
                        m.d.ss += pace_due.eq(1)

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
            # Rate-matching gap: hold the block boundary for one cycle
            # (tx_valid stays low; the PHY FIFO drains one beat).
            m.d.ss += pace_due.eq(0)

        with m.Else():
            m.d.ss += [beat_idx.eq(0), mode.eq(0), os_count.eq(0),
                       sync_gap.eq(0), skp_gap.eq(0), sds_pending.eq(0),
                       pace_cnt.eq(0), pace_due.eq(0)]

        return m


class Gen2BlockReceiver(Elaboratable):
    """Gen2 block-level receiver (stage A).

    Classifies control blocks (TS1/TS2/TSEQ consecutive detection with
    symbol-14/15 exclusion and SYNC transparency; SDS detection) and
    translates the data-block symbol stream back into the Gen1 32-bit
    K-coded dialect for the unmodified link core.
    """

    def __init__(self, queue_depth=1024, out_depth=512):
        self._queue_depth = queue_depth
        self._out_depth   = out_depth

        # PIPE block interface.
        self.rx_data      = Signal(64)
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
        self.source        = USBRawSuperSpeedStream()

        # Debug (prunable bring-up taps).
        self.queue_level   = Signal(16)
        self.debug_state   = Signal(3)
        self.debug_have    = Signal()
        self.debug_wen     = Signal()
        self.debug_out_lvl = Signal(16)

    def elaborate(self, platform):
        m = Module()

        # ── PIPE input registers ─────────────────────────────────────
        # The whole receiver works from a locally registered copy of the
        # PIPE RX beat (156.25 timing: the adapter's output registers
        # otherwise reach the enqueue idle-compare and the block
        # classifier in one routed hop).  One beat of RX latency is
        # immaterial everywhere downstream.
        rx_data  = Signal(64)
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
        beat0_data = Signal(64)
        have_beat0 = Signal()
        block_done = Signal()
        block_ctl  = Signal()
        b0 = Signal(64)
        b1 = Signal(64)

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

        # ── data path: beat queue ────────────────────────────────────
        #
        # Enqueue every data-block beat unless it is pure idle AND the
        # engine is fully drained (then it is provably inter-packet).
        # Entries are 65 bits: {is_idle, beat} -- the whole-idle flag is
        # computed ONCE at enqueue (the compare already exists in the
        # discard condition here) so the read side never re-derives it
        # from the 64-bit read data (a reported 156.25 reduce cone).
        m.submodules.queue = queue = DomainRenamer({"sync": "ss"})(
            SyncFIFO(width=65, depth=self._queue_depth))

        engine_busy = Signal()   # grammar engine mid-construct
        beat_is_idle = rx_data == Const(IDLE_BEAT, 64)
        beat_is_data = rx_valid & (rx_head == BLOCK_DATA) \
            & self.data_mode

        # (``queue_drained`` also covers the read-side prefetch skid --
        # a pending construct beat there means an incoming all-idle beat
        # may be construct PAYLOAD and must never be discarded.)
        queue_drained = Signal()

        with m.If(beat_is_data &
                  ~(beat_is_idle & ~engine_busy & queue_drained)):
            m.d.comb += [
                queue.w_data.eq(Cat(rx_data, beat_is_idle)),
                queue.w_en.eq(1),
            ]

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

        half     = Signal()    # which half of the current beat
        sub      = Signal(2)   # symbol position within the half
        cur_beat = Signal(64)
        have_cur = Signal()

        eng_syms = [Signal(8, name=f"eng_sym{i}") for i in range(4)]
        for i in range(4):
            with m.If(~half):
                m.d.comb += eng_syms[i].eq(
                    cur_beat[8 * (7 - i):8 * (8 - i)])
            with m.Else():
                m.d.comb += eng_syms[i].eq(
                    cur_beat[8 * (3 - i):8 * (4 - i)])

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
        qs_data = [Signal(65, name=f"qs_data{i}") for i in range(2)]
        qs_head = Signal()      # read slot pointer
        qs_tail = Signal()      # write slot pointer
        qs_cnt  = Signal(2)
        qs_pop  = Signal()
        qs_push = Signal()
        qh_valid = qs_cnt != 0
        qh_data  = Signal(65)

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

        load_is_idle = qh_data[64]           # computed at enqueue

        # Per-half idle flags, precomputed at beat load (the bulk
        # eligibility's all-idle test otherwise closes a combinational
        # loop cur_beat -> compare -> half_done -> cur_beat load enable).
        h_idle = Signal(2)
        load_h_idle = [
            qh_data[32:64] == Const(IDLE_BEAT & 0xFFFFFFFF, 32),
            qh_data[0:32]  == Const(IDLE_BEAT & 0xFFFFFFFF, 32),
        ]

        with m.If(~have_cur):
            with m.If(qh_valid):
                with m.If(load_is_idle & (state == ST_SEARCH)):
                    m.d.comb += qs_pop.eq(1)              # discard
                with m.Else():
                    m.d.ss += [cur_beat.eq(qh_data[0:64]),
                               h_idle.eq(Cat(load_h_idle[0],
                                             load_h_idle[1])),
                               have_cur.eq(1), half.eq(0), sub.eq(0)]
                    m.d.comb += qs_pop.eq(1)
        with m.Elif(half_done):
            m.d.ss += sub.eq(0)
            with m.If(~half):
                m.d.ss += half.eq(1)
            with m.Elif(qh_valid
                        & ~(load_is_idle & (state == ST_SEARCH)
                            & ~search_exit)):
                m.d.ss += [cur_beat.eq(qh_data[0:64]),
                           h_idle.eq(Cat(load_h_idle[0],
                                         load_h_idle[1])),
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
        m.d.comb += idle_half.eq(Mux(half, h_idle[1], h_idle[0]))
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
                        # carries a 2-byte length replica: swallow.
                        with m.If(hdr_data & (fr_kind == FR_DPH)):
                            m.d.ss += [state.eq(ST_SKIP), count.eq(2)]
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
                # Synthesized Gen1 logical idle: the partner is in its
                # data-block stream (post-SDS); the wire between packets
                # carries Gen2 Idle Symbols.  NB: while the engine is
                # mid-construct (a construct tail momentarily dips the
                # output rate below one word per cycle) the stream goes
                # INVALID instead -- an idle word spliced mid-packet
                # would make the Gen1 core's framers bail (the DPP must
                # immediately follow its DPH).
                m.d.ss += [o_valid.eq(1), o_data.eq(0), o_ctrl.eq(0)]
            with m.Else():
                m.d.ss += o_valid.eq(0)

        m.d.comb += [
            self.source.valid.eq(o_valid),
            self.source.data.eq(o_data),
            self.source.ctrl.eq(o_ctrl),
        ]

        return m
