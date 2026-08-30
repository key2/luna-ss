Link Layer

receiver equalization training. Any time for configuration will result in receiving fewer TSEQ ordered sets from its link partner.

- A port shall disable its transition path to Compliance Mode when it has successfully completed Polling.LFPS handshake or has entered Compliance Mode.
- A 360-ms timer (tPollingLFPSTimeout) shall be started upon entry to the substate.
- The operating condition of an eSS PHY shall be established when a port is ready to exit to Polling.RxEQ.
- An eSS receiver in SuperSpeed operation may optionally be enabled to receive TSEQ ordered sets for receiver equalizer training.

Note: The port first entering Polling.RxEQ will start transmitting TSEQ ordered sets while the other port is still in Polling.LFPS. Enabling a SuperSpeed receiver in Polling.LFPS will allow a port to start the receiver equalizer training while completing the requirement for Polling.LFPS exit handshake.

### 7.5.4.3.2 Exit from Polling.LFPS

- The port in SuperSpeed operation shall transition to Polling.RxEQ when the following three conditions are met:

1. At least 16 consecutive Polling.LFPS bursts meeting the Polling.LFPS specification defined in Section 6.9 are sent.
2. Two consecutive Polling.LFPS bursts are received.
3. Four consecutive Polling.LFPS bursts are sent after receiving one Polling.LFPS burst.

- The port in SuperSpeedPlus operation shall transition to Polling.LFPSPlus if two SCD1 are transmitted after one SCD1 or SCD2 as defined in Section 6.9.4.2 is received.
- The port in SuperSpeedPlus operation shall transition to Polling.RxEQ and switch to SuperSpeed operation if the following conditions are met:

1. At least two consecutive Polling.LFPS bursts are received.
2. Twenty Polling.LFPS bursts are transmitted, and no SCD1 is detected.

Note: This condition guarantees that, in the case of a port in SuperSpeedPlus operation connecting to a port in SuperSpeed operation, a port in SuperSpeed operation will receive twenty consecutive Polling.LFPS to exit from this substate if it is unable to recognize Polling.LFPS with varying tRepeat in SCD1.

3. No LFPS signal for more than tPollingSCDLFPSTimeout is observed.

Note: This condition implies the SuperSpeed link partner has entered Polling.RxEQ transmitting TSEQ ordered sets.

- An upstream port shall transition to Compliance Mode upon the 360-ms timer timeout (tPollingLFPSTimeout) and the following two conditions are met:

1. The port has never successfully completed Polling.LFPS after PowerOn Reset.
2. The condition to transition to Polling.RxEQ or Polling.LFPSPlus is not met.

Note: If the very first attempt in Polling.LFPS handshake fails after PowerOn Reset, it implies that a passive test load may be present and compliance test should be initiated. If the very first attempt in Polling.LFPS handshake succeeds after PowerOn Reset, it implies the presence of the Enhanced SuperSpeed ports on each side of the link and no compliance test is intended. Therefore, any subsequent handshake timeout in Polling.LFPS when the link is retrained is only an indication of link training failure, not a signal to enter Compliance Mode.

7-57