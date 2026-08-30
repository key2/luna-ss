intel®

Table 6-12. Command+Address Message Bus Transaction Timing (Read)

[tbl-44.md](tbl-44.md)

Table 6-13. Command+Data Message Bus Transaction Timing (Read Completion)

[tbl-45.md](tbl-45.md)

Table 6-14. Command+Address+Data Message Bus Transaction Timing (Write_uncommitted, Write_committed)

[tbl-46.md](tbl-46.md)

### 6.1.4.2 Message Bus Interface Framing

The framing of transactions is implicitly derived by adhering to the following rules:

1. All zeroes must be driven on the message bus when idle.
2. An idle to a non-idle transition indicates the start of a transaction; a new transaction can immediately start the cycle after the end of the previous transaction without an intervening idle.
3. The number of cycles to transmit a transaction depends on the command and is specified in Table 6-10.
4. The cycles associated with one transaction must be transferred in contiguous cycles.

Figure 6-1 illustrates the framing of a couple of transactions on the message bus. The start of the first transaction is inferred by the idle to a non-idle transition. The command is decoded as a write, which takes three cycles to transmit. Since the cycle following the end of the write is non-idle, it is inferred to be the start of the next transaction, which is decoded to be another write that takes three cycles to transmit.

68

Reference Number: 643108, Revision: 7.1