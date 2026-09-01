"""Wide-fabric-trim silicon probe (W0.1, usb3_design.md P0/§3.1).

A bare SerDes bring-up rig -- NO PHY, NO MAC -- that boots Quad 0
lane 1 in a selectable fabric trim and reports the resulting PCS
clocks + raw RX activity on uart0.  The 2026-09-01 tool experiment
(/tmp/kilo/trim_experiment) established the configuration space of the
GW5AT-60:

  * width_mode > 20 does not exist (vendor tool KeyError: the fabric
    bus is 80-bit TX / 88-bit RX; 32x1:4 = native 128-bit is
    IMPOSSIBLE -- Gen 2x1 @ 128-bit PIPE must use the 2:1 bridge);
  * the wide Gen1 trim 20x1:4 (8 symbols @ 62.5 MHz) IS expressible:
    its boot blob differs from the proven 20x1:2 trim in exactly two
    lane clock-tree divider registers (LN1: 0x808608 111A->121A,
    0x808628 116->126).

THIS RIG is the silicon half: flash, watch uart0 (/dev/ttyUSB4).

    C <pclk> <rxclk> <rxact> <upar> <flags>

  pclk telltales (gate 2^23 @ 24 MHz; f = delta * 24e6 / 2^23):
    0x29aaa9x = 125   MHz  (proven 20x1:2 trim)
    0x14d555x = 62.5  MHz  (wide 20x1:4 trim -- the P0 verdict)
    0x341554x = 156.25 MHz (10G trim)
  rxact counts raw rx-word-change events in the RX PCS clock domain:
  nonzero while the host port drives LFPS/training at us (TX stays in
  electrical idle -- the host gives up quickly; POR replay via the
  board KEY restarts the window).

Select the trim with TRIM= at build time:

    TRIM=wide_5g_20x4 python top.py     (default; the P0 experiment)
    TRIM=ref_5g_20x2  python top.py     (control: proven 5G trim)
    TRIM=ref_10g_16x4 python top.py     (control: proven 10G trim)

Flash: python top.py flash    (or: sudo -n openFPGALoader -c ft232
       build/probe_trims.fs)
"""

import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

from amaranth.hdl import *

from gowin_serdes.dkusb_gw5at60 import (DKUSBGW5AT60Platform,
                                        add_serdes_refclk_forward)
from gowin_serdes import GowinDevice, GowinSerDes, GowinSerDesGroup
from gowin_serdes.config import (LaneConfig, OperationMode, PLLSelection,
                                 RefClkSource, GearRate)
from gowin_serdes.usb3 import (USB3_LANE_OVERRIDES, USB3_QUAD_OVERRIDES,
                               usb3_boot_writes)
from gowin_serdes.bench import ClockFreqProbe

# ── Configuration ─────────────────────────────────────────────────────
QUAD, LANE = 0, 1
REF_CLK_SOURCE = RefClkSource.Q0_REFCLK1
REF_CLK_FREQ = "200M"
DBG_FREQ = 24_000_000
BAUD_RATE = 115_200

TRIMS = {
    #                 rate    gear          width   expected pclk
    "wide_5g_20x4":  ("5G",  GearRate.G1_4, 20),  # 62.5  MHz, 8 sym
    "ref_5g_20x2":   ("5G",  GearRate.G1_2, 20),  # 125   MHz, 4 sym
    "ref_10g_16x4":  ("10G", GearRate.G1_4, 16),  # 156.25 MHz, 64-bit
}
TRIM = os.environ.get("TRIM", "wide_5g_20x4")


