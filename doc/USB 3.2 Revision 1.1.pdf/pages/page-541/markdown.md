Revision 1.1
June 2022

- 510 -

Universal Serial Bus 3.2
Specification

○ For SSP operation, it shall perform the clock offset compensation as defined in Section 6.4.3.
- A bit-level re-timer shall perform its link training and complete its clock and OS switching based on Section E.3.4.4.1.
- The re-timer in SSP operation shall monitor and forward LBPMs upon detection. Note that this situation may happen when the host or device fail the training and timeout to Polling.PortMatch to re-negotiate the next link speed.
- The re-timer shall start the tPollingActiveTimeout timer upon entry to this substate. This timer shall be reset and disabled upon observing successful exit handshake from Polling.Active. Note that the re-timer shall also disable this timer and progress forward if it has observed TS2 OS from both ports but has not observed a successful TS1 OS exit handshake. This may be a corner case where a decoding error could happen within the re-timer.
- The re-timer shall start the tPollingConfigurationTimeout timer upon observing TS2 OS at both ports. Note that a host and device may not exit from Polling.Active simultaneously. For re-timers, observing TS2 OS at both ports is an indication that both the host and device have entered Polling.Configuration.

##### E.3.4.4.3 Exit from Polling.TSx

- The re-timer shall transition to Polling.Idle upon observing successful TS2 handshake.
- The re-timer in SSP operation shall disable its eSS transceivers and transition to Polling.SpeedDetect if either one of the following conditions is met.
  ○ Upon the expiration of the tPollingActiveTimeout timer and no successful TS1 OS handshakes have been observed.
  ○ Upon the expiration of the tPollingConfigurationTimeout timer and no successful TS2 OS handshakes have been observed.
  ○ LBPM is detected at both ports.
- The re-timer in SS operation shall disable its SS transceivers and transition to Rx.Detect if either one of the following two conditions is met.
  ○ Upon the expiration of the tPollingActiveTimeout timer and no successful TS1 OS handshake has been observed.
  ○ Upon the expiration of the tPollingConfigurationTimeout timer and no successful TS2 OS handshake has been observed.
- The re-timer shall transition to Rx.Detect if Warm Reset is detected.

##### E.3.4.5 Polling.Idle

Polling.Idle is a substate where the re-timer decodes TS2 OS and determines its next operation state.

##### E.3.4.5.1 Polling.Idle Requirements

- The re-timer shall decode the link configuration field in TS2 OS and configure itself to the corresponding operation state.
- The re-timer in SSP operation shall monitor and forward LBPMs upon detection.
- The re-timer shall start the tPollingIdleTimeout timer to monitor the progression of LTSSM.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.