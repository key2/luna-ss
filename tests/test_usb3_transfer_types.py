# amaranth: UnusedElaboratable=no
# Copyright (c) 2026 luna-ss contributors
# SPDX-License-Identifier: BSD-3-Clause
"""Transfer-type annotation at the buffered protocol-to-link boundary (#56)."""

from types import SimpleNamespace
import zlib

import pytest
from amaranth.sim import Simulator
from usb_protocol.emitters import DeviceDescriptorCollection
from usb_protocol.types import USBTransferType
from usb_protocol.types.superspeed import LinkCommand

from luna.gateware.usb.usb3.device import USBSuperSpeedDevice
from luna.gateware.usb.usb3.link.transmitter import PacketTransmitter

from .test_gen2_tx_checker import END, EDB, HPSTART, SDP, _crc_bits, _crc5, _lc


CONTROL = USBTransferType.CONTROL
BULK = USBTransferType.BULK
TT_MASK = 7 << 12
ENDPOINT_TYPES = {0: CONTROL, 2: BULK, 0x82: BULK, 3: CONTROL, 0x83: BULK}
BOS50 = bytes.fromhex(
    "05 0f 32 00 03 "
    "07 10 02 02 00 00 00 "
    "0a 10 03 00 0e 00 01 0a ff 07 "
    "1c 10 0a 00 23 00 00 00 00 11 00 00 "
    "30 00 05 00 b0 00 05 00 31 40 0a 00 b1 40 0a 00"
)


def _symbols(data, ctrl, count):
    return [((data >> (8 * lane)) & 0xff, (ctrl >> lane) & 1)
            for lane in range(count)]


def _wire_packet(words, dw0, dw1, sequence, payload, *, delayed=False):
    # Independent bit-serial CRC oracle, not the gateware's XOR equations.
    crc16 = _crc_bits(dw0 | (dw1 << 32), 96, 16, 0xd008)
    link = sequence | (int(delayed) << 9)
    dw3 = crc16 | (link << 16) | (_crc5(link) << 27)
    symbols = _symbols(HPSTART, 0xf, 4)
    for word in (dw0, dw1, 0, dw3):
        symbols += _symbols(word, 0, 4)
    if payload is not None:
        symbols += _symbols(SDP, 0xf, 4)
        if delayed:
            symbols += _symbols(EDB, 0xf, 4)
        else:
            symbols += [(byte, 0) for byte in payload]
            symbols += _symbols(zlib.crc32(payload), 0, 4)
            symbols += _symbols(END, 0xf, 4)
    symbols += [(0, 0)] * (-len(symbols) % (4 * words))
    return symbols


