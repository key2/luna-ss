Revision 1.1
June 2022

- 345 -

Universal Serial Bus 3.2
Specification

### 9.4.13 Synch Frame

This request is used to set and then report an endpoint's synchronization frame.

[tbl-174.md](tbl-174.md)

When an endpoint supports isochronous transfers, the endpoint may also require per-frame transfers to vary in size according to a specific pattern. The host and the endpoint must agree on which frame the repeating pattern begins. The number of the frame in which the pattern began is returned to the host.

If an Enhanced SuperSpeed device supports the Synch Frame request, it shall internally synchronize itself to the zero$^{th}$ microframe and have a time notion of classic frame. Only the frame number is used to synchronize and reported by the device endpoint (i.e., no microframe number). The endpoint must synchronize to the zero$^{th}$ microframe.

This value is only used for isochronous data transfers using implicit pattern synchronization. If wValue is non-zero or wLength is not two, then the behavior of the device is not specified.

If the specified endpoint does not support this request, then the device will respond with a Request Error.

Default state: Device behavior when this request is received while the device is in the Default state is not specified.

Address state: The device shall respond with a Request Error.

Configured state: This is a valid request when the device is in the Configured state.

### 9.4.14 Set Firmware Status

The default power on state of the device is that it allows firmware (FW) update. This write command is used to request the device to disallow or allow further firmware upgrades. The state is retained by the device until the next power on or receipt of the FLR command. This state survives the device entering selective suspend state.

[tbl-175.md](tbl-175.md)

### 9.4.15 Get Firmware Status

In response to this read command, depending on the wValue, the device returns the current status of the FW update allowed/disallowed state or the current image hash using SHA256 algorithm. The device is required to add minimal latency overhead with this request.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.