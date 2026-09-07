# amaranth: UnusedElaboratable=no
#
# This file is part of LUNA.
#
# Copyright (c) 2026 the luna-ss contributors
# SPDX-License-Identifier: BSD-3-Clause
""" Two-clock testbench for the 2:1 PIPE bridge (width program,
usb3_design.md 13.3/13.4).

Pins BOTH directions byte-exact across the pclk <-> pclk/2 seam:

* TX: every 128-bit core beat must emit exactly two pclk beats —
  ``tx_data[64:128]`` first-on-wire (with start/sync-header), then
  ``[0:64]``; a ``tx_halfbeat`` beat (the 24-symbol SKP OS tail,
  symbols 16-23 in the top lanes) exactly ONE pclk beat; tx_datavalid
  gaps nothing on either phase.  A phase bug here is the wire-garbage
  failure class (mismatched half pairing on every block).
* RX: start-anchored pairs presented as ``(beat0 << 64) | beat1`` +
  rx_start for exactly one core cycle each — across rx_valid gap
  cadences between pairs, and dropping a startless orphan beat.
* Gen1 fallback leg (rate=0): TX low-half split ([31:0] first), RX
  low-half pair packing (first sub-beat in [31:0]) — order-exact as a
  contiguous symbol stream (pairing offset is arbitrary by design; the
  core-side aligner owns it).
* phy_status: a single-pclk pulse must reach the core exactly once at
  either pulse phase (the latch-and-hold seam register).
* Hold seam (finding #57): every pclk->core crossing must be
  relaunched once on the pclk FALLING edge before a core register
  captures it (the divided core clock's insertion delay races
  same-edge captures on silicon; structural fence below).

NEGATIVE CONTROL (the red-first teeth, recorded RED 2026-09-06): a
deliberately broken phase relation — the core clock derived from the
INVERTED divider — must fail the TX byte-exact check (the wire pairs
the second half of each beat with the first half of the next: exactly
the wire-garbage class the phase alignment exists to prevent).
"""

import random
import unittest

from amaranth import *
from amaranth.hdl import Fragment
from amaranth.sim import Simulator

from luna.gateware.interface.pipe import PIPEInterface
from luna.gateware.interface.serdes_phy.pipe_bridge_2to1 import PIPEBridge2to1


class BridgeHarness(Elaboratable):
    """The bridge against a bare 64-bit PIPE, with the core clock
    derived from the bridge's own /2 divider (or its INVERSE for the
    broken-phase negative control)."""

    def __init__(self, *, broken_phase=False):
        self.phy = PIPEInterface(width=8)
        self.dut = PIPEBridge2to1(phy=self.phy)
        self._broken_phase = broken_phase

    def elaborate(self, platform):
        m = Module()
        m.domains += ClockDomain("ss")
        m.domains += ClockDomain("core")
        src = self.dut.phase
        m.d.comb += ClockSignal("core").eq(~src if self._broken_phase
                                           else src)
        m.submodules.dut = self.dut
        return m


# ── scripted TX stimulus ─────────────────────────────────────────────

FULL, HALF, GAP = "full", "half", "gap"


def make_tx_script(seed=1):
    """Blocks, SKP halfbeats and datavalid gaps in adversarial order."""
    rng = random.Random(seed)

    def full():
        return (FULL, rng.getrandbits(128), rng.choice((0b0101, 0b1010)))

    def half():
        # SKP OS tail: symbols 16-23 ride the TOP lanes; low half is
        # idle fill the bridge must never emit.
        return (HALF, (rng.getrandbits(64) << 64) | 0x5A5A5A5A5A5A5A5A,
                0b0101)

    script = [
        full(), full(),                    # back-to-back blocks
        full(), half(),                    # the SKP OS 2+1 seam
        (GAP, 0, 0),                       # pacing gap
        full(), half(), (GAP, 0, 0), (GAP, 0, 0),
        full(),
    ]
    for _ in range(24):                    # randomized soak
        kind = rng.choice((FULL, FULL, FULL, HALF, GAP))
        script.append({FULL: full, HALF: half,
                       GAP: lambda: (GAP, 0, 0)}[kind]())
    # A halfbeat directly at the script tail (drain path).
    script += [full(), half()]
    return script


def expected_pclk_beats(script):
    """The byte-exact 64-bit wire expectation."""
    out = []
    for kind, data, head in script:
        if kind == FULL:
            out.append((data >> 64, 1, head))     # first-on-wire, start
            out.append((data & (2**64 - 1), 0, None))
        elif kind == HALF:
            out.append((data >> 64, 0, None))     # ONE beat, top lanes
    return out


