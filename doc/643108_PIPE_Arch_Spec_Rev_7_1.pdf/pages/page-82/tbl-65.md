|  Bit | Default | Attribute | Required | Description  |   |
| --- | --- | --- | --- | --- | --- |
|  [7:2] | 0h | N/A | N/A | Reserved  |   |
|  [1] | 0h | Level | PCIe, USB, and SATA | **RxPolarity:** This field is used to control the polarity inversion on the received data.  |   |
|   |   |   |   |  Value | Description  |
|   |   |   |   |  0 | The PHY does no polarity inversion.  |
|   |   |   |   |  1 | The PHY does polarity inversion.  |
|   |   |   |   |  **Note:** This field is not used in the SerDes architecture.  |   |