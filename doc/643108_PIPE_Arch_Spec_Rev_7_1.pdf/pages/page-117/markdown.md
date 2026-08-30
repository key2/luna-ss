intel®

state where PCLK is not operational are described in following sections. For all power state transitions, the MAC must not begin any operational sequences or further power state transitions until the PHY has indicated that the initial state transition is completed.

Mapping of PHY power states to states in the LTSSM found in the PCIe Base Specification are included as follows. A MAC may alternately use PHY-specific states as long as the PCIe Base Specification requirements are still met:

- P0 state: All internal clocks in the PHY are operational. P0 is the only state where the PHY transmits and receives PCIe signaling.

P0 is the appropriate PHY power management state for most states in the LTSSM. Exceptions are listed in the following subsections for each lower power PHY state.

- P0s state: PCLK must stay operational. The MAC may move the PHY to this state only when the transmit channel is idle.

P0s state can be used when the transmitter is in the Tx_L0s.Idle state.

While the PHY is in either P0 or P0s power states, if the receiver is detecting an electrical idle, the receiver portion of the PHY can take appropriate power saving measures. The PHY must be capable of obtaining the bit and symbol lock within the PHY-specified time (N_FTS with or without common clock) upon resumption of signaling on the receive channel. This requirement only applies if the receiver had previously been bit and symbol-locked while in P0 or P0s states.

- P1 state: Selected internal clocks in the PHY can be turned off. The PCLK must stay operational. The MAC will move the PHY to this state only when both transmit and receive channels are idle. The PHY must not indicate a successful entry into the P1 (by asserting the PhyStatus) until PCLK is stable and the operating DC common mode voltage is stable and within specification (as per the PCIe Base Specification).

P1 can be used for the Disabled state, all the Detect states, and the L1.Idle state (only if the L1 substates are not supported) of the LTSSM.

- P2 state: Selected internal clocks in the PHY can be turned off. The parallel interface is in an asynchronous mode and PCLK is turned off. P2 can be used for the L1.Idle, L2.Idle, and L2.TransmitWake states of the LTSSM.

PCLK as PHY Output: When transitioning into a P2, the PHY must assert PhyStatus before the PCLK is turned off and then deassert PhyStatus when the PCLK is fully off and when the PHY is in the P2 state. When transitioning out of the P2, the PHY asserts PhyStatus as soon as possible and leaves it asserted until after PCLK is stable.

PCLK as PHY Input: When transitioning into P2, the PHY must assert PhyStatus for one input PCLK cycle when it is ready for PCLK to be removed. When transitioning out of P2, the PHY must assert PhyStatus for one input PCLK cycle as soon as possible once it has transitioned to P0 and is ready for operation.

When transitioning out of a state that does not provide PCLK to another state that does not provide PCLK, the PHY asserts PhyStatus as soon as the PHY state transition is complete and leaves it asserted until the MAC asserts AsyncPowerChangeAck. Once the MAC asserts AsyncPowerChangeAck the PHY deasserts PhyStatus.

PHYs should be implemented to minimize power consumption during P2 as this is when the device will have to operate within the vaux power limits (as described in the PCIe Base Specification).

Reference Number: 643108, Revision: 7.1

117