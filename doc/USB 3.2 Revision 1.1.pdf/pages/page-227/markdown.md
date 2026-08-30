Revision 1.1
June 2022

- 196 -

Universal Serial Bus 3.2
Specification

#### 7.5.10.4 Recovery.Configuration

Recovery.Configuration is a substate designed to allow the two link partners to achieve the Enhanced SuperSpeed handshake by exchanging the TS2 ordered sets.

##### 7.5.10.4.1 Recovery.Configuration Requirements

- The port shall transmit identical TS2 ordered sets on each negotiated lane upon entry to this substate and set the link configuration field in the TS2 ordered set based on the following. Note that in Gen 2 operation, Symbols 14 and 15 of the TS2 ordered set may be different for DC balance.
  1. When directed, a downstream port shall set Reset bit in the TS2 ordered set. Note: An upstream port can only set the Reset bit in the TS2 ordered set when in Hot Reset.Active. Refer to Section 7.5.12.3 for details.
  2. When directed, the port shall set Loopback bit in the TS2 ordered set.
  3. When directed, the port shall set the Disabling Scrambling bit in the TS2 ordered set.
- In x2 operation, if one lane has met the exit conditions to Recovery.Idle first and the other lane has not, it shall continue to transmit TS2 OS until the port is ready to transition to the next state.
- A 6 ms timer (tRecoveryConfigurationTimeout) shall be started upon entry to this substate. Note that in x2 operation, the timer shall continue until each lane has met the exit conditions to Recovery.Idle.
- The port in Gen 2 operation shall insert a SYNC ordered set every 32 TS2 ordered sets on each negotiated lane.
- The port in Gen 2 operation shall perform block alignment and scrambler synchronization on each negotiated lane as defined in Sections 6.3.2.3 and 6.4.1.2.1.

##### 7.5.10.4.2 Exit from Recovery.Configuration

- The port in Gen 1 operation shall transition to Recovery.Idle after the following two conditions are met on each negotiated lane:
  1. Eight consecutive and identical TS2 ordered sets are received.
  2. Sixteen TS2 ordered sets are sent after receiving the first of the eight consecutive and identical TS2 ordered sets.
- The port in Gen 2 operation shall transition to Recovery.Idle when the following two conditions are met on each negotiated lane:
  1. Eight consecutive and identical TS2 ordered sets, excluding symbols 14 and 15, are received.
  2. Sixteen TS2 ordered sets are sent after receiving the first of the eight consecutive and identical TS2 ordered sets, excluding symbols 14 and 15.
- The port shall transition to eSS.Inactive when the following conditions are met:
  1. Either the Ux_EXIT_TIMER or the 6 ms timer (tRecoveryConfigurationTimeout) times out.
  2. For a downstream port, the transition to Recovery is not to attempt a Hot Reset.
- A downstream port shall transition to Rx.Detect when the following conditions are met:

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.