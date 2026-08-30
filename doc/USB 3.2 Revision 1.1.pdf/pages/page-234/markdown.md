Revision 1.1
June 2022

- 203 -

Universal Serial Bus 3.2
Specification

- The port Configuration information shall remain unchanged (refer to Section 8.4.6 for details).
- The port shall maintain its transmitter specifications defined in Table 6-18.
- The port shall maintain its low-impedance receiver termination (R$_{RX-DC}$) defined in Table 6-22 on each negotiated lane.

#### **7.5.12.3 Hot Reset.Active**

Hot Reset.Active is a substate where a port will perform the reset as defined in Section 7.4.2.

##### **7.5.12.3.1 Hot Reset.Active Requirements**

- Upon entry to this substate, the port shall first transmit at least 16 TS2 ordered sets continuously on each negotiated lane with the Reset bit asserted.

Note: Depending on the time delay between the two ports entering Hot Reset, when the downstream port is transmitting the first 16 TS2 ordered sets with the Reset bit asserted, it may still receive part of the TS2 ordered sets from the upstream port exiting from Polling.Configuration or Recovery.Configuration. The downstream port shall ignore those TS2 ordered sets. Also upon entry to this substate, both ports shall ignore the Disabling Scrambling bit in the link configuration field of the TS2 Ordered Set. This bit is only decoded in Polling.Idle or Recovery.Idle.

- A 12 ms timer (tHotResetActiveTimeout) shall be started upon entry to this substate.
- A downstream port shall continue to transmit TS2 ordered sets on each negotiated lane with the Reset bit asserted until the upstream port transitions from sending TS2 ordered sets with the Reset bit asserted to sending the TS2 ordered sets with the Reset bit de-asserted on each negotiated lane.
- An upstream port shall transmit TS2 ordered sets with the Reset bit asserted while performing the Hot Reset on each negotiated lane.
- An upstream port shall transmit TS2 ordered sets with the Reset bit de-asserted after completing the Hot Reset on each negotiated lane.
- The port shall perform Hot Reset described in Hot Reset requirement of this section.

##### **7.5.12.3.2 Exit from Hot Reset.Active**

- The port shall transition to Hot Reset.Exit when the following three conditions are met on each negotiated lane.
  1. At least 16 TS2 ordered sets with the Reset bit asserted are transmitted.
  2. Two consecutive TS2 ordered sets are received with the Reset bit de-asserted.
  3. Four consecutive TS2 ordered sets with the Reset bit de-asserted are sent after receiving one TS2 ordered set with the Reset bit de-asserted.
- The port shall transition to eSS.Inactive upon the 12 ms timer timeout (tHotResetActiveTimeout) and the conditions to transition to Hot Reset.Exit are not met.
- The port in SuperSpeedPlus operation may ignore SDS OS if corrupted.
- A downstream port shall transition to eSS.Disabled when directed.
- A downstream port shall transition to Rx.Detect when directed to issue Warm Reset.
- An upstream port shall transition to Rx.Detect when Warm Reset is detected.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.