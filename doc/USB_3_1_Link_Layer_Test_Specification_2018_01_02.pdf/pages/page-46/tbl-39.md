|  7.5.7.2#3 | An upstream port shall transition from U1 to Rx.Detect when Warm Reset is detected. | NT  |
| --- | --- | --- |
|  7.5.7.2#4 | A self-powered upstream port shall transition from U1 to eSS.Disabled upon not detecting valid VBUS. | NT  |
|  7.5.7.2#5 | A port shall transition from U1 to U2 upon the timeout of the U2 inactivity timer. | NT  |
|  7.5.7.2#6 | A port shall transition from U1 to Recovery upon completion of an LFPS handshake (U1 LFPS exit). | 7.18 7.23  |
|  7.5.7.2#7 | A port shall transition from U1 to eSS.Inactive upon the 2-ms LFPS handshake timer timeout if a successful LFPS handshake is not achieved. | NT  |
|  Subsection reference: 7.5.8 U2  |   |   |
|  Subsection reference: 7.5.8.1 U2 Requirements  |   |   |
|  7.5.8.1#1 | A port shall maintain its low-impedance receiver termination (RRX-DC) in U2. | NT  |
|  7.5.8.1#2 | A port shall enable its U2 exit detect functionality when in U2. | 7.19 7.24  |
|  7.5.8.1#3 | A port shall enable its LFPS transmitter when it initiates the exit from U2. | NT  |
|  7.5.8.1#4 | A downstream port shall perform a far-end receiver termination detection every 100 ms in U2. | NT  |
|  Subsection reference: 7.5.8.2 Exit from U2  |   |   |
|  7.5.8.2#1 | A downstream port shall transition from U2 to Rx.Detect upon detection of a far-end high-impedance receiver termination (ZRX-HIGH-IMP-DC-POS). | NT  |
|  7.5.8.2#2 | A downstream port shall transition from U2 to Rx.Detect when directed to issue Warm Reset. | NT  |
|  7.5.8.2#3 | An upstream port shall transition from U2 to Rx.Detect when Warm Reset is detected. | NT  |
|  7.5.8.2#4 | A self-powered upstream port shall transition from U2 to eSS.Disabled upon not detecting valid VBUS. | NT  |
|  7.5.8.2#5 | A port shall transition from U2 to Recovery upon successful completion of a LFPS handshake (U2 LFPS exit). | 7.19 7.24  |
|  7.5.8.2#6 | The port shall transition from U2 to eSS.Inactive upon the 2-ms LFPS handshake timer timeout if a successful LFPS handshake is not achieved. | NT  |
|  Subsection reference: 7.5.9 U3  |   |   |