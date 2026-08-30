Revision 1.1
June 2022

- 49 -

Universal Serial Bus 3.2
Specification

### 4.4.9 Device Notifications

Device notifications are a standard method for a device to communicate asynchronous device- and bus-level event information to the host. This feature does not map to the pipe model defined for the standard transfer types. Device notifications are always initiated by a device and the flow of data information is always device to host.

Device notifications are message-oriented data communications that have a specific data format structure as defined in Section 8.5.6. Device notifications do not have any data payload. Devices can send a device notification at any time.

### 4.4.10 Reliability

To ensure reliable operation, several layers of protection are used. This provides reliability for both flow control and data end to end.

#### 4.4.10.1 Physical Layer

The Enhanced SuperSpeed physical layer provides bit error rates less than 1 bit in 10¹² bits.

#### 4.4.10.2 Link Layer

The Enhanced SuperSpeed link layer has mechanisms that ensure a bit error rate less than 1 bit in 10²⁰ bits for header packets. The link layer uses a number of techniques including packet framing ordered sets, link level flow control and retries to ensure reliable end-to-end delivery for header packets.

#### 4.4.10.3 Protocol Layer

The Enhanced SuperSpeed protocol layer depends on a 32-bit CRC appended to the Data Payload and a timeout coupled with retries to ensure that reliable data is provided to the application.

### 4.4.11 Efficiency

Enhanced SuperSpeed communications efficiency is dependent on a number of factors, including line encoding, packet structure and framing, link level flow control and protocol overhead.

For links that operate at Gen 1x1 speed (5 Gbps and 8b/10b line encoding) the raw throughput is 500 MB/sec. Accounting for flow control, packet framing and protocol overheads reduces the effective bandwidth down to 450 MB/sec or less to be delivered to an application. The effective bandwidth is doubled in Gen 1x2 operation.

For links that operate at Gen 2x1 speed (10 Gbps and 128b/132b line encoding) the raw throughput is approximately 1.2 GB/sec. Accounting for flow control, packet framing, and protocol overheads reduces the best case effective bandwidth down to approximately 1.1 GB/sec or less to be delivered to an application. Also, effective bandwidth of individual endpoint flows can be affected by interaction with other simultaneously active endpoint flows traversing through SuperSpeedPlus hub arbiters. The effective bandwidth is doubled in Gen 2x2 operation.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.