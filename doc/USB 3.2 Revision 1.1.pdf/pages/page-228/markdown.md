Revision 1.1
June 2022

- 197 -

Universal Serial Bus 3.2
Specification

1. Either the Ux_EXIT_TIMER or the 6 ms timer (tRecoveryConfigurationTimeout) times out.
2. The transition to Recovery is to attempt a Hot Reset.

- A downstream port shall transition to eSS.Disabled when directed.
- A downstream port shall transition to Rx.Detect when directed to issue Warm Reset.
- An upstream port shall transition to Rx.Detect when Warm Reset is detected.

### 7.5.10.5 Recovery.Idle

Recovery.Idle is a substate where a port decodes the link configuration field defined in the TS2 ordered set received during Recovery.Configuration and determines the next state.

#### 7.5.10.5.1 Recovery.Idle Requirements

- A 2 ms timer (tRecoveryIdleTimeout) shall be started upon entry to this substate. Note that in x2 operation, the timer shall continue until each lane has met the exit conditions to the next designated link state.
- The port in Gen 1 operation shall transmit Idle Symbols if the next state is U0. The port may transmit Idle Symbols if the next state is Loopback or Hot Reset.
- The port shall decode the link configuration field defined in the TS2 ordered sets received during Recovery.Configuration and proceed to the next state.
- The port in Gen 1 operation shall enable the scrambling by default if the Disabling Scrambling bit is not asserted in the TS2 ordered set received in Recovery.Configuration.
- The port in Gen 1 operation shall disable the scrambling if directed, or if the Disabling Scrambling bit is asserted in the TS2 ordered set received in Recovery.Configuration.
- The port in Gen 2 operation shall transmit a single SDS ordered set on each negotiated lane before the start of the data blocks with Idle Symbols if the next state is U0. The port may transmit SDS ordered set if the next state is Loopback or Hot Reset.

Note: Under situation where a SKP ordered set is also scheduled at the same time with SDS ordered set, SKP ordered set shall be transmitted first.

- In x2 operation, the lane-to-lane de-skew shall be completed upon receiving SDS on each negotiated lane.
- The port in Gen 2 operation shall disable the scrambling upon completion of SDS ordered set transmission if directed, or if the Disabling Scrambling bit is asserted in the TS2 ordered set received in Recovery.Configuration.
- The port in Gen 2 operation may ignore SDS ordered set if corrupted and continue to process the following data block. The port may optionally choose to recover SDS ordered set if error is detected.
- The port shall be able to receive the Header Sequence Number Advertisement from its link partner.

Note: The exit time difference between the two ports will result in one port entering U0 first and starting the Header Sequence Number Advertisement while the other port is still in Recovery.Idle.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.