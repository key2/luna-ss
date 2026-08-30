intel®

- P3: Shutdown mode. This is the lowest PHY power consumption state.
- P4: Transmitter is off. This mode is suitable for usages with higher exit latency budgets. A typical usage is during PSR and Panel Replay deep sleep.

Table 8-2. DisplayPort PHY Power States

[tbl-131.md](tbl-131.md)

1. Where PLL is specified as ON/OFF, the MAC determines whether it should be on or off.

2. The total latency is defined as the time interval to enter a state and exit back to P0. The intention is to ensure the return to a fully active state in the case of wake event race scenario. Budget includes turn OFF and ON of PLL when the power state allows. In the case that the PHY has completed the entry phase, this delay can be considered as the exit latency budget in which the PHY can take extra power optimizations.

### 8.3.6 Asynchronous Deep Power Management

#### 8.3.6.1 Deep Power Management Control Handshake Sequencing

The PIPE specification enables deep power management states during certain PowerDown states by defining a set of asynchronous handshake signals DeepPMReq# and DeepPMAck#. During deep power management states, the PHY is permitted to take appropriate actions to reduce power such as clock gating, power gating, or power rail removal. By implementing Active State Deep Power Management (ASDPM) mechanisms, for instance, through latency tolerance reporting or workload monitoring, the MAC determines when it can tolerate higher exit latencies and subsequently notifies the PHY that it is permitted to enter a deep power management state by asserting DeepPMReq#. The PHY acknowledges this request immediately by asserting DeepPMAck#; the actual PHY entry to a deep power management state occurs after the DeepPMAck# is asserted, and it is possible that PHY internal conditions may prevent entry from ever happening. Since DeepPMReq# and DeepPMAck# are asynchronous signals, the PCLK is permitted to remain gated during transitions into and out of the deep power management states. The MAC directs the PHY to exit its deep power management state by deasserting DeepPMReq#. Upon detecting deassertion of DeepPMReq#, the PHY must exit its deep power management state and then signal that the exit has occurred by deasserting DeepPMAck#. The MAC confirms that the PHY is not in a deep power management state before transitioning PowerDown states; this enables PowerDown to always be used in a synchronous manner when the PCLK is a PHY input. Figure 8-12 illustrates the handshake sequencing for entering and exiting deep power management.

124

Reference Number: 643108, Revision: 7.1