Revision 1.1
June 2022

- 149 -

Universal Serial Bus 3.2
Specification

### 7.3.4 Header Packet Errors

Several types of header packet errors are detected. They are:

1. Missing of a header packet
2. Invalid header packet due to CRC errors
3. Mismatch of a Rx Header Sequence Number

Regardless, the Link Error Count is incremented for only one class of errors in the link layer, and those are errors which will cause the link to transition to Recovery. For errors that will not cause the link to enter Recovery, the Link Error Count shall remain unchanged.

#### 7.3.4.1 Packet Framing Error

A packet framing ordered set is constructed such that any single symbol corruption within the ordered set will not prevent its packet framing recognition.

Header packet framing ordered sets and DPP framing ordered sets are all constructed using four symbol ordered sets. A header packet contains only one packet framing ordered set at the beginning of the packet defined in Section 7.2.1. A DPP begins with start packet framing ordered set and ends with end packet framing ordered set as defined in Section 7.2.2.

- A valid HPSTART ordered set, or a valid DPHSTART ordered set, or a valid DPP framing ordered set shall be declared if the following two conditions are met:
  1. At least three of the four symbols in the four consecutive symbol periods are valid packet framing symbols.
  2. The four symbols are in the order defined in Table 7-9.

Note: If an HPSTART ordered set or a DPHSTART ordered set has two or more symbols corrupted, a header packet will not be detectable and, therefore, result in missing of a header packet. Similarly, if a DPP framing ordered set is corrupted in Gen 1 operation, it will result in missing of a data packet payload. In Gen 2 operation, a corruption of a DPP framing ordered set will result in the loss of data packet payload boundary.

- Missing of a header packet shall result in a port transitioning to Recovery depending on which one of the following conditions becomes true first:
  1. A port transmitting the header packet upon its PENDING_HP_TIMER timeout.
  2. A port receiving the header packet upon detection of a Rx Header Sequence Number error.
- Missing of a DPP framing ordered set in Gen 2 operation shall result in a port transitioning to Recovery.

**Table 7-9. Valid Packet Framing Symbol Order**
**(Sx is One of SHP, DPHP, SDP, END or EDB)**

[tbl-86.md](tbl-86.md)

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.