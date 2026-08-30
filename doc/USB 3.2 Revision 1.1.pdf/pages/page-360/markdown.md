Revision 1.1
June 2022

- 329 -

Universal Serial Bus 3.2
Specification

Table 9-3. Format of Setup Data

[tbl-146.md](tbl-146.md)

### 9.3.1 bmRequestType

This bitmapped field identifies the characteristics of the specific request. In particular, this field identifies the direction of data transfer in the second stage of the control transfer. The state of the Direction bit is ignored if the wLength field is zero, signifying there is no Data stage.

USB defines a series of standard requests that all devices shall support. These are listed in Table 9-4. In addition, a device class may define additional requests. A device vendor may also define requests supported by the device.

Requests may be directed to the device, an interface on the device, or a specific endpoint on a device. This field also specifies the intended recipient of the request. When an interface is specified, the wIndex field identifies the interface. When an endpoint is specified, the wIndex field identifies the endpoint.

### 9.3.2 bRequest

This field specifies the particular request. The Type bits in the bmRequestType field modify the meaning of this field. This specification defines values for the bRequest field only when the bits are reset to zero, indicating a standard request (refer to Table 9-4).

### 9.3.3 wValue

The contents of this field vary according to the request. It is used to pass a parameter to the device, specific to the request.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.