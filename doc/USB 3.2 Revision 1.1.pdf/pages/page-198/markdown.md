Revision 1.1
June 2022

- 167 -

Universal Serial Bus 3.2
Specification

- The number of far-end receiver termination detection events shall be counted by an upstream port. The detection of far-end receiver termination is defined in Section 6.11.

Note: This count value is used by a peripheral device to determine when it needs to transition to eSS.Disabled. It is also used by a hub to control its downstream port state machine. Refer to Section 10.3.1.1 for details.

### 7.5.3.6 Exit from Rx.Detect.Active

- The port shall transition to Polling upon detection of a far-end low-impedance receiver termination (R$_{RX-DC}$) defined in Table 6-22. Note that for an upstream port capable of x2 operation, the far-end low-impedance receiver termination (R$_{RX-DC}$) is only presented on the Configuration Lane. Refer to Section 6.11.1 for details.
- A downstream port shall transition to Rx.Detect.Quiet when a far-end low-impedance receiver termination (R$_{RX-DC}$) defined in Table 6-22 is not detected.
- A downstream port shall transition to eSS.Disabled when directed.
- An upstream port of a hub shall transition to Rx.Detect.Quiet when a far-end low-impedance receiver termination (R$_{RX-DC}$) defined in Table 6-22 is not detected.
- An upstream port of a peripheral device shall transition to Rx.Detect.Quiet when the following two conditions are met:

1. A far-end low-impedance receiver termination (R$_{RX-DC}$) defined in Table 6-22 is not detected.
2. The number of far-end receiver termination detection events is less than eight.

- An upstream port of a peripheral device shall transition to eSS.Disabled when the following two conditions are met:

1. A far-end low-impedance receiver termination (R$_{RX-DC}$) defined in Table 6-22 is not detected.
2. The number of far-end receiver termination detection events has reached eight.

Note: This limit on the number of the far-end receiver termination detections is to allow an Enhanced SuperSpeed peripheral device on a legacy platform to transition to USB 2.0 after 80 ms.

### 7.5.3.7 Rx.Detect.Quiet

Rx.Detect.Quiet is a substate where a port has disabled its far-end receiver termination detection.

### 7.5.3.7.1 Rx.Detect.Quiet Requirements

- The far-end receiver termination detection shall be disabled.
- A downstream port shall start a timer (tRxDetectQuietTimeoutDFP) with a timeout between 12 ms and 120 ms upon entry to the substate.
- An upstream port shall start a timer (tRxDetectQuietTimeoutUFP) with a timeout of 12 ms upon entry to the substate.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.