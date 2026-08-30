Universal Serial Bus 3.1 Specification

- An upstream port of a hub shall transition to Rx.Detect.Quiet when a far-end low-impedance receiver termination (R_RX-DC) defined in Table 6-21 is not detected.
- An upstream port of a peripheral device shall transition to Rx.Detect.Quiet when the following two conditions are met:

1. A far-end low-impedance receiver termination (R_RX-DC) defined in Table 6-21 is not detected.
2. The number of far-end receiver termination detection events is less than eight.

- An upstream port of a peripheral device shall transition to eSS.Disabled when the following two conditions are met:

1. A far-end low-impedance receiver termination (R_RX-DC) defined in Table 6-21 is not detected.
2. The number of far-end receiver termination detection events has reached eight.

Note: This limit on the number of the far-end receiver termination detections is to allow an Enhanced SuperSpeed peripheral device on a legacy platform to transition to USB 2.0 after 80 ms.

### 7.5.3.7 Rx.Detect.Quiet

Rx.Detect.Quiet is a substate where a port has disabled its far-end receiver termination detection.

#### 7.5.3.7.1 Rx.Detect.Quiet Requirements

- The far-end receiver termination detection shall be disabled.
- A downstream port shall start a timer (tRxDetectQuietTimeoutDFP) with a timeout between 12ms and 120ms upon entry to the substate.
- An upstream port shall start a timer (tRxDetectQuietTimeoutUFP) with a timeout of 12ms upon entry to the substate.

#### 7.5.3.7.2 Exit from Rx.Detect.Quiet

- A downstream port shall transition to Rx.Detect.Active upon the timeout of the tRxDetectQuietTimeoutDFP timer (12 ms to 120ms).
- An upstream port shall transition to Rx.Detect.Active upon the timeout of the tRxDetectQuietTimeoutUFP timer (12 ms).
- A downstream port shall transition to eSS.Disabled when directed.

7-54