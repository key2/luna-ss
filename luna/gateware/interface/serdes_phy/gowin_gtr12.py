#
# This file is part of LUNA.
#
# Copyright (c) 2026 whitequark research heavy industries
# SPDX-License-Identifier: BSD-3-Clause
""" Gowin GTR12 (Arora V) SerDes-based USB3 PIPE PHY.

Wraps ``gw_usb3.Usb31Phy`` -- an Amaranth port of the Gowin USB 3.1 soft
PHY (8b/10b, word alignment, elastic buffer, LFPS pattern generation, and
the UPAR CSR sequencer that drives the GTR12 hard macro) -- and adapts it
to the LUNA :class:`PIPEInterface` convention (``width=8``).

The wrapped PHY is hardware-proven: driven by the Gowin reference LTSSM it
enumerates at SuperSpeed Plus Gen2x1 on a GW5AT-60 (DK_USB board).

Implementation-dependent behavior of the standard PIPE signals:

``pclk``
    Provided by the PHY from the SerDes PCS transmit clock: 125 MHz at
    Gen1 (5 GT/s), 156.25 MHz at Gen2.  All interface signals are
    synchronous to it.  This backend assumes the LUNA ``ss`` domain *is*
    pclk (no gearing: the interface is natively 32-bit @ 125 MHz at Gen1).
``tx_data`` / ``rx_data``
    64-bit.  At Gen1 only bits [31:0] carry symbols (4 symbols/cycle,
    ``tx_datak[3:0]``); the upper half is reserved for the Gen2 block
    payload.  This matches LUNA's 32-bit Gen1 stream layer, which
    naturally drives/consumes the low half.
``rate``
    Ignored.  The TUSB1310A dialect drives ``rate=1`` for 5 GT/s, while
    the Gowin PIPE encodes 0=5G/1=10G; this backend is Gen1-only and ties
    the PHY's Rate input to 0.  The PHY must be built with
    ``rate_init=0`` and a 5G-boot SerDes CSR configuration so no rate
    change is needed at startup.
``power_down``
    P0..P3 sequencing implemented by the PHY (with PhyStatus acks).  The
    PHY powers up in P2 and acks the MAC's transition to P0.
``tx_detrx_lpbk`` / ``tx_elec_idle``
    PIPE-standard: in P0, asserting both requests LFPS transmission (the
    PHY generates the LFPS pattern and toggles the SerDes electrical-idle
    CSR per burst); in P2/P3, ``tx_detrx_lpbk`` with ``tx_elec_idle``
    requests receiver detection (CSR-mediated, several microseconds).
``rx_elec_idle``
    Follows the true line state (SerDes signal-detect, 6-sample
    filtered) whenever no valid RX symbols have been decoded for ~10 us;
    reads as 1 (idle) while RX symbols flow.  LFPS bursts are therefore
    visible with ~10 us onset latency after traffic stops.
``phy_status``
    Synthesized TUSB1310A-style startup semantics: held high from reset
    until the PHY reports its first status event with the SerDes PLL
    locked, then low; subsequent PHY event pulses (power-state acks) are
    forwarded.
``power_present``
    Tied high by the PHY (device-side; VBUS presence is not routed
    through the SerDes).
``phy_mode``, ``elas_buf_mode``, ``tx_deemph``, ``tx_margin``,
``tx_swing``, ``tx_ones_zeros``, ``tx_compliance``, ``rx_eq_training``
    Accepted and ignored (fixed by the SerDes CSR configuration).

The underlying SerDes lane/DRP connections are *not* made here: on
hardware, wire ``self.phy`` with ``gowin_serdes.usb3.attach_usb3_phy``;
in simulation, drive the ``self.phy.serdes_*`` ports from the testbench.
"""

from amaranth import *

from ..pipe import PIPEInterface


