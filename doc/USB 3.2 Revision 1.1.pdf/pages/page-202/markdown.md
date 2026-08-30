Revision 1.1
June 2022

- 171 -

Universal Serial Bus 3.2
Specification

**7.5.4.3.2 Exit from Polling.LFPS**

- If the port begins with SuperSpeed operation, it shall transition to Polling.RxEQ when the following two conditions are met:
  1. At least 16 consecutive Polling.LFPS bursts meeting the Polling.LFPS specification defined in Section 6.9 are sent.
  2. The completion of SS Polling.LFPS handshake with two consecutive Polling.LFPS bursts received and four consecutive Polling.LFPS bursts sent after receiving one Polling.LFPS burst.
- The port in SuperSpeedPlus operation shall transition to Polling.LFPSPlus if two SCD1 are transmitted after one SCD1 or SCD2 as defined in Section 6.9.4.2 is received.
- If the port begins with SuperSpeedPlus operation, it shall transition to Polling.RxEQ and switch to SuperSpeed operation if the following conditions are met:
  1. No SCD1 or SCD2 is detected within the received Polling.LFPS bursts.
  2. At least four consecutive SCD1 are transmitted.
  3. The completion of SS Polling.LFPS with two consecutive Polling.LFPS bursts received and one SCD1 or four consecutive Polling.LFPS bursts transmitted after receiving one Polling.LFPS burst.
  4. Either one of the following conditions are met.
     i. No LFPS signal for more than tPollingSCDLFPSTimeout is observed.
       Note: This also includes, but is not limited to, a scenario where a SS link partner can recognize the Polling.LFPS bursts with varying tRepeat and has already met the exit conditions to Polling.RxEQ.
     ii. Before the tPollingSCDLFPSTimeout timer expiration, sixteen additional Polling.LFPS bursts with non-varying tRepeat are transmitted after the above three conditions are met.
       Note: This also includes, but is not limited to, a scenario where a SS link partner may not recognize the Polling.LFPS bursts with varying tRepeat.

Note: This condition implies the SuperSpeed link partner has entered Polling.RxEQ transmitting TSEQ ordered sets.

Figure 7-18 provides a number of example timing diagrams of a SSP port switching to SS operation.

- An upstream port shall transition to Compliance Mode upon the 360 ms timer timeout (tPollingLFPSTimeout) and the following two conditions are met:
  1. The port has never successfully completed Polling.LFPS after PowerOn Reset.
  2. The condition to transition to Polling.RxEQ or Polling.LFPSPlus is not met.

Note: If the very first attempt in Polling.LFPS handshake fails after PowerOn Reset, it implies that a passive test load may be present and compliance test should be initiated. If the very first attempt in Polling.LFPS handshake succeeds after PowerOn Reset, it implies the presence of the Enhanced SuperSpeed ports on each side of the link and no compliance test is intended. Therefore, any subsequent handshake timeout in Polling.LFPS when the link is retrained is only an indication of link training failure, not a signal to enter Compliance Mode.

- A downstream port shall transition to Compliance Mode upon the 360 ms timer timeout (tPollingLFPSTimeout) if the following three conditions are met:

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.