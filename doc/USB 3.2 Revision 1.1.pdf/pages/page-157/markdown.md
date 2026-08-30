Revision 1.1
June 2022

- 126 -

Universal Serial Bus 3.2
Specification

LCRD_x and LCRD1_x/LCRD2_x use an explicit alphabetical index. The index A, B, C, D, A, B, C... (Gen 1x1, Gen 1x2 or Gen 2x1), or A, B, C, D, E, F, G, A, B, C... (Gen 2x2) is advanced by one with each header packet being processed and an Rx Header Buffer Credit is available. The index is used to ensure Rx Header Buffer Credits are received in order such that missing of an LCRD_x or LCRD1_x/LCRD2_x can be detected. The index operation of LCRD1_x and LCRD2_x are independent.

LBAD and LRTY do not use indexes.

LGO_U1, LGO_U2, LGO_U3, LAU, LXU, and LPMA are link commands used for link power management.

LDN and LUP are special link commands used by a downstream port and an upstream port to indicate their port presence in U0. The usage of LDN and LUP is described in Table 7-5.

Additional requirements and examples on the use of link commands are found in Section 7.2.4.

Table 7-5. Link Command Definitions

[tbl-81.md](tbl-81.md)

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.