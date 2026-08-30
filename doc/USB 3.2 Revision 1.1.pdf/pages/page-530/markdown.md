Revision 1.1
June 2022

- 499 -

Universal Serial Bus 3.2
Specification

24 ms timer. Note that this may be due to a temporary receiver termination mismatch between re-timers and their link partners, or due to the next transition path to Compliance Mode, or an error case. Note also that the tPollingLFPSTimeout timer shall continue while performing the far-end receiver termination detection.

- The re-timer shall forward and decode Warm Reset it may receive. The re-timer shall ensure the duration of forwarded Warm Reset meets the timing requirement defined in Section 6.9.3. Refer to Section E.3.1 for details. Note that the re-timer may also assign the port receiving Warm Reset as USP, and the port transmitting Warm Reset as DSP.

### E.3.2.2 Exit from Rx.Detect

- A re-timer shall transition to Polling if Polling.LFPS is received at both ports.
- The re-timer shall enter Compliance Mode upon the first timeout of the tPollingLFPSTimeout timer after power-on.

### E.3.3 eSS.Disabled

eSS.Disabled is an optional state where no eSS activity is enabled. The re-timer is at its lowest possible power state. Note that there is no defined mechanism for entry to and exit from eSS.Disabled. It is the responsibility of the implementation to manage eSS.Disabled based on its capabilities.

### E.3.3.1 eSS.Disabled Requirements

- The re-timer shall present high impedance to ground of ZRX-HIGH-IMP-DC-POS defined in Table 6-22 at both ports.
- The re-timer shall be in its lowest power state.

### E.3.3.2 Exit from eSS.Disabled

- The re-timer shall transition to Rx.Detect upon direction.

### E.3.4 Polling

Polling is a state for the re-timer to participate in speed negotiation, link training and to determine the state of operation upon exit from Polling. A simplified re-timer Polling substate machine is shown in Figure E-7. Note that the transition to Rx.Detect due to Warm Reset is not shown.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.