Revision 1.1
June 2022

- 312 -

Universal Serial Bus 3.2
Specification

A device shall support all possible pipelined Isochronous IN transactions allowed by these rules.

### 8.12.6.5 Device Response to Isochronous IN Transactions

Table 8-33 lists the possible responses a device may make in response to an ACK TP. An ACK TP is considered to be invalid if any of the following conditions exist:

- It has an incorrect Device Address
- Its endpoint number and direction does not refer to an endpoint that is part of the current configuration
- It does not have the expected sequence number
- It has the deferred bit set in it
- Its TT does not match the endpoint type (for devices operating in SuperSpeedPlus mode).

Table 8-33. Device Responses to Isochronous IN Transactions

[tbl-137.md](tbl-137.md)

### 8.12.6.6 Host Processing of Isochronous IN Transactions

Table 8-34 lists the host processing of data from an IN transaction. The host never returns a response to isochronous IN data received. In Table 8-34, DP Error may be due to one or more of the following:

- CRC-32 incorrect
- DPP aborted
- DPP missing
- DPH TT is not set to Isochronous (from a device operating in SuperSpeedPlus mode)
- Data length in the DPH does not match the actual data payload length.

If the host receives a corrupted data packet, it discards the remaining data in the current service interval and informs host software of the error.

Table 8-34. Host Responses to IN Transactions

[tbl-138.md](tbl-138.md)

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.