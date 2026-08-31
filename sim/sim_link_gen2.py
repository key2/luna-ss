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
                         header_packet_syms, dpp_syms, beats_to_syms,
                         HPSTART, DPHSTART, DPPSTART, DPPEND, DPPABORT,
                         LCSTART, IDL as G2_IDL, SHP as G2_SHP,
                         DPHP as G2_DPHP, SDP as G2_SDP, END as G2_END,
                         EDB as G2_EDB, SLC as G2_SLC, EPF as G2_EPF)

PHASE = os.environ.get("PHASE", "train")
VERBOSE = int(os.environ.get("VERBOSE", "0"))

# Sim-shortening knobs (fb-timeout): scale the ms-scale LTSSM timeouts
# and the TSEQ burst length (same idiom as the Gen1 training sims).
TSEQ_LEN = int(os.environ.get("TSEQ_LEN", "65536"))
TSCALE = float(os.environ.get("TSCALE", "1"))
# Negative-control knob (evidence that the conformance checks bite):
# NEG=nolcrd2 withholds the host's Type-2 credits -- a device with a
# REAL LCRD1/LCRD2 split must then never transmit its descriptor DP.
NEG = os.environ.get("NEG", "")

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
        # SuperSpeedPlus: bcdUSB 0310h [9.6.1].
        dd.bcdUSB = 3.10
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

        if PHASE == "echo":
            # Loopback endpoint pair on EP1 (the small bulk echo of the
            # ``gen2-echo`` battery entry).
            from luna.gateware.usb.usb3.endpoints.stream import \
                SuperSpeedStreamInEndpoint
            from luna.gateware.usb.usb3.endpoints.ss_stream_out import \
                SuperSpeedStreamOutEndpoint
            out_ep = SuperSpeedStreamOutEndpoint(
                endpoint_number=1, max_packet_size=1024)
            in_ep = SuperSpeedStreamInEndpoint(
                endpoint_number=1, max_packet_size=1024)
            usb.add_endpoint(out_ep)
            usb.add_endpoint(in_ep)
            m.d.comb += in_ep.stream.stream_eq(out_ep.stream)

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
        self.bench = bench
        self.pipe = bench.pipe
        self.cyc = 0
        self.pulses = []          # (start_cyc, length_cycles)
        self.rate_changes = []    # (cyc, new_value)
        self.notes = []           # protocol-level debug strobes
        self._act_prev = False
        self._act_start = 0
        self._pd_prev = 0
        self._ack_at = None
        self._rate_prev = None

    def _observe(self):
        ctx, pipe = self.ctx, self.pipe
        usb = getattr(self.bench, "usb", None)
        if usb is not None:
            if ctx.get(usb.debug_rx_dpp_invalid):
                self.notes.append(("dpp_invalid", self.cyc))
            if ctx.get(usb.debug_rx_hdr_stb):
                self.notes.append(("hdr_to_protocol",
                                   ctx.get(usb.debug_rx_hdr_type), self.cyc))
            if VERBOSE and ctx.get(usb.rx_data_tap.valid):
                d = ctx.get(usb.rx_data_tap.data)
                c = ctx.get(usb.rx_data_tap.ctrl)
                if d or c:
                    self.notes.append(("rxw", f"{d:08x}/{c:x}", self.cyc))
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


async def feed_blocks(ctx, bench, model_tx, blocks, rx=None, hm=None):
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
            if hm:
                hm.cyc += 1
                hm._observe()
    ctx.set(descr.data_in_valid, 0)


IDLE_SYM = int(BlockType.LIS)          # Gen2 Idle Symbol, 5Ah [7.1.2]


