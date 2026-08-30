Revision 1.1
June 2022

- 412 -

Universal Serial Bus 3.2
Specification

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

### 10.8.7 SuperSpeedPlus Upstream Flowing Packet Modifications

When the upstream port of a SuperSpeedPlus hub is operating in SuperSpeedPlus mode and the hub Downstream Controller receives a valid IN/ACK TP that is routed to a downstream port (DFPi) that is operating in SuperSpeed mode, the Downstream Controller shall:

1) Save the transfer type (SAVE_TT) of the TP for that DFPi.

When the hub Downstream Controller receives a valid DPH packet from DFPi, the Downstream Controller shall:

1) If the transfer type for this DFPi has been saved and the DPH is not a deferred DPH, set the transfer type of the DP to the saved value (DFPi.SAVE_TT).
2) If the AW field value of the received DPH is zero and the transfer type is Control or Bulk, modify the AW field of the received DPH by setting the DPH.AW field to DFPi.AW
3) If the DPH was modified, recompute the CRC-16 for the DPH.

This packet modification shall be done when the packet is received.

When the hub Upstream Controller selects (as described in Section 10.8.6.4) a Control/Bulk packet (S_DP) to transmit on the upstream port and there are multiple downstream ports (DFPi) with buffered Control/Bulk DPs awaiting transmission, the Upstream Controller shall:

1) For each DFPi, determine a candidate buffered Control/Bulk DP (C_DPi) for that DFPi that would be selected for upstream transmission if there were no other DFPi's with buffered Control/Bulk DPs.
2) Compute the sum (SUM_AW) of the AWs of the C_DPi's.
3) If the SUM_AW is different than the current value of the S_DP DPH.AW, modify the AW field of the S_DP DPH by replacing the AW value with SUM_AW
4) If the DPH was modified, recompute the CRC-16 for the S_DP DPH.

This modification shall be done before the packet is routed to the upstream port for transmission.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.