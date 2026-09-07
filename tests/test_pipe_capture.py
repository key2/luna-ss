# Copyright (c) 2026 luna-ss contributors
# SPDX-License-Identifier: BSD-3-Clause
"""Cycle-exact PIPE rings and wire-level UART dumps on independent clocks.

Run only this suite with:
    .venv/bin/python -u -m pytest tests/test_pipe_capture.py
"""

import importlib.util
from pathlib import Path

import pytest
from amaranth import ClockDomain, ClockSignal, Elaboratable, Module, ResetSignal, Signal
from amaranth.sim import Simulator


_path = (Path(__file__).resolve().parents[1]
         / "examples/gowin/luna-enum-gen2/pipe_capture.py")
_spec = importlib.util.spec_from_file_location("pipe_capture", _path)
_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_module)
PipeBeatCapture = _module.PipeBeatCapture

DIVISOR = 4
MASK24 = (1 << 24) - 1
FIELDS = ("data", "datavalid", "start_block", "sync_header",
          "fifo_level", "tx_state", "context")


@pytest.mark.parametrize("fall_offset", [-3, -2, -1, 0, 1, 3])
def test_core_trigger_pipeline_retains_fall_and_does_not_double_pulse(fall_offset):
    class Events(Elaboratable):
        def __init__(self):
            self.long = Signal()
            self.trained = Signal()
            self.events = Signal(2)

        def elaborate(self, platform):
            m = Module()
            m.domains += [ClockDomain("ss"), ClockDomain("core")]
            phase = Signal()
            m.d.ss += phase.eq(~phase)
            m.d.comb += ClockSignal("core").eq(phase)
            events, _ = _module.capture_events(m, self.long, self.trained)
            m.d.comb += self.events.eq(events)
            return m

    dut = Events()
    sim = Simulator(dut)
    sim.add_clock(6.4e-9, domain="ss")
    counts = [0, 0]

    async def source(ctx):
        for cycle in range(24):
            ctx.set(dut.long, cycle == 8)
            ctx.set(dut.trained, cycle < 8 + fall_offset)
            await ctx.tick("core")
        assert counts == [1, 1], "core pulses must become exactly one pclk event"

    async def monitor(ctx):
        while True:
            _, _, events = await ctx.tick("ss").sample(dut.events)
            for bit in range(2):
                counts[bit] += (events >> bit) & 1

    sim.add_testbench(source)
    sim.add_testbench(monitor, background=True)
    sim.run()


class CaptureHarness(Elaboratable):
    def __init__(self, dut):
        self.dut = dut
        self.ss_run = Signal(init=1)
        self.dbg_run = Signal(init=1)
        self.ss_reset = Signal()

    def elaborate(self, platform):
        m = Module()
        m.domains += [ClockDomain("ss"), ClockDomain("dbg", reset_less=True),
                      ClockDomain("ss_clock", reset_less=True),
                      ClockDomain("dbg_clock", reset_less=True)]
        # Test-only clock gating permits either side of a handshake to stop.
        m.d.comb += [
            ClockSignal("ss").eq(ClockSignal("ss_clock") & self.ss_run),
            ClockSignal("dbg").eq(ClockSignal("dbg_clock") & self.dbg_run),
            ResetSignal("ss").eq(self.ss_reset),
        ]
        m.submodules.capture = self.dut
        return m


def run_capture(dut, body, *, background=None, ss_period=10e-9, dbg_period=17e-9):
    harness = CaptureHarness(dut)
    wire = bytearray()
    sim = Simulator(harness)
    sim.add_clock(ss_period, phase=ss_period * 0.3, domain="ss_clock")
    sim.add_clock(dbg_period, phase=dbg_period * 0.4, domain="dbg_clock")

    async def uart_receiver(ctx):
        # Decode tx_o itself at bit centers, not the transmitter's byte interface.
        bit_period = dbg_period * DIVISOR
        while True:
            await ctx.negedge(dut.tx_o)
            await ctx.delay(1.5 * bit_period)
            value = 0
            for bit in range(8):
                value |= ctx.get(dut.tx_o) << bit
                await ctx.delay(bit_period)
            assert ctx.get(dut.tx_o) == 1, "UART stop bit missing"
            wire.append(value)

    async def stimulus(ctx):
        await body(ctx, harness, wire)

    if background is not None:
        async def background_stimulus(ctx):
            await background(ctx, harness)
        sim.add_testbench(background_stimulus, background=True)
    sim.add_testbench(uart_receiver, background=True)
    sim.add_testbench(stimulus)
    sim.run()


