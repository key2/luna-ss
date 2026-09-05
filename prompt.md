# Mission: the WIDTH PROGRAM, session 20 — ship the Gen2-128 image
# and take the bug #49 bench verdict.  The 128-bit core is fully
# behavior-proven in simulation (all nine Gen2 phases green at
# core_width=128, battery 66/66); the ONLY thing between us and a
# clean, repeatable 10 Gb/s enumeration is the hardware glue: the 2:1
# PIPE bridge, one SDC line, and the top-level build.  After the
# verdict, begin the full-128 PHY per the standing directive.

## What this work is (read first, no ambiguity)

This is **forward engineering and validation of our own device
stack**, in our own repositories, on our own hardware:

* `luna-ss` — our public BSD-3-Clause fork of the LUNA USB framework.
  Upstream license and copyright headers stay intact; our commits
  carry our own attribution alongside.  Everything we add is code we
  wrote ourselves.
* `gw_usb3` — our own Amaranth implementation of the USB3 PHY layer
  for the serdes hard IP on our FPGA.  It was written against the PHY
  reference sources that ship with our licensed dev kit (they are the
  vendor's own documentation of how to drive their hard IP), and it
  is proven equivalent to that reference module-by-module by our own
  cocotb harness (`tests/test_equiv.py`).  Consulting one's licensed
  SDK sources to interoperate with the hard silicon on one's own chip
  is ordinary embedded engineering; no third-party RTL is copied into
  our repositories.
* `gowin-serdes` — our own PUBLIC board-support library.  It must
  stay free of anything that is not ours to publish.
* Behavior is validated against the **published USB 3.2 Revision 1.1
  specification** (markdown + page images in
  `doc/USB 3.2 Revision 1.1.pdf/` — the page images matter: bug #48
  was resolved by reading Figure 7-4 as an image), plus the PIPE
  architecture spec and the USB 3.1 Link Layer test spec in `doc/`.
* The link partner is the standard Linux xHCI host on the bench PC
  (dmesg, usbmon, PORTSC, our own on-chip probes on our own design).
* The manufacturer's reference bitstream (`prj.fs` in the frozen
  `~/Downloads/GW_USB3` archive) is used **unmodified, only as a
  known-good link-partner health baseline** — it proves the bench
  port and cable are fine before we trust new data.  We do not modify
  it and we do not derive code from it.

Read `HANDOVER.md` first — **§10aa** (session 19b) is the current
story; then §10z, §10y, §10x, §10w in that order for the width
program's history, and `doc/usb3_design.md` §13 for the design note
(§13.3/13.4 = the bridge spec and seam table; §13.8 = the PHY-side
widening that is now the plan of record).

## Where the program stands (all pushed through commit 36e883a)

* **The 128-bit core is BEHAVIOR-PROVEN**: `W128=1 PHASE=<any>` runs
  the full Gen2 phase set at core_width=128 — train, enum (full
  ladder: SET_ADDRESS, byte-exact descriptor, the 50-byte BOS with
  the SuperSpeedPlus capability, config), echo, u0, hotreset,
  hotreset-parked, recovery, reccut, advearly — **all green** at the
  78.125 MHz core clock, with the #44 pacing band held (max 16/32,
  zero hi28, zero starvation).  Battery = **66 entries, all green**
  (the full W64 regression set + the 9-entry w128 section).
* **Bug #49's device-side mechanisms are FIXED and sim-fenced**
  (session 17): #50 = the link-down advertisement/credit race (a
  header accepted in the first link-down cycle was delivered but not
  covered by the re-advertisement → the partner's rule-7
  retransmission read as a bad sequence → recovery loop + wedged
  EP0); #51 = the consumed-payload bookkeeping window (a retrain
  cutting a DP after its last payload word made the DL=1
  retransmission attach phantom payload instead of aborting the DPP
  — the BOS/22 EPROTO wire shape).  Both red-first via PHASE=reccut.
  The SSP BOS device capability [9.6.2.5] landed the same session.
  **The bench verdict is the only open gate on #49.**
* **The protocol boundary stays 32-bit** behind
  `link/width_adapters.py` (store-and-forward TX with the state-keyed
  header offer + `data_tx.external_accept`; monitor-style RX splitter
  with through-FIFO verdict strobes).  Control traffic is
  full-fidelity; sustained bulk is capped at 4 B/core-cycle until the
  endpoints widen (a parked item — sha-exactness is the ladder
  verdict at Gen2, MB/s is documented-degraded).
