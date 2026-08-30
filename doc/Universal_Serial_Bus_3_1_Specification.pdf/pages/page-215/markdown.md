Link Layer

## 7.2 Link Management and Flow Control

This section contains information regarding link data integrity, flow control, and link power management.

- The packet and packet framing section defines packet types, packet structures, and CRC requirements for each packet.
- The link command section defines special link command structures that control various functionalities at the link level.
- The logical idle defines a special symbol used in U0.
- The flow control defines a set of handshake rules for packet transactions.

### 7.2.1 Packets and Packet Framing

The Enhanced SuperSpeed USB uses packets to transfer information. Detailed packet formats for Link Management Packets (LMP), Transaction Packets (TP), Isochronous Timestamp Packets (ITP), and Data Packets (DP) are defined in Section 8.2.

#### 7.2.1.1 Header Packet Structure

For SuperSpeed USB, all header packets are 20 symbols long, as is formatted in Figure 7-3. This includes LMPs, TPs, ITPs, and DPHs. A header packet consists of three parts, a header packet framing, a packet header, and a Link Control Word.

For SuperSpeedPlus USB, all header packets except for non-deferred DPH are the same as SuperSpeed USB. The non-deferred SuperSpeedPlus DPH is a header packet with its own framing ordered set, and contains a length field replica immediately after the Link Control word. The purpose of this special construction is to allow the non-deferred SuperSpeedPlus DPH to be processed differently from all other header packets and to achieve single bit error tolerance in its length field. The non-deferred SuperSpeedPlus DPH format is shown in Figure 7-4.

##### 7.2.1.1.1 Header Packet Framing

Header packet framing, HPSTART ordered set, is a four-symbol header packet starting frame ordered set. For SuperSpeed USB, it is defined as three consecutive K symbols of SHP followed by a single K-symbol of EPF. For SuperSpeedPlus USB, HPSTART ordered set is the framing ordered set for all header packets except for non-deferred DPH, and is defined as three consecutive symbols of SHP followed by a single symbol of EPF. A non-deferred SuperSpeedPlus DPH uses DPHSTART ordered set, which is defined as three consecutive symbols of DPHP followed by a single symbol of EPF. Refer to Table 6-1 for framing symbol definition.

- All header packets except for non-deferred SuperSpeedPlus data packet header shall always begin with HPSTART ordered set.
- A non-deferred SuperSpeedPlus data packet header shall always begin with DPHSTART ordered set.
- A deferred SuperSpeedPlus data packet header shall always begin with HPSTART ordered set and it shall contain the length field replica.

The construction of the header packet framing is to achieve one symbol error tolerance.

7-3