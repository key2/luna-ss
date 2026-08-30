|  Name | Active Level | Description |   | Relevant Protocols  |
| --- | --- | --- | --- | --- |
|  PHY mode[3:0] | N/A | Selects the PHY operating mode. |   | PCIe, SATA, USB, DisplayPort, and USB4  |
|   |   |  Value | Description  |   |
|   |   |  0 | PCIe  |   |
|   |   |  1 | USB  |   |
|   |   |  2 | SATA  |   |
|   |   |  3 | DisplayPort  |   |
|   |   |  4 | Reserved  |   |
|   |   |  5 | Reserved  |   |
|   |   |  6 | Reserved  |   |
|   |   |  7 | USB4  |   |
|   |   |  All Others Reserved |   |   |
|   |   |  Implementation of this signal is not required for PHYs that only support a single mode.The MAC is permitted to change this signal only during Reset# assertion. This signal is asynchronous.  |   |   |
|  DP_mode_Tx_Rx | N/A | This signal is used to distinguish between DPTx and DPRx when PHY mode=0x3.A value of "0" specifies DPTx; a value of "1" specifies DPRx.The MAC is permitted to change this signal only during the Reset# assertion.This signal is asynchronous. |   | DisplayPort  |
|  SerDesArch | High | This signal indicates whether the SerDes architecture is enabled. Displayport and USB4 must always set this to "1".The MAC is permitted to change this signal only during the Reset# assertion.This signal is asynchronous. |   | PCIe, SATA, USB, DisplayPort, and USB4  |
|  SRISEnable | High | Used to tell the PHY to configure itself to support Separate Reference Clock (Refclk) with Independent Spread Spectrum Clocking (SRIS) for PCIe.SRISEnable must be set by the MAC before the first receiver detection. The PHY internally does sequencing and gates the exit to P0 with having setup for SRIS if SRISEnable is asserted.PHYs may have implementation-specific requirements for how early this signal must be stable, for example, before configuring the PLL. For PCIe Rev 5.0 and earlier MACs, this signal must not change after that point.For PCIe Rev 6.0 capable and newer MACs, this signal is permitted to change during link training in the Configuration LTSSM state. Specifically, this signal may be asserted initially and then deassert during link training. |   | PCIe  |