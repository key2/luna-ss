Revision 1.1
June 2022

- 193 -

Universal Serial Bus 3.2
Specification

U3 does not contain any substates. Transitions to other states are shown in Figure 7-24.

#### 7.5.9.1 U3 Requirements

- The transmitter DC common mode voltage does not need to be within specification (VTX-CM-DC-ACTIVE-IDLE-DELTA) defined in Table 6-19 on each negotiated lane.
- The port shall maintain its low-impedance receiver termination (R$_{RX-DC}$) defined in Table 6-22. If the port is in x2 operation, it shall enable its low-impedance receiver termination (R$_{RX-DC}$) on the each negotiated lane.
- LFPS Ping detection shall be disabled.
- The port shall enable its U3 wakeup detect functionality as defined in Section 6.9.2. If the port is in x2 operation, it shall enable this functionality on the Configuration Lane.
- The port shall enable its LFPS transmitter when it initiates the exit from U3. If the port is in x2 operation, it shall initiate the exit from U3 on the Configuration Lane.
- A downstream port shall perform the far-end receiver termination detection every 100 ms (tU3RxdetDelay). Note that in x2 operation, a downstream port shall perform the far-end receiver termination detection on the Configuration Lane.
- The port not able to respond to U3 LFPS wakeup within tNoLFPSResponseTimeout may initiate U3 LFPS wakeup when it is ready to return to U0.

#### 7.5.9.2 Exit from U3

- A downstream port shall transition to eSS.Disabled when directed.
- A downstream port shall transition to Rx.Detect upon detection of a far-end high-impedance receiver termination (Z$_{RX-HIGH-IMP-DC-POS}$) defined in Table 6-22.
- A downstream port shall transition to Rx.Detect when directed to issue Warm Reset.
- An upstream port shall transition to Rx.Detect when Warm Reset is detected.
- A self-powered upstream port shall transition to eSS.Disabled upon not detecting valid VBUS as defined in Section 11.4.5.
- The port shall transition to Recovery upon successful completion of a LFPS handshake meeting the U3 wakeup signaling defined in Section 6.9.2.
- The port shall remain in U3 when the 10 ms LFPS handshake timer times out (tNoLFPSResponseTimeout) and a successful LFPS handshake meeting the U3 wakeup handshake signaling in Section 6.9.2 is not achieved. 100 ms (tU3WakeupRetryDelay) after an unsuccessful LFPS handshake and the requirement to exit U3 still exists, then the port shall initiate the U3 wakeup LFPS Handshake signaling to wake up the host.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.