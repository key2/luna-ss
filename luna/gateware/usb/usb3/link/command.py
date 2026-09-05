#
# This file is part of LUNA.
#
# Copyright (c) 2020 Great Scott Gadgets <info@greatscottgadgets.com>
# SPDX-License-Identifier: BSD-3-Clause
""" USB Link Commands Transmitter/Receivers """

import functools
import operator

from enum import IntEnum

from amaranth          import *

from .crc              import compute_usb_crc5
from ..physical.coding import SLC, EPF, stream_matches_symbols, \
    get_word_for_symbols, half_matches_symbols
from ...stream         import USBRawSuperSpeedStream


class LinkCommandDetector(Elaboratable):
    """ USB3 Link Command Detector.

    This module detects USB3 link commands as they're received on the bus.

    Attributes
    ----------
    sink: USBRawSuperSpeedStream, input stream
        The (aligned and descrambled) data stream captured from the physical layer.

    command: Signal(4), output
        The link command; including its two-bit class and two-bit type.

    command_class: Signal(2), output
        The link command's class; equivalent to the first two bits of :attr:``command``.
    command_type: Signal(2), output
        The link command's type; equivalent to the second two bits of :attr:``command``.

    subtype: Signal(4), output
        The link command's subtype.

    new_command: signal(), output
        Strobe; indicates that a new link command has been received, and the details of this command
        are ready to be read.
    """

    def __init__(self, words=1):
        # Width program (usb3_design.md 13.5): at ``words=2`` a link
        # command (LCSTART + command word, 8 symbols) fits ONE beat --
        # but a real partner emits constructs at 4-symbol granularity,
        # so the detector walks both beat halves (offsets 0/4).
        # ``words=1`` is the historical unit verbatim.
        self._words = words

        #
        # I/O port
        #
        self.sink = USBRawSuperSpeedStream(payload_words=4 * words)

        # Link command information.
        self.command       = Signal(4)
        self.command_class = Signal(2)
        self.command_type  = Signal(2)
        self.subtype       = Signal(4)

        # Status strobes.
        self.new_command   = Signal()


    def elaborate(self, platform):
        m = Module()

        # Create our ``command_class`` and ``command_type`` aliases,
        # which are always just slices of our command.
        m.d.comb += [
            self.command_class  .eq(self.command[2:4]),
            self.command_type   .eq(self.command[0:2])
        ]

        # Assume we don't have a new command, unless asserted below.
        m.d.ss += self.new_command.eq(0)

        if self._words == 2:
            return self._elaborate_wide(m)

        with m.FSM(domain="ss"):

            # WAIT_FOR_LCSTART -- we're currently waiting for LCSTART framing, which indicates
            # that the following word is a link command.
            with m.State("WAIT_FOR_LCSTART"):

                is_lcstart = stream_matches_symbols(self.sink, SLC, SLC, SLC, EPF)
                with m.If(is_lcstart):
                    m.next = "PARSE_COMMAND"


            # PARSE_COMMAND -- our previous data word contained LCSTART; so this word contains our
            # link command. We'll parse / validate it.
            with m.State("PARSE_COMMAND"):

                with m.If(self.sink.valid):

                    link_command_word    = self.sink.data.word_select(0, 16)
                    link_command_replica = self.sink.data.word_select(1, 16)

                    # The payload of a link command contains only data packets; and should never contain
                    # control packets. We'll sanity check this.
                    contains_only_data = (self.sink.ctrl == 0)

                    # A valid two-byte link command word is repeated twice, exactly. [USB3.2r1: 7.2.2.1]
                    # Per the specification, we can only accept commands where both copies match.
                    redundancy_matches = (link_command_word == link_command_replica)

                    # The core ten bits of our link command word are guarded by a CRC-5. We'll only
                    # accept link commands whose CRC matches.
                    crc_matches  = (link_command_word[11:16] == compute_usb_crc5(link_command_word[0:11]))

                    # If we have a word that matches -all- of these criteria, accept it as a new command.
                    with m.If(contains_only_data & redundancy_matches & crc_matches):
                        m.d.ss += [

                            # Copy our fields out of the link command...
                            self.command      .eq(link_command_word[7:11]),
                            self.subtype      .eq(link_command_word[0: 4]),

                            # ... and indicate that we've received a new command
                            self.new_command  .eq(1)
                        ]

                    # No matter the word's validity, we'll move back to waiting for a new command header;
                    # as we can't do anything about invalid commands.
                    m.next = "WAIT_FOR_LCSTART"


        return m


    def _elaborate_wide(self, m):
        """ The words=2 detector: both beat halves examined per cycle.

        An LCSTART in the LOW half has its command word in the HIGH
        half of the SAME beat; an LCSTART in the HIGH half completes
        in the LOW half of the NEXT valid beat (the offset-4 case,
        with the following high half free to start another command).
        Mirrors the narrow unit's semantics exactly: the word after an
        LCSTART is consumed as a command candidate (never re-examined
        as framing), and an invalid candidate is silently discarded.
        """
        sink = self.sink

        def parse_half(half):
            """Validity + fields of one half parsed as a command word."""
            data = sink.data.word_select(half, 32)
            ctrl = sink.ctrl.word_select(half, 4)
            word    = data.word_select(0, 16)
            replica = data.word_select(1, 16)
            valid = (
                (ctrl == 0)
                & (word == replica)
                & (word[11:16] == compute_usb_crc5(word[0:11]))
            )
            return valid, word

        def accept(word):
            return [
                self.command     .eq(word[7:11]),
                self.subtype     .eq(word[0: 4]),
                self.new_command .eq(1),
            ]

        lcstart_low  = half_matches_symbols(sink, 0, SLC, SLC, SLC, EPF)
        lcstart_high = half_matches_symbols(sink, 1, SLC, SLC, SLC, EPF)

        with m.FSM(domain="ss"):

            # ALIGNED -- no partially received command pending.
            with m.State("ALIGNED"):
                with m.If(sink.valid):
                    # Offset-0 command: framing low, command word high;
                    # completes within this very beat.
                    with m.If(lcstart_low):
                        valid, word = parse_half(1)
                        with m.If(valid):
                            m.d.ss += accept(word)
                    # Offset-4 command: framing high; the command word
                    # arrives in the next beat's low half.
                    with m.Elif(lcstart_high):
                        m.next = "PARSE_LOW"

            # PARSE_LOW -- an LCSTART occupied the previous beat's high
            # half; this beat's low half is its command word.
            with m.State("PARSE_LOW"):
                with m.If(sink.valid):
                    valid, word = parse_half(0)
                    with m.If(valid):
                        m.d.ss += accept(word)
                    # The high half may immediately start another
                    # offset-4 command; otherwise realign.
                    with m.If(lcstart_high):
                        m.next = "PARSE_LOW"
                    with m.Else():
                        m.next = "ALIGNED"

        return m



