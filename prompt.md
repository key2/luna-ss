# Mission: the WIDTH PROGRAM, single lane only — make our USB 3.2
# device stack width-generic (64-bit AND 128-bit cores) so every
# shipping configuration closes timing cleanly: Gen 1x1 on the 64-bit
# core as today, Gen 1x1 and Gen 2x1 on the 128-bit core.  Resolve
# open bug #45 on the way (it unblocks Gen2 enumeration).  This
# supersedes the 64-bit Gen2 timing fight: a Gen2 64-bit trim that
# misses timing is ACCEPTABLE as long as the 128-bit trim meets it.

Context, so there is no confusion about the nature of this work: this
is **forward engineering and validation of our own device stack**, in
our own repositories.  Everything here is code we wrote or
BSD-3-Clause open source we maintain as a public fork with license
and copyright headers intact (`luna-ss`, our fork of the LUNA USB
framework), plus our own `gw_usb3` PHY implementation and our
`gowin-serdes` board-support library as submodules.  We develop and
test on our own dev board on our own bench, and we validate behavior
against the **published USB 3.2 Revision 1.1 specification** (markdown
copy in `doc/USB 3.2 Revision 1.1.pdf/markdown.md`; also the PIPE
architecture spec and the USB 3.1 Link Layer test spec in `doc/`).
The link partner is the standard Linux xHCI host on the bench PC
(dmesg, usbmon, PORTSC, our on-chip probes).  The manufacturer's
reference design that ships with the dev kit (`prj.fs` in the frozen
`~/Downloads/GW_USB3` archive) is used unmodified, only as a
known-good link-partner baseline to verify that the bench port and
cable are healthy.

Read `HANDOVER.md` first — **§10u** (session 15) is the whole story:
bugs #42/#43/#44 found and fixed, the #45 evidence trail, the bench
recovery procedures, and the two BINDING scope decisions this prompt
implements.  Then §10t (session 14) for the W0 width-trim verdicts
this program builds on, and `doc/usb3_design.md` + the
`physical/gen2.py` docstring for the stage-A architecture.

## Why this program (the bench owner's decisions, now binding)

1. The 64-bit stage-A core at the Gen2 rate needs pclk ≥ 156.25 and
   rxclk ≥ 161.29 (the honest gates; see §10u).  Session 15 burned
   ~30 placement-seed rolls across four netlist revisions to close it
   twice; every RTL change re-enters that lottery.  **At a 128-bit
   core width the Gen2 core clock is 78.125 MHz and the fight
   disappears.**
2. **Gen 1x2 is out of scope permanently.**  Neither the bench xHCI
   (80:14.0) nor TB4 hosts support x2 lane bonding; nearly nothing in
   the field does.  We use ONE lane, period.  The x2 negotiation
   artifacts already in the tree (gen1x2 example, ssp_capability
   surface) stay as-is but receive no further work.

## The target matrix (all single-lane)

| config | core width | core clock | status target |
|--------|-----------|------------|---------------|
| Gen 1x1 | 64 | 125 | the SHIPPING build — stays bitstream-payload-identical and ladder-green throughout (the fence) |
| Gen 1x1 | 128 | 62.5 | NEW: native serdes trim (W0: "the 62.5 native trim is real") — build, timing, full ladder |
| Gen 2x1 | 128 | 78.125 | NEW: the Gen2 ship vehicle — 2:1 bridge at the PIPE boundary (W0 verdict: the 10G serdes fabric attach is fixed at 64-bit/156.25; native 128 is impossible on this fabric) — timing MET, #45 resolved, **10000M enumeration + ladder** |
| Gen 2x1 | 64 | 156.25 | kept sim-green and buildable; timing is OPTIONAL (bench-debug vehicle only when a lottery happens to win) |

The PHY side (`gw_usb3`) keeps its proven 64-bit/156.25 datapath at
Gen2 (rxclk truly 161.133 — the 6.2 ns SDC from §10u stays) and gains
whatever narrow shims the 2:1 PIPE bridge needs; at Gen1/128 the
serdes attach itself moves to the native 62.5 trim.  The proven 5G
configuration is pinned by the PHY's regression suite and must not
change behavior.

