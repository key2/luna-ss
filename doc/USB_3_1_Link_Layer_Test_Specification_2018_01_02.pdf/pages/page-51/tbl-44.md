|  7.5.11.3.2#1 | A downstream port shall transition from Loopback.Active to Rx.Detect when directed to issue Warm Reset. | NT  |
| --- | --- | --- |
|  7.5.11.3.2#2 | An upstream port shall transition from Loopback.Active to Rx.Detect when Warm Reset is detected. | NT  |
|  7.5.11.3.2#3 | When directed, loopback master shall transition from Loopback.Active to Loopback.Exit. | NT  |
|  7.5.11.3.2#4 | A loopback slave shall transition from Loopback.Active to Loopback.Exit upon detection of Loopback LFPS exit handshake. | NT  |
|  Subsection reference: 7.5.11.4 Loopback.Exit  |   |   |
|  Subsection reference: 7.5.11.4.1 Loopback.Exit Requirements  |   |   |
|  7.5.11.4.1#1 | A LFPS transmitter and the LFPS receiver shall be enabled in Loopback.Exit. | NT  |
|  7.5.11.4.1#2 | A port shall transmit and receive Loopback LFPS exit handshake in Loopback.Exit. | NT  |
|  Subsection reference: 7.5.11.4.2 Exit from Loopback.Exit  |   |   |
|  7.5.11.4.2#1 | A port shall transition from Loopback.Exit to Rx.Detect upon a successful Loopback LFPS exit handshake. | NT  |
|  7.5.11.4.2#2 | A port shall transition from Loopback.Exit to eSS.Inactive upon the 2-ms timer timeout if the condition to transition to Rx.Detect is not met | NT  |
|  7.5.11.4.2#3 | A downstream port shall transition from Loopback.Exit to Rx.Detect when directed to issue Warm Reset. | NT  |
|  7.5.11.4.2#4 | An upstream port shall transition from Loopback.Exit to Rx.Detect when Warm Reset is detected. | NT  |
|  Subsection reference: 7.5.12 Hot Reset  |   |   |
|  Subsection reference: 7.5.12.2 Hot Reset Requirements  |   |   |
|  7.5.12.2#1 | A downstream port shall reset its PM timers and the U1 and U2 timeout value to zero in Hot Reset. | NT  |
|  Subsection reference: 7.5.12.3 Hot Reset.Active  |   |   |
|  Subsection reference: 7.5.12.3.1 Hot Reset.Active Requirements  |   |   |
|  7.5.12.3.1#1 | Upon entry to this Hot Reset.Active, the port shall first transmit at least 16 TS2 ordered sets continuously with the Reset bit asserted. | 7.27-29  |
|  7.5.12.3.1#2 | In Hot Reset.Active a downstream port shall continue to transmit TS2 ordered sets with the Reset bit asserted until the upstream port transitions from sending TS2 ordered sets with the Reset bit | 7.29  |