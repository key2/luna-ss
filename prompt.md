# Mission: gate G5 — prove the dual-rate stack ON HARDWARE.
# One bitstream: Gen2 (10G) enumeration + ladder on the 10G root
# port, Gen1 (5G) enumeration + ladder via per-spec fallback on the
# 5G hub port, and the shipping Gen1 build still green. Debug on
# the bench until BOTH rates demonstrably work.

Context, so there is no confusion about the nature of this work: this
is **validating our own device stack** in our own fork. Everything
here is our code or BSD-3-Clause open source we forked with headers
and LICENSE intact (luna-ss), plus our gw_usb3 PHY and gowin-serdes
GTR12 port as submodules, running on our own dev board on our own
bench, validated against the public USB 3.2 specification (markdown
copy in `doc/USB 3.2 Revision 1.1.pdf/markdown.md`; also
`doc/643108_PIPE_Arch_Spec_Rev_7_1.pdf` and the USB 3.1 Link Layer
Test Spec). The link partner is the standard Linux xHCI host on the
bench PC (usbmon, dmesg, our on-chip probes). The vendor reference
bitstream (`prj.fs`, in the frozen GW_USB3 archive) is used only as
an untouched black-box link-partner baseline on our own board.

Read `HANDOVER.md` first — **§10r** (session 12) is the whole story:
gates G3 and G4 closed on sim, the G5 checklist, the timing
diagnosis, and the regression state. §10o has the fork map and bench
history. Then `doc/gen2_design.md` §5 (timing budget) and the
`physical/gen2.py` module docstring (the stage-A architecture and
the RX grammar engine you will be pipelining).

## Where things stand (session-12 end — the starting position)

| asset | status |
|-------|--------|
| G0–G2 | CLOSED (fork parity, design note, Gen2 sim + oracle) |
| **G3 (negotiation)** | **CLOSED on sim** (`bb4bf07`): LBPM PortMatch/PortConfig, LTSSM-driven rate handshake, full SS-fallback matrix — `gen2-lbpm`/`lbpm5g`/`fb-legacy`/`fb-noscd2`/`fb-timeout` green |
| **G4 (framing)** | **CLOSED on sim** (`5514c5c`): `physical/gen2.py` stage-A block machinery + 32↔64 bridges; modulo-16 + LCRD1/LCRD2 (runtime rate-selected); `gen2-train`/`enum`/`echo` green end-to-end through the RTL scrambler chain; `NEG=nolcrd2` negative control fenced |
| battery | **46/46** from a settled tree (35 Gen1-era entries = the regression fence, 11 gen2); pytest 104/104 |
| shipping parity | proven twice in session 12: luna-multiep rebuild payload-identical to the resident POR-66_011 image (4 timestamp bytes) |
| G5 groundwork | `examples/gowin/luna-enum-gen2` (first `gen2=True` top) + `GowinGTR12PIPE(gen2=True)` (rate forward + synthesized ~7 ms rate ack + `ltssm_training`) — **built once, NEVER flashed** (`cfeb27c`) |
| **G5 timing** | **NOT MET**: pclk Fmax 71.7 @ 22 levels — cone = `gen2_rx` grammar-engine slot chain → collector/out_fifo (elastic, safe to pipeline); `serdes_pcs_rx_clk_i` 114.9 @ 16 levels also short; debug ClockFreqProbes disabled (their snap/delta arithmetic was the roll-1 false cone — they need a pipelined delta before riding at 156.25) |
| bench | board on 10G root port **`usb 4-3`** (straight = LN1); 5G path = hub at `4-8.x`; **resident image = the Gen1 shipping build** (POR 66_011, pclk 139.0) — untouched all of session 12, last verified ladder-green session 11c |
| bugs | #38 closed; **#39 next**; #37 + §10n/§10q parked items carry |

## Deliverable — GEN1 AND GEN2 both proven on hardware

1. **Gen1 fence first**: the current tree's Gen1 shipping build
   re-verified on the bench (enumeration 5000M + the full multiep
   ladder, sha-exact, uart1 ch0=0) BEFORE any Gen2 flash.
2. **Gen2 clock MET**: pclk AND the PHY rx domain ≥ 156.25 operating
   in the Gen2 build; no Gen2 image is ever flashed before this.
3. **Gen2 enumeration**: `lsusb` shows **10000M** (SuperSpeedPlus
   Gen 2x1) on port 4-3, dmesg clean, from `luna-enum-gen2`. Debug
   on the bench — probes, usbmon, A/B rigs — until it does.
4. **Gen2 ladder**: luna-multiep at Gen2 — 1 MiB ×10 → 16 → 64 MiB →
   ×10 soak, sha-exact, per-pipe MB/s recorded, wire checker ported
   to Gen2 framing reading ch0 retry_flagged=0.
