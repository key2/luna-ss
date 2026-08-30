Revision 1.1
June 2022

- 422 -

Universal Serial Bus 3.2
Specification

- If the downstream port to which the packet is being routed is operating in SuperSpeed mode and the header packet is a valid IN/ACK, save the transfer type (DFP.SAVE_TT) of the IN/ACK. The DFP.SAVE_TT is preserved until the next IN/ACK is received that is routed to the same downstream port. See Section 10.9.4.4.4.
- If the header packet is routed to the hub controller:
  1. The header packet is processed by the hub controller.
  2. The header packet is removed from the Upstream Receive buffer.
  3. A response to the header packet is buffered awaiting arbitration for transmission on the upstream port if required.

#### **10.9.4.4.3 SuperSpeed Hub Downstream Facing Port**

- The header packet is queued for transmission on the upstream port.

If the queue for the upstream port is full, the header packet is queued as soon as a space is available in the upstream port queue. The hub shall process subsequent header packets while the upstream port queue is full. If header packets have been received on more than one downstream port or are queued to be sent by the hub controller when a space becomes available in the upstream port header packet queue, the hub shall prioritize a non-data packet header over a data packet header packet if one is waiting at the front of a downstream queue or from the hub controller. Otherwise, the arbitration algorithm the hub uses is not specified.

Note: These arbitration requirements only apply across multiple downstream ports and the hub controller. For a single source (downstream port or hub controller), packets must be transmitted in the ordered received or generated.

#### **10.9.4.4.4 SuperSpeedPlus Hub Downstream Facing Port**

- If a valid DP is received then:
  1. If the port is operating in SuperSpeed mode then set the transfer type of the DP to the value of DFP.SAVE_TT. See Section 10.9.4.4.2.
  2. If the transfer type is asynchronous and the AW field value is zero, modify the AW field of the received DPH by setting the DPH.AW field to DFP.AW. See Section 10.8.6.
- The header packet is buffered awaiting arbitration for transmission on the upstream port (see Section 10.8.6).

#### **10.9.4.5 Rx Link Command**

In the Rx Link Command state, the port receiver is actively processing received symbols and looking for the speed specific indication of the end of a link command.

A port shall transition to the Rx Link Command state when it receives a valid speed specific indication of the beginning of a link command.

#### **10.9.4.6 Process Link Command**

Once the link command is received, the port shall perform all additional processing necessary for the link command. Any such processing shall not block the port from immediately returning to the Rx Default state.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.