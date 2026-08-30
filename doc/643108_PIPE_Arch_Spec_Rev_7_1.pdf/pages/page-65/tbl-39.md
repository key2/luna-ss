|  Name | Active Level | Description |   |   |   | Relevant Protocols  |
| --- | --- | --- | --- | --- | --- | --- |
|  RxElecIdle2 | High | This corresponds to the Rx2 differential pair. See RxElecIdle2 for details. |   |   |   | USB4  |
|  RxStatus[2:0] | N/A | Encodes receiver status and error codes for the received data stream when receiving data. |   |   |   | PCIe, SATA, and USB  |
|   |   |  2 | 1 | 0 | Description  |   |
|   |   |  0 | 0 | 0 | Received data OK  |   |
|   |   |  0 | 0 | 1 | PCIe mode: 1 SKP added USB mode: 1 SKP ordered set added SATA mode: 1 ALIGN added Asserted with the first byte of ALIGN that was added. An align may only be added in conjunction with receiving one or more aligns in the data stream and only when the elasticity buffer is operating in half full mode.  |   |
|   |   |  0 | 1 | 0 | PCIe mode: 1 SKP removed USB mode: 1 SKP ordered set removed SATA mode: 1 or more ALIGNs removed This status is asserted with first non-ALIGN byte following an ALIGN. This status message is applicable to both EB buffer modes.  |   |
|   |   |  0 | 1 | 1 | PCIe and USB modes: Receiver detected SATA mode: Misalign Signaled on the first symbol of an ALIGN that was received misaligned in elasticity buffer nominal half full mode. Signaled on the first data following an align in elasticity buffer nominal empty mode.  |   |
|   |   |  1 | 0 | 0 | Both 8B/10B (128B/130B^{1}) decode error and (optionally) the receive disparity error. This error is never reported if EncodeDecodeBypass is asserted.  |   |
|   |   |  1 | 0 | 1 | Elastic Buffer Overflow  |   |
|   |   |  1 | 1 | 0 | Elastic buffer underflow: This error code is not used if the elasticity buffer is operating in the nominal buffer empty mode.  |   |
|   |   |  1 | 1 | 1 | Receive disparity error (Reserved if Receive Disparity error is reported with code 0b100.) Not used if EncodeDecodeBypass is asserted. For USB3 Gen2, it indicates "SKP Corrected".  |   |
|   |   |  **Note: The only status applicable to the SerDes architecture is "Receiver detected" (0x3).**  |   |   |   |   |
|  PowerPresent | High | USB mode: It indicates the presence of VBUS. Implementation of this signal is only required for PHYs that support the USB mode. |   |   |   | USB  |
|  PclkChangeOk | High | Only used when PCLK is a PHY input. Asserted by the PHY when it is ready for the MAC to change the PCLK rate or Rate or, if required, width. The PHY shall only assert this signal after the MAC has requested a PCLK rate change by changing PCLK_Rate or rate change by changing Rate or, if required, a width change by changing Width. This signal is not used for DisplayPort or USB4 mode. |   |   |   | PCIe, SATA, and USB  |