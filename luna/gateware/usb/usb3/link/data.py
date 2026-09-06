#
# This file is part of LUNA.
#
# Copyright (c) 2020 Great Scott Gadgets <info@greatscottgadgets.com>
# SPDX-License-Identifier: BSD-3-Clause
""" Data Packet Payload (DPP) management gateware. """

from amaranth import *

from usb_protocol.types import USBDirection
from usb_protocol.types.superspeed import HeaderPacketType

from .crc              import HeaderPacketCRC, DataPacketPayloadCRC, compute_usb_crc5
from .header           import HeaderPacket, HeaderQueue

from ..physical.coding import SHP, SDP, EPF, stream_matches_symbols, \
    half_matches_symbols
from ...stream         import USBRawSuperSpeedStream, SuperSpeedStreamInterface


class DataHeaderPacket(HeaderPacket):
    DW0_LAYOUT = [
        ('type',                5),
        ('route_string',       20),
        ('device_address',      7),
    ]
    DW1_LAYOUT = [
        ('data_sequence',       5),
        ('reserved_0',          1),
        ('end_of_burst',        1),
        ('direction',           1),
        ('endpoint_number',     4),
        ('reserved_1',          3),
        ('setup',               1),
        ('data_length',        16),
    ]
    DW2_LAYOUT = [
        ('stream_id',          16),
        ('reserved_2',         11),
        ('packet_pending',      1),
        ('reserved_3',          4),
    ]



