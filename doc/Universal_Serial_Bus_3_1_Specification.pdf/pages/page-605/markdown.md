Power Management

packet transmission model with multiple INs in flight. However, this does not impact the link power management as the packets are routed only through the ports directly between the host and device.

### C.1.2.2 Packet Deferring

Packet deferring is a mechanism that enables efficient bus utilization while supporting aggressive link power management. Packet deferring achieves this by enabling a hub to respond on behalf of a downstream device whose link is in a low power state. This allows the host to make forward progress while the device is brought back to the active state.

# **Hub's Role in Packet Deferring**

After receiving a header packet from the host and detecting a packet deferring condition, the hub informs the host of this by sending a deferred header packet back to the host. The hub also sends the original header packet to the device, with the deferred field asserted, once it is brought back to the U0 state. The host treats this deferred header packet as it would receipt of an NRDY, and so is then free to initiate transfers with other devices' endpoints instead of waiting for the sleeping link to return to U0 (refer to Chapter 10 for details).

# **Device's Role in Packet Deferring**

When a device receives an IN or an OUT header packet with the deferred field asserted, it prepares for the transfer, sends an ERDY to the host when ready, and keeps its link in U0 until the transfer occurs.

The host ultimately responds to the ERDY by rescheduling the original transfer.

### C.1.2.3 Software Interface

The software interface for downstream port power management consists of the following port controls and status fields:

- PORT_LINK_STATE feature and port status field
- PORT_REMOTE_WAKE_MASK feature
- C_PORT_LINK_STATE port status change bit
- PORT_U1_TIMEOUT feature
- PORT_U2_TIMEOUT feature

# **The PORT_LINK_STATE**

This feature is used to request a link state change from any current U-state to any next U-state. In a normal operating environment, this feature is used solely to request U0 → U3 and U3 → U0 transitions. It can be used for test purposes though, to request other state transitions.

# **The PORT_REMOTE_WAKE_MASK**

This feature is used to mask each remote wakeup event that might be originated at a downstream port.

Note that if remote wake notifications for connect, disconnect, or over current events are disabled, these events are still captured and reported as port status change events after the host or hub is resumed.

C-7