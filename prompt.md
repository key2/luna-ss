# Mission: the WIDTH PROGRAM, single lane only — continue making our
# USB 3.2 device stack width-generic (64-bit AND 128-bit cores) so
# every shipping configuration closes timing cleanly: Gen 1x1 on the
# 64-bit core as today, Gen 1x1 and Gen 2x1 on the 128-bit core.
# Resolve open bug #49 on the way (it is the last thing standing
# between us and clean 10 Gb/s enumeration).  A Gen2 64-bit trim that
# misses timing remains ACCEPTABLE as long as the 128-bit trim meets it.

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
  is proven equivalent to that reference module-by-module by our
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

Read `HANDOVER.md` first — **§10v** (session 16) is the current
story; then §10u (session 15) and the `doc/usb3_design.md` §13 design
note (the width-program plan, the 2:1 bridge, the §13.8
considered-alternative record).

## Where the program stands (session-16 outcomes, all pushed)

* **Bug #45 RESOLVED** (the 142 kHz U0→Recovery metronome): root
  cause was #46 — the TX request-seam hazards (U0-entry idle_mode
  blip truncating a 132-bit block mid-stream; the SDS arm/wipe write
  race; the TX bridge carrying a stale mid-cut link command across
  retrains).  Fixed, sim-fenced red-first (`tests/test_gen2_tx_seams
  .py`), bench-verified: the per-cause probe counters read zero and
  PORTSC reaches U0 at 10 Gb/s with transfer attempts.
* **#47 hardening**: early link-command capture window
  (`PHASE=advearly` battery entry).  The concurrent-advertisement
  lead was executed and EXCLUDED as a #45 cause under causally-legal
  host timing.
* **Bug #48 RESOLVED on the wire**: the non-deferred Gen 2 DPH is
  **24 bytes** — the length-field replica appears TWICE after the LCW
  (Figure 7-4); we had implemented one copy from the prose, and the
  strict-host upgrade reproduced the silicon failure byte-exact
  before the fix.  Bench: the device descriptor and BOS-header reads
  now SUCCEED at 10 Gb/s against the real host.
* **Bug #49 OPEN — first among bugs**: enumeration now dies at the
  FULL BOS read (`GetDescriptor(BOS, 22)` → EPROTO -71 after ~7 ms),
  after which EVERY transfer fails (even read/8, even after the port
  falls back to 5 Gb/s) until the device is power-cycled — an
  EP0/protocol-state wedge that survives hot reset.  Device-side
  evidence from our probes during the window: OUR recovery causes
  read ZERO, but ts1-det counts ~1.4 M/s and sds-det ~5.5 k/s
  (host-initiated retrains at kHz rates THROUGHOUT the window, even
  while the earlier transfers succeed between them), and the
  `txfifo-hi28` canary (TX FIFO ≥ 28 of 32) fires ~71 k/s — the #44
  closed loop should hover at 16, so something periodically overshoots
  the pacing band toward overflow.  The extended sim ladder
  (BOS/5 → BOS/22 → Config/9, now in `PHASE=enum`, GREEN) does NOT
  reproduce it in lockstep timing: the gap is timing/pipelining
  (the real host overlaps traffic and yanks retrains mid-transfer).
* **Width program**: V0 done (design note §13); V1a done
  (`core_width` elaboration point, 64 = verbatim, parity-proven);
  V1b under way — wide CRC-16/CRC-32 and 8-symbol scrambler surfaces
  landed by composition with byte-exact equivalence fences.
* The Gen1 fence was re-proven green at session start AND end.

## The binding scope decisions (unchanged)

1. The 64-bit core at the Gen2 rate needs pclk ≥ 156.25 and rxclk ≥
   161.29 — the placement lottery is real (the #48-fix netlist took 10
   rolls to MET; the seed history lives in the enum-gen2 top).  **At
   128-bit the Gen2 core clock is 78.125 MHz and the fight
   disappears.**  Do not budget sessions on 64-bit rolls; a lottery
   win is a bonus debug vehicle, nothing more.
