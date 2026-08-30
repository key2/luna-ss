Universal Serial Bus 3.1 Specification

- A downstream port shall implement a counter (cPollingTimeout) to count the number of consecutive transition events from any Polling substate to Rx.Detect due to timeout. The operation of cPollingTimeout shall adhere to the following rules.

1. It shall be reset to zero upon any of the following conditions.

i. PowerOn Reset.
ii. Warm Reset on the upstream port.
iii. Upon exit to eSS.Disabled, or eSS.Inactive, or U0.
iv. Upon detection of the removal of far-end low-impedance receiver termination (R_RX-DC) defined in Table 6-21.

2. It shall be incremented by one or saturated at two if a transition to Rx.Detect is due to timeout in any of the Polling substates.

### 7.5.4.3 Polling.LFPS

Polling.LFPS is a substate designed to establish the PHY's DC operating point, and to synchronize the operations between the two link partners after exiting from Rx.Detect. This is also a substate for a port to identify itself based on various Polling.LFPS signatures.

#### 7.5.4.3.1 Polling.LFPS Requirements

- Upon entry, a LFPS receiver shall be enabled to receive the Polling.LFPS signals defined in Section 6.9.1.
- Upon entry, a port shall establish its LFPS operating condition within 80 μs.
- A downstream port shall disable its transition path to Compliance Mode upon PowerOn Reset or Warm Reset.
- A downstream port shall enable its transition path to Compliance Mode, if directed.
- An upstream port always has its transition path to Compliance Mode enabled upon PowerOn Reset.
- A port in SuperSpeed operation shall transmit Polling.LFPS.
- An upstream port in SuperSpeedPlus operation shall transmit SCD1 defined in Table 6-32. If no signature of SCD1 is found in sixteen consecutive Polling.LFPS received, the port shall switch to SuperSpeed operation and transmit Polling.LFPS instead of SCD1.
- A downstream port in SuperSpeedPlus operation shall transmit SCD1 defined in Table 6-32 if Compliance Mode is disabled. If no signature of SCD1 is found in sixteen consecutive Polling.LFPS received, the port shall switch to SuperSpeed operation and transmit Polling.LFPS instead of SCD1.
- A downstream port in SuperSpeedPlus operation shall transmit SCD2 if Compliance Mode is enabled.

Note: In case a retimer is connected to the downstream port, SCD2 is used for the retimer to enable Compliance Mode. Refer to Appendix E for details.

- A port in SuperSpeedPlus operation shall implement a 60-us timer (tPollingSCDLFPSTimeout) to monitor the absence of LFPS signal after the completion of SuperSpeed Polling.LFPS handshake.
- A port in SuperSpeedPlus operation shall be ready for SuperSpeed operation if it has detected that its link partner operates at SuperSpeed.

Note: There is no time allocated for a SuperSpeedPlus port to re-configure itself for SuperSpeed operation upon detection of its link partner operating at SuperSpeed. A SuperSpeedPlus port shall switch to SuperSpeed operation as quickly as possible for its

7-56