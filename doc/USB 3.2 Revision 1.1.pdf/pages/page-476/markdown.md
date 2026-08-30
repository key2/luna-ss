Revision 1.1
June 2022

- 445 -

Universal Serial Bus 3.2
Specification

Table 10-12. Port Status Type Codes

[tbl-248.md](tbl-248.md)

It is a Request Error if the Port Status Type equals EXT_PORT_STATUS and the hub that does not define a SuperSpeedPlus USB Capability descriptor, or if the Port Status Type equals a reserved value, or if wValue or wLength are other than as specified in Table 10-7, or if wIndex specifies a port that does not exist.

If the hub is not configured, the behavior of the hub in response to this request is undefined.

### 10.16.2.6.1 Port Status Bits

Table 10-13. Port Status Field, wPortStatus

[tbl-249.md](tbl-249.md)

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.