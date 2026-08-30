Revision 1.1
June 2022

- 419 -

Universal Serial Bus 3.2
Specification

Table 10-3. Downstream Flowing Header Packet Processing Actions

[tbl-211.md](tbl-211.md)

The steps described in the next 4 sections depend on:

- whether the hub is operating as a SuperSpeed hub or a SuperSpeedPlus hub, and
- whether the port processing is being done for an upstream or downstream facing port.

#### 10.9.4.4.1 SuperSpeed Hub Upstream Facing Port

- The header packet is not an ITP and not a PING and is routed to a downstream port that is in U1 or in U2:

1. The hub initiates U0 entry on the appropriate downstream port link. U0 entry shall be initiated no later than tDownLinkStateChange from when the hub received the first symbol of the header packet.

2. If the header packet is not already marked deferred:

a) The header packet is marked deferred and the Link Control Word CRC-5 is re-calculated for the deferred header packet. If the deferred header packet is a DPH, the corresponding DPP is silently discarded.
b) A copy of the header packet is modified to include the hub's hub depth, marked as deferred and with the Link Control Word CRC-5 recalculated is queued for transmission on the upstream port. Note that the route string in this deferred header packet is preserved and not set to zero.

3. The deferred header packet (see Section 7.2.4.1.4) is queued for transmission on the appropriate downstream port.

- If the header packet is a PING and is routed to a downstream port that is in U0 or is in U1 or is in U2 or is in Recovery:

1. If the appropriate downstream port link is in U1 or in U2, the hub initiates U0 entry on the appropriate downstream port link. U0 entry shall be initiated no later than tDownLinkStateChange from when the hub received the first symbol of the header packet.

2. The header packet is queued for transmission on the appropriate downstream port.

- If the header packet is not an ITP and not a PING and is routed to a downstream port that is in U0 or in Recovery:

1. If the downstream port Tx header packet buffer queue is not empty (there is at least one header packet in the queue that has not been completely transmitted) or no link credit is available for transmission on the

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.