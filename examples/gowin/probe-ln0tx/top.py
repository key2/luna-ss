"""LN0 TX bring-up probe (W0.2, usb3_design.md P0/§3.2).

Bug #38 proved Q0_LN0's CSR path and RX side on silicon; the TX
serializer has never fired.  With the bench cable in the straight
orientation LN0's TX pair faces the host's (ignored) lane-1 receiver,
so the only software-reachable TX exercise is the GTR12's own loopback:

    PIPE P0 + TxDetectRx_loopback=1 (TxElecIdle=0)
      -> UparCsr writes 0x10000 to the lane loopback CSR
         (0x800256 + lane*0x200) [gw_usb3 upar_csr dispatch]
      -> the PHY's PIPE wrapper ALSO short-circuits PipeRx* from
         PipeTx* digitally (vendor behavior) -- so the PIPE RX side
         proves nothing.

THIS RIG therefore taps the RAW FABRIC RX WORD (lane.rx.data, below
the PHY) and scans it for the 8b10b K28.5 comma of the transmitted
pattern at EVERY bit offset:

  * comma at arbitrary/rotating bit alignment  = the data crossed the
    serializer + CDR + deserializer (PMA-level loopback): LN TX FIRES.
  * comma only at the transmitted alignment    = PCS-digital loopback
    (weaker: TX PCS exercised, serializer unproven).
  * no comma, rx word static                   = loopback dead on this
    lane.

uart0:  C <pclk> <rxclk> <comma-any> <comma-aligned> <flags>
  flags: [0] por released  [1] phy_ready  [2] loopback engaged
Run A/B: build+flash LANE=1 (control: the proven lane) then LANE=0.

    LANE=1 python top.py ; python top.py flash
    LANE=0 python top.py ; python top.py flash
"""

import os
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

# ── Configuration ─────────────────────────────────────────────────────
QUAD = 0
LANE = int(os.environ.get("LANE", "0"))
# LOOPBACK=0: control build -- hold electrical idle, never engage the
# loopback.  Discriminates loopback-sourced RX from HOST-sourced RX
# (straight cable: LN1's RX pads face the host's TX lane 0, and the
# host's polling TS1 stream is comma-rich).
LOOPBACK = int(os.environ.get("LOOPBACK", "1"))
REF_CLK_SOURCE = RefClkSource.Q0_REFCLK1
REF_CLK_FREQ = "200M"
DBG_FREQ = 24_000_000
BAUD_RATE = 115_200
BOOT_RATE = "10G"        # byte-pinned blob; adapter boot-switches to 5G

# K28.5 10-bit codes (abcdeifghj transmit order), both running
# disparities, plus their bit reversals (fabric word bit-order guard).
K28_5_CODES = (0b0011111010, 0b1100000101,
               0b0101111100, 0b1010000011)


def make_serdes():
    return make_usb3_serdes(GowinDevice.GW5AT_60, QUAD, LANE,
                            REF_CLK_SOURCE, REF_CLK_FREQ,
                            boot_rate=BOOT_RATE)


