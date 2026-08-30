Universal Serial Bus 3.1 Specification, Revision 1.0

# C_PORT_LINK_STATE

This flag is used to signal completion of a transition from U3 → U0. Specifically, assertion of this flag results from a host initiated wakeup on a downstream port.

Once the C_PORT_LINK_STATE flag is set, a port status change event is sent to system software indicating that the downstream port and its link partner have completed the transition to the U0 state.

Note that C_PORT_LINK_STATE is not asserted in the event of a remote wakeup. As discussed previously, in the event of a Remote Wakeup the associated function sends the host a Function Wake device notification packet.

# PORT_U1_TIMEOUT

This feature is used to enable and disable U1 entry on downstream ports. It also specifies the U1 inactivity timeout value.

[tbl-271.md](tbl-271.md)

# PORT_U2_TIMEOUT

This feature is used to enable and disable U2 on downstream ports, and also to set an inactivity timeout for initiating a transition to U2.

[tbl-272.md](tbl-272.md)

Other hub port controls can impact link power management behavior, e.g., the PORT_RESET feature, but are not covered here (refer to Chapter 10 for details).

### C.1.3 Other Link Power Management Support Mechanisms

#### C.1.3.1 Packets Pending Flag

Devices may use the Packets Pending flag (refer to Chapter 8) to help decide when to place their link in a low power state. The Packets Pending flag provides an indication of whether the host controller has any additional packets to transfer on the schedule associated with a given non-Stream

C-8