Revision 1.1
June 2022

- 344 -

Universal Serial Bus 3.2
Specification

#### 9.4.11 Set Isochronous Delay

This request informs the device of the delay from the time a host transmits a packet to the time it is received by the device.

[tbl-171.md](tbl-171.md)

The wValue field specifies a delay from 0 to 65535 ns. This delay represents the time from when the host starts transmitting the first framing symbol of the packet to when the device receives the first framing symbol of that packet. The wValue field shall be calculated as follows.

\[
w V a l u e = (s u m o f w H u b D e l a y v a l u e s) + (t T P T r a n s m i s s i o n D e l a y * (n u m b e r o f h u b s + 1))
\]

Where, a wHubDelay value is provided by the Enhanced SuperSpeed Hub Descriptor of each hub in the path, respectively, and tTPTransmissionDelay is defined in Table 8-35.

If wIndex or wLength is non-zero, then the behavior of this request is not specified.

Default state: This is a valid request when the device is in the Default state.

Address state: This is a valid request when the device is in the Address state.

Configured state: This is a valid request when the device is in the Configured state.

#### 9.4.12 Set SEL

This request sets both the U1 and U2 System Exit Latency and the U1 or U2 exit latency for all the links between a device and a root port on the host.

[tbl-172.md](tbl-172.md)

The latency values are sent to the device in the data stage of the control transfer in the following format:

[tbl-173.md](tbl-173.md)

If wIndex or wValue is not set to zero or wLength is not six, then the behavior of the device is not specified.

Default state: Device behavior when this request is received while the device is in the Default state is not specified.

Address state: This is a valid request when the device is in the Address state.

Configured state: This is a valid request when the device is in the Configured state.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.