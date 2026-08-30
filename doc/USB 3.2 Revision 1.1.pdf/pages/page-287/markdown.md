Revision 1.1
June 2022

- 256 -

Universal Serial Bus 3.2
Specification

In Table 8-28, DPP Error may be due to one or more of the following:

- CRC incorrect
- DPP aborted
- DPP missing
- Data length in the DPH does not match the actual data payload length

Table 8-28. Host Responses to Data Received from a Device (Bulk, Control, and Interrupt Endpoints)

[tbl-132.md](tbl-132.md)

### 8.11.3 Device Response to Data Received from the Host

TP responses by a device to data received from the host for bulk, control, and interrupt endpoints are shown in Table 8-29. A DPH is considered to be invalid if one or more of the following conditions exist:

- It has an incorrect Device Address
- Its endpoint number and direction does not refer to an endpoint that is part of the current configuration
- It does not have the expected sequence number
- Its Data length in the DPH is greater than the endpoint's maximum packet size
- Its TT does not match the endpoint type (for a device operating in SuperSpeedPlus mode).

In Table 8-29, DPP Error may be due to one or more of the following:

- CRC incorrect
- DPP aborted
- DPP missing
- Data length in the DPH does not match the actual data payload length

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.