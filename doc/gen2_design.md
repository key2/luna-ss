# Gen2 (10 Gbps / SuperSpeedPlus) through the whole stack — design note

Phase 1 deliverable (prompt.md). Spec references are USB 3.2 Rev 1.1
(`doc/USB 3.2 Revision 1.1.pdf/markdown.md`); section numbers as
printed there. Status of every gw_usb3 block cited below: see the
module docstrings — the bit-level Gen2 machinery is equivalence-proven
against the vendor RTL and **silicon-proven** (usb31-enum enumerates
Gen2 on the bench 10G root port with our PHY + our serdes).

## 0. Scope and ground rules

* One bitstream, both rates: Gen1 (5G, 8b/10b, 32-bit @ 125 MHz) and
  Gen2 (10G, 128b/132b) with per-spec fallback. The shipping Gen1
  configuration must stay buildable and ladder-green from every
  commit; the Gen1 battery entries are the regression fence.
* Reuse, don't rewrite: gw_usb3 already implements the Gen2 bit
  level (gearboxes, scrambler, DC balance, block alignment, LFPS/SCD
  machinery). The fork adds what the vendor *link/LTSSM netlist* did:
  Gen2 ordered-set handling, packet/link-command framing, LTSSM
  substates, rate switching — in LUNA-style Amaranth we own.

## 1. Datapath width / clock plan — DECISION: (c) then (a)

Numbers: Gen2 line rate 10 Gbps; after 128b/132b overhead the symbol
payload is ~9.7 Gbps ≈ 1212 MB/s. A 32-bit datapath needs ~312 MHz —
not achievable in this fabric (GW5AT-60 C2/I1; vendor closes its own
Gen2 link at 156.25/160 MHz). The GTR12 gives the fabric **64-bit @
156.25 MHz** at 10G (raw interface), and gw_usb3's PIPE is already
64-bit (`PipeTxData/PipeRxData` In/Out(64) + PIPE 4.x block signals
in `luna/gateware/interface/pipe.py`).

