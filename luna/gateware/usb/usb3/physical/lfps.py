#
# This file is part of LUNA.
#
# Copyright (c) 2020 Great Scott Gadgets <info@greatscottgadgets.com>
# Copyright (c) 2020 Florent Kermarrec <florent@enjoy-digital.fr>
#
# Code based in part on ``usb3_pipe``.
# SPDX-License-Identifier: BSD-3-Clause
""" Low-frequency periodic signaling gateware.

LFPS is the first signaling to happen during the initialization of the USB3.0 link.

LFPS allows partners to exchange Out Of Band (OOB) controls/commands and consists of bursts where
a "slow" clock is generated (between 10M-50MHz) for a specific duration and with a specific repeat
period. After the burst, the transceiver is put in electrical idle mode (same electrical level on
P/N pairs while in nominal mode P/N pairs always have an opposite level):

Transceiver level/mode: _=0, -=1 x=electrical idle
|-_-_-_-xxxxxxxxxxxxxxxxxxxx|-_-_-_-xxxxxxxxxxxxxxxxxxxx|...
|<burst>                    |<burst>                    |...
|<-----repeat period------->|<-----repeat period------->|...

A LFPS pattern is identified by a burst duration and repeat period.

To be able generate and receive LFPS, a transceiver needs to be able put its TX in electrical idle
and to detect RX electrical idle.
"""

from math import ceil

from amaranth         import *
from amaranth.lib.cdc import FFSynchronizer

from ....utils       import rising_edge_detected


__all__ = ['LFPSTransceiver']


#
# LPFS timing "constants", and collection classes that represent them.
#

class LFPSTiming:
    """LPFS timings with typical, minimum and maximum timing values."""

    def __init__(self, t_typ=None, t_min=None, t_max=None):
        self.t_typ = t_typ
        self.t_min = t_min
        self.t_max = t_max
        assert t_min is not None
        assert t_max is not None

        self.range = (t_min, t_max)


class LFPS:
    """LPFS patterns with burst and repeat timings."""

    def __init__(self, burst, repeat=None, cycles=None):
        self.burst  = burst
        self.repeat = repeat
        self.cycles = None


# Our actual pattern constants; as specified by the USB3 specification.
# [USB 3.2r1: Table 6-30]

_PollingLFPSBurst  = LFPSTiming(t_typ=1.0e-6,  t_min=0.6e-6, t_max=1.4e-6)
_PollingLFPSRepeat = LFPSTiming(t_typ=10.0e-6, t_min=6.0e-6, t_max=14.0e-6)

# SuperSpeedPlus Capability Declaration [USB 3.2r1 6.9.4]: information
# is carried in the Polling.LFPS burst repeat period -- logic 0 =
# tRepeat 6-9 us, logic 1 = 11-14 us (9-11 us is a guard band).
# SCD1 = '0010', SCD2 = '1101', transmitted LSb first.  Typicals are
# chosen mid-bin (and so that a receiver classifying with generous
# bins decodes them under either the 125 or 156.25 MHz clock
# assumption -- the Gen2 sim bench runs the ss domain at 156.25).
SCD_REPEAT_0 = 7.0e-6
SCD_REPEAT_1 = 13.5e-6
SCD1_PATTERN = (0, 1, 0, 0)     # '0010', wire (LSb-first) order
SCD2_PATTERN = (1, 0, 1, 1)     # '1101', wire (LSb-first) order
_PollingLFPS       = LFPS(burst=_PollingLFPSBurst, repeat=_PollingLFPSRepeat)

_PingLFPSBurst     = LFPSTiming(t_min=40.0e-9, t_max=160.0e-9)
_PingLFPSRepeat    = LFPSTiming(t_typ=200e-3, t_min=160e-3, t_max=240.0e-3)
_PingLFPS          = LFPS(burst=_PingLFPSBurst, repeat=_PingLFPSRepeat)

_ResetLFPSBurst    = LFPSTiming(t_typ=100.0e-3, t_min=80.0e-3,  t_max=120.0e-3)
_ResetLFPS         = LFPS(burst=_ResetLFPSBurst)


