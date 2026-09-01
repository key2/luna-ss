# Mission: the WIDTH PROGRAM — width-generic LUNA + wide PHY, on silicon

`doc/usb3_design.md` is the design authority for everything in this
mission (read it FIRST, in full — it merges and supersedes the old
gen2/gen1x2 notes and records the program decision).  Then read
HANDOVER **§10s** (session 13: G5 H0/H1 closed on hardware, H2 open,
bugs #39/#40, every operational pitfall you will hit again) and §10r.

The decision this mission executes:

* **LUNA goes width-generic**: `core_width ∈ {32, 64, 128}` chosen at
  core initiation.  The historical 32-bit core is NOT parameterized —
  it stays frozen as the Gen 1x1 shipping fence; the wide core is NEW
  RTL beside it.
* **The PHY (gw_usb3) grows a width-selectable PIPE `{64, 128}`**; the
  32-bit PIPE retires from the forward architecture (kept only for the
  frozen legacy build).  The PHY must present BOTH widths for Gen 1x1,
  Gen 1x2 and Gen 2x1; Gen 2x2 is 128-only by physics.
* Clocking per `usb3_design.md` §4.1: scaled pclk for the designed-for
  config, **duty-cycled full beats at the PHY clock as the mandatory
  fallback mode** (every capability falls back to Gen 1x1 — the wide
  core runs it duty-cycled, no mid-fallback pclk retune).

**You are free to modify ANYTHING the mission needs**: `luna/` (link,
protocol, physical, endpoints, streams), the `gw_usb3` submodule (PHY
datapath, PIPE surface, UPAR trim tables), the `gowin-serdes` submodule
(lane configs, fabric width/gear trims, SDC, platform), the examples,
the sims/battery, new tops, new modules, new battery axes.  Freedom is
bounded only by the standing fences below — not by module ownership.

## Where things stand (session-13 end)

| asset | status |
|-------|--------|
| G5 H0 (Gen1 fence) | CLOSED on hardware; bench RESTORED to it and re-verified (5000M, ladder green); image `/tmp/kilo/h0_gen1_fence.fs`, resident |
| G5 H1 (Gen2 156.25) | CLOSED: pclk 156.263 / rxclk 169.777 (`luna-enum-gen2`, POR 66_033 current) |
| G5 H2 (Gen2 enum) | **OPEN**: link trains at Gen 2x1 ("new SuperSpeed Plus Gen 2x1" in dmesg), U0 reached ~5×/boot, dies on the host's first control exchange; the header-event-capture build is coded but has NOT won the placement lottery (14 rolls, best 150.8) — never flashed |
| bugs | #39 (ltssm_training/polarity walk) + #40 (SKP inside packets) FIXED, silicon/sim verified; **#41 next**; #37 + §10n/§10q parked items carry |
| battery | 47/47 from a settled tree (runs 3–5); pytest = gw_usb3's 104 + gen2-pacing (fork-root `testpaths` only covers gw_usb3/tests — new fork tests need battery entries) |
| bench | board on 10G root port `usb 4-3` (straight = LN1); 5G hub at `4-8.x`; **the host is Gen 2x2-capable** (usb4 root hub: speed 20000, `rx_lanes = tx_lanes = 2`) — Gen 1x2 is negotiable and validatable on this bench |
| saved images | /tmp/kilo: `h0_gen1_fence.fs` (resident), `h1_gen2_enum_met.fs`, `h2_gen2_debug_met.fs`, `h2_gen2_skpfix_met.fs` (all timing-MET builds of their trees) |
| commits | everything pushed: fork `a9b5cff` (merged design doc), gowin-serdes `313033d` |

## Deliverables (gates W0–W3; HANDOVER continues at §10t, bugs at #41)

### W0 — bench probes + H2 disposition (do this first, it de-risks everything)

1. **Wide fabric trim experiments** (probe rigs, #38 pattern): does the
   GTR12 PCS support 8b10b at `width_mode 20 × gear 1:4` (5G → 8 sym @
   62.5) and raw `32 × 1:4` (10G → 128-bit @ 78.125)?  Record verdicts
   — the native-vs-bridge decisions in `usb3_design.md` §3.3 hang on
   them.  The trims are UPAR-reachable (`recfg_width_mode_1..4`); trim
   flips inherit the #22 boot-window discipline.
2. **LN0 TX bring-up** (the flipped-orientation pair as lane 1): #38
   proved LN0 CSR+RX; TX has never fired.  Probe rig + A/B vs LN1.
3. **Gen 1x2 PortMatch trace**: add `LBPM_CAP_GEN1X2 = 0x20` + the
   PortMatch arm, advertise it from a probe build, and capture whether
   the 20G root port answers with a dual-lane match.  This needs no
   datapath and answers "does this host really do x2" before P2.
4. **H2 disposition** (recommended, time-boxed): the remaining U0-death
   is BELOW the width layer — every finding carries 1:1 into the wide
   stack (`usb3_design.md` §10).  Either win the evcap lottery (scratch
   rolls in /tmp/kilo, 3 parallel) and read the first-64-header capture,
   or consciously park H2 with a HANDOVER note.  Suspect ranking is in
   §10s (LUP keepalive watchdog first — extend the strict host to
   REQUIRE LUPs at U0, red-first, before touching RTL).

### W1 — the width-generic core at 64-bit, proven at Gen 1x1 ON THE BENCH

* New wide core (`core_width` parameter, 64 first): stream contract
  per `usb3_design.md` §4.2 (`valid/len/first/offs`), RX barrel
  normalization (the proven gen2 bulk/boundary shape), padded TX,
  parallel CRC-16/32 with byte-enable tails, duty-cycle tolerance
  everywhere.  The SSP link mechanics (modulo-16, LCRD1/LCRD2) come
  along rate-selected.
* PHY: the 64-bit Gen 1 PIPE presentation (native 62.5 trim if W0
  proves it, else 125-duty) behind a width-normalization stage; the
  per-lane datapaths stay vendor-exact.
* Unit fences red-first: CRC equivalence vs the 32-bit reference
  (exhaustive lengths × offsets), barrel oracle, duty-cycle stress
  bench with randomized valid/ready (the #40 lesson: forgiving benches
  hide width bugs).
* **Gate W1**: wide-core Gen 1x1 sim battery green (new `w64` battery
  axis) AND the bench integration milestone — `luna-multiep`-class top
  on the wide stack at Gen 1x1, full ladder (enum 5000M, 1 MiB ×10 →
  16 → 64 MiB ×3, sha-exact, uart1 ch0=0), recorded verdicts.  The
  frozen 32-bit shipping build stays payload-identical throughout
  (rebuild-compare after every shared-file change; the "6 timestamp
  bytes" rule widens across date rollovers — check "all diffs below
  offset ~622").

### W2 — Gen 1x2 on the bench

* x2 PHY layer per `usb3_design.md` §3.2: striper/unstriper (byte
  interleave aligned to lane 0, control OS duplicated, simultaneous SKP
  + ≤8-idle padding), per-lane deskew (8-symbol, OS-boundary datum),
  lane-1 seed `8000h`, lane-0 crossbar (phase 1 pins straight
  orientation).  Strict 2-lane host model red-first for every rule.
* LTSSM x2 arms (24 ms Polling.Active, both-lanes exit, TS1-on-any-lane
  → Recovery-on-all), gen-x2-gated, x1 elaborations verbatim.
* Enumeration surface: SSP BOS + Sublink Speed Attributes with lane
  count, bcdUSB 0320, Sublink Speed Device Notification TP — build it
  parameterized once; it also closes the Gen 2 §10r-suspect-4 gap.
* **Gate W2**: `lsusb`/sysfs shows 10000 with `rx_lanes = tx_lanes = 2`
  on 4-3; full ladder at Gen 1x2 (target: meaningfully above the 284
  MB/s Gen 1x1 aggregate); fallback matrix (x2 on 4-3 ↔ x1 on the 5G
  hub port; replug/POR ×5) recorded.  Timing gate: pclk ≥ 125 MHz per
  table 1 of the design doc — no lottery is expected at this cell; if
  you find yourself grinding rolls, something is architecturally wrong,
  stop and re-read §7.

### W3 (stretch) — Gen 2x1 on the wide core

* Retire stage A: w64 @ 156.25 full-wire-rate first (the H2 findings
  carry), then the 128 @ 78.125 elaboration (bridge or native trim per
  W0) — the cell that ends the lottery era.  Gates: the H2/H3/H4
  ladders from the G5 checklist, on the wide core.

## Keep the discipline that closed forty bugs

* Sim first, STRICT models, red before green — every new wire rule gets
  a host-model check that fails against the old code (the #39/#40
  method).  Sim-reproduce every bench finding where feasible.
* One mechanism per change; full battery (47+ entries) from a SETTLED
  tree before each hardware build — never concurrent with source edits.
* Gen 1x1 shipping parity: payload-identical rebuild after EVERY change
  to a Gen1-shared file; the Gen 1 battery entries are the fence, never
  a casualty.  All wide/x2 changes in shared files are elaboration-
  gated; legacy elaborations verbatim.
* Timing gates are absolute: a build is never flashed for a config
  whose table-1 clock it misses.  Document POR-nudge rolls in the top
  comments; parallel scratch rolls in /tmp/kilo (copy the example dir,
  sed the POR value — and sed any relative imports to absolute paths).
* Hardware ladders with recorded verdicts before the next change; watch
  uart1 ch0 on every run; fresh POR after every replug (reflash or
  board KEY); vendor `prj.fs` is the port A/B baseline.
* Commit submodules FIRST (gowin-serdes is PUBLIC — no vendor
  artifacts, ever; gw_usb3 keeps its equivalence suite green with the
  vendor-exact trims pinned), then the fork; push everything; findings
  into HANDOVER §10t as you go.
* BSD-3-Clause: upstream LUNA headers stay intact; our commits carry
  our own attribution alongside.

## Tooling and bench facts (verify before trusting)

* One clone: `git clone --recurse-submodules github.com/key2/luna-ss
  && pdm install -G :all`.  Frozen archive = `~/Downloads/GW_USB3`
  (ARCHIVE.md; vendor `prj.fs` + hybrid A/B rig).
* Rebuild: `pdm run python top.py` in `examples/gowin/<name>/` (4–20
  min).  Timing: `.venv/bin/python tools/gowin_timing_report.py
  <example>/build --section fmax`.  Flash: `sudo -n openFPGALoader -c
  ft232 <fs>`.  Board KEY replays POR.
* **Run sims as `.venv/bin/python -u`** (`timeout`+`pdm run` orphans
  children).  Battery: `pdm run battery`, logs `/tmp/kilo/batt_*.log`.
  Fork-root pytest `testpaths` only covers `gw_usb3/tests` — new fork
  tests ride as battery entries (see `gen2-pacing`).
* Verdicts: `multiep_test.py <MiB> --eps 1,2,3` (sudo); uart0/uart1 @
  115200 on `/dev/ttyUSB4`/`/dev/ttyUSB5`; `uart_capture.py <s>
  <prefix>` interleaves both.  usbmon `/sys/kernel/debug/usb/usbmon/4u`;
  `sudo -n dmesg` works.  Probe decode ss-freq: 0x341554x ≈ 156.25,
  0x29aaa9x ≈ 125, and at new clocks recompute (delta × 24e6 / 2^23).
* Operational pitfalls (all burned in §10s): the background-process
  tool EATS `$vars` — literal commands only; `DomainRenamer({"cfg":
  "dbg"})`, never the string form, for the probes; Gowin TA hard-errors
  on `get_regs` patterns that match nothing; deterministic PnR — a
  winning scratch roll reproduces in-tree from the same sources+POR.
* Current tops: `luna-enum-gen2` (POR 66_033, timing-MET, evcap on
  uart1 pending lottery), `luna-multiep` (shipping, POR 66_011).
  x2/wide tops are new (`luna_multiep_w64`, `luna_enum_gen1x2`, … —
  add them to the gowin-serdes SDC branch or PnR falls back to the
  100 MHz default goal).

## Constraints

* The frozen 32-bit Gen 1x1 configuration must remain buildable and
  ladder-green from every commit on main — it retires only per
  `usb3_design.md` §12.6 (not this mission).
* gw_usb3's vendor-exact per-lane trims stay pinned by the equivalence
  suite; width/lane layers wrap them (new modules), they don't edit
  them — except behind elaboration knobs with the vendor-exact default
  pinned (the `skp_x4_fix` pattern).
* The vendor `prj.fs` and refdesign stay untouched restore baselines.
* gowin-serdes is PUBLIC: no vendor artifacts there, ever.
