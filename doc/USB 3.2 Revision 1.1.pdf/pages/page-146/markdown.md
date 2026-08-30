Revision 1.1
June 2022

- 115 -

Universal Serial Bus 3.2
Specification

### 7.2 Link Management and Flow Control

This section contains information regarding link data integrity, flow control, and link power management.

- The packet and packet framing section defines packet types, packet structures, and CRC requirements for each packet.
- The link command section defines special link command structures that control various functionalities at the link level.
- The logical idle defines a special symbol used in U0.
- The flow control defines a set of handshake rules for packet transactions.

### 7.2.1 Packets and Packet Framing

The Enhanced SuperSpeed USB uses packets to transfer information. Detailed packet formats for Link Management Packets (LMP), Transaction Packets (TP), Isochronous Timestamp Packets (ITP), and Data Packets (DP) are defined in Section 8.2.

#### 7.2.1.1 Header Packet Structure

In Gen 1 operation, all header packets are 20 symbols long, as is formatted in Figure 7-3. This includes LMPs, TPs, ITPs, and DPHs. A header packet consists of three parts, a header packet framing, a packet header, and a Link Control Word.

In Gen 2 operation, all header packets except for non-deferred DPH are the same as Gen 1 operation. The non-deferred Gen 2 DPH is a header packet with its own framing ordered set, and contains a length field replica immediately after the Link Control word. The purpose of this special construction is to allow the non-deferred Gen 2 DPH to be processed differently from all other header packets and to achieve single bit error tolerance in its length field. The non-deferred Gen 2 DPH format is shown in Figure 7-4.

##### 7.2.1.1.1 Header Packet Framing

Header packet framing, HPSTART ordered set, is a four-symbol header packet starting frame ordered set. In Gen 1 operation, it is defined as three consecutive K symbols of SHP followed by a single K-symbol of EPF. In Gen 2 operation, HPSTART ordered set is the framing ordered set for all header packets except for non-deferred DPH, and is defined as three consecutive symbols of SHP followed by a single symbol of EPF. A non-deferred Gen 2 DPH uses DPHSTART ordered set, which is defined as three consecutive symbols of DPHP followed by a single symbol of EPF. Refer to Table 6-2 for framing symbol definition.

- All header packets except for non-deferred Gen 2 data packet header shall always begin with HPSTART ordered set.
- A non-deferred Gen 2 data packet header shall always begin with DPHSTART ordered set.
- A deferred Gen 2 data packet header shall always begin with HPSTART ordered set and it shall not contain the length field replica.

The construction of the header packet framing is to achieve one symbol error tolerance.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.