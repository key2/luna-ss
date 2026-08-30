Revision 1.1
June 2022

- 513 -

Universal Serial Bus 3.2
Specification

- The re-timer shall determine its port orientation towards a host downstream port or device upstream port.
- The re-timer shall decode U2 Inactivity timeout LMP from host, when acknowledged by device with ACK.
- A SRIS re-timer shall perform the clock offset compensation as defined in Section E.4.
- The re-timer shall not initiate entry to Recovery due to bit errors at its inbound traffic.
- The re-timer shall start a 1 ms timer (tU0RecoveryTimeout) to monitor the absence of link command at each port. This timer will be reset and restarted every time a link command is received. Note that a re-timer may lose receiver lock before the timer expires. Under this condition, a re-timer may transmit any scrambled idle symbols based its local scrambler. A bit-level re-timer may transmit idle symbols or TS1A OS with its local reference clock.

### E.3.7.2 Exit from U0

- The re-timer shall transition to U1 upon successful completion of LGO_U1 entry sequence. Refer to Section 7.2.4.2 for details.
- The re-timer shall transition to U2 upon successful completion of LGO_U2 entry sequence. Refer to Section 7.2.4.2 for details.
- The re-timer shall transition to U3 upon successful completion of LGO_U3 entry sequence. Refer to Section 7.2.4.2 for details.
- The re-timer shall transition to Recovery if either one of the following conditions is met.

- Upon observing TS1 OS, TS2 OS, TS1A OS, or TS1B OS.
- Upon timeout of the tU0RecoveryTimeout timer.

- The re-timer shall transition to Rx.Detect if Warm Reset is detected. Refer to Section E.3.1 for Warm Reset detection.

### E.3.8 U1

U1 is a low power state where no packets are observed and the re-timer is in a standby state.

### E.3.8.1 U1 Requirements

- The re-timer shall distinguish the received LFPS signal to determine if it is Ping.LFPS or U1 LFPS exit signal.
- The re-timer shall either forward or regenerate Ping.LFPS meeting the timing requirement defined in Table 6-30. Note that if a re-timer forwards Ping.LFPS, it shall be prepared that the received Ping.LFPS meet only the minimum Ping.LFPS timing requirement defined in Table 6-30. Any distortion introduced by the re-timer may lead to non-compliant Ping.LFPS.
- A captive re-timer shall perform the U1 LFPS exit handshake meeting the timing specification defined in Section 6.9.2. This is measured at the connector side.
- The re-timers in active cable shall initiate simultaneous U1 LFPS exit handshake at both sides of its connectors and meet the timing specification defined in Section 6.9.2. This is defined by re-timers performing the following operation.

- As LP2 defined in Section 6.9.2 responding to the U1 LFPS exit handshake.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.