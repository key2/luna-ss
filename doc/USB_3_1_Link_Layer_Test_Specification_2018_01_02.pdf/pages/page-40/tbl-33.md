|  7.5.4.8.2#1 | The port in SuperSpeed operation shall transition from Polling.Active to Polling.Configuration upon receiving eight consecutive and identical TS1 or TS2 ordered sets. | BC  |
| --- | --- | --- |
|  7.5.4.8.2#2 | The port in SuperSpeedPlus operation shall transition from Polling.Active to Polling.Configuration upon receiving eight consecutive and identical TS1 or TS2 ordered sets, excluding symbols 14 and 15 of TS1 or TS2 ordered sets. | BC  |
|  7.5.4.8.2#3 | A downstream port in SuperSpeed operation shall transition from Polling.Active to Rx.Detect upon the 12-ms timer timeout if the conditions to transition to Polling.Configuration are not met and cPollingTimeout is less than two. | 7.40  |
|  7.5.4.8.2#4 | A downstream port in SuperSpeed operation shall transition from Polling.Active to eSS.Inactive upon the 12-ms timer timeout if the conditions to transition to Polling.Configuration are not met and cPollingTimeout is two. | 7.40  |
|  7.5.4.8.2#5 | An upstream port of a hub shall transition from Polling.Active to Rx.Detect upon the 12-ms timer timeout if the conditions to transition to Polling.Configuration are not met. | NT  |
|  7.5.4.8.2#6 | An upstream port of a peripheral device shall transition from Polling.Active to eSS.Disabled upon the 12-ms timer timeout if the conditions to transition to Polling.Configuration are not met. | NT  |
|  7.5.4.8.2#7 | A downstream port in SuperSpeedPlus operation shall transition to Polling.PortMatch to negotiate for alternative operation upon the 12ms timeout and the conditions to transition to Polling.Configuration are not met. | NT  |
|  7.5.4.8.2#8 | An upstream port of a hub in SuperSpeedPlus operation shall transition to Polling.PortMatch to negotiate for alternative operation upon the 12ms timeout and the conditions to transition to Polling.Configuration are not met. | NT  |
|  7.5.4.8.2#9 | An upstream port of a peripheral device in SuperSpeedPlus operation shall transition to Polling.PortMatch to negotiate for alternative operation upon the 12ms timeout and the conditions to transition to Polling.Configuration are not met. | NT  |
|  7.5.4.8.2#10 | A downstream port shall transition to from Polling.Active to Rx.Detect when directed to issue Warm Reset. | NT  |
|  7.5.4.8.2#11 | An upstream port shall transition to from Polling.Active to Rx.Detect when Warm Reset is detected. | NT  |
|  Subsection reference: 7.5.4.9 Polling.Configuration  |   |   |
|  Subsection reference: 7.5.4.9.1 Polling.Configuration Requirements  |   |   |
|  7.5.4.9.1#1 | The downstream port shall transmit identical TS2 ordered sets upon entry to Polling.Configuration and set the Reset bit, when directed. | BC 7.29  |
|  7.5.4.9.1#2 | A port that has Loopback Master capability and has been directed to enter Loopback shall transmit identical TS2 ordered | NT  |