#
# This file is part of LUNA.
#
# Copyright (c) 2020 Great Scott Gadgets <info@greatscottgadgets.com>
# SPDX-License-Identifier: BSD-3-Clause
""" Header Packet Rx-handling gateware. """

from amaranth                      import *

from usb_protocol.types.superspeed import LinkCommand

from .header                       import HeaderPacket, HeaderQueue
from .crc                          import compute_usb_crc5, HeaderPacketCRC
from .command                      import LinkCommandGenerator
from ..physical.coding             import SHP, EPF, stream_matches_symbols, \
    half_matches_symbols
from ...stream                     import USBRawSuperSpeedStream


class RawHeaderPacketReceiver(Elaboratable):
    """ Class that monitors the USB bus for Header Packet, and receives them.

    This class performs the validations required at the link layer of the USB specification;
    which include checking the CRC-5 and CRC-16 embedded within the header packet.


    Attributes
    ----------
    sink: USBRawSuperSpeedStream(), input (monitor only)
        Stream that the USB data to be monitored.
    packet: HeaderPacket(), output
        The de-serialized form of our header packet.

    new_packet: Signal(), output
        Strobe; indicates that a new, valid header packet has been received. The new
        packet is now available on :attr:``packet``.
    bad_packet: Signal(), output
        Strobe; indicates that a corrupted, invalid header packet has been received.
        :attr:``packet`` has not been updated.

    expected_sequence: Signal(3), input
        Indicates the next expected sequence number; used to validate the received packet.

    """

    def __init__(self, gen2=False, words=1):
        # SuperSpeedPlus trim: 4-bit header sequence numbers, with the
        # top bit riding in the LCW's SS-reserved bit (dw3_reserved[0]).
        self._gen2 = gen2
        # Width program (usb3_design.md 13.5): at ``words=2`` a header
        # packet (HPSTART + 16 bytes, 20 symbols) spans 2.5 beats and
        # may start at EITHER beat half (offsets 0/4) -- back-to-back
        # headers alternate phase.  ``words=1`` is verbatim.
        self._words = words

        #
        # I/O port
        #
        self.sink              = USBRawSuperSpeedStream(payload_words=4 * words)

        # Header packet output.
        self.packet            = HeaderPacket()

        # State indications.
        self.new_packet        = Signal()
        self.bad_packet        = Signal()

        # Sequence tracking.
        self.expected_sequence = Signal(4 if gen2 else 3)
        self.bad_sequence      = Signal()


    def elaborate(self, platform):
        m = Module()

        if self._words == 2:
            return self._elaborate_wide(m)

        sink   = self.sink

        # Store our header packet in progress; which we'll output only once it's been validated.
        packet = HeaderPacket()

        # Cache our expected CRC5, so we can pipeline generation and comparison.
        expected_crc5 = Signal(5)

        # Keep our "new packet" signal de-asserted unless asserted explicitly.
        m.d.ss += self.new_packet.eq(0)

        #
        # CRC-16 Generator
        #
        m.submodules.crc16 = crc16 = HeaderPacketCRC()
        m.d.comb += crc16.data_input.eq(sink.data),


        #
        # Receiver Sequencing
        #
        is_hpstart = stream_matches_symbols(sink, SHP, SHP, SHP, EPF)

        with m.FSM(domain="ss"):

            # WAIT_FOR_HPSTART -- we're currently waiting for HPSTART framing, which indicates
            # that the following 16 symbols (4 words) will be a header packet.
            with m.State("WAIT_FOR_HPSTART"):

                # Don't start our CRC until we're past our HPSTART header.
                m.d.comb += crc16.clear.eq(1)

                with m.If(is_hpstart):
                    m.next = "RECEIVE_DW0"

            # RECEIVE_DWn -- the first three words of our header packet are data words meant form
            # the protocol layer; we'll receive them so we can pass them on to the protocol layer.
            for n in range(3):
                with m.State(f"RECEIVE_DW{n}"):

                    with m.If(sink.valid):
                        m.d.comb += crc16.advance_crc.eq(1)
                        m.d.ss += packet[f'dw{n}'].eq(sink.data)
                        m.next = f"RECEIVE_DW{n+1}"

            # RECEIVE_DW3 -- we'll receive and parse our final data word, which contains the fields
            # relevant to the link layer.
            with m.State("RECEIVE_DW3"):

                with m.If(sink.valid):
                    m.d.ss += [
                        # Collect the fields from the DW...
                        packet.crc16            .eq(sink.data[ 0:16]),
                        packet.sequence_number  .eq(sink.data[16:19]),
                        packet.dw3_reserved     .eq(sink.data[19:22]),
                        packet.hub_depth        .eq(sink.data[22:25]),
                        packet.delayed          .eq(sink.data[25]),
                        packet.deferred         .eq(sink.data[26]),
                        packet.crc5             .eq(sink.data[27:32]),

                        # ... and pipeline a CRC of the to the link control word.
                        expected_crc5           .eq(compute_usb_crc5(sink.data[16:27]))
                    ]

                    m.next = "CHECK_PACKET"

            # CHECK_PACKET -- we've now received our full packet; we'll check it for validity.
            with m.State("CHECK_PACKET"):

                # A minor error occurs if if one of our CRCs mismatches; in which case the link can
                # continue after sending an LBAD link command. [USB3.2r1: 7.2.4.1.5].
                # We'll strobe our less-severe "bad packet" indicator, but still reject the header.
                crc5_failed  = (expected_crc5 != packet.crc5)
                crc16_failed = (crc16.crc     != packet.crc16)
                with m.If(crc5_failed | crc16_failed):
                    m.d.comb += self.bad_packet.eq(1)

                # Our worst-case scenario is we're receiving a packet with an unexpected sequence
                # number; this indicates that we've lost sequence, and our device should move back to
                # into Recovery [USB3.2r1: 7.2.4.1.5].
                if not self._gen2:
                    rx_sequence = packet.sequence_number
                else:
                    rx_sequence = Cat(packet.sequence_number,
                                      packet.dw3_reserved[0])
                with m.Elif(rx_sequence != self.expected_sequence):
                    m.d.comb += self.bad_sequence.eq(1)

                # If neither of the above checks failed, we now know we have a valid header packet!
                # We'll output our packet, and then return to IDLE.
                with m.Else():
                    m.d.ss += [
                        self.new_packet  .eq(1),
                        self.packet      .eq(packet)
                    ]

                # A new header packet may begin on this very cycle: nothing requires
                # the link partner to leave a gap between consecutive header packets,
                # and a host under load packs them back to back.  Treating this cycle
                # as blind silently drops that header, desequencing the link (the
                # next header triggers bad_sequence -> Recovery).  Restart reception
                # immediately; our (registered) CRC clear below takes effect next
                # cycle, after the comparisons above have already used this packet's
                # running CRC.
                with m.If(is_hpstart):
                    m.d.comb += crc16.clear.eq(1)
                    m.next = "RECEIVE_DW0"
                with m.Else():
                    m.next = "WAIT_FOR_HPSTART"


        return m


    def _elaborate_wide(self, m):
        """ The words=2 receiver: a half-phase walker.

        Beat layouts (H0 = symbols 0-3, H1 = symbols 4-7):

          offset 0: [HPSTART|DW0] [DW1|DW2] [DW3|tail]
          offset 4: [....|HPSTART] [DW0|DW1] [DW2|DW3]

        A 20-symbol header is an odd number of halves, so back-to-back
        headers ALTERNATE phase: the offset-0 tail may itself be the
        next header's HPSTART, and an offset-4 header ends beat-aligned
        with the next header free to start at either half of the next
        beat.  There is no separate CHECK state: the validity checks
        run in the DW3 beat (the running CRC-16 is committed through
        DW2 for offset 0; the offset-4 case -- DW2 and DW3 in the SAME
        beat -- uses the CRC's combinational one-word lookahead), and
        the outcome strobes register out one cycle after the DW3 beat,
        exactly the narrow unit's relative timing.
        """
        sink = self.sink

        packet = HeaderPacket()

        m.d.ss += [
            self.new_packet   .eq(0),
            self.bad_packet   .eq(0),
            self.bad_sequence .eq(0),
        ]

        #
        # CRC-16 Generator (wide surface: one- and two-word advances,
        # plus the one-word combinational lookahead).
        #
        m.submodules.crc16 = crc16 = HeaderPacketCRC(words=2)
        m.d.comb += crc16.data_input2.eq(sink.data)

        hpstart_low  = half_matches_symbols(sink, 0, SHP, SHP, SHP, EPF)
        hpstart_high = half_matches_symbols(sink, 1, SHP, SHP, SHP, EPF)

        low  = sink.data.word_select(0, 32)
        high = sink.data.word_select(1, 32)

        def finish(dw3, crc16_value, dw2_now=None):
            """The end-of-packet actions: validity checks against the
            given (possibly lookahead) CRC-16, then the outcome
            strobes.  ``dw2_now``: for the offset-4 case DW2 arrives in
            this very beat -- the intermediate ``packet`` record is one
            cycle stale for it, so it is spliced in directly."""
            crc5_ok  = (dw3[27:32] == compute_usb_crc5(dw3[16:27]))
            crc16_ok = (crc16_value == dw3[0:16])
            if not self._gen2:
                rx_sequence = dw3[16:19]
            else:
                rx_sequence = Cat(dw3[16:19], dw3[19])
            seq_ok = (rx_sequence == self.expected_sequence)

            with m.If(~crc5_ok | ~crc16_ok):
                m.d.ss += self.bad_packet.eq(1)
            with m.Elif(~seq_ok):
                m.d.ss += self.bad_sequence.eq(1)
            with m.Else():
                m.d.ss += [
                    self.new_packet .eq(1),
                    self.packet     .eq(packet),
                    self.packet.crc16           .eq(dw3[ 0:16]),
                    self.packet.sequence_number .eq(dw3[16:19]),
                    self.packet.dw3_reserved    .eq(dw3[19:22]),
                    self.packet.hub_depth       .eq(dw3[22:25]),
                    self.packet.delayed         .eq(dw3[25]),
                    self.packet.deferred        .eq(dw3[26]),
                    self.packet.crc5            .eq(dw3[27:32]),
                ]
                if dw2_now is not None:
                    m.d.ss += self.packet.dw2.eq(dw2_now)

        with m.FSM(domain="ss"):

            # WAIT -- no header in progress; a header may start in
            # either half of the next valid beat.
            with m.State("WAIT"):
                m.d.comb += crc16.clear.eq(1)
                with m.If(sink.valid):
                    with m.If(hpstart_low):
                        # [HPSTART|DW0]: DW0 enters the CRC now.
                        # (clear + advance would collide -- but the CRC
                        # register is already at its initial value in
                        # WAIT, so simply suppress the clear and
                        # advance over DW0.)
                        m.d.comb += [
                            crc16.clear       .eq(0),
                            crc16.data_input  .eq(high),
                            crc16.advance_crc .eq(1),
                        ]
                        m.d.ss += packet.dw0.eq(high)
                        m.next = "P0_MID"
                    with m.Elif(hpstart_high):
                        m.next = "P4_DW01"

            # P0_MID -- offset-0 body beat: [DW1|DW2].
            with m.State("P0_MID"):
                with m.If(sink.valid):
                    m.d.comb += crc16.advance_crc2.eq(1)
                    m.d.ss += [
                        packet.dw1.eq(low),
                        packet.dw2.eq(high),
                    ]
                    m.next = "P0_END"

            # P0_END -- offset-0 final beat: [DW3|tail].  The running
            # CRC is committed through DW2; check directly.  The tail
            # may already be the next header's HPSTART (phase flip).
            with m.State("P0_END"):
                with m.If(sink.valid):
                    finish(low, crc16.crc)
                    m.d.comb += crc16.clear.eq(1)
                    with m.If(hpstart_high):
                        m.next = "P4_DW01"
                    with m.Else():
                        m.next = "WAIT"

            # P4_DW01 -- offset-4 body beat: [DW0|DW1].
            with m.State("P4_DW01"):
                with m.If(sink.valid):
                    m.d.comb += crc16.advance_crc2.eq(1)
                    m.d.ss += [
                        packet.dw0.eq(low),
                        packet.dw1.eq(high),
                    ]
                    m.next = "P4_END"

            # P4_END -- offset-4 final beat: [DW2|DW3].  DW2 and DW3
            # arrive together: the CRC-16 comparison uses the
            # combinational one-word lookahead over DW2.  The packet
            # ends beat-aligned; the next may start at either half of
            # the next beat (back to WAIT).
            with m.State("P4_END"):
                with m.If(sink.valid):
                    m.d.comb += crc16.data_input.eq(low)
                    finish(high, crc16.crc_after_word, dw2_now=low)
                    m.d.comb += crc16.clear.eq(1)
                    m.next = "WAIT"

        return m


