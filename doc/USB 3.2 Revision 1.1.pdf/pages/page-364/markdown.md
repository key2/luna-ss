Revision 1.1
June 2022

- 333 -

Universal Serial Bus 3.2
Specification

The INTERFACE_POWER descriptor is defined in the current revision of the USB Interface Power Management Specification.

Feature selectors are used when enabling or setting features, such as function remote wakeup, specific to a device, interface, or endpoint. The values for the feature selectors are given in Table 9-7.

Table 9-7. Standard Feature Selectors

[tbl-153.md](tbl-153.md)

$^{1}$ This Feature Selector value shall be reserved for OTG use. Refer to Section 6.4 of the USB 3.0 OTG and EH Supplement for its definition.

If an unsupported or invalid request is made to a device, the device responds by returning a STALL Transaction Packet in the Data or Status stage of the request. If the device detects the error in the Setup stage, it is preferred that the device returns a STALL Transaction Packet at the earlier of the Data or Status stage. Receipt of an unsupported or invalid request does not cause the Halt feature on the control pipe to be set. If, for any reason, the device becomes unable to communicate via its Default Control Pipe due to an error condition, the device shall be reset to clear the condition and restart the Default Control Pipe.

### 9.4.1 Clear Feature

This request is used to clear or disable a specific feature.

[tbl-154.md](tbl-154.md)

Feature selector values in wValue shall be appropriate to the recipient. Only device feature selector values may be used when the recipient is a device, only interface feature selector

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.