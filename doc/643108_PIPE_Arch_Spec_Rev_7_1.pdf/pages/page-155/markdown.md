intel®

Table 8-6. Control Signal Decode Table – USB Mode, USB4 Mode, and DisplayPort Mode (Sheet 2 of 2)

[tbl-143.md](tbl-143.md)

### 8.25 Control Signal Decode Table – SATA Mode

The following table summarizes the encodings of the control signals that cause different behaviors in POWER_STATE_0. For other control signals, Reset# always overrides any other PHY activity.

Note:

The PHY transmit latency reported in Section 8.20 must be consistent for all the different behaviors in POWER_STATE_0. This means that the amount of time OOB signaling is present on the analog Tx pair must be the same as the time OOB signaling was indicated on the PIPE interface.

Table 8-7. Control Signal Decode Table – SATA Mode

[tbl-144.md](tbl-144.md)

### 8.26 Required Synchronous Signal Timings

To improve interoperability between MACs and PHYs from different vendors the following timings for synchronous signals are required:

- Setup time for input signals: No greater than 25% of cycle time
- Hold time for input signals: 0 ns
- PCLK to data valid for outputs: No greater than 25% of cycle time

Reference Number: 643108, Revision: 7.1

155