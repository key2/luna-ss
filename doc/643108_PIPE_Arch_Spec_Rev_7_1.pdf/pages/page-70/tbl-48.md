|  Name | Active Level | Description |   | Relevant Protocols  |
| --- | --- | --- | --- | --- |
|  RxWidth[2:0] | N/A | **This signal is only used in the SerDes architecture.** It controls the PIPE receive data path width. |   | PCIe, SATA, USB, USB4, and DisplayPort Rx  |
|   |   |  Value | Datapath Width  |   |
|   |   |  0 | 10 bits  |   |
|   |   |  1 | 20 bits  |   |
|   |   |  2 | 40 bits  |   |
|   |   |  3 | 80 bits (PCIe SerDes only)/56-bits USB4  |   |
|   |   |  4 | 160 bits  |   |
|   |   |  5-7 | Reserved  |   |
|   |   |  **Note:** PHYs that support greater than x4 link width must provide option of 32-bit data width or smaller. PIPE implementations that only support one option at each signaling rate do not implement this signal.  |   |   |