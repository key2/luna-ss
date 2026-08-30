Revision 1.1
June 2022

- 195 -

Universal Serial Bus 3.2
Specification

### 7.5.10.3.1 Recovery.Active Requirements

- A 12 ms timer (tRecoveryActiveTimeout) shall be started upon entry to this substate. Note that in x2 operation, the timer shall continue until each negotiated lane has met the exit conditions to Recovery.Configuration.
- The port shall transmit identical TS1 ordered sets on each negotiated lane upon entry to this substate. Note that in Gen 2 operation, Symbols 14 and 15 of the TS1 ordered set may be different for DC balance. Note also that in x2 operation, one lane may complete its TS1 OS exit handshake earlier than the other lane. Under this condition, the lane that has completed the TS1 OS exit handshake successfully shall continue to transmit TS1 OS until the port is ready to transition to the next state.
- The port shall train its receiver on each negotiated lane with TS1 or TS2 ordered sets.

Note: Depending on the link condition and different receiver implementations, one port's receiver may train faster than the other. When this occurs, the port whose receiver trains first will enter Recovery.Configuration and start transmitting TS2 ordered sets while the port whose receiver is not yet trained is still in Recovery.Active using the TS2 ordered sets to train its receiver.

- The port shall monitor the exit handshake on each negotiated lane.
- The port in Gen 2 operation shall insert a SYNC ordered set every 32 TS1 ordered sets.
- The port in Gen 2 operation shall perform block alignment and scrambler synchronization as defined in Sections 6.3.2.3 and 6.4.1.2.4.

### 7.5.10.3.2 Exit from Recovery.Active

- The port in SuperSpeed operation shall transition to Recovery.Configuration after eight consecutive and identical TS1 or TS2 ordered sets are received on each negotiated lane.
- The port in Gen 2 operation shall transition to Recovery.Configuration upon receiving eight consecutive and identical TS1 or TS2 ordered sets on each negotiated lane, excluding symbols 14 and 15 of TS1 or TS2 ordered sets.

Note: SYNC OS and SKP OS in between TS1 OS and/or TS2 OS do not disqualify the consecutive detection of TS1 OS and TS2 OS. Symbols 14 and 15 are used for TS1 or TS2 ordered set identifier or DC balance adjustment.

- The port shall transition to eSS.Inactive when the following conditions are met:

1. Either the Ux_EXIT_TIMER or the 12 ms timer (tRecoveryActiveTimeout) times out.
2. For a downstream port, the transition to Recovery is not to attempt a Hot Reset.

- A downstream port shall transition to Rx.Detect when the following conditions are met:

1. Either the Ux_EXIT_TIMER or the 12 ms timer (tRecoveryActiveTimeout) times out.
2. The transition to Recovery is to attempt a Hot Reset.

- A downstream port shall transition to eSS.Disabled when directed.
- A downstream port shall transition to Rx.Detect when directed to issue Warm Reset.
- An upstream port shall transition to Rx.Detect when Warm Reset is detected.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.