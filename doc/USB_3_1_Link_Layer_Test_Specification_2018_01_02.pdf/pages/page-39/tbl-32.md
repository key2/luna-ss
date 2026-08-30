|  7.5.4.6.2#5 | A peripheral device shall transition to eSS.Disabled upon the tPollingLBPMLFPSTimeout and the conditions to transition to Polling.PortConfig are not met. | NT  |
| --- | --- | --- |
|  7.5.4.6.2#6 | A downstream port shall transition to Rx.Detect when directed to issue Warm Reset. | NT  |
|  7.5.4.6.2#7 | An upstream port shall transition to Rx.Detect when a Warm Reset is detected. | NT  |
|  Subsection reference: 7.5.4.7 Polling.RxEQ  |   |   |
|  Subsection reference: 7.5.4.7.1 Polling.RxEQ Requirements  |   |   |
|  7.5.4.7.1#1 | The detection and correction of the lane polarity inversion in SuperSpeed operation shall be enabled in Polling.RxEQ. | 6.1  |
|  7.5.4.7.1#2 | The port shall transmit the corresponding TSEQ ordered sets in Polling.RxEQ. | BC  |
|  7.5.4.7.1#3 | The port shall complete receiver equalizer training upon exit from Polling.RxEQ . | BC  |
|  Subsection reference: 7.5.4.7.2 Exit from Polling.RxEQ  |   |   |
|  7.5.4.7.2#1 | The port in SuperSpeed operation shall transition from Polling.RxEQ to Polling.Active after 65,536 consecutive TSEQ ordered sets are transmitted. | BC  |
|  7.5.4.7.2#1 | The port in SuperSpeedPlus operation shall transition from Polling.RxEQ to Polling.Active after 262,143 TSEQ ordered sets are transmitted. | BC  |
|  7.5.4.7.2#2 | A downstream port shall transition from Polling.RxEQ to Rx.Detect when directed to issue Warm Reset. | NT  |
|  7.5.4.7.2#3 | An upstream port shall transition from Polling.RxEQ to Rx.Detect when Warm Reset is detected. | NT  |
|  Subsection reference: 7.5.4.8 Polling.Active  |   |   |
|  Subsection reference: 7.5.4.8.1 Polling.Active Requirements  |   |   |
|  7.5.4.8.1#1 | The port shall transmit TS1 ordered sets in Polling.Active. | BC  |
|  7.5.4.8.1#2 | The port in SuperSpeedPlus operation shall insert a SYNC ordered set every 32 TS1 ordered sets. | BC  |
|  7.5.4.8.1#3 | The port in SuperSpeedPlus operation shall perform block alignment and scrambler synchronization. | BC  |
|  7.5.4.8.1#4 | Lane polarity detection and correction shall be completed. | BC  |
|  7.5.4.8.1#5 | The receiver is training using TS1 or TS2 ordered sets in Polling.Active. | BC  |
|  Subsection reference: 7.5.4.8.2 Exit from Polling.Active  |   |   |