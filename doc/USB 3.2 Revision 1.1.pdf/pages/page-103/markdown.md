Revision 1.1
June 2022

- 72 -

Universal Serial Bus 3.2
Specification

assume that there are four re-timers between the loopback master and the loopback slave. There exists a possibility that all re-timers in the forward path from the loopback master to the loopback slave may all remove the maximum number of SKP symbols allowed on the first SKP block, leaving with no SKPs, but only SKPEND and the LFSR seeds. There also exists a theoretical possibility that all re-timers in the forward and return path, and loopback slave, may all insert the maximum number of SKP symbols allowed. A loopback master shall be prepared to deal with such extreme scenarios. A loopback slave and a re-timer may perform its clock offset compensation on either of the SKP blocks.

The SKPEND Symbol indicates the last four Symbols of SKP Ordered Set so that receivers can identify the location of the next Block Header in the bit stream. The three Symbols following the SKPEND Symbol contain the transmitter LFSR state.

A receiver shall always perform single bit error correction on the SKP and SKPEND (and all other special) symbols. However, since the Hamming distance between the SKP and SKPEND symbols is 8, once a receiver has determined that it is dealing with a SKP OS (by proper detection of a first SKP symbol) it may be beneficial to use multiple bit (up to 3-bit) error correction in differentiating between a SKP and a SKPEND symbol.

**Table 6-13. Gen 2 SKP Ordered Set**

[tbl-48.md](tbl-48.md)

Note: The transmitted LFSR state is intended for use by test equipment vendors needing to re-synch their data scramblers. The transmitted LFSR state is not intended to be used by ports in normal operation.

The following rules apply for SKP insertion for Gen 2 operation:

1. A port shall keep a running count of the number of transmitted blocks since the last SKP Ordered Set. The value of this count will be referred to as Y. The value of Y is reset whenever the transmitter enters Polling.Active. Y is not incremented for transmitted SKP Ordered Sets.
2. A port shall calculate the integer result of Y/40 when an opportunity to insert a SKP Ordered Set arises. The integer result of Y/40 is the number of accumulated SKP Ordered Sets that need to be transmitted – this value will be referred to as Z. The value of Z can be either 0, 1, or 2.

Note: The non-integer remainder of the Y/40 SKP calculation shall not be discarded and shall be used in the calculation to schedule the next SKP Ordered Set.

3. Unless otherwise specified, when the LTSSM is not in the loopback state, a transmitter shall insert Z SKP Ordered Sets immediately after each transmitted SYNC, TS1, TS2, SDS, LMP, Header Packet, Data Packet, or Logical idle. When the LTSSM is in the Loopback state, the Loopback Master transmitter shall insert 2*Z SKP Ordered Sets immediately after each transmitted SYNC, TS1, TS2, SDS, LMP,

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.