class LinkCommandGenerator(Elaboratable):
    """ USB3 Link Command Generator.

    This module generates link commands on the USB3 bus.

    Attributes
    ----------
    source: USBRawSuperSpeedStream(), output stream
        The data generated in sending our link commands.

    command: Signal(4), output
        The link command; including its two-bit class and two-bit type.
    subtype: Signal(4), output
        The link command's subtype.

    generate: Signal(), input
        Strobe; indicates that a link command should be generated.
    done: Signal(), output
        Indicates that the link command will be complete this cycle; and thus this unit will
        be ready to send another link command next cycle.
    """


    def __init__(self, words=1):
        # Width program: at ``words=2`` the whole link command (LCSTART
        # + duplicated command word, 8 symbols) is emitted as a SINGLE
        # beat.  ``words=1`` is the historical unit verbatim.
        self._words = words

        #
        # I/O port
        #
        self.source = USBRawSuperSpeedStream(payload_words=4 * words)

        # Link command information.
        self.command    = Signal(4)
        self.subtype    = Signal(4)

        # Control inputs.
        self.generate   = Signal()
        self.done       = Signal()


    def elaborate(self, platform):
        m = Module()

        # Latched versions of our signals guaranteed not to change mid-transmission.
        latched_command = Signal.like(self.command)
        latched_subtype = Signal.like(self.subtype)

        if self._words == 2:
            header_data, header_ctrl = get_word_for_symbols(SLC, SLC, SLC, EPF)
            with m.FSM(domain="ss"):

                # IDLE -- waiting to generate a link command.
                with m.State("IDLE"):
                    with m.If(self.generate):
                        m.d.ss += [
                            latched_command  .eq(self.command),
                            latched_subtype  .eq(self.subtype)
                        ]
                        m.next = "TRANSMIT"

                # TRANSMIT -- the full 8-symbol link command in one beat:
                # LCSTART framing low, the duplicated command word high.
                with m.State("TRANSMIT"):
                    link_command = Signal(16)
                    m.d.comb += [
                        link_command[ 0: 4]      .eq(latched_subtype),
                        link_command[ 4: 7]      .eq(0),  # Reserved.
                        link_command[ 7:11]      .eq(latched_command),
                        link_command[11:16]      .eq(
                            compute_usb_crc5(link_command[0:11])),

                        self.source.valid        .eq(1),
                        self.source.data[ 0:32]  .eq(header_data),
                        self.source.ctrl[ 0: 4]  .eq(header_ctrl),
                        self.source.data[32:48]  .eq(link_command),
                        self.source.data[48:64]  .eq(link_command),
                        self.source.ctrl[ 4: 8]  .eq(0),

                        # Packet boundary (see the words=1 comment below).
                        self.source.first        .eq(1),
                    ]
                    with m.If(self.source.ready):
                        m.d.comb += self.done.eq(1)
                        m.next = "IDLE"

            return m

        with m.FSM(domain="ss"):

            # IDLE -- we're currently waiting to generate a link command
            with m.State("IDLE"):

                # Once we have a generate command...
                with m.If(self.generate):

                    # ... latch in our command and subtype ...
                    m.d.ss += [
                        latched_command  .eq(self.command),
                        latched_subtype  .eq(self.subtype)
                    ]
                    m.next = "TRANSMIT_HEADER"

            # TRANSMIT_HEADER -- we're starting our link command by transmitting a header.
            with m.State("TRANSMIT_HEADER"):

                # Drive the bus with our header...
                header_data, header_ctrl = get_word_for_symbols(SLC, SLC, SLC, EPF)
                m.d.comb += [
                    self.source.valid  .eq(1),
                    self.source.data   .eq(header_data),
                    self.source.ctrl   .eq(header_ctrl),

                    # Packet boundary: allow the CTC skip inserter to place SKP
                    # ordered sets before this link command (see transmitter.py).
                    self.source.first  .eq(1),
                ]

                # ... and keep driving it until it's accepted.
                with m.If(self.source.ready):
                    m.next = "TRANSMIT_COMMAND"


            # TRANSMIT_COMMAND -- we're now ready to send the core of our command.
            with m.State("TRANSMIT_COMMAND"):
                link_command = Signal(16)

                # Drive our command onto the bus...
                m.d.comb += [
                    # First, build our core command...
                    link_command[ 0: 4]      .eq(latched_subtype),
                    link_command[ 4: 7]      .eq(0),  # Reserved.
                    link_command[ 7:11]      .eq(latched_command),
                    link_command[11:16]      .eq(compute_usb_crc5(link_command[0:11])),

                    # ... and then duplicate it as a command onto the output.
                    self.source.valid        .eq(1),
                    self.source.data[ 0:16]  .eq(link_command),
                    self.source.data[16:32]  .eq(link_command),
                    self.source.ctrl         .eq(0)
                ]

                # ... and keep driving it until it's accepted.
                with m.If(self.source.ready):
                    m.d.comb += self.done.eq(1)
                    m.next = "IDLE"


        return m
