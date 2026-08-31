"""Host-side USB 3.2 Gen2 (128b/132b) coding oracle.

Pure-Python model of the Gen2 wire coding used by the link-partner
simulations: 132-bit block assembly, the 23-bit scrambler LFSR
(G(X) = X^23 + X^21 + X^16 + X^8 + X^5 + X^2 + 1, seed 1DBFBCh), the
per-block-type scramble/bypass/freeze/reset rules, ordered sets
(TSEQ/TS1/TS2/SYNC/SDS/SKP), and the Gen2 data-block framing symbols
[USB 3.2 r1.1 Table 6-2, 6-7..6-13, 6.3.2.x].

The LFSR math is imported from ``gw_usb3.lfsr`` (the same matrices the
RTL's XOR networks are generated from), and the whole model is pinned
byte-exact against the silicon-proven RTL ``gw_usb3.scramble``
Scrambler/Descrambler pair by ``sim_gen2_oracle.py`` — keep that sim
green when touching anything here.

Beat convention (matches the RTL datapath): a 132-bit block crosses
the 64-bit datapath as two beats (three for the 24-symbol SKP OS)
with a 4-bit ``block_head`` (0x3 data / 0xC control) and
``start_block`` on the first beat.  Symbol 0 of a beat lives in bits
[56:64] (big-endian symbol packing); the scrambler keystream is
byte-swapped to match.
"""

from gw_usb3.lfsr import advance_masks, keystream_masks, GEN2_WIDTH
from gw_usb3.tables import (BlockType, BLOCK_CONTROL, BLOCK_DATA,
                            DEFAULT_SCRAMBLER_INIT)

# ── Gen2 framing symbols (Table 6-2; = gw_usb3.tables.BlockType values) ──
SHP  = int(BlockType.SHPS)    # 0x9A  header packet start
DPHP = int(BlockType.DPHPS)   # 0x95  non-deferred Gen2 DPH start
SDP  = int(BlockType.SDPS)    # 0x96  data packet payload start
END  = int(BlockType.ENDS)    # 0x65  DPP end
EDB  = int(BlockType.EDBS)    # 0x69  DPP abort
SLC  = int(BlockType.SLCS)    # 0x4B  link command start
EPF  = int(BlockType.EPFS)    # 0x36  end packet framing
IDL  = int(BlockType.LIS)     # 0x5A  Gen2 logical Idle Symbol [7.1.2]
                              # (Gen1's 00h does NOT carry over!)

HPSTART  = (SHP, SHP, SHP, EPF)
DPHSTART = (DPHP, DPHP, DPHP, EPF)
DPPSTART = (SDP, SDP, SDP, EPF)
DPPEND   = (END, END, END, EPF)
DPPABORT = (EDB, EDB, EDB, EPF)
LCSTART  = (SLC, SLC, SLC, EPF)

# ── LFSR ─────────────────────────────────────────────────────────────

_ADV64 = advance_masks(64)
_KS64  = keystream_masks(64)


def _parity(v: int) -> int:
    return bin(v).count("1") & 1


def lfsr_advance64(state: int) -> int:
    """State after 64 bit-times."""
    return sum(_parity(state & _ADV64[i]) << i for i in range(GEN2_WIDTH))


def _byteswap64(v: int) -> int:
    return int.from_bytes(v.to_bytes(8, "little"), "big")


def lfsr_keystream64(state: int) -> int:
    """64 keystream bits for one beat, in WIRE beat order (symbol 0 in
    bits [56:64]) — i.e. already byte-swapped like the RTL."""
    raw = sum(_parity(state & _KS64[i]) << i for i in range(64))
    return _byteswap64(raw)


# ── blocks and beats ─────────────────────────────────────────────────

def syms_to_beats(syms):
    """Pack symbols (len multiple of 8) into 64-bit beats, symbol 0 of
    each beat in bits [56:64]."""
    assert len(syms) % 8 == 0
    beats = []
    for off in range(0, len(syms), 8):
        b = 0
        for i in range(8):
            b |= (syms[off + i] & 0xFF) << (8 * (7 - i))
        beats.append(b)
    return beats


def beats_to_syms(beats):
    out = []
    for b in beats:
        out += [(b >> (8 * (7 - i))) & 0xFF for i in range(8)]
    return out


