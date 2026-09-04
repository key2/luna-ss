#!/usr/bin/env python3
"""Full Gen2 PHY RX chain simulation (bug #42 hunt).

Every earlier Gen2 sim feeds the RTL Descrambler directly; the silicon
path in front of it -- raw serdes words at the RECOVERED clock through
``RxGearbox132`` (block alignment, SKP tracking, LFSR seed extraction)
and the rx->pclk ``AsyncFifo`` -- has never been in a sim loop with our
MAC.  This bench serializes scrambled 132-bit blocks to the raw 64-bit
wire stream (LSB-first bit order, arbitrary initial bit offset,真 async
clocks: rx 161.133 MHz vs pclk 156.25 MHz) and runs the REAL chain:

    python host (blocks -> ScramblerModel -> bit serializer)
      -> RxGearbox132 (rx domain)
      -> AsyncFifo (rx -> ss)  [src_valid = ~Empty, RdEn=1, like phy.py]
      -> Descrambler (ss domain, descrambler_init = rxgears.next_lfsr)
      -> Gen2BlockReceiver (ss domain)
      -> translated Gen1-dialect word check

Traffic mirrors a real host: SYNC-led training (gearbox lock), TS1/TS2,
SDS, then a U0 data phase with 24-symbol SKP OS every 40 blocks
[6.4.3.3], LDN keepalives, and header packets / DPs / link commands at
sweeping symbol offsets [7.2.1.3: any symbol position, crossing
blocks].

Run: .venv/bin/python -u sim/rx_chain_full.py  [OFFSET=n] [INVERT=1]
"""
import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from amaranth import Module, ClockDomain, Elaboratable, Signal, DomainRenamer
from amaranth.sim import Simulator

from luna.gateware.usb.usb3.physical.gen2 import Gen2BlockReceiver
from gw_usb3.gearbox import RxGearbox132
from gw_usb3.scramble import Descrambler
from gw_usb3.async_fifo import AsyncFifo
from gw_usb3.tables import BLOCK_CONTROL, BLOCK_DATA, BlockType

from gen2_coding import (ScramblerModel, sync_block, tseq_block, ts1_block,
                         ts2_block, sds_block, idle_block, skp_block,
                         data_block, header_packet_syms, dpp_syms,
                         link_command_syms, beats_to_syms, HPSTART, DPHSTART,
                         IDL)

OFFSET = int(os.environ.get("OFFSET", "5"))     # initial wire bit offset
INVERT = int(os.environ.get("INVERT", "0"))     # wire polarity inversion
VERBOSE = int(os.environ.get("VERBOSE", "0"))

K_SHP, K_EPF, K_SDP, K_END, K_EDB, K_SLC = 0xFB, 0xF7, 0x5C, 0xFD, 0x7C, 0xFE

RX_CLK = 161.1328125e6         # 10.3125 GHz / 64 (recovered)
SS_CLK = 156.25e6              # pclk at the 10G trim


# ── wire serializer ──────────────────────────────────────────────────

class WireStream:
    """LSB-first bit serializer (the tb_p132brxgears_v6 convention)."""

    def __init__(self, offset=0, invert=False):
        self.bits = [0] * offset
        self.invert = bool(invert)

    def push_bits(self, value, nbits):
        v = value ^ ((1 << nbits) - 1) if self.invert else value
        self.bits += [(v >> i) & 1 for i in range(nbits)]

    def push_scrambled_block(self, model, blk):
        """Scramble a Block with the python model and serialize it."""
        head_bits = 0b1100 if blk.head == BLOCK_CONTROL else 0b0011
        beats = [model.feed(s, h, d) for (s, h, d) in blk.beats()]
        syms = beats_to_syms(beats)[:len(blk.syms)]
        self.push_bits(head_bits, 4)
        for b in syms:
            self.push_bits(b, 8)

    def pop_word(self):
        assert len(self.bits) >= 64
        word = sum(b << i for i, b in enumerate(self.bits[:64]))
        del self.bits[:64]
        return word

    def n_words(self):
        return len(self.bits) // 64


