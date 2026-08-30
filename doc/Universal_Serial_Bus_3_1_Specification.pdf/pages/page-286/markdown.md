Universal Serial Bus 3.1 Specification

- For SuperSpeed USB, all header packets in the Tx Header Buffers and the Rx Header Buffers shall be handled based on the requirements specified in Section 7.2.4.
- For SuperSpeedPlus USB, all header packets and data packet headers in the Type 1/Type 2 Tx Header Buffers and the Type 1/Type 2 Rx Buffers shall be handled based on the requirements specified in Section 7.2.4.

### 7.5.10.3 Recovery.Active

Recovery.Active is a substate to train the Enhanced SuperSpeed link by transmitting the TS1 ordered sets.

#### 7.5.10.3.1 Recovery.Active Requirements

- A 12-ms timer (tRecoveryActiveTimeout) shall be started upon entry to this substate.
- The port shall transmit the TS1 ordered sets upon entry to this substate.
- The port shall train its receiver with TS1 or TS2 ordered sets.

Note: Depending on the link condition and different receiver implementations, one port's receiver may train faster than the other. When this occurs, the port whose receiver trains first will enter Recovery.Configuration and start transmitting TS2 ordered sets while the port whose receiver is not yet trained is still in Recovery.Active using the TS2 ordered sets to train its receiver.

- The port in SuperSpeedPlus operation shall insert a SYNC ordered set every 32 TS1 ordered sets.
- The port in SuperSpeedPlus operation shall perform block alignment and scrambler synchronization as defined in Sections 6.3.2.3 and 6.4.1.2.4 of Chapter 6.

#### 7.5.10.3.2 Exit from Recovery.Active

- The port in SuperSpeed operation shall transition to Recovery.Configuration after eight consecutive and identical TS1 or TS2 ordered sets are received.
- The port in SuperSpeedPlus operation shall transition to Recovery.Configuration upon receiving eight consecutive and identical TS1 or TS2 ordered sets, excluding symbols 14 and 15 of TS1 or TS2 ordered sets.

Note: SYNC OS and SKP OS in between TS1 OS and/or TS2 OS do not disqualify the consecutive detection of TS1 OS and TS2 OS. Symbols 14 and 15 are used for TS1 or TS2 ordered set identifier or DC balance adjustment.

- The port shall transition to eSS.Inactive when the following conditions are met:

1. Either the Ux_EXIT_TIMER or the 12-ms timer (tRecoveryActiveTimeout) times out.
2. For a downstream port, the transition to Recovery is not to attempt a Hot Reset.

- A downstream port shall transition to Rx.Detect when the following conditions are met:

1. Either the Ux_EXIT_TIMER or the 12-ms timer (tRecoveryActiveTimeout) times out.
2. The transition to Recovery is to attempt a Hot Reset.

- A downstream port shall transition to eSS.Disabled when directed.
- A downstream port shall transition to Rx.Detect when directed to issue Warm Reset.
- An upstream port shall transition to Rx.Detect when Warm Reset is detected.

### 7.5.10.4 Recovery.Configuration

Recovery.Configuration is a substate designed to allow the two link partners to achieve the Enhanced SuperSpeed handshake by exchanging the TS2 ordered sets.

7-74