#
# Gateware for generating and detecting bursts of LFPS patterns. Does not deal with
# the actual 10-50 MHz LFPS clock, delegating that to the PHY.
#

class LFPSDetector(Elaboratable):
    """ LFPS Signaling Detector

    Compares received (and demodulated) LFPS signaling with a specified pattern.

    Attributes
    ----------

    signaling_received: Signal(), input
        Held high when our PHY is detecting LFPS square waves.
    detect: Signal(), output
        Strobes high when a valid LFPS burst is detected.
    """
    def __init__(self, lfps_pattern, ss_clk_frequency=125e6):
        self._pattern              = lfps_pattern
        self._clock_frequency      = ss_clk_frequency

        #
        # I/O port
        #
        self.signaling_received = Signal() # i
        self.detect             = Signal() # o


    def elaborate(self, platform):
        m = Module()

        # Create an in-domain version of our square-wave-detector signal.
        present = Signal()
        m.submodules.present_cdc = FFSynchronizer(self.signaling_received, present, o_domain="ss")

        # Figure out how large of a counter we're going to need...
        burst_cycles_min    = ceil(self._clock_frequency * self._pattern.burst.t_min)
        burst_cycles_max    = ceil(self._clock_frequency * self._pattern.burst.t_max)

        # If we have a repeat interval, include it in our calculations.
        if self._pattern.repeat is not None:
            repeat_cycles_max   = ceil(self._clock_frequency * self._pattern.repeat.t_max)
            repeat_cycles_min   = ceil(self._clock_frequency * self._pattern.repeat.t_min)
            counter_max         = max(burst_cycles_max, repeat_cycles_max)
        else:
            counter_max         = burst_cycles_max

        # ... and create our counter.
        count = Signal(range(0, counter_max + 1))
        m.d.ss += count.eq(count + 1)

        # Keep track of whether our previous iteration matched; as we're typically in detecting
        # sequences of two correct LFPS cycles in a row.
        last_iteration_matched = Signal()

        #
        # Detector state machine.
        #
        with m.FSM(domain="ss"):

            # WAIT_FOR_NEXT_BURST -- we're not currently in a measurement; but are waiting for a
            # burst to begin, so we can perform a full measurement.
            with m.State("WAIT_FOR_NEXT_BURST"):
                m.d.ss += last_iteration_matched.eq(0)

                # If we've just seen the start of a burst, start measuring it.
                with m.If(rising_edge_detected(m, present, domain="ss")):
                    m.d.ss += count.eq(1),
                    m.next = "MEASURE_BURST"

            # MEASURE_BURST -- we're seeing something we believe to be a burst; and measuring its length.
            with m.State("MEASURE_BURST"):

                # Failing case: if our counter has gone longer than our maximum burst time, this isn't
                # a relevant burst. We'll wait for the next one.
                with m.If(count == burst_cycles_max):
                    m.next = 'WAIT_FOR_NEXT_BURST'

                # Once our burst is over, we'll need to decide if the burst matches our pattern.
                with m.If(~present):

                    # Failing case: if our burst is over, but we've not yet reached our minimum burst time,
                    # then this isn't a relevant burst. We'll wait for the next one.
                    with m.If(count < burst_cycles_min):
                        m.next = 'WAIT_FOR_NEXT_BURST'

                    # If our burst ended within a reasonable span, we can move on.
                    with m.Else():

                        # If we don't have a repeat interval, we're done!
                        if self._pattern.repeat is None:
                            m.d.comb += self.detect.eq(1)
                            m.next = "WAIT_FOR_NEXT_BURST"

                        # Otherwise, we'll need to check the repeat interval, as well.
                        else:
                            m.next = "MEASURE_REPEAT"

            if self._pattern.repeat is not None:

                # MEASURE_REPEAT -- we've just finished seeing a burst; and now we're measuring the gap between
                # successive bursts, which the USB specification calls the "repeat interval". [USB3.2r1: Fig 6-32]
                with m.State("MEASURE_REPEAT"):

                    # Failing case: if our counter has gone longer than our maximum burst time, this isn't
                    # a relevant burst. We'll wait for the next one.
                    with m.If(count == repeat_cycles_max):
                        m.next = 'WAIT_FOR_NEXT_BURST'

                    # Once we see another potential burst, we'll start our detection back from the top.
                    with m.If(present):
                        m.d.ss += count.eq(1)
                        m.next = 'MEASURE_BURST'

                        # If this lasted for a reasonable repeat interval, we've seen a correct burst!
                        with m.If(count >= repeat_cycles_min):

                            # Mark this as a correct iteration, and if the previous iteration was also
                            # a correct one, indicate that we've detected our output.
                            m.d.ss   += last_iteration_matched.eq(1)
                            m.d.comb += self.detect.eq(last_iteration_matched)

                        with m.Else():
                            m.d.ss   += last_iteration_matched.eq(0)

        return m



