#
# This file is part of LUNA.
#
# Copyright (c) 2026 the luna-ss contributors
# SPDX-License-Identifier: BSD-3-Clause
""" Width-program CTC + aligner equivalence fences (usb3_design.md 13.5).

The 64-bit (``words=2``) skip remover, skip inserter and word/packet
aligners are the historical 32-bit units at twice the beat width.
These tests pin them against the narrow elaborations over the same
symbol streams:

* remover: byte-exact SKP-stripped output equality (wide vs narrow vs
  the software-stripped reference), SKPs at every byte lane, in runs,
  and straddling beat boundaries;
* inserter: stream preservation (non-SKP bytes untouched, in order),
  full-beat SKP-only insertion, and the Y/354 average rate with its
  carried remainder (bounded pending backlog at both widths);
* aligners: post-lock byte-exact equality against the narrow unit at
  the shared offsets, and lock at all eight byte offsets wide (COM
  burst for the word aligner, SHP/SLC framing for the packet aligner).

``words=1`` elaborations are the historical classes verbatim (covered
by test_usb3_ctc.py and the shipping-parity fence).
"""

import random
import unittest

from amaranth import Module
from amaranth.sim import Simulator

from luna.gateware.usb.usb3.physical.ctc import (
    CTCSkipRemover, CTCSkipInserter)
from luna.gateware.usb.usb3.physical.alignment import (
    RxWordAligner, RxPacketAligner)
from luna.gateware.usb.usb3.physical.coding import COM, SHP, EPF, SKP


SKP_BYTE = SKP.value  # 0x3c, ctrl=1


def _run(dut_module, tb):
    sim = Simulator(dut_module)
    sim.add_clock(1 / 125e6, domain="ss")
    sim.add_testbench(tb)
    sim.run()


def _beats(symbols, bytes_per_beat):
    """Groups a [(byte, ctrl)] list into (data_word, ctrl_word) beats."""
    assert len(symbols) % bytes_per_beat == 0
    out = []
    for k in range(0, len(symbols), bytes_per_beat):
        data = 0
        ctrl = 0
        for i in range(bytes_per_beat):
            b, c = symbols[k + i]
            data |= b << (8 * i)
            ctrl |= c << i
        out.append((data, ctrl))
    return out


class WideSkipRemoverEquivalence(unittest.TestCase):
    """The words=2 remover must emit the byte stream of the words=1 unit."""

    def _stimulus(self):
        """A symbol stream with SKPs in singles/pairs/runs at every lane."""
        rng = random.Random(0x517)
        symbols = []
        while len(symbols) < 512:
            burst = rng.randrange(4)
            if burst:
                # SKP runs of 1..4 symbols at arbitrary positions.
                symbols += [(SKP_BYTE, 1)] * rng.randrange(1, 5)
            n = rng.randrange(1, 9)
            for _ in range(n):
                b = rng.randrange(256)
                # Data bytes only; avoid aliasing a SKP symbol.
                symbols.append((b, 0))
        # Pad to a multiple of 8 with data bytes.
        while len(symbols) % 8:
            symbols.append((0x11, 0))
        return symbols

    def _run_remover(self, words, symbols):
        dut = CTCSkipRemover(words=words)
        bpb = 4 * words
        out = []

        async def tb(ctx):
            ctx.set(dut.source.ready, 1)
            ctx.set(dut.sink.valid, 1)
            for data, ctrl in _beats(symbols, bpb):
                ctx.set(dut.sink.data, data)
                ctx.set(dut.sink.ctrl, ctrl)
                await ctx.delay(1e-9)
                if ctx.get(dut.source.valid):
                    d = ctx.get(dut.source.data)
                    c = ctx.get(dut.source.ctrl)
                    for i in range(bpb):
                        out.append(((d >> (8 * i)) & 0xFF, (c >> i) & 1))
                await ctx.tick("ss")
            # Drain: keep clocking with idle input until the buffer runs dry.
            ctx.set(dut.sink.valid, 0)
            for _ in range(4):
                await ctx.delay(1e-9)
                if ctx.get(dut.source.valid):
                    d = ctx.get(dut.source.data)
                    c = ctx.get(dut.source.ctrl)
                    for i in range(bpb):
                        out.append(((d >> (8 * i)) & 0xFF, (c >> i) & 1))
                await ctx.tick("ss")

        _run(dut, tb)
        return out

    def test_wide_matches_narrow_and_reference(self):
        symbols = self._stimulus()
        stripped = [s for s in symbols if s != (SKP_BYTE, 1)]

        narrow = self._run_remover(1, symbols)
        wide   = self._run_remover(2, symbols)

        # Both outputs are prefixes of the stripped reference (a sub-beat
        # tail legitimately stays in the elastic buffer).
        self.assertEqual(narrow, stripped[:len(narrow)],
                         "narrow remover corrupted the stream")
        self.assertEqual(wide, stripped[:len(wide)],
                         "wide remover corrupted the stream")
        self.assertGreaterEqual(len(narrow), len(stripped) - 4)
        self.assertGreaterEqual(len(wide), len(stripped) - 8)

        # And byte-exact against each other over the common span.
        n = min(len(narrow), len(wide))
        self.assertEqual(wide[:n], narrow[:n],
                         "the 64-bit remover diverged from the 32-bit unit")


