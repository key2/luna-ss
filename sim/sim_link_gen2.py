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
``lbpm-x2`` (run with DEVCAP=gen1x2) the width-program W0.3 arm: the
           host announces Gen 2x2 (0x44); a Gen 1x2-highest device
           must hold its 0x40 dual-lane announcement (the higher
           host adjusts down, Table 7-14), match at Gen 1x2, run
           the PHY Ready handshake and configure the 5G rate.
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
``u0``     ``train`` + the sim-uncovered REAL-host U0 behaviors
           (HANDOVER 10s suspects 1-3), STRICT:
           - the device's link-up Port Capability LMP must carry the
             SSP reserved-zero field rules (link_speed=0,
             num_hp_buffers=0 when not operating at Gen 1x1)
             [8.4.5, Table 8-7];
           - inbound host Port Capability + Port Configuration LMPs
             (link_speed=0 at SSP [Table 8-9]); the device must
             answer Port Configuration with a Port Configuration
             Response whose Response Code is reserved-0 at SSP (a
             nonzero code reads as REJECTED at the DFP -> port error
             [Table 8-10, 10.16.2.6]);
           - inbound ITPs (broadcast; link-level ack only, no
             protocol response [8.7]);
           - LUP keepalives while idle in U0 (tU0LTimeout = 10 us
             [7.5.6.1]);
           then a SET_ADDRESS to prove the link survived it all.

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

from amaranth import (ClockDomain, ClockSignal, Elaboratable, Module,
                      ResetSignal, Signal)
from amaranth.sim import Simulator

from luna.gateware.interface.pipe import PIPEInterface
from luna.gateware.usb.usb3.device import USBSuperSpeedDevice
from luna.gateware.usb.usb3.descriptors import add_superspeedplus_bos
from usb_protocol.emitters import SuperSpeedDeviceDescriptorCollection
from usb_protocol.types import USBTransferType

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
# Device advertised-highest capability (width program W0.3):
# DEVCAP=gen1x2 builds the DUT with ssp_capability=LBPM_CAP_GEN1X2.
DEVCAP = os.environ.get("DEVCAP", "")

# ss clock: 156.25 MHz (the Gen2 operating point)
# Width program (usb3_design.md 13.5, session 19): ``W128=1`` runs the
# whole bench at core_width=128 -- the 128-bit one-beat-per-block PIPE
# contract at the 78.125 MHz core clock.  The RTL scrambler/descrambler
# conditioning (64-bit gw_usb3 units, one sub-beat per core cycle
# impossible in a single domain) is bypassed: blocks move CLEAR both
# ways and the python ScramblerModel round-trip is skipped -- the PHY
# conditioning is validated by the W64 fences and the PHY's own suite.
W128 = int(os.environ.get("W128", "0") or "0")

CLK = 78.125e6 if W128 else 156.25e6
US = int(CLK / 1e6)              # cycles per microsecond (156 / 78)

# LBPM constants [USB 3.2r1 6.9.5, Tables 6-33 / 7-13]
TPWM_US = 2.2
LBPM_CAP_GEN2X1 = 0x04           # PHY Capability, [3:2]=01: 10 Gbps
LBPM_CAP_GEN1X1 = 0x00           # PHY Capability, [3:2]=00: 5 Gbps
# Dual-lane capabilities: b6 = dual-lane [Table 7-13].  NOTE the
# session-14 mission text / usb3_design.md 5 said 0x20 -- that is b5,
# a RESERVED bit; the spec table (b0..b7 columns) puts dual-lane at b6
# = 0x40.  Corrected here and in physical/lfps.py.
LBPM_CAP_GEN1X2 = 0x40           # b6=1, rate 00: two 5 Gbps lanes
LBPM_CAP_GEN2X2 = 0x44           # b6=1, rate 01: two 10 Gbps lanes
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
    # bcdUSB 0310 requires the SuperSpeedPlus device capability in the
    # BOS [9.6.2.5]; the default (USB2 ext + SS cap only) draws a
    # bench-host complaint and under-describes the Gen2 sublinks.
    add_superspeedplus_bos(d)
    return d


class BenchPIPE(PIPEInterface, Elaboratable):
    """Bare PIPE (64-bit, or the 128-bit W128 contract): all signals
    driven/observed by the testbench."""

    def __init__(self):
        super().__init__(width=16 if W128 else 8)
        # Gen2 closed-loop TX pacing reference (bug #44): the PHY TX
        # gearbox FIFO occupancy.  Driven by HostRx's python FIFO model
        # so the sims exercise the same loop the silicon runs.
        self.tx_fifo_occupancy = Signal(5)

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
        if DEVCAP == "gen1x2":
            kwargs["ssp_capability"] = LBPM_CAP_GEN1X2
        usb = USBSuperSpeedDevice(phy=self.pipe, sync_frequency=CLK,
                                  gen2=True,
                                  core_width=128 if W128 else 64,
                                  **kwargs)
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
            usb.add_endpoint(out_ep,
                             endpoint_types={0x01: USBTransferType.BULK})
            usb.add_endpoint(in_ep,
                             endpoint_types={0x81: USBTransferType.BULK})
            m.d.comb += in_ep.stream.stream_eq(out_ep.stream)

        m.submodules.usb = self.usb = usb

        if not W128:
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
        # (W128: the testbench drives pipe.rx_* directly with clear
        # blocks and reads pipe.tx_* directly; see feed_blocks and
        # HostRx.sample.)
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
            # Device-initiated recovery causes (the #49 wedge hunt: the
            # bench per-cause counters read ZERO through the failure
            # window -- the sim must show the same silence or name the
            # cause).
            if ctx.get(usb.debug_recovery_timers):
                self.notes.append(("rec_timers", self.cyc))
            if ctx.get(usb.debug_recovery_rx):
                self.notes.append(("rec_rx", self.cyc))
            if ctx.get(usb.debug_recovery_tx):
                self.notes.append(("rec_tx", self.cyc))
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


async def phase_lbpm_x2(ctx, bench):
    """Gen 1x2 PortMatch trace (W0.3, usb3_design.md P0/5): the host
    announces Gen 2x2 (0x44 -- the bench 20G root port's true highest);
    a device built with ``ssp_capability=LBPM_CAP_GEN1X2`` must hold
    its Gen 1x2 announcement (the host, higher, adjusts down per Table
    7-14: UFP Gen 1x2 x DFP Gen 2x2 -> Gen 1x2), match at 0x40, run
    the PHY Ready handshake, and configure the 5G rate (both lanes are
    Gen 1).  RED against a Gen 2x1-highest device: it announces 0x04
    and never 0x40."""
    tag = "LBPM-X2"
    pipe = bench.pipe
    await bringup(ctx, pipe)
    hm = HostModem(ctx, bench)

    ok, diag = await hm.scd_exchange()
    if not ok:
        print(f"{tag} FAIL: SCD stage: {diag}")
        return False
    print(f"{tag}: SCD1+SCD2 exchange complete")

    # ── PortMatch: host announces Gen 2x2; wait for the device's
    # announcement, then adjust down to it like a real higher port ──
    mark = hm.cyc
    await hm.send_lbpm(LBPM_CAP_GEN2X2, count=6)
    msgs = [v for (_, v) in hm.lbpm_messages(mark)]
    print(f"{tag}: device LBPMs vs our Gen 2x2: {[hex(v) for v in msgs]}")
    caps = [v for v in msgs if (v & 0x3) == 0]
    if not caps:
        print(f"{tag} FAIL: no PHY Capability LBPM from device")
        return False
    dev_cap = caps[-1]
    if dev_cap != LBPM_CAP_GEN1X2:
        print(f"{tag} FAIL: device announced {dev_cap:#04x}, expected the "
              f"Gen 1x2 dual-lane capability ({LBPM_CAP_GEN1X2:#04x}) "
              f"[Table 7-13 b6]")
        return False

    # Adjust down to the device's Gen 1x2 (Table 7-14 start-up match).
    mark = hm.cyc
    await hm.send_lbpm(LBPM_CAP_GEN1X2, count=10)
    msgs = [v for (_, v) in hm.lbpm_messages(mark)]
    print(f"{tag}: device LBPMs after our adjust-down: "
          f"{[hex(v) for v in msgs]}")
    matched = [v for v in msgs if v == LBPM_CAP_GEN1X2]
    if len(matched) < 4:
        print(f"{tag} FAIL: expected >=4 matched Gen 1x2 capability LBPMs, "
              f"got {len(matched)}")
        return False

    # ── PortConfig: PHY Ready handshake ──
    mark = hm.cyc
    await hm.send_lbpm(LBPM_PHY_READY, count=12)
    msgs = [v for (_, v) in hm.lbpm_messages(mark)]
    print(f"{tag}: device LBPMs during PortConfig: {[hex(v) for v in msgs]}")
    ready = [v for v in msgs if v == LBPM_PHY_READY]
    if len(ready) < 2:
        print(f"{tag} FAIL: expected >=2 PHY Ready LBPMs, got {len(ready)}")
        return False

    # ── rate outcome: Gen 1x2 is a 5G configuration ──
    final_rate = ctx.get(pipe.rate)
    print(f"{tag}: rate changes {hm.rate_changes}; "
          f"final pipe.rate={final_rate}")
    if final_rate != 0:
        print(f"{tag} FAIL: Gen 1x2 outcome but pipe.rate never switched "
              f"to the 5G trim")
        return False

    if not await check_training_entry(ctx, bench, hm, tag):
        return False
    print(f"{tag}: Gen 1x2 matched (0x40), PHY Ready handshake complete, "
          f"5G configured -- the x2 negotiation surface works")
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
        # PHY TX gearbox FIFO model (gw_usb3 phy.py ``tx_fifo``, 32
        # deep): fills on every MAC tx_datavalid beat at the 10G trim
        # and drains through the REAL TxGearbox132 consumption law
        # (session 17, the #49 txfifo-hi28 hunt -- the historical
        # flat 32-per-33 approximation hid the boundary dynamics):
        #   - the FIFO read side is ``RdEn = S_READY & ~empty_r`` with
        #     ``empty_r`` REGISTERED (one cycle stale);
        #   - the gearbox accepts 64 wire bits per beat plus 4 sync-
        #     header bits on start_block beats, and emits 64 bits per
        #     cycle while primed: one dead read cycle whenever the
        #     residue exceeds 64 (once per 16 two-beat blocks);
        #   - from empty (UNDERFLOW) the residue restarts at zero.
        # On silicon an overflow silently corrupts the wire stream --
        # and so does an UNDERFLOW while the wire is mid-stream (bug
        # #44: the gearbox serializes stale bits when starved), so the
        # sim fails hard on either.  The model's level feeds the DUT's
        # closed pacing loop (pipe.tx_fifo_occupancy), exactly like
        # TxFifoWrNum on silicon.  ``fifo_hi28`` mirrors the bench
        # txfifo-hi28 probe (cycles at level >= 28; the #49 canary
        # fires ~71k/s on silicon during the enumeration window).
        self.fifo_level    = 0
        self.fifo_max      = 0
        self.fifo_cyc      = 0
        self.fifo_overflow = False
        self.fifo_armed    = False   # prefill reached once
        self.fifo_starved  = 0       # drain-eligible cycles at level 0
                                     # after prefill (wire starvation)
        self.fifo_hi28     = 0       # cycles at level >= 28 (bench canary)
        self._fifo_q       = []      # start_block flag per buffered beat
        self._gb_active    = False   # gearbox primed (ACTIVE state)
        self._gb_bits      = 0       # gearbox residue above the 64/cycle
        self._empty_r      = True    # registered FIFO empty (1 stale cycle)

    def sample(self, ctx):
        if W128:
            return self._sample_w128(ctx)
        pipe = self.bench.pipe
        self.fifo_cyc += 1
        # ── FIFO write side (MAC supply) ──
        if ctx.get(pipe.tx_datavalid) and ctx.get(pipe.rate) == 1:
            self.fifo_level += 1
            self._fifo_q.append(bool(ctx.get(pipe.tx_start_block)))
        # ── FIFO read side + gearbox drain (the real law) ──
        ready = (not self._gb_active) or (self._gb_bits <= 64)
        rd = ready and not self._empty_r and self.fifo_level > 0
        self._empty_r = (self.fifo_level == 0)
        if rd:
            start = self._fifo_q.pop(0)
            self.fifo_level -= 1
            self._gb_bits += 68 if start else 64
            self._gb_active = True
        if self._gb_active:
            self._gb_bits -= 64
            if self._gb_bits < 0:
                # The wire consumed bits the MAC never supplied: the
                # gearbox serializes stale bits (bug #44 starvation).
                self._gb_bits = 0
                self._gb_active = False
                if self.fifo_armed:
                    self.fifo_starved += 1
        if self.fifo_level >= 8:
            self.fifo_armed = True
        if self.fifo_level > self.fifo_max:
            self.fifo_max = self.fifo_level
        if self.fifo_level >= 28:
            self.fifo_hi28 += 1
        if self.fifo_level > 32:
            self.fifo_overflow = True
        ctx.set(pipe.tx_fifo_occupancy, min(self.fifo_level, 31))
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

    def _sample_w128(self, ctx):
        """The 128-bit contract sampler: one beat = one whole block
        (a halfbeat = the SKP OS tail, symbols 16-23 in the top
        lanes).  The PHY FIFO model works in 64-bit pclk words: a full
        beat supplies 2 (the first with the 68-bit start), a halfbeat
        1; the gearbox drain law runs TWICE per core cycle (pclk =
        2x core).  Data moves CLEAR (no scrambler round-trip)."""
        pipe = self.bench.pipe
        self.fifo_cyc += 1
        # ── FIFO write side ──
        halfbeat = False
        if ctx.get(pipe.tx_datavalid) and ctx.get(pipe.rate) == 1:
            halfbeat = bool(ctx.get(pipe.tx_halfbeat))
            if halfbeat:
                self.fifo_level += 1
                self._fifo_q.append(False)
            else:
                self.fifo_level += 2
                self._fifo_q.append(bool(ctx.get(pipe.tx_start_block)))
                self._fifo_q.append(False)
        # ── drain law, twice per core cycle ──
        for _ in range(2):
            ready = (not self._gb_active) or (self._gb_bits <= 64)
            rd = ready and not self._empty_r and self.fifo_level > 0
            self._empty_r = (self.fifo_level == 0)
            if rd:
                start = self._fifo_q.pop(0)
                self.fifo_level -= 1
                self._gb_bits += 68 if start else 64
                self._gb_active = True
            if self._gb_active:
                self._gb_bits -= 64
                if self._gb_bits < 0:
                    self._gb_bits = 0
                    self._gb_active = False
                    if self.fifo_armed:
                        self.fifo_starved += 1
        if self.fifo_level >= 8:
            self.fifo_armed = True
        if self.fifo_level > self.fifo_max:
            self.fifo_max = self.fifo_level
        if self.fifo_level >= 28:
            self.fifo_hi28 += 1
        if self.fifo_level > 32:
            self.fifo_overflow = True
        ctx.set(pipe.tx_fifo_occupancy, min(self.fifo_level, 31))

        # ── block collection (clear data straight off the PIPE) ──
        if not ctx.get(pipe.tx_datavalid):
            return
        d = ctx.get(pipe.tx_data)
        hi, lo = (d >> 64) & (2**64 - 1), d & (2**64 - 1)
        if halfbeat:
            # SKP OS tail: symbols 16-23 append to the open block.
            if self._cur is not None:
                h0, syms = self._cur
                self._cur = (h0, syms + beats_to_syms([hi]))
            return
        h = ctx.get(pipe.tx_sync_header)
        if self._cur:
            self.blocks.append(self._cur)
        self._cur = (h, beats_to_syms([hi, lo]))

    def block_count(self, head, first_sym):
        n = 0
        for h, syms in self.blocks:
            if h == head and syms and syms[0] == first_sym:
                n += 1
        return n


