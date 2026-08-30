Revision 1.1
June 2022

- 181 -

Universal Serial Bus 3.2
Specification

- The port in Gen 2 operation shall transition to Polling.Active after 524,288 TSEQ ordered sets defined in Table 6-8 are transmitted on each negotiated lane.
- A downstream port shall transition to eSS.Disabled when directed.
- A downstream port shall transition to Rx.Detect when directed to issue Warm Reset.
- An upstream port shall transition to Rx.Detect when Warm Reset is detected.

#### 7.5.4.8 Polling.Active

Polling.Active is a substate where the link's receiver training continues. TS1 OS are exchanged on each negotiated lane. In x2 operation, the port performs the link training on each lane independently, and advances to the next state when each negotiated lane has met the exit conditions.

##### 7.5.4.8.1 Polling.Active Requirements

- In x1 operation, a 12 ms timer (tPollingActiveTimeout) shall be started upon entry to this substate. In x2 operation, a 24 ms timer shall be used. Note that in x2 operation, the timer shall continue until each lane has met the exit conditions to Polling.Configuration.
- The port shall transmit identical TS1 ordered sets on each negotiated lane. Note that in Gen 2 operation Symbols 14 and 15 of the TS1 ordered set may be different for DC balance. Note also that in x2 operation, one lane may complete its TS1 OS exit handshake earlier than the other lane. Under this condition, the lane that has completed the TS1 OS exit handshake successfully shall continue to transmit TS1 OS until the port is ready to transition to the next state.
- The port in Gen 2 operation shall insert a SYNC ordered set every 32 TS1 ordered sets on each negotiated lane. Refer to Section 6.4.1.2 for details.
- The port in Gen 2 operation shall perform block alignment and scrambler synchronization as defined in Sections 6.3.2.3 and 6.4.1.2.4.
- Lane polarity detection and correction shall be completed.
- The port shall monitor the exit handshake on each negotiated lane.
- The port in x2 operation shall perform the lane-to-lane de-skew at its receiver.
- The port that fails to achieve a successful training with its link partner shall reconfigure itself for the next capability it supports.

Note: An example of this is, when a port in Gen 1x2 fails to reach successful handshake with its link partner, it shall re-configure itself for Gen 1x1 operation. Refer to Section 7.5.4.5 for mechanism of PHY capability fallback.

- The receiver shall be in training using TS1 or TS2 ordered sets.

Note: Depending on the link condition and different receiver implementations, one port's receiver training may be faster than the other. When this occurs, the port whose receiver training is completed earlier will enter Polling.Configuration and start transmitting TS2 ordered sets while the other port is still in Polling.Active using TS2 ordered sets to complete its receiver training.

##### 7.5.4.8.2 Exit from Polling.Active

- The port in Gen 1 operation shall transition to Polling.Configuration upon receiving eight consecutive and identical TS1 or TS2 ordered sets on each negotiated lane.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.