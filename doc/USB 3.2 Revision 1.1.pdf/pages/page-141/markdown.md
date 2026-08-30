Revision 1.1  
June 2022

- 110 -

Universal Serial Bus 3.2  
Specification

### 6.11.3 Upper Limit on Channel Capacitance

The interconnect total capacitance to ground seen by the Receiver Detection circuit shall not exceed 3 nF to ground, including capacitance added by attached test instrumentation. This limit is needed to guarantee proper operation during Receiver detect. Note that this capacitance is separate and distinct from the AC coupling capacitance value.

### 6.12 Re-timers

Requirements for re-timers are defined in Appendix E.

### 6.13 Dual-lane Requirements

#### 6.13.1 Operation

Dual-lane operation refers to Gen 1x2 or Gen 2x2 operation. In x2 operation, connect detect and the start-up speed negotiation are performed only on a single lane referred to as the Configuration Lane. Refer to the USB Type-C Specification for identification of the Configuration Lane between the DFP and UFP.

Note that the preceding requirements pertain to implementations using USB Type-C cables and connectors. For other implementations, the method for determining the Configuration Lane is implementation specific.

#### 6.13.2 Capability Determination

x2 capability is determined during Polling.PortMatch based on the PHY Capability LBPM described in Table 7-14 of Section 7.5.4.5.1.

#### 6.13.3 Lane Numbering

Lane 0 shall be mapped to the Configuration Lane.

#### 6.13.4 Data Striping

Data blocks shall be striped. Data striping is aligned to Lane 0, an example of which is shown in Figure 6-40.

Control blocks shall be duplicated on both lanes, and are therefore not striped.

Transmission of packets and link commands including framing symbols may be initiated on either lane. Example: transmission of the last byte of a data packet on Lane 0, and the first byte of a subsequent packet or link command on Lane 1.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.