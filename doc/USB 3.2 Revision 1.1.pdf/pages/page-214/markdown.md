Revision 1.1
June 2022

- 183 -

Universal Serial Bus 3.2
Specification

1. When directed, a downstream port shall set Reset bit in the TS2 ordered set.
   Note: An upstream port can only set the Reset bit in the TS2 ordered set when in Hot Reset.Active. Refer to Section 7.5.12.3 for details.
2. When directed, the port shall set Loopback bit in the TS2 ordered set.
3. When directed, the port shall set the Disabling Scrambling bit in the TS2 ordered set.
- The port in Gen 2 operation shall insert a SYNC ordered set every 32 TS2 ordered sets on each negotiated lane. Refer to Section 6.4.1.2 for details.
- The port in Gen 2 operation shall maintain block alignment and scrambler synchronization as defined in Sections 6.3.2.3 and 6.4.1.2.4.
- The port shall monitor the exit handshake on each negotiated lane.
- The port that fails to achieve a successful training with its link partner shall reconfigure itself for the next capability it supports.

   Note: An example of this is, when a port in Gen 1x2 operation fails to reach successful handshake with its link partner, it shall re-configure itself for Gen 1x1 operation. Refer to Section 7.5.4.5 for mechanism of PHY capability fallback.
- In x1 operation, a 12 ms timer (tPollingConfigurationTimeout) shall be started upon entry to this substate. In x2 operation, a 24 ms timer shall be used. Note that in x2 operation, the timer shall continue until each lane has met the exit conditions to Polling.Idle.

#### 7.5.4.9.2 Exit from Polling.Configuration

- The port in Gen 1 operation shall transition to Polling.Idle when the following two conditions are met on each negotiated lane:
  1. Eight consecutive and identical TS2 ordered sets are received.
  2. Sixteen TS2 ordered sets are sent after receiving the first of the eight consecutive and identical TS2 ordered sets.
- The port in Gen 2 operation shall transition to Polling.Idle when the following two conditions are met on each negotiated lane:
  1. Eight consecutive and identical TS2 ordered sets, excluding symbols 14 and 15, are received.
  2. Sixteen TS2 ordered sets are sent after receiving the first of the eight consecutive and identical TS2 ordered sets, excluding symbols 14 and 15.

   Note: SYNC OS and SKP OS in between TS2 OS do not disqualify the consecutive detection of TS2 OS.
- A downstream port in SuperSpeed operation shall transition to Rx.Detect upon the 12 ms timer timeout (tPollingConfigurationTimeout) and the following two conditions are met.
  1. The conditions to transition to Polling.Idle are not met.
  2. cPollingTimeout is less than two.
- A downstream port in SuperSpeed operation shall transition to eSS.Inactive upon the 12 ms timer timeout (tPollingConfigurationTimeout) and the following two conditions are met.
  1. The conditions to transition to Polling.Idle are not met.
  2. cPollingTimeout is two.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.