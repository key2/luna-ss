Protocol Layer

### 8.12.1.4.3.9 OUTMvData Host

In this state the host has just received an ACK TP from the device for a previous DP and has more Endpoint Data available for CStream. The host generates a DP in this state. The pipe will also wait in this state between bursts from the host.

DP(CStream, PP=1) - If the device receives a DP with PP = 1, then it shall transition to the OUTMvData Device state. The DPP shall contain a CStream data payload. This is the host response if it has more than one Max Packet Size of Endpoint Data available for CStream.

DP(CStream, PP=0) - If the device receives a DP with PP = 0, then it shall transition to the OUTMvData Host Terminate state. The DPP shall contain a CStream data payload. This is the host response if it has exhausted the Endpoint Data that it has available for CStream. The length of the DP will be less than or equal to one Max Packet Size.

DPH(Deferred) - If a DPH with the Deferred (DF) flag set is received, then the device shall transition to the Idle state, exiting the DOMDSM. This packet is received when the link has transitioned to a U1 or U2 state while waiting for the next DP from the host. There is no DPP associated with a deferred DPH.

### 8.12.1.4.3.10 OUTMvData Host Terminate

This state is entered because the host has just sent the last DP that it has available for CStream, e.g., it has exhausted its CStream Endpoint Data. In this state the device acknowledges the last DP from the host for the Move Data transfer.

ACK(CStream, NumP=0) - If the device has also exhausted its Function Buffer space, then it shall generate an ACK TP with NumP = 0 and transition to the Idle state, exiting the DOMDSM.

ACK(CStream, NumP>0) - If the device has not exhausted its Function Buffer space, then it shall generate an ACK TP with NumP > 0, and transition to the Idle state, exiting the DOMDSM. The device shall set CStream to Not Ready due to this transition.

ACK(CStream, NumP>0, Rty) - If an error was detected on the last DP by the device, then it shall generate an ACK TP with NumP > 0 and Rty = 1, so that the host will retry the last DP. The device shall then transition to the OUTMvData Host state.

NRDY(CStream) - The device may flow control on the last CStream transfer by sending an NRDY with its Stream ID set to CStream and transition to the Idle state, exiting the DOMDSM. The device may generate this transition due to unexpected internal conditions where it wants to flow control CStream.

### 8.12.1.4.4 Host IN Stream Protocol

This section defines the Enhanced SuperSpeed packet exchanges that transition the host side of the Stream Protocol from one state to another on an IN bulk endpoint.

In the following text, a Host IN Stream state transition is assumed to occur at the point the host sends the first bit of the first symbol of a state machine related message to the device, or at the point the host first decodes state machine related message from the device.

For an IN pipe, Endpoint Buffers in the host receive Function Data from a device.

8-81