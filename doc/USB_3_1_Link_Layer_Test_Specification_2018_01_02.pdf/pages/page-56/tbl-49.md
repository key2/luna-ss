|  8.4.8.3.1.2# 5 | If an Init Response Timeout occurs and the Init Response Timeout Counter is equal to 3, then the Requester shall transition to the LDM Disabled state. | NT  |
| --- | --- | --- |
|  Subsection reference: 8.4.8.3.1.3 Timestamp Request  |   |   |
|  8.4.8.3.1.3# 1 | Upon entering this state, the Requester shall wait for a Trigger Event. | NT  |
|  8.4.8.3.1.3# 2 | When a trigger event occurs, the Requester shall transmit a LDM Timestamp (TS) Request LMP to the Responder, save timestamp t1 from the Local Time Source in the LDM Context to record the time that the LDM Request was transmitted, and transition to the Timestamp Response state. | NT  |
|  8.4.8.3.1.3# 3 | Timestamp t1 shall be adjusted for the TS Delay. | NT  |
|  Subsection reference: 8.4.8.3.1.4 Timestamp Response  |   |   |
|  8.4.8.3.1.4# 1 | Upon entering this state, the Requester shall start the Response Timer and wait for a LDM TS Response LMP or a timeout. | NT  |
|  8.4.8.3.1.4# 2 | If a LDM TS Response LMP is received and the LCW Delayed (DL) flag is zero, the Requester shall save timestamp t4 from the Local Time Source in the LDM Context to record the time that the LDM Response was received, then calculate the LDM Link Delay, set the LDM Valid flag to 1, and transition to the Timestamp Request state. | NT  |
|  8.4.8.3.1.4# 3 | If a LDM TS Response LMP is received and the LCW Delayed (DL) flag is one, the Requester shall consider the Response Delay field of the LDM TS Response LMP invalid, invalidate the LDM Context t1, t2, and t3 timestamps, immediately generate a Trigger Event to initiate another Timestamp Exchange, and transition to the Timestamp Request state. | NT  |
|  8.4.8.3.1.4# 4 | If a Response Timeout occurs the Requester shall transition to the Init Request state, where the LDM state machine will attempt to retry the Timestamp Exchange with the Responder. | NT  |
|  8.4.8.3.1.4# 5 | Timestamp t4 shall be adjusted for the TS Delay. | NT  |
|  Subsection reference: 8.4.8.3.1.5 LDM Disabled  |   |   |
|  8.4.8.3.1.5# 1 | Upon entering this state, the Requester shall clear the LDM_ENABLE flag and terminate all LDM protocol activity. | NT  |
|  8.4.8.3.1.5# 2 | When the device receives a CLEAR_FEATURE(LDM_ENABLE) request it shall transition from any other LDM state to the LDM Disabled state. | NT  |
|  8.4.8.3.1.5# 3 | When the device receives a SET_FEATURE(LDM_ENABLE) request it shall transition to the Init Request state. | NT  |
|  Subsection reference: 8.4.8.3.2 Responder Operation  |   |   |