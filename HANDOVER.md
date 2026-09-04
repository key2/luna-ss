# HANDOVER — GW_USB3 project state

Written 2026-08-25, end of a long working session; extended 2026-08-26/27
(§10a–§10e). This document is the single entry point for continuing the
work. Everything below has been done and verified in this checkout;
nothing here is aspirational unless marked **TODO** or **UNVERIFIED**.

**Read order for a new session: §10a→§10i FIRST (dated updates — they
supersede anything contradicting in §1–§9, e.g. the old UART polarity,
the "gwu2x" programmer guess, the RAM16SDP/"no SSRAM" workaround story
and the §7b timing snapshot), then `prompt.md` for the active mission,
then the sections below as reference.** Status in one line (§10f): the
Gen1 (5G) TX bug is FOUND (GowinSynthesis pROM mis-inference in the
8b/10b encoder) and FIXED (`syn_romstyle="logic"` on all emitted
modules); hybrid, usb31-enum and luna-enum all enumerate at Gen1 —
LUNA-on-our-PHY reached U0 on hardware.  Next: LUNA endpoints
(§10c step list), Gen2-through-LUNA later.

## 1. Project goal

Port the Gowin USB3.1 PHY (encrypted vendor IP, decrypted into
`rtl/usb31phy/`) to **Amaranth HDL** (`gw_usb3/` package), prove it
bit/cycle-exact against the vendor Verilog, and build a **basic USB3
enumeration example** on real hardware using:

* our Amaranth PHY,
* the Python-generated SerDes (`gowin-serdes/`, previously unproven),
* the vendor USB3.2 device controller netlists + descriptors from
  `Gowin_USB3.1_UVC_BULK_RefDesign/` (LTSSM/link layer sit *above* the PHY).

Target: **5 Gbit (Gen1) enumeration**. Do not assume Gen2/10G works; the
design boots the SerDes in the Gen2 trim like the vendor and falls back.

## 2. Environment

* Python via **pdm** (`.venv`, Python 3.13): `amaranth 0.5.9` (note: a
  second amaranth 0.5.8 lives in `~/.local` and is picked up by bare
  `python3` — the examples work with both, but `pdm run` uses the venv).
* Simulators: **iverilog 12** (cocotb equivalence), verilator (lint only).
* `cocotb 2.0.x` + pytest (dev deps in `pyproject.toml`).
* **Gowin IDE V1.9.12.03** at `/home/key2/Downloads/gowin` (`gowin_path` in
  the platform files). Linux quirks handled inside the example `build()`
  functions: `LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libfreetype.so.6`,
  `LD_LIBRARY_PATH=$GOWIN/IDE/lib`, PATH prepend. The TOML→CSR tool
  (`serdes_toml_to_csr_60k.bin` etc., in `IDE/bin/serdes_toml_to_csr.dist/`)
  needs **absolute paths** (handled in `gowin_serdes/toml_gen.py`).
* Not a git repo at the time of writing (`git status` shows everything
  untracked; a `.gitignore` exists). **TODO: initial commit.**

## 3. Repository map

| Path | Content | State |
|---|---|---|
| `rtl/usb31phy/` | Decrypted vendor PHY, split per module (golden reference) | read-only reference |
| `gw_usb3/` | **The Amaranth PHY port** (16 modules) | done, fully verified |
| `tests/` | 100 tests, all passing (`pdm run test-all`, ~60 s) | green |
| `scripts/build_amaranth.py` | convert all components to Verilog (`build/amaranth/`) | works (`pdm run amaranth`) |
| `gowin-serdes/` | Python SerDes generator (Amaranth) + `usb3` recipe | verified against vendor artifacts (see §6) |
| `gowin-serdes/example/gw5ast-138/usb31-enum/` | Enumeration example, **Tang Mega 138K Pro** | **bitstream built**, not yet on hardware |
| `gowin-serdes/example/gw5at-60-dkusb/` | **DK_USB board platform** + enumeration example | elaborates; **full PnR never run** |
| `gowin-serdes/example/gw5at-15/` | eidle/csr_rw experiments (Slogic16U3) | USB example REMOVED — design cannot fit 15K (see §8) |
| `Gowin_USB3.1_UVC_BULK_RefDesign/` | Vendor reference design (controller netlists, descriptors, serdes.v/csr/toml, top.cst/sdc) | read-only reference / golden artifacts |
| `CUSTOMIZED/`, `Upar_Arbiter/` | Vendor pass-through SerDes wrapper + plaintext UPAR arbiter | used as golden references |
| `doc/` | USB 3.1/3.2 specs, PIPE spec, Link-Layer Test Spec, **DK_USB board guide** (all as markdown+tables) | reference |
| `gowin_timing_report.py` | parses Gowin PnR HTML reports (`--section`, `--paths`, `--json`) | works |
| `build/equiv/` | cocotb equivalence workdirs (auto-generated) | disposable |

## 4. The PHY port (`gw_usb3/`) — done

One `wiring.Component` per vendor module, generated from Python data instead
of line-by-line (8b/10b tables, GF(2) LFSR matrices, CSR tables from
`UparCsrConfig(pll, quad, lane, refclk)`, barrel/scan loops, `m.FSM()`s).
Externally-observable vendor quirks are reproduced on purpose and documented
in module docstrings; dead vendor code is dropped with notes.

Key parameters added beyond the vendor:

* `Usb31Phy(csr_config, sim_model=False, gen2=True, rate_init=1)`
  * `gen2=False`: omits the Gen2 128b/132b datapath (−3.2k LUTs). Gen2 SCD
    negotiation/rate-change still work; Gen2 *training* cannot → spec
    fallback to Gen1. Used by the 138K example.
  * `rate_init`: reset value of all rate synchronizers. Keep **1** when the
    SerDes CSR boots the 10G trim (vendor scheme, both examples); use 0 for
    a 5G-boot experiment so no spurious rate-change fires.
* `UparCsr(..., rate2_delay_bits=(18,19))` — vendor 2^18-cycle rate delay.
* Defaults = vendor behavior; the equivalence suite pins them.

## 5. Verification of the PHY — all green

Four layers (see `README.md` for detail):

1. `tests/test_static_tables.py` (10) — generated LFSR XOR networks == the
   vendor's hand equations; CSR tables (Q0_LN1@200M **and Q1_LN0@125M**,
   addresses *and* values) == vendor `elsif branches; 8b/10b symbol spot
   checks. NB the parser strips `//` comments (vendor keeps commented-out
   localparams that would shadow real values).
2. `tests/test_amaranth_sim.py` (10) — functional round trips (encode↔decode,
   scramble↔descramble, COM lock at every offset, SKP strip, FIFO, gearbox
   TX→RX, CSR rate sequence incl. the 2^18 delay).