async def feed_blocks(ctx, bench, model_tx, blocks, rx=None, hm=None):
    """Scramble blocks with the python model and push them through the
    RTL descrambler into the DUT, one beat per cycle.

    SKP OS handling mirrors the real RX datapath: the RTL descrambler
    reseeds its LFSR from ``descrambler_init`` on SKP blocks, which the
    silicon feeds from RxGearbox132's ``next_lfsr`` extraction of the
    SKP-carried seed [Table 6-13].  The bench emulates that extraction
    here from the spliced wire beat (session 13: without it the
    descrambler reseeds from zero and everything after the first SKP
    descrambles to garbage -- a bench-model gap, not a stack bug)."""
    if W128:
        # One CLEAR beat per block on the 128-bit contract.  A 24-symbol
        # SKP OS (3 narrow beats) becomes a start beat (16 syms) plus a
        # startless tail beat carrying symbols 16-23 in the TOP lanes
        # (the wide receiver's assembly ignores startless beats, exactly
        # as the narrow one ignores the third SKP beat).
        pipe = bench.pipe
        for blk in blocks:
            beats = list(blk.beats())
            (s0, h0, d0) = beats[0]
            d1 = beats[1][2] if len(beats) > 1 else 0
            ctx.set(pipe.rx_datavalid, 1)
            ctx.set(pipe.rx_start_block, 1)
            ctx.set(pipe.rx_sync_header, h0)
            ctx.set(pipe.rx_data, (d0 << 64) | d1)
            await ctx.tick("ss")
            if rx:
                rx.sample(ctx)
            if hm:
                hm.cyc += 1
                hm._observe()
            for (s2, h2, d2) in beats[2:]:
                ctx.set(pipe.rx_start_block, 0)
                ctx.set(pipe.rx_data, (d2 << 64)
                        | int.from_bytes(bytes([IDLE_SYM] * 8), "big"))
                await ctx.tick("ss")
                if rx:
                    rx.sample(ctx)
                if hm:
                    hm.cyc += 1
                    hm._observe()
        ctx.set(pipe.rx_datavalid, 0)
        return

    descr = bench.host_descr
    skp_left = 0
    for blk in blocks:
        for (s, h, d) in blk.beats():
            wire = model_tx.feed(s, h, d)
            if s and h == BLOCK_CONTROL and ((d >> 56) & 0xFF) in \
                    (int(BlockType.SKP), int(BlockType.SKPEND)):
                skp_left = 2          # two continuation beats follow
            elif skp_left:
                skp_left -= 1
                if skp_left == 0:
                    ctx.set(descr.descrambler_init, wire & 0xFFFFFF)
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


async def phase_train(ctx, bench, continue_to_enum=False, u0_checks=False,
                      hot_reset=False, recovery=False, advearly=False,
                      reccut=False):
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

    # TS2 handshake (SKP OS interleaved, as a real partner would)
    for _ in range(6):
        await feed_blocks(ctx, bench, model_tx,
                          [sync_block()] + [ts2_block()] * 8
                          + [skp_block()] + [ts2_block()] * 8, rx, hm)
        if rx.block_count(BLOCK_CONTROL, int(BlockType.TS2)) >= 8:
            break
    n_ts2 = rx.block_count(BLOCK_CONTROL, int(BlockType.TS2))
    if n_ts2 < 8:
        print(f"TRAIN FAIL: only {n_ts2} TS2 blocks from device")
        return False

    # SDS -> Idle [7.5.4.10]: a single SDS, then data blocks carrying
    # Idle Symbols (5Ah at Gen2!).  SKP OS are interleaved like a real
    # link partner's (one per ~40 blocks; session-13 bench delta: the
    # sim host historically never sent SKPs, hiding any SKP-adjacency
    # sensitivity in the SDS/idle handshake window).
    await feed_blocks(ctx, bench, model_tx,
                      [skp_block(), sds_block()]
                      + [idle_block()] * 20 + [skp_block()]
                      + [idle_block()] * 20 + [skp_block()]
                      + [idle_block()] * 8, rx, hm)
    got_sds = any(h == BLOCK_CONTROL and s[0] == 0xE1
                  for h, s in rx.blocks)
    got_idle = any(h == BLOCK_DATA and all(x == IDLE_SYM for x in s)
                   for h, s in rx.blocks)
    if not (got_sds and got_idle):
        print(f"TRAIN FAIL: SDS={got_sds} idle={got_idle} from device")
        return False
    print(f"TRAIN: PHY TX FIFO model max occupancy {rx.fifo_max}/32, "
          f"starved {rx.fifo_starved}")
    if rx.fifo_overflow:
        print("TRAIN FAIL: MAC tx_datavalid overran the PHY's 32-deep "
              "TX gearbox FIFO (no Gen2 beat pacing)")
        return False
    # Prefill accrues at the 132/128 overhead rate (~1 word per 16.5
    # blocks); the short TSEQ_LEN=64 training run at W128 cannot reach
    # the 8-word arming level within its block budget -- require the
    # prefill only when enough words were actually supplied.  (The
    # sustained enum/echo phases stream far past this bound and keep
    # the full band assertions.)
    prefill_expected = rx.fifo_cyc >= (16 * 33 * (1 if not W128 else 1))
    if (not rx.fifo_armed and rx.fifo_max >= 8) or rx.fifo_starved \
            or (not rx.fifo_armed and prefill_expected
                and rx.fifo_max < 8):
        print("TRAIN FAIL: PHY TX FIFO ran at the underflow boundary "
              f"(prefill={rx.fifo_armed} starved={rx.fifo_starved} "
              f"max={rx.fifo_max}); "
              "the gearbox serializes stale bits when starved mid-"
              "stream -- closed-loop pacing must hold a cushion "
              "(bug #44)")
        return False
    print("TRAIN: U0 data stream established at Gen2 framing")

    if u0_checks:
        return await run_u0_checks(ctx, bench, hm, rx, model_tx)
    if hot_reset:
        return await run_hotreset(ctx, bench, hm, rx, model_tx,
                                  parked=(PHASE == "hotreset-parked"))
    if recovery:
        return await run_recovery(ctx, bench, hm, rx, model_tx)
    if reccut:
        return await run_reccut(ctx, bench, hm, rx, model_tx)
    if advearly:
        return await run_advearly(ctx, bench, hm, rx, model_tx)
    if not continue_to_enum:
        return True
    return await run_enum(ctx, bench, hm, rx, model_tx,
                          echo=(PHASE == "echo"))


