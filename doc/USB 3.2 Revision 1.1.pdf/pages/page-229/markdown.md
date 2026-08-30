Revision 1.1
June 2022

- 198 -

Universal Serial Bus 3.2
Specification

**7.5.10.5.2 Exit from Recovery.Idle**

- The port shall transition to Loopback when directed as a loopback master and the port is capable of being a loopback master.
- The port shall transition to Loopback as a loopback slave if the Loopback bit is asserted in TS2 ordered sets.
- The port shall transition to U0 when the following two conditions are met on each negotiated lane:
  1. Eight consecutive Idle Symbols are received.
  2. Sixteen Idle Symbols are sent after receiving one Idle Symbol.
- The port shall transition to eSS.Inactive when one of the following timers times out and the conditions to transition to U0 are not met:
  1. Ux_EXIT_TIMER
  2. The 2 ms timer (tRecoveryIdleTimeout)
- A downstream port shall transition to Hot Reset when directed.
- A downstream port shall transition to eSS.Disabled when directed.
- A downstream port shall transition to Rx.Detect when directed to issue Warm Reset.
- An upstream port shall transition to Rx.Detect when Warm Reset is detected.
- An upstream port shall transition to Hot Reset if the Reset bit is asserted in TS2 ordered sets.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.