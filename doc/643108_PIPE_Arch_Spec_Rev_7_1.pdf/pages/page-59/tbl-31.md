|  Name | Active Level | Description |   | Relevant Protocols  |
| --- | --- | --- | --- | --- |
|  Width[2:0] | N/A | Controls the PIPE data path width. For SerDes architecture, this applies only to the transmit side and RxWidth[1:0] controls the receive side. If EncodeDecodeBypass is "0", use the following encodings. |   | PCIe, SATA, USB, USB4 DisplayPort TX  |
|   |   |  Value | Datapath Width  |   |
|   |   |  0 | 8 bits  |   |
|   |   |  1 | 16 bits  |   |
|   |   |  2 | 32 bits  |   |
|   |   |  3-7 | Reserved  |   |
|   |   |  If EncodeDecodeBypass is "1" or in SerDes architecture, use the following encodings.  |   |   |
|   |   |  Value | Datapath Width  |   |
|   |   |  0 | 10 bits  |   |
|   |   |  1 | 20 bits  |   |
|   |   |  2 | 40 bits  |   |
|   |   |  3 | 80 bits (PCIe SerDes only)/56 bits (USB4 only)  |   |
|   |   |  4 | 160bits (PCIe SerDes only)  |   |
|   |   |  5-7 | Reserved  |   |
|   |   |  **Note:** PHYs that support greater than x4 link width must provide option of 32-bit data width or smaller. PIPE implementations that only support one option at each signaling rate do not implement this signal.  |   |   |