class Gen2LinkHost:
    """Symbol-level Gen2 link partner: parses the device's data-block
    symbol stream (through HostRx) into link commands, header packets
    (validating the DPHSTART length replica) and DPPs, and builds the
    host's transmissions."""

    # Native SSP TT: control EP0, declared bulk EP1 (both directions).
    _tt_by_ep = {0: 0b100, 1: 0b110}

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
        self._dph_pending = False  # DPH parsed; its DPP must follow
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
            else:
                # STRICT host rule [6.4.3.3]: "SKP Ordered Sets shall
                # not be inserted within any packet."  A control block
                # arriving while a construct is partially parsed means
                # the device split a packet (session-13 bench finding:
                # the real xHC rejects the DP -> descriptor read
                # error -71 -> retrain loop; the forgiving bench host
                # hid it).
                self._walk()
                mid = (self._state != 'search' or self._dph_pending
                       or any(x != G2_IDL for x in self._syms))
                if mid and syms and syms[0] != 0xFF and syms[0] != 0x00:
                    self.errors.append(
                        f"control block (first sym {syms[0]:#04x}) "
                        f"inside a packet [6.4.3.3]")
        self._walk()

    def _walk(self):
        s = self._syms
        i = 0
        n = len(s)
        while True:
            if self._state == 'search':
                while i < n and s[i] == G2_IDL:
                    if self._dph_pending:
                        # STRICT [7.2.1.2.3]: "There shall be no
                        # spacing between a DPH and its corresponding
                        # DPP."
                        self.errors.append(
                            "spacing between DPH and DPP [7.2.1.2.3]")
                        self._dph_pending = False
                    i += 1
                if i >= n:
                    break
                if n - i < 4:
                    break
                frame = tuple(s[i:i + 4])
                if self._dph_pending and frame != DPPSTART:
                    self.errors.append(
                        f"DPH followed by {'/'.join(hex(x) for x in frame)}"
                        f" instead of its DPP [7.2.1.2.3]")
                self._dph_pending = False
                if frame == HPSTART:
                    self._state, self._need = 'hdr', 20 - 4
                    self._kind = 'hp'
                elif frame == DPHSTART:
                    # non-deferred Gen2 DPH: 24 bytes -- framing + 12B
                    # header + CRC-16 + LCW + TWO length replicas
                    # [7.2.1.1 Figure 7-4].
                    self._state, self._need = 'hdr', 24 - 4
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
                # An aborted DPP carries NO payload: DPPSTART is followed
                # immediately by the EDB EDB EDB EPF abort framing (the
                # DL=1 retransmission of a consumed-payload DP; bug #51
                # surface).  Recognize it before demanding payload-length
                # symbols.
                if self._state == 'dpp' and n - i >= 4 \
                        and tuple(s[i:i + 4]) == DPPABORT:
                    self.events.append(('dpp', b'', False, True))
                    if VERBOSE:
                        print(f"    [{self.tag} ev] {self.events[-1]}")
                    i += 4
                    self._state = 'search'
                    continue
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
            packet_type = dws[0] & 0x1F
            if packet_type == 8 or (packet_type == 4
                                    and (dws[1] & 0xF) == 1):
                # TT exists only in DP/ACK, not NRDY/ERDY/STALL.
                ep = (dws[1] >> 8) & 0xF
                tt = (dws[1] >> 12) & 0x7
                expected_tt = self._tt_by_ep.get(ep)
                if expected_tt is not None and tt != expected_tt:
                    self.errors.append(
                        f"native SSP device "
                        f"{'DPH' if packet_type == 8 else 'ACK'} EP{ep} "
                        f"TT={tt:03b}, expected {expected_tt:03b} "
                        f"(DW1=0x{dws[1]:08x}; Table 8-13 p264, bug #56)")
            if self._kind == 'dph':
                # STRICT [7.2.1.1 Figure 7-4, 7.2.4.1.6]: TWO length
                # replicas follow the LCW; a real xHC validates both
                # ("the two length field replica are valid and
                # identical" -- a mismatch is a Recovery condition).
                replica = body[16] | (body[17] << 8)
                replica2 = body[18] | (body[19] << 8)
                length = (dws[1] >> 16) & 0xFFFF
                if replica != length or replica2 != length:
                    self.errors.append(
                        f"DPH length replicas {replica}/{replica2} != "
                        f"length {length} (the 24-byte Figure 7-4 "
                        f"format; bug #48)")
                self._dpp_len = length
                self._dph_pending = True
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
            self.events.append(('dpp', payload, crc_ok, end == DPPABORT))
        if VERBOSE and self.events:
            print(f"    [{self.tag} ev] {self.events[-1]}")

    # ── host -> device transmission ──────────────────────────────────
    async def send_syms(self, syms):
        await feed_blocks(self.ctx, self.bench, self.model_tx,
                          pack_symbol_stream(syms), self.rx, self.hm)

    async def send_lc(self, cmd, sub):
        await self.send_syms(link_command_syms(cmd, sub))

    async def send_frame(self, frame, *, seq=None):
        """Send a Gen1 frame as Gen2; explicit seq preserves retry numbering."""
        packet_type = frame["dw0"] & 0x1F
        dw1 = frame["dw1"]
        ep = (dw1 >> 8) & 0xF
        if packet_type in (4, 8) and ep == 0:
            # Control direction is zero, including IN polls [8.12.2].
            dw1 &= ~(1 << 7)
        if packet_type == 8 or (packet_type == 4 and (dw1 & 0xF) == 1):
            # Replace Gen1 reserved-zero TT before regenerating CRC-16.
            dw1 = (dw1 & ~(0x7 << 12)) | (self._tt_by_ep[ep] << 12)
        if seq is None:
            seq = self.tx_seq
            self.tx_seq = (self.tx_seq + 1) & 0xF
        is_dp = frame["payload"] is not None
        syms = header_packet_syms(frame["dw0"], dw1, frame["dw2"], seq,
                                  start=DPHSTART if is_dp else HPSTART)
        if is_dp:
            syms += dpp_syms(frame["payload"])
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

    # STRICT credit advertisement [7.2.4.1.1]: "If a port enters U0 from
    # Polling or Hot Reset, its Local Type 1/Type 2 Rx Buffer Credit
    # Count is 4" (rule 2.e.1) -- so the advertisement SHALL be
    # LCRD1_A..D and LCRD2_A..D (rule 3.d).  A real host arms its Type
    # 1/Type 2 CREDIT_HP_TIMERs at U0 entry; they only clear at count 4
    # (Gen 2x1) and their timeout forces Recovery [7.3.9] -- a shorter
    # advertisement walks the link down (bug #42's silicon signature:
    # the host never transmits a single header packet).  Like a
    # conformant host, we send NO header packets until it completes.
    credits = []
    for _ in range(8):
        ev = await host.expect(
            "credit advertisement (Type 1/2 CREDIT_HP_TIMER pending)",
            lambda e: e[0] == 'lc' and e[1] == 0b0001)
        if ev is None:
            print("ENUM FAIL: Type 1/Type 2 CREDIT_HP_TIMER would expire "
                  "-> Recovery [7.2.4.1.1 rule 2.e.1, 7.3.9]: a port "
                  "entering U0 from Polling shall advertise 4 credits "
                  "per class at Gen 2x1")
            return False
        credits.append(ev[2])
    lcrd1 = [c & 0x3 for c in credits if not (c & 0x4)]
    lcrd2 = [c & 0x3 for c in credits if c & 0x4]
    print(f"ENUM: device credit advertisement LCRD1={lcrd1} LCRD2={lcrd2}")
    if lcrd1 != [0, 1, 2, 3] or lcrd2 != [0, 1, 2, 3]:
        print("ENUM FAIL: expected the full 4+4 advertisement in "
              "alphabetical order (LCRD1_A..D + LCRD2_A..D) "
              "[7.2.4.1.1 rules 2.e.1 + 3.d, 7.2.4.1.2]")
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

    # ── the bench xHC's descriptor ladder (bug #48 tail; session 16):
    # after the 18-byte device descriptor the real host reads BOS at
    # wLength=5 (header), then the FULL BOS at wLength=22 -- the FIRST
    # transfer that died with EPROTO -71 on silicon -- then the config
    # descriptor at wLength=9.  Replicated verbatim, with data-stage
    # length checks. ──
    hseq = 5

    async def control_in(tag, w_value, w_length, want_len):
        nonlocal dev_seq, hseq
        setup = bytes([0x80, 0x06, w_value & 0xFF, w_value >> 8,
                       0x00, 0x00, w_length & 0xFF, w_length >> 8])
        await host.send_frame(frame_out_dp(0, 0, setup, setup=1,
                                           address=1))
        if not await expect_lgood(hseq):
            return None
        hseq = (hseq + 1) & 0xF
        if await expect_lcrd(2) is None:
            return None
        if not await expect_ack_tp(f"{tag} SETUP ack"):
            return None
        await host.send_frame(frame_ack_tp(ep=0, nseq=0, nump=1,
                                           direction=1))
        if not await expect_lgood(hseq):
            return None
        hseq = (hseq + 1) & 0xF
        if await expect_lcrd(1) is None:
            return None
        ev = await host.expect(f"{tag} DPH",
                               lambda e: e[0] == 'hdr'
                               and (e[1][0] & 0x1F) == 8)
        if ev is None:
            return None
        if ev[3] != 'dph':
            print(f"ENUM FAIL: {tag} DPH not DPHSTART-framed")
            return None
        if ev[2] != dev_seq:
            print(f"ENUM FAIL: {tag} DPH seq {ev[2]} != {dev_seq}")
            return None
        dev_seq = (dev_seq + 1) & 0xF
        ev_dpp = await host.expect(f"{tag} DPP", lambda e: e[0] == 'dpp')
        if ev_dpp is None:
            return None
        payload, crc_ok = ev_dpp[1], ev_dpp[2]
        if not crc_ok:
            print(f"ENUM FAIL: {tag} DPP CRC-32 invalid")
            return None
        if len(payload) != want_len:
            print(f"ENUM FAIL: {tag} data stage {len(payload)} bytes, "
                  f"expected {want_len}")
            return None
        await host.send_lc(0b0000, (dev_seq - 1) & 0xF)
        await return_credit(2)
        await host.send_frame(frame_status_tp(0, address=1))
        if not await expect_lgood(hseq):
            return None
        hseq = (hseq + 1) & 0xF
        if await expect_lcrd(1) is None:
            return None
        if not await expect_ack_tp(f"{tag} STATUS ack"):
            return None
        return payload

    bos5 = await control_in("BOS/5", 0x0f00, 5, 5)
    if bos5 is None:
        return False
    total = bos5[2] | (bos5[3] << 8)
    print(f"ENUM: BOS header {bos5.hex()} (wTotalLength={total})")
    bos_full = await control_in("BOS/full", 0x0f00, total, total)
    if bos_full is None:
        print(f"ENUM FAIL: the full-BOS control read died (the exact "
              f"silicon #48-tail shape: wLength={total})")
        return False
    print(f"ENUM: full BOS ({total} bytes) {bos_full.hex()}")

    # A bcdUSB-0310 device must carry the SuperSpeedPlus device
    # capability [9.6.2.5] -- the bench host complains without it
    # (the #49-adjacent enum-surface gap, session 17).  Walk the BOS
    # subordinates and demand a type-0x0A capability whose sublink
    # speed attributes include a 10 Gb/s SSP entry (LSE=3, LSM=10,
    # LP=SSP).
    ssp_cap = None
    off = 5
    while off + 2 <= len(bos_full):
        blen = bos_full[off]
        if blen < 3 or off + blen > len(bos_full):
            break
        if bos_full[off + 1] == 0x10 and bos_full[off + 2] == 0x0A:
            ssp_cap = bos_full[off:off + blen]
        off += blen
    if ssp_cap is None:
        print("ENUM FAIL: BOS carries no SuperSpeedPlus device "
              "capability (required at bcdUSB 0310 [9.6.2.5])")
        return False
    ssac = (ssp_cap[4] & 0x1F) + 1
    attrs = [int.from_bytes(ssp_cap[12 + 4 * k:16 + 4 * k], 'little')
             for k in range(ssac)]
    has_10g_ssp = any((((a >> 4) & 3) == 3) and ((a >> 16) == 10)
                      and (((a >> 14) & 3) == 1) for a in attrs)
    if not has_10g_ssp:
        print(f"ENUM FAIL: SSP capability lacks a 10 Gb/s SSP sublink "
              f"speed attribute (attrs: {[hex(a) for a in attrs]})")
        return False
    print(f"ENUM: SSP device capability present "
          f"({ssac} sublink attrs: {[hex(a) for a in attrs]})")
    cfg9 = await control_in("Config/9", 0x0200, 9, 9)
    if cfg9 is None:
        return False
    print(f"ENUM: config header {cfg9.hex()}")

    if host.errors:
        print(f"ENUM FAIL: parser errors: {host.errors[:6]}")
        return False
    print("ENUM: modulo-16 sequence numbers, LCRD1/LCRD2 credit classes, "
          "DPH length replica, bcdUSB 0310, BOS 5/full + config-9 reads "
          "-- all verified at Gen2")

    if not echo:
        print(f"ENUM: PHY TX FIFO model max occupancy {rx.fifo_max}/32, "
              f"starved {rx.fifo_starved}, hi28 cycles {rx.fifo_hi28}")
        if rx.fifo_overflow or not rx.fifo_armed or rx.fifo_starved:
            print("ENUM FAIL: PHY TX FIFO left the near-full pacing band "
                  f"(overflow={rx.fifo_overflow} prefill={rx.fifo_armed} "
                  f"starved={rx.fifo_starved}) (bug #44)")
            return False
        if rx.fifo_hi28:
            print(f"ENUM FAIL: PHY TX FIFO overshot the pacing band "
                  f"(level >= 28 for {rx.fifo_hi28} cycles, max "
                  f"{rx.fifo_max} -- the silicon txfifo-hi28 canary, "
                  f"bug #49 lead (a))")
            return False
        return True

    # ── small bulk echo through EP1 (Gen2 framing end to end) ──
    host.tag = "ECHO"
    payload = bytes((17 * i + 3) & 0xFF for i in range(64))
    await host.send_frame(frame_out_dp(1, 0, payload, address=1))
    if not await expect_lgood(hseq):
        return False
    hseq = (hseq + 1) & 0xF
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
    if not await expect_lgood(hseq):
        return False
    hseq = (hseq + 1) & 0xF
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
    print(f"ECHO: PHY TX FIFO model max occupancy {rx.fifo_max}/32, "
          f"starved {rx.fifo_starved}")
    if rx.fifo_overflow or not rx.fifo_armed or rx.fifo_starved:
        print("ECHO FAIL: PHY TX FIFO left the near-full pacing band "
              f"(overflow={rx.fifo_overflow} prefill={rx.fifo_armed} "
              f"starved={rx.fifo_starved}) (bug #44)")
        return False
    print(f"ECHO: {len(payload)} bytes OUT and IN through Gen2 framing, "
          f"sha-exact, CRC-32 valid")
    return True


