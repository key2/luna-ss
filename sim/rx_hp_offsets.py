#!/usr/bin/env python3
"""Gen2BlockReceiver: header packets at every symbol offset (bug #42 hunt).

The real host places packets at ANY symbol position within a data block
[7.2.1.3] and link commands back to back [7.2.2.3]; every 20-symbol
header packet necessarily crosses a data-block boundary.  The link sims
only ever feed block-aligned, idle-padded constructs -- this bench
sweeps the placement surface the silicon sees:

  * an HPSTART header packet at symbol offsets 0..15;
  * a DPHSTART DPH (+replica) + DPP at offsets 0..15;
  * back-to-back constructs (LC+HP, HP+HP, LC at odd offsets);
  * PIPE rx_valid gaps in the style of RxGearbox132's nibble-wrap dead
    cycle (one gap every N beats, all phases), including mid-block.

Each case checks the translated Gen1-dialect byte stream exactly.

Run: .venv/bin/python -u sim/rx_hp_offsets.py [GAP=0|33|7] [VERBOSE=1]
"""
import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from amaranth import Module, ClockDomain, Elaboratable
from amaranth.sim import Simulator

from luna.gateware.usb.usb3.physical.gen2 import Gen2BlockReceiver
from gw_usb3.tables import BLOCK_CONTROL, BLOCK_DATA

from gen2_coding import (header_packet_syms, dpp_syms, pack_symbol_stream,
                         sds_block, idle_block, HPSTART, DPHSTART,
                         link_command_syms, IDL)

VERBOSE = int(os.environ.get("VERBOSE", "0"))
# Gap cadence: 0 = no valid gaps; N = one rx_valid gap every N valid
# beats (RxGearbox132's wrap gap lands every ~33 beats on silicon; 7
# makes gaps hit every block phase quickly).
GAP = int(os.environ.get("GAP", "0"))

K_SHP, K_EPF, K_SDP, K_END, K_EDB, K_SLC = 0xFB, 0xF7, 0x5C, 0xFD, 0x7C, 0xFE


def hp_syms(seed):
    """A TP-like header packet (HPSTART framing, 20 symbols)."""
    dw0 = 0x00000404 | ((seed & 0xFF) << 16)      # type=TP(4)
    dw1 = 0x11223344 ^ seed
    dw2 = 0x55667788 ^ (seed << 1)
    return header_packet_syms(dw0 & 0xFFFFFFFF, dw1 & 0xFFFFFFFF,
                              dw2 & 0xFFFFFFFF, seq=seed & 0xF)


def dph_dpp_syms(seed, payload):
    dw0 = 0x00000408 | ((seed & 0xFF) << 16)      # type=DPH(8)
    dw1 = (len(payload) << 16) | 0x1234
    dw2 = 0x9abcdef0 ^ seed
    syms = header_packet_syms(dw0 & 0xFFFFFFFF, dw1 & 0xFFFFFFFF,
                              dw2 & 0xFFFFFFFF, seq=seed & 0xF,
                              start=DPHSTART)
    return syms + dpp_syms(payload)


def expected_hp_bytes(syms):
    """Expected translated Gen1 (byte, k) stream for a symbol list built
    by hp_syms/dph_dpp_syms/link_command_syms (drop Gen2-only content:
    the DPH length replica; map framing)."""
    out = []
    i = 0
    n = len(syms)
    while i < n:
        s = syms[i]
        if s == IDL:
            i += 1
            continue
        if i + 4 <= n and tuple(syms[i:i+4]) == HPSTART:
            out += [(K_SHP, 1)] * 3 + [(K_EPF, 1)]
            body = syms[i+4:i+20]
            out += [(b, 0) for b in body]
            i += 20
        elif i + 4 <= n and tuple(syms[i:i+4]) == DPHSTART:
            out += [(K_SHP, 1)] * 3 + [(K_EPF, 1)]
            body = syms[i+4:i+20]
            out += [(b, 0) for b in body]
            i += 22                      # skip the 2-byte replica
        elif i + 4 <= n and syms[i] == 0x96:      # DPPSTART
            out += [(K_SDP, 1)] * 3 + [(K_EPF, 1)]
            i += 4
        elif i + 4 <= n and syms[i] in (0x65, 0x69):   # DPPEND/ABORT
            k = K_EDB if syms[i] == 0x69 else K_END
            out += [(k, 1)] * 3 + [(K_EPF, 1)]
            i += 4
        elif i + 4 <= n and syms[i] == 0x4B:      # LCSTART
            out += [(K_SLC, 1)] * 3 + [(K_EPF, 1)]
            out += [(b, 0) for b in syms[i+4:i+8]]
            i += 8
        else:
            out.append((s, 0))
            i += 1
    return out


