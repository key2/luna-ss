Revision 1.1
June 2022

- 282 -

Universal Serial Bus 3.2
Specification

exiting the HIMDSM. This transition informs the device the host has exhausted its Endpoint Buffer space for the Stream.

### 8.12.1.4.4.8 INMvData Burst End

This state is entered because the host has terminated a burst on a stream pipe. The host will exit this state when it is ready to start another burst. If this state was entered while retrying (Rty =1), then the host shall continue the retry process within the constraints of the endpoint when exiting the state.

ACK(CStream, NumP>0, PP=1) – When ready to start another burst to the device on CStream, the host shall generate an ACK with NumP > 0 and PP = 1 and transition to the INMvData Device state. Note, if the Rty flag was set when the state was entered, then it shall be set upon exit.

### 8.12.1.4.4.9 INMvData Device Terminate

In this state the host has received the last DP from a device for this Move Data operation because the device has exhausted the Function Data it has available for CStream. The host responds with an acknowledgement after copying the received data to the Endpoint Buffer space associated with the Stream and exits the HIMDSM. If the DP received from the device is bad, then retries may be performed within the constraints of the endpoint type.

ACK(CStream, NumP=0, No Rty) – If the DP received from the device is good, then the host generates an ACK with NumP = 0 and Rty = 0, and transitions to the Idle state, exiting the HIMDSM.

ACK(CStream, NumP>0, PP=1, Rty) – If the DP received from the device is bad and the current burst is not complete, then the host shall generate an ACK with NumP > 0, PP = 1 and Rty = 1, and transition to the INMvData Device state. The host may continue the INMvData Device Terminate to INMvData Device loop until all retries are exhausted or a good packet is received.

ACK(CStream, NumP=0, PP=1, Rty) – If the DP received from the device is bad and the current burst is complete, then the host shall generate an ACK with NumP = 0, PP = 1 and Rty = 1, and transition to the INMvData Burst End state. The host shall continue the retry process in the next burst.

### 8.12.1.4.5 Host OUT Stream Protocol

This section defines the Enhanced SuperSpeed packet exchanges that transition the host side of the Stream Protocol from one state to another on an OUT bulk endpoint.

In the following text, a Host OUT Stream state transition is assumed to occur at the point the host sends the first bit of the first symbol of a state machine related message to the device, or at the point the host first decodes state machine related message from the device.

For an OUT pipe, Function Buffers in the device receive Endpoint Data from the host.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.