Revision 1.1
June 2022

- 112 -

Universal Serial Bus 3.2
Specification

Table 6-34. Lane-to-Lane Skew Requirements

[tbl-75.md](tbl-75.md)

Note: refer to Figure 6-6 for definition of the test points.

### 6.13.9 Compliance Patterns

Compliance patterns shall be transmitted independently on each lane.

- A Port shall transmit the same compliance pattern on all supported lanes. While in compliance mode, the transmitted compliance pattern shall advance for all supported lanes upon receiving a Ping.LFPS on either lane as defined in Section 6.4.4.
- CP0 and CP9 use the scrambler seeds defined in Section 6.13.5.
- All compliance patterns, including CP4, shall be transmitted on all lanes

### 6.13.10 Receiver Detection

Receiver termination detection is required on the Configuration Lane only.

The LTSSM flow for disconnect detection remains the same as for single-lane configurations.

### 6.13.11 Receiver Loopback

Receiver loopback for x2 operation is performed on a per lane basis.

All lanes shall exit from loopback upon receiving LFPS.

### 6.13.12 LFPS

LFPS signals are transmitted on the Configuration Lane only. This includes:

- Polling.LFPS (including SCD1 and SCD2)
- LBPM
- Ping.LFPS
- Warm Reset
- U1/U2/U3 exit
- Loopback exit

### 6.13.13 Ux Exit

While in U1/U2/U3, the port shall enable exit functionality in the receiver on the Configuration Lane.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.