Revision 1.1
June 2022

- 169 -

Universal Serial Bus 3.2
Specification

- Polling.Active
- Polling.Configuration
- Polling.Idle

### 7.5.4.2 Polling Requirements

- The port shall maintain its low-impedance receiver termination (R_RX-DC) defined in Table 6-22.
- A downstream port shall implement a counter (cPollingTimeout) to count the number of consecutive transition events from any Polling substate to Rx.Detect due to timeout. The operation of cPollingTimeout shall adhere to the following rules.

1. It shall be reset to zero upon any of the following conditions.

a. PowerOn Reset.
b. Warm Reset on the port.
c. Upon exit to eSS.Disabled, or eSS.Inactive, or U0.
d. Upon detection of the removal of far-end low-impedance receiver termination (R_RX-DC) defined in Table 6-22.

2. It shall be incremented by one or saturated at two if a transition to Rx.Detect is due to timeout in any of the Polling substates.

### 7.5.4.3 Polling.LFPS

Polling.LFPS is a substate designed to establish the PHY's DC operating point for LFPS operation, and to synchronize the operation between the two link partners after exiting from Rx.Detect. This is also a substate for a port to identify itself based on various Polling.LFPS signatures. In x2 operation, the LFPS operation is performed on the Configuration Lane.

#### 7.5.4.3.1 Polling.LFPS Requirements

- Upon entry, an LFPS receiver shall be enabled to receive the Polling.LFPS signals defined in Section 6.9.1.
- Upon entry, a port shall establish its LFPS operating condition within 80 µs.
- A downstream port shall disable its transition path to Compliance Mode upon PowerOn Reset or Warm Reset.
- A downstream port shall enable its transition path to Compliance Mode, if directed.
- An upstream port shall always have its transition path to Compliance Mode enabled upon PowerOn Reset.
- A port in SuperSpeed operation shall transmit Polling.LFPS.
- An upstream port in SuperSpeedPlus operation shall transmit SCD1 defined in Table 6-33. It shall perform in one of the following ways if no signature of SCD1 or SCD2 is detected within the received Polling.LFPS bursts.

1. If it has received sixteen or more consecutive Polling.LFPS bursts and the tPollingSCDLFPSTimeout timer has not expired, it shall switch to SuperSpeed operation and transmit Polling.LFPS with non-varying tRepeat after four SCD1 are transmitted.

Note: This may imply that its SuperSpeed link partner may not recognize the Polling.LFPS burst in SCD1 due to varying tRepeat.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.