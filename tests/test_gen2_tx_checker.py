# Copyright (c) 2026 luna-ss contributors
# SPDX-License-Identifier: BSD-3-Clause
"""Accepted-MAC TX monitor fences, without a PHY, build, or hardware.

The software CRC oracles are independent of the gateware equations. The
older sim_link_loopback CRC helpers invoke those equations, so deliberately
do not serve as this checker's oracle. The real-transmitter test also checks
every accepted beat against the software encoder, not just checker pulses.
"""

import importlib.util
from pathlib import Path
import zlib

import pytest
from amaranth import DomainRenamer
from amaranth.sim import Simulator

from luna.gateware.usb.usb3.link.transmitter import RawPacketTransmitter


_CHECKER_PATH = (Path(__file__).resolve().parents[1]
                 / "examples/gowin/luna-enum-gen2/tx_checker.py")
_SPEC = importlib.util.spec_from_file_location("gen2_tx_checker", _CHECKER_PATH)
_MODULE = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_MODULE)
Gen2TxWireChecker = _MODULE.Gen2TxWireChecker

HPSTART = 0xF7FBFBFB
SDP = 0xF75C5C5C
END = 0xF7FDFDFD
EDB = 0xF77C7C7C
LCSTART = 0xF7FEFEFE
PULSES = (
    "tp_seen", "dph_seen", "dpp_seen", "long_dph", "framing_error",
    "crc_error", "header_error", "lc_seen", "lc_error", "abort_seen",
    "cap_strobe",
)
ERRORS = ("framing_error", "crc_error", "header_error", "lc_error")
LENGTHS = list(range(25)) + [50, 1024]
_SIMULATORS = {}


def _crc_bits(value, count, width, reflected_polynomial):
    crc = (1 << width) - 1
    for bit in range(count):
        feedback = (crc ^ (value >> bit)) & 1
        crc >>= 1
        if feedback:
            crc ^= reflected_polynomial
    return crc ^ ((1 << width) - 1)


def _crc5(value):
    return _crc_bits(value, 11, 5, 0x14)  # Reflected USB polynomial 0x05.


def _header(dw0, dw1, dw2, *, delayed=False):
    covered = dw0 | (dw1 << 32) | (dw2 << 64)
    crc16 = _crc_bits(covered, 96, 16, 0xD008)  # Reflected USB3 0x100B.
    link = 3 | (int(delayed) << 9)
    dw3 = crc16 | (link << 16) | (_crc5(link) << 27)
    is_data = (dw0 & 0x1F) == 8
    return [
        (HPSTART | (dw0 << 32), 0x0F),
        (dw1 | (dw2 << 32), 0),
        (dw3 | ((SDP if is_data else 0) << 32), 0xF0 if is_data else 0),
    ]


def _fields(payload, ep=0):
    if payload is None:
        dw0 = 4 | (1 << 25)
        dw1 = 1 | (1 << 7) | (ep << 8) | (3 << 16) | (5 << 21)
    else:
        dw0 = 8 | (1 << 25)
        dw1 = 5 | (1 << 7) | (ep << 8) | (len(payload) << 16)
    return dw0, dw1, 0x10234567


def _packet(payload=None, *, ep=0, delayed=False, abort=False):
    beats = _header(*_fields(payload, ep), delayed=delayed)
    if payload is None:
        return beats
    if abort:
        return beats + [(EDB, 0x0F)]
    body = payload + zlib.crc32(payload).to_bytes(4, "little")
    body += END.to_bytes(4, "little")
    controls = [0] * (len(payload) + 4) + [1] * 4
    for offset in range(0, len(body), 8):
        data = int.from_bytes(body[offset:offset + 8], "little")
        ctrl = sum(c << lane for lane, c in enumerate(controls[offset:offset + 8]))
        beats.append((data, ctrl))
    return beats


def _lc(command=1, subtype=0):
    word = subtype | (command << 7)
    word |= _crc5(word) << 11
    return (LCSTART | (word << 32) | (word << 48), 0x0F)


def _payload(length):
    return bytes((index * 71 + length * 13) & 0xFF for index in range(length))


def _flip(beats, byte_offset, *, data=0, ctrl=False):
    result = list(beats)
    beat, lane = divmod(byte_offset, 8)
    old_data, old_ctrl = result[beat]
    result[beat] = (old_data ^ (data << (8 * lane)), old_ctrl ^ (int(ctrl) << lane))
    return result


def _accepted(beats):
    return [(data, ctrl, 1, 1) for data, ctrl in beats]


