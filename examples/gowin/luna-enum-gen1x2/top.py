"""Gen 1x2 PortMatch trace probe -- Gowin DK_USB (GW5AT-60).

W0.3 of the width program (usb3_design.md P0/5): advertise
**Gen 1x2** (LBPM capability 0x40 -- Table 7-13 b6 = dual-lane; the
mission text's 0x20 was a transcription error, b5 is reserved) as the
device's highest PHY capability and CAPTURE the 20G root port's
answer.  Expected per Table 7-14 (UFP Gen 1x2 x DFP Gen 2x2): the
host adjusts its announcement down to 0x40 -- the dual-lane match.

This build has NO x2 datapath: after PortConfig at Gen 1x2 the
x1-only training cannot complete (the host trains BOTH lanes), the
24 ms Polling.Active window expires, and the LTSSM re-enters
PortMatch advertising its next-highest = Gen 1x1 [7.5.4.5.1], where
training succeeds -- the device should ultimately enumerate at
5000M.  The uart1 LBPM ring shows the whole story:

    'D' entries: received PHY LBPM bytes, word = rx byte | (our
        concurrent tx byte << 8) -- look for rx 0x44 (host announces
        Gen 2x2), then rx 0x40 (HOST MATCHED DUAL-LANE = the W0.3
        verdict), PHY Ready 0x41/0xC1 (b6=DFP, b7=RT-Config), then
        the second PortMatch round at 0x00.
    'A' entries: our transmitted LBPM completions (word = tx byte).

Clocking: the MAC rides the PROVEN pre-MAC boot rate switch (adapter
boots the byte-pinned 10G blob, retunes to 5G, THEN wakes the MAC):
a Gen 1x2-highest device never needs the 10G trim, so the whole MAC
runs at 125 MHz -- Gen1-class timing closure, no 156.25 lottery
(usb3_design.md 7: the Gen 1x2 cells close at Gen1 effort).  The
device is built with ``phy_boots_gen2=False`` so the LTSSM's
applied-rate tracking and the physical layer's rate handshake both
reset to the 5G state the adapter hands over.

Build & program:

    python top.py                # build only (build/)
    python top.py flash          # flash the existing bitstream
    python top.py program        # build + flash

Watch: uart0 link probe /dev/ttyUSB4, uart1 LBPM ring /dev/ttyUSB5
(both 115200).
"""

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

from amaranth.hdl import *
from amaranth.lib.cdc import FFSynchronizer

from gowin_serdes.dkusb_gw5at60 import (DKUSBGW5AT60Platform,
                                        add_serdes_refclk_forward)
from gowin_serdes import GowinDevice, make_usb3_serdes, usb3_boot_writes
from gowin_serdes.config import RefClkSource
from gowin_serdes.usb3 import attach_usb3_phy
from gowin_serdes.bench import ClockFreqProbe

from luna.gateware.interface.serdes_phy.gowin_gtr12 import GowinGTR12PIPE
from luna.gateware.usb.usb3.device import USBSuperSpeedDevice
from luna.gateware.usb.usb3.physical.lfps import LBPM_CAP_GEN1X2

from usb_protocol.emitters import SuperSpeedDeviceDescriptorCollection

# ── Configuration ─────────────────────────────────────────────────────
QUAD, LANE = 0, 1
REF_CLK_SOURCE = RefClkSource.Q0_REFCLK1
REF_CLK_FREQ = "200M"
DBG_FREQ = 24_000_000
BAUD_RATE = 115_200
BOOT_RATE = "10G"       # byte-pinned blob; the ADAPTER retunes to 5G


def make_serdes():
    return make_usb3_serdes(GowinDevice.GW5AT_60, QUAD, LANE,
                            REF_CLK_SOURCE, REF_CLK_FREQ,
                            boot_rate=BOOT_RATE)


def create_descriptors():
    descriptors = SuperSpeedDeviceDescriptorCollection()

    with descriptors.DeviceDescriptor() as d:
        d.idVendor           = 0x1209       # pid.codes
        d.idProduct          = 0x0001       # test PID
        d.bcdUSB             = 3.1
        d.bMaxPacketSize0    = 9            # 2**9 = 512
        d.iManufacturer      = "LUNA + gw_usb3"
        d.iProduct           = "GTR12 Gen1x2 PortMatch probe"
        d.iSerialNumber      = "DK60"
        d.bNumConfigurations = 1

    with descriptors.ConfigurationDescriptor() as c:
        c.bMaxPower = 50
        with c.InterfaceDescriptor() as i:
            i.bInterfaceNumber = 0

    return descriptors


