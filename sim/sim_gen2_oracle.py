#!/usr/bin/env python3
"""Gen2 coding oracle vs the silicon-proven RTL — battery entry
``gen2-oracle`` (must stay GREEN).

Pins ``gen2_coding.ScramblerModel`` byte-exact against
``gw_usb3.scramble.Scrambler`` and ``Descrambler`` (the
equivalence-proven, Gen2-silicon-proven RTL) over a block battery
covering every block type and rule: SYNC reset, TSEQ/TS1/TS2 partial
scrambling, SKP freeze + LFSR splice, SDS bypass-with-advance, data
blocks, and back-to-back mixes.

Two checks per direction:

* TX: python-scrambled beats == RTL ``Scrambler`` output beats.
* RX: RTL ``Descrambler`` fed with the python-scrambled stream must
  reproduce the original cleartext beats (SKP LFSR symbols excepted:
  there the RTL forwards the received state symbols).

Run from the fork root: .venv/bin/python -u sim/sim_gen2_oracle.py
"""

import random
import sys
from pathlib import Path

# luna/gw_usb3 are installed packages; gen2_coding sits beside us.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from amaranth import Module
from amaranth.sim import Simulator

from gw_usb3.scramble import Scrambler, Descrambler
from gw_usb3.tables import BLOCK_CONTROL, BLOCK_DATA

from gen2_coding import (Block, ScramblerModel, sync_block, tseq_block,
                         ts1_block, ts2_block, sds_block, skp_block,
                         data_block, idle_block, pack_symbol_stream,
                         link_command_syms, header_packet_syms)

SEED = 2026


def block_battery():
    rng = random.Random(SEED)
    blocks = []
    # training-shaped preamble
    blocks += [sync_block()]
    blocks += [tseq_block()] * 4
    blocks += [sync_block()]
    blocks += [ts1_block()] * 8
    blocks += [skp_block()]
    blocks += [ts1_block(), ts2_block(0x01), ts2_block(0x01)]
    blocks += [sync_block()]
    blocks += [ts2_block(0x01)] * 4
    # data stream entry
    blocks += [sds_block()]
    blocks += [idle_block()] * 3
    # framed content (link command + header packet + payload-ish data)
    syms = link_command_syms(0b0000, 3)               # LGOOD_3
    syms += header_packet_syms(0x00000004, 0x01020304, 0x0A0B0C0D, seq=5)
    blocks += pack_symbol_stream(syms)
    blocks += [skp_block()]                           # SKP inside data stream
    for _ in range(4):
        blocks += [data_block([rng.randrange(256) for _ in range(16)])]
    blocks += [skp_block()]
    blocks += [idle_block()] * 2
    # re-train (recovery-shaped): SYNC resets mid-stream
    blocks += [sync_block()]
    blocks += [ts1_block()] * 3
    blocks += [sds_block()]
    blocks += [idle_block()] * 2
    return blocks


def flatten(blocks):
    return [beat for blk in blocks for beat in blk.beats()]


