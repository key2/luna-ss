#
# This file is part of LUNA.
#
# Copyright (c) 2020 Great Scott Gadgets <info@greatscottgadgets.com>
# SPDX-License-Identifier: BSD-3-Clause
""" USB3 link-layer abstraction."""

from amaranth import *

from ....interface.pipe import TXDeemphMode
from ...stream          import USBRawSuperSpeedStream, SuperSpeedStreamArbiter, SuperSpeedStreamInterface
from ..physical.coding  import IDL

from .idle         import IdleHandshakeHandler
from .ltssm        import LTSSMController
from .header       import HeaderQueue, HeaderQueueArbiter
from .receiver     import HeaderPacketReceiver
from .transmitter  import PacketTransmitter
from ..physical.ctc import TxStreamSkidBuffer
from .timers       import LinkMaintenanceTimers
from .ordered_sets import TSTransceiver
from .data         import DataPacketReceiver, DataPacketTransmitter, DataHeaderPacket
from .compliance   import CompliancePatternEmitter


class USB3LinkLayer(Elaboratable):
    """ Abstraction encapsulating the USB3 link layer hardware.

    Performs the lower-level data manipulations associated with transporting USB3 packets
    from place to place.

    """

    def __init__(self, *, physical_layer, ss_clock_frequency=125e6,
                 tseq_burst_length=65536, gen2=False,
                 polling_timeout_scale=1.0,
                 ssp_capability=None, phy_boots_gen2=True):
        self._physical_layer    = physical_layer
        self._clock_frequency   = ss_clock_frequency
        self._tseq_burst_length = tseq_burst_length
        self._gen2              = gen2
        self._timeout_scale     = polling_timeout_scale
        # Advertised-highest capability + PHY boot rate: see
        # LTSSMController (defaults are elaboration-identical).
        self._ssp_capability    = ssp_capability
        self._phy_boots_gen2    = phy_boots_gen2

        #
        # I/O port
        #

        # Header packet exchanges.
        self.header_sink               = HeaderQueue()
        self.header_source             = HeaderQueue()

        # Data packet exchange interface.
        self.data_source               = SuperSpeedStreamInterface()
        self.data_header_from_host     = DataHeaderPacket()
        self.data_source_complete      = Signal()
        self.data_source_invalid       = Signal()

        self.data_sink                 = SuperSpeedStreamInterface()
        self.data_sink_send_zlp        = Signal()
        self.data_sink_sequence_number = Signal(5)
        self.data_sink_endpoint_number = Signal(4)
        self.data_sink_length          = Signal(range(1024 + 1))
        self.data_sink_direction       = Signal()
        self.data_sink_eob             = Signal()

        # Strobe: the parameters above were consumed for the packet whose
        # transmission is beginning (see DataPacketTransmitter -- used by
        # the endpoint multiplexer to release its parameter registers).
        self.data_sink_parameters_consumed = Signal()

        # Device state for header packets
        self.current_address           = Signal(7)

        # Status signals.
        self.trained                   = Signal()
        self.ready                     = Signal()
        self.in_reset                  = Signal()

        # Debug hook: strobe to force ONE link recovery entry from U0
        # (ORed into the LTSSM's recovery trigger).  Gives bench and
        # simulation a cycle-exact recovery entry: the recovery-
        # retransmit conformance fixes (#29-#31) are otherwise
        # unreachable on a bench whose link never leaves U0, and the
        # receiver's acked-but-undrained rule-2d window is only 1-2
        # cycles wide.
        self.force_recovery            = Signal()

        # Debug taps.
        self.debug_ts1_detected        = Signal()
        self.debug_ts2_detected        = Signal()
        self.debug_idle_handshake      = Signal()  # LTSSM in idle handshake
        self.debug_idle_complete       = Signal()  # handshake satisfied
        self.ltssm_in_training         = Signal()  # TS-exchange states

        # Recovery-cause debug taps (single-cycle strobes; prunable).
        self.debug_rec_timers          = Signal()
        self.debug_rec_rx              = Signal()
        self.debug_rec_tx              = Signal()
        self.debug_rx_bad_packet       = Signal()
        self.debug_tx_credits          = Signal(3)
        self.debug_tx_pending          = Signal(3)
        self.debug_rx_expected_seq     = Signal(3)
        self.debug_rx_seq              = Signal(3)
        self.debug_dtx_fsm             = Signal(2)
        self.debug_dsink_valid         = Signal()
        self.debug_dsink_ready         = Signal()
        self.debug_payload_underrun    = Signal()

        # Test and debug signals.
        self.disable_scrambling        = Signal()
        self.enable_compliance         = Signal()


    def elaborate(self, platform):
        m = Module()
        physical_layer = self._physical_layer

        # Mark ourselves as always consuming physical-layer packets.
        m.d.comb += physical_layer.source.ready.eq(1)

        #
        # Compliance pattern generation
        #
        m.submodules.compliance_emitter = compliance_emitter = CompliancePatternEmitter()

        #
        # Training Set Detectors/Emitters
        #
        training_set_source = USBRawSuperSpeedStream()

        m.submodules.ts = ts = TSTransceiver(
            tseq_burst_length=self._tseq_burst_length)

        # The training-set stream is decoupled through a registered skid:
        # the emitters' FSM state otherwise reaches through the transmit
        # arbiter into the U0 datapath ready cone.
        m.submodules.ts_skid = ts_skid = TxStreamSkidBuffer()
        m.d.comb += [
            # Note: we bring the physical layer's "raw" (non-descrambled) source to the TS detector,
            # as we'll still need to detect non-scrambled TS1s and TS2s if they arrive during normal
            # operation.
            ts.sink              .tap(physical_layer.raw_source),
            ts_skid.sink         .stream_eq(ts.source),
            training_set_source  .stream_eq(ts_skid.source)
        ]



        #
        # Idle handshake / logical idle detection.
        #
        m.submodules.idle = idle = IdleHandshakeHandler()
        m.d.comb += idle.sink.tap(physical_layer.source)


        #
        # U0 Maintenance Timers
        #
        m.submodules.timers = timers = LinkMaintenanceTimers(ss_clock_frequency=self._clock_frequency)


        #
        # Link Training and Status State Machine (LTSSM)
        #
        m.submodules.ltssm = ltssm = LTSSMController(
            ss_clock_frequency=self._clock_frequency, gen2=self._gen2,
            polling_timeout_scale=self._timeout_scale,
            ssp_capability=self._ssp_capability,
            phy_boots_gen2=self._phy_boots_gen2)

        # Distribute ``link_ready`` through a register: it is decoded
        # combinationally from the LTSSM state, and its fanout otherwise
        # reaches into U0 datapath enables all over the link layer.  U0
        # entry/exit tolerates a cycle trivially.
        link_ready = Signal()
        m.d.ss += link_ready.eq(ltssm.link_ready)

        send_tseq_burst_r = Signal()
        send_ts1_burst_r  = Signal()
        send_ts2_burst_r  = Signal()
        m.d.ss += [
            send_tseq_burst_r.eq(ltssm.send_tseq_burst),
            send_ts1_burst_r .eq(ltssm.send_ts1_burst),
            send_ts2_burst_r .eq(ltssm.send_ts2_burst),
        ]
        if self._gen2:
            # Registered like the burst requests: the Gen2 idle-mode OR
            # below mixes this with the (also 1-cycle-late)
            # ``link_ready`` register -- the historical COMB decode
            # dropped one cycle BEFORE link_ready rose at the
            # Polling.Idle/Recovery.Idle -> U0 transition, presenting a
            # deterministic 1-cycle idle_mode gap to the block
            # transmitter's ``active`` gate at EVERY U0 entry (the #45
            # request-seam hazard class; the transmitter is now also
            # drain-safe against any such blip, see physical/gen2.py +
            # test_gen2_tx_seams).  Gen1 elaborations do not create
            # this register (payload parity).
            perform_idle_r = Signal()
            m.d.ss += perform_idle_r.eq(ltssm.perform_idle_handshake)

        tx_deemph = Mux(compliance_emitter.disable_deemph,
                        TXDeemphMode.DEEMPH_NONE,
                        TXDeemphMode.DEEMPH_3P5DB)

        m.d.comb += [
            ltssm.phy_ready                      .eq(physical_layer.ready),

            # For now, we'll consider ourselves in USB reset iff we detect reset signaling.
            # This should be expanded; ideally to also consider e.g. loss of VBUS on some devices.
            ltssm.in_usb_reset                   .eq(physical_layer.lfps_reset_detected | ~physical_layer.vbus_present),

            # Link Partner Detection
            physical_layer.perform_rx_detection  .eq(ltssm.perform_rx_detection),
            ltssm.link_partner_detected          .eq(physical_layer.link_partner_detected),
            ltssm.no_link_partner_detected       .eq(physical_layer.no_link_partner_detected),

            # Pass down our link controls to the physical layer.
            physical_layer.tx_deemph             .eq(tx_deemph),
            physical_layer.tx_electrical_idle    .eq(ltssm.tx_electrical_idle),
            physical_layer.tx_ones_zeros         .eq(compliance_emitter.tx_ones_zeros),
            physical_layer.engage_terminations   .eq(ltssm.engage_terminations),
            physical_layer.invert_rx_polarity    .eq(ltssm.invert_rx_polarity),
            physical_layer.train_equalizer       .eq(ltssm.train_equalizer),

            # LFPS control.
            ltssm.lfps_polling_detected          .eq(physical_layer.lfps_polling_detected),
            physical_layer.send_lfps_polling     .eq(ltssm.send_lfps_polling | compliance_emitter.send_lfps_polling),
            ltssm.lfps_cycles_sent               .eq(physical_layer.lfps_cycles_sent),
        ]

        if not self._gen2:
            m.d.comb += [
                # Training set detectors
                ltssm.tseq_detected                  .eq(ts.tseq_detected),
                ltssm.ts1_detected                   .eq(ts.ts1_detected),
                ltssm.inverted_ts1_detected          .eq(ts.inverted_ts1_detected),
                self.debug_ts1_detected              .eq(ts.ts1_detected),
                self.debug_ts2_detected              .eq(ts.ts2_detected),
                ltssm.ts2_detected                   .eq(ts.ts2_detected),
                ltssm.hot_reset_requested            .eq(ts.hot_reset_requested),
                ltssm.loopback_requested             .eq(ts.loopback_requested),
                ltssm.no_scrambling_requested        .eq(ts.no_scrambling_requested),

                # Training set emitters (registered: these are decoded from the
                # LTSSM state, and the TS stream's valid otherwise carries the
                # LTSSM into the transmit arbiter's idle/ready cone; bursts are
                # millisecond-scale, so a cycle of latency is free).
                ts.send_tseq_burst                   .eq(send_tseq_burst_r),
                ts.send_ts1_burst                    .eq(send_ts1_burst_r),
                ts.send_ts2_burst                    .eq(send_ts2_burst_r),
                ts.request_hot_reset                 .eq(ltssm.request_hot_reset),
                ts.request_no_scrambling             .eq(ltssm.request_no_scrambling),
                ltssm.ts_burst_complete              .eq(ts.burst_complete),
            ]
        else:
            # Dual-rate ordered-set routing: at the 10G trim the Gen2
            # block-level generators/detectors own training; the Gen1
            # TSTransceiver is gated off (and vice versa).  Lane
            # polarity inversion is the PHY's at Gen2.
            op_gen2 = physical_layer.operating_gen2
            m.d.comb += [
                ltssm.tseq_detected.eq(Mux(
                    op_gen2, physical_layer.gen2_tseq_detected,
                    ts.tseq_detected)),
                ltssm.ts1_detected.eq(Mux(
                    op_gen2, physical_layer.gen2_ts1_detected,
                    ts.ts1_detected)),
                ltssm.inverted_ts1_detected
                    .eq(ts.inverted_ts1_detected & ~op_gen2),
                self.debug_ts1_detected.eq(ltssm.ts1_detected),
                self.debug_ts2_detected.eq(ltssm.ts2_detected),
                ltssm.ts2_detected.eq(Mux(
                    op_gen2, physical_layer.gen2_ts2_detected,
                    ts.ts2_detected)),
                ltssm.hot_reset_requested.eq(Mux(
                    op_gen2, physical_layer.gen2_hot_reset_requested,
                    ts.hot_reset_requested)),
                ltssm.loopback_requested.eq(Mux(
                    op_gen2, physical_layer.gen2_loopback_requested,
                    ts.loopback_requested)),
                ltssm.no_scrambling_requested.eq(Mux(
                    op_gen2, physical_layer.gen2_no_scrambling_requested,
                    ts.no_scrambling_requested)),

                ts.send_tseq_burst      .eq(send_tseq_burst_r & ~op_gen2),
                ts.send_ts1_burst       .eq(send_ts1_burst_r & ~op_gen2),
                ts.send_ts2_burst       .eq(send_ts2_burst_r & ~op_gen2),
                ts.request_hot_reset    .eq(ltssm.request_hot_reset),
                ts.request_no_scrambling.eq(ltssm.request_no_scrambling),
                ltssm.ts_burst_complete.eq(Mux(
                    op_gen2, physical_layer.gen2_burst_complete,
                    ts.burst_complete)),

                physical_layer.gen2_send_tseq_burst
                    .eq(send_tseq_burst_r & op_gen2),
                physical_layer.gen2_send_ts1_burst
                    .eq(send_ts1_burst_r & op_gen2),
                physical_layer.gen2_send_ts2_burst
                    .eq(send_ts2_burst_r & op_gen2),
                physical_layer.gen2_idle_mode
                    .eq((perform_idle_r | link_ready) & op_gen2),
                physical_layer.gen2_request_hot_reset
                    .eq(ltssm.request_hot_reset),
                physical_layer.gen2_request_no_scrambling
                    .eq(ltssm.request_no_scrambling),
            ]

        m.d.comb += [

            # Scrambling control.
            physical_layer.enable_scrambling     .eq(ltssm.enable_scrambling),

            # Idle detection.
            idle.enable                          .eq(ltssm.perform_idle_handshake),
            ltssm.idle_handshake_complete        .eq(idle.idle_handshake_complete),
            self.debug_idle_handshake            .eq(ltssm.perform_idle_handshake),
            self.debug_idle_complete             .eq(idle.idle_handshake_complete),
            self.ltssm_in_training               .eq(ltssm.in_training),

            # Link maintainance.
            timers.enable                        .eq(link_ready),

            # Status signaling.
            self.trained                         .eq(link_ready),
            self.in_reset                        .eq(ltssm.request_hot_reset | ltssm.in_usb_reset),

            # Test and debug.
            ltssm.disable_scrambling             .eq(self.disable_scrambling),
            ltssm.enable_compliance_scrambling   .eq(compliance_emitter.enable_scrambling),
            compliance_emitter.enable            .eq(ltssm.emit_compliance_pattern),
            compliance_emitter.lfps_ping_detected.eq(physical_layer.lfps_ping_detected),
        ]


        #
        # Packet transmission path.
        # Accepts packets from the protocol and link layers, and transmits them.
        #

        # Transmit header multiplexer.
        m.submodules.hp_mux = hp_mux = HeaderQueueArbiter()
        hp_mux.add_producer(self.header_sink)

        # Track how the current period in U0 was entered: entry from
        # Recovery preserves the transmit-side header state (the coming
        # Header Sequence Number Advertisement decides what is flushed
        # vs retransmitted); entry from Polling or Hot Reset flushes
        # everything [USB3.2r1: 7.2.4.1.x rule 7].
        u0_from_recovery = Signal()
        with m.If(ltssm.entering_u0):
            m.d.ss += u0_from_recovery.eq(ltssm.entering_u0_from_recovery)

        # Core transmitter.
        m.submodules.transmitter = transmitter = PacketTransmitter(
            ss_clock_frequency=self._clock_frequency, gen2=self._gen2)
        if self._gen2:
            m.d.comb += transmitter.gen2_active \
                .eq(physical_layer.operating_gen2)
        m.d.comb += [
            transmitter.sink                .tap(physical_layer.source),
            transmitter.enable              .eq(link_ready),
            transmitter.usb_reset           .eq(self.in_reset),
            transmitter.from_recovery       .eq(u0_from_recovery),

            transmitter.queue               .header_eq(hp_mux.source),

            # Link state management handling.
            timers.link_command_received  .eq(transmitter.link_command_received),
            self.ready                    .eq(transmitter.bringup_complete),
        ]



        #
        # Header Packet Rx Path.
        # Receives header packets and forwards them up to the protocol layer.
        #
        # Gen2 builds carry 8 Rx header buffers: a port entering U0 from
        # Polling at Gen 2x1 SHALL advertise 4 Type-1 + 4 Type-2 Rx
        # Buffer Credits [USB3.2r1 7.2.4.1.1 rules 2.e.1 + 3.d], and
        # every advertised credit needs a physical buffer behind it.  A
        # shorter advertisement leaves the link partner's Type 1/Type 2
        # CREDIT_HP_TIMERs armed (they only clear at count 4), whose
        # timeout forces Recovery [7.3.9] -- bug #42: a real xHC then
        # never transmits a single header packet and walks the link
        # down.  Gen1 builds keep the historical 4-buffer pool verbatim.
        m.submodules.header_rx = header_rx = HeaderPacketReceiver(
            gen2=self._gen2, buffer_count=8 if self._gen2 else 4)
        if self._gen2:
            m.d.comb += header_rx.gen2_active \
                .eq(physical_layer.operating_gen2)
        m.d.comb += [
            header_rx.sink                   .tap(physical_layer.source),
            header_rx.enable                 .eq(link_ready),
            header_rx.usb_reset              .eq(self.in_reset),

            # Bring our header packet interface to the protocol layer.
            self.header_source               .header_eq(header_rx.queue),

            # Keepalive handling.
            timers.link_command_transmitted  .eq(header_rx.source.valid),
            header_rx.keepalive_required     .eq(timers.schedule_keepalive),
            timers.packet_received           .eq(header_rx.packet_received),

            # Transmitter event path.
            header_rx.retry_required         .eq(transmitter.retry_required),
            transmitter.lrty_pending         .eq(header_rx.lrty_pending),
            header_rx.retry_received         .eq(transmitter.retry_received),

            # For now, we'll reject all forms of power management by sending a REJECT
            # whenever we receive an LGO (Link Go-to) request.
            header_rx.reject_power_state     .eq(transmitter.lgo_received),
        ]


        #
        # Link Recovery Control
        #
        m.d.comb += ltssm.trigger_link_recovery.eq(
            timers.transition_to_recovery |
            header_rx.recovery_required   |
            transmitter.recovery_required |
            self.force_recovery
        )

        # Debug taps for the individual recovery causes.
        m.d.comb += [
            self.debug_rec_timers    .eq(timers.transition_to_recovery),
            self.debug_rec_rx        .eq(header_rx.recovery_required),
            self.debug_rec_tx        .eq(transmitter.recovery_required),
            self.debug_rx_bad_packet .eq(header_rx.bad_packet_received),
            self.debug_tx_credits    .eq(transmitter.credits_available),
            self.debug_tx_pending    .eq(transmitter.packets_to_send),
            self.debug_rx_expected_seq .eq(header_rx.debug_expected_seq),
            self.debug_rx_seq          .eq(header_rx.debug_rx_seq),
        ]


        #
        # Data packet handlers.
        #

        # Receiver.
        m.submodules.data_rx = data_rx = DataPacketReceiver(gen2=self._gen2)

        # The received payload stream is registered before it fans out to
        # the endpoints: its per-lane valids are decoded combinationally
        # from the physical-layer stream (byte-count comparisons), and that
        # cone otherwise stretches into every endpoint's capture logic.
        # The completion strobes are delayed identically, preserving their
        # ordering against the payload.
        rx_data_q     = Signal.like(data_rx.source.data)
        rx_valid_q    = Signal.like(data_rx.source.valid)
        rx_first_q    = Signal()
        rx_last_q     = Signal()
        rx_good_q     = Signal()
        rx_bad_q      = Signal()
        m.d.ss += [
            rx_data_q   .eq(data_rx.source.data),
            rx_valid_q  .eq(data_rx.source.valid),
            rx_first_q  .eq(data_rx.source.first),
            rx_last_q   .eq(data_rx.source.last),
            rx_good_q   .eq(data_rx.packet_good),
            rx_bad_q    .eq(data_rx.packet_bad),
        ]

        m.d.comb += [
            data_rx.sink                .tap(physical_layer.source),

            # Data interface to Protocol layer.
            self.data_source.data       .eq(rx_data_q),
            self.data_source.valid      .eq(rx_valid_q),
            self.data_source.first      .eq(rx_first_q),
            self.data_source.last       .eq(rx_last_q),
            self.data_header_from_host  .eq(data_rx.header),
            self.data_source_complete   .eq(rx_good_q),
            self.data_source_invalid    .eq(rx_bad_q),
        ]

        # Transmitter.
        m.submodules.data_tx = data_tx = DataPacketTransmitter()
        hp_mux.add_producer(data_tx.header_source)

        m.d.comb += [
            transmitter.data_sink    .stream_eq(data_tx.data_source),

            # Device state information.
            data_tx.address          .eq(self.current_address),

            # Data interface from Protocol layer.
            data_tx.data_sink        .stream_eq(self.data_sink),
            data_tx.send_zlp         .eq(self.data_sink_send_zlp),
            data_tx.sequence_number  .eq(self.data_sink_sequence_number),
            data_tx.endpoint_number  .eq(self.data_sink_endpoint_number),
            data_tx.data_length      .eq(self.data_sink_length),
            data_tx.direction        .eq(self.data_sink_direction),
            data_tx.end_of_burst     .eq(self.data_sink_eob),

            self.data_sink_parameters_consumed
                                     .eq(data_tx.parameters_consumed),
        ]
        m.d.comb += [
            self.debug_dtx_fsm         .eq(data_tx.debug_fsm),
            self.debug_dsink_valid     .eq(transmitter.data_sink.valid.any()),
            self.debug_dsink_ready     .eq(transmitter.data_sink.ready),
            self.debug_payload_underrun.eq(transmitter.debug_payload_underrun),
        ]


        #
        # Transmit stream arbiter.
        #
        m.submodules.stream_arbiter = arbiter = SuperSpeedStreamArbiter()

        # Add each of our streams to our arbiter, from highest to lowest priority.
        arbiter.add_stream(compliance_emitter.source)
        arbiter.add_stream(training_set_source)
        arbiter.add_stream(header_rx.source)
        arbiter.add_stream(transmitter.source)

        # If we're idle, send logical idle.
        with m.If(arbiter.idle):
            m.d.comb += [
                # Drive our idle stream with our IDL value (0x00)...
                physical_layer.sink.valid    .eq(1),
                physical_layer.sink.data     .eq(IDL.value),
                physical_layer.sink.ctrl     .eq(IDL.ctrl),

                # Logical idle words are always a safe place for the CTC
                # inserter to place SKP ordered sets; mark them as packet
                # boundaries.  (The physical layer derives its insertion
                # qualifier from the stream's ``first`` markers.)
                physical_layer.sink.first    .eq(1),

                # Legacy qualifier; informational.
                physical_layer.can_send_skp  .eq(1)
            ]

        # Otherwise, output our stream data.
        with m.Else():
            m.d.comb += physical_layer.sink.stream_eq(arbiter.source)

            # SKP ordered sets are also required during training bursts
            # [USB 3.2r1: 6.4.3.1] -- without them, the link partner's
            # elastic buffer under/overruns during our multi-millisecond
            # TSEQ/TS1/TS2 bursts (+-300ppm and SSC accumulate) and it
            # never recognizes our training sets.  They are equally
            # required under saturated U0 traffic, where back-to-back
            # packets and link commands leave no idle cycles.  The packet
            # transmitter, link-command generator and training-set
            # emitters all mark the first word of everything they send;
            # the physical layer's inserter holds a marked word and
            # transmits the pending SKPs first, so they land cleanly
            # between packets.
            m.d.comb += physical_layer.can_send_skp.eq(
                arbiter.source.valid & arbiter.source.first)



        if self._gen2:
            # SuperSpeedPlus negotiation surface: exists only on gen2
            # physical layers (the Gen1 sims drive this layer with
            # reduced stubs, so keep this gated).
            m.d.comb += [
                ltssm.scd1_detected        .eq(physical_layer.scd1_detected),
                ltssm.scd2_detected        .eq(physical_layer.scd2_detected),
                physical_layer.scd2_select .eq(ltssm.scd2_select),
                physical_layer.scd_clear   .eq(ltssm.scd_clear),
                physical_layer.scd_enable  .eq(ltssm.scd_enable),
                ltssm.lfps_burst_received  .eq(physical_layer.lfps_burst_received),

                # LBPM modem (Polling.PortMatch / PortConfig).
                physical_layer.lbpm_enable .eq(ltssm.lbpm_enable),
                physical_layer.lbpm_message.eq(ltssm.lbpm_message),
                ltssm.lbpm_sent            .eq(physical_layer.lbpm_sent),
                ltssm.lbpm_rx_message      .eq(physical_layer.lbpm_rx_message),
                ltssm.lbpm_rx_valid        .eq(physical_layer.lbpm_rx_valid),

                # LTSSM-driven PHY rate handshake.
                physical_layer.rate_select .eq(ltssm.rate_select),
                physical_layer.rate_request.eq(ltssm.rate_request),
                ltssm.rate_done            .eq(physical_layer.rate_done),
            ]

        return m