class GowinGTR12PIPE(PIPEInterface, Elaboratable):
    """ PIPE adapter around the gw_usb3 Gowin GTR12 soft PHY.

    Parameters
    ----------
    phy: gw_usb3.Usb31Phy, optional
        A pre-constructed PHY instance.  If omitted, one is created from
        ``phy_kwargs`` (requires ``gw_usb3`` to be importable).
    phy_kwargs: dict, optional
        Constructor arguments for ``gw_usb3.Usb31Phy`` when ``phy`` is not
        given.  Sensible Gen1 defaults are applied: ``gen2=False``,
        ``rate_init=0``.

    Attributes
    ----------
    phy: gw_usb3.Usb31Phy
        The wrapped PHY; its ``serdes_*`` ports must be connected to a
        GTR12 lane (``attach_usb3_phy``) or driven by a testbench.
    """

    def __init__(self, *, phy=None, phy_kwargs=None, boot_rate_switch=False,
                 boot_domain="ss", gen2=False):
        """``boot_rate_switch``: boot the SerDes in the (byte-pinned,
        hardware-proven) 10G trim and have the adapter itself perform the
        vendor 10G->5G rate-change sequence before reporting the PHY
        ready -- the MAC only ever sees a 125 MHz Gen1 PHY.  Requires the
        PHY built with ``rate_init=1`` and a 10G-boot CSR blob.

        ``boot_domain``: the clock domain the boot sequencing runs in.
        On hardware this MUST be a reset-free pclk-derived domain (e.g.
        the top's ``ss_raw``): the whole point of the sequenced bring-up
        is that the MAC's ``ss`` domain can be *held in reset* until
        ``phy_ready`` -- no MAC state then ever clocks at the 156.25 MHz
        boot rate or through the CSR-driven pclk retune glitches, which
        were observed to corrupt idle-but-clocking MAC registers
        (dead TP generator / wedged handshake arbiter at 3 endpoint
        pairs; HANDOVER 10k).

        Boot-mode handshake (``boot_rate_switch`` only):

        ``boot_start`` (input)
            Begin the PHY bring-up; driven by the top's power-on reset
            chain (double-synchronized into ``boot_domain`` here).
        ``phy_ready`` (output, registered in ``boot_domain``)
            The rate switch has fully completed (including the CSR
            sequencer's delayed second write burst); the MAC reset may
            be released.  Latched once; deliberately survives a MAC-side
            POR replay (the SerDes stays configured at 5G).

        In boot mode the adapter also *owns* ``phy_resetn``: the MAC's
        startup reset pulse must not reach the PHY, because the CSR
        sequencer's rate-request synchronizers reset to the 10G boot
        value and a post-switch reset pulse (with Rate low) would fire a
        spurious rate-change sequence -- glitching pclk under a live MAC.
        """
        super().__init__(width=8)
        self._boot_rate_switch = boot_rate_switch
        self._boot_domain = boot_domain
        # Dual-rate (SuperSpeedPlus) mode: the PHY is built with its Gen2
        # datapath, boots in the 10G trim, and the MAC owns ``rate``
        # (Gowin encoding, 0 = 5 GT/s / 1 = 10 GT/s): the LTSSM's
        # PortConfig/SpeedSwitch handshake drives it and expects a
        # phy_status ack pulse once the change applied.  Incompatible
        # with ``boot_rate_switch`` (the LTSSM owns the rate instead).
        # NOTE: the ack currently uses the boot path's proven fixed
        # envelope rather than CSR completion feedback -- hardware
        # verdict pending (G5; HANDOVER 10r).
        self._gen2 = gen2
        if gen2:
            assert not boot_rate_switch

        self.boot_start = Signal()
        self.phy_ready  = Signal()

        # Gen2 builds: LTSSM training indicator (consumed by the PHY's
        # Gen2 descrambler acquisition).
        self.ltssm_training = Signal()

        # Gen2 builds: the PHY's 32-deep TX gearbox FIFO occupancy
        # (TxFifoWrNum) -- the MAC's closed-loop TX pacing reference
        # (bug #44: the FIFO must run near-full; the open-loop cadence
        # left it riding the underflow boundary and the gearbox
        # serialized stale bits whenever the phases misaligned).
        self.tx_fifo_occupancy = Signal(5)

        if phy is None:
            from gw_usb3 import Usb31Phy
            # Bug #38: Usb31Phy's DEFAULT csr_config is Q0_LN1.  If the
            # serdes is generated for any other quad/lane, the runtime
            # CSR sequencer (eidle/FFE handshakes, 10G->5G rate change)
            # silently addresses the WRONG lane's registers: on hardware
            # the boot rate switch then "completes" (UPAR acks) while
            # pclk stays at the 156.25 MHz boot trim.  Pass
            # phy_kwargs=dict(csr_config=UparCsrConfig(quad=..., lane=...))
            # matching the serdes blob (as the examples/gowin tops do).
            kwargs = dict(gen2=gen2,
                          rate_init=1 if (boot_rate_switch or gen2) else 0)
            kwargs.update(phy_kwargs or {})
            phy = Usb31Phy(**kwargs)
        self.phy = phy

    def elaborate(self, platform):
        m = Module()
        m.submodules.phy = phy = self.phy

        #
        # Clocking & reset
        #
        m.d.comb += self.pclk.eq(phy.pclk)
        if not self._boot_rate_switch:
            m.d.comb += phy.phy_resetn.eq(~self.reset)
        # (in boot mode, phy_resetn is owned by the boot sequencer below)

        #
        # MAC -> PHY (transmit + control)
        #
        m.d.comb += [
            phy.PipeTxData          .eq(self.tx_data),
            phy.PipeTxDataK         .eq(self.tx_datak[0:4]),
            # PIPE 3.0 MACs (LUNA today) do not drive tx_datavalid; the
            # Gen1 rule is "valid whenever not in electrical idle".
            phy.PipeTxDataValid     .eq(self.tx_datavalid | ~self.tx_elec_idle),
            phy.PipeTxSyncHead      .eq(self.tx_sync_header),
            phy.PipeTxStartBlock    .eq(self.tx_start_block),

            phy.RxPolarity          .eq(self.rx_polarity),
            phy.RxTermination       .eq(self.rx_termination),
            phy.ElasticityBufferMode.eq(self.elas_buf_mode),

            # Only consumed by the Gen2 (128b/132b) datapath.
            phy.LTSSM_is_Training   .eq(self.ltssm_training
                                        if self._gen2 else 0),
        ]

        # Gen1-only backend: Gowin rate encoding 0 = 5 GT/s.  (The
        # TUSB1310A dialect's rate input means something different;
        # deliberately not forwarded.)
        boot_done = Signal(init=0 if self._boot_rate_switch else 1)
        boot_settled = Signal(init=0 if self._boot_rate_switch else 1)
        if self._boot_rate_switch:
            # Boot in the proven 10G trim, then run the vendor rate-change
            # sequence to 5G by dropping Rate.  Fixed, generous timing;
            # pclk stalls/shifts (156.25 -> 125 MHz) during the CSR
            # sequence simply pause the counter.  Runs in ``boot_domain``
            # (reset-free on hardware) so the MAC can sleep through it.
            #
            # Thresholds: PHY reset released at bit 10 (~8 us, mirrors the
            # MAC reset controller's startup pulse this replaces); rate
            # drop at bit 16 (~0.4 ms, the proven envelope); done at
            # all-ones (2^20 pclk = ~7-8 ms) -- generously past the CSR
            # sequencer's full rate sequence, whose delayed second write
            # burst runs 2^18 *upar* clocks (~2.2-4.7 ms at the 56-118 MHz
            # ring oscillator) after the first burst.  The old 18-bit
            # count released phy_status before that second burst (reset
            # release + rxsd), i.e. with CSR activity still pending.
            dom = m.d[self._boot_domain]
            boot_cnt  = Signal(20)
            post_cnt  = Signal(12)
            rate_r    = Signal(init=1)
            boot_rstn = Signal(init=0)
            start_s   = Signal()
            start_d   = Signal()
            dom += [start_s.eq(self.boot_start), start_d.eq(start_s)]
            with m.If(start_d & ~boot_done):
                dom += boot_cnt.eq(boot_cnt + 1)
                with m.If(boot_cnt[10]):        # ~8 us: release PHY reset
                    dom += boot_rstn.eq(1)
                with m.If(boot_cnt[16]):        # ~0.4 ms: request 10G->5G
                    dom += rate_r.eq(0)
                with m.If(boot_cnt.all()):      # ~7 ms: settled at 5G
                    dom += boot_done.eq(1)
            # Post-boot settle: phy_status is held high for ~33 us more so
            # the (just-woken) MAC reset controller sees the TUSB startup
            # handshake edge (high during startup, then low).
            with m.If(boot_done & ~boot_settled):
                dom += post_cnt.eq(post_cnt + 1)
                with m.If(post_cnt.all()):
                    dom += boot_settled.eq(1)
            m.d.comb += [
                phy.Rate         .eq(rate_r),
                phy.phy_resetn   .eq(boot_rstn),
                self.phy_ready   .eq(boot_done),
            ]
        elif self._gen2:
            # Dual-rate: forward the MAC-owned rate (the PHY's own CSR
            # sequencer runs the retune on changes) and synthesize the
            # PIPE completion ack after the boot path's proven envelope
            # (2^20 pclk, ~7 ms -- generously past the CSR sequencer's
            # delayed second write burst).
            rate_s  = Signal(init=1)
            rate_d  = Signal(init=1)
            ack_cnt = Signal(20)
            ack_run = Signal()
            rate_ack = Signal()
            m.d.ss += [rate_s.eq(self.rate), rate_d.eq(rate_s)]
            m.d.comb += phy.Rate.eq(rate_d)
            with m.If(rate_s != rate_d):
                m.d.ss += [ack_run.eq(1), ack_cnt.eq(0)]
            with m.Elif(ack_run):
                m.d.ss += ack_cnt.eq(ack_cnt + 1)
                with m.If(ack_cnt.all()):
                    m.d.ss += ack_run.eq(0)
                    m.d.comb += rate_ack.eq(1)
            m.d.comb += self.phy_ready.eq(1)

            # At the 10G trim the Gen2 block transmitter drives
            # tx_datavalid with real meaning: closed-loop rate-matching
            # gaps for the 128b/132b gearbox (see Gen2BlockTransmitter's
            # pacing section).  Forward it truly -- the Gen1 "valid when
            # not in electrical idle" OR rule above would nullify the
            # gaps and overflow the PHY's 32-deep TX FIFO.  At the 5G
            # trim the Gen1 rule still applies (last assignment wins;
            # Gen1-only builds keep the original statement untouched).
            m.d.comb += phy.PipeTxDataValid.eq(
                Mux(rate_d, self.tx_datavalid,
                    self.tx_datavalid | ~self.tx_elec_idle))

            # The pacing loop's feedback: the PHY's TX gearbox FIFO
            # occupancy (pclk domain, ~2 cycles of register lag --
            # inside the pacing threshold's headroom).
            m.d.comb += self.tx_fifo_occupancy.eq(phy.TxFifoWrNum)
        else:
            m.d.comb += [
                phy.Rate         .eq(0),
                self.phy_ready   .eq(1),
            ]

        #
        # LFPS transmit dialect translation.
        #
        # LUNA (TUSB1310A convention) requests an LFPS burst by asserting
        # TxDetectRx/Loopback *and* TxElecIdle while in P0.  The Gowin
        # PIPE instead uses the PIPE 3.0 low-power signaling convention:
        # an LFPS burst is requested by dropping TxElecIdle while in
        # P1/P2/P3, for the duration of the burst (this is how the
        # hardware-proven vendor LTSSM drives it: parked in P2 with
        # TxElecIdle pulsed low per burst).  Translate combinationally;
        # the PHY's own burst engine shapes the waveform and performs the
        # per-burst electrical-idle CSR writes.
        #
        # Note: each translated burst momentarily sequences the PHY's
        # power-state FSM P0 -> P2 -> P0, emitting PhyStatus ack pulses;
        # LUNA ignores phy_status outside of startup, so this is benign.
        #
        lfps_tx_burst = (self.power_down == 0) \
            & self.tx_elec_idle & self.tx_detrx_lpbk
        with m.If(lfps_tx_burst):
            m.d.comb += [
                phy.PowerDown           .eq(0b10),   # P2
                phy.TxElecIdle          .eq(0),      # burst active
                phy.TxDetectRx_loopback .eq(0),
            ]
        with m.Else():
            m.d.comb += [
                phy.PowerDown           .eq(self.power_down),
                phy.TxElecIdle          .eq(self.tx_elec_idle),
                phy.TxDetectRx_loopback .eq(self.tx_detrx_lpbk),
            ]

        #
        # PHY -> MAC (receive + status)
        #
        m.d.comb += [
            self.rx_data        .eq(phy.PipeRxData),
            self.rx_datak       .eq(phy.PipeRxDataK),      # zero-extended
            self.rx_datavalid   .eq(phy.PipeRxDataValid),
            self.rx_valid       .eq(phy.PipeRxDataValid),
            self.rx_sync_header .eq(phy.PipeRxSyncHead),
            self.rx_start_block .eq(phy.PipeRxStartBlock),

            self.rx_elec_idle   .eq(phy.RxElecIdle),
            self.rx_status      .eq(phy.RxStatus),
            self.power_present  .eq(phy.PowerPresent),
        ]

        #
        # phy_status: synthesize the TUSB1310A startup level.
        #
        # The Gowin PHY emits *pulses* (one shortly after reset, then one
        # per power-state/rate acknowledgement); LUNA's reset controller
        # expects the TUSB level convention (high during startup, low once
        # ready).
        #
        if self._boot_rate_switch:
            # Boot mode: the boot sequencer knows when the PHY is ready --
            # the MAC slept through the PHY's actual startup pulses, so
            # they cannot be used.  Held high until the post-boot settle
            # elapses (the MAC wakes at ``phy_ready`` and its reset
            # controller then sees the high->low startup edge), pulses
            # forwarded afterwards (receiver-detect acks etc.).
            m.d.comb += self.phy_status.eq(
                Mux(boot_settled & phy.serdes_pll_lock, phy.PhyStatus, 1))
        else:
            # Hold phy_status high until the first pulse arrives with
            # the SerDes PLL locked, then forward pulses.  Gen2 builds
            # additionally pulse it when a MAC rate change completes
            # (the PIPE rate-change ack the LTSSM's handshake expects).
            startup_done = Signal()
            with m.If(~startup_done & phy.PhyStatus & phy.serdes_pll_lock):
                m.d.ss += startup_done.eq(1)
            status_pulses = phy.PhyStatus
            if self._gen2:
                status_pulses = phy.PhyStatus | rate_ack
            m.d.comb += self.phy_status.eq(
                Mux(startup_done, status_pulses, 1))

        return m
