#
# This file is part of LUNA.
#
# Copyright (c) 2026 the luna-ss contributors
# SPDX-License-Identifier: BSD-3-Clause
""" Gen2 TX beat pacing test.

The gw_usb3 PHY's Gen2 transmit path buffers MAC beats in a 32-deep
gearbox FIFO drained at the 128b/132b wire payload rate: 132 wire bits
(one block) per 128 payload bits (two 64-bit beats), i.e. 32 beats per
33 pclk cycles.  A MAC that asserts tx_datavalid on every beat
therefore gains one queued beat per 33 cycles and silently overflows
the FIFO after ~1056 sustained cycles -- far shorter than a real
training sequence (Gen2 TSEQ alone is 524,288 ordered sets), so the
wire stream would be corrupted before the link partner ever locks.

``Gen2BlockTransmitter`` must insert one dead beat (tx_valid low) at a
block boundary every 16 blocks (32 valid beats + 1 gap = 33 cycles =
exactly 16 x 132 wire bits at 10 GT/s), keeping the FIFO occupancy
bounded and rate-matched with zero long-term drift.  This test streams
the transmitter against the FIFO model for long enough that an unpaced
transmitter overflows (recorded RED baseline: occupancy grows ~1/33
without bound; with pacing the model stays in the low single digits).
"""

import unittest

from amaranth.sim import Simulator

from luna.gateware.usb.usb3.physical.gen2 import Gen2BlockTransmitter


class Gen2TxPacingTest(unittest.TestCase):

    FIFO_DEPTH = 32

    def _run_stream(self, configure, cycles=6000):
        """Streams the transmitter and returns (max_level, overflowed)."""
        dut = Gen2BlockTransmitter(tseq_count=65536)

        results = {}

        async def tb(ctx):
            configure(ctx, dut)
            level = 0
            max_level = 0
            overflowed = False
            for cyc in range(cycles):
                await ctx.tick("ss")
                if ctx.get(dut.tx_valid):
                    level += 1
                if cyc % 33 != 0 and level > 0:
                    level -= 1
                max_level = max(max_level, level)
                if level > self.FIFO_DEPTH:
                    overflowed = True
            results["max"] = max_level
            results["overflow"] = overflowed

        sim = Simulator(dut)
        sim.add_clock(1 / 156.25e6, domain="ss")
        sim.add_testbench(tb)
        sim.run()
        return results["max"], results["overflow"]

    def test_tseq_stream_is_paced(self):
        """Training streams (the longest sustained TX) must not overflow
        the PHY's 32-deep gearbox FIFO."""
        def configure(ctx, dut):
            ctx.set(dut.send_tseq_burst, 1)
        max_level, overflowed = self._run_stream(configure)
        self.assertFalse(
            overflowed,
            f"unpaced TSEQ stream overran the 32-deep PHY TX FIFO "
            f"(max occupancy {max_level})")

    def test_ts1_stream_is_paced(self):
        def configure(ctx, dut):
            ctx.set(dut.send_ts1_burst, 1)
        max_level, overflowed = self._run_stream(configure)
        self.assertFalse(
            overflowed,
            f"unpaced TS1 stream overran the 32-deep PHY TX FIFO "
            f"(max occupancy {max_level})")

    def test_idle_stream_is_paced(self):
        """U0 idle (SDS + idle data blocks) is also a sustained stream."""
        def configure(ctx, dut):
            ctx.set(dut.idle_mode, 1)
        max_level, overflowed = self._run_stream(configure)
        self.assertFalse(
            overflowed,
            f"unpaced idle stream overran the 32-deep PHY TX FIFO "
            f"(max occupancy {max_level})")


if __name__ == "__main__":
    unittest.main()
