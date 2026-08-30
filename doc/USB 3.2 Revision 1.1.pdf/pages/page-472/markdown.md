Revision 1.1
June 2022

- 441 -

Universal Serial Bus 3.2
Specification

Table 10-9. Hub Class Feature Selectors

[tbl-238.md](tbl-238.md)

### 10.16.2.1 Clear Hub Feature

This request resets a value reported in the hub status.

[tbl-239.md](tbl-239.md)

Clearing a feature disables that feature; refer to Table 10-9 for the feature selector definitions that apply to the hub as a recipient. If the feature selector is associated with a status change, clearing that status change acknowledges the change. This request format is used to clear either the C_HUB_LOCAL_POWER or C_HUB_OVER_CURRENT features.

It is a Request Error if wValue is not a feature selector listed in Table 10-9 or if wIndex or wLength are not as specified above.

If the hub is not configured, the hub's response to this request is undefined.

### 10.16.2.2 Clear Port Feature

This request resets a value reported in the port status.

[tbl-240.md](tbl-240.md)

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.