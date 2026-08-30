|  Field | TS1 Symbol 5 | Description  |
| --- | --- | --- |
|  Bit 0 | 0 = Normal Training 1 = Reset | Reset is set by the Host only in order to reset the device.  |
|  Bit 1 | Set to 0 | Reserved for future use.  |
|  Bit 2 | 0 = Loopback de-asserted 1 = Loopback asserted | When set, the receiving component enters digital loopback.  |
|  Bit 3 | 0 = Disable Scrambling de-asserted 1 = Disable Scrambling asserted | When set, the receiving component disables scrambling. When this is asserted during Gen 2 operation the training Ordered Sets are still scrambled and the disabling of scrambling begins with the first Data Block after the SDS.  |
|  Bit 4 | 0 = Local loopback in repeater de-asserted 1 = Local loopback in repeater asserted | When set, the nearest repeater in the link is placed into local loopback mode.  |
|  Bit 5:7 | Set to 0 | Reserved for future use.  |