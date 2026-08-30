Universal Serial Bus 3.1 Specification, Revision 1.0

A receiver must always perform single bit error correction on the SKP and SKPEND (and all other special) symbols. However, since the Hamming distance between the SKP and SKPEND symbols is 8, once a receiver has determined that it is dealing with a non-empty SKP OS (by proper detection of a first SKP symbol) it may be beneficial to use multiple bit (up to 3-bit) error correction in differentiating between a SKP and a SKPEND symbol.

Table 6-12. Gen 2 SKP Ordered Set

[tbl-65.md](tbl-65.md)

The following rules apply for SKP insertion for Gen 2 operation:

1. A transmitter shall keep a running count of the number of transmitted blocks since the last SKP Ordered set. The value of this count will be referred to as Y. The value of Y is reset whenever the transmitter enters Polling.Active or when a SKP OS is transmitted.
2. Once the count, Y, gets to 21 a transmitter must insert a SKP OS at the next legitimate opportunity. The fastest a transmitter can insert SKP OS is once every 22 blocks. Situations that delay the immediate insertion of a SKP OS are the following: a transmitter shall not interrupt a data packet or a SYNC OS to insert a SKP OS. In the worst case it may take 90 blocks before there is an opportunity to insert a SKP OS. In Gen 2 operation there is no accumulation of SKP OS, each time a SKP OS is transmitted the SKP counter, Y, is reset to 0.
3. SKP Ordered Sets do not count as interruptions when monitoring for Ordered Sets (i.e., consecutive TS1, TS2 Ordered Sets in Polling and Recovery).

6-20