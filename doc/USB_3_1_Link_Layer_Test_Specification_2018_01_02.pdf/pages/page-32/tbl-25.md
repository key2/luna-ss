|  7.5.1.2.4#3 | A self-powered peripheral upstream port shall remain in eSS.Disabled.Error upon detection of USB 2.0 bus reset. | NT  |
| --- | --- | --- |
|  Subsection reference: 7.5.2 eSS.Inactive  |   |   |
|  Subsection reference: 7.5.2.3 eSS.Inactive.Quiet  |   |   |
|  Subsection reference: 7.5.2.3.1 eSS.Inactive.Quiet Requirement  |   |   |
|  7.5.2.3.1#1 | The function of the far-end receiver termination detection shall be disabled. | NT  |
|  Subsection reference: 7.5.2.3.2 Exit from eSS.Inactive.Quiet  |   |   |
|  7.5.2.3.2#1 | The port shall transition to eSS.Inactive.Disconnect.Detect upon the eSSInactiveQuietTimeout timer timeout. | NT  |
|  7.5.2.3.2#2 | A downstream port shall transition to Rx.Detect when Warm Reset is issued. | NT  |
|  7.5.2.3.2#3 | An upstream port shall transition to Rx.Detect upon detection of Warm Reset. | NT  |
|  Subsection reference: 7.5.2.4 eSS.Inactive.Disconnect.Detect  |   |   |
|  Subsection reference: 7.5.2.4.1 eSS.Inactive.Disconnect.Detect Requirements  |   |   |
|  7.5.2.4.1#1 | The transmitter shall perform the far-end receiver termination detection when in eSS.Inactive.Disconnect.Detect. | NT  |
|  Subsection reference: 7.5.2.4.2 Exit from eSS.Inactive.Disconnect.Detect  |   |   |
|  7.5.2.4.2#1 | The port shall transition to Rx.Detect when a far-end low-impedance receiver termination (RRX-DC) is not detected. | NT  |
|  7.5.2.4.2#2 | The port shall transition to eSS.Inactive.Quiet when a far-end low-impedance receiver termination (RRX-DC) is detected. | NT  |
|  Subsection reference: 7.5.3 Rx.Detect  |   |   |
|  Subsection reference: 7.5.3.3 Rx.Detect.Reset  |   |   |
|  Subsection reference: 7.5.3.3.1 Rx.Detect.Reset Requirements  |   |   |
|  7.5.3.3.1#1 | A downstream port shall transmit Warm Reset for the duration of tReset. | 7.31  |
|  7.5.3.3.1#2 | An upstream port shall remain in this state until it detects the completion of Warm Reset. | NT  |
|  Subsection reference: 7.5.3.3.2 Exit from Rx.Detect.Reset  |   |   |
|  7.5.3.3.2#1 | The port shall transition directly to Rx.Detect.Active when the entry to Rx.Detect is not due to a Warm Reset. | NT  |