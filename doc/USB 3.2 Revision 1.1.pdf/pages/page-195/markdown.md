Revision 1.1
June 2022

- 164 -

Universal Serial Bus 3.2
Specification

absence of a far-end receiver termination (R_RX-DC) specified in Table 6-22, or upon a Warm Reset. An upstream port can only exit to Rx.Detect upon a Warm Reset, or upon detecting an absence of a far-end receiver termination (R_RX-DC) specified in Table 6-22.

During eSS.Inactive, a port periodically performs a far-end receiver termination detection. If a disconnection is detected, a port will return to Rx.Detect. If a disconnect is not detected, the link will stay in eSS.Inactive until software intervention.

### 7.5.2.1 eSS.Inactive Substate Machines

eSS.Inactive contains the following substate machines shown in Figure 7-16:

- eSS.Inactive.Disconnect.Detect
- eSS.Inactive.Quiet

### 7.5.2.2 eSS.Inactive Requirements

- VBUS shall be present.
- The receiver termination in single-lane operation shall meet the requirement (R_RX-DC) specified in Table 6-22.
- The receiver termination of the Configuration Lane in x2 operation shall meet the requirement (R_RX-DC) specified in Table 6-22.
- The transmitter common mode is not required to be within specification during this state.

### 7.5.2.3 eSS.Inactive.Quiet

eSS.Inactive.Quiet is a substate defined in which a port has disabled its far-end receiver termination detection so that extra power can be saved while waiting for software intervention.

#### 7.5.2.3.1 eSS.Inactive.Quiet Requirements

- The function of the far-end receiver termination detection shall be disabled.
- A 12 ms timer (teSSInactiveQuietTimeout) shall be started upon entry to the substate.

#### 7.5.2.3.2 Exit from eSS.Inactive.Quiet

- The port shall transition to eSS.Inactive.Disconnect.Detect upon the 12 ms timer timeout (teSSInactiveQuietTimeout).
- A downstream port shall transition to eSS.Disabled when directed.
- A downstream port shall transition to Rx.Detect when Warm Reset is issued.
- An upstream port shall transition to Rx.Detect upon detection of Warm Reset.

### 7.5.2.4 eSS.Inactive.Disconnect.Detect

eSS.Inactive.Disconnect.Detect is a substate in which a port will perform the far-end receiver termination detection in order to determine if its link partner is disconnected during eSS.Inactive, or if the transition to eSS.Inactive is due to a disconnect from its link partner.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.