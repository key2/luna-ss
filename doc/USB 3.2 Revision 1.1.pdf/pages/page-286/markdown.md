Revision 1.1
June 2022

- 255 -

Universal Serial Bus 3.2
Specification

### 8.11.1 Device Response to TP Requesting Data

Table 8-27 shows the possible ways a device shall respond to a TP requesting data for bulk, control, and interrupt endpoints. A TP is considered to be invalid if one or more of the following conditions exist:

- It has an incorrect Device Address
- Its endpoint number and direction does not refer to an endpoint that is part of the current configuration
- It does not have the expected sequence number
- Its TT does not match the endpoint type (for a device operating in SuperSpeedPlus mode).

Table 8-27. Device Responses to TP Requesting Data (Bulk, Control, and Interrupt Endpoints)

[tbl-131.md](tbl-131.md)

An IN endpoint shall wait until it receives an ACK TP for the last DP it transmitted before it can send an STALL TP.

### 8.11.2 Host Response to Data Received from a Device

Table 8-28 shows the host responses to data received from a device for bulk, control, and interrupt endpoints. The host is able to return only an ACK TP. A DPH is considered to be invalid if any of the following conditions exist:

- It has an incorrect Device Address
- Its endpoint number and direction does not refer to an endpoint that is part of the current configuration
- It does not have the expected sequence number
- Its Data length in the DPH is greater than the endpoint's maximum packet size
- Its TT does not match the endpoint type (from a device operating in SuperSpeedPlus mode).

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.