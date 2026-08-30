Universal Serial Bus 3.1 Specification, Revision 1.0

- Protocol level endpoint flow control conditions, e.g., an endpoint having sent an NRDY
- Device class and device implementation
- U1 and U2 device-to-host exit latencies

U1 and U2 device-to-host exit latencies are the total latency to transition all links in the path between the device and the host to U0, when exit is initiated by the device. The device may assume a device-to-host exit latency based on the worst case exit latency (device connected five hubs deep). The device may alternatively use the device-to-host exit latency provided with the U1PEL and U2PEL fields of the SET_SEL request (refer to Chapter 9).

### C.3.2 Entry Conditions for U1 and U2

A device should initiate U1 or U2 when idle conditions are met for all its endpoints. A device typically initiates U1. However, if a device is able to determine that its link will not be needed for a long time, then the device may be able to initiate U2. For example, WiFi has a protocol where its radio may be shut off for long periods, e.g., 100 ms, and since the link is not needed during this time it may be placed in U2.

A device should initiate U2 if it is able to determine its link is not needed for a period of time that exceeds the U2 device-to-host exit latency (plus an appropriate guard band). The device should initiate U1 in all other cases.

Devices should consider the device-to-host exit latency when determining whether to initiate U1 and U2 entry. The host-to-device exit latency and the device-to-host exit latency are both considered by host software when determining whether to enable U1 or U2 on each link. Devices are enabled to initiate U1 and U2 with the U1_Enable and U2_Enable feature selectors (refer to Chapter 9).

The following subsections offer recommendations for determining when an endpoint is idle, or does not need to use the link for a known period, based on endpoint type. Idle conditions may be determined in other implementation specific ways.

### C.3.2.1 Control Endpoints

A control endpoint is idle when all of the following conditions are met:

- Device is in the configured state
- Device is not in the midst of a control transfer
- Either an NRDY was sent, or the Packets Pending flag was set to zero in the last ACK packet received from the host
- Device does not have a pending ERDY

### C.3.2.2 Bulk Endpoints

A bulk endpoint is idle when both of the following conditions are met:

- Either an NRDY was sent, or the Packets Pending flag was set to zero in the last ACK packet received from the host
- Device does not have a pending ERDY

Some devices can also determine that their link is not needed for a known period of time. For example, a mass storage device may need to spin up a spindle to service a request. Since the spin up time can be hundreds of milliseconds, the device should place its link in U2.

C-22