class Block:
    """One 128b/132b block: ``head`` (0x3/0xC) + symbol payload
    (16 symbols, or 24 for the SKP OS control block)."""

    def __init__(self, head, syms):
        assert head in (BLOCK_CONTROL, BLOCK_DATA)
        assert len(syms) in (16, 24)
        self.head = head
        self.syms = list(syms)

    def beats(self):
        """[(start_block, head, data64), ...]"""
        bs = syms_to_beats(self.syms)
        return [(1 if i == 0 else 0, self.head, b) for i, b in enumerate(bs)]

    def __repr__(self):
        k = "ctl" if self.head == BLOCK_CONTROL else "dat"
        return f"<Block {k} {' '.join(f'{s:02x}' for s in self.syms)}>"


# ordered sets [Tables 6-7..6-13]
def sync_block():
    """SYNC OS: even symbols 00h, odd FFh; resets the scrambler."""
    return Block(BLOCK_CONTROL, [0x00 if i % 2 == 0 else 0xFF
                                 for i in range(16)])


def tseq_block():
    s = [0x87] * 16
    s[4] = s[5] = 0x00
    return Block(BLOCK_CONTROL, s)


def ts1_block(link_func=0):
    s = [int(BlockType.TS1)] * 16
    s[4] = 0x00
    s[5] = link_func & 0xFF
    return Block(BLOCK_CONTROL, s)


def ts2_block(link_func=0):
    s = [int(BlockType.TS2)] * 16
    s[4] = 0x00
    s[5] = link_func & 0xFF
    return Block(BLOCK_CONTROL, s)


def sds_block():
    return Block(BLOCK_CONTROL, [0xE1] * 4 + [0x55] * 12)


def skp_block():
    """TX-nominal SKP OS: 20x SKP + SKPEND + 3 LFSR-state symbols
    (24 symbols = 3 beats).  The three trailing symbols are
    placeholders here — the scrambler (RTL and model) splices the live
    LFSR state into them on the wire [Table 6-13]."""
    return Block(BLOCK_CONTROL,
                 [int(BlockType.SKP)] * 20 + [int(BlockType.SKPEND)]
                 + [0x00, 0x00, 0x00])


def data_block(syms16):
    assert len(syms16) == 16
    return Block(BLOCK_DATA, syms16)


def idle_block():
    return data_block([IDL] * 16)


# ── the scrambler model (mirrors gw_usb3.scramble.Scrambler) ─────────

class ScramblerModel:
    """Beat-level model of the RTL Gen2 scrambler.

    Feed beats in wire order; returns the scrambled beat.  The model is
    used self-inversely for descrambling (`descramble=True` only
    changes the SKP splice behaviour: on descramble the SKP LFSR
    symbols are passed through and the LFSR is reseeded from them,
    like the RTL descrambler).

    Rule table (pinned by sim_gen2_oracle.py against the RTL):

    block type      first word          continuation word(s)
    SYNC            reset, bypass       reset, bypass
    SKP/SKPEND      freeze, bypass      freeze, bypass; LFSR spliced
                                        into the last 3 symbols
    SDS             advance, bypass     advance, bypass
    TSEQ/TS1/TS2    advance, sym0 raw   advance, all scrambled
                    syms1-7 scrambled
    data            advance, all        advance, all scrambled
    """

    def __init__(self, descramble=False):
        self.state = DEFAULT_SCRAMBLER_INIT
        self.block_type = None
        self.skp_cnt = 0
        self.descramble = descramble

    def feed(self, start, head, data):
        first_byte = (data >> 56) & 0xFF

        if self.skp_cnt > 0:
            self.skp_cnt -= 1

        rst = False
        en = False
        xor = 0b000                       # (sym0, syms1-5, syms6-7) lanes
        splice = False

        if head == BLOCK_DATA:
            self.block_type = first_byte
            en, xor = True, 0b111
        elif start:                       # control block, first word
            self.block_type = first_byte
            if first_byte == BlockType.SDS:
                en = True
            elif first_byte in (BlockType.SKP, BlockType.SKPEND):
                self.skp_cnt = 2
            elif first_byte in (BlockType.SYNC_HIG, BlockType.SYNC_LOW):
                rst = True
            else:                         # TS1/TS2/TSEQ and friends
                en, xor = True, 0b011
        else:                             # control continuation word
            bt = self.block_type
            if bt == BlockType.SDS:
                en = True
            elif bt in (BlockType.SKP, BlockType.SKPEND):
                splice = (self.skp_cnt == 0)
            elif bt in (BlockType.TS1, BlockType.TS2, BlockType.TSEQ):
                en, xor = True, 0b111
            elif bt in (BlockType.SYNC_HIG, BlockType.SYNC_LOW):
                rst = True

        ks = lfsr_keystream64(self.state)
        out = data
        if en:
            for lo, hi, sel in ((56, 64, xor & 0b100),
                                (16, 56, xor & 0b010),
                                (0, 16, xor & 0b001)):
                if sel:
                    mask = ((1 << (hi - lo)) - 1) << lo
                    out ^= ks & mask

        if splice and not self.descramble:
            # TX: splice the CURRENT (frozen) LFSR state into the last
            # three symbols, bit 23 = ~bit 22 [Table 6-13].  Pinned
            # against the RTL by sim_gen2_oracle: the state carried is
            # exactly the one the next scrambled beat's keystream
            # derives from, so an acquiring receiver that reseeds from
            # it is aligned immediately.
            st = self.state
            out = (out & ~0xFFFFFF) | (st & 0x7FFFFF) \
                  | (((~st >> 22) & 1) << 23)

        if rst:
            self.state = DEFAULT_SCRAMBLER_INIT
        elif en:
            self.state = lfsr_advance64(self.state)
        return out

    def feed_block(self, block):
        return [self.feed(s, h, d) for (s, h, d) in block.beats()]


