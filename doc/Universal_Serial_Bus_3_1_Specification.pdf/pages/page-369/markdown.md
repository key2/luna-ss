Protocol Layer

### 8.12.1.4.2.9 INMvData Device Terminate

This state is entered because the device has just sent the last DP that it has available for CStream, e.g., it has exhausted its CStream Function Data. In this state the device waits for an acknowledgement from the host for the last DP of the Move Data transfer.

ACK(CStream, NumP=0, No Rty) - If the device receives an ACK with NumP = 0 and Rty = 0, then it shall transition to the Idle state, exiting the DIMDSM. This is the normal host response (Terminating ACK) for acknowledging the successful reception of the last DP for CStream from the device.

ACK(CStream, NumP>0, PP=1, Rty) - If the device receives an ACK with Rty = 1, then it shall transition to the INMvData Device state and resend the appropriate DP. This is the host response if an error was detected on the DP from the device and the burst was not complete.

ACK(CStream, NumP=0, PP=1, Rty) - If the device receives an ACK with Rty = 1 and NumP = 0, then it shall transition to the INMvData Burst End state and wait for the host to initiate the next burst. This is the host response if an error was detected on the DP from the device but the burst was complete. The host shall continue the retry process in the next burst.

### 8.12.1.4.2.10 INMvData Burst End

This state is entered because the host has terminated a burst on a stream pipe. In this state the device waits for an ACK TP that signifies the start of another burst.

ACK(CStream, NumP>0, PP=1) - If the device receives an ACK with NumP > 0 and PP = 1, then it shall transition to the INMvData Device state. Note, if the Rty flag was set when the state was entered, then it shall be set upon exit.

ACK(Deferred) - If an ACK with the Deferred (DF) flag set is received, then the device shall transition to the Idle state, exiting the DIMDSM. This transition occurs when the link has entered to a U1 or U2 state while waiting for the host to restart a burst, and this transition becomes more likely as the transfer activity associated with other devices increases.

### 8.12.1.4.3 Device OUT Stream Protocol

This section defines the Enhanced SuperSpeed packet exchanges that transition the device side of the Stream Protocol from one state to another on an OUT bulk endpoint.

In the following text, a Device OUT Stream state transition is assumed to occur at the point the device sends the first bit of the first symbol of a state machine related message to the host, or at the point the device first decodes a state machine related message from the host.

For an OUT pipe, Endpoint Data in the host is transmitted to Function Buffers in a device. Unless otherwise stated, a DP will contain Endpoint Data.

8-75