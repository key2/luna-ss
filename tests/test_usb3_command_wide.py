#
# This file is part of LUNA.
#
# Copyright (c) 2026 the luna-ss contributors
# SPDX-License-Identifier: BSD-3-Clause
""" Width-program link-command framer fences (usb3_design.md 13.5).

At ``words=2`` a link command (LCSTART + duplicated command word,
8 symbols) fits exactly one beat -- but a real partner emits
constructs at 4-symbol granularity, so the wide detector must parse
commands at BOTH beat offsets (0 and 4).  These fences pin:

* detector: event-sequence equality (command, subtype) between the
  words=1 and words=2 elaborations over the same symbol stream --
  offset-0 and offset-4 commands, back-to-back offset-4 runs,
  corrupted CRC-5, replica mismatch, ctrl-bit garbage, valid gaps;
* generator: flat-symbol-stream equality (data+ctrl per symbol)
  between the widths over the same command list, under ready
  backpressure.

``words=1`` elaborations are the historical units verbatim.
"""

import unittest

from amaranth import Module
from amaranth.sim import Simulator

from luna.gateware.usb.usb3.link.command import (
    LinkCommandDetector, LinkCommandGenerator)

SLC = (0xFE, 1)
EPF = (0xF7, 1)
IDLE = (0x00, 0)


def crc5(v11):
    """The gateware CRC-5 xor tree (link/crc.py), bit for bit."""
    bits = [(v11 >> (10 - i)) & 1 for i in range(11)]  # bits[i] = MSB-first

    def xor(*idx):
        r = 0
        for i in idx:
            r ^= bits[i]
        return r

    return (
        (xor(10, 9, 8, 5, 4, 2)             << 0)
        | ((xor(10, 9, 8, 7, 4, 3, 1) ^ 1)  << 1)
        | (xor(10, 9, 8, 7, 6, 3, 2, 0)     << 2)
        | (xor(10, 7, 6, 4, 1)              << 3)
        | (xor(10, 9, 6, 5, 3, 0)           << 4)
    )


def lc_word(command, subtype):
    w = (subtype & 0xF) | ((command & 0xF) << 7)
    return w | (crc5(w) << 11)


def lc_syms(command, subtype, corrupt_crc=False, break_replica=False,
            ctrl_garbage=False):
    w = lc_word(command, subtype)
    if corrupt_crc:
        w ^= 0x8000
    lo, hi = w & 0xFF, (w >> 8) & 0xFF
    r_lo, r_hi = lo, hi
    if break_replica:
        r_lo ^= 0x01
    body_ctrl = 1 if ctrl_garbage else 0
    return [SLC, SLC, SLC, EPF,
            (lo, body_ctrl), (hi, 0), (r_lo, 0), (r_hi, 0)]


def _run(dut, tb):
    sim = Simulator(dut)
    sim.add_clock(1 / 125e6, domain="ss")
    sim.add_testbench(tb)
    sim.run()