def _empty_trace():
    return {name: [] for name in PULSES} | {"caps": [], "sticky": []}


def _record(ctx, dut, trace):
    cycle = len(trace["sticky"])
    for name in PULSES:
        if ctx.get(getattr(dut, name)):
            trace[name].append(cycle)
    if ctx.get(dut.cap_strobe):
        trace["caps"].append((cycle, ctx.get(dut.cap_type), ctx.get(dut.cap_dw1)))
    sticky = {name: ctx.get(getattr(dut, name + "_sticky")) for name in ERRORS}
    trace["sticky"].append(sticky)
    assert ctx.get(dut.error_sticky) == int(any(sticky.values()))


def _simulate(samples, *, domain="core"):
    # The wide polynomial takes much longer to compile than to simulate.
    # Simulator.reset resets every signal, clock and testbench per case;
    # only compiled code is shared, never packet state or sticky bits.
    reuse = domain in _SIMULATORS
    if not reuse:
        dut = Gen2TxWireChecker()
        work = {}

        async def bench(ctx):
            for data, ctrl, strobe, enable in work["samples"]:
                ctx.set(dut.data, data)
                ctx.set(dut.ctrl, ctrl)
                ctx.set(dut.strobe, strobe)
                ctx.set(dut.enable, enable)
                await ctx.tick(domain)
                _record(ctx, dut, work["trace"])

        top = dut if domain == "ss" else DomainRenamer({"ss": domain})(dut)
        sim = Simulator(top)
        sim.add_clock(12.8e-9, domain=domain)
        sim.add_testbench(bench)
        _SIMULATORS[domain] = sim, work
    sim, work = _SIMULATORS[domain]
    work["samples"] = list(samples) + [(0, 0, 0, 1)] * 6
    work["trace"] = _empty_trace()
    if reuse:
        sim.reset()
    sim.run()
    return work["trace"]


def _assert_counts(trace, **expected):
    expected.setdefault("cap_strobe", expected.get("tp_seen", 0)
                        + expected.get("dph_seen", 0))
    for name in PULSES:
        assert len(trace[name]) == expected.get(name, 0), f"{name}: {trace[name]}"
    previous = dict.fromkeys(ERRORS, 0)
    for cycle, sticky in enumerate(trace["sticky"]):
        for name in ERRORS:
            previous[name] |= int(cycle in trace[name])
            assert sticky[name] == previous[name], (cycle, name, sticky)


def test_independent_crc_oracle_vectors():
    assert _crc5(0) == 2
    assert _crc5(0x7FF) == 8
    assert zlib.crc32(b"") == 0
    assert zlib.crc32(b"123456789") == 0xCBF43926
    for length in LENGTHS:
        data = _payload(length)
        assert _crc_bits(int.from_bytes(data, "little"), 8 * length,
                         32, 0xEDB88320) == zlib.crc32(data)


def test_ep0_tp_completes_once_with_exact_header_latency():
    beats = _packet(ep=0)
    trace = _simulate(_accepted(beats))
    _assert_counts(trace, tp_seen=1)
    assert trace["tp_seen"] == [4]  # DW3 accepted at edge 2, verdict at edge 4.
    assert trace["caps"] == [(4, 4, _fields(None, 0)[1])]


@pytest.mark.parametrize("length", LENGTHS)
def test_all_lengths_between_back_to_back_ep0_transactions(length):
    dp = _packet(_payload(length), ep=0)
    trace = _simulate(_accepted(_packet() + dp + _packet(ep=3)))
    _assert_counts(trace, tp_seen=2, dph_seen=1, dpp_seen=1,
                   long_dph=int(length > 18))
    assert trace["dph_seen"] == [7]
    assert trace["long_dph"] == ([7] if length > 18 else [])
    assert trace["dpp_seen"] == [len(dp) + 4]
    assert trace["tp_seen"] == [4, len(dp) + 7]
    assert [entry[2] for entry in trace["caps"]] == [
        _fields(None)[1], _fields(_payload(length))[1], _fields(None, 3)[1],
    ]


@pytest.mark.parametrize("length", [0, 1, 2, 3, 4, 5, 6, 7, 8,
                                    18, 19, 20, 21, 22, 50, 1024])
def test_every_crc_byte_at_every_tail_alignment(length):
    beats = []
    for byte in range(4):
        beats += _flip(_packet(_payload(length)), 24 + length + byte, data=1)
        beats += _packet()
    trace = _simulate(_accepted(beats))
    _assert_counts(trace, tp_seen=4, dph_seen=4, dpp_seen=4,
                   long_dph=4 * int(length > 18), crc_error=4)


