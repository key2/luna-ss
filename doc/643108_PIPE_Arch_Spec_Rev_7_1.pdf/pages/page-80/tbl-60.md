|  Byte Address | Register Name | Notes  |
| --- | --- | --- |
|  12'h0 | RX1: Rx Margin Control0 | -  |
|  12'h1 | RX1: Rx Margin Control1 | -  |
|  12'h2 | RX1: Elastic buffer control | N/A for SerDes architecture  |
|  12'h3 | RX1: PHY Rx Control0 | N/A for SerDes architecture  |
|  12'h4 | RX1: PHY Rx Control1 | -  |
|  12'h5 | RX1: PHY Rx Control2 | -  |
|  12'h6 | RX1: PHY Rx Control3 | -  |
|  12'h7 | RX1: Elastic buffer location update frequency | N/A for SerDes architecture  |
|  12'h8 | RX1: PHY Rx Control4 | Some fields N/A for SerDes architecture  |
|  12'h9 | RX1: PHY Rx Control 5 | -  |
|  12'h10-12'h1FF | RX1: Reserved | -  |
|  12'h200 to 12'h3FF | RX2: Same registers are defined in this region for RX2 as for RX1 above. | -  |
|  12'h400 | TX1: PHY Tx Control0 | N/A for SerDes architecture  |
|  12'h401 | TX1: PHY Tx Control1 | N/A for SerDes architecture  |
|  12'h402 | TX1: PHY Tx Control2 | -  |
|  12'h403 | TX1: PHY Tx Control3 | -  |
|  12'h404 | TX1: PHY Tx Control4 | -  |
|  12'h405 | TX1: PHY Tx Control5 | -  |
|  12'h406 | TX1: PHY Tx Control6 | -  |
|  12'h407 | TX1: PHY Tx Control7 | -  |
|  12'h408 | TX1: PHY Tx Control8 | -  |
|  12'h409 | TX1: PHY Tx Control9 | -  |
|  12'h40A | TX1: PHY Tx Control10 | -  |
|  12'h40B-12'h5FF | TX1: Reserved | -  |
|  12'h600-12'h7FF | TX2: Same registers are defined in this region for TX2 as for TX1 in previous rows. | -  |
|  12'h800 | CMN1: PHY Common Control0 | N/A for SerDes architecture  |
|  12'h801 | PHY Near-end loopback control | -  |
|  12'h802-12'h9FF | CMN1: Reserved | -  |