Universal Serial Bus 3.1 Specification, Revision 1.0

Note: If the queue for the appropriate downstream port is full, the header packet is queued as soon as a space is available for the appropriate downstream port. The hub shall process subsequent header packets while a downstream port buffer is full if they are directed to a different downstream port.

- If the header packet is an ITP then for each downstream port:

1. The ITP is silently discarded for any downstream port with a link not in U0 and not in Recovery.
2. The Delta and Correction fields in the ITP shall be updated to account for the measured delay of propagating the ITP through the hub.
a) If the delay introduced by the hub exceeds the tPropagationDelayJitterLimit, then the header packet shall be marked Delayed (DL) and the correct Link Control Word CRC-5 is re-calculated for modified header packet.
b) If the Delta subfield overflowed, the ITP shall not be queued, otherwise the header packet shall be queued for transmission on each downstream port that has completed Port Configuration and is in U0 or in Recovery.

Note: If the queue for the appropriate downstream port is full, the header packet is queued as soon as a space is available in the appropriate downstream port queue. The hub shall process subsequent header packets while a downstream port queue is full if they are directed to a different downstream port.

- If the header packet is routed to a disabled or nonexistent downstream port or to a downstream port that is in not in U0 and not in U1 and not in U2 and not in Recovery:

1. The header packet is removed from the RX header packet queue.
2. The header packet is silently discarded.
3. If the header packet is a DPH the corresponding DPP is silently discarded.

- If the header packet is routed to the hub controller:

1. The header packet is processed by the hub controller.
2. The header packet is removed from the RX header packet queue.
3. A response to the header packet is queued for transmission on the upstream port, if required.

### 10.9.4.4.2 SuperSpeedPlus Hub Upstream Facing Port

- The header packet is not an ITP and not a PING and is routed to a downstream port that is in U1 or in U2:

1. The hub initiates U0 entry on the appropriate downstream port link. U0 entry shall be initiated no later than tDownLinkStateChange from when the hub received the first symbol of the header packet.
2. If the header packet is not already marked deferred:

a) The header packet is marked deferred and the Link Control Word CRC-5 is re-calculated for the deferred header packet. If the deferred header packet is a DPH, the corresponding DPP is silently discarded.
b) A copy of the header packet is modified to include the hub's hub depth, marked as deferred and with the Link Control Word CRC-5 recalculated is buffered awaiting arbitration for transmission on the upstream port. Note that the route string in this deferred header packet is preserved and not set to zero.

3. The deferred header packet (see Section 7.2.4.1.4) is buffered awaiting arbitration (see Section 10.8.6.4) for transmission on the appropriate downstream port.

10-50