class Gen2BridgeTXTest(unittest.TestCase):

    def _run_tx(self, broken_phase=False):
        harness = BridgeHarness(broken_phase=broken_phase)
        dut, phy = harness.dut, harness.phy
        script = make_tx_script()
        collected = []
        state = {"done": False}

        async def driver(ctx):
            ctx.set(dut.rate, 1)
            await ctx.tick("core").repeat(4)
            for kind, data, head in script:
                if kind == GAP:
                    ctx.set(dut.tx_datavalid, 0)
                else:
                    ctx.set(dut.tx_data, data)
                    ctx.set(dut.tx_sync_header, head)
                    ctx.set(dut.tx_datavalid, 1)
                    ctx.set(dut.tx_start_block, 1 if kind == FULL else 0)
                    ctx.set(dut.tx_halfbeat, 1 if kind == HALF else 0)
                await ctx.tick("core")
            ctx.set(dut.tx_datavalid, 0)
            await ctx.tick("core").repeat(4)
            state["done"] = True

        async def collector(ctx):
            while not state["done"]:
                await ctx.tick("ss")
                if ctx.get(phy.tx_datavalid):
                    collected.append((
                        ctx.get(phy.tx_data),
                        ctx.get(phy.tx_start_block),
                        ctx.get(phy.tx_sync_header),
                    ))

        sim = Simulator(harness)
        sim.add_clock(1 / 156.25e6, domain="ss")
        sim.add_testbench(driver)
        sim.add_testbench(collector)
        sim.run()

        expect = expected_pclk_beats(script)
        self.assertEqual(
            len(collected), len(expect),
            f"wire beat count {len(collected)} != expected {len(expect)} "
            f"(gaps must emit nothing; a halfbeat exactly one beat)")
        for i, ((gd, gs, gh), (ed, es, eh)) in enumerate(
                zip(collected, expect)):
            self.assertEqual(
                gd, ed,
                f"wire beat {i}: data {gd:016x} != expected {ed:016x} "
                f"(half-select phase / ordering)")
            self.assertEqual(
                gs, es, f"wire beat {i}: start_block {gs} != {es}")
            if es:
                self.assertEqual(
                    gh, eh, f"wire beat {i}: sync_header {gh} != {eh}")

    def test_tx_byte_exact(self):
        """Blocks + SKP halfbeat seam + valid gaps, byte-exact on the
        64-bit wire, first-on-wire = tx_data[64:128]."""
        self._run_tx()

    def test_tx_broken_phase_is_red(self):
        """NEGATIVE CONTROL: the inverted divider phase must be caught
        by the byte-exact check (the wire-garbage class)."""
        with self.assertRaises(AssertionError):
            self._run_tx(broken_phase=True)


class Gen2BridgeRXTest(unittest.TestCase):

    def _run_rx(self, gap_pattern):
        harness = BridgeHarness()
        dut, phy = harness.dut, harness.phy
        rng = random.Random(7)
        blocks = [(rng.getrandbits(64), rng.getrandbits(64),
                   rng.choice((0b0101, 0b1010))) for _ in range(40)]
        collected = []
        state = {"done": False}

        async def driver(ctx):
            ctx.set(dut.rate, 1)
            await ctx.tick("ss").repeat(8)
            for i, (hi, lo, head) in enumerate(blocks):
                gap = gap_pattern[i % len(gap_pattern)]
                for _ in range(gap):
                    ctx.set(phy.rx_datavalid, 0)
                    await ctx.tick("ss")
                ctx.set(phy.rx_datavalid, 1)
                ctx.set(phy.rx_start_block, 1)
                ctx.set(phy.rx_sync_header, head)
                ctx.set(phy.rx_data, hi)
                await ctx.tick("ss")
                ctx.set(phy.rx_start_block, 0)
                ctx.set(phy.rx_data, lo)
                await ctx.tick("ss")
            # A startless orphan beat: the PHY never emits one (it
            # strips SKPs), but the accumulator must drop it cold.
            ctx.set(phy.rx_datavalid, 1)
            ctx.set(phy.rx_start_block, 0)
            ctx.set(phy.rx_data, 0xDEAD_BEEF_DEAD_BEEF)
            await ctx.tick("ss")
            ctx.set(phy.rx_datavalid, 0)
            await ctx.tick("ss").repeat(12)
            state["done"] = True

        async def collector(ctx):
            while not state["done"]:
                await ctx.tick("core")
                if ctx.get(dut.rx_datavalid):
                    collected.append((
                        ctx.get(dut.rx_data),
                        ctx.get(dut.rx_sync_header),
                        ctx.get(dut.rx_start_block),
                    ))

        sim = Simulator(harness)
        sim.add_clock(1 / 156.25e6, domain="ss")
        sim.add_testbench(driver)
        sim.add_testbench(collector)
        sim.run()

        expect = [((hi << 64) | lo, head, 1) for hi, lo, head in blocks]
        self.assertEqual(
            len(collected), len(expect),
            f"core beat count {len(collected)} != {len(expect)} "
            f"(each pair exactly once; the orphan dropped) "
            f"[gaps {gap_pattern}]")
        for i, (got, exp) in enumerate(zip(collected, expect)):
            self.assertEqual(
                got[0], exp[0],
                f"core beat {i}: data {got[0]:032x} != {exp[0]:032x} "
                f"[gaps {gap_pattern}]")
            self.assertEqual(got[1], exp[1],
                             f"core beat {i}: sync_header mismatch")
            self.assertEqual(got[2], 1,
                             f"core beat {i}: rx_start_block not set")

    def test_rx_dense(self):
        """Back-to-back pairs (the steady-state wire)."""
        self._run_rx([0])

    def test_rx_gap_cadences(self):
        """rx_valid gaps between pairs at mixed cadences (the gearbox
        wrap-gap pattern lands at every alignment against the
        divider)."""
        self._run_rx([1, 0, 0, 2, 0, 3, 0, 0, 0, 1])


