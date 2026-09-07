"""LUNA dual-rate (Gen1+Gen2) SuperSpeed device — Gowin DK_USB (GW5AT-60).

THE GEN2-128 VEHICLE (width program, session 20): the gen2=True LUNA
MAC at **core_width=128** running at pclk/2 = 78.125 MHz behind the
2:1 PIPE bridge, on the gw_usb3 PHY's silicon-proven 64-bit Gen2
datapath pinned at pclk = 156.25 MHz.  The 64-bit Gen2 trim is
RETIRED for timing (10-12 LUT levels against 6.4 ns, -60.8 ns TNS,
10/10 seed rolls failed; HANDOVER 10aa); only the register-thin
bridge and the PHY fabric attach remain in the pclk domain.

    [gowin-serdes]   GTR12 Quad 0 lane 1, CPLL, 200 MHz refclk forward,
                     **10G boot trim** (the byte-pinned reference blob).
    [gw_usb3]        Usb31Phy(gen2=True, rate_init=1) behind
                     GowinGTR12PIPE(gen2=True): the MAC owns pipe.rate,
                     the adapter forwards it to the CSR sequencer and
                     synthesizes the PIPE rate-change ack.
    [bridge]         PIPEBridge2to1 (usb3_design.md 13.3/13.4): the
                     128-bit one-beat-per-block contract at the pclk/2
                     core clock (fabric FF divider ``core_div``,
                     constrained as a generated clock).  5G fallback
                     rides the SAME divider (125 -> 62.5; the
                     core:wire timer stretch stays 1.25).
    [LUNA]           USBSuperSpeedDevice(gen2=True, core_width=128) at
                     core = 78.125 MHz (timing gates: core >= 78.125
                     AND pclk >= 156.25 AND rxclk >= 161.29).  Three
                     bulk loopback pairs for the Gen2 ladder (bulk is
                     adapter-capped at 4 B/core-cycle by the 32-bit
                     protocol boundary -- sha-exactness is the ladder
                     verdict, MB/s is documented-degraded until the
                     endpoint widening).

STATUS: session 20 met timing and trained at 10G; #49 wedges TX after
the first >18-byte DP (HANDOVER 10ab). Session 21 adds the passive
PIPE ring and full-width MAC TX checker to distinguish H1 from H2.

Build & program:

    python top.py                # build only (build/)
    python top.py serdes         # regenerate serdes.toml/csr only
    python top.py flash          # flash the existing bitstream
    python top.py program        # build + flash

Watch:  examples/gowin/luna-multiep/uart_capture.py <s> <prefix>
"""

import json
import math
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

# luna (this fork), gw_usb3 and gowin_serdes are installed packages
# (fork venv: `pdm install` at the repo root).  No sys.path reaches.

from amaranth.hdl import *
from amaranth.lib.cdc import FFSynchronizer
from amaranth.lib.fifo import SyncFIFOBuffered

from gowin_serdes.dkusb_gw5at60 import DKUSBGW5AT60Platform, add_serdes_refclk_forward

from gowin_serdes import GowinDevice, make_usb3_serdes, usb3_boot_writes
from gowin_serdes.config import RefClkSource
from gowin_serdes.usb3 import attach_usb3_phy

from luna.gateware.interface.serdes_phy.gowin_gtr12 import GowinGTR12PIPE
from luna.gateware.interface.serdes_phy.pipe_bridge_2to1 import PIPEBridge2to1
from luna.gateware.usb.usb3.device import USBSuperSpeedDevice
from luna.gateware.usb.usb3.descriptors import add_superspeedplus_bos
from luna.gateware.usb.usb3.endpoints.stream import SuperSpeedStreamInEndpoint
from luna.gateware.usb.usb3.endpoints.ss_stream_out import SuperSpeedStreamOutEndpoint

from usb_protocol.emitters import SuperSpeedDeviceDescriptorCollection
from usb_protocol.types import USBTransferType

from gowin_serdes.bench import AsyncSerialRX, ClockFreqProbe
from pipe_capture import PipeBeatCapture, capture_events
from tx_checker import Gen2TxWireChecker

# ── Configuration ─────────────────────────────────────────────────────
QUAD, LANE = 0, 1
REF_CLK_SOURCE = RefClkSource.Q0_REFCLK1
REF_CLK_FREQ = "200M"
DBG_FREQ = 24_000_000
BAUD_RATE = 115_200

