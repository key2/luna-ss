Protocol Layer

U1 or U2 state while the pipe was waiting for its initial Endpoint Buffer assignment. e.g. after an ACK(Prime, NumP>0, PP=0) has been generated in the Disabled state.

ERDY() - If an ERDY is received, a race condition has occurred. During this condition, the device is in the Start Stream state and the host is in the Prime Pipe state. The host has entered the Prime Pipe state to inform the device that the Endpoint Buffers for one or more Streams have been updated, at the same time that the device has attempted to initiate a Stream transfer, and their respective messages have passed each other on the link. To resolve this condition, the host shall remain in the Prime Pipe state and wait for an NRDY(Prime) from the device.

### 8.12.1.4.4.3 Idle

In the Idle state, the pipe is waiting for a Stream selection (e.g., a transition to Start Stream or Move Data) or a notification from the host that Stream Endpoint Data has been added or modified for the pipe (i.e., transition to Prime Pipe). Note that upon the initial entry in to Idle (i.e., from Disabled), only the device may initiate a Stream selection.

ERDY(Stream n, NumP>0) -If an ERDY is received, the host shall transition to the Start Stream state. The device generates an ERDY to select a specific Stream (Stream n) that it expects the host to begin IN transactions on. A device may initiate this transition when it wishes to start a Stream transfer, regardless of whether it had previously flow controlled the pipe or not. Note that the value of the ERDY NumP field reflects the amount of Endpoint Data the device has available for Stream n. The value of the ERDY NumP is informative and the method that a device uses for Stream selection is outside the scope of this specification and is normally defined by the Device Class associated with the pipe. Upon transitioning to the Start Stream state the host sets LCStream to the value of Stream n.

ACK(Deferred) - If an ACK with the Deferred (DF) flag set is received, then the host shall remain in the Idle state. This packet is received if the link has transitioned to a U1 or U2 state when the host rejects a Start Stream request from the device (i.e., due to an ACK( NoStream, NumP=0, PP=0)). This case only occurs if tERDYTimeout is exceeded.

Stream x EP Buffer Change - This transition occurs if the state of one or more Endpoint Buffers has changed in the host. The host evaluates (at the Joint “&”) the ID of the Stream that software presents to the host controller (Stream x) and transitions to the Prime Pipe or Move Data states. This is an optimization that allows the host to transition the Stream pipe directly to the Move Data state, rather than going through the Prime Pipe, Start Stream, Move Data sequence, and is referred to as a Host Initiated Move Data or HIMD. The specific algorithm used to make this decision is host specific.

&

ACK(Prime, NumP>0, PP=0) - If the transition to Prime Pipe is selected, then the host shall generate a ACK TP with the Stream ID = Prime, NumP > 0, and PP = 0, and transition to the Prime Pipe state. Note that the host asserts a non-zero NumP value so that the device may respond with an NRDY. If NumP = 0, the device would consider it a Terminating ACK and not respond. Typically the Prime Pipe transition will be selected when the Stream that has just had its host Endpoint Buffers modified is not the same Stream that the device has last selected, e.g., Stream x != LCStream.

ACK(Stream x, NumP>0) - If the transition to Move Data is selected, then the host shall generate a ACK TP with the Stream ID = Stream x and NumP > 0, and transition to the Move

8-83