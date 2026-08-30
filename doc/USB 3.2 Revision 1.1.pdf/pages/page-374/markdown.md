Revision 1.1
June 2022

- 343 -

Universal Serial Bus 3.2
Specification

Table 9-9. Suspend Options

[tbl-169.md](tbl-169.md)

If the feature selector is FUNCTION_SUSPEND, then the most significant byte of wIndex is used to specify Suspend options. The recipient of a SetFeature (FUNCTION_SUSPEND...) shall be the first interface in the function; and, hence, the bmRequestType shall be set to one. The valid encodings for the FUNCTION_SUSPEND suspend options are listed in Table 9-9.

If wLength is non-zero, then the behavior of the device is not specified.

If an endpoint or interface is specified that does not exist, then the device responds with a Request Error.

Default state: Device behavior when this request is received while the device is in the Default state is not specified.

Address state: If an interface or an endpoint other than the Default Control Pipe is specified then the device responds with a Request Error. If the device receives a SetFeature(U1/U2 Enable or LTM Enable or LDM Enable or FUNCTION_SUSPEND), then the device responds with a Request Error.

Configured state: This is a valid request when the device is in the Configured state.

### 9.4.10 Set Interface

This request allows the host to select an alternate setting for the specified interface.

[tbl-170.md](tbl-170.md)

Some devices have configurations with interfaces that have mutually exclusive settings. This request allows the host to select the desired alternate setting. If a device only supports a default setting for the specified interface, then a STALL Transaction Packet may be returned in the Status stage of the request. This request cannot be used to change the set of configured interfaces (the SetConfiguration() request shall be used instead).

If the interface or the alternate setting does not exist, then the device responds with a Request Error. If wLength is non-zero, then the behavior of the device is not specified.

Default state: Device behavior when this request is received while the device is in the Default state is not specified.

Address state: The device shall respond with a Request Error.

Configured state: This is a valid request when the device is in the Configured state.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.