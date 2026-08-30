|   | acknowledge the packet and return credit for the same as per the requirement specified in Section 7.2.4.1. |   |
| --- | --- | --- |
|  8.4.8.2#2 | LDM timestamps shall reference the first framing symbol of a received or transmitted LDM LMP. | NT  |
|  Subsection reference: 8.4.8.3 LDM State Machines  |   |   |
|  Subsection reference: 8.4.8.3.1 Requester Operation  |   |   |
|  8.4.8.3.1#1 | The LDM Requester State Machine shall maintain the local variable Init Response Timeout Counter. | NT  |
|  8.4.8.3.1#2 | The LDM Requester State Machine shall maintain the local timer Response Timer. | NT  |
|  Subsection reference: 8.4.8.3.1.1 Init Request  |   |   |
|  8.4.8.3.1.1#1 | Upon entering this state, the Requester shall set the LDM Enabled flag to 1. | NT  |
|  8.4.8.3.1.1#2 | The Init Response Timeout Counter shall be initialized to 0 at power up, or if the Init Request state is entered from the LDM Disabled or Timestamp Response states. | NT  |
|  8.4.8.3.1.1#3 | If the Init Request state is entered from the Init Response state, then the Init Response Timeout Counter shall not be changed. | NT  |
|  8.4.8.3.1.1#4 | When a trigger event occurs, the Requester shall transmit a LDM TS Request LMP to the Responder, save timestamp t1 from the Local Time Source in the LDM Context to record the time that the LDM Request was transmitted, and transition to the Init Response state. | NT  |
|  Subsection reference: 8.4.8.3.1.2 Init Response  |   |   |
|  8.4.8.3.1.2#1 | Upon entering this state, the Requester shall increment the Init Response Timeout Counter, start the Response Timer and wait for a TS Response LMP or a timeout. | NT  |
|  8.4.8.3.1.2#2 | If a LDM TS Response LMP and LCW Delayed (DL)=0 is received, the Requester shall save timestamp t4 from the Local Time Source in the LDM Context to record the time that the LDM Response was received, then calculate the LDM Link Delay and set the LDM Valid flag to 1, and transition to the Timestamp Request state. | NT  |
|  8.4.8.3.1.2#3 | If a LDM TS Response LMP and LCW Delayed (DL)=1 is received, the Requester shall consider the Response Delay field of the LDM TS Response LMP invalid, invalidate the LDM Context t1, t2, and t3 timestamps, immediately generate a Trigger Event to initiate another Exchange, and transition to the Timestamp Request state. | NT  |
|  8.4.8.3.1.2#4 | If an Init Response Timeout occurs and the Init Response Timeout Counter is less than 3, then the Requester shall increment the Init Response Timeout Counter and transition to the Init Request state. | NT  |