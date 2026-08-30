Revision 1.1
June 2022

- 276 -

Universal Serial Bus 3.2
Specification

### 8.12.1.4.3.8 OUTMvData Device

This state is initially entered from the Start Stream state or the Idle state. In this state the device acknowledges the last DP sent by the host or it may reject a HIMD from the host.

ACK(CStream, NumP>0) - If the device has more Function Buffer space available for CStream, then it shall send an ACK TP to the host with NumP > 0 and transition to the OUTMvData Host state. Note that the Retry (Rty) flag may be set in this packet if the device detected an error in the last DP from the host. The host shall continue the current burst until all retries are exhausted or a positive acknowledgement (Rty=0) is received. This transition shall indicate that the data payload of the previously received DP has been accepted by the endpoint for CStream.

ACK(CStream, NumP=0) - If the device has no more Endpoint Buffer space available for CStream, then it shall generate an ACK TP with NumP = 0, exit the DOMDSM and transition to the Idle state. This transition allows the device to exit from the Move Data state if its Endpoint Buffer space is exhausted. This transition shall indicate that the data payload of the previously received DP has been accepted by the endpoint for CStream.

NRDY(CStream) - The device may also terminate further CStream transfers by sending an NRDY with its Stream ID set to CStream, transitioning to the Idle state, exiting the DOMDSM. The device may generate this transition upon initial entry into the DOMDSM to reject a HIMD, or during a Stream transfer due to unexpected internal conditions where it wants to flow control CStream. This transition shall indicate that the data payload of the previously received DP has been dropped.

### 8.12.1.4.3.9 OUTMvData Host

In this state the host has just received an ACK TP from the device for a previous DP and has more Endpoint Data available for CStream. The host generates a DP in this state. The pipe will also wait in this state between bursts from the host.

DP(CStream, PP=1) - If the device receives a DP with PP = 1, then it shall transition to the OUTMvData Device state. The DPP shall contain a CStream data payload. This is the host response if it has more than one Max Packet Size of Endpoint Data available for CStream.

DP(CStream, PP=0) - If the device receives a DP with PP = 0, then it shall transition to the OUTMvData Host Terminate state. The DPP shall contain a CStream data payload. This is the host response if it has exhausted the Endpoint Data that it has available for CStream. The length of the DP will be less than or equal to one Max Packet Size.

DPH(Deferred) - If a DPH with the Deferred (DF) flag set is received, then the device shall transition to the Idle state, exiting the DOMDSM. This packet is received when the link has transitioned to a U1 or U2 state while waiting for the next DP from the host. There is no DPP associated with a deferred DPH.

### 8.12.1.4.3.10 OUTMvData Host Terminate

This state is entered because the host has just sent the last DP that it has available for CStream, e.g., it has exhausted its CStream Endpoint Data. In this state the device acknowledges the last DP from the host for the Move Data transfer.

ACK(CStream, NumP=0) - If the device has also exhausted its Function Buffer space, then it shall generate an ACK TP with NumP = 0 and transition to the Idle state, exiting the DOMDSM.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.