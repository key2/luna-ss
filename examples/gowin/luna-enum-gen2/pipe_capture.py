# Copyright (c) 2026 luna-ss contributors
# SPDX-License-Identifier: BSD-3-Clause
"""Circular PIPE beat capture, with an independently clocked UART dump.

All beat inputs and ``triggers`` belong to ``ss`` (the actual pclk, not the
half-rate MAC clock). While armed, every rising edge writes a beat, even dv=0.
Fields, trigger, and timestamp refer to that same edge. The complete RAM
write transaction is pipelined one edge, including address and enable; the
last captured beat therefore commits one edge after logical freeze.
``timestamp`` is a free-running 24-bit count of ss edges, modulo 2**24;
the value BEFORE the edge is stored. It keeps counting through freeze/rearm,
does not advance while pclk is stopped, and is not an absolute time across
rate changes. No core/pclk phase relationship is assumed here.

Power-on arms mode 0. The first selected trigger writes its own beat, then
exactly ``post_trigger`` further beats before freezing. Subsequent triggers
cannot extend that window. A full ring retains depth-post_trigger-1 prebeats
(31 with the 128/96 defaults). A partial ring only dumps entries actually
written. ``frozen``, ``triggered``, ``count``, ``trigger_index``, ``reason``,
``mode``, ``generation``, and ``timestamp`` are ss-domain status outputs;
trigger_index is the trigger's logical position in the final chronological
dump. Reason is 0=none, 1=long DPH, 2=trained-state fall, 3=manual. Capture state,
RAM, and the ss side of the mailbox ignore ss reset, preserving evidence
across link warm resets. Keep this outside the MAC's ss->core renaming.

``command`` and one-cycle ``command_strobe`` are in ``dbg``. Commands:
  '0' / '1' / '2': select long DPH / trained-state fall / manual and rearm;
  'A': rearm the current mode; 'T': trigger only in mode 2;
  'D': dump if frozen, otherwise do nothing; 'R' and other bytes: ignored.
The top converts its >18-DPH event to triggers[0] and a trained-state fall to
triggers[1]; this module does not determine which partner caused recovery.
Rearm is atomic at the ss mailbox acceptance edge, clears all validity and
trigger state, and takes priority over a coincident trigger. The next ss
edge is the first new sample. Generation starts at 0 and increments modulo
2**32 per rearm. Four commands can queue in dbg in addition to one in flight.
Only strobe recognized commands when ``command_ready`` is high; otherwise
the byte is dropped and ``command_overflow`` stays high until power-on.

One dump is automatic on freeze; 'D' allows replay. No empty or endless
sweeps. UART is AsyncSerialTX, 8N1, divisor floor(clk_freq/baud); ``tx_o`` is
the sole UART0 driver. All numeric fields below are fixed-width lowercase
hex, most significant digit first, with literal spaces and CRLF endings:

  P1 gggggggg cccc iiii r m pppp dddd\r\n
  R gggggggg jjjj ttttttccssssffffdddddddddddddddd\r\n
  E gggggggg\r\n

P1 identifies layout version 1: generation, valid record count (INCLUDING
dv=0), trigger index, reason, mode, post_trigger, depth. Each R has that
generation, logical index j (0..count-1), and one 128-bit record. E completes
the dump. Record fields, in Amaranth half-open bit notation:
  [0:64] data, [64] datavalid, [65] start_block, [66:70] sync_header,
  [70:75] fifo_level, [75:80] zero, [80:96] tx_state, [96:104] context,
  [104:128] timestamp. Thus hex groups are timestamp6/context2/state4/
  flags4/data16; context bits are defined by the integrating top.

Rearm during a dump finishes its in-flight line and emits ``X gggggggg``
plus CRLF instead of E (unless E was already being sent), BEFORE any new
epoch's records. The reader must treat X as an incomplete old dump. The RAM
is only released after this boundary. 'D' requests consumed at record
boundaries coalesce into one replay; requests arriving at the final record
or footer are handled after E. 'T' while frozen is ignored. Rearm cancels a
pending replay.

Commands, metadata snapshots, and RAM reads share one toggle request/ack
mailbox, following the shipping BurstEventCapture idiom. Payloads are held
until ack; only control toggles cross synchronizers. Metadata is captured
together in ss, then copied in dbg after ack. A synchronous ss RAM read gets
an extra holding-register cycle before ack, and validates generation/index.
No live multi-bit status is independently synchronized. A frozen ring stays
unchanged until an ordered rearm, so epochs cannot mix. Either clock may
pause: outstanding requests wait safely, but fetching needs ss edges and
serialization needs dbg edges. As with any UART, stopping dbg mid-byte
interrupts the physical baud timing; dbg must otherwise remain reset-less.
"""

