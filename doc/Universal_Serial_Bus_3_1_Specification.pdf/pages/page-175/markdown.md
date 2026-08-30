Physical Layer

The total magnitude of the frequency delta can range from -5300 to 300 ppm. This frequency delta is managed by an elasticity buffer that consumes or inserts SKP ordered sets.

SKP Ordered Sets shall be used to compensate for frequency differences between the two ends of the link. The transmitter sends SKP ordered sets at an average of every 354 symbols. However, SKP ordered sets shall not be inserted within any packet. The transmitter is allowed to buffer the SKP ordered sets up to a maximum of four SKP ordered sets. For Gen 1 operation the receiver shall implement an elasticity buffer capable of buffering (or starving) eight symbols of data. For Gen 2 operation, due to the presence of retimers along the signal path, a receiver shall tolerate not receiving any SKP Symbols for up to 180 blocks. Thus during Gen 2 operation a receiver must implement an elasticity buffer capable of buffering (or starving) twenty two symbols of data.

### 6.4.3.1 SKP Rules (Host/Device/Hub) for Gen 1 Operation

- The SKP Ordered Set shall consist of a SKP K-Symbol followed by a SKP K-Symbol. A SKP Ordered Set represents two Symbols that can be used for clock compensation.
- A device shall keep a running count of the number of transmitted symbols since the last SKP Ordered set. The value of this count will be referred to as Y. The value of Y is reset whenever the transmitter enters Polling.Active.
- Unless otherwise specified, a transmitter shall insert the integer result of Y/354 calculation Ordered sets immediately after each transmitted TS1, TS2 Ordered Set, LMP, TP Data Packet Payload, or Logical idle. During training only, a transmitter is allowed the option of waiting to insert 2 SKP ordered sets when the integer result of Y/354 reaches 2. A transmitter shall not transmit SKP Ordered Sets at any other time.

Note: The non-integer remainder of the Y/354 SKP calculation shall not be discarded and shall be used in the calculation to schedule the next SKP Ordered Set.

- SKP Commands do not count as interruptions when monitoring for Ordered Sets (i.e., consecutive TS1, TS2 Ordered Sets in Polling and Recovery).

Table 6-11. Gen 1 SKP Ordered Set Structure

[tbl-64.md](tbl-64.md)

### 6.4.3.2 SKP Rules (Host/Device/Hub) for Gen 2 Operation:

Table 6-12 describes the layout of the SKP Ordered Set when using 128b/132b encoding. A transmitted SKP Ordered Set always starts out as 16 Symbols long. The granularity for which SKP Symbols can be added or removed by a Port is two symbols. A port may add or remove more than 2 SKP symbols, but the number of SKP symbols that is added or removed shall be a multiple of two. This includes retimers within the signal path. Thus, a receiver may receive a SKP OS with anywhere from 0 to thirty six SKP symbols with the number of SKP symbols being a multiple of two. A SKP OS with 0 SKP symbols has only a SKPEND symbol followed by the three symbols that describe the LFSR state. Another impact of receiving variable length SKP OS is that a receiver is always allowed to add up to 12 SKP symbols to any SKP OS regardless of the length of the received SKP OS.

The SKPEND Symbol indicates the last four Symbols of SKP Ordered Set so that receivers can identify the location of the next Block Header in the bit stream. The three Symbols following the SKPEND Symbol contain different information depending on the LTSSM state.

6-19