def main():
    blocks = block_battery()
    clear = flatten(blocks)
    model_tx = ScramblerModel()
    scrambled = []
    for (s, h, d) in clear:
        scrambled.append((s, h, model_tx.feed(s, h, d)))

    # The RTL descrambler drops SKP beats from its output and reseeds
    # its LFSR from descrambler_init (wired from the RxGearbox132's
    # SKP-payload extraction in the PHY).  The splice carries the
    # FROZEN transmitter state -- exactly the state the next scrambled
    # beat's keystream derives from -- so the reseed is alignment-
    # neutral for an in-sync receiver and alignment-establishing for an
    # acquiring one (this sim's early iterations pinned that; a
    # spliced ADVANCED state would desync the pair by one advance).
    skp_beats = set()
    idx = 0
    for blk in blocks:
        n = len(blk.syms) // 8
        if n == 3:
            skp_beats.update(range(idx, idx + 3))
        idx += n
    clear_stripped = [b for i, b in enumerate(clear) if i not in skp_beats]
    # descrambler_init per beat: the spliced (frozen) state of the most
    # recent SKP OS, as the gearbox would present it.
    seed_by_beat = []
    last = 0
    for i, (s, h, d) in enumerate(scrambled):
        if i in skp_beats and (i - 2) in skp_beats and (i + 1) not in skp_beats:
            last = d & 0x7FFFFF          # third SKP beat: spliced state
        seed_by_beat.append(last)

    # Host-model self-check: the python descrambler (which DOES see the
    # full stream, SKPs included, when decoding device TX) must
    # reproduce the cleartext.
    model_rx = ScramblerModel(descramble=True)
    for i, ((s, h, d), (cs, ch, cd)) in enumerate(zip(scrambled, clear)):
        got = model_rx.feed(s, h, d)
        if i in skp_beats:
            continue                    # SKP symbols pass through as-is
        if got != cd:
            print(f"FAIL python-RX beat {i}: {got:016x} != {cd:016x}")
            return 1

    m = Module()
    m.submodules.scr = scr = Scrambler()
    m.submodules.dsc = dsc = Descrambler()

    failures = []

    async def tb(ctx):
        ctx.set(scr.data_out_ready, 1)
        ctx.set(dsc.LTSSM_is_Training, 0)
        # ---- TX direction: RTL Scrambler vs python model ----
        outs = []

        async def drive(dut, beats, out_list, n_expected, seeds=None):
            fed = 0
            collected = 0
            idle = 0
            while collected < n_expected and idle < 64:
                if fed < len(beats):
                    s, h, d = beats[fed]
                    ctx.set(dut.data_in_valid, 1)
                    ctx.set(dut.data_in_start_block, s)
                    ctx.set(dut.data_in_block_head, h)
                    ctx.set(dut.data_in, d)
                    if seeds is not None:
                        ctx.set(dut.descrambler_init, seeds[fed])
                    fed += 1
                else:
                    ctx.set(dut.data_in_valid, 0)
                await ctx.tick()
                if ctx.get(dut.data_out_valid):
                    out_list.append((ctx.get(dut.data_out_start_block),
                                     ctx.get(dut.data_out_block_head),
                                     ctx.get(dut.data_out)))
                    collected += 1
                    idle = 0
                else:
                    idle += 1

        await drive(scr, clear, outs, len(clear))
        if len(outs) != len(clear):
            failures.append(f"TX: RTL produced {len(outs)}/{len(clear)} beats")
        for i, ((es, eh, ed), (gs, gh, gd)) in enumerate(zip(scrambled, outs)):
            if (es, eh, ed) != (gs, gh, gd):
                failures.append(
                    f"TX beat {i}: model start={es} head={eh:x} "
                    f"data={ed:016x} != RTL start={gs} head={gh:x} "
                    f"data={gd:016x}")
                if len(failures) > 8:
                    return

        # ---- RX direction: RTL Descrambler recovers the cleartext ----
        # Full stream (SKPs included; the RTL drops them from its
        # output), acquisition seed driven like the PHY wires it.
        expected_rx = clear_stripped
        outs_rx = []
        await drive(dsc, scrambled, outs_rx, len(expected_rx),
                    seeds=seed_by_beat)
        if len(outs_rx) != len(expected_rx):
            failures.append(
                f"RX: RTL produced {len(outs_rx)}/{len(expected_rx)} beats")
        for i, ((es, eh, ed), (gs, gh, gd)) in enumerate(
                zip(expected_rx, outs_rx)):
            if (es, eh, ed) != (gs, gh, gd):
                failures.append(
                    f"RX beat {i}: expect start={es} head={eh:x} "
                    f"data={ed:016x} got start={gs} head={gh:x} "
                    f"data={gd:016x}")
                if len(failures) > 16:
                    return

    sim = Simulator(m)
    sim.add_clock(1 / 156.25e6)
    sim.add_testbench(tb)
    sim.run()

    if failures:
        for f in failures[:16]:
            print("FAIL", f)
        print("GEN2 ORACLE FAIL")
        return 1
    print(f"GEN2 ORACLE PASS: {len(clear)} beats TX-exact, "
          f"{len(scrambled)} beats RX-recovered vs RTL "
          f"({len(blocks)} blocks incl. SYNC/TSEQ/TS1/TS2/SKP/SDS/data)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
