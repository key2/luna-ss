#
# This file is part of LUNA.
#
# Copyright (c) 2020 Great Scott Gadgets <info@greatscottgadgets.com>
# SPDX-License-Identifier: BSD-3-Clause
"""
Contains the organizing hardware used to add USB3 Device functionality
to your own designs; including the core :class:`USBSuperSpeedDevice` class.
"""

import logging

from amaranth import *

from usb_protocol.emitters import DeviceDescriptorCollection

# USB3 Protocol Stack
from .physical             import USB3PhysicalLayer
from .link                 import USB3LinkLayer
from .protocol             import USB3ProtocolLayer
from .endpoints            import USB3ControlEndpoint
from .protocol.endpoint    import SuperSpeedEndpointMultiplexer

# Temporary
from ..stream              import USBRawSuperSpeedStream, SuperSpeedStreamInterface


class USBSuperSpeedDevice(Elaboratable):
    """ Core gateware common to all LUNA USB3 devices. """

    def __init__(self, *, phy, sync_frequency=None, gen2=False,
                 tseq_burst_length=65536, polling_timeout_scale=1.0):
        self._phy = phy
        self._sync_frequency = sync_frequency
        # Gen2 (SuperSpeedPlus) capability.  Session 11d onward, built
        # up mechanism by mechanism per doc/gen2_design.md; with the
        # default False the device elaborates exactly the proven Gen1
        # stack (the forced-Gen1 build knob of the fallback matrix).
        # Currently enabled: SCD1 declaration + SCD2 confirmation
        # [6.9.4], LBPM PortMatch/PortConfig rate negotiation with the
        # per-spec SS-operation fallbacks [6.9.5, 7.5.4.3-.6], and the
        # LTSSM-driven PHY rate handshake.
        self._gen2 = gen2
        # Simulation-only shortening knobs (threaded to the link layer /
        # LTSSM; the defaults are the spec values and are elaboration-
        # identical to the historical stack).
        self._tseq_burst_length = tseq_burst_length
        self._timeout_scale = polling_timeout_scale

        # Create a collection of endpoints for this device.
        self._endpoints = []

        #
        # I/O port
        #

        # General status signals.
        self.link_trained   = Signal()
        self.link_in_reset  = Signal()

        # Debug taps (physical-layer visibility for hardware bring-up).
        self.debug_phy_ready              = Signal()
        self.debug_send_lfps_polling      = Signal()
        self.debug_lfps_polling_detected  = Signal()
        self.debug_engage_terminations    = Signal()
        self.debug_ts1_detected           = Signal()
        self.debug_ts2_detected           = Signal()

        # Debug taps (control-transfer/handshake path visibility for the
        # SET_ADDRESS bring-up contract; prunable).
        self.debug_hsk_ack_dispatch       = Signal()  # generator accepted an ACK request
        self.debug_hsk_ep0_dispatch       = Signal()  # ...and it names endpoint 0
        self.debug_status_received        = Signal()  # STATUS TP broadcast to endpoints
        self.debug_address_changed        = Signal()  # SET_ADDRESS commit strobe
        self.debug_address_nonzero        = Signal()  # current device address != 0
        self.debug_hsk_pending0           = Signal()  # control iface demoted off fast path
        self.debug_tp_hdr_accepted        = Signal()  # TP generator header entered link queue
        self.debug_tp_hdr_valid           = Signal()  # TP generator holds a header (in SEND_x)
        self.debug_link_hdr_blocked       = Signal()  # link header queue offered but not ready
        self.debug_link_hdr_accepted      = Signal()  # link header queue consumed a header (any)
        self.debug_tx_credits_zero        = Signal()  # transmitter holds no link credits
        self.debug_recovery               = Signal()  # any recovery-required strobe
        self.debug_hsk_ready              = Signal()  # generator ready as seen by the mux
        self.debug_hsk_granted            = Signal()  # arbiter grant path active
        self.debug_hsk_grant_is0          = Signal()  # grant parked on the control iface
        self.debug_hsk_pass_is0           = Signal()  # fast path selecting the control iface
        self.debug_hsk_any_dispatch       = Signal()  # generator accepted any request kind
        self.debug_hsk_stall_dispatch     = Signal()  # ...specifically a STALL
        self.debug_hsk_bus                = Signal(16) # arbiter cycle-trace bus

        # Wire-level TX tap + RX ACK broadcast (open item #23 probes).
        self.debug_wire_tx_data           = Signal(32) # pre-scrambler TX word
        self.debug_wire_tx_ctrl           = Signal(4)
        self.debug_wire_tx_strobe         = Signal()   # word consumed this cycle
        self.debug_ack_received           = Signal()   # ACK TP broadcast strobe
        self.debug_payload_underrun       = Signal()   # transmitter consumed invalid payload
        self.debug_rx_dpp_invalid         = Signal()   # received DPP failed CRC-32
        self.debug_rx_hdr_bad             = Signal()   # received header failed CRC (LBAD path)
        # RX header field tap (bug-#34 ACK/DPH field probe): every header
        # the link layer delivers to -- and is accepted by -- the protocol
        # layer, with its type and raw DW1 (ACK TPs: nseq/rty/NumP; DPHs:
        # dseq/EOB/length).  Registered; strobe aligned with the fields.
        self.debug_rx_hdr_stb             = Signal()   # header accepted this cycle
        self.debug_rx_hdr_type            = Signal(5)  # dw0[0:5] of that header
        self.debug_rx_hdr_dw1             = Signal(32) # dw1 of that header
        # Debug hook: strobe to force one link recovery entry from U0
        # (hardware verdict path for the #29-#31 recovery-retransmit
        # fixes; see link.force_recovery).
        self.debug_force_recovery         = Signal()

        # Temporary, debug signals.
        self.rx_data_tap         = USBRawSuperSpeedStream()
        self.tx_data_tap         = USBRawSuperSpeedStream()

        self.ep_tx_stream        = SuperSpeedStreamInterface()
        self.ep_tx_length        = Signal(range(1024 + 1))


    def add_endpoint(self, endpoint):
        """ Adds an endpoint interface to the device.

        Parameters
        ----------
        endpoint: Elaborateable
            The endpoint interface to be added. Can be any piece of gateware with a
            :class:`EndpointInterface` attribute called ``interface``.
        """
        self._endpoints.append(endpoint)


    def add_standard_control_endpoint(self, descriptors: DeviceDescriptorCollection):
        """ Adds a control endpoint with standard request handlers to the device.

        Parameters
        ----------
        descriptors: DeviceDescriptorCollection
            The descriptors to use for this device.

        Return value
        ------------
        The endpoint object created.
        """

        # TODO: split out our standard request handlers

        control_endpoint = USB3ControlEndpoint()
        control_endpoint.add_standard_request_handlers(descriptors)
        self.add_endpoint(control_endpoint)

        return control_endpoint



    def elaborate(self, platform):
        m = Module()

        # Figure out the frequency of our ``sync`` domain, for e.g. PHY bringup timing.
        # We'll default to the platform's default frequency if none was provided.
        sync_frequency = self._sync_frequency
        if sync_frequency is None:
            sync_frequency = platform.default_clk_frequency

        #
        # Global device state.
        #

        # Stores the device's current address. Used to identify which packets are for us.
        address       = Signal(7, init=0)

        # Stores the device's current configuration. Defaults to unconfigured.
        configuration = Signal(8, init=0)


        #
        # Physical layer.
        #
        from .physical.lfps import SCD1_PATTERN
        m.submodules.physical = physical = USB3PhysicalLayer(
            phy            = self._phy,
            sync_frequency = sync_frequency,
            scd_pattern    = SCD1_PATTERN if self._gen2 else None,
            gen2           = self._gen2,
        )

        #
        # Link layer.
        #
        # NB: ss_clock_frequency historically defaulted to 125e6
        # regardless of sync_frequency -- harmless while ss ran at
        # 125 MHz (all shipping Gen1 tops pass 125e6), wrong for the
        # LTSSM/link timers at the 156.25 MHz Gen2 operating point.
        # Passing it through is elaboration-identical at 125 MHz.
        m.submodules.link = link = USB3LinkLayer(
            physical_layer=physical, gen2=self._gen2,
            ss_clock_frequency=sync_frequency,
            tseq_burst_length=self._tseq_burst_length,
            polling_timeout_scale=self._timeout_scale)
        m.d.comb += [
            self.link_trained     .eq(link.trained),
            self.link_in_reset    .eq(link.in_reset),

            link.current_address  .eq(address),

            # Debug taps.
            self.debug_phy_ready             .eq(physical.ready),
            self.debug_send_lfps_polling     .eq(physical.send_lfps_polling),
            self.debug_lfps_polling_detected .eq(physical.lfps_polling_detected),
            self.debug_engage_terminations   .eq(physical.engage_terminations),
            self.debug_ts1_detected          .eq(link.debug_ts1_detected),
            self.debug_ts2_detected          .eq(link.debug_ts2_detected),
            self.debug_wire_tx_data          .eq(physical.debug_tx_data),
            self.debug_wire_tx_ctrl          .eq(physical.debug_tx_ctrl),
            self.debug_wire_tx_strobe        .eq(physical.debug_tx_strobe),
            self.debug_payload_underrun      .eq(link.debug_payload_underrun),
            self.debug_rx_dpp_invalid        .eq(link.data_source_invalid),
            self.debug_rx_hdr_bad            .eq(link.debug_rx_bad_packet),
        ]

        # RX header field tap (bug-#34 probe): registered so the consumer
        # sees stable fields aligned with the strobe.
        m.d.ss += [
            self.debug_rx_hdr_stb .eq(link.header_source.valid
                                      & link.header_source.ready),
            self.debug_rx_hdr_type.eq(link.header_source.header.dw0[0:5]),
            self.debug_rx_hdr_dw1 .eq(link.header_source.header.dw1),
        ]
        m.d.comb += link.force_recovery.eq(self.debug_force_recovery)

        #
        # Protocol layer.
        #
        m.submodules.protocol = protocol = USB3ProtocolLayer(link_layer=link)
        m.d.comb += [
            protocol.current_address        .eq(address),
            protocol.current_configuration  .eq(configuration)
        ]


        #
        # Application layer.
        #

        # Create our endpoint multiplexer...
        m.submodules.endpoint_mux = endpoint_mux = SuperSpeedEndpointMultiplexer()
        endpoint_collection = endpoint_mux.shared

        m.d.comb += [
            # Receive interface.
            endpoint_collection.rx                          .tap(protocol.endpoint_interface.rx),
            endpoint_collection.rx_header                   .eq(protocol.endpoint_interface.rx_header),
            endpoint_collection.rx_complete                 .eq(protocol.endpoint_interface.rx_complete),
            endpoint_collection.rx_invalid                  .eq(protocol.endpoint_interface.rx_invalid),

            # Transmit interface.
            protocol.endpoint_interface.tx                  .stream_eq(endpoint_collection.tx),
            protocol.endpoint_interface.tx_zlp              .eq(endpoint_collection.tx_zlp),
            protocol.endpoint_interface.tx_length           .eq(endpoint_collection.tx_length),
            protocol.endpoint_interface.tx_endpoint_number  .eq(endpoint_collection.tx_endpoint_number),
            protocol.endpoint_interface.tx_sequence_number  .eq(endpoint_collection.tx_sequence_number),
            protocol.endpoint_interface.tx_direction        .eq(endpoint_collection.tx_direction),
            protocol.endpoint_interface.tx_eob              .eq(endpoint_collection.tx_eob),
            endpoint_collection.tx_parameters_consumed
                .eq(protocol.endpoint_interface.tx_parameters_consumed),

            # Link state: burst engines void their grants while the link
            # is out of U0 (see SuperSpeedEndpointInterface.link_reset).
            endpoint_collection.link_reset                  .eq(~link.trained),

            # Handshake interface.
            protocol.endpoint_interface.handshakes_out      .connect(endpoint_collection.handshakes_out),
            protocol.endpoint_interface.handshakes_in       .connect(endpoint_collection.handshakes_in)
        ]


        # Control-path debug taps (see __init__).  Registered: several of
        # these sample deep combinational cones (the shared handshake
        # strobes reach through the endpoint-mux arbitration from every
        # interface's parameters); observing them combinationally drags
        # that cone to wherever the consumer is placed and costs Fmax.
        # They are event/level probes -- one cycle of lag is immaterial.
        m.d.ss += [
            self.debug_hsk_ack_dispatch .eq(endpoint_collection.handshakes_out.send_ack &
                                            endpoint_collection.handshakes_out.ready),
            self.debug_hsk_ep0_dispatch .eq(endpoint_collection.handshakes_out.send_ack &
                                            endpoint_collection.handshakes_out.ready &
                                            (endpoint_collection.handshakes_out.endpoint_number == 0)),
            self.debug_status_received  .eq(endpoint_collection.handshakes_in.status_received),
            self.debug_ack_received     .eq(endpoint_collection.handshakes_in.ack_received),
            self.debug_address_changed  .eq(endpoint_collection.address_changed),
            self.debug_address_nonzero  .eq(address != 0),
            self.debug_hsk_pending0     .eq(endpoint_mux.debug_pending0_any),
            self.debug_tp_hdr_accepted  .eq(protocol.debug_tp_hdr_accepted),
            self.debug_tp_hdr_valid     .eq(protocol.debug_tp_hdr_valid),
            self.debug_link_hdr_blocked .eq(link.header_sink.valid &
                                            ~link.header_sink.ready),
            self.debug_link_hdr_accepted.eq(link.header_sink.valid &
                                            link.header_sink.ready),
            self.debug_tx_credits_zero  .eq(link.debug_tx_credits == 0),
            self.debug_recovery         .eq(link.debug_rec_timers |
                                            link.debug_rec_rx |
                                            link.debug_rec_tx),
            self.debug_hsk_ready        .eq(endpoint_collection.handshakes_out.ready),
            self.debug_hsk_granted      .eq(endpoint_mux.debug_granted),
            self.debug_hsk_grant_is0    .eq(endpoint_mux.debug_grant_is0),
            self.debug_hsk_pass_is0     .eq(endpoint_mux.debug_pass_is0),
            self.debug_hsk_any_dispatch .eq((endpoint_collection.handshakes_out.send_ack |
                                             endpoint_collection.handshakes_out.send_nrdy |
                                             endpoint_collection.handshakes_out.send_erdy |
                                             endpoint_collection.handshakes_out.send_stall) &
                                            endpoint_collection.handshakes_out.ready),
            self.debug_hsk_stall_dispatch.eq(endpoint_collection.handshakes_out.send_stall &
                                             endpoint_collection.handshakes_out.ready),
            self.debug_hsk_bus          .eq(endpoint_mux.debug_bus),
        ]

        # If an endpoint wants to update our address or configuration, accept the update.
        with m.If(endpoint_collection.address_changed):
            m.d.ss += address.eq(endpoint_collection.new_address)
        with m.If(endpoint_collection.config_changed):
            m.d.ss += configuration.eq(endpoint_collection.new_config)


        # Finally, add each of our endpoints to this module and our multiplexer.
        for endpoint in self._endpoints:

            # Create a display name for the endpoint...
            name = endpoint.__class__.__name__
            if hasattr(m.submodules, name):
                name = f"{name}_{id(endpoint)}"

            # ... and add it, both as a submodule and to our multiplexer.
            endpoint_mux.add_interface(endpoint.interface)
            m.submodules[name] = endpoint


        #
        # Reset handling.
        #

        # Restore ourselves to our unconfigured state when a reset occurs.
        with m.If(link.in_reset):
            m.d.ss += [
                address        .eq(0),
                configuration  .eq(0)
            ]


        #
        # Debug helpers.
        #

        # Tap our transmit and receive lines, so they can be externally analyzed.
        m.d.comb += [
            self.rx_data_tap   .tap(physical.source),
            self.tx_data_tap   .tap(physical.sink),

            self.ep_tx_stream  .tap(protocol.endpoint_interface.tx, tap_ready=True),
            self.ep_tx_length  .eq(protocol.endpoint_interface.tx_length)
        ]


        return m
