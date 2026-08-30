Revision 1.1  
June 2022

- 224 -

Universal Serial Bus 3.2  
Specification

#### 8.4.8.3.2.1 Responder Disabled

This is the initial state of the Responder after power-up, Hot Reset, or Warm Reset.

Upon entering this state the Responder shall terminate all LDM protocol activity.

*LDM Enabled=0* – If *LDM Enabled* equals 0, then the Responder shall transition from any other LDM state to the **Responder Disabled** state.

*LDM Enabled=1* – If *LDM Enabled* equal 1, then the Responder shall transition to the **Timestamp Request** state.

#### 8.4.8.3.2.2 Timestamp Request

Upon entering this state, the Responder shall wait for a LDM TS Request LMP.

LDM TS Request LMP – If a LDM TS Request LMP is received, the Responder shall capture timestamp t2 from the PTM Local Time Source to record the time that the LDM TS Request was received and transition to the **Timestamp Response** state.

Note: Timestamp t2 shall be adjusted for the TS Delay. Refer to Section 8.4.8.6 for more information.

#### 8.4.8.3.2.3 Timestamp Response

Upon entering this state the Responder shall wait for a Trigger Event.

Trigger Event – When a Trigger Event occurs, the Responder shall capture timestamp t3 from the PTM Local Time Source to record the time that the LDM Response was transmitted. If the value t3 - t2 is less than tLDMResponseDelay, the Responder shall form a LDM TS Response LMP by initializing the *Response Delay* field with the value t3 - t2, transmit the LDM TS Response LMP to the Requester, and transition to the **Timestamp Request** state. If the value t3 - t2 is equal to or greater than tLDMResponseDelay, then the Responder shall transition to the **Timestamp Request** state.

A typical Trigger Event for the Responder **Timestamp Response** state would be the next opportunity to schedule a LDM TS Response LMP on its downstream link after a LDM TS Request LMP has been received.

Note: The Timestamp t3 shall be adjusted for the TS Delay. Refer to Section 8.4.8.6 for more information.

Note: A Responder shall set the *LCW Delayed* (DL) flag and re-calculate CRC-5 if a LDM TS Response LMP is delayed if its adjusted *Response Delay* value exceeds tLDMRequestTimeout. Refer to Section 8.4.8.6 for more information.

#### 8.4.8.4 LDM Link Delay

LDM defines the set of PTM capabilities which support the measurement of the LDM Link Delay.

**LDM Link Delay** identifies the delay between the first symbol of a packet being transmitted on a Responder's downstream facing port and the first symbol of the same packet being received on the Requester's upstream facing port. In a hub or device the LDM Link Delay is derived from Timestamp Exchanges with its upstream Responder.

A Requester may execute multiple Timestamp Exchanges to refine its LDM Link Delay value through averaging.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.