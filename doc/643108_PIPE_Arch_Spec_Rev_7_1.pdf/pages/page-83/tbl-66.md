|  Bit | Default | Attribute | Required | Description  |   |
| --- | --- | --- | --- | --- | --- |
|  [0] | 0h | Level | PCIe (optional), SATA (optional), and USB (optional) | **Elasticity Buffer Mode:** This field is used to select the elasticity buffer operating mode.  |   |
|   |   |   |   |  Value | Description  |
|   |   |   |   |  0 | Nominal half full buffer mode  |
|   |   |   |   |  1 | Nominal empty buffer Mode  |
|   |   |   |   |  This field can only be changed when the receiver is OFF and the Pclk is running, for example, the P0 with RXStandby is asserted or P1. This field is not valid when TxDetectRx/Loopback is asserted. The PHY is responsible for switching to Nominal Half Full Buffer mode when loopback follower is requested. The Process Control System (PCS) is responsible for making the stream switch and abiding by the *PCIe Base Specification* rules for follower loopback stream switching, for instance, switch on the 10b boundary in 8b/10b modes. **Note:** This field is not used in the SerDes architecture. |   |