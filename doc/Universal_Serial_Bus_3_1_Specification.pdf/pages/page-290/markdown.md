Universal Serial Bus 3.1 Specification

### 7.5.11.2 Loopback Requirements

- There shall be one loopback master and one loopback slave. The loopback master is the port that has the Loopback bit asserted in TS2 ordered sets.
- The port shall maintain its transmitter specifications defined in Table 6-17.
- The port shall maintain its low-impedance receiver termination (R_RX-DC) defined in Table 6-21.

### 7.5.11.3 Loopback.Active

Loopback.Active is a substate where the loopback test is active. The loopback master is sending data/commands to its loopback slave. The loopback slave is either looping back the data or detecting/executing the commands it received from the loopback master.

#### 7.5.11.3.1 Loopback.Active Requirements

- The loopback master shall send valid symbols with SKPs as necessary.
- The loopback slave shall retransmit the received symbols.
- The loopback slave shall not modify the received symbols, other than lane polarity inversion if necessary, and SKP ordered set, which may be added or dropped as required.

Note: For SuperSpeed operation this implies that the loopback slave should disable or bypass its own 8b/10b encoder/decoder and scrambler/descrambler. For SuperSpeedPlus operation this implies that the loopback slave should disable or bypass its own scrambler/descrambler.

- The loopback slave must process the BERT commands as defined in Section 6.8.4.
- The LFPS receiver shall be enabled.

#### 7.5.11.3.2 Exit from Loopback.Active

- A downstream port shall transition to eSS.Disabled when directed.
- A downstream port shall transition to Rx.Detect when directed to issue Warm Reset.
- An upstream port shall transition to Rx.Detect when Warm Reset is detected.
- When directed, the loopback master shall transition to Loopback.Exit.
- The loopback slave shall transition to Loopback.Exit upon detection of Loopback LFPS exit handshake signal meeting Loopback LFPS exit signaling defined in Section 6.9.2.

### 7.5.11.4 Loopback.Exit

Loopback.Exit is a substate where a loopback master has completed the loopback test and starts the exit from Loopback.

#### 7.5.11.4.1 Loopback.Exit Requirements

- A 2-ms timer (tLoopbackExitTimeout) shall be started upon entry to the substate.
- The LFPS transmitter and the LFPS receiver shall be enabled.
- The port shall transmit and receive Loopback LFPS exit handshake signal defined in Section 6.9.2.

#### 7.5.11.4.2 Exit from Loopback.Exit

- The port shall transition to Rx.Detect upon a successful Loopback LFPS exit handshake defined in Section 6.9.2.
- The port shall transition to eSS.Inactive upon the 2-ms timer timeout (tLoopbackExitTimeout) and the condition to transition to Rx.Detect is not met.
- A downstream port shall transition to eSS.Disabled when directed.
- A downstream port shall transition to Rx.Detect when directed to issue Warm Reset.

7-78