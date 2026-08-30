intel®

- P3 state: Selected internal clocks in the PHY can be turned off. The parallel interface is in an asynchronous mode and PCLK output is turned off.

PCLK as PHY output: When transitioning into P3, the PHY must assert the PhyStatus before PCLK is turned off and then deassert PhyStatus when PCLK is fully off and when the PHY is in the P3 state. When transitioning out of P3, the PHY asserts PhyStatus as soon as possible and leaves it asserted until after PCLK is stable.

PCLK as PHY input: When transitioning into P3, the PHY must assert PhyStatus for one input PCLK cycle when it is ready for PCLK to be removed. When transitioning out of P3, the PHY must assert PhyStatus for one input PCLK cycle as soon as possible once it has transitioned to P0 and is ready for operation.

PHYs should be implemented to minimize power consumption during P3 as this is when the device will have to operate within power limits described in the USB 3.0 Specification:

- The P3 state must be used in states SS.disabled and U3.
- There is a limited set of legal power state transitions that a MAC can ask the PHY to make. Referencing the main state diagram in the USB Specification and the mapping of link states to PHY power states described in the preceding paragraphs, those legal transitions are: P0 to P1, P0 to P2, P0 to P3, P1 to P0, P2 to P0, P2 to P3, P3 to P0, P3 to P2, and P1 to P2. The base specification also describes what causes those state transitions.

U1 has strict exit latency requirements as described in the USB 3.2 Specification.

Figure 8-11 illustrates the timing requirements for PIPE signals associated with U1 exit with the following explanation:

- T2-T1: PHY decodes LFPS and reflects it through RxElecIdle (120 ns maximum)
- T4-T3: P1 to P0 transition latency (300 ns maximum)
- T6-T5: LFPS transmit latency (100 ns maximum)
- T7-T1: 0.6–0.9 us from the USB Specification

120

Reference Number: 643108, Revision: 7.1