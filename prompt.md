# Mission: the WIDTH PROGRAM, session 21 — name and kill the #49
# device-TX wedge.  The Gen2-128 image is BUILT, MET (first roll) and
# TRAINS AT 10 Gb/s; enumeration completes byte-exact through BOS/5
# and then dies on one deterministic mechanism: the device's TX side
# wedges after transmitting its first >18-byte DP.  Session 20
# collapsed the mechanism space and named the instruments; this
# session builds them, localizes the wedge (H1 vs H2), fixes it
# red-first, and takes the #49 verdict.  Then the full-128 PHY
# begins per the standing directive.

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
  (dmesg, usbmon, xhci ftrace, PORTSC, our own on-chip probes).
* The manufacturer's reference bitstream (`prj.fs` in the frozen
  `~/Downloads/GW_USB3` archive) is used **unmodified, only as a
  known-good link-partner health baseline**.  We do not modify it and
  we do not derive code from it.

Read `HANDOVER.md` first — **§10ab** (session 20) is the current
story and carries the complete #49 evidence chain; then §10aa, §10z
for the width program's recent history, and `doc/usb3_design.md` §13
(§13.3/13.4 = the bridge, LANDED; §13.8 = the PHY-side widening).

## Where the program stands (all pushed through commit 4787f1f;
## submodules: gowin-serdes a698d24, gw_usb3 1b54cf6)

* **The Gen2-128 image EXISTS and TRAINS AT 10 Gb/s.**
  `examples/gowin/luna-enum-gen2` is the Gen2-128 vehicle:
  core_width=128 under `DomainRenamer({"ss": "core"})` at pclk/2
  (78.125 MHz), the 2:1 PIPE bridge
  (`luna/gateware/interface/serdes_phy/pipe_bridge_2to1.py`,
  sim-fenced with the inverted-phase negative control), the 3
  multiep bulk pairs + 16 KiB elastic FIFOs, the uart1 'R'
  forced-recovery hook, probes re-homed per domain.  Timing gate MET
  ON THE FIRST ROLL: core_clk 78.872 / pclk 157.425 / rxclk 161.934,
  TNS 0 setup AND hold (the retired Gen2-64 missed 10/10 rolls).
  Resources: 48% logic, 61% CLS, 75% BSRAM (30 BSRAM + ~31k LUT
  free for instruments).  Image: `/tmp/kilo/s20_gen2_128_met.fs`.
* **Bug #49 is the ONLY blocker, and its mechanism space collapsed
  in session 20** (all repeatable, 3/3 PORs, evidence in §10ab):
  - The image trains SuperSpeed Plus Gen 2x1 and completes dev/8,
    SET_ADDRESS, SET_ISOCH_DELAY, dev/18, BOS/5 **byte-exact**.
  - **The length law**: every EP0 IN transfer with payload ≤ 18
    bytes completes; the first ≥ 22 bytes (the 50-byte BOS read)
    dies EPROTO -71 **deterministically** and EP0 is wedged for
    everything after (even dev/8 on re-enumeration; survives warm
    reset; only POR clears).  Same law at Gen2-64 in s16 (BOS/22)
    → width-independent, PRE-DATES the bridge.
  - **Device-side per-cause recovery counters read ZERO** (uart0
    ch1/2/3) — the #50/#51 mechanisms are confirmed GONE on
    silicon.  The retrain storm is host-initiated (~70k/s ts2
    handshakes during the window).  txfifo-hi28 = 0 throughout.
  - **xhci ftrace localization** (`/tmp/kilo/s20_xhci_trace.txt`):
    the Transaction Error points at the **Status Stage TRB** of the
    BOS/50 TD (Setup@..b0/Data@..c0/Status@..d0 ring layout — a
    data-stage error would point at the Data TRB): **the 50-byte
    DPP reached the xHC intact**; the transfer died at the status
    handshake.  Every later SETUP errors with len 8 (zero bytes
    accepted): the device stops handshaking ALL host packets while
    its RX header counters KEEP COUNTING.  Shape: **the device TX
    side wedges immediately after transmitting its first >18-byte
    DP; RX stays alive.**
  - **The MAC's cut handling is exonerated for the exact transfer**:
    `run_reccut` now carries the bos50 sweep (GetDescriptor(BOS,50)
    cut at 14 offsets walking the whole construct) — GREEN at BOTH
    widths (W64 = through the RTL scrambler round-trip).  The plain
    50-byte read is green in every enum phase.  Battery = **67/67**.
