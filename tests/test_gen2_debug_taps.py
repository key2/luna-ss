# amaranth: UnusedElaboratable=no
# Copyright (c) 2026 the luna-ss contributors
# SPDX-License-Identifier: BSD-3-Clause
"""The hardware discriminator must observe whole accepted MAC beats."""

import importlib.util
import json
from pathlib import Path

import pytest
from amaranth import Module
from amaranth.hdl import Fragment
from amaranth.sim import Simulator

from luna.gateware.interface.pipe import PIPEInterface
from luna.gateware.usb.usb3.device import USBSuperSpeedDevice
from luna.gateware.usb.usb3.physical.gen2 import Gen2BlockTransmitter


@pytest.fixture
def board(monkeypatch):
    path = Path(__file__).resolve().parents[1] / "examples/gowin/luna-enum-gen2"
    monkeypatch.syspath_prepend(str(path))
    spec = importlib.util.spec_from_file_location("gen2_board_test", path / "top.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize("width", [64, 128])
@pytest.mark.parametrize("gen2", [False, True])
def test_device_wire_tap_width(width, gen2):
    dut = USBSuperSpeedDevice(phy=PIPEInterface(width=width // 8),
                             core_width=width, gen2=gen2)
    assert len(dut.debug_wire_tx_data) == width // 2
    assert len(dut.debug_wire_tx_ctrl) == width // 16


def test_wide_scheduler_state_is_registered_and_passive():
    dut = Gen2BlockTransmitter(words=2, tseq_count=4)
    sim = Simulator(dut)
    sim.add_clock(12.8e-9, domain="ss")

    async def bench(ctx):
        ctx.set(dut.idle_mode, 1)
        await ctx.tick("ss").repeat(8)
        assert ctx.get(dut.debug_state) & 1             # active
        assert ctx.get(dut.debug_state) & (1 << 12)     # idle request
        assert not ctx.get(dut.debug_state) & (1 << 5)  # not paced
        ctx.set(dut.tx_fifo_level, 16)
        await ctx.tick("ss").repeat(2)
        assert ctx.get(dut.debug_state) & (1 << 5)
        assert not ctx.get(dut.tx_valid)
        ctx.set(dut.tx_fifo_level, 0)
        await ctx.tick("ss").repeat(2)
        assert ctx.get(dut.tx_valid)

    sim.add_testbench(bench)
    sim.run()


def test_board_training_decode_stops_at_a_core_register(board, monkeypatch):
    bridges = []
    factory = board.PIPEBridge2to1

    def bridge_factory(**kwargs):
        result = factory(**kwargs)
        bridges.append(result)
        return result

    monkeypatch.setattr(board, "PIPEBridge2to1", bridge_factory)
    fragment = Fragment.get(board.LunaEnumTop(), board.DKUSBGW5AT60Platform())
    training = bridges[0].ltssm_training
    writes = [statement for statement in fragment.statements.get("core", ())
              if any(signal is training for signal in statement._lhs_signals())]
    assert len(writes) == 1, "training decode crosses directly into the 6.4 ns pclk seam"
    assert not any(signal is training for statement in fragment.statements["comb"]
                   for signal in statement._lhs_signals())

    # Simulate the actual extracted board assignment, not a duplicate model.
    m = Module()
    m.d.core += writes[0]
    sim = Simulator(m)
    sim.add_clock(12.8e-9, domain="core")

    async def bench(ctx):
        for value in (1, 0, 1):
            before = ctx.get(training)
            ctx.set(writes[0].rhs, value)
            await ctx.delay(1e-9)
            assert ctx.get(training) == before
            await ctx.tick("core")
            assert ctx.get(training) == value

    sim.add_testbench(bench)
    sim.run()


@pytest.mark.parametrize("bad", ["cross_setup", "cross_hold", "frequency", "summary", None])
def test_flash_requires_full_timing_closure(board, monkeypatch, tmp_path, bad):
    build = tmp_path / "build"
    build.mkdir()
    (build / "luna_enum_gen2.fs").write_bytes(b"test image, never sent to hardware")
    monkeypatch.setattr(board, "HERE", tmp_path)
    report = {
        "fmax": [{"clock_name": name, "actual_fmax_mhz": value + 1}
                 for name, value in (("core_clk", 78.125), ("pclk", 156.25), ("rxclk", 161.29))],
        "tns": [{"endpoints_tns": 0}],
        "setup_slack": [{"slack_ns": 0.1}],
        "hold_slack": [{"slack_ns": 0.1}],
        "sta_summary": {"Numbers of Setup Violated Endpoints": "0",
                        "Numbers of Hold Violated Endpoints": "0"},
    }
    if bad == "cross_setup":
        report["setup_slack"][0]["slack_ns"] = -0.01
    elif bad == "cross_hold":
        report["hold_slack"][0]["slack_ns"] = -0.433
    elif bad == "frequency":
        report["fmax"][0]["actual_fmax_mhz"] = 77
    elif bad == "summary":
        report["sta_summary"]["Numbers of Hold Violated Endpoints"] = "76"
    monkeypatch.setattr(board.subprocess, "check_output", lambda *a, **k: json.dumps(report))
    calls = []
    monkeypatch.setattr(board.subprocess, "check_call", lambda command: calls.append(command))
    if bad:
        with pytest.raises(SystemExit, match="timing"):
            board.flash()
        assert not calls, "an unsafe image reached the programmer"
    else:
        board.flash()
        assert len(calls) == 1
        assert calls[0][0] == "openFPGALoader"


@pytest.mark.parametrize("program", [False, True])
def test_gen2_build_explicitly_sets_pnr_options(board, monkeypatch, program):
    calls = []

    class Plan:
        files = {"luna_enum_gen2.tcl": "set_option -bit_encrypt 0\nrun all\n"}

        def execute_local(self, directory):
            text = self.files["luna_enum_gen2.tcl"]
            assert "set_option -bit_encrypt 0" in text
            assert "set_option -place_option 0 -route_option 1 -timing_driven 1" in text
            assert "set_option -clock_route_order 1 -route_maxfan 23" in text
            assert text.count("run all") == 1
            calls.append("build")
            return "products"

    class Platform:
        def add_file(self, *args):
            pass

        def build(self, design, **kwargs):
            assert kwargs.get("do_build") is False, "P&R ran before explicit options were set"
            return Plan()

        def toolchain_program(self, products, name):
            assert calls[-1] == "gate"
            assert products == "products" and name == "luna_enum_gen2"
            calls.append("program")

    monkeypatch.setattr(board, "generate_serdes_files", lambda: None)
    monkeypatch.setattr(board, "_setup_gowin_env", lambda platform: None)
    monkeypatch.setattr(board, "DKUSBGW5AT60Platform", Platform)
    monkeypatch.setattr(board, "require_timing_met", lambda: calls.append("gate"), raising=False)
    board.build(do_program=program)
    assert calls == (["build", "gate", "program"] if program else ["build"])
