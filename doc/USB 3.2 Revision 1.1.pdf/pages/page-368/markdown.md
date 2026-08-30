Revision 1.1
June 2022

- 337 -

Universal Serial Bus 3.2
Specification

Address state: If an interface or an endpoint other than the Default Control Pipe is specified, then the device responds with a Request Error.

Configured state: If an interface or an endpoint that does not exist is specified, then the device responds with a Request Error.

A GetStatus() request to a device returns the information shown in Figure 9-1.

Figure 9-4. Information Returned by a Standard GetStatus() Request to a Device

[tbl-160.md](tbl-160.md)

...

The status fields defined Figure 9-4 are returned by a STANDARD_STATUS type request to a Device recipient.

The Self Powered field indicates whether the device is currently self-powered. If D0 is reset to zero, the device is bus-powered. If D0 is set to one, the device is self-powered. The Self Powered field may not be changed by the SetFeature() or ClearFeature() requests.

The Remote Wakeup field is reserved and must be set to zero by Enhanced SuperSpeed devices. Enhanced SuperSpeed devices use the Function Remote Wake enable/disable field to indicate whether they are enabled for Remote Wake.

The U1 Enable field indicates whether the device is currently enabled to initiate U1 entry. If D2 is set to zero, the device is disabled from initiating U1 entry, otherwise; it is enabled to initiate U1 entry. The U1 Enable field can be modified by the SetFeature() and ClearFeature() requests using the U1_ENABLE feature selector. This field is reset to zero when the device is reset.

The U2 Enable field indicates whether the device is currently enabled to initiate U2 entry. If D3 is set to zero, the device is disabled from initiating U2 entry, otherwise; it is enabled to initiate U2 entry. The U2 Enable field can be modified by the SetFeature() and ClearFeature() requests using the U2_ENABLE feature selector. This field is reset to zero when the device is reset.

The LTM Enable field indicates whether the device is currently enabled to send Latency Tolerance Messages. If D4 is set to zero, the device is disabled from sending Latency Tolerance Messages, otherwise; it is enabled to send Latency Tolerance Messages. The LTM Enable field can be modified by the SetFeature() and ClearFeature() requests using the LTM_ENABLE feature selector. This field is reset to zero when the device is reset.

A GetStatus() request to the first interface in a function returns the information shown in Figure 9-5.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.