def make_serdes():
    rate, gear, width = TRIMS[TRIM]
    cfg = LaneConfig(
        operation_mode=OperationMode.TX_RX,
        tx_data_rate=rate,
        rx_data_rate=rate,
        tx_gear_rate=gear,
        rx_gear_rate=gear,
        width_mode=width,
        pll=PLLSelection.CPLL,
        ref_clk_source=REF_CLK_SOURCE,
        ref_clk_freq=REF_CLK_FREQ,
        toml_lane_overrides=dict(USB3_LANE_OVERRIDES),
    )
    group = GowinSerDesGroup(quad=QUAD, first_lane=LANE, lane_configs=[cfg],
                             toml_quad_overrides=dict(USB3_QUAD_OVERRIDES))
    return GowinSerDes(device=GowinDevice.GW5AT_60, groups=[group]), group


class ProbeTrimsTop(Elaboratable):
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

        # ── clocks & POR (the proven luna-enum-gen2 ordering) ──
        sys_clk = add_serdes_refclk_forward(m, platform)
        m.domains += ClockDomain("cfg", reset_less=True)
        m.d.comb += ClockSignal("cfg").eq(sys_clk)

        clk24 = platform.request("clk_24m", 0)
        m.domains += ClockDomain("dbg", reset_less=True)
        m.d.comb += ClockSignal("dbg").eq(clk24.i)

        por_cnt = Signal(18)
        por_n = Signal()
        with m.If(~por_cnt.all()):
            m.d.cfg += por_cnt.eq(por_cnt + 1)

        key = platform.request("key", 0)
        key_s = Signal(2)
        m.d.cfg += key_s.eq(Cat(key.i, key_s[0]))
        with m.If(key_s[1]):
            m.d.cfg += por_cnt.eq(0)

        m.d.cfg += por_n.eq(por_cnt > 66_000)

        # ── SerDes at the selected trim ──
        serdes, group = make_serdes()
        m.submodules.serdes = serdes
        lane = group.lanes[0]
        m.d.comb += serdes.por_n.eq(por_n)

        # PCS clock domains (reset-less: pure counters).
        m.domains += ClockDomain("ss", reset_less=True)
        m.d.comb += ClockSignal("ss").eq(lane.tx.pcs_clkout)
        m.domains += ClockDomain("rxprobe", reset_less=True)
        m.d.comb += ClockSignal("rxprobe").eq(lane.rx.pcs_clkout)

        # Raw RX activity: word-change events at the fabric RX width.
        rx_last = Signal(20)
        rx_act = Signal()
        m.d.rxprobe += rx_last.eq(lane.rx.data[0:20])
        m.d.comb += rx_act.eq(lane.rx.data[0:20] != rx_last)

        # ── uart0 probe ──
        # NOTE: the "upar" domain is created by GowinSerDes itself (the
        # GTR12 ring-oscillator life clock) -- referenced here by name.
        uart0 = platform.request("uart", 0)
        m.submodules.probe = probe = DomainRenamer({"cfg": "dbg"})(
            ClockFreqProbe(clk_freq=DBG_FREQ, baud=BAUD_RATE, channels=(
                ("ss", None),                # pclk frequency
                ("rxprobe", None),           # rxclk frequency
                ("rxprobe", rx_act),         # raw RX activity events
                ("upar", None),              # UPAR life clock
            )))

        flags = Signal(4)
        m.d.comb += flags.eq(Cat(por_n, C(0, 3)))
        m.d.comb += [
            probe.flags.eq(flags),
            uart0.tx.o.eq(probe.tx_o),
            led.o.eq(por_n),
        ]

        return m


def generate_serdes_files():
    serdes, _ = make_serdes()
    toml_path = HERE / "serdes.toml"
    csr_path = HERE / "serdes.csr"
    serdes.generate_csr(output_path=str(csr_path), toml_path=str(toml_path),
                        extra_writes=usb3_boot_writes(QUAD, LANE))
    print(f"Generated {toml_path.name} / {csr_path.name} (trim {TRIM})")


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
    platform.build(ProbeTrimsTop(), name="probe_trims", build_dir="build",
                   do_program=do_program)


def flash():
    bitstream = HERE / "build" / "probe_trims.fs"
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