async def run_hotreset(ctx, bench, hm, rx, model_tx, parked=False):
    """Gen2 Hot Reset (bug #44): the xHCI hub driver's very first action
    on a freshly connected SS port is a port reset = LINK Hot Reset
    [7.5.12].  On silicon the Gen2 attempt died exactly here: PORTSC
    showed U0 at PortSpeed:5 (Gen 2x1) held for ~108 ms, then
    Link:Hot-Reset for ~13 ms, then RxDetect/Not-connected -- the
    device vanished instead of completing the TS2-with-Reset handshake
    (the Gen1 path of the same flow is silicon-proven by every 5G
    enumeration).  No sim had ever exercised Hot Reset at EITHER rate.

    Sequence (strict, mirrors the DFP flow):
      1. link init + SET_ADDRESS(1) -- give the device a non-default
         address so the reset semantics are observable;
      2. Recovery entry: TS1 blocks from the host; require device TS1s;
      3. host Hot Reset.Active: TS2 blocks with the Reset bit
         (link_func[0]) set; require >= 2 device TS2s WITH Reset;
      4. host Hot Reset.Exit: TS2 blocks with Reset clear, then
         SKP + SDS + Idle; require device SDS + idle (data stream);
      5. link RE-initialization: LGOOD_15 + the full 4+4 credit
         advertisement again [7.2.4.1.1: U0 from Hot Reset resets all
         sequence numbers and credit counts];
      6. SET_ADDRESS(2) delivered to the DEFAULT address: a device
         whose address survived the reset ignores it (red signature);
      7. GetDescriptor(DEVICE) at address 2, full DPH+DPP.

    ``parked=True`` (PHASE=hotreset-parked; bug #49 sim lead (c),
    session 17): between steps 1 and 2 a control IN transfer is PARKED
    mid-data-stage -- SETUP acknowledged, IN ACK TP sent, the device's
    DPH+DPP received but never LGOOD'd and its credit never returned,
    no STATUS stage.  The bench post-#48 wedge survives hot reset AND
    the 5G fallback until a power cycle; if the EP0/protocol state
    machine holds any state across the reset (a pending IN, an
    un-acked header, a half-open control transfer), steps 5-7 go red.
    """
    from sim_link_loopback import frame_out_dp, frame_status_tp, \
        frame_ack_tp
    host = Gen2LinkHost(ctx, bench, hm, rx, model_tx, tag="HOTRESET")
    ret_idx = {1: 0, 2: 0}

    async def return_credit(series):
        sub = (0b0100 if series == 2 else 0) | ret_idx[series]
        ret_idx[series] = (ret_idx[series] + 1) & 3
        await host.send_lc(0b0001, sub)

    async def link_init(tag):
        ev = await host.expect(f"LGOOD advertisement ({tag})",
                               lambda e: e[0] == 'lc' and e[1] == 0b0000)
        if ev is None:
            return False
        if ev[2] != 15:
            print(f"HOTRESET FAIL: advertisement LGOOD_{ev[2]} ({tag}); "
                  f"sequence numbers must reset to 0 -> LGOOD_15 "
                  f"[7.2.4.1.1]")
            return False
        adv = []
        for _ in range(8):
            ev = await host.expect(f"credit advertisement ({tag})",
                                   lambda e: e[0] == 'lc'
                                   and e[1] == 0b0001)
            if ev is None:
                print(f"HOTRESET FAIL: short credit advertisement ({tag}); "
                      f"U0 from Hot Reset advertises 4+4 like from "
                      f"Polling [7.2.4.1.1 rule 2.e.1]")
                return False
            adv.append(ev[2])
        if [c & 3 for c in adv if not (c & 4)] != [0, 1, 2, 3] or \
                [c & 3 for c in adv if c & 4] != [0, 1, 2, 3]:
            print(f"HOTRESET FAIL: advertisement "
                  f"{['%#x' % c for c in adv]} not LCRD1_A..D + "
                  f"LCRD2_A..D ({tag})")
            return False
        # host advertisement
        syms = link_command_syms(0b0000, 15)
        for i in range(4):
            syms += link_command_syms(0b0001, i)
        for i in range(4):
            syms += link_command_syms(0b0001, 0b0100 | i)
        await host.send_syms(syms)
        # drain the device's link-up Port Capability LMP(s)
        dev_seq = 0
        while True:
            ev = await host.expect("link-up LMP",
                                   lambda e: e[0] == 'hdr'
                                   and (e[1][0] & 0x1F) == 0,
                                   timeout_blocks=400, quiet=True)
            if ev is None:
                break
            if ev[2] != dev_seq:
                print(f"HOTRESET FAIL: LMP seq {ev[2]} != {dev_seq} ({tag})")
                return False
            dev_seq = (dev_seq + 1) & 0xF
            await host.send_lc(0b0000, ev[2])
            await return_credit(1)
        host.dev_seq = dev_seq
        return True

    async def set_address(addr, lgood_n):
        setup = bytes([0x00, 0x05, addr, 0x00, 0x00, 0x00, 0x00, 0x00])
        await host.send_frame(frame_out_dp(0, 0, setup, setup=1, address=0))
        ev = await host.expect(f"LGOOD for SET_ADDRESS({addr}) SETUP",
                               lambda e: e[0] == 'lc' and e[1] == 0b0000)
        if ev is None or ev[2] != lgood_n:
            print(f"HOTRESET FAIL: SETUP not acked (got {ev}); expected "
                  f"LGOOD_{lgood_n} -- an addressed device ignores "
                  f"default-address traffic (address not reset?)")
            return False
        ev = await host.expect("LCRD2 return",
                               lambda e: e[0] == 'lc' and e[1] == 0b0001)
        if ev is None or not (ev[2] & 4):
            print(f"HOTRESET FAIL: SETUP credit return wrong: {ev}")
            return False
        ev = await host.expect("SETUP ACK TP",
                               lambda e: e[0] == 'hdr'
                               and (e[1][0] & 0x1F) == 4)
        if ev is None:
            return False
        if ev[2] != host.dev_seq:
            print(f"HOTRESET FAIL: ACK seq {ev[2]} != {host.dev_seq}")
            return False
        host.dev_seq = (host.dev_seq + 1) & 0xF
        await host.send_lc(0b0000, ev[2])
        await return_credit(1)
        await host.send_frame(frame_status_tp(0, address=0))
        ev = await host.expect("LGOOD for STATUS",
                               lambda e: e[0] == 'lc' and e[1] == 0b0000)
        if ev is None:
            return False
        ev = await host.expect("LCRD1 return",
                               lambda e: e[0] == 'lc' and e[1] == 0b0001)
        if ev is None:
            return False
        ev = await host.expect("STATUS ACK TP",
                               lambda e: e[0] == 'hdr'
                               and (e[1][0] & 0x1F) == 4)
        if ev is None:
            return False
        host.dev_seq = (host.dev_seq + 1) & 0xF
        await host.send_lc(0b0000, ev[2])
        await return_credit(1)
        return True

    # ── 1. initial link init + SET_ADDRESS(1) ──
    host.dev_seq = 0
    if not await link_init("initial"):
        return False
    if not await set_address(1, 0):
        return False
    print("HOTRESET: link initialized, device at address 1")

    if parked:
        # ── 1b. park a control IN mid-data-stage (lead (c)): the
        # device is left holding an un-acknowledged DPH (its
        # PENDING_HP_TIMER running), a consumed type-2 credit, and a
        # control transfer with no STATUS stage. ──
        setup = bytes([0x80, 0x06, 0x00, 0x01, 0x00, 0x00, 18, 0x00])
        await host.send_frame(frame_out_dp(0, 0, setup, setup=1,
                                           address=1))
        if not await host.expect("parked SETUP LGOOD",
                                 lambda e: e[0] == 'lc'
                                 and e[1] == 0b0000):
            return False
        if not await host.expect("parked SETUP credit",
                                 lambda e: e[0] == 'lc'
                                 and e[1] == 0b0001):
            return False
        ev = await host.expect("parked SETUP ACK TP",
                               lambda e: e[0] == 'hdr'
                               and (e[1][0] & 0x1F) == 4)
        if ev is None:
            return False
        host.dev_seq = (host.dev_seq + 1) & 0xF
        await host.send_lc(0b0000, ev[2])
        await return_credit(1)
        await host.send_frame(frame_ack_tp(ep=0, nseq=0, nump=1,
                                           direction=1))
        if not await host.expect("parked IN LGOOD",
                                 lambda e: e[0] == 'lc'
                                 and e[1] == 0b0000):
            return False
        if not await host.expect("parked IN credit",
                                 lambda e: e[0] == 'lc'
                                 and e[1] == 0b0001):
            return False
        ev = await host.expect("parked DPH",
                               lambda e: e[0] == 'hdr'
                               and (e[1][0] & 0x1F) == 8)
        if ev is None:
            return False
        ev_dpp = await host.expect("parked DPP",
                                   lambda e: e[0] == 'dpp')
        if ev_dpp is None:
            return False
        # NO LGOOD, NO credit return, NO STATUS: the transfer is
        # parked mid-data-stage as the reset begins.
        print("HOTRESET: control IN parked mid-data-stage (DPH "
              "un-acknowledged, credit held, no STATUS)")

    # ── 2. Recovery entry: TS1s ──
    def count_ts(kind, reset_bit=None, since=0):
        n = 0
        for h, syms in rx.blocks[since:]:
            if h == BLOCK_CONTROL and syms and syms[0] == int(kind):
                if reset_bit is None or bool(syms[5] & 1) == reset_bit:
                    n += 1
        return n

    mark = len(rx.blocks)
    for _ in range(12):
        await feed_blocks(ctx, bench, model_tx,
                          [sync_block()] + [ts1_block()] * 32, rx, hm)
        if count_ts(BlockType.TS1, since=mark) >= 8:
            break
    n_ts1 = count_ts(BlockType.TS1, since=mark)
    if n_ts1 < 8:
        print(f"HOTRESET FAIL: only {n_ts1} device TS1 blocks after "
              f"Recovery entry from U0")
        return False
    print(f"HOTRESET: Recovery entered ({n_ts1} device TS1s)")

    # ── 3. host Hot Reset: TS2s with the Reset bit ──
    mark = len(rx.blocks)
    for _ in range(12):
        await feed_blocks(ctx, bench, model_tx,
                          [sync_block()] + [ts2_block(link_func=1)] * 16,
                          rx, hm)
        if count_ts(BlockType.TS2, reset_bit=True, since=mark) >= 2:
            break
    n_rst = count_ts(BlockType.TS2, reset_bit=True, since=mark)
    if n_rst < 2:
        n_ts2 = count_ts(BlockType.TS2, since=mark)
        print(f"HOTRESET FAIL: no TS2-with-Reset from device "
              f"(Hot Reset.Active never entered; {n_ts2} plain TS2s) "
              f"[7.5.12]")
        return False
    print(f"HOTRESET: device in Hot Reset.Active ({n_rst} TS2+Reset)")

    # ── 4. host Hot Reset.Exit: TS2s with Reset clear, then SDS ──
    mark = len(rx.blocks)
    for _ in range(8):
        await feed_blocks(ctx, bench, model_tx,
                          [sync_block()] + [ts2_block()] * 16, rx, hm)
        if count_ts(BlockType.TS2, reset_bit=False, since=mark) >= 2:
            break
    await feed_blocks(ctx, bench, model_tx,
                      [skp_block(), sds_block()]
                      + [idle_block()] * 20 + [skp_block()]
                      + [idle_block()] * 20, rx, hm)
    got_sds = any(h == BLOCK_CONTROL and s[0] == 0xE1
                  for h, s in rx.blocks[mark:])
    if not got_sds:
        print("HOTRESET FAIL: no SDS from device in Hot Reset.Exit "
              "[6.4.1.5: SDS shall be transmitted during Hot Reset.Exit]")
        return False
    print("HOTRESET: Hot Reset.Exit complete (device SDS seen)")

    # ── 5+6+7. re-init, SET_ADDRESS(2) at default, GetDescriptor ──
    # Hot Reset resets ALL link-init state on both sides [7.2.4.1.1]:
    # sequence numbers and per-class credit indices restart at 0/A.
    host.events.clear()
    host.errors.clear()
    host.tx_seq = 0
    host.dev_seq = 0
    ret_idx[1] = ret_idx[2] = 0
    if not await link_init("post-reset"):
        return False
    print("HOTRESET: link re-initialized after Hot Reset")
    if not await set_address(2, 0):
        return False
    print("HOTRESET: SET_ADDRESS(2) at the DEFAULT address accepted "
          "(device address was reset)")

    setup = bytes([0x80, 0x06, 0x00, 0x01, 0x00, 0x00, 0x12, 0x00])
    await host.send_frame(frame_out_dp(0, 0, setup, setup=1, address=2))
    ev = await host.expect("descriptor SETUP LGOOD",
                           lambda e: e[0] == 'lc' and e[1] == 0b0000)
    if ev is None:
        return False
    ev = await host.expect("descriptor SETUP credit",
                           lambda e: e[0] == 'lc' and e[1] == 0b0001)
    if ev is None:
        return False
    ev = await host.expect("descriptor SETUP ACK",
                           lambda e: e[0] == 'hdr'
                           and (e[1][0] & 0x1F) == 4)
    if ev is None:
        return False
    host.dev_seq = (host.dev_seq + 1) & 0xF
    await host.send_lc(0b0000, ev[2])
    await return_credit(1)
    from sim_link_loopback import frame_ack_tp
    await host.send_frame(frame_ack_tp(ep=0, nseq=0, nump=1, direction=1))
    ev = await host.expect("IN token LGOOD",
                           lambda e: e[0] == 'lc' and e[1] == 0b0000)
    if ev is None:
        return False
    ev = await host.expect("IN token credit",
                           lambda e: e[0] == 'lc' and e[1] == 0b0001)
    if ev is None:
        return False
    ev = await host.expect("descriptor DPH",
                           lambda e: e[0] == 'hdr'
                           and (e[1][0] & 0x1F) == 8)
    if ev is None:
        return False
    ev_dpp = await host.expect("descriptor DPP", lambda e: e[0] == 'dpp')
    if ev_dpp is None:
        return False
    if not ev_dpp[2] or len(ev_dpp[1]) != 18 or ev_dpp[1][1] != 1:
        print(f"HOTRESET FAIL: bad descriptor after reset "
              f"(crc_ok={ev_dpp[2]} len={len(ev_dpp[1])})")
        return False
    if host.errors:
        print(f"HOTRESET FAIL: parser errors: {host.errors[:6]}")
        return False
    print("HOTRESET: Hot Reset handshake, SDS, link re-init, address "
          "reset, descriptor read -- the xHCI port-reset flow works "
          "at Gen2")
    return True


