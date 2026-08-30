Revision 1.1
June 2022

- 204 -

Universal Serial Bus 3.2
Specification

**7.5.12.4 Hot Reset.Exit**

Hot Reset.Exit is a substate where the port has completed Hot Reset and is ready to exit from Hot Reset.

**7.5.12.4.1 Hot Reset.Exit Requirements**

- The port in Gen 1 operation shall transmit idle symbols.
- The port in Gen 2 operation shall transmit a single SDS ordered set before the start of the data block with Idle Symbols.
- The port in Gen 2 operation may ignore SDS ordered set if corrupted and continue to process the following data block. The port may optionally choose to recover SDS ordered set if error is detected.
- A 2 ms timer (tHotResetExitTimeout) shall be started upon entry to this substate.
- The port shall be able to receive the Header Sequence Number Advertisement from its link partner.

Note: The exit time difference between the two ports will result in one port entering U0 first and starting the Header Sequence Number Advertisement while the other port is still in Hot Reset.Exit.

**7.5.12.4.2 Exit from Hot Reset.Exit**

- The port shall transition to U0 when the following two conditions are met on each negotiated lane:
  1. Eight consecutive Idle Symbols are received.
  2. Sixteen Idle Symbols are sent after receiving one Idle Symbol.
- The port shall transition to eSS.Inactive upon the 2 ms timer timeout (tHotResetExitTimeout) and the conditions to transition to U0 are not met.
- A downstream port shall transition to eSS.Disabled when directed.
- A downstream port shall transition to Rx.Detect when directed to issue Warm Reset.
- An upstream port shall transition to Rx.Detect when Warm Reset is detected.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.