* The Gen1-64 shipping build is untouched: parity proven after every
  shared-file change (diffs only in the ~600–622 header date region),
  fence ladder green on hardware.

## The standing directives (binding)

1. **Full-128 PHY+MAC is the end state.**  The gw_usb3 PHY datapath
   moves to 128 bits after the bench verdict; the 64-bit GEN2 trims
   retire (the 64-bit Gen2 core misses timing structurally: 10–12
   LUT levels against a 6.4 ns budget, −60.8 ns TNS across 303 MAC
   endpoints, 10/10 seed rolls failed).  The 2:1 PIPE bridge built
   this session is therefore INTERIM — it ships the first Gen2-128
   image against the proven 64-bit PHY datapath so the #49 verdict
   lands soonest, and its testbench + pacing-lag model become the
   acceptance fixtures for the PHY widening.
2. The Gen1-64 shipping configuration stays buildable and
   ladder-green from every commit on main (it is the shipping
   product and the future C2/I1 speed-grade trim); `gen2=False`
   64-bit elaborations of shared files stay bitstream-payload-
   identical unless a change is explicitly intended, battery-proven,
   and hardware-laddered.
3. Single lane everywhere.  No x2 work, ever.
4. Do not spend sessions on Gen2-64 placement rolls; that path is
   closed.

## Deliverables (in order)

1. **The 2:1 PIPE bridge** (new module under
   `luna/gateware/interface/serdes_phy/`), per usb3_design.md
   §13.3/13.4 and HANDOVER §10aa:
   * pclk-domain phase toggle aligned to the /2 FF divider (which
     also generates the core clock);
   * TX: each core beat → two pclk beats (`tx_data[64:128]` is
     first-on-wire, then `[0:64]`); a `tx_halfbeat` beat → exactly
     ONE pclk beat (the 24-symbol SKP OS tail, symbols 16–23 in the
     top lanes); tx_datavalid gaps emit nothing on either phase;
   * RX: start-anchored pair accumulator presenting
     `(beat0 << 64) | beat1` + rx_start for one core cycle;
   * seam registers per the §13.4 table: `phy_status`
     latch-and-hold ≥ 2 pclk; `tx_fifo_occupancy` registered at the
     core edge;
   * **RED-FIRST proof before any hardware**: a two-clock testbench
     pinning BOTH directions byte-exact — including the SKP-halfbeat
     seam and valid gaps (a phase bug here is the wire-garbage
     failure class) — plus the #44 pacing-lag re-proof in
     `tests/test_gen2_pacing.py` (the bridged occupancy lags 2–3
     pclk; the loop was designed for that budget — show it).
2. **gowin-serdes SDC branch**: `create_generated_clock -divide_by 2`
   on the divider FF; the pclk 6.4 ns and rxclk 6.2 ns constraints
   stay.  gowin-serdes is PUBLIC — keep it clean.