def _exercise(words, gen2_active, endpoint_types, packets, *, replay=()):
    frequency = (156.25e6 if gen2_active else 125e6) / words
    dut = PacketTransmitter(gen2=True, words=words,
                            ss_clock_frequency=frequency,
                            endpoint_types=endpoint_types)
    sim = Simulator(dut)
    sim.add_clock(1 / frequency, domain="ss")
    width = 4 * words

    async def bench(ctx):
        output = []
        payload = b""
        offset = cycle = retries = 0
        held = None

        async def step(*, ready=None):
            nonlocal offset, cycle, held, retries
            if ready is None:
                ready = cycle % 4 != 1
            chunk = payload[offset:offset + width]
            ctx.set(dut.source.ready, ready)
            ctx.set(dut.data_sink.data, int.from_bytes(chunk, "little"))
            ctx.set(dut.data_sink.valid, (1 << len(chunk)) - 1)
            ctx.set(dut.data_sink.first, bool(chunk) and offset == 0)
            ctx.set(dut.data_sink.last, bool(chunk) and offset + len(chunk) == len(payload))
            (_, _, valid, data, ctrl, first, data_ready, qvalid, qready,
             retry, recovery, underrun) = await ctx.tick("ss").sample(
                dut.source.valid, dut.source.data, dut.source.ctrl, dut.source.first,
                dut.data_sink.ready, dut.queue.valid, dut.queue.ready,
                dut.retry_required, dut.recovery_required, dut.debug_payload_underrun)
            assert not recovery, "unexpected link recovery (advertisement/credit sequencing)"
            assert not underrun, "payload producer violated the gapless-feed contract"
            if held is not None:
                assert valid and (data, ctrl, first) == held, "output changed while stalled"
            held = (data, ctrl, first) if valid and not ready else None
            if valid and ready:
                output.extend(_symbols(data, ctrl, width))
            if data_ready and chunk:
                offset += len(chunk)
            retries += retry
            cycle += 1
            return qvalid and qready

        async def command(kind, subtype=0):
            data, ctrl = _lc(kind, subtype)
            for shift in range(0, 8, width):
                ctx.set(dut.sink.valid, 1)
                ctx.set(dut.sink.data, (data >> (8 * shift)) & ((1 << (8 * width)) - 1))
                ctx.set(dut.sink.ctrl, (ctrl >> shift) & ((1 << width) - 1))
                await step()
            ctx.set(dut.sink.valid, 0)
            await step()
            await step()

        async def drain():
            for _ in range(400):
                await step()
                if not ctx.get(dut.packets_to_send) and not ctx.get(dut.source.valid):
                    break
            else:
                pytest.fail("buffered transmitter failed to finish within 400 clocks")
            for _ in range(3):
                await step()
            assert offset == len(payload), "packet finished without consuming its payload"

        ctx.set(dut.gen2_active, gen2_active)
        ctx.set(dut.enable, 1)
        await step()
        assert not ctx.get(dut.queue.ready)
        # A real partner advertises modulo-16/modulo-8, then four credits
        # per active pool. No internal bringup/credit registers are forced.
        await command(LinkCommand.LGOOD, 15 if gen2_active else 7)
        assert ctx.get(dut.bringup_complete)
        for pool in range(2 if gen2_active else 1):
            for index in range(4):
                await command(LinkCommand.LCRD, (pool << 2) | index)
        assert ctx.get(dut.credits_available) == 4
        next_credit = [0, 0]

        for number, (name, kind, dw1, packet_payload, native_tt) in enumerate(packets):
            sequence = number & (15 if gen2_active else 7)
            dw0 = kind | (5 << 25) if kind in (4, 8) else kind
            expected_tt = ((dw1 >> 12) & 7) if native_tt is None else (
                native_tt if gen2_active else 0)
            expected_dw1 = (dw1 & ~TT_MASK) | (expected_tt << 12)
            payload = packet_payload or b""
            offset = 0
            start = len(output)
            ctx.set(dut.queue.header.dw0, dw0)
            ctx.set(dut.queue.header.dw1, dw1)
            ctx.set(dut.queue.header.dw2, 0)
            ctx.set(dut.queue.valid, 1)
            for _ in range(20):
                if await step(ready=False):
                    break
            else:
                pytest.fail(f"{name}: header not accepted despite returned link credits")
            ctx.set(dut.queue.valid, 0)
            # Poison live inputs immediately after acceptance, before the raw
            # serializer starts. TT must use the acceptance-time rate/endpoint.
            ctx.set(dut.queue.header.dw0, 4 | (17 << 25))
            ctx.set(dut.queue.header.dw1, 0x281 | TT_MASK)
            ctx.set(dut.queue.header.dw2, 0xdeadbeef)
            ctx.set(dut.gen2_active, 1 - gen2_active)
            for _ in range(5):
                await step(ready=False)
            await drain()
            actual = output[start:]
            actual_dw1 = int.from_bytes(bytes(byte for byte, _ in actual[8:12]), "little")
            assert (actual_dw1 >> 12) & 7 == expected_tt, f"{name}: serialized DW1 TT"
            assert actual == _wire_packet(words, dw0, expected_dw1, sequence,
                                          packet_payload), name

            if name in replay:
                start = len(output)
                before = retries
                ctx.set(dut.lrty_pending, 1)
                await command(LinkCommand.LBAD)
                assert retries == before + 1
                for _ in range(4):
                    await step()
                assert len(output) == start, "retry escaped before the receiver's LRTY"
                # Model the receiver completing its LRTY on the shared wire.
                ctx.set(dut.lrty_pending, 0)
                await drain()
                assert output[start:] == _wire_packet(
                    words, dw0, expected_dw1, sequence, packet_payload, delayed=True), name

            ctx.set(dut.gen2_active, gen2_active)
            await command(LinkCommand.LGOOD, sequence)
            pool = int(gen2_active and kind == 8)
            await command(LinkCommand.LCRD, (pool << 2) | next_credit[pool])
            next_credit[pool] = (next_credit[pool] + 1) & 3

    sim.add_testbench(bench)
    sim.run()