class WideCommandDetectorEquivalence(unittest.TestCase):

    def _stimulus(self):
        """Symbol stream with commands at both offsets and invalid
        variants.  Idle padding shifts the 8-symbol beat phase."""
        s = []
        s += [IDLE] * 8
        s += lc_syms(0b0000, 5)                    # offset 0
        s += [IDLE] * 4                            # shift phase
        s += lc_syms(0b0001, 2)                    # offset 4
        s += lc_syms(0b0001, 3)                    # back-to-back offset 4
        s += lc_syms(0b0010, 0)                    # still offset 4
        s += [IDLE] * 4                            # realign
        s += lc_syms(0b0100, 1, corrupt_crc=True)  # invalid: CRC
        s += lc_syms(0b0011, 7)                    # offset 0, valid
        s += [IDLE] * 4
        s += lc_syms(0b0101, 4, break_replica=True)   # invalid: replica
        s += lc_syms(0b0110, 6, ctrl_garbage=True)    # invalid: ctrl
        s += lc_syms(0b0111, 1)                    # offset 4, valid
        s += [IDLE] * 8
        while len(s) % 8:
            s.append(IDLE)
        return s

    EXPECTED = [(0b0000, 5), (0b0001, 2), (0b0001, 3), (0b0010, 0),
                (0b0011, 7), (0b0111, 1)]

    def _run_detector(self, words, symbols, gap_every=0):
        dut = LinkCommandDetector(words=words)
        bpb = 4 * words
        events = []

        async def tb(ctx):
            beats = [symbols[k:k + bpb]
                     for k in range(0, len(symbols), bpb)]
            n = 0
            for beat in beats:
                if gap_every and n % gap_every == 0:
                    # A valid gap: the detector must hold state.
                    ctx.set(dut.sink.valid, 0)
                    await ctx.tick("ss")
                    if ctx.get(dut.new_command):
                        events.append((ctx.get(dut.command),
                                       ctx.get(dut.subtype)))
                data = 0
                ctrl = 0
                for i, (b, c) in enumerate(beat):
                    data |= b << (8 * i)
                    ctrl |= c << i
                ctx.set(dut.sink.valid, 1)
                ctx.set(dut.sink.data, data)
                ctx.set(dut.sink.ctrl, ctrl)
                await ctx.tick("ss")
                if ctx.get(dut.new_command):
                    events.append((ctx.get(dut.command),
                                   ctx.get(dut.subtype)))
                n += 1
            ctx.set(dut.sink.valid, 0)
            for _ in range(3):
                await ctx.tick("ss")
                if ctx.get(dut.new_command):
                    events.append((ctx.get(dut.command),
                                   ctx.get(dut.subtype)))

        _run(dut, tb)
        return events

    def test_wide_matches_narrow(self):
        symbols = self._stimulus()
        narrow = self._run_detector(1, symbols)
        wide   = self._run_detector(2, symbols)
        self.assertEqual(narrow, self.EXPECTED,
                         "narrow detector event sequence wrong")
        self.assertEqual(wide, self.EXPECTED,
                         "wide detector diverged (offsets 0/4 parse)")

    def test_wide_matches_narrow_with_gaps(self):
        symbols = self._stimulus()
        narrow = self._run_detector(1, symbols, gap_every=3)
        wide   = self._run_detector(2, symbols, gap_every=3)
        self.assertEqual(narrow, self.EXPECTED)
        self.assertEqual(wide, self.EXPECTED,
                         "wide detector lost state across a valid gap")


class WideCommandGeneratorEquivalence(unittest.TestCase):

    COMMANDS = [(0b0000, 15), (0b0001, 0), (0b0001, 4 | 2),
                (0b0010, 0), (0b0100, 1), (0b1000, 3)]

    def _run_generator(self, words, ready_stall=0):
        dut = LinkCommandGenerator(words=words)
        bpb = 4 * words
        out = []

        async def tb(ctx):
            cyc = 0
            for command, subtype in self.COMMANDS:
                ctx.set(dut.command, command)
                ctx.set(dut.subtype, subtype)
                ctx.set(dut.generate, 1)
                for _ in range(64):
                    # Optional backpressure on the source.
                    stall = ready_stall and (cyc % ready_stall == 0)
                    ctx.set(dut.source.ready, 0 if stall else 1)
                    cyc += 1
                    await ctx.delay(1e-9)
                    take = (ctx.get(dut.source.valid)
                            and ctx.get(dut.source.ready))
                    done = ctx.get(dut.done)
                    if take:
                        d = ctx.get(dut.source.data)
                        c = ctx.get(dut.source.ctrl)
                        for i in range(bpb):
                            out.append(((d >> (8 * i)) & 0xFF,
                                        (c >> i) & 1))
                    await ctx.tick("ss")
                    if take:
                        ctx.set(dut.generate, 0)
                    if done:
                        break
                else:
                    self.fail(f"generator (words={words}) never "
                              f"finished command {command:#x}")
                await ctx.tick("ss")

        _run(dut, tb)
        return out

    def test_wide_matches_narrow(self):
        expected = []
        for command, subtype in self.COMMANDS:
            expected += lc_syms(command, subtype)
        narrow = self._run_generator(1)
        wide   = self._run_generator(2)
        self.assertEqual(narrow, expected,
                         "narrow generator symbol stream wrong")
        self.assertEqual(wide, narrow,
                         "wide generator diverged from narrow")

    def test_wide_matches_narrow_backpressured(self):
        narrow = self._run_generator(1, ready_stall=3)
        wide   = self._run_generator(2, ready_stall=3)
        self.assertEqual(wide, narrow,
                         "wide generator diverged under backpressure")


if __name__ == "__main__":
    unittest.main()