5. **The dual-rate matrix, same bitstream**: the Gen2 image on the
   5G hub port must fall back per spec and run the GEN1 ladder;
   replug/POR cycles on both ports; the forced-Gen1 (`gen2=False`)
   build re-laddered. A recorded verdict table is the gate.

HANDOVER continues at **§10s**; bug numbering continues at **#39**.

## Phase plan (each phase gated; one mechanism per change, as always)

### Phase H0 — Gen1 fence (half a day, do it before touching anything)

Rebuild luna-multiep from the tree (defaults), payload-compare
against the resident image (the established trick — 6 timestamp
bytes max), flash, fresh POR, and run the full ladder: enumeration
on 4-3 (5000M, flags d), `multiep_test.py 1 --eps 1,2,3` ×10, 16 MiB
×3, 64 MiB ×3, sha-exact, uart1 ch0 retry_flagged=0
(`uart_capture.py` interleaves both uarts). Record the verdicts.
This is half of the mission statement ("GEN1 works") and the
restore point for everything after. Save the .fs to /tmp/kilo.

### Phase H1 — 156.25 MET (the Gen2 flash gate)

Sim red/green discipline continues: every RTL change re-runs
`gen2-train`/`gen2-enum`/`gen2-echo` (and the full battery from a
settled tree before each hardware build).

- **M1 — pipeline the `gen2_rx` engine** (the 71.7 MHz / 22-level
  cone, `physical/gen2.py`): register the per-slot emissions ahead
  of the output collector (the whole path is elastic — out_fifo
  absorbs a cycle; NOTHING in the engine is cycle-exact-load-bearing)
  or split the 4-slot chain 2+2 with a pipe stage. Watch the chained
  state regs (`fr_kind` fanout was the reported source). Re-run the
  gen2 sims; they must stay green untouched.
- **M2 — ClockFreqProbe pipelined delta** (`gowin-serdes` submodule,
  PUBLIC repo — commit there first, then bump the fork): the
  snap/delta subtractors must close at 156.25 so the bench probes
  can ride in Gen2 builds. Re-enable the probes in `luna-enum-gen2`
  (they are the primary debug tool of Phase H2 — do not go to the
  bench blind).
- **M3 — the PHY rx-domain cone** (114.9 @ 16 levels,
  `serdes_pcs_rx_clk_i`): the vendor closes this domain on the same
  silicon (usb31-enum enumerates Gen2), so expect
  constraints/placement first: add proper 156.25 clock constraints
  for the pclk/rxclk domains (they currently inherit the 100 MHz
  serdes-attach bases), then the lottery. If it is a real cone in
  our ported datapath, fix behind the equivalence suite (vendor-
  exact trim stays pinned).
- Escalation ladder (in order, all documented in the archive §10k):
  POR-nudge lottery (66_012+, document rolls in the top comment),
  targeted register stages on reported cones, the Yosys
  pre-lowering flow (`~/Downloads/yosys/build/yosys`).
  StreamArbiter hardening idiom is MANDATORY for any new
  arbitration cones (GowinSynthesis miscompile history).
- **Gate: pclk AND rxclk Fmax ≥ 156.25 operating**
  (`.venv/bin/python tools/gowin_timing_report.py
  examples/gowin/luna-enum-gen2/build --section fmax`). A build that
  misses is not flashed for Gen2 runs, period.

### Phase H2 — Gen2 enumeration on the bench (expect debug; budget for it)

This is the first silicon exposure of: LBPM on real LFPS hardware,
the block TX/RX bridges against the real gearboxes, the synthesized
rate-ack envelope, and the `LTSSM_is_Training` approximation. The
§10r known-suspect list, in expected-failure order:

1. **TX beat pacing**: the PHY's Gen2 TX path has a 32-deep FIFO
   (`TxFifoWrNum` exposed on `Usb31Phy`) drained at the 128/132
   gearbox rate; our block transmitter currently streams
   tx_datavalid every beat → overflow after ~32 sustained beats.
   Wire a probe channel on TxFifoWrNum FIRST; if it saturates,
   implement pacing (1-gap-in-33 beats at block boundaries, or a
   TxFifoWrNum threshold throttle in the adapter). Add the sim
   equivalent (a ready-modeled bench scrambler or a pacing assert)
   so the mechanism is red/green tested before the flash.
2. **`LTSSM_is_Training`**: currently approximated as
   terminations-engaged-and-not-trained in the top. The PHY's Gen2
   descrambler acquisition consumes it — if RX never locks (uart
   probes: no TS detects at 156.25 pclk), fix the wiring (a proper
   LTSSM training-state output is a small ltssm.py addition,
   gen2-gated).
