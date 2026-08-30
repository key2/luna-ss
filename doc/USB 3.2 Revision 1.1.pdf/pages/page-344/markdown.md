Revision 1.1
June 2022

- 313 -

Universal Serial Bus 3.2
Specification

[tbl-139.md](tbl-139.md)

### 8.12.6.7 Device Response to an Isochronous OUT Data Packet

Table 8-35 lists the device processing of data from an OUT data packet. A device never returns a TP in response. In Table 8-35, DP Error may be due to one or more of the following:

- CRC-32 incorrect
- DPP aborted
- DPP missing
- DPH TT is not set to Isochronous (for a device operating in SuperSpeed Mode)
- Data length in the DPH does not match the actual data payload length
- Deferred bit set in the DPH

Table 8-35. Device Responses to OUT Data Packets

[tbl-140.md](tbl-140.md)

### 8.13 Timing Parameters

Table 8-36 lists the minimum and/or maximum times a device shall adhere to when responding to various types of packets it receives. It also lists the default and minimum times a device may set in Latency Tolerance messages as well as the minimum time after receipt of certain TPs and when it can initiate a U1 or U2 entry. In addition, it lists the maximum time between DPs a device must adhere to while bursting.

All txxxResponse (e.g., tNRDYResponse), tMaxBurstInterval and tGen2MaxBurstInterval times are all timings that a host/device shall meet when the host/device has nothing else to send on its downstream/upstream link.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.