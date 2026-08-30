#!/usr/bin/env python3
#
# This file is part of LUNA.
#
# Copyright (c) 2026 whitequark research heavy industries
# SPDX-License-Identifier: BSD-3-Clause
""" Full link-training simulation: LUNA SuperSpeed physical+link layers on
the Gowin GTR12 soft PHY, against a scripted symbol-level link partner.

The partner drives the PHY's *raw SerDes receive interface* (10-bit
symbols, 88-bit words) through the same 8b/10b encoder gateware the PHY
uses for transmit, so the entire receive path is exercised for real:
word alignment, 8b/10b decode, elastic buffer, PIPE handoff, LUNA CTC/
aligner/descrambler, TS detectors, idle handshake.

Scripted handshake (mirrors a USB3 Gen1 host):

  phase LFPS : partner answers Polling.LFPS (1 us bursts / 10 us repeat,
               driven via the SerDes signal-detect astat bit);
  phase TS1  : partner streams TS1 ordered sets;
  phase TS2  : partner streams TS2 ordered sets (once LUNA sends TS2s);
  phase IDLE : partner streams scrambled logical idle.

Milestones asserted:

  1. physical.ready               (PHY startup handshake)
  2. lfps_polling_detected        (RX LFPS through the RxElecIdle mux)
  3. LTSSM exits Polling.LFPS     (TSEQ burst starts; LFPS TX stops)
  4. LUNA transmits TS2s          (host TS1s were received and decoded)
  5. link.trained                 (Polling.Idle handshake complete -> U0)

Run from the fork root (gw_usb3 is an installed submodule package):

    pdm run python examples/usb/superspeed/gowin_gtr12_training_sim.py
"""

# luna and gw_usb3 are installed packages (pdm install at the fork
# root).  No sys.path reaches.

import sys

from amaranth import *
from amaranth.sim import Simulator

from luna.gateware.interface.serdes_phy.gowin_gtr12 import GowinGTR12PIPE
from luna.gateware.usb.usb3.physical.layer import USB3PhysicalLayer
from luna.gateware.usb.usb3.physical.scrambling import Scrambler
from luna.gateware.usb.usb3.link.layer import USB3LinkLayer
from luna.gateware.usb.usb3.link.ordered_sets import TS1_SET_DATA, TS2_SET_DATA

from gw_usb3 import Encoder8b10bMulti

SS_PERIOD   = 8e-9
UPAR_PERIOD = 10e-9

PHASE_QUIET, PHASE_LFPS, PHASE_TS1, PHASE_TS2, PHASE_IDLE = range(5)

LFPS_BURST  = 125       # 1.0 us at 125 MHz
LFPS_REPEAT = 1251      # 10.0 us


