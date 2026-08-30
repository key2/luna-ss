|  7.5.4.10.2#2 | A port shall transition to Loopback as a loopback slave when the Loopback bit is asserted in the TS2 ordered set received in Polling.Configuration. | NT  |
| --- | --- | --- |
|  7.5.4.10.2#3 | A downstream port shall transition to Hot Reset when directed. | 7.29  |
|  7.5.4.10.2#4 | An upstream port shall transition to Hot Reset when the Reset bit is asserted in the TS2 ordered set received in Polling.Configuration. | 7.27  |
|  7.5.4.10.2#5 | The port shall transition from Polling.Idle to U0 when the following two conditions are met: • Eight consecutive Idle Symbols are received. • Sixteen Idle Symbols are sent after receiving one Idle Symbol. | NT  |
|  7.5.4.10.2#6 | A downstream port in SuperSpeed operation shall transition from Polling.Idle to Rx.Detect upon the 2-ms timer timeout if the conditions to transition to U0 are not met and cPollingTimeout is less than two. | NT  |
|  7.5.4.10.2#7 | A downstream port in SuperSpeed operation shall transition from Polling.Idle to eSS.Inactive upon the 2-ms timer timeout if the conditions to transition to U0 are not met and cPollingTimeout is two. | NT  |
|  7.5.4.10.2#8 | An upstream port of a hub in SuperSpeed operation shall transition from Polling.Idle to Rx.Detect upon the 2-ms timer timeout if the conditions to transition to U0 are not met. | NT  |
|  7.5.4.10.2#9 | An upstream port of a peripheral device in SuperSpeed operation shall transition from Polling.Idle to eSS.Disabled upon the 2-ms timer timeout if the conditions to transition to U0 are not met. | NT  |
|  7.5.4.10.2#10 | A downstream port in SuperSpeedPlus operation shall transition to Polling.PortMatch to negotiate for alternative operation upon the 12ms timeout and the conditions to transition to Polling.Configuration are not met. | NT  |
|  7.5.4.10.2#11 | An upstream port of a hub in SuperSpeedPlus operation shall transition to Polling.PortMatch to negotiate for alternative operation upon the 12ms timeout and the conditions to transition to Polling.Configuration are not met. | NT  |
|  7.5.4.10.2#12 | An upstream port of a peripheral device in SuperSpeedPlus operation shall transition to Polling.PortMatch to negotiate for alternative operation upon the 12ms timeout and the conditions to transition to Polling.Configuration are not met. | NT  |
|  7.5.4.10.2#13 | A downstream port shall transition from Polling.Idle to Rx.Detect when Reset is directed. | NT  |
|  7.5.4.10.2#14 | An upstream port shall transition from Polling.Idle to Rx.Detect when Warm Reset is detected. | NT  |
|  Subsection reference: 7.5.5 Compliance Mode  |   |   |