Revision 1.1
June 2022

- 538 -

Universal Serial Bus 3.2
Specification

There may be an optimal LRD placement. Placing an LRD very close to a transmitter should be avoided. In this case, the signal amplitude entering the LRD is very high and the output signal will be seriously compressed by the LRD such that the signal does not have enough strength to reach the receiver. It is up to system integrators to optimize the LRD location based their specific implementations.

### E.6.4.9 Electrical Over Stress Requirements

To ensure the electrical compatibility with an on-board host or device, the re-driver shall comply to the following transmitter and receiver requirements.

- It shall meet the instantaneous voltages (DC+AC) VTX-DC+AC_CONN as defined in Table 6-18. Note that the measurement of VTX-DC+AC_CONN is at the far side of the AC coupling capacitors. Refer to TBD LRD Compliance Program for VTX-DC+AC_CONN test configuration.
- It shall meet the instantaneous DC common mode voltage coupled to the far-end Tx VRX-CM-DC_CONN as defined in Table 6-23. Note that VRX-CM-DC_CONN requirement for re-driver is normative and is measured at the side of the AC cap associated with the far-end Tx. Refer to TBD LRD Compliance Program for VRX-CM-DC_CONN test configuration.

### E.7 Compliance

### E.7.1 Host and Device Product Compliance

Host and device products with re-timers shall meet the transmitter compliance requirements defined in Section 6.7.3 and the receiver jitter tolerance requirements defined in Section 6.8.5 of the base specification. During all host or device product compliance testing the re-timer shall be in the normal operation state (U0).

### E.7.2 Component-Level Re-timer Compliance

Re-timer products may also undergo component level compliance testing. The transmitter and receiver compliance requirements specified in Sections 6.7.3 and 6.8.5 apply to component level compliance testing. When undergoing component level compliance testing for the transmitter, the re-timer shall generate appropriate compliance patterns. When undergoing component level compliance testing for the receiver, the re-timer shall be placed into loopback mode.

### E.7.3 Component-Level LRD Conformance

The Re-driver for on-board applications may also undergo component level compliance test. The transmitter and receiver compliance requirements and the test environment are specified in Section E.6.4.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.