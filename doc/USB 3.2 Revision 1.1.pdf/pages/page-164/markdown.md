Revision 1.1
June 2022

- 133 -

Universal Serial Bus 3.2
Specification

c. LCRD1_A, LCRD1_B, and LCRD1_C/ LCRD2_A, LCRD2_B, and LCRD2_C if the Local Type 1/Type 2 Rx Buffer Credit Count is three.
d. LCRD1_A, LCRD1_B, LCRD1_C and LCRD1_D/ LCRD2_A, LCRD2_B, LCRD2_C and LCRD2_D if the Local Type 1/Type 2 Rx Buffer Credit Count is four.
e. LCRD1_A, LCRD1_B, LCRD1_C, LCRD1_D and LCRD1_E/ LCRD2_A, LCRD2_B, LCRD2_C, LCRD2_D and LCRD2_E if the Local Type 1/Type 2 Rx Buffer Credit Count is five. Note that Rx Buffer Credit Count of five or more applies to Gen 2x2 operation.
f. LCRD1_A, LCRD1_B, LCRD1_C, LCRD1_D, LCRD_E and LCRD1_F/ LCRD2_A, LCRD2_B, LCRD2_C, LCRD2_D, LCRD2_E and LCRD2_F if the Local Type 1/Type 2 Rx Buffer Credit Count is six.
g. LCRD1_A, LCRD1_B, LCRD1_C, LCRD1_D, LCRD_E, LCRD1_F and LCRD1_G/ LCRD2_A, LCRD2_B, LCRD2_C, LCRD2_D, LCRD2_E, LCRD2_F and LCRD2_G if the Local Type 1/Type 2 Rx Buffer Credit Count is seven.
4. A port receiving LCRD1_x/LCRD2_x from its link partner shall increment its respective Remote Type 1/Type 2 Rx Buffer Credit Count by one each time a LCRD1_x/LCRD2_x is received up to four or seven.
5. A port shall not transmit any Type 1 or Type 2 packet if the respective Remote Type 1 or Type 2 Rx Buffer Credit Count is zero.
6. A port shall not request for a low power link state entry before receiving and sending LCRD1_x and LCRD2_x during the Type 1 and Type 2 Rx Buffer Credit Advertisements.
Note: The rules of Low Power Link State Initiation (refer to Section 7.2.4.2) still apply.
• The following rules shall be applied additionally when a port enters U0 from Recovery:
1. A port sending LBAD before Recovery shall not expect to receive LRTY before a retried header packet from its link partner upon entry to U0.
2. A port receiving LBAD before Recovery shall not send LRTY before a retried header packet to its link partner upon entry to U0.
Note: There exists a situation where an LBAD was sent by a port before Recovery and it may or may not be received properly by its link partner. Under this situation, the rules of LBAD/LRTY do not apply. Refer to Sections 7.2.4.1.4 and 7.2.4.1.12 for details.
• Upon entry to Recovery and the next state is Hot Reset or Loopback, a port may optionally continue its processing of all the packets received properly.

#### 7.2.4.1.2 General Rules of LGOOD_n and LCRD_x/LCRD1_x/LCRD2_x Usage

• For SuperSpeed USB, the Rx Header Buffer Credit shall be transmitted in the alphabetical order of LCRD_A, LCRD_B, LCRD_C, LCRD_D, and back to LCRD_A. LCRD_x received out of alphabetical order is considered as missing of a link command, and transition to Recovery shall be initiated.
• For SuperSpeedPlus USB, the Type 1 Rx Buffer Credit shall be transmitted in the alphabetical order of LCRD1_A, LCRD1_B, LCRD1_C, LCRD1_D in Gen 1x2 or Gen 2x1 operation, and additionally LCRD1_E, LCRD1_F, LCRD1_G in Gen 2x2 operation and back to LCRD1_A. LCRD1_x received out of alphabetical order is considered as

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.