class Gen2BridgeGen1LegTest(unittest.TestCase):
    """The 5G fallback leg through the same phase machinery."""

    def _find_run(self, haystack, needle):
        """Index of ``needle`` as a contiguous run in ``haystack``."""
        for i in range(len(haystack) - len(needle) + 1):
            if haystack[i:i + len(needle)] == needle:
                return i
        return -1

    def test_gen1_tx_low_half_split(self):
        harness = BridgeHarness()
        dut, phy = harness.dut, harness.phy
        rng = random.Random(3)
        beats = [(rng.getrandbits(64), rng.getrandbits(8))
                 for _ in range(24)]
        collected = []
        state = {"done": False}

        async def driver(ctx):
            ctx.set(dut.rate, 0)
            ctx.set(dut.tx_elec_idle, 0)
            await ctx.tick("core").repeat(4)
            for data, datak in beats:
                ctx.set(dut.tx_data, data)
                ctx.set(dut.tx_datak, datak)
                await ctx.tick("core")
            await ctx.tick("core").repeat(4)
            state["done"] = True

        async def collector(ctx):
            while not state["done"]:
                await ctx.tick("ss")
                collected.append((ctx.get(phy.tx_data) & 0xFFFFFFFF,
                                  ctx.get(phy.tx_datak) & 0xF))

        sim = Simulator(harness)
        sim.add_clock(1 / 125e6, domain="ss")
        sim.add_testbench(driver)
        sim.add_testbench(collector)
        sim.run()

        expect = []
        for data, datak in beats:
            expect.append((data & 0xFFFFFFFF, datak & 0xF))          # low first
            expect.append(((data >> 32) & 0xFFFFFFFF, (datak >> 4) & 0xF))
        idx = self._find_run(collected, expect)
        self.assertGreaterEqual(
            idx, 0,
            "Gen1 TX sub-beat stream not found order-exact on the wire "
            "(low-half-first split broken)")

    def test_gen1_rx_pair_packing(self):
        harness = BridgeHarness()
        dut, phy = harness.dut, harness.phy
        rng = random.Random(5)
        subs = [(rng.getrandbits(32), rng.getrandbits(4))
                for _ in range(48)]
        collected = []
        state = {"done": False}

        async def driver(ctx):
            ctx.set(dut.rate, 0)
            await ctx.tick("ss").repeat(9)
            for data, datak in subs:
                ctx.set(phy.rx_data, data)
                ctx.set(phy.rx_datak, datak)
                await ctx.tick("ss")
            await ctx.tick("ss").repeat(12)
            state["done"] = True

        async def collector(ctx):
            while not state["done"]:
                await ctx.tick("core")
                d = ctx.get(dut.rx_data)
                k = ctx.get(dut.rx_datak)
                collected.append((d & 0xFFFFFFFF, k & 0xF))           # first
                collected.append(((d >> 32) & 0xFFFFFFFF, (k >> 4) & 0xF))

        sim = Simulator(harness)
        sim.add_clock(1 / 125e6, domain="ss")
        sim.add_testbench(driver)
        sim.add_testbench(collector)
        sim.run()

        # Pairing offset is arbitrary (the aligner owns it); order and
        # grouping must hold: the fed sub-beat stream must appear as one
        # contiguous run, minus at most one sub-beat at each edge.
        idx = self._find_run(collected, subs[1:-1])
        self.assertGreaterEqual(
            idx, 0,
            "Gen1 RX sub-beat stream not contiguous through the pair "
            "packer (ordering/pairing broken)")


