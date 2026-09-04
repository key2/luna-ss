#
# This file is part of LUNA.
#
# Copyright (c) 2026 the luna-ss contributors
# SPDX-License-Identifier: BSD-3-Clause
""" Gen2 TX request-seam conformance (the #45 sim leads, HANDOVER 10u).

Two seam hazards against the closed-loop (#44) block transmitter:

* BLIP: the LTSSM burst-request/idle-mode surface can (pre-fix, DID:
  the Polling.Idle->U0 seam in link/layer.py mixes a comb decode with
  a 1-cycle-late registered ``link_ready``) present a 1-cycle low gap
  to the scheduler's registered ``active`` gate.  The historical
  inactive arm wiped beat_idx/mode/skp_gap/sds_pending IMMEDIATELY --
  mid-block, when the gap landed at the wrong parity: the PIPE then
  received a start beat with no continuation (a TRUNCATED 132-bit
  block), desynchronizing the PHY TX gearbox against the standing
  ~16-beat FIFO and corrupting every subsequent block at the host's
  receiver.  Test: inject a 1-cycle idle_mode gap at EVERY alignment
  in a window; the emitted block stream must stay well-formed (every
  start followed by exactly its block's beats; SKP = 3, others = 2)
  and exactly ONE SDS may be emitted per data-stream start.

* STALE FLUSH: a recovery entry resets the link layer's LC generator
  mid-command; the TX bridge (which closes an open packet when the
  NEXT first-marked word arrives) then held the truncated fragment
  across the retrain and flushed it -- padded with idle -- onto the
  freshly trained link AHEAD of the header-sequence advertisement.
  The fragment [SLC SLC SLC EPF][5A 5A 5A 5A] even aliases a
  REPLICA-VALID link command (both halves 0x5A5A).  Test: capture a
  half LC, yank idle_mode (recovery), re-enter, send a fresh LC; the
  block stream must carry ONLY the two complete LCs -- no fragment.
"""

import unittest

from amaranth.sim import Simulator

from luna.gateware.usb.usb3.physical.gen2 import Gen2BlockTransmitter

# Gen1 K-codes (the 32-bit link dialect) and Gen2 symbols.
K_SLC, K_EPF = 0xFE, 0xF7
G2_SLC, G2_EPF, G2_IDL, SDS_ID, SKP_SYM = 0x4B, 0x36, 0x5A, 0xE1, 0xCC

LCSTART_WORD = int.from_bytes(bytes([K_SLC, K_SLC, K_SLC, K_EPF]), "little")

BLOCK_CONTROL = 0xC
BLOCK_DATA    = 0x3


class BlockStreamChecker:
    """Tracks the PIPE block framing cycle by cycle."""

    def __init__(self):
        self.errors = []
        self.blocks = []          # (head, [syms]) completed blocks
        self._open = None         # (head, [syms], beats_expected)

    def cycle(self, valid, start, head, data):
        if not valid:
            return
        syms = [(data >> (8 * (7 - i))) & 0xFF for i in range(8)]
        if start:
            if self._open is not None:
                head_o, syms_o, need = self._open
                self.errors.append(
                    f"TRUNCATED block: start_block while {len(syms_o)}/8*"
                    f"{need} symbols of a head-{head_o:x} block pending")
            beats = 3 if (head == BLOCK_CONTROL and syms[0] == SKP_SYM) else 2
            self._open = (head, list(syms), beats)
            self._maybe_close()
        else:
            if self._open is None:
                self.errors.append("orphan continuation beat (no open block)")
                return
            head_o, syms_o, need = self._open
            syms_o += syms
            self._open = (head_o, syms_o, need)
            self._maybe_close()

    def _maybe_close(self):
        head, syms, need = self._open
        if len(syms) >= 8 * need:
            self.blocks.append((head, syms))
            self._open = None

    def sds_count(self):
        return sum(1 for h, s in self.blocks
                   if h == BLOCK_CONTROL and s[0] == SDS_ID)

    def data_symbols(self):
        out = []
        for h, s in self.blocks:
            if h == BLOCK_DATA:
                out += s
        return out

    def constructs(self):
        """Parse the data-symbol stream into LC constructs; anything
        that is neither idle nor a complete LC is an error."""
        s = self.data_symbols()
        found = []
        i = 0
        while i < len(s):
            if s[i] == G2_IDL:
                i += 1
                continue
            if (i + 8 <= len(s) and s[i] == G2_SLC and s[i+1] == G2_SLC
                    and s[i+2] == G2_SLC and s[i+3] == G2_EPF):
                body = s[i+4:i+8]
                found.append(tuple(body))
                i += 8
                continue
            found.append(("junk", tuple(s[i:i+8])))
            i += 8
        return found


