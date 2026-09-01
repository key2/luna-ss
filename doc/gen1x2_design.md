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
the strict sims as its fence, and keep both cores in the tree:

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
