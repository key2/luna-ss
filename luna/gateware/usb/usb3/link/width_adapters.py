#
# This file is part of LUNA.
#
# Copyright (c) 2026 the luna-ss contributors
# SPDX-License-Identifier: BSD-3-Clause
""" Protocol-boundary width adapters for the 128-bit core.

At ``core_width=128`` the link layer's data paths run at 64 bits/beat,
but the protocol layer and every endpoint keep their proven 32-bit
shape: these adapters sit at the link layer's external data boundary.

* ``TxPacketWidthAdapter`` (32 -> 64): STORE-AND-FORWARD per packet --
  the whole packet is buffered before a single gapless 64-bit burst,
  because the packet transmitter's payload feed contract is gapless
  (an underrun puts stale bytes on the wire).  Word pairs pack into
  beats; an odd tail becomes a half-valid final beat.
* ``RxWidthSplitter`` (64 -> 32): each beat splits into one or two
  words through a small FIFO (the RX data path has no backpressure;
  the FIFO absorbs construct bursts -- control-endpoint DPPs at the
  128-bit trims arrive at <= 4 symbols/cycle sustained from the Gen2
  block receiver's collector, so the splitter keeps up; full-rate
  64-bit BULK endpoints are the documented follow-up).

Throughput note: the 32-bit protocol side caps sustained payload at
4 bytes/core-cycle (312 MB/s at 78.125, 250 MB/s at 62.5).  Control
traffic (the Gen2 enumeration vehicle) is unaffected; the bulk-ladder
rate targets need the endpoint widening.
"""

from amaranth          import *
from amaranth.lib.fifo import SyncFIFO

from ...stream         import SuperSpeedStreamInterface


class TxPacketWidthAdapter(Elaboratable):
    """ 32-bit protocol data stream -> 64-bit link data stream. """

    def __init__(self, depth=512):
        # Entries: {last, valid[8], data[64]} -- packed beats.
        self._depth = depth

        self.sink   = SuperSpeedStreamInterface(payload_words=4)
        self.source = SuperSpeedStreamInterface(payload_words=8)

    def elaborate(self, platform):
        m = Module()
        sink, source = self.sink, self.source

        m.submodules.fifo = fifo = DomainRenamer({"sync": "ss"})(
            SyncFIFO(width=64 + 8 + 1, depth=self._depth))

        # ── pack side ────────────────────────────────────────────────
        low_v  = Signal()          # a low half is staged
        low_d  = Signal(32)
        low_c  = Signal(4)

        packets_buffered = Signal(8)
        pkt_in  = Signal()
        pkt_out = Signal()
        with m.If(pkt_in & ~pkt_out):
            m.d.ss += packets_buffered.eq(packets_buffered + 1)
        with m.Elif(pkt_out & ~pkt_in):
            m.d.ss += packets_buffered.eq(packets_buffered - 1)

        m.d.comb += sink.ready.eq(fifo.w_rdy)
        with m.If(sink.valid.any() & fifo.w_rdy):
            with m.If(~low_v & ~sink.last):
                # Stage the low half.
                m.d.ss += [low_v.eq(1), low_d.eq(sink.data),
                           low_c.eq(sink.valid)]
            with m.Elif(~low_v & sink.last):
                # Single-word packet (or odd final word arriving with
                # nothing staged): a half-valid final beat.
                m.d.comb += [
                    fifo.w_data.eq(Cat(sink.data, Const(0, 32),
                                       sink.valid, Const(0, 4),
                                       C(1, 1))),
                    fifo.w_en.eq(1),
                    pkt_in.eq(1),
                ]
            with m.Else():
                # Pair the staged low half with this word.
                m.d.comb += [
                    fifo.w_data.eq(Cat(low_d, sink.data,
                                       low_c, sink.valid,
                                       sink.last)),
                    fifo.w_en.eq(1),
                    pkt_in.eq(sink.last),
                ]
                m.d.ss += low_v.eq(0)

        # ── serve side: gapless per-packet bursts ────────────────────
        # A packet's first beat is only presented once the WHOLE packet
        # is queued, so mid-packet refills always find the FIFO ready.
        head_v    = Signal()
        head_d    = Signal(64)
        head_c    = Signal(8)
        head_last = Signal()
        mid_pkt   = Signal()

        m.d.comb += [
            source.valid.eq(Mux(head_v, head_c, 0)),
            source.data .eq(head_d),
            source.last .eq(head_v & head_last),
            source.first.eq(0),
        ]

        consume = head_v & source.ready
        with m.If(~head_v | consume):
            with m.If(fifo.r_rdy & (mid_pkt | (packets_buffered != 0))):
                m.d.ss += [
                    head_v   .eq(1),
                    head_d   .eq(fifo.r_data[0:64]),
                    head_c   .eq(fifo.r_data[64:72]),
                    head_last.eq(fifo.r_data[72]),
                    mid_pkt  .eq(~fifo.r_data[72]),
                ]
                m.d.comb += [
                    fifo.r_en.eq(1),
                    pkt_out  .eq(fifo.r_data[72]),
                ]
            with m.Else():
                m.d.ss += head_v.eq(0)

        return m


