Revision 1.1
June 2022

- 411 -

Universal Serial Bus 3.2
Specification

- A simple round robin arbitration behavior to select the next Interrupt/Isochronous DP buffered from the hub downstream ports.

The next section describes when an incompletely buffered DP that is still being received can be a candidate. The section after that describes the upstream weighted round robin arbitration mechanism.

### 10.8.6.4.1 Partially Buffered DP Selection Candidate

A DP (call it RCV_DP) shall be considered as a possible candidate, after the DPH has been fully received and validated and all of the following conditions are true:

- Let ALT_P be the candidate packet that would have been selected from the current set of fully buffered packets (i.e. when not considering RCV_DP as a possible candidate). RCV_DP would be selected when compared to ALT_P.
- The time remaining to fully receive this DPP is less than the time it will take to transmit ALT_P.
- Enough of the DPP has been received to ensure that upstream port transmitter under-run will not occur during the transmission of this packet.

For example, if there are only buffered Bulk DPs from other downstream ports and an Isochronous DP is being received on one downstream port, the Upstream Controller shall select the Isochronous DP as the next packet to transmit on the upstream port; as long as the remaining time to receive the Isochronous DP is less than the time required to transmit the Bulk DP and there is a sufficient amount of the Isochronous DPP already received.

### 10.8.6.4.2 Upstream Weighted Round Robin Arbitration

When the Upstream Controller needs to select the next Control/Bulk DP to transmit on the upstream port, the Upstream Controller uses the following selectPacket() algorithm to determine the next DP.

In the selectPacket() algorithm pseudo code, once a packet is selected, the algorithm is complete and any remaining steps in the algorithm are ignored for the selection of the current packet to transmit upstream.

Across invocations of the selectPacket algorithm, retain the value of i and curr_weight. Initial values of i=-1 and curr_weight=0.

The i$^{th}$ downstream facing port is DFPI. The candidate packet for the i$^{th}$ DFP is CPi.

selectPacket() algorithm:

1) If there are no buffered packets, set i=-1 and curr_weight=0 and don't select a packet. Note: The upstream port will await the arrival of a packet on some DFPI.
2) For each DFPI, identify a candidate packet CPi for the DFPI:
  a. if there is a Control or Bulk DP buffered, set CPi to be the first one that had been buffered.
3) If there is only one DFPI with packets buffered for upstream transmission:
  a. Set i = port index
  b. Set cw = CPi.AW
  c. Select CPi
  d. exit

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.