async def run_recovery(ctx, bench, hm, rx, model_tx):
    """Plain Recovery mid-traffic at Gen2 (the silicon 142 kHz
    recovery-loop hunt): unlike Hot Reset, a Recovery pass PRESERVES
    sequence numbers, so the re-initialization advertisement carries
    NONZERO values -- the device advertises LGOOD_(last properly
    received) and re-advertises per-class credits for its FREE buffers
    [7.2.4.1.1 rules 2.e.2 / 7.b]; the host does the same.  The
    continuation surface (nonzero LGOOD advertisement value, mod-16;
    credit indices restarting at A while counts reflect occupancy;
    traffic resuming with preserved sequence numbers) was never
    sim-covered at Gen2.
    """
    from sim_link_loopback import frame_out_dp, frame_status_tp
    host = Gen2LinkHost(ctx, bench, hm, rx, model_tx, tag="RECOVERY")
    ret_idx = {1: 0, 2: 0}

    async def return_credit(series):
        sub = (0b0100 if series == 2 else 0) | ret_idx[series]
        ret_idx[series] = (ret_idx[series] + 1) & 3
        await host.send_lc(0b0001, sub)

    async def link_init(tag, expect_lgood):
        ev = await host.expect(f"LGOOD advertisement ({tag})",
                               lambda e: e[0] == 'lc' and e[1] == 0b0000)
        if ev is None:
            return False
        if ev[2] != expect_lgood:
            print(f"RECOVERY FAIL: advertisement LGOOD_{ev[2]} ({tag}), "
                  f"expected LGOOD_{expect_lgood} (the last properly "
                  f"received header, PRESERVED across Recovery "
                  f"[7.2.4.1.1])")
            return False
        adv = []
        for _ in range(8):
            ev = await host.expect(f"credit advertisement ({tag})",
                                   lambda e: e[0] == 'lc'
                                   and e[1] == 0b0001)
            if ev is None:
                print(f"RECOVERY FAIL: short credit advertisement ({tag})")
                return False
            adv.append(ev[2])
        if [c & 3 for c in adv if not (c & 4)] != [0, 1, 2, 3] or \
                [c & 3 for c in adv if c & 4] != [0, 1, 2, 3]:
            print(f"RECOVERY FAIL: advertisement "
                  f"{['%#x' % c for c in adv]} not LCRD1_A..D + "
                  f"LCRD2_A..D ({tag})")
            return False
        # host advertisement: LGOOD_(last received from device) + 4+4
        syms = link_command_syms(0b0000, (host.dev_seq - 1) & 0xF)
        for i in range(4):
            syms += link_command_syms(0b0001, i)
        for i in range(4):
            syms += link_command_syms(0b0001, 0b0100 | i)
        await host.send_syms(syms)
        return True

    async def drain_lmps():
        while True:
            ev = await host.expect("link-up LMP",
                                   lambda e: e[0] == 'hdr'
                                   and (e[1][0] & 0x1F) == 0,
                                   timeout_blocks=400, quiet=True)
            if ev is None:
                return True
            if ev[2] != host.dev_seq:
                print(f"RECOVERY FAIL: LMP seq {ev[2]} != {host.dev_seq}")
                return False
            host.dev_seq = (host.dev_seq + 1) & 0xF
            await host.send_lc(0b0000, ev[2])
            await return_credit(1)

    async def control_xfer(addr, first_lgood):
        setup = bytes([0x00, 0x05, addr, 0x00, 0x00, 0x00, 0x00, 0x00])
        await host.send_frame(frame_out_dp(0, 0, setup, setup=1,
                                           address=0 if addr else 0))
        ev = await host.expect("SETUP LGOOD",
                               lambda e: e[0] == 'lc' and e[1] == 0b0000)
        if ev is None or ev[2] != first_lgood:
            print(f"RECOVERY FAIL: SETUP ack {ev} != LGOOD_{first_lgood}")
            return False
        ev = await host.expect("SETUP credit",
                               lambda e: e[0] == 'lc' and e[1] == 0b0001)
        if ev is None:
            return False
        ev = await host.expect("SETUP ACK TP",
                               lambda e: e[0] == 'hdr'
                               and (e[1][0] & 0x1F) == 4)
        if ev is None:
            return False
        if ev[2] != host.dev_seq:
            print(f"RECOVERY FAIL: ACK seq {ev[2]} != {host.dev_seq}")
            return False
        host.dev_seq = (host.dev_seq + 1) & 0xF
        await host.send_lc(0b0000, ev[2])
        await return_credit(1)
        await host.send_frame(frame_status_tp(0, address=0))
        ev = await host.expect("STATUS LGOOD",
                               lambda e: e[0] == 'lc' and e[1] == 0b0000)
        if ev is None:
            return False
        ev = await host.expect("STATUS credit",
                               lambda e: e[0] == 'lc' and e[1] == 0b0001)
        if ev is None:
            return False
        ev = await host.expect("STATUS ACK TP",
                               lambda e: e[0] == 'hdr'
                               and (e[1][0] & 0x1F) == 4)
        if ev is None:
            return False
        host.dev_seq = (host.dev_seq + 1) & 0xF
        await host.send_lc(0b0000, ev[2])
        await return_credit(1)
        return True

    # ── initial link-up + SET_ADDRESS(1): two host headers exchanged ──
    host.dev_seq = 0
    if not await link_init("initial", 15):
        return False
    if not await drain_lmps():
        return False
    if not await control_xfer(1, 0):
        return False
    print("RECOVERY: initial traffic complete (host seq at 2, device "
          f"seq at {host.dev_seq})")

    # ── THREE plain recovery passes with traffic in between ──
    for n in range(3):
        mark = len(rx.blocks)

        def count_ts(kind, since):
            return sum(1 for h, s in rx.blocks[since:]
                       if h == BLOCK_CONTROL and s and s[0] == int(kind))

        for _ in range(12):
            await feed_blocks(ctx, bench, model_tx,
                              [sync_block()] + [ts1_block()] * 32, rx, hm)
            if count_ts(BlockType.TS1, mark) >= 8:
                break
        if count_ts(BlockType.TS1, mark) < 8:
            print(f"RECOVERY FAIL: pass {n}: no TS1s from device")
            return False
        mark2 = len(rx.blocks)
        for _ in range(8):
            await feed_blocks(ctx, bench, model_tx,
                              [sync_block()] + [ts2_block()] * 16, rx, hm)
            if count_ts(BlockType.TS2, mark2) >= 8:
                break
        await feed_blocks(ctx, bench, model_tx,
                          [skp_block(), sds_block()]
                          + [idle_block()] * 20, rx, hm)

        # re-initialization: the device advertises its PRESERVED
        # sequence state: LGOOD_(host_seq - 1) = LGOOD_(2 + 2n - 1)
        host.events.clear()
        host.errors.clear()
        ret_idx[1] = ret_idx[2] = 0
        if not await link_init(f"pass {n}", (2 + 2 * n - 1) & 0xF):
            return False
        if not await drain_lmps():
            return False
        # traffic must continue with preserved numbering
        if not await control_xfer(1, (2 + 2 * n) & 0xF):
            return False
        print(f"RECOVERY: pass {n} complete -- re-advertised "
              f"LGOOD_{(2 + 2 * n - 1) & 0xF}, traffic resumed")

    if host.errors:
        print(f"RECOVERY FAIL: parser errors: {host.errors[:6]}")
        return False

    # The #49 lead-(a) instrument (session 17): the bench canary fires
    # txfifo-hi28 ~71k/s against ~5.5k host retrains/s (~13 hi28
    # cycles per retrain) -- if the TX FIFO overshoots the #44 band
    # across U0->Recovery->U0 crossings, it must reproduce here under
    # the real gearbox drain law.
    print(f"RECOVERY: PHY TX FIFO across {3} retrain crossings: max "
          f"{rx.fifo_max}/32, hi28 cycles {rx.fifo_hi28}, "
          f"starved {rx.fifo_starved}, overflow {rx.fifo_overflow}")
    if rx.fifo_overflow or rx.fifo_hi28 or rx.fifo_starved:
        print(f"RECOVERY FAIL: PHY TX FIFO left the pacing band across "
              f"a retrain (hi28={rx.fifo_hi28} starved={rx.fifo_starved} "
              f"overflow={rx.fifo_overflow}) -- the #49 lead (a) shape")
        return False
    print("RECOVERY: three mid-traffic Recovery passes with preserved "
          "sequence numbers and full 4+4 re-advertisement -- the U0 "
          "re-initialization surface works at Gen2")
    return True


