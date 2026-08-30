Universal Serial Bus 3.1 Specification, Revision 1.0

Data state. Upon transitioning to the Move Data state the host sets CStream to the value of Stream x. Typically the Move Data transition will be selected when the Stream that has just had its Endpoint buffers modified is the same Stream as the one that the device last selected, e.g., Stream x = LCStream. PP shall equal 1 because the host is capable of receiving another DP from the device. This transition optionally may be disabled in some hosts, and some Device Classes may not process this transition (e.g., Mass Storage UASP).

### 8.12.1.4.4.4 Start Stream

In the Start Stream state, the device has sent an ERDY proposing to the host that it initiate an IN transfer for Stream n and it is waiting for the host to accept or reject the Stream selection.

ACK(Stream n, NumP>0) - If the host has accepted the device's proposal for starting Stream n, then it shall transmit an ACK TP with a Stream ID equal to Stream n, and transition to the Move Data state. Upon transitioning to the Move Data state the host sets CStream to the value of Stream n. The host shall accept a Stream proposal from a device if there are Endpoint Buffers available to receive the Function Data for the Stream. PP shall equal 1 because the host is capable of receiving another DP from the device.

ACK(NoStream, NumP=0, PP = 0) - If the host rejects the device's proposal for starting Stream n, then it shall transmit an ACK TP with a Stream ID equal to NoStream, and transition to the Idle state. The host shall reject a Stream proposal from a device if there are no Endpoint Buffers available to receive the Function Data for the Stream.

8-84