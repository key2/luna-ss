|  7.5.4.5.3#4 | An upstream port of a hub shall transition to Rx.Detect upon the tPollingLBPMLFPSTimeout and the conditions to transition to Polling.PortConfig are not met. | NT  |
| --- | --- | --- |
|  7.5.4.5.3#5 | A peripheral device shall transition to eSS.Disabled upon the tPollingLBPMLFPSTimeout and the conditions to transition to Polling.PortConfig are not met. | NT  |
|  7.5.4.5.3#6 | A downstream port shall transition to Rx.Detect when directed to issue Warm Reset. | BC  |
|  7.5.4.5.3#7 | An upstream port shall transition to Rx.Detect when a Warm Reset is detected. | BC  |
|  Subsection reference: 7.5.4.6 Polling.PortConfig  |   |   |
|  Subsection reference: 7.5.4.6.1 Polling.PortConfig Requirements  |   |   |
|  7.5.4.6.1#1 | The operation of the tPollingLBPMLFPSTimeout shall continue without reset upon entry to this substate from Polling.PortMatch. | BC  |
|  7.5.4.6.1#2 | Upon entry to this state, the port shall place its transmitter in electrical idle if it is preparing its PHY re-configuration according to PHY Capability LBPM negotiated in Polling.PortMatch. | BC  |
|  7.5.4.6.1#3 | The port shall perform the following PHY re-configuration: - The transmitter DC voltage shall be within specification. - The port shall maintain its low-impedence receiver terminations. - The port shall be ready to transmit TSEQ OS. - The port shall be ready to receive TSEQ OS for receiver equalization training. | BC  |
|  7.5.4.6.1#4 | Upon completion of PHY re-configuration, the port shall transmit consecutive PHY Ready LBPMs to notify its link partner. | 7.1  |
|  Subsection reference: 7.5.4.6.2 Exit from Polling.PortConfig  |   |   |
|  7.5.4.6.2#1 | The port shall transition to Polling.RxEQ when four consecutive and matched PHY Ready LBPMs are sent after two consecutive and matched PHY Ready LBPMs are received. | 7.1  |
|  7.5.4.6.2#2 | A downstream port shall transition to Rx.Detect upon the tPollingLBPMLFPSTimeout and cPollingTimeout is less than two. | NT  |
|  7.5.4.6.2#3 | A downstream port shall transition to eSS.Inactive upon the tPollingLBPMLFPSTimeout and cPollingTimeout is two. | NT  |
|  7.5.4.6.2#4 | An upstream port of a hub shall transition to Rx.Detect upon the tPollingLBPMLFPSTimeout and the conditions to transition to Polling.PortConfig are not met. | NT  |