# ── expected translated bytes for the data phase ─────────────────────

def expected_bytes(syms):
    out = []
    i, n = 0, len(syms)
    dpp_len = 0
    while i < n:
        s = syms[i]
        if s == IDL:
            i += 1
            continue
        if i + 4 <= n and tuple(syms[i:i+4]) == HPSTART:
            out += [(K_SHP, 1)] * 3 + [(K_EPF, 1)]
            body = syms[i+4:i+20]
            out += [(b, 0) for b in body]
            if body[0] & 0x1F == 8:                  # DATA-type header
                dpp_len = body[6] | (body[7] << 8)
            i += 20
        elif i + 4 <= n and tuple(syms[i:i+4]) == DPHSTART:
            out += [(K_SHP, 1)] * 3 + [(K_EPF, 1)]
            body = syms[i+4:i+20]
            out += [(b, 0) for b in body]
            dpp_len = body[6] | (body[7] << 8)
            i += 24                        # 2x2-byte replicas swallowed
        elif syms[i] == 0x96:              # DPPSTART
            out += [(K_SDP, 1)] * 3 + [(K_EPF, 1)]
            i += 4
            # payload + CRC-32 verbatim (values may collide with
            # framing symbols; extent is length-tracked, like the RTL)
            ext = dpp_len + 4
            out += [(b, 0) for b in syms[i:i+ext]]
            i += ext
            # terminator framing
            k = K_EDB if syms[i] == 0x69 else K_END
            out += [(k, 1)] * 3 + [(K_EPF, 1)]
            i += 4
        elif syms[i] == 0x4B:              # LCSTART
            out += [(K_SLC, 1)] * 3 + [(K_EPF, 1)]
            out += [(b, 0) for b in syms[i+4:i+8]]
            i += 8
        else:
            out.append((s, 0))
            i += 1
    return [(b, k) for (b, k) in out if not (b == 0 and k == 0)]


# ── DUT ──────────────────────────────────────────────────────────────

class Bench(Elaboratable):
    def __init__(self):
        self.gears = RxGearbox132()
        self.descr = Descrambler()
        self.fifo = AsyncFifo(dsize=69, asize=8, aempt=1, afull=255)
        self.rx = Gen2BlockReceiver()
        self.ltssm_training = Signal(init=1)
        self.i_data = Signal(64)
        self.i_valid = Signal()

    def elaborate(self, platform):
        m = Module()
        m.domains += ClockDomain("ss")
        m.domains += ClockDomain("rx")

        m.submodules.gears = gears = DomainRenamer("rx")(self.gears)
        m.submodules.fifo = fifo = DomainRenamer(
            {"wr": "rx", "rd": "ss"})(self.fifo)
        m.submodules.descr = descr = DomainRenamer(
            {"sync": "ss"})(self.descr)
        m.submodules.rx = rx = self.rx

        # exactly the datapath.py RX wiring
        src_valid = Signal()
        m.d.ss += src_valid.eq(~fifo.Empty)
        m.d.comb += [
            gears.i_data_valid.eq(self.i_valid),
            gears.i_data.eq(self.i_data),
            fifo.Data.eq(0),
            fifo.Data[0:64].eq(gears.M_DATA),
            fifo.Data[64:68].eq(gears.M_SYNCHEAD),
            fifo.Data[68].eq(gears.M_STARTBLOCK),
            fifo.WrEn.eq(gears.M_VALID),
            fifo.RdEn.eq(1),

            descr.LTSSM_is_Training.eq(self.ltssm_training),
            descr.descrambler_init.eq(gears.next_lfsr),
            descr.descramble_en.eq(1),
            descr.data_in_valid.eq(src_valid),
            descr.data_in_start_block.eq(fifo.Q[68]),
            descr.data_in_block_head.eq(fifo.Q[64:68]),
            descr.data_in.eq(fifo.Q[0:64]),

            rx.rx_data.eq(descr.data_out),
            rx.rx_valid.eq(descr.data_out_valid),
            rx.rx_start.eq(descr.data_out_start_block),
            rx.rx_head.eq(descr.data_out_block_head),
        ]
        return m


