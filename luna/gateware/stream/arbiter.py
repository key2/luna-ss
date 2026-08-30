#
# This file is part of LUNA.
#
# Copyright (c) 2020 Great Scott Gadgets <info@greatscottgadgets.com>
# SPDX-License-Identifier: BSD-3-Clause

""" Stream multiplexers/arbiters. """

from amaranth       import *
from .              import StreamInterface


class StreamMultiplexer(Elaboratable):
    """ Gateware that merges a collection of StreamInterfaces into a single interface.

    This variant performs no scheduling. Assumes that only one stream will be communicating at once.

    Attributes
    ----------
    output: StreamInterface(), output stream
        Our output interface; has all of the active busses merged together.
    """

    def __init__(self, stream_type=StreamInterface):
        """
        Parameters:
            stream_type   -- The type of stream we'll be multiplexing. Must be a subclass of StreamInterface.
        """

        # Collection that stores each of the interfaces added to this bus.
        self._inputs = []

        #
        # I/O port
        #
        self.output = stream_type()


    def add_input(self, input_interface):

        """ Adds a transmit interface to the multiplexer. """
        self._inputs.append(input_interface)


    def elaborate(self, platform):
        m = Module()

        #
        # Our basic functionality is simple: we'll build a priority encoder that
        # connects whichever interface has its .valid signal high.
        #

        conditional = m.If

        for interface in self._inputs:

            # If the given interface is asserted, drive our output with its signals.
            with conditional(interface.valid):
                m.d.comb += interface.attach(self.output)

            # After our first iteration, use Elif instead of If.
            conditional = m.Elif


        return m



class StreamArbiter(Elaboratable):
    """ Gateware that merges a collection of StreamInterfaces into a single interface.

    This variant uses a simple priority scheduler; and will use a standard valid/ready handshake
    to schedule a single stream to communicate at a time. Bursts of ``valid`` will never be interrupted,
    so streams will only be switched once the current transmitter drops ``valid`` low.


    Attributes
    ----------
    source: StreamInterface(), output stream
        Our output interface; has all of the active busses merged together.

    idle: Signal(), output
        Asserted when none of our streams is currently active.

    Parameters
    ----------
    stream_type: subclass of StreamInterface
        If provided, sets the type of stream we'll be multiplexing (and thus our output type).
    domain: str
        The name of the domain in which this arbiter should operate. Defaults to "sync".
    """

    def __init__(self, *, stream_type=StreamInterface, domain="sync"):
        self._domain = domain

        # Collection that stores each of the interfaces added to this bus.
        self._sinks = []

        #
        # I/O port
        #
        self.source = stream_type()
        self.idle   = Signal()


    def add_stream(self, stream):
        """ Adds a stream to our arbiter.

        Parameters
        ----------
        stream: StreamInterface subclass
            The stream to be added. Streams added first will have higher priority.
        """
        self._sinks.append(stream)


    def elaborate(self, platform):
        m = Module()
        active_stream = self.source
        stream_count  = len(self._sinks)

        # SYNTHESIS NOTE (GowinSynthesis V1.9.12.03 hardening, bug #36):
        # the historical shape -- a Switch on a binary index for the
        # routing plus a priority scan that re-reads each sink's
        # ``valid`` for the re-selection -- is exactly the "duplicated
        # expression cone" pattern GowinSynthesis was observed to
        # miscompile in the endpoint multiplexer (HANDOVER 10k, bug #21:
        # the synthesized clones of one reduction DISAGREED on hardware
        # while RTL simulation, fuzzing and timing all passed).  On the
        # link-layer header-packet arbiter the same class of miscompile
        # drops a data packet header offered by the DataPacketTransmitter
        # while the queue believes nothing was offered: the DPH vanishes
        # and every following DPH pairs with the PREVIOUS packet's
        # payload (bug #34's bench signature: wire dseq one ahead,
        # first-of-burst DPH missing, TP ACKs coalescing while the
        # arbiter sits parked).  Mitigate with the validated idiom:
        # every reduction is ONE named net used by every consumer, the
        # selection is a registered ONE-HOT (no binary index decode to
        # clone), and routing is driven directly from the register bits.
        valids = Signal(stream_count)
        m.d.comb += valids.eq(Cat(*(s.valid for s in self._sinks)))

        # One-hot registered selection; out of reset, sink 0 is selected.
        selected = Signal(stream_count, init=1)

        # THE single "selected sink is offering" net, computed from the
        # same nets that drive the routing below.
        sel_valid = Signal()
        m.d.comb += sel_valid.eq((valids & selected).any())

        #
        # Stream output multiplexer (AND-OR from the one-hot register).
        #
        for i, stream in enumerate(self._sinks):
            with m.If(selected[i]):
                m.d.comb += active_stream.stream_eq(stream)

        #
        # Active stream selection: only change which stream we're working
        # with when the active stream stops transmitting (bursts of
        # ``valid`` are never interrupted).
        #
        with m.If(~sel_valid):

            # Idle iff nobody is offering at all.
            m.d.comb += self.idle.eq(~valids.any())

            # Priority order: sinks added first win (the last assignment
            # in the reversed scan "wins").
            for i in reversed(range(stream_count)):
                with m.If(valids[i]):
                    m.d.sync += selected.eq(1 << i)


        # If we're operating in a domain other than sync, replace 'sync' with it.
        if self._domain != "sync":
            m =  DomainRenamer(self._domain)(m)

        return m
