intel®

Table 3-7. USB4 Mode – Possible PCLK or RXCLK Rates and Data Widths

[tbl-16.md](tbl-16.md)

1. While the data widths are 10, 20, or 40 bits for consistency with other protocols, USB4 only utilizes only 8 out of every 10 bits of data since it uses block encoding. See Section 6.1.1 for more details.

**Note:**

When a MAC that implements the TXDataValid signal is using a mode that does not use TXDataValid the MAC shall keep TXDataValid asserted. When a PHY that implements RXDataValid is in a mode that does not use RXDataValid the PHY mustkeep RXDataValid asserted.

There may be PIPE implementations that support multiples of these configurations. PHY implementations that support multiple configurations at the same rate must support the width and PCLK rate control signals. A PHY that supports multiple rates in PCIe mode or SATA mode or USB mode must support configurations across all supported rates that are fixed at the PCLK rate. A PHY that supports multiple rates in PCIe mode or SATA mode must support configurations across all supported rates that are fixed data path width.

Reference Number: 643108, Revision: 7.1

33