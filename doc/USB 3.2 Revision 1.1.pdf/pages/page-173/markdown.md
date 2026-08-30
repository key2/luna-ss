Revision 1.1
June 2022

- 142 -

Universal Serial Bus 3.2
Specification

Table 7-7. Transmitter Timers Summary

[tbl-84.md](tbl-84.md)

Note 1: The timeout value also includes the propagation delays introduced by a long active cable, and additional re-timers that maybe on a host and/or a device side. It is important to realize that any delay of the link command return by a port receiving HP may result in throughput performance degradation.

- A port in SS operation, upon receiving HP, shall return its correspondent LGOOD_n or LBAD within 3.0us. Note that this delay is based on the worst case scenario of a DP with maximum DPP payload being just transmitted. In this case, a port has to wait until the current DP is transmitted, followed by SKP OS and the preceding link commands.
- A port in SSP operation, upon receiving HP, shall return its correspondent LGOOD_n or LBAD within 1.5us. Note that this delay is based on the worst case scenario of a DP with maximum DPP payload being just transmitted. In this case, a port has to wait until the current DP is transmitted, followed by SKP OS and the preceding link commands.
- A port, upon receiving the link command, shall complete the link command processing within 200ns

Note 2: The relaxation of the timeout value is to allow some low cost implementation at a performance penalty of staling its link partner.

### 7.2.4.2 Link Power Management and Flow

Requests to transition to low power link states are done at the link level during U0. Link commands LGO_U1, LGO_U2, and LGO_U3 are sent by a port as a request to enter a low power link state. LAU or LXU is sent by the other port as the response. LPMA is sent by a port in response only to LAU. Details on exit/wake from a low power link state are described in Sections 7.5.7, 7.5.8, and 7.5.9.

#### 7.2.4.2.1 Power Management Link Timers

A port shall have three timers for link power management. First, a PM_LC_TIMER is used for a port initiating an entry request to a low power link state. It is designed to ensure a prompt entry to a low power link state. Second, a PM_ENTRY_TIMER is used for a port accepting the entry request to a low power link state. It is designed to ensure that both ports across the link are in the same low power link state regardless if the LAU or LPMA is lost or corrupted. Finally, a Ux_EXIT_TIMER is used for a port to initiate the exit from U1 or U2. It is specified to ensure that the duration of U1 or U2 exit is bounded and the latency of a header packet transmission is not compromised. The timeout values of the three timers are specified in Table 7-8.

A port shall operate the PM_LC_TIMER based on the following rules:

- A port requesting a low power link state entry shall start PM_LC_TIMER after the last symbol of the LGO_Ux link command is sent.
- A port requesting a low power link state entry shall disable and reset PM_LC_TIMER upon receipt of the last symbol of LAU or LXU at its receiver.

A port shall operate the PM_ENTRY_TIMER based on the following rules:

- A port accepting the request to enter a low power link state shall start PM_ENTRY_TIMER after the last symbol of LAU is sent.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.