class HostPartner(Elaboratable):
    """ Scripted Gen1 link partner at the raw-symbol level ("ss" domain).

    Outputs plug into the PHY's SerDes-side receive ports.
    """

    def __init__(self):
        self.phase          = Signal(3)     # testbench-driven
        self.rxdata         = Signal(88)    # 4 x 10-bit at 20-bit strides
        self.rx_vld         = Signal()
        self.signal_present = Signal()      # -> serdes_astat_i[5]

    def elaborate(self, platform):
        m = Module()

        sending_symbols = Signal()
        m.d.comb += sending_symbols.eq(
            (self.phase == PHASE_TS1) | (self.phase == PHASE_TS2)
            | (self.phase == PHASE_IDLE))

        # ---- word source: TS ROMs / idle zeros -------------------------
        widx = Signal(2)
        word = Signal(32)
        ctrl = Signal(4)
        with m.If(sending_symbols):
            m.d.ss += widx.eq(widx + 1)
        with m.Else():
            m.d.ss += widx.eq(0)

        with m.Switch(self.phase):
            with m.Case(PHASE_TS1):
                m.d.comb += [
                    word.eq(Array([Const(w, 32) for w in TS1_SET_DATA])[widx]),
                    ctrl.eq(Array([Const(c, 4) for c in (0b1111, 0, 0, 0)])[widx]),
                ]
            with m.Case(PHASE_TS2):
                m.d.comb += [
                    word.eq(Array([Const(w, 32) for w in TS2_SET_DATA])[widx]),
                    ctrl.eq(Array([Const(c, 4) for c in (0b1111, 0, 0, 0)])[widx]),
                ]
            with m.Default():
                m.d.comb += [word.eq(0), ctrl.eq(0)]   # logical idle

        # ---- scrambler (idle phase only; LFSR syncs on the COMs we
        #      send during the TS phases, exactly like LUNA's TX) --------
        m.submodules.scrambler = scrambler = DomainRenamer("ss")(
            Scrambler(initial_value=0xffff))
        m.d.comb += [
            scrambler.enable      .eq(self.phase == PHASE_IDLE),
            scrambler.sink.valid  .eq(sending_symbols),
            scrambler.sink.data   .eq(word),
            scrambler.sink.ctrl   .eq(ctrl),
            scrambler.source.ready.eq(1),
        ]

        # ---- 8b/10b encode (the PHY's own encoder gateware) ------------
        m.submodules.encoder = encoder = DomainRenamer("ss")(
            Encoder8b10bMulti(4))
        m.d.comb += [
            encoder.din_en.eq(scrambler.source.valid & sending_symbols),
            encoder.din   .eq(scrambler.source.data),
            encoder.din_k .eq(scrambler.source.ctrl),
        ]

        # ---- pack into the 88-bit serdes word (10b at 20b strides) -----
        packed = Signal(88)
        m.d.comb += packed.eq(sum(
            (encoder.dout[10 * i:10 * i + 10] << (20 * i)) for i in range(4)
        ))
        m.d.comb += [
            self.rxdata.eq(packed),
            self.rx_vld.eq(encoder.dout_vld),
        ]

        # ---- LFPS burst rhythm ------------------------------------------
        lfps_cnt = Signal(range(LFPS_REPEAT))
        with m.If(self.phase == PHASE_LFPS):
            with m.If(lfps_cnt == LFPS_REPEAT - 1):
                m.d.ss += lfps_cnt.eq(0)
            with m.Else():
                m.d.ss += lfps_cnt.eq(lfps_cnt + 1)
        with m.Else():
            m.d.ss += lfps_cnt.eq(0)

        lfps_window = (self.phase == PHASE_LFPS) & (lfps_cnt < LFPS_BURST)
        m.d.comb += self.signal_present.eq(lfps_window | sending_symbols)

        return m


class TrainingBench(Elaboratable):
    def __init__(self, tseq_burst_length=128):
        self.adapter  = GowinGTR12PIPE()
        self.physical = USB3PhysicalLayer(phy=self.adapter,
                                          sync_frequency=125e6)
        self.link     = USB3LinkLayer(physical_layer=self.physical,
                                      ss_clock_frequency=125e6,
                                      tseq_burst_length=tseq_burst_length)
        self.host     = HostPartner()

    def elaborate(self, platform):
        m = Module()
        m.domains.ss   = ClockDomain()
        m.domains.upar = ClockDomain()

        m.submodules.adapter  = adapter  = self.adapter
        m.submodules.physical = physical = self.physical
        m.submodules.link     = link     = self.link
        m.submodules.host     = host     = self.host

        phy = adapter.phy

        m.d.comb += [
            phy.serdes_pcs_tx_clk_i     .eq(ClockSignal("ss")),
            phy.serdes_pcs_rx_clk_i     .eq(ClockSignal("ss")),
            phy.serdes_upar_clk_i       .eq(ClockSignal("upar")),
            phy.ref_clk                 .eq(0),

            phy.serdes_cpll_ok_i        .eq(1),
            phy.serdes_q0_qpll0_ok_i    .eq(0),
            phy.serdes_q0_qpll1_ok_i    .eq(0),
            phy.serdes_q1_qpll0_ok_i    .eq(0),
            phy.serdes_q1_qpll1_ok_i    .eq(0),
            phy.serdes_pma_rx_lock_i    .eq(1),

            phy.serdes_tx_fifo_wrusewd_i.eq(16),
            phy.serdes_rx_fifo_rdusewd_i.eq(0),
            phy.serdes_rxfifo_aempty_i  .eq(~host.rx_vld),

            # Host partner -> raw SerDes receive interface.
            phy.serdes_rx_vld_i         .eq(host.rx_vld),
            phy.serdes_rxdata_i         .eq(host.rxdata),
            phy.serdes_rxelecidle_i     .eq(~host.signal_present),
            phy.serdes_astat_i          .eq(Cat(Const(0, 5),
                                                host.signal_present)),
        ]

        # UPAR slave stub (ready must idle low; see gowin_gtr12_sim).
        ready = Signal()
        rdvld = Signal()
        m.d.upar += [
            ready.eq((phy.serdes_upar_wren_o | phy.serdes_upar_rden_o)
                     & ~ready),
            rdvld.eq(phy.serdes_upar_rden_o & ready),
        ]
        m.d.comb += [
            phy.serdes_upar_ready_i .eq(ready),
            phy.serdes_upar_rdvld_i .eq(rdvld),
            phy.serdes_upar_rddata_i.eq(0),
            phy.serdes_upar_resp_i  .eq(0),
        ]

        return m


