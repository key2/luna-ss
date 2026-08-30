Revision 1.1
June 2022

- 101 -

Universal Serial Bus 3.2
Specification

[tbl-71.md](tbl-71.md)

Notes:

1. If the transmission of an LFPS signal does not meet the specification, the receiver behavior is undefined.
2. Only Ping.LFPS has a requirement for minimum number of LFPS cycles.
3. The declaration of Ping.LFPS depends on only the Ping.LFPS burst.
4. Warm Reset, U1/U2/Loopback Exit, and U3 Wakeup are all single burst LFPS signals. tRepeat is not applicable.
5. The minimum duration of an LFPS burst shall be transmitted as specified. The LFPS handshake process and timing are defined in Section 6.9.2.
6. A Port in U2 or U3 is not required to keep its transmitter DC common mode voltage. A port in U2 or U3 is not required to keep its transmitter DC common mode voltage but must not exceed the VTX-CM-IDLE-DELTA spec at TP1. This can be met by either managing the magnitude of the CM shift or the slew rate of the shift. Accordingly, LFPS detectors must tolerate positive and negative CM excursions up to VTX-CM-IDLE-DELTA without false detection. When a port begins U2 exit or U3 wakeup, it may start sending LFPS signal while establishing its transmitter DC common mode voltage. To make sure its link partner receives a proper LFPS signal, a minimum of 80 μs tBurst shall be transmitted. The same consideration also applies to a port receiving LFPS U2 exit or U3 wakeup signal.
7. A port is still required to detect U1 LFPS exit signal at a minimum of 300ns. The extra 300ns is provided as the guard band for successful U1 LFPS exit handshake.
8. This requirement applies to Gen 1x1 only designs.
9. This requirement applies to Gen 1x2, Gen 2x1 and Gen 2x2 designs.

### IMPLEMENTATION NOTE

Detect and differentiate between Ping.LFPS and U1 LFPS exit signaling for a downstream port in U1 or U2

When a downstream port is in U1, it may receive either a Ping.LFPS as a message from its link partner to inform its presence, or an U1 LFPS exit signal to signal that its link partner is attempting exit from U1. This will also occur when a downstream port is in U2, since there are situations where a downstream port enters U2 from U1 when its U2 inactivity timer times out, and its link partner is still in U1.

Upon detecting the break of electrical idle due to receiving an LFPS signal, a downstream port may start a timer to measure the duration of the LFPS signal. If an electrical idle condition does not occur when the timer expires at 300 ns, a downstream port can declare the received LFPS signal is U1 exit and then respond to U1 exit by sending U1 LFPS exit handshake signal. If an electrical idle condition is detected before the timer reaches 300 ns, a downstream port can declare that the received LFPS signal is Ping.LFPS.

### 6.9.2 Example LFPS Handshake for U1/U2 Exit, Loopback Exit, and U3 Wakeup

The LFPS signal used for U1/U2 exit, Loopback exit, and U3 wakeup is defined the same as continuous LFPS signals with the exception of timeout values defined in Table 6-31. The handshake process for U1/U2 exit and U3 wakeup is illustrated in Figure 6-33. The timing requirements are different for U1 exit, U2 exit, Loopback exit, and U3 wakeup. They are listed in Table 6-31.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.