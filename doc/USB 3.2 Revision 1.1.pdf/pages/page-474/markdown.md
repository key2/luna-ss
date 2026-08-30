Revision 1.1
June 2022

- 443 -

Universal Serial Bus 3.2
Specification

wLength bytes of the descriptor are returned; this is not considered an error even if wLength is zero.

It is a Request Error if wValue or wIndex are other than as specified above.

If the hub is not configured, the hub's response to this request is undefined.

### 10.16.2.4 Get Hub Status

This request returns the current hub status and the states that have changed since the previous acknowledgment.

[tbl-242.md](tbl-242.md)

The first word of data contains the wHubStatus field (refer to Table 10-10). The second word of data contains the wHubChange field (refer to Table 10-11).

It is a Request Error if wValue, wIndex, or wLength are other than as specified above.

If the hub is not configured, the hub's response to this request is undefined.

Table 10-10. Hub Status Field, wHubStatus

[tbl-243.md](tbl-243.md)

There are no defined feature selector values for these status bits and they can neither be set nor cleared by the USB system software.

Table 10-11. Hub Change Field, wHubChange

[tbl-244.md](tbl-244.md)

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.