def build_traffic():
    """Returns (blocks, train_end_block_idx, data_syms).

    ``blocks``: full block sequence (training + data phase).
    ``data_syms``: the clear symbol stream of all post-SDS data blocks
    (for the expectation builder).
    """
    blocks = []

    # ── training: SYNC-led (gearbox lock), TSEQ, TS1/TS2 with SKPs ──
    blocks += [sync_block()] * 4
    blocks += [tseq_block()] * 16
    for _ in range(4):
        blocks += [sync_block()] + [ts1_block()] * 16 + [skp_block()]
    for _ in range(2):
        blocks += [sync_block()] + [ts2_block()] * 16 + [skp_block()]
    train_end = len(blocks)

    # ── U0 data phase: one continuous symbol stream chopped into data
    # blocks with SKP OS interleaved every 40 blocks ──
    syms = []

    def pad(n):
        syms.extend([IDL] * n)

    def ldn():
        syms.extend(link_command_syms(0b1000, 0))          # LDN

    def lgood(n):
        syms.extend(link_command_syms(0b0000, n))

    def hp(seed):
        dw0 = 0x00000404 | ((seed & 0xFF) << 16)
        syms.extend(header_packet_syms(dw0, 0x11223344 ^ seed,
                                       0x55667788 ^ seed, seq=seed & 0xF))

    def dp(seed, payload):
        dw0 = 0x00000408 | ((seed & 0xFF) << 16)
        syms.extend(header_packet_syms(dw0, (len(payload) << 16) | 0x1234,
                                       0x9abcdef0 ^ seed, seq=seed & 0xF,
                                       start=DPHSTART))
        syms.extend(dpp_syms(payload))

    # idle lead-in with keepalives
    pad(64); ldn(); pad(40); ldn(); pad(13)
    # header packets sweeping symbol offsets (pads 1..17 shift the
    # stream through every alignment; constructs cross block bounds)
    for k in range(17):
        hp(k + 1)
        pad(k + 1)
        if k % 3 == 0:
            ldn()
    # DPs with several payload sizes (odd tails included)
    for k, size in enumerate((8, 12, 33, 128)):
        dp(k + 1, bytes((7 * i + k) & 0xFF for i in range(size)))
        pad(2 * k + 1)
    # all-5Ah payload: whole-idle beats as construct PAYLOAD (the
    # run-replay correctness case of the #43 idle compression)
    dp(9, bytes([0x5A] * 40))
    pad(5)
    dp(10, bytes([0x5A] * 200))
    pad(2)
    # back-to-back constructs
    lgood(3); hp(40)
    hp(41); lgood(4)
    pad(3)

    # SKP endurance: 100 SKP OS at the 40-block cadence, an LGOOD after
    # each (proves descrambling stays aligned across every reseed)
    endurance_marks = 100

    # chop into data blocks, inserting a SKP OS every 40 blocks
    data_syms = list(syms)
    while len(data_syms) % 16:
        data_syms.append(IDL)
    data_blocks = [data_block(data_syms[i:i+16])
                   for i in range(0, len(data_syms), 16)]

    blocks.append(skp_block())
    blocks.append(sds_block())
    since_skp = 0
    for db in data_blocks:
        blocks.append(db)
        since_skp += 1
        if since_skp >= 40:
            blocks.append(skp_block())
            since_skp = 0

    # endurance phase
    endur_syms = []
    for k in range(endurance_marks):
        blk_syms = []
        blk_syms += link_command_syms(0b0000, k & 0xF)
        blk_syms += [IDL] * 8
        endur_syms += blk_syms
        blocks.append(data_block(blk_syms))
        blocks += [idle_block()] * 39
        blocks.append(skp_block())
        endur_syms += [IDL] * 39 * 16
    blocks += [idle_block()] * 8
    endur_syms += [IDL] * 8 * 16

    return blocks, train_end, data_syms + endur_syms


