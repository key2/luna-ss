Universal Serial Bus 3.1 Specification, Revision 1.0

### 8.11.4 Device Response to a SETUP DP

A SETUP DP is a special DP that is identified by the Setup field set to one and addressed to any control endpoint. SETUP is a special type of host-to-device data transaction that permits the host to initiate a command that the device shall perform. Upon receiving a SETUP DP, a device shall respond as shown in Table 8-30.

A SETUP DPH shall be considered invalid if it has any one of the following:

- Incorrect Device Address
- Endpoint number and direction does not refer to an endpoint that is part of the current configuration
- Endpoint number does not refer to a control endpoint
- Non-zero sequence number
- Data length is not set to eight
- TT does not match the endpoint type (for a device not operating at Gen 1 speed).

In Table 8-30, DPP Error may be due to one or more of the following:

- CRC incorrect
- DPP aborted
- DPP missing
- Data length in the Setup DPH does not match the actual data payload length.

Table 8-30. Device Responses to SETUP Transactions (Only for Control Endpoints)

[tbl-136.md](tbl-136.md)

8-60