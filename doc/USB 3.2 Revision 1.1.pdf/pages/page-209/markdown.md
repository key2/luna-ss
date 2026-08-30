Revision 1.1
June 2022

- 178 -

Universal Serial Bus 3.2
Specification

### 7.5.4.6.1 Polling.PortConfig Requirements

- Upon entry to this state, the port shall place its transmitter in electrical idle if it is preparing its PHY re-configuration according to PHY Capability LBPM negotiated in Polling.PortMatch. The port shall perform the following PHY re-configuration.

1. The transmitter DC common mode voltage shall be within specification (V_TX-CM-DCACTIVE-IDLE-DELTA) defined in Table 6-19.
2. The port shall maintain its low-impedance receiver termination (R_RX-DC) defined in Table 6-22.
3. The port shall be ready to transmit TSEQ OS on each negotiated lane.
4. The port shall be ready to receive TSEQ OS for receiver equalization training on each negotiated lane.
5. The port configured to x2 operation shall have both lanes ready for link training.

- The port shall monitor the received LBPM and perform the PHY Ready LBPM handshake. It is defined by the port sending four consecutive and identical PHY Ready LBPMs after receiving two consecutive and identical PHY Ready LBPMs.

- The operation of the 12-ms timer (tPollingLBPMLFPSTimeout) shall continue without reset upon entry to the substate from Polling.PortMatch. In x2 operation, additional rules in the following apply.

○ A downstream port shall continue the tPollingLBPMLFPSTimeout timer without reset when sending the PHY Ready LBPM with bit-7 de-asserted.
○ A downstream port shall reset the tPollingLBPMLFPSTimeout timer upon completing the PHY Ready LBPM handshake with bit-7 of its PHY Ready LBPM asserted. It shall re-start the tPollingLBPMLFPSTimeout timer when it is ready to exit to Polling.RxEQ by transmitting the PHY Ready LBPM with bit-7 de-asserted. Note that the duration of RT Config is managed by DFP upper layer.
○ An upstream port shall reset the tPollingLBPMLFPSTimeout timer and remain in this substate upon completing the PHY Ready LBPM handshake and detecting bit-7 of the PHY Ready LBPM from DFP is asserted.

- In x2 operation, a downstream port shall initiate the re-timer presence announcement as defined in Appendix E. If it has bit-7 of the PHY Ready LBPM handshake asserted, a downstream port shall remain in this substate after completing the PHY Ready LBPM handshake. Note that this is an intermediate state for DFP to perform additional operations in future revisions. A downstream port shall transmit PHY Ready LBPM with bit 7 de-asserted if it's ready to transition to Polling.RxEQ.

- In x2 operation, upon completing the PHY Ready LBPM handshake with bit-7 of the PHY Ready LBPM from DFP asserted, an upstream port shall perform the following.

○ It shall remain in this substate, keep its transmitter in LFPS EI, and continue to look for the received PHY Ready LBPM from DFP with bit-7 de-asserted. Note that DFP may send non PHY Ready LBPM or remain in LFPS EI during this period of time. Shown in Figure 7-20 are example timing diagrams of the port in x2 operation.
○ Upon detecting PHY Ready LBPM from DFP with bit-7 de-asserted, it shall prepare itself to exit to Polling.RxEQ and respond with PHY Ready LBPM to complete the PHY Ready LBPM handshake.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.