class WideSkipInserterProperties(unittest.TestCase):
    """The words=2 inserter preserves the stream and the Y/354 schedule."""

    N_BYTES = 4096  # > 11 * 354: several insertion rounds

    def _run_inserter(self, words):
        dut = CTCSkipInserter(words=words)
        bpb = 4 * words
        n_beats = self.N_BYTES // bpb
        out = []

        async def tb(ctx):
            ctx.set(dut.source.ready, 1)
            ctx.set(dut.can_send_skip, 1)
            seq = 0
            sent = 0
            while sent < n_beats:
                data = 0
                for i in range(bpb):
                    data |= ((seq + i) & 0xFF) << (8 * i)
                ctx.set(dut.sink.valid, 1)
                ctx.set(dut.sink.data, data)
                ctx.set(dut.sink.ctrl, 0)
                await ctx.delay(1e-9)
                if ctx.get(dut.sink.ready):
                    seq = (seq + bpb) & 0xFF
                    sent += 1
                await ctx.tick("ss")
                # The inserter's output register lags a cycle; sample it
                # after the edge.
                await ctx.delay(1e-9)
                if ctx.get(dut.source.valid):
                    d = ctx.get(dut.source.data)
                    c = ctx.get(dut.source.ctrl)
                    out.append((d, c))

        _run(dut, tb)
        return out

    def _check(self, out, words):
        bpb = 4 * words
        data_bytes = []
        skp_symbols = 0
        for d, c in out:
            syms = [((d >> (8 * i)) & 0xFF, (c >> i) & 1)
                    for i in range(bpb)]
            if any(s == (SKP_BYTE, 1) for s in syms):
                # Insertion beats must be *entirely* SKP symbols.
                self.assertTrue(
                    all(s == (SKP_BYTE, 1) for s in syms),
                    f"partial SKP beat: {[hex(b) for b, _ in syms]}")
                skp_symbols += bpb
            else:
                data_bytes += [b for b, _ in syms]

        # Stream preservation: the numbered sequence passes untouched.
        for k in range(1, len(data_bytes)):
            self.assertEqual(
                data_bytes[k], (data_bytes[k - 1] + 1) & 0xFF,
                f"data stream corrupted at byte {k}")

        # Schedule: one SKP ordered set (2 symbols) owed per 354 bytes;
        # pending backlog below the emission threshold is bounded by
        # (sets_per_beat - 1) sets.
        owed_sets = len(data_bytes) // 354
        sent_sets = skp_symbols // 2
        backlog = owed_sets - sent_sets
        self.assertGreaterEqual(
            backlog, 0, "inserter emitted more SKP sets than owed")
        self.assertLessEqual(
            backlog, 2 * words - 1,
            f"inserter fell behind the Y/354 schedule "
            f"({sent_sets} sent, {owed_sets} owed)")

    def test_narrow_properties(self):
        self._check(self._run_inserter(1), 1)

    def test_wide_properties(self):
        self._check(self._run_inserter(2), 2)


def _aligner_stimulus(offset, kind="com"):
    """A byte stream misaligned by ``offset``: junk, then repeated
    16-symbol training-set-shaped patterns, then payload."""
    rng = random.Random(0x519 + offset)
    symbols = [(0x55, 0)] * offset
    for rep in range(8):
        if kind == "com":
            symbols += [(COM.value, 1)] * 4
            body = 12
        else:
            symbols += [(SHP.value, 1)] * 3 + [(EPF.value, 1)]
            body = 12
        symbols += [((0x20 + rep * 16 + i) & 0xFF, 0) for i in range(body)]
    symbols += [(rng.randrange(0x01, 0xBB), 0) for _ in range(32)]
    while len(symbols) % 8:
        symbols.append((0x00, 0))
    return symbols


