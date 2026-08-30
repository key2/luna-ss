Revision 1.1
June 2022

- 416 -

Universal Serial Bus 3.2
Specification

- From the Tx Link Command state when there are additional link commands queued for transmission.

### 10.9.3 Port Receive State Machine

This section describes the functional requirements of the upstream and downstream facing port receiver (Rx) state machine.

Figure 10-20. Upstream Facing Port Rx State Machine

![img-181.jpeg](img-181.jpeg)

### 10.9.4 Port Receive State Descriptions

#### 10.9.4.1 Rx Default

In the Rx Default state, the port receiver is actively receiving symbols and looking for the speed specific beginning of a valid packet or a link command.

A port receiver shall transition to the Rx Default state in any of the following situations:

- From the Rx Data state when a speed specific end of packet or abort indication is detected.
- From the Rx Header state when the last symbol of the header packet is received.
- After receiving a link command.
- As the default state when the link enters U0.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.