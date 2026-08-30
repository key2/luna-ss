Revision 1.1
June 2022

- 127 -

Universal Serial Bus 3.2
Specification

[tbl-82.md](tbl-82.md)

### 7.2.2.3 Link Command Placement

The link command placement shall meet the following rules:

- Link commands shall not be placed inside header packet structures (i.e., within LMPs, TPs, ITPs, or DPHs).
- Link commands shall not be placed within the DPP of a DP structure.
- Link commands shall not be placed between the DPH and the DPP.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.