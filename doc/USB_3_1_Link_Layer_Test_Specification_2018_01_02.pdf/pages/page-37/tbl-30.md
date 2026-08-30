|   | • Twenty Polling.LFPS bursts are transmitted, after finding no SCD2 is detected. |   |
| --- | --- | --- |
|  7.5.4.4.2#3 | A downstream port shall transition to Rx.Detect upon the 360ms timeout detected and cPollingTimeout is less than two. | NT  |
|  7.5.4.4.2#4 | A downstream port shall transition to eSS.Inactive upon the 360ms timeout detected and cPollingTimeout is two. | NT  |
|  7.5.4.4.2#5 | An upstream port of a hub shall transition to Rx.Detect upon the 360ms timeout. | NT  |
|  7.5.4.4.2#6 | An peripheral device shall transition to eSS.Disabled upon the 360ms timeout. | NT  |
|  7.5.4.4.2#7 | A downstream port shall transition to Rx.Detect when directed to issue Warm Reset. | BC  |
|  7.5.4.4.2#8 | An upstream port shall transition to Rx.Detect when a Warm Reset is detected. | BC  |
|  Subsection reference: 7.5.4.5 Polling.PortMatch  |   |   |
|  Subsection reference: 7.5.4.5.2 Polling.PortMatch Requirements  |   |   |
|  7.5.4.5.2#1 | Upon entry to this substate from Polling.LFPSPlus, the port shall transmit continuous PHY Capability LBPMs to announce its highest PHY capability. | BC  |
|  7.5.4.5.2#2 | Upon entry to this substate from Polling.Active or Polling.Configuration or Polling.Idle, the port shall transmit continuous PHY Capability LBPMs to announce its next highest PHY capability from its previous PHY Capability. | 7.39  |
|  7.5.4.5.2#3 | A port shall decode received PHY Capability LBPM or PHY Ready LBPM and compare to its own PHY Capability. | BC  |
|  7.5.4.5.2#4 | The port with higher PHY capability shall adjust its PHY capability by transmitting PHY Capability LBPM that matches its link partner's. | NT  |
|  7.5.4.5.2#5 | The port with lower PHY capability shall continue transmitting its own PHY Capability LBPMs and monitoring the PHY Capability LBPMs from its link partner. | NT  |
|  Subsection reference: 7.5.4.5.3 Exit from Polling.PortMatch  |   |   |
|  7.5.4.5.3#1 | The port shall transition to Polling.PortConfig when four consecutive and matched PHY Capability LBPMs are sent after two consecutive and matched PHY Capability LBPMs or PHY Ready LBPMs are received. | BC  |
|  7.5.4.5.3#2 | A downstream port shall transition to Rx.Detect upon the tPollingLBPMLFPSTimeout and cPollingTimeout is less than two. | NT  |
|  7.5.4.5.3#3 | A downstream port shall transition to eSS.Inactive upon the tPollingLBPMLFPSTimeout and cPollingTimeout is two. | NT  |