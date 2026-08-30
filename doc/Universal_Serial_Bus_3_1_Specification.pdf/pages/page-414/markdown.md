Universal Serial Bus 3.1 Specification, Revision 1.0

If the host receives a corrupted data packet, it discards the remaining data in the current service interval and informs host software of the error.

Table 8-34. Host Responses to IN Transactions

[tbl-140.md](tbl-140.md)

### 8.12.6.7 Device Response to an Isochronous OUT Data Packet

Table 8-35 lists the device processing of data from an OUT data packet. A device never returns a TP in response. In Table 8-35, DP Error may be due to one or more of the following:

- CRC-32 incorrect
- DPP aborted
- DPP missing
- DPH TT is not set to Isochmous (for a device not operating at Gen 1 speed)
- Data length in the DPH does not match the actual data payload length
- Deferred bit set in the DPH

Table 8-35. Device Responses to OUT Data Packets

[tbl-141.md](tbl-141.md)

8-120