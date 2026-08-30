Revision 1.1
June 2022

- 157 -

Universal Serial Bus 3.2
Specification

[tbl-90.md](tbl-90.md)

### 7.4 PowerOn Reset and Inband Reset

There are two categories of reset associated with a link. The first, PowerOn Reset, restores storage elements, registers, or memories to predetermined states when power is applied. Upon PowerOn Reset, the LTSSM (described in Section 7.5) shall enter Rx.Detect. The second, Inband Reset, uses Enhanced SuperSpeed or LFPS signaling to propagate the reset across the link. There are two mechanisms to complete an Inband Reset, Hot Reset and Warm Reset. Upon completion of either a PowerOn Reset or an Inband Reset, the link shall transition to U0 as described in Section 7.4.2.

#### 7.4.1 PowerOn Reset

PowerOn Reset restores a storage element, register, or memory to a predetermined state when power is applied (refer to Section 9.1.1.2 for clarification of when power is applied for self-powered devices). A port must be responsible for its own internal Reset signaling and timing.

The following shall occur when PowerOn Reset is asserted or while VBUS is invalid:

1. Receiver termination shall meet the ZRX-HIGH-IMP-DC-POS specification defined in Table 6-22.
2. Transmitters shall hold a constant DC common mode voltage (VTX-DC-CM) defined in Table 6-18.

The following shall occur when PowerOn Reset is completed and VBUS is valid:

1. The LTSSM of a port shall be initialized to Rx.Detect. Note that an dual-lane capable port shall not enter Rx.Detect until the Configuration Lane is decided.
2. The LTSSM and the PHY level variables (such as Rx equalization settings) shall be reset to their default values.
3. The receiver termination of a port shall meet the RRX-DC specification defined in Table 6-22.

Note: Rx termination shall always be maintained throughout operation except for eSS.Disabled

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.