* **Finding #52 (FIXED, binding lesson)**: session 19b's
  `external_accept` hook perturbed the words=1 shipping netlist
  (42105 diff bytes vs the fence image; 19b never ran the parity
  step).  Fixed via a constructor knob; parity restored to 13 bytes
  (602–620, header date only).  THE LESSON: the shipping-parity
  rebuild is part of EVERY session that touches a shared file.
* The Gen1-64 shipping build: fence GREEN at session-20 start AND
  end; the fence image is RESIDENT on the board (5000M on 4-3).

## The standing directives (binding)

1. **Full-128 PHY+MAC is the end state.**  The gw_usb3 PHY datapath
   moves to 128 bits after the #49 verdict; the 2:1 bridge is
   INTERIM.  Its testbench + pacing-lag model
   (tests/test_gen2_pipe_bridge.py, tests/test_gen2_pacing.py) are
   the acceptance fixtures for the PHY widening.
2. The Gen1-64 shipping configuration stays buildable and
   ladder-green from every commit on main; `gen2=False` 64-bit
   elaborations of shared files stay bitstream-payload-identical
   (the parity rebuild EVERY session that touches a shared file —
   the #52 lesson) unless a change is explicitly intended,
   battery-proven, and hardware-laddered.
3. Single lane everywhere.  No x2 work, ever.
4. No Gen2-64 placement rolls; that path is closed and retired.

## Deliverables (in order)

1. **The H1/H2 discriminator instruments** in the Gen2-128 top
   (BSRAM/LUT headroom is ample; the core domain has 12.8 ns —
   instruments are timing-cheap there):
   * **PipeBeatCapture** — extend the proven `BurstEventCapture`
     ring pattern (luna-multiep/top.py) into a triggered PIPE-beat
     ring: pre-trigger ring (keep writing, freeze at trigger+offset)
     of ~128 records × {tx_data beat, tx_datavalid, tx_start_block,
     tx_sync_header, TxFifoWrNum, gen2_tx.debug_state, a coarse
     timestamp}, trigger = "device DPH with data_length > 18"
     (content tap at the link-layer TX) with a runtime-selectable
     trigger mux over the uart1 RX command channel (the 'R'-hook
     idiom; 2–3 trigger sources so one bitstream serves several
     questions).  Dump over uart as hex records.  RED-FIRST: a unit
     testbench proving trigger/freeze/dump against scripted streams
     (including the no-trigger and double-trigger cases).
   * **TxWireChecker for Gen2** — the multiep checker (CRC-32
     recompute + DP framing) on the dialect-neutral link-layer TX
     tap, its sticky flags + per-cause counters on uart channels;
     plus a per-interval **device-TX TP/DPH counter** channel (does
     the MAC keep TRANSMITTING after the wedge onset?).
   * Do NOT import LiteScope/foreign RTL — the in-tree ring pattern
     + our CDC/SDC idiom covers it (session-20 assessment).
2. **The bench localization run**: rebuild (native yosys — see
   tooling), gate timing (core ≥ 78.125, pclk ≥ 156.25, rxclk ≥
   161.29 — a build that misses ITS gate is never flashed for Gen2
   runs), flash, POR under full instrumentation (uart capture +
   usbmon + xhci ftrace).  The verdict tree:
   - MAC keeps emitting well-formed TPs the host never sees → **H1**
     (gen2_tx scheduler → PHY TX gearbox/scrambler/FIFO seam under
     OUR beat pattern; the vendor MAC drives the same silicon
     through long bulk DPs fine — diff OUR beat/gap/SKP pattern
     around a >18-byte construct against the vendor's using the
     capture; the sim's #44 drain-law model and the gw_usb3 TX-path
     equivalence suite are the reference points).
   - MAC goes quiet (no TX TPs after the DP) → **H2** (a MAC-level
     TX-arbiter/credit/handshake hang the idealized sim host's
     timing never provokes — feed the captured real-host timing
     shape back into the sim as a new stimulus, red-first).
   - The **12-byte-BOS diagnostic build** (BOS truncated to the
     USB2-ext cap only; spec-invalid but host-readable) is the
     second POR if needed: if BOS/12 completes and the wedge
     migrates to the next ≥22-byte read, the length law is
     descriptor-independent — pure TX-construct-length.
3. **The fix, red-first**: once the mechanism is named, reproduce it
   in sim (new battery entry with the RED baseline recorded), fix
   with one mechanism per change, full battery from a settled tree,
   parity rebuild (the #52 lesson), THEN rebuild/gate/flash and
   **take the #49 bench verdict**: repeatable **10000M** on port 4-3
   across POR cycles, dmesg clean (no SSP-BOS complaint), `lsusb`
   shows the device, then the Gen2 ladder (multiep_test 1 MiB ×10,
   16 ×3, 64 ×3 — sha-exact is the verdict; MB/s is adapter-capped
   and documented-degraded), with the uart1 'R' forced-recovery hook
   run during the ladder (the parked #29–#31 verdict).  If the
   verdict is clean, run the 5G-hub-port fallback row (dual-rate
   matrix run 2) while the bench is hot.
4. **Begin the full-128 PHY** (directive 1): survey gw_usb3's
   datapath units; widen bottom-up (RX/TX gearboxes, scrambler
   chain, elastic buffer) at 16 symbols/beat behind elaboration
   knobs, against the `tests/test_equiv.py` oracle-harness pattern —
   unit-by-unit equivalence fences exactly like the MAC widening.
   The proven 5G configuration stays pinned by its regression suite.
5. **The Gen1 fence intact** throughout: parity rebuild after every
   shared-file change (diffs only in the ~600–622 header date
   region vs `/tmp/kilo/h0_gen1_fence.fs`), ladder-green on
   hardware at session start.

HANDOVER continues at **§10ac**; bug numbering continues at **#53**
(#49 is open and comes first).

## Phase plan (each phase gated; one mechanism per change)

### W0 — orientation and the fence (short)

Read HANDOVER §10ab (the evidence chain), §10aa.  Re-verify the Gen1
fence on the bench (the fence image should be resident at 5000M on
4-3; run 1 MiB ×10, 16 ×3, 64 ×3, sha-exact, uart1 ch0 = 0; expect
the port-recovery runbook if the port loops).  Battery 67/67 from
the settled tree.  Parity rebuild if ANY shared file changes later.

### W1 — the instruments, sim-proven (deliverable 1)

PipeBeatCapture unit testbench red-first; the Gen2 TxWireChecker
wiring; battery from the settled tree; build + timing gate.  No
verdict weight on any build that misses its gate.

### W2 — localization and the fix (deliverables 2–3)

Instrumented PORs; H1/H2 verdict; the 12-byte-BOS build if the
length law needs the second axis; sim repro red-first; fix; battery
+ parity; rebuild; **the #49 verdict** with recorded evidence.

### W3 — the full-128 PHY begins (deliverable 4)

Bottom-up widening with equivalence fences; 5G configuration pinned.

## Parked items that stay on the books

The Gen1-rail twins of #50/#51 (verbatim-preserved; need the
intend/battery/ladder ceremony); full-rate 64-bit endpoint widening
(the Gen2 bulk MB/s targets); the reccut sweep at sub-block cut
granularity; #37 RX side (truncated inbound DPP never retried);
RX-side DPH replica-match validation [7.2.4.1.6 rule 2a]; rule-2d/
#36 positive-validation stimuli; data_tx SEND_ZLP bare-ready;
wire-checker TP blindness; SKP x=4 aligner knob; stage-B credit
scaling beyond 4+4; the Gen1-128 native serdes trim (20×1:4);
the 5G-hub-port fallback row (untested — needs the physical hub
path; the 10G root port never produced a 5G fallback enum).

## Keep the discipline that closed fifty-two findings

* Sim first; red-first for every new mechanism; the FULL battery
  (67 entries) from a SETTLED tree before each hardware build —
  never concurrent with source edits.
* Shipping parity (payload compare vs `/tmp/kilo/h0_gen1_fence.fs`)
  after EVERY shared-file change — no exceptions (#52).
* One mechanism per change; hardware ladder with recorded verdicts;
  watch uart1 ch0 on every run; never trust a single boot.
* A Gen2 build that misses ITS width's timing gate is never flashed
  for Gen2 runs.
* New findings into HANDOVER §10ac as you go; commit submodules
  first (gowin-serdes is PUBLIC — keep it clean), then the fork;
  push.

## Tooling and bench facts (verify before trusting)

* One clone: `~/Downloads/luna-ss` (github.com/key2/luna-ss, with
  submodules; `pdm install -G :all`).  Frozen archive =
  `~/Downloads/GW_USB3` (ARCHIVE.md maps it; the reference `prj.fs`
  health baseline lives there).
* **W128 BUILD REQUIREMENT**: the bundled wasm yosys dies
  `bad_alloc` on Gen2-128 RTLIL.  Build with a native yosys ≥ 0.40:
  `PATH=/tmp/kilo/oss-cad-suite/bin:$PATH AMARANTH_USE_YOSYS=system
  .venv/bin/python -u top.py` — oss-cad-suite (yosys 0.68) is
  unpacked at `/tmp/kilo/oss-cad-suite`; if /tmp was wiped,
  re-download from github.com/YosysHQ/oss-cad-suite-build releases
  (linux-x64 tarball).  Gen1 builds still fit the wasm yosys.
* **SDC**: the generated core clock targets net `core_raw_clk`
  (GowinSynthesis canonicalizes the divider's alias group to the
  domain clock net; a `core_div` pattern hard-errors TA2003/TA2004).
  Timing gate: `tools/gowin_timing_report.py <build> --section fmax`
  (also `--section tns`, `--section resources`).
* Board on 10G root port **`usb 4-3`**; 5G test path = hub at
  `4-8.x` (physical replug).  Flash: `sudo -n openFPGALoader -c
  ft232 <fs>`.  The device parks in SS.Disabled ~360 ms after boot —
  every test wants a fresh POR (reflash) against a QUIET port.
* **Port-recovery runbook (order matters)**: (1) PCI unbind/rebind
  of `0000:80:14.0`; (2) after a rebind the kernel may bind ftdi_sio
  to ALL FOUR FTDI channels — unbind the JTAG channel before
  flashing: `echo -n "3-7.3.2:1.0" | sudo tee
  /sys/bus/usb/drivers/ftdi_sio/unbind` (check the actual path; the
  JTAG is the single-channel FT232H — it WILL be rebound after any
  rebind, session 20 hit this); (3) flash the reference `prj.fs`,
  confirm 10000M; (4) only then the image under test.
* UARTs by stable path: `examples/gowin/luna-multiep/uart_capture.py
  <s> <prefix>` (tag **L = uart0**/if02 link probe: ss-cnt telltale
  0x341556x=156.25 / 0x29aaab2=125; ch1-3 = per-cause recovery
  timers/rx/tx; tag **C = uart1**/if03 pipe probe: rxclk, accepted
  RX headers, sds, ts2, txfifo-hi28).  Channel maps at the top of
  `examples/gowin/luna-enum-gen2/top.py`.  uart1 RX: 'R' = forced
  recovery (extend the same idiom for the capture trigger mux).
* Host instruments: usbmon `/sys/kernel/debug/usb/usbmon/4u`;
  **xhci ftrace** (session-20 proven decisive):
  `/sys/kernel/tracing/events/xhci-hcd/xhci_handle_transfer/enable`
  + `xhci_handle_event` — the event TRB pointer localizes the
  failing STAGE; ring math: TRB=0x10, control TD = Setup/Data/
  Status.  PORTSC tracer `/tmp/kilo/portsc_trace.py`.
* Verdicts: `multiep_test.py <MiB> --eps 1,2,3` (sudo).
* **Run sims as `.venv/bin/python -u`** (`timeout`+`pdm run` orphans
  children).  Battery: `bash sim/sim_battery.sh` (67 entries), logs
  in /tmp/kilo.  Gen2 sim knobs: `PHASE=` (train/enum/echo/u0/
  hotreset/hotreset-parked/recovery/reccut/advearly), `W128=1`
  (clear-data conditioning — the RTL scrambler round-trip is a
  64-bit surface, W64-only), `TSEQ_LEN=64` (always for phase runs),
  `NEG=nolcrd2`, `VERBOSE=1`.  reccut now sweeps dev18 AND bos50.
* Timing gates: Gen1-64 pclk ≥ 125; Gen2-128 core ≥ 78.125 AND
  pclk ≥ 156.25 AND rxclk ≥ 161.29.
* Saved images in `/tmp/kilo/`: `h0_gen1_fence.fs` (the fence,
  RESIDENT on the board), `s20_gen2_128_met.fs` (the Gen2-128 MET
  image — the #49 RED evidence vehicle), `s20_parity_run1.fs` (the
  #52 red build).  Session-20 evidence: `s20_xhci_trace.txt` (the
  status-stage localization), `s20_gen2_por1_both.txt` (uart during
  the RED window), `s20_gen2_por1_usbmon.log`, `s20_battery_v1.log`,
  `s20_reccut_bos50_*.log`.  s16 comparables: `s16_usbmon_bos.log`,
  `s16_bos_window_both.txt`.

## Constraints

* Single lane everywhere.  No x2 work, ever.
* The `gw_usb3` 5G configuration and its regression suite are
  settled — PHY-side changes go behind elaboration knobs with the
  proven configuration still pinned.
* The manufacturer's reference bitstream stays untouched; it is only
  the link-partner health baseline.  No third-party RTL is copied
  into our repositories (this includes debug IP: no LiteScope — the
  in-tree BurstEventCapture ring pattern is the template).
* BSD-3-Clause: upstream LUNA license and copyright headers stay
  intact; our commits carry our own attribution alongside.
* The shipping Gen1-64 configuration must remain buildable and
  ladder-green from every commit on main.
* gowin-serdes is PUBLIC: keep it free of anything that is not ours
  to publish.