3. **`luna-enum-gen2` at core_width=128**: divider + bridge between
   `GowinGTR12PIPE` (64-bit pclk side, unchanged) and
   `USBSuperSpeedDevice(core_width=128)` under
   `DomainRenamer({"ss": "core"})`; probes re-homed to the domain
   whose state they sample.  Build, gate timing
   (`tools/gowin_timing_report.py <build> --section fmax`: core ≥
   78.125 AND pclk ≥ 156.25 AND rxclk ≥ 161.29 — only the thin
   bridge and the PHY fabric attach remain in the pclk domain), 
   flash, and take **the #49 bench verdict**: repeatable **10000M**
   on port 4-3 across replug/POR cycles, dmesg clean (and no
   SSP-BOS complaint), `lsusb` shows the device, then the Gen2
   ladder (sha-exact is the verdict; MB/s is adapter-capped).
   Run the uart1 'R' forced-recovery hook during the ladder (the
   parked #29–#31 verdict).  A build that misses ITS timing gate is
   never flashed for Gen2 runs.
4. **Begin the full-128 PHY** (directive 1): gw_usb3 datapath at 16
   symbols/beat end to end (RX/TX gearboxes, scrambler chain,
   elastic buffer), against the `tests/test_equiv.py` oracle-harness
   pattern — unit-by-unit equivalence fences exactly like the MAC
   widening; the proven 5G configuration stays pinned by its
   regression suite until its own hardware ladder.
5. **The Gen1 fence intact** throughout: payload-identical after
   every shared-file change, ladder-green on hardware.

HANDOVER continues at **§10ab**; bug numbering continues at **#52**
(#49 is open pending the bench verdict and comes first).

## Phase plan (each phase gated; one mechanism per change)

### V0' — orientation and the fence (short)

Read HANDOVER §10z–§10aa and usb3_design.md §13.3/13.4/13.8.
Re-verify the Gen1 fence on the bench BEFORE touching anything
(5000M on 4-3, 1 MiB ×10, 16 ×3, 64 ×3, sha-exact, uart1 ch0 = 0);
fence image = `/tmp/kilo/h0_gen1_fence.fs`.  Expect the
port-recovery runbook on arrival (the resident image may be a
wedged Gen2 build — see the runbook below).  Then confirm the
battery is 66/66 from the settled tree.

### V1 — the bridge, sim-proven (deliverable 1)

The two-clock testbench first, red against a deliberately broken
phase relation, then green; the pacing-lag model red-first.  Full
battery from a settled tree before any hardware build.

### V2 — the Gen2-128 bitstream and the #49 verdict (deliverables 2–3)

SDC, top, build, gate, flash — bench evidence with the established
tooling (dmesg, lsusb, usbmon, PORTSC tracer, uart captures with
per-cause probe counters: the #50/#51 fixes predict the retrain
storm and the EPROTO wedge DISAPPEAR; if any trace remains, the
per-cause counters and the sub-block-granularity reccut parked item
are the next evidence steps).  Record verdicts.  If the verdict is
clean, also run the 5G-hub-port fallback row (the dual-rate matrix
run 2) while the bench is hot.

### V3 — the full-128 PHY begins (deliverable 4)

Survey gw_usb3's datapath units; widen bottom-up with equivalence
fences (the landed MAC pattern: words parameter, narrow verbatim,
composition proofs, mutation checks).  Do NOT destabilize the 5G
configuration — elaboration knobs, proven trim pinned.

## Parked items that stay on the books

The Gen1-rail twins of #50/#51 (same races exist in the non-gen2
elaborations, verbatim-preserved for the fence — they need the
explicit intend/battery/hardware-ladder ceremony); full-rate 64-bit
endpoint widening (the Gen2 bulk MB/s targets); the reccut sweep at
sub-block cut granularity; #37 RX side (truncated inbound DPP never
retried); RX-side DPH replica-match validation [7.2.4.1.6 rule 2a];
rule-2d/#36 positive-validation stimuli; data_tx SEND_ZLP
bare-ready; wire-checker TP blindness; SKP x=4 aligner knob; stage-B
credit scaling beyond 4+4; the Gen1-128 native serdes trim (20×1:4,
the V2 matrix row) — superseded in priority by the full-128 PHY but
still on the books.

## Keep the discipline that closed fifty-one findings

* Sim first; red-first for every new mechanism; the FULL battery
  (66 entries) from a SETTLED tree before each hardware build —
  never concurrent with source edits.
* Gen1-64 entries are a regression fence, never a casualty; shipping
  parity (payload compare vs `/tmp/kilo/h0_gen1_fence.fs`, diffs
  only in the ~600–622 header date region) after every
  Gen1-shared-file change.
* One mechanism per change; hardware ladder with recorded verdicts
  before the next change; watch uart1 ch0 on every run.
* A Gen2 build that misses ITS width's timing gate is never flashed
  for Gen2 runs.
* New findings into HANDOVER §10ab as you go; commit submodules
  first (gowin-serdes is PUBLIC — keep it clean), then the fork;
  push.

## Tooling and bench facts (verify before trusting)

* One clone: `git clone --recurse-submodules
  github.com/key2/luna-ss && pdm install -G :all`.  Frozen archive =
  `~/Downloads/GW_USB3` (ARCHIVE.md maps it; the reference `prj.fs`
  health-baseline bitstream lives there).
