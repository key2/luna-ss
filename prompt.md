# Mission: finish the dual-rate stack — Gen2 negotiation (G3),
# Gen2 framing through link+protocol (G4), and the Gen2 hardware
# ladder (G5). One bitstream, both rates.

Context, so there is no confusion about the nature of this work: this
is **building our own device stack** in our own fork. Everything here
is our code or BSD-3-Clause open source we forked with headers and
LICENSE intact (luna-ss), plus our gw_usb3 PHY and gowin-serdes GTR12
port as submodules, running on our own dev board on our own bench,
validated against the public USB 3.2 specification (markdown copy in
`doc/USB 3.2 Revision 1.1.pdf/markdown.md` — the conformance
reference; also `doc/643108_PIPE_Arch_Spec_Rev_7_1.pdf` and the USB
3.1 Link Layer Test Spec). The link partner is the standard Linux
xHCI host on the bench PC (usbmon, dmesg, our on-chip probes). The
vendor reference bitstream (`prj.fs`, in the frozen GW_USB3 archive)
is used only as an untouched black-box link-partner baseline on our
own board.

Read `HANDOVER.md` first — **§10o–§10q** (session 11, all in this
fork). §10q is freshest. Then `doc/gen2_design.md` — the reviewed
Phase-1 design note this mission executes; its framing delta table
and §9.1 pinned-contract facts are the Phase-4 blueprint.

## Where things stand (session-11 end — the starting position)

| asset | status |
|-------|--------|
| Phase 0 (the fork) | **G0 CLOSED**: one-clone flow verified; pytest 104/104; battery green; hardware ladder green from the fork build (284 MB/s aggregate, sha-exact, uart1 ch0=0) |
| Phase 1 (design note) | **G1 CLOSED**: `doc/gen2_design.md`, incl. staged width plan ((c)-then-(a)) and the two non-framing link deltas (modulo-16 sequence numbers, LCRD1/LCRD2 split) |
| Phase 2 (Gen2 sim) | **G2 red half CLOSED**: `sim/gen2_coding.py` oracle byte-exact vs the RTL (`gen2-oracle` GREEN); `sim/sim_link_gen2.py` end-to-end harness with the real RTL scrambler chain both directions; red baselines recorded |
| Phase 3 M1+M2 | **SIM-GREEN**: SCD1 declaration + Polling.LFPSPlus/SCD2 exchange (`gen2-scd` GREEN in the battery); `gen2=False` is the forced-Gen1 knob, and the shipping Gen1 bitstream is **bit-exact unchanged** (payload-identical rebuild proof) |
| Phase 3 M3–M5 | **NOT STARTED** — this mission's first work item |
| Phase 4, Phase 5 | NOT STARTED |
| battery | 38 entries: 35 Gen1 (regression fence) + `gen2-oracle` (green) + `gen2-scd` (green) + `gen2-train` (ENFORCED-RED, flips with Phase 4) |
| bench | board on **10G root port `usb 4-3`** (moved from 4-9; port re-verified Gen2-capable with the gold baseline); straight orientation = LN1 = correct; resident image = the shipping BURST=2 multiep build (POR 66_011, pclk 139.0), enumerated and ladder-green |
| gw_usb3 Gen2 datapath | silicon-proven at 10G (usb31-enum); PIPE contract beat-level facts pinned by the oracle (HANDOVER 10p, design note §9.1) |
| #38 | CLOSED (adapter lane/CSR mismatch; Q0_LN0 CSR path silicon-proven en route) |

## Deliverable

Complete the original dual-rate mission from where session 11 left
off:

1. **G3 — sim-green Gen2 negotiation**: LBPM PortMatch/PortConfig,
   LTSSM-driven rate switching, per-spec Gen1 fallback — all proven
   in `sim_link_gen2.py` phases (red-first per mechanism).
2. **G4 — full sim battery**: Gen2 block-level framing through
   `physical/` + `link/` per the design-note delta table;
   `gen2-train` flipped green; the enum + small bulk echo phases
   implemented and green; every Gen1 entry untouched.
3. **G5 — the numbers**: Gen2 clock MET (operating), enumeration as
   SuperSpeedPlus on the bench 10G root port (lsusb 10000M), the
   multiep ladder at Gen2 with recorded verdicts, and the fallback
   matrix (5G hub port + forced-Gen1 build + replug cycles) — same
   bitstream.

HANDOVER continues at **§10r**; bug numbering continues at **#39**.

