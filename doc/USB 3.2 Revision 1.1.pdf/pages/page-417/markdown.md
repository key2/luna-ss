Revision 1.1
June 2022

- 386 -

Universal Serial Bus 3.2
Specification

In the DSPORT-Powered-off state, the port's link is in the eSS.Disabled state.

Table 10-2 shows the allowed state of VBUS for hub downstream USB Standard-A ports for possible states of the hub upstream port and logical port power for a downstream USB Standard-A port. The table covers the case where the hub has adequate power to provide power for the downstream ports (local power source is present). For a hub that does not implement per port power control, all downstream ports that will be affected by removing VBUS shall be in a state where power may be off (refer to Table 10-2) before the hub removes VBUS.

Table 10-2. Downstream USB Standard-A Port VBUS Requirements

[tbl-210.md](tbl-210.md)

* If the hub upstream port is unable to connect on the USB 2.0 bus, the downstream port VBUS may be off in this state.

For downstream USB Type-C ports, the port power shall be on if:

((USB 2.0 Port Power On || USB 3.2 Port Power On) && (USB Type-C is in Attached.SRC))

A hub may provide power to its downstream ports all of the time to support power applications from a USB port. Such hubs must ensure that Enhanced SuperSpeed devices on its downstream-facing ports attempt Enhanced SuperSpeed connection once upstream VBUS is seen by the hub. The recommended method to achieve this is to cycle VBUS off for a duration or by actively discharging so that it is seen to be off by the downstream device.

### 10.3.1.2 DSPORT.Disconnected (Waiting for eSS Connect)

A port transitions to this state in any of the following situations:

- From the DSPORT-Powered-off state when the hub's Upstream Port link has detected far-end receiver terminations, Upstream Port VBUS is on (implied by receiver detection), no power-off condition is met and no Over-current condition exists.
- From any state that can and does detect a disconnect, except from DSPORT-Powered-off-detect.
- From the DSPORT-Powered-off-reset state when conditions for Repowering defined in Section 10.3.1.10 are met and the DSPORT-Powered-off-reset state has been maintained for tReset.
- From the DSPORT-Powered-off-detect state when conditions for Repowering defined in Section 10.3.1.10 are met.
- From the DSPORT.Resetting state when a port's link times out from Rx.Detect.Active during a reset. That is, it detects a disconnect.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.