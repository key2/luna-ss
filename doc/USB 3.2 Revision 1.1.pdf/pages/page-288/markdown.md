Revision 1.1
June 2022

- 257 -

Universal Serial Bus 3.2
Specification

Note: Receipt of an ACK TP indicates to the host the DP with the previous sequence number was successfully received by a device as well as the number of data packet buffers the device has available to receive any pending DPs the host has. A device shall send an ACK TP for each DP successfully received.

**Table 8-29. Device Responses to OUT Transactions (Bulk, Control, and Interrupt Endpoints)**

[tbl-133.md](tbl-133.md)

#### 8.11.4 Device Response to a SETUP DP

A SETUP DP is a special DP that is identified by the **Setup** field set to one and addressed to any control endpoint. SETUP is a special type of host-to-device data transaction that permits the host to initiate a command that the device shall perform. Upon receiving a SETUP DP, a device shall respond as shown in Table 8-30.

A SETUP DPH shall be considered invalid if it has any one of the following:

- Incorrect Device Address
- Endpoint number and direction does not refer to an endpoint that is part of the current configuration
- Endpoint number does not refer to a control endpoint
- Non-zero sequence number
- Data length is not set to eight
- TT does not match the endpoint type (for a device operating in SuperSpeedPlus mode).

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.