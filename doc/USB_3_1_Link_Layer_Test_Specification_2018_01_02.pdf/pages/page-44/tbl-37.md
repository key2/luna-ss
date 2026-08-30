|  Subsection reference: 7.5.5.1 Compliance Mode Requirements  |   |   |
| --- | --- | --- |
|  7.5.5.1#1 | The port shall maintain the low-impedance receiver termination (RRX-DC) when it is in Compliance Mode. | NT  |
|  7.5.5.1#2 | Upon entry to Compliance Mode, the port shall wait until its SS Tx DC common mode voltage meets specification in Table 6-18 before it starts to send the first compliance test pattern. | NT  |
|  7.5.5.1#3 | The port shall transmit the next compliance test pattern continuously upon detection of a Ping.LFPS when in Compliance Mode. | 7.33 7.34  |
|  7.5.5.1#4 | The port shall transmit the first compliance test pattern continuously upon detection of a Ping.LFPS and the test pattern has reached the final test pattern. | NT  |
|  Subsection reference: 7.5.5.2 Exit from Compliance Mode  |   |   |
|  7.5.5.2#1 | A downstream port shall transition from Compliance Mode to Rx.Detect when directed to issue Warm Reset. | 7.34  |
|  7.5.5.2#2 | An upstream port shall transition from Compliance Mode to Rx.Detect upon detection of Warm Reset. | 7.33  |
|  Subsection reference: 7.5.6 U0  |   |   |
|  Subsection reference: 7.5.6.1 U0 Requirements  |   |   |
|  7.5.6.1#1 | The port shall maintain the low-impedance receiver termination (RRX-DC) in U0. | NT  |
|  7.5.6.1#2 | The LFPS receiver shall be enabled in U0. | IOP  |
|  7.5.6.1#3 | A port shall enable a 1-ms timer to measure the time interval between two consecutive link commands in U0. | 7.16  |
|  7.5.6.1#4 | A port shall enable a 10-μs timer in U0. It shall be reset when the first symbol of any link command or packet is sent and restarted after the last symbol of any link command or packet is sent. This timer shall be active when the link is in logical idle. | NT  |
|  7.5.6.1#5 | An upstream port shall transmit a single LUP when the 10-μs timer expires in U0. | 5.1  |
|  7.5.6.1#6 | A downstream port shall transmit a single LDN when the 10-μs timer expires in U0. | 5.1  |
|  Subsection reference: 7.5.6.2 Exit from U0  |   |   |
|  7.5.6.2#1 | The port shall transition from U0 to Recovery upon detection of a TS1 ordered set. | NT  |
|  7.5.6.2#2 | The port shall transition from U0 to Recovery when directed. | NT  |
|  7.5.6.2#3 | The port shall transition from U0 to eSS.Inactive when PENDING_HP_TIMER times out for the fourth consecutive time. | NT  |