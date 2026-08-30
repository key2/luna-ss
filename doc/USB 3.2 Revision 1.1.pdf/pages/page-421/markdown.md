Revision 1.1
June 2022

- 390 -

Universal Serial Bus 3.2
Specification

Note that Upstream Port VBUS is considered to have transitioned from off to on when it is on at power-up.

When no “power-off” condition is met and any of the following conditions are true, this state is entered regardless of the previous state.

- Over-current condition is detected either on this port or globally and Upstream Port Far-end Receiver Terminations are present and Upstream VBUS is on. Note: If Upstream VBUS is turned off while Over-current is active port transitions to Powered-off state immediately (without waiting for tReset to complete) if ds power switches are supported.
- Upstream Port VBUS is off and the hub does not support power switching.
- The hub receives a ClearPortFeature(PORT_POWER) request for this port. In this case, power is removed from the port only if it would not impact the low-speed, full-speed, or high-speed operation on any of the downstream ports on the hub and would not impact SS operation on any ports other than the target port.
- The hub upstream port receives a SetConfiguration(0) request. In this case the downstream port will stay in this state or transition between this state and DSPORT.Powered-off-reset state regardless of other conditions until the hub is reset or the hub upstream port receives a non-zero SetConfiguration request.

Note: If a USB Type-C port is implemented on the DFP and the respective USB 2.0 Hub port power is also logically off, the terminations, and therefore ability for Rx.Detect to complete, may be disabled due to the USB Type-C controller entering the USB Type-C Disabled state.

#### **10.3.1.11 DSPORT.Powered-off-reset**

This state is entered when the downstream power state is logically off and an Enhanced SuperSpeed connection, rather than a USB 2.0 connection, is desired. To ensure that an Enhanced SuperSpeed connection is established, unlike the DSPORT.Powered-off state, the terminations are maintained while in this state, and to avoid a link training failure, which would allow the downstream device to drop into Compliance Mode or USB 2.0 operation, Warm Reset signaling shall be driven for tReset duration. This state shall drive Warm Reset with the link in the Rx.Detect.Reset substate, until the tReset duration is met.

This state is entered from DSPORT.Powered-off-detect whenever a far end receiver is detected.

#### **10.3.2 Disconnect Detect Mechanism**

Disconnect detection mechanisms are covered in Section 7.5.

#### **10.3.3 Labeling**

USB system software uses port numbers to reference an individual port with a ClearPortFeature or SetPortFeature request. If a vendor provides a labeling to identify individual downstream facing ports, then each port connector shall be labeled with its respective port number. The port numbers assigned to a specific port by the hub shall be consistent between the USB 2.0 hub and Enhanced SuperSpeed hub.

It is recommended that all exposed physically identical (same connector type) downstream ports on a hub also provide identical capabilities, or that some method of labeling is provided that indicates the individual capability of each port to the end-user. If labeling is not practical for the product, then ports of differing capabilities should not be grouped together or co-located. Ports that are on the same side of a product should either present identical capabilities or they should be grouped by capability. Thus, identically capable

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.