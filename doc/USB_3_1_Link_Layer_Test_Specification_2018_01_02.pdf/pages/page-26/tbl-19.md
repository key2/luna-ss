|  7.2.4.2.7#1 | When a port is initiating U3 wakeup, it shall start sending U3 LFPS wakeup handshake signal. | 7.36  |
| --- | --- | --- |
|  7.2.4.2.7#2 | A port upon receiving U1/U2 EXIT or U3 wakeup LFPS handshake signal shall start U1/U2 exit or U3 wakeup by responding with U1/U2 Exit or U3 wakeup LFPS signal. | 7.18-19 7.23-25  |
|  7.2.4.2.7#3 | Upon a successful LFPS handshake before tNoLFPSResponse Timeout, a port shall transition to Recovery. | 7.18-19 7.23-25  |
|  7.2.4.2.7#4 | A port initiating U1 or U2 Exit shall transition to eSS.Inactive upon tNoLFPSResponse timeout and the condition of a successful LFPS handshake is not met. | NT  |
|  7.2.4.2.7#5 | A port initiating U1 or U2 Exit shall transition to eSS.Inactive upon Ux_EXIT_TIMER timeout and the link has not transitioned to U0. | NT  |
|  7.2.4.2.7#6 | A port initiating U3 wakeup shall remain in U3 when the condition of a successful LFPS handshake is not met upon tNoLFPSResponse Timeout. | NT  |
|  Subsection reference: 7.3 Link Error Rules/Recovery  |   |   |
|  Subsection reference: 7.3.3 Link Error Statistics  |   |   |
|  Subsection reference: 7.3.3.1 Link Error Count  |   |   |
|  7.3.3.1#1 | Except for the upstream port in SuperSpeed operation, all ports shall implement the Link Error Count. | NT  |
|  7.3.3.1#2 | A port in SuperSpeedPlus operation shall implement a Link Error Count that counts up to 65,535 error events. The Link Error Count shall saturate if it has reached its maximum count value. | NT  |
|  7.3.3.1#3 | The Link Error Count shall be reset to zero during PowerOn Reset. | NT  |
|  7.3.3.1#4 | The Link Error Count shall be reset to zero during entry to Polling.Idle. | NT  |
|  7.3.3.1#5 | The Link Error Count shall be reset to zero when directed. | NT  |
|  7.3.3.1#6 | The Link Error Count shall be reset to zero during Hot Reset. | NT  |
|  7.3.3.1#7 | The Link Error Count shall be incremented by one each time a port transitions from U0 to Recovery to recover an error event. | NT  |
|  Subsection reference: 7.3.4.1 Packet Framing Errors  |   |   |
|  7.3.4.1#1 | A valid HPSTART or DPHSTART OS, or a valid DPP framing ordered set shall be declared if the following two conditions are met: • At least three of the four symbols in the four consecutive symbol periods are valid packet framing symbols. | 7.6 7.7  |