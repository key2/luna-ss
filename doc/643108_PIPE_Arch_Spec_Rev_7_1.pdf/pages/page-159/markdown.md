intel®

Certain registers are defined as part of a register group. To simplify validation space, whenever one register in a register group needs to be updated, all the registers in the register group must be updated using a sequence of uncommitted writes and a single committed write. The defined register groups are listed in Table 8-9, where each row corresponds to a register group.

Table 8-9. Defined Register Groups

[tbl-146.md](tbl-146.md)

### 8.29.2 Message Bus Operations vs. Dedicated Signals

For simplicity, dependencies between message bus operations and dedicated signals are kept to a minimum. The dependencies that do exist are there only because no acceptable workarounds for eliminating them have been identified; these dependencies are documented in this section:

- The PHY must wait for the write_ack to come back for any write to LocalLF, LocalFS, LocalG4LF, or LocalG4FS, if any, before it asserts PhyStatus for a rate change.

### 8.30 PCIe Lane Margining at the Receiver

Table 8-10 provides the sequence of PIPE message bus commands associated with various receiver margining operations; different sequences are shown for independent and dependent samplers. Writes to Sample Count and Error Count fields are only applicable if the PHY supports those features.

Reference Number: 643108, Revision: 7.1

159