def fields(cycle):
    return (((cycle + 1) * 0x9E3779B97F4A7C15) & ((1 << 64) - 1),
            int(cycle % 3 != 0), int(cycle % 2 == 0), (cycle * 5 + 3) & 15,
            (cycle * 7 + 1) & 31, (cycle * 1237 ^ 0xA56C) & 0xFFFF,
            (cycle * 11 + 0x80) & 0xFF)


def drive_fields(ctx, dut, values):
    for name, value in zip(FIELDS, values):
        ctx.set(getattr(dut, name), value)


def packed(values, timestamp):
    data, dv, start, head, level, state, context = values
    flags = dv | (start << 1) | (head << 2) | (level << 6)
    return (data | (flags << 64) | (state << 80) | (context << 96)
            | (timestamp << 104))


async def beat(ctx, dut, cycle, triggers=0):
    values = fields(cycle)
    drive_fields(ctx, dut, values)
    ctx.set(dut.triggers, triggers)
    timestamp = ctx.get(dut.timestamp)
    await ctx.tick("ss")
    return packed(values, timestamp)


async def command(ctx, dut, char):
    assert ctx.get(dut.command_ready), "test command queue unexpectedly full"
    ctx.set(dut.command, ord(char))
    ctx.set(dut.command_strobe, 1)
    await ctx.tick("dbg")
    ctx.set(dut.command_strobe, 0)
    await ctx.tick("dbg")


async def wait_for(ctx, predicate, *, domain="dbg", limit=60000):
    for _ in range(limit):
        if predicate():
            return
        await ctx.tick(domain)
    assert predicate(), "capture/command/UART operation did not finish within its bound"


def frame_bytes(generation, records, trigger_index, reason, mode, depth, post):
    result = (f"P1 {generation:08x} {len(records):04x} {trigger_index:04x} "
              f"{reason:x} {mode:x} {post:04x} {depth:04x}\r\n")
    for index, record in enumerate(records):
        result += f"R {generation:08x} {index:04x} {record:032x}\r\n"
    result += f"E {generation:08x}\r\n"
    return result.encode("ascii")


@pytest.mark.parametrize("depth,post,pre,initial_timestamp", [
    (8, 3, 1, 0),                 # partial ring
    (8, 3, 21, MASK24 - 3),       # multiple wraps, invalid trigger beat, timestamp wrap
    (8, 0, 0, 0),                # trigger is also the last beat
    (8, 7, 12, 0),               # all prehistory must give way to trigger + post
    (1, 0, 0, 0),                # smallest legal ring
])
def test_ring_freeze_and_uart_replay(depth, post, pre, initial_timestamp):
    dut = PipeBeatCapture(4_000_000, baud=1_000_000, depth=depth, post_trigger=post)

    async def body(ctx, harness, wire):
        ctx.set(dut.timestamp, initial_timestamp)
        recorded = []
        for cycle in range(pre + post + 1):
            ctx.set(harness.ss_reset, int(cycle == pre + 1))
            triggers = 1 if cycle in (pre, pre + 1, pre + post) else 2
            recorded.append(await beat(ctx, dut, cycle, triggers))
            assert ctx.get(dut.count) == min(cycle + 1, depth), (
                "every pclk beat, including dv=0, must be retained")
            assert ctx.get(dut.timestamp) == (initial_timestamp + cycle + 1) & MASK24
            assert ctx.get(dut.triggered) == int(cycle >= pre)
            assert ctx.get(dut.frozen) == int(cycle == pre + post), (
                "freeze must include the trigger and exactly post_trigger later beats")
        ctx.set(harness.ss_reset, 0)
        expected_index = min(pre, depth - post - 1)
        assert ctx.get(dut.trigger_index) == expected_index
        assert ctx.get(dut.reason) == 1
        assert ctx.get(dut.mode) == 0
        assert ctx.get(dut.generation) == 0
        saved_count = ctx.get(dut.count)
        for cycle in range(40):
            await beat(ctx, dut, 500 + cycle, 3)
            assert ctx.get(dut.frozen) and ctx.get(dut.triggered)
            assert ctx.get(dut.count) == saved_count
            assert ctx.get(dut.trigger_index) == expected_index
            assert ctx.get(dut.reason) == 1

        expected = frame_bytes(0, recorded[-depth:], expected_index, 1, 0, depth, post)
        await wait_for(ctx, lambda: wire.endswith(b"E 00000000\r\n"))
        assert bytes(wire) == expected
        await ctx.tick("dbg").repeat(500)
        assert bytes(wire) == expected, "auto-dump must not repeat indefinitely"

        # Even an asserted ss reset must not wipe the frozen ring or its read handshake.
        ctx.set(harness.ss_reset, 1)
        await command(ctx, dut, "D")
        await wait_for(ctx, lambda: len(wire) >= 2 * len(expected))
        assert bytes(wire) == expected * 2
        assert ctx.get(dut.frozen) and ctx.get(dut.count) == saved_count
        assert ctx.get(dut.command_overflow) == 0

    run_capture(dut, body)