def scramble_stream(blocks, descramble=False):
    """Scramble (or descramble) a block list; returns beats
    [(start, head, data64), ...]."""
    mdl = ScramblerModel(descramble=descramble)
    out = []
    for blk in blocks:
        for (s, h, d) in blk.beats():
            out.append((s, h, mdl.feed(s, h, d)))
    return out


# ── link commands / header packets (content layer) ──────────────────
#
# CRC generators are shared with the Gen1 host model (same
# polynomials); the Gen2 deltas are the 4-bit header sequence numbers
# (LGOOD_0..15) and the LCRD1/LCRD2 credit classes [Table 7-4,
# 7.2.1.1.3].

def lc_word(command, subtype):
    """16-bit link command word incl. CRC-5 (Gen2: subtype is 4 bits —
    LGOOD_0..15, LCRD1_A..D / LCRD2_A..D)."""
    from sim_link_loopback import crc5
    lcw = (subtype & 0xF) | ((command & 0xF) << 7)
    return lcw | (crc5(lcw & 0x7FF) << 11)


def link_command_syms(command, subtype):
    """8 framing+payload symbols of a Gen2 link command (LCSTART + the
    16-bit word twice, LSB first) [7.2.2.1]."""
    w = lc_word(command, subtype)
    lo, hi = w & 0xFF, (w >> 8) & 0xFF
    return list(LCSTART) + [lo, hi, lo, hi]


def header_packet_syms(dw0, dw1, dw2, seq, dl=0, hub_depth=0, deferred=False,
                       start=None):
    """Header packet symbols: HPSTART/DPHSTART + 3 DWs (LSB first) +
    CRC-16 + Link Control Word.  ``seq`` is the 4-bit Gen2 header
    sequence number.  A DPHSTART-framed (non-deferred Gen2 DPH) header
    additionally carries the 2-byte length-field replica (mirroring
    dw1[16:32], LSB first) right after the LCW [7.2.1.1]."""
    from sim_link_loopback import crc16_header, crc5
    lcw = (seq & 0xF) | ((hub_depth & 0x7) << 6) | ((dl & 1) << 9) \
        | ((1 if deferred else 0) << 10)
    lcw |= crc5(lcw & 0x7FF) << 11
    crc16 = crc16_header([dw0, dw1, dw2])
    if start is None:
        start = HPSTART
    syms = list(start)
    for dw in (dw0, dw1, dw2):
        syms += list(dw.to_bytes(4, "little"))
    syms += list(crc16.to_bytes(2, "little"))
    syms += list(lcw.to_bytes(2, "little"))
    if tuple(start) == DPHSTART:
        length = (dw1 >> 16) & 0xFFFF
        syms += list(length.to_bytes(2, "little"))
    return syms


def dpp_syms(payload: bytes, abort=False):
    """Data Packet Payload symbols: DPPSTART + payload + CRC-32 +
    DPPEND (or DPPABORT)."""
    from sim_link_loopback import crc32_payload
    syms = list(DPPSTART)
    syms += list(payload)
    syms += list(crc32_payload(payload).to_bytes(4, "little"))
    syms += list(DPPABORT if abort else DPPEND)
    return syms


def pack_symbol_stream(syms):
    """Pad a symbol stream with IDL to a whole number of data blocks
    and return the Block list."""
    syms = list(syms)
    while len(syms) % 16:
        syms.append(IDL)
    return [data_block(syms[i:i + 16]) for i in range(0, len(syms), 16)]
