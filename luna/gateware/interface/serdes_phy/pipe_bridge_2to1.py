#
# This file is part of LUNA.
#
# Copyright (c) 2026 the luna-ss contributors
# SPDX-License-Identifier: BSD-3-Clause
""" 2:1 PIPE width/rate bridge (the width program's Gen2-128 seam).

Presents the 128-bit one-beat-per-block PIPE contract
(usb3_design.md 13.3) to a MAC running at pclk/2, against a 64-bit
PHY-side PIPE pinned at pclk (GowinGTR12PIPE, unchanged).  This is the
ONLY new pclk-domain logic in a Gen2-128 build: a phase bit plus one
beat register per direction; no FSMs, no content parsing beyond the
``tx_halfbeat`` qualifier.

INTERIM per the session-19 directive: it ships the first Gen2-128
image against the silicon-proven 64-bit PHY datapath; the full-128
PHY-side widening (usb3_design.md 13.8) retires it afterwards.

Clocking contract
-----------------
The core domain is pclk/2 by a fabric FF divider, edge-locked to pclk
and constrained as a generated clock (``create_generated_clock
-divide_by 2``; the gowin-serdes SDC branch).  ``phase`` must be the
very FF that generates the core clock: ``ClockSignal(core_domain) ==
phase``.  If ``phase`` is not given, the bridge instantiates its own
divider in the pclk domain and the instantiator must derive the core
clock from ``self.phase`` (the two-clock testbench does this; the
hardware top passes its reset-free divider in).

Phase convention: ``phase == 1`` during the FIRST pclk cycle of every
core period (the divider rises exactly on the core clock's rising
edge).

Seam inventory (usb3_design.md 13.4) — all synchronous 2:1 paths, not
metastability CDCs (the only true async crossing stays inside the PHY,
rxclk->pclk):

* TX data (core->pclk): one core-side beat register captured at the
  core edge, then a phase-muxed half-select.  A full beat emits TWO
  pclk beats — ``tx_data[64:128]`` first-on-wire (symbols 0-7; the
  wide contract packs symbol 0 in the top byte), then ``[0:64]``.  A
  ``tx_halfbeat`` beat (the 24-symbol SKP OS tail, symbols 16-23 in
  the top lanes) emits exactly ONE pclk beat, from the top lanes.
  ``tx_datavalid`` gaps emit nothing on either phase; the bridge never
  inserts or deletes gaps.
* RX data (pclk->core): a start-anchored pair accumulator.  The pair
  ``(beat0 << 64) | beat1`` with ``rx_start_block`` is presented to
  the core for exactly one core cycle (a 2-pclk qualifier window
  guarantees exactly one core edge samples it).  Tolerant of rx_valid
  gaps between pairs; a startless orphan beat (never emitted by the
  PHY, which strips SKPs) is dropped by construction.
* Gen1 fallback leg (5G, pclk 125 / core 62.5, same phase machinery):
  TX splits the low 64 (8 symbols) low-half-first into 4-symbol pclk
  beats on ``tx_data[31:0]``; RX packs two consecutive 4-symbol
  sub-beats into the low 64 of a core beat (first received in
  ``[31:0]``).  Alignment is arbitrary — the core-side CTC/word
  aligner owns symbol alignment, exactly as at words=1.
* ``phy_status`` (1-pclk pulse): latched-and-held for 2 pclk so the
  core edge cannot fall between pulse and decay; a held level passes
  as a level.
* ``tx_fifo_occupancy`` (TxFifoWrNum): registered once at the core
  edge.  The added sampling lag folds into the #44 pacing-lag budget
  (re-proven red-first in tests/test_gen2_pacing.py).
* All remaining PIPE control/status signals are levels with
  microsecond tolerances: registered once at the boundary.
"""

from amaranth import *

from ..pipe import PIPEInterface


