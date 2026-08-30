Revision 1.1
June 2022

- 451 -

Universal Serial Bus 3.2
Specification

### 10.16.2.7 Set Hub Descriptor

This request overwrites the hub descriptor.

[tbl-254.md](tbl-254.md)

The SetDescriptor request for the hub class descriptor follows the same usage model as that of the standard SetDescriptor request (refer to the Chapter 9). The standard hub descriptor is denoted by using the value bDescriptorType defined in Section 10.15.2.1. All hubs are required to implement one hub descriptor with descriptor index zero.

This request is optional. This request writes data to a class-specific descriptor. The host provides the data that is to be transferred to the hub during the data transfer stage of the control transaction. This request writes the entire hub descriptor at once.

Hubs shall buffer all the bytes received from this request to ensure that the entire descriptor has been successfully transmitted from the host. Upon successful completion of the bus transfer, the hub updates the contents of the specified descriptor.

It is a Request Error if wIndex is not zero or if wLength does not match the amount of data sent by the host. Hubs that do not support this request respond with a STALL during the Data stage of the request.

If the hub is not configured, the hub's response to this request is undefined.

### 10.16.2.8 Set Hub Feature

This request sets a value reported in the hub status.

[tbl-255.md](tbl-255.md)

Setting a defined feature enables that feature. Status changes may not be acknowledged using this request.

It is a Request Error if wValue is not a defined feature selector or if wIndex or wLength are not as specified above.

If the hub is not configured, the hub's response to this request is undefined.

### 10.16.2.9 Set Hub Depth

This request sets the value that the hub uses to determine the index into the Route String Index for the hub.

[tbl-256.md](tbl-256.md)

wValue has the value of the Hub Depth. The Hub Depth left shifted by two is the offset into the Route String that identifies the lsb of the Route String Port Field for the hub.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.