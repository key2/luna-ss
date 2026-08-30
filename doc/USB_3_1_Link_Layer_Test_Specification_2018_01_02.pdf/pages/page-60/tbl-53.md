|  10.3.1.6#6 | If the port initiates a hot reset on the link and the hot reset TS1/TS2 handshake fails, a warm reset is automatically tried. | 7.31  |
| --- | --- | --- |
|  10.3.1.6#7 | When the downstream port link enters Rx.Detect.Active during a warm reset, the hub shall start a timer to count the time it is in Rx.Detect.Active. If this timer exceeds tTimeForResetError while the link remains in Rx.Detect.Active, the port shall transition to the DSPORT.Disconnected state. | 7.32  |
|  Subsection reference: 10.4 Hub Downstream Facing Port Power Management  |   |   |
|  Subsection reference: 10.4.2 Hub Downstream Facing Port State Descriptions  |   |   |
|  Subsection reference: 10.4.2.1 Enabled U0 States  |   |   |
|  10.4.2.1#14 | Hub shall ensure that there is no race condition between a link partner initiating a U1/U2 request and transitioning to U0 based on SetPortFeature(PORT_LINK_STATE) request. | NT  |
|  XHCI Specification Chapter 5 Test Assertions: Register Interface  |   |   |
|  Subsection reference: xHCI 5.4 Host Controller Operational Registers  |   |   |
|  Subsection reference: xHCI 5.4.8 Port Status and Control Register (PORTSC)  |   |   |
|  5.4.8 | The xHC shall set the PLC bit of the PORTSC register of a USB3 port to '1' when an Error occurs (the link transitions from any state -> Inactive). | NT  |