async def phase_train(ctx, bench, continue_to_enum=False):
    pipe = bench.pipe
    await bringup(ctx, pipe)
    hm = HostModem(ctx, bench)

    # Negotiate SuperSpeedPlus first (the proven G3 machinery): SCD1 +
    # SCD2, then PortMatch/PortConfig at the 10G outcome.
    ok, diag = await hm.scd_exchange(scd2_reps=16)
    if not ok:
        print(f"TRAIN FAIL: SCD stage: {diag}")
        return False
    ok, _ = await lbpm_negotiate(ctx, bench, hm, "TRAIN",
                                 LBPM_CAP_GEN2X1, count=8)
    if not ok:
        print("TRAIN FAIL: LBPM negotiation did not reach Polling.RxEQ")
        return False
    if hm.rate_changes or ctx.get(pipe.rate) != 1:
        print(f"TRAIN FAIL: pipe.rate left the 10G trim: {hm.rate_changes}")
        return False
    print("TRAIN: 10G negotiated; streaming training blocks")

    ctx.set(pipe.rx_elec_idle, 0)
    ctx.set(pipe.rx_valid, 1)

    model_tx = ScramblerModel()
    rx = HostRx(bench)

    # Polling.RxEQ/Active shape (shortened): SYNC + TSEQ burst, then
    # TS1 bursts with SYNC every 32 [6.4.1.2.1].
    await feed_blocks(ctx, bench, model_tx, [sync_block()] +
                      [tseq_block()] * 64, rx, hm)
    for _ in range(12):
        await feed_blocks(ctx, bench, model_tx,
                          [sync_block()] + [ts1_block()] * 32, rx, hm)
        if rx.block_count(BLOCK_CONTROL, int(BlockType.TS1)) >= 8:
            break

    n_ts1 = rx.block_count(BLOCK_CONTROL, int(BlockType.TS1))
    n_tseq = rx.block_count(BLOCK_CONTROL, int(BlockType.TSEQ))
    print(f"TRAIN: device emitted {n_tseq} TSEQ + {n_ts1} block-format "
          f"TS1 ordered sets ({len(rx.blocks)} blocks total)")
    if n_ts1 < 8:
        print("TRAIN FAIL: no Gen2 TS1 blocks from device "
              "(Gen1-only physical/link framing)")
        return False

    # TS2 handshake
    for _ in range(6):
        await feed_blocks(ctx, bench, model_tx,
                          [sync_block()] + [ts2_block()] * 16, rx, hm)
        if rx.block_count(BLOCK_CONTROL, int(BlockType.TS2)) >= 8:
            break
    n_ts2 = rx.block_count(BLOCK_CONTROL, int(BlockType.TS2))
    if n_ts2 < 8:
        print(f"TRAIN FAIL: only {n_ts2} TS2 blocks from device")
        return False

    # SDS -> Idle [7.5.4.10]: a single SDS, then data blocks carrying
    # Idle Symbols (5Ah at Gen2!).
    await feed_blocks(ctx, bench, model_tx,
                      [sds_block()] + [idle_block()] * 48, rx, hm)
    got_sds = any(h == BLOCK_CONTROL and s[0] == 0xE1
                  for h, s in rx.blocks)
    got_idle = any(h == BLOCK_DATA and all(x == IDLE_SYM for x in s)
                   for h, s in rx.blocks)
    if not (got_sds and got_idle):
        print(f"TRAIN FAIL: SDS={got_sds} idle={got_idle} from device")
        return False
    print("TRAIN: U0 data stream established at Gen2 framing")

    if not continue_to_enum:
        return True
    return await run_enum(ctx, bench, hm, rx, model_tx,
                          echo=(PHASE == "echo"))


