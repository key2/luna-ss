|  8.4.8.3.2#1 | The LDM Responder State Machine shall maintain the local variable Responder Response Delay Overflow. | NT  |
| --- | --- | --- |
|  Subsection reference: 8.4.8.3.2.1 Responder Disabled  |   |   |
|  8.4.8.3.2.1#1 | Upon entering this state the Responder shall terminate all LDM protocol activity. | NT  |
|  8.4.8.3.2.1#2 | If LDM Enabled equals 0, then the Responder shall transition from any other LDM state to the Responder Disabled state. | NT  |
|  8.4.8.3.2.1#2 | If LDM Enabled equals 1, then the Responder shall transition to the Timestamp Request state. | NT  |
|  Subsection reference: 8.4.8.3.2.2 Timestamp Request  |   |   |
|  8.4.8.3.2.2#1 | Upon entering this state the Responder shall wait for a LDM TS Request LMP. | NT  |
|  8.4.8.3.2.2#2 | If a LDM TS Request LMP is received, the Responder shall capture timestamp t2 from the PTM Local Time Source to record the time that the LDM TS Request was received and transition to the Timestamp Response state. | NT  |
|  8.4.8.3.2.2#3 | Timestampe t2 shall be adjusted for the TS Delay. | NT  |
|  Subsection reference: 8.4.8.3.2.3 Timestamp Response  |   |   |
|  8.4.8.3.2.3#1 | Upon entering this state the Responder shall wait for a Trigger Event. | NT  |
|  8.4.8.3.2.3#2 | When a Trigger Event occurs, the Responder shall capture timestamp t3 from the PTM Local Time Source to record the time that the LDM Response was transmitted. | NT  |
|  8.4.8.3.2.3#3 | If the value t3 – t2 is less than tLDMResponseDelay, the Responder shall form a LDM TS Response LMP by initializing the Response Delay field with the value t3 – t2, transmit the LDM TS Response LMP to the Requester, and transition to the Timestamp Request state. | NT  |
|  8.4.8.3.2.3#4 | If the value t3 – t2 is equal to or greater than tLDMResponseDelay, then the Responder shall transition to the Timestamp Request state. | NT  |
|  8.4.8.3.2.3#5 | The timestamp t3 shall be adjusted for the TS Delay. | NT  |
|  8.4.8.3.2.3#6 | A Responder shall set the LCW Delayed (DL) flag and re-calculate CRC-5 if a LDM TS Response LMP is delayed if its adjusted Response Delay value exceeds tLDMRequestTimeout. | NT  |
|  Subsection reference: 8.4.8.5 PTM Bus Interval Boundary Device Calculation  |   |   |
|  8.4.8.5#1 | If Delta(RxITP) is greater than or equal to 7500, the device shall ignore the ITP. | NT  |