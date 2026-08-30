Revision 1.1
June 2022

- 125 -

Universal Serial Bus 3.2
Specification

[tbl-80.md](tbl-80.md)

Link commands are defined for four usage cases. First, link commands are used to ensure the successful transfer of a packet. Second, link commands are used for link flow control. Third, link commands are used for link power management. And finally, special link commands are defined for a port to signal its presence in U0.

Successful header packet transactions between the two link partners require proper header packet acknowledgement. Rx Header Buffer Credit exchange facilitates link flow control. Header packet acknowledgement and Rx Header Buffer Credit exchange are realized using different link commands. LGOOD_n and LBAD are used to acknowledge whether a header packet has been received properly or not. LRTY is used to signal that a header packet is re-sent.

For SuperSpeed USB, LCRD_A, LCRD_B, LCRD_C, and LCRD_D are the link commands used to signal the availability of Rx Header Buffers in terms of Credit.

For SuperSpeedPlus USB, Type 1 and Type 2 traffic classes are defined. Type 1 traffic class, or namely Type 1 packet, includes the following packet types: periodic DPs, TPs, ITPs, and LMPs. Type 2 traffic class, or namely Type 2 packet, includes only the asynchronous DPs. In Gen 1x2 and Gen 2x1 operation, LCRD1_A, LCRD1_B, LCRD1_C, and LCRD1_D are link commands used for Type 1 traffic class to signal the availability of Rx Buffers for Type 1 header packets or data packets in terms of Credit. LCRD2_A, LCRD2_B, LCRD2_C, and LCRD2_D are link commands used for Type 2 traffic class to signal the availability of Rx Buffers for Type 2 packets in terms of Credit. In Gen 2x2 operation, three additional Rx Header Buffer Credits (LCRD1_E/LCRD1_F/LCRD1_G, LCRD2_E/LCRD2_F/LCRD2_G) for each traffic class are added to sustain the burst performance.

In the following sections, LCRD_x or LCRD1_x/LCRD2_x is used with x denoting either A, B, C, D, E, F, or G. See Table 7-5 for details. LGOOD_n uses an explicit numerical index called Header Sequence Number to represent the sequencing of a header packet. For SuperSpeed operation, the Header Sequence Number starts from 0 and is incremented by one based on modulo-8 addition with each header packet. For SuperSpeedPlus operation, the Header Sequence Number advancement is based on modulo-16 addition. The index corresponds to the received Header Sequence Number and is used for flow control and detection of lost or corrupted header packets.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.