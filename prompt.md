# Mission: fork LUNA into a first-class dual-rate (Gen1 5G + Gen2 10G)
# SuperSpeed stack — our PHY and serdes as native submodules, and
# Gen2 through the WHOLE stack, not just the PHY

Context, so there is no confusion about the nature of this work: this
is **building our own device stack**. Everything here is our code or
BSD-3-Clause open source we are entitled to fork and modify — the
LUNA USB3 gateware (BSD-3-Clause; keep upstream copyright headers and
LICENSE intact in the fork), our gw_usb3 PHY, our gowin-serdes GTR12
port, running on our own dev board on our own bench, validated
against the public USB 3.2 specification (markdown copy in
`doc/USB 3.2 Revision 1.1.pdf/markdown.md` — the conformance
reference; also `doc/643108_PIPE_Arch_Spec_Rev_7_1.pdf` and the USB
3.1 Link Layer Test Spec). The link partner is the standard Linux
xHCI host on the bench PC, observed through standard kernel
interfaces (usbmon, dmesg) and our own on-chip probes. Nothing here
analyzes, unpacks, or circumvents anyone else's product; the vendor
reference bitstream (`prj.fs`) is used only as an untouched black-box
link partner baseline on our own board.

Read `HANDOVER.md` first — **§10g–§10n** (sessions 4–10). §10n is the
freshest: ten sessions found and fixed thirty-six numbered stack bugs
(#37 open, see "parked items"); session 10 closed the burst hardware
bring-up (#34/#35) and **BURST=2 is the shipping Gen1 default at
283 MB/s aggregate across 3 full-duplex bulk pairs**, sha-exact under
soak, retry_flagged=0. The upstream-patch era ends with this mission:
we now fork.

## Where things stand (session-10 end — the starting position)

| asset | status |
|-------|--------|
| LUNA Gen1 stack (our 30+ fixes) on gw_usb3 + gowin-serdes | **hardware-proven**: enumerates, 3 bulk pairs, BURST=2, 94 MB/s/direction/pipe, ×10 64 MiB soak, wire clean |
| gw_usb3 PHY **Gen2 (10G) datapath** (128b/132b: `datapath.py` RxGearbox132/TxGearbox132, Gen2 scrambler, `dc_balance.py`, `tables.py`; `gen2=True` knob, ~3.2k LUTs) | **silicon-proven**: `usb31-enum` (our PHY + our serdes + vendor link/LTSSM netlist) **enumerates at Gen2 on the bench 10G root port** (§10c/§10d table) |
| vendor original example (`prj.fs`) | enumerates Gen2 AND Gen1 — untouched gold-reference link partner baseline on this exact board |
| hybrid A/B rig (`Gowin_USB3.1_UVC_BULK_RefDesign/hybrid/`) | proven bisect methodology: vendor project with single blocks swapped for ours (§10c) |
| gowin-serdes | 10G boot trim + CSR rate reconfiguration 10G→5G on every Gen1 link-up (both examples); GTR12 raw 64-bit fabric interface at 10G, 40-bit/8b10b at 5G |
| PIPE surface | gw_usb3 `phy.py` already exposes a **64-bit PIPE** (`PipeTxData/PipeRxData In/Out(64)`); LUNA rides it today through the Gen1 32-bit adapter (`luna/gateware/interface/serdes_phy/gowin_gtr12.py`) |
| regression | pytest 104/104; sim battery 35/35 (recovery, burst, blast, tx-fuzz); all in-repo |
| LUNA link/protocol/LTSSM | **Gen1-only**: 32-bit @ 125 MHz, 8b/10b K-symbol framing, no LBPM, no 128b/132b, no rate switch |

**What this means**: the physical layer for Gen2 exists and works on
this silicon. The mission is (a) the repo restructure the team wants,
and (b) teaching the LUNA-side stack — LTSSM, physical-layer framing,
link layer, datapath width — to negotiate and run Gen2, falling back
to Gen1 per spec. One bitstream, both rates.

## Deliverable

A LUNA fork (suggested name: `luna-ss`, our repo, real commits — the
`patches/luna_gowin_adapter.patch` era ends) that:

1. contains `gw_usb3/` and `gowin-serdes/` as **git submodules**,
   with the GTR12/PIPE adapter code native to the fork;
2. builds the existing Gen1 examples unchanged in behavior
   (**Gen1 parity gate**: battery green + the standard multiep
   hardware ladder green from the NEW layout before any Gen2 work);
3. negotiates Gen2 per spec (SCD1/SCD2 in Polling.LFPS, LBPM in
   Polling.LFPSPlus → PortMatch → PortConfig — grep the spec markdown
   for `SCD1`, `LBPM`, `Polling.LFPSPlus`; 141 hits to work from),
   trains at 10G with 128b/132b, enumerates as a SuperSpeedPlus
   device, and runs the multiep bulk ladder at Gen2;
4. falls back to Gen1 cleanly (5G hub port test — the §10d matrix —
   and a forced-Gen1 build knob) — same bitstream.

`prompt.md` and `HANDOVER.md` move into the fork; HANDOVER continues
at **§10o**; bug numbering continues at **#38**.

## Phase plan (each phase gated; one mechanism per change, as always)

### Phase 0 — the fork and restructure (gate G0: Gen1 parity)

- Split `gw_usb3/` out of the GW_USB3 workspace into its own repo
  with history (`git filter-repo`/subtree split). gowin-serdes is
  already standalone.
- Create the fork from upstream `82a8f733`; land our delta as a
  reviewable commit series (the class structure in
  `patches/README.md` / `upstream_drafts/` is the natural grouping:
  adapter, one-liners, handshake robustness, TX-path integrity,
  recovery conformance, burst engines, session-10 recovery
  groundwork). Byte-identical tree at the end — verify with
  `diff -r` against the current `luna/` checkout.
- Add submodules; move the bench/test collateral so that ONE clone +
  `git submodule update --init` + `pdm install` gives: pytest, the
  full `sim_battery.sh`, and every example build. Examples may stay
  in gowin-serdes or move into the fork's `examples/` — your call;
  the hard requirement is no `sys.path` archaeology and no dead
  paths.
- Keep the old GW_USB3 workspace as a frozen bench archive (vendor
  refdesign, gowin_bug_report*, doc/ can move or stay — document
  where).
- **Gate G0**: battery 35/35 + pytest from the fork layout; rebuild
  luna-multiep from the fork; flash; standard ladder (1 MiB ×10,
  64 MiB ×3, uart1 ch0=0). Also re-run the §10n-tail ladder note:
  the resident image predates the rule-2d/#36/hook changes, so this
  rebuild is ALSO their first hardware exposure.

### Phase 1 — design note before code (gate G1: written + reviewed)

Read, then write `doc/gen2_design.md` in the fork covering, minimum:

- **Datapath width/clock plan.** Gen2 payload is ~9.7 Gbps; 32-bit
  needs ~312 MHz — not happening in this fabric. The serdes gives
  64-bit @ 156.25 MHz at 10G, and gw_usb3's PIPE is already 64-bit.
  Decide: (a) width-generic link+protocol layers elaborated 32-bit@125
  for Gen1 and 64-bit@156.25 for Gen2 (the honest target: header = 2
  beats, full line rate); or first stage (c): keep the 32-bit link
  layer at 156.25 behind per-packet 64↔32 burst buffers (DPPs must be
  wire-contiguous, so buffer whole packets and burst them; sustained
  throughput ~halves but protocol correctness and enumeration are
  fully exercisable). (c)-then-(a) is a legitimate de-risking ladder;
  choose deliberately and write down why.
- **Framing delta table, from the spec markdown**: Gen2 has no
  K-symbol framing — packet/link-command delimiters, TS1/TS2/TSEQ as
  16-symbol blocks, SDS, SYNC, Gen2 SKP OS format+cadence, Gen2
  scrambler, block header bits. Map each Gen1 construct in
  `physical/` + `link/` (HPSTART/SDP/END/EPF detection, CTC skip
  inserter, scrambler, alignment) to its Gen2 replacement, and mark
  which gw_usb3 blocks already implement the Gen2 side (most of the
  bit-level work: gearboxes, scrambler, DC balance are DONE and
  proven — reuse, don't rewrite).
- **LTSSM delta**: Polling substates for LBPM, rate selection,
  Recovery at Gen2, and where the serdes CSR rate switch (existing
  10G→5G machinery in the examples — make it LTSSM-driven, both
  directions) hooks in. Note gw_usb3 already does SCD/rate-change
  even with `gen2=False` (§10a) — mine that logic.
- **Timing budget**: at Gen2 the 156.25 MHz constraint becomes an
  OPERATING requirement, not the benign-miss boot window of #22.
  Current full multiep builds land 139–149; luna-enum-sized builds
  have hit 156.3. Expect #22-class pipelining work on the hot cones;
  escalation paths: placement lottery (POR nudge), targeted register
  stages, the Yosys pre-lowering flow (§10k addendum). Budget for it.
- **Vendor aligner SKP bug** (§10c): the vendor Gen2 block aligner
  mis-tracks SKP OS with x=4 symbols — our RX path must handle what
  the HOST sends legally, and our TX must not tickle host-side
  quirks; note the workaround plan.

### Phase 2 — sim first: a Gen2 link partner (gate G2: red/green pair)

Extend the link-partner simulation before touching device RTL:

- Either extend `sim_link_loopback.py` with a `GEN=2` mode or write
  `sim_link_gen2.py` reusing its host-model logic (frames, credits,
  handshake/burst/9249 models are rate-agnostic at the header level —
  the encoding layer below them changes). It must speak: LBPM
  negotiation, 128b/132b blocks with the REAL Gen2 scrambler (the
  Gen1 sim's whole value came from the real scrambler chain — same
  rule here), SDS, Gen2 SKP, Gen2 packet framing.
- Reuse gw_usb3's own Python models (`sim_model=True` paths,
  equivalence-suite vectors) as the encoding oracle where possible.
- The battery grows a `gen2` section; every existing Gen1 entry must
  stay green untouched throughout the mission.
- **Gate G2**: a Gen2 training + enumeration + small bulk echo sim
  that FAILS against the unmodified stack and PASSES once each
  device phase lands (keep the red run recorded in HANDOVER).

### Phase 3 — LTSSM + rate switch (gate G3: sim-green negotiation)

LBPM/SCD in the fork's LTSSM; serdes rate reconfiguration driven by
the LTSSM (10G↔5G, both directions, mid-LTSSM); PIPE rate/width mux;
Gen1 fallback when the host never answers SCD2/LFPSPlus. The §10d
test matrix (10G root port / 5G hub port) is the eventual hardware
acceptance shape.

### Phase 4 — Gen2 physical + link framing (gate G4: full sim battery)

Wrap gw_usb3's proven Gen2 datapath as the fork's Gen2 PIPE backend;
implement block-level ordered-set detect/generate, SDS, SKP, and the
Gen2 packet/link-command framers in `physical/` + `link/` per the
Phase-1 delta table; datapath width per the Phase-1 decision. Header
packet content, CRCs, LGOOD/LCRD machinery, protocol layer, and the
burst engines should be untouched or width-adapted only — all thirty
-six bugs' worth of fixes carry over by construction.

### Phase 5 — hardware ladder (gate G5: the numbers)

Climb exactly like Gen1 did, with recorded verdicts:

1. Timing gate first: Gen2 clock MET (operating, not boot-window).
2. `usb31-enum`-style enumeration top from the fork at Gen2 —
   A/B against `usb31-enum` (our PHY + vendor link) and `prj.fs`
   when stuck: the hybrid-rig methodology (§10c) is the proven
   debug path, and BOTH already enumerate Gen2 on this board.
3. lsusb shows 10000M; dmesg clean; then luna-multiep at Gen2:
   1 MiB ×10 → 16 → 64 MiB → ×10 soak, sha-exact, per-pipe MB/s
   recorded. Wire checker ported to Gen2 framing (ch0 retry_flagged
   discipline carries over — it must read 0).
4. Fallback matrix: same bitstream on the 5G hub port → Gen1
   enumeration + ladder; forced-Gen1 knob build; replug cycles.
5. Stretch: beat Gen1's 283 MB/s aggregate meaningfully (the Gen2
   ceiling is ~2× even with the staged 32-bit core; ~1.1 GB/s runway
   with the full 64-bit datapath).

## Parked items that stay on the books (do not lose them)

From §10n: **#37** (truncated inbound DPP never retried —
`FORCE_REC_AT=710` repro) and the forced-recovery sim-harness feed
truncation WIP; rule-2d/#36 positive-validation stimuli; the bench
forced-recovery verdict for #29–#31 (uart1 `'R'` hook is already in
the tree); data_tx SEND_ZLP bare-ready; wire-checker TP blindness.
Fix them opportunistically when the affected files are open anyway —
recovery behavior matters MORE at Gen2 bring-up, where marginal links
are likelier. `upstream_drafts/` classes 1–2 remain valid against the
pre-fork base if the team ever wants to send them.

