Universal Serial Bus 3.1 Specification, Revision 1.0

The Halt feature is required to be implemented for all interrupt and bulk endpoint types. If the endpoint is currently halted, then the Halt feature is set to one. Otherwise, the Halt feature is reset to zero. The Halt feature may optionally be set with the SetFeature(ENDPOINT_HALT) request. When set by the SetFeature() request, the endpoint exhibits the same stall behavior as if the field had been set by a hardware condition. If the condition causing a halt has been removed, clearing the Halt feature via a ClearFeature(ENDPOINT_HALT) request results in the endpoint no longer returning a STALL Transaction Packet. Regardless of whether an endpoint has the Halt feature set, a ClearFeature(ENDPOINT_HALT) request always results in the data sequence being reinitialized to zero, and if Streams are enabled, the Stream State Machine shall be reinitialized to the Disabled state. The Halt feature is reset to zero after either a SetConfiguration() or SetInterface() request even if the requested configuration or interface is the same as the current configuration or interface.

Enhanced SuperSpeed devices do not support functional stall on control endpoints and hence do not require the Halt feature be implemented for any control endpoints.

[tbl-163.md](tbl-163.md)

U-085a

Figure 9-7. Information Returned by a PTM GetStatus() Request to an Endpoint

The status fields defined by Figure 9-7 are returned by a PTM_STATUS type request to a Device recipient.

The LDM Enabled flag indicates whether the device is currently enabled to participate in Precision Time Measurement (PTM). If D5 is set to zero, the device is disabled from executing the LDM protocol and providing a local bus interval boundary reference, otherwise; it is enabled to execute the LDM protocol. The LDM Enabled flag can be modified by the SetFeature() and ClearFeature() requests using the LDM_ENABLE feature selector. This field shall be set to one when the device is reset, allowing a PTM capable device to automatically attempt to participate in LDM with its upstream partner. If a Requestor is unable to successfully establish LDM Timestamp Exchanges in its Responder, then the LDM Enabled field shall be cleared to zero.

The LDM Valid field indicates whether the LDM Link Delay is valid, otherwise; it is invalid. LDM Valid shall be zero if LDM Enabled is zero.

The LDM Link Delay field is in tIsochTimestampGranularity units. If LDM Valid is one, then the LDM Link Delay field defines the link delay value measured by the PTM LDM mechanism. If LDM Valid is one, then the LDM Link Delay field shall be set to zero. Refer to section 8.4.8.4.

9-26