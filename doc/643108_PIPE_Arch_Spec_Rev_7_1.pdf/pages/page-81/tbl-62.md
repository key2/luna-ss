|  Bit | Default | Attribute | Required | Description  |
| --- | --- | --- | --- | --- |
|  [7:5] | 0h | N/A | N/A | Reserved  |
|  [4] | 0h | Level | USB4 | **Voltage Margining Eye:** This field is used only for PAM3 signaling rates. This field indicates which of the eyes is being margined. 0 - Bottom Eye 1 - Top Eye  |
|  [3] | 0h | 1-cycle | PCIe (optional) | **Sample Count Reset:** This field is used to reset the "Sample Count[6:0]" field of the Rx Margin Status1 register.  |
|  [2] | 0h | 1-cycle | PCIe (optional) | **Error Count Reset:** This field is used to reset the "Error Count[5:0]" field of the Rx Margin Status2 register.  |
|  [1] | 0h | Level | PCIe | **Margin Voltage or Timing:** This field is used to select between margining voltage (1'b0) or margining timing (1'b1). The value can be changed only when margining is stopped.  |
|  [0] | 0h | Level | PCIe | **Start Margin:** This field is used to start and stop margining. A transition from 1'b0 to 1'b1 starts the margining process. A transition from 1'b1 to 1'b0 stops the margining process.  |