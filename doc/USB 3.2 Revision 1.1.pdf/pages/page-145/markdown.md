Revision 1.1
June 2022

- 114 -

Universal Serial Bus 3.2
Specification

### 7.1 Byte Ordering

Multiple byte fields in a packet or a link command are moved over to the bus in little-endian order, i.e., the least significant byte (LSB) first, and the most significant byte (MSB) last. Figure 7-2 shows an example of byte ordering.

Figure 7-2. Byte Ordering

![img-62.jpeg](img-62.jpeg)

#### 7.1.1 Gen 1 Line Code

Each byte of a packet or link command will be encoded in the physical layer using 8b/10b encoding. Refer to Section 6.3.1.3 regarding 8b/10b encoding and bit ordering.

Gen 1 operation may be based on either SuperSpeed USB or SuperSpeedPlus USB.

- The Gen 1x1 operation shall be based on SuperSpeed USB.
- The Gen 1x2 operation shall be based on SuperSpeedPlus USB.

#### 7.1.2 Gen 2 Line Code

To improve the effective throughput for of Gen 2 operation, 128b/132b line code is employed to replace 8b/10b line code used in Gen 1 operation. Two block types are defined based on 128b/132b line code. A control block is defined to transmit TSEQ, TS1, TS2, SYNC, SDS, and SKP ordered sets. A data block is defined to transmit packets, link commands, and Idle Symbols. Refer to Section 6.3 for 128b/132b block definition and bit ordering. Each symbol within a data block is scrambled by default, unless disabled otherwise by the Disabling Scrambling bit asserted in the TS2 ordered set received in Polling.Configuration or Recovery.Configuration. Refer to Sections 7.5.4.9 and 7.5.10.4 for details.

Gen 2 operation may be either Gen 2x1 or Gen 2x2. Gen 2 operation shall be based on SuperSpeedPlus USB.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.