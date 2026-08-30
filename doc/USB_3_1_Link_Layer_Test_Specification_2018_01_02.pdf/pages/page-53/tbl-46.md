|  7.5.12.4.2#3 | A downstream port shall transition from Hot Reset.Exit to Rx.Detect when directed to issue Warm Reset. | NT  |
| --- | --- | --- |
|  7.5.12.4.2#4 | An upstream port shall transition from Hot Reset.Exit to Rx.Detect when Warm Reset is detected. | NT  |
|  Chapter 8 Test Assertions: Protocol Layer  |   |   |
|  Subsection reference: 8.3 Packet Formats  |   |   |
|  Subsection reference: 8.3.1 Fields Common to all Headers  |   |   |
|  Subsection reference: 8.3.1.1 Reserved Values and Reserved Field Handling  |   |   |
|  8.3.1.1#1 | A receiver shall ignore any Reserved field. | PT 7.6  |
|  8.3.1.1#2 | A receiver shall ignore any packet that has any of its defined fields set to a reserved value, but it shall acknowledge the packet and return credit for the same. | NT  |
|  Subsection reference: 8.4 Link Management Packet (LMP)  |   |   |
|  Subsection reference: 8.4.2 Set Link Function  |   |   |
|  8.4.2#1 | Upon receipt of an LMP with the Force_LinkPM_Accept bit asserted, the upstream port shall accept all LGO_U1 and LGO_U2 Link Commands until the port receives an LMP with Force_LinkPM_Accept bit is de-asserted. | 7.23-24  |
|  Subsection reference: 8.4.4 Vendor Device Test  |   |   |
|  8.4.4#1 | The Vendor Device Test LMP shall not be used during normal operation of the link. | NT  |
|  Subsection reference: 8.4.5 Port Capabilities  |   |   |
|  8.4.5#1 | The port shall send the Port Capability LMP within tPortConfiguration time after completion of link initialization. | 5.1 7.17  |
|  8.4.5#2 | When the link partner that has downstream capability does not receive the Port Capability LMP within tPortConfiguration time, it shall signal an error. | NT  |
|  8.4.5#3 | When the link partner that only supports upstream capability does not receive Port Capability LMP within tPortConfiguration time, it shall transition to SS.Disabled and try to connect at the other speeds this device supports. | 7.17  |
|  8.4.5#4 | After exchanging Port Capability LMPs, the link partners shall determine which of the link partners shall be configured as the downstream facing port. | 7.38  |
|  Subsection reference: 8.4.6 Port Configuration  |   |   |