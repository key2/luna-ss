|  Name | Active Level | Description |   |   | Relevant Protocols  |
| --- | --- | --- | --- | --- | --- |
|  DataBusWidth[1:0] | N/A | This field reports the width of the data bus that the PHY is configured for. This field is optional. For Original PIPE architecture: |   |   | PCIe, SATA, USB, DisplayPort, and USB4  |
|   |   |  [1] | [0] | Description  |   |
|   |   |  0 | 0 | 32-bit mode  |   |
|   |   |  0 | 1 | 16-bit mode  |   |
|   |   |  1 | 0 | 8-bit mode  |   |
|   |   |  1 | 1 | Reserved  |   |
|   |   |  For SerDes architecture:  |   |   |   |
|   |   |  [1] | [0] | Description  |   |
|   |   |  0 | 0 | 10-bit mode  |   |
|   |   |  0 | 1 | 20-bit mode  |   |
|   |   |  1 | 0 | 40-bit mode  |   |
|   |   |  1 | 1 | 80-bit mode  |   |