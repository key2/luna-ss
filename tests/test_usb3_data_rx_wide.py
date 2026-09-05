#
# This file is part of LUNA.
#
# Copyright (c) 2026 the luna-ss contributors
# SPDX-License-Identifier: BSD-3-Clause
""" Width-program data-packet receiver fences (usb3_design.md 13.5).

The words=2 ``DataPacketReceiver`` handles data packets at both beat
offsets: an offset-0 DPH carries its DPP framing in the final beat's
high half (payload beat-aligned); an offset-4 DPH ends beat-aligned,
its DPPSTART occupies the next beat's LOW half, and the payload runs
HALF-SKEWED (assembled from consecutive beat halves).  These fences
pin the wide unit against the words=1 unit over the same symbol
streams: header fields, payload byte-exactness through the source
stream, packet_good/packet_bad verdicts (CRC-32 at every final-beat
alignment 1..8, corrupted CRC, ctrl codes inside the payload), and
both offsets.
"""

import os
import sys
import unittest

from amaranth import Module
from amaranth.sim import Simulator

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "sim"))
sys.path.insert(0, os.path.dirname(__file__))

from sim_link_loopback import crc16_header, crc32_payload   # noqa: E402
from test_usb3_command_wide import crc5                     # noqa: E402

from luna.gateware.usb.usb3.link.data import (              # noqa: E402
    DataPacketReceiver)

SHP, SDP, EPF, END = 0xFB, 0x5C, 0xF7, 0xFD
IDLE = (0x00, 0)


def dp_syms(payload, seq=3, ep=1, corrupt32=False, ctrl_glitch=False):
    """A full data packet: DPH + DPP with valid CRCs."""
    dw0 = 0x8 | (1 << 25)                       # DATA, device address 1
    dw1 = (seq & 0x1F) | (ep << 8) | (len(payload) << 16)
    dw2 = 0
    c16 = crc16_header([dw0, dw1, dw2])
    mid = seq & 0x7
    dw3 = c16 | (mid << 16) | (crc5(mid) << 27)

    syms = [(SHP, 1)] * 3 + [(EPF, 1)]
    for dw in (dw0, dw1, dw2, dw3):
        syms += [((dw >> (8 * k)) & 0xFF, 0) for k in range(4)]
    syms += [(SDP, 1)] * 3 + [(EPF, 1)]
    for k, b in enumerate(payload):
        syms.append((b, 1 if (ctrl_glitch and k == 1) else 0))
    crc = crc32_payload(payload)
    if corrupt32:
        crc ^= 0x1
    syms += [((crc >> (8 * k)) & 0xFF, 0) for k in range(4)]
    syms += [(END, 1)] * 3 + [(EPF, 1)]
    # The receiver's refined-header view of this packet.
    return syms, (0x8, 1, seq & 0x1F, len(payload), ep)


def _run(dut, tb):
    sim = Simulator(dut)
    sim.add_clock(1 / 125e6, domain="ss")
    sim.add_testbench(tb)
    sim.run()