class SCDDetector(Elaboratable):
    """SuperSpeedPlus Capability Declaration receiver [USB 3.2r1 6.9.4].

    Classifies the repeat period between received Polling.LFPS burst
    starts (logic 0 = 6-9 us, logic 1 = 11-14 us; generous windows so
    both the 125 and 156.25 MHz clock assumptions classify) and
    pattern-matches the sliding 4-bit window against SCD1 ('0010') and
    SCD2 ('1101'), any cyclic rotation.  Outputs are sticky until
    ``clear``.
    """

    def __init__(self, ss_clk_freq=125e6):
        self._clock_frequency = ss_clk_freq

        self.signaling_received = Signal()  # i
        self.clear              = Signal()  # i
        self.scd1_detected      = Signal()  # o, sticky
        self.scd2_detected      = Signal()  # o, sticky

    def elaborate(self, platform):
        m = Module()

        clk = self._clock_frequency
        bit0_min = ceil(clk * 4.5e-6)
        bit0_max = ceil(clk * 9.9e-6)
        bit1_min = ceil(clk * 10.5e-6)
        bit1_max = ceil(clk * 18.0e-6)
        refractory = ceil(clk * 2.0e-6)

        # synchronize + edge-detect the LFPS envelope
        sig_sync = Signal(2)
        m.submodules += FFSynchronizer(self.signaling_received, sig_sync[0],
                                       o_domain="ss")
        m.d.ss += sig_sync[1].eq(sig_sync[0])
        burst_start = sig_sync[0] & ~sig_sync[1]

        gap = Signal(range(bit1_max + 2))
        window = Signal(8)          # (bit, valid) pairs, 4 deep
        bits   = Signal(4)
        valid  = Signal(4)

        with m.If(gap <= bit1_max):
            m.d.ss += gap.eq(gap + 1)

        def push(bit_value, bit_valid):
            return [
                bits .eq(Cat(bit_value, bits[:-1])),
                valid.eq(Cat(bit_valid, valid[:-1])),
            ]

        with m.If(burst_start & (gap > refractory)):
            m.d.ss += gap.eq(0)
            with m.If((gap >= bit0_min) & (gap <= bit0_max)):
                m.d.ss += push(0, 1)
            with m.Elif((gap >= bit1_min) & (gap <= bit1_max)):
                m.d.ss += push(1, 1)
            with m.Else():
                m.d.ss += push(0, 0)
        with m.Elif(gap > bit1_max):
            # silence longer than any legal repeat: window invalid
            m.d.ss += valid.eq(0)

        # cyclic-rotation matcher; wire (LSb-first shift) order.  The
        # newest bit lands in bits[0].
        def rotations(pat):
            p = list(pat)
            return {tuple(p[i:] + p[:i]) for i in range(len(p))}

        with m.If(valid.all()):
            for pat, out in ((SCD1_PATTERN, self.scd1_detected),
                             (SCD2_PATTERN, self.scd2_detected)):
                for rot in sorted(rotations(pat)):
                    value = sum(b << i for i, b in enumerate(rot))
                    with m.If(bits == value):
                        m.d.ss += out.eq(1)
        with m.If(self.clear):
            m.d.ss += [self.scd1_detected.eq(0), self.scd2_detected.eq(0),
                       valid.eq(0)]

        return m


