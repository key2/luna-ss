Revision 1.1
June 2022

- 270 -

Universal Serial Bus 3.2
Specification

DP(CStream, EOB=1) - If the device's Endpoint Data for CStream is less than or equal to one Max Packet Size, then the device may send a DP to the host with EOB = 1 and transition to the INMvData Device Terminate state. The DPP shall contain CStream data.

NRDY(CStream) - The device may reject further CStream transfers by sending an NRDY with its Stream ID set to CStream and transition to the Idle state, exiting the DIMDSM. The device may generate this transition upon initial entry into the DIMDSM to reject a HIMD, or during a Stream transfer due to unexpected internal conditions where it wants to flow control CStream.

### 8.12.1.4.2.8 INMvData Host

In this state the device has just sent a DP to the host and has more Function Data available for CStream. The device waits in this state for an acknowledgement from the host for the last DP that it sent.

ACK(CStream, NumP>0, PP=1) - If the device receives an ACK with NumP > 0 and PP = 1, then it shall transition to the INMvData Device state. This is the host response if the current burst is not complete and it has more Endpoint Buffer space available for a CStream DP from the device. Note that the Retry (Rty=1) flag may be set in this packet if the host detected an error in the last DP from the device. If Rty is set, then the device shall return the DP with the appropriate Sequence Number the next time it sends a DP. If a DP error is detected, the host may continue the current burst until all retries are exhausted or a good DP is received. If the host cannot continue the current burst, the host shall initiate another burst to this endpoint at the next available opportunity within the constraints of the transfer type.

ACK(CStream, NumP=0, PP=1) - If the device receives an ACK with NumP = 0 and PP = 1, then it shall transition to the INMvData Burst End state. This is the host response if it has more Endpoint Buffer space available for another CStream DP; however, it must terminate the current burst from the device. Note that during the INMvData Host to INMvData Device transitions, the device should see NumP decrement towards 0 as the burst reaches completion. Note that the Retry (Rty=1) flag may be set in this packet if the host detected an error in the last DP from the device.

ACK(CStream, NumP=0, PP=0) - If the device receives an ACK with NumP = 0, and PP = 0, then it shall transition to the Idle state, exiting the DIMDSM. This is the host response to a DP when it has accepted the last DP because it has exhausted its CStream Endpoint Buffer space. The device shall set CStream to Not Ready due to this transition. During the INMvData Host to INMvData Device transitions, the device should see NumP decrement towards 0 as the Endpoint Buffer is exhausted.

Note: Receiving an ACK with NumP > 0 and PP = 0 is an illegal combination in the INMvData Host state and the device should halt the EP if detected.

### 8.12.1.4.2.9 INMvData Device Terminate

This state is entered because the device has just sent the last DP that it has available for CStream, e.g., it has exhausted its CStream Function Data. In this state the device waits for an acknowledgement from the host for the last DP of the Move Data transfer.

ACK(CStream, NumP=0, No Rty) - If the device receives an ACK with NumP = 0 and Rty = 0, then it shall transition to the Idle state, exiting the DIMDSM. This is the normal host response (Terminating ACK) for acknowledging the successful reception of the last DP for CStream from the device.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.