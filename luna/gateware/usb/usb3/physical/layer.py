#
# This file is part of LUNA.
#
# Copyright (c) 2020 Great Scott Gadgets <info@greatscottgadgets.com>
# Copyright (c) 2026 the luna-ss contributors
# SPDX-License-Identifier: BSD-3-Clause
""" USB3 physical-layer abstraction."""

import logging

from amaranth import *
from amaranth.lib.fifo import AsyncFIFOBuffered

from ....interface.pipe import TXDeemphMode
from ...stream  import USBRawSuperSpeedStream

from .lfps       import LFPSTransceiver
from .scrambling import Scrambler, Descrambler
from .power      import PHYResetController, LinkPartnerDetector
from .ctc        import CTCSkipInserter, CTCSkipRemover, TxStreamSkidBuffer
from .alignment  import RxWordAligner, RxPacketAligner

class USB3PhysicalLayer(Elaboratable):
    """ Abstraction encapsulating the USB3 physical layer hardware.

    Performs the lowest-level PHY interfacing, including scrambling/descrambling.

    Attributes
    ----------
    sink: USBRawSuperSpeedStream(), input stream
        Data stream accepted from the Link layer; contains raw data to be transmitted.
    source: USBRawSuperSpeedStream(), output stream
        Data stream generated for transit to the Link layer; contains descrambled data accepted from the SerDes.

    enable_scrambling: Signal(), input
        When asserted, scrambling/descrambling will be enabled.
    """

    def __init__(self, *, phy, sync_frequency, scd_pattern=None, gen2=False,
                 gen2_tseq_count=524288, phy_boots_gen2=True, words=1):
        # Width program (usb3_design.md 13.1/13.5): ``words=2`` runs the
        # whole conditioning chain at 8 symbols/beat; the PIPE-shaped
        # ``phy`` interface is then the 128-bit block contract (Gen2:
        # 1 beat = 1 block + tx_halfbeat; Gen1 leg: 8 symbols riding
        # [63:0]).  words=1 verbatim.
        self._words = words
        self._scd_pattern = scd_pattern
        self._gen2 = gen2
        self._gen2_tseq_count = gen2_tseq_count
        # PHY trim at MAC reset release: True = the Gen2 (10G) boot trim
        # (MAC-owned-rate builds); False = the MAC wakes to a 5G PHY
        # (adapter pre-MAC boot rate switch, e.g. Gen 1x2-highest tops).
        # Sets the reset value of the applied-rate register so the rate
        # handshake's "already applied" short-circuit stays truthful.
        self._phy_boots_gen2 = phy_boots_gen2
        self._phy = phy
        self._sync_frequency = sync_frequency

        #
        # I/O port
        #

        # Data streams.
        self.sink                       = USBRawSuperSpeedStream(payload_words=4 * words)
        self.source                     = USBRawSuperSpeedStream(payload_words=4 * words)

        # Raw source (never descrambled; for reset detection).
        self.raw_source                 = USBRawSuperSpeedStream(payload_words=4 * words)

        # Physical link state.
        self.ready                      = Signal()
        self.engage_terminations        = Signal()
        self.tx_deemph                  = Signal(TXDeemphMode)
        self.tx_electrical_idle         = Signal()
        self.tx_ones_zeros              = Signal()
        self.invert_rx_polarity         = Signal()
        self.train_equalizer            = Signal()
        self.vbus_present               = Signal()

        # Scrambling control.
        self.enable_scrambling          = Signal()

        # Link partner detection.
        self.perform_rx_detection       = Signal()
        self.link_partner_detected      = Signal()
        self.no_link_partner_detected   = Signal()

        # LFPS control / detection.
        self.send_lfps_polling          = Signal()
        self.lfps_cycles_sent           = Signal(16)

        self.lfps_ping_detected         = Signal()
        self.lfps_polling_detected      = Signal()

        # SuperSpeedPlus Capability Declaration (SCD builds only)
        self.scd2_select                = Signal()
        self.scd_clear                  = Signal()
        self.scd_enable                 = Signal()
        self.scd1_detected              = Signal()
        self.scd2_detected              = Signal()
        self.lfps_burst_received        = Signal()
        self.lfps_reset_detected        = Signal()

        # SuperSpeedPlus LBPM modem (SCD builds only)
        self.lbpm_enable                = Signal()
        self.lbpm_message               = Signal(8)
        self.lbpm_sent                  = Signal()
        self.lbpm_rx_message            = Signal(8)
        self.lbpm_rx_valid              = Signal()

        # LTSSM-driven PHY rate handshake (gen2 builds only): while
        # ``rate_request`` is held, apply ``rate_select`` (Gowin PIPE
        # encoding: 0 = 5 GT/s, 1 = 10 GT/s) to the PHY's ``rate`` and
        # report ``rate_done`` once the PHY acks (immediately if the
        # rate is already applied).
        self.rate_select                = Signal()
        self.rate_request               = Signal()
        self.rate_done                  = Signal()
        # Currently applied PHY rate (gen2 builds; selects the Gen1 vs
        # Gen2 datapath muxing here and the OS routing in the link
        # layer).
        self.operating_gen2             = Signal()

        # Gen2 block-level ordered-set surface (gen2 builds only).
        self.gen2_send_tseq_burst       = Signal()
        self.gen2_send_ts1_burst        = Signal()
        self.gen2_send_ts2_burst        = Signal()
        self.gen2_idle_mode             = Signal()
        self.gen2_request_hot_reset     = Signal()
        self.gen2_request_no_scrambling = Signal()
        self.gen2_burst_complete        = Signal()
        self.gen2_tseq_detected         = Signal()
        self.gen2_ts1_detected          = Signal()
        self.gen2_ts2_detected          = Signal()
        self.gen2_hot_reset_requested   = Signal()
        self.gen2_loopback_requested    = Signal()
        self.gen2_no_scrambling_requested = Signal()
        self.gen2_sds_detected          = Signal()  # debug (bring-up)
        self.gen2_data_mode             = Signal()  # debug (bring-up)

        # SKP insertion control.
        self.can_send_skp               = Signal()
        self.skip_removed               = Signal()

        # Debug signaling.
        self.ctc_bytes_in_buffer        = Signal(range(8 * words + 1))
        self.alignment_offset           = Signal(range(4 * words))

        # Debug tap: conditioned (descrambled-equivalent) transmit stream
        # as consumed from the TX skid stage (see elaborate; prunable).
        self.debug_tx_data              = Signal(32 * words)
        self.debug_tx_ctrl              = Signal(4 * words)
        self.debug_tx_strobe            = Signal()
        if gen2 and words == 2:
            self.debug_gen2_tx_state    = Signal(16)


    def elaborate(self, platform):
        m = Module()
        phy = self._phy

        #
        # PHY reset & power management.
        #
        m.submodules.reset_controller = reset_controller = PHYResetController(sync_frequency=self._sync_frequency)
        m.d.comb += [
            phy.reset                       .eq(reset_controller.reset),
            reset_controller.phy_status     .eq(phy.phy_status),
            self.ready                      .eq(reset_controller.ready),
        ]


        #
        # PHY control signal handling.
        #
        if self._gen2:
            # Gen2 build: the MAC owns the PIPE rate (Gowin encoding,
            # 0 = 5 GT/s / 1 = 10 GT/s; the PHY boots in its 10G trim).
            # The LTSSM requests changes through the rate handshake; a
            # PIPE rate change is acknowledged by a phy_status pulse
            # (PIPE 3.0/4.x contract -- the Gowin adapter's CSR
            # sequencer acks the same way).  Power-state acks cannot
            # alias into WAIT_ACK: the LTSSM only runs the handshake
            # from Polling states, where power_down is stable at P0.
            rate_r = Signal(init=1 if self._phy_boots_gen2 else 0)
            phy_rate_drive = rate_r
            m.d.comb += self.operating_gen2.eq(rate_r)

            with m.FSM(domain="ss", name="rate_fsm"):

                with m.State("IDLE"):
                    with m.If(self.rate_request):
                        with m.If(self.rate_select == rate_r):
                            m.next = "DONE"
                        with m.Else():
                            m.d.ss += rate_r.eq(self.rate_select)
                            m.next = "WAIT_ACK"

                with m.State("WAIT_ACK"):
                    with m.If(phy.phy_status):
                        m.next = "DONE"

                with m.State("DONE"):
                    m.d.comb += self.rate_done.eq(1)
                    with m.If(~self.rate_request):
                        m.next = "IDLE"
        else:
            # Gen1: use USB3.0 5Gbps signaling (TUSB1310A dialect:
            # rate 1 = 5 GT/s; the Gowin adapter ignores it and pins
            # its 5G trim itself).  Kept in its historical statement
            # position for netlist parity.
            phy_rate_drive = 1

        m.d.comb += [
            # SuperSpeed USB signaling.
            phy.phy_mode                .eq(0b01),
            phy.rate                    .eq(phy_rate_drive),

            # Use nominal half full elastic buffer mode.
            phy.elas_buf_mode           .eq(0),

            # Use default/normal signal thresholds.
            phy.tx_swing                .eq(0),
            phy.tx_margin               .eq(0b000),
            phy.tx_deemph               .eq(self.tx_deemph),
            phy.tx_ones_zeros           .eq(self.tx_ones_zeros),

            # Pass through our remaining control signals directly to the PHY.
            phy.rx_termination          .eq(self.engage_terminations),
            phy.rx_polarity             .eq(self.invert_rx_polarity),
            phy.rx_eq_training          .eq(self.train_equalizer),

            # Pass through our VBUS detected signal up to the link layer.
            self.vbus_present           .eq(phy.power_present)
        ]


        #
        # Link Partner Detection
        #
        m.submodules.rx_detect = rx_detect = LinkPartnerDetector()
        m.d.comb += [
            rx_detect.request_detection    .eq(self.perform_rx_detection),
            rx_detect.phy_status           .eq(phy.phy_status),
            rx_detect.rx_status            .eq(phy.rx_status),

            #self.link_partner_detected     .eq(rx_detect.new_result & rx_detect.partner_present),
            #self.no_link_partner_detected  .eq(rx_detect.new_result & ~rx_detect.partner_present)

            # FIXME: this is temporary; it speeds up partner detection, but isn't strictly correct.
            # (This incorrectly attempts to do link training on USB2 hosts, too).
            phy.power_down                  .eq(0),
            self.link_partner_detected      .eq(phy.power_present)
        ]


        #
        # Transmit output conditioning.
        #

        # Decouple the link layer's transmit handshake from the skip
        # inserter's (combinational) backpressure: without this stage, the
        # inserter's hold condition reaches all the way back into the link
        # layer FSM enables in a single cycle, which does not close timing
        # at 125 MHz.
        m.submodules.tx_skid = tx_skid = TxStreamSkidBuffer(words=self._words)
        m.d.comb += tx_skid.sink.stream_eq(self.sink)

        # Register the scrambling enable: it is decoded combinationally from
        # the LTSSM state and fans into both data-conditioning pipelines;
        # scrambling only toggles at training-state boundaries, so a cycle
        # of latency is free.
        enable_scrambling = Signal()
        m.d.ss += enable_scrambling.eq(self.enable_scrambling)

        # Scramble our data before transmitting it, if scrambling is enabled.
        #
        # The scrambler's sink is held always-valid: the wire always carries
        # a word, and the LFSR must advance with it.  The skid stage above,
        # however, CAN present an invalid cycle (it runs dry for one cycle
        # at transmit-stream arbiter switches -- e.g. between a packet and
        # the link commands that follow it).  Forwarding the stale
        # data/ctrl through the always-valid sink put a fabricated word on
        # the wire at packet boundaries -- stale data XORed with a fresh
        # LFSR value, and stale K-bits passed through unscrambled.  The
        # link partner sees a framing/CRC violation adjacent to the packet
        # and requests a retransmission: ~40-110% of all data packets were
        # silently retransmitted (rty=1) under sustained bulk traffic, and
        # the resulting retry storms are what the three-pipe failures grew
        # from (bug #28, HANDOVER 10l; reproduced in sim_link_loopback.py
        # once its TX conditioning gained the real scrambler).
        #
        # Substitute logical idle (data 0, ctrl 0 -- exactly what the link
        # emits when idle) for the bubble instead: it scrambles to the
        # idle sequence the partner expects between packets.
        m.submodules.scrambler = scrambler = Scrambler(
            initial_value=0xffff, words=self._words)

        if self._gen2:
            # Dual-rate TX front: at the 10G trim the link layer's
            # stream feeds the Gen2 block transmitter instead of the
            # Gen1 scrambler/CTC chain (the PHY owns Gen2 scrambling).
            from .gen2 import Gen2BlockTransmitter, Gen2BlockReceiver
            m.submodules.gen2_tx = gen2_tx = Gen2BlockTransmitter(
                tseq_count=self._gen2_tseq_count, words=self._words)
            m.submodules.gen2_rx = gen2_rx = Gen2BlockReceiver(
                words=self._words)
            if self._words == 2:
                m.d.comb += self.debug_gen2_tx_state.eq(gen2_tx.debug_state)

            # The block transmitter's LTSSM control surface is registered
            # at the seam in BOTH directions (156.25 routing: the
            # link-side burst request registers otherwise reach the
            # block scheduler's FIFO controls in one hop, and the
            # scheduler's ``burst_complete`` reaches the LTSSM's
            # transition cone the same way).  All of these are levels or
            # counting strobes with microsecond-scale tolerances.
            m.d.ss += [
                gen2_tx.send_tseq_burst .eq(self.gen2_send_tseq_burst),
                gen2_tx.send_ts1_burst  .eq(self.gen2_send_ts1_burst),
                gen2_tx.send_ts2_burst  .eq(self.gen2_send_ts2_burst),
                gen2_tx.idle_mode       .eq(self.gen2_idle_mode),
                gen2_tx.request_hot_reset
                    .eq(self.gen2_request_hot_reset),
                gen2_tx.request_no_scrambling
                    .eq(self.gen2_request_no_scrambling),
                self.gen2_burst_complete.eq(gen2_tx.burst_complete),
            ]
            # Closed-loop TX pacing reference (bug #44): the PHY's Gen2
            # TX gearbox FIFO occupancy (TxFifoWrNum), exposed by the
            # PIPE backend as ``tx_fifo_occupancy``.  The block
            # transmitter keeps the FIFO near-full against it -- the
            # only regime the PHY's TX path is silicon-proven in.  A
            # Gen2 build against a backend without this signal is a
            # wiring error, not a fallback case.
            if not hasattr(phy, "tx_fifo_occupancy"):
                raise AttributeError(
                    "gen2=True requires the PIPE backend to expose "
                    "tx_fifo_occupancy (the PHY TX gearbox FIFO level; "
                    "TxFifoWrNum on the gw_usb3 backend)")
            m.d.ss += gen2_tx.tx_fifo_level.eq(phy.tx_fifo_occupancy)

            m.d.comb += [
                gen2_rx.rx_data  .eq(phy.rx_data),
                gen2_rx.rx_head  .eq(phy.rx_sync_header),
                gen2_rx.rx_start .eq(phy.rx_start_block),
                gen2_rx.rx_valid .eq(phy.rx_datavalid),
            ]
            # The ordered-set detect surfaces are registered once more
            # at the seam (156.25 routing: they otherwise reach the
            # LTSSM's timer resets and the link TS mux in one hop).
            # Strobes stay distinct (a TS block spans two beats) and the
            # LTSSM's timing tolerances are microseconds.
            m.d.ss += [
                self.gen2_tseq_detected .eq(gen2_rx.tseq_detected),
                self.gen2_ts1_detected  .eq(gen2_rx.ts1_detected),
                self.gen2_ts2_detected  .eq(gen2_rx.ts2_detected),
                self.gen2_sds_detected  .eq(gen2_rx.sds_detected),
                self.gen2_data_mode     .eq(gen2_rx.data_mode),
                self.gen2_hot_reset_requested
                    .eq(gen2_rx.hot_reset_requested),
                self.gen2_loopback_requested
                    .eq(gen2_rx.loopback_requested),
                self.gen2_no_scrambling_requested
                    .eq(gen2_rx.no_scrambling_requested),
            ]

            # A second registered skid stage on the Gen2 TX leg: the
            # bridge's byte-granular capture cone (symbol translation +
            # accumulator + FIFO write) otherwise starts at tx_skid's
            # output registers across the seam (a reported 156.25
            # routing cone).  Fully elastic; ``first``/``last`` markers
            # ride along.
            m.submodules.gen2_tx_skid = gen2_tx_skid = \
                TxStreamSkidBuffer(words=self._words)
            m.d.comb += gen2_tx.sink.stream_eq(gen2_tx_skid.source)

            with m.If(rate_r):
                m.d.comb += [
                    gen2_tx_skid.sink     .stream_eq(tx_skid.source),
                    # Keep the (unused) Gen1 scrambler fed with idle.
                    scrambler.enable      .eq(0),
                    scrambler.sink.valid  .eq(1),
                ]
            with m.Else():
                m.d.comb += [
                    scrambler.enable      .eq(enable_scrambling),
                    scrambler.sink        .stream_eq(
                        tx_skid.source, omit={'valid', 'data', 'ctrl'}),
                    scrambler.sink.valid  .eq(1),
                    scrambler.sink.data   .eq(Mux(tx_skid.source.valid,
                                                  tx_skid.source.data, 0)),
                    scrambler.sink.ctrl   .eq(Mux(tx_skid.source.valid,
                                                  tx_skid.source.ctrl, 0)),
                ]
        else:
            m.d.comb += [
                scrambler.enable      .eq(enable_scrambling),
                scrambler.sink        .stream_eq(tx_skid.source,
                                                 omit={'valid', 'data', 'ctrl'}),
                scrambler.sink.valid  .eq(1),
                scrambler.sink.data   .eq(Mux(tx_skid.source.valid,
                                              tx_skid.source.data, 0)),
                scrambler.sink.ctrl   .eq(Mux(tx_skid.source.valid,
                                              tx_skid.source.ctrl, 0)),
            ]

        # Debug tap (prunable): the conditioned transmit stream as consumed
        # from the skid stage -- post link layer, pre scrambler/SKP, i.e.
        # the descrambled wire-equivalent word stream.  Used by bring-up
        # wire checkers (open item #23 probes).
        m.d.comb += [
            self.debug_tx_data   .eq(tx_skid.source.data),
            self.debug_tx_ctrl   .eq(tx_skid.source.ctrl),
            self.debug_tx_strobe .eq(tx_skid.source.valid &
                                     tx_skid.source.ready),
        ]

        # Insert Clock Tolerance Compensation SKP ordered sets, where necessary.
        # SKPs may be placed wherever the *next word to transmit* starts a
        # packet (``first``, which the packet/link-command/training-set
        # generators mark, and which the link layer marks on logical idle) --
        # the inserter holds that word while the SKPs go out.  Computing this
        # from the post-skid stream keeps the qualifier aligned with the word
        # the inserter is actually looking at.
        m.submodules.tx_ctc = tx_ctc = CTCSkipInserter(words=self._words)
        m.d.comb += [
            tx_ctc.sink           .stream_eq(scrambler.source),
            tx_ctc.can_send_skip  .eq(tx_skid.source.valid &
                                      tx_skid.source.first),

            scrambler.hold        .eq(tx_ctc.sending_skip)
        ]

        # Register the electrical-idle gate: it is decoded combinationally
        # from the LTSSM state, and feeding it straight into the transmit
        # ready chain creates an ltssm -> everything critical path.  Idle
        # transitions are microsecond-scale; one cycle of latency is free.
        tx_electrical_idle = Signal(init=1)
        m.d.ss += tx_electrical_idle.eq(self.tx_electrical_idle)

        # Convert our Tx stream into PHY connections whenever we're not in electrical idle.
        if self._gen2:
            with m.If(~tx_electrical_idle):
                with m.If(rate_r):
                    m.d.comb += [
                        phy.tx_data          .eq(gen2_tx.tx_data),
                        phy.tx_datavalid     .eq(gen2_tx.tx_valid),
                        phy.tx_sync_header   .eq(gen2_tx.tx_head),
                        phy.tx_start_block   .eq(gen2_tx.tx_start),
                    ]
                    if self._words == 2:
                        m.d.comb += phy.tx_halfbeat.eq(gen2_tx.tx_halfbeat)
                with m.Else():
                    if self._words == 1:
                        m.d.comb += [
                            phy.tx_data          .eq(tx_ctc.source.data),
                            phy.tx_datak         .eq(tx_ctc.source.ctrl),
                            tx_ctc.source.ready  .eq(1),
                        ]
                    else:
                        m.d.comb += [
                            phy.tx_data[0:64]    .eq(tx_ctc.source.data),
                            phy.tx_datak[0:8]    .eq(tx_ctc.source.ctrl),
                            tx_ctc.source.ready  .eq(1),
                        ]
        else:
            with m.If(~tx_electrical_idle):
                m.d.comb += [
                    phy.tx_data          .eq(tx_ctc.source.data),
                    phy.tx_datak         .eq(tx_ctc.source.ctrl),
                    tx_ctc.source.ready  .eq(1),
                ]


        #
        # Receive input conditioning.
        #

        # Clock tolerance compensation / SKP remover.
        m.submodules.rx_ctc = rx_ctc = CTCSkipRemover(words=self._words)
        m.d.comb += [
            # Connect our PHY's receive data directly to our CTC hardware.
            # (words=2: the Gen1 leg rides the PIPE register's low half;
            # words=1 keeps the historical implicit-truncation assign
            # verbatim for the shipping parity fence.)
            rx_ctc.sink.data   .eq(phy.rx_data if self._words == 1
                                   else phy.rx_data[0:64]),
            rx_ctc.sink.ctrl   .eq(phy.rx_datak if self._words == 1
                                   else phy.rx_datak[0:8]),
            rx_ctc.sink.valid  .eq(1),

            # Diagnostic output.
            self.skip_removed         .eq(rx_ctc.skip_removed),
            self.ctc_bytes_in_buffer  .eq(rx_ctc.bytes_in_buffer),
        ]
        if self._gen2:
            # At the 10G trim the Gen1 RX chain is starved (the Gen2
            # block receiver owns the PIPE RX).
            m.d.comb += rx_ctc.sink.valid.eq(~rate_r)

        # Word align the data, so it's easily handleable internally.
        m.submodules.aligner = aligner = RxWordAligner(words=self._words)
        m.d.comb += [
            aligner.sink           .stream_eq(rx_ctc.source),
            self.raw_source        .tap(aligner.source),

            self.alignment_offset  .eq(aligner.alignment_offset)
        ]


        # De-scramble our data before output, if needed.
        m.submodules.descrambler = descrambler = Descrambler(words=self._words)
        m.d.comb += [
            descrambler.enable  .eq(enable_scrambling),
            descrambler.sink    .stream_eq(aligner.source),
        ]

        # Finally, as a requirement of strict compliance, we'll ensure we can handle packets
        # that arrive even without correct alignment.
        m.submodules.realigner = realigner = RxPacketAligner(words=self._words)
        if self._gen2:
            m.d.comb += realigner.sink.stream_eq(descrambler.source)
            # The muxed RX stream is REGISTERED at the physical->link
            # seam (156.25 routing: the gen2_rx output register
            # otherwise reaches every link-layer receiver cone --
            # crc16/crc32/lc_detector -- in a single hop).  The link
            # side holds ``source.ready`` tied high (monitor taps), so a
            # plain register is exact; both dialect legs are elastic and
            # the Gen1 leg at the 5G trim tolerates the extra cycle
            # identically.  Gen1-only builds keep the historical
            # combinational connection verbatim.
            src_valid = Signal()
            src_data  = Signal(32 * self._words)
            src_ctrl  = Signal(4 * self._words)
            with m.If(rate_r):
                m.d.ss += [src_valid.eq(gen2_rx.source.valid),
                           src_data .eq(gen2_rx.source.data),
                           src_ctrl .eq(gen2_rx.source.ctrl)]
                m.d.comb += gen2_rx.source.ready.eq(1)
            with m.Else():
                m.d.ss += [src_valid.eq(realigner.source.valid),
                           src_data .eq(realigner.source.data),
                           src_ctrl .eq(realigner.source.ctrl)]
                m.d.comb += realigner.source.ready.eq(1)
            m.d.comb += [
                self.source.valid.eq(src_valid),
                self.source.data .eq(src_data),
                self.source.ctrl .eq(src_ctrl),
            ]
        else:
            m.d.comb += [
                realigner.sink      .stream_eq(descrambler.source),
                self.source         .stream_eq(realigner.source),
            ]


        #
        # LFPS signaling.
        #

        # NB: ss_clk_freq historically defaulted to 125e6 regardless of
        # sync_frequency -- harmless while the ss domain always ran at
        # 125 MHz, wrong at the Gen2 operating point (156.25).  Passing
        # it through is elaboration-identical for the 125 MHz builds.
        m.submodules.lfps_transciever = lfps = LFPSTransceiver(
            ss_clk_freq=self._sync_frequency, scd_pattern=self._scd_pattern)
        m.d.comb += [
            lfps.send_polling           .eq(self.send_lfps_polling),
            self.lfps_cycles_sent       .eq(lfps.cycles_sent),

            self.lfps_ping_detected     .eq(lfps.ping_detected),
            self.lfps_polling_detected  .eq(lfps.polling_detected),
            lfps.scd2_select            .eq(self.scd2_select),
            lfps.scd_clear              .eq(self.scd_clear),
            lfps.scd_enable             .eq(self.scd_enable),
            self.scd1_detected          .eq(lfps.scd1_detected),
            self.scd2_detected          .eq(lfps.scd2_detected),
            self.lfps_burst_received    .eq(lfps.lfps_burst_received),
            lfps.lbpm_enable            .eq(self.lbpm_enable),
            lfps.lbpm_message           .eq(self.lbpm_message),
            self.lbpm_sent              .eq(lfps.lbpm_sent),
            self.lbpm_rx_message        .eq(lfps.lbpm_rx_message),
            self.lbpm_rx_valid          .eq(lfps.lbpm_rx_valid),
            self.lfps_reset_detected    .eq(lfps.reset_detected),

            # The RX_ELECIDLE signal being de-asserted indicates we're receiving valid
            # LFPS signaling. [TUSB1310A: Table 3-3]
            lfps.signaling_received     .eq(~phy.rx_elec_idle),
        ]

        if self._gen2:
            # Gen2 trims REGISTER the PIPE LFPS/idle control outputs: the
            # LTSSM's state decode otherwise reaches the adapter's LFPS
            # engine in one combinational sweep (LTSSM -> send_polling ->
            # generator merge -> this power_down mux -> adapter FSM), a
            # reported 156.25 seam cone.  Burst-edge granularity is
            # microseconds and both edges shift together, so one pclk of
            # latency is immaterial.  Gen1 elaborations keep the
            # historical combinational mux verbatim below.
            eidle_r = Signal(init=1)
            detrx_r = Signal()
            with m.Switch(phy.power_down):
                with m.Case(0):
                    m.d.ss += [
                        eidle_r.eq(lfps.drive_electrical_idle
                                   | self.tx_electrical_idle),
                        detrx_r.eq(lfps.send_signaling),
                    ]
                with m.Default():
                    m.d.ss += [
                        eidle_r.eq(1),
                        detrx_r.eq(rx_detect.detection_control),
                    ]
            m.d.comb += [
                phy.tx_elec_idle              .eq(eidle_r),
                phy.tx_detrx_lpbk             .eq(detrx_r),
            ]
            return m

        with m.Switch(phy.power_down):

            # In PO, we'll let the LTSSM control electrical idle, and pass through our signals
            # in a way that allows LTSSM.
            with m.Case(0):
                m.d.comb += [
                    # In P0, pass through TX_ELECIDLE directly, as it has its intended meaning.
                    phy.tx_elec_idle              .eq(lfps.drive_electrical_idle | self.tx_electrical_idle),

                    # In P0, the TX_DETRX_LPBK signal is used to drive an LFPS square wave onto the
                    # transmit line when we're in electrical idle, and places us into loopback
                    # otherwise. [TUSB1310A: Table 5-3]  Our LFPS generator takes care of this.
                    phy.tx_detrx_lpbk             .eq(lfps.send_signaling)
                ]

            # For now, we won't support LFPS from states other than P0, as our LTSSM only
            # performs it from P0. We'll use the PHY exclusively for receiver detection.
            with m.Default():
                m.d.comb += [
                    phy.tx_elec_idle              .eq(1),
                    phy.tx_detrx_lpbk             .eq(rx_detect.detection_control)
                ]

        return m
