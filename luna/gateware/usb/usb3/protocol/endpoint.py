#
# This file is part of LUNA.
#
# Copyright (c) 2020 Great Scott Gadgets <info@greatscottgadgets.com>
# SPDX-License-Identifier: BSD-3-Clause
""" Endpoint abstractions for USB3. """

import operator
import functools

from amaranth import *

from .transaction import HandshakeGeneratorInterface, HandshakeReceiverInterface

from ..link.data   import DataHeaderPacket
from ....utils.bus import OneHotMultiplexer
from ...stream     import SuperSpeedStreamInterface

class SuperSpeedEndpointInterface:
    """ Interface that connects a USB3 endpoint module to a USB device.

    Many non-control endpoints won't need to use the latter half of this structure;
    it will be automatically removed by the relevant synthesis tool.

    Attributes
    ----------
    rx: SuperSpeedStreamInterface(), input stream to endpoint
        Receive interface for this endpoint. This stream's ``ready`` signal is ignored.
    rx_header: DataHeaderPacket(), input to endpoint
        The header associated with the packet currently being received.
    rx_complete: Signal(), input to endpoint
        Strobe that indicates that the concluding rx-stream was valid (CRC check passed).
    rx_invalid: Signal(), input to endpoint
        Strobe that indicates that the concluding rx-stream was invalid (CRC check failed).
    rx_new_header: Signal(), input to endpoint
        Strobe; indicates that a new header is available on rx_header.

    tx: SuperSpeedStreamInterface(), output stream from endpoint
        Transmit interface for this endpoint. This stream's ``valid`` must remain high for
        an entire packet; and it must respect the transmitter's ``ready`` signal.
    tx_zlp: Signal(), output from endpoint
        Strobe; when pulsed, triggers sending of a zero-length packet.
    tx_length: Signal(range(1024 + 1)), output from endpoint
        The length of the packet to be transmitted; required for generating its header.
    tx_endpoint_number: Signal(4), output from endpoint
        The endpoint number associated with the active transmission.
    tx_sequence_number: Signal(4), output from endpoint
        The sequence number associated with the active transmission.
    tx_direction: Signal(), output from endpoint
        The direction associated with the active transmission; used for control endpoints.

    active_address: Signal(7), input to endpoint
        Contains the device's current address.
    address_changed: Signal(), output from endpoint.
        Strobe; pulses high when the device's address should be changed.
    new_address: Signal(7), output from endpoint
        When :attr:`address_changed` is high, this field contains the address that should be adopted.

    active_config: Signal(8), input to endpoint
        The configuration number of the active configuration.
    config_changed: Signal(), output from endpoint
        Strobe; pulses high when the device's configuration should be changed.
    new_config: Signal(8)
        When `config_changed` is high, this field contains the configuration that should be applied.
    """

    def __init__(self):

        # Data packet reception.
        self.rx                    = SuperSpeedStreamInterface()
        self.rx_header             = DataHeaderPacket()
        self.rx_complete           = Signal()
        self.rx_invalid            = Signal()

        # Data packet transmission.
        self.tx                    = SuperSpeedStreamInterface()
        self.tx_zlp                = Signal()
        self.tx_length             = Signal(range(1024 + 1))
        self.tx_endpoint_number    = Signal(4)
        self.tx_sequence_number    = Signal(5)
        self.tx_direction          = Signal(init=1)

        # End-of-burst flag for the packet being transmitted: set on the
        # final data packet of a burst (grant exhausted, short packet, or
        # nothing further buffered), so a bursting host knows not to wait
        # for more packets on the current grant [USB3.2r1: 8.12.1.2].
        self.tx_eob                = Signal()

        # Strobe, driven by the protocol/link layer on the *shared* (mux)
        # interface only: the transmit parameters above have been latched
        # by the shared data-packet transmitter for the packet whose
        # transmission is beginning.  Until it fires, the parameters of
        # the previous packet are still live and must not be overwritten
        # by a new grant (bug #25).
        self.tx_parameters_consumed = Signal()

        # Handshaking / transaction packet exchange.
        self.handshakes_out        = HandshakeGeneratorInterface()
        self.handshakes_in         = HandshakeReceiverInterface()

        # Endpoint state.
        self.ep_reset              = Signal()

        # High while the link is out of U0 (training / recovery).  Burst
        # engines void their remaining grant on it: transaction-layer
        # credit does not meaningfully survive a retrain -- the host
        # re-establishes open bursts with fresh (retry) ACK TPs after
        # recovery, and transmitting on a stale grant races them.
        self.link_reset            = Signal()

        # Typically only used for control endpoints.
        self.active_address        = Signal(7)
        self.address_changed       = Signal()
        self.new_address           = Signal(7)

        self.active_config         = Signal(8)
        self.config_changed        = Signal()
        self.new_config            = Signal(8)