from amaranth import Array, Cat, Const, DomainRenamer, Elaboratable, Module, Mux, Signal
from amaranth.lib.cdc import FFSynchronizer
from amaranth.lib.fifo import SyncFIFOBuffered
from amaranth.lib.memory import Memory

from gowin_serdes.bench import AsyncSerialTX


def capture_events(m, long_dph, trained):
    """Core events -> one pclk pulse each, including the detector's tail.

    A trained-state fall can precede long_dph's registered verdict by up
    to three core edges. Retain that fall until the first verdict arms us.
    Reason 2 is a trained-state fall, NOT proof of host-initiated recovery.
    """
    toggles = Signal(2)
    long_seen = Signal()
    trained_d = Signal()
    falls = Signal(3)
    falling = trained_d & ~trained
    m.d.core += [trained_d.eq(trained), falls.eq(Cat(falling, falls[:2]))]
    with m.If(long_dph):
        m.d.core += [long_seen.eq(1), toggles[0].eq(~toggles[0])]
    with m.If((long_seen & falling)
              | (~long_seen & long_dph & (falling | falls.any()))):
        m.d.core += toggles[1].eq(~toggles[1])
    sampled = Signal(2)
    delayed = Signal(2)
    m.d.ss += [sampled.eq(toggles), delayed.eq(sampled)]
    return sampled ^ delayed, long_seen


