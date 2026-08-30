Power Management

After a device has sent an ERDY associated with a bulk endpoint, the link should be kept in U0 until the host sends a request in response to the ERDY (or until the tERDYTimeout occurs, refer to Section 8.13).

### C.3.2.3 Interrupt Endpoints

An interrupt endpoint is idle when both of the following conditions are met:

- Either an NRDY was sent, or the Packets Pending flag was set to zero in the last ACK packet received from the host.

After a device has sent an ERDY associated with an interrupt endpoint, the link should be kept in U0 until the host sends a request in response to the ERDY (or until the tERDYTimeout occurs) in order to achieve the subscribed interrupt service latency. However, when all transfers for a given service interval have been completed, the endpoint will not need the link until the next service interval. The device may be able to place its link in U1 or U2 during this time. The End of Burst flag can be used to determine when all transfers for a given service interval are completed. Note that hosts are required to initiate interrupt transfers far enough ahead of a transfer window to meet subscribed service requirements.

### C.3.2.4 Isochronous Endpoints

An isochronous endpoint is idle when all transfers for a given service interval have been completed, as indicated by the Last Packet flag. The endpoint will not need the link until the next service interval. Note that the host is required to send a PING packet far enough ahead of a transfer window to meet subscribed service requirements.

### C.3.2.5 Devices That Need Timestamp Packets

When a device needs timestamp information, it needs to ensure that its link is in U0 when the next bus interval boundary is reached in order to receive a timestamp packet. If the device’s link is not in U0, it should transition to U0 prior to the next bus interval boundary. The device must track when the bus interval boundary will occur. The device initiates a transition to U0 a period of time before the bus interval boundary occurs, where the period of time is the device-to-host link exit latency.

## C.4 Latency Tolerance Message (LTM) Implementation Example

Computer systems typically maintain a high state of readiness to service devices even when the computer system is idle. LTM supports a mechanism for a system to reduce its state of readiness with the cooperation of Enhanced SuperSpeed devices. This may result in substantial system power savings without requiring additional cost to devices.

This section provides a device implementation example for LTM support. This example is based on a model using two device Latency Tolerance states, an active state and an idle state. Each state has a different Best Effort Latency Tolerance (BELT).

C-23