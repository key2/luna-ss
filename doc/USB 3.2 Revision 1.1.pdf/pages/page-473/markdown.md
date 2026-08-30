Revision 1.1
June 2022

- 442 -

Universal Serial Bus 3.2
Specification

The port number shall be a valid port number for that hub, greater than zero. The port field is located in bits 7..0 of the wIndex field.

Clearing a feature disables that feature or starts a process associated with the feature; refer to Table 10-9 for the feature selector definitions. If the feature selector is associated with a status change, clearing that status change acknowledges the change. This request format is used to clear the following features:

- PORT_POWER
- C_PORT_CONNECTION
- C_PORT_RESET
- C_PORT_OVER_CURRENT
- C_PORT_LINK_STATE
- C_PORT_CONFIG_ERROR
- C_BH_PORT_RESET
- FORCE_LINKPM_ACCEPT

Clearing the PORT_POWER feature causes the port to be placed in the DSPORT-Powered-off-reset state and may, subject to the constraints due to the hub's method of power switching, result in power being removed from the port. When in the DSPORT-Powered-off or the DSPORT-Powered-off-detect or the DSPORT-Powered-off-reset state, the only requests that are valid when this port is the recipient are Get Port Status (refer to Section 10.16.2.6) and Set Port Feature (PORT_POWER) (refer to Section 10.16.2.10).

Clearing the FORCE_LINKPM_ACCEPT feature causes the port to de-assert the Force_LinkPM_Accept bit in Set Link Function LMPs. If the Force_LinkPM_Accept bit is not asserted on the port, the hub shall treat this request as a functional no-operation.

It is a Request Error if wValue is not a feature selector listed in Table 10-9, if wIndex specifies a port that does not exist, or if wLength is not as specified above. It is not an error for this request to try to clear a feature that is already cleared (the hub shall treat this as a functional no-operation).

If the hub is not configured, the hub's response to this request is undefined.

### 10.16.2.3 Get Hub Descriptor

This request returns the hub descriptor.

[tbl-241.md](tbl-241.md)

The GetDescriptor() request for the hub class descriptor follows the same usage model as that of the standard GetDescriptor() request (refer to Chapter 9). The standard hub descriptor is denoted by using the value bDescriptorType defined in Section 10.15.2.1. All hubs are required to implement one hub descriptor, with descriptor index zero.

If wLength is larger than the actual length of the descriptor, then only the actual length is returned. If wLength is less than the actual length of the descriptor, then only the first

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.