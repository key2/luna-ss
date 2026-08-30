Revision 1.1
June 2022

- 514 -

Universal Serial Bus 3.2
Specification

○ As LP1 defined in Section 6.9.2 initiating the U1 LFPS exit handshake within 500 ns at the other side of the connector upon detecting U1 LFPS exit signal.

• A re-timer may receive Polling.LFPS from a host while in U1. This is a corner case where a host may declare device disconnect earlier than a re-timer. Before a re-timer declares device disconnect, a host may transition from U1 to Rx.Detect declaring a new event of device connect, and subsequently transition to Polling transmitting Polling.LFPS signal. A re-timer shall perform one of the following.

○ If a re-timer forwards LFPS signal in U1 and determines that it is Polling.LFPS, it shall stop forwarding the LFPS signal, and transition to Rx.Detect.
○ If a re-timer performing simultaneous U1 LFPS exit treats the LFPS burst of the first Polling.LFPS signal as U1 LFPS exit signal from LP1, it may initiate simultaneous U1 LFPS exit towards device as LP1, while acknowledging to host with U1 LFPS exit handshake as LP2. It shall be expected that its UFP LTSSM may be in Recovery, and its DFP LTSSM still in U1. If it has determined the received LFPS signal is Polling.LFPS, it shall transition to Rx.Detect.

• The re-timer shall distinguish between U1 LFPS exit handshake and Warm Reset based on specification defined in Section E.3.1.

• The re-timer shall enable an U2 inactivity timer upon entry to this state if the U2 inactivity timer has a non-zero timeout value between 0x01H and 0xFEH. It shall set its timeout value to be at least 500 μs more than the value defined in the U2 inactivity timeout LMP. Note this is to make sure that re-timer remains in U1 until the device has entered U2 and no Ping.LFPS is to be transmitted. Refer to Section 10.6.1 for PM timer accuracy requirement.

• The re-timer shall enable a 300 ms timer (tU1PingTimeout). This timer will be reset and restarted when a Ping.LFPS is received.

• In x2 operation, the transmitter DC common mode voltage of the non-Configuration Lane shall be also within specification (VTX-CM-DC-ACTIVE-IDLE-DELTA) defined in Table 6-19 on each both lanes. The receiver's low-impedance receiver termination (RRX-DC) defined in Table 6-22 shall also be maintained on the non-Configuration Lane.

### E.3.8.2 Exit from U1

• The re-timer shall transition to Recovery upon successful completion of a LFPS handshake meeting the U1 LFPS exit handshake signaling in Section 6.9.2 and additional conditions defined in Section E.3.1.
• The re-timer shall transition to U2 upon the timeout of the U2 inactivity timer.
• The re-timer shall transition to Rx.Detect if one of the following three conditions is met.

○ Upon the 300 ms timer (tU1PingTimeout) expiration and removal of the receiver termination at its own corresponding port mirroring the far-end receiver termination.
○ Upon detecting Warm Reset. Refer to Section E.3.1 for Warm Reset detection.
○ Upon the 2 ms LFPS handshake timer timeout (tNoLFPSResponseTimeout) and a successful LFPS handshake meeting the U1 LFPS exit handshake signaling in Section 6.9.2 is not achieved.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.