class LFPSGenerator(Elaboratable):
    """ LFPS Signaling Generator

    Transmits (to be modulated) LFPS signaling that follows a specified pattern.

    Attributes
    ----------

    generate: Signal(), input
        When asserted, continuously generates LFPS patterns.
    done: Signal(), output
        Strobes high every time a cycle is completed.

    drive_electrical_idle: Signal(), output
        Held high while cycles are being generated; during both burst and repeat intervals.
    send_signaling: Signal(), output
        Held high during a burst.
    """
    def __init__(self, lfps_pattern, sys_clk_freq, scd_pattern=None):
        self._pattern         = lfps_pattern
        self._clock_frequency = sys_clk_freq
        # Optional SuperSpeedPlus Capability Declaration: when given
        # (a tuple of bits, wire order), the repeat interval of each
        # successive burst is modulated per [6.9.4] instead of the
        # pattern's fixed t_typ.  ``None`` elaborates the historical
        # fixed-repeat generator unchanged.  With SCD enabled,
        # ``scd2_select`` switches the transmitted declaration from
        # SCD1 to SCD2 at runtime (Polling.LFPSPlus).
        self._scd_pattern     = scd_pattern

        #
        # I/O ports
        #
        self.generate               = Signal() # i
        self.completed              = Signal() # o
        self.drive_electrical_idle  = Signal() # o
        self.send_signaling         = Signal() # o
        self.scd2_select            = Signal() # i (SCD builds only)


    def elaborate(self, platform):
        m = Module()

        # Compute the amount of cycles it takes to transmit the burst and reach
        # the end of the pattern...
        burst_cycles  = ceil(self._clock_frequency * self._pattern.burst.t_typ)
        repeat_cycles = ceil(self._clock_frequency * self._pattern.repeat.t_typ)

        if self._scd_pattern is not None:
            # SCD repeat modulation [6.9.4]: per-burst repeat target
            # selected by the pattern bit; the bit index advances at
            # the end of every repeat interval, cycling the pattern
            # (consecutive SCDs are sent back to back per 6.9.4.2).
            repeat_scd = [ceil(self._clock_frequency * SCD_REPEAT_0),
                          ceil(self._clock_frequency * SCD_REPEAT_1)]
            repeat_cycles = max(repeat_cycles, *repeat_scd)
            scd_index  = Signal(range(len(self._scd_pattern)))
            scd_bit    = Signal()
            assert len(self._scd_pattern) == len(SCD2_PATTERN)
            with m.Switch(scd_index):
                for i, (b1, b2) in enumerate(zip(self._scd_pattern,
                                                 SCD2_PATTERN)):
                    with m.Case(i):
                        m.d.comb += scd_bit.eq(
                            Mux(self.scd2_select, b2, b1))
            repeat_target = Signal(range(repeat_cycles + 1))
            m.d.comb += repeat_target.eq(
                Mux(scd_bit, repeat_scd[1], repeat_scd[0]))

        # ... and create our cycle counter.
        count = Signal(range(0, repeat_cycles))
        m.d.ss += count.eq(count + 1)

        with m.FSM(domain="ss"):

            # IDLE -- wait for an LFPS burst request.
            with m.State("IDLE"):
                m.d.ss += count.eq(0)

                # Once we get one, start a burst.
                with m.If(self.generate):
                    m.d.comb += self.drive_electrical_idle.eq(1)
                    m.next = "BURST"

            # BURST -- transmit an LFPS burst for the duration of the burst interval.
            with m.State("BURST"):
                m.d.comb += self.drive_electrical_idle.eq(1)
                m.d.comb += self.send_signaling.eq(1)

                with m.If(count + 1 == burst_cycles):
                    m.next = "WAIT"

            # WAIT -- do nothing for the remaining part of the repeat interval.
            with m.State("WAIT"):
                m.d.comb += self.drive_electrical_idle.eq(1)

                if self._scd_pattern is not None:
                    with m.If(count + 1 == repeat_target):
                        m.d.comb += self.completed.eq(1)
                        with m.If(scd_index == len(self._scd_pattern) - 1):
                            m.d.ss += scd_index.eq(0)
                        with m.Else():
                            m.d.ss += scd_index.eq(scd_index + 1)
                        m.next = "IDLE"
                else:
                    with m.If(count + 1 == repeat_cycles):
                        m.d.comb += self.completed.eq(1)
                        m.next = "IDLE"

        return m


