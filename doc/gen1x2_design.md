# Gen 1x2 design note — dual-lane 5G alongside Gen 2x1

**Status: design study (pre-implementation).**  Written against the USB 3.2
R1.1 redline (`GW_USB3/docs/USB 3.2 Revision 1.1 Redline against 3.2
R1.0.pdf/markdown.md`), the base spec markdown in `doc/`, and the state of
this tree at session 13 end (G5 phases H0/H1 closed, H2 open — see
HANDOVER §10s).  Section references are USB 3.2 R1.1 unless noted.

---

## 0. What the redline itself says (R1.0 → R1.1 deltas that matter here)

The dual-lane machinery (§3.2.1.3, §6.13, the x2 arms of §7.5.4) is carried
text from 3.2 R1.0 — Gen 1x2 is not new in R1.1.  The R1.1 refinements a
Gen 1x2 implementation must honor:

* **TX idle padding allowance** [6.4.3.1/6.4.3.2]: a transmitter *may pad up
  to 8 idle symbols* before a scheduled SKP OS "for implementation
  consistency with Gen 1x2 operation relating to lane alignment", and in x2
  *shall* pad idle symbols so SKP insertion stays aligned on both lanes when
  a DP payload ends on one lane ahead of the other.  This is the TX-side
  escape hatch our striper needs — it is normative permission to burn up to
  8 idle symbols to realign the lanes at an OS boundary.
* **x2 timer language** [7.5.4.8.1, Polling.Idle]: Polling.Active uses a
  **24 ms** timer in x2 (12 ms in x1) and the timers "continue until each
  lane has met the exit conditions"; one lane may finish its TS handshake
  early and must keep transmitting TS until the port as a whole advances.
* **Re-timer deskew wording** [E.x]: re-timers may deskew on TS1/TS2 *or SKP*
  in Gen 1x2 (SYNC in Gen 2x2) and must preserve OS boundaries when
  switching sources — useful confirmation that OS boundaries are the
  deskew datum for Gen 1 (there is no SDS at Gen 1).
* **PHY Ready LBPM bit-7 / RT Config** [7.5.4.5.1, Table 7-13]: the x2
  PHY Ready handshake carries re-timer presence announcement and a DFP
  RT-Config phase.  As a UFP we only ever answer with bit-7 = 0 and
  b6 = 0 (UFP); we must *tolerate* a DFP announcing RT Config.

## 1. What Gen 1x2 is on the wire (requirements inventory)

