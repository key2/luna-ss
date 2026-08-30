Revision 1.1
June 2022

- 190 -

Universal Serial Bus 3.2
Specification

- If the port has not received a Port Capability LMP within tPortConfiguration time, a downstream port shall be directed to transition to eSS.Inactive and an upstream port shall be directed to transition to eSS.Disabled.
- A downstream port shall transition to Recovery upon not receiving any link commands within 1 ms (tU0RecoveryTimeout).

Note: Not receiving any link commands including LUP within 1 ms implies either a link is under serious error condition, or an upstream port has been removed. To accommodate for both situations, a downstream port will transition to Recovery and attempt to retrain the link. If the retraining fails, it will then transition to eSS.Inactive. During eSS.Inactive, a downstream port will attempt a far-end receiver termination detection. If it determines that a far-end low-impedance receiver termination (R_RX-DC) defined in Table 6-22 is not present, it will enter Rx.Detect. Otherwise, it will wait for software intervention.

- An upstream port shall transition to Recovery if it does not receive any link command or any packet (as specified in Section 7.2.4.1.4) within 1 ms (tU0RecoveryTimeout).
- A downstream port shall transition to Rx.Detect when directed to issue Warm Reset.
- An upstream port shall transition to Rx.Detect when Warm Reset is detected.
- An upstream port shall transition to eSS.Disabled upon detection of VBUS off.

Note: this condition only applies to a self-powered upstream port. eSS.Disabled is a logical power-off state for a self-powered upstream port.

### 7.5.7 U1

U1 is a low power state where no packets are to be transmitted and both ports agree to enter a link state where an Enhanced SuperSpeed PHY can be placed into a low power state.

U1 does not contain any substates. Transitions to other states are shown in Figure 7-22.

### 7.5.7.1 U1 Requirements

- The transmitter DC common mode voltage shall be within specification (V_TX-CM-DC-ACTIVE-IDLE-DELTA) defined in Table 6-19 on each negotiated lane.
- The port shall maintain its low-impedance receiver termination (R_RX-DC) defined in Table 6-22. If the port is in x2 operation, it shall enable its low-impedance receiver termination (R_RX-DC) on each negotiated lane.
- The port shall enable its U1 exit detect functionality as defined in Section 6.9.2. If the port is in x2 operation, it shall enable this functionality on the Configuration Lane.
- The port shall enable its LFPS transmitter when it initiates the exit from U1. If the port is in x2 operation, it shall initiate the exit from U1 on the Configuration Lane.
- The port shall enable its U2 inactivity timer upon entry to this state if the U2 inactivity timer has a non-zero timeout value.
- A downstream port shall enable its Ping.LFPS detection. If the port is in x2 operation, it shall enable its Ping.LFPS detection on the Configuration Lane.
- A downstream port shall enable a 300 ms timer (tU1PingTimeout). This timer will be reset and restarted when a Ping.LFPS is received.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.