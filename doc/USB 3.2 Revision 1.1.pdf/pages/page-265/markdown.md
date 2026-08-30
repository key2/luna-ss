Revision 1.1
June 2022

- 234 -

Universal Serial Bus 3.2
Specification

[tbl-112.md](tbl-112.md)

### 8.5.2 Not Ready (NRDY) Transaction Packet

This TP can only be sent by a device for a non-isochronous endpoint. An OUT endpoint sends this TP to the host if it has no packet buffer space available to accept the DP sent by the host. An IN endpoint sends this TP to the host if it cannot return a DP in response to an ACK TP sent by the host.

Only the fields that are different from an ACK TP are described in this section.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.