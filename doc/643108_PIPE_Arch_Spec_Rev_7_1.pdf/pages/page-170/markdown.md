intel®

- In NELB mode, the controller must not perform any operations that require the use of the following:

- RxEIDetectDisable
- TxCommonModeDisable
- AsyncPowerChangeAck

- AlignDetect should continue to follow normal operation.
- Tx Pattern must continue to follow normal operation.
- PowerPresent must be set high in NELB mode.
- TxOneZeros must be low in NELB mode.

### 8.34.2 Entry and Exit from NELB Mode

The handshake sequence for Entry into NELB Mode is as follows:

1. MAC releases PIPE lane reset.
2. MAC moves to proper PowerDown state.
3. MAC writes to the PHY NELB Control register with position desired and enable set (PHY sends write Ack).
4. PHY does its internal setup for NELB.
5. PHY writes to the NELB Status register in the MAC, setting NELB State to 1 (MAC sends write Ack).
6. MAC now free to train in NELB.

The handshake sequence for exit from NELB is as follows:

- Option 1: MAC asserts PIPE lane reset OR
- Option 2: (The PHY must specify in its datasheet whether it supports this exit method)
  1. Mac moves to proper PowerDown state.
  2. MAC sends NELB Control message to PHY with enable cleared (PHY sends write Ack back).
  3. PHY does set up to move back to normal operation.
  4. PHY sends NELB Acknowledgment message to MAC, setting NELB State to 0 (MAC sends write Ack back).
  5. MAC now free to train in normal operation.

Handshake rules:

- Handshake must occur in a PowerDown state that has both Tx and Rx off but PCLK running.
- Handshake must complete prior to doing transmitter receiver detect if TxdetectRx is to be used.
- Handshake may be done at any data rate if supported by PHY. The PHY must support the handshake at initial protocol defined rate (for instance, 2.5GT/s for PCIe).
- If PHY is to report an error in the NELB Status register on entry, the state must indicate out of NELB, and the PHY must remain functionally in normal mode.

170

Reference Number: 643108, Revision: 7.1