3. `tests/test_equiv.py` (20 specs) — **golden + Amaranth side-by-side in
   one iverilog sim**, same stimulus, all outputs compared every cycle after
   warm-up. Golden compiled un-mangled from the real (non-MSIM) source via
   `` `getname(a,b) → a_gold`` include shim (`tests/equiv/harness.py`).
   Covers all leaf modules, `datapath`, `upar_csr` (full 262k-cycle rate
   change), the **complete `usb3_1_phy`**, and the **UPAR arbiter** (vendor
   `Upar_Arbiter/` vs `gowin_serdes.GowinUPARArbiter`). Seed-varied
   (`EQUIV_SEED=n`), waves via `EQUIV_WAVES=1` (FST in `build/equiv/*/sim`).
4. `tests/test_link_layer_spec.py` (48) — USB-IF Link-Layer Test Spec
   physical-layer tests recast for the PHY (TD.6.1/6.2/6.3/6.4/6.5, TD.7.42).

**Locked-in findings** (tests guard them):

* Vendor Gen2 block aligner **mis-tracks SKP OS with x=4 symbols**
  (TD.6.2 compliance gap; x=8..36 fine) — `test_td_6_2_gen2_skp_x4_vendor_gap`.
* Vendor LFPS detector false-detects sub-MHz toggles once its 6-bit counter
  saturates (harmless: its output is tied off in the shipped PHY).
* Vendor `datapath.SRC_VALID` uses a blocking assignment that races in event
  simulators; the port implements the synthesis-true flop and the datapath
  TB keeps the read clock slower than the write rate to stay out of the
  race window (`gw_usb3/datapath.py` comment).

Simulator pitfalls the harness handles (do not remove): warm-up for X-flush,
the 4ch-encoder RD_out_c X-lock deposit, `fix_t0_triggers()` for icarus
never waking constant-input `always @*` blocks.

## 6. gowin-serdes — verified & extended

The generator was *unproven*; it is now pinned to vendor truth:

* **UPAR arbiter**: cycle-exact vs `Upar_Arbiter/upar_arbiter.v` (cocotb,
  in the equivalence suite). Known deliberate divergence: a 2^19-cycle
  lockup-guard timeout (vendor can hang forever).
* **Lane↔quad wiring**: `tests/test_serdes_wiring.py` joins the reference
  `serdes.v` net-by-net (PHY↔GTR12_QUADA) and checks the generator port map
  *and* the `usb3.PHY_LANE_WIRING` table against it.
* **TOML**: byte-identical to the IDE-generated `serdes_tmp.toml` for the
  reference configuration (canonical IDE key ordering now lives in
  `toml_gen.py`; sections are reordered via `_reorder_section`).
* **CSR**: byte-identical to the shipped `serdes.csr`, including the two
  hand-appended vendor boot writes (TX AFE `0xA02` + **TX EIDLE = 1**, the
  reset state the PHY's CSR sequencer assumes).

Improvements made to the package (all upstream-able):

* `GowinSerDesGroup(toml_quad_overrides=...)`, `LaneConfig(toml_lane_overrides=...)`;
* `generate_csr(..., extra_writes=[(addr, data), ...])` + absolute paths;
* lane exposes full `status.astat[5:0]` and `status.rx_elecidle`;
* `cpll_reset_by_fabric` propagates to disabled lanes (shared POR net);
* **`gowin_serdes/usb3.py`** — the single source of truth:
  `usb3_lane_config()`, `USB3_QUAD/LANE_OVERRIDES`, `usb3_boot_writes()`,
  `make_usb3_serdes()`, `attach_usb3_phy(m, phy, lane, drp)` (table-driven,
  includes the deliberately **crossed fabric clocks**). Documented in
  `gowin-serdes/ARCHITECTURE.md`.

The PHY is the **only runtime CSR/DRP master**; boot registers come from
the `.csr` blob (bitstream-time), consistent with the PHY's reset state.

## 7. Enumeration example — architecture (both boards share it)

```
USB-C ── GTR12 lane (gowin-serdes, 10G boot trim, CSR from Python)
      ── gw_usb3.Usb31Phy (equivalence-proven)
      ── usb31_enum_core.sv shim
           ├─ vendor usb3_2_device_controller (pipe/ltssm/link .vg netlists
           │  + plaintext protocol/EP0/transfer-mem RTL, getname-mangled)
           └─ vendor UserLayer (ControlTransfer + UVC descriptors,
              EP2 video tied off — enumerates as VID 0x030A camera, no data)
      ── UART debug reporter (usb_debug.py, "upar" 62.5 MHz domain)
```

* The shim exists because the vendor modules use SV unpacked-array ports
  that Amaranth `Instance` cannot connect. It exposes flat ports only.
* `ControlTransfer.v` is packaged with patched `$readmemh` paths
  (descriptors land in `build/descriptors/`) and `../UVCDefine.v` fixed.
* `phy_pwrpresent` is tied 1 (no Type-C CC handling anywhere).
* UART protocol (115200 8N1): `U <8 hex>` status word (bit map in
  `usb_debug.py` docstring; bit5 = rate, bit12 = **attached/U0**) +
  `R bm bR wValue wIndex wLength` per SETUP — enumeration visible live.
* Rate strategy: LTSSM advertises Gen2 (frozen netlist); with
  `GEN2_DATAPATH=False` Gen2 training fails → per-spec Gen1 fallback. The
  10G→5G CSR reconfiguration runs on **every** Gen1 link-up (SerDes boots
  10G). **Bring up on a 5 Gbit host port first.**

### 7a. Tang Mega 138K Pro (`gowin-serdes/example/gw5ast-138/usb31-enum/`)

* Config: **Quad 1 Lane 0**, 125 MHz on Q1 REFCLK0 (user-confirmed;
  REFCLK1 = 100 MHz also possible — vendor tables support 100/125/200).
* `GEN2_DATAPATH = False` (fit/timing), `rate_init=1` default.
* **Bitstream built**: `build/usb31_enum.fs` (`python top.py`, ~7 min).
* Die quirks handled: no SSRAM on GW5AST-138 → vendor netlist `RAM16SDP*`
  instances renamed to register equivalents (`ram16sdp_lutram.v`),
  descriptor ROMs → `syn_ramstyle="registers"` (reads are registered, safe).
* **Timing** (C1/I0 slow corner, via `gowin_timing_report.py build`):
  Gen1-operation clocks close (pclk 125.7, rxclk 131.2 vs 125 required);
  the 156.25 MHz Gen2-boot window does **not** close (~126 MHz; worst
  offenders are vendor link reset fan-outs + statically-held Gen1 paths —
  analysis in the README). Treat Polling-at-10G-trim as best-effort.
* Caveat: board has a poor USB-C connector (user statement) — hence 7b.

### 7b. DK_USB GW5AT-LV60UG225 (`gowin-serdes/example/gw5at-60-dkusb/`)

The board the vendor reference design ships for (proper Type-C). New
platform file `dk_usb_gw5at60.py` (validated by `tests/test_dkusb_platform.py`
against the board guide tables **and** the vendor `top.cst`):

* Part `GW5AT-LV60UG225C2/I1`, family `GW5AT-60B`.
* Clocks: 24 MHz (H5), 200 MHz LVDS (K5/J5), `serdes_refclk_out` output
  pair (L9/K8) looped on the PCB to **Q0 REFPAD1** —
  `add_serdes_refclk_forward(m, platform)` reproduces the vendor
  TLVDS_IBUF→ELVDS_OBUF chain and returns the 200 MHz fabric clock.
* USB3 pairs (SerDes pads, in `SERDES_PINS`, never IO_LOC'd): TX1/RX1 =
  straight orientation = **vendor Q0 lane 1**; TX2/RX2 = flipped
  (vendor IP is single-orientation; board guide warns CC circuit unverified).
* Debug UART: `uart` 0 on MIPI J18 GPIOs, or `uart_j21` — TX on the J21
  header **SCL pin** (toggling SCL alone can't form an I2C START, so the
  FUSB302B/INA3221 on that bus stay idle; mutually exclusive with `i2c`).
* Example `usb31-enum/top.py`: **Q0 LN1, 200 MHz** — this is
  `UparCsrConfig()` *default*, the config every table is pinned against.
  Uses `make_usb3_serdes`/`attach_usb3_phy`/`usb3_boot_writes`. No netlist
  patches (GW5AT-60 has native SSRAM). LED = attached. `USB_PWR_EN` driven 0.
* `python top.py serdes` regenerates and **byte-compares** serdes.toml/csr
  against the reference design (currently: exact match, checked at every
  build too).
* State: elaborates (304 kB Verilog); **full Gowin synthesis/PnR NOT yet
  run** — next concrete step. The C2/I1 grade is what the vendor closes at
  160 MHz, so the 138K timing shortfall should shrink.
* `programmer_cable = "gwu2x"` is a **guess (UNVERIFIED)** — adjust for the
  actual on-board download circuit or use external JTAG (C15/D15/B15/E15).

## 8. Dead ends / decisions (do not re-litigate without new data)

* **GW5AT-15 (Slogic16U3) cannot fit the stack**: vendor link netlist alone
  is 10.3k LUTs; netlists ≈ 13.8k + PHY ≥ 2.4k (Gen1-only) + protocol > 15.1k
  device. Example dir was removed. Options if ever revisited: replace the
  vendor link/LTSSM entirely (big) or constant-prop Gen2 out of the
  netlists via `speed=0` in the plaintext wrapper (untried).
* Full-PHY equivalence must use the **non-MSIM** golden (`getname→_gold`):
  the vendor MSIM variant has a wire/reg bug and structural differences.
* SDC on these boards: **do not** `create_clock` on hard-macro pins with
  paths that don't exist post-PnR; either use the auto-detected clock names
  (`get_nets {serdes_pcs_tx_clk_i}` worked on the 138K after checking the
  synthesized netlist) or leave empty and review with `gowin_timing_report.py`.

## 9. How to run everything

```console
pdm run test-fast     # static + amaranth-sim + fast equivalence (~35 s)
pdm run test-all      # + datapath/upar_csr/full-PHY equivalence (~60 s, 100 tests)
pdm run amaranth      # emit all PHY modules to build/amaranth/

EQUIV_SEED=7 pdm run pytest tests/test_equiv.py -k rxgears   # one DUT, other seed
EQUIV_WAVES=1 ...                                            # record FST

# 138K example (bitstream + timing)
cd gowin-serdes/example/gw5ast-138/usb31-enum
python top.py            # → build/usb31_enum.fs
python top.py program
python ../../../../gowin_timing_report.py build --section fmax --section setup-slack

# DK_USB example
cd gowin-serdes/example/gw5at-60-dkusb/usb31-enum
python top.py serdes     # regenerate + byte-compare serdes.toml/csr vs reference
python top.py            # TODO: first full build (see §10)
```

## 10. Next steps (ordered)

1. **DK_USB: run the full Gowin build** (`python top.py`) — expect possible
   small platform/TCL fixes on first run (the 138K needed the freetype
   preload, `.vg` template iteration, SDC iteration — all already in the
   platform copy here, but PnR was never exercised for this part). Then
   `gowin_timing_report.py build` and compare against the vendor's 160 MHz
   expectation.
2. **Hardware bring-up on DK_USB** (5 Gbit host port first): watch UART —
   healthy sequence: cpll_ok → rx-detect pulses (PowerDown=2 window) →
   training → rate bit drops to 0 → attached=1 → burst of `R 80 06 ...`
   lines → `lsusb` shows VID 0x030A. LED = attached.
3. If Polling misbehaves at the 10G boot trim: try `boot_rate="5G"` +
   `Usb31Phy(rate_init=0)` (recipe supports it; LTSSM will still emit SCD,
   but the SerDes never leaves the proven-in-eidle 5G trim). This
   configuration is expressible but **untested**.
4. Once Gen1 enumerates: flip `GEN2_DATAPATH = True` (equivalence-proven
   datapath) and chase Gen2 on the C2/I1 board.
5. Nice-to-haves: commit to git; upstream the gowin-serdes improvements;
   real CC/orientation handling (FUSB302 driver) instead of pwrpresent=1;
   EP2 bulk data source to exercise streaming after enumeration.

## 10a. Update 2026-08-26 — DK_USB bench debug verified

* **Two debug UARTs** hand-wired to the J18 MIPI connector (FT4232H "Quad
  RS232-HS"): `uart` 0 = channel C = `/dev/ttyUSB4` (FPGA RX G5, TX H12),
  `uart` 1 = channel D = `/dev/ttyUSB5` (FPGA RX H15, TX J15).  Polarity
  was determined on hardware (auto-detect probe in
  `~/Downloads/TangMegaPro/luna_softphy_example/uart_probe_dk60.py`); the
  platform file's former `uart` 0 pin directions were **reversed** and are
  now fixed; `uart` 1 added.  115200 8N1, both directions byte-exact.
* **Programming verified**: the board's Mini USB-B download port is an
  FT232H (`/dev/ttyUSB1`) — `openFPGALoader -c ft232 <fs>` works (the old
  `programmer_cable = "gwu2x"` guess is gone; platform now uses `ft232`
  with a `sudo -n` fallback).
* **First full Gowin PnR on this platform**:
  `gowin-serdes/example/gw5at-60-dkusb/uart-hello/` (LED heartbeat +
  banner/echo on both UARTs) — built clean on the first run, timing
  233 MHz vs 24 MHz required, flashed, and verified live on both ttys.
  Next-step item §10.1 (usb31-enum full build) is now de-risked on the
  platform/toolchain side.
* `usb31-enum/top.py` debug output now defaults to `UART_RESOURCE =
  "uart"` (ttyUSB4) instead of the J21/SCL hack.
* The host bench: board Type-C is on a 10 Gbit host port; HANDOVER §7
  still recommends first bring-up on a 5 Gbit port if Polling misbehaves.

## 10b. Update 2026-08-26 (late) — DK_USB USB3 ENUMERATES AT GEN2

`usb31-enum` on the DK_USB now enumerates as **SuperSpeed Plus Gen 2x1
(10 Gbit) `030a:0301 Gowin UVC`** on a real host.  Root causes found via
two A/B experiments (vendor prebuilt `prj/impl/pnr/prj.fs` = working
control; a "hybrid" build = vendor project with ONLY the PHY swapped for
our Amaranth port, see `Gowin_USB3.1_UVC_BULK_RefDesign/hybrid/run/`,
which also enumerated at Gen2 — proving the PHY and blaming the
integration):

1. **Reset ordering was inverted.**  The old top released `phy_resetn` at
   1.3 us and the quad `por_n` at 1.3 ms; the PHY's one-shot CSR init
   writes (CDR/FFE/TX trims) landed while the quad was still in POR and
   were lost.  Rx-detect and rate changes still worked (runtime writes),
   so the LTSSM limped: host LFPS was visible but never answered
   correctly.  Vendor order (top.sv): base reset ~1.3 us -> por_n
   ~330 us -> PHY **last** (~1.3 ms, vendor gates it on pll_init lock).
2. **`GEN2_DATAPATH = False` is not viable against a Gen2 host.**  The
   LTSSM netlist always advertises Gen2; Polling.PortMatch (LTSSM state
   12) wedges without the Gen2 datapath signals.  With `gen2=True` the
   design trains and enumerates at Gen2 directly (and timing still
   closes).

Supporting discoveries (all encoded in the platform/example):

* **`set_option -enable_dsrm 1`** (in the vendor project's OptionList):
  DSRM = distributed SRAM.  GW5AT-60B *has* SSRAM; without this option
  the IDE reports RP0007 "no SSRAM resource", which had been misread as
  a die limitation (the 138K RAM16SDP register workaround came from the
  same misreading — recheck the 138K with this option!).  Reverting the
  register workaround also fixed pclk timing (descriptor ROM muxes back
  to LUT-RAM).
* **The GTR12 "life clock" (upar/DRP) is an unstable ring oscillator**,
  measured 56..118 MHz (ClockFreqProbe).  Never clock a UART from it;
  the vendor's 10 ns SDC constraint is a bound, not a rate.  Debug now
  runs on the 24 MHz oscillator.
* Vendor-style SDC: every clock in its own async group; MCPs declared
  for the protocol-stable ControlTransfer SETUP latches and the
  controller `speed` fanout.  All clocks close including the 156.25 MHz
  Gen2 window.
* Amaranth DiffPairs emit per-pin constraints that Gowin PnR rejects
  (CT1000); the platform now rewrites the cst to the vendor convention
  (`IO_LOC "x__p" P,N;`, N side unconstrained).
* USB2 pins must be requested and quieted (pullup_en=0 etc.), otherwise
  the host sees a phantom low-speed device and power-cycles the port
  mid-training.
* Board KEY = full POR replay (LTSSM recovery without reflash).
* Debug: uart0/ttyUSB4 = status reporter with **LTSSM state in bits
  [21:16]** (state names in `usb3_const.vh`: 10=Polling.LFPS,
  12=PortMatch, 16=Polling.Active, 19=U0, 23=Compliance); uart1/ttyUSB5 =
  clock-frequency probe + PIPE ordered-set/LFPS counters.  The vendor
  controller exposes `ltssm_state[5:0]` via a build-time patch.

## 10c. Update 2026-08-27 — LUNA-on-our-PHY: Phase 2 started (sim PASSING)

Goal: replace the vendor LTSSM/link/protocol netlists with LUNA's open
SuperSpeed stack on top of our hardware-proven PHY.  Work lives in the
`luna/` clone (greatscottgadgets/luna, amaranth 0.5, includes the
SuperSpeed + serdes_phy work).  `usb-protocol` added to the pdm deps.

Done (all in `luna/`):

* `luna/gateware/interface/pipe.py`: `PIPEInterface` extended to
  **width=8 (64-bit)** + PIPE 4.x block-coding signals (`tx/rx_datavalid`,
  `tx/rx_sync_header`, `tx/rx_start_block`).  Our PHY's Gen1 geometry
  (32-bit @ 125 MHz in data[31:0]/K[3:0]) matches LUNA's internal
  32-bit stream layer with no gearing; the upper half is the Gen2 block
  payload.
* `luna/gateware/interface/serdes_phy/gowin_gtr12.py`:
  **GowinGTR12PIPE** adapter wrapping `gw_usb3.Usb31Phy` (gen1 defaults:
  `gen2=False`, `rate_init=0` -- needs a 5G-boot CSR blob on hardware,
  semi-proven by the eidle experiments).  Handles the dialect deltas:
  * `rate`: LUNA/TUSB drives 1 for 5G; Gowin encodes 0=5G -> tied 0.
  * **LFPS TX dialect**: LUNA requests bursts as (P0, TxElecIdle=1,
    TxDetectRx=1); the Gowin PIPE uses PIPE-3.0 low-power signaling
    (drop TxElecIdle in P2 for the burst duration -- confirmed both from
    the vendor pipe FSM source and the hardware LTSSM trace).  Adapter
    translates combinationally; PHY's burst engine shapes the waveform
    and does the per-burst eidle CSR writes.  Spurious PhyStatus pulses
    from the P0<->P2 hops are ignored by LUNA (only its reset controller
    consumes phy_status).
  * `phy_status`: Gowin PHY emits event *pulses*; LUNA expects the TUSB
    startup *level* -- synthesized (high until first pulse with PLL
    lock, then pulse passthrough).
  * LUNA never uses PIPE rx-detect (VBUS shortcut via power_present=1).
* `luna/examples/usb/superspeed/gowin_gtr12_sim.py`: smoke sim of
  LUNA physical+link on the real (non-sim-model) PHY with the CSR
  sequencer running against a UPAR slave stub.  **PASSES**: ready @510,
  Polling @512, LFPS bursts (1 us / 10 us textbook rhythm) with real
  UPAR eidle/FFE writes @1876.
  * Stub gotcha (also relevant to any future UPAR model): `ready` must
    idle LOW; a constant-high ready collapses the sequencer's wren to
    zero cycles (same-cycle override) and no bus transaction appears.
  * `sim_model=True` is NOT usable for LFPS tests: the FFE/eidle acks
    only exist with the real sequencer.

Next steps (Phase 2 continuation, then Phase 3):

1. RX-direction sim: drive host-side LFPS (toggle `serdes_astat_i[5]`
   with burst timing while no RX symbols flow) and check LUNA's LFPS
   detector sees Polling.LFPS via our RxElecIdle mux (~10 us onset
   latency after TX quiet -- see 10b; LUNA timer tolerances to verify).
2. Loopback-ish training sim: feed our PHY's encoded TX back into the
   RX decoder path (serdes_rxdata_i) to exercise TS1/TS2 through LUNA.
3. Hardware `luna-enum/` example on the DK_USB platform: gowin-serdes
   lane via `attach_usb3_phy(m, adapter.phy, lane, drp)`, 5G-boot CSR
   (`GowinUsb3SerDes(boot_rate="5G")` + relax the byte-pin check),
   same POR ordering as usb31-enum (quad POR ~330 us before releasing
   LUNA+PHY), debug UARTs with a LUNA LTSSM state tap.
4. Keep `usb31-enum` (vendor LTSSM, enumerates at Gen2) as the on-board
   A/B baseline.

## 10d. Update 2026-08-27 (late) — LUNA phases 2+3 executed; Gen1-TX open item

Simulation (both PASS, in `luna/examples/usb/superspeed/`):

* `gowin_gtr12_sim.py` — smoke: LUNA drives the PHY into Polling.LFPS
  with real per-burst eidle/FFE CSR writes.
* `gowin_gtr12_training_sim.py` — full raw-symbol training to
  **link.trained (U0)** against a scripted host partner (TS ROMs through
  the PHY's own 8b/10b encoder into the 88-bit serdes RX format from
  `tests/equiv/tb/tb_usb3_1_phy.py`; LUNA's Scrambler reused for the
  logical-idle phase, LFSR synced via COM).  LUNA's
  `TSTransceiver`/`USB3LinkLayer` gained a `tseq_burst_length` parameter
  (spec 65536; sims shorten).

Hardware (`gowin-serdes/example/gw5at-60-dkusb/luna-enum/`, builds clean,
all clocks close at 125 MHz):

* 5G-boot CSR blob works (pclk = 125 MHz from power-on) BUT its TX was
  fully host-invisible.  Superseded by **BOOT_RATE="10G"**: byte-pinned
  blob (build-verified identical to usb31-enum's) + the adapter's
  `boot_rate_switch` runs the hardware-proven 10G->5G rate change before
  reporting PHY-ready (LUNA only ever sees a 125 MHz Gen1 PHY).
* Fixed en route: luna-enum passed the refclk source as a *string*
  ("REFPAD1") instead of `RefClkSource.Q0_REFCLK1`, silently generating
  a blob with `ref_pad1_freq="0M"` (CDR calib error at csr-gen time).
* **LUNA bug found & fixed** (`link/layer.py`): `can_send_skp` was only
  asserted during logical idle -- NO SKP ordered sets during
  TSEQ/TS1/TS2 bursts [USB 3.2r1 6.4.3.1].  Now also asserted while an
  ordered set's *first* word is presented (the CTC inserter holds that
  word, so SKPs land between sets).  Required regardless of the open
  item below.
* Debug taps added: `USBSuperSpeedDevice.debug_*` (phy_ready,
  send/detected LFPS, engage_terminations, ts1/ts2_detected).

Hardware results (link probe, /dev/ttyUSB4, fresh host port per attempt):

* LFPS handshake completes both directions (~200 detected cycles).
* Terminations engage; LUNA transmits TSEQ+TS1 bursts (millions of
  symbols); **host TS1s are received and recognized: `ts1_detected`
  ~285k per attempt** -- the entire RX chain (GTR12 5G trim, alignment,
  8b/10b, elastic buffer, PIPE, LUNA CTC/aligner/detectors) is
  hardware-proven, including full-rate continuous decode (host CP1 at
  100% of cycles).
* **`ts2_detected` = 0 always: the host never recognizes OUR TS1s.**
  After 360 ms LUNA parks in SS.Disabled (per spec; KEY replays POR).

### The open item, precisely characterized

Our **Gen1 (5 Gbps) transmit path has never been decoded by the host
under ANY stack**: the vendor-LTSSM Gen1-fallback attempts in every
earlier capture show the same signature (host polls, our TS bursts
unanswered), while Gen2 enumerates perfectly (usb31-enum, hybrid,
vendor prj.fs).  Stack-independent => suspects are the gw_usb3 TX path
at the 5G trim, the gowin-serdes fabric-TX wiring in 20-bit/1:2 gear
mode, or the 5G trim itself on this board -- none ever hardware-proven
at Gen1 (equivalence only proves logic vs vendor RTL; the vendor design
never uses Gen1 on this board either).

**RESOLVED to a pinpoint (2026-08-27, 5 Gbit hub-port test):**

| stack                                   | Gen2 (10G port) | Gen1 (5G port) |
|-----------------------------------------|-----------------|----------------|
| vendor PHY + vendor serdes (prj.fs)     | enumerates      | **enumerates** |
| our PHY + vendor serdes (hybrid.fs)     | enumerates      | **silent**     |
| our PHY + our serdes (usb31-enum/LUNA)  | enumerates      | fails          |

=> **the bug is in gw_usb3's Gen1 (5G) TX path** -- board, trim and
gowin-serdes are exonerated (the vendor bitstream enumerates at plain
SuperSpeed 5 Gbps on a 5000M hub port instantly; a known-good Gen1
baseline now exists on this very board).  The equivalence suite passes,
so the divergence is a blind spot of the harness (initialization, an
unexercised gearing phase state, or output-timing-sensitive behavior of
the TX fabric interface), not RTL-visible logic.

Next-session discriminators, in order of leverage:

1. **Sub-block swap bisect in the hybrid**: replace our PHY's Gen1 TX
   blocks (encode_8b10b_4ch, TX gearing/fifo write logic) with the
   vendor's decrypted split modules (`rtl/usb31phy/*.v`) one at a time;
   each hybrid rebuild ~13 min on the 5G port converges in 2-3 steps.
2. **Serdes-level loopback at 5G** (PIPE loopback command = P0 +
   TxDetectRx without elec idle -> CSR LOOPBACK_MODE) while streaming
   TS1s; our own hardware-proven TS1 detector as the judge.  Detections
   => TX bitstream well-formed (points at eidle/FFE interplay);
   silence => TX gearing/packing/phase bug.
3. Diff FF init values / netlist structure of the TX path: our emitted
   `amr_*` Verilog vs the vendor `usb3_1_phy.v` netlist (TX gearing
   phase FFs are prime suspects -- a wrong half-word phase at gear 1:2
   produces a 10-bit-rotated, undecodable stream).

The vendor prj.fs is left flashed on the board (Gen1-enumerated,
device on the 5G hub port) as the working baseline.

## 10e. Bench + operations cheat-sheet (for the Gen1 TX bisect)

Physical state as of 2026-08-27 01:00:

* Board USB-C is on a **5 Gbit hub port** (host sees it as ``usb 4-8.2``;
  a Gen1-only link -- the decisive test environment).  The 10 G root
  ports used earlier: ``4-2`` and ``4-9``.
* **Vendor ``prj.fs`` is flashed** and enumerated at Gen1
  (``lsusb -d 030a:`` -> ``030a:0301 Gowin UVC``; dmesg says plain
  ``new SuperSpeed USB device`` -- "Plus Gen 2x1" would mean a 10G port).
* Serial map: ``/dev/ttyUSB1`` = FT232H = JTAG
  (``sudo -n openFPGALoader -c ft232 <file.fs>``, passwordless sudo
  works); ``/dev/ttyUSB4``/``ttyUSB5`` = debug UARTs (only used by OUR
  bitstreams; the vendor/hybrid images have no UARTs).
  **One reader per tty at a time** -- a second ``cat`` steals bytes and
  corrupts both captures.
* Host-side check loop (~10 s after flashing):
  ``sudo -n dmesg -C; sudo -n openFPGALoader -c ft232 X.fs; sleep 8;``
  ``dmesg | grep -iE 'SuperSpeed|030a|Cannot'; lsusb -d 030a:``
* Hosts err-disable a port after repeated failed training: when in
  doubt ask for a physical replug.  Our own tops park in SS.Disabled
  (LUNA) after 360 ms -- board KEY = full POR replay (our tops only;
  the vendor top has its own key logic).

Hybrid build (``Gowin_USB3.1_UVC_BULK_RefDesign/hybrid/run/``):

* ``build.tcl`` = vendor project file list with ONE swap: our PHY
  (``usb31_phy_amaranth.v``, module ``USB3_1_PHY_Top``) instead of the
  encrypted ``$SRC/serdes/usb3_1_phy/usb3_1_phy.v``.  Local
  ``top_hybrid.sdc`` retargets one rx-clock constraint to
  ``SerDes_Top_inst/q0_lane1_pcs_rx_o_fabric_clk`` (our passthrough
  assign gets collapsed).  ``set_option -enable_dsrm 1`` is required.
  ``impl/project_process_config.json`` carries the PnR options.
* Rebuild (~13 min):
  ``cd Gowin_USB3.1_UVC_BULK_RefDesign/hybrid/run &&``
  ``LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libfreetype.so.6``
  ``LD_LIBRARY_PATH=$HOME/Downloads/gowin/IDE/lib``
  ``PATH=$HOME/Downloads/gowin/IDE/bin:$PATH gw_sh build.tcl``
  -> ``hybrid.fs``.  License check is flaky: just re-run.
* Our PHY emit (what produced ``usb31_phy_amaranth.v``):
  ``verilog.convert(Usb31Phy(gen2=True, rate_init=1),
  name="USB3_1_PHY_Top")`` + ``tests.equiv.harness.fix_t0_triggers``,
  from the workspace root with ``pdm run``.

Bisect raw material:

* ``rtl/usb31phy/`` = the **decrypted vendor PHY RTL, split per module**
  with ``usb31phy.filelist`` (build order).  CAUTION: do NOT define
  ``MSIM`` for synthesis -- it selects *behavioral sim variants* via
  ifdefs, not just plain names.  Child modules are name-mangled via the
  ``getname()`` macro (``usb3_1_phy_name.v`` sets
  ``module_name = USB3_1_PHY_Top``); to swap one child, string-patch
  the *instantiation site* in its parent at build time (the technique
  used throughout this project) and add a wrapper module around our
  emitted ``amr_<name>``.
* ``scripts/build_amaranth.py`` emits every component as
  ``build/amaranth/amr_<name>.v`` -- port-compatible with the vendor
  split modules by construction (that is what ``tests/equiv`` runs).
* Equivalence spec inventory (tests/equiv/specs.py): async_fifo,
  datapath, dc_balance, decode_8b10b(_4ch), elastic_buffer,
  encode_8b10b(_4ch), p132brxgears_v6, p132btxgears, pulse_detect,
  upar_arbiter, upar_csr, usb3_1_descramble, usb3_1_lfsr, usb3_1_phy,
  usb3_1_scramble, usb3_lfps_detector_v2, usb_pipe_interface,
  word_alignment.

gw_usb3 Gen1 (5G) TX path, in signal order (the suspect list):

1. ``gw_usb3/pipe_interface.py`` -- P0 data steering (``data_sel``),
   LFPS pattern states, ``RxData -> tx_data_encode_i`` handoff;
2. ``gw_usb3/encode_8b10b.py`` -- ``Encoder8b10bMulti(4)``: vendor
   disparity topology (lane0 chains from the *registered* disparity of
   the previous word);
3. ``gw_usb3/phy.py`` TX section -- 4x10-bit -> serdes 20-bit/gear-1:2
   packing, ``serdes_fabric_tx_vld_o`` cadence, TX fifo write logic and
   ``serdes_tx_fifo_wrusewd_i`` handling, ``serdes_pcs_tx_rst_o``;
4. (``dc_balance.py`` / ``async_fifo.py`` -- Gen2/RX-heavy, low
   priority).

A "hybrid-from-split-RTL" baseline (all-vendor PHY built from
``rtl/usb31phy`` instead of the encrypted file) MUST be validated at
Gen1 first -- it proves the split RTL + naming scheme is sound before
any swap is trusted.

## 10f. Update 2026-08-27 (session 3) — Gen1 TX bug FOUND & FIXED

**Root cause: GowinSynthesis V1.9.12.03 mis-infers a BSRAM `pROM` from
the Amaranth-emitted 8b/10b encoder tables and produces a functionally
WRONG netlist.**  Not an RTL bug — every iverilog equivalence test
passes because the corruption is introduced at synthesis.  The vendor
PHY synthesizes all of its tables to plain LUTs (zero BSRAM in the
whole PHY; the only design pROMs are in `PLL_INIT`).

How it was found (each step verified on the 5 G hub port, `usb 4-8.2`):

1. Sanity anchors: vendor `prj.fs` re-enumerated Gen1; `hybrid.fs`
   silent.  Loop validated.
2. **Split-RTL baseline** (`hybrid/run/build_split.tcl` → `split.fs`):
   all-vendor PHY built from `rtl/usb31phy` **enumerates Gen1** — the
   split RTL + getname scheme is sound.  NB: with the split RTL the
   `q0_lane1_fabric_rx_clk` alias net survives synthesis, so the build
   uses the vendor `top.sdc` (targeting the *pcs* net instead is a
   TA2003 PnR **error**, not a warning).
3. **Bisect hit on the first swap** (`build_swap.tcl` + `make_swap.py`,
   swap = `encode_8b10b_4ch`): vendor PHY + our encoder = **silent at
   Gen1**.  Same build with `syn_romstyle="logic"` on the emitted
   encoder modules = **enumerates Gen1** (A/B/A complete).
4. Netlist forensics (`/tmp/kilo` scratch, technique reproducible):
   per-lane the tool built `pROM` (sync read, addr = {k28, RD,
   din[4:0]}) + a bizarre DFFRE/LUT3 hold-feedback; pROM INIT content
   read back via `prim_sim.v` differs from the 5b6b table at 37 of 66
   reachable words, and a post-synthesis netlist-vs-golden cocotb sim
   mismatches on every resolvable cycle (b6 groups stuck ~0).  Decoder
   is NOT affected (0 BSRAM even unannotated) — which is why RX always
   worked.  Timing was ruled out first: at Gen1 (125 MHz, 8 ns) every
   pclk/rx path meets timing in all failing builds; the 160 MHz SDC
   FAILs are the same protocol-stable classes the working builds have.

The fix (all in-tree):

* `gw_usb3/synthesis.py` — `gowin_compat()` /
  `force_logic_romstyle()`: appends `/* synthesis syn_romstyle =
  "logic" */` to every emitted `module` header.  Applied in
  `scripts/build_amaranth.py`, `scripts/build_hybrid_phy.py` (NEW —
  regenerates `usb31_phy_amaranth.v`), and both example platforms
  (`dk_usb_gw5at60.py::_apply_gowin_compat`, 138K
  `usb31-enum/gw5ast_dvk.py`) which post-process `plan.files[name.v]`.
* `gw_usb3/phy.py` — the resettable domains (`p`, `rxi`, `u`) are now
  **async-reset** like every vendor reset (`always @(posedge clk or
  negedge rst_n)`).  Matters when the recovered clocks pause during
  the CPLL retune; also makes the new rate-change equivalence test
  cycle-exact (previously 1 cycle of divergence at the pll-drop edge).
* New regression tests (suite now 103):
  * `tests/equiv/tb/tb_usb3_1_phy_ratechange.py` +
    `test_equiv_phy_ratechange` — live 10G→5G rate change with CPLL
    dip, then 5G TX incl. TS1-like K-framing and LFPS excursions
    (the old tb drove `Rate=0` statically — the blind spot).
  * `tests/test_gowin_synthesis.py` — runs real GowinSynthesis on the
    emitted encoder/decoder (seconds; auto-skips without the IDE) and
    asserts **no BSRAM primitive** in the netlist.  Without the
    annotation the encoder infers 4 pROMs — the test catches exactly
    the failure class.

Verified ladder, ALL RUNGS GREEN (5 G hub port `usb 4-8.2` unless
noted; 10 G root port = `usb 4-9`):

* vendor `prj.fs` Gen1 ✓ (anchor); broken `hybrid.fs` silent ✓ (anchor)
* `split.fs` (all-vendor split RTL) Gen1 ✓
* `swap_encode_8b10b_4ch.fs` without fix: silent ✗ (bisect hit);
  with `syn_romstyle="logic"`: Gen1 ✓ (A/B/A)
* **`hybrid.fs` (FULL Amaranth PHY, fixed): Gen1 ✓ — mission goal**
* **`usb31-enum` (our PHY + our serdes, fixed): Gen1 ✓** — the
  previously-failing full-own-stack Gen1 now enumerates `030a:0301`
  as plain SuperSpeed on the 5 G hub port
* `hybrid.fs` Gen2x1 ✓ and `usb31-enum` Gen2x1 ✓ on the 10 G port
  (no regression from the fix)
* **`luna-enum`: `link_trained=1` and `1209:0001` "GTR12 SuperSpeed
  bring-up / LUNA + gw_usb3" enumerates at Gen1 on the 10 G root
  port ✓✓** — LUNA LTSSM + our PHY + gowin-serdes trained to U0 on
  hardware.  The §10c/§10d roadmap resumption point is REACHED
  (next: endpoints, Gen2-through-LUNA later).

luna-enum caveat: on the 5 G *hub* port it still parks — LUNA
completes its side of the LFPS handshake and pumps ~60 M TSEQ/TS1
symbols, but that hub's port never leaves Polling.LFPS
(`rx_elec_idle` stays 1 through our TS1 flood, host sends no TS1s,
probe: `lfps_det` counts for ~1 s then everything stops).  A/B'd
against a sync-reset PHY build: identical → NOT caused by the fix;
hub-port-specific LFPS interaction (vendor LTSSM stacks enumerate on
that hub fine).  Investigate with the hub if it matters.  Also note:
the 10 G root ports are USB-C with two orientations and the vendor
IP is single-orientation — if a known-good image is silent on a root
port, flip the plug before debugging.

Bench state at session end: board on the 10 G root port (4-9),
`luna_enum.fs` flashed and ENUMERATED (`1209:0001`).  Vendor `prj.fs`
untouched as the restore baseline.  One flash quirk seen: an
openFPGALoader run reported DONE but the old bitstream kept running
(uart still printing the previous design's reporter) — reflash and
check the uart format if a verdict looks impossible.  Bisect
scaffolding kept in `hybrid/run/`: `build_split.tcl`,
`build_swap.tcl`, `make_swap.py`, `patched/` (swap name in
`patched/SWAP_NAME`), per-variant logs `build_*.log`.  Suite: 103
tests green (`pdm run test-all` + `tests/test_gowin_synthesis.py`).

## 10g. Update 2026-08-27 (session 4) — CDC-ACM echo: datapath validated,
## seven LUNA SS bugs found; sustained streaming still deadlocks

Goal: go beyond enumeration — a ttyACM echo device to validate the bulk
datapath through LUNA + gw_usb3 at Gen1.  New example:
`gowin-serdes/example/gw5at-60-dkusb/luna-acm/` (CDC-ACM descriptors,
EP1 bulk OUT→IN loopback, EP2 idle notification endpoint, minimal CDC
class-request handler, IN-ladder debug probes on uart1).  LUNA has no
SS OUT endpoint upstream: `luna-acm/ss_stream_out.py` implements
`SuperSpeedStreamOutEndpoint` (single-buffered, ACK-after-drain,
sequence tracking, retry on CRC error / wrong sequence — its FSM is
provably idle until U0 so the 156 MHz boot window cannot corrupt it).

**Validation achieved (10 G root port, Gen1):**
* enumerates; `cdc_acm` binds `/dev/ttyACM0`; CDC class requests
  ({GET,SET}_LINE_CODING, SET_CONTROL_LINE_STATE) handled — clean dmesg;
* **raw bulk echo is repeatable in BOTH directions** (pyusb, kernel
  driver detached): OUT 8B → IN readback OK, and the NRDY→park→
  ERDY→resume flow works (`/tmp/kilo/raw_bulk_test.py` phases A/B/C);
* tty echo (46-byte string) demonstrated end-to-end, but is
  INTERMITTENT: cdc-acm keeps ~16 read URBs pending, and the resulting
  pipelined-token pattern still hits unfixed races;
* sustained multi-packet streaming (8 KB+) deadlocks after a varying
  number of packets.

**Seven upstream LUNA SS bugs found and fixed along the way** (all in
`patches/luna_gowin_adapter.patch`, upstream-candidates):
1. `protocol/transaction.py` — ERDY dispatch typo: `send_erdy` entered
   the SEND_**NRDY** state; ERDY was never sent (host parks forever).
2. `protocol/endpoint.py` — handshake mux dropped requests: gating
   covered only ack|stall (NRDY/ERDY never forwarded), and colliding
   single-cycle strobes lost one handshake → pipe deadlocks.  Replaced
   with a two-tier arbiter: zero-latency comb fast path (preserves the
   original same-cycle dispatch contract) + edge-latched backup with
   done-ownership tracking, self-healing empty-grant release, watchdog.
3. The SET_ADDRESS status ACK must be generated in the SAME cycle the
   handler strobes it — one cycle later and the generator samples the
   NEW device address, the host discards the misaddressed ACK and
   enumeration dies ("Device not responding to setup address").  This
   is why the fast path in (2) exists; discovered the hard way.
4. `endpoints/stream.py` — SEND_PACKET dropped the final word of every
   DP when the transmitter back-pressured (header still in the queue
   arbiter): payload shorter than the header's data_length → host
   -EPROTO.  Added FINISH_LAST_WORD hold state.
5. `link/data.py` — DataPacketTransmitter offered the DPH one cycle
   before the payload was staged; an idle transmitter samples
   `data_sink.valid==0` at header-accept and emits a "ZLP" whose header
   claims N bytes → -EPROTO.  Header now gated on staged payload.
6. `endpoints/stream.py` — the just-ACKed buffer was recycled as the
   write buffer with a stale `stream_ended` flag → fill side refuses
   all further data (pipeline freeze).  Both count and flag now clear.
7. `endpoints/stream.py` — unanswered token credit: an ACK that doubles
   as the next IN token (NumP>0) with nothing buffered was silently
   consumed (host times out -EPROTO ~35 ms); same for a token crossing
   REQUEST_IN_TOKEN.  Both now answered (NRDY / immediate dispatch).
   Also added `generate_zlps=False` option (echo marks `last` per
   packet; ZLP-per-max-packet is pure overhead).

**Also:** the luna builds had NO SDC (the platform gated constraints on
`name == "usb31_enum"`) — Gowin silently applied a 100 MHz default goal
while pclk runs 156.25/125 MHz.  luna-enum passed by luck; the platform
now constrains luna_enum/luna_acm (6.4 ns pclk/rxclk + async groups).
`protocol/endpoint.py` additionally registers the handshakes_in
broadcast once, centrally — the header-RX→TP-decode→endpoint-FSM→
tx-params cone was 9.5 ns.  After all fixes: pclk Fmax 130 MHz (>125
operating; the 156 MHz boot window only clocks reset-held/idle LUNA
logic, same risk envelope luna-enum always had).

**Remaining (next session):** sustained-streaming deadlocks — at least
the IN endpoint's ping-pong commit (no "read buffer free" guard:
commits toggle onto an unACKed read buffer under load) and suspected
further token/flow races under cdc-acm's pipelined URBs.  STRATEGY:
stop hardware whack-a-mole; build a host-model simulation at the
header/payload-queue level (drive tokens/ACKs/OUT-DPs against
USBSuperSpeedDevice, run the 8 KB echo in sim) and harden until clean —
each of bugs 1-7 would have been caught by such a sim.  Debug assets:
`/tmp/kilo/raw_bulk_test.py` (pyusb A/B/C discriminator),
`/tmp/kilo/acm_echo_test.py` (tty integrity/throughput), usbmon
(`-71 EPROTO` = malformed response; `Set TR Deq Ptr` warnings = wedged
endpoint rings), luna-acm uart1 IN-ladder probe (tokens/NRDY/ERDY/
tx-words/echo-words + sticky flags).

Bench state at session end: board on the 10 G root port (4-9),
luna-acm (build_acm14, all fixes) flashed; the port survived heavy
error traffic — if a known-good image stops enumerating, replug.
gw_usb3 test suite: 103/103 green (nothing in gw_usb3 changed this
session — all findings are LUNA-side).

## 10h. Update 2026-08-27 (session 5) — bulk loopback bandwidth: 23-25 MB/s
## per direction sustained; concurrency envelope = 2 packets in flight

Goal: a bandwidth test via an IN/OUT loopback device + libusb.  New
example `gowin-serdes/example/gw5at-60-dkusb/luna-loopback/`: bare
vendor-class device (no kernel driver; pyusb claims it directly),
EP1 bulk OUT -> EP1 bulk IN echo, same SS OUT endpoint as luna-acm.

**Method that finally converged: endpoint-layer simulation with a USB3
host model** (`luna-loopback/sim_loopback.py`): OUT/IN driver
coroutines + an every-cycle monitor drive the real endpoint pair +
mux + TP generator with tokens/ACKs/NRDY/ERDY at NumP=1, byte-check
the echo, and dump event traces + windowed cycle traces
(TRACE_LO/TRACE_HI env) on deadlock.  It reproduced every functional
bug deterministically in seconds and now PASSES 64 KiB (across the
5-bit sequence wrap) at ~165 MB/s endpoint-layer.

**Bugs found & fixed this session** (patch + ss_stream_out.py):
8. `endpoints/stream.py` WAIT_FOR_ACK: the plain "nothing more
   buffered" arm never asserted `advance_sequence` -- every packet
   after the first repeated the acknowledged sequence number; the host
   discards duplicates -> retransmit wedge.  (This was the 8 KB tty
   stall on hardware.)
9. Endpoint-mux tier-1 pass-through leaked the generator's `done`
   from a still-completing UNRELATED request into a hold-until-done
   requester connecting at that moment (ERDY holder released unserved,
   its pending then suppressed).  Fixed with pass_dispatched tracking;
   tier-1 now routes `done` only after its own dispatch.
10. `ss_stream_out.py`: capture was gated on the IDLE state and lost a
   word presented during the 1-cycle ACK state (then mis-addressed the
   rest via the stale fill count).  Capture now runs whenever not
   draining.
Also: `generate_zlps=False` used by the echo (per-packet `last` would
otherwise force a ZLP after every max-size packet), debug taps on the
IN EP / OUT EP / mux (`debug_*`, prunable), FSM-state tap.

**Hardware results (10 G root port, Gen1, integrity-verified):**
* strict ping-pong: 256 KiB clean, ~12.5 MB/s (syscall-bound);
* windowed loopback, 2 KiB URBs (= device buffer depth): **64 MiB
  byte-exact at 23.2-24.7 MB/s per direction sustained**
  (`window2_test.py`); repeatable after every clean flash;
* window >= 3 packets in flight: instant wire-level corruption --
  usbmon shows ~10 packets flow then `-71 EPROTO` on both pipes
  (varies).  The failing ingredient is OUR concurrent TX (IN DPs +
  OUT-ACK TPs + LGOOD/LCRD) through the link transmit path, which the
  endpoint-layer sim does NOT cover.  cdc-acm pipelines ~16 read URBs,
  so luna-acm's tty echo still trips this race immediately; raw pyusb
  with a bounded window is the validated interface.

**Suspects for the >2-packet race** (link TX serialization, never
hardware-tested upstream; for the next session):
* `link/transmitter.py` SEND_PAYLOAD captures `data_sink` on every
  accepted word WITHOUT checking `data_sink.valid` (assumes gapless
  payload feed);
* the ABORT_DPP / `header.delayed` retransmission path;
* `SuperSpeedStreamArbiter` switches on any 1-cycle `valid` drop --
  any bubble in `transmitter.source` mid-packet lets the
  higher-priority link-command stream interleave inside a DP;
* PacketTransmitter credit/retry-buffer interaction under interleaved
  TP+DP traffic.
STRATEGY: extend the sim to a full link-partner model (drive
USB3LinkLayer's physical boundary with host-side header/CRC-16/CRC-5
generation and LGOOD/LCRD credit handling, parse our wire output and
assert DPH/DPP atomicity).  That is the remaining gap between the
165 MB/s endpoint layer and the wire.

Bench state: luna_loopback.fs flashed, freshly verified 8 MiB echo at
24.7 MB/s.  After any failed >2-packet experiment the device wedges:
reflash before the next test.  gw_usb3 suite: 103/103.

## 10i. Update 2026-08-28 (session 6) — >2-packet concurrency SOLVED:
## 94-110 MB/s per direction full-duplex, all windows byte-exact

Mission (prompt.md): fix the link-TX concurrency race that killed any
traffic with >2 bulk packets in flight.  Strategy as documented: build
the **link-partner simulation** first, fix what it shows, then climb
the hardware ladder.  Result: five more bugs (#11-#15, continuing the
§10g/§10h numbering) — four found by the new sim before touching
hardware, the fifth pinned by the first hardware run + usbmon and then
reproduced deterministically in the sim.  None of them was the
mission's suspect #1 (SEND_PAYLOAD valid) — that one never fires in
this rig (the payload feed is gapless by construction; the sim asserts
it stays so).

**The link-partner sim** (`luna-loopback/sim_link_loopback.py`, permanent
regression asset next to `sim_loopback.py`): full `USB3LinkLayer` +
`USB3ProtocolLayer` + endpoint mux + real endpoint pair — i.e.
`USBSuperSpeedDevice` minus the physical/PIPE layer — against a fake
physical boundary of raw streams, plus the REAL `TxStreamSkidBuffer` +
`CTCSkipInserter` TX conditioning so SKP scheduling is bit-faithful.
The host model:
* scripts the LTSSM through Polling (LFPS handshake, reactive TS1/TS2
  feed, idle handshake) to U0 in ~620 cycles;
* speaks the raw wire dialect with bit-exact CRC-5/CRC-16/CRC-32
  (ported by evaluating the gateware's own XOR equations on Python
  ints — monkeypatched `Cat`; host and device agree by construction);
* does the LGOOD_7/LCRD_A-D bringup, LMP dance, credit accounting;
* parses every TX word and asserts: DPH/DPP atomicity, framing, CRCs,
  3-bit header + 5-bit DP sequence continuity, LGOOD/LCRD ordering,
  SKP cadence (max wire-byte gap between SKP ordered sets ≤ 1800 =
  the 2x354 pair threshold + one max packet), byte-exact echo;
* fault injection: `LBAD_EVERY` (host LBADs device headers → LRTY →
  DL=1 resends → EDB-aborted DPP → protocol-level endpoint
  retransmit), `BADHDR_EVERY` (corrupt host header CRC → device LBAD/
  ignore/LRTY path → host DL=1 resends), `HOST_BUBBLES` (mid-frame
  valid gaps as the SKP remover leaves), `HOST_GAP`, `WINDOW_KIB`
  (mimics window_test.py's write-window-then-read pattern).
Run: `pdm run python .../sim_link_loopback.py` (~40 s for 16 KiB).
The retry paths (mission suspects 3+4: ABORT_DPP/header.delayed,
credit/retry interplay) test CLEAN under injection — they were not
the race.

**Bugs found & fixed (all in the luna tree; patch regenerated):**
11. `link/receiver.py` — RawHeaderPacketReceiver's CHECK_PACKET cycle
    was blind: a header packet whose HPSTART lands exactly there
    (back-to-back headers, which a loaded xHC sends) was silently
    dropped; the next header then hits bad_sequence → Recovery mid-
    transfer.  Only reachable with ≥3 packets in flight — at ≤2 the
    round trips space the host's headers apart.  Fix: CHECK_PACKET
    also matches HPSTART and restarts reception (CRC clear folded in).
12. `endpoints/stream.py` — SuperSpeedStreamInEndpoint never drove
    handshakes_out.endpoint_number: its NRDY/ERDY went out addressed
    to ENDPOINT 0.  Under pipelined URBs (buffer runs dry → flow
    control actually engages) the host applies/discards flow control
    on the wrong pipe.  Fix: tag constantly with the endpoint number.
13. SKP starvation under saturated TX (the §10h "concurrent TX
    collision" suspect, precisely): in U0 can_send_skp was only
    asserted while the arbiter was idle; back-to-back DP + LGOOD/LCRD
    + TP traffic has no idle cycles, the inserter's debt counter
    (3 bits) wraps, the 1/354 average breaks, and the host's elastic
    buffer drifts into symbol corruption after ~10 packets → -71 on
    both pipes.  Fix package (one mechanism):
    * transmitter/link-command generator mark `source.first` on their
      opening framing word; layer.py marks logical-idle words too;
    * `physical/layer.py` computes can_send_skip = post-skid
      `valid & first` (alignment exact by construction);
    * `physical/ctc.py` inserter now HOLDS the offered word during
      insertion (comb ready) instead of silently dropping it (the old
      registered ready held a stale 1 — insertion while real data was
      presented ATE the word; §10d's "the inserter holds that word"
      comment was wrong), and the debt counter saturates at 4.
    Verdict knob: the sim's SKP-cadence assert fails pre-fix at the
    first IN DP under load, max gap 1768 ≤ 1800 post-fix.
14. `ss_stream_out.py` (+ `protocol/transaction.py`,
    `protocol/endpoint.py`) — THE HARDWARE KILLER: the OUT endpoint
    ACKs only after draining into the IN endpoint; with >2 KiB unread
    in flight both IN buffers are full, the drain stalls, and the
    third OUT DP is left UNANSWERED FOREVER — protocol violation; the
    host retries for ~35 ms then errors the pipe (-71), matching
    usbmon exactly (2 OUT URBs complete, 3rd EIO, nothing echoed).
    The endpoint sims never saw it because their host models waited
    for the device ACK before the next OUT.  Fix: accept a completed
    packet only when the sink advertises room for a whole packet
    (`packet_space`, defaulting to stream.ready which for the packet-
    buffered IN endpoint means exactly that); otherwise DISCARD +
    NRDY, then ERDY once space frees — the host retransmits.  This
    needed direction-correct TPs: HandshakeGeneratorInterface gained
    `direction`/`direction_valid` (defaults preserve every existing
    user: ACK/STALL=OUT, NRDY/ERDY=IN), plumbed through both tiers of
    the endpoint-mux arbiter; ss_stream_out sends dir=OUT.
15. Timing regressions from the fix work (acm build fell to 106 MHz
    pclk): three registered cuts, all latency-tolerant —
    * `physical/layer.py`: TxStreamSkidBuffer (new, in ctc.py) between
      link sink and scrambler/inserter, so the inserter's comb hold
      cannot reach the link-layer FSM enables; electrical-idle gate
      registered (was ltssm-state → tx-ready comb);
    * `protocol/endpoint.py`: rx_complete/rx_invalid broadcast
      registered centrally (they decode from the CRC-32 compare; the
      OUT endpoint turns them straight into handshake strobes);
    * `link/ltssm.py`: timeout comparators registered (26-bit state-
      timer compare was inside the state-transition select cone),
      same cycle counts preserved.
    Post-surgery: luna_acm pclk 137.0 MHz, luna_loopback 133.8 MHz
    (≥125 bar; 156.25 SDC misses remain the §10g boot-window classes).

**Example-side changes:**
* `luna-loopback/top.py`: 64 KiB BSRAM elastic FIFO (16384x37,
  SyncFIFOBuffered) between OUT and IN endpoints + `packet_space` =
  (free ≥ 260 words).  Why: the single-threaded window_test.py writes
  its whole window BEFORE the first read, so passing a W-KiB window
  requires absorbing W KiB — flow control alone gives clean NRDY
  behavior but the writes then wait on a reader that hasn't started.
  BSRAM 45/118.  Also fixed flash() path (luna_acm.fs → luna_loopback.fs).
* `ss_stream_out.py`: endpoint_number/direction tagging, packet_space
  accept gate, AWAIT_SPACE/SEND_ERDY states (see #14).
* luna-acm: no top changes — flow control + 16 pipelined read URBs is
  sufficient for the tty (reads always posted).

**Hardware verdicts (10 G root port `usb 4-9`, Gen1, all byte-exact /
sha256-verified; reflash between attempts as before):**
| test                                   | before        | after |
|----------------------------------------|---------------|-------|
| window2_test 64 MiB (2 KiB URBs)       | 23.2-24.7 MB/s| 23.7 MB/s (unchanged, syscall-bound) |
| window_test 4 MiB @ 4 KiB window       | -71 at pkt 3  | 12.5 MB/s OK |
| window_test 8 MiB @ 8/16 KiB window    | wedge         | 12.6 MB/s OK |
| window_test 16 MiB @ 64 KiB window     | wedge         | 12.5 MB/s OK |
| bandwidth_test 16 MiB full-duplex      | wedge         | **93.7 MB/s per direction** |
| bandwidth_test 64 MiB full-duplex      | wedge         | **103.9 MB/s per direction** |
| luna-acm tty echo 8 KiB / 64 KiB / 1 MiB / 8 MiB | immediate wedge | **104-108 MB/s, all pass** |
(window_test rates are the single-threaded harness's syscall bound,
not the device's.)  The old 23-25 MB/s 2-packet ceiling is gone; the
full-duplex threads test now runs ~4.3x faster than the best §10h
number, correctness-first as briefed.  /tmp/kilo/acm_echo_test.py: its
writer needed EAGAIN handling on the nonblocking fd (harness bug; >64
KiB stalls were the test, not the device).

**Regression state:** `pdm run pytest tests/` 103/103 (untouched by
luna changes); `sim_loopback.py` PASS (163 MB/s endpoint layer);
`sim_link_loopback.py` PASS incl. all fault-injection modes;
`gowin_gtr12_sim.py` + `gowin_gtr12_training_sim.py` PASS (the CTC/
skid/eidle rework is exercised by the full training path).  Debug
taps added: USB3LinkLayer.debug_rec_* / debug_rx_* / debug_tx_* and
HeaderPacketReceiver.debug_* (recovery-cause + sequence visibility;
prunable).

Bench state at session end: luna_loopback.fs (all fixes, FIFO build,
133.8 MHz) flashed and verified: bandwidth_test 64 = 103.9 MB/s,
window ladder green.  luna_acm.fs (137.0 MHz) in luna-acm/build/,
verified this session (8 MiB tty echo).  Vendor prj.fs untouched as
restore baseline.  patches/luna_gowin_adapter.patch regenerated —
now the COMPLETE luna delta vs upstream 82a8f733 (the previous patch
was missing gowin_gtr12.py, the training sim, command.py; recreate
the tree per patches/README.md).

## 10j. Update 2026-08-28 (session 6, part 2) — multi-endpoint concurrency:
## two simultaneous loopback pairs at 69-70 MB/s per direction EACH

Goal: multiple bulk OUT->IN loopback pairs driven simultaneously.  New
example `luna-multiep/` (EP1..EPn pairs, per-pair 16 KiB FIFO +
packet_space, same scaffolding as luna-loopback) + `multiep_test.py`
(one writer+reader thread pair per endpoint, all concurrent, per-pipe
sha256).  The link-partner sim gained `NUM_EPS` (per-EP host engines,
routing by endpoint+direction) and `WITH_CONTROL` (a real
USB3ControlEndpoint in the bench + a SET_ADDRESS phase asserting the
wire-visible §10g contract: the status ACK must carry the OLD address).

**Five more bugs (#16-#20), all found/reproduced by the sim first:**
16. Endpoint-mux TX stream: pure combinational last-wins priority mux —
    a second IN endpoint going valid mid-packet STEALS the shared
    stream (words of one endpoint spliced into another's DPP; END
    symbol mid-payload on the wire at 3 EPs).  Fixed with
    packet-granular grant locking + a one-'none'-cycle handoff gap
    (the shared DataPacketTransmitter delimits packets by a 1-cycle
    valid drop — zero-gap handoff spliced packets and wedged it).
17. Handshake arbiter: one interface with several request KINDS in
    flight (latched NRDY + held ERDY) shared one `done` and one
    pending-clear — the earlier kind's completion released the held
    ERDY unserved (park-after-unpark on the wire, pipe wedged).
    Rewritten kind-granular: one kind dispatched at a time, done
    delivered only while the interface still asserts the dispatched
    kind, per-kind pending clears; kind priority = ACK > STALL > NRDY
    > ERDY (park must precede unpark); tier-1 blocked while older
    latched requests pend (order inversion); in-flight tracking
    latched at dispatch (a concurrent grant blanking the comb pass
    selection used to swallow completions -> duplicate TPs).
18. header_rx: pending-LGOOD starvation — SEND_ACKS/ISSUE_CREDITS
    looped while their OWN queue was non-empty; under sustained
    traffic the credit queue refills continuously and LGOODs starve
    (LCRD outran LGOOD by 40+; a real host's PENDING_HP_TIMER then
    forces Recovery).  Now re-arbitrates by priority after EVERY link
    command; acks_to_send/credits_to_issue widened 3->5 bits (the
    3-bit counter wrapped at 8, silently discarding 8 LGOODs —
    invisible to the 3-bit sequence check).
19. Link-retry races in PacketTransmitter (mission suspect 3, now
    actually reachable — needs >=2 DATA headers queued around an
    LBAD): (a) WAIT_FOR_RETRY aborted the DPP of never-transmitted
    delayed headers, orphaning their staged payload and wedging the
    shared data_tx for every endpoint — now only sent-once headers
    abort (EDB), never-sent ones retransmit WITH their payload
    (per-buffer sent_flags); (b) sent_flags indexed via the live
    read_pointer, which REWINDS mid-send on LBAD — now latched per
    transmission start (sending_slot); (c) an LBAD one cycle after
    packet_tx.done dispatched the retry-set head as a NORMAL send
    (no DL, no LRTY wait, wrong payload => suspect #1 fired) —
    DISPATCH_PACKET now also honors the combinational retry_required;
    (d) enqueue_send coinciding with retry_required left the
    just-enqueued header uncounted in packets_to_send (buffered but
    never dispatched -> data_tx wedge).
20. SuperSpeedStreamInEndpoint: `erdy_required` was never cleared and
    only honored on the WAIT_FOR_DATA path — the WAIT_FOR_ACK buffer
    swap into WAIT_TO_SEND stranded buffered data against a parked
    host forever.  Now cleared when the ERDY dispatches and honored
    in WAIT_TO_SEND.
Plus: transmitter debug_payload_underrun tap (asserts the gapless
payload-feed contract in the sim), and a host-model hardening pass
(sequence-driven ACK handling, idempotent OUT queueing, tolerance for
stale flow control after link-level replays — mirroring xHC behavior).

**Timing work** (multi-EP fanout pushed pclk to 101-118 MHz; all
latency-tolerant register cuts, verified by the full sim battery +
training sims after each): registered link_ready + TS-burst-command +
enable_scrambling + eidle distribution; registered LTSSM timeout
comparators (26-bit compare was in the state-transition cone);
registered rx_complete/rx_invalid broadcast (mux) and per-endpoint
handshake decode; registered RX payload stage (link/layer.py — the
per-lane valid decode reached every endpoint's capture logic);
TxStreamSkidBuffer between link TX and scrambler/CTC; TxDataSkidBuffer
between endpoint mux and data_tx; TX stream muxed on the registered
tx_owner with parameters latched at grant lock (see below); tier-1
handshake fast path restricted to interface 0 (the control endpoint —
the only one with the same-cycle contract); endpoint send_position_p1
(no adder in the BRAM address mux); crc16 fed from header words
directly (the DPP CRC-splice cone was a false path into its XOR tree).
Final pclk: luna_loopback 148.9, luna_acm 156.3 (156.25 SDC PASS!),
luna_multiep(2 pairs) 137.8 MHz.

**The short-packet regression this exposed** (caught on hardware by
bandwidth_test's 4-byte warmup, then reproduced with LOOPBACK_BYTES=4):
with the registered tx_owner select + the data-path skid, a short
packet clears its endpoint in ~2 cycles and the comb-driven tx
parameters dropped before the skid-delayed data reached data_tx — the
wire showed DPH(ep=0,len=0) followed by the payload.  Fixed by
latching {length, endpoint, sequence, direction, tx_zlp} into mux
registers at grant-lock time (they persist until the next lock).
LOOPBACK_BYTES=4 and =1028 are now part of the sim battery.

**Hardware verdicts (10 G root port, Gen1, all sha256-verified):**
* luna-multiep (2 pairs): simultaneous full-duplex on EP1+EP2,
  **69-70 MB/s per direction EACH, 139-141 MB/s aggregate**, 4 MiB /
  16 MiB / 64 MiB per EP — byte-exact, incl. per-pipe NRDY/ERDY flow
  control and 16 KiB FIFO backpressure.
* luna-loopback regression: window 4/64 KiB + window2 + bandwidth_test
  64 MiB = 106.4 MB/s — all green with the final tree.
* luna-acm regression: tty echo 64 KiB + 8 MiB green.

**OPEN ITEM — 3 loopback pairs**: a THREE-pair luna_multiep build
reproducibly fails enumeration at SET_ADDRESS ("Device not responding
to setup address", -71, host retries then gives up) while 1- and
2-pair builds enumerate, across different placements (Fmax 111-147),
FIFO sizes, with/without the per-pair skids, and with 2- or 3-pair
descriptor sets.  The same configuration passes the link-partner sim
INCLUDING the SET_ADDRESS address-contract check (WITH_CONTROL=1
NUM_EPS=3) and all traffic batteries.  The failure is content- (not
placement-) dependent and precedes any bulk traffic; suspicion is on
a boot-window (156 MHz) or hardware-timing-phase interaction in the
control-transfer handshake path that the sim cannot see.  Next step:
a probe build with uart1 channels on the control endpoint's send_ack
strobe, the generator dispatch (shared.handshakes_out.send_ack &
ready), mux.debug_pending[0] and address_changed, to localize where
the status ACK dies.  luna-multiep ships with BULK_EPS=(1,2) (a note
in top.py marks the anomaly).

**Regression state**: pytest 103/103; sim battery green including
NUM_EPS=1..4, WITH_CONTROL, WINDOW_KIB, LBAD/BADHDR/bubble injection,
LOOPBACK_BYTES=4/1028; endpoint sim; LFPS smoke + full training sims.
Bench state at session end: luna_multiep.fs (2 pairs) flashed and
verified (4 MiB/EP simultaneous PASS); luna_loopback.fs and
luna_acm.fs rebuilt with the final tree and verified this session.
patches/luna_gowin_adapter.patch regenerated (complete delta).

## 10k. Update 2026-08-28 (session 7) — the 3-pair SET_ADDRESS failure:
## ROOT-CAUSED (GowinSynthesis miscompile) & FIXED; boot window hardened

Mission (prompt.md): the reproducible 3-endpoint-pair enumeration
failure at SET_ADDRESS (-71).  Both suspects that the probes confirmed
are FIXED; enumeration and burst traffic on 3 pairs now work.  A NEW,
distinct intermittency under *sustained* 3-pipe traffic was exposed
(open item #23, below); the shipping default stays `BULK_EPS=(1, 2)`
per the ladder rule, and the 2-pair configuration re-verified green.

**How it was found** (the probe ladder that localized it, all layouts
kept in git history; uart1 repurposed per build):
1. Sim phase scan first: `CTRL_GAP`/`CTRL_PRE_GAP` (SETUP->STATUS and
   bringup->SETUP phases), `ITP_EVERY`, `HOST_LDN_EVERY` added to
   `sim_link_loopback.py` — 47/47 scan combinations PASS at NUM_EPS=3
   WITH_CONTROL=1 → protocol/stimulus-class races (suspects 2/3)
   exonerated.
2. Probe build 1 (counters on the control-ack path): the SETUP ACK is
   strobed by the control endpoint but the TP generator NEVER
   dispatches (0 dispatches, 0 TP headers ever queued), and the
   arbiter's `pending[0]` wedges nonzero from before the first SETUP
   → boot-window corruption suspected (suspect 1).
3. Boot-window fix landed (see below) → stickies CLEAN at U0, but the
   wedge then appears AT the first SETUP: strobed, never dispatched,
   pending stuck, `granted` never asserts — RTL-impossible (the
   arbiter is self-healing by construction; an adversarial fuzz bench
   of the real mux+generator, `/tmp/kilo/fuzz_hsk_mux.py` style,
   passes for millions of cycles).
4. Cycle-trace probe (32-sample embedded capture around the first
   iface-0 strobe): ONE cycle with `strobes=ACK, pass_sel selected,
   generator ready` and the shared strobes NOT driven — the netlist
   contradicts the RTL in a single cycle.  The emitted Verilog
   simulates CORRECTLY under iverilog → the divergence is introduced
   by GowinSynthesis.
5. Standalone synthesis of the emitted endpoint-mux + netlist-level
   iverilog sim (prim_sim.v, §10f technique) reproduces the wedge in
   a box; reduced to a 90-line plain-Verilog micro-repro.

**Bug #21 — GowinSynthesis V1.9.12.03 all-ones-sentinel constant
fold (THE SET_ADDRESS killer).**  A multi-bit selector register (or a
comb selector with a constant default) whose "none" sentinel is the
ALL-ONES value of the signal — exactly what
`Signal(range(n + 1), init=n)` produces at n = 7 interfaces (3 bulk
pairs + control ⇒ 3-bit signals with sentinel 7) — gets its sentinel
comparisons constant-folded (`grant != 3'h7` → constant TRUE even
though the grant DFFs demonstrably hold 3'b111), and the whole
dependent cone is then deleted as dead logic: the netlist ties the
shared handshake outputs to GND and `granted` to VCC.  The endpoint
mux's `grant`, `pass_sel` AND `tx_owner`/`tx_grant` all had this
shape.  At 5 interfaces (2 pairs) the sentinel is 5 = 3'b101 — not
all-ones — which is why 1- and 2-pair builds never failed;
content-dependent and placement-independent exactly as observed.
* Fix (`protocol/endpoint.py`): zero sentinels — "none" = 0,
  interface `i` encoded as `i + 1` — for grant/pass_sel/tx_owner/
  tx_grant (encoding notes in the source).  Also: per-interface strobe
  vectors and pending-any reductions materialized as single named
  nets (CSE hygiene; the duplicated expression cones were where the
  netlist disagreed with itself).