**Stage A (first light, this mission's Phases 3–5): keep the 32-bit
link+protocol core, clock it at 156.25 MHz, and put per-packet 64↔32
burst buffers between it and the 64-bit Gen2 physical layer.**

* Same clock domain both sides (ss domain = pclk = 156.25 at Gen2),
  so the buffers are width converters, not CDCs.
* DPPs must be wire-contiguous [§7.2.1.2]: the TX buffer stages a
  whole packet (header + payload) at 32-bit rate, then bursts it to
  the 64-bit framer with no mid-packet bubbles; RX buffers a whole
  incoming packet at 64-bit rate and drains it at 32-bit rate.
  1116-byte max DPP → one BRAM-scale buffer each direction.
* Bandwidth: the 32-bit core at 156.25 MHz sustains ~5 Gbps payload —
  half the Gen2 wire, still ≥ the whole Gen1 rate. Protocol
  correctness, enumeration, and the entire multiep ladder are fully
  exercisable; flow control (NumP/credits) absorbs the rate mismatch
  by construction.
* Every one of the 36 bug fixes rides along untouched: the link
  layer sees exactly the word stream it sees today.

**Stage B (the honest target, after G5): width-generic link+protocol
elaborated 32-bit@125 for Gen1 and 64-bit@156.25 for Gen2.** Header
packet = 2 beats at 64-bit (today: 4 at 32-bit); CRC-16/CRC-32,
HPSTART/framing detection, scrambler interface, CTC and the RX/TX
skid stages all become width-parametric. ~1.1 GB/s runway.

Why staged: the width refactor touches the exact files that carry
the 36 fixes; doing it before a working Gen2 link exists would
entangle "new framing wrong" with "width refactor wrong". Stage A
gives a Gen2 link where the only new variables are the new
mechanisms. Contingency if 156.25 cannot be closed on the 32-bit
core's hot cones (see §5): none needed for correctness — the stage-A
core is the timing-critical piece either way, and stage B *relaxes*
per-bit logic depth at the same clock.

## 2. Framing delta table (Gen1 construct → Gen2 replacement)

| Gen1 (in `physical/`+`link/` today) | Gen2 replacement | Spec | Owner / status |
|---|---|---|---|
| 8b/10b symbols, K/D codes, 32-bit ctrl strobes | 128b/132b blocks: 4-bit header (0011 data / 1100 ctrl, 1-bit-error-correctable) + 16 symbols | §6.3.2.2/.4 | **gw_usb3 DONE** (`datapath.py` RxGearbox132/TxGearbox132), silicon-proven |
| COM-based symbol alignment (`word_alignment`) | block-header alignment; SKPEND-anchored realignment on variable-length SKP OS | §6.4.1.2.4 | **gw_usb3 DONE** (vendor-exact; carries the x=4 quirk, §6 below) |
| Gen1 scrambler X^16+X^5+X^4+X^3+1 (LUNA-side `physical/scrambling.py`) | LFSR G(X)=X^23+X^21+X^16+X^8+X^5+X^2+1, seed 1DBFBCh, LSb-first; re-init after SYNC; per-construct bypass/advance rules | §6.3.2.3 | **gw_usb3 DONE** (Gen2 scrambler in the PHY datapath). LUNA-side scrambling is bypassed at Gen2 — ownership is the PHY's, matching the vendor stack split. Verify the exact PIPE-boundary contract in Phase 4 (which constructs arrive descrambled). |
| n/a | per-TS running DC balance, symbols 14/15 → DFh/F7h / 20h/08h; receivers ignore sym 14/15 | §6.4.1.2.2 | **gw_usb3 DONE** (`dc_balance.py`, `tables.py`) |
| TSEQ ×65,536 (8b/10b) | TSEQ block (87h×… layout) ×**524,288**; SYNC every 16,384; SKP ≤ 1/128 TSEQ | §7.5.4.7, Table 6-9 | fork: LTSSM counts + OS generator tables (encodings from gw_usb3 `tables.py`) |
| TS1/TS2 4-symbol ordered sets, K28.5 based | TS1 (1Eh)/TS2 (2Dh) 16-symbol blocks; sym 5 = link functionality; sym 1–13 scrambled; sym 14/15 excluded from match; **SYNC every 32 TS** | Tables 6-7/6-8, §6.4.1.2.1 | fork: new block-level TS gen/detect (replaces `link/ordered_sets.py` TSTransceiver at Gen2) |
| n/a | SYNC OS (even 00h / odd FFh, bypass, LFSR re-init after last symbol; also polarity detect) | Table 6-10 | fork: generate per cadence rules; PHY consumes for aligner/scrambler sync — verify split in Phase 4 |
| n/a | SDS (E1h×4 + 55h×12): sent once in Polling.Idle / Recovery.Idle / HotReset.Exit before the first data block | Table 6-11, §6.4.1.2.2 | fork: LTSSM-driven; marks OS-stream → data-stream transition |
| CTC SKP: K28.1 pairs, avg 1/354 symbols (`physical/ctc.py`) | SKP OS control block: TX always 24 symbols (20×CCh + 33h SKPEND + 3 LFSR-state symbols); **average 1 per 40 blocks**, Z=int(Y/40)∈{0,1,2} inserted only at block boundaries after SYNC/TS/SDS/packet/idle; RX legal range 4–36 SKP symbols in ×4 steps; elastic buffer must absorb 11 symbols (Gen1: 8) | §6.4.3.3, Table 6-13 | split: PHY owns RX SKP strip/elastic buffer (proven); fork owns TX SKP scheduling at block granularity (new, replaces CTC inserter at Gen2) |
| HPSTART = K27.7×3+EPF; SDP/END/EDB/SLC K-codes | scrambled data-symbol framing: SHP=9Ah, **DPHP=95h (new)**, SDP=96h, END=65h, EDB=69h, SLC=4Bh, EPF=36h. HPSTART=3×SHP+EPF; **DPHSTART=3×DPHP+EPF** (non-deferred DPH only); DPPSTART=3×SDP+EPF; DPPEND=3×END+EPF; DPPABORT=3×EDB+EPF; LCSTART=3×SLC+EPF; ≤1 corrupted symbol tolerated | Table 6-2, §7.2.1.1.1/.2.1, §7.3.3 | fork: new Gen2 packet/link-command framers + detectors in `physical/`+`link/` |
| logical idle = D0.0 scrambled | Idle Symbols inside data blocks (post-SDS) | §7.1.2 | fork (trivially width-adapted) |

### Link-layer deltas that are NOT just framing (found in spec review;
### they narrow the "protocol untouched" assumption and are the main
### scope risk to track)

* **Header sequence numbers go modulo-16** at SSP: Link Control Word
  carries a 4-bit sequence number (SS: 3-bit), LGOOD_0…15
  [§7.2.1.1.3, Table 7-4]. `link/transmitter.py`/`receiver.py`
  sequence arithmetic and the recovery advertisement (#29/#31 fixes)
  get a rate-selected modulus. Mechanical, but touches conformance-
  sensitive code — the Gen2 sim must cover the wrap and the
  advertisement at both moduli.
* **Credit classes split**: SSP replaces LCRD_A–D with **LCRD1_x**
  (Type-1: TPs, LMPs, ITPs, periodic DPs) and **LCRD2_x** (Type-2:
  asynchronous DPs), each 4 deep at Gen2x1 [Table 7-4, §7.2.4.1.x].
  RX buffer accounting, the credit re-advertisement (rule-2d work),
  and TX gating by credit class follow. For a bulk-only device all
  our DPs are Type-2 and everything else is Type-1 — both pools must
  exist and both advertisements must be correct after recovery.
* **Non-deferred Gen2 DPH carries a length-field replica** right
  after the Link Control Word (single-bit-error tolerance for the
  DPP boundary); deferred DPHs use HPSTART without replica; RX may
  use the replica to ride out a bad-CRC DPH [§7.2.1.1, lines around
  5220]. TX: emit replica; RX: ignore for validity, optionally use.
* **DPPABORT semantics**: Gen2 preserves the DPP boundary per the
  DPH length even for partially nullified DPPs [§7.2.1.2.1] —
  relevant to #37's class (truncated inbound DPP): at Gen2 the
  receiver can always resynchronize to the declared length.
* Link command single-bit tolerance: a link command is valid if one
  of the two 16-bit words passes CRC-5 [§7.3.4].
* tDPHResponse tightens to <1610 ns at Gen2x1; tGen2MaxBurstInterval
  = 50 ns between bursted DPs (EOB rules already handle the
  can't-sustain case after #34).

## 3. LTSSM delta

New/changed states (device = peripheral port; §7.5.4):

```
Polling.LFPS ── SCD1 exchange ──► Polling.LFPSPlus ── SCD2 ──►
Polling.PortMatch ── PHY Capability LBPMs (RATE SELECTION) ──►
Polling.PortConfig ── PHY reconfig + PHY Ready LBPMs ──►
Polling.RxEQ (TSEQ ×524288) ──► Polling.Active (TS1) ──►
Polling.Configuration (TS2) ──► Polling.Idle (SDS → Idle) ──► U0
```

* **SCD1/SCD2** [§6.9.4]: information lives in the Polling.LFPS
  burst *repeat period*: tRepeat 6–9 µs = '0', 11–14 µs = '1'
  (9–11 µs guard). SCD1='0010', SCD2='1101', LSb first, back-to-back,
  terminated by an extra tBurst + EI ≥ 2×tRepeat(max). The PHY's
  LFPS burst engine already shapes bursts; the LTSSM gains a tRepeat
  modulator. gw_usb3 already performs SCD/rate-change interop even
  with `gen2=False` (§10a) — mine `pipe_interface.py`/`lfps.py` for
  the burst/repeat plumbing before writing anything new.
* **Gen1 fallback** (the §10d matrix, now per spec):
  - Polling.LFPS: no SCD1/SCD2 seen + ≥16 consecutive legacy bursts
    (before tPollingSCDLFPSTimeout=60 µs) → switch to SS operation
    after ≥4 SCD1 sent, non-varying tRepeat; or SCD timeout → SS →
    Polling.RxEQ [§7.5.4.3].
  - Polling.LFPSPlus: 20 non-varying bursts transmitted after no
    SCD2, or no SCD2 within 64 received bursts → revert to
    non-varying / SS path [§7.5.4.4].
  - **Speed-fallback loop**: at Gen2, Polling.Active/Configuration/
    Idle timeouts (12/12/2 ms) return to **Polling.PortMatch**, where
    the port advertises its *next highest* capability — this, not
    Polling re-entry, is how 10G→5G downgrade happens after failed
    Gen2 training [§7.5.4.5.2].
  - **Forced-Gen1 build knob**: never emit SCD1 (plain non-varying
    Polling.LFPS) → link partner sees a Gen1 device; LTSSM skips
    LFPSPlus/PortMatch/PortConfig. This is elaboration-time and
    cheap; it is also the fallback matrix's control build.
* **LBPM** [§6.9.5, §7.5.4.5/.6]: byte messages, LSb first, PWM
  encoded: tPWM=2–2.4 µs; '0' = 1/3 LFPS + 2/3 EI, '1' = 2/3 LFPS +
  1/3 EI; delimiter = 1 tPWM LFPS + 1 tPWM EI, framing starts/ends
  with delimiters. PHY Capability LBPM: [1:0]=00, [3:2]=rate
  (00=5G, 01=10G), b6=lane count. PHY Ready LBPM: [1:0]=01. Match
  rule: send 4 matched after receiving 2 matched; 12 ms
  tPollingLBPMLFPSTimeout shared across PortMatch+PortConfig;
  timeout at a peripheral → eSS.Disabled.
  Implementation: an LFPS PWM modem (TX shaping + RX pulse-width
  classifier) beside the existing LFPS burst detector; the RxElecIdle
  mux path that already feeds LUNA's LFPS detector carries the RX
  side.
* **Rate switch execution — Polling.PortConfig**: the serdes CSR
  rate machinery (10G→5G on Gen1 link-up, both examples, plus the
  adapter's boot_rate_switch) becomes **LTSSM-driven and
  bidirectional**: boot at 10G trim (unchanged); PortMatch outcome
  10G → stay; outcome 5G (or forced-Gen1/SCD fallback) → CSR switch
  to 5G exactly as today. Re-entry to PortMatch after a failed Gen2
  training downgrades → CSR switch 10G→5G mid-LTSSM; a subsequent
  warm reset / Rx.Detect cycle may need 5G→10G — the CSR sequencer
  already supports both directions (rate_change_table), the adapter
  grows a `rate_select` input + `rate_done` handshake and the PHY's
  PIPE `rate` plumbing replaces the tied-0 in the adapter. TX
  electrical idle is allowed during reconfig [§7.5.4.6]; PHY-ready
  gating reuses the boot-window discipline (#22) so no LUNA state
  clocks through the retune.
* **Recovery at Gen2** [§7.5.10]: TS1/TS2 as blocks, SYNC every 32,
  sym-14/15 exclusion, block re-alignment + scrambler re-sync in
  Recovery.Active, single SDS in Recovery.Idle before Idle symbols.
  No PortMatch fallback from Recovery (timeouts → eSS.Inactive).
  The #29–#31/#36/rule-2d recovery work carries over; the
  advertisement moves to modulo-16 + LCRD1/LCRD2 (see §2). Recovery
  matters MORE at Gen2 bring-up — the parked forced-recovery harness
  (#37, feed truncation) should be finished against Gen1 first, then
  ported into the Gen2 sim.
* **Polling.Idle / U0 entry**: exit to U0 = 8 consecutive Idle
  symbols received + 16 sent after receiving one (same shape as
  today); scrambling-disable (TS2 bit) takes effect after SDS.

## 4. PIPE boundary at Gen2 (who does what)

Matching the proven vendor split (vendor link netlist ↔ our PHY):

* **PHY (gw_usb3, proven)**: serdes 64-bit raw attach, Tx/RxGearbox132
  (block header insert/extract), Gen2 scrambler/descrambler, DC
  balance, block alignment (SKPEND tracking), RX SKP strip + elastic
  buffer, LFPS burst shaping, CSR/rate sequencing, rx-detect.
* **Fork (LUNA side, new RTL)**: block-level ordered-set generate/
  detect (TSEQ/TS1/TS2/SYNC/SDS as 16-symbol payloads over the
  64-bit PIPE with `tx/rx_sync_header`/`start_block`), TX SKP OS
  scheduling (40-block average), Gen2 packet/link-command framers
  and detectors (Table 6-2 symbols), LBPM modem, LTSSM substates,
  rate-switch orchestration, dual-rate muxing between the existing
  Gen1 path and the new Gen2 path.
* Phase-4 verification item: confirm on the equivalence harness
  exactly which constructs cross the PIPE descrambled and where SYNC
  is consumed vs forwarded; the vendor stack is the oracle (drive
  the netlist link layer and our PHY side by side — the hybrid rig
  methodology, in sim).

## 5. Timing budget

At Gen2 the **156.25 MHz ss/pclk domain is an operating requirement**
(not #22's benign boot window). Current facts:

* luna-enum-sized builds have hit 156.3 MHz Fmax; full multiep
  builds roll 107–149 MHz (placement lottery; the 66_0xx POR-nudge
  reroll is the documented first response — session-11 note: the
  first fork build rolled 107.4 and rerolled).
* Known hot cones from the fmax reports: endpoint-mux grant/kind
  locking, tp_generator FSM enables, get_descriptor ROM muxes,
  aligner/CTC payload paths, LTSSM timeout comparators (already
  registered once).
* Plan: (1) stage-A keeps the core logic identical, so the gap to
  close is the SAME cones from 125 to 156.25 — expect #22-class
  targeted register stages (grant/kind pipelining, descriptor ROM
  output registers, handshake decode stages — several already exist
  as idioms in the tree); (2) placement lottery per build; (3) the
  validated Yosys pre-lowering flow (§10k addendum) as escalation;
  (4) the StreamArbiter hardening idiom for any NEW arbitration
  cones (mandatory — GowinSynthesis miscompile history).
* Gate discipline: Phase 5 rung 1 is "Gen2 clock MET" before any
  bench protocol work; a build that misses 156.25 is not flashed
  for Gen2 runs.

## 6. Vendor aligner SKP quirk (x=4) — workaround plan

Locked-in finding (tests/test_link_layer_spec.py,
`test_td_6_2_gen2_skp_x4_vendor_gap`): the vendor Gen2 block aligner
— and our port, quirk-for-quirk — mis-tracks a received SKP OS with
exactly 4 SKP symbols; 8–36 are fine. Per §6.4.3.3 a received SKP OS
is 4–36 SKP symbols in multiples of 4, so x=4 is legal RX input.

* Exposure: x=4 requires four cumulative 4-symbol removals from the
  nominal 20 — only produced by chains of re-timers; the bench 10G
  root port is direct-attached. Low bench risk, real conformance gap.
* Plan: fix the SKPEND-anchored length tracking in our aligner
  behind an elaboration knob (`skp_x4_fix=True` in the fork's
  examples; default False keeps the vendor-exact configuration the
  equivalence suite pins). Add a TD.6.2 x=4 PASS test for the fixed
  trim next to the vendor-gap guard. Do this when `word_alignment`/
  datapath files are open in Phase 4, not before.
* TX side: we always emit the nominal 24-symbol SKP OS (spec
  requires it), so we cannot tickle the same class of bug in the
  host.

## 7. Enumeration surface (Phase 5 exit criteria)

* bcdUSB 0310h; BOS + **SuperSpeedPlus USB Device Capability**
  descriptor (SSAC≥1; sublink speed attrs: LSE=3/LSM=10 for 10 Gb/s,
  LP=1) [§9.6.2.5]; SS Endpoint Companion unchanged for bulk
  (bMaxBurst as today; 1024-byte MPS).
* **Sublink Speed Device Notification TPs** on entering Address
  state when operating SSP [§8.5.6.7] — new small TP source in the
  protocol layer, LTSSM/state driven.
* lsusb shows 10000M; the multiep ladder then runs unchanged
  (BURST=2 engines are rate-agnostic above the link layer).

## 8. Phase-2 sim shape (gate G2 requirements)

Extend the proven link-partner methodology, real coding chain at
both rates:

* Host model grows a Gen2 personality: SCD1/SCD2 tRepeat scripting,
  LBPM PWM exchange, 128b/132b block generation with the REAL Gen2
  scrambler (reuse gw_usb3's Python models / equivalence-suite
  vectors as the encoding oracle), TSEQ/TS1/TS2/SYNC/SDS cadences,
  Gen2 SKP insertion (including x=4 stimulus), Table 6-2 framing,
  modulo-16 LGOOD + LCRD1/LCRD2 credit model.
* Red/green pair: the sim must FAIL against the unmodified fork
  (records the red run) and turn green phase by phase (G3: training
  to U0 + fallback scripts; G4: enumeration + bulk echo).
* Every existing Gen1 battery entry stays untouched and green; the
  battery gains a `gen2` section.

## 9. Open questions carried into Phase 2/3

1. PIPE contract details at Gen2 (descrambling/SYNC ownership) — to
   be pinned by an equivalence-style sim against the vendor link
   netlist before the fork framers are written (§4).
2. LCRD1/LCRD2 buffer partitioning: 4+4 vs shared-with-typing; pick
   after reading §7.2.4.1.x credit rules against the current
   receiver buffer implementation.
3. Whether Polling.RxEQ's 524,288-TSEQ burst needs a sim-shortening
   parameter plumbed like `tseq_burst_length` (yes, almost surely —
   same idiom).
4. Stage-A burst-buffer sizing (1 max-DPP each way vs 2× for
   overlap) — decide from the Gen2 sim's throughput trace, not
   guesswork.