BULK_EPS = (1, 2, 3)        # the ladder pairs (multiep_test.py --eps 1,2,3)
FIFO_WORDS = 4096           # per-pair elastic buffer: 16 KiB

# SerDes boot trim.  "10G" = the byte-pinned reference blob; the LTSSM
# owns any downgrade (dual-rate: the MAC drives pipe.rate).
BOOT_RATE = "10G"


def make_serdes():
    return make_usb3_serdes(GowinDevice.GW5AT_60, QUAD, LANE,
                            REF_CLK_SOURCE, REF_CLK_FREQ,
                            boot_rate=BOOT_RATE)


def create_descriptors():
    """Vendor-specific device: one interface, three bulk OUT/IN pairs
    (non-burst: the first Gen2-128 image keeps the sim-fenced endpoint
    shape; the Gen2 bulk rate is adapter-capped regardless)."""
    descriptors = SuperSpeedDeviceDescriptorCollection()

    with descriptors.DeviceDescriptor() as d:
        d.bDeviceClass       = 0xFF        # vendor specific
        d.idVendor           = 0x1209      # pid.codes
        d.idProduct          = 0x0001      # test PID
        d.bcdUSB             = 3.1
        d.bMaxPacketSize0    = 9           # 2**9 = 512
        d.iManufacturer      = "LUNA + gw_usb3"
        d.iProduct           = "GTR12 SuperSpeed+ multi-EP (Gen2-128)"
        d.iSerialNumber      = "DK60"
        d.bNumConfigurations = 1

    with descriptors.ConfigurationDescriptor() as c:
        c.bMaxPower = 50

        with c.InterfaceDescriptor() as i:
            i.bInterfaceNumber   = 0
            i.bInterfaceClass    = 0xFF    # vendor specific
            i.bInterfaceSubclass = 0x00
            i.bInterfaceProtocol = 0x00

            for ep in BULK_EPS:
                with i.EndpointDescriptor() as e:
                    e.bEndpointAddress = 0x80 | ep
                    e.bmAttributes     = 0x02  # bulk
                    e.wMaxPacketSize   = 1024
                    with e.SuperSpeedCompanion():
                        pass               # bMaxBurst = 0 (no burst)

                with i.EndpointDescriptor() as e:
                    e.bEndpointAddress = ep
                    e.bmAttributes     = 0x02  # bulk
                    e.wMaxPacketSize   = 1024
                    with e.SuperSpeedCompanion():
                        pass

    # bcdUSB 0310 requires the SuperSpeedPlus device capability in the
    # BOS [9.6.2.5] -- without it the bench host complains at every
    # 10G enumeration (session-17 #49-adjacent enum-surface gap; the
    # sim's PHASE=enum ladder validates the same bytes).
    add_superspeedplus_bos(descriptors)

    return descriptors