async def run_reccut(ctx, bench, hm, rx, model_tx):
    """Bug #49 sim lead (b) (session 17): a control transfer CUT by a
    host-initiated Recovery mid-data-stage.  The bench evidence: the
    full-BOS read dies EPROTO -71 while the host retrains at kHz rates
    throughout the window -- a retrain lands between the host's IN ACK
    TP and the device's DPP with certainty at those rates.  The
    idealized enum ladder never overlaps a retrain with a transfer;
    this phase does, at swept offsets:

      offset 0       the TS1 burst begins IMMEDIATELY after the IN ACK
                     TP is acknowledged -- the device is yanked while
                     preparing or transmitting the DPH/DPP;
      offset 1..N    idle blocks first, walking the cut across the
                     DPH, the DPH/DPP seam and the DPP body.

    After each retrain + re-advertisement the device must retransmit
    the un-acknowledged DP -- SAME link-header sequence number,
    byte-exact SAME payload [7.2.4.1.1 rule 7, 7.2.4.1.5]; if the cut
    landed after the full DP was properly received, the host's
    advertisement covers it and NO retransmission may occur.  The
    STATUS stage then completes, and a further full control transfer
    proves EP0 survived (the #49 post-failure wedge shape).  The
    PHY TX FIFO instrument rides along: the #44 pacing band must hold
    across every mid-transfer retrain (lead (a) under overlap).

    The #37 parked item (truncated inbound DPP never retried) is the
    RX-side sibling of this surface; a red here localizes the wedge.
    """
    from sim_link_loopback import frame_out_dp, frame_ack_tp, \
        frame_status_tp
    host = Gen2LinkHost(ctx, bench, hm, rx, model_tx, tag="RECCUT")
    ret_idx = {1: 0, 2: 0}

    async def return_credit(series):
        sub = (0b0100 if series == 2 else 0) | ret_idx[series]
        ret_idx[series] = (ret_idx[series] + 1) & 3
        await host.send_lc(0b0001, sub)

    async def link_init(tag, legal_lgoods):
        """Advertisement exchange; returns the device's advertised
        LGOOD (the last host header it PROPERLY received -- a header
        fully delivered but yanked out of the RX pipeline by the
        retrain may legitimately be excluded: the host then
        retransmits past the advertisement, exactly like the real
        xHC), or None on failure."""
        ev = await host.expect(f"LGOOD advertisement ({tag})",
                               lambda e: e[0] == 'lc' and e[1] == 0b0000)
        if ev is None:
            return None
        if ev[2] not in legal_lgoods:
            print(f"RECCUT FAIL: advertisement LGOOD_{ev[2]} ({tag}), "
                  f"legal values {sorted(legal_lgoods)}")
            return None
        lgood = ev[2]
        adv = []
        for _ in range(8):
            ev = await host.expect(f"credit advertisement ({tag})",
                                   lambda e: e[0] == 'lc'
                                   and e[1] == 0b0001)
            if ev is None:
                print(f"RECCUT FAIL: short credit advertisement ({tag})")
                return None
            adv.append(ev[2])
        if [c & 3 for c in adv if not (c & 4)] != [0, 1, 2, 3] or \
                [c & 3 for c in adv if c & 4] != [0, 1, 2, 3]:
            print(f"RECCUT FAIL: advertisement "
                  f"{['%#x' % c for c in adv]} not 4+4 ({tag})")
            return None
        syms = link_command_syms(0b0000, (host.dev_seq - 1) & 0xF)
        for i in range(4):
            syms += link_command_syms(0b0001, i)
        for i in range(4):
            syms += link_command_syms(0b0001, 0b0100 | i)
        await host.send_syms(syms)
        return lgood

    async def drain_lmps():
        while True:
            ev = await host.expect("link-up LMP",
                                   lambda e: e[0] == 'hdr'
                                   and (e[1][0] & 0x1F) == 0,
                                   timeout_blocks=400, quiet=True)
            if ev is None:
                return True
            if ev[2] != host.dev_seq:
                print(f"RECCUT FAIL: LMP seq {ev[2]} != {host.dev_seq}")
                return False
            host.dev_seq = (host.dev_seq + 1) & 0xF
            await host.send_lc(0b0000, ev[2])
            await return_credit(1)

    async def retrain(tag):
        """Yank the link into Recovery with TS1s, run the handshake,
        clear the (legitimately truncated) parser state, re-init."""
        mark = len(rx.blocks)

        def count_ts(kind, since):
            return sum(1 for h, s in rx.blocks[since:]
                       if h == BLOCK_CONTROL and s and s[0] == int(kind))

        for _ in range(12):
            await feed_blocks(ctx, bench, model_tx,
                              [sync_block()] + [ts1_block()] * 32, rx, hm)
            if count_ts(BlockType.TS1, mark) >= 8:
                break
        if count_ts(BlockType.TS1, mark) < 8:
            print(f"RECCUT FAIL: {tag}: no TS1s from device")
            return False
        mark2 = len(rx.blocks)
        for _ in range(8):
            await feed_blocks(ctx, bench, model_tx,
                              [sync_block()] + [ts2_block()] * 16, rx, hm)
            if count_ts(BlockType.TS2, mark2) >= 8:
                break
        await feed_blocks(ctx, bench, model_tx,
                          [skp_block(), sds_block()]
                          + [idle_block()] * 20, rx, hm)
        # The cut legitimately truncates the device's wire stream:
        # reset the parser mid-construct state and drop cut artifacts.
        host.events.clear()
        host.errors.clear()
        host._state = 'search'
        host._syms = []
        host._dph_pending = False
        host._cursor = len(rx.blocks)
        ret_idx[1] = ret_idx[2] = 0
        return True

    # ── link-up + SET_ADDRESS(1) ──
    host.dev_seq = 0
    if await link_init("initial", {15}) is None:
        return False
    if not await drain_lmps():
        return False
    setup = bytes([0x00, 0x05, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00])
    await host.send_frame(frame_out_dp(0, 0, setup, setup=1, address=0))
    if not await host.expect("SET_ADDRESS LGOOD",
                             lambda e: e[0] == 'lc' and e[1] == 0b0000):
        return False
    if not await host.expect("SET_ADDRESS credit",
                             lambda e: e[0] == 'lc' and e[1] == 0b0001):
        return False
    ev = await host.expect("SET_ADDRESS ACK TP",
                           lambda e: e[0] == 'hdr'
                           and (e[1][0] & 0x1F) == 4)
    if ev is None:
        return False
    host.dev_seq = (host.dev_seq + 1) & 0xF
    await host.send_lc(0b0000, ev[2])
    await return_credit(1)
    await host.send_frame(frame_status_tp(0, address=0))
    if not await host.expect("STATUS LGOOD",
                             lambda e: e[0] == 'lc' and e[1] == 0b0000):
        return False
    if not await host.expect("STATUS credit",
                             lambda e: e[0] == 'lc' and e[1] == 0b0001):
        return False
    ev = await host.expect("STATUS ACK TP",
                           lambda e: e[0] == 'hdr'
                           and (e[1][0] & 0x1F) == 4)
    if ev is None:
        return False
    host.dev_seq = (host.dev_seq + 1) & 0xF
    await host.send_lc(0b0000, ev[2])
    await return_credit(1)
    print("RECCUT: SET_ADDRESS complete; sweeping mid-data-stage cuts")

    expected_payload = {}

    # ── the cut sweeps ──
    #
    # dev18: GetDescriptor(Device, 18) -- the historical #50/#51 sweep
    #        (payload BELOW the bench length boundary: 18-byte reads
    #        complete on silicon).
    # bos50: GetDescriptor(BOS, 50) -- THE bench EPROTO transfer
    #        (session 20: every read with payload >= 22 bytes dies
    #        EPROTO -71 deterministically at Gen2 while <= 18-byte
    #        reads complete; the wedge follows).  The offsets walk the
    #        cut across the whole longer construct.
    async def sweep_cuts(tag, setup, offsets, validate):
      for offset in offsets:
        await host.send_frame(frame_out_dp(0, 0, setup, setup=1,
                                           address=1))
        if not await host.expect(f"{tag} SETUP LGOOD",
                                 lambda e: e[0] == 'lc'
                                 and e[1] == 0b0000):
            return False
        if not await host.expect(f"{tag} SETUP credit",
                                 lambda e: e[0] == 'lc'
                                 and e[1] == 0b0001):
            return False
        ev = await host.expect(f"{tag} SETUP ACK TP",
                               lambda e: e[0] == 'hdr'
                               and (e[1][0] & 0x1F) == 4)
        if ev is None:
            return False
        if ev[2] != host.dev_seq:
            print(f"RECCUT FAIL: {tag} SETUP ACK seq {ev[2]} != "
                  f"{host.dev_seq} (offset {offset})")
            return False
        host.dev_seq = (host.dev_seq + 1) & 0xF
        await host.send_lc(0b0000, ev[2])
        await return_credit(1)

        # IN token -- the device now owes DPH+DPP...
        in_ack = frame_ack_tp(ep=0, nseq=0, nump=1, direction=1)
        ack_seq = host.tx_seq
        await host.send_frame(in_ack)
        # ...and the cut lands after ``offset`` idle blocks.
        await feed_blocks(ctx, bench, model_tx,
                          [idle_block()] * offset, rx, hm)

        # Classify what made it out before the cut: a COMPLETE DP
        # (DPH event + CRC-valid DPP event) counts as properly
        # received; anything less does not.
        host.pump()
        dph_seq = None
        got_payload = None
        for e in host.events:
            if e[0] == 'hdr' and (e[1][0] & 0x1F) == 8 and e[3] == 'dph':
                dph_seq = e[2]
            elif e[0] == 'dpp' and e[2] and dph_seq is not None:
                got_payload = e[1]
        complete_pre_cut = got_payload is not None
        if complete_pre_cut:
            host.dev_seq = (dph_seq + 1) & 0xF

        if not await retrain(f"{tag} offset {offset}"):
            return False
        # The device advertises the last host header it PROPERLY
        # received: the IN ACK TP (seq ``ack_seq``) if it cleared the
        # RX pipeline before the yank, else the header before it.
        lgood = await link_init(f"{tag} offset {offset}",
                                {ack_seq, (ack_seq - 1) & 0xF})
        if lgood is None:
            return False
        if not await drain_lmps():
            return False

        if lgood != ack_seq:
            # The IN ACK TP died in the cut: host-side rule-7
            # retransmission with the ORIGINAL sequence number.
            print(f"RECCUT: offset {offset}: IN ACK TP (seq {ack_seq}) "
                  f"not covered by LGOOD_{lgood}; host retransmits")
            await host.send_frame(in_ack, seq=ack_seq)
            if not await host.expect(
                    f"retransmitted-ACK LGOOD (offset {offset})",
                    lambda e: e[0] == 'lc' and e[1] == 0b0000
                    and e[2] == ack_seq):
                return False
            if not await host.expect(
                    f"retransmitted-ACK credit (offset {offset})",
                    lambda e: e[0] == 'lc' and e[1] == 0b0001):
                return False

        if complete_pre_cut:
            payload = got_payload
            print(f"RECCUT: offset {offset}: DP completed pre-cut "
                  f"(seq {dph_seq}); host advertisement covers it")
        else:
            # The DP must now arrive: RETRANSMITTED (if it went out
            # pre-cut un-acked) or fresh (if the IN ACK TP itself was
            # cut) -- either way with the device's next unacknowledged
            # sequence number and a byte-exact payload.
            ev = await host.expect(
                f"post-cut DPH (offset {offset})",
                lambda e: e[0] == 'hdr' and (e[1][0] & 0x1F) == 8
                and e[3] == 'dph')
            if ev is None:
                print(f"RECCUT FAIL: offset {offset}: the cut DP was "
                      f"never (re)transmitted after the retrain (the "
                      f"#37 class on the TX side; bug #49 lead (b))")
                return False
            if ev[2] != host.dev_seq:
                print(f"RECCUT FAIL: offset {offset}: post-cut DPH "
                      f"seq {ev[2]} != {host.dev_seq} (rule-7 go-back-N "
                      f"must preserve numbering)")
                return False
            ev_dpp = await host.expect(
                f"post-cut DPP (offset {offset})",
                lambda e: e[0] == 'dpp')
            if ev_dpp is None:
                print(f"RECCUT FAIL: offset {offset}: post-cut DPH "
                      f"without its DPP")
                return False
            host.dev_seq = (host.dev_seq + 1) & 0xF
            await host.send_lc(0b0000, (host.dev_seq - 1) & 0xF)
            await return_credit(2)

            if len(ev_dpp) > 3 and ev_dpp[3]:
                # The DL=1 retransmission ABORTED its DPP (the payload
                # was consumed by the cut transmission; no link-level
                # copy exists) -- the spec-correct wire shape.  Recovery
                # of the DATA is the protocol layer's job: the host
                # re-requests the IN data stage and the endpoint must
                # re-serve it [the #37 surface, TX side].
                print(f"RECCUT: offset {offset}: retransmitted DP "
                      f"aborted its DPP (payload consumed); host "
                      f"protocol-retries the IN stage")
                await host.send_frame(frame_ack_tp(ep=0, nseq=0, nump=1,
                                                   direction=1))
                if not await host.expect(
                        f"retry-IN LGOOD (offset {offset})",
                        lambda e: e[0] == 'lc' and e[1] == 0b0000):
                    return False
                if not await host.expect(
                        f"retry-IN credit (offset {offset})",
                        lambda e: e[0] == 'lc' and e[1] == 0b0001):
                    return False
                ev = await host.expect(
                    f"re-served DPH (offset {offset})",
                    lambda e: e[0] == 'hdr' and (e[1][0] & 0x1F) == 8
                    and e[3] == 'dph')
                if ev is None:
                    print(f"RECCUT FAIL: offset {offset}: the endpoint "
                          f"never re-served the aborted data stage (the "
                          f"#37 class; the #49 EP0 wedge shape)")
                    return False
                if ev[2] != host.dev_seq:
                    print(f"RECCUT FAIL: offset {offset}: re-served DPH "
                          f"seq {ev[2]} != {host.dev_seq}")
                    return False
                ev_dpp = await host.expect(
                    f"re-served DPP (offset {offset})",
                    lambda e: e[0] == 'dpp')
                if ev_dpp is None:
                    print(f"RECCUT FAIL: offset {offset}: re-served DPH "
                          f"without its DPP")
                    return False
                host.dev_seq = (host.dev_seq + 1) & 0xF
                await host.send_lc(0b0000, (host.dev_seq - 1) & 0xF)
                await return_credit(2)

            payload, crc_ok = ev_dpp[1], ev_dpp[2]
            if not crc_ok:
                print(f"RECCUT FAIL: offset {offset}: post-cut DPP "
                      f"CRC-32 invalid")
                return False

        err = validate(payload)
        if err:
            print(f"RECCUT FAIL: {tag} offset {offset}: {err} "
                  f"(payload {payload.hex() if payload else payload})")
            return False
        if tag not in expected_payload:
            expected_payload[tag] = payload
        elif payload != expected_payload[tag]:
            print(f"RECCUT FAIL: {tag} offset {offset}: post-cut payload "
                  f"{payload.hex()} != original "
                  f"{expected_payload[tag].hex()} "
                  f"(byte-exactness across the cut)")
            return False

        # STATUS stage completes the cut transfer.
        await host.send_frame(frame_status_tp(0, address=1))
        if not await host.expect("post-cut STATUS LGOOD",
                                 lambda e: e[0] == 'lc'
                                 and e[1] == 0b0000):
            return False
        if not await host.expect("post-cut STATUS credit",
                                 lambda e: e[0] == 'lc'
                                 and e[1] == 0b0001):
            return False
        ev = await host.expect("post-cut STATUS ACK TP",
                               lambda e: e[0] == 'hdr'
                               and (e[1][0] & 0x1F) == 4)
        if ev is None:
            return False
        host.dev_seq = (host.dev_seq + 1) & 0xF
        await host.send_lc(0b0000, ev[2])
        await return_credit(1)
        print(f"RECCUT: {tag} offset {offset}: transfer completed across "
              f"the mid-data-stage retrain")
      return True

    def validate_dev18(payload):
        if len(payload) != 18 or payload[0] != 0x12 or payload[1] != 0x01:
            return "descriptor payload malformed"
        return None

    def validate_bos50(payload):
        if len(payload) != 50 or payload[0:4] != bytes([5, 0x0F, 50, 0]) \
                or payload[4] != 3:
            return "BOS payload malformed (50-byte SSP BOS expected)"
        return None

    if not await sweep_cuts(
            "dev18", bytes([0x80, 0x06, 0x00, 0x01, 0x00, 0x00, 18, 0x00]),
            (0, 1, 2, 3, 4, 8, 24), validate_dev18):
        return False
    print("RECCUT: dev18 sweep complete; sweeping the 50-byte BOS read "
          "(the bench EPROTO transfer, session 20)")
    if not await sweep_cuts(
            "bos50", bytes([0x80, 0x06, 0x00, 0x0F, 0x00, 0x00, 50, 0x00]),
            (0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 28),
            validate_bos50):
        return False

    if host.errors:
        print(f"RECCUT FAIL: parser errors: {host.errors[:6]}")
        return False

    # The lead-(a) instrument under transfer/retrain overlap.
    print(f"RECCUT: PHY TX FIFO across the cut sweep: max "
          f"{rx.fifo_max}/32, hi28 cycles {rx.fifo_hi28}, "
          f"starved {rx.fifo_starved}, overflow {rx.fifo_overflow}")
    if rx.fifo_overflow or rx.fifo_hi28 or rx.fifo_starved:
        print(f"RECCUT FAIL: PHY TX FIFO left the pacing band across a "
              f"mid-transfer retrain (hi28={rx.fifo_hi28} "
              f"starved={rx.fifo_starved} overflow={rx.fifo_overflow}) "
              f"-- the #49 lead (a) shape under overlap")
        return False
    print("RECCUT: every mid-data-stage cut recovered -- rule-7 "
          "retransmission byte-exact, STATUS stages completed, EP0 "
          "alive, pacing band held (bug #49 leads (a)+(b) surface)")
    return True


