intel®

# 8 PIPE Operational Behavior

## 8.1 Clocking

There are three clock signals used by the PHY interface component. The first clock (CLK) is a reference clock that the PHY uses to generate internal bit rate clocks for transmitting and receiving data. The specifications for this signal are implementation-dependent and must be fully specified by vendors. The specifications may vary for different PHY operating modes. This clock may have a spread spectrum modulation that matches a system Reference Clock (REFCLK) (for example, the spread spectrum modulation could come from a REFCLK from the Card Electro-Mechanical Specification [CEMS]).

The second clock (PCLK) is an output from the PHY in "PCLK as PHY Output" mode and an input to each PHY lane in the "PCLK as PHY Input" mode and is the parallel interface clock used to synchronize data transfers across the parallel interface. This clock runs at a rate dependent on the Rate, PCLK Rate, and PHY Mode control inputs and data interface width. The rising edge of this clock is the reference point. This clock may also have a spread spectrum modulation. The CLK and PCLK must be sourced from the same reference clock and must contain the same clocking characteristics, that is, they can be mesochronous with each other.

The third clock (MAX PCLK) is a constant frequency clock with a frequency determined by the maximum signaling rate supported by the PHY and is only required in "PCLK as PHY Input" mode or in all modes for a PHY that supports PCIe at 8 GT/s or higher maximum speed. The Max PCLK value should be set to the maximum PCLK supported by the PHY.

The fourth clock (MacCLK) is an optional clock with support advertised by the PHY vendor parameter "MacCLK Support". This clock is independent of the data lanes and is specified using MacCLK lane signals.

### 8.1.1 Clocking Topologies

This section describes some clocking topologies that are compatible with PIPE. Figure 8-1 shows PCLK as a PHY output. This topology is only applicable for legacy PIPE implementations and is not supported for PCIe Gen5 designs, USB4 or DisplayPort. Figure 8-2 shows PCLK as a PHY input with the PLL residing in the PHY; the PHY provides a source for PCLK, in this case, MAX PCLK, that is mesochronous to the PHY's bit rate clock. Figure 8-3 shows the PCLK as a PHY input with the PLL that provides the PCLK source residing outside of the PHY; the reference clock for PLL that sources the bit rate clock and the PLL that provides the PCLK source must be the same. Figure 8-4 shows CLK as a PHY input with a single PLL that provides the source for PCLK as well as for the bit rate clock.

110

Reference Number: 643108, Revision: 7.1