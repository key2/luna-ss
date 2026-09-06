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


class Gen2TxPacingBridgedLagTest(unittest.TestCase):
    """ #44 pacing across the 2:1 PIPE bridge seam (width program,
    usb3_design.md 13.3).

    At core_width=128 the block transmitter runs at pclk/2 behind the
    bridge, and its occupancy reference is STALER than the words=1
    loop's single register: TxFifoWrNum's own pclk register, the
    bridge's core-edge sample register (up to 2 pclk of phase
    staleness), and the physical layer's seam register (one core cycle
    = 2 pclk) -- while its supply beats land in the PHY FIFO one core
    cycle (the bridge TX latency) after tx_valid.  Modeled here as a
    one-core-cycle supply delay plus a level-presentation lag swept
    over 2..4 core cycles (>= the 4-6 pclk budget, with margin).  The
    drain law runs TWICE per core cycle (pclk = 2x core); words are
    64-bit PHY words: a full beat supplies 2 (the first with the
    68-bit start), a halfbeat 1.

    The loop must hold the #44 band at every swept lag: no overflow,
    prefill reached, ZERO starvation after prefill, and a maximum
    level below the 28-word hi28 bench canary.

    NEGATIVE CONTROL (the red-first teeth, recorded RED 2026-09-06): at
    a lag far past the budget (10 core cycles) the gap decision arrives
    so late that the drain undershoots to empty -- the model MUST
    report starvation/underflow (the stale-level failure is exactly
    the #44 class the band exists to prevent).
    """

    FIFO_DEPTH = 32

    def _run_stream_lagged(self, configure, lag, cycles=6000):
        """Streams the words=2 transmitter at the core clock against
        the pclk-law FIFO model, presenting the level ``lag`` core
        cycles stale and applying supply one core cycle late."""
        from collections import deque

        dut = Gen2BlockTransmitter(tseq_count=65536, words=2)
        results = {}

        async def tb(ctx):
            configure(ctx, dut)
            level = 0
            fifo_q = []
            gb_active = False
            gb_bits = 0
            empty_r = True
            max_level = 0
            overflowed = False
            armed = False
            starved = 0
            hi28 = 0
            hist = deque([0] * lag, maxlen=lag)   # level, lag cycles ago
            pending = None                        # 1-core-cycle supply delay
            for cyc in range(cycles):
                ctx.set(dut.tx_fifo_level, min(hist[0], 31))
                await ctx.tick("ss")
                # ── supply (delayed one core cycle: the bridge TX) ──
                if pending is not None:
                    half, start = pending
                    if half:
                        level += 1
                        fifo_q.append(False)
                    else:
                        level += 2
                        fifo_q.append(start)
                        fifo_q.append(False)
                pending = None
                if ctx.get(dut.tx_valid):
                    pending = (bool(ctx.get(dut.tx_halfbeat)),
                               bool(ctx.get(dut.tx_start)))
                # ── drain law, twice per core cycle (pclk = 2x) ──
                for _ in range(2):
                    ready = (not gb_active) or (gb_bits <= 64)
                    rd = ready and not empty_r and level > 0
                    empty_r = (level == 0)
                    if rd:
                        start = fifo_q.pop(0)
                        level -= 1
                        gb_bits += 68 if start else 64
                        gb_active = True
                    if gb_active:
                        gb_bits -= 64
                        if gb_bits < 0:
                            gb_bits = 0
                            gb_active = False
                            if armed:
                                starved += 1
                if level >= 8:
                    armed = True
                max_level = max(max_level, level)
                if level >= 28:
                    hi28 += 1
                if level > self.FIFO_DEPTH:
                    overflowed = True
                hist.append(level)
            results["max"] = max_level
            results["overflow"] = overflowed
            results["armed"] = armed
            results["starved"] = starved
            results["hi28"] = hi28

        sim = Simulator(dut)
        sim.add_clock(1 / 78.125e6, domain="ss")
        sim.add_testbench(tb)
        sim.run()
        return results

    def _check_band(self, r, what):
        self.assertFalse(
            r["overflow"],
            f"{what} overran the 32-deep PHY TX FIFO "
            f"(max {r['max']})")
        self.assertTrue(
            r["armed"],
            f"{what} never prefilled the PHY TX FIFO (max {r['max']}): "
            f"the gearbox rides its underflow boundary (bug #44)")
        self.assertEqual(
            r["starved"], 0,
            f"{what} starved the PHY TX gearbox {r['starved']} times "
            f"after prefill (max {r['max']}): stale bits on the wire "
            f"(bug #44)")
        self.assertLess(
            r["max"], 28,
            f"{what} rode into the hi28 canary band "
            f"(max {r['max']}): the bridged lag overshoots the pacing "
            f"threshold")

    def test_idle_stream_holds_band_at_bridged_lags(self):
        """U0 idle/data blocks (the sustained U0 stream) across the
        bridged-lag budget sweep."""
        for lag in (2, 3, 4):
            def configure(ctx, dut):
                ctx.set(dut.idle_mode, 1)
            self._check_band(
                self._run_stream_lagged(configure, lag),
                f"idle stream at {lag}-core-cycle occupancy lag")

    def test_training_stream_holds_band_at_bridged_lags(self):
        """TSEQ training (the longest sustained TX) across the sweep."""
        for lag in (2, 3, 4):
            def configure(ctx, dut):
                ctx.set(dut.send_tseq_burst, 1)
            self._check_band(
                self._run_stream_lagged(configure, lag),
                f"TSEQ stream at {lag}-core-cycle occupancy lag")

    def test_absurd_lag_is_red(self):
        """NEGATIVE CONTROL: a lag far past the budget must be caught
        by the band assertions (the model's teeth)."""
        def configure(ctx, dut):
            ctx.set(dut.idle_mode, 1)
        r = self._run_stream_lagged(configure, 10)
        self.assertTrue(
            r["starved"] > 0 or r["overflow"] or r["max"] >= 28,
            f"10-core-cycle lag unexpectedly held the band "
            f"(max {r['max']}, starved {r['starved']}): the lag model "
            f"has no teeth")


if __name__ == "__main__":
    unittest.main()
