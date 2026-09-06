#!/bin/bash
# Full regression battery (HANDOVER 10j set, extended in sessions 8+).
# Run from anywhere: paths resolve relative to this script.
# Logs land in /tmp/kilo (created if missing); failures are copied to
# /tmp/kilo/batt_FAIL_<tag>.log for inspection.
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"                   # luna-ss fork root
cd "$ROOT"
LL=sim
mkdir -p /tmp/kilo
run() {
    local tag="$1"; shift
    if env "$@" pdm run python "$LL/sim_link_loopback.py" \
        > /tmp/kilo/batt_last.log 2>&1; then
        echo "PASS $tag"
    else
        echo "FAIL $tag <<<<<<<<"
        cp /tmp/kilo/batt_last.log "/tmp/kilo/batt_FAIL_${tag// /_}.log"
    fi
}
run "default"
run "eps2" NUM_EPS=2
run "eps3" NUM_EPS=3
run "eps4" NUM_EPS=4
run "eps3+ctrl" NUM_EPS=3 WITH_CONTROL=1
run "ctrl" WITH_CONTROL=1
run "bytes4" LOOPBACK_BYTES=4
run "bytes1028" LOOPBACK_BYTES=1028
run "lbad5" LBAD_EVERY=5 LOOPBACK_BYTES=8192
run "badhdr7" BADHDR_EVERY=7 LOOPBACK_BYTES=8192
run "bubbles3" HOST_BUBBLES=3 LOOPBACK_BYTES=8192
run "window4" WINDOW_KIB=4 LOOPBACK_BYTES=16384
run "eps3+ctrl+itp" NUM_EPS=3 WITH_CONTROL=1 ITP_EVERY=211 HOST_LDN_EVERY=97
# link-recovery conformance (session 9): retrain from U0 mid-traffic;
# unacked headers must be retransmitted per the advertisement, not flushed
run "rec-every" RECOVERY_EVERY=1200 NUM_EPS=3
run "rec+lbad" RECOVERY_EVERY=2000 NUM_EPS=2 LBAD_EVERY=5
run "rec+badhdr" RECOVERY_EVERY=2000 NUM_EPS=2 BADHDR_EVERY=7
run "rec+ctrl" RECOVERY_AT=1500 WITH_CONTROL=1 NUM_EPS=3 LOOPBACK_BYTES=8192
run "rec+urb" RECOVERY_EVERY=3000 NUM_EPS=3 URB_PACKETS=4 URB_GAP=800 HOST_LATENCY=20 LC_LATENCY=12 REORDER=1
# bMaxBurst>1 engines (session 9): multi-packet bursts per token, per-packet
# sequence advance, cumulative ACKs, EOB, rewind-on-retry, OUT window
# advertisement.  (Recovery below ~2600-cycle periods with 3 bursting pipes
# is a starvation regime -- recovery overhead plus the spec-correct
# EOB/terminating-ACK/ERDY round trip per burst (session 10) eats the
# service windows -- not a correctness bound; see HANDOVER 10m/10n.)
run "burst" BURST=4 NUMP=4 NUM_EPS=3
run "burst+sweep" BURST=4 NUMP=4 NUMP_SWEEP=1 NUM_EPS=2
run "burst+lbad" BURST=4 NUMP=4 LBAD_EVERY=5
run "burst+badhdr" BURST=4 NUMP=4 BADHDR_EVERY=7
run "burst+short" BURST=4 NUMP=4 LOOPBACK_BYTES=1028
run "burst+rec" BURST=4 NUMP=4 RECOVERY_EVERY=2600 NUM_EPS=3
run "burst+urb" BURST=4 NUMP=4 NUM_EPS=3 URB_PACKETS=4 URB_GAP=800 HOST_LATENCY=20 LC_LATENCY=12 REORDER=1
run "burst+ctrl" BURST=2 NUMP=2 WITH_CONTROL=1 NUM_EPS=3 LOOPBACK_BYTES=8192
# bug-#35 regression (session 10): the bench xHC pipelines its whole
# scheduling window at transfer start (16 back-to-back OUT DPs before any
# device ACK); with the hardware's elastic loopback FIFO behind the OUT
# engine, the ring can become non-full MID-PACKET and the un-fixed engine
# commits partial tails / phantom ZLPs (the BURST=2 2048-byte bench wedge).
run "burst+blast" BURST=2 NUMP=2 OUT_WINDOW0=16 WITH_FIFO=4096 NUM_EPS=1 LOOPBACK_BYTES=65536 RETRY_TIMEOUT=1500
run "burst+blast3" BURST=2 NUMP=2 OUT_WINDOW0=16 WITH_FIFO=4096 NUM_EPS=3 LOOPBACK_BYTES=32768 RETRY_TIMEOUT=2500
run "blast+fifo1" BURST=1 NUMP=1 OUT_WINDOW0=16 WITH_FIFO=4096 NUM_EPS=1 LOOPBACK_BYTES=65536 RETRY_TIMEOUT=1500
if pdm run python "$LL/sim_loopback.py" > /tmp/kilo/batt_ep.log 2>&1; then
    echo "PASS endpoint-sim"
