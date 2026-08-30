|  7.5.4.3.2#6 | A downstream port shall transition from Polling.LFPS to Rx.Detect upon the 360-ms timer timeout if cPollingTimeout is less than two and Compliance Mode is disabled. | 7.40  |
| --- | --- | --- |
|  7.5.4.3.2#7 | A downstream port shall transition from Polling.LFPS to eSS.Inactive upon the 360-ms timer timeout and cPollingTimeout is two. | 7.40  |
|  7.5.4.3.2#8 | An upstream port of a hub shall transition from Polling.LFPS to Rx.Detect upon the 360-ms timer timeout after having trained once since PowerOn Reset if the conditions to transition to Polling.RxEQ are not met. | NT  |
|  7.5.4.3.2#9 | A peripheral device shall transition from Polling.LFPS to eSS.Disabled upon the 360-ms timeout after having trained once since PowerOn Reset if the conditions to transition to Polling.ExEQ are not met. | NT  |
|  7.5.4.3.2#10 | A downstream port shall transition from Polling.LFPS to Rx.Detect when directed to issue Warm Reset. | NT  |
|  7.5.4.3.2#11 | An upstream port shall transition from Polling.LFPS to Rx.Detect when Warm Reset is detected. | NT  |
|  Subsection reference: 7.5.4.4 Polling.LFPSPlus  |   |   |
|  Subsection reference: 7.5.4.4.1 Polling.LFPSPlus Requirements  |   |   |
|  7.5.4.4.1#1 | A port in SuperSpeedPlus operation shall transmit SCD2. If SCD2 cannot be found in sixteen consecutive Polling.LFPS received, the port shall transmit Polling.LFPS instead of SCD2. | NT  |
|  7.5.4.4.1#2 | The operation of the 360ms timer (tPollingLFPSTimeout) shall continue without reset upon entry to this substate from Polling.LFPS. | NT  |
|  7.5.4.4.1#3 | A port in SuperSpeedPlus operation shall be ready for SuperSpeed operation if it has detected that its link partner operates at SuperSpeed. | 7.1  |
|  7.5.4.4.1#4 | A port in SuperSpeedPlus operation shall implement a 60us timer (tPollingSCDLFPSTimeout) to monitor the absence of LFPS signal after the completion of SuperSpeed Polling.LFPS handshake. | 7.1  |
|  Subsection reference: 7.5.4.4.2 Exit from Polling.LFPSPlus  |   |   |
|  7.5.4.4.2#1 | A port in SuperSpeedPlus operation shall transition to Polling.PortMatch if two SCD2 are transmitted after one SCD2 is received. | BC  |
|  7.5.4.4.2#2 | A port in SuperSpeedPlus operation shall transition to Polling.RxEQ and switch to SuperSpeed operation if the following two conditions are met: • No LFPS signal for more than tPollingSCDLFPSTimeout is observed. | NT  |