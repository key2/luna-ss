Revision 1.1
June 2022

- 245 -

Universal Serial Bus 3.2
Specification

Table 8-24. PING_RESPONSE TP Format (Differences with ACK TP)

[tbl-127.md](tbl-127.md)

### 8.6 Data Packet (DP)

This packet can be sent by either the host or a device. The host uses this packet to send data to a device. Devices use this packet to return data to the host in response to an ACK TP. All data packets are comprised of a Data Packet Header and a Data Packet Payload. Only the fields that are different from an ACK TP are described in this section.

Data packets traverse the direct path between the host and a device. Note that it is permissible to send a data packet with a zero length data block; however, it shall have a CRC-32.

Figure 8-30. Example Data Packet

![img-121.jpeg](img-121.jpeg)

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.