#!/usr/bin/env python3
"""Gen2 (10 Gbps / SuperSpeedPlus) link-partner simulation — gate G2.

The scripted-host counterpart of ``sim_link_loopback.py`` for Gen2:
the DUT is the full ``USBSuperSpeedDevice`` (physical + link +
protocol + endpoints, exactly the stack the hardware tops build) on a
64-bit PIPE, and the host model speaks the Gen2 wire dialect through
the REAL coding chain: every block the host sends is scrambled by the
oracle-pinned python model and pushed through the silicon-proven RTL
``gw_usb3`` **Descrambler** into the DUT's PIPE RX (just like the
PHY), and every DUT TX beat is pushed through the RTL **Scrambler**
and decoded by the python descrambler (host side).

Phases (env ``PHASE=``, default ``train``):

``scd``    Polling.LFPS SuperSpeedPlus Capability Declaration: the
           host pulses rx_elec_idle as Polling.LFPS bursts whose
           repeat period is SCD1-modulated ('0010', tRepeat 6-9 us =
           0 / 11-14 us = 1 [6.9.4]); it then measures the DEVICE's
           burst repeat periods and requires an SCD1 signature.
``lbpm``   SCD1/SCD2 exchange, then Polling.PortMatch/PortConfig:
           the host transmits PHY Capability LBPMs (PWM-shaped, tPWM
           2.2 us [6.9.5, Table 6-33]) announcing Gen 2x1, requires
           >=4 matched capability LBPMs from the device, performs
           the PHY Ready handshake, and requires pipe.rate to remain
           at the 10G boot trim [7.5.4.5/.6].
``lbpm5g`` as ``lbpm``, but the host announces Gen 1x1 (5 Gbps):
           the device (higher capability) must adjust its
           advertisement down, and the PortConfig window must run
           the 10G->5G rate handshake (pipe.rate -> 0, acked by the
           host's PIPE phy_status stub).
``fb-legacy``   Gen1-only host (plain 8.5 us Polling.LFPS, never any
           SCD): the device must lead with >=4 SCD1, then switch to
           NON-VARYING tRepeat (the 16-legacy-burst rule
           [7.5.4.3.1]), switch the PHY to 5G, and reach
           Polling.RxEQ at SuperSpeed.
``fb-noscd2``   SCD1 answered, but the host never declares SCD2 in
           Polling.LFPSPlus: after 64 received bursts without SCD2
           the device must revert to non-varying tRepeat and fall
           back to SuperSpeed operation [7.5.4.4].
``fb-timeout``  full 10G negotiation (SCD + PortMatch + PortConfig +
           PHY Ready), then the host goes silent through training:
           the Polling.Active timeout at Gen2 must re-enter
           Polling.PortMatch advertising the NEXT-highest capability
           (Gen 1x1), negotiate 5G, and complete Gen1 training entry
           [7.5.4.8.2].  Run with TSCALE=0.0625 TSEQ_LEN=256 to keep
           the 12 ms training timeouts sim-sized.
``train``  post-PortConfig 10G training: host streams SYNC + TSEQ +
           TS1 blocks (real scrambler chain) and requires >= 8
           block-format TS1s from the device, then TS2 handshake,
           SDS, and Idle Symbols [7.5.4.7-.10].
``enum``   ``train`` + header-sequence/credit advertisement
           (modulo-16 LGOOD, LCRD1/LCRD2 [7.2.4.1.x]) + a
           GetDescriptor(Device) SETUP over Gen2 framing; requires a
           DPH+DPP response.

RED BASELINE (recorded in HANDOVER 10p): against the unmodified
Gen1-only stack every phase must FAIL with its diagnostic — scd:
"non-varying tRepeat, no SCD1"; train: "0 block-format TS1s".  The
battery runs these entries with EXPECT=red until the Phase-3/4 device
work lands; a phase that unexpectedly PASSES trips the battery so the
flip is always a conscious act.

Run: .venv/bin/python -u sim/sim_link_gen2.py     (PHASE=scd|train|enum)
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from amaranth import ClockDomain, ClockSignal, Elaboratable, Module, ResetSignal
from amaranth.sim import Simulator

from luna.gateware.interface.pipe import PIPEInterface
from luna.gateware.usb.usb3.device import USBSuperSpeedDevice
from usb_protocol.emitters import SuperSpeedDeviceDescriptorCollection

from gw_usb3.scramble import Scrambler, Descrambler
from gw_usb3.tables import BLOCK_CONTROL, BLOCK_DATA, BlockType

from gen2_coding import (ScramblerModel, sync_block, tseq_block, ts1_block,
                         ts2_block, sds_block, idle_block, skp_block,
                         pack_symbol_stream, link_command_syms,
                         header_packet_syms, beats_to_syms)

PHASE = os.environ.get("PHASE", "train")
VERBOSE = int(os.environ.get("VERBOSE", "0"))

# Sim-shortening knobs (fb-timeout): scale the ms-scale LTSSM timeouts
# and the TSEQ burst length (same idiom as the Gen1 training sims).
TSEQ_LEN = int(os.environ.get("TSEQ_LEN", "65536"))
TSCALE = float(os.environ.get("TSCALE", "1"))

# ss clock: 156.25 MHz (the Gen2 operating point)
CLK = 156.25e6
US = int(CLK / 1e6)              # cycles per microsecond (156)

# LBPM constants [USB 3.2r1 6.9.5, Tables 6-33 / 7-13]
TPWM_US = 2.2
LBPM_CAP_GEN2X1 = 0x04           # PHY Capability, [3:2]=01: 10 Gbps
LBPM_CAP_GEN1X1 = 0x00           # PHY Capability, [3:2]=00: 5 Gbps
LBPM_PHY_READY = 0x01            # PHY Ready, [1:0]=01

SCD1 = (0, 1, 0, 0)              # '0010' wire (LSb-first) order
SCD2 = (1, 0, 1, 1)              # '1101' wire (LSb-first) order


def create_descriptors():
    d = SuperSpeedDeviceDescriptorCollection()
    with d.DeviceDescriptor() as dd:
        dd.idVendor = 0x1209
        dd.idProduct = 0x0001
        dd.iManufacturer = "luna-ss"
        dd.iProduct = "gen2 sim"
        dd.iSerialNumber = "0"
        dd.bNumConfigurations = 1
    with d.ConfigurationDescriptor() as c:
        with c.InterfaceDescriptor() as i:
            i.bInterfaceNumber = 0
            with i.EndpointDescriptor() as e:
                e.bEndpointAddress = 0x81
                e.wMaxPacketSize = 1024
            with i.EndpointDescriptor() as e:
                e.bEndpointAddress = 0x01
                e.wMaxPacketSize = 1024
    return d


class BenchPIPE(PIPEInterface, Elaboratable):
    """Bare 64-bit PIPE: all signals driven/observed by the testbench."""

    def __init__(self):
        super().__init__(width=8)

    def elaborate(self, platform):
        return Module()


class Bench(Elaboratable):
    def __init__(self):
        self.pipe = BenchPIPE()
        # real RTL coding chain, wired by the testbench
        self.host_descr = Descrambler()   # host->device direction
        self.dev_scr = Scrambler()        # device->host direction

    def elaborate(self, platform):
        m = Module()
        for dom in ("ss", "sync"):
            m.domains += ClockDomain(dom)
        m.d.comb += [
            ClockSignal("sync").eq(ClockSignal("ss")),
            ResetSignal("sync").eq(ResetSignal("ss")),
        ]
        m.submodules.host_descr = self.host_descr
        m.submodules.dev_scr = self.dev_scr

        kwargs = {}
        if TSEQ_LEN != 65536:
            kwargs["tseq_burst_length"] = TSEQ_LEN
        if TSCALE != 1:
            kwargs["polling_timeout_scale"] = TSCALE
        usb = USBSuperSpeedDevice(phy=self.pipe, sync_frequency=CLK,
                                  gen2=True, **kwargs)
        usb.add_standard_control_endpoint(create_descriptors())
        m.submodules.usb = self.usb = usb

        # host->device: RTL descrambler output feeds the PIPE RX
        # (identical to the PHY's datapath position).
        m.d.comb += [
            self.pipe.rx_data        .eq(self.host_descr.data_out),
            self.pipe.rx_datavalid   .eq(self.host_descr.data_out_valid),
            self.pipe.rx_start_block .eq(self.host_descr.data_out_start_block),
            self.pipe.rx_sync_header .eq(self.host_descr.data_out_block_head),
            # device->host: PIPE TX into the RTL scrambler
            self.dev_scr.data_in            .eq(self.pipe.tx_data),
            self.dev_scr.data_in_valid      .eq(self.pipe.tx_datavalid),
            self.dev_scr.data_in_start_block.eq(self.pipe.tx_start_block),
            self.dev_scr.data_in_block_head .eq(self.pipe.tx_sync_header),
            self.dev_scr.data_out_ready     .eq(1),
        ]
        return m


# ── host-side helpers ────────────────────────────────────────────────

async def bringup(ctx, pipe):
    """PIPE reset/startup dance (TUSB dialect: phy_status high through
    reset, dropping only after the MAC releases pipe.reset)."""
    ctx.set(pipe.phy_status, 1)
    ctx.set(pipe.power_present, 1)
    ctx.set(pipe.rx_elec_idle, 1)
    ctx.set(pipe.rx_valid, 0)
    for _ in range(2000):
        await ctx.tick("ss")
        if not ctx.get(pipe.reset):
            break
    else:
        raise AssertionError("MAC never released pipe.reset")
    await ctx.tick("ss").repeat(20)
    ctx.set(pipe.phy_status, 0)
    await ctx.tick("ss").repeat(10)


def classify_trepeat(gap_cycles):
    """tRepeat bins per 6.9.4.1 (in us): 6-9 -> 0, 11-14 -> 1.  Bins
    widened (+/-) so both 125 MHz and 156.25 MHz LTSSM timing
    assumptions classify; returns '?' for out-of-bin."""
    us = gap_cycles / US
    if 4.0 <= us <= 9.9:
        return 0
    if 10.5 <= us <= 18.0:
        return 1
    return None


async def lfps_burst(ctx, pipe, burst_us=1.0):
    ctx.set(pipe.rx_elec_idle, 0)
    await ctx.tick("ss").repeat(int(burst_us * US))
    ctx.set(pipe.rx_elec_idle, 1)


async def phase_scd(ctx, bench):
    """SCD1 exchange in Polling.LFPS, then the SCD2 confirmation in
    Polling.LFPSPlus [6.9.4, 7.5.4.3/.4]: stage 1 sends host SCD1 and
    requires the device's SCD1 signature; stage 2 switches the host to
    SCD2 and requires the device's SCD2 signature (the device is then
    in Polling.LFPSPlus)."""
    pipe = bench.pipe
    await bringup(ctx, pipe)

    cyc = 0
    tx_starts = []
    tx_active_prev = False
    pd_prev = 0
    pd_ack_at = None

    def step_observers():
        nonlocal tx_active_prev, pd_prev, pd_ack_at
        pd = ctx.get(pipe.power_down)
        if pd != pd_prev:
            pd_ack_at = cyc + 4
            pd_prev = pd
        if pd_ack_at is not None:
            ctx.set(pipe.phy_status, 1 if cyc == pd_ack_at else 0)
            if cyc > pd_ack_at:
                pd_ack_at = None
        active = bool(ctx.get(pipe.tx_detrx_lpbk)) and \
            bool(ctx.get(pipe.tx_elec_idle))
        if active and not tx_active_prev:
            tx_starts.append(cyc)
        tx_active_prev = active

    async def host_bursts(pattern_bits, reps):
        nonlocal cyc
        for rep in range(reps):
            bit = pattern_bits[rep % 4]
            gap_us = 7.5 if bit == 0 else 12.5
            for phase_len, ei in ((int(1.0 * US), 0), (int(gap_us * US), 1)):
                ctx.set(pipe.rx_elec_idle, ei)
                for _ in range(phase_len):
                    await ctx.tick("ss")
                    cyc += 1
                    step_observers()

    def device_bits(since_cycle=0):
        starts = [s for s in tx_starts if s >= since_cycle]
        gaps = [b - a for a, b in zip(starts, starts[1:])]
        return [classify_trepeat(g) for g in gaps], gaps

    def has_rotation(bits, pattern):
        seq = "".join("x" if b is None else str(b) for b in bits)
        rots = {"".join(str(x) for x in pattern[i:] + pattern[:i])
                for i in range(4)}
        return any(r in seq for r in rots)

    # stage 1: host declares SCD1
    scd1_wire = [0, 1, 0, 0]         # '0010' LSb first
    scd2_wire = [1, 0, 1, 1]         # '1101' LSb first
    await host_bursts(scd1_wire, 24)
    bits1, gaps1 = device_bits()
    print(f"SCD: stage-1 device gaps (us): "
          f"{[round(g / US, 1) for g in gaps1[:12]]}")
    print(f"SCD: stage-1 bits: {bits1[:12]}")
    if not has_rotation(bits1, scd1_wire):
        print("SCD FAIL: non-varying tRepeat, no SCD1 signature "
              "(Gen1-only Polling.LFPS)")
        return False
    print("SCD: SCD1 signature found")

    # stage 2: host confirms with SCD2; device must follow into
    # Polling.LFPSPlus and declare SCD2.
    stage2_start = cyc
    await host_bursts(scd2_wire, 32)
    bits2, gaps2 = device_bits(stage2_start)
    print(f"SCD: stage-2 device bits: {bits2[:16]}")
    if not has_rotation(bits2, scd2_wire):
        print("SCD FAIL: no SCD2 from device after host SCD2 "
              "(Polling.LFPSPlus missing)")
        return False
    print("SCD: SCD2 signature found (device in Polling.LFPSPlus)")
    return True


def has_rotation(bits, pattern):
    """True if any cyclic rotation of ``pattern`` appears in ``bits``."""
    seq = "".join("x" if b is None else str(b) for b in bits)
    pat = list(pattern)
    rots = {"".join(str(x) for x in pat[i:] + pat[:i])
            for i in range(len(pat))}
    return any(r in seq for r in rots)


class HostModem:
    """Host-side LFPS/LBPM modem plus PIPE housekeeping for the
    negotiation phases.

    * Emulates the PHY-side ``phy_status`` acks for ``power_down`` and
      ``rate`` changes (the PIPE contract; the hardware adapter's rate
      sequencer acks the same way) and records every ``rate`` change.
    * Records every device TX signaling pulse (``tx_detrx_lpbk &
      tx_elec_idle`` while in P0) and demodulates them into polling
      bursts ('B'), LBPM bits ('0'/'1') and delimiters ('D').
    """

    def __init__(self, ctx, bench):
        self.ctx = ctx
        self.pipe = bench.pipe
        self.cyc = 0
        self.pulses = []          # (start_cyc, length_cycles)
        self.rate_changes = []    # (cyc, new_value)
        self._act_prev = False
        self._act_start = 0
        self._pd_prev = 0
        self._ack_at = None
        self._rate_prev = None

    def _observe(self):
        ctx, pipe = self.ctx, self.pipe
        pd = ctx.get(pipe.power_down)
        if pd != self._pd_prev:
            self._ack_at = self.cyc + 4
            self._pd_prev = pd
        rate = ctx.get(pipe.rate)
        if self._rate_prev is None:
            self._rate_prev = rate
        elif rate != self._rate_prev:
            self.rate_changes.append((self.cyc, rate))
            self._ack_at = self.cyc + 8
            self._rate_prev = rate
        ctx.set(pipe.phy_status, 1 if self._ack_at == self.cyc else 0)
        if self._ack_at is not None and self.cyc > self._ack_at:
            self._ack_at = None
        active = bool(ctx.get(pipe.tx_detrx_lpbk)) and \
            bool(ctx.get(pipe.tx_elec_idle))
        if active and not self._act_prev:
            self._act_start = self.cyc
        if self._act_prev and not active:
            self.pulses.append((self._act_start, self.cyc - self._act_start))
        self._act_prev = active

    async def run(self, cycles, ei=1):
        self.ctx.set(self.pipe.rx_elec_idle, ei)
        for _ in range(cycles):
            await self.ctx.tick("ss")
            self.cyc += 1
            self._observe()

    async def pulse(self, on_cycles, off_cycles):
        await self.run(on_cycles, ei=0)
        await self.run(off_cycles, ei=1)

    async def send_bursts(self, pattern_bits, reps, burst_us=1.0):
        """Polling.LFPS bursts: 1 us on + gap.  Pattern bits modulate
        the start-to-start repeat (None = plain 8.5 us legacy)."""
        for rep in range(reps):
            bit = pattern_bits[rep % len(pattern_bits)]
            gap = 8.5 if bit is None else (8.5 if bit == 0 else 13.5)
            await self.pulse(int(burst_us * US),
                             int((gap - burst_us) * US))

    async def send_lbpm(self, byte, count=1):
        """PWM-shaped LBPM byte messages, delimiters at start/end and
        in between [6.9.5.2]."""
        tpwm = int(TPWM_US * US)
        on0, on1 = tpwm // 3, (2 * tpwm) // 3
        for _ in range(count):
            await self.pulse(tpwm, tpwm)              # (re)opening delim
            for i in range(8):
                on = on1 if (byte >> i) & 1 else on0
                await self.pulse(on, tpwm - on)
        await self.pulse(tpwm, tpwm)                  # closing delimiter

    # ── demodulation ─────────────────────────────────────────────────
    def symbols(self, since=0):
        out = []
        for (s, d) in self.pulses:
            if s < since:
                continue
            w = d / US
            if 0.55 <= w <= 0.90:
                out.append((s, '0'))
            elif 0.90 < w <= 1.25:
                out.append((s, 'B'))      # plain polling/SCD burst
            elif 1.30 <= w <= 1.75:
                out.append((s, '1'))
            elif 1.95 <= w <= 2.60:
                out.append((s, 'D'))
            else:
                out.append((s, '?'))
        return out

    def lbpm_messages(self, since=0):
        """Decode LBPM byte messages (LSb first, delimiter framed)."""
        msgs, bits, framed = [], [], False
        for (s, sym) in self.symbols(since):
            if sym == 'D':
                if framed and len(bits) == 8:
                    msgs.append((s, sum(b << i for i, b in enumerate(bits))))
                framed, bits = True, []
            elif sym in '01' and framed:
                bits.append(int(sym))
                if len(bits) > 8:
                    framed, bits = False, []
            else:
                framed, bits = False, []
        return msgs

    def burst_gaps(self, since=0):
        starts = [s for (s, d) in self.pulses
                  if s >= since and 0.5 <= d / US <= 1.5]
        return [b - a for a, b in zip(starts, starts[1:])]

    def scd_bits(self, since=0):
        return [classify_trepeat(g) for g in self.burst_gaps(since)]

    async def scd_exchange(self, scd1_reps=24, scd2_reps=32):
        """Drive the SCD1 then SCD2 stages; (ok, diagnostic)."""
        await self.send_bursts(SCD1, scd1_reps)
        bits1 = self.scd_bits()
        if not has_rotation(bits1, SCD1):
            return False, f"no SCD1 from device: {bits1[:12]}"
        mark = self.cyc
        await self.send_bursts(SCD2, scd2_reps)
        bits2 = self.scd_bits(mark)
        if not has_rotation(bits2, SCD2):
            return False, f"no SCD2 from device: {bits2[:16]}"
        return True, ""


async def lbpm_negotiate(ctx, bench, hm, tag, host_cap, count=12):
    """PortMatch + PortConfig from the host side; returns (ok, expect)
    where expect is the matched capability byte."""
    pipe = bench.pipe

    # ── Polling.PortMatch: announce our capability, require the match ──
    mark = hm.cyc
    await hm.send_lbpm(host_cap, count=count)
    msgs = [v for (_, v) in hm.lbpm_messages(mark)]
    print(f"{tag}: device LBPMs during PortMatch: {[hex(v) for v in msgs]}")
    # The lower capability wins; the device is Gen 2x1, so the match
    # outcome equals the host's announcement.
    expect = host_cap
    if not msgs:
        print(f"{tag} FAIL: no LBPM from device (Polling.PortMatch missing)")
        return False, expect
    matched = [v for v in msgs if v == expect]
    if len(matched) < 4:
        print(f"{tag} FAIL: expected >=4 matched PHY Capability LBPMs "
              f"({expect:#04x}), got {len(matched)}")
        return False, expect

    # ── Polling.PortConfig: PHY Ready handshake ──
    mark = hm.cyc
    await hm.send_lbpm(LBPM_PHY_READY, count=count)
    msgs = [v for (_, v) in hm.lbpm_messages(mark)]
    print(f"{tag}: device LBPMs during PortConfig: {[hex(v) for v in msgs]}")
    ready = [v for v in msgs if v == LBPM_PHY_READY]
    if len(ready) < 2:
        print(f"{tag} FAIL: expected >=2 PHY Ready LBPMs, got {len(ready)}")
        return False, expect
    return True, expect


async def check_training_entry(ctx, bench, hm, tag):
    """After PortConfig/fallback the device must be in Polling.RxEQ:
    LFPS stops and the transmitter leaves electrical idle."""
    await hm.run(int(60 * US))
    if ctx.get(bench.pipe.tx_elec_idle):
        print(f"{tag} FAIL: device did not enter Polling.RxEQ "
              f"(tx still in electrical idle)")
        return False
    return True


async def phase_lbpm(ctx, bench, host_cap=LBPM_CAP_GEN2X1):
    """Polling.PortMatch / PortConfig happy paths (M3a+M3b+M3c)."""
    tag = "LBPM" if host_cap == LBPM_CAP_GEN2X1 else "LBPM5G"
    pipe = bench.pipe
    await bringup(ctx, pipe)
    hm = HostModem(ctx, bench)

    ok, diag = await hm.scd_exchange()
    if not ok:
        print(f"{tag} FAIL: SCD stage: {diag}")
        return False
    print(f"{tag}: SCD1+SCD2 exchange complete")

    ok, expect = await lbpm_negotiate(ctx, bench, hm, tag, host_cap)
    if not ok:
        return False

    # ── rate outcome (M3c): the MAC owns pipe.rate ──
    want_gen2 = expect == LBPM_CAP_GEN2X1
    final_rate = ctx.get(pipe.rate)
    print(f"{tag}: rate changes {hm.rate_changes}; "
          f"final pipe.rate={final_rate}")
    if want_gen2 and (hm.rate_changes or final_rate != 1):
        print(f"{tag} FAIL: rate should have stayed at the 10G boot trim")
        return False
    if not want_gen2 and final_rate != 0:
        print(f"{tag} FAIL: 5G outcome but pipe.rate never switched to 0")
        return False

    if not await check_training_entry(ctx, bench, hm, tag):
        return False
    print(f"{tag}: PortMatch/PortConfig complete; device training at "
          f"{'Gen2' if want_gen2 else 'Gen1'}")
    return True


async def phase_fb_legacy(ctx, bench):
    """Fallback (i): Gen1-only host never declares SCD [7.5.4.3]."""
    pipe = bench.pipe
    await bringup(ctx, pipe)
    hm = HostModem(ctx, bench)

    await hm.send_bursts([None], 48)
    bits = hm.scd_bits()
    if not has_rotation(bits[:16], SCD1):
        print(f"FB-LEGACY FAIL: no leading SCD1 declaration: {bits[:16]}")
        return False
    gaps_us = [round(g / US, 1) for g in hm.burst_gaps()]
    tail = gaps_us[-12:]
    if len(tail) < 12 or not all(9.0 <= u <= 11.0 for u in tail):
        print(f"FB-LEGACY FAIL: device keeps modulating (no non-varying "
              f"tRepeat tail): {tail}")
        return False
    if ctx.get(pipe.rate) != 0 or not hm.rate_changes:
        print(f"FB-LEGACY FAIL: no 10G->5G rate switch before SS "
              f"training: {hm.rate_changes}")
        return False
    if not await check_training_entry(ctx, bench, hm, "FB-LEGACY"):
        return False
    print("FB-LEGACY: >=4 SCD1, then non-varying tRepeat, 5G switch, "
          "Polling.RxEQ at SuperSpeed")
    return True


async def phase_fb_noscd2(ctx, bench):
    """Fallback (ii): SCD2 never arrives in Polling.LFPSPlus [7.5.4.4]."""
    pipe = bench.pipe
    await bringup(ctx, pipe)
    hm = HostModem(ctx, bench)

    await hm.send_bursts(SCD1, 24)
    if not has_rotation(hm.scd_bits(), SCD1):
        print(f"FB-NOSCD2 FAIL: no SCD1 from device: {hm.scd_bits()[:12]}")
        return False
    mark = hm.cyc
    await hm.send_bursts([None], 100)
    bits2 = hm.scd_bits(mark)
    if not has_rotation(bits2, SCD2):
        print(f"FB-NOSCD2 FAIL: device never reached Polling.LFPSPlus "
              f"(no SCD2): {bits2[:16]}")
        return False
    gaps_us = [round(g / US, 1) for g in hm.burst_gaps(mark)]
    tail = gaps_us[-12:]
    if len(tail) < 12 or not all(9.0 <= u <= 11.0 for u in tail):
        print(f"FB-NOSCD2 FAIL: no non-varying tRepeat after missing "
              f"SCD2: {tail}")
        return False
    if ctx.get(pipe.rate) != 0 or not hm.rate_changes:
        print(f"FB-NOSCD2 FAIL: no 10G->5G rate switch: {hm.rate_changes}")
        return False
    if not await check_training_entry(ctx, bench, hm, "FB-NOSCD2"):
        return False
    print("FB-NOSCD2: SCD2 lead, then non-varying fallback, 5G switch, "
          "Polling.RxEQ at SuperSpeed")
    return True


async def phase_fb_timeout(ctx, bench):
    """Fallback (iii): Gen2 training timeout -> Polling.PortMatch
    re-entry with the next-highest capability [7.5.4.8.2].  Needs
    TSCALE/TSEQ_LEN to keep the 12 ms timers sim-sized."""
    pipe = bench.pipe
    await bringup(ctx, pipe)
    hm = HostModem(ctx, bench)

    ok, diag = await hm.scd_exchange(scd2_reps=16)
    if not ok:
        print(f"FB-TIMEOUT FAIL: SCD stage: {diag}")
        return False

    ok, _ = await lbpm_negotiate(ctx, bench, hm, "FB-TIMEOUT",
                                 LBPM_CAP_GEN2X1, count=8)
    if not ok:
        return False
    if hm.rate_changes:
        print(f"FB-TIMEOUT FAIL: unexpected rate change at the 10G "
              f"outcome: {hm.rate_changes}")
        return False
    print("FB-TIMEOUT: 10G negotiation complete; host now SILENT through "
          "Gen2 training")

    # The device trains alone (RxEQ then Polling.Active) and must fall
    # back to PortMatch, advertising Gen 1x1, after 12 ms (scaled).
    mark = hm.cyc
    deadline = hm.cyc + int(12e-3 * TSCALE * CLK) + TSEQ_LEN * 8 + 60000
    msgs = []
    while hm.cyc < deadline:
        await hm.run(2000)
        msgs = hm.lbpm_messages(mark)
        if msgs:
            break
    if not msgs:
        print("FB-TIMEOUT FAIL: device never re-entered Polling.PortMatch "
              "after the Gen2 training timeout")
        return False
    if msgs[0][1] != LBPM_CAP_GEN1X1:
        print(f"FB-TIMEOUT FAIL: re-entry advertisement {msgs[0][1]:#04x}, "
              f"expected next-highest Gen 1x1 (0x00)")
        return False
    print("FB-TIMEOUT: PortMatch re-entry advertising Gen 1x1")

    ok, _ = await lbpm_negotiate(ctx, bench, hm, "FB-TIMEOUT",
                                 LBPM_CAP_GEN1X1, count=8)
    if not ok:
        return False
    if ctx.get(pipe.rate) != 0 or not hm.rate_changes:
        print(f"FB-TIMEOUT FAIL: no 10G->5G rate switch after the 5G "
              f"outcome: {hm.rate_changes}")
        return False
    if not await check_training_entry(ctx, bench, hm, "FB-TIMEOUT"):
        return False
    print("FB-TIMEOUT: negotiation loop closed -- 10G match, Gen2 "
          "training timeout, PortMatch re-entry, 5G match, Gen1 training")
    return True


class HostRx:
    """Collects device TX beats (through the RTL scrambler) and
    decodes them with the python descrambler."""

    def __init__(self, bench):
        self.bench = bench
        self.model = ScramblerModel(descramble=True)
        self.blocks = []            # (head, syms) per completed block
        self._cur = None

    def sample(self, ctx):
        scr = self.bench.dev_scr
        if not ctx.get(scr.data_out_valid):
            return
        s = ctx.get(scr.data_out_start_block)
        h = ctx.get(scr.data_out_block_head)
        d = ctx.get(scr.data_out)
        clear = self.model.feed(s, h, d)
        if s or self._cur is None:
            if self._cur:
                self.blocks.append(self._cur)
            self._cur = (h, beats_to_syms([clear]))
        else:
            h0, syms = self._cur
            self._cur = (h0, syms + beats_to_syms([clear]))

    def block_count(self, head, first_sym):
        n = 0
        for h, syms in self.blocks:
            if h == head and syms and syms[0] == first_sym:
                n += 1
        return n


async def feed_blocks(ctx, bench, model_tx, blocks, rx=None):
    """Scramble blocks with the python model and push them through the
    RTL descrambler into the DUT, one beat per cycle."""
    descr = bench.host_descr
    for blk in blocks:
        for (s, h, d) in blk.beats():
            wire = model_tx.feed(s, h, d)
            ctx.set(descr.data_in_valid, 1)
            ctx.set(descr.data_in_start_block, s)
            ctx.set(descr.data_in_block_head, h)
            ctx.set(descr.data_in, wire)
            await ctx.tick("ss")
            if rx:
                rx.sample(ctx)
    ctx.set(descr.data_in_valid, 0)


async def phase_train(ctx, bench, continue_to_enum=False):
    pipe = bench.pipe
    await bringup(ctx, pipe)

    # skip LFPS negotiation: pretend PortConfig completed at Gen2 —
    # signal presence, then stream training blocks.
    ctx.set(pipe.rx_elec_idle, 0)
    ctx.set(pipe.rx_valid, 1)
    # (pipe.rate is MAC-driven; at Gen2 the LTSSM will own the rate
    # select -- nothing to force from the host side here.)

    model_tx = ScramblerModel()
    rx = HostRx(bench)

    # Polling.RxEQ/Active shape (shortened): SYNC + TSEQ burst, then
    # TS1 bursts with SYNC every 32 [6.4.1.2.1].
    await feed_blocks(ctx, bench, model_tx, [sync_block()] +
                      [tseq_block()] * 64, rx)
    for _ in range(8):
        await feed_blocks(ctx, bench, model_tx,
                          [sync_block()] + [ts1_block()] * 32, rx)
        if rx.block_count(BLOCK_CONTROL, int(BlockType.TS1)) >= 8:
            break

    n_ts1 = rx.block_count(BLOCK_CONTROL, int(BlockType.TS1))
    print(f"TRAIN: device emitted {n_ts1} block-format TS1 ordered sets "
          f"({len(rx.blocks)} blocks total from device TX)")
    if n_ts1 < 8:
        print("TRAIN FAIL: no Gen2 TS1 blocks from device "
              "(Gen1-only physical/link framing)")
        return False

    # TS2 handshake
    for _ in range(4):
        await feed_blocks(ctx, bench, model_tx,
                          [sync_block()] + [ts2_block()] * 16, rx)
    n_ts2 = rx.block_count(BLOCK_CONTROL, int(BlockType.TS2))
    if n_ts2 < 8:
        print(f"TRAIN FAIL: only {n_ts2} TS2 blocks from device")
        return False

    # SDS -> Idle
    await feed_blocks(ctx, bench, model_tx,
                      [sds_block()] + [idle_block()] * 24, rx)
    got_sds = any(h == BLOCK_CONTROL and s[0] == 0xE1
                  for h, s in rx.blocks)
    got_idle = any(h == BLOCK_DATA and all(x == 0 for x in s)
                   for h, s in rx.blocks)
    if not (got_sds and got_idle):
        print(f"TRAIN FAIL: SDS={got_sds} idle={got_idle} from device")
        return False
    print("TRAIN: U0 data stream established at Gen2 framing")

    if not continue_to_enum:
        return True

    # ---- enum: advertisement + GetDescriptor(Device) ----
    # header seq advertisement LGOOD_15 (=our seq-1 with expected 0),
    # then LCRD1_A..D and LCRD2_A..D [7.2.4.1.x].
    syms = link_command_syms(0b0000, 15)                  # LGOOD_15
    for i in range(4):
        syms += link_command_syms(0b0001, i)              # LCRD1_x
    for i in range(4):
        syms += link_command_syms(0b0001, 0b1000 | i)     # LCRD2_x (b3 set)
    await feed_blocks(ctx, bench, model_tx, pack_symbol_stream(syms), rx)

    # SETUP DPH+DPP: GetDescriptor(DEVICE, 8 bytes) to addr 0 ep 0
    setup = bytes([0x80, 0x06, 0x00, 0x01, 0x00, 0x00, 0x08, 0x00])
    from sim_link_loopback import crc32_payload
    dw0 = 0x08 | (0 << 25)          # type=DPH... (see Gen1 host model)
    # NOTE: exact DW packing is filled in when the Phase-4 device work
    # lands; the enum phase cannot get past training against the
    # unmodified stack, so this is scaffolding kept minimal on purpose.
    print("ENUM FAIL: not implemented past training (Phase-4 scaffolding)")
    return False


async def watchdogged(ctx, coro, cycles):
    return await coro


def main():
    bench = Bench()
    sim = Simulator(bench)
    sim.add_clock(1 / CLK, domain="ss")

    result = {}

    async def tb(ctx):
        if PHASE == "scd":
            result["ok"] = await phase_scd(ctx, bench)
        elif PHASE == "lbpm":
            result["ok"] = await phase_lbpm(ctx, bench)
        elif PHASE == "lbpm5g":
            result["ok"] = await phase_lbpm(ctx, bench,
                                            host_cap=LBPM_CAP_GEN1X1)
        elif PHASE == "fb-legacy":
            result["ok"] = await phase_fb_legacy(ctx, bench)
        elif PHASE == "fb-noscd2":
            result["ok"] = await phase_fb_noscd2(ctx, bench)
        elif PHASE == "fb-timeout":
            result["ok"] = await phase_fb_timeout(ctx, bench)
        elif PHASE == "train":
            result["ok"] = await phase_train(ctx, bench)
        elif PHASE == "enum":
            result["ok"] = await phase_train(ctx, bench,
                                             continue_to_enum=True)
        else:
            raise SystemExit(f"unknown PHASE={PHASE}")

    sim.add_testbench(tb)
    sim.run()

    if result.get("ok"):
        print(f"GEN2 {PHASE.upper()} PASS")
        return 0
    print(f"GEN2 {PHASE.upper()} FAIL (red against the current stack "
          f"is the expected G2 baseline; see HANDOVER 10p)")
    return 1


if __name__ == "__main__":
    sys.exit(main())
