Device Framework

All devices shall provide a device descriptor and at least one configuration descriptor. If a device does not support a requested descriptor, it responds with a Request Error.

Default state: This is a valid request when the device is in the Default state.

Address state: This is a valid request when the device is in the Address state.

Configured state: This is a valid request when the device is in the Configured state.

### 9.4.4 Get Interface

This request returns the selected alternate setting for the specified interface.

[tbl-157.md](tbl-157.md)

Some devices have configurations with interfaces that have mutually exclusive settings. This request allows the host to determine the currently selected alternate setting.

If wValue or wLength are not as specified above, then the device behavior is not specified.

If the interface specified does not exist, then the device responds with a Request Error.

Default state: Device behavior when this request is received while the device is in the Default state is not specified.

Address state: A Request Error response is given by the device.

Configured state: This is a valid request when the device is in the Configured state.

### 9.4.5 Get Status

This request returns status for the specified recipient.

[tbl-158.md](tbl-158.md)

The Recipient bits of the bmRequestType field specify the desired recipient. The data returned is the current status of the specified recipient. If the recipient is an endpoint, then the lower byte of wIndex identifies the endpoint whose status is being queried. If the recipient is an interface, then the lower byte of wIndex identifies the interface whose status is being queried.

Only a Device is allowed as the Recipient for a PTM Status request.

The wValue field specifies the Status type in the low order byte (refer to Table 9-8) and the high order byte is reserved. The Status Type is used to select a specific status register when several types of status registers are implemented in a device.

9-23