Universal Serial Bus 3.1 Specification, Revision 1.0

The DOMDSM allows either the device to terminate the Move Data operation because it has exhausted its Function Buffer space associated with a Stream or the host to terminate the Move Data operation because it has exhausted its Endpoint Data associated with a Stream.

PP=0 - Upon entry into the DOMDSM, if the host has only one packet of Endpoint Data available for the Stream then PP will equal 0 in the first DP received by the Device, and it shall transition to the OUTMvData Device Terminate state.

PP = 1 - Upon entry into the DOMDSM, if the host has more than one packet of Endpoint Data available for the Stream then PP will equal 1 in the first DP received by the Device, and it shall transition to the OUTMvData Device state.

The DOMDSM always exits to the Idle state. The Retry (Rty=1) flag shall never be set in a packet that causes a DOMDSM exit. A Stream pipe remains in the Move Data state during packet retries.

Note: The Stream ID value shall be CStream for all packets exchanged in the Move Data state. If a Stream ID value other than CStream is detected while in the DOMDSM the device should halt the endpoint.

Note: if CStream is not Active upon initially entering the Move Data state, the device may reject the Stream proposal with an NRDY or STALL the pipe, as defined by the associated Device Class.

# 8.12.1.4.3.8 OUTMvData Device

This state is initially entered from the Start Stream state or the Idle state. In this state the device acknowledges the last DP sent by the host or it may reject a HIMD from the host.

ACK(CStream, NumP>0) - If the device has more Function Buffer space available for CStream, then it shall send an ACK TP to the host with NumP > 0 and transition to the OUTMvData Host state. Note that the Retry (Rty) flag may be set in this packet if the device detected an error in the last DP from the host. The host shall continue the current burst until all retries are exhausted or a positive acknowledgement (Rty=0) is received. This transition shall indicate that the data payload of the previously received DP has been accepted by the endpoint for CStream.

ACK(CStream, NumP=0) - If the device has no more Endpoint Buffer space available for CStream, then it shall generate an ACK TP with NumP = 0, exit the DOMDSM and transition to the Idle state. This transition allows the device to exit from the Move Data state if its Endpoint Buffer space is exhausted. This transition shall indicate that the data payload of the previously received DP has been accepted by the endpoint for CStream.

NRDY(CStream) - The device may also terminate further CStream transfers by sending an NRDY with its Stream ID set to CStream, transitioning to the Idle state, exiting the DOMDSM. The device may generate this transition upon initial entry into the DOMDSM to reject a HIMD, or during a Stream transfer due to unexpected internal conditions where it wants to flow control CStream. This transition shall indicate that the data payload of the previously received DP has been dropped.

8-80