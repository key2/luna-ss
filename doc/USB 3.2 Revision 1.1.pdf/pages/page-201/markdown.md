Revision 1.1
June 2022

- 170 -

Universal Serial Bus 3.2
Specification

2. If the tPollingSCDLFPSTimeout timer has expired, it shall switch to SuperSpeed operation in preparation to transition to Polling.RxEQ when all other exit conditions are met.

Note: This may imply that its SuperSpeed link partner may enter Polling.LFPS first, can recognize the Polling.LFPS bursts with varying tRepeat in SCD1 or SCD2, and has met all of the exit conditions to Polling.RxEQ.

- A downstream port in SuperSpeedPlus operation shall transmit SCD1 defined in Table 6-33 if Compliance Mode is disabled. It shall perform in one of the following ways if no signature of SCD1 or SCD2 is detected within the received Polling.LFPS bursts.

1. If it has received sixteen or more consecutive Polling.LFPS bursts and the tPollingSCDLFPSTimeout timer has not expired, it shall switch to SuperSpeed operation and transmit Polling.LFPS with non-varying tRepeat after four SCD1 are transmitted.

Note: This may include, but is not limited to, a scenario that its SuperSpeed link partner may not recognize the Polling.LFPS bursts with varying tRepeat in SCD1.

2. If the tPollingSCDLFPSTimeout timer has expired, it shall switch to SuperSpeed operation in preparation to transition to Polling.RxEQ when all exit conditions are met.

Note: This may imply that its SuperSpeed link partner may enter Polling.LFPS first, can recognize the Polling.LFPS bursts with varying tRepeat in SCD1 or SCD2, and has met all of the exit conditions to Polling.RxEQ.

- A downstream port in SuperSpeedPlus operation may transmit SCD1 or SCD2 if Compliance Mode is enabled.
- A port in SuperSpeedPlus operation shall implement a 60 µs timer (tPollingSCDLFPSTimeout) to monitor the absence of LFPS signal after the completion of SuperSpeed Polling.LFPS handshake. During this period, the port shall continue the transmission of Polling.LFPS or SCD1 until its expiration.
- A port in SuperSpeedPlus operation shall be ready for SuperSpeed operation if it has detected that its link partner operates at SuperSpeed.

Note: There is no time allocated for a SuperSpeedPlus port to re-configure itself for SuperSpeed operation upon detection of its link partner operating at SuperSpeed. A SuperSpeedPlus port shall switch to SuperSpeed operation as quickly as possible for its receiver equalization training. Any time for configuration will result in receiving fewer TSEQ ordered sets from its link partner.

- A port shall disable its transition path to Compliance Mode when it has successfully completed Polling.LFPS handshake or has entered Compliance Mode.
- A 360 ms timer (tPollingLFPSTimeout) shall be started upon entry to the substate.
- The operating condition of an eSS PHY shall be established when a port is ready to exit to Polling.RxEQ.
- An eSS receiver in SuperSpeed operation may optionally be enabled to receive TSEQ ordered sets for receiver equalizer training.

Note: The port first entering Polling.RxEQ will start transmitting TSEQ ordered sets while the other port is still in Polling.LFPS. Enabling a SuperSpeed receiver in Polling.LFPS will allow a port to start the receiver equalizer training while completing the requirement for Polling.LFPS exit handshake.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.