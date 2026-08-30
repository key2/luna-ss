Revision 1.1
June 2022

- 201 -

Universal Serial Bus 3.2
Specification

**7.5.11.3.2 Exit from Loopback.Active**

- A downstream port shall transition to eSS.Disabled when directed.
- A downstream port shall transition to Rx.Detect when directed to issue Warm Reset.
- An upstream port shall transition to Rx.Detect when Warm Reset is detected.
- When directed, the loopback master shall transition to Loopback.Exit.
- The loopback slave shall transition to Loopback.Exit upon detection of Loopback LFPS exit handshake signal meeting Loopback LFPS exit signaling defined in Section 6.9.2.

**7.5.11.4 Loopback.Exit**

Loopback.Exit is a substate where a loopback master has completed the loopback test and starts the exit from Loopback.

**7.5.11.4.1 Loopback.Exit Requirements**

- A 2 ms timer (tLoopbackExitTimeout) shall be started upon entry to the substate.
- The LFPS transmitter and the LFPS receiver shall be enabled. In x2 operation, the LFPS transmitter shall be enabled on the Configuration Lane only.
- The port shall transmit and receive Loopback LFPS exit handshake signal defined in Section 6.9.2.

**7.5.11.4.2 Exit from Loopback.Exit**

- The port shall transition to Rx.Detect upon a successful Loopback LFPS exit handshake defined in Section 6.9.2.
- The port shall transition to eSS.Inactive upon the 2 ms timer timeout (tLoopbackExitTimeout) and the condition to transition to Rx.Detect is not met.
- A downstream port shall transition to eSS.Disabled when directed.
- A downstream port shall transition to Rx.Detect when directed to issue Warm Reset.
- An upstream port shall transition to Rx.Detect when Warm Reset is detected.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.