Revision 1.1
June 2022

- 339 -

Universal Serial Bus 3.2
Specification

Figure 9-7. Information Returned by a PTM GetStatus() Request to an Endpoint

[tbl-163.md](tbl-163.md)

The status fields defined by Figure 9-7 are returned by a PTM_STATUS type request to a Device recipient.

The LDM Enabled flag indicates whether the device is currently enabled to participate in Precision Time Measurement (PTM). If LDM Enabled flag is set to zero, the device is disabled from executing the LDM protocol and providing a local bus interval boundary reference, otherwise; it is enabled to execute the LDM protocol. The LDM Enabled flag can be modified by the SetFeature() and ClearFeature() requests using the LDM_ENABLE feature selector. This field shall be set to one when the device is reset, allowing a PTM capable device to automatically attempt to participate in LDM with its upstream partner. If a Requestor is unable to successfully establish LDM Timestamp Exchanges in its Responder, then the LDM Enabled field shall be cleared to zero.

The LDM Valid field indicates whether the LDM Link Delay is valid, otherwise; it is invalid. LDM Valid shall be zero if LDM Enabled is zero.

The LDM Link Delay field is in tIsochTimestampGranularity units. If LDM Valid is one, then the LDM Link Delay field defines the link delay value measured by the PTM LDM mechanism. If LDM Valid is zero, then the LDM Link Delay field shall be set to zero. Refer to section 8.4.8.5.1.

#### 9.4.6 Set Address

This request sets the device address for all future device accesses.

[tbl-164.md](tbl-164.md)

The wValue field specifies the device address to use for all subsequent accesses.

The Status stage after the initial Setup packet assumes the same device address as the Setup packet. The device does not change its device address until after the Status stage of this request is completed successfully. Note that this is a difference between this request and all other requests. For all other requests, the operation indicated shall be completed before the Status stage.

If the specified device address is greater than 127, or if wIndex or wLength is non-zero, then the behavior of the device is not specified.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.