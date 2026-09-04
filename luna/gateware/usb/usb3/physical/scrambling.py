#
# This file is part of LUNA.
#
# Copyright (c) 2020 Great Scott Gadgets <info@greatscottgadgets.com>
# Copyright (c) 2020 Florent Kermarrec <florent@enjoy-digital.fr>
#
# Code based on ``usb3_pipe``.
# SPDX-License-Identifier: BSD-3-Clause
""" Scrambling and descrambling for USB3. """

import operator
import functools

from amaranth import *

from .coding   import COM, stream_word_matches_symbol
from ...stream import USBRawSuperSpeedStream


#
# Scrambling modules.
# See [USB3.2r1: Appendix B].
#

class ScramblerLFSR(Elaboratable):
    """ Scrambler LFSR.

    Linear feedback shift register used for USB3 scrambling.
    Polynomial: X^16 + X^5 + X^4 + X^3 + 1

    See [USB3.2: Appendix B]

    Attributes
    ----------
    clear: Signal(), input
        Strobe; when high, resets the LFSR to its initial value.
    advance: Signal(), input
        Strobe; when high, the LFSR advances on each clock cycle.
    value: Signal(32), output
        The current value of the LFSR.

    Parameters
    ----------
    initial_value: 32-bit int, optional
        The initial value for the LFSR. Optional; defaults to all 1's, per the USB3 spec.
    """
    def __init__(self, initial_value=0xffff, words=1):
        self._initial_value = initial_value
        # Width program (usb3_design.md 13.5): ``words=2`` advances the
        # 16-bit LFSR state TWICE per cycle and emits 64 scramble bits
        # (low word first on the wire) -- the same spec transformation
        # composed, no re-derivation.  ``words=1`` is verbatim.
        self._words = words

        #
        # I/O port
        #
        self.clear   = Signal()
        self.advance = Signal()
        self.value   = Signal(32 * words)


    def elaborate(self, platform):
        m = Module()

        next_value       = Signal(16)
        current_value    = Signal(16, init=self._initial_value)

        def xor_bits_of(state, *indices):
            bits = (state[i] for i in indices)
            return functools.reduce(operator.__xor__, bits)

        def xor_bits(*indices):
            return xor_bits_of(current_value, *indices)


        # Compute the next value in our internal LFSR state...
        m.d.comb += next_value.eq(Cat(
            xor_bits(0, 6, 8, 10),               # 0
            xor_bits(1, 7, 9, 11),               # 1
            xor_bits(2, 8, 10, 12),              # 2
            xor_bits(3, 6, 8, 9, 10, 11, 13),    # 3
            xor_bits(4, 6, 7, 8, 9, 11, 12, 14), # 4
            xor_bits(5, 6, 7, 9, 12, 13, 15),    # 5
            xor_bits(0, 6, 7, 8, 10, 13, 14),    # 6
            xor_bits(1, 7, 8, 9, 11, 14, 15),    # 7
            xor_bits(0, 2, 8, 9, 10, 12, 15),    # 8
            xor_bits(1, 3, 9, 10, 11, 13),       # 9
            xor_bits(0, 2, 4, 10, 11, 12, 14),   # 10
            xor_bits(1, 3, 5, 11, 12, 13, 15),   # 11
            xor_bits(2, 4, 6, 12, 13, 14),       # 12
            xor_bits(3, 5, 7, 13, 14, 15),       # 13
            xor_bits(4, 6, 8, 14, 15),           # 14
            xor_bits(5, 7, 9, 15)                # 15
        ))

        # Compute the LFSR's current output.
        def output_of(state):
            def xor_bits(*indices):
                return xor_bits_of(state, *indices)
            return Cat(
                state[15],
                state[14],
                state[13],
                state[12],
                state[11],
                state[10],
                state[9],
                state[8],
                state[7],
                state[6],
                state[5],
                xor_bits(4,  15),
                xor_bits(3,  14, 15),
                xor_bits(2,  13, 14, 15),
                xor_bits(1,  12, 13, 14),
                xor_bits(0,  11, 12, 13),
                xor_bits(10, 11, 12, 15),
                xor_bits(9,  10, 11, 14),
                xor_bits(8,  9 , 10, 13),
                xor_bits(7,  8 , 9,  12),
                xor_bits(6,  7 , 8,  11),
                xor_bits(5,  6 , 7,  10),
                xor_bits(4,  5 , 6,  9,  15),
                xor_bits(3,  4 , 5,  8,  14),
                xor_bits(2,  3 , 4,  7,  13, 15),
                xor_bits(1,  2 , 3,  6,  12, 14),
                xor_bits(0,  1 , 2,  5,  11, 13, 15),
                xor_bits(0,  1 , 4,  10, 12, 14),
                xor_bits(0,  3 , 9,  11, 13),
                xor_bits(2,  8 , 10, 12),
                xor_bits(1,  7 , 9,  11),
                xor_bits(0,  6 , 8,  10)
            )

        m.d.comb += self.value[0:32].eq(Cat(
            current_value[15],
            current_value[14],
            current_value[13],
            current_value[12],
            current_value[11],
            current_value[10],
            current_value[9],
            current_value[8],
            current_value[7],
            current_value[6],
            current_value[5],
            xor_bits(4,  15),
            xor_bits(3,  14, 15),
            xor_bits(2,  13, 14, 15),
            xor_bits(1,  12, 13, 14),
            xor_bits(0,  11, 12, 13),
            xor_bits(10, 11, 12, 15),
            xor_bits(9,  10, 11, 14),
            xor_bits(8,  9 , 10, 13),
            xor_bits(7,  8 , 9,  12),
            xor_bits(6,  7 , 8,  11),
            xor_bits(5,  6 , 7,  10),
            xor_bits(4,  5 , 6,  9,  15),
            xor_bits(3,  4 , 5,  8,  14),
            xor_bits(2,  3 , 4,  7,  13, 15),
            xor_bits(1,  2 , 3,  6,  12, 14),
            xor_bits(0,  1 , 2,  5,  11, 13, 15),
            xor_bits(0,  1 , 4,  10, 12, 14),
            xor_bits(0,  3 , 9,  11, 13),
            xor_bits(2,  8 , 10, 12),
            xor_bits(1,  7 , 9,  11),
            xor_bits(0,  6 , 8,  10)
        ))

        # words=2: the high word's scramble bits come from the
        # once-advanced state; a cycle's advance moves the state by two
        # words.
        if self._words == 2:
            next2_value = Signal(16)
            m.d.comb += [
                next2_value.eq(Cat(
                    xor_bits_of(next_value, 0, 6, 8, 10),
                    xor_bits_of(next_value, 1, 7, 9, 11),
                    xor_bits_of(next_value, 2, 8, 10, 12),
                    xor_bits_of(next_value, 3, 6, 8, 9, 10, 11, 13),
                    xor_bits_of(next_value, 4, 6, 7, 8, 9, 11, 12, 14),
                    xor_bits_of(next_value, 5, 6, 7, 9, 12, 13, 15),
                    xor_bits_of(next_value, 0, 6, 7, 8, 10, 13, 14),
                    xor_bits_of(next_value, 1, 7, 8, 9, 11, 14, 15),
                    xor_bits_of(next_value, 0, 2, 8, 9, 10, 12, 15),
                    xor_bits_of(next_value, 1, 3, 9, 10, 11, 13),
                    xor_bits_of(next_value, 0, 2, 4, 10, 11, 12, 14),
                    xor_bits_of(next_value, 1, 3, 5, 11, 12, 13, 15),
                    xor_bits_of(next_value, 2, 4, 6, 12, 13, 14),
                    xor_bits_of(next_value, 3, 5, 7, 13, 14, 15),
                    xor_bits_of(next_value, 4, 6, 8, 14, 15),
                    xor_bits_of(next_value, 5, 7, 9, 15))),
                self.value[32:64].eq(output_of(next_value)),
            ]
            advance_target = next2_value
        else:
            advance_target = next_value

        # If we have a reset, clear our LFSR.
        with m.If(self.clear):
            m.d.ss += current_value.eq(self._initial_value)

        # Otherwise, advance when desired.
        with m.Elif(self.advance):
            m.d.ss += current_value.eq(advance_target)

        return m


