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

STATUS: behavior-proven core (all nine Gen2 phases green at W128,
battery 66/66; HANDOVER 10aa) + the sim-fenced bridge; THIS TOP IS THE
FIRST GEN2-128 HARDWARE ELABORATION — the #49 bench-verdict vehicle.

Build & program:

    python top.py                # build only (build/)
    python top.py serdes         # regenerate serdes.toml/csr only
    python top.py flash          # flash the existing bitstream
    python top.py program        # build + flash

Watch:  examples/gowin/luna-multiep/uart_capture.py <s> <prefix>
"""

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

from gowin_serdes.bench import AsyncSerialRX, ClockFreqProbe

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
            usb.add_endpoint(out_ep)

            in_ep = SuperSpeedStreamInEndpoint(
                endpoint_number=ep, max_packet_size=1024,
                generate_zlps=False, max_burst=1)
            usb.add_endpoint(in_ep)

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
        # core->pclk seam register.
        m.d.comb += bridge.ltssm_training.eq(usb.ltssm_in_training)

        m.d.comb += led.o.eq(usb.link_trained)

        # ==============================================================
        # Debug UARTs
        # ==============================================================
        # Probes are re-homed to the domain whose state they sample:
        # MAC state = "core"; TxFifoWrNum = "ss" (pclk); rxclk telltale
        # unchanged.  The platform SDC declares pclk/rxclk/core_clk and
        # the mutual false paths (H1 lesson: without them the probes'
        # skew-tolerant snapshot handshakes are analyzed against the
        # 100 MHz default clocks and mask the real cones).
        #
        # uart0 (link probe, tag L):
        #   C <ss-cnt> <rec-timers> <rec-rx> <rec-tx> <ts1-det> <flags>
        #   ss-cnt telltale: 0x341554x = 156.25 MHz pclk (still 10G);
        #   0x29aaa9x = 125 MHz (fell back / never matched).  The MAC
        #   channels count in the 78.125 MHz core domain.
        #   ch1..3 split debug_recovery by cause: link maintenance
        #   timers / receiver bad_sequence / transmitter (LGOOD-LCRD
        #   mismatch, credit timeout).
        #   flags: trained[0] in_reset[1] phy_ready[2] terminations[3].
        # uart1 (pipe probe, tag C):
        #   C <rxclk> <rx-hdrs-accepted> <sds-det> <ts2-det> <txfifo-hi28> <flags>
        #   ch1 = debug_rx_hdr_stb count: ACCEPTED inbound header
        #   packets reaching the protocol layer (zero at Gen2 U0 = the
        #   old #42 failure; counting = host LMP/ITP traffic flowing).
        #   flags: power_down[0] tx_elec_idle[1] rx_elec_idle[2]
        #   data_mode[3].
        # uart1 RX: byte 'R' (0x52) forces ONE link recovery entry from
        # U0 -- the hardware verdict path for the recovery-retransmit
        # conformance (#29-#31) at Gen2.  During the forced-recovery
        # test itself the host may legitimately send rty=1
        # re-establishment ACKs; uart1 ch0 has no retry counter on this
        # loadout (the wire checkers stay multiep/Gen1) -- the verdict
        # is sha-exactness across the retrain.
        uart0 = platform.request("uart", 0)
        uart1 = platform.request("uart", 1)

        # TX beat-pacing visibility: TxFifoWrNum is the PHY's 32-deep
        # Gen2 TX FIFO occupancy, pclk domain.
        txfifo_hi28 = Signal()
        m.d.ss += txfifo_hi28.eq(adapter.phy.TxFifoWrNum >= 28)

        m.submodules.linkprobe = linkprobe = DomainRenamer({"cfg": "dbg"})(
            ClockFreqProbe(clk_freq=DBG_FREQ, baud=BAUD_RATE, channels=(
                ("ss", None),
                ("core", usb.debug_recovery_timers),
                ("core", usb.debug_recovery_rx),
                ("core", usb.debug_recovery_tx),
                ("core", usb.debug_ts1_detected),
            )))
        link_flags = Signal(4)
        m.submodules += FFSynchronizer(
            Cat(usb.link_trained, usb.link_in_reset,
                usb.debug_phy_ready, usb.debug_engage_terminations),
            link_flags, o_domain="dbg")
        m.d.comb += [
            linkprobe.flags.eq(link_flags),
            uart0.tx.o.eq(linkprobe.tx_o),
        ]

        m.domains += ClockDomain("rxprobe", reset_less=True)
        m.d.comb += ClockSignal("rxprobe").eq(lane.rx.pcs_clkout)
        m.submodules.pipeprobe = pipeprobe = DomainRenamer({"cfg": "dbg"})(
            ClockFreqProbe(clk_freq=DBG_FREQ, baud=BAUD_RATE, channels=(
                ("rxprobe", None),
                ("core", usb.debug_rx_hdr_stb),
                ("core", usb.debug_gen2_sds_detected),
                ("core", usb.debug_ts2_detected),
                ("ss", txfifo_hi28),
            )))
        pipe_flags = Signal(4)
        m.submodules += FFSynchronizer(
            Cat(adapter.power_down[0], adapter.tx_elec_idle,
                adapter.rx_elec_idle, usb.debug_gen2_data_mode),
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
        forcerec_tgl = Signal()
        with m.If(rx1.rdy & (rx1.data == ord("R"))):
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
    platform.build(LunaEnumTop(), name="luna_enum_gen2", build_dir="build",
                   do_program=do_program)


def flash():
    bitstream = HERE / "build" / "luna_enum_gen2.fs"
    if not bitstream.exists():
        sys.exit(f"no bitstream at {bitstream}; run `python top.py` first")
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