def test_default_128_by_96_window():
    dut = PipeBeatCapture(4_000_000, baud=1_000_000)

    async def body(ctx, harness, wire):
        assert dut.depth == 128 and dut.post_trigger == 96
        for cycle in range(100):
            await beat(ctx, dut, cycle, int(cycle == 3))
            assert ctx.get(dut.frozen) == int(cycle == 99)
            assert ctx.get(dut.count) == cycle + 1
        assert ctx.get(dut.trigger_index) == 3
        assert ctx.get(dut.reason) == 1

    run_capture(dut, body)


def test_no_trigger_commands_modes_and_rearm():
    depth, post = 8, 2
    dut = PipeBeatCapture(4_000_000, baud=1_000_000, depth=depth, post_trigger=post)

    async def body(ctx, harness, wire):
        for cycle in range(depth * 4):
            await beat(ctx, dut, cycle, 2)   # unselected retraining trigger
        for char in ("R", "?", "T", "D"):
            await command(ctx, dut, char)
            await ctx.tick("dbg").repeat(30)
        assert not ctx.get(dut.triggered) and not ctx.get(dut.frozen)
        assert ctx.get(dut.count) == depth
        assert ctx.get(dut.generation) == 0 and ctx.get(dut.mode) == 0
        assert ctx.get(dut.reason) == 0 and bytes(wire) == b""

        for generation, (char, mode) in enumerate((("1", 1), ("A", 1),
                                                   ("2", 2), ("0", 0)), start=1):
            ctx.set(dut.triggers, 0)
            await command(ctx, dut, char)
            await wait_for(ctx, lambda: ctx.get(dut.generation) == generation)
            assert ctx.get(dut.mode) == mode
            assert not ctx.get(dut.triggered) and not ctx.get(dut.frozen)
            assert ctx.get(dut.reason) == 0
            wrong_trigger = 3 if mode == 2 else (1 if mode == 1 else 2)
            for cycle in range(8):
                await beat(ctx, dut, generation * 100 + cycle, wrong_trigger)
                assert not ctx.get(dut.triggered)

            await command(ctx, dut, "T")
            if mode == 2:
                await wait_for(ctx, lambda: ctx.get(dut.triggered), domain="ss", limit=100)
            else:
                for cycle in range(20):
                    await beat(ctx, dut, generation * 100 + 10 + cycle, wrong_trigger)
                    assert not ctx.get(dut.triggered), "T must only fire in manual mode"
                await beat(ctx, dut, generation * 100 + 40, 1 << mode)
            assert ctx.get(dut.triggered) and not ctx.get(dut.frozen)
            assert ctx.get(dut.reason) == mode + 1
            for offset in range(1, post + 1):
                await beat(ctx, dut, generation * 100 + 40 + offset, 3)
                assert ctx.get(dut.frozen) == int(offset == post)
            assert ctx.get(dut.trigger_index) == depth - post - 1

        await wait_for(ctx, lambda: wire.endswith(b"E 00000004\r\n"))
        last_frame = bytes(wire)[wire.rfind(b"P1 "):]
        assert last_frame.startswith(b"P1 00000004 0008 0005 1 0 0002 0008\r\n")
        assert len(last_frame.splitlines()) == depth + 2
        assert ctx.get(dut.command_overflow) == 0

    run_capture(dut, body)


