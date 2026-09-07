# Copyright (c) 2026 luna-ss contributors
# SPDX-License-Identifier: BSD-3-Clause
"""Passive checker for the 64-bit, dialect-neutral accepted MAC TX tap."""

from amaranth import Cat, Elaboratable, Module, Signal
from usb_protocol.types.superspeed import HeaderPacketType

from luna.gateware.usb.usb3.link.crc import (
    DataPacketPayloadCRC, HeaderPacketCRC, compute_usb_crc5,
)
from luna.gateware.usb.usb3.physical.coding import (
    EDB, END, EPF, SDP, SHP, SLC, get_word_for_symbols,
)


class Gen2TxWireChecker(Elaboratable):
    """Gen2-only TX monitor, clocked in ``ss`` (renamable to ``core``).

    Connect only the accepted, dialect-neutral MAC tap: ``data[0:8]`` is
    byte zero, ``ctrl[n]`` qualifies byte n, and ``strobe`` means accepted,
    not merely offered. All four inputs are registered. There is no ready
    output and no connection back into the functional path.

    The TX layout is [HPSTART, DW0], [DW1, DW2], [DW3, SDP-or-zero].
    Payload starts on the following beat; its length comes from DW1[16:32].
    All eight tail positions, CRC32, END and zero/Non-K padding are checked.
    This is not an arbitrarily aligned RX or physical Gen2-symbol decoder.

    Latency contract, with inputs sampled at rising edge N:

    * A final header beat produces ``cap_strobe``, ``tp_seen``/``dph_seen``
      and ``long_dph`` at N+2. Capture fields hold until the next capture;
      ``cap_type`` is all five DW0 type bits, ``cap_dw1`` is the full DW1.
      Counts include complete candidates with header faults, and all EPs.
      ``long_dph`` is exactly one pulse for each complete DPH of length >18.
    * A final length-delimited DPP tail produces ``dpp_seen`` and its
      framing/CRC verdict at N+2, including candidates with bad checks.
      An immediate, correctly padded DL=1 EDB also produces ``dpp_seen``
      and ``abort_seen`` at N+2, with no CRC32 check. Other EDBs are faults.
    * Header control/CRC16/CRC5/padding faults appear at N+2 of DW3.
      LC count and replica/CRC5/control faults appear at N+1 of LCSTART.
      Missing SDP, malformed HPSTART, illegal EDB and interrupted-packet
      faults appear at N+1 of the offending/resynchronizing beat.

    ``header_error`` never means DPPCRC. ``crc_error`` means CRC32 mismatch
    on a structurally valid DPP only; structural faults take precedence.
    An invalid header does not seed a payload CRC check with untrusted
    length. ``lc_seen`` counts LC candidates even if ``lc_error`` is set;
    no LCRD credit/sequence-order semantics are inferred.

    Strobe gaps have no timeout. A low-half, K-qualified HPSTART or LCSTART
    resynchronizes even inside a truncated packet; Non-K lookalikes cannot.
    Unrecognized traffic outside packets is ignored except damaged SHP
    framing with surviving K-qualified SHP symbols. Dropping ``enable``
    silently discards incomplete work; already complete verdicts drain.
    Each error has an ``*_sticky`` bit, cleared only by domain reset, plus
    the OR ``error_sticky``. Pulses and sticky updates are simultaneous.
    """

    def __init__(self):
        self.data = Signal(64)
        self.ctrl = Signal(8)
        self.strobe = Signal()
        self.enable = Signal()

        self.tp_seen = Signal()
        self.dph_seen = Signal()
        self.dpp_seen = Signal()
        self.long_dph = Signal()
        self.framing_error = Signal()
        self.crc_error = Signal()
        self.header_error = Signal()
        self.lc_seen = Signal()
        self.lc_error = Signal()
        self.abort_seen = Signal()

        self.cap_strobe = Signal()
        self.cap_type = Signal(5)
        self.cap_dw1 = Signal(32)

        self.framing_error_sticky = Signal()
        self.crc_error_sticky = Signal()
        self.header_error_sticky = Signal()
        self.lc_error_sticky = Signal()
        self.error_sticky = Signal()

    def elaborate(self, platform):
        m = Module()
        data = Signal(64)
        ctrl = Signal(8)
        strobe = Signal()
        enable = Signal()
        m.d.ss += [
            data.eq(self.data), ctrl.eq(self.ctrl),
            strobe.eq(self.strobe & self.enable), enable.eq(self.enable),
        ]

        idle, header1, header2, payload, tail = range(5)
        state = Signal(range(5), init=idle)
        remaining = Signal(16)
        first_payload = Signal()
        payload_bad = Signal()

        hp_data, _ = get_word_for_symbols(SHP, SHP, SHP, EPF)
        sdp_data, _ = get_word_for_symbols(SDP, SDP, SDP, EPF)
        end_data, _ = get_word_for_symbols(END, END, END, EPF)
        edb_data, _ = get_word_for_symbols(EDB, EDB, EDB, EPF)
        lc_data, _ = get_word_for_symbols(SLC, SLC, SLC, EPF)
        hpstart = (data[:32] == hp_data) & (ctrl[:4] == 0xF)
        lcstart = (data[:32] == lc_data) & (ctrl[:4] == 0xF)
        edb = (data[:32] == edb_data) & (ctrl[:4] == 0xF)
        damaged_hp = (
            (ctrl[0] & (data[:8] == SHP.value))
            | (ctrl[1] & (data[8:16] == SHP.value))
            | (ctrl[2] & (data[16:24] == SHP.value))
        )

        # One-beat CRC input pipeline allows a fresh HPSTART to clear the
        # CRC even on resync. DW0 advances next clock, then DW1/DW2; DW3
        # waits in a register, so header checking needs no CRC lookahead.
        m.submodules.crc16 = crc16 = HeaderPacketCRC(words=2)
        header_word = Signal(32)
        header_pair = Signal(64)
        header_end = Signal(32)
        header_one = Signal()
        header_two = Signal()
        header_pending = Signal()
        header_ctrl_bad = Signal()
        header_fault = Signal()
        kind = header_word[:5]
        is_data = kind == HeaderPacketType.DATA
        m.d.comb += [
            crc16.clear.eq(~enable | (strobe & hpstart)),
            crc16.data_input.eq(header_word), crc16.advance_crc.eq(header_one),
            crc16.data_input2.eq(header_pair), crc16.advance_crc2.eq(header_two),
            header_fault.eq(header_ctrl_bad | (header_end[:16] != crc16.crc)
                            | (header_end[27:32] != compute_usb_crc5(header_end[16:27]))),
        ]
        reject_header = header_pending & header_fault

        m.submodules.crc32 = crc32 = DataPacketPayloadCRC(words=2)
        m.d.comb += [
            crc32.data_input2.eq(data),
            crc32.clear.eq(~enable | ((state != payload) & (state != tail))),
        ]
        tail_first_data = Signal(64)
        tail_first_ctrl = Signal(8)
        tail_count = Signal(3)
        wire_crc = Signal(32)
        expected_crc = Signal(32)
        tail_bad = Signal()
        dpp_pending = Signal()
        aborted_pending = Signal()

        framing_fault = Signal()
        header_fault_event = Signal()
        crc_fault = Signal()
        lc_fault = Signal()
        m.d.comb += [
            framing_fault.eq(dpp_pending & tail_bad),
            header_fault_event.eq(reject_header),
            crc_fault.eq(dpp_pending & ~aborted_pending & ~tail_bad
                         & (wire_crc != expected_crc)),
            lc_fault.eq(0),
        ]
        for name, fault in (
            ("framing_error", framing_fault), ("header_error", header_fault_event),
            ("crc_error", crc_fault), ("lc_error", lc_fault),
        ):
            sticky = getattr(self, name + "_sticky")
            m.d.ss += [getattr(self, name).eq(fault), sticky.eq(sticky | fault)]
        m.d.comb += self.error_sticky.eq(
            self.framing_error_sticky | self.header_error_sticky
            | self.crc_error_sticky | self.lc_error_sticky)

        # These verdict pipelines run independently of the parser, including
        # after enable falls. Returning to IDLE never eats the next HPSTART.
        m.d.ss += [
            header_one.eq(0), header_two.eq(0), header_pending.eq(0), dpp_pending.eq(0),
            self.tp_seen.eq(header_pending & (kind == HeaderPacketType.TRANSACTION)),
            self.dph_seen.eq(header_pending & is_data),
            self.long_dph.eq(header_pending & is_data & (header_pair[16:32] > 18)),
            self.cap_strobe.eq(header_pending), self.dpp_seen.eq(dpp_pending),
            self.abort_seen.eq(dpp_pending & aborted_pending), self.lc_seen.eq(0),
        ]
        with m.If(header_pending):
            m.d.ss += [self.cap_type.eq(kind), self.cap_dw1.eq(header_pair[:32])]

        with m.If(~enable):
            m.d.ss += [state.eq(idle), first_payload.eq(0)]

        with m.Elif(strobe & (hpstart | lcstart)):
            with m.If((state == header1) | (state == header2)):
                m.d.comb += header_fault_event.eq(1)
            with m.Elif(((state == payload) | (state == tail)) & ~reject_header):
                m.d.comb += framing_fault.eq(1)
            with m.If(hpstart):
                m.d.ss += [
                    header_word.eq(data[32:64]), header_one.eq(1),
                    header_ctrl_bad.eq(ctrl[4:8].any()), state.eq(header1),
                ]
            with m.Else():
                command = data[32:48]
                m.d.ss += [self.lc_seen.eq(1), state.eq(idle)]
                m.d.comb += lc_fault.eq(
                    ctrl[4:8].any() | (command != data[48:64])
                    | (command[11:16] != compute_usb_crc5(command[:11])))

        with m.Elif(reject_header):
            m.d.ss += state.eq(idle)

        with m.Elif(strobe):
            with m.Switch(state):
                with m.Case(idle):
                    with m.If(damaged_hp):
                        m.d.comb += header_fault_event.eq(1)

                with m.Case(header1):
                    m.d.ss += [
                        header_pair.eq(data), header_two.eq(1),
                        header_ctrl_bad.eq(header_ctrl_bad | ctrl.any()),
                        state.eq(header2),
                    ]

                with m.Case(header2):
                    m.d.ss += [
                        header_end.eq(data[:32]), header_pending.eq(1),
                        header_ctrl_bad.eq(header_ctrl_bad | ctrl[:4].any()
                                           | (~is_data & ((data[32:64] != 0)
                                                          | ctrl[4:8].any()))),
                        state.eq(idle),
                    ]
                    with m.If(is_data):
                        with m.If((data[32:64] == sdp_data) & (ctrl[4:8] == 0xF)):
                            m.d.ss += [
                                remaining.eq(header_pair[16:32]), payload_bad.eq(0),
                                first_payload.eq(1), state.eq(payload),
                            ]
                        with m.Else():
                            m.d.comb += framing_fault.eq(1)

                with m.Case(payload):
                    m.d.ss += first_payload.eq(0)
                    with m.If(edb):
                        m.d.ss += state.eq(idle)
                        with m.If(first_payload & header_end[25]
                                  & (data[32:64] == 0) & (ctrl[4:8] == 0)):
                            m.d.ss += [
                                dpp_pending.eq(1), aborted_pending.eq(1), tail_bad.eq(0),
                            ]
                        with m.Else():
                            m.d.comb += framing_fault.eq(1)
                    with m.Elif(remaining >= 8):
                        m.d.comb += crc32.advance_2words.eq(1)
                        m.d.ss += [
                            remaining.eq(remaining - 8),
                            payload_bad.eq(payload_bad | ctrl.any()),
                        ]
                    with m.Elif(remaining == 0):
                        m.d.ss += [
                            wire_crc.eq(data[:32]), expected_crc.eq(crc32.crc),
                            tail_bad.eq(payload_bad | (ctrl != 0xF0)
                                        | (data[32:64] != end_data)),
                            dpp_pending.eq(1), aborted_pending.eq(0), state.eq(idle),
                        ]
                    with m.Else():
                        # Advance only the n payload bytes. CRC compare is
                        # deliberately after this advance has been registered.
                        for n in range(1, 8):
                            with m.If(remaining == n):
                                m.d.comb += getattr(crc32, f"advance_{n}B").eq(1)
                        m.d.ss += [
                            tail_first_data.eq(data), tail_first_ctrl.eq(ctrl),
                            tail_count.eq(remaining[:3]), state.eq(tail),
                        ]

                with m.Case(tail):
                    m.d.ss += [
                        expected_crc.eq(crc32.crc), dpp_pending.eq(1),
                        aborted_pending.eq(0), state.eq(idle),
                    ]
                    # Constant slices, not eight serial byte-FSM stages or a
                    # variable shifter in front of the CRC feedback path.
                    with m.Switch(tail_count):
                        for n in range(1, 8):
                            with m.Case(n):
                                joined_data = Cat(tail_first_data[8 * n:], data[:8 * n])
                                joined_ctrl = Cat(tail_first_ctrl[n:], ctrl[:n])
                                m.d.ss += [
                                    wire_crc.eq(joined_data[:32]),
                                    tail_bad.eq(payload_bad | tail_first_ctrl[:n].any()
                                                | (joined_ctrl != 0xF0)
                                                | (joined_data[32:64] != end_data)
                                                | (data[8 * n:] != 0) | ctrl[n:].any()),
                                ]
        return m