class Scrambler(Elaboratable):
    """ USB3-compliant data scrambler.

    Scrambles the transmitted data stream to reduce EMI.

    Attributes
    ----------
    clear: Signal(), input
        Strobe; when high, resets the scrambler to the start of its sequence.
    enable: Signal(), input
        When high, data scrambling is enabled. When low, data is passed through without scrambling.
    sink: USBRawSuperSpeedStream(), input stream
        The stream containing data to be scrambled.
    sink: USBRawSuperSpeedStream(), output stream
        The stream containing data the scrambled output.

    Parameters
    ----------
    initial_value: 32-bit int, optional
        The initial value for the LFSR. Optional.
    """
    def __init__(self, initial_value=0x7dbd, words=1):
        self._initial_value = initial_value
        # Width program: ``words=2`` scrambles 8-symbol (64-bit) beats
        # -- the native Gen1 trim of the 128-bit core (usb3_design.md
        # 13.1).  ``words=1`` is verbatim.
        self._words = words

        #
        # I/O port
        #
        self.clear  = Signal()
        self.enable = Signal()
        self.hold   = Signal()

        self.sink   = USBRawSuperSpeedStream(payload_words=4 * words)
        self.source = USBRawSuperSpeedStream(payload_words=4 * words)

        # Debug signaling.
        self.lfsr_state = Signal.like(self.source.data)


    def elaborate(self, platform):
        m = Module()

        sink   = self.sink
        source = self.source

        # Detect when we're sending a comma; which should reset our scrambling LFSR.
        comma_present = stream_word_matches_symbol(sink, 0, symbol=COM)

        # Create our inner LFSR, which should advance whenever our input streams do.
        m.submodules.lfsr = lfsr = ScramblerLFSR(
            initial_value=self._initial_value, words=self._words)
        m.d.comb += [
            lfsr.clear    .eq(self.clear | comma_present),
            lfsr.advance  .eq(sink.valid & source.ready & ~self.hold)
        ]

        # Pass through non-scrambled signals directly.
        m.d.comb += [
            source.ctrl   .eq(sink.ctrl),
            source.valid  .eq(sink.valid),
            sink.ready    .eq(source.ready)
        ]


        # If we have any non-control words, scramble them by overriding our data assignment above
        # with the relevant data word XOR'd with our LFSR value. Note that control words are -never-
        # scrambled, per [USB3.2: Appendix B]
        for i in range(4 * self._words):
            is_data_code = ~sink.ctrl[i]
            lfsr_word    = lfsr.value.word_select(i, 8)

            with m.If(self.enable & is_data_code):
                m.d.comb += source.data.word_select(i, 8).eq(sink.data.word_select(i, 8) ^ lfsr_word)
            with m.Else():
                m.d.comb += source.data.word_select(i, 8).eq(sink.data.word_select(i, 8))


        # Connect up our debug outputs.
        m.d.comb += [
            self.lfsr_state.eq(lfsr.value)
        ]


        return m



class Descrambler(Scrambler):
    """ USB3-compliant data descrambler.

    This module descrambles the received data stream. K-codes are not affected.
    This module automatically resets itself whenever a COM alignment character is seen.

    Attributes
    ----------
    enable: Signal(), input
        When high, data scrambling is enabled. When low, data is passed through without scrambling.
    sink: USBRawSuperSpeedStream(), input stream
        The stream containing data to be descrambled.
    source: USBRawSuperSpeedStream(), output stream
        The stream containing data the descrambled output.

    Parameters
    ----------
    initial_value: 32-bit int, optional
        The initial value for the LFSR. Optional.

    """
    def __init__(self, initial_value=0xffff, words=1):
        self._initial_value = initial_value
        super().__init__(initial_value=initial_value, words=words)
