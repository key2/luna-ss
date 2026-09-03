# USB 3.2 unified stack design — dual rate × dual lane × width-generic

**This document merges and supersedes `gen2_design.md` (the Gen 2x1
stage-A design note, gates G0–G4 executed against it) and
`gen1x2_design.md` (the Gen 1x2 / width study).  Decision recorded here:
we do them TOGETHER —**

* **LUNA becomes width-generic: `core_width ∈ {32, 64, 128}`** at core
  initiation.  The historical 32-bit core survives only as the frozen
  Gen 1x1 shipping fence; all forward work happens on the wide core.
* **The PHY (gw_usb3) moves to a width-selectable PIPE: `{64, 128}`**.
  The 32-bit PIPE retires from the forward architecture ("32 is too slow
  anyway") — it remains in the tree solely for the frozen legacy build.
* **The PHY must present BOTH 64- and 128-bit PIPE for Gen 1x1, Gen 1x2
  and Gen 2x1.  Gen 2x2 is 128-only at the PIPE by physics** (19.4 Gb/s
  payload over 64 bits would need 312.5 MHz fabric).

Spec references are USB 3.2 R1.1 (`doc/USB 3.2 Revision 1.1.pdf/
markdown.md`) and the R1.1-vs-R1.0 redline (`GW_USB3/docs/USB 3.2
Revision 1.1 Redline against 3.2 R1.0.pdf/markdown.md`).  Measured
timing/bench facts are session-13 state (HANDOVER §10s).

**SCOPE UPDATE (session 15/16, BINDING — HANDOVER §10u): Gen 1x2 and
all x2 work are DROPPED from scope permanently** (port 4-3 is
Gen 2x1-highest; neither the bench xHCI nor TB4 hosts negotiate x2).
The x2 sections below (§3.2, the x2 rows of §1/§3.3/§7, §5's x2 arms,
Gen 2x2 prep) are retained as reference/negotiation-matrix history
only; the gen1x2 example top and `ssp_capability` surface stay in the
tree untouched.  The executable program is now **§13 — the single-lane
width program** (session-16 mission), which supersedes the §11 phasing.

---

## 1. The target matrix (the master table)

Payload rates: one Gen 1 lane = 4.0 Gb/s (8b10b), one Gen 2 lane
≈ 9.697 Gb/s (128b/132b).  Legality rule, asserted at elaboration:
`width_bits × pclk ≥ payload_rate` at a closable pclk.

| Config | Payload | PIPE 64-bit | PIPE 128-bit | 32-bit (legacy only) |
|--------|---------|-------------|--------------|----------------------|
| Gen 1x1 | 4.0 G | **62.5 MHz** native trim (P0 experiment) or 125 MHz duty-cycled | 31.25 MHz (bridged) or 62.5 duty-cycled | 125 MHz — the frozen fence |
| Gen 1x2 | 8.0 G | **125 MHz** (2 lanes × 4 sym merged) | **62.5 MHz** (2 lanes × 8 sym, 1:4 trim) | — |
| Gen 2x1 | 9.7 G | **156.25 MHz** (proven, lottery-class) | **78.125 MHz** (1:4 trim experiment or 2:1 bridge) | — |
| Gen 2x2 | 19.4 G | — impossible | **156.25 MHz** (2 lanes × 64 merged) — the hard cell | — |

Negotiated-capability legality per core width (elaboration assert):

| Advertised highest | width 32 | width 64 | width 128 |
|--------------------|:--:|:--:|:--:|
| Gen 1x1 | ✔ (fence) | ✔ | ✔ |
| Gen 1x2 | ✗ | ✔ | ✔ |
| Gen 2x1 | ✗ | ✔ | ✔ |
| Gen 2x2 | ✗ | ✗ | ✔ |

**Negotiation reality** [Table 7-13/7-14/7-15]: capabilities rank
Gen 2x2 > Gen 2x1 > Gen 1x2 > Gen 1x1, but a Gen 2x1-highest port falls
back **directly to Gen 1x1** ("its next advertised PHY capability shall
be Gen 1x1"); only a Gen 2x2-highest port walks the full four-step
ladder.  Consequences:

* Gen 1x2 and Gen 2x1 are ALTERNATIVE advertised-highest configs — a
  build/boot knob selects; no conformant single image tries 10G-x1 then
  5G-x2.
* A future Gen 2x2-highest build is the only one that exercises every
  row in one image — and the width-generic architecture is exactly what
  makes it reachable (128-bit core, both lanes: the quad has the lanes,
  and the bench host is Gen 2x2-capable — usb4 root hub reports
  `speed 20000`, `rx_lanes = tx_lanes = 2`, verified 2026-09-01).
* Every fallback terminates in Gen 1x1 → **the wide core MUST run
  Gen 1x1 traffic regardless** (see §4.1 duty-cycling); Gen 1x1-on-wide
  is not an option, it is the fallback mode.

## 2. Architecture (layer stack)

```
 GTR12 Quad 0                      straight: lane0=LN1, lane1=LN0
 ┌ LN1 ─ per-lane datapath ┐       (flipped orientation swaps; lane-0
 │  (vendor-exact, native  │        crossbar; Configuration Lane = lane 0)
 │   width per rate trim)  │
 └ LN0 ─ per-lane datapath ┘
        │        │
   [x2 stripe / deskew / merge]     ours alone; byte-granular [6.13.4]
        │
   [width normalization]            native fabric width → PIPE width;
        │                           duty-cycled or bridged (§3.3)
   PIPE {64, 128}                   one contract, width-parametric
        │
   width-generic LUNA core          core_width ∈ {32, 64, 128}
   (link + protocol + endpoints)    32 = frozen legacy elaboration
```

Ground rules carried from the Gen 2 program (proven through G0–G4 and
the session-13 silicon work):

* Reuse, don't rewrite, the **bit level**: gw_usb3's per-lane machinery
  (8b10b, Gen 2 gearboxes/scrambler/DC-balance/alignment, elastic
  buffers, LFPS/SCD, CSR rate sequencing) is equivalence-pinned against
  the vendor RTL and silicon-proven — it stays vendor-exact at its
  native widths.  Width and lanes are layered AROUND it.
* The Gen 1x1 shipping configuration stays buildable and ladder-green
  from every commit (payload-identity discipline on the frozen core).
* One mechanism per change; sim-first with STRICT host models — the
  session-13 lesson written in blood twice (#39, #40): forgiving bench
  models are where silicon bugs hide.

## 3. The PHY plan (gw_usb3 + gowin-serdes)

### 3.1 Fabric trims (what the GTR12 gives us natively)

Per-lane fabric width is a UPAR-reconfigurable trim —
`width_mode ∈ {8,10,16,20,32,40,64}` × `gear ∈ {1:1,1:2,1:4}`
(gowin-serdes `csr_map.py`), and the vendor rate tables ALREADY flip it
at runtime (`recfg_width_mode_1..4` switch 16×1:4 ↔ 20×1:2 during every
10G↔5G change).  Extending the trim tables is mechanism we own:

| Rate | Proven trim | Wide-trim candidates (P0 experiments) |
|------|-------------|----------------------------------------|
| 5G  | 20×1:2 → 4 sym @ 125 | 20×1:4 → 8 sym @ **62.5** |
| 10G | 16×1:4 → 64-bit @ 156.25 | 32×1:4 → 128-bit @ **78.125** |

**P0 verdicts (session 14, 2026-09-01; HANDOVER §10t):**

* **5G 20×1:4 EXISTS and RUNS ON SILICON**: the vendor CSR tool
  accepts it; the boot blob differs from the proven 20×1:2 trim in
  exactly two lane clock-tree divider registers (LN1: `0x808608`
  111A→121A, `0x808628` 116→126 — the gearbox register keeps its
  `0x511`); the `probe-trims` rig measured **pclk = 62.500 MHz**
  (counter 0x14d555e) with the CSR boot completing.  RX-side symbol
  delivery at the wide trim rides the W1 integration milestone.
* **10G 32×1:4 IS IMPOSSIBLE on the GW5AT-60**: the vendor tool's
  width table has no entry >20 (`KeyError: 32`; 40 and 64 likewise) —
  consistent with the fixed 80-bit TX / 88-bit RX fabric bus (128
  bits cannot be presented).  The `width_mode ∈ {8,10,16,20,32,40,64}`
  set in csr_map.py is the TOML schema, not this device.  **Gen 2x1 →
  128-bit PIPE is therefore the 2:1 bridge (the "safe hybrid" below),
  full stop**; Gen 2x2 → 128 = stripe-merge of 2×64 is unaffected.

Where a native wide trim does not exist or does not prove out, the
width-normalization layer covers the gap (§3.3).  Trim changes at
runtime inherit the **#22 boot-window discipline** (quiesce/park the MAC
across the retune); the rule stays *width follows the negotiated
configuration* — one trim per (rate × lanes × PIPE width), flipped
inside Polling.PortConfig/SpeedSwitch, no independent width state
machine.

### 3.2 The dual-lane (x2) layer — new, ours alone

Both Type-C SS pairs already land on Quad 0 (straight: lane 0 =
Configuration Lane = LN1; flipped: LN0 — bug #38 proved LN0 CSR + RX on
silicon; **LN0 TX is the remaining bring-up**).  Requirements inventory
(USB 3.2 §6.13 + R1.1 redline refinements):

| Rule | Ref |
|------|-----|
| Lane 0 = Configuration Lane; ALL LFPS (SCD/LBPM/Ping/WarmReset/Ux-exit) and receiver detect on lane 0 only; lane 1 silent until PortConfig selects x2 | 6.13.1/.3/.10/.12 |
| Byte-granular data striping aligned to lane 0; packets/LCs may START on either lane; control OS duplicated on both lanes, never striped | 6.13.4 |
| Ordered sets transmitted simultaneously on both lanes; TS handshakes complete on ALL lanes before state advance; TS1 on ANY lane in U0 → Recovery on ALL | 6.13.6 |
| Per-lane scrambler seeds: Gen 1 lane0 `FFFFh` / lane1 `8000h`; Gen 2 lane0 `1DBFBCh` / lane1 `0607BBh` | 6.13.5 |
| Per-lane SKP compensation (each elastic buffer independent); TX SKP simultaneous on both lanes, idle padding (≤8 symbols, R1.1 allowance) for odd DP tails | 6.4.3.1/.2, 6.13.6 |
| Per-lane polarity detect/correct | 6.13.7 |
| RX lane-to-lane deskew ≤ 6.4 ns at Rx Si input (≈3.2 symbols @5G); datum = simultaneous OS boundaries (TS/SKP at Gen 1 — no SDS; SDS at Gen 2); complete by training end | 6.13.8, Table 6-34, 7.5.4.8.1 |
| x2 timers: Polling.Active 24 ms; per-lane exit conditions; the early lane keeps transmitting TS | 7.5.4.8.1 (R1.1) |
| PHY Ready LBPM in x2 carries re-timer presence / DFP RT-Config (bit-7); as UFP we answer b7=0 and must tolerate a DFP RT-Config phase | 7.5.4.5.1, Table 7-13 |

New modules (no vendor netlist exists for any of this — oracle + strict
sim fences only, red-first): the **striper/unstriper** (byte interleave
aligned to lane 0; duplicate-and-verify for control OS; simultaneous SKP
with idle-padding), the **deskew buffer** (per-lane 8-symbol FIFO,
acquire on OS boundaries, maintain across SKPs), the **lane-0 crossbar**
(logical↔physical swap for orientation; phase 1 pins straight), and the
per-lane seed parameterization.  All of it is byte-lane construction —
naturally width-generic.

### 3.3 Width normalization → the {64,128} PIPE

The per-lane datapaths keep their native widths (vendor-exactness ends
where widths change); a normalization stage presents the selected PIPE
width:

| Config → PIPE | Mechanism |
|---------------|-----------|
| Gen 1x1 → 64  | native 8-sym trim @ 62.5 (if P0 proves it) **or** accumulate 2×32 @ 125 → full beats with `valid` gaps (duty-cycled) |
| Gen 1x1 → 128 | 2:1 bridge from the 64 presentation @ 31.25, or duty-cycled @ 62.5 |
| Gen 1x2 → 64  | stripe-merge 2×(4 sym @ 125) — native, full-rate |
| Gen 1x2 → 128 | stripe-merge 2×(8 sym @ 62.5) — native if the 1:4 trim proves |
| Gen 2x1 → 64  | today's proven path @ 156.25 |
| Gen 2x1 → 128 | ~~32×1:4 fabric trim @ 78.125~~ (P0 verdict: does not exist on this device) → **the safe hybrid: keep the pinned 64-bit datapath @ 156.25 + a 2:1 PIPE bridge to 128 @ 78.125** (only the shallow bridge lives at 156.25) |
| Gen 2x2 → 128 | stripe-merge 2×(64 @ 156.25) — the hard timing cell |

Duty-cycled presentations are full-width beats with `valid` gaps (RX)
and `ready` throttling (TX) — never partial beats.  RX accumulates to
full beats; TX drains full beats at the wire's pace.

### 3.4 PHY items carried unchanged from the Gen 2 note

* **PIPE beat contract** (pinned by the oracle sim, session 11c): symbol
  0 rides bits [56:64] (big-endian symbol packing); a 132-bit block = 2
  beats at 64-bit (SKP OS = 3).  At 128-bit **one beat = one whole block
  payload** (128 = 132−4) — the block assembly machinery collapses; the
  scrambler-lane rules (TS first-word sym-0 raw; SDS bypass-advance;
  SYNC reset; SKP freeze+splice, seed = frozen LFSR state, bit 23 =
  ~bit 22; RxGearbox132 extracts the seed onto `descrambler_init`) are
  width-independent facts of the block layer.
* **TX SKP scheduling**: average 1 per 40 blocks, whole 24-symbol OS,
  **never inside a packet** (bug #40: `pkt_in_flight` deferral, gap
  counter saturates at 2× interval — the strict-host fence enforces it).
  At Gen 1 the historical 1-per-354-symbols CTC rule applies per lane;
  in x2 the per-lane elastic buffers do removal BELOW the merge point —
  the merged stream never carries SKPs.
* **TX beat pacing** (Gen 2): 64-bit @ 156.25 supplies exactly 10.0 Gb/s
  against the wire's 128/132 — one dead beat per 16 blocks (32+1 = 33
  cycles), FIFO-model-fenced.  At 128-bit @ 78.125 the exact ratio is
  the same 32-data+1-gap per 33 beats (32 blocks = 422.4 ns wire = 33 ×
  12.8 ns).  Re-derive and re-pin `tests/test_gen2_pacing.py` per width;
  TxFifoWrNum thresholds and probe channels scale with beat size.
* **`LTSSM_is_Training` is a real LTSSM output** (`ltssm.in_training`,
  bug #39): the PHY's Gen 2 polarity acquisition random-walks on
  scrambled idle if the flag stays high at U0 — never approximate it.
  In x2, polarity is per-lane [6.13.7]: the flag fans to both lanes.
* **Vendor aligner SKP x=4 quirk**: our port mis-tracks a legal 4-symbol
  received SKP OS, quirk-for-quirk with the vendor (locked-in finding,
  `test_td_6_2_gen2_skp_x4_vendor_gap`).  Exposure needs re-timer
  chains; fix behind `skp_x4_fix=True` when the aligner is re-opened for
  the 128-bit work, vendor-exact default pinned.  x2 note: re-timers ARE
  first-class in x2 topologies (PHY Ready announcements) — the quirk's
  exposure grows; schedule the fix with the x2 aligner work.

## 4. The LUNA plan (width-generic core)

### 4.1 The clocking decision: scaled clock for the designed-for config, duty-cycling as the mandatory fallback mode

Running a wide core under a narrower negotiated config forces the one
real architectural choice:

* **(a) duty-cycling** — pclk stays the PHY trim clock; full beats with
  `valid` gaps / `ready` throttling.  No new clocks, no CDC; no timing
  relief.
* **(b) scaled clock** — full-rate beats at the table-1 frequency;
  maximal timing relief; more trims/bridges and #22 windows.

**Decision: (b) for the config a build is designed for, (a) mandatory
everywhere.**  The fallback matrix forces (a) regardless: every
capability falls back to Gen 1x1, where the wide core runs duty-cycled
on the 5G trim (retuning pclk mid-fallback would add a #22-class hazard
for a rate that needs no relief).  Once gap/throttle tolerance exists,
Gen 1x1-on-64/128 costs nothing — and it is the **integration vehicle**
(§7 phasing): the wide stack is first proven at Gen 1x1, the known-good
protocol, at forgiving clocks, on the bench.

This collapses the dual-chain architecture: today's dual-rate build
elaborates the full historical 32-bit Gen 1 chain NEXT TO the Gen 2
machinery and muxes the seams (stage A).  One gap-tolerant wide core
serves all negotiated configs of a build from one datapath — a large
area/congestion win precisely where the 6.4 ns placement lottery hurt
(session 13 fought it at 28 % utilization dominated by doubled chains).

### 4.2 Stream contract

The 32-bit `USBRawSuperSpeedStream` generalizes to:

```
data  : W bits          ctrl : W/8 bits   # per-byte K flag (Gen 1 dialect)
valid : 1               # beat-granular; gaps legal ANYWHERE on RX
len   : ⌈log2(W/8)⌉+1   # valid bytes in a construct's FINAL beat
first : 1  + offs : ⌈log2(W/8)⌉   # construct start position in the beat
```

* **RX normalizes early**: one barrel-rotate front-end per receiver
  class aligns constructs to offset 0 before the FSMs — the session-13
  gen2 bulk/boundary engine shape (aligned bulk beats + a one-symbol
  boundary walker), proven at the hardest clock in the matrix.  Behind
  it, FSMs see aligned full-or-tail beats only.
* **TX pads instead of packs**: construct starts align to beat
  boundaries with logical-idle fill between constructs (legal in both
  dialects; costs only inter-packet bandwidth, bounded by credit/
  turnaround overheads).  DPP payload bodies stream full beats
  (mid-packet idle is illegal — the endpoint buffer's job, already
  proven at 32-bit).  A dense multi-construct packer is a later,
  isolated optimization.  RX must nonetheless accept dense beats
  (real hosts pack: at 128-bit one beat can carry
  `[LGOOD][LCRD][HPSTART dw0…]`).

### 4.3 Module inventory

| Module class | Width-generic form | Effort |
|---|---|---|
| LTSSM, timers, LFPS/LBPM, power mgmt | untouched — control + time; timers already parameterize by `ss_clock_frequency` (G3 work) | none |
| OS detect/emit (TS/TSEQ/SYNC/SDS) | position-muxed compares; at 128-bit a whole TS/block fits one beat — detect gets EASIER | S |
| Header RX/TX | barrel front-end + N-DW/beat capture; CRC-16 over ≤12 bytes/beat combinational | M |
| Data RX/TX | parallel CRC-32 with byte-enable tails (1..W/8 B/cycle); the gen2-gated valid-tolerance (`CHECK_CRC32`) generalizes | M |
| Link commands | at ≥64-bit an LC fits one beat: single-shot compare/emit; RX accepts multiple LCs/beat | M |
| Idle handshake | N-byte window, valid-gated (already gap-aware) | S |
| Protocol layer, endpoint mux, TP gen | width-parametric plumbing | M |
| Endpoint FIFOs / multiep DMA | widen (BSRAM aspect ratios support ×4) | M |
| Gen 2 block engines | at 128-bit they SHRINK (beat = block payload; queue halves; same pacing ratio) | S |
| SSP link-layer mechanics (modulo-16 sequence numbers, LCRD1/LCRD2 credit classes, DPH length replica, DPPABORT boundary preservation, tDPHResponse <1610 ns) | DONE at Gen 2 (G3/G4); carry into the wide core as rate-selected behavior — Gen 1x2 is SSP too and uses the SAME SSP link rules over the Gen 1 dialect framing: verify mod-16 + credit classes against §7.2.4.1.x for Gen 1x2 during P2 sim work | M (verify) |
| x2 striper/deskew | naturally width-generic (byte-lane construct), lives PHY-side | §3.2 |

The historical 32-bit core is NOT parameterized — it stays frozen as the
Gen 1x1 shipping fence (payload-identity discipline; battery + parity +
hardware re-laddering costs for zero gain otherwise).  The wide core is
new RTL sharing the protocol semantics and the 40-bug lesson corpus.

## 5. LTSSM & negotiation (merged status)

The Gen 2 LTSSM delta from the original note is **implemented and
sim-closed** (G3): SCD1/SCD2 tRepeat signaling, LBPM PWM modem,
PortMatch/PortConfig with the capability rank/fallback rules,
LTSSM-driven bidirectional rate switch (CSR sequencer + `rate_select`/
`rate_done`, boot-window discipline), Gen 2 Recovery, SDS/idle U0 entry
— plus the session-13 silicon fixes (#39 `in_training`, #40 SKP-in-
packet).  What the unified program ADDS:

* **Capability set plumbing**: `LBPM_CAP_GEN1X2 = 0x40` (b6 dual-lane,
  rate 00 — **corrected**: earlier drafts and the session-14 mission
  text said 0x20, but 0x20 is b5, a RESERVED bit; Table 7-13's b0..b7
  columns put dual-lane at b6) next to `GEN2X1 = 0x04`; the
  advertised-highest knob (`ssp_capability`, landed session 14 with
  the `phy_boots_gen2` boot-trim init); the rank/fallback arms per §1
  (Gen 1x2 → Gen 1x1; Gen 2x2 → the full ladder when we get there).
* **x2 LTSSM arms** (gen-x2-gated, x1 elaborations verbatim): 24 ms
  Polling.Active timer; per-lane TS-detect inputs with both-lanes exit
  conditions (early lane keeps transmitting TS); PortConfig applies to
  all lanes; TS1-on-any-lane → Recovery-on-all; per-lane loopback;
  PHY Ready x2 fields (UFP b7=0, tolerate DFP RT-Config).
* Config-Lane discipline: LFPS/LBPM/rx-detect stay lane-0-only — the
  existing single-lane machinery IS the lane-0 machinery, unchanged.

## 6. Framing / dialect reference (carried, status-updated)

The Gen 1→Gen 2 framing delta table from the original note stands; the
"fork: new" rows are all DONE through G4 (block TS gen/detect, SYNC/SDS,
TX SKP scheduling with the #40 rule, Table 6-2 framers, DPHSTART length
replica, idle symbols).  Width- and lane-relevant addenda:

* **Gen 1x2 keeps the Gen 1 dialect** — 8b10b K-codes, HPSTART/SDP
  framing words, LUP/LDN — striped byte-wise across two lanes.  The x2
  layer is a *width* problem, not a *dialect* problem.  But Gen 1x2 IS
  SuperSpeedPlus at the LINK layer (§2 terms): modulo-16 sequence
  numbers and LCRD1/LCRD2 credit classes apply per Table 7-4 — the
  SSP link mechanics built for Gen 2 are reused, rate-selected.
* Constructs may start at ANY byte offset of a wide beat (x2 striping
  may start packets on either lane [6.13.4]; wide beats at any config) —
  the §4.2 barrel/offset contract is the universal answer.
* Per-lane scrambling with per-lane seeds (§3.2 table); the LUNA-side
  Gen 1 scrambler ownership stays PHY-side in x2 (per-lane, below the
  merge), matching the Gen 2 ownership split.

## 7. Timing analysis (measured anchors, full matrix)

Anchors (session-13 silicon data): Gen 1 builds close 125 MHz first-roll
at 11–19 % margin (shipping 139–149); 64-bit @ 156.25 closed only via
the full cut campaign (engine rewrite + seam registers + SDC) and ~30
placement-lottery rolls, winners at +0.1 % (`156.263/169.777`); logic
depth grows ~log with width while the budget grows linearly — the
un-pipelined v1 engine (13.9 ns) would have closed untouched at 12.8 ns.

| Config | PIPE/core 64 | PIPE/core 128 |
|--------|--------------|----------------|
| Gen 1x1 (designed-for or fallback) | 62.5 trivial / 125 duty = known-easy | 31.25–62.5 trivial |
| Gen 1x2 | **125 MHz — Gen 1-class closure expected (no lottery)** | 62.5 trivial |
| Gen 2x1 | 156.25 — proven but lottery-class | **78.125 — ends the lottery era** |
| Gen 2x2 | — | **156.25 — the one genuinely hard cell** (width depth + the hard budget; expect a session-13-scale campaign; prefer fabric 256@78.125 only if a future core width justifies it) |

Fine print:

* Width helps every LOW-clock cell and NO 156.25 cell: a 128-bit barrel
  is a 16-position byte rotate (~2 more mux levels than 64) and 16-byte
  CRC-32 adds ~2 XOR levels — noise at 12.8 ns, meaningful at 6.4 ns.
* Duty-cycled cells inherit the PHY clock, not the scaled one — their
  timing is the PHY-clock column regardless of width.
* Area: streams/FIFO ports/seam registers scale; from 28 % LUT a
  single-wide-core build should land ~40–50 % — absolute headroom is
  fine, and the dual-chain collapse (§4.1) claws back the seams that
  caused the placement spread in the first place.
* The x2 additions (second lane datapath, deskew, striper) are shallow
  and ride the 8 ns (or slower) domains.
* Verdict vs the old staged plan: **Gen 1x2 @ 64/125 is decisively
  easier than Gen 2x1 @ 64/156.25** — every failing session-13 lottery
  roll (133–155 MHz) would have passed a 125 MHz gate; and **Gen 2x1
  @ 128/78.125 turns the hardest point of the program into a routine
  one**.  The unified width program is not extra risk on the timing
  axis — it is the timing fix.

## 8. Enumeration surface (all SSP configs)

Gen 1x2, Gen 2x1 and Gen 2x2 are all SuperSpeedPlus: bcdUSB 0320h; BOS
**SuperSpeedPlus USB Device Capability** with Sublink Speed Attributes
covering every supported (rate × lane) pair INCLUDING lane count
[§9.6.2.5]; **Sublink Speed Device Notification TP** on entering Address
state [§8.5.6.7]; SS Endpoint Companion unchanged for bulk.  One
implementation serves all configs (this is the still-open §10r-suspect-4
gap of the Gen 2 bring-up — build it once, parameterized by the
capability set).  Verification on the bench: check
`/sys/.../{speed,rx_lanes,tx_lanes}` — speed alone does not distinguish
Gen 2x1 from Gen 1x2 (both read 10000).

## 9. Verification plan

* **Strict host models are the law** (the #39/#40 lesson): the striped
  2-lane host enforces OS duplication, simultaneous SKP + idle-padding,
  per-lane seeds, deskew injection; the wide-beat hosts inject valid
  gaps and dense multi-construct beats; the duty-cycle stress bench
  randomizes valid/ready patterns.  Red-first for every new rule.
* **Unit fences per width**: parallel CRC-16/32 equivalence vs the
  32-bit reference (exhaustive lengths × offsets); barrel front-end
  oracle (random construct streams at all offsets); pacing model per
  width; deskew/striper oracle.
* **Battery axis bounded to three first-class elaboration points**:
  `w64/gen1x2`, `w64/gen2x1`, `w128/gen2x1` (Gen 2x2 prep) — full phase
  suites each; all other legal (config × width) cells get elaboration +
  smoke entries.  The 32-bit Gen 1 entries remain the untouchable
  regression fence.
* The gen2 sims' beat-level models (`gen2_coding.py`, scrambler
  keystream slices, `sim_link_gen2.py` benches) parameterize by width;
  the PIPE-contract oracle re-pins at 128-bit (one beat = one block).
* Hardware gates unchanged in spirit: a build is never flashed for a
  config whose table-1 clock it misses; ladders with recorded verdicts;
  uart wire-checker taps are dialect-neutral and carry (verified in
  session 13) — they gain a width parameter and, for x2, a per-lane
  pre-merge tap.

## 10. Relationship to the open G5 work (stage A)

Stage A (32-bit core + 64↔32 translation bridges at Gen 2) got us
G0–G4 and the session-13 silicon truths — #39/#40 live below the width
layer and carry into the unified stack 1:1, as does every negotiation/
LTSSM/PHY-bit-level mechanism.  **Recommendation: finish the open H2
root-cause on stage A** (the remaining U0-death is a link/PHY-layer
finding; every hour spent there de-risks the unified stack too), but
stop investing in stage-A-specific machinery beyond that: the 64↔32
bridges, the dual-chain muxing, and the ½-wire-rate cap are all
superseded by the width-generic core.  H3/H4 (the Gen 2 ladder + the
dual-rate matrix) move onto the wide core.

## 11. Phasing (unified program; each phase gated, sim-first)

1. **P0 — bench probes** (cheap, de-risk everything): LN0 TX bring-up
   (#38-pattern probe rig); wide fabric trims (5G 20×1:4 @ 62.5,
   10G 32×1:4 @ 78.125); PortMatch trace with a Gen 1x2 LBPM
   advertisement against the 20G root port (needs only the capability
   value + LTSSM match arm — answers "does this host really do x2"
   before any datapath work).
2. **P1 — the width-generic core at 64-bit, Gen 1x1 dialect** (new RTL
   beside the frozen core): barrel/offset front-ends, parallel CRCs,
   padded TX, duty-cycled operation.  Gate: the Gen 1 sim battery
   equivalent green at w64, including duty-cycle stress.  Then the
   **integration bench milestone: Gen 1x1 on the wide stack** (64-bit
   PIPE @ 62.5-native or 125-duty) — full multiep ladder against the
   known-good protocol at forgiving clocks.  This is the "do them
   together" keystone: it proves PHY width normalization + wide core
   with ZERO new protocol variables.
3. **P2 — Gen 1x2**: x2 PHY layer (striper/deskew/seeds/crossbar) +
   LBPM/LTSSM x2 arms + SSP link mechanics at Gen 1x2 verified; strict
   2-lane sims; bench: `luna-multiep-gen1x2` @ 64/125 (no lottery
   expected), ladder + fallback matrix (x2 ↔ x1 on the hub port),
   `rx_lanes=2` verified.
4. **P3 — Gen 2x1 on the wide core**: retire stage A; w64 @ 156.25
   first (known-closable, full wire rate — the ~1.1 GB/s runway), then
   the 128 @ 78.125 elaboration (bridge or native trim per P0) to end
   the lottery era.  Carry the H2 findings; rerun H2–H4 gates on the
   wide core.
5. **P4 — Gen 2x2 prep** (optional until wanted): 128-bit merge of two
   Gen 2 lanes; the 156.25 × width-depth campaign budgeted; the bench
   host already speaks it.

## 12. Open questions

1. ~~P0 trim experiments: does the PCS support 8b10b at 20×1:4 (5G) and
   raw 32×1:4 (10G)?~~  **ANSWERED (session 14, §3.1): 20×1:4 yes
   (silicon-proven at 62.5 MHz, TX side); 32×1:4 impossible (no
   width_mode >20 on the GW5AT-60) — Gen 2x1 → 128 is the bridge.**
2. Quad TX clocking in x2: both lanes phase-share the CMU within the
   1.3 ns TP1 launch-skew budget? (expected yes — same PLL; measure.)
3. LCRD1/LCRD2 buffer partitioning at Gen 1x2 (4+4 vs shared) — read
   §7.2.4.1.x against the wide receiver buffers; the parked "8 RX
   header buffers" item folds in here.
4. Duty-cycled TX at exact-rate cells: confirm the padded-TX density
   suffices for the ladder targets at Gen 1x2 @ 64/125 (zero slack
   width×clock product) — else the dense packer moves up the list.
5. Flipped-orientation x2: CC/orientation detect is implicit on the
   bench today; the crossbar needs a real orientation input eventually.
6. Does the historical 32-bit fence build ever retire?  Proposal: only
   after the wide core's Gen 1x1 ladder has shipped-parity soak history
   comparable to POR-66_011's.

## 13. The single-lane WIDTH PROGRAM (session 16 — the executable plan)

This section is the design authority for the session-16 mission
(`prompt.md`): make the stack width-generic at **`core_width ∈
{64, 128}`**, single lane only, so every shipping configuration closes
timing without the placement lottery.  It supersedes the §11 phasing
(P0 executed as W0; P2/P4 struck with x2; P1/P3 re-scoped as V1–V4).

### 13.1 Naming: what `core_width` means in THIS tree

The historical LUNA link/protocol streams are 32-bit
(`USBRawSuperSpeedStream(payload_words=4)`); the PIPE register is
64-bit with Gen 1 riding its low half (4 symbols @ 125), and the
stage-A Gen 2 block machinery is 64-bit-shaped @ 156.25 behind 32↔64
per-packet bridges (`physical/gen2.py`).  **`core_width` names the
PIPE-register / Gen2-block width of an elaboration; the LUNA
link/protocol streams run at `core_width/2`:**

| | `core_width=64` (default) | `core_width=128` |
|---|---|---|
| LUNA streams (`payload_words`) | 32-bit (4) — historical, verbatim | 64-bit (8) |
| Gen 1 PIPE presentation | 4 sym @ 125 in [31:0] (20×1:2 trim) | 8 sym @ 62.5 in [63:0] (native 20×1:4 trim) **or** 2:1-bridged 4-sym halves @ 125→62.5 (the Gen2 build's 5G fallback) |
| Gen 2 block presentation | 2×64-bit beats @ 156.25 (vendor PIPE, pinned) | 1×128-bit beat @ 78.125 (OUR bridge contract, §13.3) |
| Gen 2 stage bridges | 32↔64 per-packet (today, verbatim) | 64↔128 per-packet (same shape, widened) |
| Core-domain clock | = pclk (125 / 156.25) | Gen1x1 build: = pclk (62.5); Gen2 build: = **pclk/2** (78.125 @10G, 62.5 @5G fallback) |

`core_width=64` is **today's netlist, bit-for-bit** — the elaboration
parameter is threaded with the established `gen2=`-style discipline
(64-bit statements verbatim, 128-only code behind `if` at elaboration);
the proof is the Gen1-64 shipping payload parity after every
shared-file change, plus the untouched 64-bit battery entries.

### 13.2 The target matrix (single lane; timing gates)

| config | core_width | core clock | PHY clocks | gate |
|--------|-----------|------------|-----------|------|
| Gen 1x1 | 64 | 125 (= pclk) | pclk 125 / rxclk 125 | THE FENCE: payload-identical + ladder-green throughout |
| Gen 1x1 | 128 | 62.5 (= pclk, native 20×1:4 trim) | pclk 62.5 / rxclk 62.5 | core ≥ 62.5 (trivial); full multiep ladder |
| Gen 2x1 | 128 | 78.125 (= pclk/2) | pclk 156.25 / rxclk 161.29 (6.2 ns SDC) | core ≥ 78.125 AND pclk ≥ 156.25 AND rxclk ≥ 161.29; #45 resolved; 10000M + Gen2 ladder |
| Gen 2x1 | 64 | 156.25 (= pclk) | same | sim-green + buildable; timing OPTIONAL (bench-debug vehicle; never flashed for Gen2 runs unless MET) |

### 13.3 The 2:1 PIPE bridge (Gen 2 @ 128 ↔ the pinned 64-bit PHY)

W0 verdict (§3.1): the 10G fabric attach is fixed at 64-bit/156.25
(no width_mode >20 on the GW5AT-60) — Gen2×128 is the bridge, full
stop.  Design:

* **Placement**: the bridge is the ONLY new pclk-domain logic.  It
  sits at the PIPE boundary, between `GowinGTR12PIPE` (pclk) and the
  physical layer's Gen2 block engines (core domain).  Register-thin:
  a phase bit + one beat register per direction; no FSMs, no content
  parsing beyond the `tx_halfbeat` qualifier below.
* **Clocking**: the core domain is **pclk/2 by a fabric FF divider**,
  edge-locked to pclk, constrained as a generated clock
  (`create_generated_clock -divide_by 2`; new SDC branch in
  gowin-serdes).  It is pclk/2 at BOTH rates: 156.25→78.125 at 10G,
  125→62.5 at the 5G fallback — the fallback keeps the PROVEN 20×1:2
  trim and the proven #22 retune sequence; no clock muxing, no new
  quiesce hazard.  Consequence: the core:wire timer stretch at
  fallback is 78.125/62.5 = 1.25, IDENTICAL to the silicon-proven
  156.25/125 stretch of the 64-bit dual-rate build
  (`sync_frequency=78.125e6`; every timer recomputes from it).
* **MAC-side 128-bit beat contract (ours to define; re-pin the oracle
  sim at this width)**: one TX/RX beat = one whole 132-bit block
  payload (block_head as today, start on every beat).  The 24-symbol
  SKP OS does not fit the invariant (192 = 1.5×128): TX crosses it as
  one full beat + one half beat carrying symbols 16–23 in the LOW half
  flagged by a new **`tx_halfbeat`** qualifier — the bridge emits 2+1
  pclk beats and stays content-blind.  RX never sees a SKP (the PHY
  strips them, §gen2.py): the RX side is a clean 2-beat pairer
  anchored on `rx_start_block`, tolerant of rx_valid gaps between (but
  never inside) a pair.
* **Gen 1 fallback leg through the same bridge**: at 5G (pclk 125)
  the PHY presents 4 symbols in [31:0] per pclk beat; the bridge packs
  two such beats into the low 64 of a core beat @ 62.5 (and splits on
  TX).  Same phase machinery, width-parametric packing.
* **The #44 closed-loop pacing reference crosses here — DECISION: the
  pacing decision stays CORE-side**, in the block transmitter, exactly
  as sim-fenced today.  `tx_fifo_occupancy` (TxFifoWrNum, 64-bit-word
  units, pclk) is registered once at the bridge and sampled by the
  core every pclk/2 edge; thresholds keep their PHY-word units (a full
  core beat = 2 words, a halfbeat = 1).  The added sampling lag (2–3
  pclk total) folds into the #44 lag budget: the pacing sims and
  `tests/test_gen2_pacing.py` must model the bridged lag RED-FIRST
  before the hardware build (a stale-level overshoot is exactly the
  #44 class).  The bridge itself NEVER inserts or deletes gaps.

### 13.4 Domain-crossing inventory at the bridge (pclk ↔ pclk/2)

The divided clock is edge-locked — these are synchronous 2:1 paths,
not metastability CDCs (the only true async crossing stays inside the
PHY: rxclk→pclk AsyncFifo, untouched).  Every seam signal is
registered at the boundary to keep the 156.25 cones shallow:

| signal | dir | class | mechanism |
|---|---|---|---|
| tx_data/tx_sync_header/tx_start_block/tx_datavalid (+tx_halfbeat) | core→pclk | data | phase-muxed half-select, one pclk register |
| rx_data/rx_sync_header/rx_start_block/rx_datavalid | pclk→core | data | start-anchored pair accumulator, one core register |
| tx_fifo_occupancy (TxFifoWrNum) | pclk→core | multi-bit level | registered sample @ core edge (§13.3 lag budget) |
| phy_status (rate/power acks) | pclk→core | 1-pclk pulse | latch-and-hold ≥2 pclk (pulse would vanish between core edges) |
| rx_elec_idle, power_present, rx_status | pclk→core | level | register |
| rate, power_down, tx_elec_idle, tx_detrx_lpbk, rx_termination, rx_polarity, tx_deemph, rx_eq_training, reset | core→pclk | level (µs tolerances) | register |
| ltssm_training (→ PHY polarity acquisition, #39) | core→pclk | level | register |
| Gen1-leg rx_data[31:0]/rx_datak (fallback) | pclk→core | data | low-half pair accumulator (same phase bit) |
| Gen1-leg tx_data[31:0]/tx_datak (fallback) | core→pclk | data | low-half phase split |

Everything else — LTSSM, timers, LFPSTransceiver (constants from
`sync_frequency`), PHYResetController, rate FSM, link layer, protocol
layer, endpoints, the Gen2 block engines, the Gen1
scrambler/CTC/aligner/descrambler chain (widened to 64-bit at w128) —
lives in the core domain and never sees pclk.

### 13.5 What widens at `core_width=128` (the V1 work list)

* `USBRawSuperSpeedStream(payload_words=8)` + every hard-coded
  `32`/`4`-byte assumption in link + protocol (header framers: an HP
  = 16 B = 2 beats; LC = 8 B = 1 beat single-shot; CRC-16 over 12 B
  spans beats 0–1; parallel CRC-32 with 8-byte tails; data FIFOs;
  endpoint plumbing).
* `physical/gen2.py`: the 32→64 per-packet TX bridge becomes 64→128;
  the beat/half/sub grammar walk of the v2 RX engine generalizes or
  gets a 128-bit twin (at 1 beat = 1 block the machinery SHRINKS —
  the engine's 4-sym/cycle drain vs 8-sym/cycle wire gap widens to
  8 vs 16: the #43 run-compression queue bound must be re-proven at
  width, red-first).
* Gen1 physical conditioning (Scrambler/Descrambler/CTC/aligners):
  width-parametric 32→64 (LFSR advances 8 symbols/cycle).
* gw_usb3 (behind elaboration knobs, 5G suite pinned): the Gen1 PCS
  chain at 8 sym/beat for the native 62.5 trim (8b10b ×8, comma
  align, elastic width) — the "narrow shims"; the Gen2 datapath is
  UNTOUCHED (the bridge lives MAC-side).
* gowin-serdes: the 20×1:4 trim table entry (two divider registers,
  W0-verdicted), the w128 SDC branches (62.5 build; 6.4/6.2+generated
  -clock for the Gen2-128 build).

### 13.6 Verification plan deltas (V1 gates)

* Battery axis: the 53 Gen1-64/Gen2-64 entries stay untouched-green
  at every step (the fence).  Width-parallel entries for the core
  Gen2 phases at 128: `train/enum/echo/u0/hotreset/recovery/rxchain`
  + pacing.  New-mechanism sims RED-FIRST: the bridge (beat contract,
  SKP halfbeat, pacing lag), the wide RX engine queue bound, wide
  CRC equivalence (exhaustive lengths × offsets vs the 32-bit
  reference), the 128-bit oracle re-pin.
* Gen1-64 shipping payload parity (vs `/tmp/kilo/h0_gen1_fence.fs`)
  after EVERY shared-file change — non-negotiable.
* Hardware gates per §13.2; a Gen2 build that misses ITS width's gate
  is never flashed for Gen2 runs.

### 13.7 Phases (V0–V4, from the session-16 mission)

V0 orientation + fence re-proof (DONE on the bench, see HANDOVER
§10v) → V1 width-generic core sim-proven both widths → V2 Gen1
hardware both widths (64 = fence re-proof; 128 @ 62.5 native, full
ladder) → V3 Gen2x1 @ 128 hardware (#45 FIRST among bugs; per-cause
probe at the no-lottery clock; then 10000M + Gen2 ladder) → V4 the
dual-rate matrix, re-scoped without x2 (closes G5/H4).
