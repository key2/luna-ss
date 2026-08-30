Revision 1.1
June 2022

- 444 -

Universal Serial Bus 3.2
Specification

[tbl-245.md](tbl-245.md)

Hubs may allow setting of these change bits with SetHubFeature() requests in order to support diagnostics. If the hub does not support setting of these bits, it shall either treat the SetHubFeature() request as a Request Error or as a functional no-operation. When set, these bits may be cleared by a ClearHubFeature() request. A request to set a feature that is already set or to clear a feature that is already clear has no effect and the hub shall treat this as a functional no-operation.

### 10.16.2.5 Get Port Error Count

This request returns the number of link errors detected by the hub on the port indicated by wIndex. This value is reset to zero whenever the device goes through a Reset (refer to Section 7.3) or at power up.

[tbl-246.md](tbl-246.md)

The port number shall be a valid port number for that hub, greater than zero.

It is a Request Error if wValue or wLength are other than as specified above or if wIndex specifies a port that does not exist.

If the hub is not configured, the behavior of the hub in response to this request is undefined.

### 10.16.2.6 Get Port Status

This request returns the current port status and the current value of the port status change bits.

[tbl-247.md](tbl-247.md)

The port number shall be a valid port number for that hub, greater than zero.

The first word of PORT_STATUS or EXT_PORT_STATUS data contains the wPortStatus field (refer to Table 10-13). The second word of PORT_STATUS or EXT_PORT_STATUS data contains the wPortChange field (refer to Table 10-14). An EXT_PORT_STATUS request shall return an additional dword of data that contains dwExtPortStatus field (refer to Table 10-15).

The bit locations in the wPortStatus and wPortChange fields correspond in a one-to-one fashion where applicable.

The wValue field specifies the Port Status Type in the low order byte (refer to Table 10-11 and the high order byte is reserved.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.