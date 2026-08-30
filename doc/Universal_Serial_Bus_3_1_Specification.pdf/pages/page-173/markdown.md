Physical Layer

Table 6-6. Gen 2 TS1 Ordered Set

[tbl-59.md](tbl-59.md)

Table 6-7. Gen 2 TS2 Ordered Set

[tbl-60.md](tbl-60.md)

Table 6-8. Gen 2 TSEQ Ordered Set

[tbl-61.md](tbl-61.md)

Table 6-9. Gen 2 SYNC Ordered Set

[tbl-62.md](tbl-62.md)

Table 6-10. SDS Ordered Set

[tbl-63.md](tbl-63.md)

### 6.4.1.2.3 Training Control Bits for Gen 2 Operation

The training control bits are found in the Link Functionality symbol within the TS1 and TS2 ordered sets. They are described in Table 6-5.

Bit 0 and bit 2 of the link configuration field shall not be set to 1 simultaneously. If a receiver detects this condition in the received Link configuration field, then all of the training control bits shall be ignored.

### 6.4.1.2.4 Informative Block Alignment for Gen 2 Operation

During Link training, the 132 bits of the SYNC block are a unique bit pattern that Receivers use to determine the location of the Block Headers in the received bit stream. Conceptually, Receivers

6-17