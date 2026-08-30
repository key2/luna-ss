Universal Serial Bus 3.1 Specification, Revision 1.0

&

DP(Prime, PP=0) - If the transition to Prime Pipe is selected, then the host shall generate a DP with the Stream ID = Prime and PP = 0, and transition to the Prime Pipe state. The DPP shall contain a zero-length data payload. Typically, the Prime Pipe transition will be selected when the Stream that has just had its Endpoint Data modified is not the same Stream that the device has last selected, e.g., Stream x != LCStream.

DP(Stream x) - If the transition to Move Data is selected, then the host shall generate a DP with the Stream ID = Stream x, and transition to the Move Data state. Upon transitioning to the Move Data state the host sets CStream to the value of Stream x. The DPP shall contain the first data payload for CStream. Typically the Move Data transition will be selected when the Stream that has just had its Endpoint Data modified is the same Stream as the one that the device last selected, e.g., Stream x = LCStream. The value of PP shall depend on the amount of Endpoint data the host has available. If the host has more than Max Packet Size Endpoint Data available for the Stream, then PP = 1 else PP = 0. This transition may be optionally be disabled in some hosts, and some Device Classes may not process this transition (e.g., Mass Storage UASP).

### 8.12.1.4.5.4 Start Stream

In the Start Stream state, the device has sent an ERDY proposing to the host that it initiate an OUT transfer for Stream n and it is waiting for the host to accept or reject the Stream selection.

DP(Stream n) - If the host has accepted the device's proposal for starting Stream n, then it shall transmit a DP with a Stream ID equal to Stream n, and transition to the Move Data state. Upon transitioning to the Move Data state the host sets CStream to the value of Stream n. The DPP shall contain the first data payload for CStream. The host shall accept a Stream proposal from a device if there is Endpoint Data available for the Stream.

DP(NoStream, PP = 0) - If the host rejects the device's proposal for starting Stream n, then it shall transmit a DP with a Stream ID equal to NoStream, and transition to the Start Stream End state. The DPP shall contain a zero-length data payload. The host shall reject a Stream proposal from a device if there is no Endpoint Data available to send for the Stream.

### 8.12.1.4.5.5 Start Stream End

In the Start Stream End state, the host has rejected a proposed Stream ID from the device because there was no Endpoint Data available for Stream n. Note, this state is entered when the host transmits a DP(NoStream) from the Start Stream state. If an error is detected in the DP data by the device, the device shall issue ACK(NoStream, NumP>0, Rty) packet, retrying until a DP(NoStream) is successfully received. The host may retransmit the DP(NoStream) and shall remain in the Start Stream End state until the device successfully receives the DP(NoStream) and returns an NRDY(NoStream), or the retries for the pipe are exhausted and the host halts the pipe. This case is not illustrated in the Figure above.

NRDY(NoStream) - If an NRDY with the Stream ID equal to NoStream is received, the host shall transition to the Idle state.

DPH(Deferred) - If a DPH with the Deferred (DF) bit set is received, the host shall transition to the Idle state. This packet is received when the link has transitioned to a U1 or U2 state while waiting

8-90