class DataPacketReceiver(Elaboratable):
    """ Class that monitors the USB bus for data packets, and receives them.

    This class has logic redundant with our Header Packet Receiver, to simplify data packet
    reception. Accordingly, the header section of the data packet will be parsed here as well
    as in the Header Packet receiver. This simplifies our structure at the expense of an additional
    CRC-5 and CRC-16 unit.

    This class performs the validations required at the link layer of the USB specification;
    which include checking the CRC-5 and CRC-16 embedded within the header, and CRC-32 of the
    data packet payload.

    Header sequence number is not checked, here, as a sequence error will force recovery in the
    Header Packet Receiver.


    Attributes
    ----------
    sink: USBRawSuperSpeedStream(), input (monitor only)
        Stream that the USB data to be monitored.

    header: HeaderPacket(), output
        The header packet accompanying the current data packet. Valid once a packet begins
        to be received.
    new_header: Signal(), output
        Strobe; indicates that :attr:``header`` has been updated.
    source: StreamInterface(), output stream
        A stream carrying the data received. Note that the data is not fully validated until
        the packet has been fully received; so this cannot be assumed

    packet_good: Signal(), output
        Strobe; indicates that the packet received passed validations and can be considered good.
    packet_bad: Signal(), output
        Strobe; indicates that the packet failed CRC checks, or did not end properly.
    """

    MAX_PACKET_SIZE = 1024

    def __init__(self, *, gen2=False, words=1):
        # ``gen2``: elaborate the SuperSpeedPlus trim.  At Gen2 the block
        # translation engine (physical/gen2.py) may present valid-gaps
        # ANYWHERE in the translated stream -- including between the last
        # payload word and the CRC-32 word, a boundary the Gen1 wire can
        # never gap on (SKPs are forbidden inside packets [6.4.3]), so the
        # historical CHECK_CRC32 state consumes its word un-gated.  The
        # Gen2 trim qualifies that state with ``sink.valid``; the Gen1
        # elaboration keeps the historical statements verbatim.
        self._gen2 = gen2
        # Width program (usb3_design.md 13.5): ``words=2`` receives
        # 8-symbol beats.  A data packet whose DPH starts at beat
        # offset 0 has its payload beat-aligned ([DW3|DPPSTART] then
        # whole payload beats); an offset-4 DPH ends beat-aligned, its
        # DPPSTART occupies the next beat's LOW half and the payload
        # runs HALF-SKEWED -- the receiver assembles payload beats
        # from consecutive halves.  ``words=1`` is verbatim.
        self._words = words

        #
        # I/O port
        #
        self.sink              = USBRawSuperSpeedStream(payload_words=4 * words)

        # Header and data output.
        self.header            = DataHeaderPacket()
        self.new_header        = Signal()
        self.source            = SuperSpeedStreamInterface(payload_words=4 * words)

        # State indications.
        self.packet_good       = Signal()
        self.packet_bad        = Signal()



    def elaborate(self, platform):
        m = Module()

        if self._words == 2:
            return self._elaborate_wide(m)

        sink   = self.sink
        source = self.source

        # Store our header packet in progress; which we'll output only once it's been validated.
        # We'll store it our generic way; and then refine it as our data becomes valid.
        header = HeaderPacket()

        # Cache our expected CRC5, so we can pipeline generation and comparison.
        expected_crc5 = Signal(5)

        # Store how much data is remaining in the given packet.
        data_bytes_remaining = Signal(range(self.MAX_PACKET_SIZE + 1))

        # Store the most recently received word; which we'll use in case we have an packet which
        # is not evenly divisible into words (e.g. a 3-byte data packet). In these cases, we'll need
        # this previous word for CRC validation, since the final CRC will be partially contained in the
        # last data word.
        previous_word  = Signal.like(self.sink.data)
        previous_valid = Signal.like(self.sink.ctrl)


        #
        # CRC Generators
        #
        m.submodules.crc16 = crc16 = HeaderPacketCRC()
        m.d.comb += crc16.data_input.eq(sink.data),

        m.submodules.crc32 = crc32 = DataPacketPayloadCRC()
        m.d.comb += crc32.data_input.eq(sink.data),

        #
        # Receiver Sequencing
        #
        with m.FSM(domain="ss"):

            # WAIT_FOR_HPSTART -- we're currently waiting for HPSTART framing, which indicates
            # that the following 16 symbols (4 words) will be a header packet.
            with m.State("WAIT_FOR_HPSTART"):

                # Don't start our CRCs until we're past our HPSTART header.
                m.d.comb += [
                    crc16.clear.eq(1),
                    crc32.clear.eq(1),
                ]

                is_hpstart = stream_matches_symbols(sink, SHP, SHP, SHP, EPF)
                with m.If(is_hpstart):
                    m.next = "RECEIVE_DW0"

            # RECEIVE_DWn -- the first three words of our header packet are data words meant form
            # the protocol layer; we'll receive them so we can pass them on to the protocol layer.
            for n in range(3):
                with m.State(f"RECEIVE_DW{n}"):

                    with m.If(sink.valid):
                        m.d.comb += crc16.advance_crc.eq(1)
                        m.d.ss += header[f'dw{n}'].eq(sink.data)
                        m.next = f"RECEIVE_DW{n+1}"

                        # Extra check for our first packet; we'll make sure this of -data- type;
                        # and bail out, otherwise.
                        if n == 0:
                            with m.If(sink.data[0:5] != HeaderPacketType.DATA):
                                m.next = "WAIT_FOR_HPSTART"


            # RECEIVE_DW3 -- we'll receive and parse our final data word, which contains the fields
            # relevant to the link layer.
            with m.State("RECEIVE_DW3"):

                with m.If(sink.valid):
                    m.d.ss += [
                        # Collect the fields from the DW...
                        header.crc16            .eq(sink.data[ 0:16]),
                        header.sequence_number  .eq(sink.data[16:19]),
                        header.dw3_reserved     .eq(sink.data[19:22]),
                        header.hub_depth        .eq(sink.data[22:25]),
                        header.delayed          .eq(sink.data[25]),
                        header.deferred         .eq(sink.data[26]),
                        header.crc5             .eq(sink.data[27:32]),

                        # ... and pipeline a CRC of the to the link control word.
                        expected_crc5           .eq(compute_usb_crc5(sink.data[16:27]))
                    ]

                    m.next = "CHECK_HEADER"

            # CHECK_PACKET -- we've now received our full packet; we'll check it for validity.
            with m.State("CHECK_HEADER"):
                crc5_failed  = (expected_crc5 != header.crc5)
                crc16_failed = (crc16.crc     != header.crc16)

                # If either of our CRCs fail, this isn't going to be followed by a DPP we care about.
                with m.If(crc5_failed | crc16_failed):
                    m.next = "WAIT_FOR_HPSTART"

                # Otherwise, if we have a data packet header, move to capturing our data.
                with m.Elif(stream_matches_symbols(sink, SDP, SDP, SDP, EPF)):
                    m.d.ss += [
                        # Update the header associated with the active packet.
                        self.header           .eq(header),
                        self.new_header       .eq(1),

                        # Read the data length from our header, in preparation to receive it.
                        data_bytes_remaining  .eq(header.dw1[16:]),

                        # Mark the next packet as the first packet in our stream.
                        source.first          .eq(1)
                    ]

                    # Move to receiving data.
                    m.next = "RECEIVE_PAYLOAD"

                # If our data is valid and we're -not- a start of DPP, this isn't for us.
                # Go back to watching for data.
                with m.Elif(sink.valid):
                    m.next = "WAIT_FOR_HPSTART"

            # RECEIVE_PAYLOAD -- receive the core data payload
            with m.State("RECEIVE_PAYLOAD"):
                m.d.comb += [
                    # Pass through most our data directly.
                    source.data         .eq(sink.data),

                    # Manage each of our byte-valid bits directly.
                    source.valid[0]     .eq((data_bytes_remaining > 0) & sink.valid),
                    source.valid[1]     .eq((data_bytes_remaining > 1) & sink.valid),
                    source.valid[2]     .eq((data_bytes_remaining > 2) & sink.valid),
                    source.valid[3]     .eq((data_bytes_remaining > 3) & sink.valid),

                    # Advance our CRC according to how many bytes are currently valid.
                    crc32.advance_word  .eq(source.valid == 0b1111),
                    crc32.advance_3B    .eq(source.valid == 0b0111),
                    crc32.advance_2B    .eq(source.valid == 0b0011),
                    crc32.advance_1B    .eq(source.valid == 0b0001),

                    # Mark this packet as the last one if we've a word or less remaining.
                    source.last         .eq(data_bytes_remaining <= 4)
                ]

                with m.If(sink.valid):
                    # Once we've moved on, this is no longer our first word.
                    m.d.ss += source.first.eq(0)

                    # If we see unexpected control codes in our data packet, bail out.
                    # Note that we'll only check for validity in positions we consider to have
                    # valid data; as we always expect our data packet payload to be followed by
                    # and "end of packet" set of control codes.
                    with m.If((sink.ctrl & source.valid) != 0):
                        m.d.comb += self.packet_bad.eq(1)
                        m.next = "WAIT_FOR_HPSTART"

                    # Capture the current word and valid value, so we can refer to them in
                    # future states. This is necessary for CRC validation when we have a data payload
                    # that's not evenly divisible into words; see the instantiation of ``previous_word``.
                    m.d.ss += [
                        previous_word   .eq(source.data),
                        previous_valid  .eq(source.valid)
                    ]

                    # If we have another word to receive after this, decrement our count,
                    # and continue.
                    with m.If(data_bytes_remaining > 4):
                        m.d.ss += data_bytes_remaining.eq(data_bytes_remaining - 4)

                    with m.Else():
                        m.next = "CHECK_CRC32"


            # CHECK_CRC32 -- we've received the end of our packet; and we're ready to decide if the
            # packet is good or not. We'll check its CRC, and strobe either packet_good or packet_bad.
            with m.State("CHECK_CRC32"):
                data_to_check = Signal.like(sink.data)

                # Depending on how many bytes were present in our data packet, our CRC may be partially
                # contained in the previous word. For example, if we have a 3-byte or 7-byte data packet,
                # one word of the CRC will be contained in the previous data word, and three in our current one.
                with m.Switch(previous_valid):

                    # If our data packet was word aligned, all of our CRC bytes are currently present.
                    # We'll use our current word directly.
                    with m.Case(0b1111):
                        m.d.comb += data_to_check.eq(sink.data)

                    # If we had three valid bytes of data last time, one byte of our CRC was in the previous
                    # word. We'll grab it, and stick it onto the three bytes we're seeing.
                    with m.Case(0b0111):
                        m.d.comb += data_to_check.eq(Cat(previous_word[24:32], sink.data[0:24]))

                    # Same, but for 2B in the previous word and 2B in the current.
                    with m.Case(0b0011):
                        m.d.comb += data_to_check.eq(Cat(previous_word[16:32], sink.data[0:16]))

                    # Same, but for 3B in the previous word and 1B in the current.
                    with m.Case(0b0001):
                        m.d.comb += data_to_check.eq(Cat(previous_word[8:32], sink.data[0:8]))

                if self._gen2:
                    # Gen2 trim: the block-translation engine may present
                    # a valid-gap between the final payload word and the
                    # word completing the CRC-32 (sym-wise construct
                    # tails); wait for the word before judging.  The Gen1
                    # wire can never gap here, so the historical
                    # elaboration below stays verbatim.
                    with m.If(sink.valid):
                        with m.If(data_to_check == crc32.crc):
                            m.d.comb += self.packet_good.eq(1)
                        with m.Else():
                            m.d.comb += self.packet_bad.eq(1)
                        m.next = "WAIT_FOR_HPSTART"
                else:
                    # Check our CRC based on the word we've extracted, and strobe either ``packet_good``
                    # or ``packet_bad``, depending on its validity.
                    with m.If(data_to_check == crc32.crc):
                        m.d.comb += self.packet_good.eq(1)
                    with m.Else():
                        m.d.comb += self.packet_bad.eq(1)

                    # Finally, wait for our next packet.  (This transition used
                    # to sit inside the Else arm above -- a good packet then
                    # lingered here a second cycle, re-compared against
                    # whatever word followed, and strobed a spurious
                    # ``packet_bad`` after every good packet; endpoints whose
                    # accept paths stay in their idle state on completion then
                    # served the phantom failure as a retransmission request
                    # (bug #27, HANDOVER 10l).
                    m.next = "WAIT_FOR_HPSTART"


        return m


    def _elaborate_wide(self, m):
        """ The words=2 receiver (see the constructor comment).

        The offset-0 and offset-4 paths share the payload machinery:
        a ``skewed`` flag selects between the raw beat and the
        half-assembled view Cat(previous[32:64], current[0:32]).  The
        final CRC-32 word sits at byte position v (= payload bytes in
        the last assembled beat): for v <= 4 it is already contained
        in that beat; for v in 5..7 it straddles into the next; for
        v = 8 it fills the next beat's low half.
        """
        sink   = self.sink
        source = self.source

        header = HeaderPacket()

        data_bytes_remaining = Signal(range(self.MAX_PACKET_SIZE + 1))

        # The previous ASSEMBLED payload beat and its valid mask.
        previous_word  = Signal.like(sink.data)
        previous_valid = Signal.like(sink.ctrl)

        # Offset-4 payload skew: the previous RAW beat (for assembly).
        skewed        = Signal()
        raw_prev      = Signal.like(sink.data)
        raw_prev_ctrl = Signal.like(sink.ctrl)
        with m.If(sink.valid):
            m.d.ss += [
                raw_prev      .eq(sink.data),
                raw_prev_ctrl .eq(sink.ctrl),
            ]

        # The assembled payload view (data and ctrl).
        assembled      = Signal.like(sink.data)
        assembled_ctrl = Signal.like(sink.ctrl)
        m.d.comb += [
            assembled.eq(Mux(
                skewed, Cat(raw_prev[32:64], sink.data[0:32]),
                sink.data)),
            assembled_ctrl.eq(Mux(
                skewed, Cat(raw_prev_ctrl[4:8], sink.ctrl[0:4]),
                sink.ctrl)),
        ]

        low  = sink.data.word_select(0, 32)
        high = sink.data.word_select(1, 32)

        #
        # CRC Generators (wide surfaces).
        #
        m.submodules.crc16 = crc16 = HeaderPacketCRC(words=2)
        m.d.comb += crc16.data_input2.eq(sink.data)

        m.submodules.crc32 = crc32 = DataPacketPayloadCRC(words=2)
        m.d.comb += crc32.data_input2.eq(assembled)
        m.d.comb += crc32.data_input.eq(assembled[0:32])

        hpstart_low  = half_matches_symbols(sink, 0, SHP, SHP, SHP, EPF)
        hpstart_high = half_matches_symbols(sink, 1, SHP, SHP, SHP, EPF)
        dpstart_low  = half_matches_symbols(sink, 0, SDP, SDP, SDP, EPF)
        dpstart_high = half_matches_symbols(sink, 1, SDP, SDP, SDP, EPF)

        def capture_dw3(dw3):
            return [
                header.crc16            .eq(dw3[ 0:16]),
                header.sequence_number  .eq(dw3[16:19]),
                header.dw3_reserved     .eq(dw3[19:22]),
                header.hub_depth        .eq(dw3[22:25]),
                header.delayed          .eq(dw3[25]),
                header.deferred         .eq(dw3[26]),
                header.crc5             .eq(dw3[27:32]),
            ]

        def begin_payload(new_skew, dw3=None):
            """Header checks passed and DPP framing seen: latch the
            packet parameters and enter the payload path.  ``dw3``:
            in the offset-0 case the final data word arrives in the
            SAME beat -- the intermediate ``header`` record is a cycle
            stale for its fields, so they are spliced in directly."""
            m.d.ss += [
                self.header           .eq(header),
                self.new_header       .eq(1),
                data_bytes_remaining  .eq(header.dw1[16:]),
                source.first          .eq(1),
                skewed                .eq(new_skew),
            ]
            if dw3 is not None:
                m.d.ss += [
                    self.header.crc16           .eq(dw3[ 0:16]),
                    self.header.sequence_number .eq(dw3[16:19]),
                    self.header.dw3_reserved    .eq(dw3[19:22]),
                    self.header.hub_depth       .eq(dw3[22:25]),
                    self.header.delayed         .eq(dw3[25]),
                    self.header.deferred        .eq(dw3[26]),
                    self.header.crc5            .eq(dw3[27:32]),
                ]

        m.d.ss += self.new_header.eq(0)

        with m.FSM(domain="ss"):

            # WAIT -- watch for HPSTART at either beat half.
            with m.State("WAIT"):
                m.d.comb += [
                    crc16.clear.eq(1),
                    crc32.clear.eq(1),
                ]
                with m.If(sink.valid):
                    with m.If(hpstart_low):
                        m.d.comb += [
                            crc16.clear       .eq(0),
                            crc16.data_input  .eq(high),
                            crc16.advance_crc .eq(1),
                        ]
                        m.d.ss += header.dw0.eq(high)
                        with m.If(high[0:5] != HeaderPacketType.DATA):
                            m.next = "WAIT"
                        with m.Else():
                            m.next = "P0_MID"
                    with m.Elif(hpstart_high):
                        m.next = "P4_DW01"

            # ── offset-0 header: [HPSTART|DW0] [DW1|DW2] [DW3|DPPSTART] ──
            with m.State("P0_MID"):
                with m.If(sink.valid):
                    m.d.comb += crc16.advance_crc2.eq(1)
                    m.d.ss += [
                        header.dw1.eq(low),
                        header.dw2.eq(high),
                    ]
                    m.next = "P0_END"

            with m.State("P0_END"):
                with m.If(sink.valid):
                    dw3 = low
                    crc5_ok  = (dw3[27:32] == compute_usb_crc5(dw3[16:27]))
                    crc16_ok = (crc16.crc == dw3[0:16])
                    m.d.ss += capture_dw3(dw3)
                    # The CRC-16 must be clean if the very next beat
                    # starts a new header (WAIT suppresses its clear to
                    # advance DW0 in that same cycle).
                    m.d.comb += crc16.clear.eq(1)
                    # The DPP framing must ride this beat's high half.
                    with m.If(crc5_ok & crc16_ok & dpstart_high):
                        begin_payload(new_skew=0, dw3=dw3)
                        m.next = "RECEIVE_PAYLOAD"
                    with m.Else():
                        m.next = "WAIT"

            # ── offset-4 header: [..|HPSTART] [DW0|DW1] [DW2|DW3],
            #    then [DPPSTART|payload...] half-skewed. ──
            with m.State("P4_DW01"):
                with m.If(sink.valid):
                    m.d.comb += crc16.advance_crc2.eq(1)
                    m.d.ss += [
                        header.dw0.eq(low),
                        header.dw1.eq(high),
                    ]
                    with m.If(low[0:5] != HeaderPacketType.DATA):
                        m.next = "WAIT"
                    with m.Else():
                        m.next = "P4_DW23"

            with m.State("P4_DW23"):
                with m.If(sink.valid):
                    dw3 = high
                    m.d.comb += crc16.data_input.eq(low)
                    crc5_ok  = (dw3[27:32] == compute_usb_crc5(dw3[16:27]))
                    crc16_ok = (crc16.crc_after_word == dw3[0:16])
                    m.d.ss += header.dw2.eq(low)
                    m.d.ss += capture_dw3(dw3)
                    # Leave a clean CRC-16 behind (see P0_END).
                    m.d.comb += crc16.clear.eq(1)
                    with m.If(crc5_ok & crc16_ok):
                        m.next = "P4_DPPSTART"
                    with m.Else():
                        m.next = "WAIT"

            with m.State("P4_DPPSTART"):
                with m.If(sink.valid):
                    # Re-derive the CRC verdicts?  Already checked; the
                    # DPP framing must occupy this beat's LOW half, the
                    # first payload bytes its high half (captured into
                    # ``raw_prev`` by the always-on capture above).
                    with m.If(dpstart_low):
                        begin_payload(new_skew=1)
                        m.next = "RECEIVE_PAYLOAD"
                    with m.Else():
                        m.next = "WAIT"

            # ── the shared payload path (assembled beats) ──
            with m.State("RECEIVE_PAYLOAD"):
                lanes = [(data_bytes_remaining > k) & sink.valid
                         for k in range(8)]
                m.d.comb += [
                    source.data      .eq(assembled),
                    source.valid     .eq(Cat(*lanes)),

                    crc32.advance_2words.eq(source.valid == 0b11111111),
                    crc32.advance_7B    .eq(source.valid == 0b01111111),
                    crc32.advance_6B    .eq(source.valid == 0b00111111),
                    crc32.advance_5B    .eq(source.valid == 0b00011111),
                    crc32.advance_4B    .eq(source.valid == 0b00001111),
                    crc32.advance_3B    .eq(source.valid == 0b00000111),
                    crc32.advance_2B    .eq(source.valid == 0b00000011),
                    crc32.advance_1B    .eq(source.valid == 0b00000001),

                    source.last      .eq(data_bytes_remaining <= 8),
                ]

                with m.If(sink.valid):
                    m.d.ss += source.first.eq(0)

                    # Control codes inside claimed-payload lanes: bail.
                    with m.If((assembled_ctrl & source.valid) != 0):
                        m.d.comb += [
                            self.packet_bad.eq(1),
                            crc16.clear    .eq(1),
                            crc32.clear    .eq(1),
                        ]
                        m.next = "WAIT"

                    with m.Else():
                        m.d.ss += [
                            previous_word   .eq(assembled),
                            previous_valid  .eq(source.valid),
                        ]
                        with m.If(data_bytes_remaining > 8):
                            m.d.ss += data_bytes_remaining \
                                .eq(data_bytes_remaining - 8)
                        with m.Else():
                            m.next = "CHECK_CRC32"

            # CHECK_CRC32 -- locate the CRC word relative to the final
            # assembled beat (v = payload bytes it carried).
            with m.State("CHECK_CRC32"):
                # v <= 4: the CRC is fully inside ``previous_word``.
                for pattern, v in [(0b00000001, 1), (0b00000011, 2),
                                   (0b00000111, 3), (0b00001111, 4)]:
                    with m.If(previous_valid == pattern):
                        with m.If(previous_word[8 * v:8 * v + 32]
                                  == crc32.crc):
                            m.d.comb += self.packet_good.eq(1)
                        with m.Else():
                            m.d.comb += self.packet_bad.eq(1)
                        m.d.comb += [
                            crc16.clear.eq(1),
                            crc32.clear.eq(1),
                        ]
                        m.next = "WAIT"
                # v in 5..7: straddles into this beat; v = 8: fully here.
                with m.If(previous_valid[4]):
                    with m.If(sink.valid):
                        data_to_check = Signal(32)
                        with m.Switch(previous_valid):
                            with m.Case(0b00011111):
                                m.d.comb += data_to_check.eq(Cat(
                                    previous_word[40:64], assembled[0:8]))
                            with m.Case(0b00111111):
                                m.d.comb += data_to_check.eq(Cat(
                                    previous_word[48:64], assembled[0:16]))
                            with m.Case(0b01111111):
                                m.d.comb += data_to_check.eq(Cat(
                                    previous_word[56:64], assembled[0:24]))
                            with m.Default():   # 0b11111111
                                m.d.comb += data_to_check.eq(
                                    assembled[0:32])
                        with m.If(data_to_check == crc32.crc):
                            m.d.comb += self.packet_good.eq(1)
                        with m.Else():
                            m.d.comb += self.packet_bad.eq(1)
                        m.d.comb += [
                            crc16.clear.eq(1),
                            crc32.clear.eq(1),
                        ]
                        m.next = "WAIT"

        return m