* Verified in the box: the actual Amaranth-emitted, gowin_compat-
  processed, GowinSynthesis-synthesized mux now simulates IDENTICALLY
  to RTL (same-cycle ACK dispatch; 3-way TX handoff bit-exact).
* Guard: `tests/test_gowin_synthesis.py::
  test_endpoint_mux_arbiter_not_folded` synthesizes the real emitted
  7-interface mux and asserts the shared ACK output is not tied off
  (fails in seconds if the class returns).  Suite now 104.
* Also: `syn_hier = "hard"` on the endpoint-mux module
  (`gw_usb3/synthesis.py::force_hard_hierarchy`, applied by the DK
  platform) — the cross-module optimizer had scattered the arbiter
  across sibling modules' ports; hardening the boundary contains the
  blast radius (kept even though the encoding fix is what cures it).

**Bug #22 — boot-window exposure (suspect 1, real but secondary).**
Probe1 showed arbiter state corrupted BEFORE the first SETUP: until
the adapter's 10G→5G rate switch completes, the whole LUNA stack
clocked at 156.25 MHz with its reset released (POR was time-based),
and then through the CSR-driven pclk retune glitches.  Fix, one
mechanism: the adapter now owns the entire PHY bring-up in boot mode —
`GowinGTR12PIPE(boot_rate_switch=True, boot_domain="ss_raw")` runs
the sequencing in a reset-free pclk domain (`boot_start` input from
the POR chain; 20-bit counter: PHY reset release at ~8 µs, rate drop
at ~0.4 ms, `phy_ready` at ~7 ms — generously past the CSR
sequencer's delayed RATE_2 burst, which the old 18-bit count did NOT
cover), owns `phy_resetn` (a post-boot MAC reset pulse would reset
the CSR sequencer's rate synchronisers to the 10G value and fire a
SPURIOUS rate change under a live MAC), and synthesizes the TUSB
phy_status startup edge after a ~33 µs post-boot settle.  The tops
gate the LUNA ss/sync reset on `luna_go & adapter.phy_ready`: no LUNA
state ever clocks before the PHY is settled at 5G/125 MHz.  All four
LUNA tops (multiep/loopback/acm/enum) carry the pattern.  Post-fix
probes confirm clean arbiter state at U0.  Side benefit: the 156.25
SDC misses are now genuinely irrelevant (nothing clocks at 156 out of
reset); the operating gate remains pclk ≥ 125 MHz.

