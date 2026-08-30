intel®

## 8.4 Changing Signaling Rate, PCLK Rate, or Data Bus Width

### 8.4.1 PCIe Mode

The signaling rate of the link, the PCLK rate, or the data bus width can be changed only when the PHY is in the P0 or P1 power state and TxElecIdle and RxStandby (P0 only) are asserted. When the MAC changes the Rate signal, and the Width signal, and/or the PCLK rate signal in the PCLK as the PHY Output mode, the PHY performs the rate change and the width change and the PCLK rate change and signals its completion with a single cycle assertion of PhyStatus. The MAC must not perform any operational sequences, power state transitions, deassert TxElecIdle or RxStandby, or further signaling rate changes until the PHY has indicated that the signaling rate change has completed. The sequence is the same in PCLK as PHY input mode except that the MAC needs to know when the input PCLK rate or rate, or potentially width, can be safely changed. After the MAC changes rate and either PCLK_Rate, data width, or both, any change to the PCLK can happen only after the PclkChangeOk output has been driven high by the PHY. The MAC changes the input PCLK, if necessary, and then handshakes by asserting PclkChangeAck. The PHY responds by asserting PhyStatus for one input PCLK cycle and deasserts PclkChangeOk on the trailing edge of PhyStatus.

Note:

PclkChangeOk is used by the PHY if the MAC changes PCLK_Rate and rate. The PHY datasheet indicates whether the same handshake is also required for every rate change.

Table 8-1 summarizes the handshake requirements. The MAC deasserts PclkChangeAck when PclkChangeOk is sampled low and may deassert TxElecIdle and/or RxStandby after PhyStatus is sampled high. There are instances where LTSSM state machine transitions indicate both a speed change or width or PCLK rate change and a power state change for the PHY. In these instances, the MAC must change (if necessary) the signaling rate, width and/or the PCLK rate before changing the power state.

Table 8-3. PclkChangeOK/PclkChangeAck Requirements

[tbl-132.md](tbl-132.md)

Some PHY architectures may allow a speed change and a power state change to occur at the same time as a rate, width, or PCLK rate change. If a PHY supports this, the MAC must change the rate, width, PCLK rate at the same PCLK edge that it changes the PowerDown signals. This can happen when transitioning the PHY from P0 to either P1 or P2 states. The completion mechanisms are the same as previously defined for the power state changes and indicate not only that the power state change is complete, but also that the rate, width, or rate change is complete.

126

Reference Number: 643108, Revision: 7.1