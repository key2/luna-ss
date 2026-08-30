Link Layer

### 7.5.4.6.1 Polling.PortConfig Requirements

- The operation of the 12-ms timer (tPollingLBPMLFPSTimeout) shall continue without reset upon entry to the substate from Polling.PortMatch.
- Upon entry to this state, the port shall place its transmitter in electrical idle if it is preparing its PHY re-configuration according to PHY Capability LBPM negotiated in Polling.PortMatch. The port shall perform the following PHY re-configuration.

1. The transmitter DC common mode voltage shall be within specification (VTX-CM-DCACTIVE-IDLE-DELTA) defined in Table 6-18.
2. The port shall maintain its low-impedance receiver termination (RRX-DC) defined in Table 6-21.
3. The port shall be ready to transmit TSEQ OS.
4. The port shall be ready to receive TSEQ OS for receiver equalization training.

- Upon completion of PHY re-configuration, the port shall transmit consecutive PHY Ready LBPMs to notify its link partner. Refer to Table 7-13 for PHY Ready LBPM definition.

### 7.5.4.6.2 Exit from Polling.PortConfig

- The port shall transition to Polling.RxEQ when four consecutive and matched PHY Ready LBPMs are sent after two consecutive and matched PHY Ready LBPMs are received.
- A downstream port shall transition to Rx.Detect upon the 12-ms timer timeout (tPollingLBPMLFPSTimeout) and cPollingTimeout is less than two.
- A downstream port shall transition to eSS.Inactive upon the 12-ms timer timeout (tPollingLBPMLFPSTimeout) and cPollingTimeout is two.
- An upstream port of a hub shall transition to Rx.Detect upon the 12-ms timer timeout (tPollingLBPMLFPSTimeout) and the conditions to transition to Polling.RxEQ are not met.
- A peripheral device shall transition to eSS.Disabled upon the 12-ms timer timeout (tPollingLBPMLFPSTimeout) and the conditions to transition to Polling.RxEQ are not met.
- A downstream port shall transition to eSS.Disabled when directed.
- A downstream port shall transition to Rx.Detect when directed to issue Warm Reset.
- An upstream port shall transition to Rx.Detect when Warm Reset is detected.

### 7.5.4.7 Polling.RxEQ

Polling.RxEQ is a substate for receiver equalization training. A port is required to complete its receiver equalization training.

### 7.5.4.7.1 Polling.RxEQ Requirements

- The detection and correction of the lane polarity inversion in SuperSpeed operation shall be enabled, as is described in Section 6.4.2.
- The port shall transmit the corresponding TSEQ ordered sets defined in Table 6-2.
- The port shall complete receiver equalizer training upon exit from this substate.

Note: A situation may exist where the port entering Polling.RxEQ earlier is transmitting TSEQ ordered sets while its link partner is still sending Polling.LFPS to satisfy the exit conditions from Polling.LFPS or Polling.LFPSPlus to Polling.RxEQ. In this situation, if its link partner is in electrical idle, near-end cross talk may cause the port to train its Rx equalizer using its own TSEQ ordered sets. To avoid a receiver from training itself, a port may either ignore the beginning part (about 30 μs) of the TSEQ ordered sets, or continue the equalizer training until it completes the transmission of TSEQ ordered sets.

7-61