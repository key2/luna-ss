Revision 1.1
June 2022

- 231 -

Universal Serial Bus 3.2
Specification

Table 8-11. LDM LMP

[tbl-108.md](tbl-108.md)

### 8.5 Transaction Packet (TP)

Transaction Packets (TPs) traverse the direct path between the host and a device. TPs are used to control data flow and manage the end-to-end connection. The value in the **Type** field shall be set to *Transaction Packet*. The **Route String** field is used by hubs to route a packet that appears on its upstream port to the correct downstream port. The route string is set to zero for a TP sent by a device. When the host sends a TP, the **Device Address** field contains the address of the intended recipient. When a device sends a TP to the host then it sets the **Device Address** field to its own address. This field is used by the host to identify the source of the TP. The **SubType** field in a TP is used by the recipient to determine the format and usage of the TP.

Table 8-12. Transaction Packet Subtype Field

[tbl-109.md](tbl-109.md)

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.