* Board on 10G root port **`usb 4-3`**.  5G test path = hub at
  `4-8.x`.  Flash: `sudo -n openFPGALoader -c ft232 <fs>`.  The
  device parks in SS.Disabled ~360 ms after boot — every test wants
  a fresh POR (reflash), against a QUIET port.
* **Port-recovery runbook (order matters, session-16 proven)**: if
  the port loops on warm resets: (1) PCI unbind/rebind of
  `0000:80:14.0`; (2) after a rebind the kernel may bind ftdi_sio to
  ALL FOUR FTDI channels — unbind the JTAG channel before flashing:
  `echo -n "3-7.3.2:1.0" | sudo tee
  /sys/bus/usb/drivers/ftdi_sio/unbind` (check the actual path with
  `ls /sys/bus/usb/drivers/ftdi_sio/`; the quad FTDI has been seen
  at `3-6.4` too — the JTAG is the single-channel FT232H); (3) flash
  the reference `prj.fs` and confirm 10000M (the health oracle);
  (4) only then flash the image under test.  Never trust new data
  from a looping port.
* UARTs by stable path; use the repo's
  `examples/gowin/luna-multiep/uart_capture.py <s> <prefix>` (by-id;
  tag **L = uart0**/if02 link probe, tag **C = uart1**/if03 pipe
  probe).  Gen2 probe channel maps are documented at the top of
  `examples/gowin/luna-enum-gen2/top.py`.
* Verdicts: `multiep_test.py <MiB> --eps 1,2,3` (sudo).  usbmon at
  `/sys/kernel/debug/usb/usbmon/4u`; `sudo -n dmesg` works.  PORTSC
  tracer `/tmp/kilo/portsc_trace.py` (bus4-port3 = debugfs port19).
  Boot A/B harness `/tmp/kilo/boot_ab.sh`.
* **Run sims as `.venv/bin/python -u`** (`timeout`+`pdm run` orphans
  children).  Battery: `pdm run battery` or `bash
  sim/sim_battery.sh`, logs in `/tmp/kilo/`.  Gen2 sim knobs:
  `PHASE=` (train/enum/echo/u0/hotreset/hotreset-parked/recovery/
  reccut/advearly), **`W128=1`** (the 128-bit core; clear-data
  conditioning — the RTL scrambler round-trip is a 64-bit PHY
  surface, W64-only), `TSEQ_LEN=64` (always for the phase runs),
  `TSCALE=0.0625` (fb-timeout only), `NEG=nolcrd2` (negative
  control), `VERBOSE=1` (event traces).
* Timing gates: Gen1-64 pclk ≥ 125; Gen2-128 core ≥ 78.125 AND
  pclk ≥ 156.25 AND rxclk ≥ 161.29 (the 6.2 ns rxclk SDC stays).
* Saved images in `/tmp/kilo/`: `h0_gen1_fence.fs` (the fence),
  `s16_gen2_48fix_66_135_met.fs` (the PRE-#50/#51 Gen2-64 evidence
  build — never a verdict vehicle).  Evidence captures:
  `s16_usbmon_bos.log` (the BOS/22 failure),
  `s16_bos_window_both.txt` (uart counters during the window).
* Known wiring trap (documented §10z): the sim Bench routes device
  TX through a 64-bit RTL scrambler and host RX through a 64-bit RTL
  descrambler — both single-domain, so W128 bypasses them and moves
  blocks CLEAR; keep the RTL-conditioned path at W64 (it is part of
  the proven fences).

## Constraints

* Single lane everywhere.  No x2 work, ever.
* The `gw_usb3` 5G configuration and its regression suite are
  settled — PHY-side changes go behind elaboration knobs with the
  proven configuration still pinned; the 5G hub-port run is the
  hardware guard.
* The manufacturer's reference bitstream stays untouched; it is only
  the link-partner health baseline for our own board.  No
  third-party RTL is copied into our repositories; the licensed SDK
  sources serve only as interface documentation for the hard IP our
  own PHY drives, and our PHY's equivalence to the reference is
  proven by our own test harness.
* BSD-3-Clause: upstream LUNA license and copyright headers stay
  intact; our commits carry our own attribution alongside.
* The shipping Gen1-64 configuration must remain buildable and
  ladder-green from every commit on main.
* gowin-serdes is PUBLIC: keep it free of anything that is not ours
  to publish.
