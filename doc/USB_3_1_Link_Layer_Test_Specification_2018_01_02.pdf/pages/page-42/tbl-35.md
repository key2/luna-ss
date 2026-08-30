|   | the 12ms timeout and the conditions to transition to Polling.Configuration are not met. |   |
| --- | --- | --- |
|  7.5.4.9.2#8 | An upstream port of a hub in SuperSpeedPlus operation shall transition to Polling.PortMatch to negotiate for alternative operation upon the 12ms timeout and the conditions to transition to Polling.Configuration are not met. | NT  |
|  7.5.4.9.2#9 | An upstream port of a peripheral device in SuperSpeedPlus operation shall transition to Polling.PortMatch to negotiate for alternative operation upon the 12ms timeout and the conditions to transition to Polling.Configuration are not met. | NT  |
|  7.5.4.9.2#10 | A downstream port shall transition from Polling.Configuration to Rx.Detect when directed to issue Warm Reset. | NT  |
|  7.5.4.9.2#11 | An upstream port shall transition from Polling.Configuration to Rx.Detect when Warm Reset is detected. | NT  |
|  Subsection reference: 7.5.4.10 Polling.Idle  |   |   |
|  Subsection reference: 7.5.4.10.1 Polling.Idle Requirements  |   |   |
|  7.5.4.10.1#1 | A downstream port shall reset its Link Error Count when it enters Polling.Idle. | NT  |
|  7.5.4.10.1#2 | An upstream port shall reset its port configuration information to default values when it enters Polling.Idle. | NT  |
|  7.5.4.10.1#3 | A port in SuperSpeed operation shall enable scrambling if the Disabling Scrambling bit is not asserted in the TS2 ordered set received in Polling.Configuration. | NT  |
|  7.5.4.10.1#4 | A port in SuperSpeed operation shall disable the scrambling when directed, or when the Disabling Scrambling bit is asserted in the TS2 ordered set received in Polling.Configuration. | NT  |
|  7.5.4.10.1#5 | A port in SuperSpeed operation shall transmit Idle Symbols in Polling.Idle if the next state is U0. | NT  |
|  7.5.4.10.1#6 | A port in SuperSpeedPlus operation shall transmit a single SDS ordered set before the start of the data blocks with Idle Symbols if the next state is U0. | NT  |
|  7.5.4.10.1#7 | A port in SuperSpeedPlus operation shall disable the scrambling upon completion of SDS ordered set transmission if directed, or if the Disabling Scrambling bit is asserted in the TS2 ordered set received in Polling.Configuration. | NT  |
|  7.5.4.10.1#8 | The port shall be able to receive the Header Sequence Number Advertisement from its link partner in Polling.Idle. | NT  |
|  Subsection reference: 7.5.4.10.2 Exit form Polling.Idle  |   |   |
|  7.5.4.10.2#1 | A port having Loopback Master capability shall transition to Loopback when directed. | NT  |