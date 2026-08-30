Revision 1.1
June 2022

- 71 -

Universal Serial Bus 3.2
Specification

Specific rules for x2 operation (Gen 1 or Gen 2) is described in Section 6.13.6.

### 6.4.3.1 SKP Rules (Host/Device/Hub) for Gen 1x1 Operation

- The SKP Ordered Set shall consist of a SKP K-Symbol followed by a SKP K-Symbol. A SKP Ordered Set represents two Symbols that can be used for clock compensation.
- A device shall keep a running count of the number of transmitted symbols since the last SKP Ordered set. The value of this count will be referred to as Y. The value of Y is reset whenever the transmitter enters Polling.Active.
- Unless otherwise specified, a transmitter shall insert the integer result of Y/354 calculation Ordered sets immediately after each transmitted TS1, TS2 Ordered Set, LMP, TP Data Packet Payload, or Logical idle. During training only, a transmitter is allowed the option of waiting to insert 2 SKP ordered sets when the integer result of Y/354 reaches 2. A transmitter shall not transmit SKP Ordered Sets at any other time.
- A transmitter may pad up to 8 idle symbols before the scheduled SKP Ordered Set to accommodate or implementation consistency with Gen 1x2 operation relating to lane alignment.
- Note: The non-integer remainder of the Y/354 SKP calculation shall not be discarded and shall be used in the calculation to schedule the next SKP Ordered Set.
- SKP Commands do not count as interruptions when monitoring for Ordered Sets (i.e., consecutive TS1, TS2 Ordered Sets in Polling and Recovery).

Table 6-12. Gen 1 SKP Ordered Set Structure

[tbl-47.md](tbl-47.md)

### 6.4.3.2 SKP Rules (Host/Device/Hub) for Gen 1x2 Operation

- In Gen 1x2 operation, the transmitter shall insert the integer result of Y/354 multiplied by one plus the number of re-timers detected during re-timer presence announcement as specific in Section E.3.4.2.1.
- Note: The non-integer remainder of the Y/354 SKP calculation shall not be discarded and shall be used in the calculation to schedule the next SKP Ordered Set.
- Transmitter shall insert the SKP Ordered Set on both lanes simultaneously. If transmitting an odd number of a Data Packet payload, it would finish the data transmission on one lane ahead of another. In that case, transmitter shall pad idle symbols to keep SKP Ordered Set insertion aligned on both lanes. Additionally transmitter may add up to 8 idle symbols on each lane as specified in Section 6.4.3.1.

### 6.4.3.3 SKP Rules (Host/Device/Hub) for Gen 2 Operation

Table 6-13 describes the layout of the SKP Ordered Set for Gen 2 operation. A transmitted SKP Ordered Set is 24 symbols. The granularity for which SKP Symbols can be added or removed is four SKP symbols. Upon receiving a SKP ordered set, a re-timer shall perform one and only one of the following adjustments: add four SKPs, remove four SKPs, or make no adjustment. Thus, a received SKP OS can have anywhere from 4 to 36 SKP symbols with the number of SKP symbols being a multiple of four. Note that in loopback mode, a loopback master may receive a SKP block that has the number of SKP symbols from 0 to 56. This is to

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.