class DataPacketTransmitter(Elaboratable):
    """ Gateware that generates a Data Packet Header, and orchestrates sending it and a payload.

    The actual sending is handled by our transmitter gateware.

    Attributes
    ----------
    data_sink: SuperSpeedStreamInterface(), input stream
        The data stream to be send as a data packet. The length of this stream should match thee
        length parameter.
    send_zlp: Signal(), input
        Strobe; triggers sending of a zero-length packet.

    sequence_number: Signal(5), input
        The sequence number associated with the relevant data packet. Latched in once :attr:``data_sink`` goes valid.
    endpoint_number: Signal(4), input
        The endpoint number associated with the relevant data stream. Latched in once :attr:``data_sink`` goes valid.
    data_length: Signal(range(1024 + 1))
        The length of the data packet to be sent; in bytes. Latched in once :attr:``data_sink`` goes valid.
    direction: Signal(), input
        The direction to indicate in the data header packet. Typically Direction.IN; but will be Direction.OUT
        when data is sent to the host as part of a control transfer.

    address: Signal(7), input
        The current address of the USB device.
    """

    MAX_PACKET_SIZE = 1024

    def __init__(self, words=1, external_accept=False):
        # Width program: the orchestration below is width-agnostic
        # (``valid.any()``/``stream_eq`` plumbing); ``words`` only
        # sizes the streams.  words=1 verbatim.
        words = words

        #
        # I/O port
        #

        # Input stream.
        self.data_sink       = SuperSpeedStreamInterface(payload_words=4 * words)
        self.send_zlp        = Signal()

        # Data parameters.
        self.sequence_number = Signal(5)
        self.endpoint_number = Signal(4)
        self.data_length     = Signal(range(self.MAX_PACKET_SIZE + 1))
        self.address         = Signal(7)
        self.direction       = Signal()
        self.end_of_burst    = Signal()

        # Output streams.
        self.header_source   = HeaderQueue()
        self.data_source     = SuperSpeedStreamInterface(payload_words=4 * words)

        # Width-program hook (words=2 layers, ``external_accept=True``):
        # the store-and-forward width adapter consumes our register
        # stage GREEDILY, so ``data_source.valid`` -- the historical
        # header-offer qualifier -- drops before the (externally gated)
        # offer is accepted.  The layer then completes the SEND_HEADER
        # handshake through this strobe instead.  Elaboration-gated
        # (finding #52): an always-present constant-0 OR into the
        # SEND_HEADER transition perturbed the words=1 SHIPPING netlist
        # (42k diff bytes vs the laddered fence image, caught by the
        # session-20 V0' parity rebuild); the words=1 statements below
        # stay verbatim.
        self.external_accept = Signal() if external_accept else None

        # Strobe: the data parameters above have just been consumed
        # (latched for the packet whose transmission is beginning).  The
        # endpoint multiplexer holds its captured parameter registers --
        # and defers granting the shared transmit stream to a *new*
        # packet -- until this fires: a short packet small enough to be
        # absorbed by the buffering between the multiplexer and this
        # transmitter otherwise releases the grant early, and the next
        # packet's grant-lock overwrites the shared parameters before we
        # latch them (DPH emitted with the wrong length/endpoint/sequence
        # -- GW_USB3 bug #25).
        self.parameters_consumed = Signal()

        # Debug tap (prunable).
        self.debug_fsm       = Signal(2)


    def elaborate(self, platform):
        m = Module()

        # Shortcuts.
        header_source = self.header_source
        data_sink     = self.data_sink
        data_source   = self.data_source

        # Latched resources.
        sequence_number = Signal.like(self.sequence_number)
        endpoint_number = Signal.like(self.endpoint_number)
        data_length     = Signal.like(self.data_length)
        direction       = Signal.like(self.direction)
        end_of_burst    = Signal.like(self.end_of_burst)


        # For now, we'll pass our data stream through unmodified; only buffered to improve
        # timing.
        #
        # We'll keep this architecture; as later code is likely to want to more actively
        # control when data is passed through to the transmitter.
        #
        # The register must never refill ACROSS a packet boundary: once it
        # holds the current packet's ``last`` word, the following upstream
        # word belongs to the NEXT packet.  Capturing it on the very cycle
        # the last word is consumed (upstream gaps arrive compressed
        # through the buffered stages -- see the boundary discussion in
        # SEND_PAYLOAD) absorbs the new packet's head into a register the
        # WAIT_FOR_DATA state never looks at: its header is never
        # generated and the shared transmit path wedges for every
        # endpoint (bug #24's remaining half, found by tx_fuzz).  Instead,
        # the register empties and the new packet waits upstream, where
        # WAIT_FOR_DATA observes it.
        may_refill    = ~data_source.valid.any() | data_source.ready
        boundary_hold = data_source.valid.any() & data_source.last
        with m.If(may_refill):
            with m.If(~boundary_hold):
                m.d.ss   += data_source.stream_eq(data_sink, omit={'ready'})
                m.d.comb += data_sink.ready.eq(1)
            with m.Else():
                # Consume-without-refill: the register empties.
                m.d.ss += data_source.valid.eq(0)


        with m.FSM(domain="ss") as dtx_fsm:

            # WAIT_FOR_DATA -- we're idly waiting for our input data stream to become valid.
            with m.State("WAIT_FOR_DATA"):

                # Constantly latch in our data parameters until we get a new data packet.
                m.d.ss += [
                    sequence_number  .eq(self.sequence_number),
                    endpoint_number  .eq(self.endpoint_number),
                    data_length      .eq(self.data_length),
                    direction        .eq(self.direction),
                    end_of_burst     .eq(self.end_of_burst),
                ]

                # Once our data goes valid, begin sending our data.
                # (Either transition freezes the parameter latches above:
                # signal their consumption to the endpoint multiplexer.)
                #
                # Never re-arm while the PREVIOUS packet's final word is
                # still unconsumed in our output register
                # (``boundary_hold``): the header offer and the packet
                # transmitter's ZLP decision both sample our output
                # stream, and a stale tail there would be mistaken for
                # the new packet's payload.  The tail drains within a few
                # cycles (the transmitter is still finishing that DPP).
                with m.If(data_sink.valid.any() & ~boundary_hold):
                    m.d.comb += self.parameters_consumed.eq(1)
                    m.next = "SEND_HEADER"

                with m.Elif(self.send_zlp & ~boundary_hold):
                    m.d.comb += self.parameters_consumed.eq(1)
                    m.next = "SEND_ZLP"


            # SEND_HEADER -- we're sending the header associated with our data packet.
            with m.State("SEND_HEADER"):
                header = DataHeaderPacket()
                m.d.comb += [
                    header_source.header    .eq(header),

                    # Only present the header once the first payload word is
                    # staged on our output register: the packet transmitter
                    # decides whether a data packet is a ZLP by sampling the
                    # payload stream as it accepts the header.  Offering the
                    # header a cycle early makes an idle transmitter treat a
                    # data-carrying packet as a ZLP -- a malformed packet
                    # whose payload length contradicts its header.
                    header_source.valid     .eq(data_source.valid.any()),

                    # We're sending a data packet from up to the host.
                    header.type             .eq(HeaderPacketType.DATA),
                    header.direction        .eq(direction),
                    header.device_address   .eq(self.address),

                    # Fill in our input parameters...
                    header.data_sequence    .eq(sequence_number),
                    header.data_length      .eq(data_length),
                    header.endpoint_number  .eq(endpoint_number),
                    header.end_of_burst     .eq(end_of_burst),
                ]

                # Once our header is accepted, move on to passing through our payload.
                #
                # The acceptance is ``valid & ready``: the header-queue
                # arbiter keeps routing the downstream ``ready`` to its
                # (sticky) selected producer even while that producer
                # offers nothing, so a bare ``ready`` here is NOT an
                # acceptance -- advancing on it dispatches no header, and
                # the packet's staged payload then wedges the shared
                # transmit path for every endpoint.
                header_accepted = header_source.valid & header_source.ready
                if self.external_accept is not None:
                    header_accepted = header_accepted | self.external_accept
                with m.If(header_accepted):
                    m.next = "SEND_PAYLOAD"


            # SEND_PAYLOAD -- we're now passing our payload data to our transmitter; which will
            # drive ready when it's time to accept data.
            with m.State("SEND_PAYLOAD"):

                # Once our packet is complete, we'll go back to idle.  Two
                # redundant boundary observations:
                #
                # (a) the input stream going invalid -- the historical
                #     delimiter (the endpoint multiplexer inserts a
                #     one-cycle gap between packets);
                # (b) the packet's ``last``-marked word being consumed from
                #     our register stage by the packet transmitter.
                #
                # (a) alone is UNSOUND: the gap travels through buffered
                # stages (the protocol layer's TxDataSkidBuffer) that only
                # represent gaps as "running dry" -- when the downstream
                # freezes across a packet handoff with words buffered (the
                # transmitter stops consuming payload the moment it captures
                # the last word), the following packet's words refill the
                # buffer seamlessly and the gap is silently compressed away.
                # Missing the boundary leaves this FSM in SEND_PAYLOAD
                # forever: the next packet's header is never generated and
                # its staged payload wedges the shared transmit path for
                # every endpoint (reproduced with three concurrent bulk IN
                # endpoints; GW_USB3 open-item work, bug #24).
                #
                # (b) catches exactly that case: the consumption of the
                # ``last`` word is the authoritative end of the packet's
                # payload, independent of input-gap survival.  (A packet
                # whose producer does not mark ``last`` still relies on
                # (a), as before.)
                with m.If(~data_sink.valid.any()):
                    m.next = "WAIT_FOR_DATA"
                with m.Elif(data_source.valid.any() & data_source.last
                            & data_source.ready):
                    m.next = "WAIT_FOR_DATA"


            # SEND_ZLP -- we're sending a ZLP; which in our case means we'll be sending a header
            # without driving our data stream.
            with m.State("SEND_ZLP"):
                header = DataHeaderPacket()
                m.d.comb += [
                    header_source.header    .eq(header),
                    header_source.valid     .eq(1),

                    # We're sending a data packet from up to the host.
                    header.type             .eq(HeaderPacketType.DATA),
                    header.direction        .eq(direction),
                    header.device_address   .eq(self.address),

                    # Fill in our input parameters...
                    header.data_sequence    .eq(sequence_number),
                    header.data_length      .eq(0),
                    header.endpoint_number  .eq(endpoint_number),
                    header.end_of_burst     .eq(end_of_burst),
                ]

                # Once our header is accepted, we can move directly back to idle.
                # Our transmitter will handle generating the zero-length DPP.
                with m.If(header_source.ready):
                    m.next = "WAIT_FOR_DATA"

        for _i, _name in enumerate(("WAIT_FOR_DATA", "SEND_HEADER",
                                    "SEND_PAYLOAD", "SEND_ZLP")):
            with m.If(dtx_fsm.ongoing(_name)):
                m.d.comb += self.debug_fsm.eq(_i)

        return m