def test_paused_clocks_rearm_abort_and_no_stale_epoch_entries():
    depth, post = 16, 2
    dut = PipeBeatCapture(4_000_000, baud=1_000_000, depth=depth, post_trigger=post)
    snapshots = {}

    async def source(ctx, harness):
        cycle = 0
        history = []
        trigger_position = None
        while True:
            values = fields(cycle)
            drive_fields(ctx, dut, values)
            timestamp = ctx.get(dut.timestamp)
            generation = ctx.get(dut.generation)
            frozen, triggered = ctx.get(dut.frozen), ctx.get(dut.triggered)
            await ctx.tick("ss")
            assert ctx.get(dut.timestamp) == (timestamp + 1) & MASK24
            if ctx.get(dut.generation) != generation:
                history = []
                trigger_position = None
                assert ctx.get(dut.count) == 0, "rearm must invalidate all old RAM entries"
                assert not ctx.get(dut.triggered) and not ctx.get(dut.frozen)
            elif not frozen:
                history.append(packed(values, timestamp))
                assert ctx.get(dut.count) == min(len(history), depth)
                if ctx.get(dut.triggered) and not triggered:
                    trigger_position = len(history) - 1
                if trigger_position is not None:
                    assert ctx.get(dut.frozen) == int(
                        len(history) - 1 == trigger_position + post)
                if ctx.get(dut.frozen):
                    records = history[-depth:]
                    index = trigger_position - (len(history) - len(records))
                    snapshots[generation] = (records, index)
                    assert ctx.get(dut.trigger_index) == index
            cycle += 1

    async def body(ctx, harness, wire):
        ctx.set(harness.dbg_run, 0)
        await ctx.tick("ss").repeat(35)
        ctx.set(dut.triggers, 1)
        await ctx.tick("ss")
        ctx.set(dut.triggers, 0)
        await wait_for(ctx, lambda: ctx.get(dut.frozen), domain="ss", limit=5)
        assert bytes(wire) == b"" and ctx.get(dut.generation) == 0

        ctx.set(harness.ss_run, 0)
        ctx.set(harness.dbg_run, 1)
        await ctx.tick("dbg").repeat(100)
        assert bytes(wire) == b"", "a paused source cannot acknowledge a snapshot"
        assert ctx.get(dut.frozen) and ctx.get(dut.count) == depth
        ctx.set(harness.ss_run, 1)
        await wait_for(ctx, lambda: b"R 00000000 0000 " in wire)

        # Rearm arrives in the middle of a record. It must cancel the queued
        # old replay, then deliver the mode change before the queued manual fire.
        ctx.set(harness.ss_run, 0)
        await command(ctx, dut, "D")
        await command(ctx, dut, "2")
        await command(ctx, dut, "T")
        await wait_for(ctx, lambda: wire.endswith(b"X 00000000\r\n"))
        assert ctx.get(dut.generation) == 0 and ctx.get(dut.frozen)
        await ctx.tick("dbg").repeat(50)
        assert wire.endswith(b"X 00000000\r\n")
        ctx.set(harness.ss_run, 1)
        await wait_for(ctx, lambda: wire.endswith(b"E 00000001\r\n"))
        assert ctx.get(dut.mode) == 2 and ctx.get(dut.reason) == 3
        assert ctx.get(dut.command_overflow) == 0

        old, new = bytes(wire).split(b"X 00000000\r\n")
        old_records, old_index = snapshots[0]
        old_expected = frame_bytes(0, old_records, old_index, 1, 0, depth, post)
        # The partial old frame ends on a complete line, never half a record.
        assert old.endswith(b"\r\n") and old_expected.startswith(old)
        assert len(old.splitlines()) == 2, "only the in-flight old record may finish"
        records, index = snapshots[1]
        assert post + 1 <= len(records) < depth, "new capture must exercise partial-fill gating"
        assert new == frame_bytes(1, records, index, 3, 2, depth, post)
        expected_wire = bytes(wire)
        await ctx.tick("dbg").repeat(500)
        assert bytes(wire) == expected_wire

    run_capture(dut, body, background=source, ss_period=19e-9, dbg_period=7e-9)
