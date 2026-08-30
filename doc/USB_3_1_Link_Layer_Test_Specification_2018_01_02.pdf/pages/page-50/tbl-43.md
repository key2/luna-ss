|  7.5.10.5.1#6 | A port shall be able to receive the Header Sequence Number Advertisement from its link partner in Recovery.Idle. | NT  |
| --- | --- | --- |
|  Subsection reference: 7.5.10.5.2 Exit from Recovery.Idle  |   |   |
|  7.5.10.5.2#1 | A port shall transition from Recovery.Idle to Loopback when directed as a loopback master if the port is capable of being a loopback master. | NT  |
|  7.5.10.5.2#2 | A port shall transition from Recovery.Idle to Loopback as a loopback slave when the Loopback bit is asserted in TS2 ordered sets. | NT  |
|  7.5.10.5.2#3 | A port shall transition from Recovery.Idle to U0 when the following two conditions are met: • Eight consecutive Idle Symbols are received. • Sixteen Idle Symbols are sent after receiving one Idle Symbol. | 7.26 7.30  |
|  7.5.10.5.2#4 | A port shall transition from Recovery.Idle to eSS.Inactive when Ux_EXIT_TIMER or the 2-ms timer times out if the conditions to transition to U0 are not met. | NT  |
|  7.5.10.5.2#5 | A downstream port shall transition from Recovery.Idle to Hot Reset when directed. | NT  |
|  7.5.10.5.2#6 | A downstream port shall transition from Recovery.Idle to Rx.Detect when directed to issue Warm Reset. | NT  |
|  7.5.10.5.2#7 | An upstream port shall transition from Recovery.Idle to Rx.Detect when Warm Reset is detected. | NT  |
|  7.5.10.5.2#8 | An upstream port shall transition from Recovery.Idle to Hot Reset when the Reset bit is asserted in TS2 ordered sets. | NT  |
|  Subsection reference: 7.5.11 Loopback  |   |   |
|  Subsection reference: 7.5.11.3.1 Loopback.Active Requirements  |   |   |
|  7.5.11.3.1#1 | A loopback master shall send valid 8b/10b data with SKPs as necessary when in Loopback.Active. | NT  |
|  7.5.11.3.1#2 | A loopback slave shall retransmit the received 10-bit symbols when in Loopback.Active. | NT  |
|  7.5.11.3.1#3 | A loopback slave shall not modify the received 10-bit symbols in Loopback.Active. (Other than SKP ordered set, which may be added or dropped.) | NT  |
|  7.5.11.3.1#4 | The loopback slave shall process the BERT commands in Loopback.Active. | NT  |
|  7.5.11.3.1#5 | The LFPS receiver shall be enabled in Loopback.Active. | NT  |
|  Subsection reference: 7.5.11.3.2 Exit from Loopback.Active  |   |   |