|  Bit | Default | Attribute | Required | Description  |
| --- | --- | --- | --- | --- |
|  [7:1] | 0h | N/A | N/A | Reserved  |
|  [0] | 1h^{1} | Level | USB4 and DisplayPort | **TxLaneEnable:** This field is set to "1" by the MAC to instruct the PHY to enable the transmitter. The MAC is permitted to enable or disable a transmitter in any power state while TxElecIdle is asserted. The PHY indicates completion of this operation via the TxLaneReady register bit.  |