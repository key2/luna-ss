Revision 1.1
June 2022

- 74 -

Universal Serial Bus 3.2
Specification

[tbl-50.md](tbl-50.md)

Note: Unless otherwise noted, scrambling is disabled for compliance patterns.

### 6.4.4.1 Gen 2 Compliance Pattern CP9

The Gen 2 compliance pattern comprises a pseudo-random data pattern that is used to test transmitter and receiver compliance. The pattern repeats every 65536 symbols and starts with a SYNC Ordered Set so as to reset the scrambler and mark the beginning of the pattern.

Table 6-15. Gen 2 Compliance Pattern

[tbl-51.md](tbl-51.md)

### 6.5 Clock and Jitter

#### 6.5.1 Informative Jitter Budgeting

The jitter for USB 3.1 is budgeted among the components that comprise the end to end connections: the transmitter, channel (including packaging, connectors, and cables), and the receiver. The jitter budget is derived at the silicon pads. The Dj distribution is the dual Dirac method. Table 6-16 lists Tx, Rx, and channel jitter budgets. These budgets provide the basis for the normative transmitter jitter specifications defined in Section 6.7.3 and the receiver jitter tolerance specifications defined in Section 6.8.5.

Table 6-16. Informative Jitter Budgeting at the Silicon Pads⁷

[tbl-52.md](tbl-52.md)

Notes:

1. Rj is the sigma value assuming a Gaussian distribution.

2. Rj Total is computed as the Root Sum Square of the individual Rj components.

3. Dj budget is using the Dual Dirac method.

4. Tj at a 10⁻¹² BER is calculated as 14.068 * Rj + Dj.

5. The media budget includes the cancellation of ISI from the appropriate Rx equalization function.

6. Tx is measured after application of the JTF.

7. In this table, Tx jitter is defined at TP1, Rx jitter is defined at TP4, and media jitter is defined from TP1 to TP4.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.