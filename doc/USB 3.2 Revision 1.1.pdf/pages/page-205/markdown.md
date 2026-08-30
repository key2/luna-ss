Revision 1.1
June 2022

- 174 -

Universal Serial Bus 3.2
Specification

### 7.5.4.4 Polling.LFPSPlus

Polling.LFPSPlus is a substate where the port SuperSpeedPlus operation performs SCD2 handshake, for additional confirmation of the SuperSpeedPlus capability of its link partner.

#### 7.5.4.4.1 Polling.LFPSPlus Requirements

- The port in SuperSpeedPlus operation shall transmit SCD2 defined in Table 6-33. If SCD2 cannot be found in 64 consecutive Polling.LFPS received, it shall transmit Polling.LFPS with non-varying tRepeat instead of SCD2.

Note: This is an extreme case where a port in SuperSpeed operation transmits Polling.LFPS coinciding with SCD1 and remains in Polling.LFPS.

- The operation of the 360 ms timer (tPollingLFPSTimeout) shall continue without reset upon entry to this substate from Polling.LFPS.
- A port in SuperSpeedPlus operation shall be ready for SuperSpeed operation if it has detected that its link partner operates at SuperSpeed.
- A port in SuperSpeedPlus operation shall implement a 60 μs timer (tPollingSCDLFPSTimeout) to monitor the absence of LFPS signal after the completion of SuperSpeed Polling.LFPS handshake.

#### 7.5.4.4.2 Exit from Polling.LFPSPlus

- The port in SuperSpeedPlus operation shall transition to Polling.PortMatch if two SCD2 are transmitted after one SCD2 as defined in Section 6.9.4.2 is received.
- A port in SuperSpeedPlus operation shall transition to Polling.RxEQ and switch to SuperSpeed operation if one of the following two conditions is met:

1. No LFPS signal for more than tPollingSCDLFPSTimeout is observed.

Note: This condition implies the SuperSpeed link partner has entered Polling.RxEQ transmitting TSEQ ordered sets.

2. Twenty Polling.LFPS bursts with non-varying tRepeat are transmitted, after finding no SCD2 is detected.

Note: This condition guarantees that, in the case of a port in SuperSpeedPlus operation connecting to a port in SuperSpeed operation, a port in SuperSpeed operation will receive twenty consecutive Polling.LFPS to exit from this substate if it is unable to recognize Polling.LFPS with varying tRepeat in SCD1 and SCD2, and it happens to transmit Polling.LFPS matching SCD1.

- A downstream port shall transition to Rx.Detect upon the 360 ms timer timeout (tPollingLFPSTimeout) and cPollingTimeout is less than two.
- A downstream port shall transition to eSS.Inactive upon the 360 ms timer timeout (tPollingLFPSTimeout) and cPollingTimeout is two.
- An upstream port of a hub shall transition to Rx.Detect upon the 360 ms timeout (tPollingLFPSTimeout).
- A peripheral device shall transition to eSS.Disabled upon the 360 ms timeout (tPollingLFPSTimeout).
- A downstream port shall transition to eSS.Disabled when directed.
- A downstream port shall transition to Rx.Detect when directed to issue Warm Reset.
- An upstream port shall transition to Rx.Detect when Warm Reset is detected.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.