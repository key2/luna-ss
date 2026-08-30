intel®

Table 6-8. Status Interface Output Signals (Sheet 3 of 3)

[tbl-40.md](tbl-40.md)

1. Disparity errors are not reported when the rate is 8.0 GT/s, 16 GT/s, or 32 GT/s.

### 6.1.4 Message Bus Interface

The message bus interface provides a way to initiate and participate in non-latency sensitive PIPE operations using a small number of wires, it also enables future PIPE operations to be added without adding additional wires. The use of this interface requires the device to be in a power state with PCLK running. Control and status bits used for PIPE operations are mapped into 8-bit registers that are hosted in 12-bit address spaces in the PHY and the MAC. The registers are accessed via read and write commands driven over the signals listed in Table 6-9. These signals are synchronous with the PCLK and are reset with Reset#. The specific commands and framing of the transactions sent over the message bus interface are described in the following subsections.

Table 6-9. Message Bus Interface Signals

[tbl-41.md](tbl-41.md)

Errors in SKP ordered sets must be reported by the PHY as 128/130 decode errors. An error in an SKP ordered set must be reported if there is an error in the first 4N+1 symbols of the skip ordered set.

#### 6.1.4.1 Message Bus Interface Commands

The 4-bit commands used for accessing the PIPE registers across the message bus are defined in Table 6-10. A transaction consists of a command and any associated address and data, as specified in the table. The table also specifies the number of PCLK cycles

66

Reference Number: 643108, Revision: 7.1