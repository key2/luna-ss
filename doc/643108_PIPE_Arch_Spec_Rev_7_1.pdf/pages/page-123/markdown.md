intel®

A minimum of five power states are defined, POWER_STATE_0 and a minimum of four additional states that meet minimum requirements defined in Section 6.1. The POWER_STATE_0 state is the normal operational state for the PHY. When directed from POWER_STATE_0 to a lower power state, the PHY can immediately take whatever power saving measures are appropriate.

For all state transitions between POWER_STATE_0 and lower power states that provide PCLK, the PHY indicates the successful transition into the designated power state by a single cycle assertion of **PhyStatus**. The PHY must complete transmitting all data transferred across the PIPE interface before the change in the PowerDown signals before an assertion of the **PhyStatus**. Transitions into and out-of-power state that does not provide PCLK are described as follows. For all power state transitions, the MAC must not begin any operational sequences or further power state transitions until the PHY has indicated that the initial state transition is completed. Power state transitions between two power states that do not provide PCLK are not allowed.

Mapping of PHY power states to link states in the SATA specification is MAC specific:

- POWER_STATE_0: All internal clocks in the PHY are operational. POWER_STATE_0 is the only state where the PHY transmits and receives SATA signaling. POWER_STATE_0 is the appropriate PHY power management state for most of the link states in the SATA specification. When transitioning into a power state that does not provide **PCLK**, the PHY must assert the **PhyStatus** before the **PCLK** is turned off and then deassert **PhyStatus** when PCLK is fully off and when the PHY is in the low power state. The PHY must leave the PCLK on for at least one cycle after asserting **PhyStatus**. For PCLK as PHY output, when transitioning out of a state that does not provide a PCLK, the PHY asserts **PhyStatus** as soon as possible and leaves it asserted until after **PCLK** is stable.

Transitions between any pair of PHY power states (except two states that do not provide PCLK) are allowed by PIPE. However, a MAC must ensure that SATA specification timing requirements are met.

### 8.3.5 Power Management - DisplayPort Mode

The power management signals allow the PHY to minimize power consumption. The PHY must meet all timing and electrical constraints provided in the DisplayPort specification regarding link states for the various power states.

Table 8-2 specifies required power states, which are defined to fully optimize the power consumption of eDP link states. A PHY is permitted to implement additional PHY specific power states. The MAC is permitted to use any of the PHY specific states as long as the Displayport specification requirements are still met. Transitions between any pair of PHY DisplayPort power states are allowed unless specifically prohibited.

The MAC controls the PLLs. The PLL is permitted to be turned off by the MAC in all the power states that allow the PLL to be off. Transition to a power state must not automatically result in the PLL being turned off.

Additional details of each power state are as follows:

- P0: Fully active power state. Transmitter is on.
- P1: Transmitter is off. This mode is suitable for low latency exit requirements.
- P2: Similar to P1 with a slightly larger total latency budget. The MAC is permitted to turn off the PLL in this mode as long as the latency requirements are met. The typical usage is expected to be during PSR and Panel Replay shallow sleep.

Reference Number: 643108, Revision: 7.1

123