#
# This file is part of LUNA.
#
# Copyright (c) 2026 the luna-ss contributors
# SPDX-License-Identifier: BSD-3-Clause
""" Width-program header-packet receiver fences (usb3_design.md 13.5).

At ``words=2`` a header packet (HPSTART + 16 bytes = 20 symbols) spans
2.5 beats and may start at either beat half; back-to-back headers
alternate phase (offset 0 -> tail HPSTART -> offset 4 -> beat-aligned
-> offset 0 ...).  These fences pin the words=2
``RawHeaderPacketReceiver`` against the words=1 unit over the same
symbol stream: field-exact packet events, bad-CRC16/bad-CRC5 ->
bad_packet, wrong sequence -> bad_sequence, valid gaps mid-packet,
back-to-back chains at both phases, and the gen2 4-bit sequence
(bit 3 in the LCW reserved field).
"""

import os
import sys
import unittest

from amaranth import Module
from amaranth.sim import Simulator

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "sim"))
sys.path.insert(0, os.path.dirname(__file__))

from sim_link_loopback import crc16_header          # noqa: E402
from test_usb3_command_wide import crc5             # noqa: E402

from luna.gateware.usb.usb3.link.receiver import (  # noqa: E402
    RawHeaderPacketReceiver)

SHP = (0xFB, 1)
EPF = (0xF7, 1)
IDLE = (0x00, 0)


def hp_syms(dw0, dw1, dw2, seq, gen2=False, corrupt16=False,
            corrupt5=False, delayed=0, deferred=0):
    """The 20 symbols of a header packet."""
    c16 = crc16_header([dw0, dw1, dw2])
    if corrupt16:
        c16 ^= 0x0001
    mid = (seq & 0x7)
    if gen2:
        mid |= ((seq >> 3) & 1) << 3      # dw3_reserved[0] = seq bit 3
    mid |= (delayed & 1) << 9
    mid |= (deferred & 1) << 10
    c5 = crc5(mid)
    if corrupt5:
        c5 ^= 0x10
    dw3 = c16 | (mid << 16) | (c5 << 27)

    syms = [SHP, SHP, SHP, EPF]
    for dw in (dw0, dw1, dw2, dw3):
        syms += [((dw >> (8 * k)) & 0xFF, 0) for k in range(4)]
    return syms


def _run(dut, tb):
    sim = Simulator(dut)
    sim.add_clock(1 / 125e6, domain="ss")
    sim.add_testbench(tb)
    sim.run()


