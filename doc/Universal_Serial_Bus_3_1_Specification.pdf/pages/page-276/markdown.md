Universal Serial Bus 3.1 Specification

1. Eight consecutive and identical TS2 ordered sets are received.
2. Sixteen TS2 ordered sets are sent after receiving the first of the eight consecutive and identical TS2 ordered sets.

- The port in SuperSpeedPlus operation shall transition to Polling.Idle when the following two conditions are met:

1. Eight consecutive and identical TS2 ordered sets, excluding symbols 14 and 15, are received.
2. Sixteen TS2 ordered sets are sent after receiving the first of the eight consecutive and identical TS2 ordered sets, excluding symbols 14 and 15.

Note: SYNC OS and SKP OS in between TS2 OS do not disqualify the consecutive detection of TS2 OS.

- A downstream port in SuperSpeed operation shall transition to Rx.Detect upon the 12-ms timer timeout (tPollingConfigurationTimeout) and the following two conditions are met.

1. The conditions to transition to Polling.Idle are not met.
2. cPollingTimeout is less than two.

- A downstream port in SuperSpeed operation shall transition to eSS.Inactive upon the 12-ms timer timeout (tPollingConfigurationTimeout) and the following two conditions are met.

1. The conditions to transition to Polling.Idle are not met.
2. cPollingTimeout is two.

- An upstream port of a hub in SuperSpeed operation shall transition to Rx.Detect upon the 12-ms timer timeout (tPollingConfigurationTimeout) and the conditions to transition to Polling.Idle are not met.

- An upstream port of a peripheral device in SuperSpeed operation shall transition to eSS.Disabled upon the 12-ms timer timeout (tPollingConfigurationTimeout) and the conditions to transition to Polling.Idle are not met.

- A downstream port in SuperSpeedPlus operation shall transition to Polling.PortMatch to negotiate for alternative operation upon the 12-ms timer timeout (tPollingConfigurationTimeout) and the conditions to transition to Polling.Idle are not met.

- An upstream port of a hub in SuperSpeedPlus operation shall transition to Polling.PortMatch to negotiate for alternative operation upon the 12-ms timer timeout (tPollingConfigurationTimeout) and the conditions to transition to Polling.Idle are not met.

- An upstream port of a peripheral device in SuperSpeedPlus operation shall transition to Polling.PortMatch to negotiate for alternative operation upon the 12-ms timer timeout (tPollingConfigurationTimeout) and the conditions to transition to Polling. Idle are not met.

- A downstream port shall transition to eSS.Disabled when directed.

- A downstream port shall transition to Rx.Detect when directed to issue Warm Reset.

- An upstream port shall transition to Rx.Detect when Warm Reset is detected.

### 7.5.4.10 Polling.Idle

Polling.Idle is a substate where the port decodes the TS2 ordered set received in Polling.Configuration and determines the next state.

### 7.5.4.10.1 Polling.Idle Requirements

- The port shall decode the TS2 ordered set received during Polling.Configuration and proceeds to the next state.
- A downstream port shall reset its Link Error Count.

7-64