3. **Rate-ack envelope**: the adapter acks a MAC rate change after a
   fixed ~7 ms; if PortConfig/SpeedSwitch behavior looks wrong on
   the probes, wire real CSR completion feedback from the sequencer
   instead (gw_usb3 submodule change; equivalence suite pins the
   vendor-exact config).
4. **Enum-surface gaps**: bcdUSB is 0310 but there is NO SSP BOS
   device capability and NO Sublink Speed Device Notification TP
   [8.5.6.7, 9.6.2.5]. Linux may enumerate regardless — check dmesg
   for BOS complaints. If blocked: add the SSP BOS descriptor
   (usb_protocol emitters) and a minimal gen2-gated notification-TP
   source in the protocol layer (sim red-first via a new enum-phase
   assertion).
5. **Mid-LTSSM pclk retune** (only bites on the FALLBACK path): an
   LTSSM-driven 10G→5G switch retunes pclk under a live MAC — the
   #22 corruption class. Phase H4 will find it; the fix template is
   the boot-window discipline (quiesce/park the MAC across the
   retune window inside Polling.SpeedSwitch/PortConfig).

Debug toolkit, in order of reach:
- uart0/uart1 probes (post-M2): ss-freq signature is the negotiated
  rate telltale (**156.25 ≈ 0x341554x count = still 10G; 125 ≈
  0x29aaa9x = fell back/never matched**), LFPS/SCD detect counts, TS
  detect flags, TxFifoWrNum, `Gen2BlockReceiver.queue_level` /
  `packets_buffered` high-water taps.
- `sudo -n dmesg -w` + usbmon (`/sys/kernel/debug/usb/usbmon/4u`)
  for the host's view; `lsusb -v -d 1209:0001` for the surface.
- A/B rigs: the archive `prj.fs` (known-good Gen2 on 4-3 — flash it
  whenever you suspect the bench/port before blaming our stack) and
  gw_usb3's usb31-enum (our PHY + vendor link netlist — isolates
  PHY-side vs our-MAC-side; the hybrid rig recipe is in the archive
  ARCHIVE.md).
- After any replug the device needs a fresh POR (reflash or board
  KEY); it parks in SS.Disabled 360 ms after boot. If a known-good
  image is dark: coordinate `usbX-portN/disable` warm-cycles with
  the flash (§10o).
- New bugs are **#39+**: sim-reproduce every bench finding where
  feasible (extend `sim_link_gen2.py` phases — the negotiation and
  framing paths all have host-model hooks) before fixing.

Gate: `lsusb` shows **10000M** on 4-3, dmesg clean, LED (link
trained) on, recorded uart captures.

### Phase H3 — the Gen2 ladder

- **Port the wire checker / BurstEventCapture to Gen2 framing
  FIRST** and calibrate on a quiet pipe before believing it (it is
  how #34 fell; §10n). It taps the translated Gen1-dialect streams
  around the link layer, so most of it should carry — verify the
  tap points against `physical/gen2.py`'s bridges.
- Build `luna-multiep-gen2` (the shipping 3-pair top with
  `gen2=True`, BURST=2 defaults, POR lottery comment carried over).
  Timing gate applies (Phase H1 rules; multiep is the harder
  placement — expect rolls).
- Ladder at Gen2 on 4-3: 1 MiB ×10 → 16 MiB ×3 → 64 MiB ×3 → ×10
  soak; sha-exact; per-pipe MB/s recorded; uart1 ch0
  retry_flagged=0. The stage-A core sustains ~½ the Gen2 wire
  (design note §1) — the honest target is **meaningfully above the
  284 MB/s Gen1 aggregate**; record whatever the number is. RX
  queue high-water goes into the §9.4 sizing verdict.

### Phase H4 — the dual-rate fallback matrix (same bitstream = the mission proof)

| run | image | port | expected | record |
|-----|-------|------|----------|--------|
| 1 | Gen2 multiep | 4-3 (10G) | 10000M + Gen2 ladder | lsusb, MB/s, ch0 |
| 2 | same image | hub 4-8.x (5G) | legacy fallback (no SCD from host) → 10G→5G switch → **5000M + full Gen1 ladder** | lsusb, MB/s, ch0 |
| 3 | same image, replug/POR ×5 | both ports | stable re-enumeration at the right rate every time | per-cycle verdicts |
| 4 | forced-Gen1 build (`gen2=False` = shipping) | 4-3 | 5000M + Gen1 ladder (the Phase-H0 numbers) | parity + verdicts |

Run 2 is the risky one (mid-LTSSM retune, suspect 5 above) — the
uart ss-freq signature tells you instantly whether the switch
happened. Do not regress the 5G trim: the gw_usb3 equivalence suite
plus run 2/4 are the guards.

**Gate G5 = the table above fully recorded + Phase H0/H3 ladders
green.** That closes the original dual-rate mission.

## Parked items that stay on the books (do not lose them)

From §10n/§10q/§10r, all still open: **#37** (truncated inbound DPP
never retried, `FORCE_REC_AT=710` repro) + forced-recovery harness
feed-truncation WIP; rule-2d/#36 positive-validation stimuli; the
bench forced-recovery verdict for #29–#31 (uart1 `'R'` hook is in
the tree — Gen2 recovery matters MORE, consider running it during
H3); data_tx SEND_ZLP bare-ready; wire-checker TP blindness; SKP
x=4 aligner fix behind an elaboration knob (when word_alignment is
open); stage-B width-generic core (post-G5, ~1.1 GB/s runway);
4+4 credit pools want 8 RX header buffers (stage B).

