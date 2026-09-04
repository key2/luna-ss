#
# This file is part of LUNA.
#
# Copyright (c) 2026 the luna-ss contributors
# SPDX-License-Identifier: BSD-3-Clause
""" Width-program CRC equivalence fences (usb3_design.md 13.5/13.6).

The 64-bit CRC surfaces (``words=2``) are built by COMPOSING the
spec-lifted 32-bit transformations -- these tests pin them byte-exact
against the proven byte-serial references from the link sims, over
every tail length and random contents.  The ``words=1`` elaborations
are the historical classes verbatim (covered by test_usb3_crc.py and
the shipping-parity fence).
"""

import os
import random
import sys
import unittest

from amaranth.sim import Simulator

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "sim"))
from sim_link_loopback import crc16_header, crc32_payload  # noqa: E402

from luna.gateware.usb.usb3.link.crc import (                # noqa: E402
    HeaderPacketCRC, DataPacketPayloadCRC)


class WideHeaderCRCTest(unittest.TestCase):

    def test_two_word_advance_matches_reference(self):
        """8B+4B advance over random 12-byte headers == crc16_header."""
        rng = random.Random(0x47)
        cases = [[rng.getrandbits(32) for _ in range(3)]
                 for _ in range(64)]

        dut = HeaderPacketCRC(words=2)
        failures = []

        async def tb(ctx):
            for dws in cases:
                ctx.set(dut.clear, 1)
                await ctx.tick("ss")
                ctx.set(dut.clear, 0)
                # DW0+DW1 in one two-word advance...
                ctx.set(dut.data_input2, dws[0] | (dws[1] << 32))
                ctx.set(dut.advance_crc2, 1)
                await ctx.tick("ss")
                ctx.set(dut.advance_crc2, 0)
                # ... then DW2 through the historical one-word port.
                ctx.set(dut.data_input, dws[2])
                ctx.set(dut.advance_crc, 1)
                await ctx.tick("ss")
                ctx.set(dut.advance_crc, 0)
                got = ctx.get(dut.crc)
                want = crc16_header(dws)
                if got != want:
                    failures.append((dws, got, want))

        sim = Simulator(dut)
        sim.add_clock(1 / 125e6, domain="ss")
        sim.add_testbench(tb)
        sim.run()
        self.assertEqual(failures, [],
                         [f"dws={[hex(d) for d in c[0]]}: got {c[1]:#06x} "
                          f"want {c[2]:#06x}" for c in failures[:4]])


class WideDataCRCTest(unittest.TestCase):

    def test_all_tails_match_reference(self):
        """Full 8B beats + every tail length 1..7 (and exact-8 ends),
        lengths 1..64 plus larger sprinkles, against crc32_payload;
        the next_crc_xB outputs must equal the post-advance value."""
        rng = random.Random(0x2E)
        lengths = list(range(1, 65)) + [100, 127, 128, 1024 + 3]
        cases = [bytes(rng.getrandbits(8) for _ in range(n))
                 for n in lengths]

        dut = DataPacketPayloadCRC(words=2)
        failures = []

        async def tb(ctx):
            for data in cases:
                ctx.set(dut.clear, 1)
                await ctx.tick("ss")
                ctx.set(dut.clear, 0)

                full, tail = divmod(len(data), 8)
                for k in range(full):
                    beat = int.from_bytes(data[8 * k:8 * k + 8], "little")
                    ctx.set(dut.data_input2, beat)
                    ctx.set(dut.advance_2words, 1)
                    await ctx.tick("ss")
                    ctx.set(dut.advance_2words, 0)

                predicted = None
                if tail:
                    beat = int.from_bytes(
                        data[8 * full:].ljust(8, b"\0"), "little")
                    ctx.set(dut.data_input2, beat)
                    if tail >= 4:
                        # settle combinational next-CRC and predict
                        await ctx.delay(1e-9)
                        predicted = ctx.get(
                            getattr(dut, f"next_crc_{tail}B"))
                        ctx.set(getattr(dut, f"advance_{tail}B"), 1)
                        await ctx.tick("ss")
                        ctx.set(getattr(dut, f"advance_{tail}B"), 0)
                    else:
                        await ctx.delay(1e-9)
                        predicted = ctx.get(
                            getattr(dut, f"next_crc_{tail}B"))
                        ctx.set(getattr(dut, f"advance_{tail}B"), 1)
                        await ctx.tick("ss")
                        ctx.set(getattr(dut, f"advance_{tail}B"), 0)

                got = ctx.get(dut.crc)
                want = crc32_payload(data)
                if got != want or (predicted is not None
                                   and predicted != want):
                    failures.append((len(data), got, predicted, want))

        sim = Simulator(dut)
        sim.add_clock(1 / 125e6, domain="ss")
        sim.add_testbench(tb)
        sim.run()
        self.assertEqual(failures, [],
                         [f"len={c[0]}: got {c[1]:#010x} "
                          f"next={c[2]} want {c[3]:#010x}"
                          for c in failures[:6]])


if __name__ == "__main__":
    unittest.main()