class LunaEnumTop(Elaboratable):
    def elaborate(self, platform):
        m = Module()

        led = platform.request("led", 0)
        usb_pwr_en = platform.request("usb_pwr_en", 0)
        m.d.comb += usb_pwr_en.o.eq(0)     # device mode: never source VBUS

        # Quiet the USB2 pins (see usb31-enum: floating pins make the
        # host see a phantom low-speed device and power-cycle the port).
        usb2 = platform.request("usb2_softphy", 0)
        m.d.comb += [
            usb2.pullup_en.o.eq(0),
            usb2.term_dp.o.eq(0),
            usb2.term_dn.o.eq(0),
            usb2.tx_dp.o.eq(0),
            usb2.tx_dn.o.eq(0),
            usb2.dp.oe.eq(0),
            usb2.dp_b.oe.eq(0),
            usb2.dn.oe.eq(0),
            usb2.dn_b.oe.eq(0),
        ]

        # ==============================================================
        # Clocks & power-on reset (vendor-proven ordering)
        # ==============================================================
        sys_clk = add_serdes_refclk_forward(m, platform)
        m.domains += ClockDomain("cfg", reset_less=True)
        m.d.comb += ClockSignal("cfg").eq(sys_clk)

        clk24 = platform.request("clk_24m", 0)
        m.domains += ClockDomain("dbg", reset_less=True)
        m.d.comb += ClockSignal("dbg").eq(clk24.i)

        # POR: quad POR at ~330 us, LUNA+PHY released LAST at ~1.3 ms.
        # Releasing logic before the quad leaves POR loses the CSR
        # sequencer's init writes (hard-won usb31-enum lesson).
        por_cnt = Signal(18)
        por_n = Signal()
        luna_go = Signal()
        with m.If(~por_cnt.all()):
            m.d.cfg += por_cnt.eq(por_cnt + 1)

        # Board key = full POR replay (LTSSM restart without reflash).
        key = platform.request("key", 0)
        key_s = Signal(2)
        m.d.cfg += key_s.eq(Cat(key.i, key_s[0]))
        with m.If(key_s[1]):
            m.d.cfg += por_cnt.eq(0)

        # POR-nudge placement lottery (semantically null threshold
        # changes; HANDOVER #22/10k).  The 64-bit Gen2 roll history
        # lives in the git history of this comment (sessions 13-17);
        # the 64-bit Gen2 trim is retired (10/10 rolls missed pclk,
        # -60.8 ns TNS; HANDOVER 10aa) -- THIS build is the 128-bit
        # core at pclk/2, where the MAC's cones get 12.8 ns and only
        # the register-thin bridge lives at 6.4.  Seed kept at the
        # 66_135 pin (the last hardware-laddered threshold family).
        m.d.cfg += [
            por_n.eq(por_cnt > 66_135),
            luna_go.eq(por_cnt.all()),
        ]

        # ==============================================================
        # SerDes + PHY + PIPE adapter (pclk domain, unchanged)
        # ==============================================================
        serdes, group = make_serdes()
        m.submodules.serdes = serdes
        lane = group.lanes[0]
        drp = getattr(serdes, group.drp_name)
        m.d.comb += serdes.por_n.eq(por_n)

        # Bug #38 (see luna-multiep/top.py): plumb the lane into the PHY's
        # CSR sequencer; the adapter default is Q0_LN1 regardless of QUAD/
        # LANE.  Elaboration-identical for the shipping Q0_LN1 config.
        from gw_usb3.upar_csr import UparCsrConfig
        adapter = GowinGTR12PIPE(gen2=True,
                                 phy_kwargs=dict(
                                     csr_config=UparCsrConfig(quad=QUAD,
                                                              lane=LANE)))
        m.submodules.adapter = adapter
        attach_usb3_phy(m, adapter.phy, lane, drp)

        # ss = pclk (156.25 MHz at the 10G trim, 125 at the 5G
        # fallback): the adapter and the bridge's PHY-facing half.
        m.domains += ClockDomain("ss_raw", reset_less=True)
        m.d.comb += ClockSignal("ss_raw").eq(lane.tx.pcs_clkout)
        rstn_r0 = Signal()
        rstn_r1 = Signal()
        m.d.ss_raw += [rstn_r0.eq(luna_go),
                       rstn_r1.eq(rstn_r0)]
        m.domains += ClockDomain("ss")
        m.d.comb += [
            ClockSignal("ss").eq(ClockSignal("ss_raw")),
            ResetSignal("ss").eq(~rstn_r1),
        ]

        # ==============================================================
        # The core clock: pclk/2 by a fabric FF divider (edge-locked;
        # constrained as a generated clock -- the gowin-serdes SDC
        # branch names this very register, ``core_div``).  It divides
        # BOTH trims: 156.25 -> 78.125 at 10G, 125 -> 62.5 at the 5G
        # fallback (the core:wire timer stretch stays 1.25, the
        # silicon-proven ratio).  The divider lives in the reset-free
        # ss_raw domain so the core clock never stops.
        # ==============================================================
        core_div = Signal(name="core_div")
        m.d.ss_raw += core_div.eq(~core_div)

        m.domains += ClockDomain("core_raw", reset_less=True)
        m.d.comb += ClockSignal("core_raw").eq(core_div)
        crstn_r0 = Signal()
        crstn_r1 = Signal()
        m.d.core_raw += [crstn_r0.eq(luna_go),
                         crstn_r1.eq(crstn_r0)]
        # The MAC domains: "core" (the renamed device "ss") and "sync"
        # (the device-internal default domain) both run at pclk/2.
        for dom in ("core", "sync"):
            m.domains += ClockDomain(dom)
            m.d.comb += [
                ClockSignal(dom).eq(core_div),
                ResetSignal(dom).eq(~crstn_r1),
            ]

        # ==============================================================
        # The 2:1 PIPE bridge (usb3_design.md 13.3/13.4)
        # ==============================================================
        bridge = PIPEBridge2to1(phy=adapter, phase=core_div,
                                pclk_domain="ss", core_domain="core")
        m.submodules.bridge = bridge

        # ==============================================================
        # LUNA SuperSpeed device: core_width=128 at pclk/2, plus the
        # three bulk loopback pairs for the Gen2 ladder
        # ==============================================================
        usb = USBSuperSpeedDevice(
            phy=bridge, sync_frequency=78.125e6, gen2=True,
            core_width=128)
        usb.add_standard_control_endpoint(create_descriptors())

        for ep in BULK_EPS:
            out_ep = SuperSpeedStreamOutEndpoint(
                endpoint_number=ep, max_packet_size=1024, max_burst=1)
            usb.add_endpoint(out_ep, endpoint_types={ep: USBTransferType.BULK})

            in_ep = SuperSpeedStreamInEndpoint(
                endpoint_number=ep, max_packet_size=1024,
                generate_zlps=False, max_burst=1)
            usb.add_endpoint(in_ep, endpoint_types={0x80 | ep: USBTransferType.BULK})

            # Per-pair elastic loopback buffer (bug #35: the bench xHC
            # pipelines its whole scheduling window at transfer start;
            # see luna-multiep/top.py).  Endpoint streams live in the
            # renamed core domain.
            fifo = SyncFIFOBuffered(width=32 + 4 + 1, depth=FIFO_WORDS)
            m.submodules[f"loop_fifo{ep}"] = \
                DomainRenamer({"sync": "core"})(fifo)

            out_ep.packet_space = Signal(name=f"packet_space{ep}")
            m.d.comb += [
                # OUT endpoint -> FIFO
                fifo.w_data.eq(Cat(out_ep.stream.payload,
                                   out_ep.stream.valid,
                                   out_ep.stream.last)),
                fifo.w_en.eq(out_ep.stream.valid.any() & fifo.w_rdy),
                out_ep.stream.ready.eq(fifo.w_rdy),

                # FIFO -> IN endpoint
                in_ep.stream.payload.eq(fifo.r_data[0:32]),
                in_ep.stream.valid.eq(Mux(fifo.r_rdy, fifo.r_data[32:36], 0)),
                in_ep.stream.last.eq(fifo.r_data[36]),
                fifo.r_en.eq(fifo.r_rdy & in_ep.stream.ready),
            ]
            # Accept a data packet only when a whole max-size packet
            # fits (registered; the margin absorbs the staleness).
            m.d.core += out_ep.packet_space.eq(
                (FIFO_WORDS - fifo.level) >= 260)

        # The device's "ss" is the 78.125 MHz core domain.
        m.submodules.usb = DomainRenamer({"ss": "core"})(usb)

        # LTSSM training indicator for the PHY's Gen2 descrambler /
        # polarity acquisition (bug #39 history): through the bridge's
        # core->pclk seam register. Terminate the decoded LTSSM cone at
        # a core FF first; otherwise it has only 6.4 ns across that seam.
        m.d.core += bridge.ltssm_training.eq(usb.ltssm_in_training)

        m.d.comb += led.o.eq(usb.link_trained)

        # ==============================================================
        # Debug UARTs
        # ==============================================================
        # UART0/tag L: P1/R/E (or X abort) PIPE capture frames; format in
        # pipe_capture.py. Each ring contains 128 consecutive pclk beats,
        # INCLUDING dv=0, and freezes 96 cycles after the selected event.
        # The default event is the first emitted DPH with length >18.
        #
        # UART1/tag C: interval counters, every 2**20/24MHz = 43.69 ms.
        #   0 RX ACK(rty=1), 1/2/3 recovery timers/RX/TX, 4 RX headers,
        #   5 TX TP, 6 TX DPH, 7 completed DPP (including EDB),
        #   8 TX framing errors, 9 TX DPPCRC, 10 TX header errors,
        #   11 TX LC errors, 12 pclk cycles, 13 rxclk cycles,
        #   14 TS1, 15 TS2, 16 SDS, 17 TX-FIFO>=28 cycles,
        #   18 STATUS received, 19 EP0 ACK dispatch, 20 TP offer cycles,
        #   21 TP queue accepts, 22 link-header blocked cycles,
        #   23 payload underruns, 24 capture-command overflow cycles,
        #   25 trained cycles, 26 ungated accepted MAC beats,
        #   27/28 ungated MAC TP/DPH starts (not complete-header verdicts).
        # Checker counts are trained-gated; zero during recovery alone
        # is NOT evidence of MAC silence. Ch25-28 qualify that inference.
        # Clock telltales are 1/8 the old 2**23 gate's counts.
        # Flags: sticky framing/header/LC[0], underrun[1], DPPCRC[2],
        # trained[3]. Ch0 must be zero except legitimate recovery ACKs.
        # UART1 RX: R=force recovery (unchanged); 0/1/2=select and rearm
        # long-DPH/retraining/manual capture; A=rearm; T=manual trigger;
        # D=replay the frozen dump. No serial-waveform muxing.
        uart0 = platform.request("uart", 0)
        uart1 = platform.request("uart", 1)

        # TX beat-pacing visibility: TxFifoWrNum is the PHY's 32-deep
        # Gen2 TX FIFO occupancy, pclk domain.
        txfifo_hi28 = Signal()
        m.d.ss += txfifo_hi28.eq(adapter.phy.TxFifoWrNum >= 28)

        m.submodules.txchk = txchk = DomainRenamer({"ss": "core"})(
            Gen2TxWireChecker())
        m.d.comb += [
            txchk.data.eq(usb.debug_wire_tx_data),
            txchk.ctrl.eq(usb.debug_wire_tx_ctrl),
            txchk.strobe.eq(usb.debug_wire_tx_strobe),
            txchk.enable.eq(usb.link_trained),
        ]

        m.submodules.capture = capture = PipeBeatCapture(DBG_FREQ, BAUD_RATE)
        # The two core events cross to pclk as toggles. These are true
        # synchronous 2:1 paths, NOT false-pathed CDCs. A core pulse must
        # not be counted twice by pclk. The capture inputs share its edge.
        events, long_seen = capture_events(m, txchk.long_dph, usb.link_trained)
        core_context = Signal(5)
        m.d.core += core_context.eq(Cat(usb.link_trained,
            usb.debug_gen2_data_mode, usb.ltssm_in_training,
            long_seen, usb.debug_link_hdr_blocked))
        m.d.comb += [
            capture.data.eq(adapter.phy.PipeTxData),
            capture.datavalid.eq(adapter.phy.PipeTxDataValid),
            capture.start_block.eq(adapter.phy.PipeTxStartBlock),
            capture.sync_header.eq(adapter.phy.PipeTxSyncHead),
            capture.fifo_level.eq(adapter.phy.TxFifoWrNum),
            capture.tx_state.eq(usb.debug_gen2_tx_state),
            capture.triggers.eq(events),
            # Scheduler state is one CORE cycle old; it is not claimed
            # to be metadata of the beat that the 2:1 bridge is emitting.
            # Context: rate[0], phase[1], electrical-idle[2], trained[3],
            # RX-data-mode[4], training[5], long-DPH-seen[6], blocked[7].
            # Bits 3:8 are also one core cycle old (registered seam).
            capture.context.eq(Cat(adapter.rate[0], core_div,
                adapter.tx_elec_idle, core_context)),
            uart0.tx.o.eq(capture.tx_o),
        ]

        retry_flagged = Signal()
        underrun_sticky = Signal()
        m.d.core += retry_flagged.eq(
            usb.debug_rx_hdr_stb & (usb.debug_rx_hdr_type == 4)
            & (usb.debug_rx_hdr_dw1[:4] == 1) & usb.debug_rx_hdr_dw1[6])
        with m.If(usb.debug_payload_underrun):
            m.d.core += underrun_sticky.eq(1)
        raw_tp_start = Signal()
        raw_dph_start = Signal()
        raw_hp_start = (usb.debug_wire_tx_strobe
                        & (usb.debug_wire_tx_ctrl[:4] == 15)
                        & (usb.debug_wire_tx_data[:32] == 0xf7fbfbfb))
        m.d.core += [
            raw_tp_start.eq(raw_hp_start & (usb.debug_wire_tx_data[32:37] == 4)),
            raw_dph_start.eq(raw_hp_start & (usb.debug_wire_tx_data[32:37] == 8)),
        ]
        m.domains += ClockDomain("rxprobe", reset_less=True)
        m.d.comb += ClockSignal("rxprobe").eq(lane.rx.pcs_clkout)
        m.submodules.pipeprobe = pipeprobe = DomainRenamer({"cfg": "dbg"})(
            ClockFreqProbe(clk_freq=DBG_FREQ, baud=BAUD_RATE, gate_bits=20,
                           compact=True, channels=(
                ("core", retry_flagged),
                ("core", usb.debug_recovery_timers),
                ("core", usb.debug_recovery_rx),
                ("core", usb.debug_recovery_tx),
                ("core", usb.debug_rx_hdr_stb),
                ("core", txchk.tp_seen),
                ("core", txchk.dph_seen),
                ("core", txchk.dpp_seen),
                ("core", txchk.framing_error),
                ("core", txchk.crc_error),
                ("core", txchk.header_error),
                ("core", txchk.lc_error),
                ("ss", None),
                ("rxprobe", None),
                ("core", usb.debug_ts1_detected),
                ("core", usb.debug_ts2_detected),
                ("core", usb.debug_gen2_sds_detected),
                ("ss", txfifo_hi28),
                ("core", usb.debug_status_received),
                ("core", usb.debug_hsk_ep0_dispatch),
                ("core", usb.debug_tp_hdr_valid),
                ("core", usb.debug_tp_hdr_accepted),
                ("core", usb.debug_link_hdr_blocked),
                ("core", usb.debug_payload_underrun),
                ("dbg", capture.command_overflow),
                ("core", usb.link_trained),
                ("core", usb.debug_wire_tx_strobe),
                ("core", raw_tp_start),
                ("core", raw_dph_start),
            )))
        pipe_flags = Signal(4)
        m.submodules += FFSynchronizer(
            Cat(txchk.framing_error_sticky | txchk.header_error_sticky
                | txchk.lc_error_sticky, underrun_sticky,
                txchk.crc_error_sticky, usb.link_trained),
            pipe_flags, o_domain="dbg")
        m.d.comb += [
            pipeprobe.flags.eq(pipe_flags),
            uart1.tx.o.eq(pipeprobe.tx_o),
        ]

        # uart1 RX: the 'R' forced-recovery hook (parked #29-#31
        # hardware verdict; runs during the Gen2 ladder).
        m.submodules.uart1_rx = rx1 = DomainRenamer("dbg")(
            AsyncSerialRX(divisor=DBG_FREQ // BAUD_RATE))
        rx1_i = Signal(init=1)
        m.submodules += FFSynchronizer(uart1.rx.i, rx1_i, o_domain="dbg",
                                       init=1)
        m.d.comb += [rx1.i.eq(rx1_i), rx1.ack.eq(1)]
        command_valid = rx1.rdy & ~rx1.err.as_value().any()
        m.d.comb += [capture.command.eq(rx1.data),
                     capture.command_strobe.eq(command_valid)]
        forcerec_tgl = Signal()
        with m.If(command_valid & (rx1.data == ord("R"))):
            m.d.dbg += forcerec_tgl.eq(~forcerec_tgl)
        forcerec_s = Signal()
        m.submodules += FFSynchronizer(forcerec_tgl, forcerec_s,
                                       o_domain="core")
        forcerec_d = Signal()
        m.d.core += forcerec_d.eq(forcerec_s)
        m.d.comb += usb.debug_force_recovery.eq(forcerec_s != forcerec_d)

        return m


# ======================================================================
# Build entry point
# ======================================================================

def generate_serdes_files():
    """Generate serdes.toml / serdes.csr for the selected BOOT_RATE.

    With BOOT_RATE="10G" the blob is byte-identical to the pinned,
    hardware-proven reference (verified at build time by comparison with
    the usb31-enum copy); the adapter then rate-switches on the LTSSM's
    command only.
    """
    serdes, _ = make_serdes()
    toml_path = HERE / "serdes.toml"
    csr_path = HERE / "serdes.csr"
    serdes.generate_csr(output_path=str(csr_path), toml_path=str(toml_path),
                        extra_writes=usb3_boot_writes(QUAD, LANE))
    print(f"Generated {toml_path.name} / {csr_path.name} ({BOOT_RATE} boot)")


def _setup_gowin_env(platform):
    os.environ.setdefault("LD_PRELOAD",
                          "/usr/lib/x86_64-linux-gnu/libfreetype.so.6")
    os.environ.setdefault("LD_LIBRARY_PATH",
                          str(Path(platform.gowin_path) / "IDE" / "lib"))
    gowin_bin = str(Path(platform.gowin_path) / "IDE" / "bin")
    if gowin_bin not in os.environ.get("PATH", ""):
        os.environ["PATH"] = gowin_bin + os.pathsep + os.environ["PATH"]


def build(do_program=False):
    generate_serdes_files()
    platform = DKUSBGW5AT60Platform()
    _setup_gowin_env(platform)
    platform.add_file("serdes.csr", (HERE / "serdes.csr").read_text())
    plan = platform.build(LunaEnumTop(), name="luna_enum_gen2", do_build=False)
    # The generated project_process_config.json does not set these options
    # in gw_sh. Keep the platform's other options and override this top only.
    # 3/1/0 (timing-priority placement, fanout clock order) is the measured
    # closing setting for the #57 relaunch RTL: 0/1/1 misses setup on the
    # Gen1-encoder/adapter pclk cones, while the falling-edge relaunch makes
    # the bridge seam structurally immune to the hold skew that 3/1/x used
    # to expose (HANDOVER 10ac/10ad; s22_pnr310_timing.json).
    script = plan.files["luna_enum_gen2.tcl"]
    marker = "\nrun all\n"
    if script.count(marker) != 1:
        raise RuntimeError("unexpected Gowin build script: missing unique run all")
    plan.files["luna_enum_gen2.tcl"] = script.replace(marker,
        "\nset_option -place_option 3 -route_option 1 -timing_driven 1\n"
        "set_option -clock_route_order 0 -route_maxfan 23\nrun all\n")
    products = plan.execute_local(str(HERE / "build"))
    if do_program:
        require_timing_met()
        platform.toolchain_program(products, "luna_enum_gen2")


def require_timing_met():
    """Reject unsafe Gen2 images, including related-clock failures (#55)."""
    try:
        report = json.loads(subprocess.check_output([
            sys.executable, str(HERE.parents[2] / "tools/gowin_timing_report.py"),
            str(HERE / "build"), "--json"]))
        fmax = {row["clock_name"]: row["actual_fmax_mhz"] for row in report["fmax"]}
        required = {"core_clk": 78.125, "pclk": 156.25, "rxclk": 161.29}
        valid = all(math.isfinite(fmax[name]) and fmax[name] >= minimum
                    for name, minimum in required.items())
        for section, value in (("tns", "endpoints_tns"),
                               ("setup_slack", "slack_ns"), ("hold_slack", "slack_ns")):
            valid &= bool(report[section]) and all(
                math.isfinite(row[value]) and row[value] >= 0 for row in report[section])
        for analysis in ("Setup", "Hold"):
            valid &= int(report["sta_summary"][f"Numbers of {analysis} Violated Endpoints"]) == 0
    except (OSError, subprocess.CalledProcessError, KeyError, TypeError, ValueError) as error:
        sys.exit(f"Gen2 timing report unavailable or invalid: {error}")
    if not valid:
        sys.exit("Gen2 timing gate failed; image NOT FLASHED (check related-clock setup/hold too)")
    print(f"Gen2 timing gate MET: {fmax}; related-clock setup/hold clean")


def flash():
    bitstream = HERE / "build" / "luna_enum_gen2.fs"
    if not bitstream.exists():
        sys.exit(f"no bitstream at {bitstream}; run `python top.py` first")
    require_timing_met()
    cmd = ["openFPGALoader", "-c", "ft232", str(bitstream)]
    try:
        subprocess.check_call(cmd)
    except subprocess.CalledProcessError:
        subprocess.check_call(["sudo", "-n"] + cmd)


if __name__ == "__main__":
    if "serdes" in sys.argv:
        generate_serdes_files()
    elif "flash" in sys.argv:
        flash()
    else:
        build(do_program="program" in sys.argv)