2. **Gen 1x2 is out of scope permanently.**  Single lane everywhere.
   The x2 artifacts in the tree stay as-is and receive no work.

## The target matrix (all single-lane)

| config | core width | core clock | status target |
|--------|-----------|------------|---------------|
| Gen 1x1 | 64 | 125 | the SHIPPING build — stays bitstream-payload-identical and ladder-green throughout (the fence) |
| Gen 1x1 | 128 | 62.5 | native serdes trim — build, timing, full ladder |
| Gen 2x1 | 128 | 78.125 | the Gen2 ship vehicle — 2:1 bridge at the PIPE boundary (the 10G serdes fabric attach is fixed at 64-bit/156.25; §13.8 records why the PHY datapath stays 64-bit for now) — timing MET, **#49 resolved**, 10000M enumeration + ladder |
| Gen 2x1 | 64 | 156.25 | kept sim-green and buildable; timing OPTIONAL (bench-debug vehicle; current MET image saved in /tmp/kilo) |

The PHY side (`gw_usb3`) keeps its proven 64-bit/156.25 datapath at
Gen2 (rxclk truly 161.133 — the 6.2 ns SDC stays) and gains only what
the Gen1 native 62.5 trim needs; the proven 5G configuration stays
pinned by its regression suite.

## Deliverables

1. **Bug #49 resolved** — clean, repeatable **10000M enumeration**
   (`lsusb` on port 4-3, dmesg clean).  The evidence points at three
   interacting surfaces; take them evidence-first:
   (a) the host-initiated retrain storm: why does the host's receiver
   dislike our TX at kHz rates?  The `txfifo-hi28` canary says the
   #44 pacing band is overshot — find the overshoot mechanism (SKP
   scheduling interaction, REPLICA-stall supply bursts, bridge
   prefetch) with a red-first sim modeling the real drain, THEN
   confirm on the bench;
   (b) a control transfer cut by a retrain mid-data-stage: the
   delayed-DPH / DPPABORT retransmission surface and the endpoint's
   retry handling (sim lead: inject Recovery between the IN ACK TP
   and the DPP, and between DPH and DPP — the #37 parked item is a
   live suspect);
   (c) the post-failure wedge: EP0/protocol state must fully recover
   on hot reset and on rate fallback (sim lead: run the hotreset
   phase with a transfer parked mid-data-stage).
   Also close the now-REQUIRED enum-surface gap: at bcdUSB 0310 the
   host demands a BOS with the SuperSpeedPlus device capability
   (dmesg complains today) — add the SSP capability (and the Sublink
   Speed Device Notification TP if the host asks) [8.5.6.7, 9.6.2.5].
2. **Width-generic core**: `core_width ∈ {64, 128}` through the LUNA
   stack, sim-proven at BOTH widths (V1c–V1e continue: 8-symbol
   CTC/aligners/coding next, then framers at 64-bit streams, the
   gen2 one-beat-per-block machinery, the 2:1 PIPE bridge with its
   red-first pacing-lag sims — the work list is §13.5).
3. **The Gen1 fence intact**: payload-identical (timestamp bytes
   only) after every shared-file change, ladder-green on hardware.
4. **Gen 1x1 @ 128 on hardware**: 5000M + full multiep ladder.
5. **Gen 2x1 @ 128 on hardware**: timing MET (core 78.125, pclk
   156.25, rxclk 161.29), 10000M + the Gen2 ladder (1 MiB ×10 → 16 →
   64 MiB ×3 → soak, sha-exact, per-pipe MB/s, wire checker ported
   and calibrated).
6. **The dual-rate matrix** (closes G5, re-scoped, no x2): Gen2/128
   image on the 5G hub port falls back per spec and runs the Gen1
   ladder; replug/POR ×5 both ports; forced-Gen1 build re-laddered.
   Recorded verdict table.

