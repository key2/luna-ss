|  Field | TS1 and TS2 Symbol 5 | Description  |
| --- | --- | --- |
|  Bit 0 | 0 = Normal Training 1 = Reset | Reset is set by the Host only in order to reset the device.  |
|  Bit 1 | Set to 0 | Reserved for future use.  |
|  Bit 2 | 0 = Loopback de-asserted 1 = Loopback asserted | When set, the receiving component enters digital loopback. Upon assertion of bit 2 a re-timer shall be placed in pass through loopback mode.  |
|  Bit 3 | 0 = Disable Scrambling de-asserted 1 = Disable Scrambling asserted | When set, the receiving component disables scrambling. When this is asserted during Gen 2 operation the training Ordered Sets are still scrambled and the disabling of scrambling begins with the first Data Block after the SDS.  |
|  Bit 4 | 0 = Local loopback in repeater de-asserted 1 = Local loopback in repeater asserted | When set, the nearest repeater in the link is placed into local loopback mode.  |
|  Bit 5 | 0 = Bit-level re-timer Tx compliance mode de-asserted 1 = Bit-level re-timer Tx compliance mode asserted | When set, a bit-level re-timer is placed into transmit compliance mode defined in Appendix E. All other components (hosts, devices, dual role devices, non-bit-level re-timers) ignore this bit.  |
|  Bit 6:7 | Set to 0 | Reserved for future use.  |