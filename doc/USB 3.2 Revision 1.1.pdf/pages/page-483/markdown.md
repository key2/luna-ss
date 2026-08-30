Revision 1.1
June 2022

- 452 -

Universal Serial Bus 3.2
Specification

It is a Request Error if wValue is greater than 4 or if wIndex or wLength are not as specified above.

If the hub is not configured, the hub's response to this request is undefined.

### 10.16.2.10 Set Port Feature

This request sets a value reported in the port status.

[tbl-257.md](tbl-257.md)

The port number shall be a valid port number for that hub, greater than zero. The port number is in the least significant byte (bits 7..0) of the wIndex field. The most significant byte of wIndex is zero, except when the feature selector is PORT_U1_TIMEOUT or PORT_U2_TIMEOUT or PORT_LINK_STATE or PORT_REMOTE_WAKE_MASK.

Setting a feature enables that feature or starts a process associated with that feature; see Table 10-9 for the feature selector definitions that apply to a port as a recipient. Status change may not be acknowledged using this request. Features that can be set with this request are:

- PORT_RESET
- BH_PORT_RESET
- PORT_POWER
- PORT_U1_TIMEOUT
- PORT_U2_TIMEOUT
- PORT_LINK_STATE
- PORT_REMOTE_WAKE_MASK
- FORCE_LINKPM_ACCEPT

When the feature selector is PORT_U1_TIMEOUT, the most significant byte (bits 15..8) of the wIndex field specifies the Timeout value for the U1 inactivity timer. Refer to Section 10.4.2.1 for a detailed description of how the U1 inactivity timer value is used.

The following are permissible values:

Table 10-16. U1 Timeout Value Encoding

[tbl-258.md](tbl-258.md)

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.