def _run_aligner(cls, words, symbols):
    dut = cls(words=words)
    bpb = 4 * words
    out = []

    async def tb(ctx):
        ctx.set(dut.source.ready, 1)
        ctx.set(dut.sink.valid, 1)
        for data, ctrl in _beats(symbols, bpb):
            ctx.set(dut.sink.data, data)
            ctx.set(dut.sink.ctrl, ctrl)
            await ctx.delay(1e-9)
            if ctx.get(dut.source.valid):
                d = ctx.get(dut.source.data)
                c = ctx.get(dut.source.ctrl)
                for i in range(bpb):
                    out.append(((d >> (8 * i)) & 0xFF, (c >> i) & 1))
            await ctx.tick("ss")
        # Flush the registered output.
        ctx.set(dut.sink.valid, 0)
        await ctx.delay(1e-9)
        if ctx.get(dut.source.valid):
            d = ctx.get(dut.source.data)
            c = ctx.get(dut.source.ctrl)
            for i in range(bpb):
                out.append(((d >> (8 * i)) & 0xFF, (c >> i) & 1))
        await ctx.tick("ss")

    _run(dut, tb)
    return out


def _post_lock(stream, marker):
    """The stream from the first occurrence of the 4-symbol marker."""
    for k in range(len(stream) - 3):
        if tuple(stream[k:k + 4]) == marker:
            return stream[k:]
    return None


class WideAlignerEquivalence(unittest.TestCase):

    COM_MARKER = ((COM.value, 1),) * 4
    SHP_MARKER = ((SHP.value, 1),) * 3 + ((EPF.value, 1),)

    def test_word_aligner_locks_at_all_offsets(self):
        """words=2 must lock the COM burst to byte 0 at offsets 0..7."""
        for offset in range(8):
            symbols = _aligner_stimulus(offset, "com")
            expected = _post_lock(symbols, self.COM_MARKER)
            out = _run_aligner(RxWordAligner, 2, symbols)
            got = _post_lock(out, self.COM_MARKER)
            self.assertIsNotNone(got, f"no lock at offset {offset}")
            n = min(len(got), len(expected))
            # The aligned output must reproduce the stream from the TS
            # start; the aligner's lock beat lands the marker at lane 0.
            self.assertEqual(
                got[:n], expected[:n],
                f"wide word aligner corrupted the stream at offset {offset}")
            self.assertEqual(len(got) % 8, 0,
                             f"marker not at lane 0 at offset {offset}")

    def test_word_aligner_matches_narrow(self):
        """At the shared offsets the wide unit emits the narrow stream."""
        for offset in range(4):
            symbols = _aligner_stimulus(offset, "com")
            narrow = _post_lock(_run_aligner(RxWordAligner, 1, symbols),
                                self.COM_MARKER)
            wide = _post_lock(_run_aligner(RxWordAligner, 2, symbols),
                              self.COM_MARKER)
            self.assertIsNotNone(narrow)
            self.assertIsNotNone(wide)
            n = min(len(narrow), len(wide))
            self.assertEqual(
                wide[:n], narrow[:n],
                f"wide/narrow word aligners diverged at offset {offset}")

    def test_packet_aligner_locks_at_all_offsets(self):
        """words=2 packet realigner locks SHP framing at offsets 0..7."""
        for offset in range(8):
            symbols = _aligner_stimulus(offset, "shp")
            expected = _post_lock(symbols, self.SHP_MARKER)
            out = _run_aligner(RxPacketAligner, 2, symbols)
            got = _post_lock(out, self.SHP_MARKER)
            self.assertIsNotNone(got, f"no lock at offset {offset}")
            n = min(len(got), len(expected))
            self.assertEqual(
                got[:n], expected[:n],
                f"wide packet aligner corrupted the stream "
                f"at offset {offset}")
            self.assertEqual(len(got) % 8, 0,
                             f"marker not at lane 0 at offset {offset}")


if __name__ == "__main__":
    unittest.main()