class Gen2LinkHost:
    """Symbol-level Gen2 link partner: parses the device's data-block
    symbol stream (through HostRx) into link commands, header packets
    (validating the DPHSTART length replica) and DPPs, and builds the
    host's transmissions."""

    def __init__(self, ctx, bench, hm, rx, model_tx, tag="ENUM"):
        self.ctx, self.bench, self.hm = ctx, bench, hm
        self.rx, self.model_tx = rx, model_tx
        self.tag = tag
        self.events = []          # ('lc',cmd,sub) ('hdr',dws,seq,kind)
                                  # ('dpp',bytes,crc_ok)
        self._cursor = 0          # rx.blocks consumed
        self._syms = []           # pending symbol stream
        self._state = 'search'
        self._need = 0
        self._buf = []
        self._kind = None
        self._dpp_len = 0
        self.tx_seq = 0           # host header sequence (mod 16)
        self.errors = []

    # ── device -> host parsing ───────────────────────────────────────
    def pump(self):
        blocks = self.rx.blocks
        while self._cursor < len(blocks):
            h, syms = blocks[self._cursor]
            self._cursor += 1
            if h == BLOCK_DATA:
                self._syms += syms
        self._walk()

    def _walk(self):
        s = self._syms
        i = 0
        n = len(s)
        while True:
            if self._state == 'search':
                while i < n and s[i] == G2_IDL:
                    i += 1
                if i >= n:
                    break
                if n - i < 4:
                    break
                frame = tuple(s[i:i + 4])
                if frame == HPSTART:
                    self._state, self._need = 'hdr', 20 - 4
                    self._kind = 'hp'
                elif frame == DPHSTART:
                    self._state, self._need = 'hdr', 22 - 4
                    self._kind = 'dph'
                elif frame == DPPSTART:
                    self._state = 'dpp'
                    self._need = self._dpp_len + 4 + 4  # payload+crc+end
                elif frame == LCSTART:
                    self._state, self._need = 'lc', 4
                else:
                    self.errors.append(
                        f"unparseable symbols at cursor: "
                        f"{[hex(x) for x in s[i:i+8]]}")
                    i += 1
                    continue
                i += 4
            else:
                if n - i < self._need:
                    break
                body = s[i:i + self._need]
                i += self._need
                self._finish(body)
                self._state = 'search'
        self._syms = s[i:]

    def _finish(self, body):
        from sim_link_loopback import crc16_header, crc32_payload
        if self._state == 'lc':
            w = body[0] | (body[1] << 8)
            w2 = body[2] | (body[3] << 8)
            if w != w2:
                self.errors.append(f"LC replica mismatch {w:04x}/{w2:04x}")
            self.events.append(('lc', (w >> 7) & 0xF, w & 0xF))
        elif self._state == 'hdr':
            dws = [int.from_bytes(bytes(body[4 * k:4 * k + 4]), "little")
                   for k in range(3)]
            crc16 = body[12] | (body[13] << 8)
            lcw = body[14] | (body[15] << 8)
            seq = lcw & 0xF
            if crc16 != crc16_header(dws):
                self.errors.append(f"header CRC-16 bad (dw0={dws[0]:08x})")
            if self._kind == 'dph':
                replica = body[16] | (body[17] << 8)
                length = (dws[1] >> 16) & 0xFFFF
                if replica != length:
                    self.errors.append(
                        f"DPH length replica {replica} != length {length}")
                self._dpp_len = length
            elif (dws[0] & 0x1F) == 8:
                # SHP-framed (deferred-style) DPH: still sets the length.
                self._dpp_len = (dws[1] >> 16) & 0xFFFF
            self.events.append(('hdr', dws, seq, self._kind))
        elif self._state == 'dpp':
            payload = bytes(body[:self._dpp_len])
            crc = int.from_bytes(bytes(body[self._dpp_len:
                                            self._dpp_len + 4]), "little")
            end = tuple(body[self._dpp_len + 4:])
            crc_ok = crc == crc32_payload(payload)
            if end != DPPEND and end != DPPABORT:
                self.errors.append(f"bad DPP end framing {end}")
            self.events.append(('dpp', payload, crc_ok))

    # ── host -> device transmission ──────────────────────────────────
    async def send_syms(self, syms):
        await feed_blocks(self.ctx, self.bench, self.model_tx,
                          pack_symbol_stream(syms), self.rx, self.hm)

    async def send_lc(self, cmd, sub):
        await self.send_syms(link_command_syms(cmd, sub))

    async def send_frame(self, frame):
        """Send a Gen1-host-model frame dict as Gen2 constructs."""
        is_dp = frame["payload"] is not None
        syms = header_packet_syms(frame["dw0"], frame["dw1"], frame["dw2"],
                                  self.tx_seq,
                                  start=DPHSTART if is_dp else HPSTART)
        if is_dp:
            syms += dpp_syms(frame["payload"])
        self.tx_seq = (self.tx_seq + 1) & 0xF
        await self.send_syms(syms)

    async def expect(self, what, pred, timeout_blocks=4000, quiet=False):
        """Feed idle until an un-consumed event satisfies ``pred``."""
        waited = 0
        while True:
            self.pump()
            for i, ev in enumerate(self.events):
                if pred(ev):
                    del self.events[i]
                    return ev
            if waited >= timeout_blocks:
                if not quiet:
                    print(f"{self.tag} FAIL: timed out waiting for {what}; "
                          f"events={self.events[-8:]} "
                          f"errors={self.errors[:4]} "
                          f"notes={self.hm.notes[-10:]}")
                return None
            await feed_blocks(self.ctx, self.bench, self.model_tx,
                              [idle_block()] * 8, self.rx, self.hm)
            waited += 8