class RxWidthSplitter(Elaboratable):
    """ 64-bit link data stream -> 32-bit protocol data stream.

    The 64-bit RX data stream is unbackpressured; a FIFO decouples it
    from the 1-word-per-cycle split.  ``first``/``last`` markers are
    preserved (first on the first word of a beat marked first; last on
    the FINAL word carrying valid bytes of a beat marked last).
    """

    def __init__(self, depth=64):
        self._depth = depth

        self.sink   = SuperSpeedStreamInterface(payload_words=8)
        self.source = SuperSpeedStreamInterface(payload_words=4)

        # Completion-strobe sideband: the packet_good/packet_bad
        # strobes travel THROUGH the FIFO as ordering-preserving
        # entries -- an endpoint must never see a verdict before the
        # payload words it covers.
        self.sink_good   = Signal()
        self.sink_bad    = Signal()
        self.source_good = Signal()
        self.source_bad  = Signal()

    def elaborate(self, platform):
        m = Module()
        sink, source = self.sink, self.source

        # Entries: {bad, good, last, first, valid[8], data[64]}.
        # Strobe entries carry valid == 0.
        m.submodules.fifo = fifo = DomainRenamer({"sync": "ss"})(
            SyncFIFO(width=64 + 8 + 4, depth=self._depth))

        strobe = self.sink_good | self.sink_bad
        m.d.comb += [
            fifo.w_data.eq(Cat(sink.data,
                               Mux(strobe, 0, sink.valid),
                               sink.first, sink.last,
                               self.sink_good, self.sink_bad)),
            fifo.w_en  .eq(sink.valid.any() | strobe),
            sink.ready .eq(fifo.w_rdy),
        ]

        e_data  = fifo.r_data[0:64]
        e_valid = fifo.r_data[64:72]
        e_first = fifo.r_data[72]
        e_last  = fifo.r_data[73]
        e_good  = fifo.r_data[74]
        e_bad   = fifo.r_data[75]
        high_has = e_valid[4:8].any()

        phase = Signal()    # 0: serve low half, 1: serve high half

        with m.If(fifo.r_rdy):
            with m.If(e_good | e_bad):
                # A verdict entry: pulse and retire.
                m.d.comb += [
                    self.source_good.eq(e_good),
                    self.source_bad .eq(e_bad),
                    fifo.r_en       .eq(1),
                ]
            with m.Elif(~phase):
                m.d.comb += [
                    source.valid.eq(e_valid[0:4]),
                    source.data .eq(e_data[0:32]),
                    source.first.eq(e_first),
                    # last only if the high half carries nothing.
                    source.last .eq(e_last & ~high_has),
                ]
                with m.If(source.ready):
                    with m.If(high_has):
                        m.d.ss += phase.eq(1)
                    with m.Else():
                        m.d.comb += fifo.r_en.eq(1)
            with m.Else():
                m.d.comb += [
                    source.valid.eq(e_valid[4:8]),
                    source.data .eq(e_data[32:64]),
                    source.first.eq(0),
                    source.last .eq(e_last),
                ]
                with m.If(source.ready):
                    m.d.ss += phase.eq(0)
                    m.d.comb += fifo.r_en.eq(1)

        return m
