Universal Serial Bus 3.1 Specification, Revision 1.0

- No SKP Ordered Sets are to be transmitted during the entire TSEQ time (65,536 ordered sets). This means that the PHY must manage its elasticity buffer differently than during normal operation.

Additional rules for the use of TSEQ, TS1, and TS2 Ordered Sets can be found in Chapter 7.

### 6.4.1.1.2 Training Control Bits for Gen 1 Operation

The training control bits are found in the Link Functionality symbol within the TS1 and TS2 ordered sets. They are described in Table 6-5.

Bit 0 and bit 2 of the link configuration field shall not be set to 1 simultaneously. If a receiver detects this condition in the received Link configuration field, then all of the training control bits shall be ignored.

### 6.4.1.1.3 Training Sequence Values for Gen 1 Operation

The TSEQ training sequence repeats 65,536 times to allow for testing many coefficient settings.

Table 6-2. Gen 1 TSEQ Ordered Set

[tbl-55.md](tbl-55.md)

Table 6-3. Gen 1 TS1 Ordered Set

[tbl-56.md](tbl-56.md)

6-14