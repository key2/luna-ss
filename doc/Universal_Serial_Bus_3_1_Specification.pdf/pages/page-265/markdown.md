Link Layer

### 7.5.3.3 Rx.Detect.Reset

Rx.Detect.Reset is a substate designed for the two ports to synchronize their operations on Warm Reset. In this substate, a downstream port shall generate Warm Reset when directed. If an upstream port enters Rx.Detect upon detection of Warm Reset, it shall remain in this substate until the completion of Warm Reset.

For a port entering Rx.Detect not due to a Warm Reset, it shall exit immediately.

#### 7.5.3.3.1 Rx.Detect.Reset Requirements

If a port enters Rx.Detect upon a Warm Reset, the following requirements shall be applied. Refer to Section 6.9.3 for details.

- A downstream port shall transmit Warm Reset for the duration of tReset as defined in Table 6-29.

Note: This includes the case when Hot Reset attempt fails in Recovery. Refer to Section 7.4.2 for details.

- An upstream port shall remain in this state until it detects the completion of Warm Reset.

#### 7.5.3.3.2 Exit from Rx.Detect.Reset

- The port shall transition directly to Rx.Detect.Active if the entry to Rx.Detect is not due to a Warm Reset.

Note: Warm Reset is not present during power-on.

- A downstream port shall transition to Rx.Detect.Active after it transmits Warm Reset for the duration of tReset as defined in Table 6-29.

- A downstream port shall transition to eSS.Disabled when directed.

- An upstream port shall transition to Rx.Detect.Active when it receives no more LFPS Warm Reset signaling from the downstream port as defined in Section 6.9.3.

### 7.5.3.4 Rx.Detect.Active

Rx.Detect.Active is a substate to detect the presence of an Enhanced SuperSpeed link partner. A port will perform a far-end receiver termination detection as defined in Section 6.11.

### 7.5.3.5 Rx.Detect.Active Requirements

- The transmitter shall initiate a far-end receiver termination detection described in Section 6.11.

- The number of far-end receiver termination detection events shall be counted by an upstream port. The detection of far-end receiver termination is defined in Section 6.11.

Note: This count value is used by a peripheral device to determine when it needs to transition to eSS.Disabled. It is also used by a hub to control its downstream port state machine. Refer to Section 10.3.1.1 for details.

### 7.5.3.6 Exit from Rx.Detect.Active

- The port shall transition to Polling upon detection of a far-end low-impedance receiver termination ($R_{RX-DC}$) defined in Table 6-21.

- A downstream port shall transition to Rx.Detect.Quiet when a far-end low-impedance receiver termination ($R_{RX-DC}$) defined in Table 6-21 is not detected.

- A downstream port shall transition to eSS.Disabled when directed.

7-53