else
    echo "FAIL endpoint-sim <<<<<<<<"
fi
if pdm run pytest -q > /tmp/kilo/batt_pytest.log 2>&1; then
    echo "PASS pytest ($(grep -Eo '[0-9]+ passed' /tmp/kilo/batt_pytest.log | head -1))"
else
    echo "FAIL pytest <<<<<<<<"
fi
echo BATTERY-DONE
# training sims (added session 8)
for s in gowin_gtr12_sim gowin_gtr12_training_sim; do
    if pdm run python examples/usb/superspeed/$s.py > /tmp/kilo/batt_$s.log 2>&1; then
        echo "PASS $s"
    else
        echo "FAIL $s <<<<<<<<"
    fi
done
echo BATTERY2-DONE
# stale-ACK race regression (bug #26, session 8)
if pdm run python "$LL/sim_stale_ack.py" > /tmp/kilo/batt_staleack.log 2>&1; then
    echo "PASS stale-ack"
else
    echo "FAIL stale-ack <<<<<<<<"
fi
# adversarial TX-chain fuzz (found #24/#25, session 8; in-repo session 9)
if pdm run python "$LL/tx_fuzz.py" > /tmp/kilo/batt_txfuzz.log 2>&1; then
    echo "PASS tx-fuzz"
else
    echo "FAIL tx-fuzz <<<<<<<<"
fi
echo BATTERY3-DONE
# ── gen2 section (session 11c; prompt.md Phase 2, gate G2) ──────────
# gen2-oracle must be GREEN: the host-side Gen2 coding model pinned
# byte-exact against the silicon-proven gw_usb3 scrambler RTL.
# The end-to-end phases are EXPECTED-RED until the Phase-3/4 device
# work lands: the battery PASSES when they fail with their verdict
# (red baseline enforced) and trips if one unexpectedly goes green,
# so flipping an entry to expect-green is always a conscious act.
if pdm run python "$LL/sim_gen2_oracle.py" > /tmp/kilo/batt_gen2_oracle.log 2>&1; then
    echo "PASS gen2-oracle"
else
    echo "FAIL gen2-oracle <<<<<<<<"
fi
# gen2-scd flipped to expect-green (session 11e: SCD1 tRepeat
# modulation landed -- lfps.py scd_pattern, elaboration-gated).
if PHASE=scd pdm run python "$LL/sim_link_gen2.py" > /tmp/kilo/batt_gen2_scd.log 2>&1; then
    echo "PASS gen2-scd"
else
    echo "FAIL gen2-scd <<<<<<<<"
fi
# Phase-3 M3-M5 entries (session 12, expect-green): LBPM PortMatch/
# PortConfig at 10G and 5G outcomes, the SS-operation fallbacks, and
# the Gen2 training-timeout speed-fallback loop (gate G3).
for ph in lbpm lbpm5g fb-legacy fb-noscd2; do
    if PHASE=$ph pdm run python "$LL/sim_link_gen2.py" > /tmp/kilo/batt_gen2_$ph.log 2>&1; then
        echo "PASS gen2-$ph"
    else
        echo "FAIL gen2-$ph <<<<<<<<"
    fi
done
if PHASE=fb-timeout TSCALE=0.0625 TSEQ_LEN=256 pdm run python "$LL/sim_link_gen2.py" > /tmp/kilo/batt_gen2_fb-timeout.log 2>&1; then
    echo "PASS gen2-fb-timeout"
