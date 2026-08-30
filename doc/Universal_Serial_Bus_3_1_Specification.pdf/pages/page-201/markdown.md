Physical Layer

Table 6-29. LFPS Transmitter Timing for SuperSpeed Designs¹

[tbl-83.md](tbl-83.md)

Notes:

1. If the transmission of an LFPS signal does not meet the specification, the receiver behavior is undefined.

2. Only Ping.LFPS has a requirement for minimum number of LFPS cycles.

3. The declaration of Ping.LFPS depends on only the Ping.LFPS burst.

4. Warm Reset, U1/U2/Loopback Exit, and U3 Wakeup are all single burst LFPS signals. tRepeat is not applicable.

5. The minimum duration of an LFPS burst shall be transmitted as specified. The LFPS handshake process and timing are defined in Section 6.9.2.

6. A Port in U2 or U3 is not required to keep its transmitter DC common mode voltage. When a port begins U2 exit or U3 wakeup, it may start sending LFPS signal while establishing its transmitter DC common mode voltage. To make sure its link partner receives a proper LFPS signal, a minimum of 80 μs tBurst shall be transmitted. The same consideration also applies to a port receiving LFPS U2 exit or U3 wakeup signal.

7. A port is still required to detect U1 LFPS exit signal at a minimum of 300ns. The extra 300ns is provided as the guard band for successful U1 LFPS exit handshake.

8. This requirement applies to SuperSpeed only designs (are only capable of operating at 5Gb/s).

9. This requirement applies to SuperSpeedPlus designs (capable of operating at 10Gb/s and higher speeds).

### IMPLEMENTATION NOTE

Detect and differentiate between Ping.LFPS and U1 LFPS exit signaling for a downstream port in U1 or U2

When a downstream port is in U1, it may receive either a Ping.LFPS as a message from its link partner to inform its presence, or an U1 LFPS exit signal to signal that its link partner is attempting exit from U1. This will also occur when a downstream port is in U2, since there are situations where a downstream port enters U2 from U1 when its U2 inactivity timer times out, and its link partner is still in U1.

Upon detecting the break of electrical idle due to receiving an LFPS signal, a downstream port may start a timer to measure the duration of the LFPS signal. If an electrical idle condition does not occur when the timer expires at 300 ns, a downstream port can declare the received LFPS signal is U1 exit and then respond to U1 exit by sending U1 LFPS exit handshake signal. If an electrical idle condition is detected before the timer reaches 300 ns, a downstream port can declare that the received LFPS signal is Ping.LFPS.

6-45