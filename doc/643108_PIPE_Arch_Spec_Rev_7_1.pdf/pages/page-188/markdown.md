intel®

A MAC must use all "Per-Lane Signals or Shared Signals" that are inputs to the PHY consistently on all lanes in the link. A PHY in "PCLK as PHY Output" mode must ensure that PCLK and Max PCLK are synchronized across all lanes in the link. A MAC must provide a synchronized PCLK as an input for each lane when controlling a PHY in "PCLK as PHY Input" mode with no more than 300 ps of skew on PCLK across all lanes.

It is recommended that a MAC be designed to support both PHYs that implement all signals per lane and those that implement the "Per-Lane or Shared Signals" per link. A "Variable" PHY must implement the signals in "Per-Lane Signals or Shared Signals" per lane. A "Fixed" PHY may implement the signals in "Per-Lane Signals or Shared Signals" as either Shared or Per-Lane. A "Fixed" PHY should implement all the signals in "Per-Lane Signals or Shared Signals" consistently as either Shared or Per-Lane.

# **Note:**

The following method to turn off a lane using TxElecIdle and TxCompliance is deprecated; PowerDown is used instead. Alternatively, the PHY must hold itself in its lowest power state when Reset# is asserted; the MAC is permitted to choose this mechanism instead of PowerDown to turn off lanes not in use.

In cases where a multi-lane has been "trained" to a state where not all lanes are in use (like a x4 implementation operating in x1 mode), a special signaling combination is defined to "turn off" the unused lanes allowing them to conserve as much power as the implementation allows. This special "turn off" signaling is done using the TxElecIdle and TxCompliance signals. When both are asserted, that PHY can immediately be considered "turned off" and can take whatever power saving measures are appropriate. The PHY ignores any other signaling from the MAC (except for Reset# assertion) while it is "turned off". Similarly, the MAC should ignore any signaling from the PHY when the PHY is "turned off". There is no "handshake" back to the MAC to indicate that the PHY has reached a "turned off" state.

There are two normal cases when a lane can get turned off:

1. During LTSSM Detect state, the MAC discovers that there is no receiver present and will "turn off" the lane.
2. During LTSSM Configuration state (specifically Configuration.Complete), the MAC will "turn off" any lanes that did not become part of the configured link.

As an example, both cases could occur when a x4 device is plugged into a x8 slot. The upstream device (the one with the x8 port) will not discover receiver terminations on four of its lanes so it will turn them off. Training will occur on the remaining four lanes, and let's suppose that the x8 device cannot operate in x4 mode, so the link configuration process will end up settling on x1 operation for the link. Then both the upstream and downstream devices will "turn off" all but the one lane configured in the link.

When the MAC wants to get "turned off" lanes back into an operational state, there are two cases that need to be considered:

1. If the MAC wants to reset the multi-lane PIPE, it asserts Reset# and drives other interface signals to their proper states for reset (see Section 6.2). Note that this stops signaling "turned off" to all lanes because TxCompliance is deasserted during reset. The multi-lane PHY asserts PhyStatus in response to Reset# being asserted and will deassert PhyStatus when PCLK is stable.
2. When normal operation on the active lanes causes those lanes to transition to the LTSSM Detect state, then the MAC sets the PowerDown[1:0] signals to the P1 PHY power state at the same time that it deasserts "turned off" signaling to the inactive lanes. Then as with normal transitions to the P1 state, the multi-lane PHY will assert PhyStatus for one clock when all internal PHYs are in the P1 state and PCLK is stable.

188

Reference Number: 643108, Revision: 7.1