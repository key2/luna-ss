Revision 1.1
June 2022

- 515 -

Universal Serial Bus 3.2
Specification

- The re-timer shall transition to Rx.Detect if Polling.LFPS signal is detected.

### E.3.9 U2

U2 is a link state where more power saving is allowed for the re-timer as compared to U1, but with an increased exit latency. The operation of the re-timer is the same as is defined in LTSSM with a few exceptions that are described in the following subsections.

### E.3.9.1 U2 Requirements

- A captive re-timer shall perform the U2 LFPS exit handshake meeting the timing specification defined in Section 6.9.2. This is measured at the connector side.
- The re-timers in active cable shall initiate simultaneous U2 LFPS exit handshake at both sides of its connectors and meet the timing specification defined in Section 6.9.2. This is defined by re-timers performing the following operation.
  - As LP2 defined in Section 6.9.2 responding to the U2 LFPS exit handshake.
  - As LP1 defined in Section 6.9.2 initiating the U2 LFPS exit handshake within 2 ms at the other side of the connector upon detecting U2 LFPS exit signal.
- The re-timer shall distinguish between U2 LFPS exit handshake and Warm Reset based on specification defined in Section E.3.1.
- The re-timer shall be prepared to detect Polling.LFPS signal. This is a corner case where a device may be reconnected within a period so short that the re-timer is not able to declare a disconnect event.

### E.3.9.2 Exit from U2

- The re-timer shall transition to Recovery upon successful completion of a LFPS handshake meeting the U2 LFPS exit signaling defined in Section 6.9.2 and additional conditions defined in Section E.3.1.
- The re-timer shall transition to Rx.Detect if one of the following three conditions is met.
  - Upon detection of a far-end high-impedance receiver termination (ZRX-HIGH-IMP-DC-POS) defined in Table 6-22 and removal of the receiver termination at its own corresponding port mirroring the far-end receiver termination.
  - Upon detecting Warm Reset. Refer to Section E.3.1 for Warm Reset detection.
  - Upon the 2 ms LFPS handshake timer timeout (tNoLFPSResponseTimeout) and a successful LFPS handshake meeting the U2 LFPS exit handshake signaling in Section 6.9.2 is not achieved.
- The re-timer shall transition to Rx.Detect if Polling.LFPS signal is detected.

### E.3.10 U3

U3 is a link state where a device is put into a suspend state. Significant link and re-timer power can be saved. The re-timer operation is the same as is defined in LTSSM except that U3 LFPS exit is propagated.

### E.3.10.1 U3 Requirements

- The re-timer shall perform propagated U3 LFPS exit, rather than simultaneous U1/U2 LFPS exit. This is primarily due to the fact that a port may not be ready to respond in time, and attempt U3 LFPS exit when it is ready. The re-timer shall perform the following to facilitate the propagated U3 LFPS exit.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.