| # | Requirement | Ref |
|---|-------------|-----|
| 1 | Two 5 Gb/s 8b10b lanes; aggregate 8 Gb/s payload | §3.2.1.3 |
| 2 | **Lane 0 = the Configuration Lane** (the orientation-selected Type-C pair).  ALL LFPS (SCD, LBPM, Ping, Warm Reset, Ux exit) and receiver detect happen on lane 0 ONLY; lane 1 is silent until PortConfig selects x2 | §6.13.1/.3/.10/.12 |
| 3 | x2 capability negotiated in Polling.PortMatch via PHY Capability LBPM bit b6 (dual-lane) + rate bits [b3:b2] | §6.13.2, Table 7-13 |
| 4 | **Data striping, byte-granular, aligned to lane 0** (byte 0 → lane 0, byte 1 → lane 1, …).  Packets and link commands may *start on either lane*.  Control ordered sets are NOT striped — duplicated on both lanes | §6.13.4 |
| 5 | Ordered sets (TSEQ/TS1/TS2/SKP — no SDS/SYNC at Gen 1) transmitted **simultaneously on both lanes**; TS handshakes must complete on ALL negotiated lanes before state advance | §6.13.6 |
| 6 | Per-lane scrambler seeds: lane 0 = `FFFFh` (as today), **lane 1 = `8000h`** | §6.13.5 |
| 7 | Per-lane SKP clock compensation (each lane's elastic buffer adds/drops its own SKPs); TX inserts SKP on both lanes simultaneously with idle padding for odd DP tails | §6.13.6, §6.4.3.2 |
| 8 | Per-lane polarity inversion detect/correct | §6.13.7 |
| 9 | RX must deskew lanes; total budget at the Rx silicon input ≤ **6.4 ns ≈ 32 UI ≈ 3.2 symbols** at 5G (Table 6-34); deskew complete by end of training (datum = simultaneous OS boundaries) | §6.13.8, §7.5.4.8.1 |
| 10 | TS1 received on ANY negotiated lane in U0 → Recovery, TS1 on ALL lanes | §6.13.6 |
| 11 | Loopback per lane; compliance patterns on all lanes; per-lane seeds for CP0/CP9 | §6.13.9/.11 |
| 12 | Gen 1x2 **is SuperSpeedPlus** (§2 terms): the SSP BOS device capability with correct Sublink Speed Attributes (and lane count) is required on the enum surface — the same §10r-suspect-4 gap Gen 2x1 has.  PTM is required for *hosts/hubs* at Gen 1x2 (not devices) | §2, §9.6.2.5 |

**One protocol-layer bonus:** Gen 1x2 keeps the Gen 1 *link dialect* — 8b10b
K-codes, HPSTART/SDP framing words, LGOOD/LCRD (no LCRD2 classes, no
modulo-16 headers, no length replicas, no block framing).  Everything the
Gen 2 stage-A machinery translates simply does not exist here; the x2 layer
is a *width* problem, not a *dialect* problem.

## 2. Negotiation reality — Gen 1x2 and Gen 2x1 are alternatives, not a ladder

Table 7-13/7-14 and the fallback rules [7.5.4.5.1] have a consequence that
shapes the whole plan:

* Ranking is Gen 2x2 > Gen 2x1 > **Gen 1x2** > Gen 1x1, but a port announces
  ONE capability at a time and the mandated fallback for a **Gen 2x1-highest
  port is Gen 1x1 directly** ("its next advertised PHY capability shall be
  Gen 1x1").  Only a Gen 2x2-highest port walks the full
  Gen 2x2 → Gen 2x1 → Gen 1x2 → Gen 1x1 ladder (Table 7-15).
* Start-up match (Table 7-14): a device announcing Gen 1x2 gets Gen 1x2
  against a Gen 1x2 or **Gen 2x2** host, and **Gen 1x1 against a Gen 2x1
  host** (rate mismatch never resolves to the other axis).

So "Gen 1x2 alongside Gen 2x1" means: **both capabilities live in the
codebase; a build/boot knob selects the advertised highest.**  There is no
spec-conformant single bitstream that tries 10G-x1 first and then 5G-x2 —
unless we implement Gen 2x2 as the advertised highest someday, which is
exactly what the full ladder was designed for (see §6 below: the GTR12 quad
has the lanes for it).

**Bench fact (verified 2026-09-01):** the bench host's usb4 root hub reports
`speed = 20000`, `rx_lanes = tx_lanes = 2` — a **Gen 2x2-capable xHCI**.
Per Table 7-14 it will match a Gen 1x2 announcement at Gen 1x2.  Gen 1x2 is
therefore fully validatable on our own bench, on the same 4-3 port, with the
same replug/POR discipline.  (`lsusb` verdict string to expect:
`10000M` shown as Gen 1x2 in `/sys/.../speed` = 10000 with
`rx_lanes/tx_lanes = 2` — check the lane files, not just the speed.)

## 3. What we already have

* **Both Type-C SS pairs land on GTR12 Quad 0**: straight orientation →
  `Q0_LN1`, flipped → `Q0_LN0` (pad adjacency; HANDOVER §10o, bug #38).
  In x2 terms: **lane 0 (Configuration Lane) = LN1 and lane 1 = LN0 in the
  straight orientation** — and the mapping swaps when the plug flips.
  The #38 work already proved LN0's CSR bring-up and RX path on silicon
  (probe-only rig); LN0's **TX** path has never been exercised.
* **Per-lane UPAR CSR access with known addresses** for every lane/quad
  register (`gw_usb3/upar_csr.py`), including the width/gear reconfig
  registers (`recfg_width_mode_1..4`) that the vendor 10G↔5G rate tables
  already flip at runtime.
* **The GTR12 fabric width is a per-lane trim**, not a fixed property:
  `LaneConfig.width_mode ∈ {8,10,16,20,32,40,64}` × `gear_rate ∈
  {1:1, 1:2, 1:4}` (gowin-serdes `csr_map.py`).  Our current boot trims
  (`gowin_serdes/usb3.py _BOOT_TRIMS`): 10G = width 16 × 1:4 = 64-bit fabric
  @ 156.25 MHz; 5G = width 20 × 1:2 = 40-bit raw (32-bit decoded) @ 125 MHz.
  A 5G lane at width 20 × **1:4** would present 8 symbols @ **62.5 MHz**;
  a 10G lane at width 32 × 1:4 would present 128 bits @ **78.125 MHz** —
  *if* the PCS supports those combinations at those line rates (bench
  experiment required; the vendor tables only use the two trims above).
* A Gen 1 datapath that is per-lane by construction (8b10b, SKP-stripping
  elastic buffer, word aligner — `gw_usb3` — all vendor-exact and
  equivalence-pinned), and a proven Gen 1x1 shipping stack at 125 MHz.
* The Gen 2 stage-A machinery (LBPM engine, LTSSM rate handshake, 32↔64
  bridges) — of which the **LBPM/PortMatch/PortConfig plumbing is directly
  reusable**: x2 negotiation is the same LBPM exchange with b6 set.

## 4. Work plan by layer

### 4.1 gowin-serdes (public repo)

| Item | Effort | Notes |
|------|--------|-------|
| Dual-lane `serdes.toml`/CSR generation (LN0 + LN1, both 5G trim) | S | `usb3_lane_config` already parameterized per lane; add a two-lane variant of `make_usb3_serdes` + boot writes for both lanes |
| LN0 TX bring-up | M (bench) | First TX use of the flipped pair ever; expect an AFE/trim session like the original LN1 bring-up (archive §10b); A/B against LN1 |
| Clocking | S | TX: both lanes share the quad CMU/TX PLL → one common TX word clock (verify `tx_quad_clk_internal_sel`).  RX: two recovered clocks → two `rxclk` domains; SDC: add the second lane's clocks + false paths (same pattern as session-13 M3) |
| SDC for the x2 tops | S | New top names in the constrained branch; pclk stays 8 ns |

### 4.2 gw_usb3 (PHY layer)

| Item | Effort | Notes |
|------|--------|-------|
| Second Gen 1 datapath instance | S | The per-lane RTL (8b10b, elastic buffer, aligner) instantiates cleanly; keep each lane vendor-exact so the equivalence suite still pins them individually |
| Lane-1 scrambler seed `8000h` | S | Parameterize the Gen 1 LFSR seed [6.13.5]; equivalence tests keep lane 0 pinned at `FFFFh` |
| **Lane deskew buffer** (new module, ours alone) | M | Post-elastic-buffer, per-lane 8-entry symbol FIFO; acquire alignment on TS1/TS2 OS boundaries during training (the only datum at Gen 1 — no SDS), maintain across SKP events.  Budget: cable ≤ 3.2 symbols + per-lane elastic buffer phase ± a few — 8 symbols of range is comfortable.  **No vendor netlist exists for this** → oracle + unit-bench verification only, sim-first |
| **Striping layer** (new, ours alone) | M | TX: byte-interleave the 64-bit stream to 2×32 aligned to lane 0; duplicate ordered sets on both lanes; simultaneous SKP insertion + odd-tail idle padding [6.4.3.2, R1.1 8-symbol allowance].  RX: interleave-merge the deskewed streams.  Straight wiring + a 2-symbol realignment case — much shallower than the Gen 2 block engines |
| Per-lane polarity | S | Existing per-lane mechanism, instantiate twice [6.13.7] |
| PIPE widening to 64-bit @ 125 for x2 | S | Same shape as the Gen 2 64-bit PIPE, lower clock |
| Config-Lane crossbar (orientation) | S–M | Logical lane 0/1 ↔ physical LN1/LN0 swap mux.  Phase 1 can pin straight orientation (lane 0 = LN1, as today); the mux should be designed in from the start |

### 4.3 LUNA MAC (luna-ss)

| Item | Effort | Notes |
|------|--------|-------|
| LBPM capability value | S | `LBPM_CAP_GEN1X2 = 0x20` (b6 set, rate 00) next to the existing `GEN2X1 = 0x04`; PortMatch rank/fallback per §7.5.4.5.1 (Gen 1x2 → Gen 1x1) |
| LTSSM x2 arms | M | 24 ms Polling.Active timer; per-lane TS-detect inputs, exit on BOTH lanes trained (with continue-transmitting-TS on the early lane); PortConfig applies to all lanes; TS1-on-any-lane → Recovery-on-all [6.13.6]; per-lane loopback.  All gen1x2-gated, Gen 1x1 elaborations verbatim (the session-13 discipline) |
| **64-bit Gen 1-dialect link/protocol core @ 125 MHz** | **L — the big one** | See §5/§6.  A 32-bit core cannot absorb 8 symbols/cycle: Gen 1x2 with the historical core would cap at Gen 1x1 throughput — pointless.  This is the parked "stage-B width-generic core" item (§9.4), which Gen 1x2 *requires* rather than merely benefits from |
| Enum surface | M | SSP BOS device capability with Sublink Speed Attributes incl. lane count, bcdUSB 0320; the same gap already on the Gen 2 books (§10r suspect 4) — one implementation serves both |
| Sims | M | Extend the link sim family with a striped 2-lane host model (strict, per the #40 lesson: enforce OS duplication, simultaneous SKP, seed 8000h on lane 1, deskew injection).  No vendor baseline exists for x2 — the strict host model and the oracle are the only fences, so they must be written red-first |

## 5. Timing opinion — Gen 1x2 vs Gen 2x1 (1×10G)

**Gen 1x2 is decisively easier, and it is not close.**  Grounded in this
session's measured numbers:

| Domain | Gen 2x1 (today) | Gen 1x2 (proposed) |
|--------|----------------|--------------------|
| MAC/pclk | 64-bit @ **156.25 MHz** (6.4 ns) | 64-bit @ **125 MHz** (8.0 ns) |
| PHY RX | 128b/132b gearbox + block descrambler @ 156.25 | 2× (8b10b + elastic buffer) @ 125 — the shipping Gen 1 path |
| Wire-rate engines | Gen 2 block TX/RX engines (the session-13 cone) | none — Gen 1 dialect native |

Session-13 evidence: the Gen 2 top needed the v2 bulk/boundary engine
rewrite, seven seam-register batches, an SDC campaign, and ~30 placement
lottery rolls to squeeze past 156.25, with winners at +0.1 % margin — while
every Gen 1 build closes 125 MHz on the **first roll with 11–19 % margin**
(shipping: pclk 139–149 across history).  The failing Gen 2 rolls
themselves (133–155 MHz) would ALL have passed a 125 MHz gate.  The x2
additions (second Gen 1 datapath, deskew FIFO, byte-interleave muxes) are
shallow, and 8 ns absorbs the extra placement pressure the same way the
Gen 1 domain always has.  Expected closure effort: Gen 1-like (no lottery
grinding), not Gen 2-like.

Two caveats:

1. The **64-bit MAC core at 125 MHz** is new logic; wider CRC-32 (8
   bytes/cycle) and wider muxes eat some of the 8 ns — but the Gen 2 work
   already proved the harder version of every one of those cones at 6.4 ns.
2. Total area grows (two RX datapaths + a 64-bit core + both-capability
   tops).  We are at 28 % LUT today; even ×2 leaves headroom, and low
   clocks forgive routing spread — but the dual-capability top (Gen 2
   machinery AND x2 machinery elaborated together) should be watched.

## 6. The width question: 32 / 64 / 128-bit PIPE and a width-generic LUNA

### 6.1 The configuration space

Payload rates: Gen 1 lane = 4.0 Gb/s (8b10b), Gen 2 lane ≈ 9.7 Gb/s
(128b/132b).  Candidate operating points:

| Config | Payload | 32-bit pclk | 64-bit pclk | 128-bit pclk |
|--------|---------|------------|------------|-------------|
| Gen 1x1 | 4.0 G | **125 MHz** (ships) | 62.5 | 31.25 |
| Gen 1x2 | 8.0 G | 250 — impossible | **125 MHz** | 62.5 |
| Gen 2x1 | 9.7 G | (stage-A: ½-rate translate) | **156.25 MHz** (this session, barely) | **78.125 MHz** |
| Gen 2x2 | 19.4 G | — | 312.5 — impossible | **156.25 MHz** |

The pattern: **width-up/clock-down is the strongest timing lever we have.**
Doubling width halves the clock — the per-path budget doubles while logic
depth grows sub-linearly (a 128-bit CRC-32 tree is deeper than a 64-bit one,
but nowhere near 2× the delay).  Concretely from session 13: the v1 grammar
engine failed 6.4 ns at 13.9 ns of logic; a 12.8 ns budget (128-bit
@ 78.125 for Gen 2x1) would have accepted it **untouched** — the entire
month-equivalent of pipelining surgery and lottery grinding was the price of
the 6.4 ns point specifically.

### 6.2 The GTR12 can meet us there (UPAR-reconfigurable widths)

The fabric width is a lane trim, and it is **already runtime-switched**: the
vendor 10G↔5G rate-change tables flip `recfg_width_mode_1..4`
(width 16×1:4 ↔ 20×1:2) through the same UPAR sequencer we drive today.
Extending the trim tables is mechanism we own end-to-end:

* Gen 1 @ width 20 × gear 1:4 → 8 symbols @ 62.5 MHz per lane (x2 merged:
  128-bit @ 62.5).
* Gen 2 @ width 32 × gear 1:4 → 128-bit raw @ 78.125 MHz — this would pull
  even the **PHY-side rxclk domain** (the 128b/132b gearbox, descrambler,
  aligner — today at 156.25) down to 78.125.

Two hard qualifications before planning around that:

1. **Unproven combinations.**  Only the two vendor trims are
   silicon-proven.  Whether the hard PCS supports 8b10b at width 20×1:4, or
   raw width 32×1:4 at 10.3125G line rate, is a bench experiment (a
   probe-rig session like #38's, cheap to run, must come first).
2. **Vendor-exactness ends where the width changes.**  The ported Gen 2
   datapath (RxGearbox132, Descrambler, aligner) is pinned quirk-for-quirk
   against the vendor netlist *at 64-bit*.  Re-porting it to 128-bit makes
   it ours alone — the equivalence suite loses its baseline for those
   modules and the oracle/link-layer-test-spec benches become the only
   fence.  That is the same (acceptable) position the x2 striper/deskew are
   in, but it should be a deliberate decision, not a side effect.
   The safe hybrid: keep the PHY datapath at the proven 64-bit/156.25 trim
   and put a **2:1 width bridge at the PIPE boundary** (64 @ 156.25 →
   128 @ 78.125) — the MAC gets the relaxed clock, the pinned RTL stays
   pinned, and only the shallow bridge lives at 156.25.

### 6.3 What a width-generic LUNA costs

The honest inventory of why this is a rewrite, not a parameter:

* `USBRawSuperSpeedStream` is fixed 32-bit data + 4-bit ctrl, and the link
  layer is *sequenced* in 32-bit words: `RECEIVE_DW0..DW3` FSM states,
  word-aligned `HPSTART_WORD` matching, the single-word `CHECK_CRC32`
  state, word-serial header CRC-16.  At 64-bit a header is 2 beats +
  possible straddle; at 128-bit an entire 4-DW header **plus** the start of
  the next construct arrives in ONE beat — the decoders become
  position-muxed constructs (the shape of the session-13 gen2 bulk/boundary
  engine) rather than word-serial FSMs.
* Packet/framing offsets stop being word-aligned: HPSTART may land mid-beat
  (at Gen 1x2, packets may even start on lane 1 = odd byte offsets
  [6.13.4]).  Every framer needs barrel-select front ends.
* CRC-32/CRC-16 need parallel N-byte-per-cycle forms with lane-enable
  handling for tails (the 32-bit forms exist; 64/128 are new but standard).
* Protocol layer and endpoint interfaces (`USBInSuperSpeedStreamInterface`
  etc.), the endpoint buffers, and the multiep DMA paths all carry the
  width.

**Recommendation:** do NOT parameterize the historical 32-bit core.  It is
the shipping Gen 1x1 fence, protected by payload-identity discipline — any
touch costs battery + parity + hardware re-laddering for zero Gen 1x1 gain.
Instead build the parked **stage-B core as width-generic (64 first)** with
the strict sims as its fence, and keep both cores in the tree
(the full `core_width ∈ {32,64,128}` design — legality matrix, clocking
choice, module inventory, per-cell timing — is worked out in §6.5):

1. **Step 1 — 64-bit stage-B core.**  Serves Gen 1x2 @ 125 (this note's
   subject) *and* full-wire-rate Gen 2x1 @ 156.25 (retiring stage-A's
   ½-rate translation cap, ~1.1 GB/s runway).  156.25/64 is the hardest
   point in the new core's matrix — but every cone class in it was already
   closed once this session, and Gen 1x2 only needs the 125 MHz point to
   ship.
2. **Step 2 (optional, later) — 128-bit elaboration** of the same generic
   core.  Buys: Gen 2x1 @ 78.125 (trivial closure, ends the lottery era for
   Gen 2 builds) and the only viable path to Gen 2x2 @ 156.25 (the bench
   host does 20G; the quad has 4 lanes).  Costs: the width bridge or PHY
   re-port of §6.2, ~1.5–2× stream-datapath area, deeper CRC trees
   (absorbed by 12.8 ns), and a second elaboration point in every fence.

### 6.4 Knock-on consequences of changing the PIPE width (checklist)

* **TX pacing** (bug-#40-adjacent math): the 1-gap-per-16-blocks Gen 2 rule
  is width-relative — at 128-bit @ 78.125 one beat = 1 block + 4 bits, so
  the exact ratio becomes 1 gap per 32 blocks of 33 beats... re-derive from
  first principles per width and re-pin `tests/test_gen2_pacing.py` (the
  FIFO model is already width-parameterizable via the beat clock).
* **TxFifoWrNum thresholds** and the probe channels scale with beat size.
* The gen2 sims' beat-level host models (`gen2_coding.py` beats, the
  scrambler model's 64-bit keystream slices) parameterize with the width.
* At Gen 1x2 specifically: SKP handling must stay **per-lane** *below* the
  merge point (the elastic buffers), never in the merged stream — the
  merged-stream CTC path used at Gen 1x1 is bypassed in x2.
* On-the-fly width reconfig via UPAR is the same class of operation as the
  10G↔5G rate retune — i.e., it inherits the **#22 boot-window discipline**
  (quiesce/park the MAC across the retune).  Recommendation: *width follows
  the negotiated trim* exactly like today's rate tables (one width per
  rate×lane configuration, flipped inside Polling.SpeedSwitch/PortConfig) —
  no independent width state machine.

### 6.5 A width-generic LUNA core: `core_width ∈ {32, 64, 128}` at init

The target: one core, one elaboration parameter, with this legality matrix
(a build asserts it at elaboration time — a config outside its column is a
construction error, not a runtime surprise):

| Capability (advertised highest) | 32-bit core | 64-bit core | 128-bit core |
|--------------------------------|:-----------:|:-----------:|:------------:|
| Gen 1x1 (4.0 G payload)        | ✔ (ships)   | ✔           | ✔            |
| Gen 1x2 (8.0 G)                | ✗ (caps at x1 rate) | ✔   | ✔            |
| Gen 2x1 (9.7 G)                | ✗ (stage-A ½-rate only) | ✔ | ✔          |
| Gen 2x2 (19.4 G)               | ✗           | ✗ (needs 312.5 MHz) | ✔    |

Rule of thumb: a width is legal for a capability iff
`width_bits × pclk ≥ payload_rate` at a closable pclk.  32 covers only
Gen 1x1; 64 covers everything through Gen 2x1; 128 covers everything.

#### 6.5.1 The clocking decision: full beats at a scaled clock, or duty-cycled beats at the PHY clock

Running a WIDE core under a NARROW config (e.g. Gen 1x1 on a 64/128-bit
core) forces the one real architectural choice of the whole exercise.  The
wire delivers 4 symbols per 125 MHz word at Gen 1x1; a 64-bit core must
either:

* **(a) Duty-cycling — pclk stays the PHY trim clock.**  RX accumulates
  full beats and presents them with `valid` gaps (Gen 1x1 on 64-bit: one
  full beat every 2nd cycle @ 125); TX is `ready`-throttled the same way.
  No new clock trims, no CDC, no PHY changes.  The cost: the core must be
  **gap-tolerant on every RX path and throttle-tolerant on every TX path**
  — which is exactly the discipline the Gen 2 bring-up already forced
  (`CHECK_CRC32` valid-gating, bug #40's contiguity lessons).  Timing: no
  relief (the core still closes at the PHY clock).
* **(b) Full-rate beats at a scaled pclk** (Gen 1x1 on 64-bit @ 62.5, on
  128-bit @ 31.25).  Timing relief is maximal, beats are always full in
  steady state.  The cost: pclk now depends on rate × lanes × width — more
  PHY fabric trims (§6.2, some unproven) or width bridges, more SDC
  clocks, and every trim flip inherits the #22 retune window.

**Recommendation: (b) for the operating point a build is DESIGNED for,
(a) as the mandatory fallback mode.**  The reasoning is the fallback
matrix itself: a 64-bit Gen 2x1 build that falls back to Gen 1x1 has its
PHY at the 32-bit/125 trim — the wide core then *necessarily* runs
duty-cycled (accumulate 2 cycles per beat) unless we also retune pclk
mid-LTSSM (a second #22-class hazard per fallback for no benefit — the
fallback rate needs no timing relief by definition).  So gap/throttle
tolerance must be built into the width-generic core **regardless**; once
it exists, option (a) is free everywhere, and (b) becomes a per-build
optimization knob for the designed-for config.  Concrete consequence for
the user-visible matrix: **Gen 1x1 on a 64/128-bit core costs nothing at
runtime — it is the same duty-cycled mode the fallback path requires
anyway.**

This also collapses today's dual-chain architecture: the current dual-rate
build elaborates the full historical 32-bit Gen 1 chain NEXT TO the Gen 2
machinery and muxes at the seams (stage A).  A gap-tolerant width-generic
core serves **all negotiated configs of one build from one datapath** —
the Gen 1x1 fallback leg stops being a second core.  That is a large area
and congestion win for exactly the builds that struggle with placement
today (session 13's lottery was fought at 28 % utilization dominated by
the doubled chains and their seams).

#### 6.5.2 Stream contract for the generic core

The 32-bit `USBRawSuperSpeedStream` (data + 4-bit K-ctrl) generalizes to:

```
data  : width bits
ctrl  : width/8 bits          # per-byte K flag (Gen 1 dialect)
valid : 1                      # beat-granular; gaps legal ANYWHERE on RX
len   : log2(width/8)+1 bits   # valid bytes in the FINAL beat of a
                               # construct (tail handling; full otherwise)
first : 1                      # construct starts in this beat (+ offset)
offs  : log2(width/8) bits     # byte offset of the construct start
```

`len/first/offs` are the price of beats that no longer align to construct
boundaries: at 64-bit a header straddles beats or shares one with a link
command; at 128-bit one beat can carry `[LGOOD][LCRD][HPSTART dw0 dw1…]`.
Two simplifications keep this tractable:

* **RX normalizes early.**  One barrel-rotate front-end per receiver class
  (header / data / LC) aligns constructs to offset 0 before the FSMs —
  the same shape as the session-13 gen2 bulk/boundary engine (aligned bulk
  beats + a narrow boundary walker), which is now a proven pattern at the
  HARDEST clock in the matrix.  The FSMs behind it see aligned,
  full-or-tail beats only.
* **TX may pad instead of pack.**  Aligning every construct start to a
  beat boundary with logical-idle fill between constructs is legal at
  Gen 1 (idle between packets) and at Gen 2 (idle data blocks between
  constructs).  Padding costs only inter-packet bandwidth — bounded by the
  same credit/turnaround overheads that already dominate — and removes the
  multi-construct-per-beat packer entirely.  Ship padded-TX first; a dense
  packer is a later, isolated optimization.  One exception must stay
  dense: DPP payload bodies must stream full beats (mid-packet idle is
  illegal in both dialects) — that is the endpoint buffer's job, and it
  already sustains it at 32-bit.

#### 6.5.3 Module-by-module inventory (what actually changes)

| Module class | 32-bit today | Width-generic form | Effort |
|--------------|--------------|--------------------|--------|
| LTSSM, timers, LFPS/LBPM, power mgmt | width-free (control + time) | untouched; timers already take `ss_clock_frequency` (G3 work) — they parameterize by clock, which is the same axis | none |
| Ordered-set detect/emit (TS/TSEQ) | 32-bit word compare chains | per-beat position-muxed compares; at 128-bit a whole TS fits one beat (detect gets EASIER — single-shot compare) | S |
| Header RX (`header.py`/`receiver.py`) | `RECEIVE_DW0..3` word-serial FSM + serial CRC-16 | barrel front-end + N-DW-per-beat capture; CRC-16 over up-to-12-bytes/beat combinational slices | M |
| Header TX (`transmitter.py`) | word-serial emit | beat-composed emit from a header register (whole header in ≤ beats; trivial at 128) | M |
| Data RX/TX (`data.py`) | word FSM, single-word `CHECK_CRC32` | parallel CRC-32 with byte-enable tails (1..width/8 bytes/cycle); the gen2-gated valid-tolerance generalizes to width-tolerance | M |
| Link command detect/generate | 8-symbol constructs, word-paired | at ≥64-bit an LC fits one beat: single-shot compare/emit (EASIER); multiple-LCs-per-beat only if dense TX — padded TX avoids it on TX, RX must accept back-to-back LCs in one beat from the partner (real hosts pack) | M |
| Idle handshake | 2-word window | N-byte window with valid gating (already gap-aware post session 13) | S |
| Protocol layer (`tp_generator`, endpoint mux) | 32-bit streams | width-parametric plumbing; TP composition = header-class work | M |
| Endpoint datapaths + FIFOs (multiep) | 32-bit BSRAM streams | widen (BSRAM aspect ratios support ×4); DMA/loopback plumbing mechanical | M |
| Gen 2 block engines (`gen2.py`) | 64-bit beats, half/sub walker | at 128-bit: **one beat = one whole block payload** (128 = 132−4) — the beat/half assembly collapses, the RX queue halves in depth, pacing = same 32-data+1-gap per 33 beats ratio | S (shrinks!) |
| x2 striper/deskew (§4.2) | — | naturally width-generic (it is a byte-lane construct) | included above |
| PIPE adapter + pacing + probes | 64-bit | width-parametric per §6.4 | S |

Nothing in the list is exotic; the header/data framers are the bulk of it,
and their hard version (position-muxed decode at 6.4 ns) is what session 13
already built for the gen2 RX path.

#### 6.5.4 Timing impact per (config, width) — the full matrix

Anchored to measured silicon data (Gen 1 builds close 125 MHz first-roll at
11–19 % margin; 64-bit @ 156.25 closes only via the session-13 cut
campaign + lottery; logic depth grows ~log with width while the budget
grows linearly):

| Config | 32-bit | 64-bit | 128-bit |
|--------|--------|--------|---------|
| Gen 1x1 | 125 MHz — **ships** | (b) 62.5: trivial / (a) 125: known-easy | (b) 31.25: trivial / (a) 62.5–125: easy |
| Gen 1x2 | — | **125 MHz: Gen 1-class closure expected (§5)** | 62.5: trivial |
| Gen 2x1 | — | 156.25: **proven, but lottery-class** | **78.125: the v1-engine-would-have-closed point; ends the lottery era** |
| Gen 2x2 | — | — | 156.25: **the new hard point** — wider AND the hard clock; expect a session-13-scale campaign.  Prefer 256 @ 78.125 if the fabric trims allow (§6.2), else budget for it |

Width-specific timing caveats (the honest fine print):

* Wider is not free *depth*: a 128-bit barrel front-end is a 16-position
  byte rotate (~2 more mux levels than 64) and 16-byte/cycle CRC-32 adds
  ~2 XOR levels — both are noise at 12.8 ns budgets and meaningful at
  6.4 ns.  This is why **Gen 2x2 @ 128/156.25 is the one genuinely hard
  cell** in the table: it pays the width depth AND the 6.4 ns budget
  simultaneously.
* Wider is real *area/fanout*: streams, FIFO ports, and the seam registers
  all scale.  From 28 % LUT today, a 128-bit single-core build should land
  ~40–50 % — fine in absolute terms, but placement spread was our real
  enemy at 6.4 ns, so the low-clock cells of the matrix are the ones that
  benefit; do not expect width to help any 156.25 cell.
* Duty-cycled (option-a) cells inherit the PHY clock, not the scaled one —
  their timing is the PHY-clock column regardless of width.

#### 6.5.5 Verification surface (keeping the explosion bounded)

The matrix multiplies fences; bound it the way the trees already bound
rate × dialect:

* The historical 32-bit core stays frozen as the Gen 1x1 shipping fence
  (payload-identity discipline untouched — the generic core is NEW RTL).
* The generic core pins **three first-class elaboration points** in the
  battery: `w64/gen1x2`, `w64/gen2x1`, `w128/gen2x2-prep` — each with the
  strict host models (striping rules, SKP placement, valid-gap injection,
  duty-cycled-fallback runs).  Other legal cells get elaboration + smoke
  entries only.
* Unit fences that must exist per width: parallel CRC equivalence vs the
  32-bit reference (exhaustive over lengths/offsets), barrel front-end
  oracle (random construct streams at all offsets), pacing model per
  §6.4, and a duty-cycle stress bench (randomized valid/ready patterns —
  the generalization of the #40 strict-host lesson: the FORGIVING bench is
  how width bugs will hide).

## 7. Suggested phasing (each gated, sim-first, one mechanism per change)

1. **P0 — bench probes:** LN0 TX bring-up (probe rig, #38 pattern); GTR12
   width/gear trim experiments (20×1:4 @ 5G, 32×1:4 @ 10G) — cheap, they
   de-risk everything above.
2. **P1 — stage-B 64-bit core** at 125 MHz behind the strict Gen 1-dialect
   sims (red-first).  Gate: Gen 1x1-equivalent sim battery green at 64-bit.
3. **P2 — x2 PHY layer:** striper + deskew + lane-1 seed + dual-lane
   serdes config; oracle + strict 2-lane host model (enforce §1 items 4–9).
   Gate: striped enum/echo sims green, including deskew-injection and
   odd-tail SKP-padding negatives.
4. **P3 — LTSSM/LBPM x2 arms** + fb matrix sims (Gen 1x2 → Gen 1x1
   fallback; PortMatch against a Gen 2x2 host model).
5. **P4 — bench:** `luna-enum-gen1x2` top (timing gate: pclk ≥ 125 — no
   lottery expected), against the 20G root port; verify
   `rx_lanes/tx_lanes = 2` in sysfs, then the ladder; then the tri-rate
   fallback matrix (x2 on the 10G/20G port, x1 fallback on the 5G hub).
6. Keep Gen 2x1 H2–H4 (the open G5 work) independent — the two capability
   tracks only converge if/when a Gen 2x2 top makes the full Table 7-15
   ladder real.

## 8. Open questions

1. Does the GTR12 PCS support the wider gear trims at each line rate
   (P0 experiment)?  If 10G @ 128-bit works, §6.2's hybrid bridge becomes
   optional rather than necessary.
2. Quad TX clocking in dual-lane: confirm both lanes phase-share the CMU
   such that TX OS launch skew is within Table 6-34's 1.3 ns TP1 budget
   (expected yes — same quad, same PLL — but measure).
3. Flipped-orientation x2 (lane-0 crossbar) — phase 1 pins straight; the
   Type-C CC/orientation detect is currently implicit in our bench setup.
4. Does the 20G root port's xHCI/driver actually enable Gen 1x2 (some
   hosts implement only Gen 2x2 + Gen 2x1 + Gen 1x1 in practice)?  A
   PortMatch trace on the bench answers this before any datapath work —
   it only needs the LBPM capability value and the LTSSM match arm.