class PIPEBridge2to1(PIPEInterface, Elaboratable):
    """ 128-bit @ pclk/2 MAC-facing PIPE over a 64-bit @ pclk PHY.

    Parameters
    ----------
    phy: PIPEInterface (width=8)
        The pclk-side PHY PIPE (e.g. GowinGTR12PIPE).  NOT added as a
        submodule here — the instantiating top owns it.
    phase: Signal, optional
        The pclk-domain /2 divider FF that also generates the core
        clock.  Created internally (in ``pclk_domain``) if omitted.
    pclk_domain: str
        Clock domain name of the PHY side (default "ss").
    core_domain: str
        Clock domain name of the MAC side (default "core").
    """

    def __init__(self, *, phy, phase=None, pclk_domain="ss",
                 core_domain="core"):
        if phy.width != 8:
            raise ValueError(f"PIPEBridge2to1 requires a 64-bit (width=8) "
                             f"PHY-side PIPE, not width={phy.width}")
        super().__init__(width=16)
        self.phy          = phy
        self._pclk_domain = pclk_domain
        self._core_domain = core_domain
        self._own_phase   = phase is None
        self.phase        = Signal() if phase is None else phase

        # Adapter extras carried across the seam (consumed by the MAC's
        # physical layer / top): the #44 pacing reference and the Gen2
        # descrambler-acquisition training indicator.
        self.tx_fifo_occupancy = Signal(5)
        self.ltssm_training    = Signal()
        self.phy_ready         = Signal()

    def elaborate(self, platform):
        m = Module()
        phy  = self.phy
        pclk = m.d[self._pclk_domain]
        core = m.d[self._core_domain]

        if self._own_phase:
            pclk += self.phase.eq(~self.phase)
        ph = self.phase

        #
        # Clocking & reset.
        #
        m.d.comb += self.pclk.eq(phy.pclk)
        reset_r = Signal()
        pclk += reset_r.eq(self.reset)
        m.d.comb += phy.reset.eq(reset_r)

        #
        # Control levels, core -> pclk: one boundary register each
        # (microsecond-scale tolerances; usb3_design.md 13.4).
        #
        for name in ("phy_mode", "elas_buf_mode", "power_down", "tx_deemph",
                     "tx_margin", "tx_swing", "tx_detrx_lpbk",
                     "tx_compliance", "tx_ones_zeros", "rx_polarity",
                     "rx_eq_training", "rx_termination"):
            src = getattr(self, name)
            reg = Signal.like(src, name=f"{name}_pr")
            pclk += reg.eq(src)
            m.d.comb += getattr(phy, name).eq(reg)

        # tx_elec_idle resets to 1 (electrical idle) so the PHY never
        # sees a spurious transmit-enable cycle out of reset.
        eidle_pr = Signal(init=1)
        pclk += eidle_pr.eq(self.tx_elec_idle)
        m.d.comb += phy.tx_elec_idle.eq(eidle_pr)

        # The operating rate: the pclk-side registered copy also selects
        # the bridge's own packing leg (it only changes during LTSSM
        # rate changes, which are followed by milliseconds of retrain).
        # Resets to 1: the PHY boots in its 10G trim.
        rate_pr = Signal(init=1)
        pclk += rate_pr.eq(self.rate)
        m.d.comb += phy.rate.eq(rate_pr)

        if hasattr(phy, "ltssm_training"):
            training_pr = Signal()
            pclk += training_pr.eq(self.ltssm_training)
            m.d.comb += phy.ltssm_training.eq(training_pr)

        #
        # Status levels, pclk -> core: one boundary register each.
        #
        core += [
            self.rx_elec_idle .eq(phy.rx_elec_idle),
            self.power_present.eq(phy.power_present),
            self.rx_status    .eq(phy.rx_status),
            self.rx_valid     .eq(phy.rx_valid),
        ]
        if hasattr(phy, "phy_ready"):
            core += self.phy_ready.eq(phy.phy_ready)
        else:
            m.d.comb += self.phy_ready.eq(1)

        # The #44 closed-loop pacing reference: registered once at the
        # core edge (up to 2 pclk of staleness; budgeted).
        if hasattr(phy, "tx_fifo_occupancy"):
            core += self.tx_fifo_occupancy.eq(phy.tx_fifo_occupancy)

        # phy_status: PIPE completion acks are single-pclk pulses; a
        # pulse can fall entirely between two core edges.  Stretch to a
        # 2-pclk window (exactly one core edge samples it, whatever the
        # phase); a held level (the TUSB startup convention) passes
        # through as a level.
        ps_cnt = Signal(2)
        with m.If(phy.phy_status):
            pclk += ps_cnt.eq(2)
        with m.Elif(ps_cnt != 0):
            pclk += ps_cnt.eq(ps_cnt - 1)
        core += self.phy_status.eq(ps_cnt != 0)

        #
        # TX: core beat -> pclk half-beats.
        #
        # One core-side register captures the MAC's beat at the core
        # edge (keeping every MAC cone on the 12.8 ns budget); the pclk
        # side is a pure half-select mux from that register.  The
        # register is stable for the full core period, so the two pclk
        # captures (mid edge = first half, next core edge = second
        # half) both see it settled.
        #
        tx_data_r  = Signal(128)
        tx_datak_r = Signal(16)
        tx_head_r  = Signal(4)
        tx_start_r = Signal()
        tx_dv_r    = Signal()
        tx_half_r  = Signal()
        core += [
            tx_data_r .eq(self.tx_data),
            tx_datak_r.eq(self.tx_datak),
            tx_head_r .eq(self.tx_sync_header),
            tx_start_r.eq(self.tx_start_block),
            tx_dv_r   .eq(self.tx_datavalid),
            tx_half_r .eq(self.tx_halfbeat),
        ]

        with m.If(rate_pr):
            # Gen2 128b/132b block leg.  phase==1 (first pclk cycle of
            # the core period, register freshly captured): the
            # first-on-wire half [64:128] with start/head; phase==0:
            # the second half [0:64] — suppressed for a halfbeat.
            m.d.comb += [
                phy.tx_data       .eq(Mux(ph, tx_data_r[64:128],
                                              tx_data_r[0:64])),
                phy.tx_datavalid  .eq(Mux(ph, tx_dv_r,
                                              tx_dv_r & ~tx_half_r)),
                phy.tx_start_block.eq(ph & tx_dv_r & tx_start_r),
                phy.tx_sync_header.eq(tx_head_r),
            ]
        with m.Else():
            # Gen1 fallback leg: 8 symbols riding [63:0], split into
            # two 4-symbol pclk beats, LOW half first (symbol order is
            # little-endian on the Gen1 dialect).  tx_datavalid is left
            # to the adapter's Gen1 rule (valid when not in electrical
            # idle).
            m.d.comb += [
                phy.tx_data[0:32] .eq(Mux(ph, tx_data_r[0:32],
                                              tx_data_r[32:64])),
                phy.tx_datak[0:4] .eq(Mux(ph, tx_datak_r[0:4],
                                              tx_datak_r[4:8])),
            ]

        #
        # RX Gen2: start-anchored pair accumulator (pclk domain).
        #
        # The assembled pair is written ATOMICALLY into pair_data on the
        # second beat's edge (a split write could let a core edge
        # capture halves of two different pairs), and qualified by a
        # 2-pclk countdown window so exactly one core edge samples each
        # pair regardless of divider phase.
        #
        acc_hi    = Signal(64)
        acc_head  = Signal(4)
        have_hi   = Signal()
        pair_data = Signal(128)
        pair_head = Signal(4)
        done_cnt  = Signal(2)

        pair_done = Signal()
        m.d.comb += pair_done.eq(phy.rx_datavalid & ~phy.rx_start_block
                                 & have_hi & rate_pr)
        with m.If(phy.rx_datavalid & rate_pr):
            with m.If(phy.rx_start_block):
                # Start beats (re-)anchor unconditionally.
                pclk += [
                    acc_hi  .eq(phy.rx_data),
                    acc_head.eq(phy.rx_sync_header),
                    have_hi .eq(1),
                ]
            with m.Elif(have_hi):
                pclk += [
                    pair_data.eq(Cat(phy.rx_data, acc_hi)),
                    pair_head.eq(acc_head),
                    have_hi  .eq(0),
                ]
        with m.If(pair_done):
            pclk += done_cnt.eq(2)
        with m.Elif(done_cnt != 0):
            pclk += done_cnt.eq(done_cnt - 1)

        #
        # RX Gen1 leg: free-running low-half pair packer (pclk domain).
        #
        # Pairs are assembled on the divider phase (first sub-beat into
        # [31:0]); the pairing offset is arbitrary and absorbed by the
        # core-side CTC remover / word aligner, exactly as at words=1.
        # The assembly edge is the core edge itself, so the core-side
        # presentation register always captures the pair assembled one
        # core period earlier — consistent, constant latency.
        #
        g1_first  = Signal(32)
        g1_firstk = Signal(4)
        g1_pair   = Signal(64)
        g1_pairk  = Signal(8)
        with m.If(ph):
            pclk += [
                g1_first .eq(phy.rx_data[0:32]),
                g1_firstk.eq(phy.rx_datak[0:4]),
            ]
        with m.Else():
            pclk += [
                g1_pair .eq(Cat(g1_first,  phy.rx_data[0:32])),
                g1_pairk.eq(Cat(g1_firstk, phy.rx_datak[0:4])),
            ]

        #
        # RX: core-side presentation register (one core register).
        #
        with m.If(self.rate):
            core += [
                self.rx_data       .eq(pair_data),
                self.rx_sync_header.eq(pair_head),
                self.rx_datavalid  .eq(done_cnt != 0),
                self.rx_start_block.eq(done_cnt != 0),
                self.rx_datak      .eq(0),
            ]
        with m.Else():
            core += [
                self.rx_data       .eq(g1_pair),   # zero-extended high half
                self.rx_datak      .eq(g1_pairk),
                self.rx_datavalid  .eq(0),
                self.rx_start_block.eq(0),
            ]

        return m