else
    echo "FAIL gen2-fb-timeout <<<<<<<<"
fi
# Phase-4 entries (session 12, expect-green; gate G4): Gen2 block
# training to U0 (gen2-train, CONSCIOUSLY FLIPPED from the enforced-red
# G2 baseline), enumeration (modulo-16 + LCRD1/LCRD2 + DPH length
# replica + bcdUSB 0310) and the small bulk echo -- all end-to-end
# through the RTL scrambler chain.
for ph in train enum echo; do
    if PHASE=$ph TSEQ_LEN=64 pdm run python "$LL/sim_link_gen2.py" > /tmp/kilo/batt_gen2_$ph.log 2>&1; then
        echo "PASS gen2-$ph"
    else
        echo "FAIL gen2-$ph <<<<<<<<"
    fi
done
# Gen2 TX beat pacing (session 13; HANDOVER 10r suspect #1): the block
# transmitter must never overrun the PHY's 32-deep 128b/132b gearbox
# FIFO (one dead beat per 16 blocks; the fork-root pytest testpaths
# only cover gw_usb3/tests, so this rides as its own entry).
if pdm run pytest tests/test_gen2_pacing.py -q > /tmp/kilo/batt_gen2_pacing.log 2>&1; then
    echo "PASS gen2-pacing"
else
    echo "FAIL gen2-pacing <<<<<<<<"
fi
# The 2:1 PIPE bridge (session 20; width program usb3_design.md
# 13.3/13.4): two-clock testbench pinning BOTH directions byte-exact
# across the pclk <-> pclk/2 seam -- blocks, the SKP-halfbeat seam,
# valid gaps, RX gap cadences + orphan drop, the Gen1 fallback leg,
# and the phy_status latch-and-hold.  Includes the permanent negative
# control: an INVERTED divider phase must fail the byte-exact check
# (RED recorded 2026-09-06: beat-0 data mispaired with the next
# beat's second half -- the wire-garbage class).  The pacing entry
# above additionally carries the bridged occupancy-lag band sweep
# (2-4 core cycles green, 10 = red teeth).
if pdm run pytest tests/test_gen2_pipe_bridge.py -q > /tmp/kilo/batt_gen2_bridge.log 2>&1; then
    echo "PASS gen2-bridge"
else
    echo "FAIL gen2-bridge <<<<<<<<"
fi
# Gen2 TX request-seam conformance (session 16, bug #46; the #45 sim
# leads of HANDOVER 10u): 1-cycle idle_mode blips at every alignment
# must never truncate a 132-bit block on the PIPE or disturb the
# single-SDS rule (drain-safe inactive arm + level-based SDS arming),
# and a recovery entry must flush the TX bridge -- a mid-command yank
# historically carried a truncated LC across the retrain and emitted
# it as a REPLICA-VALID 0x5A5A alias command ahead of the
# advertisement.  RED baselines recorded 2026-09-04 (truncated-block
# at odd alignments; the (90,90,90,90) fragment construct).
if pdm run pytest tests/test_gen2_tx_seams.py -q > /tmp/kilo/batt_gen2_txseams.log 2>&1; then
    echo "PASS gen2-tx-seams"
else
    echo "FAIL gen2-tx-seams <<<<<<<<"
fi
# Gen 1x2 PortMatch (session 14, width program W0.3): a Gen 1x2-highest
# device against a Gen 2x2-announcing host must hold its 0x40 dual-lane
# announcement (the higher host adjusts down, Table 7-14), match at
# Gen 1x2, PHY-Ready handshake, and configure the 5G rate.  RED baseline
# recorded 2026-09-01 against the fixed Gen2x1-highest stack: "device
# announced 0x04, expected the Gen 1x2 dual-lane capability (0x40)".
# (Constant corrected vs the mission text: Table 7-13 dual-lane = b6 =
# 0x40, not 0x20.)
if PHASE=lbpm-x2 DEVCAP=gen1x2 pdm run python "$LL/sim_link_gen2.py" > /tmp/kilo/batt_gen2_lbpm-x2.log 2>&1; then
    echo "PASS gen2-lbpm-x2"
else
    echo "FAIL gen2-lbpm-x2 <<<<<<<<"
