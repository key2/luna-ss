intel®

## 7.1 PHY Registers

Table 7-1 lists the PHY registers and their associated address. The details of each register are provided in the following subsections.

To support configurable pairs, the same registers defined for RX1 are also defined for RX2, the same registers defined for TX1 are defined for TX2, and the same registers defined for CMN1 are defined for CMN2. Only two differential pairs are active at a time based on configuration; valid combinations correspond to registers defined in RX1+TX1+CMN1, RX1+RX2+CMN1+CMN2, or TX1+TX2+CMN1+CMN2.

A PHY that does not support configurable pairs only implements registers defined for RX1, TX1, and CMN1.

Table 7-1. PHY Registers (Sheet 1 of 2)

[tbl-60.md](tbl-60.md)

80

Reference Number: 643108, Revision: 7.1