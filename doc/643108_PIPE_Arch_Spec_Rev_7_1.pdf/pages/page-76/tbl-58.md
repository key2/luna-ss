|  Name | Active Level | Description |   | Relevant Protocols  |
| --- | --- | --- | --- | --- |
|  PCLK | Rising Edge | **This signal is relevant for "PCLK as PHY Output" mode only.** All data movement across the parallel interface is synchronized to this clock. This clock operates at a frequency set by PCLK Rate. The rising edge of the clock is the reference for all signals. The spread spectrum modulation on this clock is allowed. |   | PCIe, SATA, and USB  |
|  Max PCLK | Rising Edge | Parallel interface data clock. This fixed rate clock operates at the rate advertised in the PHY datasheet subject to the following limitations: PCIe mode: |   | PCIe, SATA, USB, DisplayPort, and USB4  |
|   |   |  **Max rate supported** | **Maximum Max PCLK**  |   |
|   |   |  2.5 GT/s | 250 MHz  |   |
|   |   |  5.0 GT/s | 500 MHz  |   |
|   |   |  8.0 GT/s | 1000 MHz  |   |
|   |   |  16.0 GT/s | 2000 MHz  |   |
|   |   |  32.0 GT/s | 4000 MHz  |   |
|   |   |  64.0 GT/s | 4000 MHz  |   |
|   |   |  128 GT/s | 4000 MHz  |   |
|   |   |  This clock is provided whenever PCLK is active. SATA mode:  |   |   |
|   |   |  **Max rate supported** | **Maximum Max PCLK**  |   |
|   |   |  1.5 GT/s | 150 MHz  |   |
|   |   |  3.0 GT/s | 300 MHz  |   |
|   |   |  6.0 GT/s | 600 MHz  |   |
|   |   |  This clock is provided whenever PCLK is active. USB mode:  |   |   |
|   |   |  **Max rate supported** | **Maximum Max PCLK**  |   |
|   |   |  5.0 GT/s | 500 MHz  |   |
|   |   |  10.0 GT/s | 1250 MHz  |   |
|   |   |  This clock is provided whenever the PCLK is active. USB4 mode:  |   |   |
|   |   |  **Max rate supported** | **Maximum Max PCLK**  |   |
|   |   |  10 GT/s | 1250 MHz  |   |
|   |   |  20 GT/s | 2500 MHz  |   |
|   |   |  Spread spectrum modulation on this clock is allowed. This signal is optional for most cases in "PCLK as PHY Output" mode and required for "PCLK as PHY Input" mode.  |   |   |