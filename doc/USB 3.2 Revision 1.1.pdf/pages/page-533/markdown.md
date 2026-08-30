Revision 1.1
June 2022

- 502 -

Universal Serial Bus 3.2
Specification

○ Upon timeout of the tPollingSCDLFPSTimeout timer on either one of the ports.
- The re-timer shall transition to Polling.PortConfig if it has observed successful LBPM handshake for port match.
- The re-timer shall transition to Rx.Detect if one of the following conditions is met.
  ○ Warm Reset is detected.
  ○ The tPollingLBPMLFPSTimeout timer has expired.
  ○ The tPollingLFPSTimeout timer has expired and the conditions to transition to Polling.RxEQ or Polling.PortMatch are not met. Note that this condition also applies to the first tPollingLFPSTimeout timer timeout upon power-on.

### E.3.4.2 Polling.PortConfig

Polling.PortConfig is a substate for the re-timer to configure itself to the negotiated data. The operation of the re-timer is the same. It is also the substate for the re-timer to announce its presence if it is in x2 operation.

#### E.3.4.2.1 Mechanism for Re-timer Presence Announcement

The re-timer presence announcement applies to x2 operation only. The purpose of the re-timer presence announcement is for a port to determine the number of re-timers between the DFP and UFP such that a port adaptively determine the number of SKP OS to be inserted in Gen 2x2 operation. The re-timer presence announcement also provides a mechanism in future revisions where DFP may want to address a re-timer for purpose of performing capability discovery and configuration.

Figure E-8 illustrates the re-timer presence announcement during Polling.PortConfig where the DFP and UFP are exchanging the PHY Ready LBPM with bit 6 of the PHY Ready LBPM from the DFP asserted.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.