class SuperSpeedEndpointMultiplexer(Elaboratable):
    """ Multiplexes access to the resources shared between multiple endpoint interfaces.

    Interfaces are added using :attr:`add_interface`.

    Attributes
    ----------

    shared: SuperSpeedEndpointInterface
        The post-multiplexer endpoint interface.
    """

    def __init__(self):

        #
        # I/O port
        #
        self.shared = SuperSpeedEndpointInterface()

        # Debug taps (prunable): the first-added interface -- the control
        # endpoint in a standard device -- has latched (pending) handshake
        # requests, i.e. its next strobe is demoted off the same-cycle
        # fast path.  Bring-up visibility for the SET_ADDRESS contract.
        self.debug_pending0_any = Signal()
        self.debug_granted      = Signal()   # grant path active (any iface)
        self.debug_grant_is0    = Signal()   # grant parked on interface 0
        self.debug_pass_is0     = Signal()   # fast path selecting interface 0
        self.debug_bus          = Signal(16) # cycle-trace bus (see elaborate)

        #
        # Internals
        #
        self._interfaces = []


    def add_interface(self, interface: SuperSpeedEndpointInterface):
        """ Adds a EndpointInterface to the multiplexer.

        Arbitration is not performed; it's expected only one endpoint will be
        driving the transmit lines at a time.
        """
        self._interfaces.append(interface)


    def _multiplex_signals(self, m, *, when, multiplex):
        """ Helper that creates a simple priority-encoder multiplexer.

        Parmeters
        ---------
        when: str
            The name of the interface signal that indicates that the `multiplex` signals should be
            selected for output. If this signals should be multiplexed, it should be included in `multiplex`.
        multiplex: iterable(str)
            The names of the interface signals to be multiplexed.
        """

        # We're building an if-elif tree; so we should start with an If entry.
        conditional = m.If

        for interface in self._interfaces:
            condition = getattr(interface, when)

            with conditional(condition):

                # Connect up each of our signals.
                for signal_name in multiplex:

                    # Get the actual signals for our input and output...
                    driving_signal = getattr(interface,   signal_name)
                    target_signal  = getattr(self.shared, signal_name)

                    # ... and connect them.
                    m.d.comb += target_signal   .eq(driving_signal)

            # After the first element, all other entries should be created with Elif.
            conditional = m.Elif



    def elaborate(self, platform):
        m = Module()
        shared = self.shared

        #
        # Pass through signals being routed -to- our pre-mux interfaces.
        #

        # Register the incoming handshake events once, centrally, before
        # broadcasting them: they are decoded combinationally from the
        # header-RX queue, and fanning that cone straight into every
        # endpoint's FSM (and from there into same-cycle transmit-parameter
        # logic) creates critical paths well beyond the 8 ns budget of the
        # 125 MHz Gen1 clock.  These are single-cycle event strobes; the
        # endpoints are insensitive to one cycle of added latency.
        handshakes_in_q = HandshakeReceiverInterface()
        m.d.ss += handshakes_in_q.eq(shared.handshakes_in)

        # Register the packet-completion strobes for the same reason: they
        # are decoded combinationally from the data-packet receiver's CRC
        # comparison, and several endpoints turn them straight into
        # handshake strobes (ACK/NRDY) that feed the arbitration below --
        # a cone that misses 8 ns.  The strobes trail the payload by
        # multiple cycles already; one more is immaterial.
        rx_complete_q = Signal()
        rx_invalid_q  = Signal()
        m.d.ss += [
            rx_complete_q.eq(shared.rx_complete),
            rx_invalid_q .eq(shared.rx_invalid),
        ]

        for interface in self._interfaces:
            m.d.comb += [

                # Rx interface.
                interface.rx                     .tap(shared.rx),
                interface.rx_header              .eq(shared.rx_header),
                interface.rx_complete            .eq(rx_complete_q),
                interface.rx_invalid             .eq(rx_invalid_q),

                # Handshake exchange (registered copy; see above).
                handshakes_in_q                  .connect(interface.handshakes_in),

                # State signals.
                interface.ep_reset               .eq(shared.config_changed),
                interface.link_reset             .eq(shared.link_reset),
                interface.active_config          .eq(shared.active_config),
                interface.active_address         .eq(shared.active_address)
            ]

        #
        # Multiplex each of our transmit interfaces.
        #
        # Selection is packet-granular: once an interface has been granted
        # the shared transmit stream, it keeps it until it stops requesting
        # (i.e. until its packet's last word has been accepted and ``valid``
        # falls).  A purely combinational priority mux corrupts the stream
        # as soon as two endpoints transmit concurrently -- e.g. two bulk IN
        # endpoints answering interleaved host tokens: the later interface
        # steals the stream mid-packet, and its words are spliced into the
        # middle of the other endpoint's data packet on the wire.
        #
        # The grant is combinational for a new request into an idle mux
        # (preserving the original zero-latency dispatch), and registered
        # thereafter.  Endpoints hold ``valid`` for their whole packet, so
        # "still requesting" is exactly "packet still in progress"; the
        # non-granted endpoints simply see ``ready`` low and hold.
        #
        # ENCODING NOTE (GowinSynthesis V1.9.12.03 miscompile guard): the
        # "no owner" sentinel is 0 and interface ``i`` is encoded as
        # ``i + 1``.  With the natural encoding (sentinel = n = all-ones
        # of the signal at seven interfaces), the synthesizer constant-
        # folds comparisons against the sentinel (``owner != n`` becomes
        # constant true) and then deletes the entire dependent selection
        # logic as dead -- reproduced standalone with a 90-line Verilog
        # equivalent, netlist-vs-RTL (HANDOVER 10k).  A zero sentinel
        # synthesizes correctly.
        n_tx_none  = len(self._interfaces)
        tx_owner   = Signal(range(n_tx_none + 1), init=0)   # 0 = none
        tx_grant   = Signal.like(tx_owner)
        tx_reqs    = [iface.tx.valid.any() | iface.tx_zlp
                      for iface in self._interfaces]

        # Is the current owner still requesting?
        tx_owner_req = Signal()
        for i, req in enumerate(tx_reqs):
            with m.If(tx_owner == i + 1):
                m.d.comb += tx_owner_req.eq(req)

        # The captured transmit parameters (below) stay claimed from the
        # moment a grant locks until the shared data-packet transmitter
        # latches them for the packet whose transmission is beginning
        # (``tx_parameters_consumed``, plumbed back from the link layer).
        # A NEW grant must wait for that: a packet short enough to be
        # absorbed whole by the mux->skid->transmitter buffering releases
        # the grant while the chain is still backpressured, and an
        # unguarded next lock then overwrites the parameters before the
        # transmitter reads them -- the DPH goes out with the wrong
        # length/endpoint/sequence (bug #25; observed as a len=80 header
        # on an 8-byte DPP).  For packets larger than the chain depth the
        # consumption always precedes the grant release, so this defers
        # nothing in the common case.
        tx_params_busy = Signal()
        with m.If(shared.tx_parameters_consumed):
            m.d.ss += tx_params_busy.eq(0)

        # Grant: the locked owner while it requests; otherwise the
        # lowest-numbered requester (once the parameter registers are
        # free); otherwise none.  When an owner releases, one 'none'
        # cycle is inserted before the next grant: the shared data-packet
        # transmitter delimits packets by observing a one-cycle gap in
        # ``valid``, and a zero-gap handoff between two endpoints would
        # splice the next packet onto the previous one (its DPH is then
        # never generated, wedging the pipe).
        m.d.comb += tx_grant.eq(0)
        with m.If(tx_owner_req):
            m.d.comb += tx_grant.eq(tx_owner)
        with m.Elif(tx_owner != 0):
            pass                       # handoff gap cycle: grant none
        with m.Elif(~tx_params_busy):
            for i in reversed(range(len(self._interfaces))):
                with m.If(tx_reqs[i]):
                    m.d.comb += tx_grant.eq(i + 1)

        # The lock follows the grant (and releases to 'none' when idle).
        m.d.ss += tx_owner.eq(tx_grant)

        # The stream itself is muxed on the *registered* owner: selecting on
        # the combinational grant puts the all-endpoints valid/priority cone
        # in front of every endpoint's ready (and from there into their
        # packet-buffer addressing).  The one-cycle selection lag is benign:
        # a newly-granted stream simply starts a cycle later, and the
        # previous owner's valid has already fallen when its slot is reused.
        #
        # The transmit *parameters* (and any ZLP strobe) are captured into
        # registers at the moment the grant locks: endpoints drive them
        # combinationally only while sending, but the packet's words reach
        # the (buffered) data-packet transmitter a couple of cycles later --
        # a short packet's endpoint has already moved on by then, and the
        # generated header would sample all-zero length/endpoint fields.
        # The captured copy persists -- and blocks the next lock (see the
        # grant logic above) -- until the data-packet transmitter reports
        # it consumed them (``tx_parameters_consumed``).
        tx_p_len  = Signal.like(shared.tx_length)
        tx_p_ep   = Signal.like(shared.tx_endpoint_number)
        tx_p_seq  = Signal.like(shared.tx_sequence_number)
        tx_p_dir  = Signal.like(shared.tx_direction)
        tx_p_eob  = Signal()
        tx_zlp_q  = Signal()

        # A captured ZLP request is HELD until the transmitter consumes
        # it: the historical one-shot strobe was silently dropped
        # whenever the transmitter was still busy with an earlier packet
        # (same #25 family -- the ZLP is a parameter like any other).
        with m.If(shared.tx_parameters_consumed):
            m.d.ss += tx_zlp_q.eq(0)

        for i, interface in enumerate(self._interfaces):
            with m.If((tx_grant == i + 1) & (tx_owner != i + 1)):
                # Grant is locking onto this interface: capture (and
                # claim the parameter registers until consumption).
                m.d.ss += [
                    tx_p_len        .eq(interface.tx_length),
                    tx_p_ep         .eq(interface.tx_endpoint_number),
                    tx_p_seq        .eq(interface.tx_sequence_number),
                    tx_p_dir        .eq(interface.tx_direction),
                    tx_p_eob        .eq(interface.tx_eob),
                    tx_zlp_q        .eq(interface.tx_zlp),
                    tx_params_busy  .eq(1),
                ]

        m.d.comb += [
            shared.tx_zlp              .eq(tx_zlp_q),
            shared.tx_direction        .eq(tx_p_dir),
            shared.tx_endpoint_number  .eq(tx_p_ep),
            shared.tx_sequence_number  .eq(tx_p_seq),
            shared.tx_length           .eq(tx_p_len),
            shared.tx_eob              .eq(tx_p_eob),
        ]

        for i, interface in enumerate(self._interfaces):
            with m.If(tx_owner == i + 1):
                m.d.comb += shared.tx.stream_eq(interface.tx)


        #
        # Multiplex each of our handshake-out interfaces.
        #
        # Requests are latched per interface (edge-triggered, with their
        # parameters captured at strobe time) and serialized into the shared
        # handshake generator.  This makes single-cycle ``send_*`` strobes
        # lossless: previously two endpoints strobing in the same cycle (or
        # a strobe arriving while the generator was busy) silently dropped a
        # handshake -- e.g. a bulk OUT endpoint's ACK colliding with a bulk
        # IN endpoint's NRDY, which deadlocks the pipe.
        #
        # ``done`` is routed back kind-granularly: it is delivered to the
        # interface whose request is in flight, and only while that
        # interface is still asserting the *kind* of request that was
        # dispatched.  One interface can have several different-kind
        # requests outstanding (e.g. a fire-and-forget NRDY latched while
        # the generator was busy, followed by a held ERDY); each is
        # dispatched separately, and each completion clears only its own
        # kind.  Without this, the earlier request's ``done`` leaks into
        # the held one -- the holder releases unserved, its latched copy is
        # discarded with the grant, and the pipe wedges (observed as a
        # lost ERDY with four concurrently-active endpoint pairs).

        n_ifaces  = len(self._interfaces)
        kinds     = ('send_ack', 'send_nrdy', 'send_erdy', 'send_stall')
        K_ACK     = 0

        # Dispatch priority among simultaneously-pending kinds of one
        # interface, listed lowest-priority-first.  Chosen to match the
        # endpoints' emission order when several kinds are pending at once:
        # an ACK precedes any flow-control pair, and NRDY (park) must
        # precede ERDY (unpark) -- dispatching an ERDY before an older
        # latched NRDY puts "unpark, then park" on the wire, after which
        # the host waits forever for an ERDY the device believes it sent.
        KIND_PRIO_LOW_TO_HIGH = (2, 1, 3, 0)   # erdy < nrdy < stall < ack

        def select_kind(source, target, *, domain):
            """target <= one-hot highest-priority set bit of source."""
            for k in KIND_PRIO_LOW_TO_HIGH:
                with m.If(source[k]):
                    domain += target.eq(1 << k)

        pending   = [Signal(4,  name=f"hsk_pending_{i}") for i in range(n_ifaces)]
        p_epnum   = [Signal(7,  name=f"hsk_epnum_{i}")   for i in range(n_ifaces)]
        p_retry   = [Signal(    name=f"hsk_retry_{i}")   for i in range(n_ifaces)]
        p_nextseq = [Signal(5,  name=f"hsk_nextseq_{i}") for i in range(n_ifaces)]
        p_dir     = [Signal(    name=f"hsk_dir_{i}")     for i in range(n_ifaces)]
        p_dirv    = [Signal(    name=f"hsk_dirv_{i}")    for i in range(n_ifaces)]
        p_nump    = [Signal(5,  name=f"hsk_nump_{i}")    for i in range(n_ifaces)]
        p_numpv   = [Signal(    name=f"hsk_numpv_{i}")   for i in range(n_ifaces)]
        strobes_q = [Signal(4,  name=f"hsk_strobes_q_{i}") for i in range(n_ifaces)]

        # Materialize each interface's strobe vector and each pending
        # reduction as ONE named net, and use it at every consumer below.
        # The logic previously re-instantiated the same ``Cat(...)`` /
        # ``.any()`` expressions at five different consumers (fast-path
        # selection, presented-kind one-hot, completion gating, pending
        # bookkeeping, grant selection); GowinSynthesis V1.9.12.03 was
        # observed to miscompile that shape at seven interfaces (3 bulk
        # pairs): the duplicated cones DISAGREED on hardware -- the
        # fast path selected interface 0 while the presented-kind cone
        # read its strobes as zero, and the grant path read a stuck
        # pending vector as empty, wedging the first control transfer
        # (SET_ADDRESS ACK never generated; -71 on the host).  RTL sim,
        # adversarial fuzzing and timing all pass -- this is a synthesis
        # artifact of the same class as the 8b/10b pROM mis-inference
        # (syn_romstyle), dodged by giving the optimizer a single shared
        # net per reduction instead of clonable expression cones.
        strobes_v = [Signal(4, name=f"hsk_strobes_{i}") for i in range(n_ifaces)]
        pend_any  = [Signal(   name=f"hsk_pend_any_{i}") for i in range(n_ifaces)]
        for i, interface in enumerate(self._interfaces):
            m.d.comb += [
                strobes_v[i].eq(Cat(*(getattr(interface.handshakes_out, k)
                                      for k in kinds))),
                pend_any[i] .eq(pending[i].any()),
            ]
        m.d.comb += self.debug_pending0_any.eq(pend_any[0])

        # ENCODING NOTE: "no grant" sentinel is 0, interface ``i`` is
        # encoded as ``i + 1`` -- see the tx_owner encoding note above
        # (GowinSynthesis constant-folds comparisons against an all-ones
        # sentinel and deletes the arbiter; HANDOVER 10k).
        grant      = Signal(range(n_ifaces + 1), init=0)  # 0 = none
        granted    = (grant != 0)
        grant_kind = Signal(4)          # one-hot kind currently being served

        # Generator availability (driven back through the connect chain).
        generator_ready = shared.handshakes_out.ready

        # ── Tier 1: zero-latency pass-through ─────────────────────────────
        # When the arbiter is idle, the lowest-numbered interface that is
        # asserting a request is connected combinationally -- preserving
        # the original mux's timing contract.  This matters: the generator
        # samples context like the device address in the cycle a request
        # reaches it, and e.g. the SET_ADDRESS status-stage ACK must be
        # sent from the *old* address, which is only guaranteed when the
        # handler's strobe reaches the generator in the same cycle.
        pass_sel    = Signal(range(n_ifaces + 1), init=0)   # 0 = none
        pass_active = (pass_sel != 0)

        # Only the first-added interface -- the control endpoint in a
        # standard device -- is eligible for the fast path: it is the one
        # with a same-cycle dispatch contract (the SET_ADDRESS status ACK
        # must sample the pre-change address).  Widening eligibility puts
        # every interface's strobe cone into the pass selection, which
        # fans back into all the pending-latch enables and misses timing
        # with several endpoints.  Stream endpoints are edge-latched and
        # latency-insensitive; they dispatch through the grant path.
        m.d.comb += pass_sel.eq(0)
        with m.If(~granted):
            # An interface with older latched (pending) requests must be
            # served through the grant path in order; letting its newer
            # strobe cut the line would invert its request order.
            with m.If(strobes_v[0].any() & ~pend_any[0]):
                m.d.comb += pass_sel.eq(1)

        # The single kind the fast path is presenting right now (an
        # interface may assert more than one; the generator must only ever
        # see one, so completions stay attributable).
        pass_kind = Signal(4)
        for i, interface in enumerate(self._interfaces):
            with m.If(pass_active & (pass_sel == i + 1)):
                select_kind(strobes_v[i], pass_kind, domain=m.d.comb)

        # Track whether the request currently passed through has actually
        # been consumed by the generator -- and which kind it was: only
        # then does a ``done`` pulse belong to it.
        pass_sel_q      = Signal.like(pass_sel)
        pass_kind_q     = Signal(4)
        pass_dispatched = Signal()
        m.d.comb += [
            self.debug_granted  .eq(granted),
            self.debug_grant_is0.eq(grant == 1),
            self.debug_pass_is0 .eq(pass_sel == 1),
            # Cycle-trace bus: everything needed to reconstruct the
            # arbiter's handling of one interface-0 request.
            self.debug_bus.eq(Cat(
                pending[0],                                  # [3:0]
                strobes_v[0],                                # [7:4]
                pass_sel == 1,                               # [8]
                granted,                                     # [9]
                grant == 1,                                  # [10]
                generator_ready,                             # [11]
                Cat(*(getattr(shared.handshakes_out, k)
                      for k in kinds)),                      # [15:12]
            )),
        ]
        # debug taps
        self.debug_pass_sel   = pass_sel
        self.debug_grant      = grant
        self.debug_grant_kind = grant_kind
        self.debug_pending    = pending
        self.debug_pdisp      = pass_dispatched
        with m.If(pass_dispatched):
            # In flight: hold the dispatch record until the generator
            # completes it, regardless of what the (combinational) pass
            # selection does in the meantime -- a concurrent grant blanks
            # it, and dropping the record here loses the completion, which
            # re-dispatches held requests (duplicate TPs on the wire).
            with m.If(shared.handshakes_out.done):
                m.d.ss += pass_dispatched.eq(0)
        with m.Elif(pass_active & generator_ready):
            m.d.ss += [
                pass_dispatched.eq(1),
                pass_sel_q     .eq(pass_sel),
                pass_kind_q    .eq(pass_kind),
            ]

        for i, interface in enumerate(self._interfaces):
            with m.If(pass_active & (pass_sel == i + 1)):
                m.d.comb += [
                    shared.handshakes_out.endpoint_number
                        .eq(interface.handshakes_out.endpoint_number),
                    shared.handshakes_out.retry_required
                        .eq(interface.handshakes_out.retry_required),
                    shared.handshakes_out.next_sequence
                        .eq(interface.handshakes_out.next_sequence),
                    shared.handshakes_out.direction
                        .eq(interface.handshakes_out.direction),
                    shared.handshakes_out.direction_valid
                        .eq(interface.handshakes_out.direction_valid),
                    shared.handshakes_out.number_of_packets
                        .eq(interface.handshakes_out.number_of_packets),
                    shared.handshakes_out.number_of_packets_valid
                        .eq(interface.handshakes_out.number_of_packets_valid),
                    Cat(*(getattr(shared.handshakes_out, k) for k in kinds))
                        .eq(pass_kind),
                    interface.handshakes_out.ready
                        .eq(shared.handshakes_out.ready),
                ]
        # Deliver fast-path completions based on the dispatch record alone
        # (the live pass selection may already be blanked by a grant), and
        # only while the interface still asserts the dispatched kind
        # (fire-and-forget strobes are gone by then and nobody is
        # listening -- and a holder of a *different* kind must not be
        # released by it).
        for i, interface in enumerate(self._interfaces):
            with m.If(pass_dispatched & (pass_sel_q == i + 1)
                      & (pass_kind_q & strobes_v[i]).any()):
                m.d.comb += interface.handshakes_out.done \
                    .eq(shared.handshakes_out.done)

        # Watchdog for the granted path (self-healing; see below).
        watchdog = Signal(10)

        # The generator may still be busy completing an earlier (fast-path)
        # request when a grant begins; its `done` for that request must not
        # be mistaken for ours.  Our request is only in flight once the
        # generator has been seen ready (i.e. it sampled our strobes).
        grant_dispatched = Signal()

        # ── Pending bookkeeping (single assignment site per interface) ────
        for i, interface in enumerate(self._interfaces):
            strobes = strobes_v[i]

            # This interface's request is being dispatched right now iff it
            # is passed through while the generator is accepting requests.
            dispatched_now = pass_active & (pass_sel == i + 1) & generator_ready

            # Edge-detect the request strobes...
            m.d.ss += strobes_q[i].eq(strobes)
            rising = strobes & ~strobes_q[i]

            # Kinds completed this cycle, per tier.
            served_t1 = Signal(4, name=f"hsk_served_t1_{i}")
            served_t2 = Signal(4, name=f"hsk_served_t2_{i}")
            m.d.comb += served_t1.eq(Mux(dispatched_now, pass_kind, 0))
            m.d.comb += served_t2.eq(
                Mux((grant == i + 1) & grant_dispatched
                    & shared.handshakes_out.done, grant_kind, 0)
                | Mux((grant == i + 1) & granted & watchdog.all(), 0xF, 0))

            # Latch rising requests the fast path is not serving this very
            # cycle; clear kinds as their dispatches complete.
            m.d.ss += pending[i].eq(
                (pending[i] & ~served_t1 & ~served_t2)
                | (rising & ~served_t1))

            # Parameters are captured at strobe time.  Endpoint number and
            # direction are constant per interface; retry/next_sequence only
            # accompany ACKs, so only an ACK strobe may overwrite them.
            # (A re-strobed ACK while one is pending coalesces: the newest
            # cumulative sequence number / window supersedes the older.)
            with m.If(rising.any()):
                m.d.ss += [
                    p_epnum[i]  .eq(interface.handshakes_out.endpoint_number),
                    p_dir[i]    .eq(interface.handshakes_out.direction),
                    p_dirv[i]   .eq(interface.handshakes_out.direction_valid),
                    p_nump[i]   .eq(interface.handshakes_out.number_of_packets),
                    p_numpv[i]  .eq(interface.handshakes_out
                                    .number_of_packets_valid),
                ]
            with m.If(rising[K_ACK]):
                m.d.ss += [
                    p_retry[i]  .eq(interface.handshakes_out.retry_required),
                    p_nextseq[i].eq(interface.handshakes_out.next_sequence),
                ]

        # Grant: pick the lowest-numbered interface with a pending request
        # (only when the fast path is not actively passing a request), and
        # select the highest-priority pending kind to serve first.
        with m.If(~granted & ~pass_active):
            for i in reversed(range(n_ifaces)):
                with m.If(pend_any[i]):
                    m.d.ss += grant.eq(i + 1)
                    select_kind(pending[i], grant_kind, domain=m.d.ss)

        # Drive the shared generator from the granted request, one kind at
        # a time; on each completion, clear that kind and either move to
        # the next pending kind or release the grant.
        #
        # Self-healing: logic upstream of us may glitch during bring-up
        # (e.g. the boot window where pclk still runs above its eventual
        # rate); a corrupted grant with no pending request -- or a request
        # the generator never answers -- must not wedge the arbiter
        # forever, so empty grants release immediately and a generous
        # watchdog abandons unanswered ones (dropping the stuck request).
        with m.If(granted):
            m.d.ss += watchdog.eq(watchdog + 1)

            with m.If(generator_ready & ~grant_dispatched):
                m.d.ss += grant_dispatched.eq(1)

            for i, interface in enumerate(self._interfaces):
                with m.If(grant == i + 1):
                    m.d.comb += [
                        shared.handshakes_out.endpoint_number .eq(p_epnum[i]),
                        shared.handshakes_out.retry_required  .eq(p_retry[i]),
                        shared.handshakes_out.next_sequence   .eq(p_nextseq[i]),
                        shared.handshakes_out.direction       .eq(p_dir[i]),
                        shared.handshakes_out.direction_valid .eq(p_dirv[i]),
                        shared.handshakes_out.number_of_packets
                                                              .eq(p_nump[i]),
                        shared.handshakes_out.number_of_packets_valid
                                                              .eq(p_numpv[i]),
                        Cat(*(getattr(shared.handshakes_out, k) for k in kinds))
                            .eq(grant_kind & pending[i]),
                        interface.handshakes_out.ready
                            .eq(shared.handshakes_out.ready),
                    ]

                    # Kind-gated completion delivery (see the fast path).
                    with m.If(grant_dispatched
                              & (grant_kind & strobes_v[i]).any()):
                        m.d.comb += interface.handshakes_out.done \
                            .eq(shared.handshakes_out.done)

                    done_now  = shared.handshakes_out.done & grant_dispatched
                    remaining = pending[i] & ~grant_kind

                    with m.If(done_now):
                        with m.If(remaining.any()):
                            # Serve the next pending kind of this interface.
                            m.d.ss += grant_dispatched.eq(0)
                            select_kind(remaining, grant_kind, domain=m.d.ss)
                        with m.Else():
                            m.d.ss += [
                                grant.eq(0),
                                grant_dispatched.eq(0),
                            ]
                    with m.Elif(~pend_any[i] | watchdog.all()):
                        m.d.ss += [
                            grant.eq(0),
                            grant_dispatched.eq(0),
                        ]
        with m.Else():
            m.d.ss += [watchdog.eq(0), grant_dispatched.eq(0)]


        #
        # Multiplex the signals being routed -from- our pre-mux interface.
        #
        self._multiplex_signals(m,
            when='address_changed',
            multiplex=['address_changed', 'new_address']
        )
        self._multiplex_signals(m,
            when='config_changed',
            multiplex=['config_changed', 'new_config']
        )


        return m