@pytest.mark.parametrize("tail", range(8))
def test_end_crc_controls_and_padding_at_every_tail_alignment(tail):
    length = 16 + tail
    good = _packet(_payload(length))
    variants = [_flip(good, 24 + length + byte, ctrl=True) for byte in range(4)]
    variants += [_flip(good, 24 + length + 4 + byte, data=1) for byte in range(4)]
    variants += [_flip(good, 24 + length + 4 + byte, ctrl=True) for byte in range(4)]
    if tail:
        variants += [_flip(good, 32 + length, data=1),
                     _flip(good, 32 + length, ctrl=True)]
    beats = []
    for bad in variants:
        beats += bad + _packet()
    trace = _simulate(_accepted(beats))
    count = len(variants)
    _assert_counts(trace, tp_seen=count, dph_seen=count, dpp_seen=count,
                   long_dph=count * int(length > 18), framing_error=count)


def test_payload_control_errors_cover_all_eight_lanes_and_partial_payload():
    length = 50
    beats = []
    for offset in list(range(8)) + [48, 49]:
        beats += _flip(_packet(_payload(length)), 24 + offset, ctrl=True) + _packet()
    trace = _simulate(_accepted(beats))
    _assert_counts(trace, tp_seen=10, dph_seen=10, dpp_seen=10,
                   long_dph=10, framing_error=10)


@pytest.mark.parametrize("cause", ["dw0_ctrl", "dw1_ctrl", "dw2_ctrl", "dw3_ctrl",
                                   "crc16", "crc5", "length", "tp_pad", "tp_pad_ctrl"])
def test_header_errors_do_not_become_payload_crc_errors(cause):
    is_tp = cause.startswith("tp_")
    bad = _packet(None if is_tp else _payload(22))
    mutations = {
        "dw0_ctrl": (7, 0, True), "dw1_ctrl": (8, 0, True),
        "dw2_ctrl": (15, 0, True), "dw3_ctrl": (16, 0, True),
        "crc16": (16, 1, False), "crc5": (19, 0x80, False),
        "length": (11, 4, False), "tp_pad": (20, 1, False),
        "tp_pad_ctrl": (20, 0, True),
    }
    offset, data, ctrl = mutations[cause]
    bad = _flip(bad, offset, data=data, ctrl=ctrl)
    trace = _simulate(_accepted(bad + _packet() + _packet(_payload(18))))
    _assert_counts(trace, tp_seen=1 + int(is_tp), dph_seen=2 - int(is_tp),
                   dpp_seen=1, long_dph=int(not is_tp), header_error=1)


def test_corrupted_hpstart_does_not_claim_a_complete_header():
    beats = []
    for lane in range(4):
        beats += _flip(_packet(), lane, data=1) + _packet()
        beats += _flip(_packet(), lane, ctrl=True) + _packet()
    trace = _simulate(_accepted(beats))
    _assert_counts(trace, tp_seen=8, header_error=8)


def test_missing_sdp_is_framing_not_header_or_crc_error():
    good = _packet(_payload(22))
    beats = _flip(good, 20, data=1) + _packet()
    beats += _flip(good, 23, ctrl=True) + _packet()
    trace = _simulate(_accepted(beats))
    _assert_counts(trace, tp_seen=2, dph_seen=2, long_dph=2, framing_error=2)


def test_gaps_and_repeated_stalled_offers_are_ignored():
    beats = _packet() + _packet(_payload(50)) + [_lc(1, 9)]
    beats += _packet(_payload(22)) + _packet()
    samples = []
    for data, ctrl in beats:
        samples += [(data, ctrl, 0, 1)] * 2
        samples += [(HPSTART | (4 << 32), 0x0F, 0, 1), (0xDEADBEEF, 0xFF, 0, 1)]
        samples += [(data, ctrl, 1, 1)]
    trace = _simulate(samples)
    _assert_counts(trace, tp_seen=2, dph_seen=2, dpp_seen=2, long_dph=2, lc_seen=1)
    assert trace["tp_seen"][0] == 16  # Final TP beat accepted at edge 14.