## Phase plan (each phase gated; one mechanism per change, as always)

### Phase 3 remainder — negotiation (gate G3)

Mechanism by mechanism, sim red-first each time:

- **M3a — LBPM modem** (`physical/lfps.py` beside the SCD machinery):
  PWM TX shaping (tPWM 2–2.4 µs; '0' = 1/3 LFPS + 2/3 EI, '1' = 2/3 +
  1/3; delimiter = 1 tPWM LFPS + 1 tPWM EI; byte messages LSb first,
  delimiters at start/end/between) and an RX pulse-width classifier
  [6.9.5, Table 6-33]. Elaboration-gated like the SCD blocks.
- **M3b — Polling.PortMatch / Polling.PortConfig** (LTSSM, gen2-
  gated): PHY Capability LBPM ([1:0]=00, [3:2] rate: 00=5G/01=10G) —
  send ours (10G), match rule "4 matched sent after 2 matched
  received"; the lower-capability port's value wins; on re-entry
  advertise next-highest (the speed-fallback loop — Polling.Active/
  Configuration/Idle timeouts at Gen2 return to PortMatch, not
  Rx.Detect [7.5.4.5.2]). PortConfig: PHY reconfig window + PHY
  Ready LBPM handshake ([1:0]=01). Shared 12 ms
  tPollingLBPMLFPSTimeout across both substates; peripheral timeout
  → eSS.Disabled [7.5.4.5/.6]. Extend `PHASE=scd` into a full
  `PHASE=lbpm` (host answers SCD2 with capability LBPMs; require the
  device's matched capability + PHY Ready). Record the red first.
- **M3c — rate plumbing**: LTSSM `rate_select`/`rate_request` output
  driven by the PortMatch outcome; PIPE `rate` driven from it (the
  MAC owns `pipe.rate`); adapter side: `GowinGTR12PIPE` grows a
  rate-switch request/done handshake around its existing proven CSR
  sequencing (10G↔5G both directions — the boot path already does
  10G→5G; make it LTSSM-driven and repeatable mid-LTSSM, reusing the
  #22 boot-window discipline so no MAC state clocks through the
  retune). Sim: assert `pipe.rate` transitions per negotiated
  outcome (the serdes CSR side itself is hardware-proven; in sim,
  verify the handshake contract with a stub that acks like the
  adapter).
- **M3d — fallback matrix in sim**: (i) host never declares SCD →
  device completes legacy Gen1 handshake to Polling.RxEQ (assert the
  LFPS trace shows ≥4 SCD1 then non-varying tRepeat per 7.5.4.3
  rules — the current implementation keeps modulating; make the
  16-legacy-burst / 60 µs SCD-timeout rules real); (ii) SCD2 absent
  in LFPSPlus (20 non-varying / 64-burst rules [7.5.4.4]); (iii)
  Polling.Active timeout at Gen2 → PortMatch re-entry with
  next-highest capability → 5G outcome → Gen1 training completes
  (this closes the negotiation loop in sim); (iv) `gen2=False` knob:
  elaboration + the existing Gen1 battery is the proof.
- **Gate G3**: `gen2-lbpm` (or extended scd) green; fallback sims
  green; battery 100% with all Gen1 entries untouched; shipping
  bitstream parity re-proven (rebuild, payload compare — the
  established trick).

### Phase 4 — Gen2 framing through the stack (gate G4)

Execute the design-note delta table (§2) with the §9.1 pinned facts.
Suggested mechanism ladder, red-first each (extend `PHASE=train` /
`enum` / add `echo` as you go):

1. **Gen2 TX at the PIPE**: block-level ordered-set generator
   (TSEQ/TS1/TS2 16-symbol blocks, SYNC every 32 TS / every 16384
   TSEQ, DC-balance symbols 14/15 via gw_usb3 tables — or neutral
   first, receivers must ignore 14/15), driving
   `tx_data/tx_datavalid/tx_sync_header/tx_start_block` at Gen2;
   LTSSM RxEQ/Active/Configuration counts per spec (524,288 TSEQ —
   plumb a sim-shortening parameter like `tseq_burst_length`).
   This alone flips `gen2-train`'s first assertion.
2. **Gen2 RX OS detection**: block-level TS1/TS2 detectors
   (identifier symbols only, EXCLUDE symbols 14/15), SYNC/SDS
   detect; feed the existing LTSSM handshake counters.
3. **SDS + Idle + TX SKP scheduling**: SDS on Polling.Idle/
   Recovery.Idle entry; Idle Symbols in data blocks; SKP OS insert
   at block boundaries, average 1-per-40-blocks, Z=int(Y/40)
   [6.4.3.3] (the PHY freezes the LFSR across the SKP — send whole
   24-symbol OS blocks).
4. **Stage-A width bridge**: per-packet 64↔32 burst buffers between
   the 32-bit link core (running at pclk=156.25) and the Gen2
   framers (design note §1; DPPs wire-contiguous; single clock
   domain, width converters only).
5. **Gen2 packet/link-command framing**: Table 6-2 symbol framers/
   detectors (HPSTART/DPHSTART/DPPSTART/DPPEND/DPPABORT/LCSTART,
   ≤1-corrupt-symbol tolerance [7.3.3]); DPH length-field replica on
   non-deferred DPHs.
6. **Link-layer Gen2 mode**: modulo-16 header sequence numbers +
   4-bit LGOOD, LCRD1/LCRD2 credit classes (Type-2 = async DPs =
   all our bulk DPs; both pools advertised, both correct after
   recovery — the rule-2d/#29–#31 machinery gets a rate-selected
   modulus). This is the conformance-sensitive part: extend the
   Gen2 host model's credit/seq checking FIRST (red), then port.
   The 36 bugs' fixes carry over — width-adapt, don't rewrite.
7. **Enum surface**: bcdUSB 0310, BOS SuperSpeedPlus Device
   Capability (LSE=3/LSM=10, LP=1), Sublink Speed Device
   Notification TP on Address-state entry [8.5.6.7, 9.6.2.5].
   Complete the sim's `enum` + `echo` phases (GetDescriptor + small
   bulk echo through Gen2 framing, reusing the Gen1 host model's
   transaction logic above the encoding layer).
