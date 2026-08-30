Protocol Layer

In this state the LDM Protocol is enabled (LDM Enabled = 1); the local copy of the bus interval boundary is Invalid (LDM Valid = 0) and the Requester waits for a Trigger Event.

Trigger Event – When a Trigger Event occurs, the Requester shall transmit a LDM TS Request LMP to the Responder, save timestamp t1 from the Local Time Source in the LDM Context to record the time that the LDM Request was transmitted, and transition to the Init Response state.

A typical Trigger Event for the Requester Init Request state would be the transition of the device to the Address state.

### 8.4.8.3.1.2 Init Response

Upon entering this state, the Requester shall increment the Init Response Timeout Counter, start the Response Timer and wait for a TS Response LMP or a timeout.

LDM TS Response LMP & DL=0 – If a LDM TS Response LMP and LCW Delayed (DL) = 0 is received, the Requester shall save timestamp t4 from the Local Time Source in the LDM Context to record the time that the LDM Response was received, then calculate the LDM Link Delay (refer to Section 8.4.8.4) and set the LDM Valid flag to 1, and transition to the Timestamp Request state.

LDM TS Response LMP & DL=1 – If a LDM TS Response LMP and LCW Delayed (DL) = 1 is received, the Requester shall consider the Response Delay field of the LDM TS Response LMP invalid, invalidate the LDM Context t1, t2, and t3 timestamps, immediately generate a Trigger Event to initiate another Exchange, and transition to the Timestamp Request state. Refer to Sections 7.2.4.1.2 and 7.2.4.1.12 for the conditions that may set the Delayed bit.

Init Response Timeout(1-2) – If an Init Response Timeout (tLDMRequestTimeout) occurs and the Init Response Timeout Counter is less than 3, then the Requester shall increment the Init Response Timeout Counter and transition to the Init Request state.

Init Response Timeout(3) – If an Init Response Timeout occurs and the Init Response Timeout Counter is equal to 3, then the Requester shall transition to the LDM Disabled state

### 8.4.8.3.1.3 Timestamp Request

Upon entering this state, the Requester shall wait for a Trigger Event.

Trigger Event – When a Trigger Event occurs, the Requester shall transmit a LDM Timestamp (TS) Request LMP to the Responder, save timestamp t1 from the Local Time Source in the LDM Context to record the time that the LDM Request was transmitted, and transition to the Timestamp Response state.

A typical Trigger Event for the Requester Timestamp Request state would be to first transition to the Timestamp Request state, or execute an (averaging) algorithm to improve the accuracy of the Link Delay.

Note: Timestamp t1 shall be adjusted for the TS Delay. Refer to Section 8.4.8.6 for more information.

8-19