class WideHeaderReceiverEquivalence(unittest.TestCase):

    GOOD_SEQ = 3
    GOOD_SEQ_GEN2 = 11        # exercises the 4-bit path (bit 3 set)

    def _stimulus(self, gen2):
        seq = self.GOOD_SEQ_GEN2 if gen2 else self.GOOD_SEQ
        s = []
        s += [IDLE] * 8
        # offset 0, isolated
        s += hp_syms(0x11223344, 0x55667788, 0x99AABBCC, seq, gen2)
        s += [IDLE] * 4
        # offset 4, isolated
        s += hp_syms(0x01020304, 0x05060708, 0x090A0B0C, seq, gen2)
        s += [IDLE] * 4                       # realign to offset 0
        # back-to-back chain of four (phase alternates 0->4->0->4)
        s += hp_syms(0xA0A1A2A3, 0xB0B1B2B3, 0xC0C1C2C3, seq, gen2)
        s += hp_syms(0xD0D1D2D3, 0xE0E1E2E3, 0xF0F1F2F3, seq, gen2)
        s += hp_syms(0x10111213, 0x20212223, 0x30313233, seq, gen2)
        s += hp_syms(0x40414243, 0x50515253, 0x60616263, seq, gen2)
        s += [IDLE] * 8
        # corrupted CRC-16 -> bad_packet
        s += hp_syms(0xDEADBEEF, 0x12345678, 0x9ABCDEF0, seq, gen2,
                     corrupt16=True)
        s += [IDLE] * 4
        # corrupted CRC-5 -> bad_packet (offset 4)
        s += hp_syms(0xDEADBEEF, 0x12345678, 0x9ABCDEF0, seq, gen2,
                     corrupt5=True)
        s += [IDLE] * 4
        # wrong sequence -> bad_sequence (valid CRCs)
        s += hp_syms(0xCAFEBABE, 0x0BADF00D, 0xFEEDFACE,
                     (seq + 2) & (0xF if gen2 else 0x7), gen2)
        # delayed/deferred flags carried
        s += hp_syms(0x21436587, 0xA9CBED0F, 0x00FF00FF, seq, gen2,
                     delayed=1, deferred=1)
        s += [IDLE] * 8
        while len(s) % 8:
            s.append(IDLE)
        return s

    def _run_receiver(self, words, gen2, symbols, gap_every=0):
        dut = RawHeaderPacketReceiver(gen2=gen2, words=words)
        bpb = 4 * words
        events = []

        async def tb(ctx):
            ctx.set(dut.expected_sequence,
                    self.GOOD_SEQ_GEN2 if gen2 else self.GOOD_SEQ)
            beats = [symbols[k:k + bpb]
                     for k in range(0, len(symbols), bpb)]

            def sample():
                if ctx.get(dut.new_packet):
                    seq = ctx.get(dut.packet.sequence_number)
                    if gen2:
                        seq |= ctx.get(dut.packet.dw3_reserved[0]) << 3
                    events.append(("pkt",
                                   ctx.get(dut.packet.dw0),
                                   ctx.get(dut.packet.dw1),
                                   ctx.get(dut.packet.dw2),
                                   seq,
                                   ctx.get(dut.packet.delayed),
                                   ctx.get(dut.packet.deferred)))
                if ctx.get(dut.bad_packet):
                    events.append(("bad",))
                if ctx.get(dut.bad_sequence):
                    events.append(("badseq",))

            n = 0
            for beat in beats:
                if gap_every and n % gap_every == 0:
                    ctx.set(dut.sink.valid, 0)
                    await ctx.tick("ss")
                    sample()
                data = 0
                ctrl = 0
                for i, (b, c) in enumerate(beat):
                    data |= b << (8 * i)
                    ctrl |= c << i
                ctx.set(dut.sink.valid, 1)
                ctx.set(dut.sink.data, data)
                ctx.set(dut.sink.ctrl, ctrl)
                await ctx.tick("ss")
                sample()
                n += 1
            ctx.set(dut.sink.valid, 0)
            for _ in range(4):
                await ctx.tick("ss")
                sample()

        _run(dut, tb)
        return events

    def _expected(self, gen2):
        seq = self.GOOD_SEQ_GEN2 if gen2 else self.GOOD_SEQ
        return [
            ("pkt", 0x11223344, 0x55667788, 0x99AABBCC, seq, 0, 0),
            ("pkt", 0x01020304, 0x05060708, 0x090A0B0C, seq, 0, 0),
            ("pkt", 0xA0A1A2A3, 0xB0B1B2B3, 0xC0C1C2C3, seq, 0, 0),
            ("pkt", 0xD0D1D2D3, 0xE0E1E2E3, 0xF0F1F2F3, seq, 0, 0),
            ("pkt", 0x10111213, 0x20212223, 0x30313233, seq, 0, 0),
            ("pkt", 0x40414243, 0x50515253, 0x60616263, seq, 0, 0),
            ("bad",),
            ("bad",),
            ("badseq",),
            ("pkt", 0x21436587, 0xA9CBED0F, 0x00FF00FF, seq, 1, 1),
        ]

    def test_wide_matches_narrow_gen1(self):
        symbols = self._stimulus(gen2=False)
        narrow = self._run_receiver(1, False, symbols)
        wide   = self._run_receiver(2, False, symbols)
        self.assertEqual(narrow, self._expected(False),
                         "narrow receiver event sequence wrong")
        self.assertEqual(wide, narrow,
                         "wide receiver diverged from narrow (gen1)")

    def test_wide_matches_narrow_gen2(self):
        symbols = self._stimulus(gen2=True)
        narrow = self._run_receiver(1, True, symbols)
        wide   = self._run_receiver(2, True, symbols)
        self.assertEqual(narrow, self._expected(True),
                         "narrow receiver event sequence wrong (gen2)")
        self.assertEqual(wide, narrow,
                         "wide receiver diverged from narrow (gen2)")

    def test_wide_matches_narrow_with_gaps(self):
        symbols = self._stimulus(gen2=True)
        narrow = self._run_receiver(1, True, symbols, gap_every=3)
        wide   = self._run_receiver(2, True, symbols, gap_every=3)
        self.assertEqual(narrow, self._expected(True))
        self.assertEqual(wide, narrow,
                         "wide receiver lost state across a valid gap")


if __name__ == "__main__":
    unittest.main()
