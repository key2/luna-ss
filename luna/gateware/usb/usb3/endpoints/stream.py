#
# This file is part of LUNA.
#
# Copyright (c) 2020 Great Scott Gadgets <info@greatscottgadgets.com>
# SPDX-License-Identifier: BSD-3-Clause

""" Endpoint interfaces for working with streams.

The endpoint interfaces in this module provide endpoint interfaces suitable for
connecting streams to USB endpoints.
"""

from amaranth import *
from amaranth.lib.memory import Memory
from usb_protocol.types import USBDirection

from ...stream                import SuperSpeedStreamInterface
from ..protocol.endpoint      import SuperSpeedEndpointInterface


class SuperSpeedStreamInEndpoint(Elaboratable):
    """ Endpoint interface that transmits a simple data stream to a host.

    This interface is suitable for a single bulk or interrupt endpoint.

    This endpoint interface will automatically generate ZLPs when a stream packet would end without
    a short data packet. If the stream's ``last`` signal is tied to zero, then a continuous stream of
    maximum-length-packets will be sent with no inserted ZLPs.

    This implementation is double buffered; and can store a single packet's worth of data while transmitting
    a second packet. Bursting is currently not supported.


    Attributes
    ----------
    stream: SuperSpeedStreamInterface, input stream
        Full-featured stream interface that carries the data we'll transmit to the host.
    interface: SuperSpeedEndpointInterface
        Communications link to our USB device.


    Parameters
    ----------
    endpoint_number: int
        The endpoint number (not address) this endpoint should respond to.
    max_packet_size: int
        The maximum packet size for this endpoint. Should match the wMaxPacketSize provided in the
        USB endpoint descriptor.
    """

    SEQUENCE_NUMBER_BITS = 5


    def __init__(self, *, endpoint_number, max_packet_size=1024, generate_zlps=True,
                 max_burst=1):
        self._endpoint_number = endpoint_number
        self._max_packet_size = max_packet_size
        self._generate_zlps   = generate_zlps

        # Burst depth: the maximum number of packets that may be in
        # flight (sent, unacknowledged) at once -- the endpoint
        # descriptor's SuperSpeed companion should advertise
        # ``bMaxBurst = max_burst - 1``.  With the default of 1 the
        # historical single-packet engine is used, unchanged; larger
        # values elaborate the burst engine, which sends up to NumP
        # packets per IN token back-to-back (per-packet sequence
        # advance, cumulative acknowledgements, EOB signalling, and
        # rewind-on-retry).  ZLP generation is not supported by the
        # burst engine.
        self._max_burst = max_burst
        if max_burst > 1 and generate_zlps:
            raise ValueError("burst mode does not support ZLP generation; "
                             "use generate_zlps=False")

        # Debug taps (bring-up visibility; cheap, prunable by synthesis).
        self.debug_write_fill = Signal(11)
        self.debug_read_fill  = Signal(11)
        self.debug_pingpong   = Signal()
        self.debug_ready      = Signal()
        self.debug_fsm        = Signal(4)
        self.debug_erdyreq    = Signal()
        # Retransmission-cause taps (open item #23 probes): strobed when
        # WAIT_FOR_ACK services an acknowledgement that triggers a resend,
        # split by cause.
        self.debug_retry_flagged = Signal()   # host set the retry bit
        self.debug_stale_ack     = Signal()   # non-advancing, retry bit clear

        #
        # I/O port
        #
        self.stream    = SuperSpeedStreamInterface()
        self.interface = SuperSpeedEndpointInterface()


    def elaborate(self, platform):
        if self._max_burst > 1:
            return self._elaborate_burst(platform)

        m = Module()

        interface      = self.interface
        handshakes_in  = interface.handshakes_in
        handshakes_out = interface.handshakes_out

        # Parameters for later use.
        data_width     = len(self.stream.data)
        bytes_per_word = data_width // 8
        buffer_depth   = self._max_packet_size // bytes_per_word

        #
        # Transciever sequencing.
        #

        # Keep track of the sequence number used as we're transmitting.
        sequence_number = Signal(self.SEQUENCE_NUMBER_BITS)

        # Create a signal equal to the next sequence number; for easy comparisons.
        next_sequence_number = Signal.like(sequence_number)
        m.d.comb += next_sequence_number.eq(sequence_number + 1)

        # Advance the sequence number after transmission, or reset it when the endpoint is reset.
        advance_sequence = Signal()
        with m.If(interface.ep_reset):
            m.d.ss += sequence_number.eq(0)
        with m.Elif(advance_sequence):
            m.d.ss += sequence_number.eq(next_sequence_number)


        #
        # Transmit buffer.
        #
        # Our USB connection imposed a few requirements on our stream:
        # 1) we must be able to transmit packets at a full rate; i.e. ```valid``
        #    must be asserted from the start to the end of our transfer; and
        # 2) we must be able to re-transmit data if a given packet is not ACK'd.
        #
        # Accordingly, we'll buffer a full USB packet of data, and then transmit
        # it once either a) our buffer is full, or 2) the transfer ends (last=1).
        #
        # This implementation is double buffered; so a buffer fill can be pipelined
        # with a transmit.
        #
        ping_pong_toggle = Signal()

        # We'll create two buffers; so we can fill one as we empty the other.
        # Since each buffer will be used for every other transaction, we'll use a simple flag to identify
        # which of our "ping-pong" buffers is currently being targeted.
        buffer = Array(Memory(shape=data_width, depth=buffer_depth, init=[]) for _ in range(2))
        buffer_write_ports = Array(buffer[i].write_port(domain="ss") for i in range(2))
        buffer_read_ports  = Array(buffer[i].read_port(domain="ss") for i in range(2))

        m.submodules.transmit_buffer_0, m.submodules.transmit_buffer_1 = buffer

        # Create values equivalent to the buffer numbers for our read and write buffer; which switch
        # whenever we swap our two buffers.
        write_buffer_number =  ping_pong_toggle
        read_buffer_number  = ~ping_pong_toggle

        # Create a shorthand that refers to the buffer to be filled; and the buffer to send from.
        # We'll call these the Read and Write buffers.
        buffer_write = buffer_write_ports[write_buffer_number]
        buffer_read  = buffer_read_ports[read_buffer_number]

        # Buffer state tracking:
        # - Our ``fill_count`` keeps track of how much data is stored in a given buffer.
        # - Our ``stream_ended`` bit keeps track of whether the stream ended while filling up
        #   the given buffer. This indicates that the buffer cannot be filled further; and, when
        #   ``generate_zlps`` is enabled, is used to determine if the given buffer should end in
        #   a short packet; which determines whether ZLPs are emitted.
        buffer_fill_count   = Array(Signal(range(0, self._max_packet_size + 1)) for _ in range(2))
        buffer_stream_ended = Array(Signal(name=f"stream_ended_in_buffer{i}") for i in range(2))

        # Create shortcuts to active fill_count / stream_ended signals for the buffer being written.
        write_fill_count   = buffer_fill_count[write_buffer_number]
        write_stream_ended = buffer_stream_ended[write_buffer_number]

        # Create shortcuts to the fill_count / stream_ended signals for the packet being sent.
        read_fill_count   = buffer_fill_count[read_buffer_number]
        read_stream_ended = buffer_stream_ended[read_buffer_number]

        # Keep track of our current send position; which determines where we are in the packet.
        # ``send_position_p1`` is maintained as a registered +1 copy: the read
        # address mux on the accept path then carries no adder (the adder was
        # the tail of a timing-critical cone with several endpoints).
        send_position  = Signal(range(0, self._max_packet_size + 1))
        send_position_p1 = Signal.like(send_position, init=1)

        # Shortcut names.
        in_stream  = self.stream
        out_stream = self.interface.tx

        # We're ready to receive data iff we have space in the buffer we're currently filling.
        m.d.comb += [
            in_stream.ready.eq((write_fill_count + 4 <= self._max_packet_size) & ~write_stream_ended),
            buffer_write.en.eq(in_stream.valid.any() & in_stream.ready),

            # debug taps
            self.debug_write_fill.eq(write_fill_count),
            self.debug_read_fill .eq(read_fill_count),
            self.debug_pingpong  .eq(ping_pong_toggle),
            self.debug_ready     .eq(in_stream.ready),
        ]

        # Increment our fill count whenever we accept new data;
        # based on the number of valid bits we have.
        with m.If(buffer_write.en):
            with m.Switch(in_stream.valid):
                with m.Case(0b0001):
                    m.d.ss += write_fill_count.eq(write_fill_count + 1)
                with m.Case(0b0011):
                    m.d.ss += write_fill_count.eq(write_fill_count + 2)
                with m.Case(0b0111):
                    m.d.ss += write_fill_count.eq(write_fill_count + 3)
                with m.Case(0b1111):
                    m.d.ss += write_fill_count.eq(write_fill_count + 4)

        # If the stream ends while we're adding data to the buffer, mark this as an ended stream.
        with m.If(in_stream.last & buffer_write.en):
            m.d.ss += write_stream_ended.eq(1)


        # Use our memory's two ports to capture data from our transfer stream; and two to emit packets
        # into our packet stream. Since we'll never receive to anywhere else, or transmit to anywhere else,
        # we can just unconditionally connect these.
        m.d.comb += [
            # We'll only ever -write- data from our input stream...
            buffer_write_ports[0].data   .eq(in_stream.payload),
            buffer_write_ports[0].addr   .eq(write_fill_count >> 2),
            buffer_write_ports[1].data   .eq(in_stream.payload),
            buffer_write_ports[1].addr   .eq(write_fill_count >> 2),

            # ... and we'll only ever -send- data from the Read buffer; in the SEND_PACKET state.
            buffer_read.addr             .eq(send_position),
        ]


        #
        # Transmit controller.
        #

        # Stores whether the last packet transmitted was a ZLP. This bit of state determines how
        # retranmission behaves.
        last_packet_was_zlp = Signal()

        # Stores whether we'll need to send an ERDY packet before we send any additional data.
        # If we send an NRDY packet indicating that we have no data for the host, the host will
        # stop polling this endpoint until an ERDY packet is sent [USB3.2r1: 8.10.1]. We'll need
        # to send an ERDY packet to have it resume polling.
        erdy_required = Signal()
        m.d.comb += self.debug_erdyreq.eq(erdy_required)

        # Tag every transaction packet we emit with our endpoint number: NRDY and
        # ERDY are dispatched from several states below, and without this the TPs
        # go out addressed to endpoint 0 -- the host then applies (or discards)
        # our flow control on the wrong pipe, wedging this endpoint.
        m.d.comb += handshakes_out.endpoint_number.eq(self._endpoint_number)

        # Shortcut for when we need to deal with an in token.
        # Note that, for USB3, an IN token is an ACK that contains a non-zero ``number_of_packets``.
        #
        # The decode is registered: the handshake events are broadcast to
        # every endpoint, and feeding the endpoint-number/sequence compares
        # combinationally into the FSM (and from there into the transmit
        # buffer addressing) misses timing once several endpoints share the
        # broadcast.  These are single-cycle event strobes; one cycle of
        # latency is protocol-invisible.  The sequence comparison is sampled
        # with the strobe: the sequence number only changes as a *result* of
        # processing an acknowledgement, so it is stable in between.
        is_to_us          = (handshakes_in.endpoint_number == self._endpoint_number)
        ack_received      = Signal()
        is_in_token       = Signal()
        in_token_received = Signal()
        retry_requested   = Signal()
        sequence_advancing = Signal()
        m.d.ss += [
            ack_received      .eq(handshakes_in.ack_received & is_to_us),
            is_in_token       .eq(handshakes_in.number_of_packets != 0),
            in_token_received .eq(handshakes_in.ack_received & is_to_us
                                  & (handshakes_in.number_of_packets != 0)),
            retry_requested   .eq(handshakes_in.retry_required),
            sequence_advancing.eq(handshakes_in.next_sequence
                                  == next_sequence_number),
        ]

        # ACK events are single-cycle strobes, and the host is free to time
        # them against ANY of our states: a stale or duplicate ACK (e.g. a
        # link-level DL replay after an LBAD) received in WAIT_FOR_ACK
        # correctly starts a protocol resend -- and the GENUINE ACK+token
        # then arrives while we are mid-resend in SEND_PACKET /
        # FINISH_LAST_WORD.  Dropping it strands this pipe permanently:
        # we park in WAIT_FOR_ACK while the host waits for the packet it
        # already granted credit for, and after its response timeout it
        # halts the pipe (-71 EPROTO on the bench; open item #23 /
        # bug #26 -- reproduced deterministically in sim_stale_ack.py).
        # With several endpoint pairs active, the resend is stretched by
        # transmit-mux contention, which is what made this reachable with
        # three concurrent pipes.
        #
        # Latch such events instead (fields captured at strobe time; the
        # sequence number cannot change mid-resend, so the comparisons
        # stay valid), and consume the latch upon re-entering
        # WAIT_FOR_ACK.  A non-advancing duplicate never overwrites a
        # latched advancing acknowledgement.
        pending_ack   = Signal()
        p_adv         = Signal()
        p_retry       = Signal()
        p_token       = Signal()
        latch_ack_event = Signal()      # asserted by the states below

        with m.If(latch_ack_event & ack_received
                  & (~pending_ack | ~p_adv | sequence_advancing)):
            m.d.ss += [
                pending_ack .eq(1),
                p_adv       .eq(sequence_advancing),
                p_retry     .eq(retry_requested),
                p_token     .eq(is_in_token),
            ]

        # Effective ACK view for WAIT_FOR_ACK: a latched (older) event is
        # served before a live strobe; if both are present in the same
        # cycle, the live one is re-latched and served next.
        eff_ack_pending = Signal()
        eff_adv         = Signal()
        eff_retry       = Signal()
        eff_token       = Signal()
        m.d.comb += [
            eff_ack_pending .eq(pending_ack),
            eff_adv         .eq(Mux(pending_ack, p_adv, sequence_advancing)),
            eff_retry       .eq(Mux(pending_ack, p_retry, retry_requested)),
            eff_token       .eq(Mux(pending_ack, p_token, is_in_token)),
        ]

        with m.FSM(domain='ss') as tx_fsm:

            # WAIT_FOR_DATA -- We don't yet have a full packet to transmit, so  we'll capture data
            # to fill the our buffer. At full throughput, this state will never be reached after
            # the initial post-reset fill.
            with m.State("WAIT_FOR_DATA"):

                # We can't yet send data; so we'll send an NRDY transaction packet.
                with m.If(in_token_received):
                    m.d.comb += handshakes_out.send_nrdy  .eq(1)
                    m.d.ss   += erdy_required             .eq(1)

                # If we have valid data that will end our packet, we're no longer waiting for data.
                # We'll now wait for the host to request data from us.
                packet_complete = (write_fill_count + 4 >= self._max_packet_size)
                will_end_packet = packet_complete | in_stream.last

                with m.If(in_stream.valid & will_end_packet):

                    # If we've just finished a packet, we now have data we can send!
                    with m.If(packet_complete | in_stream.last):
                        m.d.ss += [

                            # We're now ready to take the data we've captured and _transmit_ it.
                            # We'll swap our read and write buffers.
                            ping_pong_toggle.eq(~ping_pong_toggle),

                            # Mark our current stream as no longer having ended.
                            read_stream_ended  .eq(0)
                        ]

                        # If we've already sent an NRDY token, we'll need to request an IN token
                        # before the host will be willing to send us one.
                        with m.If(erdy_required | in_token_received):
                            m.next = "REQUEST_IN_TOKEN"

                        # Otherwise, we can wait for an IN token directly.
                        with m.Else():
                            m.next = "WAIT_TO_SEND"


            # REQUEST_IN_TOKEN -- we now have at least a buffer full of data to send; but
            # we've sent a NRDY token to the host; and thus the host is no longer polling for data.
            # We'll send an ERDY token to the host, in order to request it poll us again.
            with m.State("REQUEST_IN_TOKEN"):

                # Send our ERDY token...
                m.d.comb += handshakes_out.send_erdy.eq(1)

                # If an IN token crosses our ERDY request, serve it immediately;
                # ignoring it would leave the host's credit unanswered (and the
                # ERDY itself is still emitted, which the host tolerates).
                with m.If(in_token_received):
                    # The host is polling again; the pipe is no longer parked.
                    m.d.ss += erdy_required.eq(0)
                    with m.If(read_fill_count):
                        m.d.ss += last_packet_was_zlp.eq(0)
                        m.next = "SEND_PACKET"
                    with m.Else():
                        m.d.comb += interface.tx_zlp.eq(1)
                        m.d.ss += [
                            read_stream_ended   .eq(0),
                            last_packet_was_zlp .eq(1),
                        ]
                        m.next = "WAIT_FOR_ACK"

                # ... otherwise, once that send is complete, move on to waiting
                # for an IN token.
                with m.Elif(handshakes_out.done):
                    m.d.ss += erdy_required.eq(0)
                    m.next = "WAIT_TO_SEND"


            # WAIT_TO_SEND -- we now have at least a buffer full of data to send; we'll
            # need to wait for an IN token to send it.
            with m.State("WAIT_TO_SEND"):

                # If we've NRDY'd the host and not yet re-opened the pipe, no
                # token is coming: request one with an ERDY.  (Reaching here
                # with the flag set is possible via the WAIT_FOR_ACK buffer
                # swap, which does not pass through WAIT_FOR_DATA -- leaving
                # data buffered against a parked pipe forever.)
                with m.If(erdy_required):
                    m.next = "REQUEST_IN_TOKEN"

                # Once we get an IN token, move to sending a packet.
                with m.Elif(in_token_received):

                    # If we have a packet to send, send it.
                    with m.If(read_fill_count):
                        m.next = "SEND_PACKET"
                        m.d.ss += [
                            last_packet_was_zlp  .eq(0)
                        ]

                    # Otherwise, we entered a transmit path without any data in the buffer.
                    with m.Else():
                        # ... send a ZLP...
                        m.d.comb += interface.tx_zlp.eq(1)

                        # ... and clear the need to follow up with one, since we've just sent a short packet.
                        m.d.ss += [
                            read_stream_ended    .eq(0),
                            last_packet_was_zlp  .eq(1)
                        ]

                        # We've now completed a packet send; so wait for it to be acknowledged.
                        m.next = "WAIT_FOR_ACK"


            # SEND_PACKET -- we now have enough data to send _and_ have received an IN token.
            # We can now send our data over to the host.
            with m.State("SEND_PACKET"):

                m.d.comb += [
                    # Apply our general transfer information.
                    interface.tx_direction        .eq(USBDirection.IN),
                    interface.tx_sequence_number  .eq(sequence_number),
                    interface.tx_length           .eq(read_fill_count),
                    interface.tx_endpoint_number  .eq(self._endpoint_number),

                    # ACK events landing mid-send must not be dropped
                    # (see the pending-acknowledgement latch above).
                    latch_ack_event               .eq(1),
                ]

                with m.If(~out_stream.valid.any() | out_stream.ready):
                    # Once we emitted a word of data for our receiver, move to the next word in our packet.
                    m.d.ss   += [
                        send_position     .eq(send_position_p1),
                        send_position_p1  .eq(send_position_p1 + 1),
                    ]
                    m.d.comb += buffer_read.addr  .eq(send_position_p1)

                    # We're on our last word whenever the next word would be contain the end of our data.
                    first_word = (send_position == 0)
                    last_word  = ((send_position + 1) << 2 >= read_fill_count)

                    m.d.ss += [
                        # Block RAM often has a large clock-to-dout delay; register the output to
                        # improve timings.
                        out_stream.payload        .eq(buffer_read.data),

                        # Let our transmitter know the packet boundaries.
                        out_stream.first          .eq(first_word),
                        out_stream.last           .eq(last_word),
                    ]

                    # Figure out which bytes of our stream are valid. Normally; this is all of them,
                    # but the last word is a special case, which we'll have to handle based on how
                    # many bytes we expect to be valid in the word.
                    with m.If(last_word):

                        # We can figure out how many bytes are valid by looking at the last two bits of our
                        # count; which happen to be the mod-4 remainder.
                        with m.Switch(read_fill_count[0:2]):

                            # If we're evenly divisible by four, all four bytes are valid.
                            with m.Case(0):
                                m.d.ss += out_stream.valid.eq(0b1111)

                            # Otherwise, our remainder tells os how many bytes are valid.
                            with m.Case(1):
                                m.d.ss += out_stream.valid.eq(0b0001)
                            with m.Case(2):
                                m.d.ss += out_stream.valid.eq(0b0011)
                            with m.Case(3):
                                m.d.ss += out_stream.valid.eq(0b0111)


                    # For every word that's not the last one, we know that all bytes are valid.
                    with m.Else():
                        m.d.ss += out_stream.valid.eq(0b1111)

                    # If we've just scheduled our last word, wait for it to be
                    # accepted before considering the packet sent.
                    with m.If(last_word):
                        m.next = 'FINISH_LAST_WORD'


            # FINISH_LAST_WORD -- our last word is presented on the (registered)
            # output stream, but the transmitter may not have accepted it yet
            # (it typically back-pressures until the data packet header has
            # made it through the header queue).  Keep the word -- and our
            # transmit parameters -- driven until it is accepted; dropping it
            # early truncates the payload versus the header's data_length,
            # which the host (correctly) rejects as a malformed data packet.
            with m.State("FINISH_LAST_WORD"):

                m.d.comb += [
                    # Keep our general transfer information applied.
                    interface.tx_direction        .eq(USBDirection.IN),
                    interface.tx_sequence_number  .eq(sequence_number),
                    interface.tx_length           .eq(read_fill_count),
                    interface.tx_endpoint_number  .eq(self._endpoint_number),

                    # ACK events landing mid-send must not be dropped.
                    latch_ack_event               .eq(1),
                ]

                # Once the transmitter takes the final word, the packet is
                # fully handed over; wait for the host's response.
                with m.If(out_stream.ready):
                    m.d.ss += out_stream.valid.eq(0)
                    m.next = 'WAIT_FOR_ACK'


            # WAIT_FOR_ACK -- We've just sent a packet; but don't know if the host has
            # received it correctly. We'll wait to see if the host ACKs.
            with m.State("WAIT_FOR_ACK"):

                # We're done transmitting data.
                m.d.ss   += out_stream.valid.eq(0)

                # Reset our send-position for the next data packet.
                m.d.ss   += [
                    send_position   .eq(0),
                    send_position_p1.eq(1),
                ]
                m.d.comb += buffer_read.addr.eq(0)

                # In USB3, an ACK handshake can act as an ACK, an error indicator, and/or an IN token.
                # This helps to maximize bus bandwidth, but means we have to handle each case carefully.
                #
                # A latched (older) acknowledgement -- one that arrived while we
                # were mid-send and could not be processed -- is served before a
                # live strobe; if both are present in the same cycle, the live
                # one is re-latched and served on the next pass through this
                # state.  (The ``eff_*`` signals select the pending fields
                # whenever ``pending_ack`` is set.)
                with m.If(pending_ack):
                    with m.If(ack_received):
                        m.d.ss += [
                            pending_ack .eq(1),
                            p_adv       .eq(sequence_advancing),
                            p_retry     .eq(retry_requested),
                            p_token     .eq(is_in_token),
                        ]
                    with m.Else():
                        m.d.ss += pending_ack.eq(0)

                with m.If(ack_received | eff_ack_pending):

                    # Debug taps: what kind of acknowledgement service is this?
                    m.d.comb += [
                        self.debug_retry_flagged.eq(eff_retry),
                        self.debug_stale_ack    .eq(~eff_retry & ~eff_adv),
                    ]

                    # Our simplest case is actually when an error occurs, which is indicated by receiving
                    # an ACK packet with a NON-advancing sequence number (with or without the Retry bit --
                    # a stale duplicate asks for the same resend).  An ACK whose sequence number ADVANCES
                    # acknowledges the current packet even when its Retry bit is set: the "retry" then
                    # names the NEXT packet -- one we have never transmitted (e.g. the host re-establishing
                    # an interrupted grant after link recovery) -- and transmitting it freshly through the
                    # normal path below IS the requested retry.  The historical ``eff_retry | ~eff_adv``
                    # resent the ALREADY-ACKNOWLEDGED current packet in that case; the host discards the
                    # duplicate and the pipe wedges in a retransmit loop.
                    # (``sequence_advancing`` was registered along with the strobe.)
                    with m.If(~eff_adv):

                        # In this case, we'll re-transmit the relevant data, either by sending another ZLP...
                        with m.If(last_packet_was_zlp):
                            m.d.comb += [
                                interface.tx_zlp.eq(1),
                                advance_sequence.eq(1),
                            ]

                        # ... or by moving right back into sending a data packet.
                        with m.Else():
                            m.next = 'SEND_PACKET'


                    # Otherwise, if our ACK contains the next sequence number, then this is an acknowledgement
                    # of the previous packet [USB3.2r1: 8.12.1.2].
                    with m.Else():

                        # We no longer need to keep the data that's been acknowledged; clear it.
                        # (Both the count and the stream-ended flag: this buffer becomes the
                        # write buffer on the next swap, and a stale ended flag would make
                        # the fill side refuse data forever.)
                        m.d.ss += [
                            read_fill_count   .eq(0),
                            read_stream_ended .eq(0),
                        ]

                        # Figure out if we'll need to follow up with a ZLP. If we have ZLP generation enabled,
                        # we'll make sure we end on a short packet. If this is max-packet-size packet _and_ our
                        # transfer ended with this packet; we'll need to inject a ZLP.
                        follow_up_with_zlp = \
                            (read_fill_count == self._max_packet_size) & read_stream_ended \
                            if self._generate_zlps else C(0)

                        # If we're following up with a ZLP, we have two cases, depending on whether this ACK
                        # is also requesting another packet.
                        with m.If(follow_up_with_zlp):

                            # If we are requesting another packet immediately, we can said ZLP our immediately,
                            # and then continue waiting for the next ACK.
                            with m.If(eff_token):

                                # ... send a ZLP...
                                m.d.comb += [
                                    interface.tx_zlp.eq(1),
                                    advance_sequence.eq(1),
                                ]

                                # ... and clear the need to follow up with one, since we've just sent a short packet.
                                m.d.ss += [
                                    read_stream_ended    .eq(0),
                                    last_packet_was_zlp  .eq(1)
                                ]

                            # Otherwise, we'll wait for an attempt to send data before we generate a ZLP.
                            with m.Else():
                                m.next = "WAIT_TO_SEND"


                        # Otherwise, there's a possibility we already have a packet-worth of data waiting
                        # for us in our "write buffer", which we've been filling in the background.
                        # If this is the case, we'll flip which buffer we're working with, and then
                        # ready ourselves for transmit.
                        packet_completing = in_stream.valid & (write_fill_count + 4 >= self._max_packet_size)
                        with m.Elif(~in_stream.ready | packet_completing):
                            m.d.comb += [
                                advance_sequence   .eq(1),
                            ]
                            m.d.ss += [
                                ping_pong_toggle   .eq(~ping_pong_toggle),
                                read_stream_ended  .eq(0),
                            ]

                            with m.If(eff_token):
                                m.d.ss += [
                                    last_packet_was_zlp  .eq(0)
                                ]
                                m.next = "SEND_PACKET"

                            with m.Else():
                                m.next = "WAIT_TO_SEND"

                        # If neither of the above conditions are true; we now don't have enough data to send.
                        # We'll wait for enough data to transmit.
                        with m.Else():

                            # The packet this ACK acknowledges is complete: consume
                            # its sequence number.  (The other arms advance it as a
                            # side effect of dispatching the next packet; without
                            # this, the next packet repeats the acknowledged
                            # sequence number and the host discards it as a
                            # duplicate -- wedging the pipe in a retransmit loop.)
                            m.d.comb += advance_sequence.eq(1)

                            # If this ACK also grants us credit for another packet
                            # (NumP > 0, i.e. it doubles as an IN token), we must
                            # answer it: with nothing buffered, that's an NRDY --
                            # silently consuming the token leaves the host waiting
                            # on credit we never honor, and it times the pipe out.
                            with m.If(eff_token):
                                m.d.comb += handshakes_out.send_nrdy.eq(1)
                                m.d.ss   += erdy_required           .eq(1)

                            m.next = "WAIT_FOR_DATA"

        for _i, _name in enumerate((
                "WAIT_FOR_DATA", "REQUEST_IN_TOKEN", "WAIT_TO_SEND",
                "SEND_PACKET", "FINISH_LAST_WORD", "WAIT_FOR_ACK")):
            with m.If(tx_fsm.ongoing(_name)):
                m.d.comb += self.debug_fsm.eq(_i)

        return m


    def _elaborate_burst(self, platform):
        """ Burst-capable transmit engine (``max_burst`` > 1).

        A ring of ``max_burst + 1`` packet buffers decouples three
        concurrent activities:

          * the FILL side captures stream data into ``buffer[fill_idx]``
            and hands completed packets over;
          * the SEND side transmits ready packets back-to-back while the
            host's grant (NumP) lasts, advancing the 5-bit data sequence
            per packet WITHOUT waiting for per-packet acknowledgements,
            and sets EOB on the final packet of each burst;
          * the RETIRE side processes acknowledgements: an ACK's sequence
            number cumulatively retires every packet before it (freeing
            buffers), its NumP replaces the remaining grant, and its
            retry flag rewinds transmission to the acknowledged point
            (the unacknowledged packets' buffers are retained precisely
            for this).

        Stale acknowledgements -- link-level DL replays whose sequence
        number lies outside the unacknowledged window -- are ignored
        outright: with cumulative retirement, mod-32 arithmetic would
        otherwise misread them as huge forward jumps.
        """
        m = Module()

        interface      = self.interface
        handshakes_in  = interface.handshakes_in
        handshakes_out = interface.handshakes_out

        data_width     = len(self.stream.data)
        bytes_per_word = data_width // 8
        buffer_depth   = self._max_packet_size // bytes_per_word
        ring_size      = self._max_burst + 1
        mps            = self._max_packet_size

        in_stream  = self.stream
        out_stream = self.interface.tx

        # Tag every transaction packet we emit with our endpoint number.
        m.d.comb += handshakes_out.endpoint_number.eq(self._endpoint_number)

        #
        # Packet buffer ring.
        #
        buffers     = [Memory(shape=data_width, depth=buffer_depth, init=[])
                       for _ in range(ring_size)]
        write_ports = Array(buf.write_port(domain="ss") for buf in buffers)
        read_ports  = Array(buf.read_port(domain="ss") for buf in buffers)
        for i, buf in enumerate(buffers):
            m.submodules[f"burst_buffer_{i}"] = buf

        fill_counts = Array(Signal(range(mps + 1), name=f"fill_count_{i}")
                            for i in range(ring_size))

        fill_idx    = Signal(range(ring_size))
        send_idx    = Signal(range(ring_size))
        retire_idx  = Signal(range(ring_size))

        # Ring occupancy.  ``ready`` are complete, unsent packets;
        # ``unacked`` are sent, unacknowledged (retained for retries).
        # The buffer at ``fill_idx`` is always owned by the fill side.
        ready_count   = Signal(range(ring_size + 1))
        unacked_count = Signal(range(ring_size + 1))

        ready_inc, ready_dec = Signal(), Signal()
        unack_inc, unack_dec = Signal(), Signal()
        with m.If(ready_inc & ~ready_dec):
            m.d.ss += ready_count.eq(ready_count + 1)
        with m.Elif(ready_dec & ~ready_inc):
            m.d.ss += ready_count.eq(ready_count - 1)
        with m.If(unack_inc & ~unack_dec):
            m.d.ss += unacked_count.eq(unacked_count + 1)
        with m.Elif(unack_dec & ~unack_inc):
            m.d.ss += unacked_count.eq(unacked_count - 1)

        #
        # Sequence and grant state.
        #
        sequence_number = Signal(self.SEQUENCE_NUMBER_BITS)  # next to assign
        acked_sequence  = Signal(self.SEQUENCE_NUMBER_BITS)  # oldest unacked
        grant_left      = Signal(5)                          # NumP remaining
        erdy_required   = Signal()
        m.d.comb += self.debug_erdyreq.eq(erdy_required)

        # Post-EOB grant discipline (bug #34): once we transmit a packet
        # with EOB set, WE have terminated the burst -- the host answers
        # the EOB with a terminating ACK (NumP=0) and DISCARDS any DP
        # that arrives on the closed burst [USB3.2r1: 8.12.1.2, rule
        # 9249].  Per-packet acknowledgements for the burst's EARLIER
        # packets, however, are already in flight toward us carrying
        # nonzero NumP windows; taking a grant from one launches a
        # packet straight into the closed burst.  The host silently
        # drops it, then re-tokens with the same (non-advancing) nseq
        # and rty=0 -- which this engine used to read as "grant only,
        # nothing to resend", answering with the NEXT sequence number
        # and wedging the pipe (the deterministic BURST=2 bench failure:
        # every pipe dies after its first 2-packet burst).  Gate grants
        # after an EOB until an acknowledgement retires the EOB packet
        # itself; the fresh token that reopens the pipe does exactly
        # that.
        eob_wait = Signal()                                  # burst closed by us
        eob_next = Signal(self.SEQUENCE_NUMBER_BITS)         # seq after EOB pkt

        #
        # Registered handshake-event decode (as in the single-packet
        # engine: the broadcast compare cones must not feed the FSM
        # combinationally).
        #
        is_to_us     = (handshakes_in.endpoint_number == self._endpoint_number)
        ack_received = Signal()
        ack_nseq     = Signal(self.SEQUENCE_NUMBER_BITS)
        ack_rty      = Signal()
        ack_nump     = Signal(5)
        m.d.ss += [
            ack_received .eq(handshakes_in.ack_received & is_to_us),
            ack_nseq     .eq(handshakes_in.next_sequence),
            ack_rty      .eq(handshakes_in.retry_required),
            ack_nump     .eq(handshakes_in.number_of_packets),
        ]

        # One-deep, newest-wins event latch: acknowledgements are
        # cumulative (a newer event strictly supersedes an older one),
        # and may arrive in any state.  Never dropped ("handshake events
        # are never dropped" -- the bug-#26 rule).
        ev_pending = Signal()
        ev_nseq    = Signal(self.SEQUENCE_NUMBER_BITS)
        ev_rty     = Signal()
        ev_nump    = Signal(5)

        #
        # Fill side.
        #
        fill_done  = Signal()   # buffer[fill_idx] holds a complete packet
        wfc        = fill_counts[fill_idx]
        stream_add = Signal(3)

        m.d.comb += [
            in_stream.ready.eq(~fill_done & (wfc + 4 <= mps)),

            self.debug_write_fill.eq(wfc),
            self.debug_read_fill .eq(fill_counts[send_idx]),
            self.debug_ready     .eq(in_stream.ready),
        ]
        with m.Switch(in_stream.valid):
            with m.Case(0b0001):
                m.d.comb += stream_add.eq(1)
            with m.Case(0b0011):
                m.d.comb += stream_add.eq(2)
            with m.Case(0b0111):
                m.d.comb += stream_add.eq(3)
            with m.Default():
                m.d.comb += stream_add.eq(4)

        for i in range(ring_size):
            m.d.comb += [
                write_ports[i].data.eq(in_stream.payload),
                write_ports[i].addr.eq(wfc >> 2),
                write_ports[i].en  .eq((fill_idx == i)
                                       & in_stream.valid.any()
                                       & in_stream.ready),
            ]

        accepted = in_stream.valid.any() & in_stream.ready
        with m.If(accepted):
            m.d.ss += wfc.eq(wfc + stream_add)
            # The packet completes with a full buffer or the stream's
            # ``last`` word (short packet).
            with m.If((wfc + stream_add >= mps) | in_stream.last):
                m.d.ss += fill_done.eq(1)

        # Handoff of a completed packet to the send side, when ring space
        # allows the filler to move on.  (Paused while an acknowledgement
        # is being processed, so at most one updater per counter per
        # cycle.)
        handoff_ok = Signal()   # driven by the FSM: not processing an ACK
        with m.If(fill_done & handoff_ok
                  & ((ready_count + unacked_count) <= (ring_size - 2))):
            m.d.comb += ready_inc.eq(1)
            m.d.ss += [
                fill_done .eq(0),
                fill_idx  .eq(Mux(fill_idx == ring_size - 1,
                                  0, fill_idx + 1)),
            ]

        #
        # Send position bookkeeping (as in the single-packet engine).
        #
        send_position    = Signal(range(mps + 1))
        send_position_p1 = Signal.like(send_position, init=1)
        buffer_read      = read_ports[send_idx]
        read_fill_count  = fill_counts[send_idx]
        m.d.comb += buffer_read.addr.eq(send_position)

        # EOB decision, registered at dispatch time so the transmit
        # parameters stay stable for the whole packet.
        eob_r = Signal()

        # Debug taps (uart wire-checker channels).
        m.d.comb += self.debug_pingpong.eq(0)

        def wrap_inc(sig):
            return Mux(sig == ring_size - 1, 0, sig + 1)

        with m.FSM(domain='ss') as tx_fsm:

            # DISPATCH -- the engine's hub: process acknowledgements,
            # request polling (ERDY), and launch packet transmissions.
            with m.State("DISPATCH"):
                m.d.comb += handoff_ok.eq(~ev_pending)

                # Reset our send position for the next packet.
                m.d.ss += [
                    send_position   .eq(0),
                    send_position_p1.eq(1),
                    out_stream.valid.eq(0),
                ]

                with m.If(ev_pending):
                    m.next = "PROCESS_ACK"

                # If we've parked the pipe (NRDY) and have data again,
                # ask the host to resume polling.  (The handshake mux
                # latches strobes losslessly, so this is fire-and-forget.)
                with m.Elif(erdy_required & (ready_count != 0)):
                    m.d.comb += handshakes_out.send_erdy.eq(1)
                    m.d.ss   += erdy_required.eq(0)

                # Launch the next packet of the burst.
                with m.Elif((grant_left != 0) & (ready_count != 0)):
                    m.d.ss += [
                        # EOB when this packet exhausts the grant, is the
                        # last one buffered (the burst would stall), or is
                        # a short packet (which ends a burst by rule).
                        eob_r.eq((grant_left == 1)
                                 | (ready_count == 1)
                                 | (read_fill_count != mps)),
                    ]
                    m.next = "SEND_PACKET"


            # PROCESS_ACK -- service the latched acknowledgement:
            # cumulative retirement (one buffer per cycle), optional
            # rewind-on-retry, then grant replacement.
            with m.State("PROCESS_ACK"):

                # Stale event (a DL-replayed older acknowledgement): its
                # sequence number is outside our unacknowledged window.
                # Ignore it entirely -- its grant is outdated too.
                delta = Signal(self.SEQUENCE_NUMBER_BITS)
                m.d.comb += delta.eq(ev_nseq - acked_sequence)

                with m.If(delta > unacked_count):
                    m.d.comb += self.debug_stale_ack.eq(1)
                    m.d.ss += ev_pending.eq(0)
                    m.next = "DISPATCH"

                # Retirement: free one acknowledged buffer per cycle.
                with m.Elif(acked_sequence != ev_nseq):
                    m.d.comb += unack_dec.eq(1)
                    m.d.ss += [
                        fill_counts[retire_idx].eq(0),
                        retire_idx             .eq(wrap_inc(retire_idx)),
                        acked_sequence         .eq(acked_sequence + 1),
                    ]

                # Rewind-on-retry: return every remaining unacknowledged
                # packet to the ready pool, one per cycle; transmission
                # resumes from the acknowledged point.  (The rewound
                # packets get fresh EOB decisions on re-dispatch, so a
                # pending post-EOB gate is void.)
                with m.Elif(ev_rty & (unacked_count != 0)):
                    m.d.comb += [
                        unack_dec.eq(1),
                        ready_inc.eq(1),
                        self.debug_retry_flagged.eq(1),
                    ]
                    m.d.ss += [
                        send_idx        .eq(Mux(send_idx == 0,
                                                ring_size - 1, send_idx - 1)),
                        sequence_number .eq(sequence_number - 1),
                        eob_wait        .eq(0),
                    ]

                # Event fully serviced: the acknowledgement's NumP is the
                # number of packets the host can receive FROM ITS SEQUENCE
                # NUMBER ON -- which includes any packets we have already
                # sent beyond it (an xHC acknowledges every DP, so
                # mid-burst ACKs arrive with our later packets still in
                # flight).  Our remaining grant is therefore NumP minus
                # the still-unacknowledged count; taking NumP verbatim
                # oversends into buffers the in-flight packets are about
                # to consume (host-side babble, -EIO on the bench).
                #
                # After we terminated a burst with EOB, only an
                # acknowledgement that retires the EOB packet itself may
                # re-arm the grant (see the post-EOB discipline note
                # above); windows carried by the closed burst's earlier
                # per-packet ACKs are void.
                with m.Else():
                    burst_open = Signal()
                    m.d.comb += burst_open.eq(~eob_wait
                                              | (ev_nseq == eob_next))
                    with m.If(eob_wait & (ev_nseq == eob_next)):
                        m.d.ss += eob_wait.eq(0)
                    m.d.ss += [
                        grant_left.eq(Mux(burst_open
                                          & (ev_nump > unacked_count),
                                          ev_nump - unacked_count, 0)),
                        ev_pending.eq(0),
                    ]

                    # An acknowledgement with NumP=0 puts the pipe in
                    # flow control [USB3.2r1: 8.10.1] -- in particular,
                    # the host's terminating ACK for a burst we ended
                    # with EOB.  The host will NOT token again on its
                    # own for the rest of the transfer; the pipe reopens
                    # only on our ERDY (sent from DISPATCH as soon as a
                    # packet is ready).  Without this the bench xHC
                    # falls back to its multi-second no-response re-poll
                    # after every 2-packet burst (~0.4 KB/s crawl).
                    with m.If(ev_nump == 0):
                        m.d.ss += erdy_required.eq(1)

                    # A token we cannot serve parks the pipe: NRDY now,
                    # ERDY when data arrives.  (Only when nothing is in
                    # flight: with packets outstanding the host is not
                    # waiting on us.)
                    with m.If((ev_nump != 0) & (ready_count == 0)
                              & (unacked_count == 0) & ~fill_done):
                        m.d.comb += handshakes_out.send_nrdy.eq(1)
                        m.d.ss += [
                            erdy_required.eq(1),
                            grant_left   .eq(0),
                        ]

                    m.next = "DISPATCH"


            # SEND_PACKET -- stream the packet at ``send_idx`` (as in the
            # single-packet engine, against the ring).
            with m.State("SEND_PACKET"):

                m.d.comb += [
                    interface.tx_direction        .eq(USBDirection.IN),
                    interface.tx_sequence_number  .eq(sequence_number),
                    interface.tx_length           .eq(read_fill_count),
                    interface.tx_endpoint_number  .eq(self._endpoint_number),
                    interface.tx_eob              .eq(eob_r),

                    # Fill handoffs continue during sends (that is the
                    # point of the ring); only acknowledgement processing
                    # pauses them, so each occupancy counter has at most
                    # one incrementer and one decrementer per cycle.
                    handoff_ok                    .eq(1),
                ]

                with m.If(~out_stream.valid.any() | out_stream.ready):
                    m.d.ss   += [
                        send_position     .eq(send_position_p1),
                        send_position_p1  .eq(send_position_p1 + 1),
                    ]
                    m.d.comb += buffer_read.addr.eq(send_position_p1)

                    first_word = (send_position == 0)
                    last_word  = ((send_position + 1) << 2 >= read_fill_count)

                    m.d.ss += [
                        out_stream.payload  .eq(buffer_read.data),
                        out_stream.first    .eq(first_word),
                        out_stream.last     .eq(last_word),
                    ]

                    with m.If(last_word):
                        with m.Switch(read_fill_count[0:2]):
                            with m.Case(0):
                                m.d.ss += out_stream.valid.eq(0b1111)
                            with m.Case(1):
                                m.d.ss += out_stream.valid.eq(0b0001)
                            with m.Case(2):
                                m.d.ss += out_stream.valid.eq(0b0011)
                            with m.Case(3):
                                m.d.ss += out_stream.valid.eq(0b0111)
                    with m.Else():
                        m.d.ss += out_stream.valid.eq(0b1111)

                    with m.If(last_word):
                        m.next = 'FINISH_LAST_WORD'


            # FINISH_LAST_WORD -- hold the final word (and parameters)
            # until the shared transmitter accepts it.
            with m.State("FINISH_LAST_WORD"):

                m.d.comb += [
                    interface.tx_direction        .eq(USBDirection.IN),
                    interface.tx_sequence_number  .eq(sequence_number),
                    interface.tx_length           .eq(read_fill_count),
                    interface.tx_endpoint_number  .eq(self._endpoint_number),
                    interface.tx_eob              .eq(eob_r),
                    handoff_ok                    .eq(1),
                ]

                with m.If(out_stream.ready):
                    m.d.ss += out_stream.valid.eq(0)

                    # The packet is handed over: it is now in flight.
                    m.d.comb += [
                        ready_dec.eq(1),
                        unack_inc.eq(1),
                    ]
                    m.d.ss += [
                        send_idx        .eq(wrap_inc(send_idx)),
                        sequence_number .eq(sequence_number + 1),
                        # An EOB packet voids the remainder of the grant;
                        # the host re-tokens after its (cumulative) ACK.
                        grant_left      .eq(Mux(eob_r, 0, grant_left - 1)),
                    ]
                    # We just terminated the burst: gate all grants until
                    # an acknowledgement retires this packet (post-EOB
                    # discipline; see the note at the state declaration).
                    with m.If(eob_r):
                        m.d.ss += [
                            eob_wait.eq(1),
                            eob_next.eq(sequence_number + 1),
                        ]
                    m.next = 'DISPATCH'

        # Event capture -- placed after the FSM so a strobe coinciding
        # with the FSM's ``ev_pending`` clear is re-latched, not lost.
        with m.If(ack_received):
            m.d.ss += [
                ev_pending .eq(1),
                ev_nseq    .eq(ack_nseq),
                ev_rty     .eq(ack_rty),
                ev_nump    .eq(ack_nump),
            ]

        # Link out of U0 (training / recovery): void the remaining grant
        # and any latched pre-recovery acknowledgement.  The ring --
        # including the unacknowledged, retained packets -- is preserved:
        # the host re-establishes the burst after recovery with a fresh
        # (retry) ACK TP, whose rewind-and-regrant we then serve from the
        # retained buffers.  Transmitting on a stale grant instead races
        # that re-establishment with packets the host no longer expects.
        with m.If(interface.link_reset):
            m.d.ss += [
                grant_left.eq(0),
                ev_pending.eq(0),
            ]

        # Endpoint reset: return to a clean, empty ring.
        with m.If(interface.ep_reset):
            m.d.ss += [
                sequence_number.eq(0),
                acked_sequence .eq(0),
                grant_left     .eq(0),
                ev_pending     .eq(0),
                erdy_required  .eq(0),
                fill_idx       .eq(0),
                send_idx       .eq(0),
                retire_idx     .eq(0),
                ready_count    .eq(0),
                unacked_count  .eq(0),
                fill_done      .eq(0),
                eob_wait       .eq(0),
            ]
            m.d.ss += [fc.eq(0) for fc in fill_counts]

        for _i, _name in enumerate((
                "DISPATCH", "PROCESS_ACK", "SEND_PACKET",
                "FINISH_LAST_WORD")):
            with m.If(tx_fsm.ongoing(_name)):
                m.d.comb += self.debug_fsm.eq(_i)

        return m