class Gen2BridgePhyStatusTest(unittest.TestCase):
    """The phy_status latch-and-hold: a 1-pclk pulse at EITHER divider
    phase reaches the core exactly once."""

    def _run_pulses(self, first_phase):
        harness = BridgeHarness()
        dut, phy = harness.dut, harness.phy
        seen = []
        state = {"done": False}

        async def driver(ctx):
            await ctx.tick("ss").repeat(8 + first_phase)
            for spacing in (8, 9, 12, 15):
                ctx.set(phy.phy_status, 1)
                await ctx.tick("ss")
                ctx.set(phy.phy_status, 0)
                await ctx.tick("ss").repeat(spacing)
            await ctx.tick("ss").repeat(8)
            state["done"] = True

        async def collector(ctx):
            while not state["done"]:
                await ctx.tick("core")
                if ctx.get(dut.phy_status):
                    seen.append(1)

        sim = Simulator(harness)
        sim.add_clock(1 / 156.25e6, domain="ss")
        sim.add_testbench(driver)
        sim.add_testbench(collector)
        sim.run()

        self.assertEqual(
            len(seen), 4,
            f"{len(seen)} core-side phy_status events for 4 pulses at "
            f"phase {first_phase} (latch-and-hold seam broken)")

    def test_pulse_even_phase(self):
        self._run_pulses(0)

    def test_pulse_odd_phase(self):
        self._run_pulses(1)


