Revision 1.1
June 2022

- 518 -

Universal Serial Bus 3.2
Specification

○ If switching from the received TS1 OS, it shall complete the clock switching within 140 μs. Note that a bit-level re-timer may monitor the clock offset between the recovered clock and its local reference clock, and attempt to perform the clock switching when the clock offset is small. A bit-level re-timer shall expect that the frequency range of a host or device is either within +300ppm to -5300ppm, or within -1700ppm to -5300ppm if a RF-friendly SSC profile is employed. It is desired that a bit-level re-timer to monitor the recovered clock and determine its frequency range before setting the clock switching point.

○ If switching from the received TS1A OS or TS1B OS, it shall complete the clock switching within 10 μs. Note that TS1A/TS1B OS do not contain SSC.
○ Upon completing the clock switching at both simplex links, a bit-level re-timer shall complete the OS switching within two OS interval.

• The re-timer shall start the tRecoveryActiveTimeout timer upon entry to this substate. The tRecoveryActiveTimeout timer shall be reset and disabled upon observing successful exit handshake.

• The re-timer shall start the tRecoveryConfigurationTimeout timer upon observing TS2 OS at both ports. Note that a host and device may not exit from Recovery.Active simultaneously. For re-timers, observing TS2 OS at both ports is an indication that both the host and device have entered Recovery.configuration.

### E.3.11.3 Recovery.Idle

Recovery.Idle is a substate where re-timers decode TS2 OS and decide the next operation state.

### E.3.11.3.1 Recovery.Idle Requirements

• The re-timer shall decode the link configuration field in TS2 OS and configure itself to the corresponding operation state.
• The re-timer shall start the tRecoveryIdleTimeout timer to monitor the progression of LTSSM.

### E.3.11.3.2 Exit from Recovery.Idle

• The re-timer shall transition to U0 if either one of the following conditions is met.

○ Successful idle symbol handshake is observed.
○ A link command is observed.

• The re-timer shall transition to PassThrough Loopback if the Loopback bit (bit 2) in the link configuration field is asserted and the Compliance bit (bit 5) in the link configuration field is de-asserted.
• The re-timer shall transition to BLR Compliance Mode if the Loopback bit (bit 2) in the link configuration field and the Compliance bit (bit 5) in the link configuration field are both asserted.
• The re-timer shall transition to Local Loopback as the loopback slave if the re-timer loopback bit (bit 4 in the link configuration field) is asserted. Note that it is illegal to have both bit 4 and bit 2 asserted. If both bits are asserted, the re-timer shall give priority to PassThrough Loopback.
• The re-timer shall transition to Hot Reset if the Reset bit is asserted.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.