@pytest.mark.parametrize("words", [1, 2], ids=["narrow", "wide"])
@pytest.mark.parametrize("gen2_active", [0, 1], ids=["fallback", "native"])
def test_buffered_transfer_types_on_serialized_output(words, gen2_active):
    assert len(BOS50) == 50
    # Control IN data still uses direction=OUT [8.12.2]. EP3 OUT is
    # Control while EP3 IN is Bulk, exposing endpoint-number-only lookup.
    packets = [
        ("ep0-ack", 4, 1 | (1 << 16) | (1 << 21), None, 4),
        ("ep0-bos50", 8, 0x40 | (50 << 16), BOS50, 4),
        ("ep0-zlp", 8, 0x40, b"", 4),
        # Stale TT bits must be replaced, including cleared in fallback.
        ("bulk-out-ack", 4, 0x241 | (4 << 12) | (3 << 16) | (9 << 21), None, 6),
        ("bulk-in-dp", 8, 0x2c7 | (17 << 16), bytes(range(17)), 6),
        ("nonzero-control-ack", 4, 0x301 | (1 << 16) | (2 << 21), None, 4),
        ("nonzero-control-dp", 8, 0x342 | (6 << 12) | (4 << 16), b"ctrl", 4),
        ("same-number-bulk-in", 8, 0x3c3 | (8 << 16), b"bulk-in!", 6),
        ("nrdy", 4, 0x282, None, None),
        ("erdy", 4, 0x283 | (1 << 16), None, None),
        ("stall", 4, 0x205, None, None),
        # Sentinel bits are opaque here, not TT fields to clear/annotate.
        ("lmp-opaque", 0x20, 1 | (5 << 12), None, None),
        ("nrdy-opaque", 4, 0x382 | (3 << 12), None, None),
    ]
    _exercise(words, gen2_active, ENDPOINT_TYPES, packets,
              replay=("ep0-ack", "ep0-bos50"))


@pytest.mark.parametrize("words", [1, 2], ids=["narrow", "wide"])
@pytest.mark.parametrize("gen2_active", [0, 1], ids=["fallback", "native"])
def test_bare_transmitter_preserves_caller_tt(words, gen2_active):
    packets = [
        ("caller-ack", 4, 1 | (4 << 12) | (1 << 16), None, None),
        ("caller-dp", 8, 0x2c0 | (6 << 12) | (5 << 16), b"owned", None),
        ("caller-unannotated", 4, 1 | (1 << 16), None, None),
    ]
    _exercise(words, gen2_active, None, packets)


@pytest.mark.parametrize("gen2", [False, True], ids=["gen1-default", "ssp"])
def test_endpoint_registration_and_standard_control(gen2, monkeypatch):
    device = USBSuperSpeedDevice(phy=None, gen2=gen2)
    endpoint = object()
    metadata = {2: BULK, 0x82: BULK, 3: CONTROL, 0x83: BULK, 15: BULK, 0x8f: BULK}
    device.add_endpoint(endpoint, **({"endpoint_types": metadata} if gen2 else {}))
    received_descriptors = []
    control = SimpleNamespace(add_standard_request_handlers=received_descriptors.append)
    monkeypatch.setattr("luna.gateware.usb.usb3.device.USB3ControlEndpoint", lambda: control)
    descriptors = DeviceDescriptorCollection()
    assert device.add_standard_control_endpoint(descriptors) is control
    assert received_descriptors == [descriptors]
    assert device._endpoints == [endpoint, control]
    if gen2:
        assert device._endpoint_types == metadata | {0: CONTROL}
        metadata.clear()
        assert device._endpoint_types[3] == CONTROL, "registration retained the caller's dict"


def test_ssp_registration_requires_explicit_metadata():
    device = USBSuperSpeedDevice(phy=None, gen2=True)
    for kwargs in ({}, {"endpoint_types": None}, {"endpoint_types": {}}):
        with pytest.raises(ValueError):
            device.add_endpoint(object(), **kwargs)
        assert device._endpoints == []
        assert device._endpoint_types == {}


@pytest.mark.parametrize("invalid_maps", [
    pytest.param([{address: BULK} for address in (-1, 0x10, 0x70, 0x90, 0x100, 1.5, "2")],
                 id="invalid-address"),
    pytest.param([{1: kind} for kind in (USBTransferType.ISOCHRONOUS,
                                       USBTransferType.INTERRUPT, 99)], id="unsupported-type"),
    pytest.param([{0: BULK}, {0x80: BULK}], id="ep0-noncontrol"),
    pytest.param([{0x80: CONTROL}, {0x81: CONTROL}], id="control-in-address"),
    pytest.param([{2: BULK}, {2: CONTROL}], id="duplicate-address"),
])
def test_ssp_rejects_invalid_registration_atomically(invalid_maps):
    device = USBSuperSpeedDevice(phy=None, gen2=True)
    endpoint = object()
    device.add_endpoint(endpoint, endpoint_types={2: BULK})
    for invalid in invalid_maps:
        # A valid prefix must not be installed when a later entry is invalid.
        with pytest.raises(ValueError):
            device.add_endpoint(object(), endpoint_types={0x8f: BULK} | invalid)
        assert device._endpoints == [endpoint]
        assert device._endpoint_types == {2: BULK}
