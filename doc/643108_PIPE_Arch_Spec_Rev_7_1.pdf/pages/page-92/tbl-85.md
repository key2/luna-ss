|  Bit | Default | Attribute | Required | Description  |   |   |   |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  [3] | 0h | Level | PCIe | **TxSwing:** This field controls transmitter voltage swing level.  |   |   |   |
|   |   |   |   |  Value |   | Description  |   |
|   |   |   |   |  0 |   | Full swing  |   |
|   |   |   |   |  1 |   | Low swing (optional)  |   |
|   |   |   |   |  Implementation of this signal is optional if only full swing is supported. This field is not used at the 8.0 GT/s or higher signaling rates.  |   |   |   |
|  [2:0] | 0h | Level | PCIe | **TxMargin[2:0]:** This field selects transmitter voltage levels.  |   |   |   |
|   |   |   |   |  [2] | [1] | [0] | Description  |
|   |   |   |   |  0 | 0 | 0 | TxMargin value 0 = Normal operating range  |
|   |   |   |   |  0 | 0 | 1 | TxMargin value 1 = 800–1200 mV for full swing OR 400-700 mV for Half swing  |
|   |   |   |   |  0 | 1 | 0 | TxMargin value 2 = required and vendor-defined  |
|   |   |   |   |  0 | 1 | 1 | TxMargin value 3 = required and vendor-defined  |
|   |   |   |   |  1 | 0 | 0 | TxMargin value 4 = required and 200–400 mV for full swing OR 100–200 mV for Half swing if the last value or vendor-defined  |
|   |   |   |   |  1 | 0 | 1 | TxMargin value 5 = optional and 200-400 mV for full swing OR 100-200 mV for Half swing if the last value or vendor-defined or reserved if no other values supported  |
|   |   |   |   |  1 | 1 | 0 | TxMargin value 6 = optional and 200–400 mV for full swing OR 100–200 mV for Half swing if the last value or vendor-defined or reserved if no other values supported  |
|   |   |   |   |  1 | 1 | 1 | TxMargin value 7 = optional and 200-400 mV for full swing or 100-200 mV for Half swing if the last value or reserved if no other values supported  |
|   |   |   |   |  PIPE implementations that only support PCIe mode and the 2.5 GT/s signaling rate do not implement this field.  |   |   |   |