class ProbeLn0TxTop(Elaboratable):
    def elaborate(self, platform):
        m = Module()

        led = platform.request("led", 0)
        usb_pwr_en = platform.request("usb_pwr_en", 0)
        m.d.comb += usb_pwr_en.o.eq(0)

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

        # ── clocks & POR ──
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

        key = platform.request("key", 0)
        key_s = Signal(2)
        m.d.cfg += key_s.eq(Cat(key.i, key_s[0]))
        with m.If(key_s[1]):
            m.d.cfg += por_cnt.eq(0)

        m.d.cfg += [
            por_n.eq(por_cnt > 66_000),
            luna_go.eq(por_cnt.all()),
        ]

        # ── SerDes + PHY (bug #38 discipline: CSR config follows LANE) ──
        serdes, group = make_serdes()
        m.submodules.serdes = serdes
        lane = group.lanes[0]
        drp = getattr(serdes, group.drp_name)
        m.d.comb += serdes.por_n.eq(por_n)

        from gw_usb3.upar_csr import UparCsrConfig
        adapter = GowinGTR12PIPE(boot_rate_switch=True, boot_domain="ss_raw",
                                 phy_kwargs=dict(
                                     csr_config=UparCsrConfig(quad=QUAD,
                                                              lane=LANE)))
        m.submodules.adapter = adapter
        attach_usb3_phy(m, adapter.phy, lane, drp)

        m.domains += ClockDomain("ss_raw", reset_less=True)
        m.d.comb += ClockSignal("ss_raw").eq(lane.tx.pcs_clkout)
        m.d.comb += adapter.boot_start.eq(luna_go)

        m.domains += ClockDomain("ss")
        rstn_r0 = Signal()
        rstn_r1 = Signal()
        m.d.ss_raw += [rstn_r0.eq(adapter.phy_ready), rstn_r1.eq(rstn_r0)]
        m.d.comb += [
            ClockSignal("ss").eq(ClockSignal("ss_raw")),
            ResetSignal("ss").eq(~rstn_r1),
        ]

        # ── MAC-less PIPE harness: settle, then loopback + TX pattern ──
        # Pattern: K28.5 D10.2 K28.5 D10.2 (comma-rich; the classic
        # electrical-idle-exit/alignment pattern).
        settle = Signal(18)          # ~2 ms at 125 MHz
        lb_on = Signal()
        with m.If(~settle.all()):
            m.d.ss += settle.eq(settle + 1)
        with m.Else():
            m.d.ss += lb_on.eq(LOOPBACK)

        m.d.comb += [
            adapter.reset.eq(0),
            adapter.rate.eq(0),                      # Gen1
            adapter.power_down.eq(0),                # P0
            adapter.tx_elec_idle.eq(~lb_on),
            adapter.tx_detrx_lpbk.eq(lb_on),
            adapter.rx_termination.eq(1),
            adapter.tx_data.eq(0x4A_BC_4A_BC),       # D10.2 K28.5 x2
            adapter.tx_datak.eq(0b0101),
            adapter.tx_datavalid.eq(1),
        ]

        # ── raw fabric RX comma scanner (below the PHY) ──
        # 80-bit sliding window of the 40-bit 5G fabric RX word; check
        # every bit offset for any K28.5 code variant.
        rx_now = Signal(40)
        rx_prev = Signal(40)
        m.domains += ClockDomain("rxprobe", reset_less=True)
        m.d.comb += ClockSignal("rxprobe").eq(lane.rx.pcs_clkout)
        m.d.rxprobe += [
            rx_now.eq(lane.rx.data[0:40]),
            rx_prev.eq(rx_now),
        ]
        window = Signal(80)
        m.d.comb += window.eq(Cat(rx_prev, rx_now))

        # Raw RX activity: static word = the loopback point is gated
        # (e.g. electrical idle); active-but-comma-free = data path alive
        # with a coding/ordering problem.
        rx_act = Signal()
        m.d.comb += rx_act.eq(rx_now != rx_prev)

        comma_any = Signal()
        comma_aligned = Signal()
        any_hits = []
        aligned_hits = []
        for off in range(40):
            sym = window.bit_select(off, 10)
            hit = Signal(name=f"hit_{off}")
            m.d.comb += hit.eq(sum(sym == c for c in K28_5_CODES) != 0)
            any_hits.append(hit)
            if off % 10 == 0:
                aligned_hits.append(hit)
        m.d.rxprobe += [
            comma_any.eq(Cat(*any_hits).any()),
            comma_aligned.eq(Cat(*aligned_hits).any()),
        ]

        # ── uart0 probe ──
        uart0 = platform.request("uart", 0)
        m.submodules.probe = probe = DomainRenamer({"cfg": "dbg"})(
            ClockFreqProbe(clk_freq=DBG_FREQ, baud=BAUD_RATE, channels=(
                ("ss", None),                    # pclk (125 after boot sw)
                ("rxprobe", None),               # rx pcs clk
                ("rxprobe", rx_act),             # raw RX word activity
                ("rxprobe", comma_any),          # comma at ANY bit offset
                ("rxprobe", comma_aligned),      # comma at tx alignment
            )))

        flags = Signal(4)
        m.submodules += FFSynchronizer(
            Cat(por_n, adapter.phy_ready, lb_on, C(0, 1)),
            flags, o_domain="dbg")
        m.d.comb += [
            probe.flags.eq(flags),
            uart0.tx.o.eq(probe.tx_o),
            led.o.eq(lb_on),
        ]

        return m


def generate_serdes_files():
    serdes, _ = make_serdes()
    toml_path = HERE / "serdes.toml"
    csr_path = HERE / "serdes.csr"
    serdes.generate_csr(output_path=str(csr_path), toml_path=str(toml_path),
                        extra_writes=usb3_boot_writes(QUAD, LANE))
    print(f"Generated {toml_path.name} / {csr_path.name} "
          f"(lane {LANE}, {BOOT_RATE} boot)")


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
    platform.build(ProbeLn0TxTop(), name=f"probe_ln{LANE}tx",
                   build_dir=f"build_ln{LANE}", do_program=do_program)


def flash():
    bitstream = HERE / f"build_ln{LANE}" / f"probe_ln{LANE}tx.fs"
    if not bitstream.exists():
        sys.exit(f"no bitstream at {bitstream}; run `LANE={LANE} python "
                 f"top.py` first")
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
