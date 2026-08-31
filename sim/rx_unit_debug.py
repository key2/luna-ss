#!/usr/bin/env python3
"""Standalone Gen2BlockReceiver translation check (v2 engine debug).

Feeds a hand-built data-block symbol stream (DPH + length replica + DPP,
at several alignments) and prints the translated Gen1-dialect words.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from amaranth import Module, ClockDomain, ClockSignal, ResetSignal, Elaboratable
from amaranth.sim import Simulator

from luna.gateware.usb.usb3.physical.gen2 import Gen2BlockReceiver
from gw_usb3.tables import BLOCK_CONTROL, BLOCK_DATA

from gen2_coding import (header_packet_syms, dpp_syms, pack_symbol_stream,
                         sds_block, idle_block, HPSTART, DPHSTART,
                         link_command_syms, IDL)


class Bench(Elaboratable):
    def __init__(self):
        self.rx = Gen2BlockReceiver()

    def elaborate(self, platform):
        m = Module()
        m.domains += ClockDomain("ss")
        m.submodules.rx = self.rx
        return m


def main():
    bench = Bench()
    rx = bench.rx
    sim = Simulator(bench)
    sim.add_clock(1 / 156.25e6, domain="ss")

    async def tb(ctx):
        # SDS first so data_mode engages.
        blocks = [sds_block()]
        # A DPH+DPP (setup-like 8-byte payload), then idle, at shifting
        # alignments; then an LC.
        payload = bytes(range(1, 9))
        for pad in range(3):
            syms = [IDL] * pad
            syms += header_packet_syms(0x00000408, len(payload) << 16,
                                       0, 3, start=DPHSTART)
            syms += dpp_syms(payload)
            blocks += pack_symbol_stream(syms)
            blocks += [idle_block()]
        blocks += pack_symbol_stream(link_command_syms(0b0000, 15))
        blocks += [idle_block()] * 2

        words = []
        async def drain(n):
            for _ in range(n):
                await ctx.tick("ss")
                if ctx.get(rx.source.valid):
                    d = ctx.get(rx.source.data)
                    c = ctx.get(rx.source.ctrl)
                    words.append((d, c))

        ctx.set(rx.source.ready, 1)
        ctx.set(rx.rx_valid, 0)
        await ctx.tick("ss").repeat(4)
        for blk in blocks:
            for (s, h, d) in blk.beats():
                ctx.set(rx.rx_valid, 1)
                ctx.set(rx.rx_start, s)
                ctx.set(rx.rx_head, h)
                ctx.set(rx.rx_data, d)
                await ctx.tick("ss")
                if ctx.get(rx.source.valid):
                    words.append((ctx.get(rx.source.data),
                                  ctx.get(rx.source.ctrl)))
        ctx.set(rx.rx_valid, 0)
        await drain(400)

        # Filter out idle words for the printout.
        interesting = [(d, c) for (d, c) in words if d != 0 or c != 0]
        for d, c in interesting:
            print(f"{d:08x} ctrl={c:04b}")

    sim.add_testbench(tb)
    sim.run()


if __name__ == "__main__":
    main()
