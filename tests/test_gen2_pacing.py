#
# This file is part of LUNA.
#
# Copyright (c) 2026 the luna-ss contributors
# SPDX-License-Identifier: BSD-3-Clause
""" Gen2 TX beat pacing test (closed loop; bugs #44 and the original
overflow hazard).

The gw_usb3 PHY's Gen2 transmit path buffers MAC beats in a 32-deep
gearbox FIFO drained at the 128b/132b wire payload rate (32 beats per
33 pclk cycles).  Two failure modes bracket the design:

* OVERFLOW: a MAC that asserts tx_datavalid on every beat gains one
  queued beat per 33 cycles and silently overflows after ~1056 cycles
  (recorded RED baseline of the session-13 fix).
* UNDERFLOW (bug #44): the session-13 OPEN-LOOP pacing (one dead beat
  per 16 blocks) matched the rates exactly -- leaving the FIFO level
  wherever the stream-start race put it (0..2 beats).  The PHY's
  TxGearbox132 serializes stale bits whenever the FIFO runs empty
  mid-stream, so the wire corrupted intermittently, dependent on
  per-boot supply/drain phase luck (silicon: ~5 host-initiated
  recoveries/s at Gen2 U0 with zero inbound CRC errors).

``Gen2BlockTransmitter`` must therefore run the loop CLOSED on the
FIFO occupancy (``tx_fifo_level`` <- TxFifoWrNum): stream gaplessly
until the level reaches the pacing threshold (16), then gap at block
boundaries while it stays there.  This test streams the transmitter
against the FIFO model with the loop closed and requires: no overflow,
prefill reached, and ZERO starvation events (drain-eligible cycles at
level 0) after prefill.
"""

import unittest

from amaranth.sim import Simulator

from luna.gateware.usb.usb3.physical.gen2 import Gen2BlockTransmitter


class Gen2TxPacingTest(unittest.TestCase):

    FIFO_DEPTH = 32

    def _run_stream(self, configure, cycles=6000):
        """Streams the transmitter (closed loop) and returns the model
        verdict dict."""
        dut = Gen2BlockTransmitter(tseq_count=65536)

        results = {}

        async def tb(ctx):
            configure(ctx, dut)
            level = 0
            max_level = 0
            overflowed = False
            armed = False
            starved = 0
            for cyc in range(cycles):
                # close the loop: the DUT sees the model level with a
                # 1-cycle lag (like TxFifoWrNum's register lag)
                ctx.set(dut.tx_fifo_level, min(level, 31))
                await ctx.tick("ss")
                if ctx.get(dut.tx_valid):
                    level += 1
                if cyc % 33 != 0:
                    if level > 0:
                        level -= 1
                    elif armed:
                        starved += 1
                if level >= 8:
                    armed = True
                max_level = max(max_level, level)
                if level > self.FIFO_DEPTH:
                    overflowed = True
            results["max"] = max_level
            results["overflow"] = overflowed
            results["armed"] = armed
            results["starved"] = starved

        sim = Simulator(dut)
        sim.add_clock(1 / 156.25e6, domain="ss")
        sim.add_testbench(tb)
        sim.run()
        return results

    def _check(self, r, what):
        self.assertFalse(
            r["overflow"],
            f"{what} stream overran the 32-deep PHY TX FIFO "
            f"(max occupancy {r['max']})")
        self.assertTrue(
            r["armed"],
            f"{what} stream never prefilled the PHY TX FIFO "
            f"(max occupancy {r['max']}): the gearbox rides its "
            f"underflow boundary (bug #44)")
        self.assertEqual(
            r["starved"], 0,
            f"{what} stream starved the PHY TX gearbox "
            f"{r['starved']} times after prefill (max occupancy "
            f"{r['max']}): stale bits on the wire (bug #44)")

    def test_tseq_stream_is_paced(self):
        """Training streams (the longest sustained TX) must hold the
        near-full pacing band."""
        def configure(ctx, dut):
            ctx.set(dut.send_tseq_burst, 1)
        self._check(self._run_stream(configure), "TSEQ")

    def test_ts1_stream_is_paced(self):
        def configure(ctx, dut):
            ctx.set(dut.send_ts1_burst, 1)
        self._check(self._run_stream(configure), "TS1")

    def test_idle_stream_is_paced(self):
        """U0 idle (SDS + idle data blocks) is also a sustained stream."""
        def configure(ctx, dut):
            ctx.set(dut.idle_mode, 1)
        self._check(self._run_stream(configure), "idle")


if __name__ == "__main__":
    unittest.main()
