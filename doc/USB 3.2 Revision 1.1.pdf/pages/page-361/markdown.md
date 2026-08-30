Revision 1.1
June 2022

- 330 -

Universal Serial Bus 3.2
Specification

#### 9.3.4 wIndex

The contents of this field vary according to the request. It is used to pass a parameter to the device, specific to the request.

The wIndex field is often used in requests to specify an endpoint or an interface. Figure 9-2 shows the format of wIndex when it is used to specify an endpoint.

Figure 9-2. wIndex Format when Specifying an Endpoint

[tbl-147.md](tbl-147.md)

The Direction bit is set to zero to indicate the OUT endpoint with the specified Endpoint Number and to one to indicate the IN endpoint. In the case of a control pipe, the request should have the Direction bit set to zero but the device may accept either value of the Direction bit.

Figure 9-3 shows the format of wIndex when it is used to specify an interface.

Figure 9-3. wIndex Format when Specifying an Interface

[tbl-148.md](tbl-148.md)

#### 9.3.5 wLength

This field specifies the length of the data transferred during the second stage of the control transfer. The direction of data transfer (host-to-device or device-to-host) is indicated by the Direction bit of the bmRequestType field. If this field is zero, there is no data transfer stage.

On an input request, a device shall never return more data than is indicated by the wLength value; it may return less. On an output request, wLength will always indicate the exact amount of data to be sent by the host. Device behavior is undefined if the host should send more or less data than is specified in wLength.

### 9.4 Standard Device Requests

This section describes the standard device requests defined for all devices. Table 9-4 outlines the standard device requests, while Table 9-5 and Table 9-6 give the standard request codes and descriptor types, respectively.

Devices shall respond to standard device requests, even if the device has not yet been assigned an address or has not been configured. If a standard request defines a persistent parameter that can be modified, the reset/default value for that parameter, unless otherwise specified, is zero.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.