class LunaEnumGen1x2Top(Elaboratable):
    def elaborate(self, platform):
        m = Module()

        led = platform.request("led", 0)
        usb_pwr_en = platform.request("usb_pwr_en", 0)
        m.d.comb += usb_pwr_en.o.eq(0)     # device mode: never source VBUS

        # Quiet the USB2 pins (floating pins = phantom low-speed device).
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

        m.d.cfg += [
            por_n.eq(por_cnt > 66_011),
            luna_go.eq(por_cnt.all()),
        ]

        # ==============================================================
        # SerDes + PHY + PIPE adapter (the PROVEN Gen1 shipping shape:
        # pre-MAC boot rate switch; bug #38 CSR lane plumb)
        # ==============================================================
        serdes, group = make_serdes()
        m.submodules.serdes = serdes
        lane = group.lanes[0]
        drp = getattr(serdes, group.drp_name)
        m.d.comb += serdes.por_n.eq(por_n)

        from gw_usb3.upar_csr import UparCsrConfig
        adapter = GowinGTR12PIPE(boot_rate_switch=True,
                                 boot_domain="ss_raw",
                                 phy_kwargs=dict(
                                     csr_config=UparCsrConfig(quad=QUAD,
                                                              lane=LANE)))
        m.submodules.adapter = adapter
        attach_usb3_phy(m, adapter.phy, lane, drp)

        m.domains += ClockDomain("ss_raw", reset_less=True)
        m.d.comb += ClockSignal("ss_raw").eq(lane.tx.pcs_clkout)
        m.d.comb += adapter.boot_start.eq(luna_go)
        rstn_r0 = Signal()
        rstn_r1 = Signal()
        m.d.ss_raw += [rstn_r0.eq(luna_go & adapter.phy_ready),
                       rstn_r1.eq(rstn_r0)]
        for dom in ("ss", "sync"):
            m.domains += ClockDomain(dom)
            m.d.comb += [
                ClockSignal(dom).eq(ClockSignal("ss_raw")),
                ResetSignal(dom).eq(~rstn_r1),
            ]

        # ==============================================================
        # LUNA SuperSpeed device: Gen 1x2-highest, 125 MHz throughout
        # ==============================================================
        m.submodules.usb = usb = USBSuperSpeedDevice(
            phy=adapter, sync_frequency=125e6, gen2=True,
            ssp_capability=LBPM_CAP_GEN1X2, phy_boots_gen2=False)
        usb.add_standard_control_endpoint(create_descriptors())

        # bug #39 discipline: the real LTSSM training output (consumed
        # only by Gen2-datapath builds; harmless and correct here).
        m.d.comb += adapter.ltssm_training.eq(usb.ltssm_in_training)

        m.d.comb += led.o.eq(usb.link_trained)

        # ==============================================================
        # Debug UARTs
        # ==============================================================
        # uart0 (link probe, Gen1-compatible format):
        #   C <ss-cnt> <lfps-det> <ts1-det> <ts2-det> <idle-hs> <flags>
        #   ss-cnt stays 0x29aaa9x (125 MHz) for the WHOLE session --
        #   this build never runs the 10G trim.
        uart0 = platform.request("uart", 0)
        uart1 = platform.request("uart", 1)

        linkprobe = DomainRenamer({"cfg": "dbg"})(
            ClockFreqProbe(clk_freq=DBG_FREQ, baud=BAUD_RATE, channels=(
                ("ss", None),
                ("ss", usb.debug_lfps_polling_detected),
                ("ss", usb.debug_ts1_detected),
                ("ss", usb.debug_ts2_detected),
                ("ss", usb.debug_idle_handshake),
            )))
        m.submodules.linkprobe = linkprobe
        link_flags = Signal(4)
        m.submodules += FFSynchronizer(
            Cat(usb.link_trained, usb.link_in_reset,
                usb.debug_phy_ready, usb.debug_engage_terminations),
            link_flags, o_domain="dbg")
        m.d.comb += [
            linkprobe.flags.eq(link_flags),
            uart0.tx.o.eq(linkprobe.tx_o),
        ]

        # uart1: LBPM negotiation ring (the W0.3 capture).  Port A ('D')
        # = every RECEIVED LBPM byte, word = rx | (our tx << 8); port B
        # ('A') = every completed LBPM transmission, word = tx byte.
        import importlib.util as _ilu
        _spec = _ilu.spec_from_file_location(
            "multiep_top", HERE.parent / "luna-multiep" / "top.py")
        _multiep = _ilu.module_from_spec(_spec)
        _spec.loader.exec_module(_multiep)

        m.submodules.evcap = evcap = _multiep.BurstEventCapture(
            clk_freq=DBG_FREQ, baud=BAUD_RATE)
        m.d.comb += [
            evcap.a_stb.eq(usb.debug_lbpm_rx_valid),
            evcap.a_tp .eq(0),
            evcap.a_dw1.eq(Cat(usb.debug_lbpm_rx_message,
                               usb.debug_lbpm_tx_message)),

            evcap.b_stb.eq(usb.debug_lbpm_sent),
            evcap.b_tag.eq(3),
            evcap.b_dw1.eq(usb.debug_lbpm_tx_message),

            uart1.tx.o.eq(evcap.tx_o),
        ]

        return m


# ======================================================================
# Build entry point
# ======================================================================

def generate_serdes_files():
    serdes, _ = make_serdes()
    toml_path = HERE / "serdes.toml"
    csr_path = HERE / "serdes.csr"
    serdes.generate_csr(output_path=str(csr_path), toml_path=str(toml_path),
                        extra_writes=usb3_boot_writes(QUAD, LANE))
    print(f"Generated {toml_path.name} / {csr_path.name} ({BOOT_RATE} boot)")


def _setup_gowin_env(platform):
    import os
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
    platform.build(LunaEnumGen1x2Top(), name="luna_enum_gen1x2",
                   build_dir="build", do_program=do_program)


def flash():
    bitstream = HERE / "build" / "luna_enum_gen1x2.fs"
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
