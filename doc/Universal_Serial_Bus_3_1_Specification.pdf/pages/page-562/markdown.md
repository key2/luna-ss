Universal Serial Bus 3.1 Specification, Revision 1.0

This request is optional. This request writes data to a class-specific descriptor. The host provides the data that is to be transferred to the hub during the data transfer stage of the control transaction. This request writes the entire hub descriptor at once.

Hubs shall buffer all the bytes received from this request to ensure that the entire descriptor has been successfully transmitted from the host. Upon successful completion of the bus transfer, the hub updates the contents of the specified descriptor.

It is a Request Error if wIndex is not zero or if wLength does not match the amount of data sent by the host. Hubs that do not support this request respond with a STALL during the Data stage of the request.

If the hub is not configured, the hub's response to this request is undefined.

### 10.16.2.8 Set Hub Feature

This request sets a value reported in the hub status.

[tbl-246.md](tbl-246.md)

Setting a feature enables that feature; refer to Table 10-9 for the feature selector definitions that apply to the hub as recipient. Status changes may not be acknowledged using this request.

It is a Request Error if wValue is not a feature selector listed in Table 10-9 or if wIndex or wLength are not as specified above.

If the hub is not configured, the hub's response to this request is undefined.

### 10.16.2.9 Set Hub Depth

This request sets the value that the hub uses to determine the index into the Route String Index for the hub.

[tbl-247.md](tbl-247.md)

wValue has the value of the Hub Depth. The Hub Depth left shifted by two is the offset into the Route String that identifies the lsb of the Route String Port Field for the hub.

It is a Request Error if wValue is greater than 4 or if wIndex or wLength are not as specified above.

If the hub is not configured, the hub's response to this request is undefined.

### 10.16.2.10 Set Port Feature

This request sets a value reported in the port status.

[tbl-248.md](tbl-248.md)

The port number shall be a valid port number for that hub, greater than zero. The port number is in the least significant byte (bits 7..0) of the wIndex field. The most significant byte of wIndex is zero,

10-84