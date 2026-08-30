|  7.5.3.3.2#2 | A downstream port shall transition to Rx.Detect.Active after it transmits Warm Reset for the duration of tReset. | NT  |
| --- | --- | --- |
|  7.5.3.3.2#3 | An upstream port shall transition to Rx.Detect.Active when it receives no more LFPS Warm Reset signaling. | NT  |
|  Subsection reference: 7.5.3.4 Rx.Detect.Active  |   |   |
|  Subsection reference: 7.5.3.5 Rx.Detect.Active Requirement  |   |   |
|  7.5.3.5#1 | The transmitter shall initiate a far-end receiver termination detection when in Rx.Detect.Active. | NT  |
|  7.5.3.5#2 | The number of far-end receiver termination detection events shall be counted by an upstream port when in Rx.Detect.Active. | NT  |
|  Subsection reference: 7.5.3.6 Exit from Rx.Detect.Active  |   |   |
|  7.5.3.6#1 | The port shall transition from Rx.Detect.Active to Polling upon detection of a far-end low-impedance receiver termination (RRX-DC). | NT  |
|  7.5.3.6#2 | A downstream port shall transition from Rx.Detect.Active to Rx.Detect.Quiet when a far-end low-impedance receiver termination (RRX-DC) is not detected. | NT  |
|  7.5.3.6#3 | An upstream port of a hub shall transition from Rx.Detect.Active to Rx.Detect.Quiet when a far-end low-impedance receiver termination (RRX-DC) is not detected. | NT  |
|  7.5.3.6#4 | An upstream port of a peripheral device shall transition from Rx.Detect.Active to Rx.Detect.Quiet when the following two conditions are met: - A far-end low-impedance receiver termination (RRX-DC) is not detected. - The number of far-end receiver termination detection events is less than eight. | NT  |
|  7.5.3.6#5 | An upstream port of a peripheral device shall transition from Rx.Detect.Active to eSS.Disabled when the following two conditions are met: - A far-end low-impedance receiver termination (RRX-DC) is not detected. - The number of far-end receiver termination (RRX-DC) detection events has reached eight. | NT  |
|  Subsection reference: 7.5.3.7 Rx.Detect.Quiet  |   |   |
|  Subsection reference: 7.5.3.7.1 Rx.Detect.Quiet Requirements  |   |   |
|  7.5.3.7.1#1 | The far-end receiver termination detection shall be disabled when in Rx.Detect.Quiet. | NT  |
|  Subsection reference: 7.5.3.7.2 Exit from Rx.Detect.Quiet  |   |   |