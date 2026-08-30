Universal Serial Bus 3.1 Specification, Revision 1.0

Table 9-8. Standard Status Type Codes

[tbl-159.md](tbl-159.md)

If wLength is not as specified above or if wIndex is non-zero for a device status request, then the behavior of the device is not specified.

If an interface or an endpoint is specified that does not exist, then the device responds with a Request Error.

Default state: Device behavior when this request is received while the device is in the Default state is not specified.

Address state: If an interface or an endpoint other than the Default Control Pipe is specified, then the device responds with a Request Error.

Configured state: If an interface or an endpoint that does not exist is specified, then the device responds with a Request Error.

A GetStatus() request to a device returns the information shown in Figure 9-1.

[tbl-160.md](tbl-160.md)

U-083

Figure 9-4. Information Returned by a Standard GetStatus() Request to a Device

The status fields defined Figure 9-4 are returned by a STANDARD_STATUS type request to a Device recipient.

The Self Powered field indicates whether the device is currently self-powered. If D0 is reset to zero, the device is bus-powered. If D0 is set to one, the device is self-powered. The Self Powered field may not be changed by the SetFeature() or ClearFeature() requests.

The Remote Wakeup field is reserved and must be set to zero by Enhanced SuperSpeed devices. Enhanced SuperSpeed devices use the Function Remote Wake enable/disable field to indicate whether they are enabled for Remote Wake.

The U1 Enable field indicates whether the device is currently enabled to initiate U1 entry. If D2 is set to zero, the device is disabled from initiating U1 entry, otherwise; it is enabled to initiate U1 entry. The U1 Enable field can be modified by the SetFeature() and ClearFeature() requests using the U1_ENABLE feature selector. This field is reset to zero when the device is reset.

The U2 Enable field indicates whether the device is currently enabled to initiate U2 entry. If D3 is set to zero, the device is disabled from initiating U2 entry, otherwise; it is enabled to initiate U2

9-24