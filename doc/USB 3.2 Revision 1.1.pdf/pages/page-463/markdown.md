Revision 1.1
June 2022

- 432 -

Universal Serial Bus 3.2
Specification

The hub class defines additional descriptors (refer to Section 10.15.2). In addition, vendor-specific descriptors are allowed in the USB device framework. Hubs support standard USB device commands as defined in Chapter 8.

A hub is the only device that is allowed to function at high-speed and a Gen X speed at the same time. This specification only defines the descriptors a hub shall report on the Enhanced SuperSpeed bus.

Note that an Enhanced SuperSpeed hub shall always support the Get Descriptor (BOS) (refer to Section 9.6.2) when operating at either the Gen X speed or at USB 2.0 speeds.

### 10.15.1 Standard Descriptors for Hub Class

The hub class pre-defines certain fields in standard USB descriptors. Other fields are either implementation-dependent or not applicable to this class.

A hub has a device descriptor with a bDeviceProtocol field set to 3 and an interface descriptor with a bInterfaceProtocol field set to 0.

Hub Descriptors for USB hub operating in SuperSpeed mode
Device Descriptor (SuperSpeed information)

[tbl-213.md](tbl-213.md)

BOS Descriptor

[tbl-214.md](tbl-214.md)

USB 2.0 Extension

[tbl-215.md](tbl-215.md)

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.