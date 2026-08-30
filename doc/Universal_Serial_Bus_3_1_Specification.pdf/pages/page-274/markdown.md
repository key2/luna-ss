Universal Serial Bus 3.1 Specification

### 7.5.4.7.2 Exit from Polling.RxEQ

- The port in SuperSpeed operation shall transition to Polling.Active after 65,536 consecutive TSEQ ordered sets defined in Table 6-2 are transmitted.
- The port in SuperSpeedPlus operation shall transition to Polling.Active after 262,143 TSEQ ordered sets defined in Table 6-8 are transmitted. Refer to Section 6.4.1.2.1 for SYNC ordered set insertion while transmitting TSEQ ordered sets.
- A downstream port shall transition to eSS.Disabled when directed.
- A downstream port shall transition to Rx.Detect when directed to issue Warm Reset.
- An upstream port shall transition to Rx.Detect when Warm Reset is detected.

### 7.5.4.8 Polling.Active

Polling.Active is a substate that continues the link's Enhanced SuperSpeed training.

#### 7.5.4.8.1 Polling.Active Requirements

- A 12-ms timer (tPollingActiveTimeout) shall be started upon entry to this substate.
- The port shall transmit TS1 ordered sets.
- The port in SuperSpeedPlus operation shall insert a SYNC ordered set every 32 TS1 ordered sets.
- The port in SuperSpeedPlus operation shall perform block alignment and scrambler synchronization as defined in sections 6.3.2.3 and 6.4.1.2.4 of Chapter 6.
- Lane polarity detection and correction shall be completed.
- The port that fails to achieve a successful training with its link partner shall reconfigure itself for the next capability it supports.
- Note: An example of this is, when a SuperSpeedPlus port fails to reach successful handshake with its link partner, it shall re-configure itself for SuperSpeed operation.
- The receiver is in training using TS1 or TS2 ordered sets.
- Note: Depending on the link condition and different receiver implementations, one port's receiver may train faster than the other. When this occurs, the port whose receiver trains first will enter Polling.Configuration and start transmitting TS2 ordered sets while the port whose receiver is not yet trained is still in Polling.Active using TS2 ordered sets to train its receiver.

#### 7.5.4.8.2 Exit from Polling.Active

- The port in SuperSpeed operation shall transition to Polling.Configuration upon receiving eight consecutive and identical TS1 or TS2 ordered sets.
- The port in SuperSpeedPlus operation shall transition to Polling.Configuration upon receiving eight consecutive and identical TS1 or TS2 ordered sets, excluding symbols 14 and 15 of TS1 or TS2 ordered sets.
Note: SYNC OS and SKP OS in between TS1 OS and/or TS2 OS do not disqualify the consecutive detection of TS1 OS and TS2 OS. Symbols 14 and 15 are used for TS1 or TS2 ordered set identifier or DC balance adjustment.
- A downstream port in SuperSpeed operation shall transition to Rx.Detect upon the 12-ms timer timeout (tPollingActiveTimeout) and the following two conditions are met.
1. The conditions to transition to Polling.Configuration are not met.
2. cPollingTimeout is less than two.
- A downstream port in SuperSpeed operation shall transition to eSS.Inactive upon the 12-ms timer timeout (tPollingActiveTimeout) and the following two conditions are met.

7-62