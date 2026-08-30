|  Bit | Default | Attribute | Required | Description  |
| --- | --- | --- | --- | --- |
|  [7:1] | 0h | N/A | N/A | Reserved  |
|  [0] | 1h^{1} | Level | USB4 and DisplayPort | **RxLaneEnable:** This field is set to "1" by the MAC to instruct the PHY to enable the receiver. The PHY indicates completion of this operation via the RxLaneReady register bit.  |