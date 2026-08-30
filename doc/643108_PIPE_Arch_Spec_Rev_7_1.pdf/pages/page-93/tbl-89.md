|  Bit | Default | Attribute | Required | Description  |
| --- | --- | --- | --- | --- |
|  [7:2] | 0h | N/A | N/A | Reserved  |
|  [1] | 0h | N/A | DisplayPort and USB4 | **MacTransmitLFPS:** This field controls whether the PHY or the MAC transmit the LFPS. 0 – PHY transmits LFPS 1 – MAC transmits LFPS The MAC must only change this when LFPS is not transmitting, and the MAC must not transmit LFPS at least 10 us after changing this bit.  |