async def run_enum(ctx, bench, hm, rx, model_tx, echo=False):
    """Advertisement + SET_ADDRESS + GetDescriptor(Device) over Gen2
    framing: the modulo-16 / LCRD1+LCRD2 conformance surface; with
    ``echo``, a small bulk loopback through EP1 follows."""
    from sim_link_loopback import (frame_ack_tp, frame_out_dp,
                                   frame_status_tp)
    host = Gen2LinkHost(ctx, bench, hm, rx, model_tx)

    # ── the device's Header Sequence Number Advertisement: LGOOD_15
    # (modulo-16!), then the split 2+2 credit advertisement ──
    ev = await host.expect("LGOOD advertisement",
                           lambda e: e[0] == 'lc' and e[1] == 0b0000)
    if ev is None:
        return False
    if ev[2] != 15:
        print(f"ENUM FAIL: advertisement LGOOD_{ev[2]}; a SuperSpeedPlus "
              f"port must advertise modulo-16 (LGOOD_15) [7.2.4.1.x]")
        return False
    print("ENUM: device advertised LGOOD_15 (modulo-16)")

    credits = []
    for _ in range(4):
        ev = await host.expect("credit advertisement",
                               lambda e: e[0] == 'lc' and e[1] == 0b0001)
        if ev is None:
            return False
        credits.append(ev[2])
    lcrd1 = sorted(c & 0x3 for c in credits if not (c & 0x4))
    lcrd2 = sorted(c & 0x3 for c in credits if c & 0x4)
    print(f"ENUM: device credit advertisement LCRD1={lcrd1} LCRD2={lcrd2}")
    if lcrd1 != [0, 1] or lcrd2 != [0, 1]:
        print("ENUM FAIL: expected the split 2+2 advertisement "
              "(LCRD1_A,B + LCRD2_A,B) [Table 7-4 / 7.2.4.1.x]")
        return False

    # ── host advertisement: LGOOD_15 + 4 Type-1 + 4 Type-2 credits ──
    syms = link_command_syms(0b0000, 15)
    for i in range(4):
        syms += link_command_syms(0b0001, i)              # LCRD1_x
    if NEG != "nolcrd2":
        for i in range(4):
            syms += link_command_syms(0b0001, 0b0100 | i) # LCRD2_x
    await host.send_syms(syms)

    dev_seq = 0
    ret_idx = {1: 0, 2: 0}    # host's per-class credit-return indices

    async def return_credit(series):
        sub = (0b0100 if series == 2 else 0) | ret_idx[series]
        ret_idx[series] = (ret_idx[series] + 1) & 3
        await host.send_lc(0b0001, sub)

    # The device leads with its link-up LMPs (Port Capability); ack
    # them (Type 1) so the sequence bookkeeping stays aligned.
    while True:
        ev = await host.expect("link-up LMP",
                               lambda e: e[0] == 'hdr'
                               and (e[1][0] & 0x1F) == 0,
                               timeout_blocks=400, quiet=True)
        if ev is None:
            break
        if ev[2] != dev_seq:
            print(f"ENUM FAIL: LMP seq {ev[2]}, expected {dev_seq}")
            return False
        dev_seq = (dev_seq + 1) & 0xF
        await host.send_lc(0b0000, ev[2])
        sub = ret_idx[1]
        ret_idx[1] = (ret_idx[1] + 1) & 3
        await host.send_lc(0b0001, sub)
        print(f"ENUM: acked link-up LMP (dw0={ev[1][0]:08x})")

    async def expect_lgood(n):
        ev = await host.expect(f"LGOOD_{n}",
                               lambda e: e[0] == 'lc' and e[1] == 0b0000)
        if ev is None:
            return False
        if ev[2] != n:
            print(f"ENUM FAIL: expected LGOOD_{n}, got LGOOD_{ev[2]}")
            return False
        return True

    async def expect_lcrd(series):
        ev = await host.expect(f"LCRD{series}",
                               lambda e: e[0] == 'lc' and e[1] == 0b0001)
        if ev is None:
            return None
        got = 2 if ev[2] & 0x4 else 1
        if got != series:
            print(f"ENUM FAIL: expected an LCRD{series} return, got "
                  f"LCRD{got}_{'ABCD'[ev[2] & 3]}")
            return None
        return ev[2] & 3

    async def expect_ack_tp(step):
        nonlocal dev_seq
        ev = await host.expect(f"ACK TP ({step})",
                               lambda e: e[0] == 'hdr'
                               and (e[1][0] & 0x1F) == 4)
        if ev is None:
            return False
        if ev[2] != dev_seq:
            print(f"ENUM FAIL: device header seq {ev[2]}, expected "
                  f"{dev_seq} ({step})")
            return False
        dev_seq = (dev_seq + 1) & 0xF
        await host.send_lc(0b0000, ev[2])         # LGOOD_n
        await return_credit(1)                    # ACK TPs are Type 1
        return True

    # ── SET_ADDRESS(1): SETUP DP -> ACK TP; STATUS TP -> ACK TP ──
    setup = bytes([0x00, 0x05, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00])
    await host.send_frame(frame_out_dp(0, 0, setup, setup=1, address=0))
    if not await expect_lgood(0):
        return False
    if await expect_lcrd(2) is None:              # SETUP DP is Type 2
        return False
    if not await expect_ack_tp("SETUP ack"):
        return False
    await host.send_frame(frame_status_tp(0, address=0))
    if not await expect_lgood(1):
        return False
    if await expect_lcrd(1) is None:              # STATUS TP is Type 1
        return False
    if not await expect_ack_tp("STATUS ack"):
        return False
    print("ENUM: SET_ADDRESS complete over Gen2 framing")

    # ── GetDescriptor(DEVICE, 18) at address 1 ──
    setup = bytes([0x80, 0x06, 0x00, 0x01, 0x00, 0x00, 0x12, 0x00])
    await host.send_frame(frame_out_dp(0, 0, setup, setup=1, address=1))
    if not await expect_lgood(2):
        return False
    if await expect_lcrd(2) is None:
        return False
    if not await expect_ack_tp("GetDescriptor SETUP ack"):
        return False

    # IN token for the data stage.
    await host.send_frame(frame_ack_tp(ep=0, nseq=0, nump=1, direction=1))
    if not await expect_lgood(3):
        return False
    if await expect_lcrd(1) is None:
        return False

    ev = await host.expect("descriptor DPH",
                           lambda e: e[0] == 'hdr'
                           and (e[1][0] & 0x1F) == 8)
    if ev is None:
        return False
    if ev[3] != 'dph':
        print("ENUM FAIL: device DPH did not use DPHSTART framing with "
              "the length replica [7.2.1.1]")
        return False
    if ev[2] != dev_seq:
        print(f"ENUM FAIL: descriptor DPH seq {ev[2]}, expected {dev_seq}")
        return False
    dev_seq = (dev_seq + 1) & 0xF
    ev_dpp = await host.expect("descriptor DPP",
                               lambda e: e[0] == 'dpp')
    if ev_dpp is None:
        return False
    payload, crc_ok = ev_dpp[1], ev_dpp[2]
    print(f"ENUM: descriptor payload {payload[:8].hex()} crc_ok={crc_ok}")
    if not crc_ok:
        print("ENUM FAIL: descriptor DPP CRC-32 invalid")
        return False
    if len(payload) != 18 or payload[0] != 18 or payload[1] != 1:
        print("ENUM FAIL: not a device descriptor")
        return False
    if payload[2] != 0x10 or payload[3] != 0x03:
        print(f"ENUM FAIL: bcdUSB {payload[3]:02x}{payload[2]:02x}, "
              f"expected 0310 (SuperSpeedPlus)")
        return False
    await host.send_lc(0b0000, (dev_seq - 1) & 0xF)   # LGOOD for the DPH
    await return_credit(2)                            # DPs are Type 2

    # STATUS stage.
    await host.send_frame(frame_status_tp(0, address=1))
    if not await expect_lgood(4):
        return False
    if await expect_lcrd(1) is None:
        return False
    if not await expect_ack_tp("GetDescriptor STATUS ack"):
        return False

    if host.errors:
        print(f"ENUM FAIL: parser errors: {host.errors[:6]}")
        return False
    print("ENUM: modulo-16 sequence numbers, LCRD1/LCRD2 credit classes, "
          "DPH length replica, bcdUSB 0310 -- all verified at Gen2")

    if not echo:
        return True

    # ── small bulk echo through EP1 (Gen2 framing end to end) ──
    host.tag = "ECHO"
    payload = bytes((17 * i + 3) & 0xFF for i in range(64))
    await host.send_frame(frame_out_dp(1, 0, payload, address=1))
    if not await expect_lgood(5):
        return False
    if await expect_lcrd(2) is None:
        return False
    ev = await host.expect("OUT ACK TP",
                           lambda e: e[0] == 'hdr'
                           and (e[1][0] & 0x1F) == 4)
    if ev is None:
        return False
    dev_seq = (dev_seq + 1) & 0xF
    await host.send_lc(0b0000, ev[2])
    await return_credit(1)

    # IN token: the device echoes the payload back.
    await host.send_frame(frame_ack_tp(ep=1, nseq=0, nump=1, direction=1))
    if not await expect_lgood(6):
        return False
    if await expect_lcrd(1) is None:
        return False
    ev = await host.expect("echo DPH",
                           lambda e: e[0] == 'hdr'
                           and (e[1][0] & 0x1F) == 8)
    if ev is None:
        return False
    if ev[3] != 'dph':
        print("ECHO FAIL: echoed DPH lacks DPHSTART framing")
        return False
    ev_dpp = await host.expect("echo DPP", lambda e: e[0] == 'dpp')
    if ev_dpp is None:
        return False
    if not ev_dpp[2]:
        print("ECHO FAIL: echoed DPP CRC-32 invalid")
        return False
    if ev_dpp[1] != payload:
        print(f"ECHO FAIL: payload mismatch "
              f"({ev_dpp[1][:8].hex()} != {payload[:8].hex()})")
        return False
    if host.errors:
        print(f"ECHO FAIL: parser errors: {host.errors[:6]}")
        return False
    print(f"ECHO: {len(payload)} bytes OUT and IN through Gen2 framing, "
          f"sha-exact, CRC-32 valid")
    return True


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
        elif PHASE in ("enum", "echo"):
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
