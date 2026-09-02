# Mission: the WIDE CORE — Gen 1x1 + Gen 1x2 + Gen 2x1 at core_width 64 and 128, in LUNA, on silicon

`doc/usb3_design.md` is the design authority (§3.1/§3.3/§12 now carry
the session-14 P0 verdicts — read it FIRST, in full).  Then HANDOVER
**§10t** (session 14: gate W0 CLOSED, bug #41 fixed + wire-verified,
the #42 suspect, the port-4-3 finding) and §10s (the session-13
silicon lessons you will hit again: #39/#40, POR lottery, evcap,
operational pitfalls).

This mission builds what W0 de-risked: **the width-generic LUNA core
— NEW RTL beside the frozen 32-bit Gen 1x1 fence — at
`core_width ∈ {64, 128}`, carrying THREE advertised-highest
capabilities: Gen 1x1, Gen 1x2, Gen 2x1** (Gen 2x2 stays future
work; its 128-bit plumbing falls out of this mission by design).
Every (capability × width) cell of the §1 legality matrix that this
mission covers:

| Advertised highest | w64 | w128 |
|---|---|---|
| Gen 1x1 | designed-for @ 62.5 native (SILICON-PROVEN trim) or 125-duty | 31.25-bridged / 62.5-duty |
| Gen 1x2 | 125 (2×4 sym merged) — **no-lottery cell, proven closure class** | 62.5 (2×8 sym, the wide trim) |
| Gen 2x1 | 156.25 (lottery-class, proven once) | **78.125 via the 2:1 bridge — W0 verdict: native 128 does NOT exist; the bridge is final** |

Fallback rule (§4.1): every capability falls back to Gen 1x1 and the
wide core runs it DUTY-CYCLED at the PHY clock — full beats, `valid`
gaps / `ready` throttling, no partial beats, no mid-fallback pclk
retune.  Duty tolerance is not an option; it is the fallback mode.

**You are free to modify ANYTHING the mission needs** — `luna/`, the
`gw_usb3` and `gowin-serdes` submodules, examples, sims, battery,
new tops/modules/axes — bounded only by the standing fences below.

## Where things stand (session-14 end)

