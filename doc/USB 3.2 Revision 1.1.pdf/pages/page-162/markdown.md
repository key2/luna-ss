Revision 1.1
June 2022

- 131 -

Universal Serial Bus 3.2
Specification

7. A port shall flush the header packets in its Tx Header Buffers or Type 1/Type 2 Tx Header Buffers upon receiving the Header Sequence Number Advertisement. A port shall do one of the following:
   a. If a port enters U0 from Polling or Hot Reset, it shall flush all the header packets in its Tx Header Buffers or Type 1/Type 2 Tx Header Buffers.
   b. If a port enters U0 from Recovery, it shall flush all the header packets in its Tx Header Buffers or Type 1/Type 2 Tx Header Buffers that have been sent before Recovery except for those with the Header Sequence Number greater than (modulo 8 in SuperSpeed operation, and modulo-16 in SuperSpeedPlus operation) the Header Sequence Number received in Header Sequence Number Advertisement.

Note: If for example in SuperSpeed operation, the Header Sequence Number Advertisement of LGOOD_1 is received, a port shall flush the header packets in its Tx Header Buffers or Type 1/Type 2 Tx Header Buffers with Header Sequence Numbers of 1, 0, 7, 6.

• For SuperSpeed USB, the Rx Header Buffer Credit Advertisement refers to Remote Rx Header Buffer Credit Count Initialization by exchanging the number of available Local Rx Header Buffer Credits between the two ports. The main purpose of this advertisement is for a port to align its Remote Rx Header Buffer Credit Count with its link partner upon entry to U0. The following rules shall be applied during the Rx Header Buffer Credit Advertisement:
1. A port shall initiate the Rx Header Buffer Credit Advertisement after sending LGOOD_n during Header Sequence Number Advertisement.
2. A port shall initialize the following before sending the Rx Header Buffer Credit:
   a. A port shall initialize its Tx Header Buffer Credit index to A.
   b. A port shall initialize its Rx Header Buffer Credit index to A.
   c. A port shall initialize its Remote Rx Header Buffer Credit Count to zero.
   d. A port shall continue to process those header packets in its Rx Header Buffers that have been either acknowledged with LGOOD_n prior to entry to Recovery, or validated during Recovery, and then update the Local Rx Header Buffer Credit Count.
   e. A port shall set its Local Rx Header Buffer Credit Count defined in the following:
      1. If a port enters U0 from Polling or Hot Reset, its Local Rx Header Buffer Credit Count is 4.
      2. If a port enters U0 from Recovery, its Local Rx Header Buffer Credit Count is the number of Rx Header Buffers available for incoming header packets.
3. A port shall perform the Rx Header Buffer Credit Advertisement by transmitting LCRD_x to notify its link partner. A port shall transmit one of the following based on its Local Rx Header Buffer Credit Count:
   a. LCRD_A if the Local Rx Header Buffer Credit Count is one.
   b. LCRD_A and LCRD_B if the Local Rx Header Buffer Credit Count is two.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.