- **Gate G4**: full battery green with `gen2-train`, `gen2-enum`,
  `gen2-echo` flipped; Gen1 entries untouched; shipping parity
  re-proven. Port BurstEventCapture to Gen2 framing NOW (it is how
  #34 fell; calibrate on a quiet pipe before believing it).

### Phase 5 — hardware ladder (gate G5: the numbers)

1. Timing first: the **156.25 MHz domain must MEET operating
   timing** in the Gen2 build. Expect #22-class work on the known
   cones (endpoint-mux grants, tp_generator, get_descriptor ROMs);
   escalation: POR-nudge lottery (66_012+, document rolls), targeted
   register stages, the Yosys pre-lowering flow (archive §10k).
2. luna-enum-sized Gen2 enumeration top first; A/B against
   usb31-enum (our PHY + vendor link) and the archive `prj.fs` when
   stuck — both enumerate Gen2 on this board on port 4-3 (verified
   session 11). The hybrid rig lives in the archive.
3. lsusb 10000M; dmesg clean; then luna-multiep at Gen2: 1 MiB ×10 →
   16 → 64 MiB → ×10 soak, sha-exact, per-pipe MB/s recorded; wire
   checker ported to Gen2 framing (ch0 retry_flagged must read 0).
4. Fallback matrix: same bitstream on the 5G hub port (4-8.x) →
   Gen1 enumeration + ladder; forced-Gen1 (`gen2=False`) build;
   replug cycles. Do not regress the 5G trim (the gw_usb3
   equivalence suite + the hub-port run are the guards).
5. Stretch: beat Gen1's 284 MB/s aggregate meaningfully (~2×
   ceiling with the stage-A core; the stage-B 64-bit core is
   post-G5 work, ~1.1 GB/s runway).

## Parked items that stay on the books (do not lose them)

From §10n (all still open): **#37** (truncated inbound DPP never
retried — `FORCE_REC_AT=710` repro) + the forced-recovery sim-harness
feed-truncation WIP; rule-2d/#36 positive-validation stimuli; the
bench forced-recovery verdict for #29–#31 (uart1 `'R'` hook is in the
tree); data_tx SEND_ZLP bare-ready; wire-checker TP blindness. New
since: the SKP x=4 aligner fix behind an elaboration knob (design
note §6 — do it when `word_alignment` is open in Phase 4); the SCD
fallback rules of M3d partially cover the §10q note that the current
device keeps modulating SCD1 against legacy partners. Fix
opportunistically when the affected files are open — recovery
behavior matters MORE at Gen2 bring-up.

## Keep the discipline that closed thirty-eight bugs