class WideDataReceiverEquivalence(unittest.TestCase):

    def _stimulus(self, offset4=False):
        """DPs of every final-alignment length at the chosen offset."""
        s = []
        expected = []
        s += [IDLE] * 8
        if offset4:
            s += [IDLE] * 4
        lengths = [8, 1, 2, 3, 4, 5, 6, 7, 16, 17, 12, 64]
        base = 0
        for n in lengths:
            payload = bytes((base + k) & 0xFF for k in range(n))
            base += 32
            syms, dws = dp_syms(payload)
            s += syms
            expected.append(("hdr",) + dws)
            expected.append(("pay", payload))
            expected.append(("good",))
            # Word-align (the wire keeps 4-symbol construct alignment;
            # odd DPP tails are followed by the aligner's realignment
            # on real hardware) -- packets then land at offset 0 or 4
            # of the wide beats depending on the running parity.
            while len(s) % 4:
                s.append(IDLE)
            s += [IDLE] * 8
        # Corrupted CRC-32 -> bad.
        payload = bytes(range(11))
        syms, dws = dp_syms(payload, corrupt32=True)
        s += syms
        expected.append(("hdr",) + dws)
        expected.append(("pay", payload))
        expected.append(("bad",))
        while len(s) % 4:
            s.append(IDLE)
        s += [IDLE] * 8
        # Ctrl code inside the payload -> bad (payload truncated).
        payload = bytes(range(30, 40))
        syms, dws = dp_syms(payload, ctrl_glitch=True)
        s += syms
        expected.append(("hdr",) + dws)
        expected.append(("bad",))
        s += [IDLE] * 12
        while len(s) % 8:
            s.append(IDLE)
        return s, expected

    def _run_receiver(self, words, symbols):
        dut = DataPacketReceiver(gen2=False, words=words)
        bpb = 4 * words
        events = []
        pay = []

        async def tb(ctx):
            beats = [symbols[k:k + bpb]
                     for k in range(0, len(symbols), bpb)]
            for beat in beats:
                data = 0
                ctrl = 0
                for i, (b, c) in enumerate(beat):
                    data |= b << (8 * i)
                    ctrl |= c << i
                ctx.set(dut.sink.valid, 1)
                ctx.set(dut.sink.data, data)
                ctx.set(dut.sink.ctrl, ctrl)
                await ctx.delay(1e-9)
                # Sample the comb source/verdict surfaces mid-beat.
                v = ctx.get(dut.source.valid)
                if v:
                    d = ctx.get(dut.source.data)
                    for i in range(bpb):
                        if (v >> i) & 1:
                            pay.append((d >> (8 * i)) & 0xFF)
                def hdr_fields():
                    return ("hdr",
                            ctx.get(dut.header.type),
                            ctx.get(dut.header.device_address),
                            ctx.get(dut.header.data_sequence),
                            ctx.get(dut.header.data_length),
                            ctx.get(dut.header.endpoint_number))

                # ``header`` is stable from payload start through the
                # verdict; sample it at verdict time (``new_header`` is
                # not a strobe in the historical unit).
                if ctx.get(dut.packet_good):
                    events.append(hdr_fields())
                    events.append(("pay", bytes(pay)))
                    pay.clear()
                    events.append(("good",))
                if ctx.get(dut.packet_bad):
                    events.append(hdr_fields())
                    if pay:
                        events.append(("pay", bytes(pay)))
                        pay.clear()
                    events.append(("bad",))
                await ctx.tick("ss")
            ctx.set(dut.sink.valid, 0)
            for _ in range(4):
                await ctx.tick("ss")

        _run(dut, tb)
        return events

    def _normalize(self, events):
        """Canonical form: per-packet (header, payload-or-None,
        verdict) tuples."""
        packets = []
        cur_hdr = None
        cur_pay = None
        for e in events:
            if e[0] == "hdr":
                cur_hdr = e[1:]
            elif e[0] == "pay":
                cur_pay = e[1]
            else:
                # A bad packet's delivered-payload prefix is
                # width-dependent (the consumer discards it on the
                # verdict anyway); only good payloads are pinned.
                packets.append((cur_hdr,
                                cur_pay if e[0] == "good" else None,
                                e[0]))
                cur_hdr = None
                cur_pay = None
        return packets

    def _check_equal(self, symbols, expected):
        narrow = self._normalize(self._run_receiver(1, symbols))
        wide   = self._normalize(self._run_receiver(2, symbols))
        exp    = self._normalize(expected)
        self.assertEqual(narrow, exp, "narrow packets wrong")
        self.assertEqual(wide, narrow, "wide packets diverged")

    def test_offset0(self):
        symbols, expected = self._stimulus(offset4=False)
        self._check_equal(symbols, expected)

    def test_offset4(self):
        symbols, expected = self._stimulus(offset4=True)
        self._check_equal(symbols, expected)


if __name__ == "__main__":
    unittest.main()