| asset | status |
|-------|--------|
| Gate W0 | **CLOSED** — all four probes verdicted; design doc updated |
| bug #41 | CLOSED: SSP LMP field rules (Tables 8-7/8-9/8-10), sim red/green (`gen2-u0`), wire-verified (evcap `D00000080`); the Gen1x1-fallback keeps historical fields via `ssp_operating` |
| Gen2 silicon (H2) | post-#41: trains → U0 → conformant Port Capability out → **zero host headers reach the protocol layer** → host `config error` → falls back → **ENUMERATES 5000M** (fallback ladder silicon-proven).  **#42 next**: inbound Gen2 header path; prime suspect = RxGearbox132/elastic/aligner realtime behavior the sim bypasses (bench feeds the Descrambler directly) |
| trim verdicts | 5G 20×1:4 (8 sym @ **62.5**) silicon-proven (pclk 0x14d555e; blob delta = 2 clock-divider regs); **width_mode >20 does not exist** on GW5AT-60 → Gen2×128 = 2:1 bridge, final |
| Gen 1x2 surface | `LBPM_CAP_GEN1X2 = 0x40` (spec-corrected: b6, NOT the mission-text 0x20), `ssp_capability=` / `phy_boots_gen2=` through ltssm/link/physical/device; sim `gen2-lbpm-x2` green (red recorded); probe `luna-enum-gen1x2` MET FIRST ROLL (pclk 126.2 @ the new 8.0 ns SDC branch) |
| **port 4-3** | announces **Gen 2x1-highest (0x04)** in LBPM — x2 NOT negotiable as benched; our adjust-down → Gen1x1 → 5000M is silicon-correct.  The gen1x2 probe = the x2-port qualifier tool (flash + read the uart1 LBPM ring on any candidate port) |
| LN0 (lane 1) | CSR/rate/eidle re-proven; TX serializer proof software-unreachable (PIPE loopback = slave semantics) — **folds into W2 x2 PortConfig** or a physical cable flip |
| battery / pytest | **49/49** (new: gen2-u0, gen2-lbpm-x2) / **104** — settled tree |
| bench | RESTORED to the Gen1 fence (POR 66_011), re-verified (5000M, 1 MiB ×3 258.8 agg, 16 MiB 278.2, sha exact); board on 4-3 straight (LN1 = lane 0) |
| saved images | /tmp/kilo: `h0_gen1_fence.fs` (RESIDENT), `h2_gen2_lmpfix_met.fs` (POR 66_047, MET, post-#41) + session-13 images |
| commits | all pushed: fork `948a33b`, gowin-serdes `19d676d`, gw_usb3 unchanged `1b54cf6` |

## Deliverables (gates W1–W3; HANDOVER continues at §10u, bugs at #42)

### W1 — the width-generic core at 64-bit, proven at Gen 1x1 ON THE BENCH

The keystone (§4.2/§11-P1): it proves PHY width normalization + the
wide core with ZERO new protocol variables, at forgiving clocks.

1. **Stream contract** (`core_width`-parametric, 64 first):
   `data W / ctrl W/8 / valid / len / first+offs` per §4.2.  RX
   normalizes EARLY — one barrel-rotate front-end per receiver class
   (the proven session-13 gen2 bulk/boundary engine shape); FSMs see
   aligned full-or-tail beats only.  TX pads to beat boundaries with
   logical idle between constructs; DPP bodies stream full beats.
   RX must nonetheless accept DENSE beats (real hosts pack
   `[LGOOD][LCRD][HPSTART dw0…]` in one wide beat).
2. **Width-generic link/protocol machinery** (§4.3 inventory): OS
   detect/emit position-muxed; header RX/TX with parallel CRC-16;
   data RX/TX with parallel CRC-32 + byte-enable tails (1..W/8);
   single-shot LC compare/emit (an LC fits one beat at ≥64) with
   multi-LC-per-beat RX; idle handshake N-byte windows; endpoint
   FIFO/mux widening (BSRAM aspect ratios support ×4).  The SSP link
   mechanics (modulo-16, LCRD1/LCRD2, DPH replica, tDPHResponse)
   come along RATE-SELECTED — Gen 1x2 uses them over the Gen 1
   dialect [§6].
3. **Unit fences red-first** (§9): CRC-16/32 equivalence vs the
   32-bit reference (EXHAUSTIVE lengths × offsets); barrel oracle
   (random construct streams at all offsets); duty-cycle stress with
   RANDOMIZED valid/ready (the #40 lesson: forgiving benches hide
   width bugs); dense-beat host injection.
4. **PHY: the 64-bit Gen 1 PIPE presentation.**  Primary: the
   SILICON-PROVEN native 62.5 trim (boot blob = 2-register delta,
   probe-trims has it; RX-side symbol delivery gets its verdict
   HERE) behind a width-normalization stage; keep a 125-duty
   elaboration as the fallback-mode vehicle (accumulate 2×32 → full
   beats with valid gaps) — you need duty tolerance proven anyway
   (§4.1).  Per-lane datapaths stay vendor-exact; the equivalence
   suite stays green with trims pinned.  New wide-trim boot needs
   the LN1 divider values (`0x808608`=0x121A, `0x808628`=0x126) and
   an SDC branch entry (16.0 ns) — PnR falls back to a 100 MHz
   default goal for unknown top names.
5. **Battery axis `w64`** (§9): full Gen1 phase suite at w64 —
   loopback configs, training, stale-ack, tx-fuzz class coverage —
   plus the new unit fences.  The 32-bit Gen 1 entries remain the
   untouchable regression fence.
6. **Gate W1**: w64 Gen 1x1 sim battery green (incl. duty stress)
   AND the bench milestone — a `luna-multiep`-class top on the wide
   stack at Gen 1x1, full ladder (enum 5000M, 1 MiB ×10 → 16 →
   64 MiB ×3, sha-exact, uart1 ch0=0), recorded verdicts.  Timing
   gate per table 1 (62.5 or 125 — Gen1-class closure, no lottery
   expected).  The frozen 32-bit shipping build stays
   payload-identical after EVERY shared-file change ("all diffs
   below offset ~622").

### W1×128 — the 128-bit elaboration at Gen 1x1 (sim gate)

The same core at `core_width=128`: barrel = 16-position byte rotate,
16-byte CRC tails, one-beat link commands and (at Gen 2 later) one
beat = one whole block payload.  Gate: the w64 suites re-run green at
w128 (`w128` smoke axis; full suites only where behavior differs),
CRC/barrel fences exhaustive at the new width.  Bench optional
(31.25/62.5 cells are trivial; silicon exposure can ride W3's bridge
work) — but the ELABORATION must build and meet timing if a top is
produced.

### W2 — Gen 1x2 (sim-complete; bench leg gated on port qualification)

* **x2 PHY layer** (§3.2, ours alone, oracle + strict fences only):
  striper/unstriper (byte interleave aligned to lane 0; packets/LCs
  may START on either lane; control OS duplicated, never striped;
  simultaneous SKP + ≤8-symbol idle padding for odd DP tails),
  per-lane 8-symbol deskew (acquire on simultaneous OS boundaries —
  TS/SKP datum at Gen 1, no SDS; maintain across SKPs; ≤6.4 ns
  budget), per-lane scrambler seeds (lane 0 `FFFFh` / lane 1
  `8000h`), per-lane polarity, lane-0 crossbar (phase 1 pins
  straight: lane 0 = LN1, lane 1 = LN0).  Per-lane elastic buffers
  do SKP removal BELOW the merge — the merged stream never carries
  SKPs.
* **LTSSM x2 arms** (gen-x2-gated, x1 elaborations verbatim): 24 ms
  Polling.Active; per-lane TS-detect with both-lanes exit (the early
  lane keeps transmitting TS); PortConfig applies to all lanes;
  TS1-on-ANY-lane in U0 → Recovery-on-ALL; PHY Ready x2 fields (we
  answer b6=0/b7=0 as UFP and MUST tolerate the DFP RT-Config b7=1
  phase: remain in PortConfig, keep LFPS EI, wait for b7=0, respond,
  then exit [7.5.4.6.1] — the session-14 probe skipped this arm,
  W2 builds it red-first).  Config-Lane discipline: LFPS/LBPM/
  rx-detect stay lane-0-only (the existing machinery IS lane 0).
* **SSP link mechanics at Gen 1x2** verified against §7.2.4.1.x
  (mod-16 + LCRD1/LCRD2 over Gen 1 framing); the `ssp_operating`
  qualifier for bug #41's LMP field rules gains its x2 arm (Gen 1x2
  is NOT Gen 1x1 operation — fields reserved-0).
* **Enumeration surface, parameterized once** (§8; closes the old
  §10r-suspect-4 gap for Gen 2 too): bcdUSB 0320, SSP BOS SuperSpeedPlus
  Device Capability with Sublink Speed Attributes covering every
  supported (rate × lanes), SS Endpoint Companion unchanged, Sublink
  Speed Device Notification TP on Address-state entry [8.5.6.7].
* **Strict 2-lane host model red-first for EVERY wire rule** (OS
  duplication, simultaneous SKP + padding, per-lane seeds, deskew
  injection, striping at either-lane packet starts, dense beats).
* **Gate W2 (sim)**: gen1x2 battery section green — train/enum/echo
  through the striped 2-lane coding chain at w64 (and the w128
  merge), fallback arms (x2→x1 ladder), the RT-Config arm, the
  notification TP.  **Gate W2 (bench)**: FIRST qualify a port — flash
  `luna-enum-gen1x2` (the qualifier) on every reachable physical
  port/orientation and read the uart1 LBPM ring; x2 needs a 0x44- or
  0x40-announcing DFP.  Port 4-3 as benched announces 0x04 — if NO
  qualifying port exists, W2 closes on sim + the strict host, the
  hardware verdict carries as a standing HANDOVER item, and the LN0
  TX proof stays with it (it rides x2 PortConfig).  If a port
  qualifies: `lsusb`/sysfs 10000 with `rx_lanes = tx_lanes = 2`,
  full ladder above the 284 MB/s Gen 1x1 aggregate, fallback matrix
  (x2 ↔ x1) ×5, LN0-TX proof recorded.  Timing gate: pclk ≥ 125 —
  no lottery is expected at this cell; grinding rolls here means
  something is architecturally wrong (re-read §7).

### W3 — Gen 2x1 on the wide core (retire stage A)

* **Stage 1: w64 @ 156.25 full wire rate** — the ~1.1 GB/s runway.
  The stage-A 64↔32 bridges and dual-chain muxing retire; H2's
  mechanisms (#39/#40/#41 fixes, TX pacing, seam registers, the v2
  RX engine shape) carry 1:1.  Re-pin `test_gen2_pacing` per width
  (the 32+1/33 ratio is width-invariant, thresholds scale).
* **#42 folds in here — sim-first, red-first**: before believing any
  wide-core Gen2 bench result, build the FULL-RX-CHAIN sim bench
  (RxGearbox132 + elastic/aligner + Descrambler in the loop — the
  equiv harness has the machinery; the current bench feeds the
  Descrambler directly, which is exactly where #42 hides) and
  reproduce the silicon signature: LC plane alive, ZERO host headers
  delivered.  Add LBAD/LRTY counter channels to the gen2 top (uart0
  ch4 is retaskable; netlist change = new lottery, POR history in
  the top comment, next free values 66_048+).
* **Stage 2: w128 @ 78.125 via the 2:1 PIPE bridge** (W0 verdict:
  no native trim exists — only the shallow bridge lives at 156.25).
  The cell that ends the lottery era; gates: the G5-checklist H2/H3/
  H4 ladders on the wide core (enum at 10000M `rx_lanes=1`, Gen2
  ladder targets, dual-rate fallback matrix ×5).

## Keep the discipline that closed forty-one bugs

* Sim first, STRICT models, red before green — every new wire rule
  gets a host-model check that fails against the old code (#39/#40/
  #41 all fell to this).  Sim-reproduce every bench finding where
  feasible.
* One mechanism per change; full battery (49+ entries) from a
  SETTLED tree before each hardware build — never concurrent with
  source edits.
* Gen 1x1 shipping parity: payload-identical rebuild after EVERY
  Gen1-shared-file change ("all diffs below offset ~622"); the Gen 1
  battery entries are the fence, never a casualty.  All wide/x2
  changes in shared files are elaboration-gated; legacy elaborations
  verbatim.  The wide core is NEW RTL — do not parameterize the
  frozen 32-bit core.
* Timing gates are absolute: a build is never flashed for a config
  whose table-1 clock it misses.  POR-nudge rolls documented in top
  comments; parallel scratch rolls in /tmp/kilo (copy the example
  dir, sed the POR value AND any relative imports to absolute
  paths); deterministic PnR — a winning roll reproduces in-tree.
* Hardware ladders with recorded verdicts before the next change;
  watch uart1 ch0 on every run; fresh POR after every replug
  (reflash or board KEY); vendor `prj.fs` is the port A/B baseline;
  RESTORE the fence image at session end and re-verify.
* Commit submodules FIRST (gowin-serdes is PUBLIC — no vendor
  artifacts, ever; gw_usb3 keeps its equivalence suite green with
  vendor-exact trims pinned — width/lane layers WRAP them, never
  edit them except behind elaboration knobs with the vendor-exact
  default pinned, the `skp_x4_fix` pattern; note: x2 makes re-timers
  first-class, so the SKP x=4 fix is scheduled WITH the x2 aligner
  work per §3.4), then the fork; push everything; findings into
  HANDOVER §10u as you go.
* BSD-3-Clause: upstream LUNA headers stay intact; our commits carry
  our own attribution alongside.

## Tooling and bench facts (verify before trusting)

* One clone: `git clone --recurse-submodules github.com/key2/luna-ss
  && pdm install -G :all`.  Frozen archive = `~/Downloads/GW_USB3`
  (ARCHIVE.md; vendor `prj.fs` + hybrid A/B rig).
* Rebuild: `pdm run python top.py` in `examples/gowin/<name>/`
  (4–20 min).  Timing: `.venv/bin/python tools/gowin_timing_report.py
  <example>/build --section fmax`.  Flash: `sudo -n openFPGALoader -c
  ft232 <fs>`.  Board KEY replays POR.
* **Run sims as `.venv/bin/python -u`** (`timeout`+`pdm run` orphans
  children).  Battery: `pdm run battery`, logs `/tmp/kilo/batt_*.log`;
  49 PASS lines expected today.  Fork-root pytest `testpaths` only
  covers `gw_usb3/tests` — new fork tests ride as battery entries
  (`gen2-pacing` pattern).
* Verdicts: `multiep_test.py <MiB> --eps 1,2,3` (sudo); uart0/uart1 @
  115200 on `/dev/ttyUSB4`/`/dev/ttyUSB5`; `uart_capture.py <s>
  <prefix>` interleaves both.  usbmon `/sys/kernel/debug/usb/usbmon/4u`;
  `sudo -n dmesg` works.  Probe ss-freq telltales (delta × 24e6 /
  2^23): 0x341554x ≈ 156.25, 0x29aaa9x ≈ 125, **0x14d555x ≈ 62.5**;
  recompute at new clocks.
* Operational pitfalls (burned in §10s/§10t): the background-process
  tool EATS `$vars` — literal commands only; `DomainRenamer({"cfg":
  "dbg"})`, never the string form; Gowin TA hard-errors on `get_regs`
  patterns that match nothing; the "upar" clock domain is created BY
  GowinSerDes (reference it, don't recreate it); PIPE
  `TxDetectRx_loopback` is the loopback-SLAVE semantic (no TX→RX
  self-test path — don't rediscover W0.2); with the straight cable,
  LN1's RX pads carry HOST traffic (host polling TS1s are comma-rich
  — don't mistake them for loopback return).
* Current tops + POR values: `luna-multiep` (shipping fence, POR
  66_011), `luna-enum-gen2` (POR 66_047, MET, post-#41),
  `luna-enum-gen1x2` (x2-port qualifier, POR 66_011-class, MET),
  `probe-trims` (TRIM= knob), `probe-ln0tx` (LANE=/LOOPBACK=).  New
  wide tops (`luna_multiep_w64`, `luna_multiep_gen1x2`, …) MUST be
  added to the gowin-serdes SDC branches (6.4 ns gen2 / 8.0 ns
  gen1x2 / new 16.0 ns for the 62.5 trim) or PnR falls back to the
  100 MHz default goal.
* Sim knobs: `PHASE=` (scd|lbpm|lbpm5g|lbpm-x2|fb-*|train|enum|echo|
  u0), `TSEQ_LEN`, `TSCALE`, `NEG=nolcrd2`, `DEVCAP=gen1x2`.

## Constraints

* The frozen 32-bit Gen 1x1 configuration must remain buildable and
  ladder-green from every commit on main — it retires only per
  `usb3_design.md` §12.6 (not this mission; the wide core's Gen 1x1
  ladder must first accumulate shipped-parity soak history).
* gw_usb3's vendor-exact per-lane trims stay pinned by the
  equivalence suite; width/lane layers wrap them (new modules).
* The vendor `prj.fs` and refdesign stay untouched restore baselines.
* gowin-serdes is PUBLIC: no vendor artifacts there, ever.
* Spec references: USB 3.2 R1.1 markdown in `doc/`; Table 7-13 is
  the LBPM authority (dual-lane = b6 = 0x40 — the 0x20 in older
  notes was a transcription error, already corrected everywhere).
