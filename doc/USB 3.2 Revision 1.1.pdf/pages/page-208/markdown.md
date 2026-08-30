Revision 1.1
June 2022

- 177 -

Universal Serial Bus 3.2
Specification

#### **7.5.4.5.2 Polling.PortMatch Requirements**

- A 12 ms timer (tPollingLBPMLFPSTimeout) shall be started upon entry to the substate.
- Upon entry to this substate from Polling.LFPSPlus, the port shall transmit continuous PHY Capability LBPMs defined in Table 7-13 to announce its highest PHY Capability.
- Upon entry to this substate from Polling.Active, or Polling.Configuration, or Polling.Idle, the port shall transmit continuous PHY Capability LBPMs defined in Table 7-13 to announce its next highest PHY Capability from its previous PHY Capability.
- The port shall decode received PHY Capability LBPM or PHY Ready LBPM and compare to its own PHY Capability.
- The port with higher PHY capability shall adjust its PHY capability by transmitting PHY Capability LBPM that matches its link partner's.
- The port with lower PHY capability shall continue transmitting its own PHY Capability LBPMs and monitoring the PHY Capability LBPMs from its link partner.
- The two ports shall continue the interactive process of PHY Capability LBPM exchange as described above until they match the PHY Capability.

#### **7.5.4.5.3 Exit from Polling.PortMatch**

- The port shall transition to Polling.PortConfig when four consecutive and matched PHY Capability LBPMs are sent after two consecutive and matched PHY Capability LBPMs or PHY Ready LBPMs are received.
  Note: A port exiting from Polling.PortMatch and ready for PHY operation without re-configuration may immediately transmit PHY Ready LBPMs.
- A downstream port shall transition to Rx.Detect upon the 12 ms timer timeout (tPollingLBPMLFPSTimeout) and cPollingTimeout is less than two.
- A downstream port shall transition to eSS.Inactive upon the 12 ms timer timeout (tPollingLBPMLFPSTimeout) and cPollingTimeout is two.
- An upstream port of a hub shall transition to Rx.Detect upon the 12 ms timer timeout (tPollingLBPMLFPSTimeout) and the conditions to transition to Polling.PortConfig are not met.
- A peripheral device shall transition to eSS.Disabled upon the 12 ms timer timeout (tPollingLBPMLFPSTimeout) and the conditions to transition to Polling.PortConfig are not met.
- A downstream port shall transition to eSS.Disabled when directed.
- A downstream port shall transition to Rx.Detect when directed to issue Warm Reset.
- An upstream port shall transition to Rx.Detect when Warm Reset is detected.

#### **7.5.4.6 Polling.PortConfig**

Polling.PortConfig is a substate where a port configures itself according to PHY Capability LBPM matched in Polling.PortMatch, and synchronizes with its link partner in exiting from this substate to Polling.RxEQ. It is also a substate for re-timers in x2 operation to announce its presence. Refer to Appendix E for additional details.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.