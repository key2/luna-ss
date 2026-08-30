Revision 1.1
June 2022

- 185 -

Universal Serial Bus 3.2
Specification

- The port in Gen 2 operation may ignore SDS ordered set if corrupted and continue to process the following data block. The port may optionally choose to recover SDS ordered set if error is detected.
- In x2 operation, the lane-to-lane de-skew shall be completed upon receiving SDS on each negotiated lane.
- The port in Gen 2 operation shall disable the scrambling upon completion of SDS ordered set transmission if directed, or if the Disabling Scrambling bit is asserted in the TS2 ordered set received in Polling.Configuration.
- The port that fails to achieve a successful training with its link partner shall reconfigure itself for the next capability it supports.

Note: An example of this is, when a port in Gen 1x2 operation fails to reach successful handshake with its link partner, it shall re-configure itself for Gen 1x1 operation. Refer to Section 7.5.4.5 for mechanism of PHY capability fallback.

- A 2 ms timer (tPollingIdleTimeout) shall be started upon entry to this state. In x2 operation, the timer shall continue until each lane has met the transition conditions to the next state.
- The port shall be able to receive the Header Sequence Number Advertisement from its link partner.

Note: The exit time difference between the two ports will result in one port entering U0 first and starting the Header Sequence Number Advertisement while the other port is still in Polling.Idle.

#### 7.5.4.10.2 Exit from Polling.Idle

- The port shall transition to Loopback when directed as a loopback master and the port is capable of being a loopback master. Refer to Section 7.5.11 for details.
- The port shall transition to Loopback as a loopback slave if the Loopback bit is asserted in the TS2 ordered set received in Polling.Configuration. Refer to Section 7.5.4.9 for details.
- A downstream port shall transition to Hot Reset when directed.
- An upstream port shall transition to Hot Reset when the Reset bit is asserted in the TS2 ordered set received in Polling.Configuration.
- The port shall transition to U0 when the following two conditions are met on each negotiated lane:
  1. Eight consecutive Idle Symbols are received.
  2. Sixteen Idle Symbols are sent after receiving one Idle Symbol.
- A downstream port in SuperSpeed operation shall transition to eSS.Disabled when directed.
- A downstream port in SuperSpeed operation shall transition to Rx.Detect upon the 2 ms timer timeout (tPollingIdleTimeout) and the following two conditions are met.
  1. The conditions to transition to U0 are not met.
  2. cPollingTimeout is less than two.
- A downstream port in SuperSpeed operation shall transition to eSS.Inactive upon the 2 ms timer timeout (tPollingIdleTimeout) and the following two conditions are met.
  1. The conditions to transition to U0 are not met.
  2. cPollingTimeout is two.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.