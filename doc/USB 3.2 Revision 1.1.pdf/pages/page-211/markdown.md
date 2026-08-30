Revision 1.1
June 2022

- 180 -

Universal Serial Bus 3.2
Specification

- The port in x2 operation shall transition to Polling.RxEQ if both of the following conditions are met. Note that in x2 operation, the PHY Ready LBPM exchange is performed only on the Configuration Lane.
  o The PHY Ready LBPM handshake is achieved.
  o The de-assertion of bit-7 of the PHY Ready LBPM from the DFP is observed.
- A downstream port shall transition to Rx.Detect upon the 12 ms timer timeout (tPollingLBPMLFPSTimeout) and cPollingTimeout is less than two.
- A downstream port shall transition to eSS.Inactive upon the 12 ms timer timeout (tPollingLBPMLFPSTimeout) and cPollingTimeout is two.
- An upstream port of a hub shall transition to Rx.Detect upon the 12 ms timer timeout (tPollingLBPMLFPSTimeout) and the conditions to transition to Polling.RxEQ are not met.
- A peripheral device shall transition to eSS.Disabled upon the 12 ms timer timeout (tPollingLBPMLFPSTimeout) and the conditions to transition to Polling.RxEQ are not met.
- A downstream port shall transition to eSS.Disabled when directed.
- A downstream port shall transition to Rx.Detect when directed to issue Warm Reset.
- An upstream port shall transition to Rx.Detect when Warm Reset is detected.

### 7.5.4.7 Polling.RxEQ

Polling.RxEQ is a substate for receiver equalization training. A port is required to complete its receiver equalization training. For the port in x2 operation, the link training is performed on each negotiated lane simultaneously.

#### 7.5.4.7.1 Polling.RxEQ Requirements

- The detection and correction of the lane polarity inversion in Gen 1 operation shall be enabled, as is described in Section 6.4.2. In Gen 1x2 operation, the detection and correction of the lane polarity inversion shall be enabled on both lanes.
- The port shall transmit the corresponding TSEQ ordered sets defined in Table 6-3 for Gen 1 operation, or Table 6-9 for Gen 2 operation. For Gen 2 operation, refer to Section 6.4.1.2.1 for SYNC ordered set insertion while transmitting TSEQ ordered sets.
- The port shall complete receiver equalizer training upon exit from this substate.

Note: A situation may exist where the port entering Polling.RxEQ earlier is transmitting TSEQ ordered sets while its link partner is still sending Polling.LFPS to satisfy the exit conditions from Polling.LFPS or Polling.LFPSPlus to Polling.RxEQ. In this situation, if its link partner is in electrical idle, near-end cross talk may cause the port to train its Rx equalizer using its own TSEQ ordered sets. To avoid a receiver from training itself, a port may either ignore the beginning part (about 30 µs) of the TSEQ ordered sets, or continue the equalizer training until it completes the transmission of TSEQ ordered sets.

#### 7.5.4.7.2 Exit from Polling.RxEQ

- The port in Gen 1 operation shall transition to Polling.Active after 65,536 consecutive TSEQ ordered sets defined in Table 6-3 are transmitted on each negotiated lane.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.