class Gen2BridgeHoldRelaunchTest(unittest.TestCase):
    """The pclk->core hold seam (finding #57).

    The core clock is a fabric-divider generated clock whose insertion
    delay TRAILS pclk (~0.64 ns on the GW5AT-60 candidates: divider
    clk->Q plus the second global-net entry).  A core register that
    directly captures a pclk POSEDGE register races that skew on
    same-edge minimum-delay paths — the #56 candidate's 53
    related-clock hold violations (bridge/pair_data -> bridge/rx_data,
    worst -0.295 ns against 0.40-0.53 ns data delays;
    /tmp/kilo/s21_tt_pnr310_timing.json).

    Required structure: every pclk->core crossing relaunches ONCE on
    the pclk FALLING edge, moving the launch edge half a pclk ahead of
    the capture edge (~2.5 ns structural hold margin; >3 ns setup
    budget remains on the final register-to-register hop).  At nominal
    phase this is transparent — the byte-exact suites above pin the
    unchanged contract.

    Simulation's atomic-update model cannot express per-bit hold
    tearing, so this fence is structural, with the extracted relaunch
    assignment simulated for edge polarity (the training-register
    precedent in test_gen2_debug_taps.py).

    RED (recorded 2026-09-07, /tmp/kilo/s22_bridge_hold_red.log):
    direct posedge captures of pair_data / done_cnt / the PHY status
    levels, and no falling-edge domain in the elaborated bridge.
    """

    # PHY-side signals that are pclk-registered inside the PHY/adapter
    # (the serdes_astat_filter family): a core register must never
    # capture them without the relaunch.
    PHY_PCLK_SOURCES = (
        "rx_elec_idle", "power_present", "rx_status", "rx_valid",
        "phy_status", "tx_fifo_occupancy", "phy_ready",
        "rx_data", "rx_datak", "rx_datavalid", "rx_start_block",
        "rx_sync_header",
    )

    def _elaborated(self):
        phy = PIPEInterface(width=8)
        # The gw_usb3 adapter extras (a bare PIPEInterface lacks them;
        # their hasattr branches must elaborate too).
        phy.tx_fifo_occupancy = Signal(5)
        phy.phy_ready         = Signal()
        phy.ltssm_training    = Signal()
        dut = PIPEBridge2to1(phy=phy)
        return phy, dut, Fragment.get(dut, None)

    @staticmethod
    def _rhs_ids(statement):
        try:
            return {id(sig): sig for sig in statement._rhs_signals()}
        except NotImplementedError:
            return {}       # a ClockSignal tie, not a data path

    def test_no_direct_pclk_capture_into_core(self):
        phy, dut, frag = self._elaborated()

        hazards = {}
        for stmt in frag.statements.get("ss", ()):
            for sig in stmt._lhs_signals():
                hazards[id(sig)] = sig
        for name in self.PHY_PCLK_SOURCES:
            sig = getattr(phy, name)
            hazards[id(sig)] = sig

        comb_deps = {}
        for stmt in frag.statements.get("comb", ()):
            rhs = self._rhs_ids(stmt)
            for sig in stmt._lhs_signals():
                comb_deps.setdefault(id(sig), {}).update(rhs)

        offenders = set()
        for stmt in frag.statements.get("core", ()):
            work = list(self._rhs_ids(stmt).items())
            seen = set()
            while work:
                key, sig = work.pop()
                if key in seen:
                    continue
                seen.add(key)
                if key in hazards:
                    offenders.add(sig.name)
                work.extend(comb_deps.get(key, {}).items())

        self.assertFalse(
            offenders,
            f"core registers capture pclk-posedge signals directly — "
            f"the related-clock hold race against the divided core "
            f"clock's insertion delay: {sorted(offenders)}")

    # Control levels the MAC drives toward the PHY: their sources are
    # decoded core-domain cones (LTSSM state); the pclk boundary
    # register must capture a CORE REGISTER, never the decode directly
    # (the -0.021 ns fsm_state -> bridge/rx_termination setup seam at
    # 3/1/0 on the relaunch RTL; the ltssm_in_training precedent).
    CORE_LEVEL_SOURCES = (
        "phy_mode", "elas_buf_mode", "power_down", "tx_deemph",
        "tx_margin", "tx_swing", "tx_detrx_lpbk", "tx_compliance",
        "tx_ones_zeros", "rx_polarity", "rx_eq_training",
        "rx_termination", "tx_elec_idle", "rate", "ltssm_training",
        "reset",
    )

    def test_core_to_pclk_levels_are_core_preregistered(self):
        phy, dut, frag = self._elaborated()

        core_regs = {}
        for stmt in frag.statements.get("core", ()):
            for sig in stmt._lhs_signals():
                core_regs[id(sig)] = sig

        offenders = set()
        for stmt in frag.statements.get("ss", ()):
            for key, sig in self._rhs_ids(stmt).items():
                for name in self.CORE_LEVEL_SOURCES:
                    src = getattr(dut, name, None)
                    if src is not None and sig is src \
                            and key not in core_regs:
                        offenders.add(name)
        self.assertFalse(
            offenders,
            f"pclk boundary registers capture MAC control levels "
            f"directly — the decoded-LTSSM core->pclk setup seam "
            f"(fsm_state -> rx_termination class): {sorted(offenders)}")

    def test_relaunch_domain_is_falling_edge(self):
        phy, dut, frag = self._elaborated()

        neg = {name: cd for name, cd in frag.domains.items()
               if cd.clk_edge == "neg"}
        self.assertTrue(
            neg, "no falling-edge relaunch domain in the bridge "
                 "(pclk->core crossings capture same-edge)")
        (negname,) = neg
        writes = list(frag.statements.get(negname, ()))
        self.assertTrue(writes, "the relaunch domain drives nothing")

        # Simulate the actual extracted pair_data relaunch assignment:
        # it must update on the FALLING edge only.
        target = None
        for stmt in writes:
            for sig in stmt._lhs_signals():
                if sig.name == "pair_data_nr":
                    target = stmt
        self.assertIsNotNone(
            target,
            f"no pair_data relaunch register in '{negname}' (lhs: "
            f"{[s.name for w in writes for s in w._lhs_signals()]})")

        m = Module()
        cd = ClockDomain("relaunch", clk_edge="neg", reset_less=True)
        m.domains += cd
        m.d["relaunch"] += target
        sim = Simulator(m)
        pattern = 0x5A5A_A5A5_5A5A_A5A5_0123_4567_89AB_CDEF

        async def bench(ctx):
            ctx.set(cd.clk, 0)
            ctx.set(target.rhs, pattern)
            await ctx.delay(1e-9)
            before = ctx.get(target.lhs)
            ctx.set(cd.clk, 1)              # rising edge: must NOT capture
            await ctx.delay(1e-9)
            self.assertEqual(
                ctx.get(target.lhs), before,
                "relaunch register captured on the RISING pclk edge")
            ctx.set(cd.clk, 0)              # falling edge: captures
            await ctx.delay(1e-9)
            self.assertEqual(ctx.get(target.lhs), pattern)

        sim.add_testbench(bench)
        sim.run()


if __name__ == "__main__":
    unittest.main()
