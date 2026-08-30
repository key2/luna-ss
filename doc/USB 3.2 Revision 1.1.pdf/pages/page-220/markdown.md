Revision 1.1
June 2022

- 189 -

Universal Serial Bus 3.2
Specification

○ In Gen 1x1 operation, tDHPResponse shall be less than 2540 ns.
○ In Gen 2x1 operation, tDHPResponse shall be less than 1610 ns.
○ In Gen 1x2 operation, tDHPResponse shall be less than 2270 ns.
○ In Gen 2x2 operation, tDHPResponse shall be less than 1355 ns.

Note that tDHPResponse includes some worst case delay, tDPacket = 2140 ns in Gen 1x1 operation and tDPacket = 910 ns in Gen 2x1 operation, when additional packets are scheduled ahead of the corresponding LGOOD_n or LBAD. It is recommended that a design respond with LGOOD_n or LBAD within 400 ns in Gen 1x1 operation or 700 ns in Gen 2x1 operation when no packets delay the LGOOD_n or LBAD transmission. Refer to Figure E-5 of Section E.1.2.3 for details.

• A port shall acknowledge the received LGO_Ux with LAU or LXU based on the timing defined by tDHPResponse.

### 7.5.6.2 Exit from U0

• The port shall transition to U1 upon successful completion of LGO_U1 entry sequence. Refer to Section 7.2.4.2 for details.
• The port shall transition to U2 upon successful completion of LGO_U2 entry sequence. Refer to Section 7.2.4.2 for details.
• The port shall transition to U3 upon successful completion of LGO_U3 entry sequence. Refer to Section 7.2.4.2 for details.
• A downstream port shall transition to eSS.Inactive when it fails U3 entry on three consecutive attempts.
• The port shall transition to Recovery upon any errors stated in Section 7.3 that will cause a link to transition to Recovery.
• The port shall transition to Recovery upon detection of a TS1 ordered set on any negotiated lane.
• The port shall transition to Recovery when directed.
• The port shall transition to eSS.Inactive when PENDING_HP_TIMER times out for the fourth consecutive time.

Note: This implies the link has transitioned to Recovery for three consecutive times and each time the transition to Recovery is due to PENDING_HP_TIMER timeout.

• A downstream port shall transition to eSS.Disabled when directed.
• A downstream port shall transition to eSS.Inactive when directed.
• An upstream port shall transition to eSS.Disabled when directed.

Note: After entry to U0 and the successful completion of training and link initialization, both ports are required to exchange port capabilities information using Port Capability LMPs within tPortConfiguration time as defined in Section 8.4.5. This includes the following scenarios:

1. Entry to U0 from polling directly;
2. Entry to U0 indirectly from Polling through Hot Reset;
3. Entry to U0 from Recovery and port configuration has not been successfully completed after exiting from Polling. In this case, both ports shall continue the port configuration process by completing the remaining LMP exchanges.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.