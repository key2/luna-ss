#!/usr/bin/env python3
#
# This file is part of LUNA.
#
# Copyright (c) 2026 whitequark research heavy industries
# SPDX-License-Identifier: BSD-3-Clause
""" Smoke simulation: LUNA SuperSpeed physical+link layers driving the
Gowin GTR12 soft PHY (gw_usb3) through the width=8 PIPE adapter.

Proves, without hardware or a link partner:

  1. the PHY starts up and the synthesized TUSB-style phy_status
     handshake satisfies LUNA's PHYResetController (physical.ready);
  2. LUNA's LTSSM leaves Rx.Detect (VBUS-based partner detection),
     enters Polling and asserts send_lfps_polling;
  3. the PHY executes the LFPS bursts: its serial TX data output shows
     the LFPS pattern, and the UPAR CSR port shows the per-burst
     electrical-idle writes of the CSR sequencer (the real hardware
     mechanism, not a sim shortcut).

Run from the fork root (gw_usb3 is an installed submodule package):

    pdm run python examples/usb/superspeed/gowin_gtr12_sim.py
"""

# luna and gw_usb3 are installed packages (pdm install at the fork
# root).  No sys.path reaches.

import sys

from amaranth import *
from amaranth.sim import Simulator

from luna.gateware.interface.serdes_phy.gowin_gtr12 import GowinGTR12PIPE
from luna.gateware.usb.usb3.physical.layer import USB3PhysicalLayer
from luna.gateware.usb.usb3.link.layer import USB3LinkLayer

SS_PERIOD   = 8e-9      # 125 MHz -- Gen1 pclk
UPAR_PERIOD = 10e-9     # 100 MHz -- stand-in for the GTR12 life clock


class SmokeBench(Elaboratable):
    def __init__(self):
        self.adapter  = GowinGTR12PIPE()          # gen1 defaults
        self.physical = USB3PhysicalLayer(phy=self.adapter,
                                          sync_frequency=125e6)
        self.link     = USB3LinkLayer(physical_layer=self.physical,
                                      ss_clock_frequency=125e6)

    def elaborate(self, platform):
        m = Module()
        m.domains.ss   = ClockDomain()
        m.domains.upar = ClockDomain()

        m.submodules.adapter  = adapter  = self.adapter
        m.submodules.physical = physical = self.physical
        m.submodules.link     = link     = self.link

        phy = adapter.phy

        # SerDes-side stand-ins: clocks, static status, idle receive line.
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

            phy.serdes_tx_fifo_wrusewd_i.eq(16),   # half-full, steady
            phy.serdes_rx_fifo_rdusewd_i.eq(0),
            phy.serdes_rxfifo_aempty_i  .eq(1),
            phy.serdes_rx_vld_i         .eq(0),
            phy.serdes_rxdata_i         .eq(0),
            phy.serdes_rxelecidle_i     .eq(1),
            phy.serdes_astat_i          .eq(0),    # bit5 low = line idle
        ]

        # UPAR slave stub.  NB: ready must idle LOW -- the CSR sequencer
        # asserts wren/rden and *then* waits for ready; a constant-high
        # ready collapses the request to zero cycles (the ready branch
        # overrides the assertion in the same cycle) and no transaction
        # ever appears on the bus.  Model the arbiter: accept one cycle
        # after a request, return read data (0) one cycle later.
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
    bench = SmokeBench()
    sim = Simulator(bench)
    sim.add_clock(SS_PERIOD)                    # "sync" (reset controller)
    sim.add_clock(SS_PERIOD,   domain="ss")
    sim.add_clock(UPAR_PERIOD, domain="upar")

    phy      = bench.adapter.phy
    physical = bench.physical

    results = {}

    async def testbench(ctx):
        MAX_CYCLES = 400_000
        txdata_last = None
        txdata_toggles = 0
        upar_writes = 0
        polling_seen_at = None

        for cycle in range(MAX_CYCLES):
            await ctx.tick("ss")

            if "ready" not in results and ctx.get(physical.ready):
                results["ready"] = cycle
                print(f"[{cycle:7d}] physical.ready (PHY startup handshake OK)")

            if ctx.get(physical.send_lfps_polling):
                if "polling" not in results:
                    results["polling"] = cycle
                    polling_seen_at = cycle
                    print(f"[{cycle:7d}] LTSSM entered Polling: send_lfps_polling asserted")

            if polling_seen_at is not None:
                txd = ctx.get(phy.serdes_txdata_o)
                if txdata_last is not None and txd != txdata_last:
                    txdata_toggles += 1
                txdata_last = txd
                if ctx.get(phy.serdes_upar_wren_o):
                    upar_writes += 1

                if txdata_toggles > 50 and upar_writes >= 2 \
                        and "lfps_tx" not in results:
                    results["lfps_tx"] = cycle
                    print(f"[{cycle:7d}] PHY transmitting LFPS: "
                          f"{txdata_toggles} TX-data toggles, "
                          f"{upar_writes} UPAR (eidle/FFE) CSR writes")
                    return

            if cycle == MAX_CYCLES - 1:
                print(f"[{cycle:7d}] timeout; partial results: {results}, "
                      f"toggles={txdata_toggles} upar_writes={upar_writes}")

    sim.add_testbench(testbench)
    sim.run()

    ok = all(k in results for k in ("ready", "polling", "lfps_tx"))
    print()
    if ok:
        print("SMOKE TEST PASSED: LUNA link+physical layers drive the "
              "Gowin GTR12 soft PHY into Polling.LFPS transmission.")
        return 0
    print(f"SMOKE TEST FAILED; milestones reached: {results}")
    return 1


if __name__ == "__main__":
    sys.exit(run())
