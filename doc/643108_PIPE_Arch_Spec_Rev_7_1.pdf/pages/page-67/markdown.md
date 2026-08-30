intel®

that it takes to transfer the transaction across the message bus interface. The order in which the bits are transferred across the interface are illustrated in Table 6-11, Table 6-12, Table 6-13, and Table 6-14.

To address the case where multiple PIPE interface signals can change on the same PCLK, the concept of write_uncommitted and write_committed is introduced. A series of write_uncommitted transactions followed by one write_committed transaction provides a mechanism by which all the uncommitted writes and the final committed write are executed in an atomic manner, taking effect during the same PCLK cycle.

To enable the write_uncommitted command, designs must implement a write buffer in the PHY and the MAC, where each write buffer entry can accommodate the three bytes worth of information associated with each write transaction. The minimum write buffer depth required is five, however, this number may increase in the future when new PIPE operations are mapped into the message bus interface.

Table 6-10. Message Bus Commands

[tbl-42.md](tbl-42.md)

Table 6-11. Command Only Message Bus Transaction Timing (NOP, write_ack)

[tbl-43.md](tbl-43.md)

Reference Number: 643108, Revision: 7.1

67