fi
# U0 real-host surface (session 14; HANDOVER 10s suspects 1-3): LUP
# keepalives at tU0LTimeout, inbound host Port Capability/Configuration
# LMPs + ITPs, and the SSP LMP field rules [Tables 8-7/8-9/8-10].  RED
# baseline recorded 2026-09-01 against the pre-#41 stack: "Port
# Capability LMP carries Gen 1x1-only field values ... link_speed=1
# num_hp_buffers=4" + "Port Configuration Response code 0x2 ... reads
# as 'Link Speed rejected' -> DFP port error [10.16.2.6]" -- bug #41.
if PHASE=u0 TSEQ_LEN=64 pdm run python "$LL/sim_link_gen2.py" > /tmp/kilo/batt_gen2_u0.log 2>&1; then
    echo "PASS gen2-u0"
else
    echo "FAIL gen2-u0 <<<<<<<<"
fi
# Gen2 Hot Reset (session 15, bug #44 hunt): the xHCI port-reset flow
# at Gen2 -- Recovery entry from U0, TS2-with-Reset handshake, SDS in
# Hot Reset.Exit, full link re-init (LGOOD_15 + 4+4), device address
# reset, descriptor read.  Green from first run (the stack's handshake
# is sound with an idealized feed; the silicon death at this step is
# still open) -- kept as the regression fence for the reset surface.
if PHASE=hotreset TSEQ_LEN=64 pdm run python "$LL/sim_link_gen2.py" > /tmp/kilo/batt_gen2_hotreset.log 2>&1; then
    echo "PASS gen2-hotreset"
else
    echo "FAIL gen2-hotreset <<<<<<<<"
fi
# Plain mid-traffic Recovery x3 at Gen2 (session 15, #45 hunt): unlike
# Hot Reset, Recovery PRESERVES sequence numbers -- the
# re-initialization advertisement carries NONZERO LGOODs (1/3/5) and
# the full 4+4 rule-2d credit re-advertisement; traffic must resume
# with preserved numbering.  Green against the idealized feed (the
# silicon metronomic loop does not reproduce here); kept as the
# regression fence for the U0 re-initialization surface.
if PHASE=recovery TSEQ_LEN=64 pdm run python "$LL/sim_link_gen2.py" > /tmp/kilo/batt_gen2_recovery.log 2>&1; then
    echo "PASS gen2-recovery"
else
    echo "FAIL gen2-recovery <<<<<<<<"
fi
# Mid-transfer Recovery cuts (session 17, bugs #50+#51; the #49 sim
# lead (b)): a GetDescriptor data stage cut by a host-initiated
# retrain at swept offsets -- between the IN ACK TP and the DPH,
# across the DPH/DPP seam, and inside/after the DPP.  RED baselines
# recorded 2026-09-04: offset 2 = the link-down advertisement race
# (a header accepted in the first link-down cycle was delivered but
# NOT covered by the re-advertisement; the partner's rule-7
# retransmission then reads as a bad sequence -> device-initiated
# recovery loop, wedged EP0 -- bug #50); offset 24 = the
# consumed-payload bookkeeping window (a drop between the last
# payload word and ``done`` left the header marked never-sent; its
# DL=1 retransmission attached PHANTOM payload instead of aborting
# the DPP -- garbage on the wire, bug #51).  The PHY TX FIFO pacing
# band is asserted across every cut (the txfifo-hi28 canary, lead (a)).
if PHASE=reccut TSEQ_LEN=64 pdm run python "$LL/sim_link_gen2.py" > /tmp/kilo/batt_gen2_reccut.log 2>&1; then
    echo "PASS gen2-reccut"
else
    echo "FAIL gen2-reccut <<<<<<<<"
fi
# Hot Reset with a transfer PARKED mid-data-stage (session 17; the
# #49 sim lead (c)): SETUP acked, IN token sent, the device's DPH
# left un-acknowledged with its credit held and no STATUS stage --
# then the full xHCI port-reset flow.  EP0/protocol state must fully
# clear: LGOOD_15 + 4+4 re-advertisement, address reset, clean
# descriptor read (the bench wedge survives hot reset; a parked-state
# leak here would name the mechanism).
if PHASE=hotreset-parked TSEQ_LEN=64 pdm run python "$LL/sim_link_gen2.py" > /tmp/kilo/batt_gen2_hotreset-parked.log 2>&1; then
    echo "PASS gen2-hotreset-parked"