## Deliverables

1. **Width-generic core**: `core_width ∈ {64, 128}` as an elaboration
   parameter through the LUNA stack (link + protocol + endpoints +
   the Gen2 block machinery), sim-proven at BOTH widths.
2. **The Gen1 fence intact**: the 64-bit Gen1 shipping build remains
   payload-identical (timestamp bytes only) after every shared-file
   change, and ladder-green on hardware.
3. **Gen 1x1 @ 128 on hardware**: enumeration 5000M + the full
   multiep ladder, sha-exact, uart1 ch0 clean.
4. **Gen 2x1 @ 128 on hardware**: timing MET (core 78.125; PHY pclk
   156.25 / rxclk 161.29), **bug #45 resolved**, `lsusb` shows
   **10000M** on port 4-3, dmesg clean, then the Gen2 ladder
   (1 MiB ×10 → 16 → 64 MiB ×3 → soak, sha-exact, per-pipe MB/s,
   wire checker ported and calibrated).
5. **The dual-rate matrix, re-scoped without x2** (this closes the
   original G5 mission): the Gen2/128 image on the 5G hub port falls
   back per spec and runs the Gen1 ladder; replug/POR ×5 on both
   ports; the forced-Gen1 build re-laddered.  Recorded verdict table.

HANDOVER continues at **§10v**; bug numbering continues at **#46**
(#45 is open and comes first among bugs).

## Phase plan (each phase gated; one mechanism per change, as always)

### V0 — orientation and the fence (half a day)

Read HANDOVER §10r–§10u.  Re-verify the Gen1 fence on the bench
(enumeration 5000M on 4-3, 1 MiB ×10, 16 ×3, 64 ×3, sha-exact, uart1
ch0 = 0) BEFORE touching anything; the fence image is
`/tmp/kilo/h0_gen1_fence.fs`.  Update `doc/usb3_design.md` with the
width-program plan: the clock/width matrix above, the 2:1 bridge
placement (which logic stays in the 156.25 pclk domain — the PHY
datapath, the width converter, and as little else as possible — and
which moves to the 78.125 core domain — the block grammar engines,
LTSSM, link, protocol; timer constants recompute from
`sync_frequency`), and the domain-crossing inventory at the bridge.
Design note first, code second.

### V1 — the width-generic core, sim-proven (the big one)

- Introduce `core_width` and make the Gen1 dialect stack elaborate at
  64 (bit-identical to today — the parity constraint is the proof)
  and at 128.  Expect the work to concentrate in: stream widths and
  `USBRawSuperSpeedStream`, the header/DPP framers and CRC units, the
  Gen2 block bridges (`physical/gen2.py` stage-A machinery is
  64-bit-shaped: the beat/half/sub walk generalizes or gets a
  128-bit twin), the data FIFOs, and every hard-coded `32`/`4`-byte
  assumption in the protocol layer.
- Sim discipline: the FULL battery (now 53 entries) must pass with
  the 64-bit elaborations untouched-green at every step; add
  width-parallel entries for the core Gen2 phases (`train`, `enum`,
  `echo`, `u0`, `hotreset`, `recovery`, `rxchain`) at 128.  New sims
  red-first where a mechanism is new (the bridge!).
- **Gen1-64 shipping parity after every shared-file change** — the
  established payload-compare trick, non-negotiable.
- The 2:1 PIPE bridge (Gen2/128 ↔ PHY 64@156.25): design it as the
  ONLY new pclk-domain logic; keep it register-thin.  The #44
  closed-loop pacing reference (`tx_fifo_occupancy`) crosses here —
  decide and document on which side the pacing decision lives.

### V2 — Gen1 on hardware, both widths

- 64-bit: rebuild, payload-compare, flash, full ladder (this is the
  fence re-proof after V1's churn).
- 128-bit @ 62.5 native trim: new example top (`luna-multiep-w128` or
  a knob on the existing top), timing gate (62.5 core — should be
  trivial), flash, enumeration 5000M, full ladder with recorded
  verdicts.  This validates the width machinery on silicon at the
  friendly rate BEFORE Gen2 depends on it.

### V3 — Gen 2x1 @ 128 on hardware (the Gen2 gate, and #45)

- Build `luna-enum-gen2` at core_width=128 with the bridge.  Timing
  gate: core domain ≥ 78.125, PHY pclk ≥ 156.25, rxclk ≥ 161.29
  (`tools/gowin_timing_report.py <build> --section fmax`).  The
  pclk-domain content is now small — if it still misses, the cone
  report names the bridge, and the bridge gets fixed, not lotteried.
- **Bug #45 first**: the metronomic ~7.05 µs U0→Recovery loop
  (§10u: all recoveries OURS, clean CRCs, zero accepted headers,
  introduced alongside the #44 closed-loop netlist).  The per-cause
  probe loadout (uart0 ch1..3 = recovery timers/rx/tx) is already in
  the tree — at 128-bit it will finally close timing without a
  lottery.  Flash, read which cause counts ~142k/s, chase that
  mechanism.  Cheap sim leads queued in §10u: (a) drive the LTSSM
  burst-request seams with 1-cycle blips against the closed-loop
  transmitter and watch for tx_start desync against the standing
  16-beat FIFO (the transmitter's inactive arm wipes
  beat_idx/mode/sds_pending mid-stream — make it drain-safe if
  implicated); (b) deliver the host's link-up advertisement
  CONCURRENT with the device's own U0 entry (on silicon the host
  gets there first; our LC detector sits in ResetInserter(~enable)
  and may eat it).  Sim-reproduce red-first if either lands.
- Gate: `lsusb` shows **10000M** on 4-3, dmesg clean, LED on,
  recorded uart + PORTSC captures.  Then the Gen2 ladder
  (deliverable 4) with the wire checker ported to Gen2 framing and
  calibrated on a quiet pipe before being believed.

### V4 — the dual-rate matrix (G5 close, re-scoped, no x2)

| run | image | port | expected | record |
|-----|-------|------|----------|--------|
| 1 | Gen2/128 multiep | 4-3 (10G) | 10000M + Gen2 ladder | lsusb, MB/s, ch0 |
| 2 | same image | hub 4-8.x (5G) | per-spec fallback → 5000M + full Gen1 ladder | lsusb, MB/s, ch0 |
| 3 | same image, replug/POR ×5 | both ports | right rate every time | per-cycle verdicts |
| 4 | shipping Gen1-64 build | 4-3 | 5000M + Gen1 ladder (fence numbers) | parity + verdicts |
| 5 | Gen1-128 build | 4-3 | 5000M + Gen1 ladder | verdicts |

**The gate = the table fully recorded.**  That closes the dual-rate
mission on the width program's terms.

## Parked items that stay on the books (do not lose them)

#37 (truncated inbound DPP never retried, FORCE_REC_AT=710 repro);
rule-2d/#36 positive-validation stimuli; the bench forced-recovery
verdict for #29–#31 (uart1 'R' hook is in the tree — run it during
V3's ladder); data_tx SEND_ZLP bare-ready; wire-checker TP blindness;
SKP x=4 aligner behind an elaboration knob; the enum-surface gaps
(SSP BOS device capability + Sublink Speed Device Notification TP
[8.5.6.7, 9.6.2.5] — bcdUSB is 0310; Linux enumerated regardless on
good boots, but close them during V3 if dmesg complains); stage-B
credit scaling beyond 4+4 (the 8 RX header buffers landed as #42).

## Keep the discipline that closed forty-four bugs

- Sim first: every RTL change re-proves the touched battery section;
  the FULL battery from a SETTLED tree before each hardware build —
  never concurrent with source edits (session 15 had to re-run one
  for exactly this).
- Gen1-64 entries are a regression fence, never a casualty; shipping
  parity (payload compare vs `/tmp/kilo/h0_gen1_fence.fs`) after
  every Gen1-shared-file change.
- One mechanism per change; hardware ladder with recorded verdicts
  before the next change; watch uart1 ch0 on every run.
- A Gen2 build that misses ITS width's timing gate is never flashed
  for Gen2 runs.  (The 64-bit Gen2 trim missing timing is expected
  and fine — it just doesn't get flashed.)
- New bugs: **#46+** (after #45), findings into HANDOVER §10v as you
  go; commit submodules first (gowin-serdes is PUBLIC — keep it
  clean), then the fork; push everything.

## Tooling and bench facts (verify before trusting)

- One clone: `git clone --recurse-submodules
  github.com/key2/luna-ss && pdm install -G :all`.  Frozen archive =
  `~/Downloads/GW_USB3` (ARCHIVE.md maps it; the reference `prj.fs`
  baseline lives there).
- Board on 10G root port **`usb 4-3`** (straight = LN1 = correct;
  flipped = Q0_LN0 = probe-only).  5G test path = hub at `4-8.x`.
  Flash: `sudo -n openFPGALoader -c ft232 <fs>`.  Board KEY replays
  POR without reflashing; the device parks in SS.Disabled ~360 ms
  after boot, so every test wants a fresh POR.
- **Bench hygiene from §10u**: after repeated failed attempts the
  xHCI port can WEDGE (endless warm-reset loop against a
  Not-connected port, even with the cable out).  Un-wedge: PCI
  unbind/rebind of `0000:80:14.0`.  The reference `prj.fs` at 10000M
  is the port-health oracle — run it after any wedge before trusting
  new data.  PORTSC tracer: `/tmp/kilo/portsc_trace.py` (bus4-port3 =
  debugfs **port19**).  Hub debug: `echo 'file hub.c +p' >
  /sys/kernel/debug/dynamic_debug/control`.
- UARTs by stable path (tty numbers are volatile): uart0/uart1 =
  `/dev/serial/by-id/usb-FTDI_Quad_RS232-HS-if02/if03-port0` @115200;
  `uart_capture.py <s> <prefix>` interleaves both (already by-id).
  Boot-outcome A/B harness: `/tmp/kilo/boot_ab.sh <fs> <tag>`.
- Verdicts: `multiep_test.py <MiB> --eps 1,2,3` (sudo; warmup on).
  usbmon at `/sys/kernel/debug/usb/usbmon/4u`; `sudo -n dmesg` works.
- **Run sims as `.venv/bin/python -u`** (`timeout`+`pdm run` orphans
  children).  Battery: `pdm run battery` (53 entries), logs in
  `/tmp/kilo/batt_*.log`.  Gen2 sim knobs: `PHASE=` (now incl.
  `hotreset`, `recovery`), `TSEQ_LEN=64` (always for
  train/enum/echo/u0/hotreset/recovery), `TSCALE=0.0625` (fb-timeout
  only), `NEG=nolcrd2` (negative control).
- Timing gates: Gen1-64 pclk ≥ 125; Gen1-128 core ≥ 62.5; Gen2-128
  core ≥ 78.125 AND PHY pclk ≥ 156.25 AND rxclk ≥ 161.29 (the
  recovered clock truly runs 161.133 at 10G — §10u; the 6.2 ns SDC
  branch in gowin-serdes is the honest constraint).
- Saved images in `/tmp/kilo/`: `h0_gen1_fence.fs` (the fence),
  `s15_gen2_probe_66101_met.fs` (pre-#44 evidence build),
  `s15_gen2_cl_66125_met.fs` (closed-loop #45 evidence build).

## Constraints

- Single lane everywhere.  No Gen 1x2, no x2 negotiation work, ever.
- The `gw_usb3` 5G configuration and its regression suite are
  settled — PHY-side changes go behind elaboration knobs with the
  proven configuration still pinned by the suite; the 5G hub-port
  run (V4 run 2) is the hardware guard.
- The manufacturer's reference design and bitstream stay untouched;
  they are used only as a link-partner health baseline on our own
  board.
- BSD-3-Clause: upstream LUNA license and copyright headers stay
  intact; our commits carry our own attribution alongside.
- The shipping Gen1-64 configuration must remain buildable and
  ladder-green from every commit on main; `gen2=False`/64-bit
  elaborations of shared files stay bitstream-payload-identical
  unless a change is explicitly intended, battery-proven, and
  hardware-laddered.
- gowin-serdes is PUBLIC: keep it free of anything that is not ours
  to publish.