def main():
    bench = Bench()
    sim = Simulator(bench)
    sim.add_clock(1 / SS_CLK, domain="ss")
    sim.add_clock(1 / RX_CLK, domain="rx")

    blocks, train_end, data_syms = build_traffic()
    want = expected_bytes(data_syms)

    # serialize: garbage words, then everything, continuously
    stream = WireStream(offset=OFFSET, invert=INVERT)
    model = ScramblerModel()
    words = []
    import random
    rng = random.Random(42)
    for _ in range(12):
        words.append(rng.getrandbits(64))
    train_end_word = None
    for i, blk in enumerate(blocks):
        stream.push_scrambled_block(model, blk)
        while stream.n_words():
            words.append(stream.pop_word())
        if i == train_end and train_end_word is None:
            train_end_word = len(words)
    # Drain phase: keep the wire STREAMING (scrambled idle blocks) while
    # the DUT chain flushes -- a real CDR never stops mid-U0, and the
    # vendor gearbox free-runs garbage if i_data_valid drops.
    for _ in range(400):
        stream.push_scrambled_block(model, idle_block())
    while stream.n_words():
        words.append(stream.pop_word())

    state = {"done": False}
    got = []
    counters = {"sds": 0, "rxv": 0, "qmax": 0}

    async def feeder(ctx):
        ctx.set(bench.ltssm_training, 1)
        for i, w in enumerate(words):
            if train_end_word is not None and i == train_end_word:
                ctx.set(bench.ltssm_training, 0)
            ctx.set(bench.i_valid, 1)
            ctx.set(bench.i_data, w)
            await ctx.tick("rx")
        ctx.set(bench.i_valid, 0)
        state["feeding_done"] = True
        # let the ss side drain
        await ctx.tick("rx").repeat(600)
        state["done"] = True

    descr_log = []          # (cyc, start, head, data) at descrambler out
    eng_log = []            # (cyc, qlvl, st, have, wen, outlvl, srcv)

    async def collector(ctx):
        rx = bench.rx
        descr = bench.descr
        cyc = 0
        ctx.set(rx.source.ready, 1)
        while not state["done"]:
            await ctx.tick("ss")
            cyc += 1
            if state.get("feeding_done") and "feed_end" not in state:
                state["feed_end"] = cyc
            ql = ctx.get(rx.queue_level)
            if ql > counters["qmax"]:
                counters["qmax"] = ql
            eng_log.append((cyc, ql,
                            ctx.get(rx.debug_state), ctx.get(rx.debug_have),
                            ctx.get(rx.debug_wen), ctx.get(rx.debug_out_lvl),
                            ctx.get(rx.source.valid)))
            if ctx.get(descr.data_out_valid):
                descr_log.append((cyc,
                                  ctx.get(descr.data_out_start_block),
                                  ctx.get(descr.data_out_block_head),
                                  ctx.get(descr.data_out)))
            if ctx.get(rx.sds_detected):
                counters["sds"] += 1
            if ctx.get(rx.source.valid):
                d = ctx.get(rx.source.data)
                c = ctx.get(rx.source.ctrl)
                counters["rxv"] += 1
                # stop collecting once the feed ends: with i_data_valid
                # low the vendor gearbox free-runs garbage beats (a
                # bench artifact; a real CDR never stops mid-U0)
                if "feed_end" not in state:
                    for i in range(4):
                        b, k = (d >> (8 * i)) & 0xFF, (c >> i) & 1
                        if b or k:
                            got.append((b, k))
            counters["q_final"] = ctx.get(rx.queue_level) \
                if "feed_end" not in state else counters.get("q_final", 0)

    sim.add_testbench(feeder)
    sim.add_testbench(collector, background=True)
    sim.run()

    print(f"fed {len(words)} raw words; sds_detected={counters['sds']} "
          f"translated_words={counters['rxv']}")
    print(f"expected {len(want)} non-idle bytes, got {len(got)}")

    ok = got == want
    if not ok:
        # locate first divergence
        for j in range(max(len(got), len(want))):
            g = got[j] if j < len(got) else None
            w = want[j] if j < len(want) else None
            if g != w:
                lo = max(0, j - 8)
                print(f"first diff at byte {j}:")
                print(f"  want[{lo}:{j+8}]: "
                      f"{[(hex(b), k) for b, k in want[lo:j+8]]}")
                print(f"  got [{lo}:{j+8}]: "
                      f"{[(hex(b), k) for b, k in got[lo:j+8]]}")
                break
    if VERBOSE:
        print("head of got:", [(hex(b), k) for b, k in got[:40]])

    # ── anomaly hunt at the descrambler level: any DATA beat that is
    # neither pure idle nor part of a recognizable construct window ──
    IDLE_BEAT = 0x5A5A5A5A5A5A5A5A
    feed_end = state.get("feed_end", 10**9)
    lc_beats = [j for j, (c, s, h, d) in enumerate(descr_log)
                if h == BLOCK_DATA and (d >> 32) == 0x4B4B4B36]
    print(f"descrambler beats logged: {len(descr_log)} "
          f"(feed_end at cyc {feed_end}); LC-pattern beats: {len(lc_beats)}")
    # expected constructs (pre-tail) that never appeared: look for
    # garbage data beats BEFORE feed end -- a diverged descramble window
    garbage = []
    for j, (cyc, s, h, d) in enumerate(descr_log):
        if cyc >= feed_end:
            break
        if h != BLOCK_DATA or d == IDLE_BEAT:
            continue
        b0 = (d >> 56) & 0xFF
        # construct-plausible first bytes (framing, or continuation of a
        # construct = anything, so only flag beats where BOTH halves
        # look non-constructy is hopeless -- instead flag beats within
        # otherwise-idle surroundings that match nothing we sent)
        garbage.append((j, cyc, s, d))
    # dump context around the last pre-tail window (where LGOOD#100 was)
    pre_lcs = [j for j in lc_beats if descr_log[j][0] < feed_end]
    print(f"pre-tail LC beats: {len(pre_lcs)}; last 3 at cycles "
          f"{[descr_log[j][0] for j in pre_lcs[-3:]]}")
    if pre_lcs:
        c0 = descr_log[pre_lcs[-1]][0]
        print(f"engine trace around last LC beat (cyc {c0}):")
        for (cyc, ql, st, hv, wen, ol, sv) in eng_log:
            if c0 - 4 <= cyc <= c0 + 40:
                print(f"  cyc={cyc} qlvl={ql} st={st} have={hv} wen={wen} "
                      f"outlvl={ol} srcv={sv}")

    # Bug #43 bound: with idle run compression the input queue level is
    # O(constructs in flight) -- transient backlog during back-to-back
    # construct bursts is expected and DRAINS; the historical per-beat
    # idle enqueue instead ratcheted the level up monotonically (~650
    # over this traffic, never returning) toward silent overflow.
    qmax = counters["qmax"]
    q_final = counters.get("q_final", -1)
    print(f"input queue high-water: {qmax} (sanity bound 256); "
          f"level at drain end: {q_final} (must be 0)")

    if ok and counters["sds"] >= 1 and qmax < 256 and q_final == 0:
        print("RX-CHAIN-FULL PASS")
        return 0
    print("RX-CHAIN-FULL FAIL")
    return 1


if __name__ == "__main__":
    sys.exit(main())
