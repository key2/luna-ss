intel®

when operating at 2.5 GT/s signaling rate, and 16-bit data paths when operating at 5.0 GT/s signaling rate. Another implementation choice is to use a fixed data path width and change the PCLK frequency to adjust the signaling rate. In this case, an implementation with 8-bit data paths would provide PCLK at 250 MHz for 2.5 GT/s signaling and provide PCLK at 500 MHz for 5.0 GT/s signaling. Similarly, an implementation with 16-bit data paths would provide PCLK at 125 MHz for 2.5 GT/s signaling and 250 MHz for 5.0 GT/s signaling. The sample list of possibilities is shown in Table 3-1.

For PIPE implementations that support 5.0 GT/s USB mode and 10 GT/s, USB mode implementers can choose from the options shown in Table 3-3. A PIPE compliant MAC or PHY is only required to support one option for each USB transfer speed that it supports.

For SATA PIPE implementations that support only the 1.5 GT/s signaling rate implementers can choose to have 16-bit data paths with PCLK running at 75 MHz, or 8-bit data paths with PCLK running at 150, 300 or 600 MHz. The 300 and 600 MHz options require the use of TXDataValid and RXDataValid signals to toggle the use of data on the data bus.

SATA PIPE implementations that support 1.5 GT/s signaling and 3.0 GT/s signaling in SATA mode, and therefore are able to switch between 1.5 GT/s and 3.0 GT/s signaling rates, can be implemented in several ways. An implementation may choose to have PCLK fixed at 150 MHz and use 8-bit data paths when operating at 1.5 GT/s signaling rate, and 16-bit data paths when operating at 3.0 GT/s signaling rate. Another implementation choice is to use a fixed data path width and change PCLK frequency to adjust the signaling rate. In this case, an implementation with 8-bit data paths could provide PCLK at 150 MHz for 1.5 GT/s signaling and provide PCLK at 300 MHz for 3.0 GT/s signaling. Similarly, an implementation with 16-bit data paths would provide PCLK at 75 MHz for 1.5 GT/s signaling and 150 MHz for 3.0 mode are shown GT/s signaling. A sample list of possible widths and PCLK rates for SATA is shown in Table 3-4. A PIPE compliant MAC or PHY is only required to support one option for each SATA transfer speed that it supports.

A sample list of possible data width and PCLK rate combinations for PCIe mode is shown in Table 3-1; other combinations are possible as long as they conform to the PIPE definitions and the combination of PCLK rate, data width, and TXDataValid/RXDataValid strobes match the bandwidth across the serial link. A PIPE compliant MAC or PHY is only required to support one option for each PCIe transfer speed that it supports.

Note: PHYs that support greater than x4 link widths must provide an option for 32-bit or less data width.

Table 3-1. PCIe Mode - Possible PCLK Rates and Data Widths (Sheet 1 of 3)

[tbl-6.md](tbl-6.md)

28

Reference Number: 643108, Revision: 7.1