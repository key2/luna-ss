Revision 1.1
June 2022

- 498 -

Universal Serial Bus 3.2
Specification

### E.3.2 Rx.Detect

Rx.Detect is the default power-on state of the re-timer. The re-timer's responsibility is to detect the presence of its link partners by performing far-end receiver termination detection periodically and to mirror the presence status of its link partners. Rx.Detect also serves as an error state for the re-timer when an error situation is detected.

#### E.3.2.1 Rx.Detect Requirements

- The re-timer's receiver terminations at both ports shall present high impedance to ground of ZRX-HIGH-IMP-DC-POS defined in Table 6-22 upon power-on. Note that a re-timer may not have the knowledge to which port a host or a device is connected upon power-on.
- The re-timer shall preserve its original receiver termination if the transition to this state is due to an error event. Refer to transition conditions to eSS.Inactive in LTSSM.
- The re-timer shall initiate the far-end receiver termination detection at both ports upon entry to this state. It shall perform the far-end receiver termination detection at least every 8 ms. Note that this is to ensure the receiver termination from host DFP is propagated to a peripheral device before the peripheral device times out from Rx.Detect and transition to eSS.Disabled. Refer to Section 7.5.3 for behavior of a peripheral device in Rx.Detect.
- The re-timer, upon detecting far-end low-impedance receiver termination (RRX-DC) defined in Table 6-22, shall enable its low-impedance receiver termination (RRX-DC) at its respective port to mirror the presence of its link partner.
- The re-timer shall forward Polling.LFPS it may receive in this state and start monitoring the Polling.LFPS exit handshake if both of the following two conditions are met.

- The low-impedance receiver terminations (RRX-DC) are detected at both ports.
- The LFPS operating conditions are established at both ports.

- The re-timer shall start the tPollingLFPSTimeout timer upon receiving Polling.LFPS.
- The re-timer shall enable the transition path to Compliance Mode by default upon power-on.
- The re-timer shall conclude the far-end receiver termination detection at its port where Polling.LFPS is received and continue to perform the far-end receiver termination detection at its other port if Polling.LFPS is not received. A re-timer shall perform the following under this condition.

- Upon start of forwarding Polling.LFPS at one direction, it shall start a 24 ms timer to monitor the absence of the Polling.LFPS at its other direction.
- If the 24 ms timer times out and no Polling.LFPS is received, it shall terminate the Polling.LFPS forwarding and perform far-end receiver termination detection.

- If the far-end low-impedance receiver termination is removed, the re-timer shall propagate the receiver termination state by presenting high impedance to ground of ZRX-HIGH-IMP-DC-POS defined in Table 6-22, stop forwarding the Polling.LFPS signal and reset the tPollingLFPSTimeout timer. Note that this implies that a peripheral device may have transitioned to eSS.Disabled.
- If the far-end low-impedance receiver termination is detected, the re-timer shall resume forwarding the Polling.LFPS signal and restart the

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.