@pytest.mark.parametrize("cut", range(1, 7))
def test_k_qualified_header_resynchronizes_after_every_truncation_state(cut):
    broken = _packet(_payload(22))[:cut]
    beats = broken + _packet() + _packet(_payload(22)) + _packet()
    trace = _simulate(_accepted(beats))
    old_header_complete = int(cut >= 3)
    _assert_counts(trace, tp_seen=2, dph_seen=1 + old_header_complete,
                   dpp_seen=1, long_dph=1 + old_header_complete,
                   framing_error=old_header_complete, header_error=1 - old_header_complete)


def test_data_qualified_marker_lookalikes_never_resynchronize():
    payload = b"".join(word.to_bytes(4, "little") for word in
                       [HPSTART, 4, LCSTART, 8, EDB, SDP, END, HPSTART])
    beats = [(HPSTART | (4 << 32), 0), (LCSTART, 0)]
    beats += _packet(payload) + _packet()
    trace = _simulate(_accepted(beats))
    _assert_counts(trace, tp_seen=1, dph_seen=1, dpp_seen=1, long_dph=1)


@pytest.mark.parametrize("length", [0, 18, 22, 1024])
def test_delayed_abort_and_delayed_unconsumed_payload_are_both_legal(length):
    payload = _payload(length)
    beats = _packet(payload, delayed=True, abort=True) + _packet()
    beats += _packet(payload, delayed=True)
    trace = _simulate(_accepted(beats))
    _assert_counts(trace, tp_seen=1, dph_seen=2, dpp_seen=2,
                   long_dph=2 * int(length > 18), abort_seen=1)
    assert trace["abort_seen"] == [5]


@pytest.mark.parametrize("cause", ["undelayed", "padding", "late"])
def test_edb_is_only_legal_immediately_after_a_delayed_header(cause):
    beats = _packet(_payload(22), delayed=cause != "undelayed", abort=True)
    if cause == "padding":
        beats = _flip(beats, 28, data=1)
    if cause == "late":
        beats.insert(3, (0x0102030405060708, 0))
    trace = _simulate(_accepted(beats + _packet()))
    _assert_counts(trace, tp_seen=1, dph_seen=1, long_dph=1, framing_error=1)


@pytest.mark.parametrize("cut", range(1, 8))
def test_link_down_silently_discards_partial_packets_and_drains_complete_events(cut):
    packet = _packet(_payload(22))
    samples = _accepted(packet[:cut])
    samples += [(HPSTART | (4 << 32), 0x0F, 1, 0)] * 2
    samples += _accepted(packet[cut:] + _packet() + _packet(_payload(18)))
    trace = _simulate(samples)
    _assert_counts(trace, tp_seen=1, dph_seen=1 + int(cut >= 3),
                   dpp_seen=1 + int(cut == 7), long_dph=int(cut >= 3))


def test_all_sticky_causes_survive_link_down_without_extra_faults():
    beats = _flip(_packet(_payload(22)), 46, data=1)
    beats += _flip(_packet(), 16, data=1)
    beats += _flip(_packet(_payload(18)), 20, data=1)
    beats += _flip([_lc()], 6, data=1)
    beats += _packet(_payload(50))[:4]
    samples = _accepted(beats) + [(0, 0, 0, 0)] * 4 + _accepted(_packet())
    trace = _simulate(samples)
    _assert_counts(trace, tp_seen=2, dph_seen=3, dpp_seen=1, long_dph=2,
                   framing_error=1, crc_error=1, header_error=1, lc_seen=1, lc_error=1)


def test_long_dph_waits_for_the_complete_header_not_dw1():
    packet = _packet(_payload(19))
    samples = _accepted(packet[:2]) + [(0, 0, 0, 1)] * 5
    samples += _accepted(packet[2:])
    trace = _simulate(samples)
    _assert_counts(trace, dph_seen=1, dpp_seen=1, long_dph=1)
    assert trace["long_dph"] == trace["dph_seen"] == trace["cap_strobe"] == [9]


def test_link_commands_validate_replica_crc5_and_ctrl_not_credit_order():
    good = [_lc(command, subtype) for command in range(16)
            for subtype in (15, 0, 9, 2)]
    bad_replica = _flip([_lc()], 6, data=1)[0]
    bad_crc = _flip(_flip([_lc()], 5, data=0x80), 7, data=0x80)[0]
    bad_ctrl = _flip([_lc()], 4, ctrl=True)[0]
    trace = _simulate(_accepted(good + [bad_replica, bad_crc, bad_ctrl] + _packet()))
    _assert_counts(trace, tp_seen=1, lc_seen=67, lc_error=3)
    assert trace["lc_seen"] == list(range(1, 68))


