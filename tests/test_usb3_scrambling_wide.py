#
# This file is part of LUNA.
#
# Copyright (c) 2026 the luna-ss contributors
# SPDX-License-Identifier: BSD-3-Clause
""" Width-program scrambler equivalence fences (usb3_design.md 13.5).

The 64-bit (``words=2``) scrambler advances the 16-bit LFSR state
twice per beat -- these tests pin the wide elaborations byte-exact
against the historical 32-bit units over the same symbol stream, and
prove the wide scrambler/descrambler pair is an identity.  ``words=1``
elaborations are the historical classes verbatim (covered by
test_usb3_scrambling.py and the shipping-parity fence).
"""

import random
import unittest

from amaranth import Module
from amaranth.sim import Simulator

from luna.gateware.usb.usb3.physical.scrambling import (
    Scrambler, Descrambler)


def _run(dut_module, tb):
    sim = Simulator(dut_module)
    sim.add_clock(1 / 125e6, domain="ss")
    sim.add_testbench(tb)
    sim.run()


class WideScramblerEquivalence(unittest.TestCase):

    N_WORDS = 64   # 32-bit words of stimulus (even)

    def _stimulus(self):
        rng = random.Random(0x515)
        return [rng.getrandbits(32) for _ in range(self.N_WORDS)]

    def _run_narrow(self, words32):
        """The historical 4-symbol scrambler, one 32-bit word/cycle."""
        dut = Scrambler()
        out = []

        async def tb(ctx):
            ctx.set(dut.enable, 1)
            ctx.set(dut.source.ready, 1)
            ctx.set(dut.sink.valid, 1)
            for w in words32:
                ctx.set(dut.sink.data, w)
                await ctx.delay(1e-9)          # settle comb output
                out.append(ctx.get(dut.source.data))
                await ctx.tick("ss")           # LFSR advances
            ctx.set(dut.sink.valid, 0)

        _run(dut, tb)
        return out

    def _run_wide(self, words32):
        """The words=2 scrambler, one 64-bit beat/cycle."""
        dut = Scrambler(words=2)
        out = []

        async def tb(ctx):
            ctx.set(dut.enable, 1)
            ctx.set(dut.source.ready, 1)
            ctx.set(dut.sink.valid, 1)
            for k in range(0, len(words32), 2):
                beat = words32[k] | (words32[k + 1] << 32)
                ctx.set(dut.sink.data, beat)
                await ctx.delay(1e-9)          # settle comb output
                v = ctx.get(dut.source.data)
                out.append(v & 0xFFFFFFFF)
                out.append(v >> 32)
                await ctx.tick("ss")           # LFSR advances by two
            ctx.set(dut.sink.valid, 0)

        _run(dut, tb)
        return out

    def test_wide_matches_narrow(self):
        """words=2 must emit the exact byte stream of words=1."""
        words = self._stimulus()
        narrow = self._run_narrow(words)
        wide = self._run_wide(words)
        self.assertEqual(
            [hex(w) for w in wide], [hex(w) for w in narrow],
            "the 64-bit scrambler diverged from the 32-bit sequence")

    def test_wide_round_trip(self):
        """Descrambler(words=2) inverts Scrambler(words=2)."""
        words = self._stimulus()

        m = Module()
        m.submodules.scr = scr = Scrambler(words=2,
                                           initial_value=0xffff)
        m.submodules.dsc = dsc = Descrambler(words=2)
        out = []

        async def tb(ctx):
            ctx.set(scr.enable, 1)
            ctx.set(dsc.enable, 1)
            ctx.set(scr.source.ready, 1)
            ctx.set(dsc.source.ready, 1)
            ctx.set(scr.sink.valid, 1)
            ctx.set(dsc.sink.valid, 1)
            for k in range(0, len(words), 2):
                beat = words[k] | (words[k + 1] << 32)
                ctx.set(scr.sink.data, beat)
                await ctx.delay(1e-9)
                ctx.set(dsc.sink.data, ctx.get(scr.source.data))
                await ctx.delay(1e-9)
                v = ctx.get(dsc.source.data)
                out.append(v & 0xFFFFFFFF)
                out.append(v >> 32)
                await ctx.tick("ss")

        _run(m, tb)
        self.assertEqual([hex(w) for w in out],
                         [hex(w) for w in words],
                         "wide scramble/descramble is not an identity")


if __name__ == "__main__":
    unittest.main()
