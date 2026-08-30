Revision 1.1
June 2022

- 504 -

Universal Serial Bus 3.2
Specification

- The re-timer shall monitor and forward the received LBPMs until a successful handshake is reached. Note that the forwarded LBPMs shall meet the electrical and timing requirements defined in Section 6.9.
- The re-timer shall start the tPollingLBPMLFPSTimeout timer upon entry to this substate.
- In x2 operation, the re-timer shall participate the re-timer presence announcement defined in Section E.3.4.2.1. A re-timer shall announce its presence by forwarding the received PHY Ready LBPM with bits [4:2] incremented by one. Note that the re-timer may determine the source of the PHY Ready LBPM based on bit 6. Refer to Table 7-13 for details.
- In x2 operation, after completing the re-timer presence announcement, the re-timer shall perform one of the following based on bit 7 of the PHY Ready LBPM from the DFP.
  - If it is asserted, it shall reset the tPollingLBPMLFPSTimeout timer, remain in this substate, forward the received LBPM message as is including the PHY Ready LBPM, and continue to monitor the PHY Ready LBPM handshake. Note that re-timer may observe LFPS electrical idle during the operation. The re-timer may store and forward one LBPM.
  - If it is de-asserted, it shall participate the PHY Ready LBPM handshake and prepare to exit to Polling.RxEQ.
- In x2 operation, the re-timer shall start a 60 µs LFPS EI timer to monitor the absence of LFPS after observing the successful PHY Ready LBPM handshake.

### E.3.4.2.3 Exit from Polling.PortConfig

- In single-lane operation, the re-timer shall transition Polling.RxEQ if it has observed successful PHY Ready LBPM handshake.
- In x2 operation, the re-timer shall transition Polling.RxEQ if it has observed successful PHY Ready LBPM handshake with bit-7 of the PHY Ready LBPM from DFP de-asserted and the 60 µs LFPS EI timer has expired.
- The re-timer shall transition to Rx.Detect if one of the following conditions is met.
  - Warm Reset is detected.
  - The tPollingLBPMLFPSTimeout timer has expired.

### E.3.4.3 Polling.RxEQ

Polling.RxEQ is a substate for eSS receiver equalization training. The training mechanism is the same as defined in LTSSM except the exit criteria.

### E.3.4.3.1 Polling.RxEQ Requirements

- The lane polarity detection and correction for SS operation shall be enabled.
- The re-timer shall transmit the number of TSEQ ordered set (OS) defined in Section 6.4 while performing its receiver equalization training and clock data recovery.
- The re-timer shall be ready for TS1 OS detection upon completion of its receiver equalization training.
- A bit-level re-timer shall transmit TSEQ OS with its transmitter meeting the electrical and timing requirements defined in Chapter 6. Note that a bit-level re-timer shall have its SSC disabled while transmitting TSEQ OS.
- The re-timer shall forward the LFPS signal it has detected.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.