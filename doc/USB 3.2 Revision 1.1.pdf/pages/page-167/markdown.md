Revision 1.1
June 2022

- 136 -

Universal Serial Bus 3.2
Specification

- A port shall transition directly to Recovery if it fails to receive a header packet three consecutive times. A port shall not issue the third LBAD upon the third error.

#### 7.2.4.1.6 Receiving Data Packet Header in Gen 2 Operation

- Upon receiving a DPH, the following verifications shall be performed by a port:
  1. CRC-5
  2. CRC-16
  3. Matching between the Header Sequence Number in the received header packet and the Rx Header Sequence Number
  4. The availability of an Rx Buffer to store a header packet or a data packet.
- A DPH is defined as “received properly” when it has passed all four criteria described above. A port shall ignore the length field replica.
- When a DPH has been received properly, a port shall issue a single LGOOD_n with “n” corresponding to the Rx Header Sequence Number and increment the Rx Header Sequence Number by one (or roll over to 0 if the maximum Header Sequence Number is reached).
- A port shall consume one Type 1 or Type 2 Rx Buffer Credit until it has been processed and a Rx Buffer is available.
- When a DPH is not “received properly”, one of the following shall occur:
  1. If the DPH has one or more CRC-5 or CRC-16 errors, but the two length field replica are valid and identical, a port shall issue a single LBAD and track the associated DPP that immediately follows the DPH. A port shall ignore all the packets received subsequently until an LRTY has been received, or the link has entered Recovery. Refer to Section 7.2.4.1.1 for additional rules applicable when a port enters U0 from Recovery.
     Note: a valid length field is 0~1024. Refer to Section 7.2.1.2 for details.
  2. If any one of the following conditions occurs, a port shall transition to Recovery.
     a. The two length field replica is not identical.
     b. The Header Sequence Number in the received DPH does not match the Rx Header Sequence Number.
     c. The Rx Buffer does not have enough space to store the received DP
- After transmitting LBAD, a port shall continue to issue LCRD1_x or LCRD2_x if its corresponding Type 1 or Type 2 Rx Buffer Credit is made available.
- A port shall transition directly to Recovery if it fails to receive a data packet header three consecutive times. A port shall not issue the third LBAD upon the third error.

#### 7.2.4.1.7 SuperSpeed Rx Header Buffer Credit

Each port is required to have four Rx Header Buffer Credits in its receiver. This is referred to the Local Rx Header Buffer Credit. The number of the Local Rx Header Buffer Credits represents the number of header packets a port can accept and is managed by the Local Rx Header Buffer Credit Count.

- A port shall consume one Local Rx Header Buffer Credit if a header packet is “received properly”. The Local Rx Header Buffer Credit Count shall be decremented by one.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.