async def run_advearly(ctx, bench, hm, rx, model_tx):
    """The CONCURRENT-advertisement surface (#45 sim lead (b), HANDOVER
    10u): on silicon the host reaches U0 FIRST -- its U0 entry needs
    only 8 of OUR idle symbols, which we stream from Polling/Recovery
    .Idle entry, so its Header Sequence Number Advertisement can land
    up to the whole idle-handshake skew BEFORE our own U0 entry.  The
    historical link-command detector sat in ResetInserter(~link_ready)
    and ATE any part of the burst arriving before -- or straddling --
    the enable edge: a fully eaten advertisement starves the device of
    TX credits forever (its headers never dispatch); a straddled one
    mis-indexes the first caught LCRD and forces an OUR-side recovery,
    re-aligning deterministically on every re-entry (the metronome
    shape of #45).

    Stimulus: plain Recovery passes; on each re-entry the host sends
    its advertisement EARLY -- embedded in the SDS/idle feed at a
    swept offset (block and half-block granularity) -- and only then
    waits for the device's.  Traffic with preserved numbering must
    resume on every pass; device-initiated TS1s in the aftermath
    window are a verdict failure."""
    from sim_link_loopback import frame_out_dp
    host = Gen2LinkHost(ctx, bench, hm, rx, model_tx, tag="ADVEARLY")
    ret_idx = {1: 0, 2: 0}

    async def return_credit(series):
        sub = (0b0100 if series == 2 else 0) | ret_idx[series]
        ret_idx[series] = (ret_idx[series] + 1) & 3
        await host.send_lc(0b0001, sub)

    def adv_syms():
        syms = link_command_syms(0b0000, (host.dev_seq - 1) & 0xF)
        for i in range(4):
            syms += link_command_syms(0b0001, i)
        for i in range(4):
            syms += link_command_syms(0b0001, 0b0100 | i)
        return syms

    async def expect_device_adv(tag, expect_lgood):
        ev = await host.expect(f"LGOOD advertisement ({tag})",
                               lambda e: e[0] == 'lc' and e[1] == 0b0000)
        if ev is None or ev[2] != expect_lgood:
            print(f"ADVEARLY FAIL: device advertisement {ev} ({tag}), "
                  f"expected LGOOD_{expect_lgood}")
            return False
        for _ in range(8):
            ev = await host.expect(f"credit advertisement ({tag})",
                                   lambda e: e[0] == 'lc'
                                   and e[1] == 0b0001)
            if ev is None:
                print(f"ADVEARLY FAIL: short credit advertisement ({tag})")
                return False
        return True

    async def setup_ack(tag, first_lgood):
        """One SETUP DP -> LGOOD/LCRD2 -> ACK TP round: the ACK TP is
        the direct proof the device holds TX credits from OUR (early)
        advertisement."""
        setup = bytes([0x00, 0x05, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00])
        await host.send_frame(frame_out_dp(0, 0, setup, setup=1,
                                           address=0))
        ev = await host.expect(f"SETUP LGOOD ({tag})",
                               lambda e: e[0] == 'lc' and e[1] == 0b0000)
        if ev is None or ev[2] != first_lgood:
            print(f"ADVEARLY FAIL: SETUP ack {ev} != LGOOD_{first_lgood} "
                  f"({tag})")
            return False
        ev = await host.expect(f"SETUP credit ({tag})",
                               lambda e: e[0] == 'lc' and e[1] == 0b0001)
        if ev is None:
            return False
        ev = await host.expect(
            f"SETUP ACK TP ({tag}; requires the early advertisement's "
            f"credits)", lambda e: e[0] == 'hdr'
            and (e[1][0] & 0x1F) == 4)
        if ev is None:
            return False
        if ev[2] != host.dev_seq:
            print(f"ADVEARLY FAIL: ACK seq {ev[2]} != {host.dev_seq} "
                  f"({tag})")
            return False
        host.dev_seq = (host.dev_seq + 1) & 0xF
        await host.send_lc(0b0000, ev[2])
        await return_credit(1)
        return True

    def count_ts(kind, since):
        return sum(1 for h, s in rx.blocks[since:]
                   if h == BLOCK_CONTROL and s and s[0] == int(kind))

    async def drain_lmps():
        while True:
            ev = await host.expect("link-up LMP",
                                   lambda e: e[0] == 'hdr'
                                   and (e[1][0] & 0x1F) == 0,
                                   timeout_blocks=400, quiet=True)
            if ev is None:
                return
            host.dev_seq = (host.dev_seq + 1) & 0xF
            await host.send_lc(0b0000, ev[2])
            await return_credit(1)

    # ── initial link-up (normal ordering) + one SETUP round ──
    host.dev_seq = 0
    if not await expect_device_adv("initial", 15):
        return False
    await host.send_syms(adv_syms())
    await drain_lmps()
    if not await setup_ack("initial", 0):
        return False
    print("ADVEARLY: initial link-up + SETUP round complete")

    # ── recovery passes, host advertisement EARLY at swept offsets ──
    offsets = [(k, sub) for k in (0, 1, 2, 3, 4, 6, 8) for sub in (0, 1)]
    for n, (k, sub) in enumerate(offsets):
        mark = len(rx.blocks)
        for _ in range(12):
            await feed_blocks(ctx, bench, model_tx,
                              [sync_block()] + [ts1_block()] * 32, rx, hm)
            if count_ts(BlockType.TS1, mark) >= 8:
                break
        if count_ts(BlockType.TS1, mark) < 8:
            print(f"ADVEARLY FAIL: pass {n}: no TS1s from device")
            return False
        mark2 = len(rx.blocks)
        for _ in range(8):
            await feed_blocks(ctx, bench, model_tx,
                              [sync_block()] + [ts2_block()] * 16, rx, hm)
            if count_ts(BlockType.TS2, mark2) >= 8:
                break

        host.events.clear()
        host.errors.clear()
        ret_idx[1] = ret_idx[2] = 0

        # SDS, then wait for the DEVICE's idle stream (Recovery.Idle
        # entry): the host's own U0 gate is 8 of the device's idle
        # symbols, so this is the EARLIEST a real host can advertise.
        # Then k more idle blocks (sub-shifted by half a block) before
        # the early advertisement -- the device's own U0 entry is
        # still pending for small k.
        await feed_blocks(ctx, bench, model_tx,
                          [skp_block(), sds_block()], rx, hm)
        mark_idle = len(rx.blocks)
        for _ in range(64):
            await feed_blocks(ctx, bench, model_tx, [idle_block()],
                              rx, hm)
            dev_idles = sum(1 for h, s in rx.blocks[mark_idle:]
                            if h == BLOCK_DATA
                            and all(x == IDLE_SYM for x in s))
            if dev_idles >= 1:
                break
        await feed_blocks(ctx, bench, model_tx, [idle_block()] * k,
                          rx, hm)
        await host.send_syms([IDLE_SYM] * (4 * sub) + adv_syms())
        await feed_blocks(ctx, bench, model_tx, [idle_block()] * 8,
                          rx, hm)

        expect_lgood = (1 + n) & 0xF     # one host header per pass
        if not await expect_device_adv(f"pass {n} k={k}.{sub}",
                                       (expect_lgood - 1) & 0xF):
            return False
        await drain_lmps()
        if not await setup_ack(f"pass {n} k={k}.{sub}", expect_lgood):
            return False

        # Aftermath: a quiet window must stay free of device TS1s (an
        # OUR-side recovery here is the #45 metronome shape).
        mark3 = len(rx.blocks)
        await feed_blocks(ctx, bench, model_tx, [idle_block()] * 40,
                          rx, hm)
        ts1_after = count_ts(BlockType.TS1, mark3)
        if ts1_after:
            print(f"ADVEARLY FAIL: pass {n} k={k}.{sub}: {ts1_after} "
                  f"device TS1 blocks in the aftermath window (device-"
                  f"initiated recovery after the early advertisement)")
            return False
        print(f"ADVEARLY: pass {n} (k={k}.{sub}) complete")

    if host.errors:
        print(f"ADVEARLY FAIL: parser errors: {host.errors[:6]}")
        return False
    print(f"ADVEARLY: {len(offsets)} early-advertisement offsets all "
          f"captured; traffic resumed with preserved numbering each "
          f"time")
    return True


