Device Framework

### 9.3.2 bRequest

This field specifies the particular request. The Type bits in the bmRequestType field modify the meaning of this field. This specification defines values for the bRequest field only when the bits are reset to zero, indicating a standard request (refer to Table 9-4).

### 9.3.3 wValue

The contents of this field vary according to the request. It is used to pass a parameter to the device, specific to the request.

### 9.3.4 wIndex

The contents of this field vary according to the request. It is used to pass a parameter to the device, specific to the request.

The wIndex field is often used in requests to specify an endpoint or an interface. Figure 9-2 shows the format of wIndex when it is used to specify an endpoint.

[tbl-148.md](tbl-148.md)

U-081

Figure 9-2. wIndex Format when Specifying an Endpoint

The Direction bit is set to zero to indicate the OUT endpoint with the specified Endpoint Number and to one to indicate the IN endpoint. In the case of a control pipe, the request should have the Direction bit set to zero but the device may accept either value of the Direction bit.

Figure 9-3 shows the format of wIndex when it is used to specify an interface.

[tbl-149.md](tbl-149.md)

U-082

Figure 9-3. wIndex Format when Specifying an Interface

9-15