def run():
    bench = TrainingBench()
    sim = Simulator(bench)
    sim.add_clock(SS_PERIOD)
    sim.add_clock(SS_PERIOD,   domain="ss")
    sim.add_clock(UPAR_PERIOD, domain="upar")

    adapter, physical, link, host = (bench.adapter, bench.physical,
                                     bench.link, bench.host)

    results = {}

    async def testbench(ctx):
        MAX = 700_000
        lfps_det = 0
        polling_high_seen = False
        ts2_body = 0

        phase = PHASE_QUIET
        phase_at = 0

        for cycle in range(MAX):
            await ctx.tick("ss")

            if "ready" not in results and ctx.get(physical.ready):
                results["ready"] = cycle
                print(f"[{cycle:7d}] physical.ready")
                phase = PHASE_LFPS
                ctx.set(host.phase, phase)
                phase_at = cycle

            if ctx.get(physical.lfps_polling_detected):
                lfps_det += 1
                if lfps_det == 2 and "lfps_rx" not in results:
                    results["lfps_rx"] = cycle
                    print(f"[{cycle:7d}] host LFPS detected by LUNA "
                          f"(2 valid cycles)")

            polling = ctx.get(physical.send_lfps_polling)
            if polling:
                polling_high_seen = True
            if phase == PHASE_LFPS and polling_high_seen and not polling \
                    and "lfps_done" not in results and "lfps_rx" in results:
                results["lfps_done"] = cycle
                print(f"[{cycle:7d}] LTSSM exited Polling.LFPS "
                      f"(handshake complete; TSEQ next)")
                phase = PHASE_TS1
                ctx.set(host.phase, phase)
                phase_at = cycle

            # Watch LUNA's transmit for TS2 body words.
            if phase == PHASE_TS1:
                if ctx.get(adapter.tx_data) & 0xFFFFFFFF == 0x45454545 \
                        and ctx.get(adapter.tx_datak) & 0xF == 0:
                    ts2_body += 1
                    if ts2_body >= 4 and "luna_ts2" not in results:
                        results["luna_ts2"] = cycle
                        print(f"[{cycle:7d}] LUNA transmitting TS2s "
                              f"(our TS1s were received)")
                        phase = PHASE_TS2
                        ctx.set(host.phase, phase)
                        phase_at = cycle

            if phase == PHASE_TS2 and cycle - phase_at > 2000:
                phase = PHASE_IDLE
                ctx.set(host.phase, phase)
                phase_at = cycle
                print(f"[{cycle:7d}] host -> logical idle")

            if ctx.get(link.trained) and "trained" not in results:
                results["trained"] = cycle
                print(f"[{cycle:7d}] link.trained -- U0 REACHED")
                return

        print(f"timeout; milestones: {results}")

    sim.add_testbench(testbench)
    sim.run()

    need = ("ready", "lfps_rx", "lfps_done", "luna_ts2", "trained")
    ok = all(k in results for k in need)
    print()
    if ok:
        print("TRAINING SIM PASSED: full Polling handshake to U0 through "
              "the Gowin GTR12 soft PHY at the raw-symbol level.")
        return 0
    print(f"TRAINING SIM FAILED; milestones: {results}")
    return 1


if __name__ == "__main__":
    sys.exit(run())
