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

# ss clock: 156.25 MHz (the Gen2 operating point)
CLK = 156.25e6
US = int(CLK / 1e6)              # cycles per microsecond (156)


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

        usb = USBSuperSpeedDevice(phy=self.pipe, sync_frequency=CLK,
                                  gen2=True)
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
