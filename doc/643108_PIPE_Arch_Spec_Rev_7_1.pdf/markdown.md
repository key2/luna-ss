![img-0.jpeg](img-0.jpeg)

# PHY Interface for the PCI Express*, SATA, USB 3.2, DisplayPort*, and USB4* Architectures

Specification

September 2025

Revision 7.1

Reference Number: 643108

![img-1.jpeg](img-1.jpeg)

#### Intellectual Property Disclaimer

**THIS SPECIFICATION IS PROVIDED "AS IS" WITH NO WARRANTIES WHATSOEVER INCLUDING ANY WARRANTY OF MERCHANTABILITY, FITNESS FOR ANY PARTICULAR PURPOSE, OR ANY WARRANTY OTHERWISE ARISING OUT OF ANY PROPOSAL, SPECIFICATION, OR SAMPLE.**

**A COPYRIGHT LICENSE IS HEREBY GRANTED TO REPRODUCE AND DISTRIBUTE THIS SPECIFICATION FOR INTERNAL USE ONLY. NO OTHER LICENSE, EXPRESS OR IMPLIED, BY ESTOPPEL OR OTHERWISE, TO ANY OTHER INTELLECTUAL PROPERTY RIGHTS IS GRANTED OR INTENDED HEREBY.**

**INTEL CORPORATION AND THE AUTHORS OF THIS SPECIFICATION DISCLAIM ALL LIABILITY, INCLUDING LIABILITY FOR INFRINGEMENT OF PROPRIETARY RIGHTS, RELATING TO IMPLEMENTATION OF INFORMATION IN THIS DOCUMENT AND THE SPECIFICATION. INTEL CORPORATION AND THE AUTHORS OF THIS SPECIFICATION ALSO DO NOT WARRANTY OR REPRESENT THAT SUCH IMPLEMENTATION(S) WILL NOT INFRINGE SUCH RIGHTS.**

**INTEL CORPORATION MAY MAKE CHANGES TO SPECIFICATIONS, PRODUCT DESCRIPTIONS, AND PLANS AT ANY TIME, WITHOUT NOTICE.**

Intel Corporation and its subsidiaries (collectively, "Intel") would like to receive input, comments, suggestions and other feedback (collectively, "Feedback") on this specification. To be considered for incorporation into the specification, Feedback must be submitted by e-mail to: pipespecification@intel.com. To the extent that You provide Intel with Feedback, You grant to Intel a worldwide, non-exclusive, perpetual, irrevocable, royalty-free, fully paid, transferable license, with the right to sublicense, under Your Intellectual Property Rights, to make, use, sell, offer for sale, import, disclose, reproduce, make derivative works, distribute, or otherwise exploit Your Feedback without any accounting. As used in this paragraph, "Intellectual Property Rights" means, all worldwide copyrights, patents, trade secrets, and any other intellectual or industrial property rights, but excluding any trademarks or similar rights. By submitting Feedback, you represent that you are authorized to submit Feedback on behalf on your employer, if any, and that the Feedback is not confidential.

