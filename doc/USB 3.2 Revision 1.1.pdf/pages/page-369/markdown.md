Revision 1.1
June 2022

- 338 -

Universal Serial Bus 3.2
Specification

Figure 9-5. Information Returned by a Standard GetStatus() Request to an Interface

[tbl-161.md](tbl-161.md)

The status fields defined by Figure 9-5 are returned by a STANDARD_STATUS type request to an Interface recipient.

The Function Remote Wake Capable field indicates whether the function supports remote wake up. The Function Remote Wakeup field indicates whether the function is currently enabled to request remote wakeup. The default mode for functions that support function remote wakeup is disabled. If D1 is reset to zero, the ability of the function to signal remote wakeup is disabled. If D1 is set to one, the ability of the function to signal remote wakeup is enabled. The Function Remote Wakeup field can be modified by the SetFeature() requests using the FUNCTION_SUSPEND feature selector. This Function Remote Wakeup field is reset to zero when the function is reset.

A GetStatus() request to any other interface in a function shall return all zeros.

A GetStatus() request to an endpoint returns the information shown in Figure 9-6.

Figure 9-6. Information Returned by a Standard GetStatus() Request to an Endpoint

[tbl-162.md](tbl-162.md)

The status fields defined by Figure 9-6 are returned by a STANDARD_STATUS type request to an Endpoint recipient.

The Halt feature is required to be implemented for all interrupt and bulk endpoint types. If the endpoint is currently halted, then the Halt feature is set to one. Otherwise, the Halt feature is reset to zero. The Halt feature may optionally be set with the SetFeature(ENDPOINT_HALT) request. When set by the SetFeature() request, the endpoint exhibits the same stall behavior as if the field had been set by a hardware condition. If the condition causing a halt has been removed, clearing the Halt feature via a ClearFeature(ENDPOINT_HALT) request results in the endpoint no longer returning a STALL Transaction Packet. Regardless of whether an endpoint has the Halt feature set, a ClearFeature(ENDPOINT_HALT) request always results in the data sequence being reinitialized to zero, and if Streams are enabled, the Stream State Machine shall be reinitialized to the Disabled state. The Halt feature is reset to zero after either a SetConfiguration() or SetInterface() request even if the requested configuration or interface is the same as the current configuration or interface.

Enhanced SuperSpeed devices do not support functional stall on control endpoints and hence do not require the Halt feature be implemented for any control endpoints.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.