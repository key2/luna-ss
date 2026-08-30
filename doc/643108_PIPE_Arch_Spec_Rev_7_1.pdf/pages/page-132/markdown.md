intel®

## 8.9 Transmitting LFPS – USB Mode

When the PHY is in P1 and the MAC wants to transmit LFPS, the MAC deasserts TxElecIdle and the PHY should generate valid LFPS until TxElecIdle is asserted. The MAC must assert TxElecIdle before transitioning the PHY to P0. The length of time TxElecIdle is deasserted is varied for different events. When the PHY is in P0 and the MAC wants to transmit LFPS, the MAC must assert both TxElecIdle and TxDetectRx/Loopback for the desired duration of an LFPS burst. The PHY is required to complete a full LFPS period before transitioning to SuperSpeed data, and, as a consequence, it may drop SuperSpeed data if these requests overlap. This requirement does not apply to TxOnesZeros requests. See Chapter 6 in the USB 3.0 specification for more details.

Figure 8-21. LFPS Transmit

![img-42.jpeg](img-42.jpeg)

## 8.10 Transmitting LFPS – USB4 and DisplayPort Modes

By default, the PHY is responsible for transmitting LFPS. See Section 8.24 for relevant PIPE control signals. The MAC can configure the PHY to allow the MAC to transmit LFPS on the parallel data interface TxData by setting the MacTransmitLFPS field in the PHY Common Control0 register prior to transitioning the link to P0 PowerDown state. The advantage of enabling the MAC to generate LFPS is that it provides easier timing control for switchover to high speed data at a clean LPFS cycle boundary. This section describes the sequence required for the MAC to use the parallel data interface to transmit LFPS.

Figure 8-22 illustrates the requirements that must be adhered to for the MAC to transmit LFPS. When the MAC wants to transmit LFPS, it must inform the PHY in advance (t1) by asserting TxDetectRxLoopback while TxElecIdle is asserted; this allows the PHY to make any internal transmitter adjustments necessary to meeting LFPS electrical requirements. The MAC must deassert TxElecIdle (t2) when it starts transmitting LFPS. When the MAC wants to resume transmitting regular high-speed data, it must inform the PHY in advance (t3) by asserting TxElecIdle and deasserting TxDetectRx/Loopback; this allows the PHY to make any internal transmitter adjustments necessary for high-speed data transmission. High-speed data transmission resumes when TxElecIdle deasserts (t4).

132

Reference Number: 643108, Revision: 7.1