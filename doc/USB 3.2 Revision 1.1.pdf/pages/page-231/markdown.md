Revision 1.1
June 2022

- 200 -

Universal Serial Bus 3.2
Specification

### 7.5.11.2 Loopback Requirements

- There shall be one loopback master and one loopback slave. The loopback master is the port that has the Loopback bit asserted in TS2 ordered sets.
- The port shall maintain its transmitter specifications defined in Table 6-18.
- The port shall maintain its low-impedance receiver termination (R_RX-DC) defined in Table 6-22.
- In x2 operation, the loopback operation is performed on a per lane basis. The transmitter lane-to-lane skew does not need to be maintained.

### 7.5.11.3 Loopback.Active

Loopback.Active is a substate where the loopback test is active. The loopback master is sending data/commands to its loopback slave. The loopback slave is either looping back the data or detecting/executing the commands it received from the loopback master.

#### 7.5.11.3.1 Loopback.Active Requirements

- The loopback master shall send valid symbols with SKPs as necessary.
- In addition, in BLR Compliance Mode, the loopback master shall transmit four consecutive SKP OS if it is to advance the compliance pattern. Refer to Section E.3.6.1 for details.
- The loopback slave shall retransmit the received symbols.
- In Gen 1 operation, the loopback slave shall retransmit the received data in one of the following methods.

○ Loopback in the 10b domain – The loopback slave shall retransmit the received 10b symbols exactly as they were received. It may perform the lane polarity inversion and add or remove SKP OS for clock offset compensation as necessary.

Note: This implies that the loopback slave should disable or bypass its own 8b/10b encoder/decoder and scrambler/descrambler.

○ Loopback in the 8b domain – The loopback slave shall retransmit the decoded 8b symbols exactly as they were received. It shall replace any invalid 10b symbol with K28.4 and maintain the running disparity in its transmitter as describes in section 6.3.1. The loopback slave shall perform the lane polarity inversion and add or remove SKP OS for clock offset compensation as necessary.

Note: This implies that the retransmitted symbol may not have the same disparity as the symbol received. In addition, for the loopback master a single bit error will appear as a whole symbol error.

- In Gen 2 operation, the loopback slave shall retransmit all received blocks exactly as they were received without preforming any error corrections. It may perform the lane polarity inversion and add or remove SKP OS for clock offset compensation as necessary.

Note: This implies that the loopback slave should disable or bypass its own scrambler/descrambler.

- In Gen 1x1 operation, the loopback slave may process the BERT commands as defined in Section 0.

- The LFPS receiver shall be enabled. In x2 operation, the LFPS receiver shall be enabled on the Configuration Lane.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.