- Simulate first; the sim keeps the REAL scrambler/coding chain at
  both rates (the RTL Scrambler/Descrambler instances stay in the
  gen2 bench loop; `gen2-oracle` pins the host model — keep it
  green when touching `gen2_coding.py`).
- One mechanism per change; full battery after each from a SETTLED
  tree (§10q lesson: never run the battery concurrently with source
  edits — entries elaborate the live tree). Gen1 entries are a
  regression fence, never a casualty; enforced-red entries flip to
  expect-green only as a conscious commit.
- Shipping parity after Gen1-shared-file changes: rebuild
  luna-multiep with defaults and payload-compare against the
  resident image (6 timestamp bytes are the only allowed delta).
- Hardware ladder with recorded verdicts before the next change;
  watch uart1 ch0 on every run.
- New bugs: **#39+**, findings into HANDOVER §10r as you go; commit
  submodules first, then the fork; push everything.

## Tooling and bench facts (verify before trusting)

- One clone: `git clone --recurse-submodules
  github.com/key2/luna-ss && pdm install -G :all`. Repos: luna-ss +
  gw_usb3 (private), gowin-serdes (public — no vendor artifacts
  there, ever); frozen archive = `~/Downloads/GW_USB3`
  (gw_usb3-archive on GitHub; ARCHIVE.md has the map).
- Board on the 10G root port **`usb 4-3`** (straight orientation =
  LN1; both orientations probed session 11 — flipped = Q0_LN0, CSR
  path works but stays a probe config). 5G test path = the hub at
  `4-8.x`. Flash: `sudo -n openFPGALoader -c ft232 <fs>`. After any
  replug the device needs a fresh POR (reflash or board KEY) — it
  parks in SS.Disabled 360 ms after boot. If a known-good image is
  dark: coordinate `usbX-portN/disable` warm-cycles with the flash,
  and A/B the archive `prj.fs` before blaming our stack (§10o).
- Rebuild: `pdm run python top.py` in `examples/gowin/<name>/`
  (8–20 min). Timing: `.venv/bin/python tools/gowin_timing_report.py
  <example>/build --section fmax`. Gen1 gate: pclk ≥ 125 operating
  (156.25 misses benign, #22; POR-nudge reroll knob at
  `luna-multiep/top.py` — 66_011 current, history in the comment).
  **Gen2 gate: 156.25 MET.**
- Verdicts: `multiep_test.py <MiB> --eps 1,2,3` (sudo; warmup
  default on); uart0 link probe / uart1 wire checker @115200 on
  `/dev/ttyUSB4`/`/dev/ttyUSB5`; `uart_capture.py <s> <prefix>`
  interleaves both. usbmon at `/sys/kernel/debug/usb/usbmon/4u`;
  `sudo -n dmesg` works.
- **Run sims as `.venv/bin/python -u`** (`timeout`+`pdm run`
  orphans children; unbuffered or you lose the evidence). Battery:
  `pdm run battery` (= `sim/sim_battery.sh`), logs in
  `/tmp/kilo/batt_*.log`. Gen2 sims take minutes (PHASE=scd ≈ 85k
  ss cycles) — budget for it.
- The gen2 bench PIPE bring-up dance is subtle and already solved —
  reuse `sim_link_gen2.bringup()` (TUSB phy_status dialect +
  power_down ack pulses; the LTSSM parks silently without them).
- Netlist-vs-RTL box for suspected GowinSynthesis miscompiles
  (archive §10k recipe; two confirmed classes have battery guards);
  fresh Yosys at `~/Downloads/yosys/build/yosys` is the validated
  escalation. StreamArbiter hardening idiom for any NEW arbitration
  cones — mandatory (miscompile history).

## Constraints

- gw_usb3's Gen1 5G TX path and its equivalence suite are settled —
  do not regress the 5G trim while adding LTSSM-driven rate
  switching; the 5G hub-port run in the fallback matrix is the
  guard. PHY-side changes (SKP x=4 fix, LTSSM_is_Training wiring)
  go behind elaboration knobs with the vendor-exact config still
  pinned by the equivalence tests.
- The vendor `prj.fs` and refdesign stay untouched restore baselines
  (in the archive).
- BSD-3-Clause: upstream LUNA license and copyright headers stay
  intact; our commits carry our own attribution alongside.
- The shipping Gen1 configuration must remain buildable and
  ladder-green from every commit on main; `gen2=False` elaborations
  of shared files must stay bitstream-payload-identical unless a
  Gen1-affecting change is explicitly intended, battery-proven, and
  hardware-laddered.
