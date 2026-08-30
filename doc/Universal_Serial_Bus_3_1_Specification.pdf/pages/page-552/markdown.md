Universal Serial Bus 3.1 Specification, Revision 1.0

If the hub is not configured, the hub's response to this request is undefined.

### 10.16.2.3 Get Hub Descriptor

This request returns the hub descriptor.

[tbl-234.md](tbl-234.md)

The GetDescriptor() request for the hub class descriptor follows the same usage model as that of the standard GetDescriptor() request (refer to Chapter 9). The standard hub descriptor is denoted by using the value bDescriptorType defined in Section 10.15.2.1. All hubs are required to implement one hub descriptor, with descriptor index zero.

If wLength is larger than the actual length of the descriptor, then only the actual length is returned. If wLength is less than the actual length of the descriptor, then only the first wLength bytes of the descriptor are returned; this is not considered an error even if wLength is zero.

It is a Request Error if wValue or wIndex are other than as specified above.

If the hub is not configured, the hub's response to this request is undefined.

### 10.16.2.4 Get Hub Status

This request returns the current hub status and the states that have changed since the previous acknowledgment.

[tbl-235.md](tbl-235.md)

The first word of data contains the wHubStatus field (refer to Table 10-10). The second word of data contains the wHubChange field (refer to Table 10-11).

It is a Request Error if wValue, wIndex, or wLength are other than as specified above.

If the hub is not configured, the hub's response to this request is undefined.

10-74