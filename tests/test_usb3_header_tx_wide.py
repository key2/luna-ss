#
# This file is part of LUNA.
#
# Copyright (c) 2026 the luna-ss contributors
# SPDX-License-Identifier: BSD-3-Clause
""" Width-program packet-transmitter fences (usb3_design.md 13.5).

The words=2 ``RawPacketTransmitter`` emits 8-symbol beats: header
packets pad their trailing half-beat (legal inter-packet idle), and a
data header carries its DPP framing gaplessly in the final beat's
high half.  These fences parse the emitted symbol streams of BOTH
widths with a padding-tolerant checker and pin:

* header fields, CRC-16 and CRC-5 correctness (parsed == driven);
* DPH -> DPPSTART adjacency (no idle inside a data packet);
* payload byte-exactness and CRC-32 validity for lengths covering
  every final-chunk alignment (1..8 tail positions), plus ZLP;
* the DL=1 consumed-payload abort shape (EDB framing);
* equality of the parsed packet lists between the widths, with and
  without source backpressure.
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

from luna.gateware.usb.usb3.link.transmitter import (       # noqa: E402
    RawPacketTransmitter)

SHP, SDP, EPF, END, EDB = 0xFB, 0x5C, 0xF7, 0xFD, 0x7C
IDLE = (0x00, 0)


def parse_stream(syms):
    """Parses a flat [(byte, ctrl)] stream into packet tuples."""
    out = []
    i = 0
    n = len(syms)

    def at(k):
        return syms[k] if k < n else IDLE

    while i < n:
        if syms[i] == IDLE:
            i += 1
            continue
        # Expect HPSTART.
        assert [at(i), at(i + 1), at(i + 2), at(i + 3)] == \
            [(SHP, 1)] * 3 + [(EPF, 1)], f"bad framing at {i}: {at(i)}"
        i += 4
        dws = []
        for k in range(4):
            dw = 0
            for b in range(4):
                sym, ctrl = at(i)
                assert ctrl == 0, f"ctrl inside header at {i}"
                dw |= sym << (8 * b)
                i += 1
            dws.append(dw)
        dw0, dw1, dw2, dw3 = dws
        crc16_ok = (dw3 & 0xFFFF) == crc16_header([dw0, dw1, dw2])
        crc5_ok = ((dw3 >> 27) & 0x1F) == crc5((dw3 >> 16) & 0x7FF)
        entry = {
            "dw0": dw0, "dw1": dw1, "dw2": dw2,
            "seq": (dw3 >> 16) & 0x7,
            "delayed": (dw3 >> 25) & 1,
            "crc16_ok": crc16_ok, "crc5_ok": crc5_ok,
        }
        if (dw0 & 0xF) == 8:                    # data header: DPP follows
            # The DPP framing must follow IMMEDIATELY (no idle).
            nxt = [at(i), at(i + 1), at(i + 2), at(i + 3)]
            assert nxt == [(SDP, 1)] * 3 + [(EPF, 1)], \
                f"DPH not followed by DPP framing at {i}: {nxt}"
            i += 4
            # An aborted DPP: EDB framing right after DPPSTART, in
            # place of payload/CRC/END (the DL=1 consumed-payload
            # shape, mirroring the narrow unit).
            if [at(i), at(i + 1), at(i + 2), at(i + 3)] == \
                    [(EDB, 1)] * 3 + [(EPF, 1)]:
                entry["dpp"] = "aborted"
                i += 4
            else:
                body = []
                while True:
                    if [at(i), at(i + 1), at(i + 2), at(i + 3)] == \
                            [(END, 1)] * 3 + [(EPF, 1)]:
                        i += 4
                        break
                    sym, ctrl = at(i)
                    assert ctrl == 0, f"ctrl inside DPP at {i}"
                    body.append(sym)
                    i += 1
                assert len(body) >= 4, "DPP shorter than its CRC"
                payload = bytes(body[:-4])
                crc = int.from_bytes(bytes(body[-4:]), "little")
                entry["dpp"] = payload
                entry["dpp_crc_ok"] = (crc == crc32_payload(payload))
        out.append(entry)
    return out


def _run(dut, tb):
    sim = Simulator(dut)
    sim.add_clock(1 / 125e6, domain="ss")
    sim.add_testbench(tb)
    sim.run()


class WideTransmitterEquivalence(unittest.TestCase):

    # (dw0, payload-or-None, sent_before)
    CASES = [
        (0x00000004, None, 0),                     # plain TP header
        (0x00000008, bytes(range(1, 9)), 0),       # 8B (full chunk)
        (0x00000008, bytes(range(40, 41)), 0),     # 1B
        (0x00000008, bytes(range(10, 13)), 0),     # 3B
        (0x00000008, bytes(range(50, 54)), 0),     # 4B
        (0x00000008, bytes(range(60, 65)), 0),     # 5B
        (0x00000008, bytes(range(70, 76)), 0),     # 6B
        (0x00000008, bytes(range(80, 87)), 0),     # 7B
        (0x00000008, bytes(range(90, 107)), 0),    # 17B (2 full + 1B)
        (0x00000008, bytes(range(120, 136)), 0),   # 16B (2 full, v=8)
        (0x00000008, b"", 0),                      # ZLP
        (0x00000004, None, 0),                     # trailing TP
    ]
    ABORT_CASE = (0x00000008, bytes(range(8)), 1)  # delayed+sent_before

    def _drive(self, words, cases, ready_stall=0, delayed_abort=False):
        dut = RawPacketTransmitter(gen2=True, words=words)
        bpb = 4 * words
        out = []

        async def tb(ctx):
            cyc = 0
            for dw0, payload, sent_before in cases:
                ctx.set(dut.header.dw0, dw0)
                ctx.set(dut.header.dw1, 0x11111111)
                ctx.set(dut.header.dw2, 0x22222222)
                ctx.set(dut.header.sequence_number, 5)
                ctx.set(dut.header.delayed, 1 if sent_before else 0)
                ctx.set(dut.header_sent_before, sent_before)
                ctx.set(dut.generate, 1)

                chunks = []
                if payload:
                    for k in range(0, len(payload), bpb):
                        chunk = payload[k:k + bpb]
                        data = int.from_bytes(chunk, "little")
                        valid = (1 << len(chunk)) - 1
                        chunks.append((data, valid))
                ci = 0

                for _ in range(400):
                    stall = ready_stall and (cyc % ready_stall == 0)
                    ctx.set(dut.source.ready, 0 if stall else 1)
                    # Gapless payload feed: present the current chunk.
                    if ci < len(chunks):
                        d, v = chunks[ci]
                        ctx.set(dut.data_sink.data, d)
                        ctx.set(dut.data_sink.valid, v)
                        ctx.set(dut.data_sink.last,
                                1 if ci == len(chunks) - 1 else 0)
                    else:
                        ctx.set(dut.data_sink.valid, 0)
                        ctx.set(dut.data_sink.last, 0)
                    cyc += 1
                    await ctx.delay(1e-9)
                    take = (ctx.get(dut.source.valid)
                            and ctx.get(dut.source.ready))
                    consumed = ctx.get(dut.data_sink.ready) \
                        and ci < len(chunks)
                    done = ctx.get(dut.done)
                    if take:
                        d = ctx.get(dut.source.data)
                        c = ctx.get(dut.source.ctrl)
                        for i in range(bpb):
                            out.append(((d >> (8 * i)) & 0xFF,
                                        (c >> i) & 1))
                    await ctx.tick("ss")
                    if consumed:
                        ci += 1
                    ctx.set(dut.generate, 0)
                    if done:
                        break
                else:
                    self.fail(f"transmitter (words={words}) hung on "
                              f"dw0={dw0:#x} len="
                              f"{len(payload) if payload else 0}")
                await ctx.tick("ss")

        _run(dut, tb)
        return out

    def _check(self, parsed, cases):
        self.assertEqual(len(parsed), len(cases))
        for entry, (dw0, payload, sent_before) in zip(parsed, cases):
            self.assertEqual(entry["dw0"], dw0)
            self.assertTrue(entry["crc16_ok"], f"CRC-16 bad: {entry}")
            self.assertTrue(entry["crc5_ok"], f"CRC-5 bad: {entry}")
            self.assertEqual(entry["seq"], 5)
            if (dw0 & 0xF) == 8:
                if sent_before:
                    self.assertEqual(entry["dpp"], "aborted")
                else:
                    self.assertEqual(entry["dpp"], payload,
                                     "payload bytes diverged")
                    self.assertTrue(entry["dpp_crc_ok"],
                                    f"CRC-32 bad for {payload!r}")

    def test_wide_shapes(self):
        out = self._drive(2, self.CASES)
        self._check(parse_stream(out), self.CASES)

    def test_narrow_shapes(self):
        out = self._drive(1, self.CASES)
        self._check(parse_stream(out), self.CASES)

    def test_wide_matches_narrow(self):
        narrow = parse_stream(self._drive(1, self.CASES))
        wide   = parse_stream(self._drive(2, self.CASES))
        self.assertEqual(narrow, wide,
                         "parsed packets diverged between widths")

    def test_wide_backpressured(self):
        wide = parse_stream(self._drive(2, self.CASES, ready_stall=3))
        self._check(wide, self.CASES)

    def test_wide_abort_shape(self):
        cases = [self.ABORT_CASE]
        out = self._drive(2, cases)
        parsed = parse_stream(out)
        self.assertEqual(parsed[0]["dpp"], "aborted",
                         "consumed-payload retransmission must abort "
                         "its DPP (bug #51 contract)")


if __name__ == "__main__":
    unittest.main()