class LFPSTransceiver(Elaboratable):
    """ Low-Frequency Periodic Signaling (LFPS) Transciever

    Transmits and receives the LPFS sequences required for a USB 3.0 link.

    Attributes
    ----------

    drive_electrical_idle: Signal(), output
        Held high when our PHY should be either in Electrical Idle, or transmit LFPS waveforms.
    send_signaling: Signal(), output
        Held high when our PHY should be transmitting LFPS square waves.
    signaling_received: Signal(), input
        Should be asserted when our PHY is receiving LFPS square waves.

    send_polling: Signal(), input
        Strobe. When asserted, begins Polling LFPS.
    cycles_sent: Signal(16), output
        Incremented every time an LFPS cycle is completed.

    polling_detected: Signal(), output
        Strobes high when Polling LFPS is detected.
    reset_detected: Signal(), output
        Strobes high when Reset LFPS is detected.
    """

    def __init__(self, ss_clk_freq=125e6, scd_pattern=None):
        self._scd_pattern = scd_pattern
        self._clock_frequency      = ss_clk_freq

        #
        # I/O ports
        #
        self.drive_electrical_idle = Signal() # o
        self.send_signaling        = Signal() # o
        self.signaling_received    = Signal() # i

        # LFPS burst generation
        self.send_polling          = Signal() # i
        self.cycles_sent           = Signal(16) # o

        # LFPS burst reception
        self.polling_detected      = Signal() # o
        self.ping_detected         = Signal() # o
        self.reset_detected        = Signal() # o

        # SuperSpeedPlus Capability Declaration (SCD builds only)
        self.scd2_select           = Signal() # i
        self.scd_clear             = Signal() # i
        self.scd1_detected         = Signal() # o, sticky
        self.scd2_detected         = Signal() # o, sticky


    def elaborate(self, platform):
        m = Module()

        #
        # LFPS Receivers.
        #
        m.submodules.polling_detector = polling_detector = LFPSDetector(_PollingLFPS, self._clock_frequency)
        m.d.comb += [
            polling_detector.signaling_received .eq(self.signaling_received),
            self.polling_detected               .eq(polling_detector.detect)
        ]

        m.submodules.ping_detector = ping_detector = LFPSDetector(_PingLFPS, self._clock_frequency)
        m.d.comb += [
            ping_detector.signaling_received .eq(self.signaling_received),
            self.ping_detected               .eq(ping_detector.detect)
        ]

        m.submodules.reset_detector = reset_detector = LFPSDetector(_ResetLFPS, self._clock_frequency)
        m.d.comb += [
            reset_detector.signaling_received   .eq(self.signaling_received),
            self.reset_detected                 .eq(reset_detector.detect)
        ]

        #
        # LFPS Transmitter(s).
        #
        m.submodules.polling_generator = polling_generator = LFPSGenerator(_PollingLFPS, self._clock_frequency, scd_pattern=self._scd_pattern)
        if self._scd_pattern is not None:
            m.d.comb += polling_generator.scd2_select.eq(self.scd2_select)
            m.submodules.scd_detector = scd_detector = \
                SCDDetector(self._clock_frequency)
            m.d.comb += [
                scd_detector.signaling_received.eq(self.signaling_received),
                scd_detector.clear             .eq(self.scd_clear),
                self.scd1_detected             .eq(scd_detector.scd1_detected),
                self.scd2_detected             .eq(scd_detector.scd2_detected),
            ]
        m.d.comb += [
            polling_generator.generate  .eq(self.send_polling),
            self.drive_electrical_idle  .eq(polling_generator.drive_electrical_idle),
            self.send_signaling         .eq(polling_generator.send_signaling),
        ]

        with m.If(polling_generator.generate):
            with m.If(polling_generator.completed):
                m.d.ss += self.cycles_sent.eq(self.cycles_sent + 1)
        with m.Else():
            m.d.ss += self.cycles_sent.eq(0)

        return m
