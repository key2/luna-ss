Revision 1.1
June 2022

- 389 -

Universal Serial Bus 3.2
Specification

Note: If the port initiates a hot reset on the link and the hot reset fails during the link Recovery state, a warm reset will be automatically tried. Refer to the Chapter 7 for details on this process. The port stays in the DSPORT.Resetting state throughout this process until the warm reset completes.

When the downstream port link enters Rx.Detect.Active during a warm reset, the hub shall start a timer to count the time it is in Rx.Detect.Active or Rx.Detect.Quiet. If this timer exceeds tTimeForResetError while the link remains in Rx.Detect, the port shall transition to the DSPORT.Disconnected state.

#### **10.3.1.7 DSPORT.Compliance**

A port transitions to this state in any of the following situations:

- When the link enters the Compliance Mode state.

#### **10.3.1.8 DSPORT.Loopback**

A port transitions to this state in any of the following situations:

- From the DSPORT.Training state if the loopback bit is set in the received TS2 ordered sets.

In this state, the port's link shall be in the Loopback state.

#### **10.3.1.9 DSPORT.Disabled**

A port transitions to this state when the port receives a SetPortFeature(PORT_LINK_STATE) eSS.Disabled request.

In this state, the port's link shall be in the eSS.Disabled state.

#### **10.3.1.10 DSPORT.Powered-off-detect**

This state is entered when the downstream power state is logically off and an Enhanced SuperSpeed connection, rather than a USB 2.0 connection, is desired. To ensure that an Enhanced SuperSpeed connection is established, unlike the DSPORT.Powered-off state, terminations are maintained while in this state. This is the default DSPORT state at power-up if the hub does not support power switching. This state shall perform far-end receiver detection with the link in Rx.Detect, until any of the following conditions are true:

- A receiver is detected.
- Any condition to "power-off" is met.
- The conditions to "repower" the port as described below are met.

A port shall transition into this state from the DSPORT.Powered-off-reset state when tReset time has been met and the conditions to "repower" are not met.

All the following conditions shall be met for "repower":

- All "power" conditions are met.
- SetPortFeature(PORT_POWER) request is received,
  Or SetConfig(1) request is received,
  Or Upstream Port Reset is detected,
  Or Upstream Port VBUS transitioned from off to on.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.