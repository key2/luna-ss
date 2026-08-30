Revision 1.1
June 2022

- 385 -

Universal Serial Bus 3.2
Specification

[tbl-209.md](tbl-209.md)

### 10.3.1 Hub Downstream Facing Port State Descriptions

#### 10.3.1.1 DSPORT-Powered-off

The DSPORT-Powered-off state is a logical powered off state. This is a default state where DSPORT port will be after power-up if the hub supports power switching. The hub may still be required or choose to provide VBUS for a downstream port in the DSPORT-Powered-off state. Detailed requirements for presence of VBUS are covered later in this section.

A port shall transition into this state if any of the following situations occur:

- From any state when VBUS is removed from the hub upstream port and the hub supports power switching on the DS ports.
- Any "power-off" condition is met:
  - From any state when local power is lost to the port.
  - From any state if the hub's upstream port link transitions to the eSS.Disabled state and Upstream PORT VBUS is on.
  - From any state if the hub's upstream port link has attempted eight consecutive Rx.Detect events without detecting far-end receiver terminations and the receiver termination (near-end) of the hub's downstream port is ready to be turned off.

The downstream port's termination is considered to be ready to turn off when any of following conditions is met.

- Warm reset signaling has completed.
- Optionally when the port is power switched and the USB 2.0 hub has also turned off power to the port.
- The port is in a powered on state and not performing a warm reset
- No device is connected.

A port shall remain in the DSPORT-Powered-off state until the following conditions are met.

- The hub's Upstream Port link has detected far-end receiver terminations. Note that this requires Upstream Port VBUS to be on.
- No "power-off" condition is true.
- No Over-current condition is active.

If a hub was configured while the local power source was present and then if local power is lost, the hub shall place all ports in the Powered-off state if power remains to run the hub controller.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.