class PipeBeatCapture(Elaboratable):
    def __init__(self, clk_freq, baud=115_200, *, depth=128, post_trigger=96):
        if not isinstance(depth, int) or not 1 <= depth <= 32768 or depth & (depth - 1):
            raise ValueError("depth must be a power of two in 1..32768")
        if not isinstance(post_trigger, int) or not 0 <= post_trigger < depth:
            raise ValueError("post_trigger must be in 0..depth-1")
        if baud <= 0 or clk_freq < baud:
            raise ValueError("clk_freq must be at least baud, and baud must be positive")
        self._divisor = int(clk_freq // baud)
        self.depth = depth
        self.post_trigger = post_trigger

        self.data = Signal(64)
        self.datavalid = Signal()
        self.start_block = Signal()
        self.sync_header = Signal(4)
        self.fifo_level = Signal(5)
        self.tx_state = Signal(16)
        self.context = Signal(8)
        self.triggers = Signal(2)

        self.frozen = Signal(reset_less=True)
        self.triggered = Signal(reset_less=True)
        self.count = Signal(range(depth + 1), reset_less=True)
        self.trigger_index = Signal(range(depth), reset_less=True)
        self.reason = Signal(2, reset_less=True)
        self.mode = Signal(2, reset_less=True)
        self.generation = Signal(32, reset_less=True)
        self.timestamp = Signal(24, reset_less=True)

        self.command = Signal(8)
        self.command_strobe = Signal()
        self.command_ready = Signal(init=1)
        self.command_overflow = Signal(reset_less=True)
        self.tx_o = Signal(init=1)

    def elaborate(self, platform):
        m = Module()
        depth, post = self.depth, self.post_trigger
        REARM, MANUAL, SNAPSHOT, READ = 3, 4, 5, 6

        commands = SyncFIFOBuffered(width=3, depth=4)
        m.submodules.commands = DomainRenamer("dbg")(commands)
        recognized = Signal()
        with m.Switch(self.command):
            for char, operation in (("0", 0), ("1", 1), ("2", 2),
                                    ("A", REARM), ("T", MANUAL), ("D", SNAPSHOT)):
                with m.Case(ord(char)):
                    m.d.comb += [recognized.eq(1), commands.w_data.eq(operation)]
        m.d.comb += [
            commands.w_en.eq(self.command_strobe & recognized),
            self.command_ready.eq(commands.w_rdy),
        ]
        with m.If(self.command_strobe & recognized & ~commands.w_rdy):
            m.d.dbg += self.command_overflow.eq(1)

        # The entire request bundle stays unchanged from req until ack.
        req = Signal()
        opcode = Signal(3)
        read_index = Signal(16)
        request_generation = Signal(32)
        next_generation = Signal(32)
        req_s = Signal()
        ack = Signal(reset_less=True)
        ack_s = Signal()
        m.submodules += FFSynchronizer(req, req_s, o_domain="ss")
        m.submodules += FFSynchronizer(ack, ack_s, o_domain="dbg")

        reply_ok = Signal(reset_less=True)
        hold_record = Signal(128, reset_less=True)
        hold_generation = Signal(32, reset_less=True)
        hold_count = Signal(16, reset_less=True)
        hold_trigger = Signal(16, reset_less=True)
        hold_reason = Signal(4, reset_less=True)
        hold_mode = Signal(4, reset_less=True)
        read_wait = Signal(reset_less=True)
        auto_pending = Signal(reset_less=True)
        auto_s = Signal()
        m.submodules += FFSynchronizer(auto_pending, auto_s, o_domain="dbg")

        m.submodules.ring = ring = Memory(shape=128, depth=depth, init=[])
        wr = ring.write_port(domain="ss")
        rd = ring.read_port(domain="ss")
        wptr = Signal(range(depth), reset_less=True)
        remaining = Signal(range(post + 1), reset_less=True)
        new_request = (req_s != ack) & ~read_wait
        rearm = new_request & (opcode < MANUAL)
        fire = (((self.mode == 0) & self.triggers[0])
                | ((self.mode == 1) & self.triggers[1])
                | ((self.mode == 2) & new_request & (opcode == MANUAL)))

        # Register the WHOLE transaction so core->pclk half-select routing
        # terminates at movable FFs rather than the fixed RAM sites. Do not
        # gate the delayed write with frozen: that would lose the final beat.
        write_data = Signal(128, reset_less=True)
        write_addr = Signal.like(wptr, reset_less=True)
        write_enable = Signal(reset_less=True)
        m.d.ss += [
            write_enable.eq(~self.frozen & ~rearm),
            write_addr.eq(wptr),
            write_data.eq(Cat(self.data, self.datavalid, self.start_block,
                             self.sync_header, self.fifo_level, Const(0, 5),
                             self.tx_state, self.context, self.timestamp)),
        ]
        m.d.comb += [
            wr.en.eq(write_enable), wr.addr.eq(write_addr), wr.data.eq(write_data),
            rd.en.eq(0),
            rd.addr.eq(Mux(self.count == depth, wptr, 0) + read_index),
        ]

        # One source-side responder, with no overlapping reads or rearms.
        with m.If(read_wait):
            m.d.ss += [hold_record.eq(rd.data), reply_ok.eq(1),
                       read_wait.eq(0), ack.eq(req_s)]
        with m.Elif(new_request):
            m.d.ss += reply_ok.eq(0)
            with m.If(opcode == READ):
                with m.If(self.frozen & (read_index < self.count)
                          & (request_generation == self.generation)):
                    m.d.comb += rd.en.eq(1)
                    m.d.ss += read_wait.eq(1)
                with m.Else():
                    m.d.ss += ack.eq(req_s)
            with m.Else():
                m.d.ss += ack.eq(req_s)
                with m.If((opcode == SNAPSHOT) & self.frozen):
                    m.d.ss += [
                        hold_generation.eq(self.generation), hold_count.eq(self.count),
                        hold_trigger.eq(self.trigger_index), hold_reason.eq(self.reason),
                        hold_mode.eq(self.mode), reply_ok.eq(1), auto_pending.eq(0),
                    ]

        m.d.ss += self.timestamp.eq(self.timestamp + 1)
        with m.If(rearm):
            m.d.ss += [
                self.frozen.eq(0), self.triggered.eq(0), self.count.eq(0),
                self.trigger_index.eq(0), self.reason.eq(0), remaining.eq(0),
                wptr.eq(0), auto_pending.eq(0), self.generation.eq(request_generation),
            ]
            with m.If(opcode < REARM):
                m.d.ss += self.mode.eq(opcode)
        with m.Elif(~self.frozen):
            m.d.ss += wptr.eq(wptr + 1)
            with m.If(self.count < depth):
                m.d.ss += self.count.eq(self.count + 1)
            with m.If(~self.triggered & fire):
                m.d.ss += [
                    self.triggered.eq(1), self.reason.eq(self.mode + 1),
                    self.trigger_index.eq(Mux(self.count < depth - post - 1,
                                              self.count, depth - post - 1)),
                    remaining.eq(post),
                ]
                if post == 0:
                    m.d.ss += [self.frozen.eq(1), auto_pending.eq(1)]
            if post != 0:
                with m.Elif(self.triggered):
                    m.d.ss += remaining.eq(remaining - 1)
                    with m.If(remaining == 1):
                        m.d.ss += [self.frozen.eq(1), auto_pending.eq(1)]

        tx = AsyncSerialTX(divisor=self._divisor)
        m.submodules.tx = DomainRenamer("dbg")(tx)
        m.d.comb += self.tx_o.eq(tx.o)

        # Only held replies reach the formatter; nothing below is in pclk.
        generation = Signal(32)
        count = Signal(16)
        trigger_index = Signal(16)
        reason = Signal(4)
        mode = Signal(4)
        record = Signal(128)
        index = Signal(16)
        replay = Signal()
        HEADER, RECORD, END, ABORT = range(4)
        line_kind = Signal(2)
        cpos = Signal(range(50))
        line_size = Signal(range(51))

        def text(value):
            return [Const(ord(char), 9) for char in value]

        def hexchars(value, digits):
            result = []
            for digit in reversed(range(digits)):
                nibble = value[digit * 4:digit * 4 + 4]
                # Tag a nibble instead of instantiating one hex converter
                # per position; the selected token is converted just once.
                result.append(Cat(nibble, Const(0, 4), Const(1, 1)))
            return result

        header = (text("P1 ") + hexchars(generation, 8) + text(" ")
                  + hexchars(count, 4) + text(" ") + hexchars(trigger_index, 4)
                  + text(" ") + hexchars(reason, 1) + text(" ") + hexchars(mode, 1)
                  + text(f" {post:04x} {depth:04x}\r\n"))
        entry = (text("R ") + hexchars(generation, 8) + text(" ")
                 + hexchars(index, 4) + text(" ") + hexchars(record, 32) + text("\r\n"))
        footer = ([Mux(line_kind == ABORT, ord("X"), ord("E"))]
                  + text(" ") + hexchars(generation, 8) + text("\r\n"))
        token = Signal(9)
        nibble = token[:4]
        m.d.comb += tx.data.eq(Mux(token[8],
            Mux(nibble < 10, ord("0") + nibble, ord("a") - 10 + nibble), token[:8]))
        with m.Switch(line_kind):
            with m.Case(HEADER):
                m.d.comb += [token.eq(Array(header)[cpos]), line_size.eq(len(header))]
            with m.Case(RECORD):
                m.d.comb += [token.eq(Array(entry)[cpos]), line_size.eq(len(entry))]
            with m.Case(END, ABORT):
                m.d.comb += [token.eq(Array(footer)[cpos]), line_size.eq(len(footer))]

        with m.FSM(domain="dbg"):
            with m.State("IDLE"):
                with m.If(commands.r_rdy):
                    m.d.comb += commands.r_en.eq(1)
                    m.d.dbg += [opcode.eq(commands.r_data), req.eq(~req)]
                    with m.If(commands.r_data < MANUAL):
                        # The wide generation increment belongs in dbg, not pclk.
                        m.d.dbg += [next_generation.eq(next_generation + 1),
                                    request_generation.eq(next_generation + 1), replay.eq(0)]
                    with m.Elif(commands.r_data == SNAPSHOT):
                        m.d.dbg += replay.eq(0)
                    m.next = "WAIT"
                with m.Elif(auto_s | replay):
                    m.d.dbg += [opcode.eq(SNAPSHOT), req.eq(~req), replay.eq(0)]
                    m.next = "WAIT"

            with m.State("WAIT"):
                with m.If(ack_s == req):
                    m.d.dbg += cpos.eq(0)
                    with m.If(opcode == SNAPSHOT):
                        with m.If(reply_ok):
                            m.d.dbg += [
                                generation.eq(hold_generation), count.eq(hold_count),
                                trigger_index.eq(hold_trigger), reason.eq(hold_reason),
                                mode.eq(hold_mode), index.eq(0), line_kind.eq(HEADER),
                            ]
                            m.next = "SEND"
                        with m.Else():
                            m.next = "IDLE"
                    with m.Elif(opcode == READ):
                        m.d.dbg += [record.eq(hold_record),
                                    line_kind.eq(Mux(reply_ok, RECORD, ABORT))]
                        m.next = "SEND"
                    with m.Else():
                        m.next = "IDLE"

            with m.State("BOUNDARY"):
                with m.If(commands.r_rdy):
                    with m.If(commands.r_data >= MANUAL):
                        m.d.comb += commands.r_en.eq(1)
                        with m.If(commands.r_data == SNAPSHOT):
                            m.d.dbg += replay.eq(1)
                    with m.Else():
                        # Leave rearm queued until the old dump is explicitly closed.
                        m.d.dbg += line_kind.eq(ABORT)
                        m.next = "SEND"
                with m.Else():
                    m.d.dbg += [opcode.eq(READ), read_index.eq(index),
                                request_generation.eq(generation), req.eq(~req)]
                    m.next = "WAIT"

            with m.State("SEND"):
                m.d.comb += tx.ack.eq(1)
                with m.If(tx.rdy):
                    with m.If(cpos == line_size - 1):
                        m.d.dbg += cpos.eq(0)
                        with m.If(line_kind == HEADER):
                            m.next = "BOUNDARY"
                        with m.Elif(line_kind == RECORD):
                            with m.If(index == count - 1):
                                m.d.dbg += line_kind.eq(END)
                            with m.Else():
                                m.d.dbg += index.eq(index + 1)
                                m.next = "BOUNDARY"
                        with m.Else():
                            m.next = "IDLE"
                    with m.Else():
                        m.d.dbg += cpos.eq(cpos + 1)

        return m