## Keep the discipline that closed thirty-eight bugs

- Sim first: every RTL change re-proves the gen2 battery section;
  the full battery (46 entries, ~35-45 min) from a SETTLED tree
  before each hardware build — never concurrent with source edits.
- Gen1 entries are a regression fence, never a casualty; shipping
  parity (payload compare) after every Gen1-shared-file change.
- One mechanism per change; hardware ladder with recorded verdicts
  before the next change; watch uart1 ch0 on every run.
- A Gen2 build that misses 156.25 is never flashed for Gen2 runs.
- New bugs: **#39+**, findings into HANDOVER §10s as you go; commit
  submodules first (gowin-serdes is PUBLIC — no vendor artifacts),
  then the fork; push everything.

## Tooling and bench facts (verify before trusting)

- One clone: `git clone --recurse-submodules
  github.com/key2/luna-ss && pdm install -G :all`. Frozen archive =
  `~/Downloads/GW_USB3` (ARCHIVE.md has the map; vendor `prj.fs`
  baseline + hybrid A/B rig live there).
- Board on 10G root port **`usb 4-3`** (straight = LN1 = correct;
  flipped = Q0_LN0 = probe-only). 5G test path = hub at `4-8.x`.
  Flash: `sudo -n openFPGALoader -c ft232 <fs>`. Board KEY replays
  POR without reflashing.
- Rebuild: `pdm run python top.py` in `examples/gowin/<name>/`
  (4–20 min). Timing: `.venv/bin/python tools/gowin_timing_report.py
  <example>/build --section fmax`. Gen1 gate: pclk ≥ 125 operating
  (156.25 misses benign at Gen1 — #22 boot window only). **Gen2
  gate: pclk AND rxclk 156.25 MET.** POR-nudge knob + roll history
  in `luna-multiep/top.py` (66_011 current).
- Verdicts: `multiep_test.py <MiB> --eps 1,2,3` (sudo; warmup on);
  uart0 link probe / uart1 wire checker @115200 on
  `/dev/ttyUSB4`/`/dev/ttyUSB5`; `uart_capture.py <s> <prefix>`
  interleaves both. usbmon at `/sys/kernel/debug/usb/usbmon/4u`;
  `sudo -n dmesg` works.
- **Run sims as `.venv/bin/python -u`** (`timeout`+`pdm run`
  orphans children). Battery: `pdm run battery`
  (= `sim/sim_battery.sh`), logs in `/tmp/kilo/batt_*.log`; per-entry
  runtimes in HANDOVER §10r. Gen2 sim knobs: `PHASE=`, `TSEQ_LEN=64`
  (always for train/enum/echo), `TSCALE=0.0625` (fb-timeout only),
  `NEG=nolcrd2` (negative control).
- The gen2 bench PIPE bring-up dance is solved — reuse
  `sim_link_gen2.bringup()` and `HostModem` (TUSB phy_status dialect,
  power_down + rate ack pulses); the LTSSM parks silently without
  them.
- Netlist-vs-RTL box for suspected GowinSynthesis miscompiles
  (archive §10k recipe; two confirmed classes have battery guards);
  fresh Yosys at `~/Downloads/yosys/build/yosys` is the validated
  escalation.

## Constraints

- gw_usb3's Gen1 5G TX path and its equivalence suite are settled —
  do not regress the 5G trim; PHY-side changes go behind elaboration
  knobs with the vendor-exact config still pinned by the equivalence
  tests. The 5G hub-port run (H4 run 2) is the hardware guard.
- The vendor `prj.fs` and refdesign stay untouched restore baselines
  (in the archive).
- BSD-3-Clause: upstream LUNA license and copyright headers stay
  intact; our commits carry our own attribution alongside.
- The shipping Gen1 configuration must remain buildable and
  ladder-green from every commit on main; `gen2=False` elaborations
  of shared files must stay bitstream-payload-identical unless a
  Gen1-affecting change is explicitly intended, battery-proven, and
  hardware-laddered.
- gowin-serdes is PUBLIC: no vendor artifacts there, ever.