else
    echo "FAIL gen2-hotreset-parked <<<<<<<<"
fi
# Concurrent host advertisement (session 16, hardening #47; the #45
# sim lead (b) of HANDOVER 10u EXECUTED): the host advertises at its
# physically earliest instant -- gated only on observing the device's
# own idle stream -- across swept sub-block offsets on every recovery
# re-entry.  VERDICT: under causally-legal timing the historical RTL
# was NOT red (the RX pipeline delays the advertisement past
# link_ready) -- candidate (b) does not reproduce #45; the widened
# gen2 capture window (listen = idle states + U0) lands as hardening
# (the truly-early stimulus red: a credit-starved link that trains,
# receives, and never transmits a header).
if PHASE=advearly TSEQ_LEN=64 pdm run python "$LL/sim_link_gen2.py" > /tmp/kilo/batt_gen2_advearly.log 2>&1; then
    echo "PASS gen2-advearly"
else
    echo "FAIL gen2-advearly <<<<<<<<"
fi
# Negative control: withholding the host's Type-2 credits must starve
# the device's descriptor DP (proves the LCRD2 pool gating is real).
if PHASE=enum TSEQ_LEN=64 NEG=nolcrd2 pdm run python "$LL/sim_link_gen2.py" > /tmp/kilo/batt_gen2_neg.log 2>&1; then
    echo "FAIL gen2-neg-nolcrd2 (UNEXPECTED GREEN: type-2 pool not gating) <<<<<<<<"
elif grep -q "timed out waiting for descriptor DPH" /tmp/kilo/batt_gen2_neg.log; then
    echo "PASS gen2-neg-nolcrd2 (descriptor DP correctly withheld)"
else
    echo "FAIL gen2-neg-nolcrd2 (died with the wrong verdict) <<<<<<<<"
fi
# Full PHY RX chain (session 15; bugs #42/#43): wire-serialized blocks
# at the true async recovered-clock rate through the REAL RxGearbox132
# -> CDC AsyncFifo -> Descrambler -> Gen2BlockReceiver.  Checks the
# byte-exact translation of offset-swept header packets [7.2.1.3],
# all-5Ah DPP payloads (idle run replay), 100 SKP LFSR reseeds, and the
# #43 queue bound (level must RETURN TO ZERO -- the historical per-beat
# idle enqueue ratcheted to ~650 over this traffic and never drained).
if pdm run python "$LL/rx_chain_full.py" > /tmp/kilo/batt_gen2_rxchain.log 2>&1; then
    echo "PASS gen2-rxchain"
else
    echo "FAIL gen2-rxchain <<<<<<<<"
fi
# Gen2BlockReceiver placement sweep (session 15, the #42 hunt tooling):
# header packets / DPHs / LCs at every symbol offset, back-to-back
# constructs, and PIPE rx_valid gaps at several cadences (the gearbox
# wrap-gap pattern) -- direct engine feed, byte-exact expectations.
RXOFF_OK=1
for g in 0 33 3; do
    if ! GAP=$g pdm run python "$LL/rx_hp_offsets.py" > /tmp/kilo/batt_gen2_rxoff_$g.log 2>&1; then
        RXOFF_OK=0
    fi
done
if [ "$RXOFF_OK" = "1" ]; then
    echo "PASS gen2-rx-offsets"
else
    echo "FAIL gen2-rx-offsets <<<<<<<<"
fi
# -- The 128-bit core (width program, session 19): the SAME Gen2 phase
# set at core_width=128 -- one beat = one block at the 78.125 core
# clock, clear-data conditioning (the RTL scrambler round-trip is a
# 64-bit PHY surface), the protocol boundary behind the width
# adapters.  First green 2026-09-05: the whole stack (wide framers,
# gen2 128 bridges, adapters, EP0) enumerates end to end with the
# pacing band held (max 16/32, hi28 0).
for W128PH in train enum echo u0 hotreset hotreset-parked recovery reccut advearly; do
    if W128=1 PHASE=$W128PH TSEQ_LEN=64 pdm run python "$LL/sim_link_gen2.py" > /tmp/kilo/batt_w128_$W128PH.log 2>&1; then
        echo "PASS w128-$W128PH"
    else
        echo "FAIL w128-$W128PH <<<<<<<<"
    fi
done

echo BATTERY4-DONE