@pytest.mark.parametrize("cut", [1, 4])
def test_link_command_can_end_an_incomplete_construct_without_hiding_tp(cut):
    beats = _packet(_payload(22))[:cut] + [_lc()] + _packet()
    trace = _simulate(_accepted(beats))
    _assert_counts(trace, tp_seen=1, dph_seen=int(cut >= 3), long_dph=int(cut >= 3),
                   lc_seen=1, framing_error=int(cut >= 3), header_error=int(cut < 3))


def test_capture_keeps_all_five_type_bits_and_non_tp_headers():
    types = [0, 12, 20, 24]
    beats = []
    for kind in types:
        beats += _header(kind, 0xA5020304, 0x12345678)
    trace = _simulate(_accepted(beats))
    _assert_counts(trace, cap_strobe=4)
    assert [entry[1:] for entry in trace["caps"]] == [(kind, 0xA5020304) for kind in types]


def test_domain_renamer_to_core():
    trace = _simulate(_accepted(_packet(_payload(50)) + _packet()), domain="core")
    _assert_counts(trace, tp_seen=1, dph_seen=1, dpp_seen=1, long_dph=1)


def test_real_raw_packet_transmitter_stream_matches_independent_oracle():
    tx = RawPacketTransmitter(gen2=True, words=2)
    samples = []
    packets = [(None, False)] + [(_payload(n), False) for n in LENGTHS]
    packets += [(_payload(22), True), (None, False)]
    cases = [(payload, abort, stalls) for stalls in (False, True)
             for payload, abort in packets]
    observed = []
    expected = []
    header_cycles = []
    dpp_cycles = []

    async def bench(ctx):
        for payload, abort, stalls in cases:
            dw0, dw1, dw2 = _fields(payload)
            ctx.set(tx.header.dw0, dw0)
            ctx.set(tx.header.dw1, dw1)
            ctx.set(tx.header.dw2, dw2)
            ctx.set(tx.header.sequence_number, 3)
            ctx.set(tx.header.delayed, int(abort))
            ctx.set(tx.header_sent_before, int(abort))
            ctx.set(tx.generate, 1)
            chunks = [] if payload is None else [payload[k:k + 8]
                                                 for k in range(0, len(payload), 8)]
            chunk_index = 0
            accepted_cycles = []
            for _ in range(800):
                cycle = len(samples)
                ctx.set(tx.source.ready, int(not stalls or cycle % 5 not in (1, 2)))
                chunk = chunks[chunk_index] if chunk_index < len(chunks) else b""
                ctx.set(tx.data_sink.data, int.from_bytes(chunk, "little"))
                ctx.set(tx.data_sink.valid, (1 << len(chunk)) - 1)
                ctx.set(tx.data_sink.last, int(bool(chunk) and chunk_index == len(chunks) - 1))
                await ctx.delay(1e-9)
                data, ctrl = ctx.get(tx.source.data), ctx.get(tx.source.ctrl)
                accepted = ctx.get(tx.source.valid) and ctx.get(tx.source.ready)
                samples.append((data, ctrl, int(accepted), 1))
                if accepted:
                    observed.append((data, ctrl))
                    accepted_cycles.append(cycle)
                consumed = bool(chunk) and ctx.get(tx.data_sink.ready)
                done = ctx.get(tx.done)
                await ctx.tick("ss")
                ctx.set(tx.generate, 0)
                chunk_index += int(consumed)
                if done:
                    break
            else:
                pytest.fail("RawPacketTransmitter did not finish within 800 clocks")
            expected.extend(_packet(payload, delayed=abort, abort=abort))
            header_cycles.append(accepted_cycles[2] + 2)
            if payload is not None:
                dpp_cycles.append(accepted_cycles[-1] + 2)
            assert chunk_index == (0 if abort else len(chunks))

    sim = Simulator(tx)
    sim.add_clock(12.8e-9, domain="ss")
    sim.add_testbench(bench)
    sim.run()
    assert observed == expected
    # Replay every cycle of the real neutral tap, including repeated offers
    # with strobe=0. Separate simulations avoid duplicating the costly CRC
    # compilation in a combined top; no framing or CRC logic is substituted.
    trace = _simulate(samples)
    _assert_counts(trace, tp_seen=4, dph_seen=2 * (len(LENGTHS) + 1),
                   dpp_seen=2 * (len(LENGTHS) + 1), abort_seen=2,
                   long_dph=2 * (sum(n > 18 for n in LENGTHS) + 1))
    assert trace["cap_strobe"] == header_cycles
    assert trace["dpp_seen"] == dpp_cycles