**Hardware verdicts (10 G root port, Gen1):**
* 3-pair build: **enumerates cleanly, first attempt, repeatedly**
  (the mission bug is dead); `multiep_test 1 --eps 1,2,3` passes at
  38 MB/s per direction per pipe (114 MB/s aggregate) — when it
  passes (see #23).
* 2-pair regression on the SAME tree: `multiep_test 16 --eps 1,2` =
  **69.5 MB/s per direction EACH, 16 MiB byte-exact** — identical to
  the §10j verified numbers, no regression.
* Full final ladder (all sha256-exact; final tree, fresh builds:
  multiep 138.1 / loopback 156.3 (156.25 SDC PASS) / acm 143.2 MHz):

  | rung                                    | result |
  |-----------------------------------------|--------|
  | luna-multiep 3-pair enumeration         | PASS (was the mission bug) |
  | luna-multiep 3-pair `multiep_test 1 --eps 1,2,3` | 38 MB/s/dir/pipe, ~50% runs (open #23) |
  | luna-multiep 2-pair (shipping) 16 MiB   | 69.9 MB/s per direction each |
  | luna-multiep 2-pair 64 MiB              | 70.4 MB/s per direction each |
  | luna-loopback window 4 MiB @ 4 KiB      | 12.5 MB/s OK |
  | luna-loopback window 16 MiB @ 64 KiB    | 12.6 MB/s OK |
  | luna-loopback bandwidth 64 MiB          | 105.2 MB/s per direction |
  | luna-acm tty echo 64 KiB / 8 MiB        | 51.6 / 106.1 MB/s |

**OPEN ITEM #23 — sustained 3-pipe traffic intermittency** (NEW
territory: 3 pairs never enumerated before this session).  With all
three pipes under sustained load: ~50% of 1 MiB/EP runs and ~100% of
16 MiB/EP runs fail; usbmon shows -71 EPROTO completing on TWO IN
pipes within ~40 µs of each other at partial transfer counts while
the third pipe continues; the uart probes show the link NEVER leaves
U0 (no TS1/TS2, no device-initiated recovery strobes) and the
handshake path stays healthy — i.e. a malformed DEVICE TRANSMISSION
at the wire/framing level under 3-stream TX pressure, not a link or
arbiter wedge.  Failing runs are degraded from the start (0.2-3 MB/s
= retry/timeout-bound) — bimodal per run.  The synthesized TX mux is
exonerated (box: 3-way handoff netlist==RTL).  Candidate space:
TX-path interleaving/SKP scheduling under 3 saturated IN streams +
3 OUT-ACK TP flows (the §10i #13/#16 class one notch up), or the
recovery-flush spec deviation (LUNA's transmitter drops unacked
headers on `~enable` instead of retransmitting those with seq >
advertisement [USB3.2 §7.2.4.1.x "flush ... except ... greater than"]
— found while auditing, NOT yet implicated by data since no recovery
occurs in the failing window).  Next steps: extend
`sim_link_loopback.py`'s host model to xHC-like deep URB pipelining
(16 in flight per pipe) and MiB-scale soaks at NUM_EPS=3; usbmon +
uart capture around onset; the QEMU/vhci rig (repo-root architecture
study) is now genuinely the right investment for this class.

**Also fixed/landed this session:**
* device.py debug taps registered (the composed handshake-cone probes
  cost ~19 MHz of pclk Fmax when sampled combinationally into probe
  registers placed at the UART corner).
* Sim host model: `ITP_EVERY` (Isochronous Timestamp Packets),
  `HOST_LDN_EVERY` (host keepalives), `CTRL_GAP`/`CTRL_PRE_GAP`
  (control-phase scans) knobs in `sim_link_loopback.py`.
* luna-multiep uart1 = control/handshake health probe (dispatch/
  status/ACK/TP counters + pending0 level; stickies: pending0,
  recovery, post-address EP0 ACK).

**Regression state:** pytest 104/104 (incl. the new synthesis guard);
sim battery green (NUM_EPS=1..4, WITH_CONTROL, ITP/LDN, CTRL scans,
LBAD/BADHDR/bubbles, WINDOW_KIB, LOOPBACK_BYTES=4/1028); endpoint
sim; LFPS smoke + full training sims.  Fuzz benches for the arbiter
(random + collision profiles) pass.

**Addendum — Yosys pre-lowering defeats both GowinSynthesis
miscompiles (validated experiment).**  Idea: don't hand GowinSynthesis
the human-readable (word-level, behavioral) Verilog; pre-lower it with
Yosys so Gowin only re-synthesizes structural soup, starving its buggy
high-level analyses (ROM extraction, init-value reachability folding)
of anything to pattern-match.  Yosys built from GitHub master
(`~/Downloads/yosys/build/yosys`, 0.68+136 @ c3045748; CMake:
`cmake -S . -B build -DCMAKE_BUILD_TYPE=Release -DYOSYS_ENABLE_TCL=OFF
-DYOSYS_ENABLE_READLINE=OFF && cmake --build build -j`); note upstream
`synth_gowin` now has `-family gw5a` (brams_map_gw5a.v /
cells_xtra_gw5a.v, commits through 2026-08).  Two recipes, both
verified netlist-vs-RTL through the full box (Yosys output checked
first, then the GowinSynthesis re-synthesis of it):

* generic gate soup: `read_verilog; hierarchy -top X; proc; flatten;
  opt -full; techmap; opt -full; write_verilog -norename` — family-
  agnostic, Gowin still does the LUT mapping;
* full mapping: `synth_gowin -family gw5a` — emits Gowin primitives
  that GowinSynthesis passes through as instances.

Results (V1.9.12.03, same syn.tcl as the reports):
* sentinel bug (`gowin_bug_report_sentinel/src/arb_allones.v`):
  direct = 740/741 cycles mismatch; via EITHER recipe = 0/741 PASS.
* pROM bug (`gowin_bug_report/src/enc8b10b.v`, NO syn_romstyle
  annotation): direct = 4 wrong pROMs, 1831/1976 mismatch; via gate
  soup = 0 pROM inferred, 0/1976 PASS.

Caveats before adopting as the production flow: QoR/Fmax unmeasured on
the full design (gate soup discards word-level structure; pre-mapped
primitives bypass Gowin's own optimizations); register power-up init
semantics need a dedicated check (our reset-free ss_raw boot logic
depends on them); serdes/vendor macros become blackboxes through
read_verilog (fine in principle, untested at full-top scale).
Integration point would be a platform hook lowering plan.files["*.v"]
before `_apply_gowin_compat`.  Current shipped mitigations (zero
sentinels + romstyle + the two guard tests) already cover the known
bugs; the lowering flow is the systematic escalation if a third
miscompile class appears.

Bench state at session end: luna_multiep.fs (2 pairs, final tree,
138.1 MHz) flashed and verified (4 MiB/EP simultaneous PASS);
luna_loopback.fs and luna_acm.fs rebuilt with the final tree and
verified this session; luna-enum top carries the boot handshake but
is untested (parked since §10f).  multiep_test.py default --eps is
now 1,2 (matches the shipping build).  Vendor prj.fs untouched as
restore baseline.  patches/luna_gowin_adapter.patch regenerated
(complete delta vs upstream 82a8f733).  Box-repro assets for #21 in
/tmp/kilo/{muxsyn,muxsyn2,muxsyn3,micro} (recreate per §10k: emit,
standalone gw_sh synthesis, iverilog vs prim_sim.v).

## 10l. Update 2026-08-29 (session 8) — open item #23 ROOT-CAUSED & FIXED:
## the TX scrambler fabricated wire words at packet boundaries; a hidden
## 40-110% retransmission tax underlay ALL previous traffic numbers

Mission (prompt.md): the 3-pipe sustained-traffic failure (#23).  Root
cause found and fixed (bug #28), plus three more real bugs (#24, #26,
#27) found en route.  **3-pair `multiep_test 1 --eps 1,2,3`: 10/10
consecutive PASS; 16 MiB and 64 MiB/EP: PASS at 73.8-75.8 MB/s per
direction per pipe (207-227 MB/s aggregate — the old 3-pair number was
114 aggregate with ~50% of runs failing; the old 2-pair 70 MB/s/pipe is
now 87).**  `BULK_EPS = (1, 2, 3)` is the shipping default.

**Bug #28 — THE #23 ROOT CAUSE (`physical/layer.py`).**  The TX
scrambler's sink is held always-valid (the wire always carries a word;
the LFSR must advance).  The session-6 timing rework (#15) inserted
`TxStreamSkidBuffer` between the link layer and the scrambler — and
that skid emits a one-cycle `valid` bubble whenever it runs dry at a
transmit-stream-arbiter switch, i.e. between a packet and the link
commands that follow it (LGOOD/LCRD after essentially every packet
under load).  The forced-valid scrambler forwarded the STALE data/ctrl
word through: stale payload XORed with a fresh LFSR value, stale
K-bits unscrambled — a fabricated wire word adjacent to the packet.
The host sees a framing/CRC violation and requests retransmission
(protocol rty=1, or LBAD→DL-replay→EDB→rty=1 when it hit a header).
Fix: bubbles substitute logical idle (data 0, ctrl 0), which scrambles
to exactly the inter-packet idle the partner expects.
* The wire-probe measurements (probe builds 8-11, see below): before
  the fix the device retransmitted **62% of DPs at ONE pipe (1665
  wire DPs per 1025 delivered), 90% at two, 110% at three** — every
  throughput number since session 6 sat on this tax (70 MB/s/pipe at
  2 pairs was really ~135 in wire terms), and usbmon/sha256 never saw
  it (the retry machinery absorbs it perfectly).  #23's deaths were
  the tail of the storm: a retry sequence that terminally failed on
  one pipe (host halts the EP, -71).  After the fix: retry_flagged=0,
  wire-DP ratio exactly 1.00.
* **Why every sim missed it**: `sim_link_loopback.py`'s TX
  conditioning had the skid+CTC but OMITTED the scrambler as
  "data-neutral at this boundary".  It now instantiates the REAL
  scrambler wired exactly as physical/layer.py (forced valid and all)
  plus a real `Descrambler` as the host boundary — the pre-fix tree
  then fails in one run at cycle 634 with the fabricated word
  (`a080a080 at top level`), and the fixed tree passes.  Keep that
  chain in the bench forever: the scrambler is NOT data-neutral in
  the presence of bubbles.

**Bug #26 (`endpoints/stream.py`) — the per-pipe death MECHANISM.**
ACK events are single-cycle strobes; `SuperSpeedStreamInEndpoint`
ignored them in SEND_PACKET/FINISH_LAST_WORD.  A stale/duplicate ACK
(link-level DL replay, or the #28 retry storms) arriving in
WAIT_FOR_ACK correctly starts a protocol resend — and the genuine
ACK+token then lands mid-resend and was DROPPED: endpoint parks in
WAIT_FOR_ACK forever, host waits for the packet it granted credit
for, times out ~700 µs, halts the pipe (-71).  Multi-pipe mux
contention stretches the resend window (why 3 pipes died and 2
didn't).  Fix: a pending-acknowledgement latch (fields captured at
strobe time; non-advancing duplicates never overwrite a latched
advancing ACK), consumed on re-entering WAIT_FOR_ACK.  Deterministic
repro + regression: `luna-loopback/sim_stale_ack.py` (parks forever
pre-fix; recovers via NRDY/ERDY post-fix).  Found via the probe
ladder: probe build 7 (per-EP IN-endpoint FSM state on uart1) showed
the dead pipe parked in WAIT_FOR_ACK with zero resend blips while
the other pipes' ACK processing continued.

**Bug #24 (`link/data.py`) — packet-boundary gap compression.**
`DataPacketTransmitter` delimited packets solely by a one-cycle
`valid` gap on its input.  Buffered stages (the protocol-layer
`TxDataSkidBuffer`) only represent gaps as "running dry": when the
downstream freezes across a packet handoff with words buffered (the
packet transmitter stops consuming payload the moment it captures the
`last` word), the next packet's words refill the buffer seamlessly and
the gap is annihilated — data_tx never leaves SEND_PAYLOAD, the next
DPH is never generated, and the whole shared IN path wedges.  Fix: a
second, authoritative boundary observation — the `last`-marked word
leaving the register stage.  Found with `/tmp/kilo/tx_fuzz.py` (an
adversarial bench of the real mux→skid→data_tx→PacketTransmitter
chain: scripted endpoints, real link credits with latency, TP
interleave, per-cycle stall injection — wedged every seed pre-fix).
NOT the #23 mechanism (forensics: ep3 ran at full speed for 10 ms
after ep1/ep2 died — no all-pipe wedge), but real and latent; the
short-packet variant would have bitten ACM/burst work.

**Bug #27 (`link/data.py`) — spurious `packet_bad` after every good
DPP.**  `DataPacketReceiver.CHECK_CRC32`'s exit transition sat inside
the Else arm: good packets lingered a second cycle, re-compared
garbage, and strobed `packet_bad` — one phantom rx_invalid per good
packet (measured: exactly 1025 per 1025 packets, probe build 11).
Mostly masked because the OUT endpoint leaves IDLE on the good strobe
one cycle earlier; the paths that stay in IDLE (unexpected-sequence,
sink-full NRDY) served the phantom as a duplicate retry-ACK.  Fix:
moved the transition out of the arm.

**Also fixed/landed:**
* `#25 (documented, NOT fixed)`: endpoint-mux grant-lock TX parameters
  (`tx_p_*`) can be overwritten before `data_tx` latches them when a
  SHORT packet (≤ chain depth, <~16 bytes) releases the mux while the
  chain is backpressured — DPH emitted with the wrong length (repro:
  `/tmp/kilo/tx_fuzz.py` with short packets + TP interleave, len=80
  header on an 8-byte DPP).  Unreachable at 1024B (the chain can't
  absorb a whole packet), EP0 traffic is serialized — latent only.
  Fix idea: consume-gated param queue, or defer the next grant lock
  until the previous header was offered.
* Host-model upgrades in `sim_link_loopback.py` (all default-off):
  `URB_PACKETS/URB_GAP/URB_JITTER` (the synchronous-pyusb URB rhythm:
  NumP=0 closing ACKs + repeated-nseq re-tokens — the bench host's
  actual shape), `HOST_LATENCY/HOST_JITTER`, `LC_LATENCY/LC_JITTER`
  (credit-return latency: makes credit exhaustion reachable),
  `PIPE_PHASE`, `REORDER` (cross-pipe response reordering, per-pipe
  FIFO preserved), `RETRY_TIMEOUT` (xHC no-response retry + 3-strikes
  EPROTO), `DBG_HANDOFF` (mux-handoff/data_tx boundary invariant
  monitor).  Sweeps: 50+ seed/knob combinations green post-fix.
* Debug taps: physical `debug_tx_{data,ctrl,strobe}` (pre-scrambler
  wire view), device `debug_ack_received`, `debug_payload_underrun`,
  `debug_rx_dpp_invalid`, `debug_rx_hdr_bad`; stream-endpoint
  `debug_retry_flagged`/`debug_stale_ack` (WAIT_FOR_ACK service mix).
* luna-multiep uart1 is now the **TX wire checker probe**
  (`TxWireChecker` in top.py): ch0 = host-flagged retry services
  (rty=1 — nonzero means the partner is rejecting our DPs again),
  ch1/ch2 = device-RX DPP/header CRC failures, ch3 = wire DPs (ep1),
  ch4 = ACK TPs received; flags: sticky framing-violation, sticky
  payload-underrun, sticky DPP-CRC-mismatch (checker recomputes
  CRC-32 pre-scrambler), trained.  `retry_flagged` is the single most
  valuable health number this stack has: it sees what usbmon cannot.

**The probe ladder that converged** (one layout per build, verdict
each): probe 7: per-EP IN FSM state → dead pipe parked in
WAIT_FOR_ACK, everything else alive.  usbmon forensics (dev022/dev028
captures): two pipes die ~38 µs apart mid-URB at partial counts OR one
pipe alone; survivors run at full rate for 10+ ms after.  Probe 8
(wire checker v1): framing/length clean, but wire DP count ≈ 2.1× the
delivered packets — the smoking gun.  Probe 9: the resends are ALL
host-flagged (rty=1), zero stale — the host rejects our DPs.  Probe
10: CRC-32 recomputation pre-scrambler clean ⇒ damage is downstream
of the link layer.  Probe 11: device RX error counters zero (host→
device direction clean) ⇒ asymmetric ⇒ our TX conditioning ⇒ read
the scrambler wiring ⇒ #28.

**Hardware verdicts (10 G root port, Gen1, all sha256-exact; build
pclk 132.8 MHz):**

| rung                                       | result |
|--------------------------------------------|--------|
| 3-pair `multiep_test 1 --eps 1,2,3` ×10    | 10/10 PASS, 207-223 MB/s aggregate/direction |
| 3-pair 16 MiB/EP                           | PASS, 73.8 MB/s per direction per pipe |
| 3-pair 64 MiB/EP                           | PASS, 75.8 MB/s per direction per pipe (227 aggregate) |
| 2-pair subset 16 MiB (`--eps 1,2`)         | PASS, 87.0 MB/s per direction each |
| 1-pipe wire probe                          | retry_flagged=0, wire-DP ratio 1.00 |
| luna-loopback window 4 MiB @ 4 KiB         | 12.4 MB/s OK (rebuilt, pclk 147.8) |
| luna-loopback window 16 MiB @ 64 KiB       | 12.3 MB/s OK |
| luna-loopback bandwidth 64 MiB             | 108.0 MB/s per direction |
| luna-acm tty echo 64 KiB / 8 MiB           | 82.1 / 107.2 MB/s (rebuilt, pclk 149.4) |
| shipping image re-verify (4 MiB/EP ×3)     | 222.6 MB/s aggregate PASS |

**Regression state:** pytest 104/104; sim battery 18/18 (now includes
the scrambler+descrambler TX chain, `sim_stale_ack.py`, and the two
training sims); tx_fuzz matrix green.

**Next-session notes:**
* The recovery-retransmit conformance item (§10k 5a) and bMaxBurst>1
  remain the roadmap; with the wire now actually clean, bMaxBurst is
  the path from 76 to the Gen1 ceiling and the retry-flagged counter
  is the watchdog to keep at zero while doing it.
* luna-enum still carries the top changes unbuilt (§10k note stands).
* /tmp/kilo assets this session: `tx_fuzz.py` (adversarial TX-chain
  bench, found #24/#25), `run_instrumented.sh`, `uart_capture.py`,
  usbmon captures (`usbmon_r4/p2/f1/w3.txt`, `dev022.txt`).
  Permanent: `luna-loopback/sim_stale_ack.py` in-repo.

## 10m. Update 2026-08-29 (session 9) — recovery-retransmit conformance
## (bugs #29-#31), bug #25 fixed (+#32/#33 found by its repro), EP0
## pending-request latches, and bMaxBurst>1 burst engines both directions

Everything sim-first, one mechanism per change, full battery + hardware
ladder green after each landing.  `retry_flagged` (uart1 ch0) read 0 on
every hardware run.

### Housekeeping (first thing)

`tx_fuzz.py` and `sim_battery.sh` promoted into the repo at
`gowin-serdes/example/gw5at-60-dkusb/luna-loopback/` with repo-relative
paths (`sim_stale_ack.py` pattern).  The battery is the acceptance bar:
it now runs 26 link-loopback configs + endpoint-sim + pytest + the two
training sims + stale-ack + tx-fuzz (33 entries, all green at session
end).  tx_fuzz's default (short-packet) knobs ARE the #25 repro: on the
session-start tree it failed at cycle 3074 ("K in payload"), exactly as
documented in §10l.

Also fixed in tx_fuzz: the host testbench returned on PASS while the
TP-producer coroutine still awaited queue-ready — sim.run() then never
returned and the buffered PASS was lost when the process was killed
(phantom "timeouts", including one 2h wall-clock hang; `timeout(1)` on
`pdm run` also ORPHANS the python child — use `.venv/bin/python`
directly under timeout).  Completion now also waits for `tp_done`.

### 1. Recovery-retransmit conformance — bugs #29, #30, #31 (all fixed)

Sim stimulus first: `sim_link_loopback.py` gained a scripted
link-recovery capability — `RECOVERY_AT=n` / `RECOVERY_EVERY=n` retrain
the link from U0 mid-traffic (host feeds TS1s; reactive TS1/TS2/idle
dance, no LFPS from U0), then perform the Header Sequence Number
Advertisement + credit re-advertisement per USB3.2 §7.2.4.1.x: the host
retransmits its own unacked headers (original seqs, DL=1, consuming
FRESH credits — unlike LBAD resends) and expects the device to do the
same.  A DPH whose DPP the retrain truncated counts as received
(advertised) with the payload recovered protocol-side via a retry
token; with an outstanding LBAD, the advertisement is computed from the
rejected sequence (the LRTY never comes).  Every pipe whose token was
on the wire with its burst unserved is re-established after recovery
with an ACK(rty=1, nseq=expected) — and stale/duplicate DPs around that
re-establishment are discarded like an xHC does (see the burst notes
below for why they are unavoidable).

Device bugs found and fixed against that stimulus:

* **#29 — transmitter flushed ALL unacked headers on `~enable`**
  (link/transmitter.py; the known §10k 5a spec gap, now numbered).
  Fix: header buffers, pointers, `packets_awaiting_ack`, `sent_flags`
  and both sequence numbers are PRESERVED across link-down; the
  advertisement decides.  New LTSSM strobe `entering_u0_from_recovery`
  (Recovery.Idle→U0 only), latched by the link layer into
  `transmitter.from_recovery`.  On the advertisement: from recovery,
  headers ≤ LGOOD_n are retired in one shot (mod-8 delta, clamped) and
  the remainder is queued through the existing WAIT_FOR_RETRY path
  (DL=1; consumed payloads EDB-abort exactly like LBAD retries);
  entry from Polling/Hot Reset performs the historical full flush
  (moved from `~enable` to the advertisement).  `packet_tx` is now
  reset-held while the link is down (a packet interrupted mid-word
  must not resume onto a fresh link); an in-flight header whose payload
  was partially consumed is marked sent-before and the stale tail
  still staged on `data_sink` is DRAINED (new `payload_pending` output
  on RawPacketTransmitter; `drain_required` gate blocks dispatch until
  the tail is gone).
* **#30 — receiver disable-prep unreachable + stale command leak**
  (link/receiver.py).  The advertisement-preparation block lived
  INSIDE `DISPATCH_COMMAND`; a link dropping while SEND_ACKS /
  ISSUE_CREDITS was mid-command missed the one-shot disable edge
  entirely — no advertisement was prepared and the interrupted link
  command sat in the generator and leaked onto the retrained link
  (observed: pre-recovery LCRD_3 desynchronizing the fresh credit
  index).  Fix: prep moved to top level (after the FSM, so it wins
  same-cycle conflicts); `lc_generator` and the raw header receiver
  are reset-held while the link is down; every SEND_* state aborts to
  DISPATCH_COMMAND on `~enable`.
* **#31 — under-advertisement: the prep advertised
  `next_header_to_ack - 1`** (last LGOOD actually sent), which lags
  `expected_sequence_number - 1` (last header properly RECEIVED) by
  the pending-LGOOD backlog.  The partner then retransmits headers we
  already processed, and its next fresh header looks like a sequence
  skip → instant bad-sequence recovery loop.  Fix: advertise
  `expected_sequence_number - 1`.

Battery entries: `rec-every`, `rec+lbad`, `rec+badhdr`, `rec+ctrl`,
`rec+urb` (+ burst variants below).  No hardware verdict is possible
for recovery itself on this bench (the link never leaves U0 — the
§10l wire-health fix removed the last cause); the acceptance bar is
the battery + the unchanged hardware ladder, both green.  A
force-recovery debug hook (uart command) remains an option for a
future session.

### 2. Bug #25 FIXED (+ #32, #33 found by the same repro)

* **#25 — endpoint-mux TX parameter crossing on short packets.**
  Mechanism chosen: defer the next grant-lock until the shared
  DataPacketTransmitter has latched the previous packet's parameters.
  New `parameters_consumed` strobe (data_tx, fires on
  WAIT_FOR_DATA→SEND_HEADER/SEND_ZLP), plumbed back link→protocol→mux
  as `tx_parameters_consumed`; the mux holds `tx_params_busy` from
  lock to consumption and only then grants a NEW owner.  For packets
  larger than the chain depth consumption always precedes grant
  release — zero cost in the common case.  The ZLP strobe is now HELD
  until consumed (the one-shot was silently dropped whenever data_tx
  was busy — same #25 family).
* **#32 — data_tx absorbed the next packet's head across a boundary**
  (bug #24's remaining half).  On the very cycle the current packet's
  `last` word left the passthrough register, the register refilled
  from the gap-compressed upstream — with the next packet's first
  word, which WAIT_FOR_DATA (watching only the input) never sees; its
  header is never generated and the shared TX path wedges.  Fix: the
  register never refills across a `last` boundary (consume-without-
  refill empties it; the new packet waits upstream where the FSM
  observes it), and WAIT_FOR_DATA does not re-arm while the previous
  packet's unconsumed tail still occupies the register.
* **#33 — phantom header dispatch on bare `ready`** (data_tx
  SEND_HEADER exited on `header_source.ready` alone).  The header-
  queue arbiter keeps routing the downstream ready to its sticky
  selected producer even while that producer offers nothing — a bare
  ready is NOT an acceptance.  Now `valid & ready`.

tx_fuzz default + a 40-run seed/knob matrix (BIG_ONLY, STALL_PCT=60,
MAXLEN=16/32, TP_EVERY=1, CREDIT_LAT=40, seeds 1-8) all green.

### 4. Hardening + probes

* **EP0 pending-request latches** (request/standard.py): the #26 rule
  ("handshake events are never dropped") applied to the control
  request handlers — `data_requested`/`status_requested` are latched
  until a consuming state services them (void on new SETUP); the
  legacy comb-only consumption dropped strobes arriving during state
  transitions.  StallOnlyRequestHandler is stateless comb — no window.
* **Wire-checker**: `dp_other` no longer counts EP0 control DPs
  (enumeration data stages); it now means "DP from an endpoint that
  cannot send DPs" — a real mux/parameter corruption.
* **Legacy IN-endpoint retry semantics**: WAIT_FOR_ACK resent the
  current packet on `eff_retry | ~eff_adv`; an ADVANCING retry-ACK
  (post-recovery re-establishment) acknowledges the current packet and
  names the NEXT (never-sent) one — resending the acknowledged packet
  wedged the pipe in a duplicate loop.  Now resend on `~eff_adv` only.

### 3. bMaxBurst > 1 — burst engines, BOTH directions (sim-complete)

The echo bench is rate-locked to the slower direction, so IN-side
burst alone gains nothing there: both engines were needed.

* **IN** (`endpoints/stream.py`, `max_burst=n` parameter; default 1
  elaborates the historical engine untouched): ring of `max_burst+1`
  packet buffers; fill/send/retire fully decoupled.  Sends up to NumP
  packets per token back-to-back with per-packet 5-bit sequence
  advance; EOB set on the last granted packet, the last buffered
  packet, and short packets (new `tx_eob` parameter plumbed
  mux→protocol→link into the DPH `end_of_burst` field — previously
  never driven); cumulative ACK retirement (one buffer/cycle);
  rewind-on-retry from retained unacked buffers; one-deep newest-wins
  ACK-event latch (events are cumulative); stale DL-replayed ACKs
  whose nseq falls outside the unacked window are IGNORED (mod-32
  arithmetic would misread them as huge forward jumps).
* **OUT** (`ss_stream_out.py`, `max_burst=n`): ring of `max_burst`
  buffers; packets ACKed IMMEDIATELY on validation with
  NumP = free-buffers-after-commit (new `number_of_packets{,_valid}`
  override on the handshake generator interface, latched/coalesced
  through the mux tiers; everyone else keeps the literal 1); drain
  runs concurrently; ACK(NumP=0) parks the host and the drain-end
  ERDY reopens it.
* **Grants do not survive recovery**: new `link_reset` broadcast on
  the endpoint interface (`~link.trained`); the burst IN engine voids
  its grant and latched events on it, and the host re-establishes with
  ACK(rty=1).  Packets already committed to the shared TX pipeline at
  link-down still go out first — the host discards them as stale
  (xHC behavior), and duplicate resends from overlapping tokens (the
  link layer legitimately REDELIVERS a pre-recovery token that the
  re-establishing retry token supersedes) are likewise discarded
  (behind-window dseq dup filter in the host model).
* **Host model**: `NUMP=k`/`NUMP_SWEEP` grants with burst-boundary
  cumulative ACKs + EOB conformance assertion; `BURST=n` device knob;
  OUT side reworked to window accounting driven by the device's
  advertised NumP (in-flight counting, cumulative retirement,
  rewind-on-retry, ERDY window reopening — with NumP=1 advertised it
  reduces exactly to the historical send-one-wait-ack rhythm).
* Sim throughput (32 KiB echo, 1 pipe): 156.0 → 232.2 MB/s aggregate
  at BURST=2 (BURST=4 identical there — zero host latency).
* **Known stimulus limit**: RECOVERY_EVERY below ~1800 cycles with 3
  bursting pipes is a starvation regime (recovery overhead ~740
  cycles eats the burst service windows; the unlucky pipe's DPP is
  truncated by the next retrain forever).  1800 is the battery entry;
  it is a stimulus-density artifact, not a protocol bound.

### Hardware verdicts (items 1+2+4 image: fixed tree, BURST=1,
### pclk 135.1 MHz, POR 66_005)

| rung | result |
|------|--------|
| multiep 1 MiB ×10 --eps 1,2,3 | PASS ×10 |
| multiep 16 MiB ×3 | 75.7 MB/s per direction each, sha exact |
| multiep 64 MiB ×3 | 75.8 MB/s each, 227.4 aggregate, sha exact |
| multiep 64 MiB 2-pipe | 92.1 MB/s each (was 87 in §10l) |
| uart1 during 16 MiB ×3 | ch0 retry_flagged=0, ch1/ch2=0, flags=8 (trained only) |
| luna-loopback window 4 KiB / 64 KiB | integrity OK |
| luna-loopback bandwidth 64 MiB | 106.3 MB/s full-duplex, sha exact |
| luna-acm echo 8 MiB | 107.2 MB/s, sha exact (pclk 152.1) |

### Burst hardware climb: FIRST RUNG FAILED — bring-up open (#34)

BURST=2 images (both the naive `grant := NumP` and the corrected
`grant := NumP - unacked` accounting) fail identically on the bench:
warmup (short transfers) passes, then every pipe delivers EXACTLY 2048
bytes (one 2-packet burst) and wedges — readers -EIO (3-pipe run) /
writer timeout (single-pipe run).  Wire perfectly clean throughout:
retry_flagged=0, no CRC/framing flags; uart1 showed 3 wire DPs and 5
ACK TPs on ep1, then silence — the DEVICE stops serving, no babble.
The first mid-burst xHC acknowledgement pattern therefore still
diverges from both host-model modes (per-packet sliding-window AND
coalesced).  The corrected NumP accounting (an ACK's NumP counts
buffers INCLUDING our packets still in flight past its sequence
number) is spec-required regardless and stays in.

Next session needs an ACK-TP FIELD probe: extend the uart1 wire
checker (`TxWireChecker` has the RX tap for ch4 already) to dump the
first N received ACK-TP dw1 words (nseq/rty/NumP) after config, plus
the first N transmitted DPH dw1 words (dseq/EOB) — one build, one run,
and the divergence is visible.  `MULTIEP_BURST_IN` / `MULTIEP_BURST_OUT`
env knobs on the multiep top are the IN-vs-OUT discriminator (each
engine can be burst-enabled separately).  Suspects, in order: the OUT
engine's immediate-ACK window advertisement vs the xHC's write
pipelining; EOB policy (we set it on grant-exhaust / last-buffered /
short — an xHC may expect Packet Pending (DPH dw2) or different EOB
timing); the IN engine's grant arithmetic against real ack cadence.

**Shipping default is BURST=1** (`MULTIEP_BURST=1`): the historical
engines, byte-identical elaboration, with all session-9 link/protocol
fixes.  The burst engines remain in-tree, default-off, fully sim-green
(battery entries `burst*`, 8 configs).

### luna-enum (item 4b)

Rebuilt with the fixed tree: **pclk Fmax 156.3 MHz** (passes even the
156.25 SDC), trains and enumerates at SuperSpeed on the bench
("GTR12 SuperSpeed bring-up", usb 4-9).

### Session-9 regression state

pytest 104/104; sim battery **33/33** (18 historical + 5 recovery + 8
burst + tx-fuzz + stale-ack); tx_fuzz 40-run seed/knob matrix green;
recovery sweep green (12 configs).  Hardware ladder (BURST=1 shipping
image): all rungs green, retry_flagged=0 everywhere (table above).

### Session-9 notes for the next session

* Bug numbering now at **#34** (burst hardware bring-up, open).
* The receiver-side spec-rule-2d window remains: header packets
  acked-but-undelivered at recovery entry are dropped when the rx
  buffers clear on link-down.  Narrow (protocol layer drains in a few
  cycles); never observed in the recovery sweep; noted for
  completeness.
* `timeout(1)` + `pdm run` ORPHANS the python child (the sim keeps
  burning CPU and its buffered output is lost) — run
  `.venv/bin/python` directly under timeout.  Several hours of
  phantom "hangs" this session were that plus a tx_fuzz harness bug
  (host testbench returned while the TP producer still awaited ready;
  fixed — completion now requires `tp_done`).
* The multiep POR threshold is at 66_009 after the placement-lottery
  rolls; the resident shipping image (BURST=1, all session-9 fixes)
  is at **pclk Fmax 128.2 MHz**.

### Final shipping verdicts (resident image at session end)

| rung | result |
|------|--------|
| multiep 1 MiB ×10 --eps 1,2,3 | PASS ×10 |
| multiep 16 MiB ×3 | 224.8 MB/s aggregate, sha exact |
| multiep 64 MiB ×3 | 76.1 MB/s per direction each, 228.4 aggregate, sha exact |
| multiep 64 MiB 2-pipe | 93.9 MB/s each (187.9 aggregate) |
| **soak: 64 MiB ×3 pipes, ×10 consecutive** | ALL PASS, 221.0-227.7 MB/s aggregate |
| uart1 through the soak | ch0 retry_flagged=0, ch1/ch2=0, flags=8 only |
| luna-loopback (pclk 139.2) | window 4/64 KiB OK; 64 MiB 106.3 MB/s sha exact |
| luna-acm (pclk 152.1) | 8 MiB echo 107.2 MB/s sha exact |
| luna-enum (pclk 156.3) | trains + enumerates SuperSpeed |

### Upstreaming plan (draft — sending is the user's decision)

The luna patch is now ~3700 lines over upstream
`82a8f733296603b70ba56755206e13092609c6f0`.  Suggested issue/PR
grouping by bug class (each is independently reproducible with the
in-repo sims):

1. **Protocol correctness, one-liner class**: ERDY-dispatch typo
   (transaction.py), DataPacketReceiver spurious `packet_bad` (#27),
   DPH-before-payload ZLP misclassification (data.py).  Trivial
   diffs, easy review.
2. **Handshake robustness**: lossless handshake mux (two-tier
   arbiter), pending-ACK latch (#26) + advancing-retry semantics,
   EP0 pending-request latches.  Reproducers: `sim_stale_ack.py`,
   the endpoint-sim.
3. **Shared-TX-path integrity**: #24+#32 boundary handling, #25
   parameter-consumption handshake, #33 valid&ready.  Reproducer:
   `tx_fuzz.py` (its default knobs fail loudly on upstream).
4. **Link-layer recovery conformance**: #29/#30/#31 + the LTSSM
   `entering_u0_from_recovery` plumbing.  Reproducer:
   `sim_link_loopback.py RECOVERY_EVERY=...` (upstream deadlocks /
   leaks stale commands).
5. **Features**: TX skid/scrambler conditioning (#28, physical
   layer), burst engines (once #34 closes on hardware), SS OUT
   stream endpoint (lives in gowin-serdes today; upstream has none).

Classes 1-4 are pure fixes against spec text and carry their own
regression tests; class 5 is feature work.  The vendor reports in
`gowin_bug_report*/` are unchanged and still awaiting the user's
send decision.

## 10n. Update 2026-08-30 (session 10) — bug #34 CLOSED on hardware:
## post-EOB grant discipline + ERDY-on-NumP=0; bug #35 (OUT capture
## gating); BURST=2 is the shipping default at 283 MB/s aggregate

### Housekeeping (first thing)

Cleanup items from §10m done: `multiep_test.py` default is now
`--eps 1,2,3` (+ new `--no-warmup` for probe runs); the /tmp helpers
are promoted into the repo — `luna-acm/acm_echo_test.py`,
`luna-multiep/uart_capture.py`, `luna-multiep/run_instrumented.sh`
(repo-relative paths).

### The bug-#34 field probe (how the diagnosis was made)

One instrumented build, exactly as scoped in §10m, plus one hard
lesson about reading it:

* `MULTIEP_ACKPROBE=1` builds carry `BurstEventCapture`
  (luna-multiep/top.py): a 64-entry write-once ring capturing, in
  arrival order, the DW1 of every bulk-endpoint header — TX DPH/TP
  straight off the pre-scrambler wire (TxWireChecker grew a field
  capture), RX TP/DPH as accepted by the protocol layer (new
  `debug_rx_hdr_*` taps in device.py).  The ring dumps continuously
  on uart0 (`II cXXXXXXXX`, c = D/T/A/R; sweep header `#NN F`).
  uart1 (wire checker) is unaffected.  Decode cheat sheet in the
  class docstring.
* **Probe artifact that cost half the session**: the TxWireChecker
  parses TX packets one at a time, and a state that waits for END
  silently eats every intervening TP header (TPs have no END).  The
  first capture runs therefore showed a "missing first DPH",
  "dseq one ahead", and "zero TP-ACKs during the OUT blast" —
  three phantoms of one blind window that ended at the first DP END.
  A quiet single-packet echo on a virgin pipe (EP2/EP3, ring
  append) is the calibration that separated probe artifacts from
  device behavior.  Cross-check any ring reading against the uart1
  cumulative channel counts (they matched the ring exactly, event
  for event).

### Bug #34 — the actual mechanism (all evidence reconciled)

With bMaxBurst=1 the xHC grants IN bursts of 2.  The engine sends
DP(n), DP(n+1, EOB) — grant exhausted, burst terminated by us.  The
host's per-packet ACK for DP(n) (nseq=n+1, NumP=2) is already in
flight TOWARD us when it receives the EOB; the engine took that
window as a fresh grant and launched DP(n+2) INTO THE CLOSED BURST.
Per rule 9249 the host answers the EOB with a terminating ACK
(NumP=0) and DISCARDS the straggler.  It then re-tokens with
ACK(nseq=n+2, rty=0) — non-advancing, no retry bit — which the
engine read as "grant only, nothing to resend" and answered with
DP(n+3).  Discard, re-poll x4, pipe halted: the deterministic
2048-byte wedge on every pipe.

Two device fixes (endpoints/stream.py, burst engine):

* **post-EOB grant discipline**: after transmitting an EOB packet,
  grants re-arm only from an acknowledgement that retires the EOB
  packet itself (`eob_wait`/`eob_next`); windows carried by the
  closed burst's earlier per-packet ACKs are void.  A retry rewind
  clears the gate (rewound packets get fresh EOB decisions).
* **ERDY on NumP=0** [USB3.2 8.10.1]: any ACK with NumP=0 is a
  flow-control condition — the host does NOT token again on its own.
  The engine now arms `erdy_required`; DISPATCH sends the ERDY as
  soon as a packet is ready.  Without this the ladder "passed" at
  ~0.4 KB/s: the xHC re-polled each burst only on its multi-second
  no-response timer.

### Bug #35 — OUT burst engine capture gating (found by the sim first)

The blast stimulus (below) showed the OUT engine committing a
100-byte TAIL of a 1024-byte packet: `can_capture` (ring not full)
can rise MID-PACKET when a drain completes, and the completion-time
occupancy check then commits whatever was captured; a fully-dropped
packet even commits as a phantom ZLP, advancing expected_seq over
1024 vanished bytes.  Fixed with a `packet_lost` latch: a packet
that lost any word to a full ring takes the existing NRDY-and-park
path (host retransmits after our ERDY).  ss_stream_out.py.

### Host-model upgrades (sim_link_loopback.py) — the bench xHC's
### actual behaviors, all defaults or new knobs

* `OUT_WINDOW0=n` — initial OUT in-flight limit BEFORE any device
  ACK exists (the spec window rule binds the host only to "the NumP
  in the LAST ACK received"): the bench xHC pipelines its whole
  16-packet scheduling window at transfer start.  This knob is what
  reproduced #35.
* `WITH_FIFO=words` — the hardware's elastic loopback FIFO between
  OUT and IN endpoints (multiep wiring, incl. packet_space gate);
  without it the sim echo backpressures where hardware buffers.
* `IN_TOKEN_DELAY=n` — first IN token lands on a fully-primed engine
  (bench reader-vs-writer thread skew).
* **rule 9249 is now default** in per-packet-ack mode: EOB →
  terminating ACK (NumP=0) → post-EOB DPs DISCARDED → pipe parked
  until the device's ERDY reopens it (`EOB_RETOKEN_GAP` scheduling
  gap).  This is the stimulus that reproduces #34 exactly
  ("device DP sequence 5, expected 4").
* any rty=1 token now arms the discard-until-expected tolerance
  (rule 9499: in-flight packets past the retry point are void) —
  previously only the recovery re-establishment had it.
* battery: +3 entries (`burst+blast`, `burst+blast3`, `blast+fifo1`);
  `burst+rec` moved 1800→2600 cycles (the spec-correct
  EOB/terminating-ACK/ERDY round trip added per-burst overhead to
  the §10m starvation regime; still a stimulus-density artifact).

### StreamArbiter synthesis hardening (precautionary, kept)

While the probe evidence still looked like a lost DPH, the
link-layer header arbiter (StreamArbiter) was reshaped with the
#21 idiom: named shared reduction nets, registered ONE-HOT
selection, AND-OR routing — the historical Switch-plus-priority-scan
is the exact duplicated-cone shape GowinSynthesis V1.9.12.03
miscompiled twice before.  It did NOT fix #34 (the probe artifact
misled), but it is RTL-equivalent, battery-green, hardware-verified
by the whole ladder, and permanently removes a known-dangerous
pattern from the TX header path and the wire arbiter.  Kept.

### Hardware verdicts (BURST=2, all fixes; ACKPROBE probe build,
### pclk 144.7)

| rung | result |
|------|--------|
| multiep 1 MiB, 1 pipe, no warmup (the #34 repro) | PASS, 134.5 MB/s per direction |
| multiep 1 MiB ×10 --eps 1,2,3 | PASS ×10 |
| multiep 16 MiB ×3 | 94.2 MB/s per direction each, 282.6 aggregate, sha exact |
| multiep 64 MiB ×3 | 93.7 MB/s each, 281.2 aggregate, sha exact |
| multiep 64 MiB 2-pipe | 230.0 MB/s aggregate (115/pipe) |
| **soak: 64 MiB ×3 pipes ×10 consecutive** | ALL PASS, 280.6–283.6 MB/s aggregate |
| uart1 through everything | ch0 retry_flagged=0, ch1/ch2=0, flags=8 only |

BURST=1 (76 MB/s/pipe) → BURST=2: **+24% per pipe, 283 MB/s
aggregate** across 3 full-duplex pipes.

### Shipping state

`MULTIEP_BURST` default flipped to **2** (the §10m condition — "until
its full ladder is green" — is met).  `MULTIEP_BURST=1` rebuilds the
historical single-packet image (its engines are byte-identical
elaborations; note the BURST=1 configuration was NOT hardware-re-run
this session — its delta vs the §10m-verified image is the arbiter
reshape + debug taps only, battery-covered).  The resident bench
image at session end is the default build (BURST=2, no ACKPROBE),
re-verified after flash; probe builds remain one env var away.

### Session-10 regression state

pytest 104/104; battery **38/38** (29 link-loopback configs incl.
the 3 new blast entries + endpoint-sim + pytest + 2 training sims +
stale-ack + tx-fuzz); the #34/#35 repro configs fail on the
session-9 tree and pass on this one.

### Force-recovery hook + recovery-edge groundwork (items 2+3,
### partially done; validation stimulus WIP)

The debug hook is BUILT, both sides:

* device: `link.force_recovery` input (ORed into the LTSSM recovery
  trigger), exposed as `usb.debug_force_recovery`; luna-multiep's
  uart1 RX decodes byte 'R' (0x52 at 115200) into one forced
  recovery entry.  NOTE: the resident bench image predates this —
  the next multiep build carries it.
* sim: `FORCE_REC_AT=n` strobes the hook at an absolute cycle (may
  fire pre-addressing, at ANY wire phase — unlike the scripted
  host recoveries, which always start at a frame boundary).

First sweeps with the hook (FORCE_REC_AT over 650..1450) immediately
exposed recovery-edge cases the frame-aligned scripted recoveries
structurally never reach, plus one sim-harness gap:

* **#36 (FIXED, positive validation pending)**: the transmitter's
  `lc_detector` was never reset-held across link-down (the TX twin
  of #30's receiver fixes): a link command truncated by the retrain
  leaves it mid-parse and it misreads the post-recovery
  advertisement.  ResetInserter'd like the receiver side.
* **#37 (OPEN)**: an inbound (host->device) DP whose DPP the retrain
  truncates is advertised as received at the link level (correct)
  but NOBODY retries the payload: the OUT endpoint never gets
  rx_complete/rx_invalid, so no ACK(rty=1) is sent, and the host
  waits forever (writer deadlock).  Per 8.12.1.2/9993 the device
  shall answer a damaged DP with ACK(rty=1); the link layer needs a
  "DPP truncated by link-down" strobe to the protocol layer.
  Repro: `WITH_CONTROL=1 LOOPBACK_BYTES=1024 FORCE_REC_AT=710`.
* **rule-2d receiver fix (IMPLEMENTED, positive validation
  pending)**: link/receiver.py no longer wipes the rx header
  buffers on link-down — acked-but-undrained headers survive and
  drain normally; the credit re-advertisement counts only the
  actually-free buffers (`buffer_count - buffers_filled +
  release_buffer`); the full clear now happens only on usb_reset.
* **sim-harness WIP**: a forced retrain strobed mid-wire must
  truncate the host feed realistically; the first cut
  (`rx_words = []` + refill hold) leaves the retrain dance stalled
  (no "#1 complete") — feed/parser re-sync in the harness needs
  finishing before FORCE_REC_AT can deliver clean verdicts for
  #36/#37/rule-2d.  The pre-truncation runs are still evidence:
  970's replayed-LC failure is what found #36.

All of the above is battery-green (35/35: the 5 scripted-recovery
entries exercise the rule-2d and lc_detector changes on their
historical paths).  The forced-recovery HARDWARE verdict for
#29-#31 (mission item 3) is deferred until the sim harness
validates the forced path end-to-end — strobing the bench hook now
would hit the known-open #37.

### Open items / notes for the next session

* Bug numbering now at **#37** (#34/#35/#36 closed or fixed-pending-
  validation; #37 open — see above).  Also noted, unfixed:
  - **data_tx SEND_ZLP exits on bare `header_source.ready`**
    (link/data.py) — the same #33 bare-ready class (SEND_HEADER was
    fixed, SEND_ZLP was not).
  - the wire checker's TP-blindness while waiting for END (probe
    artifact above) — fix the TxWireChecker FSM so TP headers are
    parsed even mid-recovery of a DP parse (or at least assert on
    unexpected HPSTART in DPP/RESYNC states).
* Finish the forced-recovery sim harness (feed truncation +
  retrain re-sync), then: green rule-2d + #36 targeted stimuli,
  fix #37, THEN the bench forced-recovery run ('R' on uart1) for
  the #29-#31 hardware verdict — expect ch0 rty=1 ticks DURING that
  run only.
* Raising the depth past BURST=2 (bMaxBurst up to 3): engines are
  parameterized and sim-green at BURST=4 (`burst*` battery entries);
  needs its own descriptor + ladder pass.
* `timeout(1)` + piped python BUFFERS stdout — a "hung" bench test
  may be a lost buffer: use `python -u` (this session's phantom).
  Also: a wedged pyusb run can leave BOTH endpoints of a pipe
  blocked such that reads/writes neither complete nor time out;
  reflash between failed attempts (known) and budget join() time
  (2 threads × 120 s).
* The resident image (BURST=2 shipping, pclk 139.0) predates the
  session-tail luna changes (rule-2d, #36, force_recovery hook);
  those are recovery-path-only and battery-green, but the FIRST
  build of the next session should re-run the standard ladder.

## 10o. Update 2026-08-31 (session 11) — THE FORK: luna-ss exists;
## Phase 0 sim gates green; G0 hw first blocked by a bench physical
## fault (see 11b/11c addenda: root-caused to recabling; #38 found
## en route; GATE G0 CLOSED same day)

The patch era ended.  This HANDOVER now lives in the **luna-ss**
fork; the old GW_USB3 workspace is a frozen bench archive (its
ARCHIVE.md has the full move map).

### The new world (Phase 0 executed)

| repo | where | content |
|---|---|---|
| **luna-ss** | `~/Downloads/luna-ss`, github.com/key2/luna-ss (private) | LUNA fork at upstream `82a8f733` + the 36-bug delta as a reviewable 8-commit series (interface/physical/link/protocol/endpoints/arbiter/device/examples, bug numbers in the messages); `SuperSpeedStreamOutEndpoint` promoted into `luna/gateware/usb/usb3/endpoints/ss_stream_out.py`; submodules `gw_usb3/` + `gowin-serdes/`; hardware examples in `examples/gowin/{luna-enum,luna-acm,luna-loopback,luna-multiep}`; link-partner sims + battery in `sim/`; `HANDOVER.md`/`prompt.md`/`doc/` moved in; `tools/gowin_timing_report.py`; `doc/gen2_design.md` (Phase 1 note) |
| **gw_usb3** | `~/Downloads/gw_usb3`, github.com/key2/gw_usb3 (private) | split from the workspace WITH history (filter-repo); package under `src/gw_usb3` (src layout on purpose — see pitfalls); tests/ (ALL 104, incl. the three refdesign-pinned ones with golden copies under `golden/refdesign/`), scripts/, rtl/, USB31PHY/, CUSTOMIZED/, Upar_Arbiter/ |
| **gowin-serdes** | submodule + github.com/key2/gowin-serdes (public) | + pyproject; platform moved to `gowin_serdes.dkusb_gw5at60` (shim kept); bench helpers promoted to `gowin_serdes.bench` (AsyncSerial*, ClockFreqProbe); luna-* examples removed (they moved to the fork).  PUBLIC repo: no vendor artifacts allowed here — that is why the golden files live in gw_usb3 instead |
| archive | `~/Downloads/GW_USB3`, github.com/key2/gw_usb3-archive (private; renamed from the old full-workspace mirror) | frozen; vendor refdesign + hybrid rig + bug reports + upstream_drafts; gowin-serdes submodule pinned PRE-fork (86ee125) so the archive stays buildable |

One-clone flow (verified from a scratch clone):
`git clone --recurse-submodules github.com/key2/luna-ss && pdm install -G :all`
→ `pdm run pytest` (104), `pdm run battery` (full), example builds.

### Gates passed

* **Byte-identical fork**: `diff -r` of the fork tree vs the final
  patched `luna/` checkout — clean, before any restructure commits.
* **pytest 104/104** from the fork layout (the 3 relocated tests
  included; test_gowin_synthesis runs for real — the IDE is present).
* **Battery: all 35 PASS lines** (29 link-loopback configs + endpoint
  -sim + pytest + 2 training sims + stale-ack + tx-fuzz) from
  `pdm run battery`.  Same stimulus, same pass criteria, new paths.
* **One-clone gate**: fresh recursive clone + `pdm install -G :all` +
  fast pytest green (96 fast + 8 slow deselected).
* Phase 1 gate G1: `doc/gen2_design.md` written (width/clock DECISION:
  staged 32-bit@156.25-behind-burst-buffers first, then width-generic
  64-bit; framing delta table with owners; the two NON-framing link
  deltas that narrow the "protocol untouched" hope: **modulo-16
  header sequence numbers and the LCRD1/LCRD2 credit-class split**;
  LTSSM/LBPM/SCD plan with spec timings; 156.25-operating timing
  budget; SKP x=4 quirk plan).

### Packaging pitfalls (so nobody rediscovers them)

* An editable-requirements group must NOT be called `dev` (upstream
  luna has an optional-dependencies extra `dev`; pdm silently
  resolves the wrong one).  Ours is `bench`; `pdm install -G :all`.
* gw_usb3 must be **src layout**: flat layout made the submodule
  ROOT a namespace package that captured `import gw_usb3` from the
  fork root (setuptools meta-path editable finder runs after
  PathFinder).  src layout → static-path `.pth` → regular package
  wins everywhere.
* gw_usb3/tests needs `__init__.py`: `python -m pytest` from the
  fork root puts the fork root on sys.path and upstream's regular
  `tests` package captured the bare name, breaking `tests.equiv`.

### Timing: the placement lottery is alive and well

First fork build of luna-multiep (BURST=2 defaults, first hardware
elaboration of the session-10-tail rule-2d/#36/hook changes):
pclk Fmax **107.4** (POR 66_009) — worst cones are the OLD friends
(endpoint_mux grants → tp_generator FSM), not the tail changes.
Reroll 66_010 → **124.26** (0.7% under the gate).  Reroll 66_011 →
**pclk 139.0 / rxclk 149.9** — in the session-9/10 band; this is the
build to ladder.  POR threshold is now **66_011**.

### G0 hardware gate: BLOCKED — the bench lost the USB3 path

Evidence chain, in order:

1. At session start the resident session-10 image was NOT enumerated
   (nothing on any SS bus) — consistent with a board power cycle
   having wiped the SRAM bitstream.
2. Fork multiep build flashed fine (JTAG/uarts on bus 3 work).
   uart0 link probe: `C 29aaa9x 0 0 0 0 c` — ss clock alive,
   flags c = phy_ready=1, engage_terminations=1, link_trained=0,
   and **zero LFPS-detected counts ever**.  (Healthy session-10
   captures show the same counters with flags d.)  The device is
   up and polling into a void.
3. Warm-cycled every SS root port (`usb4-port1..9/disable`,
   `usb2-port1..3`) around coordinated fresh flashes (= POR replays,
   needed because LUNA parks in SS.Disabled after 360 ms) — hubs
   re-enumerated (cables to hubs are fine), the board never appeared,
   zero hotplug events on any port.
4. **Vendor gold baseline `prj.fs` flashed: also dark.**  That is
   the decisive A/B — stack-independent ⇒ physical.
5. Lane-0 probe: the DK_USB wires BOTH Type-C orientations to Quad 0
   (straight = LN1 = the design default; flipped = LN0 by pad
   adjacency).  A `QUAD, LANE = 0, 0` luna-multiep build was flashed:
   ALSO DARK — and initially inconclusive: its uart0 ss-cycle counter
   read exactly 156.25/125 × the lane-1 value, i.e. pclk never left
   the 10 G boot trim.  **Root-caused next morning as bug #38** (see
   below); with the fix the LN0 probe was re-run properly — see the
   2026-08-31 addendum.
6. Not reachable from software: cable unplugged / reseated flipped /
   moved to a non-SS port / physically failed.

**Next session, at the bench, in order**: (a) physically reseat the
USB-C into the 10 G root port (usb 4-9), straight orientation —
if unsure, try both; (b) `sudo -n openFPGALoader -c ft232
examples/gowin/luna-multiep/build/luna_multiep.fs` (or the saved
`/tmp/kilo/luna_multiep_lane1_por66011.fs`) AFTER the cable is in
(the device parks 360 ms after POR; board KEY replays POR without
reflashing); (c) `lsusb -d 1209:0001`, dmesg; (d) the standard
ladder: `multiep_test.py 1 --eps 1,2,3` ×10, 64 MiB ×3, uart1 ch0
retry_flagged must read 0 (`uart_capture.py` interleaves both
uarts).  NOTE this image is ALSO the first hardware exposure of the
rule-2d/#36/force-recovery-hook changes (recovery-path-only,
battery-green) — the full ladder is the acceptance, per §10n.

### Addendum 2026-08-31 (session 11b) — LN0 re-probe: bug #38 found
### & fixed; orientation hypothesis EXCLUDED; bench still physical

* **Bug #38 (FOUND & FIXED, LN0 side silicon-verified)**:
  `GowinGTR12PIPE` builds its default `Usb31Phy` with the DEFAULT
  `UparCsrConfig` — **Q0_LN1 — regardless of which lane the serdes
  blob configures**.  The runtime CSR sequencer (eidle/FFE
  handshakes, the 10G→5G boot rate change) then silently addresses
  lane 1's registers.  Hardware signature (the §10o v1 probe):
  UPAR acks make the boot sequencer "complete" and `phy_ready`
  asserts, but pclk stays at the 156.25 MHz boot trim (uart0
  ss-counter 0x341554d instead of the 125-MHz 0x29aaa9x signature).
  Fix: all four `examples/gowin/*` tops pass
  `phy_kwargs=dict(csr_config=UparCsrConfig(quad=QUAD, lane=LANE))`
  (elaboration-identical for the shipping Q0_LN1 — dataclass-equal
  config, plus a full rebuild bitstream-payload identity check) and
  the adapter docstring warns loudly.  Positive verification ON
  SILICON: the corrected LN0 build's netlist carries the LN0 CSR
  addresses (0x8003A4, zero 0x8005A4) and its uart0 counter reads
  0x29aaa9x — **the Q0_LN0 CSR rate-change path works** (first
  silicon proof of a non-default lane).
* **Orientation hypothesis EXCLUDED**: with LN0 bring-up proven, a
  full boot-window uart0 capture around a coordinated POR replay +
  SS-root-port warm cycle shows **zero LFPS bursts ever on lane 0**,
  matching lane 1 and the dark vendor gold baseline.  Both Type-C
  orientation pairs are silent ⇒ the bench USB3 path is physically
  disconnected (or dead), full stop.  The replug instruction below
  stands; orientation no longer needs guessing (though after replug,
  straight = LN1 = the resident image remains the expectation).
* Resident image: the lane-1 #38-fix build (payload-identical to the
  POR-66_011 build that was already resident).  Saved copies in
  /tmp/kilo: `luna_multiep_lane1_por66011.fs`,
  `luna_multiep_lane0v2.fs` (LN0, pclk roll 121.6 — probe only, do
  NOT ladder it).

### Addendum 2026-08-31 (session 11c) — BENCH RESTORED; GATE G0
### CLOSED on hardware

The USB-C was replugged (new location: **10 G root port `usb 4-3`** —
supersedes the old 4-9 bench fact; verify with dmesg after any future
recabling).  Orientation was confirmed by probing BOTH pairs with
fresh POR windows: straight (LN1) trains, flipped (LN0) sees nothing
— the plug is in the correct (straight) orientation for the shipping
LN1 configuration.

Port capability pinned for Phase 5: the vendor gold `prj.fs`
enumerates **SuperSpeed Plus Gen 2x1 (10000M) on 4-3** — the port is
Gen2-capable; baseline reconfirmed post-fork.

**G0 hardware ladder (resident image: the fork build, POR 66_011,
pclk 139.0 — payload-identical to the #38-fix tree; this run is also
the FIRST hardware exposure of the session-10-tail rule-2d / #36 /
force-recovery-hook changes):**

| rung | result |
|------|--------|
| enumeration | `1209:0001` SuperSpeed on 4-3; textbook training burst (26 LFPS, 986 TS1, rx_com lock; flags d) |
| multiep 1 MiB ×10 --eps 1,2,3 | PASS ×10, sha exact, 255–268 MB/s aggregate |
| multiep 16 MiB ×3 | PASS, 94.5 MB/s per direction each, **283.6 aggregate**, sha exact |
| multiep 64 MiB ×3 | PASS, 93.8 MB/s each, 281.5 aggregate, sha exact |
| soak 64 MiB ×3 pipes ×3 consecutive | ALL PASS, 284.4–285.6 MB/s aggregate |
| uart1 through the 64 MiB run | **ch0 retry_flagged=0**, ch1/ch2=0, flags=8 only |
| restore + re-verify (current tree's build flashed) | enumerates, 1 MiB PASS 265 MB/s |

**Gate G0 is CLOSED**: fork layout parity on sim (pytest 104/104,
battery 35/35) AND hardware (ladder at session-10 shipping numbers).
Phase 2 (the Gen2 link-partner sim) is unblocked, per the G1 design
note.

### Session-11 regression state

pytest 104/104; battery 35/35 PASS lines (= §10n's 38-entry
accounting: 29 loopback configs, endpoint-sim, pytest(104), 2
training sims, stale-ack, tx-fuzz); byte-identical-fork and
one-clone gates green.  Bug numbering now at **#38 (closed,
session 11b — adapter lane/CSR mismatch)**; **#37 still open**.  All parked items from §10n carry over verbatim
(#37 + forced-recovery harness feed truncation, rule-2d/#36 positive
stimuli, bench forced-recovery verdict for #29–#31, data_tx SEND_ZLP
bare-ready, wire-checker TP blindness).

## 10p. Update 2026-08-31 (session 11d) — Phase 2: the Gen2 link
## partner exists; oracle GREEN, red baselines RECORDED (gate G2 red
## half done)

Phase 2 per prompt.md, sim first, real coding chain at both rates.

### New files (sim/)

* **`gen2_coding.py`** — the host-side Gen2 coding oracle: 23-bit
  scrambler LFSR (matrices imported from `gw_usb3.lfsr` — the same
  source the RTL XOR networks are generated from), 132-bit block
  assembly (64-bit beats, symbol 0 in bits [56:64]), the per-block
  scramble/bypass/freeze/reset rule machine, ordered-set builders
  (SYNC/TSEQ/TS1/TS2/SDS/SKP), Table 6-2 framing symbols, Gen2 link
  command (4-bit subtype) and header-packet builders (CRC-5/16
  reused from the Gen1 host model).
* **`sim_gen2_oracle.py`** — battery entry `gen2-oracle`, GREEN
  REQUIRED: pins the python model byte-exact against the
  silicon-proven RTL `gw_usb3.scramble.Scrambler`/`Descrambler` over
  a 44-block battery (91 beats TX-exact, RX recovered; SKP splice,
  reseed, SYNC reset, TS lanes all covered).
* **`sim_link_gen2.py`** — the end-to-end Gen2 link partner: DUT =
  the full unmodified `USBSuperSpeedDevice` on a bare 64-bit PIPE;
  host->device beats go python-scramble -> REAL RTL Descrambler ->
  PIPE RX (the PHY topology), device->host beats go PIPE TX -> REAL
  RTL Scrambler -> python descramble (the real chain in the loop
  both directions).  Phases: `PHASE=scd` (Polling.LFPS SCD1
  tRepeat modulation + device burst classification), `PHASE=train`
  (SYNC/TSEQ/TS1/TS2 blocks -> SDS -> Idle), `PHASE=enum`
  (advertisement modulo-16 + LCRD1/LCRD2 + GetDescriptor —
  scaffolding past training, completed with Phase 4).

### The recorded RED baselines (G2 red half; keep these quotes)

* `PHASE=scd`: device transmits textbook Gen1 Polling.LFPS —
  measured burst gaps `[8.0 us x16]`, classified bits all 0 →
  **"SCD FAIL: non-varying tRepeat, no SCD1 signature (Gen1-only
  Polling.LFPS)"**.  (The device DOES poll in the bench: bring-up =
  TUSB phy_status dialect + PIPE power-state ack emulation.)
* `PHASE=train`: **"TRAIN: device emitted 0 block-format TS1
  ordered sets (0 blocks total from device TX)"** — the Gen1-only
  MAC never drives tx_datavalid/block signals.

### Battery: new `gen2` section (BATTERY4)

`gen2-oracle` expect-green; `gen2-scd`/`gen2-train` run in
EXPECTED-RED mode: the battery PASSES while they fail with their
verdict and TRIPS if one unexpectedly goes green — flipping an entry
to expect-green is a conscious act when the Phase-3/4 device work
lands.  All Gen1 entries untouched.

### PIPE-contract discoveries (now in doc/gen2_design.md §9.1)

The oracle iterations pinned real Phase-4 contract details: the PHY
descrambler DROPS SKP beats from its PIPE output (SKP never reaches
the MAC); the RxGearbox132 extracts the SKP-carried LFSR seed onto
`descrambler_init` (acquisition-only, alignment-neutral in-sync);
the SKP splice carries the FROZEN TX LFSR state (bit23 = ~bit22) —
a spliced ADVANCED state would desync the pair by one 64-step
advance (my first splice attempt did exactly that; the oracle
caught it).

### Bench facts for the Gen2 sims

* Full-device Gen2 sims are heavyweight: PHASE=scd ≈ 85k ss cycles.
  Run as `.venv/bin/python -u` (same rule as ever); battery entries
  log to /tmp/kilo/batt_gen2_*.log.
* The bench PIPE bring-up dance matters: phy_status must stay HIGH
  until the MAC releases pipe.reset (TUSB dialect), and every
  power_down change needs a phy_status ack pulse — without these the
  LTSSM parks silently (found the hard way, 10o-style).

### Next (Phase 3, per the G1 design note)

LTSSM SCD1 tRepeat modulation + LFPSPlus/PortMatch/PortConfig
substates + LBPM modem + LTSSM-driven serdes rate switch; flip
`gen2-scd` to expect-green when the SCD exchange lands.  Then
Phase 4: block-level OS gen/detect + Gen2 framers (flip
`gen2-train`).  #37 and the 10n parked items still carry.

## 10q. Update 2026-08-31 (session 11e) — Phase 3 mechanisms 1+2:
## SCD1 declaration + Polling.LFPSPlus/SCD2 exchange SIM-GREEN;
## gen2-scd flipped to expect-green

Phase 3 (LTSSM + rate switch), first two mechanisms, sim-first, one
mechanism per change:

### Mechanism 1 — SCD1 tRepeat modulation (TX)

* `physical/lfps.py`: `LFPSGenerator(..., scd_pattern=None)` — with a
  pattern, each burst's repeat interval is modulated per [6.9.4]
  (SCD_REPEAT_0=7.0 us / SCD_REPEAT_1=13.5 us — mid-bin typicals);
  `None` elaborates the historical fixed-repeat generator unchanged.
  `SCD1_PATTERN=(0,1,0,0)`, `SCD2_PATTERN=(1,0,1,1)` (wire/LSb-first
  of '0010'/'1101').
* Threaded as `USBSuperSpeedDevice(gen2=False)` →
  `USB3LinkLayer(gen2)` → `LTSSMController(gen2)` and
  `USB3PhysicalLayer(scd_pattern)`.  **gen2=False (default
  everywhere, incl. all hardware tops) is the forced-Gen1 knob and
  elaborates the proven Gen1 stack unchanged.**

### Mechanism 2 — SCD RX + Polling.LFPSPlus

* `physical/lfps.py` `SCDDetector`: classifies received burst
  start-to-start periods (generous bins: bit0 4.5-9.9 us, bit1
  10.5-18 us — tRepeat is burst-inclusive!) into a sliding 4-bit
  window, matches SCD1/SCD2 in any cyclic rotation (both patterns
  are single-outlier codes, so rotation matching is reversal-safe);
  sticky outputs + clear.
* `LFPSGenerator.scd2_select` input: runtime switch SCD1→SCD2.
* `ltssm.py` (gen2-gated): Polling.LFPS gains the SCD exchange —
  partner SCD seen → two more SCD1s (8 bursts) → new
  **Polling.LFPSPlus** state (SCD2 both ways, exit after 2 SCD2 sent
  post-receipt) → Polling.RxEQ.  A partner that never declares
  leaves the LEGACY Gen1 handshake in charge (the Gen1 fallback
  path, unchanged code).  PortMatch/PortConfig (LBPM rate select)
  are the NEXT mechanisms — LFPSPlus currently proceeds straight to
  training, matching a Gen 1x1-only match outcome.
* **Latent bug fixed en route**: `USB3PhysicalLayer` never passed
  `sync_frequency` into `LFPSTransceiver` (always 125e6 constants) —
  harmless while ss==125 MHz, wrong at the Gen2 operating point.
  Pass-through is elaboration-identical for the 125 MHz builds.
  (Found because the SCD classifier mis-binned at 156.25: the race
  then let the legacy handshake exit to RxEQ before scd1_detected —
  device went silent in stage 2 of the sim.)

### Sim + battery

`sim_link_gen2.py` PHASE=scd is now the full two-stage exchange:
stage 1 host SCD1 → require device SCD1; stage 2 host SCD2 →
require device SCD2 (LFPSPlus).  GREEN: stage-1 device gaps
7.0/13.5 us exact, bits (0,1,0,0)*; stage-2 bits (1,0,1,1)*.
Battery `gen2-scd` flipped to expect-green (the conscious flip);
`gen2-train` stays expected-red (flips with Phase 4).

NOTE (lesson): do NOT run the battery concurrently with source
edits — entries elaborate the live tree; a mid-edit battery run
produced 13 phantom FAILs (UnboundLocalError from a half-applied
LTSSM edit).  Battery verdicts only count from a settled tree.

Second real catch: the link-layer SCD wiring must be gated under
``if self._gen2:`` — the Gen1 link-loopback sims drive USB3LinkLayer
with a ``FakePhysicalLayer`` stub that has no SCD attributes; the
unconditional wiring broke ALL 29 loopback entries at elaboration.
Settled-tree battery after the fix: **38/38** (all Gen1 entries
green, gen2-oracle green, gen2-scd GREEN first-class, gen2-train
enforced-red).  Shipping-parity: luna-multiep rebuilt from this tree
(gen2=False default) — bitstream payload-identical to the resident
POR-66_011 image (header timestamp bytes only).

### Phase-3 remaining (next mechanisms)

M3: LBPM PWM modem (TX shaping + RX classifier) + Polling.PortMatch
/ PortConfig with PHY Capability/Ready LBPMs [6.9.5, 7.5.4.5/.6],
rate-select output; extend PHASE=scd (or new PHASE=lbpm) red-first.
M4: LTSSM-driven serdes rate switch through the adapter (both
directions) + PIPE rate plumbing.  M5: fallback matrix sims
(no-SCD1 → legacy Gen1; Polling.Active/Config timeout →
PortMatch re-entry next-highest).  Then Phase 4 (block framing).

## 10r. Update 2026-08-31 (session 12) — GATE G3 CLOSED (negotiation)
## and GATE G4 CLOSED on sim (Gen2 framing through the stack):
## gen2-train/enum/echo GREEN end-to-end through the RTL coding chain

Executed prompt.md Phases 3 (remainder) and 4, sim-first.  Bug
numbering: no new numbered stack bugs (#39 next); the session's
findings were all caught pre-commit by the red-first sims and unit
benches (see "bugs caught in development" below).

### Phase 3 M3–M5 (gate G3) — commit bb4bf07

* **M3a — LBPM modem** (`physical/lfps.py`): `LBPMTransmitter` (tPWM
  2.2 µs PWM shaping, delimiter-framed LSb-first bytes [6.9.5.2]) and
  `LBPMReceiver` (Table 6-33 ON-width classifier: bit0 0.45-0.9 µs,
  bit1 1.15-1.9 µs, delimiter ~2-3.2 µs; >6 µs silence resets
  framing).  Dev-time catch: `message` is registered, so the valid
  strobe must be registered WITH it — the first cut strobed
  combinationally and consumers sampled the previous byte (found by
  the lbpm_unit bench; the PortMatch machine then "negotiated down"
  on a phantom 0x00 capability).
* **M3b — Polling.PortMatch/PortConfig** (`ltssm.py`, gen2-gated):
  match rule 4-matched-sent-after-2-matched-received, higher port
  adjusts down, PHY Ready handshake, shared 12 ms
  tPollingLBPMLFPSTimeout → SS.Disabled (peripheral rule), entry
  advertisement highest (from LFPSPlus) vs next-highest (from
  training timeouts).
* **M3c — rate plumbing**: LTSSM `rate_select/rate_request/rate_done`
  ↔ physical-layer rate sequencer (gen2 builds own `pipe.rate`,
  Gowin encoding 0=5G/1=10G, boots 1; a change is acked by a PIPE
  phy_status pulse — the sim stub acks like the adapter; the ADAPTER
  CSR hookup itself is G5 work, see below).  `Polling.SpeedSwitch`
  (synthetic) funnels every SS fallback through the 5G switch before
  RxEQ.
* **M3d — fallback matrix**: 16-legacy-burst + 60 µs
  tPollingSCDLFPSTimeout rules in Polling.LFPS [7.5.4.3],
  64-burst-no-SCD2 + 20-non-varying rules in LFPSPlus [7.5.4.4]
  (closes the §10q "keeps modulating" note), Gen2 training-timeout
  loop: Active/Configuration/Idle timeouts at SSP → PortMatch with
  next-highest [7.5.4.8.2] (`ssp_operation` selects it — a device
  that negotiated DOWN to 5G but did the SCD handshake still returns
  to PortMatch, per spec).
* Sim: `HostModem` (PWM modem + PIPE pd/rate-ack stubs) + phases
  `lbpm`, `lbpm5g`, `fb-legacy`, `fb-noscd2`, `fb-timeout`; red
  baselines recorded against the G3-less stack first (logs
  `/tmp/kilo/red_gen2_*.log`): lbpm* red = "no LBPM from device";
  fb-legacy red = "keeps modulating [7.0, 13.5, ...]"; fb-noscd2 red
  = SCD2 forever; fb-timeout red = no PortMatch.  Sim-only knobs
  `polling_timeout_scale` + `tseq_burst_length` threaded through
  `USBSuperSpeedDevice`; the link layer now receives
  ``ss_clock_frequency=sync_frequency`` (identical at 125 MHz,
  correct timers at 156.25).
* Gate G3 evidence: battery 43/43 from a settled tree; pytest
  104/104; luna-multiep rebuild payload-identical to the resident
  POR-66_011 image (4 timestamp bytes only).

### Phase 4 (gate G4, sim side) — the framing delta table executed

New file `physical/gen2.py` (stage A per doc/gen2_design.md §1/§2):

* **Gen2BlockTransmitter**: block scheduler — TSEQ (SYNC every
  16384), TS1/TS2 (SYNC every 32; burst_complete every 16, the
  cadence the LTSSM already expects; Gen2 TSEQ count = 8× Gen1 =
  524,288, scaled by the sim knob), single SDS on idle-mode entry
  [7.5.4.10], SKP OS every 40 blocks [6.4.3.3] as whole 24-symbol
  blocks (the PHY splices the LFSR), data blocks from the TX bridge.
* **Gen2TxBridge** (32→64): captures whole packets from the arbiter
  stream (first-marker delimited; whole-packet buffering keeps DPPs
  wire-contiguous at the 2× beat rate), maps Gen1 K-framing to the
  Table 6-2 symbols at enqueue, patches DATA-type headers to
  DPHSTART framing and inserts the 2-byte length replica (device
  never emits deferred DPHs), pads packet tails with Gen2 Idle
  Symbols.  Dev-time catch: Gen1's unaligned-DPP tail words carry
  post-EPF 00h IDL filler — those must map to 5Ah on the Gen2 wire
  (the host parser flagged raw 00h symbols).
* **Gen2BlockReceiver**: control-block classification (TS1/TS2/TSEQ
  8/8/32-consecutive with symbol-14/15 exclusion and SYNC
  transparency [7.5.4.8.2], TS2 config bits, SDS→data_mode) + the
  byte-granular grammar engine (4 symbols/cycle) translating data
  blocks back to the Gen1 K-dialect: HPSTART/DPHSTART/DPPSTART/
  LCSTART recognition at ANY symbol offset, DPH length-replica
  swallow, DPP extent by DPH length field, DPPEND/DPPABORT, out-FIFO
  word packing with idle-pad flush on construct end.  THREE dev-time
  catches, all by unit bench + the enum phase:
  1. SyncFIFOs elaborated in the ``sync`` domain (invisible in the
     full-device bench where sync==ss, dead in isolation, WRONG on
     hardware) — DomainRenamer'd to ``ss``.
  2. mid-construct output-rate dips (the replica skip) must present
     ``valid=0`` toward the core, NOT synthesized idle — an idle word
     between DPH and DPP makes the Gen1 data receiver bail (this was
     the missing-ACK-TP symptom).
  3. whole-idle beats must be DISCARDED at the engine's load point at
     full beat rate — enqueueing them floods the queue (8 in vs 4
     out sym/cycle) until it silently drops a mid-packet beat (the
     LBAD-on-second-SETUP symptom).  Payload beats that HAPPEN to be
     all-5A are protected by the state gate.
* **Dual-rate muxing** (`physical/layer.py`): at rate_r==1 the Gen2
  block path owns the PIPE TX/RX and the Gen1 scrambler/CTC/aligner
  chain is starved; at rate_r==0 the original Gen1 chain elaborates
  its historical statements verbatim.  Link layer muxes the TS
  detect/emit/burst_complete surfaces by `operating_gen2`.
* **Link-layer SSP trims** (`transmitter.py`/`receiver.py`,
  elaboration-gated `gen2=`, runtime-selected `gen2_active`): the
  4-bit sequence number's top bit rides in the LCW's SS-reserved bit
  = `dw3_reserved[0]` — so the DW3 packing and CRC-5 paths carry it
  with ZERO shared-code changes; modulo-16/modulo-8 by mask mux;
  LCRD1/LCRD2 split per Table 7-4 **Gen 2x1 trim: the series select
  is subtype b2** (b3 is reserved — the session-11d host scaffolding
  had guessed b3; fixed); TX: dual pools, DATA-type headers draw
  Type 2; RX: shared 4-buffer pool split 2+2 with per-class credit
  queues, independent A-D indices, rate-aware link-up recompute and
  per-class rule-2d re-advertisement.  Stage-B note: 4+4 pools want
  8 physical buffers.
* **Enum surface**: bcdUSB 0310 in the sim descriptors; sim phases:
  `enum` = advertisement (device: LGOOD_15 + LCRD1_A,B + LCRD2_A,B —
  asserted exactly), link-up LMP ack, SET_ADDRESS, GetDescriptor
  (device descriptor read over Gen2 framing: DPHSTART + replica
  validated, CRC-32 checked, bcdUSB 0310 asserted); `echo` = 64-byte
  bulk OUT+IN loopback through EP1, payload exact.  Negative control
  `NEG=nolcrd2` (battery entry `gen2-neg-nolcrd2`): withholding host
  Type-2 credits must starve the descriptor DP while ACK TPs still
  flow — proves the pool gating (the "red-equivalent" for the P4.6
  checks; NOTE: the strict extend-host-checks-first-then-port order
  was compressed here — device and checks landed in one edit batch;
  the negative control + the 11d scaffolding red stand as evidence).
* Battery: `gen2-train` CONSCIOUSLY FLIPPED to expect-green (its
  negotiate-first red re-recorded: "0 TSEQ + 0 block-format TS1");
  new expect-green entries `gen2-enum`, `gen2-echo`,
  `gen2-neg-nolcrd2`.  47 PASS lines total expected.

### G5 groundwork done here: the first Gen2 hardware elaboration +
### the rung-1 timing verdict (NOT met yet; diagnosis in hand)

* `examples/gowin/luna-enum-gen2/`: the first `gen2=True` hardware
  top (10G boot trim, byte-pinned blob, no boot_rate_switch -- the
  LTSSM owns the rate; bcdUSB 0310; **built, never flashed**).
  `GowinGTR12PIPE(gen2=True)`: PHY built with its Gen2 datapath +
  rate_init=1; forwards the MAC-owned `rate` to the PHY's CSR
  sequencer and synthesizes the PIPE rate-change ack after the boot
  path's proven ~7 ms envelope (no CSR completion feedback yet);
  `ltssm_training` input for the Gen2 descrambler acquisition
  (approximated in the top as terminations-engaged-and-not-trained).
  Adapter changes are python-gated; both gowin_gtr12 sims re-spot-
  checked PASS after the edit.
* **Timing roll 1** (probes in): pclk Fmax 70.6 @ 22 levels -- every
  top path INSIDE the debug ClockFreqProbe (snap/delta arithmetic;
  fine at 125, not at 156.25).  The probes need a pipelined delta
  (gowin-serdes change) before any Gen2 bench build carries them;
  this top disables them for now.
* **Timing roll 2** (probes out): pclk Fmax 71.7 @ 22 levels -- the
  REAL cone: `gen2_rx` grammar engine, `fr_kind` through the 4-slot
  chained emit logic into the collector/out_fifo write
  (`col_data*/out_fifo`).  Fix path: register the per-slot emissions
  ahead of the collector (the path is elastic end-to-end -- out_fifo
  absorbs a cycle of emission latency by design), or split the slot
  chain 2+2 with a pipe stage; re-run gen2-enum/echo after (cycle
  exactness is not load-bearing anywhere in the engine).  ALSO note
  `serdes_pcs_rx_clk_i` Fmax 114.9 @ 16 levels -- the PHY's own Gen2
  RX domain also runs 156.25 at 10G and needs attention (vendor-
  proven on silicon, so likely placement/constraint-reachable).
  Constraints are still the 100 MHz serdes-attach bases; the gate is
  Fmax >= 156.25 either way.

### Session-12 regression state

Battery **46/46** PASS lines from a settled tree (35 Gen1-era entries
untouched + gen2: oracle, scd, lbpm, lbpm5g, fb-legacy, fb-noscd2,
fb-timeout, train, enum, echo, neg-nolcrd2); pytest **104/104**;
shipping parity proven TWICE this session (after G3 and after G4:
luna-multiep rebuild payload-identical to the resident POR-66_011
image, 4 timestamp bytes only).  Both gowin_gtr12 sims spot-checked
PASS again after the adapter dual-rate edit (which battery entries
also cover on the next full run).  Commits: `bb4bf07` (G3),
`5514c5c` (G4 sim), `cfeb27c` (G5 groundwork); all pushed; no
submodule changes.  Bug numbering still at #38 closed / **#39 next**;
#37 and all §10n/§10q parked items carry.

**The resident bench image is still the Gen1 shipping build**
(POR 66_011, pclk 139.0, enumerated SuperSpeed on 4-3 at session-11c
close).  The bench has NOT been touched this session; no Gen2 image
was ever flashed.

### Battery-entry runtimes (so nobody kills a slow entry)

gen2-scd/lbpm* ≈ 1-3 min each; gen2-fb-* ≈ 2-5 min; gen2-train ≈
3-5 min; gen2-enum/echo ≈ 4-6 min (negotiation + training + the
whole exchange); full battery ≈ 35-45 min.  Always
`.venv/bin/python -u`, never concurrent with source edits.

### Parked / next-session (G5) — NOT DONE here, in priority order

1. **Adapter rate handshake on silicon** (M3c hardware half): wire
   `GowinGTR12PIPE` for gen2 builds — consume `self.rate` into the
   CSR sequencer (rate_change_table both directions), ack with a
   phy_status pulse, reuse the #22 boot-window discipline.  The
   boot_rate_switch (Gen1 ships 10G→5G pre-MAC) must become the
   LTSSM-driven path when `gen2=True`.
2. **Gen2 hardware top**: no example builds `gen2=True` yet.  Start
   luna-enum-sized (add the SSP BOS device capability LSE=3/LSM=10
   LP=1 and bcdUSB 0310 to its descriptors).  **Gen2 gate: 156.25
   operating MET** before any flash.
3. **Sublink Speed Device Notification TP** on Address-state entry
   [8.5.6.7] — not implemented; real xHCI behavior without it is
   unverified.  Small protocol-layer TP source, gen2_active-gated.
4. TX beat pacing for the real PHY: the gw_usb3 TX path has a
   32-deep FIFO + `TxFifoWrNum` (vendor MACs throttle on it); the
   sim bench is always-ready.  Expose it through the adapter or pace
   1-gap-in-33 beats.  Also: `LTSSM_is_Training` is tied 0 in the
   adapter — the PHY's Gen2 descrambler consumes it; wire it to the
   LTSSM training states for hardware.
5. BurstEventCapture port to Gen2 framing (the G4 gate text asks for
   it NOW; not done — do it before believing any Gen2 bench numbers,
   it is how #34 fell).
6. RX queue sizing verdict: `Gen2BlockReceiver.queue_level` +
   `packets_buffered` debug taps exist; calibrate on the Phase-5
   throughput traces (design note §9.4).
7. All §10n/§10q parked items carry (incl. #37, SKP x=4 knob when
   word_alignment opens, forced-recovery bench verdict).

## 10s. Update 2026-08-31/09-01 (session 13) — G5 phase H0 CLOSED
## (Gen1 fence re-laddered) and phase H1 CLOSED (Gen2 156.25 MET:
## pclk 156.263 / rxclk 169.777); TX pacing + RX engine v2 landed

Executing prompt.md (session 13, gate G5).  No new numbered stack
bugs (#39 still next); one latent gen2-only hazard found by
inspection and fixed pre-silicon (see below).

### Phase H0 — the Gen1 fence (CLOSED)

luna-multiep rebuilt from the tree: payload-identical to the
resident POR-66_011 reference (5 timestamp bytes).  Timing pclk
139.0 / rxclk 149.9 (the shipping roll).  Flashed; full ladder:

| rung | result |
|------|--------|
| enumeration | 1209:0001 5000M on 4-3, dmesg clean, flags d |
| 1 MiB ×10 --eps 1,2,3 | PASS ×10, sha exact, 243.8–268.0 MB/s aggregate |
| 16 MiB ×3 | PASS, 276.0–284.4 MB/s, sha exact |
| 64 MiB ×3 | PASS, 280.4–282.2 MB/s, sha exact |
| uart1 ch0 | retry_flagged=0, all counters 0, flags=8 |

Fence image saved: `/tmp/kilo/h0_gen1_fence.fs` (and resident on the
board through H1).

### Phase H1 — 156.25 MET (the Gen2 flash gate; CLOSED)

The §10r roll-1 "probe cone" was a MISSING CONSTRAINT, not the probe:
`luna_enum_gen2` was absent from the platform's SDC branch, so PnR
targeted the 100 MHz default and the skew-tolerant ss->dbg snapshot
CDC was analyzed as a real inter-clock path.  Fixes, in order (each
sim-green before the next roll; all Gen1-shared changes are
elaboration-gated `gen2=` and the Gen1 netlist stays byte-identical):

* **SDC (gowin-serdes)**: `luna_enum_gen2`/`luna_multiep_gen2` added
  to the 6.4 ns pclk/rxclk branch + mutual false paths; gen2 tops
  additionally get `set_multicycle_path 2` on
  `usb/physical/operating_gen2*` (toggles only on an LTSSM rate
  change, always followed by ms of retraining — same argument as the
  vendor `speed` register).  NOTE: Gowin TA hard-errors on get_regs
  patterns that match nothing (a `rate_r*` pattern had to be
  dropped).
* **Probes re-enabled** in the gen2 top (uart0 link probe + uart1
  pipe probe with TxFifoWrNum high-water channels).  PITFALL
  re-learned: `DomainRenamer({"cfg": "dbg"})`, NOT
  `DomainRenamer("dbg")` — the string form renames `sync` only and
  the probe silently lands on the top's 200 MHz `cfg` domain (wrong
  timing AND ~8× baud error).
* **gen2_rx grammar engine v2** (physical/gen2.py): the v1 4-slot
  CHAINED walk was the real cone (22 levels; 16 after registering
  emissions).  v2 removes chaining entirely: BULK steps (DPP
  payload, header body, LC body, aligned idle runs) consume a whole
  aligned 4-symbol half per cycle with one parallel count update;
  BOUNDARY steps (framing/header tail/terminators/replica skip)
  consume ONE symbol per cycle, unchained.  Sustained rate stays
  ~4 sym/cycle for payload (boundaries are O(1)/construct).  Plus:
  emission pipeline stage before the collector; registered out_fifo
  headroom (`out_ok`) instead of comb w_rdy; 2-deep ring-pointer
  read prefetch on the input queue (r_en/level decoupled from the
  walk); per-half idle flags precomputed at beat load; whole-idle
  flag stored AT ENQUEUE (65-bit queue) so the read side never
  re-derives it; PIPE inputs registered at the receiver front.
  Latent v1 hazard FOUND BY INSPECTION and fixed: the reload-path
  idle discard gated on the REGISTERED state while the same-cycle
  walk had already left SEARCH — an all-5A payload beat straight
  after framing could be wrongly discarded (v2 adds the
  ``search_exit`` qualifier; enqueue-side drain check also covers
  the prefetch skid).
* **TX beat pacing** (§10r suspect #1, closed pre-silicon): 64-bit
  beats at 156.25 supply exactly 10.0 Gb/s payload but the 128b/132b
  wire carries 128/132 of that — the PHY's 32-deep TX gearbox FIFO
  gains one beat per 33 cycles and overflows after ~7 us (shorter
  than any training sequence).  RED first: tests/test_gen2_pacing.py
  streams the transmitter against the FIFO model (unpaced max
  occupancy 182/32 at 6k cycles); mechanism: ONE dead beat at a
  block boundary every 16 blocks (32+1 = 33 cycles = 16×132 wire
  bits at 10G — EXACT, and a 24-symbol/3-beat SKP OS carries the
  same per-block deficit so the ratio stays exact); the adapter
  forwards true tx_datavalid at the 10G trim (the Gen1
  "valid-when-not-idle" OR rule would nullify the gaps).  The full
  sims report the model's occupancy (steady 1-2/32); battery entry
  `gen2-pacing` (the fork-root pytest testpaths only cover
  gw_usb3/tests — the new test rides as its own battery entry).
* **DataPacketReceiver CHECK_CRC32 valid gate** (gen2= elaboration
  arg): the historical state consumes the CRC-32 word UN-gated by
  sink.valid — legal at Gen1 (SKPs are forbidden inside packets, the
  wire never gaps mid-packet) but the v2 engine's sym-wise construct
  tails present valid-gaps there (found by the enum phase:
  dpp_invalid on the SETUP DP).  Gen1 elaboration verbatim.
* **Seam registers** (all gen2-gated or gen2-only; each proved by
  the phase sims): LBPM TX merge registered in lfps.py; muxed RX
  source registered at the physical->link seam (link holds
  source.ready high — plain register is exact); gen2 TS-detect
  surfaces registered at the seam AND input-registered in the LTSSM
  (aliases; Gen1 keeps direct wiring); ts_burst_complete +
  trigger_link_recovery aliased the same way; gen2_tx LTSSM control
  surface registered both directions; second TxStreamSkidBuffer on
  the gen2 TX leg; TX bridge serves beats from a 1-deep prefetch
  register; LTSSM ``cycles_in_state`` clear via a registered
  ``transitioning`` bit with timeout-hit suppression while the clear
  is pending (state timeouts fire two cycles later — noise);
  PIPE LFPS/idle control outputs registered (gen2 arm).
* **The lottery** (POR nudges 66_012..66_030, several in parallel
  scratch dirs /tmp/kilo/gen2roll*): pre-cut center pclk ~147; after
  the full batch, winner **66_021 = pclk 156.263 / rxclk 169.777 —
  BOTH MET**.  In-tree rebuild reproduces the identical result
  (deterministic PnR; .fs differs from the scratch build by
  timestamp only).  Image: `/tmp/kilo/h1_gen2_enum_met.fs`.

Gen1 parity: luna-multiep rebuilt after ALL shared-file changes —
payload-identical to the H0 fence image (13 header bytes = the
"Mon Aug 31" -> "Tue Sep  1" date-string rollover; nothing beyond
offset 621).  NOTE for future compares: the "6 timestamp bytes"
rule of thumb widens across midnight/month boundaries — the honest
check is "all diffs inside the ~600-622 header date region".

### Session-13 regression state (as of H1 close)

Battery 46/46 PASS mid-session (run 1, pre-cut tree) and re-run
post-cuts (run 2, this tree) — see /tmp/kilo/battery_s13_run*.txt;
pytest = gw_usb3's 104 (testpaths pitfall above) + the 3 pacing
tests via the new battery entry (47 PASS lines expected from now
on).  Bench: H0 fence ladder green; the Gen2 image NOT yet flashed
at this point in the log (phase H2 next).  sim/rx_unit_debug.py
added (standalone Gen2BlockReceiver translation bench — the fast
debug loop that pinned the CHECK_CRC32 interaction).

### Phase H2 — first Gen2 silicon exposure: bugs #39 + #40 found &
### fixed; the link TRAINS at Gen 2x1 and enters U0; enumeration
### still dies on the first control exchange (OPEN)

Flash 1 (the H1 image, POR 66_021): the host attempted SET_ADDRESS
("Device not responding to setup address", -71).  Probe decode: 38
LFPS bursts, 4078 TS1 + 112 TS2 detects, pclk at the 156.25
signature (0x341556x) during training — negotiation and Gen2 block
training on REAL LFPS hardware work — but link_trained never rose;
the device dropped terminations and fell back to 125 MHz ~0.7 s in.

**Bug #39 (FIXED, silicon-verified): the ``LTSSM_is_Training``
approximation arms a lethal polarity walk.**  The PHY's Gen2
rx-polarity acquisition (scramble.py) counts inversion signatures on
the RAW first symbol of every data block while LTSSM_is_Training is
high (counter init 7, threshold 15, sticky once tripped; TS blocks
decrement).  The top's approximation (terminations & ~link_trained)
stays high through the whole U0-entry window, where SCRAMBLED
logical idle matches at P≈3/256 per block with no TS decrements —
sticky lane inversion within tens of microseconds.  Fix:
``ltssm.in_training`` (real training-state output: Polling.RxEQ/
Active/Configuration(.Exit), Hot Reset.Active, Recovery arms),
surfaced link→device→top.  SILICON VERDICT with the fix: **flags
reach 'd' (trained); dmesg prints "new SuperSpeed Plus Gen 2x1 USB
device"** — the LUNA stack's first Gen2 identification on hardware.
Probes: sds_detected/idle_complete counted ~65 train→U0→drop cycles
per boot; each U0 died on the host's first control exchange
("device descriptor read/8, error -71").

**Bug #40 (FIXED, sim red/green): scheduled SKP OS inside packets.**
[6.4.3.3]: "SKP Ordered Sets shall not be inserted within any
packet" — the block scheduler fired its 40-block interval at EVERY
block boundary, splitting DPs; the real xHC rejects them, the
FORGIVING bench host (parser drops control blocks) hid it.  Fixes:
bridge ``pkt_in_flight`` (first served beat → eop) + scheduler
deferral (gap saturates at 2× interval); the bench host is now
STRICT — red recorded ("control block (first sym 0xcc) inside a
packet"), green with the fix.  Bench-model fidelity gaps the debug
forced: feed_blocks now emulates the RxGearbox132 SKP-LFSR-seed
extraction into descrambler_init (else the RTL descrambler reseeds
from ZERO on SKP and everything after descrambles to garbage — sim
artifact, not a stack bug), and the train/enum feeds interleave SKP
OS like a real partner.

**H2 state at session end (OPEN — the remaining U0-death):** with
both fixes (POR 66_033, pclk 156.263/rxclk 157.158 MET, battery
47/47 run 4): the device negotiates, trains, reaches U0 ~5×/boot
(sds/idle_complete counters), recovery strobes seen, host walks the
link down; vendor-gold A/B mid-debug re-proved the port at 10000M.
TX pacing confirmed on silicon (zero TxFifoWrNum≥28 events through
full training).  The next discriminator is IN THE TREE: the gen2
top's uart1 now carries the multiep BurstEventCapture ring (first
64 header events after boot: 'T'/'D' TX dw0, 'A'/'R' RX dw1 with
dw0-type packed in bits[27:32]) — **that netlist has NOT won the
placement lottery yet** (14 rolls, best pclk 150.8; the 64×35 ring
hurts placement).  Do NOT flash any roll that misses 156.25.

Suspects for the U0-death, in expected order (all sim-uncovered
host behaviors — extend the strict host first, per discipline):
1. Host-side LUP watchdog: we may not emit LUP keepalives on the
   wire at Gen2 within tU0LTimeout (10 µs) — the sim host never
   checks.  Extend Gen2LinkHost.expect to REQUIRE LUPs at U0
   (red-first), and/or count LUPs on the wire tap in the capture.
2. Inbound host LMPs (Port Capability/Config SET from a real xHC —
   the sim host only ACKs, never sends its own LMPs).
3. Inbound ITPs every 125 µs (never sent by the gen2 sim host).
4. The enum-surface gaps (§10r suspect 4: no SSP BOS caps, no
   Sublink Speed Device Notification TP) — likely NOT the killer
   (the link dies at the LINK level before descriptors complete),
   but required for a clean 10000M lsusb eventually.

### Session-13 close-out state

* Bench RESTORED to the Gen1 fence image and re-verified: 5000M on
  4-3, 1 MiB ×3 pipes PASS (249.5 MB/s), 16 MiB PASS (281.7 MB/s).
* Battery runs: 46/46 (runs 1-2), 47/47 (runs 3-5, incl.
  gen2-pacing).  Gen1 shipping parity re-proven after EVERY
  shared-file batch (latest: 13 header-date bytes only — NOTE: the
  "6 timestamp bytes" rule widens across midnight/month rollovers;
  the honest check is "all diffs below offset ~622").
* Commits: gowin-serdes 313033d (SDC, pushed); fork 6abcd0d (H1) +
  41b98c4 (H2 bugs #39/#40) + this close-out; all pushed.
* Saved images (/tmp/kilo): h0_gen1_fence.fs (resident),
  h1_gen2_enum_met.fs (H1 gate build, pre-#39/#40),
  h2_gen2_debug_met.fs (#39 fix + debug taps),
  h2_gen2_skpfix_met.fs (#39+#40, POR 66_033) — all three Gen2
  images are timing-MET builds of their respective trees.
* Captures (/tmp/kilo): h2_first_flash/h2_por2 (pre-#39),
  h2_debug1 (post-#39: the trained-flag capture),
  h2_skpfix/h2_skpfix2 (post-#40); usbmon h2_usbmon_por1.txt
  (host port-status view: Inactive→warm-reset→Polling loops).
* Bug numbering: **#39 + #40 closed this session; #41 next.**
  #37 and all §10n/§10q parked items carry unchanged.
* G5 phase status: **H0 CLOSED (hardware), H1 CLOSED (hardware
  gate), H2 OPEN (deep in bring-up: train+U0 proven, first
  exchange dies), H3/H4 NOT STARTED.**  The wire-checker port
  finding for H3: the multiep taps sit on the dialect-neutral
  translated streams (tx_skid.source / debug_rx_hdr_*), so they
  carry to Gen2 unchanged — calibration on a quiet pipe remains.

## 10t. Update 2026-09-01 (session 14) — the WIDTH PROGRAM opens:
## gate W0 CLOSED (all four probes verdicted), BUG #41 (SSP LMP field
## rules) found by the new strict-U0 host, fixed, and WIRE-VERIFIED;
## the post-#41 Gen2 build now falls back and ENUMERATES at 5000M;
## Gen 1x2 negotiation surface landed (ssp_capability) and the
## PortMatch trace says port 4-3 is Gen 2x1-highest

Executing prompt.md (session 14, gates W0–W3).  W0 executed in full;
W1/W2 datapath work NOT started (this session's W2-relevant products:
the negotiation surface, the 125-MHz Gen1x2 build shape + SDC branch,
and the port-capability verdict below).  Bug numbering: **#41 closed;
#42 next** (suspect identified, see H2 state).

### W0.4 — H2 disposition: bug #41 (the U0 killer candidate), the
### strict-U0 host, and the new silicon state

* **PHASE=u0 strict host** (sim_link_gen2.py; battery `gen2-u0`): the
  three §10s U0 suspects became checks — LUP keepalives within
  tU0LTimeout [7.5.6.1], inbound host Port Capability/Configuration
  LMPs with the SSP field rules + REQUIRED Port Configuration
  Response, inbound ITPs (link-ack only), then a closing SET_ADDRESS.
  RED recorded (pre-fix): *"Port Capability LMP carries Gen 1x1-only
  field values at SSP operation: link_speed=1 num_hp_buffers=4"* and
  *"Port Configuration Response code 0x2 ... reads as 'Link Speed
  rejected' -> DFP port error [10.16.2.6]"*.  LUP + ITP checks were
  already GREEN (suspects 1 and 3 cleared in sim).
* **Bug #41 (FIXED, sim red/green, wire-verified)**: [Tables
  8-7/8-9/8-10] make Port Capability link_speed/num_hp_buffers, Port
  Configuration link_speed, and the Response Code all RESERVED-0
  when **not operating at Gen 1x1**.  The historical handler
  advertised 5GBPS/4-buffers and accepted only link_speed==1 — a
  conformant SSP host's link_speed=0 Port Configuration got
  CONFIGURATION_REJECTED, which a DFP reads as a port error →
  the U0 walk-down.  Fix in protocol/link_management.py,
  elaboration-gated `gen2=` (Gen1 statements verbatim), runtime
  `ssp_operating` = physical.operating_gen2 (Gen1x1-fallback keeps
  the historical field usage; Gen 1x2 will OR in its arm at W2).
* **Lottery**: pre-fix evcap netlist missed 17 rolls total
  (66_033..66_045, best 150.8 — abandoned); the post-#41 netlist won
  on roll 2: **POR 66_047 = pclk 156.307 / rxclk 162.692 MET**;
  in-tree rebuild reproduces (deterministic).  Image:
  `/tmp/kilo/h2_gen2_lmpfix_met.fs`.
* **Silicon verdict (flash + POR replay, reproducible)**: Gen2
  trains → U0 → our Port Capability LMP goes out with the conformant
  SSP fields (evcap `D00000080`) → **zero host header events reach
  the protocol layer at Gen2** → host declares `usb4-port3: config
  error` (~0.8 s) → device falls back per the ladder and
  **ENUMERATES at 5000M** with a clean Gen1 U0: host Port Capability
  (`R00010004`), host Port Configuration, our ACCEPTED response
  (`D000002c0`), then ITPs every 125 µs filling the ring.  Pre-#41
  this build class never enumerated at all — the fallback ladder is
  now silicon-proven end-to-end on the gen2 build.
* **H2 remains OPEN — #42 next**: the discriminator is now sharp:
  at Gen2 U0 the link-command plane works (advertisement completes
  → link_ready) but **no host header packet is ever delivered**
  (or none survives our RX chain: a CRC-failing header would LBAD
  silently — the ring taps only accepted headers).  Suspects, in
  order: (1) the Gen2 RX header path on silicon — RxGearbox132/
  elastic/aligner realtime behaviors the sim bypasses (the bench
  feeds the RTL Descrambler directly; the seed-extraction sim
  artifact of §10s is the precedent); (2) our Gen2 TX headers
  corrupt on the wire → host stalls its own LMP schedule (less
  likely: it should send Port Capability within tPortConfiguration
  regardless — and it didn't).  Next discriminators: an LBAD/LRTY
  counter probe channel (uart0 ch4 is retaskable — netlist change =
  new lottery), and a sim bench that runs the FULL RX chain
  (gearbox+descrambler; the equiv harness has the machinery).

### W0.1 — wide fabric trim verdicts (tool + silicon; the §3.3
### native-vs-bridge decisions are now CLOSED)

* Tool phase (/tmp/kilo/trim_experiment, vendor serdes_toml_to_csr as
  the encoding oracle): **width_mode > 20 does not exist on the
  GW5AT-60** (KeyError: 32/40/64) — consistent with the fixed 80-bit
  TX / 88-bit RX fabric bus.  `csr_map.py`'s {8..64} set is TOML
  schema, not this device.  **10G 32×1:4 (native 128-bit) is
  IMPOSSIBLE → Gen 2x1 @ 128-bit PIPE = the 2:1 bridge** (the safe
  hybrid); Gen 2x2 → 128 (stripe-merge 2×64) unaffected.
* **5G 20×1:4 (8 symbols @ 62.5) ACCEPTED by the tool**: boot blob
  differs from the proven 20×1:2 trim in exactly TWO lane clock-tree
  divider registers (LN1: `0x808608` 0x111A→0x121A, `0x808628`
  0x116→0x126; stride 8 per lane; gearbox reg stays 0x511) — a
  runtime 125↔62.5 flip is two writes + the #22 quiesce.
* **Silicon (examples/gowin/probe-trims, flashed)**: the wide trim
  BOOTS and the TX PCS runs at **62.500 MHz exactly** (uart0 pclk
  counter 0x14d555e; telltale table in the top).  RX-side symbol
  delivery unverified in the bare rig (no partner stimulus — CDR
  free-ran ~17 MHz, rx activity 0); it rides the W1 integration
  milestone.  **usb3_design.md §3.1/§3.3/§12.1 updated with all
  verdicts.**

### W0.2 — LN0 TX: software-reachable proof EXHAUSTED; folds into W2

examples/gowin/probe-ln0tx (LANE= and LOOPBACK= knobs, A/B-able):
the PIPE `TxDetectRx_loopback` path is the PIPE loopback-SLAVE
semantic (the PHY's wrapper also short-circuits PipeRx* from PipeTx*
digitally); the GTR12 CSR loopback write produced **no observable
TX→RX return at the raw fabric tap on either lane**.  The LN1
"commas" that first looked like loopback return were the HOST's
polling TS1s (control build with LOOPBACK=0 showed identical comma
rates); LN0 (pads unstimulated in the straight orientation) shows a
static RX word and a ~124.7 MHz free-running CDR with or without
loopback.  Re-proven en route: LN0 CSR rate path (boot switch to
pclk 125 at LN0 — #38 re-verified), eidle/FFE handshakes complete.
**The definitive LN0 TX proof is W2's x2 PortConfig (the host
validates lane-1 TX during x2 training) or a physical cable flip.**

### W0.3 — Gen 1x2 negotiation surface + the PortMatch trace:
### PORT 4-3 IS GEN 2X1-HIGHEST (x2 NOT negotiable as benched)

* **Constant corrected**: Table 7-13 (b0..b7 columns) puts dual-lane
  at **b6 → LBPM_CAP_GEN1X2 = 0x40**; the mission text / design doc
  0x20 was b5 = RESERVED (transcription error; doc §5 fixed).
* **ssp_capability plumbing** (lfps.py constants; ltssm.py
  `ssp_capability=` + `phy_boots_gen2=`; physical/link/device
  pass-throughs; device debug_lbpm_* taps): the advertised-highest
  byte is a parameter (GEN2X1 default = elaboration-identical;
  GEN1X2 selects the 5G rate for the matched-highest and the
  0x00-only adjust-down decode).  `phy_boots_gen2=False` resets
  `applied_gen2`/`rate_r` to the 5G state for tops that ride the
  adapter's pre-MAC boot rate switch.  Sim: PHASE=lbpm-x2 +
  DEVCAP=gen1x2 (battery `gen2-lbpm-x2`; red recorded: "device
  announced 0x04, expected ... 0x40").
* **examples/gowin/luna-enum-gen1x2**: the Gen 1x2-highest probe on
  the PROVEN Gen1 build shape — adapter boot_rate_switch (MAC never
  sees 156.25), gen2=True MAC at 125 MHz, uart1 LBPM ring ('D' = rx
  byte | tx<<8, 'A' = tx completions).  SDC: new 8.0 ns branch in
  gowin-serdes dkusb_gw5at60 (`luna_enum_gen1x2`/
  `luna_multiep_gen1x2`) — **MET FIRST ROLL (pclk 126.2/rxclk
  157.9)**, exactly the no-lottery prediction of usb3_design.md §7.
* **Bench capture (the W0.3 answer)**: the host's FIRST capability
  announcement on 4-3 is **0x04 = Gen 2x1-highest, not 0x44**; on
  our 0x40 it adjusted down to 0x00 (per Table 7-14 for a Gen 2x1
  port) → matched Gen 1x1 → PHY Ready both ways → trained →
  enumerated 5000M, rx_lanes=1.  Ring saved:
  /tmp/kilo/gen1x2_lbpm_ring.txt.  Consequences: (a) our x2
  negotiation machinery is silicon-correct against a real host,
  including the adjust-down and the full Gen1x2→Gen1x1 fallback;
  (b) **W2's bench gate (10000M with rx_lanes=2) is NOT achievable
  on 4-3 as benched** — the "usb4 root hub speed 20000 / 2 lanes"
  fact describes the controller, not this port's LBPM announcement.
  Next session: qualify other physical ports with this probe (flash
  + read the ring — it is the x2-port qualifier tool); W2's sim
  program is unaffected.

### Session-14 regression state

* Battery **48/48** mid-session (post-#41; new entry gen2-u0) and
  **49/49** at close-out (with gen2-lbpm-x2), both from settled
  trees; pytest **104/104**.
* Gen1 shipping parity re-proven TWICE (after #41: 10 bytes; after
  the W0.3 params: 12 bytes — all below offset 622).  The gen2 top's
  default-parameter elaboration re-proven payload-identical to the
  flashed image after the W0.3 params (3 header bytes).
* Bench: RESTORED to the Gen1 fence and re-verified (5000M on 4-3;
  1 MiB ×3 PASS 258.8 MB/s agg; 16 MiB PASS 278.2, sha exact).
* Saved images (/tmp/kilo): h2_gen2_lmpfix_met.fs (POR 66_047,
  MET, the post-#41 flash), h0_gen1_fence.fs (RESIDENT).  Probe
  builds live in their example dirs (probe-trims, probe-ln0tx
  build_ln0/build_ln1, luna-enum-gen1x2).
* New battery entries: gen2-u0, gen2-lbpm-x2 (both expect-green,
  red baselines recorded in sim_battery.sh comments).
* Bug numbering: **#41 closed this session; #42 next** (Gen2
  inbound-header path, see W0.4).  #37 + §10n/§10q parked items
  carry.
* Width-program gate status: **W0 CLOSED** (all four probes
  verdicted, design doc updated); W1 next (the w64 core: the 62.5
  native trim is real, the PIPE stays {64,128} with Gen2×128 as a
  bridge); W2's hardware leg needs a port re-qualification first.

## 10u. Session 15 addendum — G5/H2 resumed: bugs #42/#43/#44 found
## and fixed (4+4 credits, RX queue ratchet, TX pacing underflow);
## the host now SENDS at Gen2 (announced Gen 2x1 twice, thousands of
## inbound headers accepted); bug #45 OPEN: a metronomic ~7 us
## U0->Recovery loop introduced alongside the #44 closed loop; the
## bench controller wedged and was un-wedged; Gen 1x2 DROPPED from
## scope (bench owner's call)

The bench owner redirected this session from the width program back
to the G5 dual-rate mission (the session-13 prompt).  Bugs #42, #43,
#44 fell; the Gen2 enumeration gate is CLOSE but not closed: the host
now negotiates Gen 2x1, trains, port-configures, and on good boots
ANNOUNCES the device and issues descriptor reads -- the remaining
blocker is #45 (below).  Everything is committed and the tree is
settled (battery 52/52; shipping parity payload-identical, twice).

### The session in one table

| # | finding | state |
|---|---------|-------|
| #42 | Gen2 credit advertisement was 2+2; **[7.2.4.1.1 rule 2.e.1] mandates 4 Type-1 + 4 Type-2 from Polling/Hot Reset** -- the host's Type 1/2 CREDIT_HP_TIMERs (clear only at count 4) expired -> Recovery loop -> port config error; the host never sent one header packet (the G4 sim host had CODIFIED the 2+2, the #41 shared-wrong-assumption class again) | **FIXED + silicon-verified** (host header packets now flow; 8 Rx header buffers behind 4+4 pools at gen2_active, 4+0 at SS; Gen1 verbatim) |
| #43 | RX beat-queue RATCHET: idle beats enqueued unless the engine was FULLY drained, load-point discard capped at 1 beat/cycle == the arrival rate -> every construct added ~5-8 beats of PERMANENT backlog (sim: 649 beats / 4.2 us lag, monotone, toward silent overflow) | **FIXED sim-proven** (idle RUN COMPRESSION at enqueue -- one counted entry per run via a provably-1-deep skid; SEARCH discards whole runs in one cycle; mid-construct replay covers all-5Ah DPP payloads; RUN_MAX cap bounds corrupt-wire stalls) |
| #44 | TX pacing UNDERFLOW: the session-13 open-loop 1-gap-per-16-blocks matched the wire rate EXACTLY, so the PHY TX FIFO idled at the stream-start race level (0..2) and TxGearbox132 rode its underflow boundary -- stale bits on the wire whenever supply/drain phases misaligned (silicon: ZERO inbound CRC errors while the host yanked recovery ~5x/s; descriptor reads died EPROTO -71).  The vendor MAC runs this FIFO NEAR-FULL against TxFifoWrNum (netlist: it gates TX on wrnum[4], threshold 16 -- occupancy semantics confirmed in the vendor .vg) | **FIX LANDED** (closed loop on TxFifoWrNum, threshold 16, prefill-then-hover; PIPE backends expose `tx_fifo_occupancy`; sims model the loop and FAIL on prefill-miss or post-prefill starvation) -- but see #45 |
| #45 | **OPEN, the H2 blocker**: with the closed loop in, EVERY boot's Gen2 window runs a METRONOMIC ~7.05 us U0->Recovery loop: 49.6k OUR-recovery strobes per 0.35 s probe window (sds == recovery exactly, ts1 storms), rx_hdr_bad=0, accepted headers=0, at the solid 10G trim, for 25+ s.  A/B on the CLEAN port (4 boots each): pre-#44 build = old signature (announced-then--71 / fallback / walk-down, headers flowing); closed-loop build = the loop on every Gen2 window | root-cause candidates + per-cause probe below |

### #45: what is known and the candidate mechanisms

Known hard facts: deterministic ~1100-cycle period; all recoveries are
OURS (debug_recovery = timers|rx|tx strobes -- NOT the ts1-triggered
LTSSM exit); zero accepted headers, zero CRC-bad headers; training,
SDS, and the TS handshakes complete ~142,000 times per second; the 5G
fallback of the SAME image enumerates and holds U0 indefinitely
(ITPs flowing, checkers clean).  Sim coverage added this session
(hotreset, plain-recovery-with-preserved-sequences, strict 4+4, the
closed-loop FIFO model) is ALL GREEN -- the loop does not reproduce
against the idealized feed.

Candidates, in current order:

1. **bad_sequence (receiver seq mismatch on a CRC-VALID header)** --
   the only recovery cause invisible to BOTH probe counters
   (accepted-headers counts post-accept, rx_hdr_bad counts CRC fails).
   A systematic mismatch is self-sustaining: sequence numbers are
   PRESERVED across plain Recovery, so the host retransmits the same
   seq and the loop is a metronome.  What #44 changed to CAUSE it is
   the open question (the wire CONTENT is FIFO-order-preserved and
   should be bit-identical to open-loop minus the underflow bursts).
2. **The `active`-blip state wipe against the standing 16-beat
   queue**: `active` (registered OR of the LTSSM burst requests)
   may blip low for one cycle at request seams; the transmitter's
   inactive arm WIPES beat_idx/mode/skp_gap/sds_pending.  Pre-#44 the
   FIFO was empty so a wipe cost a truncated block at worst; NOW ~16
   beats are queued and a mid-block wipe desynchronizes tx_start
   against the queued stream -> the PHY gearbox emits a malformed
   block -> the HOST's RX desyncs -- but the recoveries are OURS, so
   this only fits as a second-order effect (host responses then
   mismatch our expectations).  Check the wipe-arm gating first; it
   is cheap to make the inactive arm drain-safe (finish the block).
3. Something in the tx_fifo_level plumbing (layer m.d.ss + adapter
   comb + RdDataNum register = ~2-3 cycles of lag) oscillating in a
   way the python model (1-cycle lag) does not -- would show as
   overflow/underflow though, and txfifo_hi28 stayed 0.

The decisive instrument is built and committed: the per-cause
recovery split (device.debug_recovery_timers/_rx/_tx; uart0 ch1..3 in
the current luna-enum-gen2 top).  **Its lottery is unfinished**: 4
rolls (66_125-66_128 seeds) all missed pclk (138-144).  Next session:
keep rolling (the winners this session took 3-12 rolls), flash, read
which cause counts 142k/s, then chase that specific mechanism.  A sim
lead worth trying before the bench: model the LTSSM request-seam blips
(drive send_ts2/idle_mode with 1-cycle gaps) against the closed-loop
transmitter and watch for tx_start desync; and drive the host's
re-advertisement CONCURRENT with (not after) the device's own U0
entry -- on silicon the host reaches U0 first and its advertisement
may land while our link enable is still low (the LC detector sits in
ResetInserter(~enable) and eats it).

### Architectural decisions from the bench owner (BINDING)

1. **If the 64-bit stage-A core stops closing 156.25, the 10G
   configurations move to the width-program 128-bit core** (pclk
   78.125; Gen 2x1 via the W0 2:1-bridge trim).  This session burned
   ~30 lottery rolls across four netlist revisions (winners at
   66_101, 66_125; the evcap and per-cause netlists needed 13+ and
   4+ rolls without a winner) -- the pressure is real.
2. **Gen 1x2 is DROPPED from scope entirely** (neither the bench
   xHCI (80:14.0) nor TB4 hosts support x2 lanes; Gen 1x2 is mostly
   unsupported in the wild).  The width program is therefore:
   **Gen 1x1 = 64-bit and 128-bit cores; Gen 2x1 = 128-bit core
   only; no x2 anywhere in LUNA or the PHY.**  The session-15 width
   prompt's W1-W3 gates and the G5/H4 matrix should be re-read with
   x2 struck out; the gen1x2 example top and the ssp_capability x2
   surface stay in the tree as negotiation-matrix artifacts only.

### Bench events and new tooling (trust but verify)

* **The xHCI controller WEDGED** after the session's hundreds of
  failed-attempt penalty cycles (+ sysfs `disable` pokes): endless
  "not warm reset yet / Cannot enable" against a port reporting
  Not-connected, WITH THE CABLE UNPLUGGED (the bench owner spotted
  it).  Fix: PCI unbind/rebind of `0000:80:14.0` (`echo ... >
  /sys/bus/pci/drivers/xhci_hcd/unbind` then `bind`) -- buses
  re-enumerate, port returns to clean RxDetect.  COROLLARY: any
  verdict taken while wedged is suspect; the vendor prj.fs
  (10000M first-try) is the port-health oracle -- run it after any
  wedge before trusting new data.
* **tty numbers are volatile**: the controller reset renumbered the
  FTDI quad twice; two capture windows silently read stale
  /dev/ttyUSB4/5 nodes.  `uart_capture.py` now opens
  `/dev/serial/by-id/usb-FTDI_Quad_RS232-HS-if02/if03-port0`
  (uart0/uart1).  The bench owner removed the unrelated USB serial
  dongles.
* **PORTSC tracer**: `/tmp/kilo/portsc_trace.py` polls the xHCI
  debugfs port at ~1 ms and logs transitions -- bus 4 port 3 is
  **hw port19** on `0000:80:14.0` (the debugfs portNN namespace
  spans both buses: usb3 = 14 USB2 ports first).  This is how the
  Hot Reset death and the U0<->Recovery flapping were seen from the
  host side.  Hub-level dynamic debug: `echo 'file hub.c +p' >
  /sys/kernel/debug/dynamic_debug/control` (module-wide usbcore +p
  floods dmesg with runtime-PM noise).
* Boot-outcome A/B harness: `/tmp/kilo/boot_ab.sh <fs> <tag>` --
  flash, 16 s watch, classify (GEN2-ANNOUNCED-THEN-EPROTO71 /
  FELLBACK-5000M / CONFIG-ERROR / OTHER) + a by-id uart capture.

### Timing/SDC finding (gowin-serdes commit `7accabd`)

rxclk at the 10G trim is the RECOVERED clock: **10.3125 GHz / 64 =
161.133 MHz**, not 156.25.  The shared 6.4 ns SDC under-constrained
every rx-domain path by 3%; one formally-MET build (rxclk Fmax
159.6 < the real clock) showed on-wire corruption.  The Gen2 tops now
constrain rxclk at 6.2 ns; **the honest Gen2 gate is pclk >= 156.25
AND rxclk >= 161.29 operating**.  Gen1 tops keep 6.4 ns (their
recovered clock is 125).

### Sim/battery growth (49 -> 52 entries, all green from the settled tree)

* `sim/rx_hp_offsets.py` (battery `gen2-rx-offsets`): Gen2BlockReceiver
  placement sweep -- HPs/DPHs/LCs at every symbol offset [7.2.1.3],
  back-to-back constructs, rx_valid gaps at several cadences.  All
  green (the engine was NOT #42).
* `sim/rx_chain_full.py` (battery `gen2-rxchain`): the FULL PHY RX
  chain -- wire-serialized scrambled blocks at true async clocks
  (161.133 vs 156.25) through the real RxGearbox132 -> CDC AsyncFifo
  -> Descrambler -> Gen2BlockReceiver; byte-exact translation incl.
  all-5Ah DPPs and 100 SKP LFSR reseeds; asserts the #43 queue bound
  (level returns to zero; the pre-fix stack pinned at ~650).  Also
  documents the vendor gearbox free-running garbage when
  i_data_valid drops (bench-feed artifact; keep the wire streaming).
* `PHASE=hotreset` (battery `gen2-hotreset`): the xHCI port-reset flow
  at Gen2 (Recovery entry from U0, TS2-with-Reset handshake [7.5.12],
  SDS in Hot Reset.Exit, LGOOD_15 + 4+4 re-init, address reset,
  descriptor read).  GREEN from first run -- the handshake logic is
  sound against an idealized feed; PORTSC showed one silicon boot
  dying exactly there (pre-#44 build, U0@PortSpeed:5 held 108 ms ->
  Hot Reset 13 ms -> RxDetect/Not-connected).
* `PHASE=recovery` (not yet a battery entry -- ADD IT): plain
  mid-traffic Recovery x3 with PRESERVED sequence numbers (the
  re-advertisement carries LGOOD_1/3/5) and full 4+4 rule-2d
  re-advertisement.  GREEN.
* enum/u0 host is now STRICT about the full 4+4 alphabetical
  advertisement and sends NO header packet until it completes (the
  red reproduced the #42 silicon signature exactly).
* The HostRx PHY TX FIFO model closes the #44 pacing loop
  (drives `pipe.tx_fifo_occupancy`) and FAILS on prefill-miss or
  post-prefill starvation; `tests/test_gen2_pacing.py` reworked the
  same way (3/3).

### Hardware verdicts recorded this session

* **H0 Gen1 fence re-verified on the resident image** before any
  flash: 5000M enumeration on 4-3, 1 MiB x10 (248.9-263.0 MB/s agg),
  16 MiB x3 (275.8-277.6), 64 MiB x3 (274.3-278.1), all sha-exact;
  uart1 ch0 all-zero flags=8 (retry_flagged=0); link probe 125 MHz
  flags d.  The fence image is `/tmp/kilo/h0_gen1_fence.fs`.
* **#42 kill confirmed on silicon**: post-fix, the host negotiates
  Gen 2x1, trains, and SENDS -- thousands of inbound host headers
  accepted per probe window (ITPs + LMPs), against ZERO before.
* Best Gen2 boots (pre-#44 build, clean port): "new SuperSpeed Plus
  Gen 2x1 USB device" announced, descriptor read/8 EPROTO -71 (the
  #44 underflow class killing our DP reply).
* The closed-loop (#44) build's Gen1 FALLBACK enumerates and holds
  5000M U0 indefinitely (ITPs flowing, probes clean) -- the dual-rate
  image's per-spec fallback mechanism (H4 run-2 shape) works with all
  four fixes in.
* Vendor prj.fs: 10000M first-try after the controller un-wedge
  (port-health oracle).

### Builds and the lottery lay of the land

| netlist | winner | notes |
|---------|--------|-------|
| #42+#43 + evcap ring (uart1) | NONE in 13 rolls (105-147.6 pclk) | the 64x35 ring + 8 buffers = uniform congestion |
| lean pipeprobe loadout | **66_101** = 156.274/164.001 (SDC-fixed) | flashed; the #42-kill + EPROTO71 evidence build; saved `/tmp/kilo/s15_gen2_probe_66101_met.fs` (per-cause A/B baseline) |
| + #44 closed loop | **66_125** = 156.263/161.580 | flashed; the #45 loop evidence build; saved `/tmp/kilo/s15_gen2_cl_66125_met.fs` |
| + per-cause recovery split | NONE yet (4 rolls, 138-144.6) | **next session: keep rolling** |

Shipping parity re-proven twice (payload-identical vs
`/tmp/kilo/h0_gen1_fence.fs`, diffs only in the 603-621 header date
region).

### Commits (fork `948a33b..678fa97`, gowin-serdes `7accabd`)

`092daaa` #42 (4+4 credits) / `cc57db7` #43 (idle run compression +
the two RX benches) / `54d68d3` strict-4+4 sims + hotreset phase +
battery / `dff039b` lean probe top + honest rxclk gate + POR 66_101 +
gowin-serdes bump / `6baa795` #44 (closed-loop pacing) /
`678fa97` by-id uarts + per-cause probe loadout.  NOT yet committed:
the `PHASE=recovery` sim (add a battery entry with it), this
HANDOVER section, POR 66_125-era top comment already in `6baa795`.
Push everything after the #45 verdict or at session end regardless.

### Next session start (H2 remains the gate)

1. Roll the per-cause netlist to MET (gate: pclk >= 156.25, rxclk >=
   161.29), flash, read uart0 ch1..3 at the loop: timers/rx/tx.
2. Chase the named cause (candidates above; check the `active`-blip
   wipe arm and the concurrent-advertisement window in sim first --
   both are cheap).
3. Gate: `lsusb` 10000M on 4-3, dmesg clean.  Then H3 (Gen2 ladder,
   wire checker port) and the RE-SCOPED H4 (no x2): Gen2 image on the
   5G hub port, replug/POR x5, forced-Gen1 re-ladder.
4. Carry-over: #37, rule-2d/#36 stimuli, bench forced-recovery verdict
   (#29-#31), SEND_ZLP bare-ready, wire-checker TP blindness, SKP x=4
   aligner, stage-B width program (now WITHOUT x2), 4+4 pools' 8 RX
   header buffers -- DONE this session as #42.

## 10v. Session 16 — the WIDTH PROGRAM, single lane (V0–V4 per
## prompt.md): V0 executed (bench un-wedged, oracle 10000M, Gen1 fence
## re-verified GREEN; design note usb3_design.md §13 landed)

### V0 — orientation + the fence (2026-09-04)

* **Bench arrived WEDGED** (the §10u signature: endless
  "not warm reset yet"/warm-reset loop on usb4-port3, live in dmesg).
  One PCI unbind/rebind of `0000:80:14.0` did NOT clear it alone —
  the resident image was the #45 closed-loop evidence build, whose
  metronomic retrain looks to the host like a port that never
  enables.  Vendor `prj.fs` flashed as the port-health oracle:
  **10000M first-try on 4-3** — port + cable healthy.
* **Gen1 fence re-verified** (`/tmp/kilo/h0_gen1_fence.fs` flashed):
  enumeration **5000M** on 4-3; 1 MiB ×10 = 254.7–264.9 MB/s agg,
  16 MiB ×3 = 277.4–282.8, 64 MiB ×3 = 281.7–282.2, ALL sha-exact,
  10+3+3 PASS; uart1 ch0 all-zero flags=8, zero 'R' strobes
  (capture `/tmp/kilo/v0_fence_both.txt`).  NOTE: the stale
  `/tmp/kilo/uart_capture.py` still opens ttyUSB4/5 and caught only
  one UART — use the repo's by-id
  `examples/gowin/luna-multiep/uart_capture.py` from now on.
* **Design note landed FIRST (code second): `doc/usb3_design.md` §13**
  — the single-lane width matrix with per-config timing gates;
  `core_width` naming pinned (§13.1: PIPE/block width; LUNA streams =
  core_width/2; 64 = today verbatim); the 2:1 bridge design (§13.3:
  core = pclk/2 by fabric divider at BOTH rates — fallback keeps the
  proven 20×1:2 trim and the proven 1.25 timer stretch;
  `tx_halfbeat` SKP contract; **#44 pacing decision stays CORE-side**,
  bridged-lag sims red-first); the full domain-crossing inventory
  (§13.4 — synchronous 2:1 seams, the only true async crossing stays
  the PHY-internal rxclk AsyncFifo); the V1 work list (§13.5) and
  verification deltas (§13.6).  §1 header carries the BINDING
  x2-dropped scope update.

### Bug #46 (FIXED, commit 4e60bcd): the Gen2 TX request-seam hazards
### — and the #45 metronome's mechanism

The two cheap #45 sim leads of §10u were executed red-first
(`tests/test_gen2_tx_seams.py`, new battery entry gen2-tx-seams):

* **The U0-entry blip**: link/layer.py mixed a COMB
  perform_idle_handshake decode with the 1-cycle-late registered
  link_ready — gen2_idle_mode dropped for EXACTLY one cycle at EVERY
  U0 entry (Polling.Idle and Recovery.Idle alike).  The scheduler's
  inactive arm then wiped beat_idx MID-BLOCK (odd alignments): a
  start beat with no continuation — a TRUNCATED 132-bit block on the
  PIPE, desynchronizing the host's receiver against the standing #44
  FIFO.  Even alignments exposed the SDS arm/wipe write-order race
  (cold entry emitted NO SDS at all).
* **The stale bridge flush**: the TX bridge carried packets across
  retrains; an LC cut mid-command by the reset discipline was later
  flushed idle-padded onto the FRESH link ahead of the advertisement
  — and [SLC SLC SLC EPF][5A×4] aliases a REPLICA-VALID link command
  (0x5A5A both halves).

Fixes: gapless seam (perform_idle_r registered like the burst
requests), DRAIN-SAFE emission gate (an open block always completes;
true stops quiesce at the boundary), LEVEL-based SDS arming (armed at
reset + by training-class blocks, consumed by SDS), and the bridge
held in reset while any training-class burst runs.  All gen2-only
elaborations; shipping parity re-proven; full gen2 sim section green.

### Hardening #47 (commit 4e46281): early LC capture window — sim
### lead (b) EXECUTED AND EXCLUDED

`PHASE=advearly` (new battery entry): the host advertises at its
physically earliest legal instant (gated on observing the device's
own idle stream), swept at block/half-block offsets over recovery
re-entries.  **Verdict: under causally-legal timing the historical
RTL was NOT red** — the RX pipeline delays the advertisement past
link_ready; candidate (b) cannot produce #45 from a conformant
partner.  The truly-early stimulus red (credit-starved link: trains,
receives, LGOODs/LUPs out, never one header TP) motivated the
hardening: `transmitter.listen` opens the lc_detector from the
idle-handshake states (bug-#36 protection preserved — listen drops
with training states), the state clear holds only while the window is
closed, and `ltssm.in_recovery_idle` + an idle-phase latch keep the
rule-7 disposition valid for early-captured advertisements.

### BUG #45 RESOLVED on the bench (2026-09-04): root cause = #46

The post-#46/#47 per-cause netlist (the §10u "decisive instrument")
MET ON THE FIRST ROLL from POR 66_125: pclk 156.340 / rxclk 180.039
(`/tmp/kilo/s16_gen2_46_47_percause_met.fs`).  Flashed twice with
by-id uart + PORTSC + usbmon instrumentation:

* **The metronome is GONE**: uart0 rec-timers/rec-rx/rec-tx = 0 and
  uart1 recovery = 0 across the active windows (the counters built to
  discriminate #45 read zero); ss-cnt telltale 0x341556x = 156.25 (10G
  held); trained reaches 1 with terminations engaged (flags d).
  Capture `/tmp/kilo/s16_gen2_cause_both.txt` (t≈11.2–12.3 s).
* **PORTSC now reaches 0203 (U0) at 10.0 Gb/s** and the host attempts
  transfers: `new SuperSpeed Plus Gen 2x1 USB device number NN` —
  where every pre-#46 Gen2 window died in the 7.05 µs U0→Recovery
  loop.  #45 is closed: the metronome's mechanism was #46's seam
  hazards (the truncation/stale-flush artifacts at every U0
  (re-)entry, wire-visible only against the real host's timing — the
  idealized sim feed waited for the device and never saw them).

### BUG #48 (ROOT CAUSE FOUND + FIXED, commit 1698d05; bench verdict
### pending a MET roll): the non-deferred Gen2 DPH is 24 BYTES — the
### length replica appears TWICE (Figure 7-4)

The gate one layer up: `device descriptor read/8, error -71` on EVERY
attempt at stable 10G U0 (usbmon `s 80 06 0100 0000 0008` → `C -71 0`,
completions ~100 µs / ~7 ms; ×4 per address, two addresses, then port
power-cycle; `/tmp/kilo/s16_usbmon_48.log`).  Localization: SET_ADDRESS
works (device number assigned), TPs flow both ways, host DPs are
received — the ONLY failing element is the device-TRANSMITTED DP.

**Root cause** (spec archaeology, Figure 7-4 read as an image from
`doc/USB 3.2 Revision 1.1.pdf/pages/page-147/img-64.jpeg`): the
non-deferred Gen2 DPH is **24 bytes** — framing + 12B header + CRC-16
+ LCW + **Length Field Replica ×2** ("the two length field replica are
valid and identical" [7.2.4.1.6]).  We implemented ONE replica (22-byte
DPH) from the prose of 7.2.1.1; the real xHC parsed our DPPSTART
framing as the second replica → mismatch → DP rejected → EPROTO.
Sim-green historically because the bench host embodied the SAME
misreading — the strict-host upgrade (host sends AND validates both
replicas + the [7.2.1.2.3] no-spacing rule) reproduced the silicon
failure byte-exact: `DPH length replicas 18/38550 != length 18`
(0x9696 = our SDP SDP framing).  RED recorded, RTL fixed both
directions (TX bridge REPLICA ×2 — the DPP framing now re-aligns to
the word phase; RX engine swallows 4), full gen2 sim section green.
Inbound host DPHs (always 24B on silicon) had worked by luck: the RX
engine's SEARCH state stepped past the 2 unswallowed replica bytes.

Parked from this fix: RX-side replica-match validation
([7.2.4.1.6 rule 2a → Recovery]).

**Timing lottery on the fix netlist** (the mission's point made
flesh): rolls 66_126..66_133 ALL missed pclk (141.7–154.6; the
pre-fix sibling netlist MET on its first roll at 156.340) — batch 2
(66_134..) running.  A MET roll flashes for the 10000M verdict; if
the batch fails, the verdict waits for V2/V3's 128-bit core, per the
mission's no-lottery-budget rule.

### Width program state (V1)

* V1a: `USBSuperSpeedDevice(core_width=64|128)` elaboration point
  landed (64 = verbatim, parity-proven; 128 raises until §13.5 units
  land).
* V1b start: wide CRC surfaces by COMPOSITION (commit 582eb2b):
  HeaderPacketCRC(words=2) two-word advance; DataPacketPayloadCRC
  (words=2) 8B advance + 4..7B tails + next_crc outputs;
  `tests/test_usb3_crc_wide.py` pins them byte-exact against the
  proven sim references.  words=1 verbatim.
* Next in V1: 64-bit Scrambler/Descrambler/CTC/aligner
  parameterization, the stream-width threading, the framers, the
  gen2.py 128 twin, the 2:1 bridge (+ its red-first pacing-lag sims).

### Bench notes (2026-09-04)

* The wedge appeared twice; one PCI unbind/rebind + vendor-oracle
  flash (10000M first-try) cleared it — the oracle remains the
  port-health arbiter.  The fence was re-proven green start AND end
  of the bench day (end: 16 MiB ×3 = 278.0 MB/s PASS).
* The stale `/tmp/kilo/uart_capture.py` reads only one UART (ttyUSB
  numbering rot) — use the repo's by-id
  `examples/gowin/luna-multiep/uart_capture.py` (tag L = uart0/if02,
  tag C = uart1/if03).

### Carry-over state

* Bug numbering: **#45 RESOLVED (root cause #46); #48 OPEN and first
  among bugs (the V3 Gen2 gate); #49 next.**
* Parked items unchanged from §10u (#37, rule-2d/#36 stimuli,
  #29–#31 bench forced-recovery verdict via the uart1 'R' hook during
  V3's ladder, SEND_ZLP bare-ready, wire-checker TP blindness, SKP
  x=4 aligner knob, SSP BOS device capability + Sublink Speed Device
  Notification TP during V3 if dmesg complains, stage-B credit
  scaling beyond 4+4).  #37 is now a live #48 candidate.

## 10w. Session 17 — bug #49's device-side mechanisms FOUND & FIXED
## in sim (bugs #50 + #51, red-first via the new PHASE=reccut cut
## sweep); SSP BOS capability landed; V1 CTC/aligners widened

### V0' — the fence (2026-09-04, session start)

* Bench arrived WEDGED again (the warm-reset loop on usb4-port3, live
  in dmesg; resident image = the session-16 #49-wedged build).  The
  runbook held: PCI unbind/rebind of `0000:80:14.0` alone did not
  clear it; JTAG channel unbound from ftdi_sio (`3-7.3.2:1.0` — the
  quad FTDI now enumerates at `3-6.4`, the FT232H JTAG at `3-7.3.2`);
  vendor `prj.fs` = **10000M first-try on 4-3** (port + cable
  healthy); then the fence.
* **Gen1 fence GREEN**: `h0_gen1_fence.fs` → 5000M on 4-3;
  1 MiB ×10 = 252.4–267.4 MB/s agg, 16 MiB ×3 = 277.1–284.1,
  64 MiB ×3 = 282.0–283.5, all sha-exact PASS; uart1 ch0 all-zero,
  flags=8 (capture `/tmp/kilo/s17_v0_fence_both.txt`).

### V1 — CTC + aligners width-parametric (usb3_design.md §13.5 next
### unit after the landed CRC/scrambler pattern)

* `physical/ctc.py`: `CTCSkipRemover(words=)` (the coalescing shift
  register at 2× width; the output-slice constant generalized to
  `buffer_size_bytes - i` — verbatim `8 - i` at words=1),
  `CTCSkipInserter(words=)` (words=2 emits FOUR SKP ordered sets per
  8-symbol beat once four are owed; saturation bound re-derived: 7),
  `TxStreamSkidBuffer(words=)` (Signal.like internals, streams only).
* `physical/alignment.py`: `RxWordAligner(words=)` /
  `RxPacketAligner` — eight byte offsets at words=2, 4-symbol
  criteria windows unchanged.
* Fences: `tests/test_usb3_ctc_wide.py` (remover byte-exact vs narrow
  vs software-stripped reference with SKP runs straddling beats;
  inserter stream-preservation + Y/354 schedule with carried
  remainder at both widths; word/packet aligner lock at all 8 offsets
  + post-lock byte-exact equality vs narrow).  Mutation-checked red
  (wide remover slice, wide aligner slice count), restored green.
  words=1 = verbatim; **shipping parity proven after the change (14
  diff bytes, all in 603–621 = the header date region)**.

### The SSP BOS device capability (the REQUIRED enum-surface gap)

* `luna/gateware/usb/usb3/descriptors.py` (new):
  `ssp_device_capability()` builds the SuperSpeedPlus USB Device
  Capability [9.6.2.5, Table 9-27] as raw bytes (usb_protocol 0.9.x
  has no emitter): bLength 0x1C, SSAC=3/SSIC=1 (bmAttributes 0x23),
  wFunctionalitySupport 0x1100 (SSID 0 full-function, 1+1 lanes),
  RX/TX attribute pairs per SSID — SSID0 5 Gb/s SS, SSID1 10 Gb/s SSP
  (LSE=3, LSM=5/10; field conventions cross-checked against the
  bench's 10G hub at 4-6 via sysfs `bos_descriptors`).
  `add_superspeedplus_bos()` composes USB2ext + SS cap + SSP cap
  (wTotalLength 50, 3 caps).
* RED-FIRST: the sim's enum ladder gained a BOS-walk validation
  (type-0x0A capability with a 10 Gb/s LP=SSP attribute REQUIRED at
  bcdUSB 0310); red recorded against the old surface, then the
  capability added to BOTH `sim_link_gen2.py` and the
  `luna-enum-gen2` top → green (full BOS now 50 bytes, read
  end-to-end by the PHASE=enum ladder).

### The #49 instruments and the two bugs they caught

**Lead (a) — the honest-drain FIFO model.**  `HostRx`'s PHY TX FIFO
model now drains through the REAL TxGearbox132 law (68-bit
start-block beats, one dead read cycle per 16 blocks via the residue,
registered-empty read enable, underflow-from-empty) instead of the
flat 32-per-33 approximation, and counts `fifo_hi28` — the exact
bench canary (level ≥ 28).  Verdicts: enum max 16/32, hi28 0;
recovery (3 retrain crossings) max 16, hi28 0; reccut (7
mid-transfer cuts) max 16, hi28 0.  **Steady-state supply/drain and
retrain crossings are EXCLUDED as the overshoot source in lockstep
timing** — the silicon hi28 evidence (71k/s ÷ 5.5k retrains/s ≈ 13
cycles per retrain) now points at the retrain-entry window with
host-overlapped traffic, which the reccut sweep models only at
block granularity.  Enum/reccut/recovery now FAIL on any hi28.

**Lead (b) — PHASE=reccut (new battery entry): a control transfer cut
by Recovery mid-data-stage, swept at offsets 0,1,2,3,4,8,24 idle
blocks after the host's IN ACK TP.**  The harness is spec-honest:
it accepts a legal under-advertisement (a header yanked out of the
RX pipeline is legitimately un-received) and RETRANSMITS past the
device's advertisement with original sequence numbers, exactly like
the real xHC.  Two REAL bugs, both red-first:

* **Bug #50 (FIXED, link/receiver.py): the link-down
  advertisement/credit race.**  The packet-acceptance block is not
  gated by ``enable``; a header whose parse completes in the FIRST
  link-down cycle (its ``new_packet`` strobe registered at the last
  enabled edge) is properly accepted, buffered, delivered (rule 2d) —
  and ``expected_sequence_number`` advances — but the one-shot
  link-down preparation ran in the SAME cycle and read the
  PRE-acceptance value: the re-advertisement under-reports by one
  [violates 7.2.4.1.1 rule 2.e.2], the partner retransmits a header
  the device already counted, and the device calls it a bad sequence
  → **device-initiated recovery loop + wedged EP0** (reccut offset-2
  red: advertisement LGOOD_8 with seq-9 accepted and its DP queued;
  the retransmitted seq-9 ACK TP then fired ``rec_rx``).  The same
  race under-corrected the per-class rule-2d credit recomputation
  (a same-cycle-accepted header's buffer advertised as free →
  partner oversubscribes the pool).  Fix: the prep accounts for the
  same-cycle acceptance (``reserve_buffer``/``reserve2`` are exactly
  the acceptance strobes).  Gen2 elaborations only; the Gen1 rail
  keeps both historical statements verbatim (the fence) — **the Gen1
  twin fix is a new parked item**.
* **Bug #51 (FIXED, link/transmitter.py): the consumed-payload
  bookkeeping windows.**  The link-drop handler marked a DP's payload
  as consumed only while ``payload_pending`` (first-to-last word) was
  high; a drop after the LAST payload word but before ``done``
  (payload fully consumed, DPP CRC/END framing still going onto the
  wire) — or in the first-capture cycle — left the header marked
  never-sent, and its DL=1 retransmission attached a PHANTOM payload
  from the (empty or next-transfer) data stream instead of aborting
  the DPP: **a garbage DPP with a valid-looking DPH on the wire**
  (reccut offset-24 red: retransmitted descriptor DPP =
  ``69 69 69 36`` + idle fill, CRC-32 invalid — the BOS/22 EPROTO
  wire shape).  Fix: ``RawPacketTransmitter(gen2=True)`` tracks
  ``payload_consumed`` (combinationally exact from the first consumed
  word until the next ``starting``); the drop handler marks
  ``sent_flags`` from it and keeps ``drain_required`` on the
  historical ``payload_pending`` qualifier.  Gen1 rail verbatim
  behind the elaboration gate.

Post-fix, the FULL sweep is green: honest advertisements, host
rule-7 retransmission accepted, device DP retransmission byte-exact
with original numbering, the consumed-payload cut correctly ABORTS
its DPP (EDB) and **EP0 re-serves the data stage on the host's
protocol retry** (the #37 TX-side surface verified working); every
STATUS stage completes; EP0 alive across all seven cuts; pacing band
held.  The host parser learned the DPPABORT dialect (a 4th ``dpp``
event element).

**Why this is the #49 shape**: both bugs fire exactly when a
host-initiated retrain lands inside a control transfer — certain at
the bench's ~5.5k retrains/s — and both wedge EP0 persistently
(#50: every later host header reads stale → silently dropped or
bad-sequence-looped; #51: the endpoint's data source desyncs).  The
host-observed symptom is the ~7 ms transfer timeout → EPROTO -71,
transfers dying at an arbitrary ladder step (BOS/22 on the bench),
and a wedge that survives hot reset ON THE HOST SIDE (the device
clears — sim lead (c) below — but the xHC has already torn the port
down).  Bench confirmation still required (see next steps).

**Lead (c) — PHASE=hotreset-parked (new battery entry)**: the full
xHCI port-reset flow with a control IN PARKED mid-data-stage (SETUP
acked, IN token sent, device DPH un-acknowledged, credit held, no
STATUS).  GREEN first run: LGOOD_15 + 4+4, address reset, clean
descriptor read — **the device-side reset path fully clears parked
protocol state**; the bench wedge's hot-reset survival is not a
device-side reset leak (consistent with #50/#51 being the mechanism:
the DEVICE recovers, the HOST's view is already poisoned).

### Carry-over state (supersedes the §10v list)

* Bug numbering: **#48 RESOLVED on the wire (session 16); #49 OPEN —
  its two device-side mechanisms (#50 advertisement race, #51
  consumed-payload window) are FIXED and sim-fenced; the bench
  verdict (clean repeatable 10000M enumeration) is the remaining
  gate.  Next bug number: #52.**
* NEW parked items: the Gen1-rail twins of #50 and #51 (the same
  races exist in the non-gen2 elaborations; verbatim-preserved for
  the fence — take them through the explicit
  intend/battery/hardware-ladder ceremony); the reccut sweep at
  sub-block cut granularity (the sim cuts at block boundaries; the
  silicon host yanks mid-symbol).
* Parked items carried: #37 RX side (truncated INBOUND DPP never
  retried — the TX side is now verified working by reccut),
  rule-2d/#36 stimuli, #29–#31 bench forced-recovery verdict, RX-side
  DPH replica-match validation [7.2.4.1.6 rule 2a], SEND_ZLP
  bare-ready, wire-checker TP blindness, SKP x=4 aligner knob,
  Sublink Speed Device Notification TP (if the host asks — the SSP
  BOS capability itself LANDED this session), stage-B credit scaling.
* Width program V1: CRC/scrambler (landed §10v) + CTC/aligners
  (landed §10w).  Next per §13.5: stream-width threading + framers,
  `physical/gen2.py` at 128 (re-prove the #43 queue bound red-first),
  the 2:1 PIPE bridge (+ pacing-lag sims), gowin-serdes 20×1:4 trim +
  w128 SDC branches.

## 11. Reading list for the new session (fork edition)

* `prompt.md` — the active mission (session 15: the width-generic
  core — Gen 1x1 / Gen 1x2 / Gen 2x1 at core_width 64 and 128,
  gates W1–W3).
* `doc/usb3_design.md` — THE design authority (merged gen2 + gen1x2
  notes + the program decision; §3.1/§3.3/§12 now carry the
  session-14 P0 verdicts).  `doc/gen2_design.md` and
  `doc/gen1x2_design.md` are superseded — historical only.
* `HANDOVER.md` §10t (this file) — session 14: gate W0 closed, bug
  #41 (SSP LMP field rules) fixed + wire-verified, the post-#41 Gen2
  silicon state (#42 = inbound Gen2 header path), the trim verdicts,
  the LN0 disposition, and the port-4-3 = Gen 2x1-highest finding.
  §10s has the session-13 silicon lessons (#39/#40, evcap, POR
  lottery history); §10r the G3/G4 sim architecture; §10o the fork
  map and bench history.
* `luna/gateware/usb/usb3/physical/gen2.py` — the stage-A Gen2 block
  machinery (module docstring = the architecture; the v2 RX grammar
  engine shape is the model for the wide-core barrel front-ends).
* `luna/gateware/usb/usb3/link/ltssm.py` — `ssp_capability=` /
  `phy_boots_gen2=` (session 14) and the gen2 PortMatch/PortConfig
  arms the W2 x2 work extends.
* `luna/gateware/usb/usb3/protocol/link_management.py` — bug #41's
  SSP field rules (`ssp_operating`; Gen 1x2 ORs in at W2).
* `sim/sim_link_gen2.py` header — every Gen2 phase and knob
  (PHASE=scd|lbpm|lbpm5g|lbpm-x2|fb-*|train|enum|echo|u0; TSEQ_LEN,
  TSCALE, NEG, DEVCAP).
* `examples/gowin/luna-enum-gen2/top.py` — the dual-rate top (POR
  66_125 era; session-15 loadout: uart0 = per-cause recovery split,
  uart1 = pipe probe with accepted-header counter; the POR comment
  carries the full lottery history and the 128-bit-pivot decision).
* `examples/gowin/luna-enum-gen1x2/top.py` — the Gen 1x2-highest
  PortMatch probe = the x2-PORT QUALIFIER tool (boot-rate-switch
  shape, MAC at 125, uart1 LBPM ring).
* `examples/gowin/probe-trims/top.py`, `probe-ln0tx/top.py` — the W0
  probe rigs and their verdict tables (module docstrings).
* `README.md` — the fork banner: layout, one-clone flow.
* `gw_usb3/` submodule: README + module docstrings (every vendor
  quirk documented where reproduced); `gw_usb3/tests/equiv/harness.py`
  docstring — how golden-vs-port simulation works (also the machinery
  for a full-RX-chain sim bench, the #42 discriminator).
* `gowin-serdes/` submodule: `ARCHITECTURE.md` §"USB3 Recipe",
  `gowin_serdes/usb3.py`, `gowin_serdes/dkusb_gw5at60.py` (board;
  SDC branches: pclk 6.4 ns + rxclk 6.2 ns for the gen2 tops — the
  recovered clock runs 161.133 MHz at 10G; 8.0 ns gen1x2 tops
  (x2 now out of scope)), `gowin_serdes/bench.py` (debug helpers).
* `luna/gateware/interface/serdes_phy/gowin_gtr12.py` — the PIPE
  adapter (LFPS dialect, boot-rate-switch, boot domain discipline).
* `examples/gowin/luna-multiep/top.py` — the shipping 3-pair top
  (wire checkers, ACKPROBE, BurstEventCapture, POR lottery comment).
* `sim/sim_link_loopback.py` header — every host-model knob.
* The frozen archive (`~/Downloads/GW_USB3/ARCHIVE.md`) — vendor
  refdesign baselines, hybrid A/B rig, bug-report packages.