class Bench(Elaboratable):
    def __init__(self):
        self.rx = Gen2BlockReceiver()

    def elaborate(self, platform):
        m = Module()
        m.domains += ClockDomain("ss")
        m.submodules.rx = self.rx
        return m


def words_to_bytes(words):
    """(data32, ctrl4) words -> [(byte, k)], byte 0 = data[0:8]."""
    out = []
    for d, c in words:
        for i in range(4):
            out.append(((d >> (8 * i)) & 0xFF, (c >> i) & 1))
    return out


def strip_idle(pairs):
    return [(b, k) for (b, k) in pairs if not (b == 0 and k == 0)]


def main():
    bench = Bench()
    rx = bench.rx
    sim = Simulator(bench)
    sim.add_clock(1 / 156.25e6, domain="ss")

    failures = []

    async def tb(ctx):
        gap_cnt = 0

        async def feed(blocks):
            nonlocal gap_cnt
            words = []
            for blk in blocks:
                for (s, h, d) in blk.beats():
                    if GAP:
                        gap_cnt += 1
                        if gap_cnt % GAP == 0:
                            ctx.set(rx.rx_valid, 0)
                            await ctx.tick("ss")
                            if ctx.get(rx.source.valid):
                                words.append((ctx.get(rx.source.data),
                                              ctx.get(rx.source.ctrl)))
                    ctx.set(rx.rx_valid, 1)
                    ctx.set(rx.rx_start, s)
                    ctx.set(rx.rx_head, h)
                    ctx.set(rx.rx_data, d)
                    await ctx.tick("ss")
                    if ctx.get(rx.source.valid):
                        words.append((ctx.get(rx.source.data),
                                      ctx.get(rx.source.ctrl)))
            ctx.set(rx.rx_valid, 0)
            return words

        async def drain(words, n):
            for _ in range(n):
                await ctx.tick("ss")
                if ctx.get(rx.source.valid):
                    words.append((ctx.get(rx.source.data),
                                  ctx.get(rx.source.ctrl)))

        async def run_case(name, syms):
            words = await feed(pack_symbol_stream(list(syms))
                               + [idle_block()])
            await drain(words, 200)
            got = strip_idle(words_to_bytes(words))
            want = expected_hp_bytes(list(syms))
            # The engine may flush trailing idle pad inside the last
            # word; strip_idle removed (0,0) pairs from both sides of
            # comparison -- want has no (0,0) unless header bytes are 0.
            want = [(b, k) for (b, k) in want if not (b == 0 and k == 0)]
            if got != want:
                failures.append(name)
                print(f"FAIL {name}")
                if VERBOSE:
                    print(f"  want: {[(hex(b), k) for b, k in want]}")
                    print(f"  got : {[(hex(b), k) for b, k in got]}")
                else:
                    # first divergence
                    for j in range(max(len(got), len(want))):
                        g = got[j] if j < len(got) else None
                        w = want[j] if j < len(want) else None
                        if g != w:
                            print(f"  first diff at byte {j}: "
                                  f"want={w and (hex(w[0]), w[1])} "
                                  f"got={g and (hex(g[0]), g[1])}")
                            break
            else:
                if VERBOSE:
                    print(f"pass {name}")

        ctx.set(rx.source.ready, 1)
        ctx.set(rx.rx_valid, 0)
        await ctx.tick("ss").repeat(4)
        await feed([sds_block()])          # data_mode on

        # ── HP at every symbol offset ──
        for off in range(16):
            await run_case(f"hp@{off}", [IDL] * off + hp_syms(off + 1))

        # ── DPH+DPP at every offset (replica shifts by 2) ──
        payload = bytes(range(1, 13))
        for off in range(16):
            await run_case(f"dph@{off}",
                           [IDL] * off + dph_dpp_syms(off + 1, payload))

        # ── LC at every offset ──
        for off in range(16):
            await run_case(f"lc@{off}",
                           [IDL] * off + link_command_syms(0b0000, off))

        # ── back-to-back constructs ──
        await run_case("lc+hp", link_command_syms(0b1000, 0) + hp_syms(3))
        await run_case("hp+hp", hp_syms(4) + hp_syms(5))
        await run_case("lc+lc+hp@2",
                       [IDL] * 2 + link_command_syms(0b1000, 0)
                       + link_command_syms(0b0000, 7) + hp_syms(6))
        await run_case("hp+lc+dph@6",
                       [IDL] * 6 + hp_syms(7)
                       + link_command_syms(0b0001, 2)
                       + dph_dpp_syms(8, payload))

    sim.add_testbench(tb)
    sim.run()

    if failures:
        print(f"RX-HP-OFFSETS FAIL ({len(failures)}): {failures}")
        return 1
    print("RX-HP-OFFSETS PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
