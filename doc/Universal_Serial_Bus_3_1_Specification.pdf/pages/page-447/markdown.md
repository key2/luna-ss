Device Framework

the recipient is an endpoint. If the recipient is an endpoint, then the lower byte of wIndex identifies the endpoint.

Refer to Table 9-7 for a definition of which feature selector values are defined for which recipients.

The FUNCTION_SUSPEND feature is only defined for an interface recipient. The lower byte of wIndex shall be set to the first interface that is part of that function.

The U1/U2_ENABLE feature is only defined for a device recipient and wIndex shall be set to zero. Setting the U1/U2_ENABLE feature allows the device to initiate U1/U2 entry respectively. A device shall support the U1/U2_ENABLE feature when in the Configured state only. System software must not enable the device to initiate U1 if the time for U1 System Exit Latency initiated by Host plus one Bus Interval time is greater than the minimum of the service intervals of any periodic endpoints in the device. In addition, system software must not enable the device to initiate U2 if the time for U2 System Exit Latency initiated by Host plus one Bus Interval time is greater than the minimum of the service intervals of any periodic endpoints in the device.

The LTM_ENABLE feature is only defined for a device recipient and wIndex shall be set to zero. Setting the LTM_ENABLE feature allows the device to send Latency Tolerance Messages. A device shall support the LTM_ENABLE feature if it is in the Configured state and supports the LTM capability.

The LDM_ENABLE feature is only defined for a device recipient and wIndex shall be set to zero. Setting the LDM_ENABLE feature allows the device to execute the LDM protocol. A device shall support the LDM_ENABLE feature if it is in the Address or Configured states and supports the PTM capability.

A SetFeature() request that references a feature that cannot be set or that does not exist causes a STALL Transaction Packet to be returned in the Status stage of the request.

Table 9-9. Suspend Options

[tbl-168.md](tbl-168.md)

If the feature selector is FUNCTION_SUSPEND, then the most significant byte of wIndex is used to specify Suspend options. The recipient of a SetFeature (FUNCTION_SUSPEND...) shall be the first interface in the function; and, hence, the bmRequestType shall be set to one. The valid encodings for the FUNCTION_SUSPEND suspend options are listed in Table 9-9.

If wLength is non-zero, then the behavior of the device is not specified.

9-29