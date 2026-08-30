Revision 1.1
June 2022

- 162 -

Universal Serial Bus 3.2
Specification

for details regarding the behavior of a peripheral device. Refer to Sections 10.3 to 10.6 for behaviors regarding a hub's upstream port and downstream port.

eSS.Disabled does not contain any substates in the case of downstream ports and hub upstream ports. For a peripheral upstream port, it contains two substates, eSS.Disabled.Default and eSS.Disabled.Error.

eSS.Disabled is also a logical power-off state for a self-powered hub upstream port.

eSS.Disabled.Default is also a logical power-off state for a self-powered peripheral upstream port.

A downstream port shall transition to this state from any other state when directed.

A self-powered hub or peripheral upstream port shall transition to this state when VBUS is not valid.

### 7.5.1.1 eSS.Disabled for Downstream Ports and Hub Upstream Ports

eSS.Disabled for Downstream Ports and Hub Upstream Ports does not contain any substates.

#### 7.5.1.1.1 eSS.Disabled Requirements

- VBUS may be present during eSS.Disabled.
- The port's receiver termination shall present high impedance to ground of ZRX-HIGH-IMP-DC-POS defined in Table 6-22.
- The port shall be disabled from transmitting and receiving LFPS and Enhanced SuperSpeed signals.

#### 7.5.1.1.2 Exit from eSS.Disabled

- A downstream port shall transition to Rx.Detect when directed.
- An upstream port shall transition to Rx.Detect only when VBUS transitions to valid or when directed.

### 7.5.1.2 eSS.Disabled for Upstream Ports of Peripheral Devices

eSS.Disabled of a peripheral device operates similarly to hub upstream ports, except that it only attempts a limited number of Enhanced SuperSpeed attempts upon USB 2.0 bus reset.

#### 7.5.1.2.1 eSS.Disabled Substate Machine

eSS.Disabled of a peripheral device has two substates shown in Figure 7-15.

- eSS.Disabled.Default
- eSS.Disabled.Error

eSS.Disabled.Default is a logical power-off state for a self-powered peripheral device.

#### 7.5.1.2.2 eSS.Disabled Requirements

The requirements of a peripheral upstream port are the same as defined in Section 7.5.1.1.1. In addition, a peripheral upstream port shall implement a tDisabledCount counter. The operation of the tDisabledCount counter shall meet the following requirement.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.