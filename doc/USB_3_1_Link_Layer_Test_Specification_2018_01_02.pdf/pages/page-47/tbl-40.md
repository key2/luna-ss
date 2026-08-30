|  Subsection reference: 7.5.9.1 U3 Requirements  |   |   |
| --- | --- | --- |
|  7.5.9.1#1 | The port shall maintain its low-impedance receiver termination (RRX-DC) in U3. | NT  |
|  7.5.9.1#2 | LFPS Ping detection shall be disabled in U3. (Downstream port Only.) | NT  |
|  7.5.9.1#3 | The port shall enable its U3 wakeup detect functionality in U3. | 7.25  |
|  7.5.9.1#4 | The port shall enable its LFPS transmitter when it initiates the exit from U3. | 7.36  |
|  7.5.9.1#5 | A downstream port shall perform a far-end receiver termination detection every 100 ms in U3. | NT  |
|  Subsection reference: 7.5.9.2 Exit from U3  |   |   |
|  7.5.9.2#1 | A downstream port shall transition from U3 to Rx.Detect upon detection of a far-end high-impedance receiver termination (ZRX-HIGH-IMP-DC-POS). | NT  |
|  7.5.9.2#2 | A downstream port shall transition from U3 to Rx.Detect when directed to issue Warm Reset. | 7.35  |
|  7.5.9.2#3 | An upstream port shall transition from U3 to Rx.Detect when Warm Reset is detected. | NT  |
|  7.5.9.2#4 | A self-powered upstream port shall transition from U3 to eSS.Disabled upon not detecting valid VBUS. | NT  |
|  7.5.9.2#5 | A port shall transition from U3 to Recovery upon successful completion of a LFPS handshake (U3 wakeup). | 7.36 7.25  |
|  7.5.9.2#6 | A port shall remain in U3 when the 10-ms LFPS handshake timer times out if a successful LFPS handshake is not achieved. | NT  |
|  7.5.9.2#7 | A port in U3 100ms after an unsuccessful LFPS exit handshake and the requirement to exit U3 still exists shall initiate the U3 wakeup LFPS handshake to wake up the host. | NT  |
|  Subsection reference: 7.5.10 Recovery  |   |   |
|  Subsection reference: 7.5.10.3 Recovery.Active  |   |   |
|  Subsection reference: 7.5.10.3.1 Recovery.Active Requirements  |   |   |
|  7.5.10.3.1#1 | A port shall transmit the TS1 ordered sets upon entry to Recovery.Active. | 7.26 7.30  |
|  7.5.10.3.1#2 | A port shall train its receiver with TS1 or TS2 ordered sets in Recover.Active. | 7.26 7.30  |
|  7.5.10.3.1#3 | The port in SuperSpeedPlus operation shall insert a SYNC ordered set every 32 TS1 ordered sets. | BC  |