HANDOVER continues at **§10w**; bug numbering continues at **#50**
(#49 is open and comes first among bugs).

## Phase plan (each phase gated; one mechanism per change)

### V0' — orientation and the fence (short)

Read HANDOVER §10u–§10v and usb3_design.md §13.  Re-verify the Gen1
fence on the bench (5000M on 4-3, 1 MiB ×10, 16 ×3, 64 ×3, sha-exact,
uart1 ch0 = 0) BEFORE touching anything; fence image =
`/tmp/kilo/h0_gen1_fence.fs`.

### V1 — continue the width-generic core (sim-proven)

Follow §13.5 in order, each unit with composition-equivalence fences
(the landed CRC/scrambler pattern): CTC/aligners/coding at 8 symbols;
stream-width threading + framers (HP = 2.5 beats padded on TX,
offsets 0/4 on RX; LC = 1 beat); `physical/gen2.py` at 128 (1 beat =
1 block; re-prove the #43 queue bound red-first); the 2:1 bridge
(`tx_halfbeat` SKP contract, pacing-lag sims red-first); gowin-serdes
20×1:4 trim + w128 SDC branches (generated clock /2).  Gen1-64
shipping parity after EVERY shared-file change.  Full battery (now 57
entries) green from a settled tree before any hardware build.

### V2 — Gen1 on hardware, both widths

64-bit fence re-proof after V1's churn, then the 128 @ 62.5 native
trim: new top, trivial timing gate, flash, 5000M, full ladder.

### V3 — Gen 2x1 @ 128 on hardware (the Gen2 gate, and #49)

**#49 first** (deliverable 1 — the sim leads are listed there; the
bench MET image `/tmp/kilo/s16_gen2_48fix_66_135_met.fs` is available
TODAY as the 64-bit debug vehicle for evidence runs, no new rolls).
Then build `luna-enum-gen2` at core_width=128 with the bridge, gate
timing (`tools/gowin_timing_report.py <build> --section fmax`), flash,
10000M, dmesg clean, then the Gen2 ladder.  Run the uart1 'R'
forced-recovery hook during the ladder (the parked #29–#31 verdict).

### V4 — the dual-rate matrix (G5 close)

| run | image | port | expected | record |
|-----|-------|------|----------|--------|
| 1 | Gen2/128 multiep | 4-3 (10G) | 10000M + Gen2 ladder | lsusb, MB/s, ch0 |
| 2 | same image | hub 4-8.x (5G) | fallback → 5000M + Gen1 ladder | lsusb, MB/s, ch0 |
| 3 | same image, replug/POR ×5 | both ports | right rate every time | per-cycle verdicts |
| 4 | shipping Gen1-64 build | 4-3 | 5000M + Gen1 ladder (fence numbers) | parity + verdicts |
| 5 | Gen1-128 build | 4-3 | 5000M + Gen1 ladder | verdicts |

**The gate = the table fully recorded.**

## Parked items that stay on the books

#37 (truncated inbound DPP never retried, FORCE_REC_AT=710 repro —
now a live #49 suspect); RX-side DPH replica-match validation
[7.2.4.1.6 rule 2a → Recovery] (parked from the #48 fix); rule-2d/#36
positive-validation stimuli; data_tx SEND_ZLP bare-ready;
wire-checker TP blindness; SKP x=4 aligner knob; stage-B credit
scaling beyond 4+4; §13.8 (PHY-side widening) revisits WITH the
½-wire-rate cap lift, after the V3 gate.

## Keep the discipline that closed forty-eight bugs

* Sim first; red-first for every new mechanism; the FULL battery from
  a SETTLED tree before each hardware build — never concurrent with
  source edits.
* Gen1-64 entries are a regression fence, never a casualty; shipping
  parity (payload compare vs `/tmp/kilo/h0_gen1_fence.fs`, diffs only
  in the ~600–622 header date region) after every Gen1-shared-file
  change.
* One mechanism per change; hardware ladder with recorded verdicts
  before the next change; watch uart1 ch0 on every run.
* A Gen2 build that misses ITS width's timing gate is never flashed
  for Gen2 runs.
* New findings into HANDOVER §10w as you go; commit submodules first
  (gowin-serdes is PUBLIC — keep it clean), then the fork; push.

## Tooling and bench facts (verify before trusting)

* One clone: `git clone --recurse-submodules
  github.com/key2/luna-ss && pdm install -G :all`.  Frozen archive =
  `~/Downloads/GW_USB3` (ARCHIVE.md maps it; the reference `prj.fs`
  health-baseline bitstream lives there).
* Board on 10G root port **`usb 4-3`**.  5G test path = hub at
  `4-8.x`.  Flash: `sudo -n openFPGALoader -c ft232 <fs>`.  The
  device parks in SS.Disabled ~360 ms after boot — every test wants a
  fresh POR (reflash), against a QUIET port.
* **Port-recovery runbook (order matters, session-16 proven)**: if
  the port loops on warm resets: (1) PCI unbind/rebind of
  `0000:80:14.0`; (2) after a rebind the kernel may bind ftdi_sio to
  ALL FOUR FTDI channels — unbind the JTAG channel before flashing:
  `echo -n "3-7.3.2:1.0" | sudo tee /sys/bus/usb/drivers/ftdi_sio/unbind`
  (check the actual path with `ls /sys/bus/usb/drivers/ftdi_sio/`);
  (3) flash the reference `prj.fs` and confirm 10000M (the health
  oracle); (4) only then flash the image under test.  Never trust new
  data from a looping port.
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
  children).  Battery: `pdm run battery`, logs in `/tmp/kilo/`.
  Gen2 sim knobs: `PHASE=` (incl. `hotreset`, `recovery`,
  `advearly`), `TSEQ_LEN=64` (always for
  train/enum/echo/u0/hotreset/recovery/advearly), `TSCALE=0.0625`
  (fb-timeout only), `NEG=nolcrd2` (negative control).
* Timing gates: Gen1-64 pclk ≥ 125; Gen1-128 core ≥ 62.5; Gen2-128
  core ≥ 78.125 AND pclk ≥ 156.25 AND rxclk ≥ 161.29.  Roll batches:
  `/tmp/kilo/s16_roll.sh` automates seed-nudge → build → gate.
* Saved images in `/tmp/kilo/`: `h0_gen1_fence.fs` (the fence),
  `s16_gen2_48fix_66_135_met.fs` (the current MET Gen2-64 debug
  vehicle: #46+#47+#48 fixes + per-cause probes),
  `s16_gen2_46_47_percause_met.fs` (pre-#48-fix evidence build).
  Evidence captures: `s16_usbmon_bos.log` (the BOS/22 failure),
  `s16_bos_window_both.txt` (uart counters during the window).

## Constraints

* Single lane everywhere.  No x2 work, ever.
* The `gw_usb3` 5G configuration and its regression suite are settled
  — PHY-side changes go behind elaboration knobs with the proven
  configuration still pinned; the 5G hub-port run (V4 run 2) is the
  hardware guard.
* The manufacturer's reference bitstream stays untouched; it is only
  the link-partner health baseline for our own board.  No third-party
  RTL is copied into our repositories; the licensed SDK sources serve
  only as interface documentation for the hard IP our own PHY drives,
  and our PHY's equivalence to the reference is proven by our own
  test harness.
* BSD-3-Clause: upstream LUNA license and copyright headers stay
  intact; our commits carry our own attribution alongside.
* The shipping Gen1-64 configuration must remain buildable and
  ladder-green from every commit on main; `gen2=False`/64-bit
  elaborations of shared files stay bitstream-payload-identical
  unless a change is explicitly intended, battery-proven, and
  hardware-laddered.
* gowin-serdes is PUBLIC: keep it free of anything that is not ours
  to publish.
