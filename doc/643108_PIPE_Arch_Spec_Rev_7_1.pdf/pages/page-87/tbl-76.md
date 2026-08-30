|  Bit | Default | Attribute | Required | Description  |
| --- | --- | --- | --- | --- |
|  [7:1] | 0h | N/A | N/A | Reserved  |
|  [0] | 0h | Level | USB | **TxOnesZeros:** This field is used when transmitting USB-compliance patterns CP7 or CP8. When this field is set, the transmitter is to transmit an alternating sequence of 50-250 ones and 50-250 zeros (regardless of the state of the TxData interface). This field is only applicable to 8b/10b modes. **Note:** This field is not used in the SerDes architecture.  |