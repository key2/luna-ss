#
# This file is part of LUNA.
#
# Copyright (c) 2020 Great Scott Gadgets <info@greatscottgadgets.com>
# SPDX-License-Identifier: BSD-3-Clause
""" Link Management Packet (LMP) -related gateware. """

from amaranth import *
from usb_protocol.types.superspeed import HeaderPacketType, LinkManagementPacketSubtype

from ..link.header import HeaderQueue, HeaderPacket


class PortCapabilityHeaderPacket(HeaderPacket):
    DW0_LAYOUT = [
        ('type',        5),
        ('subtype',     4),
        ('link_speed',  7),
        ('reserved',   16)
    ]
    DW1_LAYOUT = [
        ('num_hp_buffers',      8),
        ('reserved_0',          8),
        ('supports_downstream', 1),
        ('supports_upstream',   1),
        ('reserved_1',          2),
        ('tiebreaker',          4),
        ('reserved_2',          8),
    ]


class PortConfigurationHeaderPacket(HeaderPacket):
    DW0_LAYOUT = [
        ('type',        5),
        ('subtype',     4),
        ('link_speed',  7),
        ('reserved',   16)
    ]


class PortConfigurationResponseHeaderPacket(HeaderPacket):
    DW0_LAYOUT = [
        ('type',           5),
        ('subtype',        4),
        ('response_code',  7),
        ('reserved',      16)
    ]