class HeaderPacketReceiver(Elaboratable):
    """ Receiver-side Header Packet logic.

    This module handles all header-packet-reception related logic for the link layer; including
    header packet reception, buffering, flow control (credit management), and link command transmission.

    Attributes
    ----------
    sink: USBRawSuperSpeedStream(), input stream [monitor only]
        Stream that carries data from the physical layer, to be monitored.
    source: USBRawSuperSpeedStream(), output stream
        Stream that carries link commands from this unit down down to the physical layer.

    enable: Signal(), input
        When asserted, this unit will be enabled; and will be allowed to start
        transmitting link commands. Asserting this signal after a reset will perform
        a header sequence and link credit advertisement.
    usb_reset: Signal(), input
        Strobe; can be asserted to indicate that a USB reset has occurred, and sequencing
        should be restarted.

    queue: HeaderQueue(), output stream
        Stream carrying any header packets to be transmitted.

    retry_received: Signal(), input
        Strobe; should be asserted when the transmitter has seen a RETRY handshake.
    retry_required: Signal(), output
        Strobe; pulsed to indicate that we should send a RETRY handshake.

    link_command_sent: Signal(), output
        Strobe; pulses each time a link command is completed.
    keepalive_required: Signal(), input
        Strobe; when asserted; a keepalive packet will be generated.
    packet_received: Signal(), output
        Strobe; pulsed when an event occurs that should reset the USB3 "packet received" timers.
        This does *not* indicate valid data is present on the output :attr:``queue``; this has its
        own valid signal.
    bad_packet_received: Signal(), output
        Strobe; pulsed when a receive error occurs. For error counting at the link level.

    accept_power_state: Signal(), input
        Strobe; when pulsed, a LAU (Link-state acceptance) will be generated.
    reject_power_state: Signal(), input
        Strobe; when pulsed, a LXU (Link-state rejection) will be generated.
    acknowledge_power_state: Signal(), input
        Strobe; when pulsed, a LPMA (Link-state acknowledgement) will be generated.
    """

    SEQUENCE_NUMBER_WIDTH = 3

    def __init__(self, *, buffer_count=4, downstream_facing=False,
                 gen2=False):
        self._buffer_count = buffer_count
        self._is_downstream_facing = downstream_facing
        # SuperSpeedPlus trims [USB3.2r1: 7.2.4.1.x]: modulo-16 header
        # sequence numbers (LGOOD_0..15) and the LCRD1/LCRD2 credit
        # class split.  gen2_active selects them at runtime; at the SS
        # rate the device follows the SuperSpeed rules.
        self._gen2 = gen2

        #
        # I/O port
        #
        self.sink                    = USBRawSuperSpeedStream()
        self.source                  = USBRawSuperSpeedStream()

        # Simple controls.
        self.enable                  = Signal()
        self.usb_reset               = Signal()

        # Header Packet Queue
        self.queue                   = HeaderQueue()

        # Event signaling.
        self.retry_received          = Signal()
        self.lrty_pending            = Signal()
        self.retry_required          = Signal()
        self.recovery_required       = Signal()

        self.link_command_sent       = Signal()
        self.keepalive_required      = Signal()
        self.packet_received         = Signal()
        self.bad_packet_received     = Signal()

        self.accept_power_state      = Signal()
        self.reject_power_state      = Signal()
        self.acknowledge_power_state = Signal()

        # High when operating at the SuperSpeedPlus rate (gen2 builds).
        self.gen2_active             = Signal()

        # Debug taps (prunable).
        self.debug_expected_seq      = Signal(3)
        self.debug_rx_seq            = Signal(3)
        self.debug_new_packet        = Signal()


    def elaborate(self, platform):
        m = Module()

        #
        # Sequence tracking.
        #

        seq_width = 4 if self._gen2 else self.SEQUENCE_NUMBER_WIDTH
        if self._gen2:
            seq_mask = Mux(self.gen2_active, 0xF, 0x7)

        # Keep track of which sequence number we expect to see.
        expected_sequence_number = Signal(seq_width)

        # Keep track of which credit we'll need to issue next...
        next_credit_to_issue     = Signal(range(self._buffer_count))
        if self._gen2:
            # The LCRD2 (Type 2 -- asynchronous DP) series' independent
            # A-D index [Table 7-4].
            next_credit2_to_issue = Signal(range(self._buffer_count))

        # ... and which header we'll need to ACK next.
        # We'll start with the maximum number, so our first advertisement wraps us back around to zero.
        next_header_to_ack       = Signal.like(expected_sequence_number, init=-1)


        #
        # Task "queues".
        #

        # Keep track of how many header received acknowledgements (LGOODs) we need to send.
        #
        # This backlog can exceed the buffer count: our link-command stream
        # only gets the wire between packet transmissions (and yields it
        # after every single command, as the command generator drops
        # ``valid`` between commands), so while long data packets stream
        # out, LGOODs for freshly received headers queue up.  The link
        # partner may hold up to ``buffer_count`` headers outstanding and
        # keeps sending as LCRDs return, so the transient backlog is
        # bounded by roughly twice the buffer count.  A counter sized to
        # ``buffer_count`` wraps under concurrent multi-endpoint traffic,
        # silently discarding eight LGOODs at a time -- undetectable by the
        # 3-bit sequence check, but the partner's PENDING_HP_TIMER then
        # forces link recovery.  Size it with generous headroom.
        acks_to_send      = Signal(range(4 * self._buffer_count + 1), init=1)
        enqueue_ack       = Signal()
        dequeue_ack       = Signal()

        with m.If(enqueue_ack & ~dequeue_ack):
            m.d.ss += acks_to_send.eq(acks_to_send + 1)
        with m.If(dequeue_ack & ~enqueue_ack):
            m.d.ss += acks_to_send.eq(acks_to_send - 1)


        # Keep track of how many link credits we've yet to free.
        # We'll start with every one of our buffers marked as "pending free"; this ensures
        # we perform our credit restoration properly.
        # (Pending credits are structurally bounded by the buffer count --
        # a buffer cannot be refilled before its credit is announced -- but
        # share the generous sizing above for uniformity.)
        credits_to_issue  = Signal.like(acks_to_send, init=self._buffer_count)
        enqueue_credit_issue = Signal()
        dequeue_credit_issue = Signal()

        with m.If(enqueue_credit_issue & ~dequeue_credit_issue):
            m.d.ss += credits_to_issue.eq(credits_to_issue + 1)
        with m.If(dequeue_credit_issue & ~enqueue_credit_issue):
            m.d.ss += credits_to_issue.eq(credits_to_issue - 1)

        if self._gen2:
            # Type 2 (asynchronous DP) credit-issue queue; at the SSP
            # rate the 8-buffer pool is split 4+4 between the classes
            # (both advertised in full; the A-D indices run
            # independently).  The 4-per-class count is NOT a sizing
            # choice: a port entering U0 from Polling or Hot Reset has
            # its Local Type 1/Type 2 Rx Buffer Credit Counts AT 4
            # [7.2.4.1.1 rule 2.e.1] and shall advertise LCRD1_A..D +
            # LCRD2_A..D [rule 3.d]; the partner's Type 1/Type 2
            # CREDIT_HP_TIMERs clear only at count 4 and their expiry
            # forces Recovery [7.3.9] (bug #42: with the earlier 2+2
            # split a real xHC never sent a single header packet and
            # walked the link down).  At the SS rate everything is
            # Type 1 (4 credits, LCRD_A..D) and this queue idles.
            credits2_to_issue     = Signal.like(acks_to_send)
            enqueue_credit2_issue = Signal()
            dequeue_credit2_issue = Signal()

            with m.If(enqueue_credit2_issue & ~dequeue_credit2_issue):
                m.d.ss += credits2_to_issue.eq(credits2_to_issue + 1)
            with m.If(dequeue_credit2_issue & ~enqueue_credit2_issue):
                m.d.ss += credits2_to_issue.eq(credits2_to_issue - 1)

            # Per-class pool sizes (runtime-selected by operating rate).
            pool1_size = Signal(3)
            pool2_size = Signal(3)
            m.d.comb += [
                pool1_size.eq(4),
                pool2_size.eq(Mux(self.gen2_active, 4, 0)),
            ]

        # Keep track of whether we should be sending an LBAD.
        lbad_pending = Signal()

        # Keep track of whether a retry has been requested.
        lrty_pending = self.lrty_pending
        with m.If(self.retry_required):
            m.d.ss += lrty_pending.eq(1)

        # Keep track of whether a keepalive has been requested.
        keepalive_pending = Signal()
        with m.If(self.keepalive_required):
            m.d.ss += keepalive_pending.eq(1)

        # Keep track of whether we're expected to send an power state response.
        lau_pending  = Signal()
        lxu_pending  = Signal()
        lpma_pending = Signal()

        with m.If(self.accept_power_state):
            m.d.ss += lau_pending.eq(1)
        with m.If(self.reject_power_state):
            m.d.ss += lxu_pending.eq(1)
        with m.If(self.acknowledge_power_state):
            m.d.ss += lpma_pending.eq(1)

        # Keep track of the last value of the enable signal
        last_enable = Signal()
        m.d.ss     += last_enable.eq(self.enable)

        #
        # Header Packet Buffers
        #

        # Track which buffer will be filled next.
        read_pointer      = Signal(range(self._buffer_count))
        write_pointer     = Signal.like(read_pointer)

        # Track how many buffers we currently have in use.
        buffers_filled    = Signal.like(credits_to_issue, init=0)
        reserve_buffer    = Signal()
        release_buffer    = Signal()

        with m.If(reserve_buffer & ~release_buffer):
            m.d.ss += buffers_filled.eq(buffers_filled + 1)
        with m.If(release_buffer & ~reserve_buffer):
            m.d.ss += buffers_filled.eq(buffers_filled - 1)

        # Create buffers to receive any incoming header packets.
        buffers = Array(HeaderPacket() for _ in range(self._buffer_count))

        if self._gen2:
            # Per-slot traffic class of the buffered header, and
            # per-class fill counts (for the per-class credit
            # re-advertisement after a link-down).
            type2_flags = Array(Signal(name=f"hdr_type2_{i}")
                                for i in range(self._buffer_count))
            filled2 = Signal.like(buffers_filled)
            reserve2 = Signal()
            release2 = Signal()
            with m.If(reserve2 & ~release2):
                m.d.ss += filled2.eq(filled2 + 1)
            with m.If(release2 & ~reserve2):
                m.d.ss += filled2.eq(filled2 - 1)


        #
        # Packet reception (physical layer -> link layer).
        #

        # Flag that determines when we should ignore packets.
        #
        # After a receive error, we'll want to ignore all packets until we see a "retry"
        # link command; so we don't receive packets out of order.
        ignore_packets = Signal()

        # Create our raw packet parser / receiver.
        #
        # It is held in reset while the link is down: a header truncated
        # by a retrain must not leave the parser mid-packet, where it
        # would misinterpret training/idle words (or the first fresh
        # header) as the remainder of the old one.
        m.submodules.receiver = rx = \
            ResetInserter({"ss": ~self.enable})(
                RawHeaderPacketReceiver(gen2=self._gen2))
        m.d.comb += [
            # Our receiver passively monitors the data received for header packets.
            rx.sink                   .tap(self.sink),

            # Ensure it's always up to date about what sequence numbers we expect.
            rx.expected_sequence      .eq(expected_sequence_number),

            # If we ever get a bad header packet sequence, we're required to retrain
            # the link [USB3.2r1: 7.2.4.1.5]. Pass the event through directly.
            self.recovery_required    .eq(rx.bad_sequence & ~ignore_packets),

            # Notify the link layer when packets are received, for keeping track of our timers.
            self.packet_received      .eq(rx.new_packet),

            # Notify the link layer if any bad packets are received; for diagnostics.
            self.bad_packet_received  .eq(rx.bad_packet),

            # Debug taps.
            self.debug_expected_seq   .eq(expected_sequence_number),
            self.debug_rx_seq         .eq(rx.packet.sequence_number),
            self.debug_new_packet     .eq(rx.new_packet),
        ]


        # If we receive a valid packet, it's time for us to buffer it!
        with m.If(rx.new_packet & ~ignore_packets):
            m.d.ss += [
                # Load our header packet into the next write buffer...
                buffers[write_pointer]    .eq(rx.packet),

                # ... advance to the next buffer and sequence number...
                write_pointer             .eq(write_pointer + 1),
            ]
            if not self._gen2:
                m.d.ss += expected_sequence_number.eq(expected_sequence_number + 1)
            else:
                m.d.ss += [
                    expected_sequence_number
                        .eq((expected_sequence_number + 1) & seq_mask),
                    type2_flags[write_pointer]
                        .eq(self.gen2_active & (rx.packet.dw0[0:5] == 8)),
                ]
                m.d.comb += reserve2.eq(self.gen2_active
                                        & (rx.packet.dw0[0:5] == 8))
            m.d.comb += [
                # ... mark the buffer space as occupied by valid data ...
                reserve_buffer            .eq(1),

                # ... and queue an ACK for this packet.
                enqueue_ack               .eq(1)
            ]


        # If we receive a bad packet, we'll need to request that the other side re-send.
        # The rules for this are summarized in [USB3.2r1: 7.2.4.1.5], and in comments below.
        with m.If(rx.bad_packet & ~ignore_packets):


            m.d.ss += [
                # First, we'll need to schedule transmission of an LBAD, which notifies the other
                # side that we received a bad packet; and that it'll need to transmit all unack'd
                # header packets to us again.
                lbad_pending    .eq(1),

                # Next, we'll need to make sure we don't receive packets out of sequence. This means
                # we'll have to start ignoring packets until the other side responds to the LBAD.
                # The other side respond with an Retry link command (LRTY) once it's safe for us to
                # pay attention to packets again.
                ignore_packets  .eq(1)
            ]


        # Finally, if we receive a Retry link command, this means we no longer need to ignore packets.
        # This typically happens in response to us sending an LBAD and marking future packets as ignored.
        with m.If(self.retry_received):
            m.d.ss += ignore_packets.eq(0)


        #
        # Packet delivery (link layer -> physical layer).
        #
        m.d.comb += [
            # As long as we have at least one buffer filled, we have header packets pending.
            self.queue.valid    .eq(buffers_filled > 0),

            # Always provide the value of our oldest packet out to our consumer.
            self.queue.header    .eq(buffers[read_pointer])
        ]


        # If the protocol layer is marking one of our packets as consumed, we no longer
        # need to buffer it -- it's the protocol layer's problem, now!
        with m.If(self.queue.valid & self.queue.ready):

            # Move on to reading from the next buffer in sequence.
            m.d.ss += read_pointer.eq(read_pointer + 1)

            if not self._gen2:
                m.d.comb += [
                    # First, we'll free the buffer associated with the relevant packet...
                    release_buffer        .eq(1),

                    # ... and request that our link partner be notified of the new space.
                    enqueue_credit_issue  .eq(1)
                ]
            else:
                # The freed credit returns to the class the drained
                # header belonged to.
                m.d.comb += [
                    release_buffer        .eq(1),
                    release2              .eq(type2_flags[read_pointer]),
                    enqueue_credit_issue  .eq(~type2_flags[read_pointer]),
                    enqueue_credit2_issue .eq(type2_flags[read_pointer]),
                ]


        #
        # Link command generation.
        #
        # The generator is held in reset while the link is down: a link
        # command caught mid-transmission by a retrain (the arbiter
        # switches to training sets and stalls our stream) would
        # otherwise sit in the generator and be emitted -- stale -- onto
        # the freshly retrained link, ahead of the sequence/credit
        # advertisements.  Observed as a pre-recovery LCRD_n leaking out
        # after re-entry, desynchronizing the partner's credit index.
        m.submodules.lc_generator = lc_generator = \
            ResetInserter({"ss": ~self.enable})(LinkCommandGenerator())
        m.d.comb += [
            self.source             .stream_eq(lc_generator.source),
            self.link_command_sent  .eq(lc_generator.done),
        ]


        with m.FSM(domain="ss"):

            # DISPATCH_COMMAND -- the state in which we identify any pending link commands necessary,
            # and then move to the state in which we'll send them.
            with m.State("DISPATCH_COMMAND"):

                with m.If(self.enable):
                    # NOTE: the order below is important; changing it can easily break things:
                    # - ACKS must come before credits, as we must send an LGOOD before we send our initial credits.
                    # - LBAD must come after ACKs and credit management, as all scheduled ACKs need to be
                    #   sent to the other side for the LBAD to have the correct semantic meaning.

                    with m.If(lrty_pending):
                        m.next = "SEND_LRTY"

                    # If we have acknowledgements to send, send them.
                    with m.Elif(acks_to_send):
                        m.next = "SEND_ACKS"

                    # If we have link credits to issue, move to issuing them to the other side.
                    with m.Elif(credits_to_issue if not self._gen2
                                else (credits_to_issue | credits2_to_issue)):
                        m.next = "ISSUE_CREDITS"

                    # If we need to send an LBAD, do so.
                    with m.Elif(lbad_pending):
                        m.next = "SEND_LBAD"

                    # If we need to send a link power-state command, do so.
                    with m.Elif(lxu_pending):
                        m.next = "SEND_LXU"

                    # If we need to send a keepalive, do so.
                    with m.Elif(keepalive_pending):
                        m.next = "SEND_KEEPALIVE"


            # SEND_ACKS -- a valid header packet has been received, or we're advertising
            # our initial sequence number; send an LGOOD packet.
            with m.State("SEND_ACKS"):

                # Send an LGOOD command, acknowledging the last received packet header.
                m.d.comb += [
                    lc_generator.generate      .eq(1),
                    lc_generator.command       .eq(LinkCommand.LGOOD),
                    lc_generator.subtype       .eq(
                        next_header_to_ack if not self._gen2
                        else next_header_to_ack & seq_mask)
                ]

                # Wait until our link command is done, and then re-arbitrate.
                with m.If(lc_generator.done):
                    # Move to the next header packet in the sequence, and decrease
                    # the number of outstanding ACKs.
                    m.d.comb += dequeue_ack         .eq(1)
                    if not self._gen2:
                        m.d.ss += next_header_to_ack.eq(next_header_to_ack + 1)
                    else:
                        m.d.ss += next_header_to_ack.eq(
                            (next_header_to_ack + 1) & seq_mask)

                    # Return to dispatch after *every* command, so the queues
                    # are re-arbitrated by priority: staying while our own
                    # queue is non-empty starves the other queues whenever
                    # ours is continuously replenished by ongoing traffic.
                    m.next = "DISPATCH_COMMAND"

                # A link drop aborts the command (the generator is reset);
                # dispatch runs fresh -- with re-initialized queues -- on
                # the next link-up.
                with m.If(~self.enable):
                    m.next = "DISPATCH_COMMAND"


            # ISSUE_CREDITS -- header packet buffers have been freed; and we now need to notify the
            # other side, so it knows we have buffers available.
            with m.State("ISSUE_CREDITS"):

                if not self._gen2:
                    # Send an LCRD command, indicating that we have a free buffer.
                    m.d.comb += [
                        lc_generator.generate      .eq(1),
                        lc_generator.command       .eq(LinkCommand.LCRD),
                        lc_generator.subtype       .eq(next_credit_to_issue)
                    ]

                    # Wait until our link command is done, and then re-arbitrate.
                    with m.If(lc_generator.done):
                        # Move to the next credit...
                        m.d.comb += dequeue_credit_issue  .eq(1)
                        m.d.ss   += next_credit_to_issue  .eq(next_credit_to_issue + 1)

                        # Re-arbitrate by priority after every command (see
                        # SEND_ACKS): under sustained traffic the credit queue
                        # refills continuously, and looping here starves the
                        # pending-LGOOD queue -- the link partner then never
                        # sees its headers acknowledged and (on real hosts) its
                        # PENDING_HP_TIMER forces link recovery.
                        m.next = "DISPATCH_COMMAND"
                else:
                    # Two independent credit series [Table 7-4]: LCRD_x/
                    # LCRD1_x (subtype b2 clear) and LCRD2_x (b2 set).
                    # Their A-D indices advance independently, modulo 4.
                    issue2 = Signal()
                    m.d.comb += [
                        issue2.eq(~credits_to_issue.any()
                                  & credits2_to_issue.any()),
                        lc_generator.generate      .eq(1),
                        lc_generator.command       .eq(LinkCommand.LCRD),
                        lc_generator.subtype       .eq(Mux(
                            issue2,
                            Cat(next_credit2_to_issue[0:2], C(1, 1)),
                            Cat(next_credit_to_issue[0:2], C(0, 1)))),
                    ]

                    with m.If(lc_generator.done):
                        with m.If(issue2):
                            m.d.comb += dequeue_credit2_issue .eq(1)
                            m.d.ss   += next_credit2_to_issue \
                                .eq(next_credit2_to_issue + 1)
                        with m.Else():
                            m.d.comb += dequeue_credit_issue  .eq(1)
                            m.d.ss   += next_credit_to_issue  \
                                .eq(next_credit_to_issue + 1)

                        # Re-arbitrate by priority after every command
                        # (see SEND_ACKS).
                        m.next = "DISPATCH_COMMAND"

                # Aborted by a link drop (see SEND_ACKS).
                with m.If(~self.enable):
                    m.next = "DISPATCH_COMMAND"


            # SEND_LBAD -- we've received a bad header packet; we'll need to let the other side know.
            with m.State("SEND_LBAD"):
                m.d.comb += [
                    lc_generator.generate      .eq(1),
                    lc_generator.command       .eq(LinkCommand.LBAD),
                ]

                # Once we've sent the LBAD, we can mark is as no longer pending and return to our dispatch.
                # (We can't ever have multiple LBADs queued up; as we ignore future packets after sending one.)
                with m.If(lc_generator.done):
                    m.d.ss += lbad_pending.eq(0)
                    m.next = "DISPATCH_COMMAND"

                # Aborted by a link drop (see SEND_ACKS).
                with m.If(~self.enable):
                    m.next = "DISPATCH_COMMAND"


            # SEND_LRTY -- our transmitter has requested that we send an retry indication to the other side.
            # We'll do our transmitter a favor and do so.
            with m.State("SEND_LRTY"):
                m.d.comb += [
                    lc_generator.generate      .eq(1),
                    lc_generator.command       .eq(LinkCommand.LRTY)
                ]

                with m.If(lc_generator.done):
                    m.d.ss += lrty_pending.eq(0)
                    m.next = "DISPATCH_COMMAND"

                # Aborted by a link drop (see SEND_ACKS).
                with m.If(~self.enable):
                    m.next = "DISPATCH_COMMAND"



            # SEND_KEEPALIVE -- our link layer timer has requested that we send a keep-alive,
            # indicating that we're still in U0 and the link is still good. Do so.
            with m.State("SEND_KEEPALIVE"):

                # Send the correct packet type for the direction our port is facing.
                command = LinkCommand.LDN if self._is_downstream_facing else LinkCommand.LUP

                m.d.comb += [
                    lc_generator.generate      .eq(1),
                    lc_generator.command       .eq(command)
                ]

                # Once we've send the keepalive, we can mark is as no longer pending and return to our dispatch.
                # (There's no sense in sending repeated keepalives; one gets the message across.)
                with m.If(lc_generator.done):
                    m.d.ss += keepalive_pending.eq(0)
                    m.next = "DISPATCH_COMMAND"

                # Aborted by a link drop (see SEND_ACKS).
                with m.If(~self.enable):
                    m.next = "DISPATCH_COMMAND"


            # SEND_LXU -- we're being instructed to reject a requested power-state transfer.
            # We'll send an LXU packet to inform the other side of the rejection.
            with m.State("SEND_LXU"):
                m.d.comb += [
                    lc_generator.generate      .eq(1),
                    lc_generator.command       .eq(LinkCommand.LXU)
                ]

                with m.If(lc_generator.done):
                    m.d.ss += lxu_pending.eq(0)
                    m.next = "DISPATCH_COMMAND"

                # Aborted by a link drop (see SEND_ACKS).
                with m.If(~self.enable):
                    m.next = "DISPATCH_COMMAND"


        #
        # Disable (link-down) preparation.
        #
        # This must run regardless of the FSM state: the historical
        # placement inside DISPATCH_COMMAND missed the one-shot disable
        # edge whenever the link dropped while a link command was being
        # sent (SEND_ACKS / ISSUE_CREDITS under load) -- no advertisement
        # was prepared, and the interrupted stale command leaked onto the
        # retrained link.  Placed after the FSM so it takes priority over
        # any same-cycle state assignment.
        #
        # Once we've become disabled, we'll want to prepare for our next
        # enable.  This means preparing for our advertisement, by:
        if self._gen2:
            # Rate-aware credit fixup on every link-up edge: the
            # elaboration-time init (4+0, the SS trim) cannot know the
            # operating rate; recompute the per-class advertisement
            # against the pools selected by ``gen2_active`` (idempotent
            # with the link-down recomputation below -- both derive the
            # same counts from the per-class fill levels).
            with m.If(self.enable & ~last_enable):
                filled1_now = buffers_filled - filled2
                m.d.ss += [
                    credits_to_issue  .eq(pool1_size - filled1_now
                                          + (release_buffer & ~release2)),
                    credits2_to_issue .eq(pool2_size - filled2 + release2),
                ]

        with m.If((last_enable & ~self.enable) | self.usb_reset):
            m.d.ss += [
                # -Resetting our pending ACKs to 1, so we perform a sequence number advertisement
                #  when we're next enabled.
                acks_to_send          .eq(1),

                # -The advertisement must carry the sequence number of the last header packet we
                #  received PROPERLY [USB3.2r1: 7.2.4.1.x] -- that is ``expected_sequence_number - 1``,
                #  NOT ``next_header_to_ack - 1``: the latter lags by the pending-LGOOD backlog, and
                #  under-advertising makes the partner retransmit headers we already received and
                #  processed (observed as an immediate bad-sequence recovery loop after re-entry:
                #  we under-advertise, the partner resends one header too many, and its next fresh
                #  header then looks like a sequence skip).
                #
                #  Bug #50 (session 17, the #49 reccut red): the acceptance
                #  block above is NOT gated by ``enable`` -- a header whose
                #  parse completes in the FIRST link-down cycle (its
                #  ``new_packet`` strobe registered at the last enabled
                #  edge) is properly accepted, buffered and delivered
                #  (rule 2d), and ``expected_sequence_number`` advances --
                #  but this one-shot prep runs in the SAME cycle and read
                #  the PRE-acceptance value: the advertisement then
                #  under-reports by one, the partner (per rule 7)
                #  retransmits a header we already counted, and our
                #  receiver calls it a bad sequence -> device-initiated
                #  recovery loop, wedged EP0 (PHASE=reccut offset-2 red;
                #  the bench BOS/22 EPROTO shape).  Account for the
                #  same-cycle acceptance (``reserve_buffer`` is exactly
                #  the acceptance strobe).  Gen2 elaborations only; the
                #  Gen1 rail keeps the historical statement verbatim (the
                #  shipping fence) -- the twin fix is a parked item.
                next_header_to_ack    .eq(
                    (expected_sequence_number - 1) if not self._gen2
                    else ((expected_sequence_number + reserve_buffer - 1)
                          & seq_mask)),

                # - RULE 2d [USB3.2r1: 7.2.4.1.x]: header packets already
                #   counted as received (the advertisement above claims
                #   them!) but not yet drained by the protocol layer MUST
                #   still be delivered -- the partner will never
                #   retransmit them.  The buffers, their pointers and the
                #   fill level therefore SURVIVE the link-down; the
                #   protocol layer keeps draining through the normal
                #   queue path while the link retrains.  (The historical
                #   unconditional clear silently dropped any header in
                #   the 1-2 cycle buffer-to-drain window at the moment of
                #   link-down.)
                #
                # - Credits: re-advertise only the buffers that are
                #   actually FREE; the credits for still-occupied buffers
                #   are enqueued by the drain logic as usual (converging
                #   to the full count once drained).  A drain completing
                #   this very cycle is accounted through
                #   ``release_buffer``.
                next_credit_to_issue  .eq(0),

                # - Clear our pending events.
                lrty_pending          .eq(0),
                lbad_pending          .eq(0),
                keepalive_pending     .eq(0),
                ignore_packets        .eq(0)
            ]
            if not self._gen2:
                m.d.ss += credits_to_issue.eq(self._buffer_count
                                              - buffers_filled + release_buffer)
            else:
                # Per-class rule-2d credit recomputation (4+4 pools at
                # the SSP rate, 4+0 at the SS rate).  Bug #50: like the
                # advertisement above, the fill levels must account for
                # a SAME-CYCLE acceptance (``reserve_buffer``/
                # ``reserve2``) -- a header accepted in the first
                # link-down cycle occupies a buffer the historical
                # recomputation still advertised as free, letting the
                # partner oversubscribe the pool after re-entry.
                filled1 = ((buffers_filled + reserve_buffer)
                           - (filled2 + reserve2))
                m.d.ss += [
                    next_credit2_to_issue .eq(0),
                    credits_to_issue      .eq(pool1_size - filled1
                                              + (release_buffer & ~release2)),
                    credits2_to_issue     .eq(pool2_size
                                              - (filled2 + reserve2)
                                              + release2),
                ]

            # If this is a USB Reset, also reset our sequences -- and,
            # unlike a link-down, fully clear the buffers (the protocol
            # state is being torn down; rule 2d does not apply).
            with m.If(self.usb_reset):
                m.d.ss += [
                    expected_sequence_number  .eq(0),
                    next_header_to_ack        .eq(-1),
                    read_pointer              .eq(0),
                    write_pointer             .eq(0),
                    buffers_filled            .eq(0),
                ]
                if not self._gen2:
                    m.d.ss += credits_to_issue.eq(self._buffer_count)
                else:
                    m.d.ss += [
                        credits_to_issue   .eq(pool1_size),
                        credits2_to_issue  .eq(pool2_size),
                        filled2            .eq(0),
                    ]

        return m
