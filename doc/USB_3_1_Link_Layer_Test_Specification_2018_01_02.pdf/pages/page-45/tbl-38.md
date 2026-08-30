|  7.5.6.2#4 | A downstream port shall transition from U0 to eSS.Inactive when directed. | NT  |
| --- | --- | --- |
|  7.5.6.2#5 | An upstream port shall transition from U0 to eSS.Disabled when directed. | NT  |
|  7.5.6.2#6 | A downstream port shall transition from U0 to Recovery upon not receiving any link commands within 1 ms. | 7.16  |
|  7.5.6.2#7 | A downstream port shall transition from U0 to Rx.Detect when directed to issue Warm Reset. | NT  |
|  7.5.6.2#8 | An upstream port shall transition from U0 to Rx.Detect when Warm Reset is detected. | NT  |
|  7.5.6.2#9 | An upstream port shall transition from U0 to eSS.Disabled upon detection of VBUS off. | NT  |
|  7.5.6.2#10 | A downstream port shall transition from U0 to eSS.Inactive upon tPortConfiguration timeout. | 7.17  |
|  7.5.6.2#11 | An upstream port shall transition from U0 to eSS.Disabled upon tPortConfiguration timeout. | 7.17  |
|  Subsection reference: 7.5.7 U1  |   |   |
|  Subsection reference : 7.5.7.1 U1 Requirements  |   |   |
|  7.5.7.1#1 | The port shall maintain its low-impedance receiver termination (RRX-DC) in U1. | NT  |
|  7.5.7.1#2 | The port shall enable U1 exit detect functionality in U1. | 7.18 7.23  |
|  7.5.7.1#3 | The port shall enable LFPS transmitter when it initiates the exit from U1. | IOP  |
|  7.5.7.1#4 | The port shall enable its U2 inactivity timer upon entry to U1 when the U2 inactivity timer has a non-zero timeout value. | NT  |
|  7.5.7.1#5 | A downstream port shall enable its Ping.LFPS detection in U1. | NT  |
|  7.5.7.1#6 | A downstream port shall enable a 300-ms timer in U1. This timer will be reset and restarted when a Ping.LFPS is received. | NT  |
|  7.5.7.1#7 | An upstream port shall transmit Ping.LFPS in U1. | NT  |
|  Subsection reference: 7.5.7.2 Exit from U1  |   |   |
|  7.5.7.2#1 | A downstream port shall transition from U1 to Rx.Detect when the 300-ms timer expires. | NT  |
|  7.5.7.2#2 | A downstream port shall transition from U1 to RxDetect when directed to issue Warm Reset. | NT  |