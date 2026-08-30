Universal Serial Bus 3.1 Specification, Revision 1.0

- Enough of the DPP has been received to ensure that upstream port transmitter under-run will not occur during the transmission of this packet.

For example, if there are only buffered Bulk DPs from other downstream ports and an Isochronous DP is being received on one downstream port, the Upstream Controller shall select the Isochronous DP as the next packet to transmit on the upstream port; as long as the remaining time to receive the Isochronous DP is less than the time required to transmit the Bulk DP and there is a sufficient amount of the Isochronous DPP already received.

### 10.8.6.4.2 Upstream Weighted Round Robin Arbitration

When the Upstream Controller needs to select the next Control/Bulk DP to transmit on the upstream port, the Upstream Controller uses the following selectPacket() algorithm to determine the next DP.

In the selectPacket() algorithm pseudo code, once a packet is selected, the algorithm is complete and any remaining steps in the algorithm are ignored for the selection of the current packet to transmit upstream.

Across invocations of the selectPacket algorithm, retain the value of i and curr_weight. Initial values of i=-1 and curr_weight=0.

The i$^{th}$ downstream facing port is DFPi. The candidate packet for the i$^{th}$ DFP is CPi.
selectPacket() algorithm:

1) If there are no buffered packets, set i=-1 and curr_weight=0 and don't select a packet.
Note: The upstream port will await the arrival of a packet on some DFPi.
2) For each DFPi, identify a candidate packet CPi for the DFPi:
   a. if there is a Control or Bulk DP buffered, set CPi to be the first one that had been buffered.
3) If there is only one DFPi with packets buffered for upstream transmission:
   a. Set i = port index
   b. Set cw = CPi.AW
   c. Select CPi
   d. exit
4) While true
   a. i = (i + 1) mod num_ports
   b. if (i == 0) then
      i. compute the Greatest Common Divisor (GCD) of all the buffered CPi.AW
      ii. curr_weight = curr_weight - GCD
      iii. if (curr_weight <= 0) then
         1. curr_weight = max of CPi.AWs for all buffered CPi
         2. if (curr_weight == 0) then there is no packet to select
   c. if (DFPi.AW >= curr_weight) then
      i. select CPi
      ii. exit

10-42