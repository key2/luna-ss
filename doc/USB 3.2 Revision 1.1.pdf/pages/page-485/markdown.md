Revision 1.1
June 2022

- 454 -

Universal Serial Bus 3.2
Specification

to U3. While this state is active, the hub does not propagate downstream-directed traffic to this port, but the hub will respond to resume signaling from the port.

- If the value is 4 (eSS.Disabled), the hub shall transition the link to eSS.Disabled. The request is valid at all times when the value is 4. The downstream port shall transition to the DSPORT.Disabled state after this request is received.
- If the value is 5 (Rx.Detect), the hub shall transition the link to Rx.Detect. This request is only valid when the downstream port is in the DSPORT.Disabled state. If the link is in any other state when a request is received with this value, the behavior is undefined. The downstream port shall transition to the DSPORT.Disconnected state after this request is received.
- If the value is 10 (Enable Compliance Mode), the hub shall enable entry into Compliance Mode for the next attach. This request is valid only when the downstream port is in the DSPORT.Disconnected state. If the link is in any other state when a request is received with this value, the behavior is undefined. Entry into Compliance Mode is disabled once the link enters Compliance Mode or Polling.LFPS succeeds.
- The hub shall respond with a Request Error if it sees any other value in the upper byte of the wIndex field.

When the feature selector is PORT_REMOTE_WAKE_MASK, the most significant byte (bits 15..8) of the wIndex field specifies the conditions that would cause the hub to signal a remote wake event on its upstream port. The encoding for the port remote wake mask is given below:

Table 10-18. Downstream Port Remote Wake Mask Encoding

[tbl-261.md](tbl-261.md)

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.