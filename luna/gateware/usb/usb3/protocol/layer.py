#
# This file is part of LUNA.
#
# Copyright (c) 2020 Great Scott Gadgets <info@greatscottgadgets.com>
# SPDX-License-Identifier: BSD-3-Clause
""" USB3 link-layer abstraction."""

from amaranth import *

from ..link.header    import HeaderQueueArbiter, HeaderQueueDemultiplexer
from ...stream        import USBRawSuperSpeedStream, SuperSpeedStreamInterface

from .link_management import LinkManagementPacketHandler
from .timestamp       import TimestampPacketReceiver
from .endpoint        import SuperSpeedEndpointInterface
from .transaction     import TransactionPacketGenerator, TransactionPacketReceiver
from .data            import DataHeaderReceiver


class TxDataSkidBuffer(Elaboratable):
    """ Two-deep registered buffer for the endpoint -> link transmit stream.

    Terminates the (deep) combinational ready chain from the link-layer
    packet transmitter at a register boundary: without it, the ready cone
    reaches through the endpoint multiplexer into every endpoint's packet
    buffer addressing, which misses timing once several endpoints share
    the transmit path.  Preserves gapless flow (the output register refills
    every accepted cycle) and the packet delimiting gaps.
    """

    def __init__(self):
        self.sink   = SuperSpeedStreamInterface()
        self.source = SuperSpeedStreamInterface()

    def elaborate(self, platform):
        m = Module()
        sink, source = self.sink, self.source

        fields = ('payload', 'valid', 'first', 'last')

        out_regs  = {f: Signal.like(getattr(sink, f), name=f"out_{f}")
                     for f in fields}
        skid_regs = {f: Signal.like(getattr(sink, f), name=f"skid_{f}")
                     for f in fields}
        skid_full = Signal()

        m.d.comb += [
            *(getattr(source, f).eq(out_regs[f]) for f in fields),
            # Register-sourced upstream ready.
            sink.ready.eq(~skid_full),
        ]

        accept    = sink.valid.any() & sink.ready
        out_valid = out_regs['valid'].any()

        with m.If(source.ready | ~out_valid):
            with m.If(skid_full):
                m.d.ss += [
                    *(out_regs[f].eq(skid_regs[f]) for f in fields),
                ]
                with m.If(accept):
                    m.d.ss += [*(skid_regs[f].eq(getattr(sink, f))
                                 for f in fields)]
                with m.Else():
                    m.d.ss += skid_full.eq(0)
            with m.Else():
                with m.If(accept):
                    m.d.ss += [*(out_regs[f].eq(getattr(sink, f))
                                 for f in fields)]
                with m.Else():
                    m.d.ss += out_regs['valid'].eq(0)
        with m.Else():
            with m.If(accept):
                m.d.ss += [
                    skid_full.eq(1),
                    *(skid_regs[f].eq(getattr(sink, f)) for f in fields),
                ]

        return m

class USB3ProtocolLayer(Elaboratable):
    """ Abstraction encapsulating the USB3 protocol layer hardware. """

    def __init__(self, *, link_layer):
        self._link = link_layer

        #
        # I/O port
        #

        # Interface to our various endpoints.
        self.endpoint_interface    = SuperSpeedEndpointInterface()

        # Device state inputs.
        self.current_address       = Signal(7)
        self.current_configuration = Signal(7)

        # Current timestamp.
        self.bus_interval          = Signal(14)

        # Debug taps (prunable): transaction-packet generator activity at
        # the link header queue (SET_ADDRESS bring-up visibility).
        self.debug_tp_hdr_valid    = Signal()
        self.debug_tp_hdr_accepted = Signal()


    def elaborate(self, platform):
        m = Module()
        link = self._link

        #
        # Header Packet Multiplexers
        #

        # One-to-many Header demultiplexer.
        m.submodules.hp_demux = hp_demux = HeaderQueueDemultiplexer()
        m.d.comb += hp_demux.sink.header_eq(link.header_source)

        # Many-to-one Header multiplexer.
        m.submodules.hp_mux = hp_mux = HeaderQueueArbiter()
        m.d.comb += link.header_sink.header_eq(hp_mux.source)


        #
        # Link Management Packet Handler
        #
        m.submodules.lmp_handler = lmp_handler = LinkManagementPacketHandler()

        hp_demux.add_consumer(lmp_handler.header_sink)
        hp_mux.add_producer(lmp_handler.header_source)

        m.d.comb += [
            lmp_handler.usb_reset     .eq(link.in_reset),
            lmp_handler.link_ready    .eq(link.ready),
        ]

        #
        # Isochronous Timestamp Packet Handler
        #
        m.submodules.itp_handler = itp_handler = TimestampPacketReceiver()
        hp_demux.add_consumer(itp_handler.header_sink)

        m.d.comb += [
            self.bus_interval.eq(itp_handler.bus_interval_counter)
        ]


        #
        # Data Packet Handlers
        #
        m.submodules.data_header_receiver = data_header_receiver = DataHeaderReceiver()
        hp_demux.add_consumer(data_header_receiver.header_sink)


        #
        # Transaction Packet handlers.
        #

        # Generator
        m.submodules.tp_generator = tp_generator = TransactionPacketGenerator()
        hp_mux.add_producer(tp_generator.header_source)
        m.d.comb += [
            tp_generator.address.eq(self.current_address),

            # Debug taps.
            self.debug_tp_hdr_valid    .eq(tp_generator.header_source.valid),
            self.debug_tp_hdr_accepted .eq(tp_generator.header_source.valid &
                                           tp_generator.header_source.ready),
        ]

        # Receiver
        m.submodules.tp_receiver = tp_receiver = TransactionPacketReceiver()
        hp_demux.add_consumer(tp_receiver.header_sink)



        #
        # Endpoint Interfacing
        #
        m.submodules.tx_skid = tx_skid = TxDataSkidBuffer()
        endpoint_interface = self.endpoint_interface
        m.d.comb += [
            # Rx interface.
            endpoint_interface.rx           .tap(link.data_source),
            endpoint_interface.rx_header    .eq(link.data_header_from_host),
            endpoint_interface.rx_complete  .eq(link.data_source_complete),
            endpoint_interface.rx_invalid   .eq(link.data_source_invalid),

            # Tx interface (through a registered skid stage; see above).
            tx_skid.sink                    .stream_eq(endpoint_interface.tx),
            link.data_sink                  .stream_eq(tx_skid.source),
            link.data_sink_send_zlp         .eq(endpoint_interface.tx_zlp),
            link.data_sink_length           .eq(endpoint_interface.tx_length),
            link.data_sink_endpoint_number  .eq(endpoint_interface.tx_endpoint_number),
            link.data_sink_sequence_number  .eq(endpoint_interface.tx_sequence_number),
            link.data_sink_direction        .eq(endpoint_interface.tx_direction),
            link.data_sink_eob              .eq(endpoint_interface.tx_eob),
            endpoint_interface.tx_parameters_consumed
                                            .eq(link.data_sink_parameters_consumed),

            # Handshake exchange interface.
            tp_generator.interface          .connect(endpoint_interface.handshakes_out),
            tp_receiver.interface           .connect(endpoint_interface.handshakes_in)
        ]


        return m