class Gen2TxSeamTest(unittest.TestCase):

    FIFO_DEPTH = 32

    def _simulate(self, tb_body):
        dut = Gen2BlockTransmitter(tseq_count=65536)
        checker = BlockStreamChecker()
        state = {"level": 0, "cyc": 0}

        async def step(ctx, n=1):
            for _ in range(n):
                ctx.set(dut.tx_fifo_level, min(state["level"], 31))
                await ctx.tick("ss")
                v = ctx.get(dut.tx_valid)
                checker.cycle(v, ctx.get(dut.tx_start),
                              ctx.get(dut.tx_head), ctx.get(dut.tx_data))
                if v:
                    state["level"] += 1
                if state["cyc"] % 33 != 0 and state["level"] > 0:
                    state["level"] -= 1
                state["cyc"] += 1

        async def tb(ctx):
            await tb_body(ctx, dut, step)

        sim = Simulator(dut)
        sim.add_clock(1 / 156.25e6, domain="ss")
        sim.add_testbench(tb)
        sim.run()
        return checker

    # ── the blip ─────────────────────────────────────────────────────

    def test_idle_mode_blip_all_alignments(self):
        """A 1-cycle idle_mode gap at ANY alignment must not truncate a
        block on the PIPE, and must not restart the SDS."""
        for offset in range(12):
            with self.subTest(offset=offset):
                async def body(ctx, dut, step, _off=offset):
                    ctx.set(dut.idle_mode, 1)
                    await step(ctx, 200)          # SDS + idle stream, loop hovers
                    await step(ctx, _off)         # alignment
                    ctx.set(dut.idle_mode, 0)     # the blip
                    await step(ctx, 1)
                    ctx.set(dut.idle_mode, 1)
                    await step(ctx, 200)

                checker = self._simulate(body)
                self.assertEqual(checker.errors, [],
                                 f"offset {offset}: {checker.errors[:3]}")
                self.assertEqual(checker.sds_count(), 1,
                                 f"offset {offset}: SDS emitted "
                                 f"{checker.sds_count()} times (data stream "
                                 f"restarted mid-U0)")

    # ── the stale flush ──────────────────────────────────────────────

    async def _send_word(self, ctx, dut, step, data, ctrl, first):
        ctx.set(dut.sink.data, data)
        ctx.set(dut.sink.ctrl, ctrl)
        ctx.set(dut.sink.first, first)
        ctx.set(dut.sink.valid, 1)
        # wait for acceptance
        for _ in range(64):
            ready = ctx.get(dut.sink.ready)
            await step(ctx, 1)
            if ready:
                break
        ctx.set(dut.sink.valid, 0)
        ctx.set(dut.sink.first, 0)

    async def _send_lc(self, ctx, dut, step, word16):
        payload = word16 | (word16 << 16)
        await self._send_word(ctx, dut, step, LCSTART_WORD, 0b1111, 1)
        await self._send_word(ctx, dut, step, payload, 0b0000, 0)
        # close the construct the way the link layer does: idle filler
        # (data 0, ctrl 0) marked ``first``.
        await self._send_word(ctx, dut, step, 0, 0b0000, 1)

    def test_recovery_yank_no_stale_fragment(self):
        """An LC truncated by a link-down must never surface on the
        retrained link; only complete constructs may be emitted."""
        async def body(ctx, dut, step):
            ctx.set(dut.idle_mode, 1)
            await step(ctx, 120)

            # A complete LC before the yank.
            await self._send_lc(ctx, dut, step, 0x1234)
            await step(ctx, 60)

            # Half an LC: the generator is cut by the retrain after the
            # framing word.
            await self._send_word(ctx, dut, step, LCSTART_WORD, 0b1111, 1)

            # Recovery: idle mode drops, TS1/TS2 bursts run.
            ctx.set(dut.idle_mode, 0)
            ctx.set(dut.send_ts1_burst, 1)
            await step(ctx, 80)
            ctx.set(dut.send_ts1_burst, 0)
            ctx.set(dut.send_ts2_burst, 1)
            await step(ctx, 80)
            ctx.set(dut.send_ts2_burst, 0)
            ctx.set(dut.idle_mode, 1)         # U0 re-entry
            await step(ctx, 40)

            # The fresh (advertisement) LC.
            await self._send_lc(ctx, dut, step, 0x5678)
            await step(ctx, 120)

        checker = self._simulate(body)
        self.assertEqual(checker.errors, [], checker.errors[:3])
        constructs = checker.constructs()
        expected = [(0x34, 0x12, 0x34, 0x12), (0x78, 0x56, 0x78, 0x56)]
        self.assertEqual(
            constructs, expected,
            f"stale fragment leaked across the retrain: {constructs}")


if __name__ == "__main__":
    unittest.main()