async def run_u0_checks(ctx, bench, hm, rx, model_tx):
    """STRICT U0 host behaviors the enum/echo phases never exercised
    (HANDOVER 10s suspects 1-3: the sim-uncovered surface where the H2
    silicon U0-death must live if it is above the PHY):

    1. the device's link-up Port Capability LMP field conformance at
       SSP operation [8.4.5, Table 8-7: link_speed and num_hp_buffers
       are RESERVED-0 when not operating at Gen 1x1];
    2. inbound host Port Capability + Port Configuration LMPs with the
       SSP field rules (link_speed=0 [Table 8-9]); REQUIRED Port
       Configuration Response with Response Code reserved-0 [Table
       8-10] -- a nonzero code reads as "Link Speed rejected" at the
       DFP, which then signals a port error [8.4.7, 10.16.2.6]: the
       exact walk-the-link-down symptom;
    3. inbound ITPs: broadcast, link-level ack only, no protocol
       response [8.7];
    4. LUP keepalives while the link idles in U0: one within every
       tU0LTimeout = 10 us, else the DFP goes to Recovery [7.5.6.1];
    5. a closing SET_ADDRESS: the link must still work after all of
       the above.

    Conformance violations are COLLECTED (not aborted on) so a single
    red run reports the full surface; link-liveness failures abort."""
    from sim_link_loopback import frame_lmp, frame_itp, frame_out_dp
    host = Gen2LinkHost(ctx, bench, hm, rx, model_tx, tag="U0")
    failures = []

    # ── advertisement exchange (same shape as run_enum's front) ──
    ev = await host.expect("LGOOD advertisement",
                           lambda e: e[0] == 'lc' and e[1] == 0b0000)
    if ev is None:
        return False
    # STRICT: the full 4+4 credit advertisement (see run_enum; the
    # host's Type 1/Type 2 CREDIT_HP_TIMERs only clear at count 4).
    adv = []
    for _ in range(8):
        ev = await host.expect(
            "credit advertisement (Type 1/2 CREDIT_HP_TIMER pending)",
            lambda e: e[0] == 'lc' and e[1] == 0b0001)
        if ev is None:
            print("U0 FAIL: Type 1/Type 2 CREDIT_HP_TIMER would expire "
                  "-> Recovery [7.2.4.1.1 rule 2.e.1, 7.3.9]: 4 credits "
                  "per class required at Gen 2x1")
            return False
        adv.append(ev[2])
    if [c & 3 for c in adv if not (c & 4)] != [0, 1, 2, 3] or \
            [c & 3 for c in adv if c & 4] != [0, 1, 2, 3]:
        print(f"U0 FAIL: advertisement {['%#x' % c for c in adv]} is not "
              f"LCRD1_A..D + LCRD2_A..D [7.2.4.1.1 rules 2.e.1 + 3.d]")
        return False
    syms = link_command_syms(0b0000, 15)
    for i in range(4):
        syms += link_command_syms(0b0001, i)              # LCRD1_x
    for i in range(4):
        syms += link_command_syms(0b0001, 0b0100 | i)     # LCRD2_x
    await host.send_syms(syms)

    dev_seq = 0
    host_seq = 0
    ret_idx = {1: 0, 2: 0}

    async def return_credit(series):
        sub = (0b0100 if series == 2 else 0) | ret_idx[series]
        ret_idx[series] = (ret_idx[series] + 1) & 3
        await host.send_lc(0b0001, sub)

    async def ack_device_header(ev):
        nonlocal dev_seq
        if ev[2] != dev_seq:
            print(f"U0 FAIL: device header seq {ev[2]}, expected {dev_seq}")
            return False
        dev_seq = (dev_seq + 1) & 0xF
        await host.send_lc(0b0000, ev[2])
        await return_credit(2 if (ev[1][0] & 0x1F) == 8 else 1)
        return True

    async def expect_lgood_and_credit(what, series):
        nonlocal host_seq
        ev = await host.expect(f"LGOOD_{host_seq} ({what})",
                               lambda e: e[0] == 'lc' and e[1] == 0b0000)
        if ev is None:
            return False
        if ev[2] != host_seq:
            print(f"U0 FAIL: LGOOD_{ev[2]} for {what}, expected "
                  f"LGOOD_{host_seq}")
            return False
        host_seq = (host_seq + 1) & 0xF
        ev = await host.expect(f"LCRD{series} return ({what})",
                               lambda e: e[0] == 'lc' and e[1] == 0b0001)
        if ev is None:
            return False
        got = 2 if ev[2] & 0x4 else 1
        if got != series:
            print(f"U0 FAIL: LCRD{got} return for {what}, expected "
                  f"LCRD{series}")
            return False
        return True

    # ── 1. the device's link-up Port Capability LMP [8.4.5] ──
    ev = await host.expect("link-up Port Capability LMP",
                           lambda e: e[0] == 'hdr'
                           and (e[1][0] & 0x1F) == 0)
    if ev is None:
        return False
    dw0, dw1 = ev[1][0], ev[1][1]
    subtype = (dw0 >> 5) & 0xF
    if subtype != 4:
        failures.append(f"link-up LMP subtype {subtype}, expected "
                        f"Port Capability (4) [8.4.5]")
    link_speed = (dw0 >> 9) & 0x7F
    num_hp = dw1 & 0xFF
    if link_speed != 0 or num_hp != 0:
        failures.append(
            f"Port Capability LMP carries Gen 1x1-only field values at "
            f"SSP operation: link_speed={link_speed} "
            f"num_hp_buffers={num_hp} (both RESERVED, shall be 0, when "
            f"not operating at Gen 1x1) [Table 8-7]")
    if not await ack_device_header(ev):
        return False
    print(f"U0: device Port Capability LMP (dw0={dw0:08x} dw1={dw1:08x})")

    # ── 2. host LMPs: Port Capability, then Port Configuration ──
    # (SSP field rules: link_speed=0, num_hp_buffers=0 [Tables 8-7/8-9];
    # direction: downstream-capable.)
    await host.send_frame(frame_lmp(4, dw1=(1 << 16)))
    if not await expect_lgood_and_credit("host Port Capability LMP", 1):
        return False

    await host.send_frame(frame_lmp(5))          # link_speed = 0 at SSP
    if not await expect_lgood_and_credit("host Port Configuration LMP", 1):
        return False

    ev = await host.expect("Port Configuration Response LMP [8.4.7]",
                           lambda e: e[0] == 'hdr'
                           and (e[1][0] & 0x1F) == 0
                           and ((e[1][0] >> 5) & 0xF) == 6)
    if ev is None:
        print("U0 FAIL: no Port Configuration Response LMP within "
              "timeout; the DFP signals a port error without it "
              "[8.4.7, 10.16.2.6]")
        return False
    code = (ev[1][0] >> 9) & 0x7F
    if code != 0:
        failures.append(
            f"Port Configuration Response code {code:#x} at SSP "
            f"operation: the field is RESERVED-0 when not operating at "
            f"Gen 1x1 [Table 8-10]; bit1 set / bit0 clear reads as "
            f"'Link Speed rejected' -> DFP port error [10.16.2.6]")
    if not await ack_device_header(ev):
        return False
    print(f"U0: device Port Configuration Response (code={code:#x})")

    # ── 3. inbound ITPs: link-level ack only, no protocol response ──
    for k in range(3):
        await host.send_frame(frame_itp(12500 * (k + 1)))
        if not await expect_lgood_and_credit(f"ITP #{k + 1}", 1):
            return False
    ev = await host.expect("no response to ITPs",
                           lambda e: e[0] == 'hdr',
                           timeout_blocks=200, quiet=True)
    if ev is not None:
        failures.append(
            f"device responded to an ITP with a header packet "
            f"(dw0={ev[1][0]:08x}); a device shall not respond to an "
            f"ITP [8.7]")
    print("U0: 3 ITPs delivered (link-level acks only)")

    # ── 4. LUP keepalives on an idle U0 link [7.5.6.1] ──
    # tU0LTimeout = 10 us = 1562 ss cycles at 156.25 MHz; feed_blocks
    # advances one device cycle per fed beat (2 beats per block).  32 us
    # of link idle must carry >= 2 LUPs (one per timeout, restarted by
    # its own transmission).
    host.events = [e for e in host.events if not
                   (e[0] == 'lc' and e[1] == 0b1000)]
    # One device cycle per fed BEAT: 2 beats/block at W64, 1 at W128.
    idle_blocks = int(32 * US / (1 if W128 else 2))
    for _ in range(idle_blocks // 8):
        await feed_blocks(ctx, bench, model_tx, [idle_block()] * 8,
                          rx, hm)
    host.pump()
    lups = [e for e in host.events if e[0] == 'lc' and e[1] == 0b1000]
    host.events = [e for e in host.events if not
                   (e[0] == 'lc' and e[1] == 0b1000)]
    print(f"U0: {len(lups)} LUP keepalives in 32 us of link idle")
    if len(lups) < 2:
        failures.append(
            f"only {len(lups)} LUP keepalives in 32 us of idle U0; an "
            f"upstream port shall transmit LUP on every tU0LTimeout "
            f"(10 us) expiry [7.5.6.1] -- the DFP transitions to "
            f"Recovery after 1 ms without any link command")

    # ── 5. the link must still work: SET_ADDRESS(1) ──
    setup = bytes([0x00, 0x05, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00])
    await host.send_frame(frame_out_dp(0, 0, setup, setup=1, address=0))
    if not await expect_lgood_and_credit("SETUP DP", 2):
        return False
    ev = await host.expect("SETUP ACK TP",
                           lambda e: e[0] == 'hdr'
                           and (e[1][0] & 0x1F) == 4)
    if ev is None:
        return False
    if not await ack_device_header(ev):
        return False
    print("U0: SET_ADDRESS SETUP acked -- link alive after the U0 "
          "traffic surface")

    if host.errors:
        print(f"U0 FAIL: parser errors: {host.errors[:6]}")
        return False
    if failures:
        for f in failures:
            print(f"U0 FAIL: {f}")
        return False
    print("U0: LUP keepalives, host LMP/ITP tolerance, SSP LMP field "
          "rules -- all verified at Gen2")
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
        elif PHASE == "lbpm-x2":
            result["ok"] = await phase_lbpm_x2(ctx, bench)
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
        elif PHASE == "u0":
            result["ok"] = await phase_train(ctx, bench, u0_checks=True)
        elif PHASE in ("hotreset", "hotreset-parked"):
            result["ok"] = await phase_train(ctx, bench, hot_reset=True)
        elif PHASE == "recovery":
            result["ok"] = await phase_train(ctx, bench, recovery=True)
        elif PHASE == "reccut":
            result["ok"] = await phase_train(ctx, bench, reccut=True)
        elif PHASE == "advearly":
            result["ok"] = await phase_train(ctx, bench, advearly=True)
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
