Protocol Layer

### 8.12.1.4.5.8 OUTMvData Host

In this state the host has received an ACK TP from a device and the device has more Function Buffer space available for CStream. The host responds with a DP containing Endpoint Data associated with the Stream. The pipe will also wait in this state between bursts from the host. Note, that the DP retry process may span bursts.

DP(CStream, PP=1) - If more Endpoint Data is available for the Stream and the host is continuing the current burst to the device, then the host shall generate a DP with PP = 1, and transition to the OUTMvData Device state. The DPP shall contain a CStream data payload. If the Rty flag was set in the last ACK from the device, then the host shall resend the appropriate DP until all retries are exhausted or a good DP is acknowledged by the device.

DP(CStream, PP=0) - If the Endpoint Data available for the Stream is exhausted by transmitting this DP, then the host shall generate a DP with PP = 0, and transition to the OUTMvData Host Terminate state. The DPP shall contain a CStream data payload. This transition informs the device the host has exhausted its Endpoint Data for the Stream.

### 8.12.1.4.5.9 OUTMvData Host Terminate

In this state the host has just exhausted the Endpoint Data that it has available for CStream and sent the last DP for the Stream. The host is waiting for an acknowledgement for the last DP of the Stream.

ACK(CStream, NumP=0) - If the host receives and ACK TP with NumP = 0 and Rty = 0, then the host shall transition to the Idle state, exiting the HOMDSM. This transition occurs when the device has successfully received the last DP, and both the host and the device have exhausted their respective Endpoint Data and Function Buffer space at the same time.

ACK(CStream, NumP>0, No Rty) - If the host receives an ACK TP with NumP > 0, PP = 0, and Rty = 0, then the host shall transition to the Idle state, exiting the HOMDSM. This transition occurs when the device has successfully received the last DP, and the host has exhausted its Endpoint Data for the CStream, but the device still has more Function Buffer space available.

ACK(CStream, NumP>0, Rty) - If the host receives an ACK TP with NumP > 0 and Rty = 1, then the host shall transition the OUTMvData Host state and resend the appropriate DP. This transition occurs when the last packet received by the device was bad, and a Retry is required. The host shall continue the OUTMvData Host Terminate to OUTMvData Host loop until all retries are exhausted or a good DP is acknowledged by the device.

NRDY(CStream) - If the host receives an NRDY, it shall transition to the Idle state, exiting the HOMDSM. This transition may occur during a Stream transfer due to unexpected internal device conditions where it wants to flow control CStream.

DPH(Deferred) - If a DPH with the Deferred (DF) flag set is received, then the host shall transition to the Idle state, exiting the HOMDSM. This packet is received when the link had transitioned to the U1 or U2 state before the last DP was sent by the host. There is no DPP associated with a deferred DPH.

8-93