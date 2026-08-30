|  7.5.3.7.2#1 | A downstream port shall transition from Rx.Detect.Quiet to Rx.Detect.Active upon the timeout of the tRxDetectQuietTimeoutDFP timer (12ms to 120ms). | NT  |
| --- | --- | --- |
|  7.5.3.7.2#2 | An upstream port shall transition from Rx.Detect.Quiet to Rx.Detect.Active upon the timeout of the tRxDetectQuietTimeoutUFP timer (12ms). | NT  |
|  Subsection reference: 7.5.4 Polling  |   |   |
|  Subsection reference: 7.5.4.2 Polling Requirements  |   |   |
|  7.5.4.2#1 | A downstream port shall implement a counter, cPollingTimeout, which shall be reset to zero upon PowerOn Reset, Warm Reset on the upstream port, exit to eSS.Disabled or eSS.Inactive or U0, and detection of the removal of far-end terminations. | BC  |
|  7.5.4.2#2 | A downstream port shall implement a counter, cPollingTimeout, which shall be incremented by one or saturated at two if a transition to Rx.Detect is due to timeout in any of the Polling substates. | 7.40  |
|  Subsection reference: 7.5.4.3 Polling.LFPS  |   |   |
|  Subsection reference: 7.5.4.3.1 Polling.LFPS Requirements  |   |   |
|  7.5.4.3.1#1 | Upon entry to Polling.LFPS, an LFPS receiver shall be enabled. | BC  |
|  7.5.4.3.1#2 | Upon entry to Polling.LFPS, a port shall establish its LFPS operating condition within 80 μs. | NT  |
|  7.5.4.3.1#3 | A downstream port shall disable its transition path to Compliance Mode upon PowerOn Reset or Warm Reset. | NT  |
|  7.5.4.3.1#4 | A downstream port shall enabled its transition path to Compliance Mode, if directed. | 7.34  |
|  7.5.4.3.1#5 | An upstream port always has its transition path to Compliance Mode enabled upon PowerOn Reset. | 7.33  |
|  7.5.4.3.1#6 | A port in SuperSpeed operation shall transmit Polling.LFPS. | BC  |
|  7.5.4.3.1#7 | An upstream port in SuperSpeedPlus operation shall transmit SCD1. If no signature of SCD1 is found in sixteen consecutive Polling.LFPS received, the port shall switch to SuperSpeed operation and transmit Polling.LFPS instead of SCD1. | 7.1  |
|  7.5.4.3.1#8 | A downstream port in SuperSpeedPlus operation shall transmit SCD1 if Compliance Mode is disabled. If no signature of SCD1 is found in sixteen consecutive Polling.LFPS received, the port shall switch to SuperSpeed operation and transmit Polling.LFPS instead of SCD1. | 7.1  |
|  7.5.4.3.1#8 | A downstream port in SuperSpeedPlus operation shall transmit SCD2 if Compliance Mode is enabled. | NT  |
|  7.5.4.3.1#9 | A port in SuperSpeedPlus operation shall implement a 60us timer (tPollingSCDLFPSTimeout) to monitor the absence of | 7.1  |