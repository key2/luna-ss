Hub, Host Downstream Port, and Device Upstream Port Specification

- If the header packet is a PING and is routed to a downstream port that is in U0 or is in U1 or is in U2 or is in Recovery:

1. If the appropriate downstream port link is in U1 or in U2, the hub initiates U0 entry on the appropriate downstream port link. U0 entry shall be initiated no later than tDownLinkStateChange from when the hub received the first symbol of the header packet.
2. The header packet is buffered awaiting arbitration for transmission on the appropriate downstream port.

- If the header packet is not an ITP and not a PING and is routed to a downstream port that is in U0 or in Recovery:

1. If the downstream port is currently transmitting a packet or there is at least one packet buffered that will be selected before this packet or no link credit is available for transmission on the downstream port, the header packet is marked delayed and the Link Control Word CRC-5 is re-calculated for modified header packet.
2. The header packet is buffered awaiting arbitration for transmission on the appropriate downstream port.

- If the header packet is an ITP then for each downstream port:

1. The ITP is silently discarded for any downstream port with a link not in U0 and not in Recovery.
2. The Delta and Correction fields in the ITP shall be updated to account for the measured delay of propagating the ITP through the hub.

a) If the delay introduced by the hub exceeds the tPropagationDelayJitterLimit, then the header packet shall be marked Delayed (DL) and the correct Link Control Word CRC-5 is re-calculated for modified header packet.
b) If the Delta subfield overflowed, the ITP shall not be buffered, otherwise the header packet is buffered awaiting arbitration for transmission on each downstream port that has completed Port Configuration and is in U0 or in Recovery.

- If the header packet is routed to a disabled or nonexistent downstream port or to a downstream port that is in not in U0 and not in U1 and not in U2 and not in Recovery:

1. The header packet is removed from the Upstream Receive buffer.
2. The header packet is silently discarded.
3. If the header packet is a DPH the corresponding DPP is silently discarded.

- If the downstream port to which the packet is being routed is operating at Gen 1 speed and the header packet is a valid IN/ACK, save the transfer type (DFP.SAVE_TT) of the IN/ACK. The DFP.SAVE_TT is preserved until the next IN/ACK is received that is routed to the same downstream port. See Section 10.9.4.4.4.

- If the header packet is routed to the hub controller:

1. The header packet is processed by the hub controller.
2. The header packet is removed from the Upstream Receive buffer.
3. A response to the header packet is buffered awaiting arbitration for transmission on the upstream port if required.

### 10.9.4.4.3 SuperSpeed Hub Downstream Facing Port

- The header packet is queued for transmission on the upstream port.

If the queue for the upstream port is full, the header packet is queued as soon as a space is available in the upstream port queue. The hub shall process subsequent header packets while the upstream port queue is full. If header packets have been received on more than one downstream port or are queued to be sent by the hub controller when a space becomes available

10-51