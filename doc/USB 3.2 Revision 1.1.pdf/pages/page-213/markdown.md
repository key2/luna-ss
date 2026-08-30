Revision 1.1
June 2022

- 182 -

Universal Serial Bus 3.2
Specification

- The port in Gen 2 operation shall transition to Polling.Configuration upon receiving eight consecutive and identical TS1 or TS2 ordered sets on each negotiated lane, excluding symbols 14 and 15 of TS1 or TS2 ordered sets.
  Note: SYNC OS and SKP OS in between TS1 OS and/or TS2 OS do not disqualify the consecutive detection of TS1 OS and TS2 OS. Symbols 14 and 15 are used for TS1 or TS2 ordered set identifier or DC balance adjustment.
- A downstream port in SuperSpeed operation shall transition to Rx.Detect upon the 12 ms timer timeout (tPollingActiveTimeout) and the following two conditions are met.
  1. The conditions to transition to Polling.Configuration are not met.
  2. cPollingTimeout is less than two.
- A downstream port in SuperSpeed operation shall transition to eSS.Inactive upon the 12 ms timer timeout (tPollingActiveTimeout) and the following two conditions are met.
  1. The conditions to transition to Polling.Configuration are not met.
  2. cPollingTimeout is two.
- An upstream port of a hub in SuperSpeed operation shall transition to Rx.Detect upon the 12 ms timer timeout (tPollingActiveTimeout) and the conditions to transition to Polling.Configuration are not met.
- An upstream port of a peripheral device in SuperSpeed operation shall transition to eSS.Disabled upon the 12 ms timer timeout (tPollingActiveTimeout) and the conditions to transition to Polling.Configuration are not met.
- A downstream port in SuperSpeedPlus operation shall transition to Polling.PortMatch to negotiate for alternative operation upon the 12 ms timer timeout (tPollingActiveTimeout) and the conditions to transition to Polling.Configuration are not met.
- An upstream port of a hub in SuperSpeedPlus operation shall transition to Polling.PortMatch to negotiate for alternative operation upon the 12 ms timer timeout (tPollingActiveTimeout) and the conditions to transition to Polling.Configuration are not met.
- An upstream port of a peripheral device in SuperSpeedPlus operation shall transition to Polling.PortMatch to negotiate for alternative operation upon the 12 ms timer timeout (tPollingActiveTimeout) and the conditions to transition to Polling.Configuration are not met.
- A downstream port shall transition to eSS.Disabled when directed.
- A downstream port shall transition to Rx.Detect when directed to issue Warm Reset.
- An upstream port shall transition to Rx.Detect when Warm Reset is detected.

#### **7.5.4.9 Polling.Configuration**

Polling.Configuration is a substate where the two link partners complete the Enhanced SuperSpeed training.

##### **7.5.4.9.1 Polling.Configuration Requirements**

- The port shall transmit identical TS2 ordered sets on each negotiated lane upon entry to this substate and set the link configuration field in the TS2 ordered set based on the following. Note that in Gen 2 operation, Symbols 14 and 15 of the TS2 ordered set may be different for DC balance.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.