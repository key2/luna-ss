Revision 1.1
June 2022

- 453 -

Universal Serial Bus 3.2
Specification

[tbl-259.md](tbl-259.md)

When the feature selector is PORT_U2_TIMEOUT, the most significant byte (bits 15..8) of the wIndex field specifies the Timeout value for the U2 inactivity timer. The port's link shall send an LMP to its link partner with the specified timeout value after receiving a Set Port Feature request with the PORT_U2_TIMEOUT feature selector. Refer to Section 10.4.2.1 for a detailed description of how the U2 inactivity timer value is used.

The following are permissible values:

Table 10-17. U2 Timeout Value Encoding

[tbl-260.md](tbl-260.md)

Note: It is the responsibility of software to properly set the U2 timeout for a downstream port that is connected to a hub. Inconsistent link states could result if the timeout is not set properly. It is recommended that software should set the upstream U2 timeout to at least twice the value of the U2 timeout of the downstream ports on the hub.

When the feature selector is PORT_LINK_STATE, the most significant byte (bits 15..8) of the wIndex field specifies the U state the host software wants to put the link connected to the port into. This request is only valid when the PORT_ENABLE bit is set and the PORT_LINK_STATE is not set to eSS.Disabled, Rx.Detect or eSS.Inactive except as noted below:

- If the value is 0, then the hub shall transition the link to U0 from any of the U states.
- If the value is 1, then host software wants to transition the link to the U1 State. The hub shall attempt to transition the link to U1 from U0. If the link is in any state other than U0 when a request is received with a value of 1, the behavior is undefined.
- If the value is 2, then the host software wants to transition the link to the U2 State. The hub shall attempt to transition the link to U2 from U0. If the link is in any state other than U0 when a request is received with a value of 2, the behavior is undefined.
- If the value is 3, then host software wants to selectively suspend the device connected to this port. The hub shall transition the link to U3 from any of the other U states using allowed link state transitions. If the port is not already in the U0 state, then it shall transition the port to the U0 state and then initiate the transition

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.