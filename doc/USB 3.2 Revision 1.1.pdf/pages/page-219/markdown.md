Revision 1.1
June 2022

- 188 -

Universal Serial Bus 3.2
Specification

### 7.5.5.1 Compliance Mode Requirements

- The port shall maintain its low-impedance receiver termination (R_RX-DC) defined in Table 6-22.
- The LFPS receiver is used to control the test pattern sequencing.
- Upon entry to Compliance Mode, the port shall wait until its eSS Tx DC common mode voltage meets the V_TX-DC-CM specification defined in Table 6-19 before it starts to send the first compliance test pattern defined in Table 6-14.
- In x2 operation, the port shall transmit the compliance test patterns on each negotiated lane independently.
- The port shall transmit the next compliance test pattern continuously upon detection of a Ping.LFPS as defined in Section 6.9.1. Note that in x2 operation, the port shall monitor Ping.LFPS on the Configuration Lane only.
- The port shall transmit the first compliance test pattern continuously upon detection of a Ping.LFPS and the test pattern has reached the final test pattern.

### 7.5.5.2 Exit from Compliance Mode

- A downstream port shall transition to Rx.Detect when directed to issue Warm Reset.
- An upstream port shall transition to Rx.Detect upon detection of Warm Reset.
- A downstream port shall transition to eSS.Disabled when directed.

### 7.5.6 U0

U0 is the normal operational state where packets can be transmitted and received. U0 does not contain any substate machines.

### 7.5.6.1 U0 Requirements

- The port shall meet the transmitter specifications defined in Table 6-18.
- The port shall maintain the low-impedance receiver termination (R_RX-DC) defined in Table 6-22.
- The LFPS receiver shall be enabled.
- The port shall enable a 1 ms timer (tU0RecoveryTimeout) to measure the time interval between two consecutive link commands. This timer will be reset and restarted every time a link command is received.
- The port shall enable a 10 μs timer (tU0LTimeout). This timer shall be reset when the first symbol of any link command or packet is sent and restarted after the last symbol of any link command or packet is sent. This timer shall be active when the link is in logical idle.
- A downstream port shall transmit a single LDN when the 10 μs timer (tU0LTimeout) expires.
- An upstream port shall transmit a single LUP when the 10 μs timer (tU0LTimeout) expires.
- A port shall acknowledge the received header packet with either LGOOD_n or LBAD within the HP response time (tDHPResponse). This is measured at a port's connector from when the first bit of HP is received to when the first bit of either LGOOD_n or LBAD is transmitted. If a re-timer is used with the port receiving HP, the HP response time shall account for the additional delay of the re-timer.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.