## Keep the discipline that closed thirty-six bugs

- Simulate first; the sim keeps the REAL scrambler/coding chain at
  both rates. One mechanism per change; full battery after each
  (Gen1 entries are a regression fence, never a casualty).
- Hardware ladder with recorded verdicts before the next change;
  watch uart1 ch0 on every run.
- New bugs: **#38+**, findings into HANDOVER §10o as you go; commit
  submodules first, then the fork; push everything.
- The shipping Gen1 configuration must remain buildable and
  ladder-green from every commit on the fork's main branch.

## Tooling and bench facts (verify before trusting)

- Board on the 10G root port (`usb 4-9`); 5G test path = the 5000M
  hub port (§10d). Flash: `sudo -n openFPGALoader -c ft232 <fs>`.
  Rebuild: `pdm run python top.py` (8–20 min). Timing report:
  `python3 gowin_timing_report.py <example>/build --section fmax`.
  Gen1 gate: pclk ≥ 125 operating (156.25 misses benign, #22).
  **Gen2 gate: the 156.25 domain must MEET timing.**
- Verdicts: `multiep_test.py <MiB> --eps 1,2,3` (warmup default on,
  `--no-warmup` for probes); loopback window/bandwidth tests; ACM
  echo (`luna-acm/acm_echo_test.py`). usbmon at
  `/sys/kernel/debug/usb/usbmon/4u`; `sudo -n dmesg` works.
- Debug UARTs @115200: uart0 link probe (or ACKPROBE field capture),
  uart1 wire checker + `'R'` force-recovery command;
  `luna-multiep/uart_capture.py <s> <prefix>` interleaves both.
- **Run sims as `.venv/bin/python -u`** — `timeout`+`pdm run`
  orphans children, and piped python without `-u` buffers away your
  evidence (two sessions' phantoms, §10m/§10n).
- Netlist-vs-RTL box for suspected GowinSynthesis miscompiles
  (recipe §10k; two confirmed classes have guards in the battery);
  fresh Yosys at `~/Downloads/yosys/build/yosys` is the validated
  escalation. StreamArbiter-style hardening idiom for any new
  arbitration cones (§10n).
- BurstEventCapture (`MULTIEP_ACKPROBE=1`) is the field-level probe
  pattern — port it to Gen2 framing early; it is how #34 fell.
  Calibrate any new probe on a quiet virgin pipe before believing it
  (§10n's blind-window lesson).

## Constraints

- gw_usb3's Gen1 5G TX path history (§10d) and its equivalence suite
  are settled — do not regress the 5G trim while adding LTSSM-driven
  rate switching; the 5G hub port run in the fallback matrix is the
  guard.
- The vendor `prj.fs` and refdesign stay untouched restore baselines.
- BSD-3-Clause: keep LUNA's license and copyright headers in the
  fork; our commits carry our own attribution alongside.