**Notice:** Implementations developed using the information provided in this specification may infringe the patent rights of various parties including the parties involved in the development of this specification. No license, express or implied, by estoppel or otherwise, to any intellectual property rights (including without limitation rights under any party's patents) are granted herein.

Intel does not control or audit third-party benchmark data or the web sites referenced in this document. You should visit the referenced web site and confirm whether referenced data are accurate.

Copies of documents which have an order number and are referenced in this document may be obtained by calling 1-800-548-4725 or by visiting www.intel.com/design/literature.htm.

Intel, the Intel logo, and Thunderbolt are trademarks of Intel Corporation or its subsidiaries.

*Other names and brands may be claimed as the property of others

Copyright © 2025, Intel Corporation. All Rights Reserved.

2

Reference Number: 643108, Revision: 7.1

intel.

# Contents

[tbl-0.md](tbl-0.md)

Reference Number: 643108, Revision: 7.1

3

intel®

7.1.17 Address 406h: PHY Tx Control6 ...91
7.1.18 Address 407h: PHY Tx Control7 ...91
7.1.19 Address 408h: PHY Tx Control8 ...91
7.1.20 Address 409h: PHY Tx Control9 ...92
7.1.21 Address 40Ah: PHY TX Control 10 ...93
7.1.22 Address 800h: PHY Common Control0 ...93
7.1.23 Address 801h: PHY Near End Loopback Control ...94
7.2 MAC Registers ...95
7.2.1 Address 0h: Rx Margin Status0 ...97
7.2.2 Address 1h: Rx Margin Status1 ...97
7.2.3 Address 2h: Rx Margin Status2 ...97
7.2.4 Address 3h: Elastic Buffer Status ...98
7.2.5 Address 4h: Elastic Buffer Location ...98
7.2.6 Address 5h: Rx Status0 ...98
7.2.7 Address 6h: Rx Control0 ...99
7.2.8 Address 7h: Rx Margin Status3 ...99
7.2.9 Address Ah: Rx Link Evaluation Status0 ...100
7.2.10 Address Bh: Rx Link Evaluation Status1 ...100
7.2.11 Address Ch: Rx Status4 ...101
7.2.12 Address Dh: Rx Status5 ...102
7.2.13 Address Eh: Rx Link Evaluation Status2 ...102
7.2.14 Address Fh: Rx Link Evaluation Status3 ...103
7.2.15 Address 10h: Rx Status6 ...104
7.2.16 Address 400h: Tx Status0 ...104
7.2.17 Address 401h: Tx Status1 ...105
7.2.18 Address 402h: Tx Status2 ...105
7.2.19 Address 403h: Tx Status3 ...106
7.2.20 Address 404h: Tx Status4 ...106
7.2.21 Address 405h: Tx Status5 ...106
7.2.22 Address 406h: Tx Status6 ...106
7.2.23 Address 407h: Tx Status7 ...107
7.2.24 Address 408h: Tx Status8 ...107
7.2.25 Address 409h: Tx Status9 ...107
7.2.26 Address 40Ah: Tx Status10 ...107
7.2.27 Address 40Bh: Tx Status11 ...108
7.2.28 Address 40Ch: Tx Status12 ...108
7.2.29 Address 800h: Near End Loopback Status ...108
8 PIPE Operational Behavior ...110
8.1 Clocking ...110
8.1.1 Clocking Topologies ...110
8.1.2 MacCLK Clocking Scheme ...114
8.2 Reset ...116
8.3 Power Management ...116
8.3.1 Power Management – PCIe Mode ...116
8.3.2 Power Management – USB Mode ...119
8.3.3 Power Management – USB4 Mode ...121
8.3.4 Power Management – SATA Mode ...122
8.3.5 Power Management – DisplayPort Mode ...123
8.3.6 Asynchronous Deep Power Management ...124
8.4 Changing Signaling Rate, PCLK Rate, or Data Bus Width ...126
8.4.1 PCIe Mode ...126
8.4.2 USB Mode ...127
8.4.3 SATA Mode ...127
8.4.4 Fixed Data Path Implementations ...128

4

Reference Number: 643108, Revision: 7.1

intel.

8.4.5 Fixed PCLK Implementations... 128
8.5 Transmitter Margining – PCIe Mode and USB Mode ... 129
8.6 Selectable De-Emphasis – PCIe Mode... 130
8.7 Receiver Detection – PCIe Mode and USB Mode ... 130
8.8 Transmitting a Beacon – PCIe Mode... 131
8.9 Transmitting LFPS – USB Mode ... 132
8.10 Transmitting LFPS – USB4 and DisplayPort Modes... 132
8.11 Detecting a Beacon – PCIe Mode ... 133
8.12 Detecting Low Frequency Periodic Signaling – USB Mode ... 134
8.13 Detecting Low Frequency Periodic Signaling in USB4 Mode ... 134
8.14 Clock Tolerance Compensation ... 134
8.15 Error Detection ... 137
8.15.1 8B/10B Decode Errors... 137
8.15.2 Disparity Errors... 138
8.15.3 Elastic Buffer Errors... 139
8.16 Loopback ... 140
8.17 Polarity Inversion – PCIe and USB Modes ... 142
8.18 Setting Negative Disparity (PCIe Mode) ... 142
8.19 Electrical Idle – PCIe Mode ... 143
8.20 Electrical Idle – All... 145
8.21 Link Equalization Evaluation... 145
8.22 Implementation-Specific Timing and Selectable Parameter Support ... 146
8.23 Control Signal Decode Table – PCIe Mode ... 153
8.24 Control Signal Decode Table – USB Mode, USB4 Mode, and DisplayPort Mode ... 154
8.25 Control Signal Decode Table – SATA Mode ... 155
8.26 Required Synchronous Signal Timings ... 155
8.27 128b/130b Encoding and Block Synchronization (PCIe 8, 16, and 32 GT/s) ... 156
8.28 128b/132b Encoding and Block Synchronization (USB 10 GT/s) ... 157
8.29 Message Bus Interface ... 158
8.29.1 General Operational Rules ... 158
8.29.2 Message Bus Operations vs. Dedicated Signals ... 159
8.30 PCIe Lane Margining at the Receiver ... 159
8.31 Short Channel Power Control ... 163
8.32 RxEqTraining ... 164
8.33 PHY Recalibration ... 165
8.34 Digital Near End Loopback ... 166
8.34.1 PIPE Operations and Signals in DNELB Mode ... 167
8.34.2 Entry and Exit from NELB Mode ... 170
8.34.3 USB4 PAM3 Encoding on PIPE Interface ... 171
8.35 Switching Between Rx and Tx Pairs... 171
9 Sample Operational Sequences... 172
9.1 Active PM L0 to L0s and Back to L0 – PCIe Mode ... 172
9.2 Active PM to L1 and Back to L0 – PCIe Mode ... 173
9.3 Downstream Initiated L1 Substate Entry Using Sideband Mechanism ... 176
9.4 Receivers and Electrical Idle – PCIe Mode Example ... 176
9.5 Using CLKREQ# with PIPE – PCIe Mode ... 178
9.5.1 CLKREQ# in L1 ... 178
9.5.2 CLKREQ# in L2 ... 179
9.5.3 Delayed CLKREQ# in L1 ... 179
9.6 Block Alignment ... 179
9.7 Message Bus: Rx Margining Sequence ... 180
9.8 Message Bus: Updating LocalFS/LocalLF and LocalG4FS/LocalG4LF ... 180
9.9 Message Bus: Updating TxDeemph ... 181
9.10 Message Bus: Equalization... 182

Reference Number: 643108, Revision: 7.1

5

9.11 Message Bus: BlockAlignControl... 183
9.12 Message Bus: ElasticBufferLocation Update ... 184
9.13 Message Bus: RxInPhase01Equalization Update ... 185
**10 Multi-Lane PIPE – PCIe Mode**... 186
**A Appendix** ... 189
A.1 DisplayPort AUX Signals... 189

6

Reference Number: 643108, Revision: 7.1

intel.

# Figures

2-1 Partitioning PHY Layer for PCIe... 18
2-2 Partitioning PHY Layer for USB ... 19
2-3 Partitioning PHY Layer for USB4 ... 20
3-1 PHY/MAC Interface ... 26
3-2 DPTX PHY/MAC Interface ... 27
3-3 DPRX PHY/MAC Interface ... 27
4-1 PHY Functional Block Diagram for Tx+Rx Usage ... 34
4-2 PHY Functional Diagram for Tx+Tx Usage Case ... 35
4-3 PHY Functional Diagram for Rx+Rx Usage Case ... 35
4-4 Transmitter Block Diagram (2.5 and 5.0 GT/s) ... 36
4-5 Transmitter Block Diagram (8.0/10/16/32 GT/s) ... 37
4-6 Receiver Block Diagram (2.5 and 5.0 GT/s) ... 38
4-7 Receiver Block Diagram (8.0/10/16 GT/s) ... 39
4-8 SerDes Architecture: PHY Transmitter Block Diagram ... 40
4-9 SerDes Architecture: PHY Receiver Block Diagram ... 41
5-1 PHY Functional Block Diagram ... 42
5-2 Transmitter Block Diagram (1.5, 3.0, and 6.0 GT/s) ... 43
5-3 Receiver Block Diagram (1.5, 3.0, and 6.0 GT/s) ... 44
6-1 Message Bus Transaction Framing ... 69
7-1 Message Bus Address Space ... 79
8-1 PCLK as PHY Output ... 111
8-2 PCLK as PHY Input with a PHY-Owned PLL ... 112
8-3 PCLK as PHY Input with an External PLL and PHY PLL ... 113
8-4 PCLK as PHY Input with External PLL ... 114
8-5 MacCLK Lane ... 115
8-6 Basic MacCLK Lane Operation ... 115
8-7 Reset# Deassertion and PhyStatus for PCLK as PHY Output ... 116
8-8 PCIe P2 Entry and Exit with PCLK as PHY Output ... 118
8-9 PCIe P2 Entry and Exit with PCLK as PHY Input ... 118
8-10 L1 SubState Entry and Exit with PCLK as PHY Output ... 119
8-11 USB U1 Exit ... 121
8-12 DeepPMReq#/DeepPMAck# Handshake Sequencing ... 125
8-13 PHY Context Restoration after the Power is Restored ... 125
8-14 Rate Change with Fixed Data Path ... 128
8-15 Change from PCIe 2.5 Gt/s to 5.0 Gt/s with PCLK as PHY Input ... 128
8-16 Rate Change with Fixed PCLK Frequency ... 129
8-17 Selecting Tx Margining Value ... 129
8-18 Selecting Tx De-Emphasis Value ... 130
8-19 Receiver Detect – Receiver Present ... 131
8-20 Beacon Transmit ... 131
8-21 LFPS Transmit ... 132
8-22 LFPS Transmit for USB4 and DisplayPort Modes ... 133
8-23 Beacon Receive ... 133
8-24 LFPS Receive ... 134
8-25 Clock Correction – Add an SKP ... 136
8-26 Clock Correction – Remove an SKP ... 137
8-27 8B/10B Decode Error ... 138

Reference Number: 643108, Revision: 7.1

7

intel®

8-28 Disparity Error...138
8-29 Elastic Buffer Underflow...139
8-30 Elastic Buffer Overflow...140
8-31 Loopback Start...141
8-32 Loopback End...142
8-33 Polarity Inversion...142
8-34 Setting Negative Disparity...143
8-35 PCIe 3.0 TxDataValid Timings for Electrical Idle Exit and Entry...144
8-36 Data Throttling and TxElecIdle...145
8-37 Possible TxElecIdle[3:0] Transition Scenarios...154
8-38 PCIe 8 GT/s or Higher TxDataValid Timing for 8 Bit-Wide TxData Interface...156
8-39 PCIe 8 GT/s or Higher TxDataValid Timing for 16 Bit-Wide TxData Interface...157
8-40 PCIe 8 GT/s or Higher RxDataValid Timing for 16 Bit-Wide RxData Interface...157
8-41 PCIe Receiver Equalization...164
8-42 USB Receiver Equalization...164
8-43 PHY Recalibration Initiated by Controller...165
8-44 PHY Recalibration Initiated by PHY...166
8-45 Original PIPE Architecture: DNELB Path Examples...166
8-46 SerDes Architecture: DNELB Path Examples...167
8-47 Transitioning from Rx to Tx Operation...171
8-48 Transitioning from Tx to Rx Operation...171
9-1 L0 to L0s...172
9-2 L0s to L0...173
9-3 L0 to L1...174
9-4 L1 to L0...175
9-5 L1 Substate Management Using RxEIDetectDisable and TxCommonModeDisable...176
9-6 Receiver Active to Idle...177
9-7 Receiver Idle to Active...178
9-8 BlockAlignControl Example Timing...179
9-9 Sample Rx Margining Sequence...180
9-10 LocalFS/LocalLF/LocalG4FS/LocalG4LF Updates Out of Reset and After Rate Change...181
9-11 LocalFS/LocalLF Update Due to GetLocalPresetCoefficients...181
9-12 Updating TxDeemph after GetLocalPresetCoefficients Request...182
9-13 Successful Equalization...182
9-14 Equalization with Invalid Request...183
9-15 Aborted Equalization, Scenario #1...183
9-16 Aborted Equalization, Scenario #2...183
9-17 Message Bus: BlockAlignControl Example...184
9-18 Message Bus: Updating ElasticBufferLocation...184
9-19 Example Sequence: RxInPhase01Equalization and RxEqTraining Relationship...185
10-1 Four-Lane PIPE Implementation...186

8

Reference Number: 643108, Revision: 7.1

intel.

# Tables

2-1 Phy Requirements for Legacy Pin Interface versus the Low Pin Count Interface, and Original PIPE versus SerDes Architecture Support 24

3-1 PCIe Mode - Possible PCLK Rates and Data Widths 28

3-2 PCIe Mode (SerDes Only) - Possible RXCLK Rates and Data Widths 30

3-3 USB Mode - Possible PCLK or RXCLK Rates and Data Widths 31

3-4 SATA Mode - Possible PCLK Rates and Data Widths 31

3-5 SATA Mode (SerDes Only) - Possible RXCLK Rates and Data Widths 31

3-6 DPTX and DPRX Mode - Possible PCLK or RXCLK Rates and Data Widths 32

3-7 USB4 Mode - Possible PCLK or RXCLK Rates and Data Widths 33

6-1 Tx Data Interface Input Signals 46

6-2 Tx Data Interface Output Signals 47

6-3 Rx Data Interface Input Signals 47

6-4 Rx Data Interface Output Signals 48

6-5 Command Interface Input Signals 49

6-6 Command Interface Output Signals 62

6-7 Status Interface Input Signals 63

6-8 Status Interface Output Signals 64

6-9 Message Bus Interface Signals 66

6-10 Message Bus Commands 67

6-11 Command Only Message Bus Transaction Timing (NOP, write_ack) 67

6-12 Command+Address Message Bus Transaction Timing (Read) 68

6-13 Command+Data Message Bus Transaction Timing (Read Completion) 68

6-14 Command+Address+Data Message Bus Transaction Timing (Write_uncommitted, Write_committed) 68

6-15 SerDes Only: Rx data Interface Output Signals 69

6-16 SerDes Only: Command Interface Input Signals 70

6-17 MacCLK Lane Input Signals 71

6-18 MacCLK Lane Output Signals 72

6-19 Original PIPE Only: Tx Data Interface Input Signals 72

6-20 Original PIPE Only: Rx data Interface Output Signals 73

6-21 Command Interface Input Signals 73

6-22 Original PIPE Only: Command Interface Output Signals 74

6-23 Original PIPE Only: Status Interface Output Signals 75

6-24 External Input Signals 75

6-25 External Output Signals 76

7-1 PHY Registers 80

7-2 Address 0h: Rx Margin Control0 81

7-3 Address 1h: Rx Margin Control1 81

7-4 Address 2h: Elastic Buffer Control 82

7-5 Address 3h: PHY Rx Control0 82

7-6 Address 4h: PHY Rx Control1 83

7-7 Address 5h: PHY Rx Control2 85

7-8 Address 6h: PHY Rx Control3 85

7-9 Address 7h: Elastic Buffer Location Update Frequency 85

7-10 Address 8h: PHY Rx Control4 86

7-11 Address 9h: PHY Rx Control 5 86

7-12 Address 400h: PHY Tx Control0 86

Reference Number: 643108, Revision: 7.1

9

intel®

7-13 Address 401h: PHY Tx Control1 ...87
7-14 Address 402h: PHY Tx Control2 ...87
7-15 Address 403h: PHY Tx Control3 ...89
7-16 Address 404h: PHY Tx Control4 ...89
7-17 Address 405h: PHY Tx Control5 ...90
7-18 Address 406h: PHY Tx Control6 ...91
7-19 Address 407h: PHY Tx Control7 ...91
7-20 Address 408h: PHY Tx Control8 ...91
7-21 Address 409h: PHY Tx Control9 ...92
7-22 Address 40Ah: PHY TX Control 10 ...93
7-23 Address 800h: PHY Common Control0 ...93
7-24 Address 801h: PHY Near End Loopback Control ...94
7-25 MAC Registers ...95
7-26 Address 0h: Rx Margin Status0 ...97
7-27 Address 1h: Rx Margin Status1 ...97
7-28 Address 2h: Rx Margin Status2 ...97
7-29 Address 3h: Elastic Buffer Status ...98
7-30 Address 4h: Elastic Buffer Location ...98
7-31 Address 5h: Rx Status0 ...98
7-32 Address 6h: Rx Control0 ...99
7-33 Address 7h: Rx Margin Status3 ...99
7-34 Address 8h: Reserved ...99
7-35 Address 9h: Reserved ...99
7-36 Address Ah: Rx Link Evaluation Status0 ...100
7-37 Address Bh: Rx Link Evaluation Status1 ...100
7-38 Address Ch: Rx Status4 ...101
7-39 Address Dh: Rx Status5 ...102
7-40 Address Eh: Rx Link Evaluation Status2 ...102
7-41 Address Fh: Rx Link Evaluation Status3 ...103
7-42 Address 10h: Rx Status 6 ...104
7-43 Address 400h: Tx Status0 ...104
7-44 Address 401h: Tx Status1 ...105
7-45 Address 402h: Tx Status2 ...105
7-46 Address 403h: Tx Status3 ...106
7-47 Address 404h: Tx Status4 ...106
7-48 Address 405h: Tx Status5 ...106
7-49 Address 406h: Tx Status6 ...106
7-50 Address 407h: Tx Status7 ...107
7-51 Address 408h: Tx Status8 ...107
7-52 Address 409h: Tx Status9 ...107
7-53 Address 40Ah: Tx Status10 ...108
7-54 Address 40Bh: TxStatus11 ...108
7-55 Address 40Ch: TxStatus12 ...108
7-56 Address 800h: Near End Loopback Status ...108
8-1 USB4 PHY Power States ...121
8-2 DisplayPort PHY Power States ...124
8-3 PclkChangeOK/PclkChangeAck Requirements ...126
8-4 Parameters Advertised in PHY Datasheet ...146
8-5 Control Signal Decode Table – PCIe Mode ...153
8-6 Control Signal Decode Table – USB Mode, USB4 Mode, and DisplayPort Mode ...154

10

Reference Number: 643108, Revision: 7.1

intel.

8-7 Control Signal Decode Table – SATA Mode ... 155
8-8 Posted-to-Posted Writes ... 158
8-9 Defined Register Groups ... 159
8-10 Lane Margining at the Receiver Sequences ... 160
10-1 The MAC Layer ... 187
A-1 DisplayPort AUX Signals ... 189

Reference Number: 643108, Revision: 7.1

11

intel®

# Revision History

[tbl-1.md](tbl-1.md)

12

Reference Number: 643108, Revision: 7.1

intel®

[tbl-2.md](tbl-2.md)

Reference Number: 643108, Revision: 7.1

13

intel®

[tbl-3.md](tbl-3.md)

14

Reference Number: 643108, Revision: 7.1

[tbl-4.md](tbl-4.md)

Reference Number: 643108, Revision: 7.1

15

intel®

# 1 Preface

## 1.1 Scope of this Revision

The PCI Express* (PCIe*), SATA, USB, DisplayPort*, and USB4* PHY Interface Specification has definitions of all functional blocks and signals. This revision includes support for PCIe implementations conforming to the *PCIe Base Specification, Revision 7.0*, SATA implementations conforming to the *SATA Specification, Revision 3.0*, USB implementations conforming to the *USB Specification, Revision 3.2*, DisplayPort implementations conforming to the *DisplayPort 2.0 Specification*, and USB4* implementations conforming to the *USB4* *Specification v2.0*.

---16

Reference Number: 643108, Revision: 7.1

intel®

## 2 Introduction

The PHY Interface for the PCI Express* (PCIe*), SATA, USB¹, DisplayPort, and USB4 Architectures (PIPE) is intended to enable the development of functionalities equivalent to the PHYs of PCIe, SATA, USB, DisplayPort, and USB4. Such PHYs can be delivered as discrete Integrated Circuits (ICs) or as macrocells for inclusion in Application-Specific Integrated Circuit (ASIC) designs. The specification defines a set of PHY functions that must be incorporated in a PIPE-compliant PHY; it also defines a standard interface between a PHY and a Media Access Layer (MAC) and a Link Layer ASIC. This specification is not intended to define the internal architecture or design of a compliant PHY chip or macrocell. The PIPE specification is defined to allow several approaches to be used. When possible, the PIPE specification references the PCIe Base Specification, the SATA 3.0 Specification, the USB 3.2 Specification, the DisplayPort 1.4 Specification, or the USB4 2.0 Specification rather than repeating its content. In case of conflicts, the PCIe Base Specification, the SATA 3.0 Specification, the USB 3.2 Specification, DisplayPort 1.4 Specification, and USB4 2.0 Specification must supersede the PIPE specification.

This specification provides some information about how the MAC could use the PIPE interface for several Link Training and Status State Machine (LTSSM) states, link states, and other protocols. This information should be viewed as “guidelines for” or as “one way to implement” base specification requirements. MAC implementations are free to do things in other ways as long as they meet the corresponding specification requirements.

One of the intents of the PIPE specification is to accelerate the development of PCIe, SATA, USB, and USB4 devices. This document defines an interface to which ASIC and endpoint device can be developed by vendors. Peripheral and IP vendors will be able to develop and validate their designs, insulated from the high-speed and analog circuitry issues associated with the PCIe, SATA, USB, DisplayPort, or USB4 PHY interfaces, therefore minimizing the time and risk of their development cycles.

The PIPE specification defines two clocking options for the interface. In the first alternative the PHY provides a clock (PCLK) that clocks the PIPE interface as an output. In the second alternative, the PCLK is provided to each lane of the PHY as an input. The alternative, where the PCLK is provided to each lane of the PHY, was added in revision 4.1 of the PIPE specification. It allows the controller or logic external to the PHY to more easily adjust timing of the PIPE interface to meet timing requirements for silicon implementations. A PHY is only required to support one of the timing alternatives. The two clocking options must be referenced as “PCLK as PHY Output” and “PCLK as PHY Input” respectively. The DisplayPort only supports the “PCLK as PHY Input” clocking option.

Note: The “PCLK as PHY Output” mode is not supported for PCIe 5.0 and beyond, USB4, or Displayport.

Figure 2-1 shows the partitioning described in this specification for the PCIe Base Specification. Figure 2-2 shows the partitioning described in this specification for the USB 3.2 Specification. Figure 2-3 shows the partitioning described in this specification for the USB4 2.0 Specification.

1. USB refers to USB3. USB4 is referenced explicitly.

Reference Number: 643108, Revision: 7.1

17

intel®

Figure 2-1. Partitioning PHY Layer for PCIe

![img-2.jpeg](img-2.jpeg)

18

Reference Number: 643108, Revision: 7.1

intel®

Figure 2-2. Partitioning PHY Layer for USB

![img-3.jpeg](img-3.jpeg)

Reference Number: 643108, Revision: 7.1

19

intel®

Figure 2-3. Partitioning PHY Layer for USB4

![img-4.jpeg](img-4.jpeg)

## 2.1 PCIe PHY Layer

The PCIe PHY layer handles the low level PCIe protocol and signaling. This includes features such as analog buffers, receiver detection, data serialization and de-serialization, 8b/10b encoding and decoding (original PIPE), 128b/130b encoding/decoding (8 GT/s, 16 GT/s, and 32 GT/s) (original PIPE), and elastic buffers (original PIPE). The primary focus of this block is to shift the clock domain of the data from the PCIe rate to one that is compatible with the general logic in the ASIC.

Some key features of the PCIe PHY are:

20

Reference Number: 643108, Revision: 7.1

intel®

- The standard PHY interface enables multiple IP sources for the PCIe logical layer and provides a target interface for PCIe PHY vendors.
- Support for 2.5 GT/s only, or 2.5 GT/s and 5.0 GT/s, or 2.5 GT/s, 5.0 GT/s and 8.0 GT/s, or 2.5 GT/s, 5.0 GT/s, 8.0 GT/s, and 16 GT/s, or 2.5 GT/s, 5.0 GT/s, 8.0 GT/s and 16 GT/s and 32 GT/s, or 2.5 GT/s, 5.0 GT/s, 8.0 GT/s, 16 GT/s, 32 GT/s, 64 GT/s, and 128 GT/s serial data transmission rate.
- It utilizes 8-bit, 16-bit, or 32-bit parallel interfaces to transmit and receive PCIe data. Additionally, it supports a 64-bit interface (in SerDes architecture only).
- Allowed integration of high-speed components into a single functional block as seen by the endpoint device designer
- Data and clock recovery from serial stream on the PCIe bus
- Holding registers to stage transmit (Tx) and receive (Rx) data
- Support of direct disparity control for use in transmitting compliance patterns
- 8b/10b encoding and decoding, and error indication (original PIPE)
- 128b/130b encoding and decoding, and error indication (original PIPE)
- Receiver detection
- Beacon transmission and reception
- Selectable Tx margining, Tx de-emphasis and signal swing values
- Lane margining at the receiver
- Polarity (original PIPE)
- Electrical Idle entry and exit detection (Squelch)

## 2.2 USB PHY Layer

The USB PHY layer handles the low-level USB protocol and signaling. This includes features such as analog buffers, receiver detection, data serialization and de-serialization, 8b/10b encoding and decoding, 128b/132b encoding and decoding (10 GT/s), and elastic buffers. The primary focus of this block is to shift the clock domain of the data from the USB rate to one that is compatible with the general logic in the ASIC.

Some key features of the USB PHY are:

- Standard PHY interface that enables multiple IP sources to the USB link layer and provides a target interface for USB PHY vendors
- Support for 5.0 GT/s and/or 10 GT/s serial data transmission rate
- Utilizes 8-bit, 16-bit or 32-bit parallel interfaces to transmit and receive USB data
- Allowing the integration of high-speed components into a single functional block as seen in the device designer
- Data and clock recovery from serial stream on the USB bus
- Register holding to stage the Tx and Rx data
- 8b/10b encoding and decoding, and error indication
- 128b/132b encoding and decoding and error indication
- Receiver detection
- Low Frequency Periodic Signaling (LFPS)

Reference Number: 643108, Revision: 7.1

21

intel®

## 2.3 USB4 PHY Layer

The USB4 PHY Layer handles the low level USB4 protocol and signaling. This includes features such as data serialization and de-serialization, analog buffers, and receiver detection.

Some key features of the USB4 PHY:

- A standard PHY interface enables multiple IP sources for USB4 Link Layer and provides a target interface for USB4 PHY vendors
- Supports 10 GT/s and/or 20 GT/s serial data transmission rate in combination with a 40-bit parallel interface to transmit and receive USB4 data using PAM2 signaling
- Supports 40 GT/s serial data transmission rate in combination with a 56-bit parallel interface to transmit and receive USB4 data using PAM3 signaling
- Data and clock recovery from serial stream on the USB4 bus
- Holding registers to stage transmit and receive data
- Low Frequency Periodic Signaling (LFPS)

## 2.4 SATA PHY Layer

The SATA PHY layer handles the low-level SATA protocol and signaling. This includes features such as analog buffers, data serialization and deserialization, 8b/10b encoding and decoding, and elastic buffers. The primary focus of this block is to shift the clock domain of the data from the SATA rate to one that is compatible with the general logic in the ASIC.

Some key features of the SATA PHY are:

- A standard PHY interface that enables multiple IP sources for SATA controllers and provides a target interface for SATA PHY vendors
- Support of 1.5 GT/s only, or 1.5 GT/s and 3.0 GT/s, or 1.5 GT/s, or 3.0 GT/s, and 6.0 GT/s serial data transmission rate
- Utilizes 8-bit, 16-bit, or 32-bit parallel interface to transmit and receive SATA data
- Allows integration of high-speed components into a single functional block as seen in the device designer
- Data and clock recovery from serial stream on the SATA bus
- Holding registers to stage transmit and receive data
- 8b/10b encode/decode and error indication
- COMINIT and COMRESET transmission and reception

## 2.5 DisplayPort PHY Layer

The DisplayPort PHY layer handles the low-level DisplayPort protocol and signaling. This includes features such as data serialization and de-serialization, and analog buffers.

Some key features of the DisplayPort PHY include the following:

- A standard PHY interface that enables multiple IP sources for the DisplayPort link layer and provides a target interface for the DisplayPort PHY vendors

22

Reference Number: 643108, Revision: 7.1

intel®

- Support of 1.62 Gbps, 2.16 Gbps (eDP), 2.43 Gbps (eDP), 2.7 Gbps, 3.24 Gbps (eDP), 4.32 Gbps (eDP), 5.4 Gbps, 8.1 Gbps, 10 Gbps, 13.5 Gbps, and 20 Gbps serial data transmission rates
- Utilizes 10-bit, 20-bit, or 40-bit parallel interfaces to transmit and receive the DisplayPort data
- Data and clock recovery from the serial stream on the DisplayPort bus
- Holding registers to stage Tx and Rx data

## 2.6 Low Pin Count Interface and SerDes Architecture

To address the issue of increasing signal count, the message bus interface was introduced in PIPE 4.4 and utilized for PCIe lane margining at the receiver and elastic buffer depth control. In PIPE 5.0, all the legacy PIPE signals without critical timing requirements were mapped into message bus registers so that their associated functionality could be accessed via the message bus interface instead of implementing dedicated signals. Any new features added in PIPE 4.4 and onwards are available only via message bus accesses unless they have critical timing requirements that need dedicated signals.

To facilitate the design of general-purpose PHYs delivered as hard IPs, and to provide the MAC with more freedom to do latency optimizations, a SerDes architecture was defined in PIPE 5.0. This architecture simplifies the PHY and shifts much of the protocol-specific logic into the MAC.

To maximize interoperability between MAC and PHY IPs, PHY designs must adhere to the requirements stated in Table 2-1 to support the legacy pin interface versus the low pin count interface, and to support original PIPE architecture versus the SerDes architecture. For PCIe, the PCIe 6.0 in Table 2-1 heading refers to a PHY that is configured as PCIe 6.0 capable; the selection is done statically based on the capability and does not change with a rate change.

The legacy pin interface refers to a pin interface that utilizes all the applicable dedicated signals, as well as the message bus interface for features not supported through dedicated signals. The low pin count interface refers to a pin interface that utilizes the message bus interface for all features supported through the message bus, using dedicated signals only for features not supported through the message bus. The legacy pin interface dedicated signals are defined in PIPE 4.4.1 and earlier and have been deprecated in PIPE 5.0.

The original PIPE architecture is represented in Figure 4-4, Figure 4-5, Figure 4-6, and Figure 4-7. The SerDes architecture is represented in Figure 4-8 and Figure 4-9.

The legacy pin interface and the low pin count interface are not simultaneously operational, except for the PCIe 4.0 lane margining at the receiver being controlled via the low pin count interface, while other operations are managed over the legacy interface. A PHY must be statically configured to utilize either the low pin count interface or the legacy pin interface, for instance, no dynamic switching between the interfaces based on operational rate is permitted. Finally, a SerDes architecture datapath must always utilize the low pin count interface, using the legacy pin interface with SerDes architecture is considered illegal.

Reference Number: 643108, Revision: 7.1

23

intel®

Table 2-1. Phy Requirements for Legacy Pin Interface versus the Low Pin Count Interface, and Original PIPE versus SerDes Architecture Support

[tbl-5.md](tbl-5.md)

Note:

$^{1}$ To provide interoperability with PCIe and USB MACs that choose not to migrate to the SerDes architecture, PHYs are encouraged to provide support for original PIPE via a method where the associated logic can be easily optimized out. With this, designs that do not require a PHY which supports original PIPE are not burdened with any unneeded logic.

## 2.7 Support for Short Reach (SR) Applications

The PIPE specification supports short channel (also known as Short Reach [SR]) applications, for instance, for multi-chip package solutions. For such applications, the operating power can be reduced significantly by optimizing certain operational and environmental parameters for short channels. For example, the operating power for PCIe can potentially be reduced by up to roughly 50% compared to traditional PCIe applications. While specifying environmental parameters is outside the scope of the PIPE specification, PHY vendors are encouraged to advertise any such environmental knobs that can be changed in short channel applications to reduce power, for instance, reducing the PHY supply voltage. This specification provides hooks for tuning specific operational parameters for reduced power. These operational knobs are PHY vendor-dependent and may include channel loss, receiver equalization activity (including Decision Feedback Equalization [DFE] and Continuous Time Linear Equalization [CTLE]), Tx swing, and clock recovery strategy. PHY vendors that want to support power optimized, short reach applications should identify a useful set of operating points for these knobs that it advertises in its datasheet (via the ShortChannelPowerControlSettingsSupported parameter) that the customer can then select from using the PIPE control interface (via the ShortChannelPowerControl[1:0] signals).

In addition to the just mentioned potential power savings, Multi Chip Package (MCP) applications provide the opportunity for cost savings and additional operational optimization; specifically, it is strongly recommended that DC coupling is used, therefore saving on capacitor insertion cost. As part of the DC coupling support, the controller should bypass explicit receiver detection. For PCIe, the receiver detection operation in the PCIe LTSSM state Detect.Quiet should be bypassed and the LTSSM should automatically proceed to Polling. If the LTSSM transitions back to Detect from Polling due to timeout, it is recommended that a subsequent transition to Polling should occur either upon an electrical idle exit detection or after a 30 to 100 ms timeout. Further optimization based on DC coupling can be implemented to reduce power state (for instance, L1.2) exit latencies.

24

Reference Number: 643108, Revision: 7.1

intel®

## 2.8 Configurable Pairs

Support for configurable Rx and Tx differential pairs was added in version 5.0 of the PIPE specification. This configurability was primarily added to support Type-C alternate mode protocols such as DisplayPort and USB4; however, other applications are possible. Up to two differential pairs are assumed to be operational at any given time. Supported lane combinations are one Rx pair and one Tx pair, two Tx pairs, or two Rx pairs; each combination shares a single set of PIPE per-lane signals. See Section 7 for more information.

Reference Number: 643108, Revision: 7.1

25

intel®

### 3 PHY/MAC Interface

Figure 3-1 shows the data and logical command and status signals between the PHY and the MAC layer for one Rx pair and one Tx pair combination. Figure 3-2 and Figure 3-3 show the data and command and status signals between the PHY and the MAC layer for the DisplayPort DPTX and DPRX, respectively. Full support of PCIe mode, USB mode, SATA mode, DisplayPort mode, and USB4 mode at all rates require different numbers of control and status signals to be implemented. See Section 6.1 for details on which specific signals are required for each operating mode.

Figure 3-1. PHY/MAC Interface

![img-5.jpeg](img-5.jpeg)

26

Reference Number: 643108, Revision: 7.1

intel®

Figure 3-2. DPTX PHY/MAC Interface

![img-6.jpeg](img-6.jpeg)

Figure 3-3. DPRX PHY/MAC Interface

![img-7.jpeg](img-7.jpeg)

This specification allows several different PHY/MAC interface configurations to support several signaling rates.

For PIPE implementations that support only the 2.5 GT/s signaling rate in PCIe mode, implementers can choose to have 16-bit data paths with PCLK running at 125 MHz, or 8-bit data paths with PCLK running at 250 MHz. PIPE implementations that support 5.0 GT/s signaling and 2.5 GT/s signaling in PCIe mode, and therefore can switch between 2.5 GT/s and 5.0 GT/s signaling rates, can be implemented in several ways. An implementation may choose to have PCLK fixed at 250 MHz and use 8-bit data paths

Reference Number: 643108, Revision: 7.1

27

intel®

when operating at 2.5 GT/s signaling rate, and 16-bit data paths when operating at 5.0 GT/s signaling rate. Another implementation choice is to use a fixed data path width and change the PCLK frequency to adjust the signaling rate. In this case, an implementation with 8-bit data paths would provide PCLK at 250 MHz for 2.5 GT/s signaling and provide PCLK at 500 MHz for 5.0 GT/s signaling. Similarly, an implementation with 16-bit data paths would provide PCLK at 125 MHz for 2.5 GT/s signaling and 250 MHz for 5.0 GT/s signaling. The sample list of possibilities is shown in Table 3-1.

For PIPE implementations that support 5.0 GT/s USB mode and 10 GT/s, USB mode implementers can choose from the options shown in Table 3-3. A PIPE compliant MAC or PHY is only required to support one option for each USB transfer speed that it supports.

For SATA PIPE implementations that support only the 1.5 GT/s signaling rate implementers can choose to have 16-bit data paths with PCLK running at 75 MHz, or 8-bit data paths with PCLK running at 150, 300 or 600 MHz. The 300 and 600 MHz options require the use of TXDataValid and RXDataValid signals to toggle the use of data on the data bus.

SATA PIPE implementations that support 1.5 GT/s signaling and 3.0 GT/s signaling in SATA mode, and therefore are able to switch between 1.5 GT/s and 3.0 GT/s signaling rates, can be implemented in several ways. An implementation may choose to have PCLK fixed at 150 MHz and use 8-bit data paths when operating at 1.5 GT/s signaling rate, and 16-bit data paths when operating at 3.0 GT/s signaling rate. Another implementation choice is to use a fixed data path width and change PCLK frequency to adjust the signaling rate. In this case, an implementation with 8-bit data paths could provide PCLK at 150 MHz for 1.5 GT/s signaling and provide PCLK at 300 MHz for 3.0 GT/s signaling. Similarly, an implementation with 16-bit data paths would provide PCLK at 75 MHz for 1.5 GT/s signaling and 150 MHz for 3.0 mode are shown GT/s signaling. A sample list of possible widths and PCLK rates for SATA is shown in Table 3-4. A PIPE compliant MAC or PHY is only required to support one option for each SATA transfer speed that it supports.

A sample list of possible data width and PCLK rate combinations for PCIe mode is shown in Table 3-1; other combinations are possible as long as they conform to the PIPE definitions and the combination of PCLK rate, data width, and TXDataValid/RXDataValid strobes match the bandwidth across the serial link. A PIPE compliant MAC or PHY is only required to support one option for each PCIe transfer speed that it supports.

Note: PHYs that support greater than x4 link widths must provide an option for 32-bit or less data width.

Table 3-1. PCIe Mode - Possible PCLK Rates and Data Widths (Sheet 1 of 3)

[tbl-6.md](tbl-6.md)

28

Reference Number: 643108, Revision: 7.1

intel®

Table 3-1. PCIe Mode - Possible PCLK Rates and Data Widths (Sheet 2 of 3)

[tbl-7.md](tbl-7.md)

Reference Number: 643108, Revision: 7.1

29

intel®

Table 3-1. PCIe Mode - Possible PCLK Rates and Data Widths (Sheet 3 of 3)

[tbl-8.md](tbl-8.md)

1. For block encoded modes, not all 10, 20, 40, or 80 bits are used. See TXData and RXData signal descriptions for details.

2. RxDataValid is not applicable to SerDes mode.

Table 3-2. PCIe Mode (SerDes Only) - Possible RXCLK Rates and Data Widths

[tbl-9.md](tbl-9.md)

30

Reference Number: 643108, Revision: 7.1

intel®

Table 3-2. PCIe Mode (SerDes Only) - Possible RXCLK Rates and Data Widths

[tbl-10.md](tbl-10.md)

Table 3-3. USB Mode – Possible PCLK or RXClk Rates and Data Widths

[tbl-11.md](tbl-11.md)

Table 3-4. SATA Mode – Possible PCLK Rates and Data Widths

[tbl-12.md](tbl-12.md)

Note: In SATA mode, if the PHY elasticity buffer is operating in nominal empty mode, RXDataValid may also be used when the EB is empty and no data is available.

Table 3-5. SATA Mode (SerDes Only) – Possible RXCLK Rates and Data Widths

[tbl-13.md](tbl-13.md)

Reference Number: 643108, Revision: 7.1

31

intel®

Table 3-5. SATA Mode (SerDes Only) – Possible RXCLK Rates and Data Widths

[tbl-14.md](tbl-14.md)

Table 3-6 shows possible PCLK and data width options for DisplayPort implementations.

Table 3-6. DPTX and DPRX Mode – Possible PCLK or RXCLK Rates and Data Widths

[tbl-15.md](tbl-15.md)

1. 40-bit data width is for consistency with other protocols. For block-encoded DisplayPort modes (that is, 10 Gbps, 13.5 Gbps, and 20 Gbps), the controller utilizes only 8 out of every 10 bits of data. See Section 6.1.1 for more details.

32

Reference Number: 643108, Revision: 7.1

intel®

Table 3-7. USB4 Mode – Possible PCLK or RXCLK Rates and Data Widths

[tbl-16.md](tbl-16.md)

1. While the data widths are 10, 20, or 40 bits for consistency with other protocols, USB4 only utilizes only 8 out of every 10 bits of data since it uses block encoding. See Section 6.1.1 for more details.

**Note:**

When a MAC that implements the TXDataValid signal is using a mode that does not use TXDataValid the MAC shall keep TXDataValid asserted. When a PHY that implements RXDataValid is in a mode that does not use RXDataValid the PHY mustkeep RXDataValid asserted.

There may be PIPE implementations that support multiples of these configurations. PHY implementations that support multiple configurations at the same rate must support the width and PCLK rate control signals. A PHY that supports multiple rates in PCIe mode or SATA mode or USB mode must support configurations across all supported rates that are fixed at the PCLK rate. A PHY that supports multiple rates in PCIe mode or SATA mode must support configurations across all supported rates that are fixed data path width.

Reference Number: 643108, Revision: 7.1

33

intel®

# 4 PCIe, USB, USB4, and DisplayPort PHY Functionality

Figure 4-1 shows the functional block diagram of the PHY for a Tx differential pair and Rx differential pair combination. The functional blocks shown are not intended to define the internal architecture or design of a compliant PHY but to serve as an aid for signal grouping. Functional PHY diagrams illustrating Tx+Tx and Rx+Rx combinations are provided in Figure 4-2 and Figure 4-3, respectively. Note that while these diagrams illustrate the scenario where the Phase Lock Loop (PLL) is in the PHY, other topologies are possible where the PLL is external to the PHY as described in Section 8.1.1.

Figure 4-1. PHY Functional Block Diagram for Tx+Rx Usage

![img-8.jpeg](img-8.jpeg)

34

Reference Number: 643108, Revision: 7.1

intel®

Figure 4-2. PHY Functional Diagram for Tx+Tx Usage Case

![img-9.jpeg](img-9.jpeg)

Figure 4-3. PHY Functional Diagram for Rx+Rx Usage Case

![img-10.jpeg](img-10.jpeg)

Reference Number: 643108, Revision: 7.1

35

intel®

Section 4.1 and Section 4.2 provide descriptions of each of the blocks shown in Figure 4-1, Figure 4-2, Figure 4-3. These blocks represent high-level functionality that is required to exist in the PHY implementation. These descriptions and diagrams describe general architecture and behavioral characteristics. Different implementations are possible and acceptable.

## 4.1 Original PIPE Architecture

Figure 4-4. Transmitter Block Diagram (2.5 and 5.0 GT/s)

![img-11.jpeg](img-11.jpeg)

36

Reference Number: 643108, Revision: 7.1

intel®

Figure 4-5. Transmitter Block Diagram (8.0/10/16/32 GT/s)

![img-12.jpeg](img-12.jpeg)

Reference Number: 643108, Revision: 7.1

37

intel®

Figure 4-6. Receiver Block Diagram (2.5 and 5.0 GT/s)

![img-13.jpeg](img-13.jpeg)

38

Reference Number: 643108, Revision: 7.1

intel®

Figure 4-7. Receiver Block Diagram (8.0/10/16 GT/s)

![img-14.jpeg](img-14.jpeg)

## 4.2 SerDes Architecture

With the SerDes architecture, the PHY implements minimal digital logic compared to the original PIPE architecture. Figure 4-8 shows the transmitter functionality implemented in the PHY. The data received from the MAC goes through a parallel to serial converter before being driven out on differential wires. Note that in the SerDes architecture, all loopback logic resides in the MAC. Figure 4-9 shows the receiver functionality implemented in the PHY. The data received on the input differential wires goes through a serial to parallel converter before being forwarded to the MAC along with a recovered clock, RXCLK.

Reference Number: 643108, Revision: 7.1

39

intel®

Figure 4-8. SerDes Architecture: PHY Transmitter Block Diagram

![img-15.jpeg](img-15.jpeg)

40

Reference Number: 643108, Revision: 7.1

intel®

Figure 4-9. SerDes Architecture: PHY Receiver Block Diagram

![img-16.jpeg](img-16.jpeg)

Reference Number: 643108, Revision: 7.1

41

intel®

# 5 SATA PHY Functionality

Figure 4-1 shows the functional block diagram of a SATA PHY. The functional blocks shown are not intended to define the internal architecture or design of a compliant PHY but to serve as an aid for signal grouping.

Figure 5-1. PHY Functional Block Diagram

![img-17.jpeg](img-17.jpeg)

The following sections provide descriptions of each of the blocks shown in Figure 5-1. These blocks represent high-level functionality that is required to exist in the PHY implementation. These descriptions and diagrams describe general architecture and behavioral characteristics. Different implementations are possible and acceptable.

42

Reference Number: 643108, Revision: 7.1

intel®

Figure 5-2. Transmitter Block Diagram (1.5, 3.0, and 6.0 GT/s)

![img-18.jpeg](img-18.jpeg)

Reference Number: 643108, Revision: 7.1

43

intel®

Figure 5-3. Receiver Block Diagram (1.5, 3.0, and 6.0 GT/s)

![img-19.jpeg](img-19.jpeg)

44

Reference Number: 643108, Revision: 7.1

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

intel®

### 6.1.1 Data Interface

Table 6-1. Tx Data Interface Input Signals

[tbl-17.md](tbl-17.md)

1. For PCIe operating at 8 GT/s or higher link speed, USB4, and USB 10 GT/s link speed, the data bits are utilized as per the block encoded data description detailed in the previous tables. For all other modes, all the data bits are utilized.

46

Reference Number: 643108, Revision: 7.1

intel®

Table 6-2. Tx Data Interface Output Signals

[tbl-18.md](tbl-18.md)

Table 6-3. Rx Data Interface Input Signals

[tbl-19.md](tbl-19.md)

Reference Number: 643108, Revision: 7.1

47

intel®

Table 6-4. Rx Data Interface Output Signals

[tbl-20.md](tbl-20.md)

48

Reference Number: 643108, Revision: 7.1

intel®

1. For PCIe operating at 8 GT/s or higher link speed, USB4, and USB 10 GT/s link speed, the data bits are utilized as per the block encoded data description detailed in the previous tables. For all other modes, all the data bits are utilized.

#### 6.1.2 Command Interface

Table 6-5. Command Interface Input Signals (Sheet 1 of 14)

[tbl-21.md](tbl-21.md)

Reference Number: 643108, Revision: 7.1

49

intel®

Table 6-5. Command Interface Input Signals (Sheet 2 of 14)

[tbl-22.md](tbl-22.md)

50

Reference Number: 643108, Revision: 7.1

intel®

Table 6-5. Command Interface Input Signals (Sheet 3 of 14)

[tbl-23.md](tbl-23.md)

Reference Number: 643108, Revision: 7.1

51

intel®

Table 6-5. Command Interface Input Signals (Sheet 4 of 14)

[tbl-24.md](tbl-24.md)

52

Reference Number: 643108, Revision: 7.1

intel®

Table 6-5. Command Interface Input Signals (Sheet 5 of 14)

[tbl-25.md](tbl-25.md)

Reference Number: 643108, Revision: 7.1

53

intel®

Table 6-5. Command Interface Input Signals (Sheet 6 of 14)

[tbl-26.md](tbl-26.md)

54

Reference Number: 643108, Revision: 7.1

intel®

Table 6-5. Command Interface Input Signals (Sheet 7 of 14)

[tbl-27.md](tbl-27.md)

Reference Number: 643108, Revision: 7.1

55

intel®

Table 6-5. Command Interface Input Signals (Sheet 8 of 14)

[tbl-28.md](tbl-28.md)

56

Reference Number: 643108, Revision: 7.1

intel®

Table 6-5. Command Interface Input Signals (Sheet 9 of 14)

[tbl-29.md](tbl-29.md)

Reference Number: 643108, Revision: 7.1

57

intel®

Table 6-5. Command Interface Input Signals (Sheet 10 of 14)

[tbl-30.md](tbl-30.md)

58

Reference Number: 643108, Revision: 7.1

intel®

Table 6-5. Command Interface Input Signals (Sheet 11 of 14)

[tbl-31.md](tbl-31.md)

Reference Number: 643108, Revision: 7.1

59

intel®

Table 6-5. Command Interface Input Signals (Sheet 12 of 14)

[tbl-32.md](tbl-32.md)

60

Reference Number: 643108, Revision: 7.1

intel®

Table 6-5. Command Interface Input Signals (Sheet 13 of 14)

[tbl-33.md](tbl-33.md)

Reference Number: 643108, Revision: 7.1

61

intel®

Table 6-5. Command Interface Input Signals (Sheet 14 of 14)

[tbl-34.md](tbl-34.md)

Table 6-6. Command Interface Output Signals (Sheet 1 of 2)

[tbl-35.md](tbl-35.md)

62

Reference Number: 643108, Revision: 7.1

intel®

Table 6-6. Command Interface Output Signals (Sheet 2 of 2)

[tbl-36.md](tbl-36.md)

### 6.1.3 Status Interface

Table 6-7. Status Interface Input Signals

[tbl-37.md](tbl-37.md)

Reference Number: 643108, Revision: 7.1

63

intel®

Table 6-8. Status Interface Output Signals (Sheet 1 of 3)

[tbl-38.md](tbl-38.md)

64

Reference Number: 643108, Revision: 7.1

intel®

Table 6-8. Status Interface Output Signals (Sheet 2 of 3)

[tbl-39.md](tbl-39.md)

Reference Number: 643108, Revision: 7.1

65

intel®

Table 6-8. Status Interface Output Signals (Sheet 3 of 3)

[tbl-40.md](tbl-40.md)

1. Disparity errors are not reported when the rate is 8.0 GT/s, 16 GT/s, or 32 GT/s.

### 6.1.4 Message Bus Interface

The message bus interface provides a way to initiate and participate in non-latency sensitive PIPE operations using a small number of wires, it also enables future PIPE operations to be added without adding additional wires. The use of this interface requires the device to be in a power state with PCLK running. Control and status bits used for PIPE operations are mapped into 8-bit registers that are hosted in 12-bit address spaces in the PHY and the MAC. The registers are accessed via read and write commands driven over the signals listed in Table 6-9. These signals are synchronous with the PCLK and are reset with Reset#. The specific commands and framing of the transactions sent over the message bus interface are described in the following subsections.

Table 6-9. Message Bus Interface Signals

[tbl-41.md](tbl-41.md)

Errors in SKP ordered sets must be reported by the PHY as 128/130 decode errors. An error in an SKP ordered set must be reported if there is an error in the first 4N+1 symbols of the skip ordered set.

#### 6.1.4.1 Message Bus Interface Commands

The 4-bit commands used for accessing the PIPE registers across the message bus are defined in Table 6-10. A transaction consists of a command and any associated address and data, as specified in the table. The table also specifies the number of PCLK cycles

66

Reference Number: 643108, Revision: 7.1

intel®

that it takes to transfer the transaction across the message bus interface. The order in which the bits are transferred across the interface are illustrated in Table 6-11, Table 6-12, Table 6-13, and Table 6-14.

To address the case where multiple PIPE interface signals can change on the same PCLK, the concept of write_uncommitted and write_committed is introduced. A series of write_uncommitted transactions followed by one write_committed transaction provides a mechanism by which all the uncommitted writes and the final committed write are executed in an atomic manner, taking effect during the same PCLK cycle.

To enable the write_uncommitted command, designs must implement a write buffer in the PHY and the MAC, where each write buffer entry can accommodate the three bytes worth of information associated with each write transaction. The minimum write buffer depth required is five, however, this number may increase in the future when new PIPE operations are mapped into the message bus interface.

Table 6-10. Message Bus Commands

[tbl-42.md](tbl-42.md)

Table 6-11. Command Only Message Bus Transaction Timing (NOP, write_ack)

[tbl-43.md](tbl-43.md)

Reference Number: 643108, Revision: 7.1

67

intel®

Table 6-12. Command+Address Message Bus Transaction Timing (Read)

[tbl-44.md](tbl-44.md)

Table 6-13. Command+Data Message Bus Transaction Timing (Read Completion)

[tbl-45.md](tbl-45.md)

Table 6-14. Command+Address+Data Message Bus Transaction Timing (Write_uncommitted, Write_committed)

[tbl-46.md](tbl-46.md)

### 6.1.4.2 Message Bus Interface Framing

The framing of transactions is implicitly derived by adhering to the following rules:

1. All zeroes must be driven on the message bus when idle.
2. An idle to a non-idle transition indicates the start of a transaction; a new transaction can immediately start the cycle after the end of the previous transaction without an intervening idle.
3. The number of cycles to transmit a transaction depends on the command and is specified in Table 6-10.
4. The cycles associated with one transaction must be transferred in contiguous cycles.

Figure 6-1 illustrates the framing of a couple of transactions on the message bus. The start of the first transaction is inferred by the idle to a non-idle transition. The command is decoded as a write, which takes three cycles to transmit. Since the cycle following the end of the write is non-idle, it is inferred to be the start of the next transaction, which is decoded to be another write that takes three cycles to transmit.

68

Reference Number: 643108, Revision: 7.1

intel®

Figure 6-1. Message Bus Transaction Framing

![img-20.jpeg](img-20.jpeg)

## 6.2 PHY/MAC Interface Signals – SerDes Architecture Only

This section describes any signals for SerDes architecture that are required in addition to those defined in Section 6.1.

### 6.2.1 Data Interface

Table 6-15. SerDes Only: Rx data Interface Output Signals

[tbl-47.md](tbl-47.md)

Reference Number: 643108, Revision: 7.1

69

intel®

## 6.2.2 Command Interface

Table 6-16. SerDes Only: Command Interface Input Signals

[tbl-48.md](tbl-48.md)

## 6.2.3 MacCLK Lane Signals

A MacCLK lane is an optional feature that is implemented only by PHYs that support MacCLK. The signals defined here are per MacCLK lane. These signals are independent of the other PIPE signals. Refer to Section 8.1.2 for more details. The MacCLK lane signals are in the MacCLKReset# domain. The MAC and the PHY must not rely on the signals being held at a valid value when MacCLKReset# is asserted. If default values are specified, the MAC and the PHY must guarantee that the signals they drive are stable and at their reset values when MacCLKReset# deasserts. The PHY specifies the minimum MacCLKReset# assertion pulse duration it requires via the paramater MinimumMacCLKReset#AssertionPulse.

70

Reference Number: 643108, Revision: 7.1

intel®

Table 6-17. MacCLK Lane Input Signals

[tbl-49.md](tbl-49.md)

Reference Number: 643108, Revision: 7.1

71

intel®

Table 6-18. MacCLK Lane Output Signals

[tbl-50.md](tbl-50.md)

### 6.3 PHY/MAC Interface Signals – Original PIPE Only

This section describes the signals for original PIPE that are required in addition to those define in Section 6.1.

### 6.3.1 Data Interface

Table 6-19. Original PIPE Only: Tx Data Interface Input Signals

[tbl-51.md](tbl-51.md)

72

Reference Number: 643108, Revision: 7.1

intel®

Table 6-20. Original PIPE Only: Rx data Interface Output Signals

[tbl-52.md](tbl-52.md)

### 6.3.2 Command Interface

Table 6-21. Command Interface Input Signals (Sheet 1 of 2)

[tbl-53.md](tbl-53.md)

Reference Number: 643108, Revision: 7.1

73

intel®

Table 6-21. Command Interface Input Signals (Sheet 2 of 2)

[tbl-54.md](tbl-54.md)

Table 6-22. Original PIPE Only: Command Interface Output Signals

[tbl-55.md](tbl-55.md)

74

Reference Number: 643108, Revision: 7.1

intel®

Table 6-23. Original PIPE Only: Status Interface Output Signals

[tbl-56.md](tbl-56.md)

## 6.4 External Signals – Common for SerDes and Original PIPE

Table 6-24. External Input Signals

[tbl-57.md](tbl-57.md)

Reference Number: 643108, Revision: 7.1

75

intel®

Table 6-25. External Output Signals (Sheet 1 of 2)

[tbl-58.md](tbl-58.md)

76

Reference Number: 643108, Revision: 7.1

intel®

Table 6-25. External Output Signals (Sheet 2 of 2)

[tbl-59.md](tbl-59.md)

Reference Number: 643108, Revision: 7.1

77

intel®

# 7 PIPE Message Bus Address Spaces

The PIPE specification defines 12-bit address spaces to enable the message bus interface; the MAC and the PHY each implement a unique 12-bit address space as shown in Figure 7-1. These address spaces are used to host registers associated with certain PIPE operations. The MAC and PHY access specific bits in the registers to initiate operations, to participate in handshakes, or to indicate status. The MAC initiates requests on the message bus interface to access registers hosted in the PHY address space. The PHY initiates requests on the message bus interface to access registers hosted in the MAC address space.

Each 12-bit address space is divided into four main regions: the receiver address region, the transmitter address region, the common address region, and the vendor-specific address region. The receiver address region is used to configure and report the status related to receiver operation; it spans the 1024-KB region from 12'h000 to 12'h3FF and supports up to two receivers with 512 KB allocated to each. The transmitter address region is used to configure and report status related to transmitter operation; it spans the 1024-KB region from 12'h400 to 12'h7FF and supports up to two transmitters: TX1 and TX2, with a 512 KB region associated with each. The common address region hosts the registers relevant to both receiver and transmitter operation; it spans the 1024-KB region from 12'h800 to 12'hBFF and supports up two sets of Rx/Tx pairs with 512 KB allocated towards the common registers for each pair. The vendor-specific address region is the 1024K region from 12'hC00 to 12'hFFF, which enables individual vendors to define registers as needed outside of those defined in this PIPE specification.

As noted in the previous paragraphs, the address space is defined to support configurable Rx/Tx pairs. Up to two differential pairs are assumed to be operational at any one time. Supported combinations are one Rx and one Tx pair, two Tx pairs, or two Rx pairs.

78

Reference Number: 643108, Revision: 7.1

intel®

Figure 7-1. Message Bus Address Space

![img-21.jpeg](img-21.jpeg)

The PCIe Rx margining operations and elastic buffer depth are controlled via registers hosted in these address spaces. Additionally, several legacy pipe control and status signals have been mapped into the registers hosted in these address spaces.

The following subsections define the PHY registers and the MAC registers. Individual register fields are specified as required or optional. In addition, each field has an attribute description of either level or one-cycle assertion. When a level field is written, the value written is maintained by the hardware until the next write to that field or until a reset occurs. When a one-cycle field is written to assert the value high, the hardware maintains the assertion for only a single cycle and then automatically resets the value to zero on the next cycle.

Reference Number: 643108, Revision: 7.1

79

intel®

## 7.1 PHY Registers

Table 7-1 lists the PHY registers and their associated address. The details of each register are provided in the following subsections.

To support configurable pairs, the same registers defined for RX1 are also defined for RX2, the same registers defined for TX1 are defined for TX2, and the same registers defined for CMN1 are defined for CMN2. Only two differential pairs are active at a time based on configuration; valid combinations correspond to registers defined in RX1+TX1+CMN1, RX1+RX2+CMN1+CMN2, or TX1+TX2+CMN1+CMN2.

A PHY that does not support configurable pairs only implements registers defined for RX1, TX1, and CMN1.

Table 7-1. PHY Registers (Sheet 1 of 2)

[tbl-60.md](tbl-60.md)

80

Reference Number: 643108, Revision: 7.1

intel®

Table 7-1. PHY Registers (Sheet 2 of 2)

[tbl-61.md](tbl-61.md)

### 7.1.1 Address 0h: Rx Margin Control0

This register is used along with the Rx Margin Control1 to control the PCIe Lane Margining at the receiver.

Table 7-2. Address 0h: Rx Margin Control0

[tbl-62.md](tbl-62.md)

### 7.1.2 Address 1h: Rx Margin Control1

This register is used along with the Rx Margin Control0 to control the PCIe Rx margining.

Table 7-3. Address 1h: Rx Margin Control1

[tbl-63.md](tbl-63.md)

1. This is reversed from the timing margining direction convention used in the PCIe Base Specification.

Reference Number: 643108, Revision: 7.1

81

intel®

### 7.1.3 Address 2h: Elastic Buffer Control

This register is used to control the elastic buffer depth, enabling the controller to optimize latency in nominal half full mode. The ability to control the elastic buffer depth is an optional feature that may be especially beneficial for Retimers operating in the PCIe SRIS mode.

Table 7-4. Address 2h: Elastic Buffer Control

[tbl-64.md](tbl-64.md)

### 7.1.4 Address 3h: PHY Rx Control0

This register is used to control receiver functionality.

Table 7-5. Address 3h: PHY Rx Control0 (Sheet 1 of 2)

[tbl-65.md](tbl-65.md)

82

Reference Number: 643108, Revision: 7.1

intel®

Table 7-5. Address 3h: PHY Rx Control0 (Sheet 2 of 2)

[tbl-66.md](tbl-66.md)

### 7.1.5 Address 4h: PHY Rx Control1

This register is used to control the receiver functionality.

Table 7-6. Address 4h: PHY Rx Control1 (Sheet 1 of 2)

[tbl-67.md](tbl-67.md)

Reference Number: 643108, Revision: 7.1

83

intel®

Table 7-6. Address 4h: PHY Rx Control1 (Sheet 2 of 2)

[tbl-68.md](tbl-68.md)

### 7.1.6 Address 5h: PHY Rx Control2

This register is used to control receiver functionality.

84

Reference Number: 643108, Revision: 7.1

intel®

Table 7-7. Address 5h: PHY Rx Control2

[tbl-69.md](tbl-69.md)

### 7.1.7 Address 6h: PHY Rx Control3

This register is used to control receiver functionality.

Table 7-8. Address 6h: PHY Rx Control3

[tbl-70.md](tbl-70.md)

### 7.1.8 Address 7h: Elastic Buffer Location Update Frequency

Table 7-9. Address 7h: Elastic Buffer Location Update Frequency

[tbl-71.md](tbl-71.md)

Reference Number: 643108, Revision: 7.1

85

intel®

### 7.1.9 Address 8h: PHY Rx Control4

This register is used to control the receiver functionality.

Table 7-10. Address 8h: PHY Rx Control4

[tbl-72.md](tbl-72.md)

### 7.1.10 Address 9h: PHY Rx Control 5

This register controls receiver functionality.

Table 7-11. Address 9h: PHY Rx Control 5

[tbl-73.md](tbl-73.md)

1. The default value of RxLaneEnable for the RX2 region is 0h.

### 7.1.11 Address 400h: PHY Tx Control0

This register is used to control the transmitter functionality.

Table 7-12. Address 400h: PHY Tx Control0 (Sheet 1 of 2)

[tbl-74.md](tbl-74.md)

86

Reference Number: 643108, Revision: 7.1

intel®

Table 7-12. Address 400h: PHY Tx Control0 (Sheet 2 of 2)

[tbl-75.md](tbl-75.md)

### 7.1.12 Address 401h: PHY Tx Control1

This register is used to control the transmitter functionality.

Table 7-13. Address 401h: PHY Tx Control1

[tbl-76.md](tbl-76.md)

### 7.1.13 Address 402h: PHY Tx Control2

This register is used to control the transmitter functionality.

Table 7-14. Address 402h: PHY Tx Control2 (Sheet 1 of 2)

[tbl-77.md](tbl-77.md)

Reference Number: 643108, Revision: 7.1

87

intel®

Table 7-14. Address 402h: PHY Tx Control2 (Sheet 2 of 2)

[tbl-78.md](tbl-78.md)

88

Reference Number: 643108, Revision: 7.1

intel®

### 7.1.14 Address 403h: PHY Tx Control3

This register is used to control the transmitter functionality.

Table 7-15. Address 403h: PHY Tx Control3

[tbl-79.md](tbl-79.md)

### 7.1.15 Address 404h: PHY Tx Control4

This register is used to control the transmitter functionality.

Table 7-16. Address 404h: PHY Tx Control4

[tbl-80.md](tbl-80.md)

Reference Number: 643108, Revision: 7.1

89

intel®

### 7.1.16 Address 405h: PHY Tx Control5

This register is used to control the transmitter functionality.

Table 7-17. Address 405h: PHY Tx Control5

[tbl-81.md](tbl-81.md)

90

Reference Number: 643108, Revision: 7.1

intel®

### 7.1.17 Address 406h: PHY Tx Control6

This register is used to control the transmitter functionality.

Table 7-18. Address 406h: PHY Tx Control6

[tbl-82.md](tbl-82.md)

### 7.1.18 Address 407h: PHY Tx Control7

This register is used to control the transmitter functionality.

Table 7-19. Address 407h: PHY Tx Control7

[tbl-83.md](tbl-83.md)

### 7.1.19 Address 408h: PHY Tx Control8

This register is used to control the transmitter functionality.

Table 7-20. Address 408h: PHY Tx Control8 (Sheet 1 of 2)

[tbl-84.md](tbl-84.md)

Reference Number: 643108, Revision: 7.1

91

intel®

Table 7-20. Address 408h: PHY Tx Control8 (Sheet 2 of 2)

[tbl-85.md](tbl-85.md)

### 7.1.20 Address 409h: PHY Tx Control9

This register is used to control the transmitter functionality.

Table 7-21. Address 409h: PHY Tx Control9 (Sheet 1 of 2)

[tbl-86.md](tbl-86.md)

92

Reference Number: 643108, Revision: 7.1

intel®

Table 7-21. Address 409h: PHY Tx Control9 (Sheet 2 of 2)

[tbl-87.md](tbl-87.md)

### 7.1.21 Address 40Ah: PHY TX Control 10

This register is used to controller transmitter functionality.

Table 7-22. Address 40Ah: PHY TX Control 10

[tbl-88.md](tbl-88.md)

1. The default value of TxLaneEnable for the RX2 region is 0h.

### 7.1.22 Address 800h: PHY Common Control0

This register is used to control functionalities relevant to both the receiver and the transmitter functionality.

Table 7-23. Address 800h: PHY Common Control0 (Sheet 1 of 2)

[tbl-89.md](tbl-89.md)

Reference Number: 643108, Revision: 7.1

93

intel®

Table 7-23. Address 800h: PHY Common Control0 (Sheet 2 of 2)

[tbl-90.md](tbl-90.md)

### 7.1.23 Address 801h: PHY Near End Loopback Control

This register is required for PHYs that support the optional NELB feature.

Table 7-24. Address 801h: PHY Near End Loopback Control (Sheet 1 of 2)

[tbl-91.md](tbl-91.md)

94

Reference Number: 643108, Revision: 7.1

intel®

Table 7-24. Address 801h: PHY Near End Loopback Control (Sheet 2 of 2)

[tbl-92.md](tbl-92.md)

## 7.2 MAC Registers

Table 7-25 lists the MAC registers and their associated address. The details of each register are provided in the following subsections.

Table 7-25. MAC Registers (Sheet 1 of 2)

[tbl-93.md](tbl-93.md)

Reference Number: 643108, Revision: 7.1

95

**Table 7-25. MAC Registers (Sheet 2 of 2)**

[tbl-94.md](tbl-94.md)

96

Reference Number: 643108, Revision: 7.1

intel®

### 7.2.1 Address 0h: Rx Margin Status0

Table 7-26. Address 0h: Rx Margin Status0

[tbl-95.md](tbl-95.md)

### 7.2.2 Address 1h: Rx Margin Status1

Table 7-27. Address 1h: Rx Margin Status1

[tbl-96.md](tbl-96.md)

### 7.2.3 Address 2h: Rx Margin Status2

Table 7-28. Address 2h: Rx Margin Status2 (Sheet 1 of 2)

[tbl-97.md](tbl-97.md)

Reference Number: 643108, Revision: 7.1

97

intel®

Table 7-28. Address 2h: Rx Margin Status2 (Sheet 2 of 2)

[tbl-98.md](tbl-98.md)

### 7.2.4 Address 3h: Elastic Buffer Status

Table 7-29. Address 3h: Elastic Buffer Status

[tbl-99.md](tbl-99.md)

### 7.2.5 Address 4h: Elastic Buffer Location

Table 7-30. Address 4h: Elastic Buffer Location

[tbl-100.md](tbl-100.md)

### 7.2.6 Address 5h: Rx Status0

Table 7-31. Address 5h: Rx Status0 (Sheet 1 of 2)

[tbl-101.md](tbl-101.md)

98

Reference Number: 643108, Revision: 7.1

intel®

Table 7-31. Address 5h: Rx Status0 (Sheet 2 of 2)

[tbl-102.md](tbl-102.md)

### 7.2.7 Address 6h: Rx Control0

Table 7-32. Address 6h: Rx Control0

[tbl-103.md](tbl-103.md)

### 7.2.8 Address 7h: Rx Margin Status3

Table 7-33. Address 7h: Rx Margin Status3

[tbl-104.md](tbl-104.md)

Table 7-34. Address 8h: Reserved

[tbl-105.md](tbl-105.md)

Table 7-35. Address 9h: Reserved

[tbl-106.md](tbl-106.md)

Reference Number: 643108, Revision: 7.1

99

intel®

### 7.2.9 Address Ah: Rx Link Evaluation Status0

Table 7-36. Address Ah: Rx Link Evaluation Status0

[tbl-107.md](tbl-107.md)

### 7.2.10 Address Bh: Rx Link Evaluation Status1

Table 7-37. Address Bh: Rx Link Evaluation Status1

[tbl-108.md](tbl-108.md)

100

Reference Number: 643108, Revision: 7.1

intel®

#### 7.2.11 Address Ch: Rx Status4

Table 7-38. Address Ch: Rx Status4

[tbl-109.md](tbl-109.md)

Reference Number: 643108, Revision: 7.1

101

intel®

### 7.2.12 Address Dh: Rx Status5

Table 7-39. Address Dh: Rx Status5

[tbl-110.md](tbl-110.md)

### 7.2.13 Address Eh: Rx Link Evaluation Status2

Table 7-40. Address Eh: Rx Link Evaluation Status2

[tbl-111.md](tbl-111.md)

102

Reference Number: 643108, Revision: 7.1

intel®

#### 7.2.14 Address Fh: Rx Link Evaluation Status3

Table 7-41. Address Fh: Rx Link Evaluation Status3

[tbl-112.md](tbl-112.md)

Reference Number: 643108, Revision: 7.1

103

intel®

### 7.2.15 Address 10h: Rx Status6

Table 7-42. Address 10h: Rx Status 6

This register controls receiver functionality.

[tbl-113.md](tbl-113.md)

### 7.2.16 Address 400h: Tx Status0

Table 7-43. Address 400h: Tx Status0

[tbl-114.md](tbl-114.md)

104

Reference Number: 643108, Revision: 7.1

intel®

#### 7.2.17 Address 401h: Tx Status1

Table 7-44. Address 401h: Tx Status1

[tbl-115.md](tbl-115.md)

#### 7.2.18 Address 402h: Tx Status2

Table 7-45. Address 402h: Tx Status2

[tbl-116.md](tbl-116.md)

Reference Number: 643108, Revision: 7.1

105

intel®

### 7.2.19 Address 403h: Tx Status3

Table 7-46. Address 403h: Tx Status3

[tbl-117.md](tbl-117.md)

### 7.2.20 Address 404h: Tx Status4

Table 7-47. Address 404h: Tx Status4

[tbl-118.md](tbl-118.md)

### 7.2.21 Address 405h: Tx Status5

Table 7-48. Address 405h: Tx Status5

[tbl-119.md](tbl-119.md)

### 7.2.22 Address 406h: Tx Status6

Table 7-49. Address 406h: Tx Status6

[tbl-120.md](tbl-120.md)

106

Reference Number: 643108, Revision: 7.1

intel®

#### 7.2.23 Address 407h: Tx Status7

Table 7-50. Address 407h: Tx Status7

[tbl-121.md](tbl-121.md)

#### 7.2.24 Address 408h: Tx Status8

Table 7-51. Address 408h: Tx Status8

[tbl-122.md](tbl-122.md)

#### 7.2.25 Address 409h: Tx Status9

Table 7-52. Address 409h: Tx Status9

[tbl-123.md](tbl-123.md)

#### 7.2.26 Address 40Ah: Tx Status10

Reference Number: 643108, Revision: 7.1

107

intel®

Table 7-53. Address 40Ah: Tx Status10

[tbl-124.md](tbl-124.md)

### 7.2.27 Address 40Bh: Tx Status11

Table 7-54. Address 40Bh: TxStatus11

[tbl-125.md](tbl-125.md)

### 7.2.28 Address 40Ch: Tx Status12

Table 7-55. Address 40Ch: TxStatus12

[tbl-126.md](tbl-126.md)

### 7.2.29 Address 800h: Near End Loopback Status

This register is required only for PHYs that support the optional NELB feature.

Table 7-56. Address 800h: Near End Loopback Status (Sheet 1 of 2)

[tbl-127.md](tbl-127.md)

108

Reference Number: 643108, Revision: 7.1

intel®

Table 7-56. Address 800h: Near End Loopback Status (Sheet 2 of 2)

[tbl-128.md](tbl-128.md)

Reference Number: 643108, Revision: 7.1

109

intel®

# 8 PIPE Operational Behavior

## 8.1 Clocking

There are three clock signals used by the PHY interface component. The first clock (CLK) is a reference clock that the PHY uses to generate internal bit rate clocks for transmitting and receiving data. The specifications for this signal are implementation-dependent and must be fully specified by vendors. The specifications may vary for different PHY operating modes. This clock may have a spread spectrum modulation that matches a system Reference Clock (REFCLK) (for example, the spread spectrum modulation could come from a REFCLK from the Card Electro-Mechanical Specification [CEMS]).

The second clock (PCLK) is an output from the PHY in "PCLK as PHY Output" mode and an input to each PHY lane in the "PCLK as PHY Input" mode and is the parallel interface clock used to synchronize data transfers across the parallel interface. This clock runs at a rate dependent on the Rate, PCLK Rate, and PHY Mode control inputs and data interface width. The rising edge of this clock is the reference point. This clock may also have a spread spectrum modulation. The CLK and PCLK must be sourced from the same reference clock and must contain the same clocking characteristics, that is, they can be mesochronous with each other.

The third clock (MAX PCLK) is a constant frequency clock with a frequency determined by the maximum signaling rate supported by the PHY and is only required in "PCLK as PHY Input" mode or in all modes for a PHY that supports PCIe at 8 GT/s or higher maximum speed. The Max PCLK value should be set to the maximum PCLK supported by the PHY.

The fourth clock (MacCLK) is an optional clock with support advertised by the PHY vendor parameter "MacCLK Support". This clock is independent of the data lanes and is specified using MacCLK lane signals.

### 8.1.1 Clocking Topologies

This section describes some clocking topologies that are compatible with PIPE. Figure 8-1 shows PCLK as a PHY output. This topology is only applicable for legacy PIPE implementations and is not supported for PCIe Gen5 designs, USB4 or DisplayPort. Figure 8-2 shows PCLK as a PHY input with the PLL residing in the PHY; the PHY provides a source for PCLK, in this case, MAX PCLK, that is mesochronous to the PHY's bit rate clock. Figure 8-3 shows the PCLK as a PHY input with the PLL that provides the PCLK source residing outside of the PHY; the reference clock for PLL that sources the bit rate clock and the PLL that provides the PCLK source must be the same. Figure 8-4 shows CLK as a PHY input with a single PLL that provides the source for PCLK as well as for the bit rate clock.

110

Reference Number: 643108, Revision: 7.1

intel®

Figure 8-1. PCLK as PHY Output

![img-22.jpeg](img-22.jpeg)

Reference Number: 643108, Revision: 7.1

111

intel®

Figure 8-2. PCLK as PHY Input with a PHY-Owned PLL

![img-23.jpeg](img-23.jpeg)

112

Reference Number: 643108, Revision: 7.1

intel®

Figure 8-3. PCLK as PHY Input with an External PLL and PHY PLL

![img-24.jpeg](img-24.jpeg)

Reference Number: 643108, Revision: 7.1

113

intel®

Figure 8-4. PCLK as PHY Input with External PLL

![img-25.jpeg](img-25.jpeg)

### 8.1.2 MacCLK Clocking Scheme

The MacCLK is an optional clock that is independent of data lanes. MacCLK frequency is controlled via a MacCLK lane. Figure 8-5 shows the signals associated with a single MacCLK lane. Multiple MacCLK lanes may be implemented; for example, DisplayPort and USB4 implementations are likely to implement two lanes. Some implementations may choose to map a MacCLK lane to a specific data lane with a direct correlation to PCLK. Each MacCLK lane consists of the following signals: MacCLKReset#, MacCLK, MacCLKReq, MacCLKSSCEnable, MacCLKAck, MacCLKPHYMode, and MacCLKRate.

114

Reference Number: 643108, Revision: 7.1

intel®

Figure 8-5. MacCLK Lane

![img-26.jpeg](img-26.jpeg)

The following rules apply to each MacCLK lane:

- MacCLKPHYMode, MacCLKRate, MacCLKSSCEnable, MacCLKReq, MacCLKAck must be at a valid value at MacCLKReset# deassertion.
- MacCLKPHYMode must not change after MacCLKReset# deassertion.
- Once MacCLK is running, it must remain stable until MacCLKReq is deasserted.
- Signals that affect MacCLK frequency are sampled only on the rising edge of MacCLKReq.
- MacCLKRate is permitted to change only when MacCLKReq and MacCLKAck are deasserted.
- MACCLKSSCEnable is permitted to be dynamically asserted or deasserted while MacCLK is running. The PHY specifies the maximum time it takes to complete a SSC enable or disable via the MaxSSCEnableDisableTime parameter.
- MacCLKRate defines an override encoding that indicates that a vendor specific mechanism of specifying MacCLK frequency is used.

Figure 8-6 illustrates basic MacCLK operation that follows the above described rules. In this example, MacCLK is requested at an initial rate; subsequently, MacCLKReq and MacCLKAck deassert before a new rate is requested.

Figure 8-6. Basic MacCLK Lane Operation

![img-27.jpeg](img-27.jpeg)

Reference Number: 643108, Revision: 7.1

115

intel®

## 8.2 Reset

When the MAC wants to reset the PHY (for instance, during the initial power-on), the MAC must hold the PHY in reset until the power and CLK to the PHY are stable. For PCLK as a PHY output, the PHY signals that PCLK and the MAX PCLK are valid (that is, the PCLK or the MAX PCLK has been running at its operational frequency for at least one clock) and the PHY is in the specified power state by the deassertion of PhyStatus after the MAC has stopped holding the PHY in reset. The MAC must not perform any operational sequences until the PhyStatus is returned for the Reset# deassertion. While Reset# is asserted, the MAC should have TxDetectRx/Loopback deasserted, TxElecIdle asserted, TxCompliance deasserted, PowerDown = P1 (PCIe mode) or PowerDown = P2 (USB Mode), or PowerDown set to the default value reported by the PHY (SATA Mode), PHY mode set to the desired PHY operating mode, SerDesArch configured for PIPE or SerDes architecture, DP_Mode_Tx_Rx set to desired mode, and Rate set to 2.5 GT/s signaling rate for a PHY in PCIe mode or 5.0 GT/s or 10 GT/s (highest supported) for a PHY in USB mode or any rate supported by the PHY in SATA mode. The state of TxSwing during the Reset# assertion is implementation specific. RxTermination assertion in USB mode is implementation specific.

Figure 8-7. Reset# Deassertion and PhyStatus for PCLK as PHY Output

![img-28.jpeg](img-28.jpeg)

## 8.3 Power Management

### 8.3.1 Power Management – PCIe Mode

The power management signals allow the PHY to minimize power consumption. The PHY must meet all timing constraints provided in the PCIe Base Specification regarding clock recovery and link training for the various power states. The PHY must also meet all terminations requirements for transmitters and receivers.

Four standard power states are defined: P0, P0s, P1, and P2. The P0 state is the normal operational state for the PHY. When directed from P0 to a lower power state, the PHY can immediately take whatever power saving measures are appropriate. A PHY is allowed to implement additional PHY-specific power states; the L1 substate support requires implementation of additional PHY-specific power states. A MAC may use any of the PHY specific states as long as the PCIe Base Specification requirements are still met.

In states P0, P0s, and P1, the PCLK is required to be kept operational. For all state transitions between these three states and any PHY-specific states where PCLK is operational, the PHY indicates successful transition into the designated power state by a single cycle assertion of PhyStatus. Transitions into and out of a P2 or a PHY-specific

116

Reference Number: 643108, Revision: 7.1

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

intel®

Figure 8-8. PCIe P2 Entry and Exit with PCLK as PHY Output

![img-29.jpeg](img-29.jpeg)

Figure 8-9. PCIe P2 Entry and Exit with PCLK as PHY Input

![img-30.jpeg](img-30.jpeg)

There is a limited set of legal power state transitions that a MAC can ask the PHY to make. Those legal transitions are: P0 to P0s, P0 to P1, P0 to P2, P0s to P0, P1 to P0, and P2 to P0. The PCIe Base Specification also describes what causes those state transitions.

Transitions to and from any pair of PHY power states including at least one PHY specific power state are also allowed by PIPE (unless otherwise prohibited). However, a MAC must ensure that PCIe Base Specification timing requirements are met.

For L1 substate entry, the PHY must support a state where PCLK is disabled, the REFCLK can be removed, and the Rx electrical idle and Tx common mode are on; this can be P2 or a P2-like state. Figure 8-8 illustrates how a transition into and out of an L1 substate could occur. P2 or a P2-like state maps to L1.Idle; and the PhyStatus and AsyncPowerChangeAck signals are used as described earlier in this section. Alternatively, the PHY may implement a L1 substate management using a single PowerDown[3:0] encoding augmented with the RxEIDetectDisable and TxCommonModeDisable signals; the PowerDown state must remain constant across L1 substate transitions when this alternative mechanism is used. Using distinct PowerDown[3:0] encodings to define the L1 substates allows flexibility to specify different exit latencies; while using RxEIDetectDisable and TxCommonModeDisable, it

118

Reference Number: 643108, Revision: 7.1

intel®

may eliminate the need to do a handshake with AsyncPowerChangeAck. The PHY may support either mechanism or both; this capability must be advertised in the PHY datasheet. The sideband mechanism of L1 substate management via RxEIDetectDisable and TxCommonModeDisable requires PCLK as PHY input mode.

Figure 8-10. L1 SubState Entry and Exit with PCLK as PHY Output

![img-31.jpeg](img-31.jpeg)

### 8.3.2 Power Management – USB Mode

The power management signals allow the PHY to minimize power consumption. The PHY must meet all timing constraints provided in the USB 3.2 Specification regarding clock recovery and link training for the various power states. The PHY must also meet all termination requirements for transmitters and receivers.

Four power states are defined: P0, P1, P2, and P3. The P0 state is the normal operational state for the PHY. When directed from P0 to a lower power state, the PHY can immediately take whatever power saving measures are appropriate.

In the states P0, P1 and P2, the PCLK must be kept operational. For all state transitions between these three states, the PHY indicates successful transition into the designated power state by a single cycle assertion of PhyStatus. Transitions into and out of P3 are described in following subsections. For all power state transitions, the MAC must not begin any operational sequences or further power state transitions until the PHY has indicated that the initial state transition is completed.

Mapping of PHY power states to states in the LTSSM found in the USB Specification are included in following subsections. A MAC may alternately use PHY-specific states as long as the base specification requirements are still met:

- P0 state: All internal clocks in the PHY are operational. P0 is the only state where the PHY transmits and receives USB signaling.
- P0 is the appropriate PHY power management state for all cases where the link is in U0 and all other link state except those listed in following entries for P1, P2, and P3.
- P1 state: PCLK must stay operational. The MAC will move the PHY to this state only when the PHY is transmitting idles and receiving idles. The P1 state can be used for the U1 link state.
- P2 state: Selected internal clocks in the PHY can be turned off. PCLK must stay operational. The MAC will move the PHY to this state only when both transmit and receive channels are idle. The PHY must not indicate successful entry into P2 (by asserting PhyStatus) until PCLK is stable and the operating DC common mode voltage is stable and within specification (as per the base specification).
- P2 can be used for the U2, Rx.Detect, and SS.Inactive.

Reference Number: 643108, Revision: 7.1

119

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

intel®

Figure 8-11. USB U1 Exit

![img-32.jpeg](img-32.jpeg)

### 8.3.3 Power Management – USB4 Mode

The power management signals allow the PHY to minimize power consumption. The PHY must meet all timing and electrical constraints provided in the USB4 Specification regarding link states for the various power states.

Seven power states (P0, P0rx, P1, P2, P3, P4, and P0tx) are defined to fully optimize the power consumption of USB4 link states. The PHY must support all the power states that correspond to PowerDown encodings of 0 through 3 specified in Table 8-1. The power states in the table corresponding to PowerDown encodings of 4 and 5 are optional. The PHY is permitted to implement additional PHY-specific power states.

Table 8-1 provides suggested mappings of power states to USB4 link states, however, the MAC is permitted to choose alternate mappings using PHY implementation-specific states as long as the USB4 base specification requirements are met.

Table 8-1. USB4 PHY Power States (Sheet 1 of 2)

[tbl-129.md](tbl-129.md)

Reference Number: 643108, Revision: 7.1

121

intel®

Table 8-1. USB4 PHY Power States (Sheet 2 of 2)

[tbl-130.md](tbl-130.md)

1. LFPS detector enablement is controlled by the MAC in the case that the PHY implements the "RxEIDetectDisable" control wire.

2. The total latency is defined as the time interval to enter a state and exit back to P0. The intention is to ensure the return to a fully active state in the case of wake event race scenario. Budget includes turn OFF and ON of PLL when the power state allows. In the case that the PHY has completed the entry phase, this delay can be considered as the exit latency budget in which the PHY can take extra power optimizations.

Additional descriptions of each power state are:

- P0: Fully active the power state. The transmitter and receiver are ON.
- P0rx: Transmitter only power state. The receiver is OFF. Suitable for unidirectional traffic (for instance, transmitting the tunneled DisplayPort traffic).
- P1: Transmitter and receiver are OFF. This power state provides power savings while meeting low latency exit requirements.
- P2: Similar to P1 but with an increased total latency budget. The MAC is permitted to turn off the PLL in this state.
- P3: Shutdown mode, this is the lowest power consumption state. The link is virtually disconnected (CLd). Wake events are propagated via a sideband channel so common mode and LFPS detector are turned off. This state is suitable for deep sleep.
- P4: Transmitter and receiver are OFF with a total latency of up to 100 us delay. This state is suitable where higher exit latencies are tolerated (for example, storage devices).
- P0tx: Receiver only mode, the transmitter is OFF. Suitable for unidirectional traffic (for example, receiving tunneled DP traffic).

### 8.3.4 Power Management – SATA Mode

The power management signals allow the PHY to minimize power consumption. The PHY must meet all timing constraints provided in the SATA specification regarding clock recovery and link training for the various power states. The PHY must also meet all termination requirements for transmitters and receivers.

122

Reference Number: 643108, Revision: 7.1

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

intel®

Figure 8-12. DeepPMReq#/DeepPMAck# Handshake Sequencing

![img-33.jpeg](img-33.jpeg)

### 8.3.6.2 Power Removal and PHY Context Restoration after Power is Restored

Before power gating or a power rail removal in a deep power management state, a PHY may choose to save internal context to a location outside of the PHY as a power savings optimization. The MAC must guarantee that the PIPE interface is idle with no outstanding operations before the power removal. The mechanism for saving context is not part of the PIPE specification, however, the PIPE specification does define a restore window during which context is restored and specifies required MAC and PHY behavior during and immediately after the restore window.

The MAC notifies the PHY of entry to the restore window through the assertion of Restore#. The exit from the restore window is signaled via the deassertion of the Restore# signal. The Restore# must be asserted before a power rail ramp. During the restore window, all context that was saved off before a power gating or the power rail removal is restored; during this time, the MAC and the PHY must ignore any toggling of any input PIPE interface signals, except for PCLK and the Restore# signal. Upon an exit from the restore window, the MAC and the PHY must immediately resume monitoring of the input PIPE interface signals. After an exit from the restore window, the MAC and the PHY must wait for PCLK to become active and to toggle for a minimum of 32 cycles before toggling any PIPE signals that are synchronous to PCLK. Figure 8-13 illustrates the key requirements before a power removal and around the restore window.

Figure 8-13. PHY Context Restoration after the Power is Restored

![img-34.jpeg](img-34.jpeg)

Reference Number: 643108, Revision: 7.1

125

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

intel.

### 8.4.2 USB Mode

The signaling rate of the link, PCLK rate, or the Data Bus Width can be changed only when the PHY is in the P0 or P2 power state and TxElecIdle and RxStandby are asserted. Any combination of at least two of the rate and width and PCLK rate, can be changed simultaneously. The MAC is not allowed to change only one of the three. When the MAC changes the Rate signal, and/or the Width signal, and/or the PCLK rate signal in PCLK as PHY Output mode, the PHY performs the rate change and/or the width change and/or the PCLK rate change and signals its completion with a single cycle assertion of PhyStatus. The MAC must not perform any operational sequences, power state transitions, deassert TxElecIdle or RxStandby, or further signaling rate changes until the PHY has indicated that the signaling rate change has completed. The sequence is the same in PCLK as PHY Input mode except the MAC needs to know when the input PCLK rate or Rate can be safely changed. After the MAC changes PCLK_Rate the change to the PCLK can happen only after the PclkChangeOk output has been driven high by the PHY. The MAC changes the input PCLK, and then handshakes by asserting PclkChangeAck. The PHY responds by asserting PhyStatus for one input PCLK cycle and deasserts PclkChangeOk on the trailing edge of PhyStatus. Note that PclkChangeOk is only used by the PHY if the MAC changes the PCLK_Rate or Rate. The MAC deasserts PclkChangeAck when PclkChangeOk is sampled low and may deassert an TxElecIdle and/or RxStandby after the PhyStatus is sampled high.

Some PHY architectures may allow a speed change and a power state change to occur at the same time as a rate, width, or rate change. If a PHY supports this, the MAC must change the rate, width, or rate at the same PCLK edge that it changes the PowerDown signals. This can happen when transitioning the PHY from P0 to either P2 or P3 states. The completion mechanisms are the same as previously defined for the power state changes and indicate not only that the power state change is complete, but also that the rate, width, or rate change is complete.

### 8.4.3 SATA Mode

The signaling rate of the link, PCLK rate, or the data bus width can be changed only when the PHY is in POWER_STATE_0 a prnd TxElecIdle and RxStandby are asserted, or in a low-power state where the PCLK is provided. When the MAC changes the Rate signal, and/or the Width signal, and/or the PCLK rate signal in PCLK as PHY Output mode, the PHY performs the rate change, the width change, or the PCLK rate change and signals its completion with a single cycle assertion of PhyStatus. The MAC must not perform any operational sequences, power state transitions, deassert TxElecIdle, or RxStandby, or further signaling rate or width changes until the PHY has indicated that the change has completed.

The sequence is the same in the PCLK as the PHY Input mode except the MAC needs to know when the input PCLK rate can be safely changed. After the MAC changes PCLK_Rate, the change to the PCLK can happen only after the PclkChangeOk output has been driven high by the PHY. The MAC changes the input PCLK, and then handshakes by asserting PclkChangeAck. The PHY responds by asserting PhyStatus for one input PCLK cycle and deasserts PclkChangeOk on the trailing edge of PhyStatus. Note that PclkChangeOk is only used by the PHY if the MAC changes PCLK_Rate. The MAC deasserts PclkChangeAck when PclkChangeOk is sampled low and may deassert TxElecIdle and/or RxStandby after PhyStatus is sampled high.

There are instances where conditions indicate both a speed change, width, and PCLK rate change and a power state change for the PHY. In such cases, the MAC must change the signaling rate, width, or rate, before changing the power state.

Reference Number: 643108, Revision: 7.1

127

intel®

Some PHY architectures may allow a speed change and a power state change to occur at the same time as a rate, width, or rate change. If a PHY supports this, the MAC must change the rate, width, or rate at the same PCLK edge that it changes the PowerDown signals. The completion mechanisms are the same as previously defined for the power state changes and indicate not only that the power state change is complete, but also that the rate, width, or rate change is complete.

### 8.4.4 Fixed Data Path Implementations

The following figure shows the logical timings for implementations that change PCLK frequency when the MAC changes the signaling rate and PCLK is a PHY Output. Implementations that change the PCLK frequency when changing signaling rates must change the clock such that the time the clock is stopped (if it is stopped) is minimized to prevent any timers using PCLK from exceeding their specifications. In addition, during the clock transition period, the frequency of PCLK must not exceed the PHY's defined maximum clock frequency. The amount of time between when Rate is changed and the PHY completes the rate change is a PHY-specific value. These timings also apply to implementations that keep the data path fixed by using options that make use of the TxDataValid and RxDataValid signals.

Figure 8-14. Rate Change with Fixed Data Path

![img-35.jpeg](img-35.jpeg)

Figure 8-15 shows the logical timings for an implementation that changes the PCLK frequency when the MAC changes the signaling rate and PCLK is a PHY Input.

Figure 8-15. Change from PCIe 2.5 Gt/s to 5.0 Gt/s with PCLK as PHY Input

![img-36.jpeg](img-36.jpeg)

### 8.4.5 Fixed PCLK Implementations

Figure 8-16 shows the logical timings for implementations that change the width of the data path for different signaling rates. PCLK may be stopped during a rate change. These timings also apply to fixed PCLK implementations that make use of the TxDataValid and RxDataValid signals.

128

Reference Number: 643108, Revision: 7.1

intel®

Figure 8-16. Rate Change with Fixed PCLK Frequency

![img-37.jpeg](img-37.jpeg)

## 8.5 Transmitter Margining – PCIe Mode and USB Mode

While in the P0 power state, the PHY can be instructed to change the value of the voltage at the transmitter pins. When the MAC changes TxMargin[2:0], the PHY must be capable of transmitting with the new setting within 128 ns.

There is a limited set of legal TxMargin[2:0] and Rate combinations that a MAC can select. See the PCIe base specification for a complete description of legal settings when the PHY is in PCIe mode. The USB specification for a complete description of the legal settings when the PHY is in USB mode.

Figure 8-17. Selecting Tx Margining Value

![img-38.jpeg](img-38.jpeg)

Selecting Tx Margining value

Reference Number: 643108, Revision: 7.1

129

intel®

## 8.6 Selectable De-Emphasis – PCIe Mode

While in the P0 power state and transmitting at 5.0 GT/s, 8.0 GT/s, 16 GT/s, 32 GT/s, 64 GT/s, or 128 GT/s, the PHY can be instructed to change the value of the transmitter equalization. When the signaling rate is 5.0 GT/s and the MAC changes TxDeemph, the PHY must be capable of transmitting with the new setting within 128 ns. When the signaling rate is 8.0 GT/s, 16 GT/s, 32 GT/s, 64 GT/s, or 128 GT/s and the MAC changes TxDeemph, the PHY must be capable of transmitting with the new setting within 256 ns.

There is a limited set of legal TxDeemph and Rate combinations that a MAC can select. See the PCIe base specification for a complete description.

The MAC must ensure that TxDeemph is selecting -3.5 db whenever Rate is selecting 2.5 GT/s.

Figure 8-18. Selecting Tx De-Emphasis Value

![img-39.jpeg](img-39.jpeg)

Selecting Tx De-emphasis value

## 8.7 Receiver Detection – PCIe Mode and USB Mode

While in the P1 or optionally P2 power state and PCIe mode or in the P2 or P3 power state and USB mode, the PHY can be instructed to perform a receiver detection operation to determine if there is a receiver at the other end of the link. Basic operation of receiver detection is that the MAC requests the PHY to do a receiver detect sequence by asserting TxDetectRx/Loopback. When the PHY has completed the receiver detect sequence, it asserts PhyStatus for one clock and drives the RxStatus signals to the appropriate code. After the receiver detection has completed (as signaled by the assertion of PhyStatus), the MAC must deassert TxDetectRx/Loopback before initiating another receiver detection, a power state transition, or signaling a rate change.

Once the MAC has requested a receiver detect sequence (by asserting TxDetectRx/Loopback), the MAC must leave TxDetectRx/Loopback asserted until after the PHY has signaled completion by the assertion of PhyStatus. When receiver detection is performed in USB mode with the PHY in P3 or PCIe in P2, the PHY asserts PhyStatus and signals the appropriate receiver detect value until the MAC deasserts TxDetectRx/Loopback.

130

Reference Number: 643108, Revision: 7.1

intel®

Figure 8-19. Receiver Detect – Receiver Present

![img-40.jpeg](img-40.jpeg)

[tbl-133.md](tbl-133.md)

### 8.8 Transmitting a Beacon – PCIe Mode

When the PHY has been put in the P2 power state, and the MAC wants to transmit a beacon, the MAC deasserts TxElecIdle and the PHY should generate a valid beacon until TxElecIdle is asserted. The MAC must assert TxElecIdle before transitioning the PHY to P0.

Figure 8-20. Beacon Transmit

![img-41.jpeg](img-41.jpeg)

Reference Number: 643108, Revision: 7.1

131

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

intel®

Figure 8-22. LFPS Transmit for USB4 and DisplayPort Modes

![img-43.jpeg](img-43.jpeg)

t1 - MAC informs the PHY that the MAC plans to transmit LFPS
t2 - MAC starts transmitting LFPS over the parallel data interface
t3 - MAC stops transmitting LFPS over the parallel data interface
t4 - MAC starts transmitting High Speed data over parallel data interface

The transitional time window (t2-t1) allows the PHY time to adjust any parameters necessary for transmitting LFPS. The minimum time and maximum time must be specified in the PHY datasheet (MinTimeBeforeLFPS and MaxTimeBeforeLFPS) for each protocol.

The transitional time window (t4-t3) returns the link to Electrical Idle to allow the PHY time to restore parameters necessary for high-speed transmission. The minimum time must be specified in the PHY datasheet (MinTimeEIAfterLFPS) for each protocol.

### 8.11 Detecting a Beacon – PCIe Mode

The PHY receiver must monitor at all times (except during reset or when RxEIDetectDisable is set) for electrical idle. When the PHY is in the P2 power state, and RxElecIdle is deasserted, then a beacon is being detected.

Figure 8-23. Beacon Receive

![img-44.jpeg](img-44.jpeg)

Reference Number: 643108, Revision: 7.1

133

intel®

### 8.12 Detecting Low Frequency Periodic Signaling – USB Mode

The PHY receiver must monitor at all times (except during reset, when Rx terminations are removed, or when RxEIDetectDisable is set) for LFPS. When the PHY is in the P0, P1, P2, or P3 power state, and RxElecIdle is deasserted, then LFPS is being detected. The length of time RxElecIdle is deasserted indicates the length of time Low Frequency Periodic Signaling is detected. See to Chapter 6 in the USB 3.0 specification for more details on the length of LFPS for various events.

The PHY needs to differentiate LPFS received for Ping from Exit LFPS. When the PHY receives LFPS for up to two cycles only, it should deassert RxElecIdle for a maximum of 200 ns. For U1, there is a strict latency requirement for a USB controller to detect and respond back as defined in the USB specification Chapter 6 LPFS section. The PHY should not take more than 120 ns to deassert RxElecIdle after detecting LFPS in P0 and P1, and P2. For P3, the PHY is allowed to take us to 10us to deassert RxElecIdle.

Figure 8-24. LFPS Receive

![img-45.jpeg](img-45.jpeg)

### 8.13 Detecting Low Frequency Periodic Signaling in USB4 Mode

The PHY receiver must monitor for LFPS at all times when RxEIDetectDisable is clear. When the PHY is in P0, P1, P2 or P4 power state, it must deassert RxElecIdle when LFPS is detected. The length of time RxElecIdle is deasserted indicates the length of time LPFS is detected.

### 8.14 Clock Tolerance Compensation

Note: This section is not applicable to SerDes architecture.

The PHY receiver contains an elastic buffer used to compensate for differences in frequencies between bit rates at the two ends of a Link. The elastic buffer must be capable of holding enough symbols to handle worst case differences in frequency and worst-case intervals between symbols that can be used for rate compensation for the selected PHY mode.

Two models are defined for the elastic buffer operation in the PHY. The PHY may support one or both models. The Nominal Empty buffer model is only supported in PCIe, USB, or SATA Mode.

134

Reference Number: 643108, Revision: 7.1

intel®

For the Nominal Empty buffer model, the PHY attempts to keep the elasticity buffer as close to empty as possible. In the Nominal Empty mode, the PHY uses the RxDataValid interface to tell the MAC when no data is available. The Nominal Empty buffer model provides a smaller worst case and average latency than the Nominal Half Full buffer model, but it requires the MAC to support the RxDataValid signal. The PHY removes all SKP symbols in Nominal Empty buffer mode.

For the Nominal Half Full buffer model, the PHY is responsible for inserting or removing SKP symbols, ordered sets, or ALIGNs in the received data stream to avoid elastic buffer overflow or underflow. The PHY monitors the receive data stream, and when a Skip ordered set or ALIGN is received, the PHY can add or remove one SKP symbol (PCIe Mode at 2.5 or 5 GT/s), four SKP symbols (PCIe Mode at 8 GT/s, 16 GT/s, or 32 GT/s), one SKP ordered set (USB Mode at 5 GT/s), or one ALIGN from each SKP or ALIGN as appropriate to manage its elastic buffer to keep the buffer as close to half full as possible. In USB mode at 5 GT/s, the PHY must only add or remove SKP ordered sets. In USB mode at 10 GT/s, the PHY must only add or remove multiples of four SKP symbols. Whenever the SKP symbols or an ordered set is added to or removed, the PHY will signal this to the MAC using the RxStatus[2:0] signals. These signals have a non-zero value for one clock cycle and indicate whether an SKP symbol or ordered set was added to or removed from the received SKP ordered sets. For PCIe, the timing of RxStatus[2:0] assertion depends on the operational rate since SKP ordered sets are encoded differently in 8b/10b mode versus 128/130b mode. In PCIe mode at 2.5 or 5 GT/s, RxStatus[2:0] must be asserted during the clock cycle when the COM symbol of the SKP ordered set is moved across the parallel interface. In PCIe mode at 8 GT/s, 16 GT/s, or 32 GT/s, RxStatus[2:0] must assert anytime between and including the start of the SKP ordered set and the SKP_END symbol. In SATA mode, whenever an ALIGN symbol is added or removed, the PHY will signal this to the MAC using the RxStatus[2:0] signals. These signals have a non-zero value for one clock cycle and indicate whether an ALIGN was added or removed. RxStatus must be asserted during the clock cycle when the first symbol of the added ALIGN is moved across the parallel interface.

In PCIe mode, the rules for operating in Nominal Empty buffer mode are as follows:

- Use of the RxDataValid is required.
- All SKP symbols of SOS are removed (8b/10b SKP or 128/130 AA).
- When an empty condition happens (caused by clock drift or SOS removal):
  - RxValid must remain high.
    - RxValid should only be dropped for symbol alignment loss or block alignment loss.
  - RxDataValid must be deasserted.
  - RxStatus must be 0.

- EB full can still occur and is considered an error.
- Notification of an SOS coming through the EB must be reported in the following manner:

- 8b/10b: COM of SOS must be passed with RxStatus = SKP removed (010), SKP symbols dropped.

- 128/130: Start of SOS block, with first byte SKP_END or SKP_END_CTRL, must be passed with RxStatus = SKP Removed (010), all AA SKP symbols dropped.

- The EB is permitted to start RxDataValid as soon as data is available, but should never assert faster than the usual RxDataValid rate.

Reference Number: 643108, Revision: 7.1

135

intel®

- That is: rate=1, width=2, pclk_rate=2, RxDataValid should never assert for two consecutive pclk cycles.
- That is: rate=1, width=2, pclk_rate=3, RxDataValid assertions must always have at least 3 pclk cycles of de-assertion between them.

• Example of valid optimization by EB:

- Rate=1, width=2, pclk_rate=3
- RxDataValid (t=0, t=1, and so forth, E=EB Empty): 100010001000100000000000000000000000000000000000000000000000000000000000000000000000000000
— Vs. non-optimized: 1000100010001000EE00100010001
— Non-optimized design builds EB depth in-order to maintain RxDataValid fixed cycle rate

In USB mode for the Nominal Empty buffer model the PHY attempts to keep the elasticity buffer as close to empty as possible. This means that the PHY will be required to insert SKP ordered sets into the received data stream when no SKP ordered sets have been received, unless the RxDataValid signal is used. The Nominal Empty buffer model provides a smaller worst case and average latency than the Nominal Half Full buffer model, but it requires the MAC to support receiving SKP ordered sets any point in the data stream.

In SATA mode for the Nominal Empty buffer model the PHY attempts to keep the elasticity buffer as close to empty as possible. In Nominal Empty mode the PHY uses the RxDataValid interface to tell the MAC when no data is available. The Nominal Empty buffer model provides a smaller worst case and average latency than the Nominal Half Full buffer model, but it requires the MAC to support the RxDataValid signal.

It is recommended that a PHY and MAC support the Nominal Empty buffer model in USB mode using the RxDataValid signal. The alternative of inserting SKPs in the data stream when no SKPs have been received is not recommended. The following figure shows a sequence where a PHY operating in PCIe Mode added an SKP symbol in the data stream.

Figure 8-25. Clock Correction – Add an SKP

![img-46.jpeg](img-46.jpeg)

Figure 8-26 shows a sequence where a PHY operating in PCIe mode removed an SKP symbol from an SKP ordered set that only had one SKP symbol, resulting in a "bare" COM transferring across the parallel interface.

136

Reference Number: 643108, Revision: 7.1

intel®

Figure 8-26. Clock Correction – Remove an SKP

![img-47.jpeg](img-47.jpeg)

### 8.15 Error Detection

The PHY is responsible for detecting receive errors of several types. These errors are signaled to the MAC layer using the receiver status signals (RxStatus[2:0]). Because of higher level error detection mechanisms (like CRC) built into the Data Link layer, there is no need to specifically identify symbols with errors, but reasonable timing information about when the error occurred in the data stream is important. When a receive error occurs, the appropriate error code is asserted for one clock cycle at the point in the data stream across the parallel interface closest to where the error actually occurred. There are four error conditions (five for SATA mode) that can be encoded on the RxStatus signals. If more than one error should happen to occur on a received byte (or set of bytes transferred across a 16-bit, 32-bit, or 64-bit interface), the errors should be signaled with the priority shown as follows:

1. 8B/10B decode error or block decode error
2. Elastic buffer overflow
3. Elastic buffer underflow (Cannot occur in Nominal Empty buffer model)
4. Disparity errors
5. Misalign (SATA mode only)

If an error occurs during an SKP ordered set or ALIGN, such that the error signaling and SKP or ALIGN added and removed signaling on RxStatus would occur on the same PCLK, then the error signaling has precedence.

Note that the PHY does not signal 128/130B (PCIe) or 128/132B (USB) header errors. The raw received header bits are passed across the interface and the controller is responsible for any block header error detection and handling.

### 8.15.1 8B/10B Decode Errors

For a detected 8B/10B decode error, the PHY should place an End Bad (EDB) symbol (for PCIe or SATA) or SUB symbol (for USB) in the data stream in place of the bad byte, and encode RxStatus with a decode error during the clock cycle when the affected byte is transferred across the parallel interface. In the following example, the receiver

Reference Number: 643108, Revision: 7.1

137

intel®

is receiving a stream of bytes Rx-a through Rx-z, and byte Rx-f has an 8B/10B decode error. In place of that byte, the PHY places an EDB (for PCIe or SATA) or SUB (for USB) on the parallel interface, and it sets RxStatus to the 8B/10B decode error code. Note that a byte that cannot be decoded may also have bad disparity, but the 8B/10B error has precedence. Also note that for greater than 8-bit interface, if the bad byte is on the lower byte lane, one of the other bytes may have bad disparity, but again, the 8B/10B error has precedence.

Figure 8-27. 8B/10B Decode Error

![img-48.jpeg](img-48.jpeg)

### 8.15.2 Disparity Errors

For a detected disparity error, the PHY should assert RxStatus with the disparity error code during the clock cycle when the affected byte is transferred across the parallel interface. For greater than 8-bit interfaces, it is not possible to discern which byte (or possibly both) had the disparity error. In the following example, the receiver detected a disparity error on either (or both) Rx-e or Rx-f data bytes, and it indicates this with the assertion of RxStatus. Optionally, the PHY can signal disparity errors as 8B/10B decode error (using code 0b100). (MACs often treat 8B/10B errors and disparity errors identically). When operating in the USB mode, signaling disparity errors is optional.

Figure 8-28. Disparity Error

![img-49.jpeg](img-49.jpeg)

138

Reference Number: 643108, Revision: 7.1

intel®

### 8.15.3 Elastic Buffer Errors

For elastic buffer errors, an underflow should be signaled during the clock cycle or clock cycles when a spurious symbol is moved across the parallel interface. The symbol moved across the interface should be the EDB symbol (for PCIe or SATA) or SUB symbol (for USB). In the following timing diagram, the PHY is receiving a repeating set of symbols Rx-a through Rx-z. The elastic buffer underflows causing the EDB symbol (for PCIe) or SUB symbol (for USB) to be inserted between the Rx-g and Rx-h Symbols. The PHY drives RxStatus to indicate buffer underflow during the clock cycle when the EDB (for PCIe) or SUB (for USB) is presented on the parallel interface.

**Note:**

The underflow is not signaled when the PHY is operating in Nominal Empty buffer mode. In this mode SKP ordered sets are moved across the interface whenever data needs to be inserted or the RxDataValid signal is used. The RxDataValid method is preferred.

Figure 8-29. Elastic Buffer Underflow

![img-50.jpeg](img-50.jpeg)

For an elastic buffer overflow, the overflow should be signaled during the clock cycle where the dropped symbol or symbols would have appeared in the data stream. For the 16-bit interface, it is not possible, or necessary, for the MAC to determine exactly where in the data stream the symbol was dropped. In the following timing diagram, the PHY is receiving a repeating set of symbols Rx-a through Rx-z. The elastic buffer overflows causing the symbol Rx-g to be discarded. The PHY drives RxStatus to indicate buffer overflow during the clock cycle when Rx-g would have appeared on the parallel interface.

Reference Number: 643108, Revision: 7.1

139

intel®

Figure 8-30. Elastic Buffer Overflow

![img-51.jpeg](img-51.jpeg)

### 8.15.3.1 Elastic Buffer Reset

The MAC can set the ElasticBufferResetControl bit (see Section 7.1.9) to initiate an EB reset sequence in the PHY. The PHY must complete the EB reset sequence within 16 PCLK cycles as follows:

1. Assert RxStatus to value of 1xx with RxValid.
2. Hold RxStatus to 1xx while maintaining RxValid and RxDataValid.
3. Move pointers back to their initial state.
4. Release RxStatus to indicate clean data is being forwarded again.

## 8.16 Loopback

- For USB and PCIe modes, the PHY must support an internal loopback as described in the corresponding base specification.
- For SATA the PHY may optionally support an internal loopback mode when EncodeDecodeBypass is asserted.
- In the SerDes architecture, loopback is handled in the MAC instead of the PHY.

The PHY begins to loopback data when the MAC asserts TxDetectRx/Loopback while doing normal data transmission (that is, when TxElecIdle is deasserted). The PHY must, within the specified receive and transmit latencies, stop transmitting data from the parallel interface, and begin to loopback received symbols. While doing loopback, the PHY continues to present received data on the parallel interface.

The PHY stops looping back received data when the MAC deasserts TxDetectRx/Loopback. Transmission of data on the parallel interface must begin within the specified transmit latency.

The following timing diagram shows the example timing for the beginning loopback. In this example, the receiver is receiving a repeating stream of bytes, Rx-a through Rx-z. Similarly, the MAC is causing the PHY to transmit a repeating stream of bytes Tx-a through Tx-z. When the MAC asserts TxDetectRx/Loopback to the PHY, the PHY

140

Reference Number: 643108, Revision: 7.1

intel®

begins to loopback the received data to the differential Tx+/Tx- lines. Timing between assertion of TxDetectRx/Loopback and when Rx data is transmitted on the Tx pins is implementation dependent.

Figure 8-31. Loopback Start

![img-52.jpeg](img-52.jpeg)

The next timing diagram shows an example of switching from loopback mode to normal mode when the PHY is operating in PCIe Mode.

In PCIe Mode, when the MAC detects an electrical idle ordered set, the MAC deasserts the TxDetectRx/Loopback and asserts TxElecIdle. The PHY must transmit at least three bytes of the electrical idle ordered set before going to electrical idle.

# **Note:**

Transmission of the electrical idle ordered set should be part of the normal pipeline through the PHY and should not require the PHY to detect the electrical idle ordered set.

The base specification requires that a Loopback follower be able to detect and react to an electrical idle ordered set within 1 ms. The PHY's contribution to this time consists of the PHY's Receive Latency plus the PHY's Transmit Latency (see Section 8.20).

When the PHY is operating in USB mode, the device must only transition out of loopback on detection of LFPS signaling (reset) or when the VBUS is removed. When valid LFPS signaling is detected, the MAC transitions the PHY to the P2 power state to begin the LFPS handshake.

Reference Number: 643108, Revision: 7.1

141

intel®

Figure 8-32. Loopback End

![img-53.jpeg](img-53.jpeg)

### 8.17 Polarity Inversion – PCIe and USB Modes

To support lane polarity inversion, the PHY must invert received data when RxPolarity is asserted. Inverted data must begin showing up on RxData[] within 20 PCLKs of when RxPolarity is asserted.

Figure 8-33. Polarity Inversion

![img-54.jpeg](img-54.jpeg)

### 8.18 Setting Negative Disparity (PCIe Mode)

To set the running disparity to negative, the MAC asserts TxCompliance for one clock cycle that matches with the data that is to be transmitted with negative disparity. For a 16-bit interface, the low order byte will be the byte transmitted where running disparity

142

Reference Number: 643108, Revision: 7.1

intel®

is negative. The example shows how TxCompliance is used to transmit the PCIe compliance pattern in PCIe mode. TxCompliance is only used in PCIe mode and is qualified by TxDataValid when TxDataValid is being used.

Figure 8-34. Setting Negative Disparity

![img-55.jpeg](img-55.jpeg)

### 8.19 Electrical Idle – PCIe Mode

The base specification requires that devices send an Electrical Idle ordered set before Tx+/Tx- goes to the electrical idle state. For a 16-bit interface or 32-bit interface, the MAC must always align the electrical idle ordered set on the parallel interface so that the COM symbol is on the low-order data lines (TxDataK[7:0]). Figure 8-35 shows an example of electrical idle exit and entry for a PCIe 8 GT/s or 16 GT/s interface. TxDataValid must be asserted whenever TxElecIdle toggles as it is used as a qualifier for sampling TxElecIdle.

Note: For SerDes architecture, 1 bit of TxElecIdle is required per 16 bits of data.

Reference Number: 643108, Revision: 7.1

143

intel®

Figure 8-35. PCIe 3.0 TxDataValid Timings for Electrical Idle Exit and Entry

![img-56.jpeg](img-56.jpeg)

Note:

Figure 8-35 only shows two blocks of TxData and thus TxDataValid does not deassert during the data. Other examples in the specification show longer sequences where TxDataValid deasserts.

When data throttling is happening, TxElecIdle must be set long enough to be sampled by TxDataValid as shown in Figure 8-36.

144

Reference Number: 643108, Revision: 7.1

intel®

Figure 8-36. Data Throttling and TxElecIdle

![img-57.jpeg](img-57.jpeg)

## 8.20 Electrical Idle – All

The PIPE specification does not require RxStandby to be asserted within any amount of time after Electrical Idle or that it be asserted at all. Individual PHYs that rely on specific timing relationships for proper operation must specify their own timing requirements for RxStandby assertion, which may vary depending on whether they have staggering requirements.

## 8.21 Link Equalization Evaluation

While in the P0 power state, the PHY can be instructed to perform evaluation of the current Tx equalization settings of the link partner. Basic operation of the equalization evaluation is that the MAC requests the PHY to evaluate the current equalization settings by setting the RxEqEval register field. When the PHY has completed evaluating the current equalization settings, it writes to the LinkEvaluationFeedbackDirectionChange or the LinkEvaluationFeedbackFigureMerit register fields or both. After link equalization evaluation has completed, the MAC must clear the RxEqEval register field before initiating another evaluation.

Once the MAC has requested link equalization evaluation (by setting the RxEqEval register bit), the MAC must leave RxEqEval set until after the PHY has signaled completion by writing to the LinkEvaluationFeedbackDirectionChange or LinkEvaluationFeedbackFigureMerit register fields unless the MAC needs to abort the evaluation due to high level timeouts or error conditions. To abort an evaluation the MAC clears the RxEqEval register bit before the PHY has signaled completion. If the MAC aborts the evaluation the PHY must signal completion as quickly as possible. The MAC ignores returned evaluation values in an abort scenario.

Refer to Section 9.10 for example waveforms illustrating successful equalization, invalid coefficient request, aborted equalization, and aborted equalization with race condition scenarios.

Reference Number: 643108, Revision: 7.1

145

intel®

## 8.22 Implementation-Specific Timing and Selectable Parameter Support

PHY vendors (macrocell or discrete) must specify typical and worst-case timings for the cases listed in Table 8-4. Other implementation specific parameters listed in Table 8-4 must also be specified advertised by the PHY in its datasheet.

Table 8-4. Parameters Advertised in PHY Datasheet (Sheet 1 of 7)

[tbl-134.md](tbl-134.md)

146

Reference Number: 643108, Revision: 7.1

intel®

Table 8-4. Parameters Advertised in PHY Datasheet (Sheet 2 of 7)

[tbl-135.md](tbl-135.md)

Reference Number: 643108, Revision: 7.1

147

intel®

Table 8-4. Parameters Advertised in PHY Datasheet (Sheet 3 of 7)

[tbl-136.md](tbl-136.md)

148

Reference Number: 643108, Revision: 7.1

intel®

Table 8-4. Parameters Advertised in PHY Datasheet (Sheet 4 of 7)

[tbl-137.md](tbl-137.md)

Reference Number: 643108, Revision: 7.1

149

intel®

Table 8-4. Parameters Advertised in PHY Datasheet (Sheet 5 of 7)

[tbl-138.md](tbl-138.md)

150

Reference Number: 643108, Revision: 7.1

intel®

Table 8-4. Parameters Advertised in PHY Datasheet (Sheet 6 of 7)

[tbl-139.md](tbl-139.md)

Reference Number: 643108, Revision: 7.1

151

intel®

Table 8-4. Parameters Advertised in PHY Datasheet (Sheet 7 of 7)

[tbl-140.md](tbl-140.md)

152

Reference Number: 643108, Revision: 7.1

intel®

1. See the PCIe base specification. In case of discrepancy, the PCIe base specification supersedes the PIPE specification.

## 8.23 Control Signal Decode Table – PCIe Mode

Table 8-5 summarizes the encodings of four of the seven control signals that cause different behaviors depending on power state. For the other three signals, Reset# always overrides any other PHY activity. TxCompliance and RxPolarity are only valid when the PHY is in P0 and is actively transmitting. Note that these rules only apply to lanes that have not been “turned off” as described in Section 10 (multi-lane PIPE).

For SerDes mode, the rules summarized in Table 8-5 apply to each of the TxElecIdle[3:0] bits independently for the P0 and P0s states. There is an expectation that entering Electrical Idle must occur from MSB to LSB, that is, valid values of TxElecIdle[3:0] are 1000b, 1100b, 1110b, 1111b, and 0000b. Figure 8-7 shows the various scenarios of valid TxElecIdle transitions. Transitions into Electrical Idle can include a single cycle of only a subset of data bytes driven to Electrical Idle followed by all data bytes in Electrical Idle; transitions out of Electrical Idle must be done simultaneously for all data bytes. For the P1 and P2 power states, all the bits of TxElecIdle[3:0] are expected to be driven to the same value so only TxElecIdle[0] needs to be decoded.

Table 8-5. Control Signal Decode Table – PCIe Mode

[tbl-141.md](tbl-141.md)

Reference Number: 643108, Revision: 7.1

153

intel®

Figure 8-37. Possible TxElecIdle[3:0] Transition Scenarios

![img-58.jpeg](img-58.jpeg)

### 8.24 Control Signal Decode Table – USB Mode, USB4 Mode, and DisplayPort Mode

Table 8-6 summarizes the encodings of four of the seven control signals that cause different behaviors depending on power state. For the other three signals, Reset# always overrides any other PHY activity. RxPolarity is only valid, and therefore should only be asserted, when the PHY is in P0 and is actively transmitting.

Note: The same table is applicable to TxDetectRx2 and TxElecIdle2.

Table 8-6. Control Signal Decode Table – USB Mode, USB4 Mode, and DisplayPort Mode (Sheet 1 of 2)

[tbl-142.md](tbl-142.md)

154

Reference Number: 643108, Revision: 7.1

intel®

Table 8-6. Control Signal Decode Table – USB Mode, USB4 Mode, and DisplayPort Mode (Sheet 2 of 2)

[tbl-143.md](tbl-143.md)

### 8.25 Control Signal Decode Table – SATA Mode

The following table summarizes the encodings of the control signals that cause different behaviors in POWER_STATE_0. For other control signals, Reset# always overrides any other PHY activity.

Note:

The PHY transmit latency reported in Section 8.20 must be consistent for all the different behaviors in POWER_STATE_0. This means that the amount of time OOB signaling is present on the analog Tx pair must be the same as the time OOB signaling was indicated on the PIPE interface.

Table 8-7. Control Signal Decode Table – SATA Mode

[tbl-144.md](tbl-144.md)

### 8.26 Required Synchronous Signal Timings

To improve interoperability between MACs and PHYs from different vendors the following timings for synchronous signals are required:

- Setup time for input signals: No greater than 25% of cycle time
- Hold time for input signals: 0 ns
- PCLK to data valid for outputs: No greater than 25% of cycle time

Reference Number: 643108, Revision: 7.1

155

intel®

### 8.27 128b/130b Encoding and Block Synchronization (PCIe 8, 16, and 32 GT/s)

For every block (usually 128 bits – shorter/longer SKP blocks are sometimes transmitted by Retimers) that is moved across the PIPE TxData interface at the 8.0 GT/s rate, 16 GT/s rate, or 32 GT/s rate, the PHY must transmit two extra bits. The MAC must use the TxDataValid signal periodically to allow the PHY to transmit the built-up backlog of data. For example, if the TxData bus is 16-bits wide and PCLK is 500 MHz then every eight blocks the MAC must deassert TxDataValid for one PCLK to allow the PHY to transmit the 16-bit backlog of built up data. The buffers used by the PHY to store Tx data related to the 128/130b encoding rate mismatch must be empty when the PHY comes out of reset and must be empty whenever the PHY exits electrical idle (since Tx buffers are flushed before entry to idle). The PHY must use RxDataValid in a similar fashion. TxDataValid and RxDataValid must be deasserted for one clock exactly every N blocks when the PIPE interface is operating at 8 GT/s or 16 GT/s, where N is 4 for an 8 bit-wide interface, 8 for a 16-bit wide interface, and 16 for a 32-bit wide interface. The MAC must first deassert TxDataValid immediately after the end of the Nth transmitted block following reset or exit from electrical idle. Examples of the timing for TxDataValid are shown in Figure 8-38 for an 8-bit interface and in Figure 8-39 for a 16-bit interface. The PHY must first deassert RxDataValid immediately after the end of the Nth received block transmitted across the PIPE interface following reset or exit from electrical idle. Examples of timings for RxDataValid and other Rx related signals for a 16-bit wide interface are shown in Figure 8-40.

Figure 8-38. PCIe 8 GT/s or Higher TxDataValid Timing for 8 Bit-Wide TxData Interface

![img-59.jpeg](img-59.jpeg)

156

Reference Number: 643108, Revision: 7.1

intel®

Figure 8-39. PCIe 8 GT/s or Higher TxDataValid Timing for 16 Bit-Wide TxData Interface

![img-60.jpeg](img-60.jpeg)

Figure 8-40. PCIe 8 GT/s or Higher RxDataValid Timing for 16 Bit-Wide RxData Interface

![img-61.jpeg](img-61.jpeg)

There are situations, such as upconfigure or L0p, when a MAC must start transmissions on idle lanes while some other lanes are already active. In any such situation, the MAC must wait until the cycle after TxDataValid is deasserted to allow the PHY to transmit the backlog of data due to 128b/130b to start transmissions on previously idle lanes.

### 8.28 128b/132b Encoding and Block Synchronization (USB 10 GT/s)

For every 128 bits that are moved across the PIPE TxData interface at the 10.0 GT/s rate the PHY must transmit 132 bits. The MAC must use the TxDataValid signal periodically to allow the PHY to transmit the built-up backlog of data. For example – if the TxData bus is 16-bits wide and PCLK is 625 MHz then every four blocks the MAC must deassert TxDataValid for one PCLK to allow the PHY to transmit the 16-bit backlog of built up data. The buffers used by the PHY to store Tx data related to the 128/132b encoding rate mismatch must be empty when the PHY comes out of reset and must be empty whenever the PHY exits electrical idle (since Tx buffers are flushed before entry to idle). The PHY must use RxDataValid in a similar fashion. TxDataValid and

Reference Number: 643108, Revision: 7.1

157

intel®

RxDataValid must be deasserted for one clock exactly every N blocks when the PIPE interface is operating at 10 GT/s, where N is 2 for an 8-bit wide interface, 4 for a 16-bit wide interface, and 8 for a 32-bit wide interface. The MAC must first deassert TxDataValid immediately after the end of the Nth transmitted block following reset or exit from electrical idle.

## 8.29 Message Bus Interface

### 8.29.1 General Operational Rules

The message bus interface can be used after Reset# is deasserted and PCLK is stable. The message bus interface must return to its idle state immediately upon assertion of Reset# and must remain idle until Reset# is deasserted and PhyStatus is deasserted, with the exception of LocalLF and LocalFS updates by the PHY as described in Section 9.8. Since the MAC is aware of when PCLK is stable, the requirement that PCLK must be an input to use the message bus allows the MAC to only issue transactions on the message bus after PCLK becomes stable.

For each write_committed issued, the initiator must wait for a write_ack response before issuing any new write_uncommitted or write_committed transactions. A sequence of write_uncommitted transactions must always be followed by a write_committed transaction; only a single write_ack response is expected. The initiator must ensure that the total number of outstanding writes, that is, writes issued since the last write_ack was received, must not exceed the write buffer storage implemented by the receiver.

Transmission of a write_ack must not depend on receiving a write_ack.

Only one read can be outstanding at a time in each direction. The initiator must wait for a read completion before issuing a new read since there are no transaction IDs associated with outstanding reads.

To facilitate design simplicity, reads and writes cannot be mixed. There must not be any reads outstanding when a write is issued; conversely, there must not be any writes outstanding when a read is issued. An outstanding write is any write_committed that has not received a write_ack or any write_uncommitted without a subsequent write_committed that has received a write_ack.

Posted-to-posted MAC to PHY writes are those that result in a PHY to MAC write to be generated in response. For simplification of the verification space, the MAC must only have one outstanding post-to-posted write that is waiting for a write in response. Table 8-8 lists the posted-to-posted writes generated by the MAC. Additionally, any vendor defined writes with posted-to-posted properties most conform to the same restriction of only one outstanding.

Table 8-8. Posted-to-Posted Writes

[tbl-145.md](tbl-145.md)

158

Reference Number: 643108, Revision: 7.1

intel®

Certain registers are defined as part of a register group. To simplify validation space, whenever one register in a register group needs to be updated, all the registers in the register group must be updated using a sequence of uncommitted writes and a single committed write. The defined register groups are listed in Table 8-9, where each row corresponds to a register group.

Table 8-9. Defined Register Groups

[tbl-146.md](tbl-146.md)

### 8.29.2 Message Bus Operations vs. Dedicated Signals

For simplicity, dependencies between message bus operations and dedicated signals are kept to a minimum. The dependencies that do exist are there only because no acceptable workarounds for eliminating them have been identified; these dependencies are documented in this section:

- The PHY must wait for the write_ack to come back for any write to LocalLF, LocalFS, LocalG4LF, or LocalG4FS, if any, before it asserts PhyStatus for a rate change.

### 8.30 PCIe Lane Margining at the Receiver

Table 8-10 provides the sequence of PIPE message bus commands associated with various receiver margining operations; different sequences are shown for independent and dependent samplers. Writes to Sample Count and Error Count fields are only applicable if the PHY supports those features.

Reference Number: 643108, Revision: 7.1

159

intel®

Table 8-10. Lane Margining at the Receiver Sequences (Sheet 1 of 4)

[tbl-147.md](tbl-147.md)

160

Reference Number: 643108, Revision: 7.1

intel®

Table 8-10. Lane Margining at the Receiver Sequences (Sheet 2 of 4)

[tbl-148.md](tbl-148.md)

Reference Number: 643108, Revision: 7.1

161

intel®

Table 8-10. Lane Margining at the Receiver Sequences (Sheet 3 of 4)

[tbl-149.md](tbl-149.md)

162

Reference Number: 643108, Revision: 7.1

intel®

Table 8-10. Lane Margining at the Receiver Sequences (Sheet 4 of 4)

[tbl-150.md](tbl-150.md)

1. Writes to RxMarginStatus.SampleCount are only applicable if Sample Count is supported. Writes to RxMarginStatus.ErrorCount are only applicable if Error Count is supported.

### 8.31 Short Channel Power Control

For short reach (for instance, MCP applications), there should be a provision to revert the ShortChannelPowerControl[1:0] signal to normal operation mode for situations where an optimized mode setting prevents link up. For example, if a particular setting is not compatible with a 2.5 GT/s link speed and works only at higher link speeds, the expectation is that the ShortChannelPowerControl[1:0] signal would be set to normal operation mode to bring the link up initially before changing the value to an optimized power control setting while transitioning to higher link speeds.

Reference Number: 643108, Revision: 7.1

163

intel®

### 8.32 RxEqTraining

For PCIe, there are several scenarios where the controller may request that the PHY perform receiver equalization. These may be in response to far end transmitter coefficient changes, loopback entry, rate changes, and support of no equalization on the transmitter side. For PCIe, the PHY sets the RxEqTrainDone bit in the Rx Status0 register to indicate completion of receiver equalization. Figure 8-41 shows the message bus sequence for managing PCIe receiver equalization.

Figure 8-41. PCIe Receiver Equalization

![img-62.jpeg](img-62.jpeg)

For USB, the controller instructs the PHY to perform receiver equalization during Polling.ExEQ. For USB, receiver equalization is timer based and the RxEqTrainDone bit is not used. Figure 8-42 shows the message bus sequence for USB receiver equalization.

Figure 8-42. USB Receiver Equalization

![img-63.jpeg](img-63.jpeg)

164

Reference Number: 643108, Revision: 7.1

intel®

### 8.33 PHY Recalibration

In certain situations, the PHY may need to be recalibrated. These situations may include changes in operating conditions, for instance, Vref changes, or detection of certain error conditions. The PIPE specification provides mechanisms for either the controller or the PHY to initiate recalibration. Recalibration must occur during Recovery, so if the PHY determines that a recalibration is necessary, it notifies the controller that it should enter Recovery and request a recalibration. Figure 8-43 shows the sequence of message bus commands for a controller initiated PHY recalibration. Figure 8-44 shows the sequence of message bus commands for a PHY initiated PHY recalibration; this sequence essentially consists of the PHY notifying the controller that it should request a recalibration, then the controller follows the same steps as it would for a controller initiated PHY recalibration. After the PHY notifies the controller that the recalibration operation is complete by setting the IORecalDone bit, the controller is permitted to exit Recovery and resume normal operation on the link.

Figure 8-43. PHY Recalibration Initiated by Controller

![img-64.jpeg](img-64.jpeg)

Reference Number: 643108, Revision: 7.1

165

intel®

Figure 8-44. PHY Recalibration Initiated by PHY

![img-65.jpeg](img-65.jpeg)

### 8.34 Digital Near End Loopback

The PIPE specification defines an optional Digital Near-End Loopback (DNELB) operational mode to facilitate HVM testing; toggling signals via functional testing in loopback mode enables fault testing. This feature is applicable to PCIe, USB, USB4, and SATA.

Several possible loopback points from the transmit to the receive datapath are recommended as shown in Figure 8-45 and Figure 8-46. Figure 8-45 shows loopback paths in a PHY with original PIPE architecture; LB0 through LB4 are recommended paths and correspond to encodings defined in the PHY Near End Loopback Control register (See Section 7.1.23), while LB5 is a potential PHY implementation specific path. The loopback paths may require logic, represented by f in the diagrams, to convert between the Tx and Rx paths clock frequencies and data width. Figure 8-46 shows loopback paths in a PHY with SerDes architecture; L0, L3, and LB4 are recommended paths and correspond to encodings defined in the PHY Near End Loopback Control register (See Section 7.1.23), while LB5 is a potential PHY implementation specific path.

Figure 8-45. Original PIPE Architecture: DNELB Path Examples

![img-66.jpeg](img-66.jpeg)

166

Reference Number: 643108, Revision: 7.1

intel®

Figure 8-46. SerDes Architecture: DNELB Path Examples

![img-67.jpeg](img-67.jpeg)

The following subsections specify the sequences for entering and exiting DNELB mode; also specified are any differences in behavior of PIPE signals when operating in DNELB mode.

### 8.34.1 PIPE Operations and Signals in DNELB Mode

The general philosophy is to enable the LTSSM to train as closely as possible to normal operational mode. Unless differences are called out specifically in this section, PIPE signals operate the same as they do in normal operation.

- Data Path:

- Original PIPE Architecture

- Rate, Width, and PCLK Rate operate the same in DNELB mode as they do in normal operation.
- Tx interface operates same as in normal operation.

- No additional limitations on TxDataValid or TxElecIdle

- Rx interface operates same as in normal operation.

- TxDataValid and TxElecIdle have impact on RxDataValid and RxElecIdle; the loopback location determines how the Tx side translates to the Rx side.

- SerDes Architecture:

- Rate, Width, PCLK Rate, and RxWidth operate the same in NELB mode as in normal operation.
- Tx interface operates the same as in normal operation.

- No additional limitations on TxDataValid or TxElecIdle.

- Rx interface operates the same as in normal operation.

- RxValid, RxData, and RxCLK operate the same as in normal operation.

- PHY must convert the Tx data path into the expected Rx data path format.

- Convert from PCLK / TxDataValid / Width to RxCLK / RxWidth format
- If RxCLK is slower than PCLK, the PHY is permitted to skew the duty cycle; however, the shorter of the low or high portion of the clock period must not be shorter than normal operation. For example, if RxCLK is 250 MHz and PCLK is 1G Hz, acceptable duty cycles include 1 ns/3 ns or 500 ps/3.5 ns. An asymmetric duty cycle enables simplification of generation of RxCLK via a simple digital divide of incoming PCLK.

Reference Number: 643108, Revision: 7.1

167

intel®

• RxValid:

- The assertion of RxValid should continue to be affected by the Rx logic downstream of the loop back point. For instance, if alignment (8b/10b or 128/130b) must occur first before RxValid is asserted, then it must be required in NELB when the alignment logic is in the active Rx data path.
- In SerDes mode, RxValid must assert when the RxCLK is stable and the TxElecIdle is no longer asserted.

• RxElecIdle:

- The RxElecIdle signal must reflect the TxElecIdle signal with minimal delay, especially at the end of the data stream. If RxElecIdle is not asserted soon enough after TxElecIdle, this may result in false wakeups from L1. The RxElecIdle signal should not lag the RxData by more than normal operation would. RxElecIdle is permitted to precede the RxData if that is how normal operation would happen.

• RxStatus:

- For TxDetectRx functionality, see following entries.
- For error and skip adjustment status
  - If bad data will be transferred on initial EI exit, mark as required by protocol with RxStatus.
    - If the loopback point is in the analog or high speed digital domains that may be susceptible to bit errors, RxStatus should reflect these as required by the protocol mode.
    - Note: The PHY may need to be tuned to avoid errors if a loopback path in the analog or high-speed digital domain is selected.
  - If a skip adjustment is done, RxStatus must reflect such action.

• Tx Detect Receiver:

- The results of doing Tx receiver detect will be equal to the state of RXTermination (RxStatus of 3).
- If asynchronous TxDetectRx is supported in normal operation, it must also be supported in NELB mode.

• RxEqEval / RxEqTrain:

- Depending on loopback position, these operations may return fabricated dummy results. The PHY must indicate in its datasheet which loop back positions result in fabricated dummy results.
- To enable the MAC to consume the results in the same manner as it does in normal operation, the PHY must adhere to the following rules when returning fabricated dummy results:
  - Directional feedback must return no update required (0).
  - Figure of Merit Feedback must return a non-zero value.
    - It is recommended that the MAC have the ability to shorten its search algorithms in NELB mode.
  - RxEqEval / RxEqTrain response time in NELB mode must not exceed 10 us.

• Powerdown / Phystatus:

- This operates the same as in normal operation.

• RxStandby / RxStandbyStatus:

- This operates the same as in normal operation:

168

Reference Number: 643108, Revision: 7.1

intel®

- If RxStandbyStatus returns in response to RxStandby, it should continue to do so in NELB mode.
- If RxStandbyStatus is not supported (for instance, USB) or guaranteed, the same holds true in NELB mode.

- Rate Changes:

- This operates the same as in normal operation.
- The same combinations of Rate, Width, PCLK Rate, RxWIDTH, and so forth. It must be supported in NELB mode as in normal operation.
- Clock changes related to rate changes should remain the same as in normal operation.

- For instance, PclkChangeOk / PclkChangeAck should remain the same.

- TxDetectRx/Loopback must not be used to indicate follower loopback operation while NELB is enabled.

- Start of data transfer on Rx data path:

- If the PHY cannot guarantee all bits will be looped back when the Rx data path is exiting electrical idle, it must clearly specify in its datasheet when the first data will appear.

- For instance, the block aligner requires two EIEOSs to begin forwarding data and the data from the Tx data path up to the 2nd EIEOS would not be seen (similar thing for 8b/10b aligner).

- NELB must function when SRISEnable is high or low.

- No false or additional ppm is required to be applied if SRISEnable is high.

- RefClkRequired# must function as it does in normal operation.

- DataBusWidth must function as it does in normal operation.

- TxDeemph and TxSwing must continue to be consumed by the PHY. The PHY may choose to ignore them if the loopback point is not affected by the Tx EQ settings.

- The controller must not use the following functions while in NELB as the PHY may not return a response:

- Receiver Lane Margining
- TxMargin
- IORecal

- Elastic Buffer controls as defined in the message bus section (depth, run mode, and so forth) must continue to function the same as normal operation.

- BlockAlignControl functionality is expected to function the same as in normal operation.

- EncodeDecodeBypass must operate as it does in normal operation.

- RxPolarity functionality must continue to operate the same as in normal operation.

- PHY or MAC can implement implementation specific means to invert the data for increased test coverage.

- Local Preset Fetch bus must function as it does in normal operation.

- GetLocalPresetCoefficients, LocalPresetIndex, LocalFS, LocalLF, LocalG{5,4}FS, LocalG{5,4}LF, LocalTxPresetCoefficient

- FS and LF of link partner must continue to be reported as in normal operation.

Reference Number: 643108, Revision: 7.1

169

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

intel®

- The MAC is encouraged to use the exit error indication to initiate a PIPE lane reset or otherwise block functional operation.
- The **LB Position** cannot be changed while in NELB. NELB must be exited and re-entered with the new **LB Position**.

### 8.34.3 USB4 PAM3 Encoding on PIPE Interface

Each pair of binary bits on the TxData[55:0], TxData2[55:0], RxData[55:0], or RxData2[55:0] interface represents a PAM3 analog level. The mapping follows the USB4 specification:

- 0 maps to the lower voltage level, V₋₁.
- 1 maps to the middle voltage level, V₀.
- 2 maps to the upper voltage level, V₁.

The 56-bit data interface represents four symbols. Bits [13:0] comprise the first symbol, bits [27:14] comprise the second symbol, bits [41:28] comprise the third symbol, and bits [55:42] comprise the third symbol.

Within each symbol, bits[1:0] are trit 0 of the symbol, bits [3:2] are trit 1 of the symbol, bits [5:4] are trit 2 of the symbol, and so forth. Refer to the USB4 specification for further details.

### 8.35 Switching Between Rx and Tx Pairs

USB4 supports asymmetric mode. To transition between symmetric and asymmetric mode requires switching the direction of a differential Rx/Tx pair. The message bus sequence for switching from Rx to Tx operation is shown in Figure 8-47; the sequence for switching from Tx to Rx direction is specified in Figure 8-48. The traffic on all other differential pairs must not be impacted by this transition. This transition is permitted in any PowerDown state in which the message bus is operational; however, at a minimum, it must be supported in PS0.

Figure 8-47. Transitioning from Rx to Tx Operation

![img-68.jpeg](img-68.jpeg)

Figure 8-48. Transitioning from Tx to Rx Operation

![img-69.jpeg](img-69.jpeg)

Reference Number: 643108, Revision: 7.1

171

intel®

# 9 Sample Operational Sequences

These sections show sample timing sequences for some of the more common PCIe, SATA, and USB operations. These are sample sequences and timings and are not required operation.

## 9.1 Active PM L0 to L0s and Back to L0 – PCIe Mode

This example shows one way a PIPE PHY can be controlled to perform Active State Power Management on a link for the sequence of the link being in L0 state, transitioning to L0s state, and then transitioning back to L0 state.

When the MAC and higher levels have determined that the link should transition to L0s, the MAC transmits an electrical idle ordered set and then has the PHY transmitter go idle and enter P0s. Note that for a 16-bit or 32-bit interface, the MAC should always align the electrical idle on the parallel interface so that the COM symbol is in the low-order position (TxDataK[7:0]).

Figure 9-1. L0 to L0s

![img-70.jpeg](img-70.jpeg)

To cause the link to exit the L0s state, the MAC transitions the PHY from the P0s state to the P0 state, waits for the PHY to indicate that it is ready to transmit (by the assertion of PhyStatus), and then begins transmitting Fast Training Sequences (FTS).

Note: This is an example of L0s to L0 transition when the PHY is running at 2.5 GT/s.

172

Reference Number: 643108, Revision: 7.1

intel®

Figure 9-2. L0s to L0

![img-71.jpeg](img-71.jpeg)

## 9.2 Active PM to L1 and Back to L0 - - PCIe Mode

This example shows one way a PIPE PHY can be controlled to perform Active State Power Management on a link for the sequence of the link being in L0 state, transitioning to L1 state, and then transitioning back to L0 state. This example assumes that the PHY is on an endpoint (that is, it is facing upstream) and that the endpoint has met all the requirements (as specified in the base specification) for entering L1.

After the MAC has had the PHY send PM_Active_State_Request_L1 messages, and has received the PM_Request_ACK message from the upstream port, it then transmits an electrical idle ordered set, and has the PHY transmitter go idle and enter P1.

Reference Number: 643108, Revision: 7.1

173

intel®

Figure 9-3. L0 to L1

![img-72.jpeg](img-72.jpeg)

To cause the link to exit the 1 state, the MAC transitions the PHY from the P1 state to the P0 state, waits for the PHY to indicate that it is ready to transmit (by the assertion of PhyStatus), and then begins transmitting training sequence ordered sets (TS1s).

Note: This is an example when the PHY is running at 2.5 GT/s.

174

Reference Number: 643108, Revision: 7.1

intel®

Figure 9-4. L1 to L0

![img-73.jpeg](img-73.jpeg)

Reference Number: 643108, Revision: 7.1

175

intel®

## 9.3 Downstream Initiated L1 Substate Entry Using Sideband Mechanism

Figure 9-5. L1 Substate Management Using RxEIDetectDisable and TxCommonModeDisable

![img-74.jpeg](img-74.jpeg)

## 9.4 Receivers and Electrical Idle – PCIe Mode Example

This section only applies to a PHY operating to 2.5 GT/s. Note that when operating at 5.0 GT/s or 8 GT/s signaling rates, RxElecIdle may not be reliable. MACs should see the PCIe Revision 3.0 base specification or USB 3.0 specification for methods of detecting entry into the electrical idle condition.

See Section 6.1.3 for the definition of RxElecIdle when operating at 5.0 GT/s. This section shows some examples of how PIPE interface signaling may happen as a receiver transitions from active to electrical idle and back again. In these transitions, there may be a significant time difference between when RxElecIdle transitions and when RxValid transitions.

The first diagram shows how the interface responds when the receive channel has been active and then goes to electrical idle. In this case, the delay between RxElecIdle being asserted and RxValid being deasserted is directly related to the depth of the

176

Reference Number: 643108, Revision: 7.1

intel®

implementations elastic buffer and symbol synchronization logic. Note that the transmitter that is going to electrical idle may transmit garbage data and this data will show up on the RxData[] lines. The MAC should discard any symbols received after the electrical idle ordered set until RxValid is deasserted.

Figure 9-6. Receiver Active to Idle

![img-75.jpeg](img-75.jpeg)

The second diagram shows how the interface responds when the receive channel has been idle and then begins signaling again. In this case, there can be significant delay between the deassertion of RxElecIdle (indicating that there is activity on the Rx+/Rx- lines) and RxValid being asserted (indicating valid data on the RxData[] signals). This delay is composed of the time required for the receiver to retrain as well as elastic buffer depth.

Reference Number: 643108, Revision: 7.1

177

intel®

Figure 9-7. Receiver Idle to Active

![img-76.jpeg](img-76.jpeg)

## 9.5 Using CLKREQ# with PIPE – PCIe Mode

CLKREQ# is used in some implementations by the downstream device to cause the upstream device to stop signaling on REFCLK. When REFCLK is stopped, this will typically cause the CLK input to the PIPE PHY to stop as well. The PCIe CEM specification allows the downstream device to stop REFCLK when the link is in either L1 or L2 states. For implementations that use CLKREQ# to further manage power consumption, PIPE compliant PHYs can be used as follows:

The general usage model is that to stop REFCLK, the MAC puts the PHY into the P2 power state, then deasserts CLKREQ#. To get the REFCLK going again, the MAC asserts CLKREQ#, and then after some PHY and implementation specific time, the PHY is ready to use again.

### 9.5.1 CLKREQ# in L1

If the MAC is moving the link to the L1 state and intends to deassert CLKREQ# to stop REFCLK, then the MAC follows the proper sequence to get the link to L1, but instead of finishing by transitioning the PHY to P1, the MAC transition the PHY to P2. Then the MAC deasserts CLKREQ#.

When the MAC wants to get the link alive again, it can:

- Assert CLKREQ#.
- Wait for REFCLK to be stable (implementation specific).
- Wait for the PHY to be ready (PHY specific).
- Transition the PHY to P0 state and begin training.

178

Reference Number: 643108, Revision: 7.1

intel®

### 9.5.2 CLKREQ# in L2

If the MAC is moving the link to the L1 state and intends to deassert CLKREQ# to stop REFCLK, then the MAC follows the proper sequence to get the link to L2. Then the MAC deasserts CLKREQ#.

When the MAC wants to get the link alive again, it can:

- Assert CLKREQ#.
- Wait for REFCLK to be stable (implementation specific).
- Wait for the PHY to be ready (PHY specific).
- Transition the PHY to P0 state and begin training.

### 9.5.3 Delayed CLKREQ# in L1

The MAC may want to stop REFCLK after the link has been in L1 and idle for a while. In this case, the PHY is in the P1 state and the MAC must transition the PHY into the P0 state, and then the P2 state before deasserting CLKREQ#. Getting the link operational again is the same as the preceding cases.

## 9.6 Block Alignment

Figure 9-8 provides an example of a block alignment sequence using the BlockAlignControl pin. The PHY attempts to do alignment when BlockAlignControl is asserted and the PHY receiver is active.

Figure 9-8. BlockAlignControl Example Timing

![img-77.jpeg](img-77.jpeg)

Reference Number: 643108, Revision: 7.1

179

intel®

## 9.7 Message Bus: Rx Margining Sequence

Figure 9-9 shows an example of an Rx margining sequence. The MAC issues a write_uncommitted to address 0x1 followed by a write_committed to address 0x0 to set up the margining parameters and to start margining in the Rx Margin Control1 and Rx Margin Control0 registers. The PHY issues a write_ack to acknowledge that it has flushed the write buffer. Subsequently, upon processing a change in the "Start Margin" bit of the Rx Margin Control0 register, the PHY issues a write_committed to address 0x0 to assert the "Margin Status" bit. During the margining process, the PHY periodically issues write_committed transactions to address 0x2 to update the "Error Count[3:0]" value. The MAC acknowledges receipt of these writes by issuing corresponding write_ack transactions. Finally, the MAC stops the margining process by issuing a write_committed to address 0x0 to deassert the "Start Margin" bit. The PHY issues a write_ack to acknowledge that it has flushed the write buffer. In response to the "Start Margin" deassertion, the PHY pushes its final "Error Count[3:0]" value to the MAC via a write_uncommitted transaction to the "Rx Margin Status2" register, and then issues a write_committed to assert "Rx Margin Status0.Margin Status".

Figure 9-9. Sample Rx Margining Sequence

![img-78.jpeg](img-78.jpeg)

## 9.8 Message Bus: Updating LocalFS/LocalLF and LocalG4FS/LocalG4LF

Figure 9-10 shows a sequence where LocalFS and LocalLF are updated out of reset and, subsequently, LocalG4FS and LocalG4LF are updated after a rate change. Note that PhyStatus deasserts only after the write_ack returns for the LocalFS and LocalLF update out of reset. Similarly, the one cycle PhyStatus assertion occurs after the write_ack returns for the LocalG4FS and LocalG4LF update after a rate change. This is one of the rare cases where a dependency between a message bus operation and a dedicated signal exists. While this example shows LocalG4FS and LocalG4LF being updated after a rate change, it is not a requirement to wait until after the rate change to update these values; for instance, they can be updated out of reset if their values are already known by then.

Note:

This flexibility in timing of when updates can occur was intentionally introduced with the low pin count interface by allocating separate LocalFS and LocalLF registers per data rate.

180

Reference Number: 643108, Revision: 7.1

intel®

Figure 9-10. LocalFS/LocalLF/LocalG4FS/LocalG4LF Updates Out of Reset and After Rate Change

![img-79.jpeg](img-79.jpeg)

Figure 9-11 shows a sequence where LocalFS and LocalLF are updated in response to a GetLocalPresetCoefficients request where the LocalPresetIndex corresponds to an 8 GT/s rate. Note that the LocalFS and LocalLF values must be updated before or at the same cycle as the LocalTxPresetCoefficients are returned.

Figure 9-11. LocalFS/LocalLF Update Due to GetLocalPresetCoefficients

![img-80.jpeg](img-80.jpeg)

## 9.9 Message Bus: Updating TxDeemph

Figure 9-12 shows a sequence where the MAC makes a GetLocalPresetCoefficients request for one or more values of LocalPresetIndex and the, subsequently, update the TxDeemph value. Note that for every GetLocalPresetCoefficients request, there is a 128 ns maximum response time for the PHY to return the LocalTxPresetCoefficients value; this time is shown in the diagram from the end of the second write_committed to the end of the third write_committed. This maximum response time requirement only exists for designs that use just-in-time fetching of GetLocalPresetCoefficients in response to Tx coefficients request from the link partner; designs that fetch ahead of time can circumvent this requirement. Additionally, after the write_committed for TxDeemph, the new TxDeemph value must be reflected on the pins within 128 ns. Note

Reference Number: 643108, Revision: 7.1

181

intel®

that while Figure 9-12 does not show LocalLF and LocalFS getting returned in response to a GetLocalPresetCoefficients request, they can be returned along with LocalTxPresetCoefficients similar to what is done in Figure 9-11.

Figure 9-12. Updating TxDeemph after GetLocalPresetCoefficients Request

![img-81.jpeg](img-81.jpeg)

## 9.10 Message Bus: Equalization

Figure 9-13 shows a successful equalization sequence. RxEqInProgress is asserted for the entire duration of equalization. Multiple RxEqEval requests are made during the equalization process corresponding to different coefficient requests to the far end transmitter. When all the RxEqEval requests are complete, RxEqInProcess is deasserted.

Note: The PHY does not necessarily have to write to both the LinkEvaluationFeedbackFigureMerit and LinkEvaluationFeedbackDirectionChange register fields; it could write to only to one.

Figure 9-13. Successful Equalization

![img-82.jpeg](img-82.jpeg)

Figure 9-14 shows an equalization sequence where the feedback received indicates an invalid coefficient request for the link partner. Note that the write to assert InvalidRequest must happen before a new request is initiated; the write to deassert InvalidRequest can happen in the same cycle as an RxEqEval request for a new coefficient.

182

Reference Number: 643108, Revision: 7.1

intel®

Figure 9-14. Equalization with Invalid Request

![img-83.jpeg](img-83.jpeg)

Figure 9-15 shows a sequence where the MAC aborts the RxEqEval request before the link evaluation feedback is returned by the PHY. Figure 9-16 shows a sequence where the MAC aborts the RxEqEval request while the link evaluation feedback is being returned by the PHY, that is, there is an overlap. In both abort case, the MAC must ignore the feedback value returned by the PHY.

Figure 9-15. Aborted Equalization, Scenario #1

![img-84.jpeg](img-84.jpeg)

Figure 9-16. Aborted Equalization, Scenario #2

![img-85.jpeg](img-85.jpeg)

### 9.11 Message Bus: BlockAlignControl

Figure 9-17 shows a sequence where BlockAlignControl is used to reestablish block alignment after a loss of alignment is detected. This sequence also shows how RxValid transitions during this process.

Reference Number: 643108, Revision: 7.1

183

intel®

Figure 9-17. Message Bus: BlockAlignControl Example

![img-86.jpeg](img-86.jpeg)

## 9.12 Message Bus: ElasticBufferLocation Update

Figure 9-18 shows the update of ElasticBufferLocation across the message bus. The frequency of update across the message bus is controlled by the MAC by setting the value in the ElasticBufferLocationUpdateFrequency register.

Figure 9-18. Message Bus: Updating ElasticBufferLocation

![img-87.jpeg](img-87.jpeg)

184

Reference Number: 643108, Revision: 7.1

intel®

### 9.13 Message Bus: RxInPhase01Equalization Update

Figure 9-19 shows an example sequence where RxInPhase01Equalization is set prior to RxEqTraining being set. Both an uncommitted or a committed write are acceptable for first write in this sequence; the key requirement is that RxInPhase01Equalization is set before or at the same time as RxEqTraining.

Figure 9-19. Example Sequence: RxInPhase01Equalization and RxEqTraining Relationship

![img-88.jpeg](img-88.jpeg)

Reference Number: 643108, Revision: 7.1

185

intel®

# 10 Multi-Lane PIPE – PCIe Mode

This section describes a suggested method for combining multiple PIPEs together to form a multi-lane implementation. It describes which PIPE signals can be shared between each PIPE of a multi-lane implementation, and which signals should be unique for each PIPE. There are two types of PHY. "Variable" PHYs that are designed to support multiple links of variable maximum widths and "Fixed" PHYs that are designed to support a fixed number of links with fixed maximum widths.

The figure shows an example four-lane implementation of a multilane PIPE solution with PCLK as a PHY input. The signals that can be shared are shown in the figure as "Shared Signals" while signals that must be replicated for each lane are shown as "Per-lane signals".

Figure 10-1. Four-Lane PIPE Implementation

![img-89.jpeg](img-89.jpeg)

The MAC layer is responsible for handling lane-to-lane deskew and it may be necessary to use the per-lane signaling of SKP insertion and removal to help perform this function.

186

Reference Number: 643108, Revision: 7.1

intel®

Table 10-1. The MAC Layer

[tbl-151.md](tbl-151.md)

Reference Number: 643108, Revision: 7.1

187

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

intel®

# A Appendix

## A.1 DisplayPort AUX Signals

The set of DisplayPort AUX signals listed in Table A-1 should be implemented per connector.

Table A-1. DisplayPort AUX Signals

[tbl-152.md](tbl-152.md)

Reference Number: 643108, Revision: 7.1

189