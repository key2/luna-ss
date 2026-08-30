Protocol Layer

### 8.12.6.4 Host Flexibility in Performing SuperSpeedPlus Isochronous Transactions

A SuperSpeedPlus host is allowed to perform Isochronous transactions without the restrictions mentioned in Section 8.12.6.2 when performing transfers to/from a SuperSpeedPlus Isochronous endpoint. The SuperSpeedPlus host may transfer all the DPs to or from an endpoint in bursts of any size as long as the number of outstanding packets is less than or equal to the max burst size advertised by the endpoint in its descriptors.

A device shall support all possible pipelined Isochronous IN transactions allowed by these rules.

### 8.12.6.5 Device Response to Isochronous IN Transactions

Table 8-33 lists the possible responses a device may make in response to an ACK TP. An ACK TP is considered to be invalid if any of the following conditions exist:

- It has an incorrect Device Address
- Its endpoint number and direction does not refer to an endpoint that is part of the current configuration
- It does not have the expected sequence number
- It has the deferred bit set in it
- Its TT does not match the endpoint type (for devices not operating at Gen 1 speed).

Table 8-33. Device Responses to Isochronous IN Transactions

[tbl-139.md](tbl-139.md)

### 8.12.6.6 Host Processing of Isochronous IN Transactions

Table 8-34 lists the host processing of data from an IN transaction. The host never returns a response to isochronous IN data received. In Table 8-34, DP Error may be due to one or more of the following:

- CRC-32 incorrect
- DPP aborted
- DPP missing
- DPH TT is not set to Isochronous (from a device not operating at Gen 1 speed)
- Data length in the DPH does not match the actual data payload length.

8-119