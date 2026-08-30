intel®

# 6 PIPE Interface Signal Descriptions

The PHY input and output signals are described in the following tables. Note that Input/Output is defined from the perspective of a PIPE compliant PHY component. Therefore, a signal described as an "Output" is driven by the PHY and a signal described as an "Input" is received by the PHY. A basic description of each signal is provided. More details on their operation and timing can be found in following sections. All signals on the "parallel" side of a PIPE implementation are synchronous with PCLK, with exceptions noted in the following tables. In the SerDes architecture, RxData is synchronous with RxCLK. The PHYs that only support SerDes architecture do not require the signals marked as "not used in the SerDes architecture"; however, the PHYs that support both original PIPE and SerDes architecture must implement all the signals. Each signal has a column that indicates the relevant protocols; USB refers to USB 3.2 and lower, while USB4 is indicated separately.

As described in Section 2.8, up to two differential pairs are operational at any given time. For PIPE control signals that refer to Rx functionality, a control signal applies to both Rx and Rx2 unless separate control signals are defined for each of the differential pairs. For PIPE control signals that refer to Tx functionality, a control signal applies to both Tx and Tx2 unless separate control signals are defined for each of the two differential pairs.

Note:

For USB4 and DisplayPort, the low speed side channel is not part of the PIPE definition, however, the appendix lists the DisplayPort AUX signals.

## 6.1 PHY/MAC Interface Signals – Common for SerDes and Original PIPE

This section describes signals that are applicable to both SerDes architecture and original PIPE. Any deltas in usage between the two architectures are noted in the description.

Reference Number: 643108, Revision: 7.1

45