class LinkManagementPacketHandler(Elaboratable):
    """ Gateware that handles Link Management Packets.

    Attributes
    -----------
    header_sink: HeaderQueue(), input stream
        Stream that brings up header packets for handling.
    header_source: HeaderQueue(), output stream
        Stream that accepts header packets for generation.

    link_ready: Signal(), input
        Should be asserted once our link is ready; used to trigger advertising.
    """

    # Link speed constants.
    LINK_SPEED_5GBPS = 1

    # Constants.
    CONFIGURATION_ACCEPTED = 1
    CONFIGURATION_REJECTED = 2

    def __init__(self, *, gen2=False):
        self._gen2 = gen2

        #
        # I/O port
        #
        self.header_sink   = HeaderQueue()
        self.header_source = HeaderQueue()

        # Status / control.
        self.usb_reset     = Signal()
        self.link_ready    = Signal()

        # SSP-operation qualifier (gen2 builds; bug #41): asserted when
        # the negotiated configuration is anything OTHER than Gen 1x1
        # (Gen 2x1 today; Gen 1x2 / Gen 2x2 OR in here when they land).
        # The Gen 1x1-only LMP fields -- Port Capability link_speed /
        # num_hp_buffers, Port Configuration link_speed, and the Port
        # Configuration Response code -- are all RESERVED and "shall be
        # set to zero" when not operating at Gen 1x1 [USB3.2r1 8.4.5-
        # 8.4.7, Tables 8-7/8-9/8-10].  The historical behavior
        # (advertise 5GBPS/4-buffers, accept only link_speed == 5GBPS,
        # answer ACCEPTED/REJECTED) misreads a conformant SSP host's
        # link_speed=0 Port Configuration as a foreign speed and answers
        # response_code=2 -- which the DFP reads as "Link Speed
        # rejected" and signals a port error [10.16.2.6]: the U0 link
        # walk-down observed on Gen2 silicon (HANDOVER 10s phase H2).
        self.ssp_operating = Signal()


    def elaborate(self, platform):
        m = Module()

        header_sink   = self.header_sink
        header_source = self.header_source


        #
        # Pending "tasks" for our transmitter.
        #
        pending_configuration_result = Signal(2)

        # gen2 builds track "a response is owed" separately from the
        # result code: at SSP operation the code sent on the wire is
        # reserved-0, which can no longer double as the pending flag.
        if self._gen2:
            pending_response = Signal()


        #
        # LMP transmitter.
        #

        def send_packet_response(response_type, **fields):
            """ Helper that allows us to easily define a packet-send state."""

            # Create a response packet, and mark ourselves as sending it.
            response = response_type()
            m.d.comb += [
                header_source.valid    .eq(1),
                header_source.header   .eq(response),

                response.type          .eq(HeaderPacketType.LINK_MANAGEMENT)
            ]

            # Next, fill in each of the fields:
            for field, value in fields.items():
                m.d.comb += response[field].eq(value)


        def handle_resets():
            """ Helper that brings down the link on USB reset. """
            with m.If(self.usb_reset):
                m.next = "LINK_DOWN"


        with m.FSM(domain="ss"):

            # LINK_DOWN -- our link is not yet ready to exchange packets; we'll wait until
            # it's come up to the point where we can exchange header packets.
            with m.State("LINK_DOWN"):

                # Once our link is ready, we're ready to start link bringup.
                with m.If(self.link_ready):
                    m.next = "SEND_CAPABILITIES"
                with m.Else():
                    m.d.ss += pending_configuration_result.eq(0)
                    if self._gen2:
                        m.d.ss += pending_response.eq(0)


            # SEND_CAPABILITIES -- our link has come up; and we're now ready to advertise our link
            # capabilities to the other side of our link [USB3.2r1: 8.4.5].
            with m.State("SEND_CAPABILITIES"):
                handle_resets()

                if self._gen2:
                    # SSP field rules [Table 8-7]: link_speed and
                    # num_hp_buffers are reserved-0 when not operating
                    # at Gen 1x1 (bug #41).
                    send_packet_response(PortCapabilityHeaderPacket,
                        subtype           = LinkManagementPacketSubtype.PORT_CAPABILITY,
                        link_speed        = Mux(self.ssp_operating,
                                                0, self.LINK_SPEED_5GBPS),
                        num_hp_buffers    = Mux(self.ssp_operating, 0, 4),
                        supports_upstream = 1
                    )
                else:
                    send_packet_response(PortCapabilityHeaderPacket,
                        subtype           = LinkManagementPacketSubtype.PORT_CAPABILITY,
                        link_speed        = self.LINK_SPEED_5GBPS,

                        # We're required by specification to support exactly four buffers.
                        num_hp_buffers    = 4,

                        # For now, we only can operate as an upstream device.
                        supports_upstream = 1
                    )

                # Continue to drive our packet until it's accepted by the link layer.
                with m.If(header_source.ready):
                    m.next = "DISPATCH_COMMANDS"


            # DISPATCH_COMMANDS -- we'll wait for a command to be queued, and then send it.
            with m.State("DISPATCH_COMMANDS"):
                handle_resets()

                # If we have a pending configuration result, send it!
                if self._gen2:
                    with m.If(pending_response):
                        m.next = "SEND_PORT_CONFIGURATION_RESPONSE"
                else:
                    with m.If(pending_configuration_result):
                        m.next = "SEND_PORT_CONFIGURATION_RESPONSE"


            # SEND_CONFIGURATION_RESPONSE -- we're sending a Port Configuration Response,
            # typically as a result of receiving a Port Configuration Request packet.
            with m.State("SEND_PORT_CONFIGURATION_RESPONSE"):
                handle_resets()

                if self._gen2:
                    # SSP field rules [Table 8-10]: the Response Code is
                    # reserved-0 when not operating at Gen 1x1; a nonzero
                    # code reads as "Link Speed rejected" at the DFP,
                    # which then signals a port error [10.16.2.6].
                    send_packet_response(PortConfigurationResponseHeaderPacket,
                        subtype       = LinkManagementPacketSubtype.PORT_CONFIGURATION_RESPONSE,
                        response_code = Mux(self.ssp_operating,
                                            0, pending_configuration_result)
                    )
                else:
                    send_packet_response(PortConfigurationResponseHeaderPacket,
                        subtype       = LinkManagementPacketSubtype.PORT_CONFIGURATION_RESPONSE,
                        response_code = pending_configuration_result
                    )

                # Continue to drive our packet until it's accepted by the link layer.
                with m.If(header_source.ready):
                    m.d.ss += pending_configuration_result.eq(0)
                    if self._gen2:
                        m.d.ss += pending_response.eq(0)
                    m.next = "DISPATCH_COMMANDS"


        #
        # LMP receiver.
        #

        # We'll handle all link management packets.
        new_packet = header_sink.valid
        is_for_us  = header_sink.get_type() == HeaderPacketType.LINK_MANAGEMENT

        with m.If(new_packet & is_for_us):

            # Accept the packet from the physical layer, so its buffer will be freed
            # on the next clock cycle.
            m.d.comb += header_sink.ready.eq(1)

            # We'll handle link management packets based on their subtype.
            subtype = header_sink.header.dw0[5:9]
            with m.Switch(subtype):

                # As an upstream-only Gen1 port, there's not much we need to do with
                # capability advertisements. For now, we'll mostly ignore them.
                with m.Case(LinkManagementPacketSubtype.PORT_CAPABILITY):
                    pass

                # If we receive a PORT_CONFIGURATION request, then our host is assigning
                # us a configuration.
                with m.Case(LinkManagementPacketSubtype.PORT_CONFIGURATION):
                    configuration = PortConfigurationHeaderPacket()
                    m.d.comb += configuration.eq(header_sink.header)

                    if self._gen2:
                        # A response is owed either way [8.4.7].  At SSP
                        # operation the link_speed field is reserved-0
                        # [Table 8-9] and carries no decision; at Gen 1x1
                        # operation the historical accept/reject applies.
                        m.d.ss += pending_response.eq(1)

                    # For now, we only support Gen1 / 5Gbps, so we'll accept only links
                    # with that speed selected.
                    with m.If(configuration.link_speed == self.LINK_SPEED_5GBPS):
                        m.d.ss += pending_configuration_result.eq(self.CONFIGURATION_ACCEPTED)
                    with m.Else():
                        m.d.ss += pending_configuration_result.eq(self.CONFIGURATION_REJECTED)


                # TODO: handle any invalid packet types?
                with m.Default():
                    pass

        return m
