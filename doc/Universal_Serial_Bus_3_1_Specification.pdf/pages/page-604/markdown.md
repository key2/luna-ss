Universal Serial Bus 3.1 Specification, Revision 1.0

# Exiting the U3 State

The only legitimate link state transition from U3 is U3 → U0, and either link partner can initiate it.

Host software initiates U3 exit on a downstream port by issuing a

SetPortFeature(PORT_LINK_STATE) request to the desired downstream port. Upstream ports (e.g., upstream port of a hub, or a peripheral device), initiate U3 exit in response to a remote wakeup event. An example of this would be an incoming Wake on LAN packet for a USB attached network interface device. The exit process consists of a Low Frequency Periodic Signaling (LFPS) handshake followed by link recovery and training.

# Device Initiated U3 Exit

If the exit was initiated by a device, the specific function within the device that initiated the wakeup would follow up the LFPS triggered transition to U0 by sending a Function Wake device notification packet to the host.

# Host initiated U3 Exit

For host initiated U3 exit, the LFPS handshake process allows devices up to 20 ms to complete, allowing sufficient time for a device to turn on a switched power rail if implemented (refer to Chapter 6 for details).

The software interface associated with U3 consists of a set of port controls and function controls. The port controls, e.g., initiating U3 on a hub downstream port, are described in Section C.1.2.3. The function controls, e.g., enabling a function (device) for remote wakeup, are described in Section C.1.4.1.

# C.1.2 Link Power Management for Downstream Ports

Hubs play several critical roles in link power management. They perform the following functions:

- Coordinate the upstream port link power management state with that of their downstream ports.
- Handle packet deferral, where the hub tells the host that a packet was sent to a downstream port that is not currently in U0.
- Provide inactivity timers on downstream ports to initiate U1 and U2 entry.

# C.1.2.1 Link State Coordination and Management

A hub monitors its downstream ports' link states and keeps its upstream port in the lowest power link state it can without allowing it to be in a lower power state than any of its downstream ports. The intent for this policy is to ensure that the path to the host, (i.e., the upstream port), is as active as the most active of its downstream ports.

When a device initiates a transition from a low power state back to U0 on a hub downstream port, the hub begins transitioning its upstream port to U0 immediately, in parallel with the downstream port.

For packets traveling downstream, hubs must first receive the packet, determine which of its downstream ports the packet is targeted at, and then only initiate a transition to U0 for that particular downstream port.

USB 3.0 hubs use a unicast packet transmission model and this improves the power efficiency of the platform in every instance where a hub is deployed. USB 3.1 hubs use a store and forward

C-6