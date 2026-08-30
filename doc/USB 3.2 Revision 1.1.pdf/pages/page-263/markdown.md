Revision 1.1
June 2022

- 232 -

Universal Serial Bus 3.2
Specification

### 8.5.1 Acknowledgement (ACK) Transaction Packet

This TP is used for two purposes:

- For IN endpoints, this TP is sent by the host to request data from a device as well as to acknowledge the previously received data packet.
- For OUT endpoints, this TP is sent by a device to acknowledge receipt of the previous data packet sent by the host, as well as to inform the host of the number of data packet buffers it has available after receipt of this packet.

Figure 8-18. ACK Transaction Packet

![img-111.jpeg](img-111.jpeg)

Table 8-13. ACK TP Format

[tbl-110.md](tbl-110.md)

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.