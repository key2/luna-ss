Link Layer

### 7.5.10.4.1 Recovery.Configuration Requirements

- The port shall transmit identical TS2 ordered sets upon entry to this substate and set the link configuration field in the TS2 ordered set based on the following:

1. When directed, a downstream port shall set Reset bit in the TS2 ordered set.

Note: An upstream port can only set the Reset bit in the TS2 ordered set when in Hot Reset. Active. Refer to Section 7.5.12.3 for details.

2. When directed, the port shall set Loopback bit in the TS2 ordered set.
3. When directed, the port shall set the Disabling Scrambling bit in the TS2 ordered set.

- A 6-ms timer (tRecoveryConfigurationTimeout) shall be started upon entry to this substate.
- The port in SuperSpeedPlus operation shall insert a SYNC ordered set every 32 TS2 ordered sets.
- The port in SuperSpeedPlus operation shall perform block alignment and scrambler synchronization as defined in Sections 6.3.2.3 and 6.4.1.2.1 of Chapter 6.

### 7.5.10.4.2 Exit from Recovery.Configuration

- The port in SuperSpeed operation shall transition to Recovery.Idle after the following two conditions are met:

1. Eight consecutive and identical TS2 ordered sets are received.
2. Sixteen TS2 ordered sets are sent after receiving the first of the eight consecutive and identical TS2 ordered sets.

- The port in SuperSpeedPlus operation shall transition to Recovery.Idle when the following two conditions are met:

1. Eight consecutive and identical TS2 ordered sets, excluding symbols 14 and 15, are received.
2. Sixteen TS2 ordered sets are sent after receiving the first of the eight consecutive and identical TS2 ordered sets, excluding symbols 14 and 15.

- The port shall transition to eSS.Inactive when the following conditions are met:

1. Either the Ux_EXIT_TIMER or the 6-ms timer (tRecoveryConfigurationTimeout) times out.
2. For a downstream port, the transition to Recovery is not to attempt a Hot Reset.

- A downstream port shall transition to Rx.Detect when the following conditions are met:

1. Either the Ux_EXIT_TIMER or the 6-ms timer (tRecoveryConfigurationTimeout) times out.
2. The transition to Recovery is to attempt a Hot Reset.

- A downstream port shall transition to eSS.Disabled when directed.
- A downstream port shall transition to Rx.Detect when directed to issue Warm Reset.
- An upstream port shall transition to Rx.Detect when Warm Reset is detected.

### 7.5.10.5 Recovery.Idle

Recovery.Idle is a substate where a port decodes the link configuration field defined in the TS2 ordered set received during Recovery.Configuration and determines the next state.

### 7.5.10.5.1 Recovery.Idle Requirements

- A 2-ms timer (tRecoveryIdleTimeout) shall be started upon entry to this substate.
- The port in SuperSpeed operation shall transmit Idle Symbols if the next state is U0. The port may transmit Idle Symbols if the next state is Loopback or HotReset.

7-75