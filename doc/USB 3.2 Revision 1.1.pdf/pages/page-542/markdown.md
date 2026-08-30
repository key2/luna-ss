Revision 1.1
June 2022

- 511 -

Universal Serial Bus 3.2
Specification

# E.3.4.5.2 Exit from Polling.Idle

- The re-timer shall transition to U0 if either one of the following conditions is met.

o Successful idle symbol handshake is observed.
o A link command is observed.

- The re-timer shall transition to PassThrough Loopback if the Loopback bit (bit 2) in the link configuration field is asserted and the Compliance bit (bit 5) in the link configuration field is de-asserted.

- The re-timer shall transition to BLR Compliance Mode if the Loopback bit (bit 2) in the link configuration field and the Compliance bit (bit 5) in the link configuration field are both asserted.

- The re-timer shall transition to Local Loopback as the loopback slave if the re-timer loopback bit (bit 4 in the link configuration field) is asserted. Note that it is illegal to have both bit4 and bit 2 asserted. If both bits are asserted, the re-timer shall give priority to PassThrough Loopback.

- The re-timer shall transition to Hot Reset if the Reset bit is asserted.

- The re-timer in SSP operation shall disable its eSS transceivers and transition to Polling.SpeedDetect if either one of the following two conditions is met.

o Upon the expiration of the tPollingIdleTimeout timer and no successful idle symbol handshake has been observed.
o LBPMs is detected at both of its ports.

- The re-timer in SS operation shall disable its SS transceivers and transition to Rx.Detect upon the expiration of the tPollingIdleTimeout timer and no successful idle symbol handshake has been observed.

- The re-timer shall transition to Rx.Detect if Warm Reset is detected.

# E.3.5 Compliance Mode

Compliance Mode is to test re-timer's transmitter characteristics based on a local reference clock.

# E.3.5.1 Compliance Mode Requirements

- Upon entry to the substate, the re-timer shall transmit CP0 on its transmitter. An x2 capable re-timer shall meet the additional scrambler seed requirement on each lane as defined in Section 6.13.5.

- An x2 re-timer shall monitor the LFPS signal at its Configuration Lane.

o If the received signal is Ping.LFPS, it shall advance the compliance pattern accordingly. An x2 capable re-timer shall advance the compliance pattern on both lanes.
o If the received signal is WarmReset, it shall conclude the compliance test

- The re-timer shall monitor the LFPS signal at both ports. Note that the re-timer may receive Ping.LFPS at the port in the compliance test, or WarmReset at either port if the compliance test is concluded.

- The re-timer shall configure the port not receiving Polling.LFPS in Rx.Detect for the transmitter compliance test and keep the transmitter at its port receiving Polling.LFPS in electrical idle.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.