Revision 1.1
June 2022

- 505 -

Universal Serial Bus 3.2
Specification

**E.3.4.3.2 Exit from Polling.RxEQ**

- The re-timer shall transition to Polling.TSx once it has transmitted the number of TSEQ OS defined in Section 6.4.
- The re-timer shall transition to Rx.Detect if Warm Reset is detected.

**E.3.4.4 Polling.TSx**

Polling.TSx is a substate where the re-timer tracks the TS1/TS2 OS to achieve end to end symbol/block alignment. This is also a substate for bit-level re-timers to perform sequential clock and OS switching.

**E.3.4.4.1 Mechanism of the Sequential Clock Switching for Cascaded Bit-Level Re-timer**

The bit-level re-timer architecture and its specific operation mechanism is defined to only support Gen 1x1 operation.

Sequential clock switching refers to a mechanism of clock switching in the ordered progression from the last re-timer to the leading re-timer, where multiple bit-level re-timers are cascaded between the host and device. This is illustrated in Figure E-9. In the simplex link from the host to device, RT4 is the last re-timer, and its preceding re-timer is RT3. RT1 is leading re-timer, and its following re-timer is RT2. Similarly in the opposite simplex link from the device to host, RT1 is the last re-timer, and its preceding re-timer is RT2. RT4 is the leading re-timer, and its following re-timer is RT3. The clock switching process is described in this section.

In the simplex link from host to device, the last bit-level re-timer RT4 will first perform its clock switching from its local transmit clock that has SSC disabled to the recovered clock from RT3 that also has SSC disabled. Because SSC are both disabled, RT4 only needs to achieve the receiver bit/symbol lock and perform the clock switching within 600-ppm, thus facilitating fast and robust clock switching. After RT4 completes its clock switching, RT3 will switch from its local clock to the recovered clock from RT2. Since RT4 is tracking RT3's clock, once RT3 completes its clock switching, RT4 is tracking RT2's clock through RT3. This process continues until RT1 completes its clock switching, and RT4 is now tracking RT1's clock through RT3 and RT2. Note that RT1 is switching from its local clock with SSC disabled to recovered clock from the host that has SSC enabled.

In the opposite simplex link from the device to host, the same clock switching process from RT1 to RT4 is performed simultaneously.

Once a bit-level re-timer completes clock switching at both simplex links, it will perform the OS switching to complete its clock and OS switching.

Note that this operation also applies to bit-level re-timers when in Recovery.TSx.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.