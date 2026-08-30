# Universal Serial Bus 3.1 Specification

Hewlett-Packard Company

Intel Corporation

Microsoft Corporation

Renesas Corporation

ST-Ericsson

Texas Instruments

Revision 1.0

July 26, 2013

Universal Serial Bus 3.1 Specification, Revision 1.0

# Revision History

[tbl-0.md](tbl-0.md)

# INTELLECTUAL PROPERTY DISCLAIMER

THIS SPECIFICATION IS PROVIDED TO YOU "AS IS" WITH NO WARRANTIES WHATSOEVER, INCLUDING ANY WARRANTY OF MERCHANTABILITY, NON-INFRINGEMENT, OR FITNESS FOR ANY PARTICULAR PURPOSE. THE AUTHORS OF THIS SPECIFICATION DISCLAIM ALL LIABILITY, INCLUDING LIABILITY FOR INFRINGEMENT OF ANY PROPRIETARY RIGHTS, RELATING TO USE OR IMPLEMENTATION OF INFORMATION IN THIS SPECIFICATION. THE PROVISION OF THIS SPECIFICATION TO YOU DOES NOT PROVIDE YOU WITH ANY LICENSE, EXPRESS OR IMPLIED, BY ESTOPPEL OR OTHERWISE, TO ANY INTELLECTUAL PROPERTY RIGHTS.

Please send comments to techsup@usb.org

For industry information, refer to the USB Implementers Forum web page at http://www.usb.org

All product names are trademarks, registered trademarks, or servicemarks of their respective owners.

Copyright © 2007-2013, Hewlett-Packard Company, Intel Corporation, Microsoft Corporation, Renesas Corporation, ST-Ericsson, and Texas Instruments.

All rights reserved.

ii

# Acknowledgement of Technical Contribution

# Dedication

Dedicated to the memory of Brad Hosler, the impact of whose accomplishments made the Universal Serial Bus one of the most successful technology innovations of the Personal Computer era.

The authors of this specification would like to recognize the following people who participated in the USB 3.0 Bus Specification technical workgroups. We would also like to acknowledge the many others throughout the industry who provided feedback and contributed to the development of this specification.

Promoter Company Employees

[tbl-1.md](tbl-1.md)

iii

# Universal Serial Bus 3.1 Specification, Revision 1.0

[tbl-2.md](tbl-2.md)

iv

[tbl-3.md](tbl-3.md)

## Contributor Company Employees

[tbl-4.md](tbl-4.md)

v

Universal Serial Bus 3.1 Specification, Revision 1.0

[tbl-5.md](tbl-5.md)

The authors of this specification would like to recognize the following people who participated in the USB 3.1 Bus Specification technical workgroups. Additionally we would like to acknowledge the many others throughout industry who provided feedback and contributed to the development of this specification.

### Promoter Company Employees

[tbl-6.md](tbl-6.md)

vi

[tbl-7.md](tbl-7.md)

## Contributor Company Employees

[tbl-8.md](tbl-8.md)

vii

Universal Serial Bus 3.1 Specification, Revision 1.0

[tbl-9.md](tbl-9.md)

viii

Egbert Stellinga  
Noah Zhang  
Marvin DeForest  
Larry McMillan  
Cristian Roman Del Nido  
Curtis Stevens

Tyco Electronics Corp., a TE Connectivity Ltd. company  
Tyco Electronics Corp., a TE Connectivity Ltd. company  
Western Digital Technologies, Inc.  
Western Digital Technologies, Inc.  
Western Digital Technologies, Inc.  
Western Digital Technologies, Inc.

ix

# Contents

Acknowledgement of Technical Contribution...iii

1 Introduction ... 1-1

1.1 Background ... 1-1
1.2 Objective of the Specification... 1-1
1.3 Scope of the Document ... 1-2
1.4 USB Product Compliance ... 1-2
1.5 Document Organization ... 1-2
1.6 Design Goals ... 1-3
1.7 Related Documents ... 1-3

2 Terms and Abbreviations ... 2-1

3 Architectural Overview ... 3-1

3.1 USB 3.1 System Description... 3-1
3.1.1 USB 3.1 Physical Interface ... 3-2
3.1.1.1 USB 3.1 Mechanical... 3-3
3.1.2 USB 3.1 Power... 3-3
3.1.3 USB 3.1 System Configuration ... 3-4
3.1.4 USB 3.1 Architecture Summary ... 3-4
3.2 Enhanced SuperSpeed Bus Architecture... 3-4
3.2.1 Physical Layer ... 3-6
3.2.1.1 Gen 1 Physical Layer ... 3-7
3.2.1.2 Gen 2 Physical Layer ... 3-7
3.2.2 Link Layer... 3-8
3.2.3 Protocol Layer ... 3-8
3.2.3.1 SuperSpeed Protocol ... 3-9
3.2.3.2 SuperSpeedPlus Protocol ... 3-10
3.2.4 Robustness ... 3-10
3.2.4.1 Error Detection ... 3-10
3.2.4.2 Error Handling ... 3-11
3.2.5 Enhanced SuperSpeed Power Management... 3-11
3.2.6 Devices ... 3-12
3.2.6.1 Peripheral Devices ... 3-12
3.2.6.2 Hubs... 3-14
3.2.6.3 SuperSpeed Hub... 3-14
3.2.6.4 SuperSpeedPlus Hub ... 3-14
3.2.7 Hosts... 3-16
3.3 Enhanced SuperSpeed Bus Data Flow Models ... 3-16

4. Enhanced SuperSpeed Data Flow Model... 4-1

4.1 Implementer Viewpoints... 4-1
4.2 Enhanced SuperSpeed Communication Flow... 4-1
4.2.1 Pipes ... 4-2
4.3 Enhanced SuperSpeed Protocol Overview ... 4-2
4.3.1 Differences from USB 2.0... 4-2

x

Contents

4.3.1.1 Comparing USB 2.0 and Enhanced SuperSpeed Transactions...4-3

4.3.1.2 Introduction to Enhanced SuperSpeed Packets ...4-4

4.4 Generalized Transfer Description ...4-4

4.4.1 Data Bursting ...4-5

4.4.2 IN Transfers ...4-5

4.4.3 OUT Transfers...4-6

4.4.4 Power Management and Performance ...4-7

4.4.5 Control Transfers...4-8

4.4.5.1 Control Transfer Packet Size...4-8

4.4.5.2 Control Transfer Bandwidth Requirements...4-8

4.4.5.3 Control Transfer Data Sequences ...4-9

4.4.6 Bulk Transfers ...4-9

4.4.6.1 Bulk Transfer Data Packet Size...4-9

4.4.6.2 Bulk Transfer Bandwidth Requirements ...4-10

4.4.6.3 Bulk Transfer Data Sequences...4-10

4.4.6.4 Bulk Streams...4-10

4.4.7 Interrupt Transfers...4-12

4.4.7.1 Interrupt Transfer Packet Size ...4-13

4.4.7.2 Interrupt Transfer Bandwidth Requirements ...4-13

4.4.7.3 Interrupt Transfer Data Sequences ...4-14

4.4.8 Isochronous Transfers...4-14

4.4.8.1 Isochronous Transfer Packet Size...4-15

4.4.8.2 Isochronous Transfer Bandwidth Requirements ...4-15

4.4.8.3 Isochronous Transfer Data Sequences ...4-16

4.4.8.4 Special Considerations for Isochronous Transfers...4-16

4.4.8.4.1 Explicit Feedback...4-16

4.4.9 Device Notifications...4-18

4.4.10 Reliability...4-18

4.4.10.1 Physical Layer...4-18

4.4.10.2 Link Layer ...4-18

4.4.10.3 Protocol Layer ...4-18

4.4.11 Efficiency...4-18

# 5 Mechanical ...5-1

5.1 Objective ...5-1

5.2 Significant Features ...5-1

5.2.1 Connectors...5-2

5.2.1.1 USB 3.1 Standard-A Connector...5-2

5.2.1.2 USB 3.1 Standard-B Connector...5-2

5.2.1.3 USB 3.1 Micro-B Connector ...5-3

5.2.1.4 USB 3.1 Micro-AB and USB 3.1 Micro-A Connectors ...5-3

5.2.2 Allowed Cable Assemblies ...5-3

5.2.3 Raw Cables...5-3

5.3 Connector Mating Interfaces...5-4

5.3.1 USB 3.1 Standard-A Connector...5-4

5.3.1.1 Interface Definition ...5-4

5.3.1.2 USB 3.1 Standard-A Reference Footprints ...5-13

5.3.1.3 Pin Assignments and Description ...5-19

xi

[tbl-10.md](tbl-10.md)

xii

Contents

[tbl-11.md](tbl-11.md)

xiii

6.4.1.2.4 Informative Block Alignment for Gen 2 Operation ...6-17
6.4.2 Lane Polarity Inversion...6-18
6.4.2.1 Gen 1 Operation...6-18
6.4.2.2 Gen 2 Operation...6-18
6.4.3 Elasticity Buffer and SKP Ordered Set ...6-18
6.4.3.1 SKP Rules (Host/Device/Hub) for Gen 1 Operation...6-19
6.4.3.2 SKP Rules (Host/Device/Hub) for Gen 2 Operation:...6-19
6.4.4 Compliance Pattern...6-21
6.4.4.1 Gen 2 Compliance Pattern CP9 ...6-21
6.5 Clock and Jitter...6-22
6.5.1 Informative Jitter Budgeting...6-22
6.5.2 Normative Clock Recovery Function...6-22
6.5.3 Normative Spread Spectrum Clocking (SSC) ...6-25
6.5.4 Normative Slew Rate Limit ...6-26
6.6 Signaling...6-26
6.6.1 Eye Diagrams...6-26
6.6.2 Voltage Level Definitions ...6-28
6.6.3 Tx and Rx Input Parasitics...6-29
6.7 Transmitter Specifications...6-30
6.7.1 Transmitter Electrical Parameters...6-30
6.7.2 Low Power Transmitter...6-31
6.7.3 Transmitter Eye...6-32
6.7.4 Tx Compliance Reference Receiver Equalize Function ...6-32
6.7.5 Informative Transmitter De-emphasis...6-33
6.7.5.1 Gen 1 (5GT/s) ...6-33
6.7.5.2 Gen 2 (10GT/s) ...6-33
6.7.6 Entry into Electrical Idle, U1...6-35
6.8 Receiver Specifications ...6-35
6.8.1 Receiver Equalization Training ...6-35
6.8.2 Informative Receiver CTLE Function...6-36
6.8.2.1 Gen 1 Reference CTLE...6-36
6.8.2.2 Gen 2 Reference Equalizer Function...6-37
6.8.2.2.1 Reference CTLE...6-37
6.8.2.2.2 Reference DFE...6-38
6.8.3 Receiver Electrical Parameters ...6-39
6.8.4 Receiver Loopback...6-40
6.8.4.1 Loopback BERT for Gen 1 Operation...6-40
6.8.5 Normative Receiver Tolerance Compliance Test...6-42
6.9 Low Frequency Periodic Signaling (LFPS)...6-43
6.9.1 LFPS Signal Definition...6-43
6.9.2 Example LFPS Handshake for U1/U2 Exit, Loopback Exit, and U3
Wakeup...6-46
6.9.3 Warm Reset ...6-48
6.9.4 SuperSpeedPlus Capability Declaration ...6-48
6.9.4.1 Binary Representation of Polling.LFPS...6-49
6.9.4.2 SCD1/SCD2 Definitions and Transmission...6-49
6.9.5 SuperSpeedPlus LFPS Based PWM Message (LBPM)...6-51
6.9.5.1 Introduction to LFPS Based PWM Signaling (LBPS) ...6-51
6.9.5.2 LBPM Definition and Transmission...6-52

xiv

Contents

[tbl-12.md](tbl-12.md)

xv

[tbl-13.md](tbl-13.md)

xvi

Contents

7.5.2.4.1 eSS.Inactive.Disconnect.Detect Requirements...7-51
7.5.2.4.2 Exit from eSS.Inactive.Disconnect.Detect...7-51
7.5.3 Rx.Detect...7-52
7.5.3.1 Rx.Detect Substate Machines...7-52
7.5.3.2 Rx.Detect Requirements...7-52
7.5.3.3 Rx.Detect.Reset...7-53
7.5.3.3.1 Rx.Detect.Reset Requirements...7-53
7.5.3.3.2 Exit from Rx.Detect.Reset...7-53
7.5.3.4 Rx.Detect.Active...7-53
7.5.3.5 Rx.Detect.Active Requirements...7-53
7.5.3.6 Exit from Rx.Detect.Active...7-53
7.5.3.7 Rx.Detect.Quiet...7-54
7.5.3.7.1 Rx.Detect.Quiet Requirements...7-54
7.5.3.7.2 Exit from Rx.Detect.Quiet...7-54
7.5.4 Polling...7-55
7.5.4.1 Polling Substate Machines...7-55
7.5.4.2 Polling Requirements...7-55
7.5.4.3 Polling.LFPS...7-56
7.5.4.3.1 Polling.LFPS Requirements...7-56
7.5.4.3.2 Exit from Polling.LFPS...7-57
7.5.4.4 Polling.LFPSPlus...7-58
7.5.4.4.1 Polling.LFPSPlus Requirements...7-58
7.5.4.4.2 Exit from Polling.LFPSPlus...7-58
7.5.4.5 Polling.PortMatch...7-59
7.5.4.5.1 PHY Capability LBPM Definition...7-59
7.5.4.5.2 Polling.PortMatch Requirements...7-60
7.5.4.5.3 Exit from Polling.PortMatch...7-60
7.5.4.6 Polling.PortConfig...7-60
7.5.4.6.1 Polling.PortConfig Requirements...7-61
7.5.4.6.2 Exit from Polling.PortConfig...7-61
7.5.4.7 Polling.RxEQ...7-61
7.5.4.7.1 Polling.RxEQ Requirements...7-61
7.5.4.7.2 Exit from Polling.RxEQ...7-62
7.5.4.8 Polling.Active...7-62
7.5.4.8.1 Polling.Active Requirements...7-62
7.5.4.8.2 Exit from Polling.Active...7-62
7.5.4.9 Polling.Configuration...7-63
7.5.4.9.1 Polling.Configuration Requirements...7-63
7.5.4.9.2 Exit from Polling.Configuration...7-63
7.5.4.10 Polling.Idle...7-64
7.5.4.10.1 Polling.Idle Requirements...7-64
7.5.4.10.2 Exit from Polling.Idle...7-65
7.5.5 Compliance Mode...7-67
7.5.5.1 Compliance Mode Requirements...7-67
7.5.5.2 Exit from Compliance Mode...7-68
7.5.6 U0...7-68
7.5.6.1 U0 Requirements...7-68
7.5.6.2 Exit from U0...7-68
7.5.7 U1...7-70

xvii

[tbl-14.md](tbl-14.md)

xviii

Contents

[tbl-15.md](tbl-15.md)

xix

[tbl-16.md](tbl-16.md)

xx

Contents

8.12.1.4.3.8 OUTMvData Device ...8-80

8.12.1.4.3.9 OUTMvData Host ...8-81

8.12.1.4.3.10 OUTMvData Host Terminate ...8-81

8.12.1.4.4 Host IN Stream Protocol ...8-81

8.12.1.4.4.1 Disabled ...8-82

8.12.1.4.4.2 Prime Pipe ...8-82

8.12.1.4.4.3 Idle 8-83

8.12.1.4.4.4 Start Stream ...8-84

8.12.1.4.4.5 Move Data ...8-85

8.12.1.4.4.6 INMvData Device ...8-86

8.12.1.4.4.7 INMvData Host ...8-86

8.12.1.4.4.8 INMvData Burst End ...8-87

8.12.1.4.4.9 INMvData Device Terminate ...8-87

8.12.1.4.5 Host OUT Stream Protocol ...8-88

8.12.1.4.5.1 Disabled ...8-88

8.12.1.4.5.2 Prime Pipe ...8-89

8.12.1.4.5.3 Idle 8-89

8.12.1.4.5.4 Start Stream ...8-90

8.12.1.4.5.5 Start Stream End ...8-90

8.12.1.4.5.6 Move Data ...8-91

8.12.1.4.5.7 OUTMvData Device ...8-92

8.12.1.4.5.8 OUTMvData Host ...8-93

8.12.1.4.5.9 OUTMvData Host Terminate ...8-93

8.12.2 Control Transfers ...8-94

8.12.2.1 Reporting Status Results ...8-96

8.12.2.2 Variable-length Data Stage ...8-97

8.12.2.3 STALL TPs Returned by Control Pipes ...8-97

8.12.3 Bus Interval and Service Interval ...8-98

8.12.4 Interrupt Transactions ...8-98

8.12.4.1 Interrupt IN Transactions ...8-98

8.12.4.2 Interrupt OUT Transactions ...8-101

8.12.5 Host Timing Information ...8-104

8.12.6 Isochronous Transactions ...8-106

8.12.6.1 Enhanced SuperSpeed Isochronous Transactions ...8-106

8.12.6.1.1 Smart Isochronous Scheduling Protocol ...8-112

8.12.6.2 Host Flexibility in Performing SuperSpeed Isochronous

Transactions ...8-116

8.12.6.3 SuperSpeedPlus Isochronous Transactions ...8-116

8.12.6.3.1 Pipelined Isochronous IN Transactions ...8-116

8.12.6.4 Host Flexibility in Performing SuperSpeedPlus Isochronous

Transactions ...8-119

8.12.6.5 Device Response to Isochronous IN Transactions ...8-119

8.12.6.6 Host Processing of Isochronous IN Transactions ...8-119

8.12.6.7 Device Response to an Isochronous OUT Data Packet 8-120

8.13 Timing Parameters ...8-121

# 9 Device Framework ...9-1

9.1 USB Device States ...9-1

9.1.1 Visible Device States ...9-1

xxi

[tbl-17.md](tbl-17.md)

xxii

Contents

9.5 Descriptors ...9-35
9.6 Standard USB Descriptor Definitions ...9-35

9.6.1 Device ...9-35
9.6.2 Binary Device Object Store (BOS) ...9-38

9.6.2.1 USB 2.0 Extension ...9-40
9.6.2.2 SuperSpeed USB Device Capability ...9-41
9.6.2.3 Container ID ...9-43
9.6.2.4 Platform Descriptor ...9-43
9.6.2.5 SuperSpeedPlus USB Device Capability ...9-44
9.6.2.6 Precision Time Measurement ...9-46

9.6.3 Configuration ...9-46
9.6.4 Interface Association ...9-48
9.6.5 Interface ...9-49
9.6.6 Endpoint ...9-51
9.6.7 SuperSpeed Endpoint Companion ...9-55
9.6.8 SuperSpeedPlus Isochronous Endpoint Companion ...9-58
9.6.9 String ...9-59

9.7 Device Class Definitions ...9-60

9.7.1 Descriptors ...9-60
9.7.2 Interface(s) ...9-60
9.7.3 Requests ...9-60

# 10 Hub, Host Downstream Port, and Device Upstream Port Specification 10-1

10.1 Hub Feature Summary ...10-1

10.1.1 Connecting to an Enhanced SuperSpeed Capable Host ...10-5
10.1.2 Connecting to a USB 2.0 Host ...10-6
10.1.3 Hub Connectivity ...10-6

10.1.3.1 Routing Information ...10-6
10.1.3.2 SuperSpeed Hub Packet Signaling Connectivity ...10-8
10.1.3.3 SuperSpeedPlus Hub Packet Routing ...10-9

10.1.4 Resume Connectivity ...10-10
10.1.5 Hub Fault Recovery Mechanisms ...10-10
10.1.6 Hub Buffer Architecture ...10-11

10.1.6.1 SuperSpeed Hub Buffer Architecture ...10-11

10.1.6.1.1 SuperSpeed Hub Header Packet Buffer Architecture 10-11
10.1.6.1.2 Hub Data Buffer Architecture ...10-12

10.1.6.2 SuperSpeedPlus Hub Buffer Architecture ...10-12

10.2 Hub Power Management ...10-13

10.2.1 Link States ...10-13
10.2.2 Hub Downstream Port U1/U2 Timers ...10-13
10.2.3 Downstream/Upstream Port Link State Transitions ...10-14

10.3 Hub Downstream Facing Ports ...10-14

10.3.1 Hub Downstream Facing Port State Descriptions ...10-17

10.3.1.1 DSPORT.Powered-off ...10-17
10.3.1.2 DSPORT.Disconnected (Waiting for eSS Connect) ...10-18
10.3.1.3 DSPORT.Training ...10-19
10.3.1.4 DSPORT.ERROR ...10-19
10.3.1.5 DSPORT.Enabled ...10-19
10.3.1.6 DSPORT.Resetting ...10-20

xxiii

[tbl-18.md](tbl-18.md)

xxiv

Contents

10.8.6 SuperSpeedPlus Hub Arbitration of Packets ...10-40
10.8.6.1 Arbitration Weight...10-40
10.8.6.2 Direction Independent Packet Selection ...10-40
10.8.6.3 Downstream Flowing Packet Reception and Selection...10-41
10.8.6.4 Upstream Flowing Packet Reception and Selection ...10-41
10.8.6.4.1 Partially Buffered DP Selection Candidate...10-41
10.8.6.4.2 Upstream Weighted Round Robin Arbitration ...10-42
10.8.7 SuperSpeedPlus Upstream Flowing Packet Modifications...10-43
10.8.8 SuperSpeedPlus Downstream Controller ...10-43
10.9 Port State Machines ...10-43
10.9.1 Port Transmit State Machine ...10-44
10.9.2 Port Transmit State Descriptions ...10-46
10.9.2.1 Tx IDLE...10-46
10.9.2.2 Tx Header ...10-46
10.9.2.3 Tx Data ...10-46
10.9.2.4 Tx Data Abort...10-46
10.9.2.5 Tx Link Command ...10-46
10.9.3 Port Receive State Machine ...10-47
10.9.4 Port Receive State Descriptions ...10-47
10.9.4.1 Rx Default ...10-47
10.9.4.2 Rx Data ...10-48
10.9.4.3 Rx Header...10-48
10.9.4.4 Process Header Packet...10-48
10.9.4.4.1 SuperSpeed Hub Upstream Facing Port...10-49
10.9.4.4.2 SuperSpeedPlus Hub Upstream Facing Port...10-50
10.9.4.4.3 SuperSpeed Hub Downstream Facing Port ...10-51
10.9.4.4.4 SuperSpeedPlus Hub Downstream Facing Port ...10-52
10.9.4.5 Rx Link Command...10-52
10.9.4.6 Process Link Command ...10-52
10.10 Suspend and Resume ...10-52
10.11 Hub Upstream Port Reset Behavior...10-53
10.12 Hub Port Power Control...10-53
10.12.1 Multiple Gangs ...10-54
10.13 Hub Controller ...10-54
10.13.1 Endpoint Organization...10-55
10.13.2 Hub Information Architecture and Operation...10-55
10.13.3 Port Change Information Processing ...10-57
10.13.4 Hub and Port Status Change Bitmap...10-58
10.13.5 Over-current Reporting and Recovery ...10-59
10.13.6 Enumeration Handling...10-60
10.14 Hub Configuration...10-60
10.15 Descriptors ...10-62
10.15.1 Standard Descriptors for Hub Class ...10-62
10.15.2 Class-specific Descriptors ...10-68
10.15.2.1 Hub Descriptor ...10-68
10.16 Requests ...10-70
10.16.1 Standard Requests...10-70
10.16.2 Class-specific Requests ...10-71
10.16.2.1 Clear Hub Feature...10-73

xxv

[tbl-19.md](tbl-19.md)

## 11 Interoperability and Power Delivery 11-1

[tbl-20.md](tbl-20.md)

xxvi

Contents

[tbl-21.md](tbl-21.md)

xxvii

[tbl-22.md](tbl-22.md)

xxviii

Contents

# Figures

Figure 2-1. Port and Link Pictorial ...2-9

Figure 3-1. USB 3.1 Dual Bus System Architecture...3-2

Figure 3-2. USB 3.1 Cable ...3-3

Figure 3-3. USB 3.1 Terminology Reference Model ...3-5

Figure 3-4. Enhanced SuperSpeed Bus Communications Layers and Power Management
Elements...3-6

Figure 3-5. Examples of Supported USB 3.1 USB Physical Device Topologies...3-13

Figure 3-6. SuperSpeed Only Enhanced SuperSpeed Peripheral Device Configuration..3-13

Figure 3-7. Enhanced SuperSpeed Device Configuration ...3-13

Figure 3-8. Multiple SuperSpeed Bus Instances in an Enhanced SuperSpeed System...3-15

Figure 4-1. Enhanced SuperSpeed IN Transaction Protocol ...4-6

Figure 4-2. Enhanced SuperSpeed OUT Transaction Protocol ...4-7

Figure 4-3. Enhanced SuperSpeed IN Stream Example...4-11

Figure 5-1. USB 3.1 Standard-A Receptacle Interface Dimensions ...5-7

Figure 5-2. Example USB 3.1 Standard-A Receptacle with Grounding Springs and Required
contact zones on the Standard-A Plug...5-9

Figure 5-3. Example USB 3.1 Standard-A Mid-Mount Receptacles with Insertion Detect 5-10

Figure 5-4. USB 3.1 Standard-A Plug Interface Dimensions...5-13

Figure 5-5. Example Footprint for the USB 3.1 Standard-A Receptacle - Through-Hole with
Back-Shield...5-16

Figure 5-6. Example Footprint for the USB 3.1 Standard-A Receptacle - Mid-Mount
Standard Mount Through-Hole with Insertion Detect...5-17

Figure 5-7. Example Footprint for the USB 3.1 Standard-A Receptacle - Mid-Mount Reverse
Mount Through-Hole with Insertion Detect ...5-18

Figure 5-8. Illustration of Color Coding Recommendation for USB 3.1 Standard-A
Connector ...5-20

Figure 5-9. USB 3.1 Standard-B Receptacle Interface Dimensions ...5-22

Figure 5-10. USB 3.1 Standard-B Plug Interface Dimensions...5-23

Figure 5-11. Reference Footprint for the USB 3.1 Standard-B Receptacle ...5-24

Figure 5-12. USB 3.1 Micro-B and -AB Receptacles Interface Dimensions ...5-27

Figure 5-13. USB 3.1 Micro-B and Micro-A Plug Interface Dimensions ...5-30

Figure 5-14. Reference Footprint for the USB 3.1 Micro-B or Micro-AB Receptacle ...5-32

Figure 5-15. Illustration of a USB 3.1 Cable Cross-Section ...5-34

Figure 5-16. USB 3.1 Standard-A to USB 3.1 Standard-B Cable Assembly ...5-37

Figure 5-17. USB 3.1 Micro-B Plug Cable Overmold Dimensions...5-39

Figure 5-18. USB 3.1 Micro-A Cable Overmold Dimensions...5-41

Figure 5-19. Typical Plug Orientation ...5-44

Figure 5-20. Recommended Ground Void Dimension for USB Standard-A Receptacle...5-47

Figure 5-21. Impedance Limits of a Mated Connector for Gen 2 Speed ...5-48

Figure 5-22. Illustration of Cable Assembly Mounted on Test Fixture ...5-49

Figure 5-23. Illustration of Cable Assembly with Reference Host and Device ...5-50

Figure 5-24. Illustration of Insertion Loss Fit at Nyquist Frequency...5-51

Figure 5-25. Example of Insertion Loss Deviation ...5-52

Figure 5-26. Pass/Fail Examples...5-54

Figure 5-27. Illustration of Peak-to-Peak Crosstalk...5-55

Figure 5-28. Differential-to-Common-Mode Conversion Requirement for Gen 2...5-56

Figure 5-29. Set Up For Cable SE Measurement (subject to change) ...5-56

Figure 5-30. 4-Axes Continuity Test ...5-60

xxix

Figure 5-31. Mated USB 3.1 Standard-A Connector...5-63
Figure 5-32. Mated USB 3.1 Standard-B Connector...5-64
Figure 5-33. Mated USB 3.1 Micro-B Connector...5-65
Figure 5-34. Examples of Connector Apertures...5-66
Figure 6-1. SuperSpeed Physical Layer...6-1
Figure 6-2. Transmitter Block Diagram...6-2
Figure 6-3. Gen 1 Receiver Block Diagram...6-3
Figure 6-4. Gen 2 Receiver Block Diagram...6-4
Figure 6-5. Channel Models...6-5
Figure 6-6. Character to Symbol Mapping...6-6
Figure 6-7. Bit Transmission Order...6-7
Figure 6-8. LFSR with Scrambling Polynomial...6-8
Figure 6-9. Gen 2 Serialization and Deserialization Order...6-9
Figure 6-10. Gen 2 Bit Transmission Order and Framing...6-9
Figure 6-11. LFSR for use in Gen 2 operation...6-11
Figure 6-12. Jitter Filtering – “Golden PLL” and Jitter Transfer Functions...6-23
Figure 6-13. “Golden PLL” and Jitter Transfer Functions for Gen 1 Operation...6-24
Figure 6-14. “Golden PLL” and Jitter Transfer Functions for Gen 2 Operation...6-24
Figure 6-15. Example of Period Modulation from Triangular SSC...6-26
Figure 6-16. Eye Masks...6-27
Figure 6-17. Single-ended and Differential Voltage Levels...6-28
Figure 6-18. Device Termination Schematic...6-29
Figure 6-19. Tx Normative Setup with Reference Channel...6-32
Figure 6-20. De-Emphasis Waveform...6-33
Figure 6-21. 3-tap Transmit Equalizer Structure...6-34
Figure 6-22. Example Output Waveform for 3-tap Transmit Equalizer...6-34
Figure 6-23. Frequency Spectrum of TSEQ...6-36
Figure 6-24. Gen 1 Tx Compliance Rx EQ Transfer Function...6-37
Figure 6-25. Gen 2 Compliance Rx EQ Transfer Function...6-38
Figure 6-26. Gen 2 reference DFE Function...6-39
Figure 6-27. Rx Tolerance Setup...6-42
Figure 6-28. Jitter Tolerance Curve...6-42
Figure 6-29. LFPS Signaling...6-44
Figure 6-30. U1 Exit, U2 Exit, and U3 Wakeup LFPS Handshake Timing Diagram...6-46
Figure 6-31. Example of Warm Reset Out of U3...6-48
Figure 6-32. Example of Binary Representation based on Polling.LFPS...6-49
Figure 6-33. SCD1/SCD2 transmission...6-50
Figure 6-34. Logic Representation of LBPS...6-61
Figure 6-35. LBPM Transmission Examples...6-52
Figure 6-36. Rx Detect Schematic...6-54
Figure 7-1. Link Layer...7-1
Figure 7-2. Byte Ordering...7-2
Figure 7-3. Enhanced SuperSpeed Header Packet with HPSTART, Packet Header, and
Link Control Word...7-4
Figure 7-4. SuperSpeedPlus DPH Format...7-4
Figure 7-5. Packet Header...7-5
Figure 7-6. CRC-16 Remainder Generation...7-6
Figure 7-7. Link Control Word...7-7
Figure 7-8. CRC-5 Remainder Generation...7-8

xxx

Contents

Figure 7-9. Data Packet Payload with CRC-32 and Framing ...7-8

Figure 7-10. CRC-32 Remainder Generation ...7-9

Figure 7-11. Data Packet with Data Packet Header Followed by Data Packet Payload. (a)
SuperSpeed DP; (b). SuperSpeedPlus DP ...7-11

Figure 7-12. Link Command Structure...7-12

Figure 7-13. Link Command Word Structure ...7-13

Figure 7-14. State Diagram of the Link Training and Status State Machine ...7-48

Figure 7-15. eSS.Disabled Substate Machine ...7-50

Figure 7-16. eSS.Inactive Substate Machine...7-52

Figure 7-17. Rx.Detect Substate Machine ...7-55

Figure 7-18. Polling Substate Machine ...7-67

Figure 7-19. U1 ...7-71

Figure 7-20. U2 ...7-72

Figure 7-21. U3 ...7-73

Figure 7-22. Recovery Substate Machine...7-77

Figure 7-23. Loopback Substate Machine ...7-79

Figure 7-24. Hot Reset Substate Machine ...7-81

Figure 8-1. Protocol Layer Highlighted ...8-1

Figure 8-2. Example Transaction Packet...8-4

Figure 8-3. Link Control Word Detail ...8-6

Figure 8-4. Link Management Packet Structure...8-7

Figure 8-5. Set Link Function LMP ...8-8

Figure 8-6. U2 Inactivity Timeout LMP...8- 9

Figure 8-7. Vendor Device Test LMP ...8-10

Figure 8-8. Port Capability LMP...8-11

Figure 8-9. Port Configuration LMP ...8-12

Figure 8-10. Port Configuration Response LMP ...8-13

Figure 8-11. Link Delay Measurement Protocol...8-15

Figure 8-12. PTM ITP Protocol...8-16

Figure 8-13. LDM State Machine Notation...8-17

Figure 8-14. LDM Requester State Machine...8-18

Figure 8-15. LDM Responder State Machine...8-21

Figure 8-16. PTM Path Performance Contributors...8-26

Figure 8-17. LDM LMP ...8-29

Figure 8-18. ACK Transaction Packet ...8-31

Figure 8-19. NRDY Transaction Packet...8-34

Figure 8-20. ERDY Transaction Packet...8-34

Figure 8-21. STATUS Transaction Packet...8-35

Figure 8-22. STALL Transaction Packet...8-36

Figure 8-23. Device Notification Transaction Packet ...8-36

Figure 8-24. Function Wake Device Notification ...8-37

Figure 8-25. Latency Tolerance Message Device Notification ...8-38

Figure 8-26. Bus Interval Adjustment Message Device Notification ...8-39

Figure 8-27. Sublink Speed Device Notification...8-42

Figure 8-28. PING Transaction Packet...8-44

Figure 8-29. PING_RESPONSE Transaction Packet ...8-45

Figure 8-30. Example Data Packet...8-46

Figure 8-31. Isochronous Timestamp Packet ...8-49

Figure 8-32. Route String Detail ...8-51

xxxi

Figure 8-33. Sample Concurrent BULK IN Transactions ...8-55
Figure 8-34. Sample Concurrent BULK and Isochronous IN Transactions ...8-56
Figure 8-35. Legend for State Machines...8-62
Figure 8-36. Sample BULK IN Sequence ...8-64
Figure 8-37. Sample BULK OUT Sequence ...8-65
Figure 8-38. General Stream Protocol State Machine (SPSM) ...8-66
Figure 8-39. Device IN Stream Protocol State Machine (DISPSM)...8-70
Figure 8-40. Device IN Move Data State Machine (DIMDSM) ...8-73
Figure 8-41. Device OUT Stream Protocol State Machine (DOSPSM) ...8-76
Figure 8-42. Device OUT Move Data State Machine (DOMDSM)...8-79
Figure 8-43. Host IN Stream Protocol State Machine (HISPSM) ...8-82
Figure 8-44. Host IN Move Data State Machine (HIMDSM)...8-85
Figure 8-45. Host OUT Stream Protocol State Machine (HOSPSM)...8-88
Figure 8-46. Host OUT Move Data State Machine (HOMDSM) ...8-91
Figure 8-47. Control Read Sequence ...8-95
Figure 8-48. Control Write Sequence ...8-96
Figure 8-49. Host Sends Interrupt IN Transaction in Each Service Interval ...8-99
Figure 8-50. Host Stops Servicing Interrupt IN Transaction Once NRDY is Received ...8-100
Figure 8-51. Host Resumes IN Transaction after Device Sent ERDY ...8-100
Figure 8-52. Endpoint Sends STALL TP...8-100
Figure 8-53. Host Detects Error in Data and Device Resends Data...8-101
Figure 8-54. Host Sends Interrupt OUT Transaction in Each Service Interval...8-102
Figure 8-55. Host Stops Servicing Interrupt OUT Transaction Once NRDY is Received ...8-103
Figure 8-56. Host Resumes Sending Interrupt OUT Transaction After Device Sent ERDY8-103
Figure 8-57. Device Detects Error in Data and Host Resends Data...8-104
Figure 8-58. Endpoint Sends STALL TP...8-104
Figure 8-59. Multiple Active Isochronous Endpoints with Aligned Service Interval
Boundaries...8-106
Figure 8-60. Enhanced SuperSpeed Isochronous IN Transaction Format...8-107
Figure 8-61. Enhanced SuperSpeed Isochronous OUT Transaction Format...8-107
Figure 8-62. Sample Enhanced SuperSpeed Isochronous IN Transaction ...8-109
Figure 8-63. Sample Enhanced SuperSpeed Isochronous OUT Transaction ...8-110
Figure 8-64. Sample Enhanced SuperSpeed Isochronous IN Transaction ...8-111
Figure 8-65. Sample Enhanced SuperSpeed Isochronous OUT Transaction ...8-112
Figure 8-66. Sample Smart Enhanced SuperSpeed Isochronous IN Transaction ...8-114
Figure 8-67. Sample Smart Enhanced SuperSpeed Isochronous OUT Transaction ...8-115
Figure 8-68. Sample Pipeline Isochronous IN Transactions ...8-118
Figure 9-1. Peripheral State Diagram and Hub State Diagram (Enhanced SuperSpeed
Portion Only)...9-2
Figure 9-2. wIndex Format when Specifying an Endpoint...9-15
Figure 9-3. wIndex Format when Specifying an Interface ...9-15
Figure 9-4. Information Returned by a Standard GetStatus() Request to a Device ...9-24
Figure 9-5. Information Returned by a Standard GetStatus() Request to an Interface ...9-25
Figure 9-6. Information Returned by a Standard GetStatus() Request to an Endpoint...9-25
Figure 9-7. Information Returned by a PTM GetStatus() Request to an Endpoint...9-26
Figure 9-8. Example of Feedback Endpoint Relationships...9-54
Figure 10-1. USB Hub Architecture . =...10-2
Figure 10-2. SuperSpeed Portion of the USB Hub Architecture==...10-3
Figure 10-3. SuperSpeedPlus Portion of the Hub Architecture== ...10-4

xxxii

Contents

Figure 10-4. Simple USB Topology ...10-5
Figure 10-5. Route String Example ...10-7
Figure 10-6. SuperSpeed Hub Signaling Connectivity ...10-8
Figure 10-7. Resume Connectivity ...10-10
Figure 10-8. Typical SuperSpeed Hub Header Packet Buffer Architecture ...10-11
Figure 10-9. SuperSpeed Hub Data Buffer Traffic (Header Packet Buffer Only Shown for
DS Port 1) ...10-12
Figure 10-10. Downstream Facing Hub Port State Machine ...10-15
Figure 10-11. Downstream Facing Hub Port Power Management State Machine ...10-23
Figure 10-12. Upstream Facing Hub Port State Machine ...10-28
Figure 10-13. Hub Connect (HCONNECT) State Machine ...10-30
Figure 10-14. Upstream Facing Hub Port Power Management State Machine ...10-32
Figure 10-15. Example SS Hub Header Packet Buffer Architecture - Downstream Traffic 10-37
Figure 10-16. Example SS Hub Header Packet Buffer Architecture - Upstream Traffic ... 10-37
Figure 10-17. Logical Representation of Upstream Flowing Buffers ...10-39
Figure 10-18. Logical Representation of Downstream Flowing Buffers ...10-40
Figure 10-19. Port Transmit State Machine ...10-45
Figure 10-20. Upstream Facing Port Rx State Machine ...10-47
Figure 10-21. Example Hub Controller Organization ...10-55
Figure 10-22. Relationship of Status, Status Change, and Control Information to Device
States ...10-56
Figure 10-23. Port Status Handling Method ...10-57
Figure 10-24. Hub and Port Status Change Bitmap ...10-58
Figure 10-25. Example Hub and Port Change Bit Sampling ...10-59
Figure 10-26. Peripheral Upstream Device Port State Machine ...10-90
Figure 11-1. Compound Self-powered Hub ...11-4
Figure 11-2. Low-power Bus-powered Function ...11-5
Figure 11-3. High-power Bus-powered Function ...11-5
Figure 11-4. Self-powered Function ...11-6
Figure 11-5. Worst-case Voltage Drop Topology (Steady State) ...11-7
Figure 11-6. Worst-case Voltage Drop Analysis Using Equivalent Resistance ...11-7
Figure 11-7. Typical Suspend Current Averaging Profile ...11-8
Figure C-1. Flow Diagram for Host Initiated Wakeup ...C-11
Figure C-2. Device Total Intrinsic Latency Tolerance ...C-13
Figure C-3. Host to Device Path Exit Latency Calculation Examples ...C-15
Figure C-4. Device Connected Directly to a Host ...C-16
Figure C-5. Device Connected Through a Hub ...C-18
Figure C-6. Downstream Host to Device Path Exit Latency with Hub ...C-19
Figure C-7. Upstream Device to Host Path Exit Latency with Hub ...C-20
Figure C-8. LT State Diagram ...C-24
Figure C-9. System Power during SuperSpeed and High Speed Device Data Transfers ..C-27
Figure D-1. Sample ERDY Transaction Packet ...D-1
Figure D-2. Sample Data Packet ...D-1
Figure D-3. Example placement of Gen 2 SKP Block, Idle Symbols, Link Command and
Header Packet ...D-2
Figure D-4. Example placement of Gen 2 Data Packets and Idle Symbols ...D-3

xxxiii

# Tables

Table 3-1. Comparing Enhanced SuperSpeed Bus to USB 2.0 Bus...3-4

Table 5-1. Plugs Accepted By Receptacles...5-2

Table 5-2. USB 3.1 Standard-A Connector Pin Assignments ...5-19

Table 5-3. USB 3.1 Standard-B Connector Pin Assignments ...5-25

Table 5-4. USB 3.1 Micro-B Connector Pin Assignments ...5-33

Table 5-5. USB 3.1 Micro-AB/-A Connector Pin Assignments ...5-33

Table 5-6. Cable Wire Assignments ...5-35

Table 5-7. Reference Wire Gauges ...5-35

Table 5-8. USB 3.1 Standard-A to USB 3.1 Standard-B Cable Assembly Wiring...5-38

Table 5-9. USB 3.1 Standard-A to USB 3.1 Standard-A Cable Assembly Wiring...5-38

Table 5-10. USB 3.1 Standard-A to USB 3.1 Micro-B Cable Assembly Wiring ...5-40

Table 5-11. USB 3.1 Micro-A to USB 3.1 Micro-B Cable Assembly Wiring ...5-42

Table 5-12. USB 3.1 Micro-A to USB 3.1 Standard-B Cable Assembly Wiring ...5-43

Table 5-13. SDP Differential Insertion Loss Examples for Gen 2 speed ...5-46

Table 5-14. SDP Differential Insertion Loss Examples for Gen 2 speed with Coaxial
Construction...5-46

Table 5-15. Design Targets ...5-49

Table 5-16. Durability Ratings ...5-58

Table 5-17. Environmental Test Conditions...5-61

Table 5-18. Reference Materials¹ ...5-62

Table 6-1. Special Symbols...6-12

Table 6-2. Gen 1 TSEQ Ordered Set ...6-14

Table 6-3. Gen 1 TS1 Ordered Set...6-14

Table 6-4. Gen 1 TS2 Ordered Set...6-15

Table 6-5. Gen 1/Gen 2 Link Configuration...6-15

Table 6-6. Gen 2 TS1 Ordered Set...6-17

Table 6-7. Gen 2 TS2 Ordered Set...6-17

Table 6-8. Gen 2 TSEQ Ordered Set ...6-17

Table 6-9. Gen 2 SYNC Ordered Set ...6-17

Table 6-10. SDS Ordered Set ...6-17

Table 6-11. Gen 1 SKP Ordered Set Structure...6-19

Table 6-12. Gen 2 SKP Ordered Set...6-20

Table 6-13. Compliance Pattern Sequences ...6-21

Table 6-14. Gen 2 Compliance Pattern ...6-22

Table 6-15. Informative Jitter Budgeting at the Silicon Pads...6-22

Table 6-16. SSC Parameters ...6-25

Table 6-17. Transmitter Normative Electrical Parameters...6-30

Table 6-18. Transmitter Informative Electrical Parameters at Silicon Pads...6-31

Table 6-19. Normative Transmitter Eye Mask at Test Point TP1 ...6-32

Table 6-20. Informative Gen 2 Transmitter Equalization Settings ...6-35

Table 6-21. Receiver Normative Electrical Parameters ...6-39

Table 6-22. Receiver Informative Electrical Parameters ...6-40

Table 6-23. BRST ...6-41

Table 6-24. BDAT ...6-41

Table 6-25. BERC ...6-41

Table 6-26. BCNT ...6-41

Table 6-27. Input Jitter Requirements for Rx Tolerance Testing...6-43

xxxiv

Contents

Table 6-28. Normative LFPS Electrical Specification...6-44
Table 6-29. LFPS Transmitter Timing for SuperSpeed Designs¹...6-45
Table 6-30. LFPS Handshake Timing for U1/U2 Exit, Loopback Exit, and U3 Wakeup ...6-47
Table 6-31. Binary Representation of Polling.LFPS...6-49
Table 6-32. LBPS Transmit and Receive Specification...6-51
Table 7-1. CRC-16 Mapping...7-6
Table 7-2. CRC-32 Mapping...7-10
Table 7-3. Link Command Ordered Set Structure...7-12
Table 7-4. Link Command Bit Definitions...7-14
Table 7-5. Link Command Definitions...7-15
Table 7-6. Logical Idle Definition ...7-17
Table 7-7. Transmitter Timers Summary ...7-29
Table 7-8. Link Flow Control Timers Summary...7-30
Table 7-9. Valid Packet Framing Symbol Order (Sx is One of SHP, DPHP, SDP, END or
EDB)...7-37
Table 7-10. Valid Link Command Symbol Order...7-38
Table 7-11. Error Types and Recovery...7-42
Table 7-12. LTSSM State Transition Timeouts...7-46
Table 7-13. PHY Capability LBPM...7-59
Table 8-1. Type Field Description...8-5
Table 8-2. Link Control Word Format...8-6
Table 8-3. Link Management Packet Subtype Field ...8-7
Table 8-4. Set Link Function ...8-9
Table 8-5. U2 Inactivity Timer Functionality ...8-9
Table 8-6. Vendor-specific Device Test Function...8-10
Table 8-7. Port Capability LMP Format ...8-11
Table 8-8. Port Type Selection Matrix ...8-12
Table 8-9. Port Configuration LMP Format (Differences with Port Capability LMP)...8-13
Table 8-10. Port Configuration Response LMP Format (Differences with Port Capability
LMP)...8-14
Table 8-11. LDM LMP ...8-29
Table 8-12. Transaction Packet Subtype Field ...8-30
Table 8-13. ACK TP Format ...8-32
Table 8-14. NRDY TP Format (Differences with ACK TP)...8-34
Table 8-15. ERDY TP Format (Differences with ACK TP) ...8-35
Table 8-16. STATUS TP Format (Differences with ACK TP) ...8-35
Table 8-17. STALL TP Format (Differences with ACK TP) ...8-36
Table 8-18. Device Notification TP Format (Differences with ACK TP)...8-37
Table 8-19. Function Wake Device Notification ...8-38
Table 8-20. Latency Tolerance Message Device Notification ...8-39
Table 8-21. Bus Interval Adjustment Message Device Notification ...8-39
Table 8-22. Sublink Speed Device Notification ...8-42
Table 8-23. PING TP Format (differences with ACK TP) ...8-44
Table 8-24. PING_RESPONSE TP Format (Differences with ACK TP)...8-45
Table 8-25. Data Packet Format (Differences with ACK TP) ...8-47
Table 8-26. Isochronous Timestamp Packet Format ...8-50
Table 8-27. Device Responses to TP Requesting Data (Bulk, Control, and Interrupt
Endpoints)...8-57

xxxv

Table 8-28. Host Responses to Data Received from a Device (Bulk, Control, and Interrupt Endpoints)...8-58
Table 8-29. Device Responses to OUT Transactions (Bulk, Control, and Interrupt Endpoints)...8-59
Table 8-30. Device Responses to SETUP Transactions (Only for Control Endpoints) ...8-60
Table 8-31. Status Stage Responses ...8-97
Table 8-32. ACK TP and DPs for Pipelined Isochronous IN Transactions ...8-117
Table 8-33. Device Responses to Isochronous IN Transactions...8-119
Table 8-34. Host Responses to IN Transactions ...8-120
Table 8-35. Device Responses to OUT Data Packets ...8-120
Table 8-36. Timing Parameters ...8-121
Table 9-1. Visible Enhanced SuperSpeed Device States ...9-3
Table 9-2. Preserved USB Suspend State Parameters ...9-10
Table 9-3. Format of Setup Data ...9-14
Table 9-4. Standard Device Requests ...9-17
Table 9-5. Standard Request Codes ...9-18
Table 9-6. Descriptor Types ...9-19
Table 9-7. Standard Feature Selectors...9-20
Table 9-8. Standard Status Type Codes...9-24
Table 9-9. Suspend Options...9-29
Table 9-10. Device Parameters and Events ...9-34
Table 9-11. Standard Device Descriptor ...9-37
Table 9-12. BOS Descriptor ...9-38
Table 9-13. Format of a Device Capability Descriptor...9-39
Table 9-14. Device Capability Type Codes...9-39
Table 9-15. USB 2.0 Extension Descriptor ...9-40
Table 9-16. SuperSpeed Device Capability Descriptor ...9-41
Table 9-17. Container ID Descriptor ...9-43
Table 9-18. Platform Descriptor...9-43
Table 9-19. SuperSpeedPlus Descriptor ...9-44
Table 9-20. PTM Capability Descriptor ...9-46
Table 9-21. Standard Configuration Descriptor...9-47
Table 9-22. Standard Interface Association Descriptor...9-48
Table 9-23. Standard Interface Descriptor ...9-50
Table 9-24. Standard Endpoint Descriptor...9-51
Table 9-25. Example of Feedback Endpoint Numbers...9-53
Table 9-26. SuperSpeed Endpoint Companion Descriptor ...9-55
Table 9-27. SuperSpeedPlus Isochronous Endpoint Companion Descriptor ...9-58
Table 9-28. String Descriptor Zero, Specifying Languages Supported by the Device ...9-59
Table 9-29. UNICODE String Descriptor ...9-59
Table 10-1. Downstream Facing Hub Port State Machine Diagram Legend ...10-16
Table 10-2. Downstream Port VBUS Requirements ...10-18
Table 10-3. Downstream Flowing Header Packet Processing Actions...10-49
Table 10-4. Hub Power Operating Mode Summary ...10-60
Table 10-5. Enhanced SuperSpeed Hub Descriptor ...10-68
Table 10-6. Hub Responses to Standard Device Requests ...10-70
Table 10-7. Hub Class Requests...10-71
Table 10-8. Hub Class Request Codes ...10-72
Table 10-9. Hub Class Feature Selectors...10-72

xxxvi

Contents

Table 10-10. Hub Status Field, wHubStatus...10-75
Table 10-11. Hub Change Field, wHubChange...10-75
Table 10-12. Port Status Type Codes...10-77
Table 10-13. Port Status Field, wPortStatus...10-78
Table 10-14. Port Change Field, wPortChange...10-81
Table 10-15. Extended Port Status Field, dwExtPortStatus...10-83
Table 10-16. U1 Timeout Value Encoding...10-85
Table 10-17. U2 Timeout Value Encoding...10-85
Table 10-18. Downstream Port Remote Wake Mask Encoding...10-87
Table 10-19. Hub Parameters...10-93
Table 11-1. USB 3.0 and USB 2.0 Interoperability...11-1
Table 11-2. DC Electrical Characteristics...11-10
Table 11-3. VBus/Gnd Wire Gauge vs. Maximum Length...11-11
Table A-1. 8b/10b Data Symbol Codes...A-1
Table C-1. Link States and Characteristics Summary...C-2

xxxvii

xxxviii

# 1 Introduction

## 1.1 Background

The original Universal Serial Bus (USB) was driven by the need to provide a user-friendly plug-and-play way to attach external peripherals to a Personal Computer (PC). USB has gone beyond just being a way to connect peripherals to PCs. Printers use USB to interface directly to cameras. Mobile devices use USB connected keyboards and mice. USB technology commonly finds itself in automobiles, televisions, and set-top boxes. USB, as a protocol, is also being picked up and used in many nontraditional applications such as industrial automation. And USB as a source of power has become the mobile device charging solution endorsed by international communities across the globe.

Initially, USB provided two speeds (12 Mbps and 1.5 Mbps) that peripherals could use. As PCs became increasingly powerful and able to process larger amounts of data, users needed to get more and more data into and out of their PCs. This led to the definition of the USB 2.0 specification in 2000 to provide a third transfer rate of 480 Mbps while retaining backward compatibility. By 2006, two things in the environment happened: the transfer rates of HDDs exceeded 100MB/s, far outstripping USB 2.0's ~32MB/s bandwidth and the amount of digital content users were creating was an ever increasing pace. USB 3.0 was the USB community's response and provided users with the ability to move data at rates up to 450MB/s while retaining backward compatibility with USB 2.0.

Now, with the continued trend for more bandwidth driven by larger and faster storage solutions, higher resolution video, and broader use of USB as an external expansion/docking solution, USB 3.1 extends the performance range of USB up to 1GB/s by doubling the SuperSpeed USB clock rate to 10Gbps and enhancing data encoding efficiency.

## 1.2 Objective of the Specification

This document defines the latest generation USB industry-standard, USB 3.1. The specification describes the protocol definition, types of transactions, bus management, and the programming interface required to design and build systems and peripherals that are compliant with this specification. USB 3.1 is primarily a performance enhancement to SuperSpeed USB 3.0 resulting in providing more than double the bandwidth for devices such as Solid State Drives and High Definition displays.

This specification refers to Enhanced SuperSpeed as a collection of features or requirements that apply to both USB 3.0 and USB 3.1 bus operation. Additionally, where specific differences exist with regard to the USB 3.0 definition of SuperSpeed features or requirements, those differences will be uniquely identified as SuperSpeedPlus (or SSP) features or requirements – generally, "SuperSpeed" is in reference to 5Gbps operation and "SuperSpeedPlus" is in reference to 10Gbps operation.

USB 3.1's goal remains to enable devices from different vendors to interoperate in an open architecture, while maintaining and leveraging the existing USB infrastructure (device drivers,

1-1

Universal Serial Bus 3.1 Specification, Revision 1.0

software interfaces, etc.). The specification is intended as an enhancement to the PC architecture, spanning portable, business desktop, and home environments, as well as simple device-to-device communications. It is intended that the specification allow system OEMs and peripheral developers adequate room for product versatility and market differentiation without the burden of carrying obsolete interfaces or losing compatibility.

### 1.3 Scope of the Document

The specification is primarily targeted at peripheral developers and platform/adapter developers, but provides valuable information for platform operating system/ BIOS/ device driver, adapter IHVs/ISVs, and system OEMs. This specification can be used for developing new products and associated software.

Product developers using this specification are expected to know and understand the USB 2.0 Specification. Specifically, USB 3.1 devices must implement device framework commands and descriptors as defined in the USB 2.0 Specification. Devices operating at the new 10Gbps (Gen 2) speed must implement the SuperSpeedPlus enhancements defined in this version of the specification.

### 1.4 USB Product Compliance

Adopters of the USB 3.1 specification have signed the USB 3.0 Adopters Agreement, which provides them access to a reasonable and nondiscriminatory (RANDZ) license from the Promoters and other Adopters to certain intellectual property contained in products that are compliant with the USB 3.1 specification. Adopters can demonstrate compliance with the specification through the testing program as defined by the USB Implementers Forum (USB-IF). Products that demonstrate compliance with the specification will be granted certain rights to use the USB-IF logos as defined in the logo license.

Starting with USB 3.1, product compliance requirements are being tightened up to prohibit non-certified cables and connectors. Use of any registered icons or logos on products, documentation or packaging will require a license and license requirements will include passing specific product certification.

### 1.5 Document Organization

Chapters 1 through 4 provide an overview for all readers, while Chapters 5 through 11 contain detailed technical information defining USB 3.1.

Readers should contact operating system vendors for operating system bindings specific to USB 3.1.

1-2

Introduction

## 1.6 Design Goals

USB 3.0 was a revolutionary step for USB. USB 3.1 is the next evolutionary step to increase the bandwidth. The goal remains the same; end users view it as the same as they viewed USB 2.0 and USB 3.0, just faster. Several key design areas to meet this goal are listed below:

- Preserve the USB model of smart host and simple device.
- Leverage the existing USB infrastructure. There are a vast number of USB products in use today. A large part of their success can be traced to the existence of stable software interfaces, easily developed software device drivers, and a number of generic standard device class drivers (HID, mass storage, audio, etc.). Enhanced SuperSpeed USB devices are designed to keep this software infrastructure intact so that developers of peripherals can continue to use the same interfaces and leverage all of their existing development work.
- Significantly improve power management. Reduce the active power when sending data and reduce idle power by providing a richer set of power management mechanisms to allow devices to drive the bus into lower power states.
- Ease of use has always been and remains a key design goal for all varieties of USB.
- Preserve the investment. There are a large number of PCs in use that support only USB 2.0. There are a larger number of USB 2.0 peripherals in use. Retaining backward compatibility at the Type-A connector to allow Enhanced SuperSpeed devices to be used, albeit at a lower speed, with USB 2.0 PCs and allow high speed devices with their existing cables to be connected to the USB 3.1 SuperSpeed Type-A connectors.
- Features that allow the host controller to take advantage of the USB 3.1 speed without any change to the OS.

## 1.7 Related Documents

Universal Serial Bus Specification, Revision 2.0

USB On-the-Go Supplement to the USB 2.0 Specification, Revision 1.3

USB On-the-Go and Embedded Host Supplement to the USB 3.0 Specification, Revision 1.0

Universal Serial Bus Micro-USB Cables and Connectors Specification, Revision 1.01

EIA-364-1000.01: Environmental Test Methodology for Assessing the Performance of Electrical Connectors and Sockets Used in Business Office Applications

USB 3.0 Connectors and Cable Assemblies Compliance Document

USB SuperSpeed Electrical Test Methodology white paper

USB 3.0 Jitter Budgeting white paper

INCITS TR-35-2004, INCITS Technical Report for Information Technology – Fibre Channel – Methodologies for Jitter and Signal Quality Specification (FC-MJSQ)

Universal Serial Bus 3.0 Specification (including errata and ECNs through May 1, 2011)

Universal Serial Bus Power Delivery Specification, Revision 1.0 Including Errata through 31-October-2012

For USB Contributor Review Only

1-3

Universal Serial Bus 3.1 Specification, Revision 1.0

1-4

## 2 Terms and Abbreviations

This chapter lists and defines terms and abbreviations used throughout this specification. Note, for terms and abbreviations not defined here, use their generally accepted or dictionary meaning.

[tbl-23.md](tbl-23.md)

2-1

Universal Serial Bus 3.1 Specification, Revision 1.0

[tbl-24.md](tbl-24.md)

2-2

Terms and Abbreviations

[tbl-25.md](tbl-25.md)

For USB Contributor Review Only

2-3

Universal Serial Bus 3.1 Specification, Revision 1.0

[tbl-26.md](tbl-26.md)

2-4

Terms and Abbreviations

[tbl-27.md](tbl-27.md)

For USB Contributor Review Only

2-5

Universal Serial Bus 3.1 Specification, Revision 1.0

[tbl-28.md](tbl-28.md)

2-6

Terms and Abbreviations

[tbl-29.md](tbl-29.md)

For USB Contributor Review Only

2-7

Universal Serial Bus 3.1 Specification, Revision 1.0

[tbl-30.md](tbl-30.md)

2-8

Terms and Abbreviations

[tbl-31.md](tbl-31.md)

![img-0.jpeg](img-0.jpeg)

Figure 2-1. Port and Link Pictorial

Figure 2-1 illustrates the parts of a port and the connection between ports. The USB 3.1 specification only defines a port with a single Tx and Rx. The inclusion of more than one Rx/Tx

For USB Contributor Review Only

2-9

Universal Serial Bus 3.1 Specification, Revision 1.0

pair in a port is for harmonization with the SSIC specification where multiple Rx/Tx pairs are defined. Note: The meanings of the terms used in this figure are not the same as used in PCIe.

2-10

# 3 Architectural Overview

This chapter presents an overview of Universal Serial Bus 3.1 architecture and key concepts. USB 3.1 is similar to earlier versions of USB in that it is a cable bus supporting data exchange between a host computer and a wide range of simultaneously accessible peripherals. The attached peripherals share bandwidth through a host-scheduled protocol. The bus allows peripherals to be attached, configured, used, and detached while the host and other peripherals are in operation.

USB 3.1 is a dual-bus architecture that provides backward compatibility with USB 2.0. One bus is a USB 2.0 bus (see Universal Serial Bus Specification, Revision 2.0) and the other is an Enhanced SuperSpeed bus (see Section 3.1). This specification uses the term Enhanced SuperSpeed as a generic adjective referring to any valid collection of USB defined features that were defined for the bus that runs in parallel to the USB 2.0 bus in a USB 3.1 system, as defined below. This chapter is organized into several focus areas. The first focuses on architecture and concepts related to elements which span the USB 3.1 system (Section 3.1). The remaining sections focus on Enhanced SuperSpeed USB specific architecture and concepts.

Later chapters describe the various components and specific requirements of Enhanced SuperSpeed USB in greater detail. The reader is expected to have a fundamental understanding of the architectural concepts of USB 2.0. Refer to the Universal Serial Bus Specification, Revision 2.0 for complete details.

## 3.1 USB 3.1 System Description

The USB 3.1 system architecture (Figure 3-1) is comprised of two simultaneously active buses: a USB 2.0 bus and an Enhanced SuperSpeed bus. The Enhanced SuperSpeed bus has similar architectural components to USB 2.0, namely:

3-1

Universal Serial Bus 3.1 Specification, Revision 1.0

![img-1.jpeg](img-1.jpeg)

Figure 3-1. USB 3.1 Dual Bus System Architecture

- USB 3.1 interconnect
- USB 3.1 devices
- USB 3.1 host

The USB 3.1 interconnect is the manner in which USB 3.1 and USB 2.0 devices connect to and communicate with the USB 3.1 host. The USB 3.1 interconnect inherits core architectural elements from USB 2.0, although several are augmented to accommodate the dual bus architecture.

The baseline structural topology is the same as USB 2.0. It consists of a tiered star topology with a single host at tier 1 and hubs at lower tiers to provide bus connectivity to devices.

The USB 3.1 connection model accommodates backward and forward compatibility for connecting USB 3.1 or USB 2.0 devices into a USB 3.1 connector. Similarly, USB 3.1 devices

can be attached to a USB 2.0 connector. The mechanical and electrical backward/forward compatibility for USB 3.1 is accomplished via a composite cable and associated connector assemblies that form the mechanical infrastructure for the dual-bus architecture. USB 3.1 peripheral devices accomplish backward compatibility by including both Enhanced SuperSpeed and USB 2.0 interfaces. USB 3.1 hosts have both Enhanced SuperSpeed and USB 2.0 interfaces, which are essentially parallel buses that may be active simultaneously.

The USB 3.1 connection model allows for the discovery and configuration of USB devices at the highest signaling speed supported by the peripheral device, the highest signaling rate supported by hubs between the host and peripheral device, and the current host capability and configuration.

USB 3.1 hubs are a specific class of USB device whose purpose is to provide additional connection points to the bus beyond those provided by the host. In this specification, non-hub devices are referred to as peripheral devices in order to differentiate them from hub devices. In addition, in USB 2.0 the term “function” was sometimes used interchangeably with device. In this specification a function is a logical entity within a device, see Figure 3-4.

The architectural implications of Enhanced SuperSpeed bus support on hosts, hub devices and peripheral devices are described in detail in Section 3.2.

### 3.1.1 USB 3.1 Physical Interface

The physical interface of USB 3.1 is comprised of USB 2.0 and Enhanced SuperSpeed portions. The USB 2.0 definitions for Electrical can be found in Chapter 7 of the USB 2.0 specification. The Enhanced SuperSpeed definitions are contained in this USB 3.1 specification and comprised of Mechanical (Chapter 5), and Physical Layer (Chapter 6) specifications. The physical layer for the Enhanced SuperSpeed bus is described in Section 3.2.1.

3-2

USB 3.1 Architectural Overview

### 3.1.1.1 USB 3.1 Mechanical

The mechanical specifications for USB 3.1 cables and connector assemblies are provided in Chapter 5. All USB devices have an upstream connection. Hosts and hubs (defined below) have one or more downstream connections. Upstream and downstream connectors are not mechanically interchangeable, thus eliminating illegal loopback connections at hubs.

USB 3.1 cables have eight primary conductors: three twisted signal pairs for USB data paths and a power pair. Figure 3-2 illustrates the basic signal arrangement for the USB 3.1 cable. In addition to the twisted signal pair for USB 2.0 data path, two twisted signal pairs are used to provide the Enhanced SuperSpeed data path, one for the transmit path and one for the receive path.

![img-2.jpeg](img-2.jpeg)

Figure 3-2. USB 3.1 Cable

USB 3.1 receptacles (both upstream and downstream) are backward compatible with USB 2.0 connector plugs. USB 3.1 cables and plugs are not intended to be compatible with USB 2.0 upstream receptacles. As an aid to users, USB 3.1 recommends standard coloring for plastic portions of USB 3.1 plugs and receptacles.

Electrical (insertion loss, return loss, crosstalk, etc.) performance for USB 3.1 is defined with regard to raw cables, mated connectors, and mated cable assemblies, with compliance requirements using industry test specifications established for the latter two categories. Similarly, mechanical (insertion/extraction forces, durability, etc.) and environmental (temperature life, mixed flowing gas, etc.) requirements are defined and compliance established via recognized industry test specifications.

### 3.1.2 USB 3.1 Power

The specification covers two aspects of power:

- Power distribution over the USB deals with the issues of how USB devices consume power provided by the downstream ports to which they are connected. USB 3.1 power distribution is similar to USB 2.0, with increased supply budgets for devices operating on an Enhanced SuperSpeed bus.
- Power management deals with how hosts, devices, hubs, and the USB system software interact to provide power efficient operation of the bus. The power management of the USB 2.0 bus portion is unchanged. The use model for power management of the Enhanced SuperSpeed bus is described in Appendix C.

3-3

Universal Serial Bus 3.1 Specification, Revision 1.0

### 3.1.3 USB 3.1 System Configuration

USB 3.1 supports USB devices (all speeds) attaching and detaching from the USB 3.1 at any time. Consequently, system software must accommodate dynamic changes in the physical bus topology. The architectural elements for the discovery of attachment and removal of devices on USB 3.1 are identical to those in USB 2.0. There are enhancements provided to manage the specifics of the Enhanced SuperSpeed bus for configuration and power management.

The independent, dual-bus architecture allows for activation of each of the buses independently and provides for the attachment of USB devices to the highest speed bus available for the device.

### 3.1.4 USB 3.1 Architecture Summary

USB 3.1 is a dual-bus architecture that incorporates USB 2.0 and an Enhanced SuperSpeed bus. Table 3-1 summarizes the key architectural differences between an Enhanced SuperSpeed bus and a USB 2.0 bus.

Table 3-1. Comparing Enhanced SuperSpeed Bus to USB 2.0 Bus

[tbl-32.md](tbl-32.md)

## 3.2 Enhanced SuperSpeed Bus Architecture

Figure 3-3 illustrates the reference model for the terminology in this specification.

3-4

USB 3.1 Architectural Overview

![img-3.jpeg](img-3.jpeg)

U-3-002

Figure 3-3. USB 3.1 Terminology Reference Model

The Enhanced SuperSpeed bus is a layered communications architecture that is comprised of the following elements:

- Enhanced SuperSpeed Interconnect. The Enhanced SuperSpeed interconnect is the manner in which devices are connected to and communicate with the host over the Enhanced SuperSpeed bus. This includes the topology of devices connected to the bus, the communications layers, the relationships between them and how they interact to accomplish information exchanges between the host and devices.
- Devices. Enhanced SuperSpeed devices are sources or sinks of information exchanges. They implement the required device-end, Enhanced SuperSpeed communications layers to accomplish information exchanges between a driver on the host and one or more logical functions on the device.
- Host. An Enhanced SuperSpeed host is a source or sink of information. It implements the required host-end, Enhanced SuperSpeed communications layers to accomplish information exchanges over the bus. It owns the Enhanced SuperSpeed data activity schedule and management of the Enhanced SuperSpeed bus and all devices connected to it.

Figure 3-4 illustrates a reference diagram of the Enhanced SuperSpeed interconnect represented as communications layers through a topology of host, zero to five levels of hubs, and devices.

3-5

Universal Serial Bus 3.1 Specification, Revision 1.0

![img-4.jpeg](img-4.jpeg)

Figure 3-4. Enhanced SuperSpeed Bus Communications Layers and Power Management Elements

The rows (device or host, protocol, link, physical) realize the communications layers of the Enhanced SuperSpeed interconnect. Sections 3.2.1 through 3.2.3 provide architectural overviews of each of the communications layers. The three, left-most columns (host, hub, and device) illustrate the topological relationships between devices connected to the Enhanced SuperSpeed bus; refer to the overview in Sections 3.2.6 through 3.2.7. The right-most column illustrates the influence of power management mechanisms over the communications layers; refer to the overview in Section 3.2.5.

### 3.2.1 Physical Layer

The Gen X physical layer specifications are detailed in Chapter 6. The physical layer defines the PHY portion of a port and the physical connection between a downstream facing port (on a host or hub) and the upstream facing port on a device. The Gen X physical connection is comprised of two differential data pairs, one transmit path and one receive path (see Figure 3-2).

The electrical aspects of each path are characterized as a transmitter, channel, and receiver; these collectively represent a unidirectional differential sublink. Each differential sublink is AC-coupled with capacitors located on the transmitter side of the differential sublink. The channel includes the electrical characteristics of the cables and connectors.

At an electrical level, each differential sublink is initialized by enabling its receiver termination. The transmitter is responsible for detecting the far end receiver termination as an indication of a bus connection and informing the link layer so the connect status can be factored into link operation and management.

When receiver termination is present but no signaling is occurring on the differential sublink, it is considered to be in the electrical idle state. When in this state, low frequency periodic signaling

3-6

USB 3.1 Architectural Overview

(LFPS) is used to signal initialization and power management information. The LFPS is relatively simple to generate and detect and uses very little power.

Each PHY has its own clock domain with Spread Spectrum Clocking (SSC) modulation. The USB 3.1 cable does not include a reference clock so the clock domains on each end of the physical connection are not explicitly connected. Bit-level timing synchronization relies on the local receiver aligning its bit recovery clock to the remote transmitter's clock by phase-locking to the signal transitions in the received bit stream.

The receiver needs to reliably recover clock and data from the bit stream. For Gen 1 operation the transmitter encodes data and control characters into symbols, see section 3.2.1.1. Control symbols are used to achieve byte alignment and are used for framing data and managing the link. Special characteristics make control symbols uniquely identifiable from data symbols. For Gen 2 operation the transmitter block encodes the data and control bytes, see section 3.2.1.2. Special control blocks are used to achieve block alignment in the receiver and for managing the link.

A number of techniques are employed to improve channel performance. For example, to avoid overdriving and improve eye margin at the receiver, transmitter de-emphasis may be applied when multiple bits of the same polarity are sent. Also, equalization may be used in the receiver with the characteristics of the equalization profile being established adaptively as part of link training.

Signal (timing, jitter tolerance, etc.) and electrical (DC characteristics, channel capacitance, etc.) performance of Gen X links are defined with compliance requirements specified in terms of transmit and receive signaling eyes.

The specific Gen X physical layers are summarized in the following sections.

### 3.2.1.1 Gen 1 Physical Layer

The nominal signaling data rate for Gen 1 physical layer is 5 Gbps.

A Gen 1 transmitter encodes data and control characters into symbols using an 8b/10b code.

The physical layer receives 8-bit data from the link layer and scrambles the data to reduce EMI emissions. It then encodes the scrambled 8-bit data into 10-bit symbols for transmission over the physical connection. The resultant data are sent at a rate that includes spread spectrum to further lower the EMI emissions. The bit stream is recovered from the differential sublink by the receiver, assembled into 10-bit symbols, decoded and descrambled, producing 8-bit data that are then sent to the link layer for further processing.

### 3.2.1.2 Gen 2 Physical Layer

The nominal signaling data rate for the Gen 2 physical layer is 10 Gbps.

A Gen 2 transmitter frames data and control bytes (referred to as Symbols) by prepending a 4-bit block identifier to 16 symbols (128 bits) to create a 128b132b block. The symbols of the block may be scrambled or not depending upon their source (whether they are data or which type of control symbol). As in Gen 1 operation the resultant data are sent out across the electrical interconnect using spread spectrum clocking to lower EMI emissions. The bit stream is recovered from the electrical interconnect by the receiver and then assembled and aligned into 132 bit blocks. The data is descrambled and the identifier information and the descrambled bits are passed onto the link layer for further processing.

A Gen 2 PHY uses a protocol over LFPS signaling to negotiate to the highest common data rate capability of two connected PHYs.

3-7

Universal Serial Bus 3.1 Specification, Revision 1.0

### 3.2.2 Link Layer

The Enhanced SuperSpeed link layer specifications are detailed in Chapter 7. An Enhanced SuperSpeed link is a logical and physical connection of two ports. The connected ports are called link partners. A port has a physical part (refer to Section 3.2.1) and a logical part. The link layer defines the logical portion of a port and the communications between link partners.

The logical portion of a port has:

- State machines for managing its end of the physical connection. These include physical layer initialization and event management, i.e., connect, removal, and power management.
- State machines and buffering for managing information exchanges with the link partner. It implements protocols for flow control, reliable delivery (port to port) of packet headers, and link power management. The different link packet types are defined in Chapter 7.
- Buffering for data and protocol layer information elements.

The logical portion of a port also:

- Provides correct framing of sequences of bytes into packets during transmission; e.g., insertion of packet delimiters
- Detects received packets, including packet delimiters and error checks of received header packets (for reliable delivery)
- Provides an appropriate interface to the protocol layer for pass-through of protocol-layer packet information exchanges

The physical layer provides the logical port an interface through which it is able to:

- Manage the state of its PHY (i.e., its end of the physical connection), including power management and events (connection, removal, and wake).
- Transmit and receive byte streams, with additional signals that qualify the byte stream as control sequences or data. The physical layer includes discrete transmit and receive physical links, therefore, a port is able to simultaneously transmit and receive control and data information.

The protocol between link partners uses specific encoded control sequences. Note that control sequences are encoded to be tolerant to a single bit error. Control sequences are used for port-to-port command protocol, framing of packet data (packet delimiters), etc. There is a link-partner protocol for power management that uses packet headers.

### 3.2.3 Protocol Layer

The protocol layer specifications for Enhanced SuperSpeed are detailed in Chapter 8. This protocol layer defines the “end-to-end” communications rules between a host and device (see Figure 3-4).

The Enhanced SuperSpeed protocol provides for application data information exchanges between a host and a device endpoint. This communications relationship is called a pipe. It is a host-directed protocol, which means the host determines when application data is transferred between the host and device. The Enhanced SuperSpeed protocol is not a polled protocol, as a device is able to asynchronously request service from the host on behalf of a particular endpoint.

All protocol layer communications are accomplished via the exchange of packets. Packets are sequences of data bytes with specific control sequences which serve as delimiters managed by the link layer. Host transmitted protocol packets are routed through intervening hubs directly to a peripheral device. They do not traverse bus paths that are not part of the direct path between the host and the target peripheral device. A peripheral device expects it has been targeted by any

3-8

USB 3.1 Architectural Overview

protocol layer packet it receives. Device transmitted protocol packets simply flow upstream through hubs to the host.

Packet headers are the building block of the protocol layer. They are fixed size packets with type and subtype field encodings for specific purposes. A small record within a packet header is utilized by the link layer (port-to-port) to manage the flow of the packet from port to port. Packet headers are delivered through the link layer (port-to-port) reliably. The remaining fields are utilized by the end-to-end protocol.

Application data is transmitted within data packet payloads. Data packet payloads are preceded (in the protocol) by a specifically encoded data packet headers. Data packet payloads are not delivered reliably through the link layer (however, the accompanying data packet headers are delivered reliably). The protocol layer supports reliable delivery of data packets via explicit acknowledgement (header) packets and retransmission of lost or corrupt data. Not all data information exchanges utilize data acknowledgements. Packets moving over the Enhanced SuperSpeed bus (e.g. through multiple hubs) are strongly ordered, end-to-end. They arrive at the recipient device or host in the same order that the host or device endpoint originally transmitted them.

Data may be transmitted in bursts of back-to-back sequences of data packets (depending on the scheduling by the host). The protocol allows efficient bus utilization by concurrently transmitting and receiving over the link. For example, a transmitter (host or device) can burst multiple packets of data back-to-back while the receiver can transmit data acknowledgements without interrupting the burst of data packets. The number of data packets in a specific burst is scheduled by the host. Furthermore, an Enhanced SuperSpeed host may simultaneously schedule multiple OUT bursts to be active at the same time as at least one IN burst. See section 3.2.6.1 for a summary of valid combinations of Enhanced SuperSpeed topologies and section 3.2.7 for limitations of hosts to schedule combinations of bursts to those devices.

The protocol provides flow control support for some transfer types. A device-initiated flow control is signaled by a device via a defined protocol packet. A host-initiated flow control event is realized via the host schedule (host will simply not schedule information flows for a pipe unless it has data or buffering available). On reception of a flow control event, the host will remove the pipe from its schedule. Resumption of scheduling information flows for a pipe may be initiated by the host or device. A device endpoint will notify a host of its readiness (to source or sink data) via an asynchronously transmitted “ready” packet. On reception of the “ready” notification, the host will add the pipe to its schedule, assuming that it still has data or buffering available.

Independent information streams can be explicitly delineated and multiplexed on the bulk transfer type. This means through a single pipe instance, more than one data stream can be tagged by the source and identified by the sink. The protocol provides for the device to direct which data stream is active on the pipe.

Devices may asynchronously transmit notifications to the host. These notifications are used to convey a change in the device or function state.

### 3.2.3.1 SuperSpeed Protocol

All packets of a SuperSpeed burst on a SuperSpeed bus will not have packets from other endpoint flows intermingled within the burst.

A SuperSpeed host transmits a special packet header to the SuperSpeed bus (from the root port) that includes the host’s timestamp. The value in this packet is used to keep SuperSpeed devices (that need to) in synchronization with the host. In contrast to other packet types, the timestamp packet is

3-9

Universal Serial Bus 3.1 Specification, Revision 1.0

forwarded down all paths not in a low power state. The SuperSpeed timestamp packet transmission is scheduled by the host at a specification determined period.

### 3.2.3.2 SuperSpeedPlus Protocol

The SuperSpeedPlus protocol inherits almost all of the SuperSpeed protocol. SuperSpeedPlus protocol defines the following features on the SuperSpeed protocol base:

- ACK Transaction Packets (TPs) and Data Packets (DPs) are annotated with the transfer type of the endpoint and upstream flowing asynchronous DPs on SuperSpeedPlus bus segments are annotated with an arbitration weight (AW) used by SuperSpeedPlus hub arbiters for fair service.
- Relaxed Enhanced SuperSpeed host concurrent endpoint scheduling rules for SuperSpeedPlus endpoints. This decouples asynchronous and periodic transaction scheduling and allows concurrent IN endpoint scheduling for SuperSpeedPlus endpoints and for SuperSpeed endpoints on different SuperSpeed bus-instances (see section 3.2.6.4 for more information).
- Packets to or from simultaneously active endpoints moving over a SuperSpeedPlus bus can be intermingled with each other and reordered (with respect to different endpoints flows) by each SuperSpeedPlus hub they transit.

The SuperSpeedPlus bus also uses the host timestamp packet feature defined for the SuperSpeed bus as described in Section 3.2.3.1it uses the Precision Time Measurement (PTM) feature defined in Section 8.4.8 to determine the link delay. In addition, SuperSpeedPlus hubs are required to update the host timestamp packet based on the link delay and the delay in the hub before forwarding it as described in Section 10.9.4.4.1.

### 3.2.4 Robustness

There are several attributes of Enhanced SuperSpeed USB that contribute to its robustness:

- Signal integrity using differential drivers, receivers, and shielding
- CRC protection for header and data packets
- Link level header packet retries to ensure their reliable delivery
- End-to-end protocol retries of data packets to ensure their reliable delivery
- Detection of attach and detach and system-level configuration of resources
- Data and control pipe constructs for ensuring independence from adverse interactions between functions

### 3.2.4.1 Error Detection

The Gen X physical layer bit error rate is expected to be less than one in 10¹² bits. To provide protection against occasional bit errors, packet framing and link commands have sufficient redundancy to tolerate single-bit errors. Each packet includes a CRC to provide error detection of multiple bit errors. When data integrity is required an error recovery procedure may be invoked in hardware or software.

The protocol includes separate CRCs for headers and data packet payloads. Additionally, the link control word (in each packet header) has its own CRC. A failed CRC in the header or link control word is considered a serious error which will result in a link level retry to recover from the error. A failed CRC in a data packet payload is considered to indicate corrupted data and can be handled by the protocol layer with a request to resend the data packet.

3-10

USB 3.1 Architectural Overview

The link and physical layers work together to provide reliable packet header transmission. The physical layer provides an error rate that does not exceed (on average) one bit error in every 10¹² bits. The link layer uses error checking to catch errors and retransmission of the packet header further reducing the packet header error rate.

### 3.2.4.2 Error Handling

Errors may be handled in hardware or software. Hardware error handling includes reporting and retrying of failed header packets. A USB host controller will try a transmission that encounters errors up to three times before informing the client software of the failure. The client software can recover in an implementation-specific way.

### 3.2.5 Enhanced SuperSpeed Power Management

Enhanced SuperSpeed provides power management at distinct areas in the bus architecture, link, device, and function (refer to Figure 3-4). These power management areas are not tightly coupled but do have dependencies; these mostly deal with allowable power state transitions based on dependencies with power states of links, devices, and functions.

Link power management occurs asynchronously on every link (i.e., locally) in the connected hierarchy. The link power management policy may be driven by the device, the host or a combination of both. The link power state may be driven by the device or by the downstream port inactivity timers that are programmable by host software. The link power states are propagated upwards by hubs (e.g., when all downstream ports are in a low power state, the hub is required to transition its upstream port to a low power state). The decisions to change link power states are made locally. The host does not directly track the individual link power states. Since only those links between the host and device are involved in a given data exchange, links that are not being utilized for data communications can be placed in a lower power state.

The host does not directly control or have visibility of the individual links' power states. This implies that one or more links in the path between the host and device can be in reduced power state when the host initiates a communication on the bus. There are in-band protocol mechanisms that force these links to transition to the operational power state and notify the host that a transition has occurred. The host knows (can calculate) the worst-case transition time to bring a path to any specific device to an active, or ready state, using these mechanisms. Similarly, a device initiating a communication on the bus with its upstream link in a reduced power state, will first transition its link into an operational state which will cause all links between it and the host to transition to the operational state.

The key points of link power management include:

- Devices send asynchronous ready notifications to the host.
- Packets are routed, allowing links that are not involved in data communications to transition to and/or remain in a low power state.
- Packets that encounter ports in low power states cause those ports to transition out of the low power state with indications of the transition event.
- Multiple host or device driven link states with progressively lower power at increased exit latencies.

As with the USB 2.0 bus, devices can be explicitly suspended via a similar port-suspend mechanism. This sets the link to the lowest link power state and sets a limit on the power draw requirement of the device.

3-11

Universal Serial Bus 3.1 Specification, Revision 1.0

Enhanced SuperSpeed provides support for function power management in addition to device power management. For multi-function (composite) devices, each function can be independently placed into a lower power state. Note that a device shall transition into the suspended state when directed by the host via a port command. The device shall not automatically transition into the suspended state when all the individual functions within it are suspended.

Functions on devices may be capable of being remote wake sources. The remote-wake feature on a function must be explicitly enabled by the host. Likewise, a protocol notification is available for a function to signal a remote wake event that can be associated with the source function. All remote-wake notifications are functional across all possible combinations of individual link power states on the path between the device and host.

### 3.2.6 Devices

All Enhanced SuperSpeed devices share their base architecture with USB 2.0. They are required to carry information for self-identification and generic configuration. They are also required to demonstrate behavior consistent with the defined Enhanced SuperSpeed Device States.

All devices are assigned a USB address when enumerated by the host. Each device supports one or more pipes through which the host may communicate with the device. All devices must support a designated pipe at endpoint zero to which the device’s Default Control Pipe is attached. All devices support a common access mechanism for accessing information through this control pipe. Refer to Chapter 9 for a complete definition of a control pipe.

Enhanced SuperSpeed inherits the categories of information that are supported on the default control pipe from USB 2.0.

The USB 3.1 specification defines two types of USB devices that can be connected to an Enhanced SuperSpeed host. These are described briefly below.

#### 3.2.6.1 Peripheral Devices

A USB 3.1 peripheral device must provide support for both Enhanced SuperSpeed and at least one of the USB 2.0 speeds. The minimal functional requirement for the USB 2.0 speed implementation is for a device to be detected on a USB 2.0 host and allow system software to direct the user to attach the device to an Enhanced SuperSpeed port. A device implementation may provide appropriate full functionality when operating in the implemented USB 2.0 speed mode. Simultaneous operation of Enhanced SuperSpeed and USB 2.0 speed modes is not allowed for peripheral devices.

USB 3.1 devices within a single physical package (i.e., a single peripheral) can consist of a number of functional topologies including single function, multiple functions on a single peripheral device (composite device), and permanently attached peripheral devices behind an integrated hub (compound device) (see Figure 3-5).

3-12

USB 3.1 Architectural Overview

![img-5.jpeg](img-5.jpeg)

Figure 3-5. Examples of Supported USB 3.1 USB Physical Device Topologies

An Enhanced SuperSpeed portion of a peripheral device may only be assembled into one of the following configurations:

- SuperSpeed Only Peripheral Device. This device implementation is comprised of a Gen 1 only PHY and conforms to the SuperSpeed link, protocol and device specifications; see Figure 3-6.

![img-6.jpeg](img-6.jpeg)

Figure 3-6. SuperSpeed Only Enhanced SuperSpeed Peripheral Device Configuration

- Enhanced SuperSpeed Device. This is an attachable device that must implement both SuperSpeed and SuperSpeedPlus device architecture and at all Gen X speeds; see Figure 3-7.

![img-7.jpeg](img-7.jpeg)

Figure 3-7. Enhanced SuperSpeed Device Configuration

For additional information about USB 3.1 Hubs, see section 3.2.6.2.

3-13

Universal Serial Bus 3.1 Specification, Revision 1.0

### 3.2.6.2 Hubs

The specifications for the Enhanced SuperSpeed portion of a USB 3.1 hub are detailed in Chapter 10. Hubs have always been a key element in the plug-and-play architecture of the USB. Hosts provide an implementation-specific number of downstream ports to which devices can be attached. Hubs provide additional downstream ports so they provide users with a simple connectivity expansion mechanism for the attachment of additional devices to the USB.

In order to support the dual-bus architecture of USB 3.1, a USB 3.1 hub is the logical combination of two hubs: a USB 2.0 hub and an Enhanced SuperSpeed hub (see the hub in Figure 3-1). The power and ground from the cable connected to the upstream port are shared across both units within the USB 3.1 hub. The USB 2.0 hub unit is connected to the USB 2.0 data lines and the Enhanced SuperSpeed hub is connected to the SuperSpeed data lines. A USB 3.1 hub connects upstream as two devices; an Enhanced SuperSpeed hub on the Enhanced SuperSpeed bus and a USB 2.0 hub on the USB 2.0 bus.

A USB 3.1 hub has one upstream port and one or more downstream ports. All ports operate at all USB 2.0 speeds and at all Gen X speeds. The Enhanced SuperSpeed hub manages the Enhanced SuperSpeed portions of the downstream ports and the USB 2.0 hub manages the USB 2.0 portions of the downstream ports. Each physical port has bus-specific control/status registers. Refer to the Universal Serial Bus Specification, Revision 2.0 for details on the USB 2.0 hub. Hubs detect device attach, removal, and remote-wake events on downstream ports and enable the distribution of power to downstream devices. It also has hardware support for reset and suspend/resume signaling.

An Enhanced SuperSpeed hub has a hub controller that responds to standard, hub-specific status/control commands that are used by a host to configure the hub and to monitor and control its downstream ports.

An Enhanced SuperSpeed hub operates as a SuperSpeed hub when its upstream facing port is operating at Gen 1 speed and operates as a SuperSpeedPlus hub when it upstream facing port is operating in any Gen X speeds beyond Gen 1.

### 3.2.6.3 SuperSpeed Hub

A SuperSpeed hub consists of two logical components: a SuperSpeed hub controller and a SuperSpeed repeater/forwarder. The hub repeater/forwarder is a protocol-controlled router between the SuperSpeed upstream port and downstream ports. The repeater architecture allows a host to schedule simultaneous out-bound bursts to different endpoints on a SuperSpeed bus. It limits the number of simultaneous in-bound bursts from different endpoints on a SuperSpeed bus to one.

SuperSpeed hubs actively participate in the (end-to-end) protocol in several ways, including:

- Routes out-bound packets to explicit downstream ports.
- Routes in-bound packets from a downstream port to the upstream port.
- Propagates the timestamp packet to all downstream ports not in a low-power state.
- Detects when packets encounter a port that is in a low-power state. The hub transitions the targeted port out of the low-power state and notifies the host and device (in-band) that the packet encountered a port in a low-power state.

### 3.2.6.4 SuperSpeedPlus Hub

A SuperSpeedPlus hub serves a special role when its upstream facing port is operating at a Gen 2 or beyond speed (not Gen 1 speed). A SuperSpeedPlus hub isolates downstream signaling environments from the upstream signaling environment utilizing a store-and-forward architecture.

3-14

USB 3.1 Architectural Overview

Figure 3-8 illustrates a SuperSpeedPlus hub with an upstream facing port running in beyond Gen 1 speed, supporting downstream devices operating at both Gen 1 speed and beyond Gen 1 speeds.

In contrast to the SuperSpeed hub, which is characterized as a repeater/forwarder hub architecture, the SuperSpeedPlus hub is characterized as a store-and-forward hub because it can receive one or more entire DPs before transmitting up or downstream. The store-and-forward architecture of a SuperSpeedPlus hub allows a host to schedule multiple endpoint bursts, across multiple endpoints, for both in-bound and out-bound flows, as long as they bursts are to SuperSpeedPlus endpoints. The SuperSpeedPlus host is also able to use the same SuperSpeedPlus scheduling rules across SuperSpeed endpoints on different downstream SuperSpeed bus instances. The SuperSpeedPlus host must use SuperSpeed only bus scheduling rules for all SuperSpeed endpoints on the same SuperSpeed bus instance.

![img-8.jpeg](img-8.jpeg)

Figure 3-8. Multiple SuperSpeed Bus Instances in an Enhanced SuperSpeed System

A SuperSpeedPlus hub consists of three logical components: a SuperSpeedPlus hub controller, a SuperSpeedPlus upstream controller and a SuperSpeedPlus downstream controller (one for each downstream facing port).

A SuperSpeedPlus hub is required to implement USB PTM (Precision Time Management).

SuperSpeedPlus hubs actively participate in the (end-to-end) protocol in several ways, including:

- Routes and preserves ordering (within an endpoint flow) of out-bound packets (TPs, DPs) from the upstream port to specific downstream ports
- Routes in-bound packets and preserves ordering (within an endpoint flow) to the upstream port, via:

- Providing fair-service for simultaneously active, in-bound, asynchronous transfer type endpoint data flows, independent of device operating speed or location within the topology.
- Providing strict-priority for simultaneously active, in-bound, periodic transfer type endpoint data flows, independent of device operating speed or location within the topology.

3-15

Universal Serial Bus 3.1 Specification, Revision 1.0

- SuperSpeedPlus hubs ensure compatibility with SuperSpeed devices connected to its downstream facing ports.
- Detects when packets encounter a port that is in a low-power state. The hub transitions the targeted port out of the low-power state and notifies the host and device (in-band) that the packet encountered a port in a low-power state.
- Updates the host timestamp packet based on the link delay and the delay in the hub before forwarding it to all downstream ports that are not in a low-power state.

### 3.2.7 Hosts

A USB 3.1 host interacts with USB devices through a host controller. To support the dual-bus architecture of USB 3.1, a host controller must include both Enhanced SuperSpeed and USB 2.0 elements, which can simultaneously manage control, status and information exchanges between the host and devices over each bus.

The host includes an implementation-specific number of root downstream ports for Enhanced SuperSpeed and USB 2.0. Through these ports the host:

- Detects the attachment and removal of USB devices
- Manages control flow between the host and USB devices
- Manages data flow between the host and USB devices
- Collects status and activity statistics
- Provides power to attached USB devices
- A SuperSpeedPlus host is required to implement USB PTM (Precision Time Management)..

USB System Software inherits its architectural requirements from USB 2.0, including:

- Device enumeration and configuration
- Scheduling of periodic and asynchronous data transfers
- Device and function power management
- Device and bus management information

## 3.3 Enhanced SuperSpeed Bus Data Flow Models

The data flow models for the Enhanced SuperSpeed bus are described in Chapter 4. The Enhanced SuperSpeed bus inherits the data flow models from USB 2.0, including:

- Data and control exchanges between the host and devices are via sets of either unidirectional or bi-directional pipes.
- Data transfers occur between host software and a particular endpoint on a device. The endpoint is associated with a particular function on the device. These associations between host software to endpoints related to a particular function are called pipes. A device may have more than one active pipe. There are two types of pipes: stream and message. Stream data has no USB-defined structure, while message does. Pipes have associations of data bandwidth, transfer service type (see below), and endpoint characteristics, like direction and buffer size.
- Most pipes come into existence when the device is configured by system software. However, one message pipe, the Default Control Pipe, always exists once a device has been powered and is in the default state, to provide access to the device's configuration, status, and control information.

3-16

USB 3.1 Architectural Overview

- A pipe supports one of four transfer types as defined in USB 2.0 (bulk, control, interrupt, and isochronous). The basic architectural elements of these transfer types are unchanged from USB 2.0.
- The bulk transfer type has an extension for Enhanced SuperSpeed protocol called Streams. Streams provide in-band, protocol-level support for multiplexing multiple independent logical data streams through a standard bulk pipe.

3-17

Universal Serial Bus 3.1 Specification, Revision 1.0

3-18

# 4. Enhanced SuperSpeed Data Flow Model

This chapter presents a high-level description of how data and information move across the Enhanced SuperSpeed bus. Consult the Protocol Layer Chapter for details on the low-level protocol. This chapter provides device framework overview information that is further expanded in the Device Framework Chapter. All implementers should read this chapter to understand the key concepts of the Enhanced SuperSpeed bus.

## 4.1 Implementer Viewpoints

The Enhanced SuperSpeed bus is very similar to USB 2.0 in that it provides communication services between a USB Host and attached USB Devices. The communication model view preserves the USB 2.0 layered architecture and basic components of the communication flow (i.e., point-to-point, same transfer types, etc.). Refer to Chapter 5 in the *Universal Serial Bus Specification, Revision 2.0* for more information about the USB 2.0 communication flow.

This chapter describes the differences (from USB 2.0) of how data and control information are communicated between an Enhanced SuperSpeed Host and its attached Enhanced SuperSpeed Devices. In order to understand Enhanced SuperSpeed data flow, the following concepts are useful:

- Communication Flow Models: Section 4.2 describes how communication flows between the host and devices over the Enhanced SuperSpeed bus.
- Enhanced SuperSpeed Protocol Overview: Section 4.3 gives a high level overview of the Enhanced SuperSpeed protocol and compares it to the USB 2.0 protocol.
- Generalized Transfer Description: Section 4.4 provides an overview of how data transfers work using the Enhanced SuperSpeed protocol and subsequent sections define the operating constraints for each transfer type.
- Device Notifications: Section 4.4.9 provides an overview of Device Notifications, a feature which allows a device to asynchronously notify its host of events or status on the device.
- Reliability and Efficiency: Sections 4.4.10 and 4.4.11 summarize the information and mechanisms available for the Enhanced SuperSpeed bus to ensure reliability and increase efficiency.

## 4.2 Enhanced SuperSpeed Communication Flow

The Enhanced SuperSpeed Bus retains the familiar concepts, mechanisms and support for endpoints, pipes, and transfer types. Refer to the *Universal Serial Bus Specification, Revision 2.0* for details. As in USB 2.0, the ultimate consumer/producer of data is an endpoint.

The endpoint's characteristics (Max Packet Size, Burst Size, etc.) are reported in the endpoint descriptor and the SuperSpeed Endpoint Companion Descriptor. As in USB 2.0, the endpoint is identified using an addressing triple {Device Address, Endpoint Number, Direction}.

All Enhanced SuperSpeed devices must implement at least the Default Control Pipe (endpoint zero). The Default Control Pipe is a control pipe as defined in the *Universal Serial Bus Specification, Revision 2.0*.

4-1

Universal Serial Bus 3.1 Specification, Revision 1.0

### 4.2.1 Pipes

An Enhanced SuperSpeed pipe is an association between an endpoint on a device and software on the host. Pipes represent the ability to move data between software on the host via a memory buffer and an endpoint on a device and have the same behavior as defined in the *Universal Serial Bus Specification, Revision 2.0*. The main difference is that when a non-isochronous Enhanced SuperSpeed endpoint is busy it returns a Not Ready (NRDY) response and must send an Endpoint Ready (ERDY) notification when it wants to be serviced again. The host will then reschedule the transaction at the next available opportunity within the constraints of the transfer type.

## 4.3 Enhanced SuperSpeed Protocol Overview

As mentioned in the Architecture Overview Chapter, the Enhanced SuperSpeed protocol is architected to take advantage of the dual-simplex physical layer. All USB 2.0 transfer types are supported by the Enhanced SuperSpeed protocol. The differences between the USB 2.0 protocol and the Enhanced SuperSpeed protocol are first discussed followed by a brief description of the packets used in the Enhanced SuperSpeed protocol.

### 4.3.1 Differences from USB 2.0

The Enhanced SuperSpeed bus is backward compatible with USB 2.0 at the framework level. However, there are some fundamental differences between the USB 2.0 and the Enhanced SuperSpeed protocol:

- • USB 2.0 uses a three-part transaction (Token, Data, and Handshake) while the Enhanced SuperSpeed protocol uses the same three parts differently. For OUTs, the token is incorporated in the data packet; while for INs, the Token is replaced by a handshake.
- • USB 2.0 does not support bursting while the Enhanced SuperSpeed protocol supports continuous bursting.
- • USB 2.0 is a half-duplex broadcast bus while the Enhanced SuperSpeed bus is a dual-simplex unicast bus which allows concurrent IN and OUT transactions.
- • USB 2.0 uses a polling model while the Enhanced SuperSpeed protocol uses asynchronous notifications.
- • USB 2.0 does not have a Streaming capability while the Enhanced SuperSpeed protocol supports Streaming for bulk endpoints.
- • USB 2.0 offers no mechanism for isochronous capable devices to enter the low power USB bus state between service intervals. The Enhanced SuperSpeed bus allows isochronous capable devices to autonomously enter low-power link states between service intervals or within a service interval. An Enhanced SuperSpeed host shall transmit a PING packet to the targeted isochronous device before the service interval to allow time for the path to transition back to the active power state before initiating the isochronous transfer.
- • USB 2.0 offers no mechanism for a device to inform the host how much latency the device can tolerate if the system enters lower system power states. Thus a host may not enter lower system power states as it might impact a device's performance because it lacks an understanding of a device's power policy. USB 3.1 provides a mechanism to allow Enhanced SuperSpeed devices to inform the host of their latency tolerance using Latency Tolerance Messaging. The host may use this information to establish a system power policy that accounts for the devices' latency tolerance.

4-2

USB 3.1 Enhanced SuperSpeed Data Flow Model

- USB 2.0 transmits SOF/uSOF at fixed 1 ms/125 μs intervals, with very tight duration and jitter specifications. Enhanced SuperSpeed links have a similar mechanism called an Isochronous Timestamp Packet (ITP) that is transmitted by a host. The USB host may send an Isochronous Timestamp Packet (ITP) within a relaxed timing window from a bus interval boundary. USB 3.0 added a mechanism for devices to send a Bus Interval Adjustment Message that is used by the host to adjust its 125 μs bus interval up to +/-13.333 μs. A device may change the interval with small finite adjustments.
- USB 3.1 defines an optional-normative for hosts and hubs operating at Gen 1 speed and required for hosts and hubs operating at Gen 2 speed, Precision Time Measurement (PTM) capability for Enhanced SuperSpeed devices, enabling the host, hubs, and devices to accurately determine propagation delays through the USB topology.
- USB 2.0 power management, including Link Power Management, is always directly initiated by the host. The Enhanced SuperSpeed bus supports link-level power management that may be initiated from either end of the link. Thus, each link can independently enter low-power states whenever idle and exit whenever communication is needed.
- USB 2.0 handles transaction error detection and recovery and flow control only at the end-to-end level for each transaction. The Enhanced SuperSpeed protocol splits these functions between the end-to-end and link levels.

### 4.3.1.1 Comparing USB 2.0 and Enhanced SuperSpeed Transactions

The Enhanced SuperSpeed dual-simplex physical layer allows information to travel simultaneously in both directions. The Enhanced SuperSpeed protocol allows the transmitter to send multiple data packets before receiving a handshake. For OUT transfers, the information contained in the USB 2.0 Token is incorporated in the data packet header so a separate Token is not required. For IN transfers, a handshake is sent to the device to request data. The device may respond by either returning data, returning a STALL handshake, or by returning a Not Ready (NRDY) handshake to defer the transfer until the device is ready.

The USB 2.0 broadcasts packets to all enabled downstream ports. Every device is required to decode the address triple {device address, endpoint, and direction} of each packet to determine if it needs to respond. The Enhanced SuperSpeed bus unicasts the packets; downstream packets are sent over a directed path between the host and the targeted device while upstream packets are sent over the direct path between the device and the host. Enhanced SuperSpeed packets contain routing information that the hubs use to determine which downstream port the packet needs to traverse to reach the device. There is one exception; the Isochronous Timestamp Packet (ITP) is multicast to all active ports.

USB 2.0 style polling has been replaced with asynchronous notifications. The Enhanced SuperSpeed transaction is initiated by the host making a request followed by a response from the device. If the device can honor the request, it either accepts or sends data. If the endpoint is halted, the device shall respond with a STALL handshake. If it cannot honor the request due to lack of buffer space or data, it responds with a Not Ready (NRDY) to tell the host that it is not able to process the request at this time. When the device can honor the request, it will send an Endpoint Ready (ERDY) to the host which will then reschedule the transaction.

The move to unicasting and the limited multicasting of packets together with asynchronous notifications allows links that are not actively passing packets to be put into reduced power states. Upstream and downstream ports cooperate to place their link into a reduced power state that hubs will propagate upstream. Allowing link partners to control their independent link power state and a

4-3

Universal Serial Bus 3.1 Specification, Revision 1.0

hub's propagating the highest link power state seen on any of its downstream ports to its upstream port, puts the bus into the lowest allowable power state rapidly.

### 4.3.1.2 Introduction to Enhanced SuperSpeed Packets

Enhanced SuperSpeed packets start with a 16-byte header. Some packets consist of a header only. All headers begin with the Packet Type information used to decide how to handle the packet. The header is protected by a 16-bit CRC (CRC-16) and ends with a 2-byte link control word. Depending on the Type, most packets contain routing information (Route String) and a device address triple {device address, endpoint number, and direction}. The Route String is used to direct packets sent by the host on a directed path through the topology. Packets sent by the device are implicitly routed as the hub always forwards a packet seen on any downstream port to its upstream port. There are four basic types of packets: Link Management Packets, Transaction Packets, Data Packets, and Isochronous Timestamp Packets:

- A Link Management Packet (LMP) only traverses a pair of directly connected ports and is primarily used to manage that link.
- A Transaction Packet (TP) traverses all the links in the path directly connecting the host and a device. It is used to control the flow of data packets, configure devices and hubs, etc. Note that a Transaction Packet does not have a data payload.
- A Data Packet (DP) traverses all the links in the path directly connecting the host and a device. Data Packets consist of two parts: a Data Packet Header (DPH) which is similar to a TP and a Data Packet Payload (DPP) which consists of the data block plus a 32-bit CRC (CRC-32) used to ensure the data's integrity.
- An Isochronous Timestamp Packet (ITP) is a multicast packet sent by an Enhanced SuperSpeed host/hub to all active links.

## 4.4 Generalized Transfer Description

Each non-isochronous data packet sent to a receiver is acknowledged by a handshake (called an ACK transaction packet). However, due to the fact that the Enhanced SuperSpeed bus has independent transmit and receive paths, the transmitter does not have to wait for an explicit handshake for each data packet transferred before sending the next packet.

The Enhanced SuperSpeed bus preserves all of the basic data flow and transfer concepts defined in USB 2.0, including the transfer types, pipes, and basic data flow model. The differences with USB 2.0 are discussed in this section, starting at the protocol level, followed by transfer type constraints.

The USB 2.0 specification utilizes a serial transaction model. This essentially means that a host starts and completes one bus transaction {Token, Data, Handshake} before starting the next transaction. Split transactions also adhere to this same model since they are comprised of complete high-speed transactions {Token, Data, Handshake} that are completed under the same model as all other transactions.

The Enhanced SuperSpeed protocol improves on the USB 2.0 transaction protocol by using the independent transmit and receive paths. The result is that the Enhanced SuperSpeed USB transaction protocol is essentially a split-transaction protocol that generally allows more than one IN or OUT "bus transaction to be active on the bus at the same time. Note that a SuperSpeed link has a restriction that at most one IN "bus transaction" can be active on that SuperSpeed bus instance. The order in which a device responds to transactions is fixed on a per endpoint basis (for example, if an endpoint received three DPs, the endpoint must return ACK TPs for each one, in the

4-4

USB 3.1 Enhanced SuperSpeed Data Flow Model

order that the DPs were received). The order a device responds to ACKs or DPs that are sent to different endpoints on the device is device implementation dependent and software can not expect them to occur/complete in any particular order. The split-transaction protocol scales well (across multiple transactions to multiple function endpoints) with signaling bit-rates as it is not subject to propagation delays.

The USB 2.0 protocol completes an entire IN or OUT transaction {Token, Data, Handshake} before continuing to the next bus transaction for the next scheduled function endpoint. All transmissions from the host are essentially broadcast on the USB 2.0 bus. In contrast, the Enhanced SuperSpeed protocol does not broadcast any packets (except for ITPs) and packets traverse only the links needed to reach the intended recipient. The host starts all transactions by sending handshakes or data and devices respond with either data or handshakes. If the device does not have data available, or cannot accept the data, it responds with a packet that states that it is not able to do so. Subsequently, when the device is ready to either receive or transmit data it sends a notification to the host that indicates that it is ready to resume transactions. In addition, the Enhanced SuperSpeed bus provides the ability to transition links into and out of specific low power states. Lower power link states are entered either under software control or under autonomous hardware control after being enabled by software. Mechanisms are provided to automatically transition all links in the path between the host and a device from a non-active power state to the active power state.

Devices report the maximum packet size for each endpoint in its endpoint descriptor. The size indicates data payload length only and does not include any of the overhead for link and protocol level. Bandwidth allocation for SuperSpeed is similar to USB 2.0.

### 4.4.1 Data Bursting

Data Bursting enhances efficiency by eliminating the wait time for acknowledgements on a per data packet basis. Each endpoint on an Enhanced SuperSpeed device indicates the number of packets that it can send/receive (called the maximum data burst size) before it has to wait for an explicit handshake. Maximum data burst size is an individual endpoint capability; a host determines an endpoint's maximum data burst size from the SuperSpeed Endpoint Companion descriptor associated with this endpoint (refer to Section 9.6.7).

The host may dynamically change the burst size on a per-transaction basis up to the configured maximum burst size. Examples of when a host may use different burst sizes include, but are not limited to, a fairness policy on the host and retries for an interrupt stream. When the endpoint is an OUT, the host can easily control the burst size (the receiver must always be able to manage a transaction burst size). When the endpoint is an IN, the host can limit the burst size for the endpoint on a per-transaction basis via a field in the acknowledgement packet sent to the device.

### 4.4.2 IN Transfers

The host and device shall adhere to the constraints of the transfer type and endpoint characteristics.

A host initiates a transfer by sending an acknowledgement packet (IN) to the device. This acknowledgement packet contains the addressing information required to route the packet to the intended endpoint. The host tells the device the number of data packets it can send and the sequence number of the first data packet expected from the device. In response the endpoint will transmit data packet(s) with the appropriate sequence numbers back to the host. The acknowledgement packet also implicitly acknowledges the previous data packet that was received successfully.

4-5

Universal Serial Bus 3.1 Specification, Revision 1.0

Note that even though the host is required to send an acknowledgement packet for every data packet received, the device can send up to the number of data packets requested without waiting for any acknowledgement packet.

The Enhanced SuperSpeed IN transaction protocol is illustrated in Figure 4-1. An IN transfer on the Enhanced SuperSpeed bus consists of one, or more, IN transactions consisting of one, or more, packets and completes when any one of the following conditions occurs:

- All the data for the transfer is successfully received.
- The endpoint responds with a packet that is less than the endpoint's maximum packet size.
- The endpoint responds with an error.

![img-9.jpeg](img-9.jpeg)

Figure 4-1. Enhanced SuperSpeed IN Transaction Protocol

### 4.4.3 OUT Transfers

The host and device shall adhere to the constraints of the transfer type and endpoint characteristics.

A host initiates a transfer by sending a burst of data packets to the device. Each data packet contains the addressing information required to route the packet to the intended endpoint. It also includes the sequence number of the data packet. For a non-isochronous transaction, the device returns an acknowledgement packet including the sequence number for the next data packet and implicitly acknowledging the current data packet.

Note that even though the device is required to send an acknowledgement packet for every data packet received, the host can send up to the maximum burst size number of data packets to the device without waiting for an acknowledgement.

4-6

USB 3.1 Enhanced SuperSpeed Data Flow Model

The Enhanced SuperSpeed OUT transaction protocol is illustrated in Figure 4-2. An OUT transfer on the Enhanced SuperSpeed bus consists of one, or more, OUT transactions consisting of one, or more, packets and completes when any one of the following conditions occurs:

- All the data for the transfer is successfully transmitted.
- The host sends a packet that is less than the endpoints maximum packet size.
- The endpoint responds with an error.

![img-10.jpeg](img-10.jpeg)

Figure 4-2. Enhanced SuperSpeed OUT Transaction Protocol

### 4.4.4 Power Management and Performance

The use of inactivity timers and device-driven link power management provides the ability for very aggressive power management. When the host sends a packet to a device behind a hub with a port whose link is in a non-active state, the packet will not be able to traverse the link until it returns to the active state. In the case of an IN transaction on a SuperSpeed bus instance, the host will not be able to start another IN transaction on that SuperSpeed bus instance until the current one completes. The effect of this behavior could have a significant impact on overall performance.

To balance power management with good performance, the concept of a deferral (to both INs and OUTs) is used. When a host initiates a transaction that encounters a link in a non-active state, a deferred response is sent by the hub to tell the host that this particular path is in a reduced power managed state and that the host should go on to schedule other transactions. In addition, the hub sends a deferred request to the device to notify it that a transaction was attempted. This mechanism informs the host of added latency due to power management and allows the host to mitigate performance impacts that result from the link power management.

4-7

Universal Serial Bus 3.1 Specification, Revision 1.0

### 4.4.5 Control Transfers

The purpose and characteristics of Control Transfers are identical to those defined in Section 5.5 of the Universal Serial Bus Specification, Revision 2.0. The Protocol Layer chapter of this specification describes the details of the packets, bus transactions, and transaction sequences used to accomplish Control transfers. The Device Framework chapter of this specification defines the complete set of standard command codes used for devices.

Each device is required to implement the default control pipe as a message pipe. This pipe is intended for device initialization and management. This pipe is used to access device descriptors and to make requests of the device to manipulate its behavior (at a device-level). Control transfers must adhere to the same request definitions described in the Universal Serial Bus Specification, Revision 2.0.

The EnhancedSuperSpeed system will make a “best effort” to support delivery of control transfers between the host and devices. As with USB 2.0, a function and its client software cannot request specific bandwidth for control transfers.

#### 4.4.5.1 Control Transfer Packet Size

Control endpoints have a fixed maximum control transfer data payload size of 512 bytes and have a maximum burst size of one. These maximums apply to all data transactions during the data stage of the control transfer. Refer to Section 8.12.2 for detailed information on the Setup and Status stages of an Enhanced SuperSpeed control transfer.

An Enhanced SuperSpeed device must report a value of 09H in the bMaxPacketSize field of its Device Descriptor. The rule for decoding the default maximum packet size for the Default Control Pipe is given in Section 9.6.1. The Default Control Pipe must support a maximum sequence value of 32 (i.e., sequence values in the range [0-31] are used).

The requirements for data delivery and completion of device-to-host and host-to-device Data stages are generally not changed between USB 2.0 and the Enhanced SuperSpeed bus (refer to Section 5.5.3 of the Universal Serial Bus Specification, Revision 2.0).

#### 4.4.5.2 Control Transfer Bandwidth Requirements

A device has no way to indicate the desired bandwidth for a control pipe. A host balances the bus access requirements of all control pipes and pending transactions on those pipes to provide a “best effort” delivery between client software and functions on the device. This policy is the same as the USB 2.0 policy.

The Enhanced SuperSpeed bus requires that bus bandwidth be reserved to be available for use by control transfers as follows:

- The transactions of a control transfer may be scheduled coincident with transactions for other function endpoints of any defined transfer type.
- Retries of control transfers are not given priority over other best effort transactions.
- If there are control and bulk transfers pending for multiple endpoints, control transfers for different endpoints are selected for service according to a fair access policy that is host controller implementation-dependent.
- When a control endpoint delivers a flow control event (as defined in Section 8.10.1), the host will remove the endpoint from the actively scheduled endpoints. The host will resume the transfer to the endpoint upon receipt of a ready notification from the device.

4-8

USB 3.1 Enhanced SuperSpeed Data Flow Model

These requirements allow control transfers between a host and devices to regularly move data across the Enhanced SuperSpeed bus with “best effort.” System software’s discretionary behavior defined in Section 5.5.4 of the Universal Serial Bus Specification, Revision 2.0 applies equally to Enhanced SuperSpeed control transfers.

### 4.4.5.3 Control Transfer Data Sequences

The Enhanced SuperSpeed protocol preserves the message format and general stage sequencing of control transfers defined in Section 5.5.5 of the Universal Serial Bus Specification, Revision 2.0. The Enhanced SuperSpeed protocol defines some changes to the Setup and Status stages of a control transfer. However, all of the sequencing requirements for normal and error recovery scenarios defined in Section 5.5.5 of the Universal Serial Bus Specification, Revision 2.0 directly map to the SuperSpeed Protocol.

### 4.4.6 Bulk Transfers

The purpose and characteristics of Bulk Transfers are similar to those defined in Section 5.8 of the Universal Serial Bus Specification, Revision 2.0. Section 8.12.1 of this specification describes the details of the packets, bus transactions and transaction sequences used to accomplish Bulk transfers. The Bulk transfer type is intended to support devices that want to communicate relatively large amounts of data at highly variable times where the transfer can use any available Enhanced SuperSpeed bandwidth. An Enhanced SuperSpeed Bulk function endpoint provides the following:

- Access to the Enhanced SuperSpeed bus on a bandwidth available basis
- Guaranteed delivery of data, but no guarantee of bandwidth or latency

The Enhanced SuperSpeed bus retains the following characteristics of bulk pipes:

- No data content structure is imposed on the communication flow for bulk pipes.
- A bulk pipe is a stream pipe and, therefore, always has communication flow either into or out of the host for any pipe instance. If an application requires a bi-directional bulk communication flow, two bulk pipes must be used (one IN and one OUT).

Standard USB bulk pipes provide the ability to move a stream of data. The Enhanced SuperSpeed bus adds the concept of Streams that provide protocol-level support for a multi-stream model.

### 4.4.6.1 Bulk Transfer Data Packet Size

An endpoint for bulk transfers shall set the maximum data packet payload size in its endpoint descriptor to 1024 bytes. It also specifies the burst size that the endpoint can accept from or transmit on the Enhanced SuperSpeed bus. The allowable burst size for a bulk endpoint shall be in the range of 1 to 16. All Enhanced SuperSpeed bulk endpoints shall support sequence values in the range [0-31].

A host is required to support any Enhanced SuperSpeed bulk endpoint. A host shall support all bulk burst sizes. The host ensures that no data payload of any data packet in a burst transaction will be sent to the endpoint that is larger than the maximum packet size. Additionally, it shall not send more data packets than the reported maximum burst size.

A bulk function endpoint must always transmit data payloads with data fields less than, or equal to, 1024 bytes. If the bulk transfer has more data than that, all data payloads in the burst transaction are required to be 1024 bytes in length except for the last data payload in the burst, which may contain the remaining data. A bulk transfer may span multiple bus transactions. A bulk transfer is complete when the endpoint does one of the following:

4-9

Universal Serial Bus 3.1 Specification, Revision 1.0

- Has transferred exactly the amount of data expected.
- Transfers a data packet with a payload less than 1024 bytes.
- Responds with a STALL handshake.

#### 4.4.6.2 Bulk Transfer Bandwidth Requirements

As with USB 2.0 a bulk function endpoint has no way to indicate a desired bandwidth for a bulk pipe. Bulk transactions occur on the Enhanced SuperSpeed bus only on a bandwidth available basis. The Enhanced SuperSpeed host provides a “good effort” delivery of bulk data between client software and device functions. Moving control transfers over the Enhanced SuperSpeed bus has priority over moving bulk transactions. When there are bulk transfers pending for multiple endpoints, the host will provide transaction opportunities to individual endpoints according to a fair access policy, which is host implementation dependent.

All bulk transfers pending in a system contend for the same available bus time. An endpoint and its client software cannot assume a specific rate of service for bulk transfers. Bus time made available to a software client and its endpoint can be changed as other devices are inserted into and removed from the system or as bulk transfers are requested for other function endpoints. Client software cannot assume ordering between bulk and control transfers; i.e., in some situations, bulk transfers can be delivered ahead of control transfers.

The host can use any burst size between 1 and the reported maximum in transactions with a bulk endpoint to more effectively utilize the available bandwidth. For example, there may be more bulk transfers than bandwidth available, so a host can employ a policy of using smaller data bursts per transactions to provide fair service to all pending bulk data streams.

When a bulk endpoint delivers a flow control event (as defined in Section 8.10.1), the host will remove it from the actively scheduled endpoints. The host will resume the transfer to the endpoint upon receipt of a ready notification from the device.

#### 4.4.6.3 Bulk Transfer Data Sequences

Bulk transactions use the standard burst sequence for reliable data delivery defined in Section 8.10.2. Bulk endpoints are initialized to the initial transmit or receive sequence number and burst size (refer to Section 8.12.1.2 and Section 8.12.1.3) by an appropriate control transfer (SetConfiguration, SetInterface, ClearEndpointFeature). Likewise, a host assumes the initial transmit or receive sequence number and burst size for bulk pipes after it has successfully completed the appropriate control transfer as mentioned above.

Halt conditions for an Enhanced SuperSpeed bulk pipe have the identical side effects as defined for a USB 2.0 bulk endpoint. Recovery from halt conditions are also identical to USB 2.0 (refer to Section 5.8.5 of the Universal Serial Bus Specification, Revision 2.0). A bulk pipe halt condition includes a STALL handshake response to a transaction or exhaustion of the host’s transaction retry policy due to transmission errors.

#### 4.4.6.4 Bulk Streams

A standard USB Bulk Pipe represents the ability to move single stream of (FIFO) data between the host and a device via a host memory buffer and a device endpoint. Enhanced SuperSpeed streams provide protocol-level support for a multi-stream model and utilize the “stream” pipe communications mode (refer to Section 5.3.2 of the Universal Serial Bus Specification, Revision 2.0).

4-10

USB 3.1 Enhanced SuperSpeed Data Flow Model

Streams are managed between the host and a device using the Stream Protocol. Each Stream is assigned a Stream ID (SID).

The Stream Protocol defines a handshake, which allows the device or host to establish the Current Stream (CStream) ID associated with an endpoint. The host uses the CStream ID to select the command or operation-specific Endpoint Buffer(s) that will be used for subsequent data transfers on the pipe (see Figure 4-3). The device uses the CStream ID to select the Function Data buffer(s) that will be used.

![img-11.jpeg](img-11.jpeg)

Figure 4-3. Enhanced SuperSpeed IN Stream Example

The example in Figure 4-3 represents an IN Bulk pipe, where a large number of Streams have been established. Associated with each Stream in host memory is one or more Endpoint Buffers to receive the Stream data. In the device, there is a corresponding command or operation-specific Function Data to be transmitted to the host.

When the device has data available for a specific Stream (G in this example), it issues an ERDY tagged with the CStream ID, and the host will begin issuing IN ACK TP's to the device that is tagged with the CStream ID. The device will respond by returning DPs that contain the Function Data associated with the CStream ID that is also tagged with the CStream ID. When the host receives the data, it uses the CStream ID to select the set of Endpoint Buffers that will receive the data.

When the Function Data is exhausted, the device terminates the Stream (refer to Section 8.12.1.4). The host is also allowed to terminate the Stream if it runs out of Endpoint Buffer space.

Streams may be used, for example, to support out-of-order data transfers required for mass storage device command queuing.

A standard bulk endpoint has a single set of Endpoint Buffers associated with it. Streams extend the number of host buffers accessible by an endpoint from 1 to up to 65533. There is a 1:1 mapping between a host buffer and a Stream ID.

Device Class defined methods are used for coordinating the Stream IDs that are used by the host to select Endpoint Buffers and the device to select Function Data associated with a particular Stream. Typically this is done via an out-of-band mechanism (e.g., another endpoint) that is used to pass the list of valid Stream IDs between the host and the device.

The selection of the Current Stream may be initiated by the host or the device and, in either case, the Stream Protocol provides a method for a selection to be rejected. For example, the host may reject a Stream selection initiated by the device if it has no Endpoint Buffers available for it. Or the

4-11

Universal Serial Bus 3.1 Specification, Revision 1.0

device may reject a Stream selection initiated by the host if it has no Function Data available for it. The Device Class defines when a stream may be selected by the host or the device, and the actions that will be taken when a Stream is rejected (refer to Section 8.12.1.4).

A combination of vendor and Device Class defined algorithms determine how Streams are scheduled by a device. The Stream protocol provides methods for starting, stopping, and switching Streams (refer to Section 8.12.1.4).

Mechanisms defined by the Stream protocol allow the device or the host to flow control a Stream. These mechanisms overlap with the standard bulk flow control mechanism.

The host also may start or stop a Stream. For instance, the host will stop a Stream if it runs out of buffer space for the Stream. When the host controller informs the device of this condition, the device may switch to another Stream or wait and continue the same Stream when the host receives more buffers.

The Stream Protocol also provides a mechanism which allows the host to asynchronously inform the device when Endpoint Buffers have been added to the pipe. This is useful in cases in which the host must terminate a stream because it ran out of Endpoint Buffers; however, the device still has more Function Data to transfer. Without this mechanism, the device would have to periodically retry starting the Stream (impacting power management), or a long latency out-of-band method would be required.

Since Streams are run over a standard bulk pipe, an error will halt the pipe, stopping all stream activity. Removal of the halt condition is achieved via software intervention through a separate control pipe as it is for a standard bulk pipe.

Finally, Streams significantly increase the functionality of a bulk endpoint, while having a minimal impact on the additional hardware required to support the feature in hosts and devices.

### 4.4.7 Interrupt Transfers

The purpose and characteristics of interrupt transfers are similar to those defined in USB 2.0 (see Section 5.7 of the Universal Serial Bus Specification, Revision 2.0). The Enhanced SuperSpeed interrupt transfer types are intended to support devices that require a high reliability method to communicate a small amount of data with a bounded service interval. The Protocol Layer chapter of this specification describes the details of the packets, bus transactions and transaction sequences used to accomplish Interrupt transfers. The Enhanced SuperSpeed Interrupt transfer type nominally provides the following:

- Guaranteed maximum service interval
- Guaranteed retry of transfer attempts in the next service interval

Interrupt transfers are attempted each service interval for an interrupt endpoint. Bandwidth is reserved to guarantee a transfer attempt each service interval. Once a transfer is successful, another transfer attempt is not made until the next service interval. If the endpoint responds with a not ready notification, or an acknowledgement indicating that it cannot accept any more packets, the host will not attempt another transfer to that endpoint until it receives a ready notification. The host must then service the endpoint within the larger of (a) twice the service interval, and (b) the device's last reported BELT, after receipt of the ready notification. The requested service interval for the endpoint is described in its endpoint descriptor.

The Enhanced SuperSpeed architecture retains the following characteristics of interrupt pipes:

- No data content structure is imposed on communication flow for interrupt pipes

4-12

USB 3.1 Enhanced SuperSpeed Data Flow Model

- An interrupt pipe is a stream pipe and, therefore, is always unidirectional

### 4.4.7.1 Interrupt Transfer Packet Size

An endpoint for interrupt transfers specifies the maximum data packet payload size that it can accept from or transmit on the SuperSpeed bus. The only allowable maximum data payload size for interrupt endpoints is 1024 bytes for interrupt endpoints that support a burst size greater than one and can be any size from 1 to 1024 for an interrupt endpoint with a burst size equal to one. The maximum allowable burst size for interrupt endpoints is three. All Enhanced SuperSpeed interrupt endpoints shall support sequence values in the range [0-31].

Enhanced SuperSpeed interrupt endpoints are only intended for moving small amounts of data with a bounded service interval. The Enhanced SuperSpeed protocol does not require the interrupt transactions to be maximum size.

A host is required to support Enhanced SuperSpeed interrupt endpoints. A host shall support all allowed combinations of interrupt packet sizes and burst sizes. The host ensures that no data payload of any data packet in a burst transaction shall be sent to the endpoint that is larger than the endpoint's maximum packet size. Also, the host shall not send more data packets in a burst transaction than the endpoint's maximum burst size.

An interrupt endpoint shall always transmit data payloads with data fields less than, or equal to, the endpoint's maximum packet size. If the interrupt transfer has more information than will fit into the maximum packet size for the endpoint, all data payloads in the burst transaction are required to be maximum packet size except for the last data payload in the burst transaction, which may contain the remaining data. An interrupt transfer may span multiple burst transactions.

An interrupt transfer is complete when the endpoint does one of the following:

- Has transferred exactly the amount of data expected
- Transfers a data packet with a payload less than the maximum packet size
- Responds with a STALL handshake

### 4.4.7.2 Interrupt Transfer Bandwidth Requirements

Periodic endpoints may be allocated up to 90% of the total available bandwidth on an Enhanced SuperSpeed bus.

An endpoint for an interrupt pipe specifies its desired service interval bound via its endpoint descriptor. An interrupt endpoint can specify a desired period 2^(bInterval-1) x 125 μs, where bInterval is in the range 1 up to (and including) 16. The USB System Software will use this information during configuration to determine a period that can be sustained. The period provided by the system may be shorter than that desired by the device up to the shortest period defined by the Enhanced SuperSpeed architecture (125 μs which is also referred to as a bus interval). Note that errors on the bus can prevent an interrupt transaction from being successfully delivered over the bus and consequently exceed the desired period.

An Enhanced SuperSpeed interrupt endpoint can move up to three maximum sized packets (3 x 1024 bytes) per service interval. Interrupt transfers are moved over the USB by accessing an interrupt endpoint every service interval. For interrupt endpoints, the host has no way to determine whether the endpoint will source/sync data without accessing the endpoint and requesting an interrupt transfer. If an interrupt IN endpoint has no interrupt data to transmit, or an interrupt OUT endpoint has insufficient buffer to accept data when accessed by the host, it responds with a flow control response.

4-13

Universal Serial Bus 3.1 Specification, Revision 1.0

An endpoint should only provide interrupt data when it has interrupt data pending to avoid having a software client erroneously notified of a transfer completion. A zero-length data payload is a valid transfer and may be useful for some implementations. The host may access an endpoint at any point during the service interval. The interrupt endpoint should not assume a fixed spacing between transaction attempts. The interrupt endpoint can assume only that it will receive a transaction attempt within the service interval bound. Errors can prevent the successful exchange of data within the service interval bound and a host is not required to retry the transaction in the same service interval and is only required to retry the transaction in the next service interval.

#### 4.4.7.3 Interrupt Transfer Data Sequences

Interrupt transactions use the standard burst sequence for reliable data delivery protocol defined in Section 8.10.2. Interrupt endpoints are initialized to the initial transmit, or receive, sequence number and burst size (refer to Section 8.12.4.1 and Section 8.12.4.2) by an appropriate control transfer (SetConfiguration, SetInterface, ClearEndpointFeature). A host sets the initial transmit or receive sequence number and burst size for interrupt pipes after it has successfully completed the appropriate control transfer.

Halt conditions for a SuperSpeed interrupt pipe have the identical side effects as defined for a USB 2.0 interrupt endpoint. Recovery from halt conditions are also identical to the USB 2.0, refer to Section 5.7.5 in the *Universal Serial Bus Specification, Revision 2.0*. An interrupt pipe halt condition includes a STALL handshake response to a transaction, or exhaustion, of the host's transaction retry policy due to transmission errors.

#### 4.4.8 Isochronous Transfers

The purpose of Enhanced SuperSpeed isochronous transfers is similar to those defined in USB 2.0 (refer to Section 5.6 of the *Universal Serial Bus Specification, Revision 2.0*). As in USB 2.0, the Enhanced SuperSpeed isochronous transfer type is intended to support streams that want to perform error tolerant, periodic transfers within a bounded service interval. The Enhanced SuperSpeed bus does not transmit start of frames as on USB 2.0. Timing information is transmitted to devices using Isochronous Timestamp Packets (ITPs). The Protocol Layer chapter of this specification describes the details of the packets, bus transactions, and transaction sequences used to accomplish isochronous transfers. It also describes how the timing information is conveyed to devices.

The Enhanced SuperSpeed isochronous transfer type provides the following:

- Guaranteed bandwidth for transaction attempts on the Enhanced SuperSpeed bus with bounded latency
- Guaranteed data rate through the pipe as long as data is provided to the pipe

Isochronous transactions are attempted each service interval for an isochronous endpoint. Isochronous endpoints that are admitted on the Enhanced SuperSpeed bus are guaranteed the bandwidth they require on the bus. The host can request data from the device, or send data to the device, at any time during the service interval for a particular endpoint on that device. The requested service interval for the endpoint is described in its endpoint descriptor. The Enhanced SuperSpeed isochronous transfer type is designed to support a source and sink that produce and consume data at the same average rate.

An Enhanced SuperSpeed isochronous pipe is a stream pipe and is always unidirectional. The endpoint description identifies whether a given isochronous pipe's communication flow is into or

4-14

USB 3.1 Enhanced SuperSpeed Data Flow Model

out of the host. If a device requires bi-directional isochronous communication flows, two isochronous pipes must be used, one in each direction.

Enhanced SuperSpeed power management may interfere with isochronous transfers whenever an isochronous transfer needs to traverse a non-active link. The resultant delay could result in the data not arriving within the service interval. To overcome this, the Enhanced SuperSpeed protocol defines a PING and PING_RESPONSE mechanism (refer to Section 8.5.7). Before initiating an isochronous transfer the host shall send a PING packet to the device. The device responds with a PING_RESPONSE packet that tells the host that all the links in the path to the device are in the active state.

### 4.4.8.1 Isochronous Transfer Packet Size

An endpoint for isochronous transfers specifies the maximum data packet payload size that the endpoint can accept from or transmit on SuperSpeed. The only allowable maximum data payload size for isochronous endpoints is 1024 bytes for isochronous endpoints that support a burst size greater than one and can be any size from 0 to 1024 for an isochronous endpoint with a burst size equal to one. The maximum allowable burst size for isochronous endpoints is 16. However an isochronous endpoint can request up to six burst transactions in the same service interval.

The Enhanced SuperSpeed protocol does not require the isochronous data packets to be maximum size. If an amount of data less than the maximum packet size is being transferred, the data packet shall not be padded.

A host shall support Enhanced SuperSpeed isochronous endpoints for all allowed combinations of isochronous packet sizes and burst sizes. The host shall ensure that no data payload of any data packet in a burst transaction be sent to the endpoint that is larger than the reported maximum packet size. Also, the host shall not send more data packets in a burst transaction than the endpoint's maximum burst size.

An isochronous endpoint shall always transmit data payloads with data fields less than, or equal to, the endpoint's maximum packet size. If the isochronous transfer has more information than will fit into the maximum packet size for the endpoint, all data payloads in the burst transaction are required to be maximum packet size except for the last data payload in the burst transaction, which may contain the remaining data. An isochronous transfer may span multiple burst transactions.

### 4.4.8.2 Isochronous Transfer Bandwidth Requirements

Periodic endpoints can be allocated up to 90% of the total available bandwidth on the Enhanced SuperSpeed bus.

An endpoint for an isochronous pipe specifies its desired service interval bound via its endpoint descriptor. An isochronous endpoint can specify a desired period 2^(bInterval-1) x 125 μs, where bInterval is in the range 1 to 16. The system software will use this information during configuration to determine whether the endpoint can be added to the host schedule. Note that errors on the bus can prevent an isochronous transaction from being successfully delivered over the bus.

A SuperSpeed isochronous endpoint can move up to three burst transactions of up to 16 maximum sized packets (3 x 16 x 1024 bytes) per service interval. A SuperSpeedPlus isochronous endpoint can move up to six burst transactions of up to 16 maximum sized packets (6 x 16 x 1024 bytes) per service interval. Isochronous transfers are moved over the USB by accessing an isochronous endpoint every service interval. The host will send data to, or request data from, the endpoint every

4-15

Universal Serial Bus 3.1 Specification, Revision 1.0

service interval. Note, if an endpoint has no isochronous data to transmit when accessed by the host, it shall send a zero length packet in response to the request for data.

The host may access an endpoint at any point during the appropriate service interval. The isochronous endpoint should not assume a fixed spacing between transaction attempts. The isochronous endpoint can assume only that it will receive a transaction attempt within the service interval bound. Errors may prevent the successful exchange of data within the service interval bound; however, since the packets in an isochronous transaction are not acknowledged, a host/device has no way of knowing which packets were not received successfully and hence will not retry packets.

### 4.4.8.3 Isochronous Transfer Data Sequences

Isochronous endpoints always transmit data packets starting with sequence number zero in each service interval. Each successive data packet transmitted in the same service interval is sent with the next higher sequence number. The sequence number shall roll over from thirty one to zero when transmitting the thirty second packet. Isochronous endpoints do not support retries and cannot respond with flow control responses.

### 4.4.8.4 Special Considerations for Isochronous Transfers

For a general overview of isochronous data movements over USB, USB clock model, clock synchronization, and the different types of USB-defined synchronization types and their specific requirements, refer to the USB 2.0 Specification, Section 5.12. The following section presents the information necessary to implement Enhanced SuperSpeed isochronous endpoints that need an explicit feedback isochronous endpoint.

#### 4.4.8.4.1 Explicit Feedback

An Enhanced SuperSpeed asynchronous isochronous sink endpoint must provide explicit feedback to the host by indicating accurately what its desired data rate ($F_f$) is, relative to the USB bus interval frequency. This allows the host to continuously adjust the number of samples sent to the sink so that neither underflow, nor overflow, of the data buffer occurs. Likewise, an Enhanced SuperSpeed adaptive source endpoint must receive explicit feedback from the host so that it can accurately generate the number of samples required by the host. Feedback endpoints can be specified as described in Section 9.6.6 for the bmAttributes field of the endpoint descriptor.

To generate the desired data rate $F_f$, the device must measure its actual sampling rate $F_s$, referenced to the USB notion of time, i.e., the USB bus interval frequency. This specification requires the data rate $F_f$ to be resolved to better than one sample per second (1 Hz) in order to allow a high-quality source rate to be created and to tolerate delays and errors in the feedback loop. To achieve this accuracy, the measurement time $T_{meas}$ must be at least 1 second. Therefore:

$$T_{meas} = 2^K$$

where $T_{meas}$ is now expressed in USB bus intervals and $K \ge 13$ for Enhanced SuperSpeed devices (125 $\mu$s bus intervals). However, in most devices, the actual sampling rate $F_s$ is derived from a master clock $F_m$ through a binary divider. Therefore:

$$F_m = F_s * 2^P$$

where $P$ is a positive integer (including 0 if no higher-frequency master clock is available). The measurement time $T_{meas}$ can now be decreased by measuring $F_m$ instead of $F_s$ and:

4-16

USB 3.1 Enhanced SuperSpeed Data Flow Model

$$T_{meas} = \frac{2^K}{2^P} = 2^{(K-P)}$$

In this way, a new estimate for $F_f$ becomes available every $2^{(K-P)}$ bus intervals. $P$ is practically bound to be in the range [0,K] because there is no point in using a clock slower than $F_s$ ($P$=0), and no point in trying to update $F_f$ more than once per bus interval ($P$=K). A sink can determine $F_f$ by counting cycles of the master clock $F_m$ for a period of $2^{(K-P)}$ bus intervals. The counter is read into $F_f$ and reset every $2^{(K-P)}$ bus intervals. As long as no clock cycles are skipped, the count will be accurate over the long term.

Each bus interval, an adaptive source adds $F_f$ to any remaining fractional sample count from the previous bus interval, sources the number of samples in the integer part of the sum, and retains the fractional sample count for the next bus interval. The source can look at the behavior of $F_f$ over many bus intervals to determine an even more accurate rate, if it needs to.

$F_f$ is expressed in number of samples per bus interval. The $F_f$ value consists of an integer part that represents the (integer) number of samples per bus interval and a fractional part that represents the “fraction” of a sample that would be needed to match the sampling frequency $F_s$ to a resolution of 1 Hz or better. The fractional part requires at least K bits to represent the “fraction” of a sample to a resolution of 1 Hz or better. The integer part must have enough bits to represent the maximum number of samples that can ever occur in a single bus interval. Assuming that the minimum sample size is one byte, then this number is currently limited to 48*1024=49152 and 16 bits are needed.

For Enhanced SuperSpeed endpoints, the $F_f$ value shall be encoded in an unsigned 32.K ($K\ge13$) format, encoded into eight bytes (for future extensibility). The value shall be aligned into these eight bytes so that the binary point is located between the fourth and the fifth byte so that it has a 32.32 format. Only the first K bits behind the binary point are required. The lower 32-K bits may be optionally used to extend the precision of $F_f$, otherwise, they shall be reported as zero.

An endpoint needs to implement only the number of bits that it effectively requires for its maximum $F_f$.

The choice of $P$ is endpoint-specific. Use the following guidelines when choosing $P$:

- $P$ must be in the range [0,K].
- Larger values of $P$ are preferred, because they reduce the size of the frame counter and increase the rate at which $F_f$ is updated. More frequent updates result in a tighter control of the source data rate, which reduces the buffer space required to handle $F_f$ changes.
- $P$ should be less than $K$ so that $F_f$ is averaged across at least two frames in order to reduce SOF jitter effects.
- $P$ should not be zero in order to keep the deviation in the number of samples sourced to less than 1 in the event of a lost $F_f$ value.

Isochronous transfers are used to read $F_f$ from the feedback register. The desired reporting rate for the feedback should be $2^{(K-P)}$ bus intervals. $F_f$ will be reported at most once per update period. There is nothing to be gained by reporting the same $F_f$ value more than once per update period. The endpoint may choose to report $F_f$ only if the updated value has changed from the previous $F_f$ value. If the value has not changed, the endpoint may report the current $F_f$ value or a zero length data payload. It is strongly recommended that an endpoint always report the current $F_f$ value any time it is polled.

It is possible that the source will deliver one too many or one too few samples over a long period due to errors or accumulated inaccuracies in measuring $F_f$. The sink must have sufficient buffer

4-17

Universal Serial Bus 3.1 Specification, Revision 1.0

capability to accommodate this. When the sink recognizes this condition, it should adjust the reported $F_f$ value to correct it. This may also be necessary to compensate for relative clock drifts. The implementation of this correction process is endpoint-specific and is not specified.

### 4.4.9 Device Notifications

Device notifications are a standard method for a device to communicate asynchronous device- and bus-level event information to the host. This feature does not map to the pipe model defined for the standard transfer types. Device notifications are always initiated by a device and the flow of data information is always device to host.

Device notifications are message-oriented data communications that have a specific data format structure as defined in Section 8.5.6. Device notifications do not have any data payload. Devices can send a device notification at any time.

### 4.4.10 Reliability

To ensure reliable operation, several layers of protection are used. This provides reliability for both flow control and data end to end.

### 4.4.10.1 Physical Layer

The Enhanced SuperSpeed physical layer provides bit error rates less than 1 bit in $10^{12}$ bits.

### 4.4.10.2 Link Layer

The Enhanced SuperSpeed link layer has mechanisms that ensure a bit error rate less than 1 bit in $10^{20}$ bits for header packets. The link layer uses a number of techniques including packet framing ordered sets, link level flow control and retries to ensure reliable end-to-end delivery for header packets.

### 4.4.10.3 Protocol Layer

The Enhanced SuperSpeed protocol layer depends on a 32-bit CRC appended to the Data Payload and a timeout coupled with retries to ensure that reliable data is provided to the application.

### 4.4.11 Efficiency

Enhanced SuperSpeed communications efficiency is dependent on a number of factors, including line encoding, packet structure and framing, link level flow control and protocol overhead.

Links that operate at Gen 1 speed (5 Gbps and 8b/10b line encoding) the raw throughput is 500 MBps. Accounting for flow control, packet framing and protocol overheads reduces the effective bandwidth down to 450 MBps or less to be delivered to an application.

Links that operate at Gen 2 speed (10 Gbps and 128b/132b line encoding) the raw throughput is approximately 1.2 GBps. Accounting for flow control, packet framing, and protocol overheads reduces the best case effective bandwidth down to approximately 1.1 GBps or less to be delivered to an application. Also, effective bandwidth of individual endpoint flows can be affected by interaction with other simultaneously active endpoint flows traversing through SuperSpeedPlus hub arbiters.

4-18

# 5 Mechanical

This chapter defines form, fit, and function of the USB 3.1 connectors and cable assemblies. It contains the following:

- Connector mating interfaces
- Cables and cable assemblies
- Electrical requirements
- Mechanical and environmental requirements
- Implementation notes and guidelines

The intention of this chapter is to enable connector, system, and device designers and manufacturers to build, qualify, and use the USB 3.1 connectors, cables, and cable assemblies.

If any part of this chapter conflicts with the USB 2.0 specification, the USB 3.1 specification supersedes the USB 2.0 specification.

With some clearly noted exceptions, USB 3.1 connectors and cable assemblies provide the same functionally as the previously defined USB 3.0 connectors and cables assemblies. The primary differences are that USB 3.1 connectors and cable assemblies are specifically intended to support 10Gbps SuperSpeed USB operation and USB 3.1 connectors and cable assemblies include features and requirements associated with improved EMI/RFI performance. From the perspective of interface mating interoperability, USB 3.0 connectors and cable assemblies are the same as USB 3.1 connectors and cable assemblies therefore, only USB 3.1 is listed for interface interoperability requirements and is inclusive of USB 3.0.

## 5.1 Objective

The mechanical layer specification has been developed with the following objectives:

- Supporting Gen 1 speed (5Gbps) and Gen 2 speed (10Gbps)
- Backward compatible with USB 2.0
- Minimizing connector form factor variations
- Providing the system designer features that allow implementations to comply with EMI and RFI requirements
- Supporting On-The-Go (OTG)
- Supporting compatibility with the Universal Serial Bus Power Delivery Specification
- Low cost

## 5.2 Significant Features

This section identifies the significant features of the USB 3.1 (Enhanced SuperSpeed) connectors and cable assemblies' specification. The purpose of this section is not to present all technical details associated with each major feature, but rather to highlight their existence. Where appropriate, this section references other parts of the document where additional details are found.

5-1

Universal Serial Bus 3.1 Specification, Revision 1.0

## 5.2.1 Connectors

The USB 3.1 specification defines the following connectors:

- Enhanced SuperSpeed Standard-A plug and receptacle
- Enhanced SuperSpeed Standard-B plug and receptacle
- Enhanced SuperSpeed Micro-B plug and receptacle
- Enhanced SuperSpeed Micro-A plug
- Enhanced SuperSpeed Micro-AB receptacle

All SuperSpeed connectors have the same mating interfaces and are compatible with each other. The USB Enhanced SuperSpeed Gen 2 connectors have unique electrical requirements to support the Gen 2 speed in addition to the Gen 1 speed.

Table 5-1 lists the compatible plugs and receptacles.

Table 5-1. Plugs Accepted By Receptacles

[tbl-33.md](tbl-33.md)

### 5.2.1.1 USB 3.1 Standard-A Connector

The USB 3.1 Standard-A connector is defined as the host connector. It has the same mating interface as the USB 2.0 Standard-A connector, but with additional pins for two more differential pairs and a drain. Refer to Section 5.3.1.3 for pin assignments and descriptions.

A USB 3.1 Standard-A receptacle accepts either a USB 3.1 Standard-A plug or a USB 2.0 Standard-A plug. Similarly, a USB 3.1 Standard-A plug may be mated with either a USB 3.1 Standard-A receptacle or a USB 2.0 Standard-A receptacle.

A unique color coding is recommended for the USB 3.1 Standard-A connector plastic housings to help users distinguish the USB 3.1 Standard-A connector from the USB 2.0 Standard-A connector (refer to Section 5.3.1.4 for details).

### 5.2.1.2 USB 3.1 Standard-B Connector

The USB 3.1 Standard-B connector is defined for relatively large, stationary peripherals, such as external hard drives and printers. It is defined so that the USB 3.1 Standard-B receptacle accepts either a USB 3.1 Standard-B plug, or a USB 2.0 Standard-B plug. Inserting a USB 3.1 Standard-B plug into a USB 2.0 Standard-B receptacle is physically disallowed (refer to Section 5.3.2 for details).

5-2

Mechanical

### 5.2.1.3 USB 3.1 Micro-B Connector

The USB 3.1 Micro-B plug and USB 3.1 Micro-B receptacle connectors are defined for small handheld devices and other applications where a small connector size may be used. It is defined so that the USB 3.1 Micro-B receptacle accepts either a USB 3.1 Micro-B plug, or a USB 2.0 Micro-B plug. Inserting a USB 3.1 Micro-B plug into a USB 2.0 Micro-B receptacle or USB 2.0 Micro-AB receptacle is physically disallowed by the implementation.

### 5.2.1.4 USB 3.1 Micro-AB and USB 3.1 Micro-A Connectors

The USB 3.1 Micro-AB receptacle is similar to the USB 3.1 Micro-B receptacle except for different keying. It accepts a USB 3.1 Micro-A plug, a USB 3.1 Micro-B plug, a USB 2.0 Micro-A plug, or a USB 2.0 Micro-B plug. The USB 3.1 Micro-AB receptacle is only allowed on OTG products which may function as either a host or device. All other uses of the USB 3.1 Micro-AB receptacle are prohibited.

The USB 3.1 Micro-A plug is similar to the USB 3.1 Micro-B plug except for different keying and ID pin connections. Similar to the USB 2.0 Micro-A plug, the USB 3.1 Micro-A plug is defined for OTG applications only. Section 5.3.3 defines the USB 3.1 Micro connector family

### 5.2.2 Allowed Cable Assemblies

The USB 3.1 specification defines the following cable assemblies:

- USB 3.1 Standard-A plug to USB 3.1 Standard-B plug
- USB 3.1 Standard-A plug to USB 3.1 Micro-B plug
- USB 3.1 Standard-A plug to USB 3.1 Standard-A plug
- USB 3.1 Micro-A plug to USB 3.1 Micro-B plug
- USB 3.1 Micro-A plug to USB 3.1 Standard-B plug
- Captive cable with USB 3.1 Standard-A plug
- Captive cable with USB 3.1 Micro-A plug

A captive cable is a cable assembly that has a Standard-A plug on one end and that is either hardwired or has a vendor-specific connector on the other end. A hardwired cable is directly wired to the device and it is not detachable from the device. This specification does not define how the vendor-specific connector or hardwired attachment is done on the device side.

For electrical compliance purposes, a USB 3.1 captive cable (hardwired or with vendor-specific connector on the device end) shall be considered part of the USB 3.1 device.

No other types of cable assemblies are allowed by this specification. Section 5.5 provides detailed discussion on USB 3.1 cable assemblies.

### 5.2.3 Raw Cables

Due to EMI, RFI, and signal integrity requirements, each cable differential pair used for the SuperSpeed lines in a USB 3.1 cable assembly shall be shielded; the Unshielded Twisted Pair (UTP) used for USB 2.0 is not allowed for SuperSpeed lines. Section 5.4 defines the cable construction for USB 3.1.

5-3

Universal Serial Bus 3.1 Specification, Revision 1.0

### 5.3 Connector Mating Interfaces

This section defines the connector mating interfaces, including the connector interface drawings, pin assignments, and descriptions.

### 5.3.1 USB 3.1 Standard-A Connector

#### 5.3.1.1 Interface Definition

Figure 5-1 and Figure 5-2 show the USB 3.1 Standard-A receptacle and required ground spring mating areas, respectively. Figure 5-4 shows the Standard-A plug interface dimensions for USB 3.1. Only the dimensions that govern the mating interoperability are specified. All REF dimensions are informative.

The Universal Serial Bus Power Delivery Specification defines the mechanical and electrical requirements for the Insertion Detect feature to support cold socket capability. It may be implemented in a Standard-A receptacle or a PD Standard-A receptacle. Implementation is vendor-specific. The Insertion Detect feature shall be implemented for cold socket Standard-A applications and is optional for all other Standard-A implementations. See the Universal Serial Bus Power Delivery Specification for complete Insertion Detect requirements. Example connector configurations including Insertion Detect features are shown in Figure 5-3.

Although the USB 3.1 Standard-A connector has basically the same form factor as the USB 2.0 Standard-A connector, it has significant differences inside. Below are the key features and design areas that need attention:

- In addition to the Vbus, D-, D+, and GND pins that are required for USB 2.0, the USB 3.1 Standard-A connector includes five more pins: two differential signal pairs plus one ground (GND_DRAIN). The two added differential signal pairs are for SuperSpeed data transfer, supporting dual simplex SuperSpeed signaling. The added GND_DRAIN pin is for drain wire termination and managing EMI, RFI, and signal integrity.
- The contact areas of the five SuperSpeed pins are located towards the front of the receptacle as blades, while the four USB 2.0 pins towards the back of the receptacle as beams or springs. Accordingly, in the plug, the SuperSpeed contacts are beams located behind the USB 2.0 blades. In other words, the USB 3.1 Standard-A connector has a two-tier contact system.
- The tiered-contact approach within the Standard-A connector form factor results in less contact area as compared to the USB 2.0 Standard-A connector. The connector interface dimensions take into consideration contact mating requirements between the USB 3.1 Standard-A receptacle and USB 3.1 Standard-A plug, the USB 3.1 Standard-A receptacle and USB 2.0 Standard-A plugs, and the USB 2.0 Standard-A receptacles and USB 3.1 Standard-A plug.
- The connector interface definition avoids shorting between the SuperSpeed and USB 2.0 pins during insertion when plugging a USB 2.0 Standard-A plug into a USB 3.1 Standard-A receptacle or a USB 3.1 Standard-A plug into a USB 2.0 Standard-A receptacle.
- There may be some increase in the USB 3.1 Standard-A receptacle connector depth (into a system board) to support the two-tiered-contacts as compared to the USB 2.0 Standard-A receptacle.
- Drawings for stacked USB 3.1 Standard-A receptacles are not shown in this specification. They are allowed as long as they meet all the electrical and mechanical requirements defined in this specification. When designing a stacked USB 3.1 Standard-A receptacle, efforts need to be

5-4

Mechanical

made to minimize impedance discontinuity of the top connector in the stack because of its long electrical path. Attention to the high speed electrical design of USB 3.1 Standard-A connectors is required. In addition to minimizing the connector impedance discontinuities, crosstalk between the SuperSpeed differential signal pairs and USB 2.0 D+/D- pair should also be minimized.

- The receptacle connector should have a back-shield to ensure that the receptacle connector is fully enclosed. The USB 3.1 receptacle should also make good contact to the PCB ground by providing sufficient number of ground tabs to ensure a low impedance path to PCB ground. The USB 3.1 receptacle connector should have a robust mating interface to the shield of the USB 3.1 plug when it is inserted. Previous versions of this specification required providing a grounding spring tab in the middle of the side closest to the USB SuperSpeed signal contacts and grounding springs on both sides of the shell for USB 3.0 Standard-A receptacles. New designs shall have three grounding spring tabs on the side closest to the USB SuperSpeed signal contacts, two grounding spring tabs on the side opposite the USB SuperSpeed signal contacts, and a grounding spring on both sides of the shell of the USB 3.1 Standard-A receptacle. See Figure 5-2.

![img-12.jpeg](img-12.jpeg)

Continued on next page

5-5

Universal Serial Bus 3.1 Specification, Revision 1.0

![img-13.jpeg](img-13.jpeg)

![img-14.jpeg](img-14.jpeg)

SECTION J-J

![img-15.jpeg](img-15.jpeg)

![img-16.jpeg](img-16.jpeg)

SECTION S-S

DETAIL Z

Continued on next page

5-6

Mechanical

![img-17.jpeg](img-17.jpeg)

![img-18.jpeg](img-18.jpeg)

Figure 5-1. USB 3.1 Standard-A Receptacle Interface Dimensions

5-7

Universal Serial Bus 3.1 Specification, Revision 1.0

![img-19.jpeg](img-19.jpeg)

TOP VIEW (SIDE NEAREST SUPERSPEED CONTACTS)

USB 3.1 PLUG

![img-20.jpeg](img-20.jpeg)

![img-21.jpeg](img-21.jpeg)

USB 3.1 PD PLUG

![img-22.jpeg](img-22.jpeg)

![img-23.jpeg](img-23.jpeg)

Continued on next page

5-8

Mechanical

![img-24.jpeg](img-24.jpeg)

BOTTOM VIEW (SIDE OPPOSITE SUPERSPEED CONTACTS)

USB 3.1 PLUG

![img-25.jpeg](img-25.jpeg)

USB 3.1 PD PLUG

![img-26.jpeg](img-26.jpeg)

Figure 5-2. Example USB 3.1 Standard-A Receptacle with Grounding Springs and Required contact zones on the Standard-A Plug.

5-9

Universal Serial Bus 3.1 Specification, Revision 1.0

![img-27.jpeg](img-27.jpeg)

Spring fingers on the side of
receptacle shell are EMI functional

![img-28.jpeg](img-28.jpeg)

Figure 5-3. Example USB 3.1 Standard-A Mid-Mount Receptacles with Insertion Detect

5-10

Mechanical

![img-29.jpeg](img-29.jpeg)

![img-30.jpeg](img-30.jpeg)

![img-31.jpeg](img-31.jpeg)

![img-32.jpeg](img-32.jpeg)

SECTION P-P

NOTES:

1) NON-DIMENSIONED GEOMETRY FOR REFERENCE ONLY,
SUBJECT TO CHANGE

2) DRAWING FOR MATING INTERFACE DIMENSIONS ONLY,
VIEWS MAY NOT SHOW REALISTIC MANUFACTURING CONDITION.

Continued on next page

5-11

Universal Serial Bus 3.1 Specification, Revision 1.0

![img-33.jpeg](img-33.jpeg)

![img-34.jpeg](img-34.jpeg)

SECTION P-P

![img-35.jpeg](img-35.jpeg)

SECTION T-T

![img-36.jpeg](img-36.jpeg)

![img-37.jpeg](img-37.jpeg)

SECTION Q-Q

Continued on next page

5-12

Mechanical

![img-38.jpeg](img-38.jpeg)

![img-39.jpeg](img-39.jpeg)

Figure 5-4. USB 3.1 Standard-A Plug Interface Dimensions

### 5.3.1.2 USB 3.1 Standard-A Reference Footprints

This specification does not define standard footprints. Any footprint may be used as long as all mechanical and electrical requirements are met. Example footprints are provided for reference only.

Figure 5-5 shows through-hole example footprints for the USB 3.1 Standard-A receptacle with a back-shield. Pin numbers are marked.

Figure 5-6 shows an example footprint for a mid-mount standard mount (mounted on the top of the PCB) Standard-A receptacle that includes Insertion Detect.

5-13

Universal Serial Bus 3.1 Specification, Revision 1.0

Figure 5-7 shows an example mid-mount reverse mount (mounted on the bottom of the PCB) with Insertion Detect. The reverse mount configuration locates the SuperSpeed signals between the USB 2.0 signals and the PCB edge, making the SuperSpeed signal routing more challenging. See Section 5.6.1.2 for target characteristic impedance.

![img-40.jpeg](img-40.jpeg)

PCB LAYOUT (REF.)
(STANDARD MOUNT TYPE)

Continued on next page

5-14

Mechanical

![img-41.jpeg](img-41.jpeg)

Continued on next page

5-15

Universal Serial Bus 3.1 Specification, Revision 1.0

![img-42.jpeg](img-42.jpeg)

PCB LAYOUT (REF.)
(REVERSE MOUNT TYPE)

Figure 5-5. Example Footprint for the USB 3.1 Standard-A Receptacle - Through-Hole with Back-Shield

5-16

Mechanical

![img-43.jpeg](img-43.jpeg)

![img-44.jpeg](img-44.jpeg)

Figure 5-6. Example Footprint for the USB 3.1 Standard-A Receptacle - Mid-Mount Standard Mount Through-Hole with Insertion Detect

5-17

Universal Serial Bus 3.1 Specification, Revision 1.0

![img-45.jpeg](img-45.jpeg)

![img-46.jpeg](img-46.jpeg)

Figure 5-7. Example Footprint for the USB 3.1 Standard-A Receptacle - Mid-Mount Reverse Mount Through-Hole with Insertion Detect

5-18

Mechanical

### 5.3.1.3 Pin Assignments and Description

The usage and assignments of the nine pins in the USB 3.1 Standard-A connector are defined in Table 5-2.

Table 5-2. USB 3.1 Standard-A Connector Pin Assignments

[tbl-34.md](tbl-34.md)

Note 1: Note 1: Pin numbers not included in this table do not have contacts present.

Note 2: Tx and Rx are defined from the host perspective.

Note 3: The mating sequence assumes support of INSERTION DETECT.

Note 4: Pin 12, if present, shall be connected to Shield.

The physical location of the pins in the connector is illustrated in Figure 5-1 to Figure 5-7. Pins 1 to 4 are referred to as the USB 2.0 pins, while pins 5 to 9 are referred to as the SuperSpeed pins. See the Universal Serial Bus Power Delivery Specification for location of pins 12 and 13.

5-19

Universal Serial Bus 3.1 Specification, Revision 1.0

### 5.3.1.4 USB 3.1 Standard-A Connector Color Coding

Since both the USB 2.0 Standard-A and USB 3.1 Standard-A receptacles may co-exist on a host, color coding is recommended for the USB 3.1 Standard-A connector (receptacle and plug) housings to help users distinguish it from the USB 2.0 Standard-A connector.

Blue (Pantone 300C) is the recommended color for the USB 3.1 Standard-A receptacle and plug plastic housings. When the recommended color is used, connector manufacturers and system integrators should make sure that the blue-colored receptacle housing is visible to users. Figure 5-8 illustrates the color coding recommendation for the USB 3.1 Standard-A connector.

![img-47.jpeg](img-47.jpeg)

Figure 5-8. Illustration of Color Coding Recommendation for USB 3.1 Standard-A Connector

### 5.3.2 USB 3.1 Standard-B Connector

#### 5.3.2.1 Interface Definition

Figure 5-9, Figure 5-10, and Figure 5-11 show the USB Standard-B receptacle dimensions, the USB Standard-B plug dimensions, and a USB Standard-B receptacle reference footprint, respectively. See Section 5.6.1.2 for target characteristic impedance.

5-20

Mechanical

![img-48.jpeg](img-48.jpeg)

SECTION B-B

![img-49.jpeg](img-49.jpeg)

![img-50.jpeg](img-50.jpeg)

![img-51.jpeg](img-51.jpeg)

SECTION A-A

![img-52.jpeg](img-52.jpeg)

SECTION C-C

![img-53.jpeg](img-53.jpeg)

DETAIL A

Continued on next page

5-21

Universal Serial Bus 3.1 Specification, Revision 1.0

![img-54.jpeg](img-54.jpeg)

![img-55.jpeg](img-55.jpeg)

![img-56.jpeg](img-56.jpeg)

NOTES:

1) CRITICAL DIMENSIONS ARE TOLERANCED
AND SHALL NOT BE DEVIATED.

2) GENERAL TOLERANCE IS ±0.10 OTHERWISE
THE SPECIFIED TOLERANCE APPLIES.

3) ALL DIMENSIONS ARE IN MILLIMETERS.
4) DIMENSIONS THAT ARE LABELED REF ARE
TYPICAL DIMENSIONS AND MAY VARY FROM
MANUFACTURER TO MANUFACTURER.

5) NON-DIMENSIONED GEOMETRY FOR REFERENCE
ONLY, SUBJECT TO CHANGE.

Figure 5-9. USB 3.1 Standard-B Receptacle Interface Dimensions

5-22

Mechanical

![img-57.jpeg](img-57.jpeg)

![img-58.jpeg](img-58.jpeg)

![img-59.jpeg](img-59.jpeg)

![img-60.jpeg](img-60.jpeg)

SECTION D-D

SECTION A-A

![img-61.jpeg](img-61.jpeg)

SECTION B-B

![img-62.jpeg](img-62.jpeg)

SECTION C-C

NOTES:

1) CRITICAL DIMENSIONS ARE TOLERANCED AND SHALL NOT BE DEVIATED.
2) GENERAL TOLERANCE IS ±0.10 OTHERWISE THE SPECIFIED TOLERANCE APPLIES.
3) ALL DIMENSIONS ARE IN MILLIMETERS.
4) DIMENSIONS THAT ARE LABELED REF ARE TYPICAL DIMENSIONS AND MAY VARY FROM MANUFACTURER TO MANUFACTURER.
5) NON-DIMENSIONED GEOMETRY FOR REFERENCE ONLY, SUBJECT TO CHANGE.
6) OVERALL CONNECTOR AND CABLE LENGTH IS MEASURED FROM DATUM A OF THE SERIES "B" PLUG TO DATUM A OF THE SERIES "A" PLUG OR BLUNT END TERMINATION.

Figure 5-10. USB 3.1 Standard-B Plug Interface Dimensions

5-23

Universal Serial Bus 3.1 Specification, Revision 1.0

![img-63.jpeg](img-63.jpeg)

REFERENCE PCB LAYOUT

Figure 5-11. Reference Footprint for the USB 3.1 Standard-B Receptacle

The USB 3.1 Standard-B receptacle interfaces have two portions: the USB 2.0 interface and the SuperSpeed interface. The USB 2.0 interface consists of pins 1 to 4, while the SuperSpeed interface consists of pins 5 to 9.

When a USB 2.0 Standard-B plug is inserted into the USB 3.1 Standard-B receptacle, only the USB 2.0 interface is engaged and the link will not take advantage of the Enhanced SuperSpeed capability. Since the USB 3.1 SuperSpeed portion is visibly not mated when a USB 2.0 Standard-B plug is inserted in the USB 3.1 Standard-B receptacle, users have the visual feedback that the cable plug is not matched with the receptacle. Only when a USB 3.1 Standard-B plug is inserted into the USB 3.1 Standard-B receptacle, is the interface completely visibly engaged.

5-24

Mechanical

### 5.3.2.2 Pin Assignments and Description

The usage and assignments of the nine pins in the USB 3.1 Standard-B connector are defined in Table 5-3.

Table 5-3. USB 3.1 Standard-B Connector Pin Assignments

[tbl-35.md](tbl-35.md)

Note: Tx and Rx are defined from the device perspective.

The physical location of the pins in the connector is illustrated in Figure 5-9 to Figure 5-11.

### 5.3.3 USB 3.1 Micro Connector Family

#### 5.3.3.1 Interfaces Definition

The USB 3.1 Micro connector family consists of the USB 3.1 Micro-B receptacle, USB 3.1 Micro-AB receptacle, USB 3.1 Micro-B plug, and USB 3.1 Micro-A plug. Figure 5-12 and Figure 5-13 show the USB 3.1 Micro family receptacle and plug interface dimensions, respectively. Only dimensions that govern the mating interoperability are specified.

The USB 3.1 Micro connector family has the following characteristics:

- The USB 3.1 Micro-B connector may be considered a combination of USB 2.0 Micro-B interface and the USB 3.1 SuperSpeed contacts. The USB 3.1 Micro-B receptacle accepts a USB 2.0 Micro-B plug, maintaining backward compatibility.
- The USB 3.1 Micro-B connector maintains the same connector height and contact pitch as the USB 2.0 Micro-B connector.
- The USB 3.1 Micro-B connector uses the same latch design as the USB 2.0 Micro-B connector.
- The USB 3.1 Micro-AB receptacle is identical to the USB 3.1 Micro-B receptacle except for a keying difference in the connector shell outline.
- The USB 3.1 Micro-A plug is similar to the USB 3.1 Micro-B plug with different keying and ID pin connections. The Universal Serial Bus Power Delivery Specification discusses the ID pin connections.

There is no required footprint for the USB 3.1 Micro connector family. Figure 5-14 shows reference Micro-B and -AB connector footprints.

5-25

Universal Serial Bus 3.1 Specification, Revision 1.0

![img-64.jpeg](img-64.jpeg)

![img-65.jpeg](img-65.jpeg)

![img-66.jpeg](img-66.jpeg)

![img-67.jpeg](img-67.jpeg)

![img-68.jpeg](img-68.jpeg)

![img-69.jpeg](img-69.jpeg)

![img-70.jpeg](img-70.jpeg)

NOTE : General tolerance is +/- 0.05 mm, otherwise the specified tolerances apply.

Continued on next page

5-26

Mechanical

![img-71.jpeg](img-71.jpeg)

Subject to change by individual connector
manufacturer to assure specified performance
and intermateability.

![img-72.jpeg](img-72.jpeg)

![img-73.jpeg](img-73.jpeg)

KEY B
SHIELD DIMENSIONS

![img-74.jpeg](img-74.jpeg)

KEY AB
SHIELD DIMENSIONS

![img-75.jpeg](img-75.jpeg)

NOTE : Chamfer metals are optional with no sharp edges.

Figure 5-12. USB 3.1 Micro-B and -AB Receptacles Interface Dimensions

5-27

Universal Serial Bus 3.1 Specification, Revision 1.0

![img-76.jpeg](img-76.jpeg)

NOTES:

1. Dimensions that are labeled REF may vary from manufacturer to manufacturer.

2. General tolerance is +/-0.05mm, otherwise the specified tolerances apply.

Continued on next page

5-28

Mechanical

![img-77.jpeg](img-77.jpeg)

NOTES:

1. Dimensions that are labeled REF may vary from manufacturer to manufacturer.

2. General tolerance is +/-0.05mm, otherwise the specified tolerances apply.

Continued on next page

5-29

Universal Serial Bus 3.1 Specification, Revision 1.0

![img-78.jpeg](img-78.jpeg)

CONTACT No.2,3,4,6,7,9,10

![img-79.jpeg](img-79.jpeg)

A

CONTACT No.1,5,8

![img-80.jpeg](img-80.jpeg)

Each contact location (off-set value)
by zone 0.15 (+/-0.075)

![img-81.jpeg](img-81.jpeg)

The entry angle of the contact
shall not start above the top surfaces
of the adjacent insulator walls.

![img-82.jpeg](img-82.jpeg)

Subject to change by individual connector
manufacturer to assure specified performance
and intermateability.

Figure 5-13. USB 3.1 Micro-B and Micro-A Plug Interface Dimensions

5-30

Mechanical

![img-83.jpeg](img-83.jpeg)

Standard-Surface Mount-Version Drawing

![img-84.jpeg](img-84.jpeg)

# NOTES :

1. Critical Dimensions are TOLERANCED and shall not be deviated.
2. Dimensions that labeled REF are typical dimensions and may vary from manufacturer to manufacturer.
3. General tolerance is \(+ / - 0.05\mathrm{mm}\) , otherwise the specified tolerances apply.
4. Chamfer metals are optional with no sharp edges.

Continued on next page

5-31

Universal Serial Bus 3.1 Specification, Revision 1.0

![img-85.jpeg](img-85.jpeg)

Standard-Surface Mount-Version Drawing

![img-86.jpeg](img-86.jpeg)

# NOTES :

1. Critical Dimensions are TOLERANCED and shall not be deviated.
2. Dimensions that labeled REF are typical dimensions and may vary from manufacturer to manufacturer.
3. General tolerance is +/- 0.05 mm, otherwise the specified tolerances apply.
4. Chamfer metals are optional with no sharp edges.

Figure 5-14. Reference Footprint for the USB 3.1 Micro-B or Micro-AB Receptacle

5-32

Mechanical

### 5.3.3.2 Pin Assignments and Description

Table 5-4 and Table 5-5 show the pin assignments for the USB 3.1 Micro connector family.

Table 5-4. USB 3.1 Micro-B Connector Pin Assignments

[tbl-36.md](tbl-36.md)

Note: Tx and Rx are defined from the device perspective.

Table 5-5. USB 3.1 Micro-AB/-A Connector Pin Assignments

[tbl-37.md](tbl-37.md)

Note: Tx and Rx are defined when an OTG device serves as a host.

The physical location of the pins in the connector is illustrated in Figure 5-12 to Figure 5-14.

## 5.4 Cable Construction and Wire Assignments

This section discusses the USB 3.1 cables, including cable construction, wire assignments, and wire gauges. The performance requirements are specified in Section 5.6.1.

5-33

Universal Serial Bus 3.1 Specification, Revision 1.0

### 5.4.1 Cable Construction

Figure 5-15 illustrates a USB 3.1 cable cross-section. There are three groups of wires: D+/D-signal pair (typically unshielded twisted pair (UTP)), Enhanced SuperSpeed signal pairs (typically Shielded Differential Pair (SDP), twisted, twinax, or coaxial signal pairs), and power and ground wires.

![img-87.jpeg](img-87.jpeg)

Figure 5-15. Illustration of a USB 3.1 Cable Cross-Section

The D+/D- signal pair is intended to transmit the USB 2.0 signaling while the Enhanced SuperSpeed signal pairs are used for SuperSpeed; the shield is needed for the SuperSpeed differential pairs for signal integrity and EMI performance. Each Enhanced SuperSpeed drain wire is connected to the system ground through the GND_DRAIN pin(s) in the connector.

A metal braid is required to enclose all the wires in the USB 3.1 cable. The braid shall be terminated to the plug metal shells, as close to 360° as possible, to reduce EMI.

5-34

Mechanical

### 5.4.2 Wire Assignments

Table 5-6 defines the wire number, signal assignments of the wires.

Table 5-6. Cable Wire Assignments

[tbl-38.md](tbl-38.md)

### 5.4.3 Wire Gauges and Cable Diameters

This specification does not specify wire gauges. Table 5-7 lists typical wire gauges for reference purposes only. A large gauge wire incurs less loss, but at the cost of cable flexibility. It is recommended to use the smallest possible wire gauges that meet the cable assembly electrical requirements.

To maximize cable flexibility, all wires should be stranded and the cable outer diameter should be minimized as much as possible. A typical non-USB 3.1 Power Delivery capable cable outer diameter may range from 3 mm to 6 mm.

Table 5-7. Reference Wire Gauges

[tbl-39.md](tbl-39.md)

5-35

Universal Serial Bus 3.1 Specification, Revision 1.0

## 5.5 Cable Assemblies

### 5.5.1 USB 3.1 Standard-A to USB 3.1 Standard-B Cable Assembly

Figure 5-16 shows a USB 3.1 Standard-A to USB 3.1 Standard-B cable assembly. Due to increased wire sizes required for some PD cable implementations, the overmold dimensions for PD cables have larger maximum dimensions than the non-PD cables specified. See the *Universal Serial Bus Power Delivery Specification* for the maximum overmold dimensions of PD cable assemblies.

5-36

Mechanical

![img-88.jpeg](img-88.jpeg)

STANDARD "A" PLUG
(ALWAYS UPSTREAM TOWARDS
THE "HOST" SYSTEM)

STANDARD "B" PLUG
(ALWAYS DOWNSTREAM
TOWARDS THE USB DEVICE)

![img-89.jpeg](img-89.jpeg)

![img-90.jpeg](img-90.jpeg)

![img-91.jpeg](img-91.jpeg)

STANDARD "A" PLUG

![img-92.jpeg](img-92.jpeg)

STANDARD "B" PLUG

Figure 5-16. USB 3.1 Standard-A to USB 3.1 Standard-B Cable Assembly

Table 5-8 defines the wire connections for the USB 3.1 Standard-A to USB 3.1 Standard-B cable assembly.

5-37

Universal Serial Bus 3.1 Specification, Revision 1.0

Table 5-8. USB 3.1 Standard-A to USB 3.1 Standard-B Cable Assembly Wiring

[tbl-40.md](tbl-40.md)

### 5.5.2 USB 3.1 Standard-A to USB 3.1 Standard-A Cable Assembly

The USB 3.1 Standard-A to USB 3.1 Standard-A cable assembly is defined for operating system debugging and other host-to-host connection applications. Table 5-9 shows wire connections for such a cable assembly. Refer to Figure 5-16 for the USB 3.1 Standard-A plug cable overmold dimensions.

Table 5-9. USB 3.1 Standard-A to USB 3.1 Standard-A Cable Assembly Wiring

[tbl-41.md](tbl-41.md)

5-38

Mechanical

### 5.5.3 USB 3.1 Standard-A to USB 3.1 Micro-B Cable Assembly

Figure 5-17 shows the USB 3.1 Micro-B plug overmold dimensions for a USB 3.1 Standard-A to USB 3.1 Micro-B cable assembly. The USB 3.1 Standard-A plug overmold dimensions are found in Figure 5-16. Due to increased wire sizes required for some PD cable implementations, the overmold dimensions for PD cables have larger maximum dimensions than the non-PD cables specified. See the *Universal Serial Bus Power Delivery Specification* for the maximum overmold dimensions of PD cable assemblies.

![img-93.jpeg](img-93.jpeg)

Notes:

1. Any surface may have texturing up to 0.3 mm below the surface.

2. A square area around the letter B may be lowered as much as 0.5 mm.

3. USB authorized icon, connector type letter designation (i.e., B), color of the insulator body, and maximum dimensions are mandatory. Overmold outer configuration, color, and final shape are reference.

4. Pin 4 is not connected to pin 5 inside the plug.

Figure 5-17. USB 3.1 Micro-B Plug Cable Overmold Dimensions

5-39

Universal Serial Bus 3.1 Specification, Revision 1.0

Table 5-10 shows the wire connections for the USB 3.1 Standard-A to USB 3.1 Micro-B cable assembly. Note that the ID pin in the USB 3.1 Micro-B plug shall not be connected, but left in the open condition.

Table 5-10. USB 3.1 Standard-A to USB 3.1 Micro-B Cable Assembly Wiring

[tbl-42.md](tbl-42.md)

5-40

Mechanical

### 5.5.4 USB 3.1 Micro-A to USB 3.1 Micro-B Cable Assembly

Figure 5-18 shows the USB 3.1 Micro-A plug cable overmold dimensions in a USB 3.1 Micro-A to USB 3.1 Micro-B cable assembly. The USB 3.1 Micro-B plug cable overmold dimensions are shown in Figure 5-17. Due to increased wire sizes required for some PD cable implementations, the overmold dimensions for PD cables have larger maximum dimensions than the non-PD cables specified. See the Universal Serial Bus Power Delivery Specification for the maximum overmold dimensions of PD cable assemblies.

![img-94.jpeg](img-94.jpeg)

Notes:

1. Any surface may have texturing up to 0.3 mm below the surface.

2. A square area around the letter A may be lowered as much as 0.5 mm.

3. USB authorized icon, connector type letter designation (i.e., A), color of the insulator body, and maximum dimensions are mandatory. Overmold outer configuration, color, and final shape are reference.

4. Pin 4 is connected to pin 5 inside the plug.

Figure 5-18. USB 3.1 Micro-A Cable Overmold Dimensions

5-41

Universal Serial Bus 3.1 Specification, Revision 1.0

Table 5-11 shows the wire connections for the USB 3.1 Micro-A to USB 3.1 Micro-B cable assembly. The ID pin on a USB 3.1 Micro-A plug shall be connected to the GND pin. The ID pin on a USB 3.1 Micro-B plug shall be a no-connect or connected to ground by a resistance of greater than Rb_PLUG_ID (1 MΩ minimum). See the Universal Serial Bus Power Delivery Specification for additional details regarding electrical connections to ID pins. An OTG device is required to be able to detect whether a USB 3.1 Micro-A or USB 3.1 Micro-B plug is inserted by determining if the ID pin resistance to ground is less than Ra_PLUG_ID (10 Ω maximum) or if the resistance to ground is greater than Rb_PLUG_ID. Any ID resistance less than Ra_PLUG_ID shall be treated as ID = FALSE and any resistance greater than Rb_PLUG_ID shall be treated as ID = TRUE.

Table 5-11. USB 3.1 Micro-A to USB 3.1 Micro-B Cable Assembly Wiring

[tbl-43.md](tbl-43.md)

Notes:

1. Connect to the GND.

2. No connect or connect to ground by a resistance greater than 1 MΩ minimum.

5-42

Mechanical

### 5.5.5 USB 3.1 Micro-A to USB 3.1 Standard-B Cable Assembly

A USB 3.1 Micro-A to USB 3.1 Standard-B cable assembly is also allowed. Figure 5-18 and Figure 5-16 show, respectively, the USB 3.1 Micro-A cable overmold and the USB 3.1 Standard-B cable overmold dimensions.

Table 5-12 shows the wire connections for the USB 3.1 Micro-A to USB 3.1 Standard-B cable assembly.

Table 5-12. USB 3.1 Micro-A to USB 3.1 Standard-B Cable Assembly Wiring

[tbl-44.md](tbl-44.md)

Notes:

1. Connect to the GND

5-43

Universal Serial Bus 3.1 Specification, Revision 1.0

### 5.5.6 USB 3.1 Icon Location

USB 3.1 cable assemblies compliant with the USB 3.1 Connectors and Cable Assemblies Compliance Specification shall display the appropriate USB 3.1 Icon. A dimensioned drawing and allowable usage of the icon are supplied with the license from the USB-IF.

The USB 3.1 Icon is embossed in a recessed area on the side of the USB 3.1 plug. This provides easy user recognition and facilitates alignment during the mating process. The USB Icon and Manufacturer's logo should not project beyond the overmold surface. The USB 3.1 compliant cable assembly is required to have the USB 3.1 Icons on the plugs at both ends, while the manufacturer's logo is recommended. USB 3.1 receptacles should be orientated to allow the Icon on the plug to be visible during the mating process. Figure 5-19 shows a typical plug orientation.

![img-95.jpeg](img-95.jpeg)

![img-96.jpeg](img-96.jpeg)

![img-97.jpeg](img-97.jpeg)

SECTION A-A

Figure 5-19. Typical Plug Orientation

5-44

Mechanical

### 5.5.7 Cable Assembly Length

This specification does not specify cable assembly lengths. A USB 3.1 cable assembly may be of any length as long as it meets all the requirements defined in this specification. The cable assembly voltage drop budget defined in Section 11.4.2 and the cable assembly loss budget defined in Section 5.6.1.3.2, limit the cable assembly length.

### 5.6 Electrical Requirements

This section covers the electrical requirements for USB 3.1 raw cables, mated connectors, and mated cable assemblies. USB 3.1 signals, known as Enhanced SuperSpeed are governed by this specification. The USB 2.0 signals are governed by the USB 2.0 specification, unless otherwise specified.

Compliance to the USB 3.1 specification is established through normative requirements of mated connectors and mated cable assemblies.

Enhanced SuperSpeed requirements supporting Gen 2 speed are specified in the frequency domain. Components and assemblies meeting Enhanced SuperSpeed Gen 2 speed electrical requirements do not require separate qualification testing for Gen 1 speed compliance.

DC requirements, such as contact resistance and current carrying capability, are also specified in this section.

Any informative specification for cable and connector products is for the purpose of design guidelines and manufacturing control.

In conjunction with performance requirements, the required test method is referenced for the parameter stated. A list of the industry standards for DC requirements is found in the Section 5.6.2. Additional supporting test procedures are found in the USB 3.1 Connectors and Cable Assemblies Compliance Document.

The requirements in the section apply to all USB 3.1 connectors and/or cable assemblies unless specified otherwise.

### 5.6.1 Enhanced SuperSpeed Electrical Requirements

The following sections outline the requirements for SuperSpeed signals.

#### 5.6.1.1 Raw Cable

Informative raw cable electrical performance targets are provided to help cable assembly manufacturers manage raw cable suppliers. These targets are not part of the USB 3.1 compliance requirements. The mandatory requirements are that the mated cable assembly performance specified in Section 5.6.1.3 and other tests specified in the USB 3.1 Connectors and Cable Assemblies Compliance Document.

##### 5.6.1.1.1 Characteristic Impedance

The differential characteristic impedance for the SDP pairs is recommended to be 90 Ω +/- 5 Ω. The single-ended characteristic impedance of coaxial Enhanced SuperSpeed signal wires is recommended to be 45 Ω +/- 3 Ω. It should be measured with a TDR in a differential mode using a 200 ps (10%-90%) rise time.

5-45

Universal Serial Bus 3.1 Specification, Revision 1.0

### 5.6.1.1.2 Intra-Pair Skew

The intra-pair skew for the SDP pairs is recommended to be less than 15 ps/m. It should be measured with a Time Domain Transmission (TDT) in a differential mode using a 200 ps (10%-90%) rise time with a crossing at 50% of the input voltage.

### 5.6.1.1.3 Differential Insertion Loss

Cable loss depends on wire gauges, plating and dielectric materials. Table 5-13 and Table 5-14 show examples of average differential insertion loss for the SDP pairs for Enhanced SuperSpeed Gen 2 speed. To meet the cable assembly differential insertion loss target, support of the Gen 2 speed requires better performance from the raw cable than required for support of the Gen 1 speed.

Table 5-13. SDP Differential Insertion Loss Examples for Gen 2 speed

[tbl-45.md](tbl-45.md)

Table 5-14. SDP Differential Insertion Loss Examples for Gen 2 speed with Coaxial Construction

[tbl-46.md](tbl-46.md)

### 5.6.1.2 Mated Connector Impedance

SuperSpeed signal routing on the PCB should minimize the stub length and minimize impedance discontinuities in the signal path. It is recommended that the SuperSpeed signals be routed on the opposite side of the PCB from the side the lead is inserted for through-hole implementations. It is recommended that the SuperSpeed signals be routed on the same side of the PCB as the solder pads for SMT implementations.

For Enhanced SuperSpeed Gen 2 speed applications, electrical optimization is required to achieve the best performance. The PCB stack up, lead geometry, and solder pad geometry should be modeled in three dimensions. Example ground voids under pads shown in Figure 5-20 are based on pad geometry, mounting type, and PCB stack up.

5-46

Mechanical

Example PTH

Example SMT pad

Example PCB stack-up

Note: See Section 5.6.1.3 for recommended electrical requirements in determining void dimensions

PTH for Standard A and B

![img-98.jpeg](img-98.jpeg)

[tbl-47.md](tbl-47.md)

SMT for Micro-B

![img-99.jpeg](img-99.jpeg)

[tbl-48.md](tbl-48.md)

Generic Stack-ups

![img-100.jpeg](img-100.jpeg)

Total thickness: 0.8 ~ 1.8 mm

Unit: mm

Figure 5-20. Recommended Ground Void Dimension for USB Standard-A Receptacle

### 5.6.1.2.1 Mated Connector Impedance for Gen 2 Speed

The recommended mated connector impedance is needed to maintain signal integrity. The differential impedance of a mated connector should be 90 Ω +/-10 Ω, as seen from a 40 ps (20%-80%) risetime of a differential TDR. The impedance profile of a mated connector should fall within the limits shown in Figure 5-21. The impedance profile of the mated connector is defined from the receptacle footprints through the plug cable termination area. In a case where the plug is directly attached to a device PCB, the mated connector impedance profile includes the path from the receptacle footprints to the plug footprints.

The normative cable assembly requirements are specified in Section 5.6.1.3.2.

5-47

Universal Serial Bus 3.1 Specification, Revision 1.0

![img-101.jpeg](img-101.jpeg)

Figure 5-21. Impedance Limits of a Mated Connector for Gen 2 Speed

### 5.6.1.3 Mated Cable Assemblies for Gen 2 speed

The requirements for mated cable assemblies for Gen 2 speed are divided into informative and normative requirements. The informative requirements are provided as design targets and normative requirements are pass/fail criteria for mated cable assembly compliance testing.

#### 5.6.1.3.1 Design Targets

The design targets are summarized in Table 5-15. Cable assemblies that meet the target performance should pass the cable assembly compliance tests, but it is not guaranteed. Compliance is determined with the normative requirements.

5-48

Mechanical

Table 5-15. Design Targets

[tbl-49.md](tbl-49.md)

### 5.6.1.3.2 Normative Requirements

The normative requirements manage the impact of insertion loss, multi-reflection, and crosstalk for the end-to-end link performance and mode conversion for EMI/RFI purposes.

#### 5.6.1.3.2.1 Test Fixtures

The mated cable assembly electrical requirements for Gen 2 speed are mostly specified in the frequency domain. To accurately measure the frequency response of the Gen 2 speed mated cable assembly, the fixture design and its performance characteristics are critical items. Common fixtures defined by the USB-IF or equivalent shall be used. Refer to USB 3.1 Connectors and Cable Assemblies Compliance Document for detailed descriptions of test fixtures. Figure 5-22 illustrates an example of a cable assembly mounted on a text fixture.

![img-102.jpeg](img-102.jpeg)

Figure 5-22. Illustration of Cable Assembly Mounted on Test Fixture

#### 5.6.1.3.2.2 Reference Hosts and Devices

To avoid channel margin loss associated with assigning interconnect budgets to the host, cable assembly, and device, the compliance of a Gen 2 speed cable assembly is established with reference hosts and reference devices to emulate the end-to-end condition as illustrated in Figure 5-23.

5-49

Universal Serial Bus 3.1 Specification, Revision 1.0

![img-103.jpeg](img-103.jpeg)

Figure 5-23. Illustration of Cable Assembly with Reference Host and Device

The USB 3.1 specification defines the standard reference hosts and devices in the form of S-parameter files, which are available for download from the USB website. The measured S-parameters of the Gen 2 speed cable assembly (with fixture effects removed) are cascaded with the S-parameters of the reference hosts and reference devices, resulting in frequency responses for total channels. The pass/fail criteria of the Gen 2 speed cable assembly are based on the channel frequency responses, as described in the following subsections.

### 5.6.1.3.2.3 Channel Metrics

There are three signal integrity impairments that impact the end-to-end link performance: attenuation, reflection, and crosstalk. Three parameters are used as the channel metrics to represent these three impairments: insertion loss fit at Nyquist frequency (ILfitatNq), integrated multi-reflection (IMR), and integrated crosstalk (IXT).

To obtain the channel insertion loss fit at Nyquist frequency (5 GHz for SuperSpeed Gen 2), the measured (cascaded) differential insertion loss, $IL(f)$, is fitted with a smoothing function:

$$ILfit(f) = a + b\sqrt{f} + cf + d\sqrt{f^3}, \tag{5-1}$$

where $f$ is frequency and $a$, $b$, $c$, and $d$ are fitting coefficients. Figure 5-24 shows an example of $IL(f)$ and $ILfit(f)$ plotted together; ILfitatNq = -20.6 dB, measured at 5 Ghz along $ILfit(f)$.

5-50

Mechanical

![img-104.jpeg](img-104.jpeg)

Figure 5-24. Illustration of Insertion Loss Fit at Nyquist Frequency

The difference between IL(f) and ILfit(f) is defined as the insertion loss deviation, ILD:

$$ILD(f) = IL(f) - ILfit(f). \tag{5-2}$$

It measures the ripple of the insertion loss, or the multi-reflection. Figure 5-25 shows an example of insertion loss deviation plotted against frequency.

5-51

Universal Serial Bus 3.1 Specification, Revision 1.0

![img-105.jpeg](img-105.jpeg)

Figure 5-25. Example of Insertion Loss Deviation

The integrated multi-reflection, IMR, is calculated with the equation below:

$$IMR = \sqrt{\int_{0}^{f_{\max}} |ILD(f)|^2 |V_{in}(f)|^2 df / f_{Nq}} * 1000 \text{ (in mV)}, \tag{5-3}$$

where $f_{Nq}$ is the Nyquist frequency (5 GHz), $f_{\max}$ is chosen as the 2 times the Nyquist frequency (10 GHz), and $V_{in}(f)$ is the input trapezoidal pulse spectrum, defined as:

![img-106.jpeg](img-106.jpeg)

$$|V_{in}(\omega)| = \left| \frac{\sin\left(\frac{\omega T_r}{2}\right)}{\frac{\omega T_r}{2}} \cdot \frac{\sin\left(\frac{\omega T_b}{2}\right)}{\frac{\omega T_b}{2}} \right|$$

$$\begin{array}{l} T_b = \text{Unit Interval} = 100 \text{ ps} \\ T_c = \text{Rise time (0-100\%)} = 0.2 T_b \\ \omega = 2\pi f \end{array}$$

The integrated crosstalk, IXT, is defined as:

$$IXT = \sqrt{\int_{0}^{f_{\max}} |NEXT(f)|^2 |V_{in}(f)|^2 df / f_{Nq}} * 1000 \text{ (in mV)}, \tag{5-4}$$

5-52

Mechanical

where NEXT(f) is the near-end crosstalk between the SuperSpeed Gen 2 signal pairs. The contribution of USB 2 D+/D- pair to SuperSpeed signal pairs is relatively small and is not included in IXT for simplicity.

More detailed discussion of ILfitatNq, IMR and IXT is given in a USB-IF whitepaper Establishing USB SuperSpeed Gen 2 Channel and Cable Assembly High Speed Compliance Specification. The USB-IF also provides a standard tool to convert measured cable assembly S-parameters into ILfitatNq, IMR and IXT.

### 5.6.1.3.2.4 Pass/Fail Criteria

SuperSpeed Gen 2 channel performance is based on ILfitatNq, IMR, and IXT. In general, a channel with more loss, more reflection, and more crosstalk has less margin. Channel margin is measured with BER (bit error ratio) eye height (eH) and eye width (eW) at BER=10⁻¹². The correlation between eH and eW and the channel metrics ILfitatNq, IMR, and IXT is established following the methodology described in the USB-IF whitepaper Establishing USB SuperSpeed Gen 2 Channel and Cable Assembly High Speed Compliance Specification. For each channel with a metrics ILfitatNq, IMR, and IXT, eH and eW is calculated:

$$eH = f_H (ILfitatNq, IMR, IXT) \tag{5-5}$$

$$eW = f_W (ILfitatNq, IMR, IXT)$$

Note that the effect of Tx and Rx equalization, jitter, and sampling noise is included in the eye height and eye width calculations. The pass/fail criteria are then expressed as

$$eH = f_H (ILfitatNq, IMR, IXT) > 0 \tag{5-6}$$

$$eW = f_W (ILfitatNq, IMR, IXT) > 0$$

and

$$ILfitatNq \ge -22 \text{ dB}$$

$$IMR \le 60 \text{ mV} \tag{5-7}$$

$$IXT \le 25 \text{ mV}$$

Equation (5-6) is an open-eye (at BER=10⁻¹²) requirement, while Equation (5-7) constrains the maximum channel loss, multi-reflection, and crosstalk. A SuperSpeed Gen 2 cable assembly is considered pass if both Equations (5-6) and (5-7) are satisfied. Figure 5-26 shows pass and fail examples.

5-53

Universal Serial Bus 3.1 Specification, Revision 1.0

![img-107.jpeg](img-107.jpeg)

![img-108.jpeg](img-108.jpeg)

![img-109.jpeg](img-109.jpeg)

![img-110.jpeg](img-110.jpeg)

Figure 5-26. Pass/Fail Examples

The x-axis is IMR in mV and the y-axis is IXT in mV. The “green” part represents the passing region with open eyes, while the “red” area the failing region with closed eyes. The passing area increases as |ILfitatNq| decreases. This pass/fail criteria allows tradeoffs among ILfitatNq, IMR, and IXT. For example, a cable assembly may have more loss if IMR and/or IXT is smaller.

USB-IF provides a standard tool to calculate eH and eW based on the input cable assembly S-parameters. This tool, or an equivalent, is integrated into the USB SuperSpeed Gen 2 compliance test suite in the USB CabCon compliance program.

### 5.6.1.3.2.5 Differential Crosstalk between D+/D- and SuperSpeed Gen 2 Signal Pairs (EIA-360-90)

The differential near-end crosstalk (DDNEXT) and far-end crosstalk (DDFEXT between the D+/D-pair and the SuperSpeed Gen 2 signal pairs shall be measured in time domain with a rise time of 500 ps (10-90%) entering the connector under test. The mated cable assembly meets the DDNEXT/DDFEXT requirement if its peak-to-peak value does not exceed the limits below (see Figure 5-27 for illustration of the peak-to-peak crosstalk):

- USB 3.1 Standard-A connector: 2%

5-54

Mechanical

- USB 3.1 Standard-B connector: 2%
- USB 3.1 Micro connector family: 2%

![img-111.jpeg](img-111.jpeg)

Figure 5-27. Illustration of Peak-to-Peak Crosstalk

### 5.6.1.3.2.6 Differential to Common Mode Conversion

The differential to common mode conversion (SCD21 or SCD12) does not require embedding the reference host and the reference device with the mated cable assembly; it is for the mated cable assembly only. A mated cable assembly passes the SCD12 requirement if its SCD12 is less than or equal to -20 dB across the frequency range of 100MHz to 10 GHz, as shown in Figure 5-28.

5-55

Universal Serial Bus 3.1 Specification, Revision 1.0

![img-112.jpeg](img-112.jpeg)

Figure 5-28. Differential-to-Common-Mode Conversion Requirement for Gen 2

### 5.6.1.3.2.7 Cable Shielding Effectiveness

The cable assembly shielding effectiveness (SE) test measures the radio frequency interference (RFI) level from the cable assembly. To perform the measurement, the cable assembly shall be installed in the cable SE test fixture as shown in Figure 5-29. The coupling factors from the cable to the fixture are characterized. The Cable SE test fixtures and specification values are under development and are to be included in future updates to this specification.

![img-113.jpeg](img-113.jpeg)

Figure 5-29. Set Up For Cable SE Measurement (subject to change)

5-56

Mechanical

### 5.6.2 DC Electrical Requirements

#### 5.6.2.1 Low Level Contact Resistance (EIA 364-23B)

The following requirement applies to both the power and signal contacts:

- 30 mΩ (Max) initial for Vbus and GND contacts.
- 50 mΩ (Max) initial for all other contacts.
- Maximum change (delta) of +10 mΩ after environmental stresses.
- Measure at 20 mV (Max) open circuit at 100 mA.
- Refer to Section 5.7 for environmental requirements and test sequences.

#### 5.6.2.2 Dielectric Strength (EIA 364-20)

- No breakdown shall occur when 100 Volts AC (RMS) is applied between adjacent contacts of unmated and mated connectors.

#### 5.6.2.3 Insulation Resistance (EIA 364-21)

A minimum of 100 MΩ insulation resistance is required between adjacent contacts of unmated and mated connectors.

#### 5.6.2.4 Contact Current Rating (EIA 364-70, Method 2)

A current of 1.8 A shall be applied to VBUS pin and its corresponding GND pin (pin 1 and pin 4 of the USB 3.1 Standard-A and Standard-B connectors; pin 1 and pin 5 of the USB 3.1 Micro connector family). Additionally, a minimum current of 0.25 A shall be applied to all the other contacts. When the current is applied to the contacts, the delta temperature shall not exceed +30 °C at any point on the USB 3.1 connectors under test, when measured at an ambient temperature of 25 °C.

## 5.7 Mechanical and Environmental Requirements

The requirements in this section apply to all USB 3.1 connectors and/or cable assemblies unless specified otherwise.

### 5.7.1 Mechanical Requirements

#### 5.7.1.1 Insertion Force (EIA 364-13)

The connector insertion force shall not exceed 35 N at a maximum rate of 12.5 mm (0.492") per minute.

It is recommended to use a non-silicon based lubricant on the latching mechanism to reduce wear. The effects of lubricants should be restricted to insertion and extraction characteristics.

#### 5.7.1.2 Extraction Force Requirements (EIA 364-13)

##### 5.7.1.2.1 Extraction Force (EIA 364-13, USB3.1 Standard Connector)

The connector extraction force shall not be less than 10 N initial and 8 N after the specified insertion/extraction or durability cycles (at a maximum rate of 12.5 mm (0.492") per minute).

5-57

Universal Serial Bus 3.1 Specification, Revision 1.0

No burs or sharp edges are allowed on top of locking latches (hook surfaces that will rub against the receptacle shield).

It is recommended to use a non-silicon based lubricant on the latching mechanism to reduce wear. The effects of lubricants should be restricted to insertion and extraction characteristics.

### 5.7.1.2.2 Extraction Force (EIA 364-13, USB 3.1 Micro Connector Family Only)

The connector extraction force shall not be less than 10 N or more than 25 N initial and less than 8 N and more than 25 N after the specified insertion/extraction or durability cycles (at a maximum rate of 12.5 mm (0.492") per minute).

No burs or sharp edges are allowed on top of locking latches (hook surfaces that will rub against the receptacle shield).

It is recommended to use a non-silicon based lubricant on the latching mechanism to reduce wear. The effects of lubricants should be restricted to insertion and extraction characteristics.

### 5.7.1.3 Durability or Insertion/Extraction Cycles (EIA 364-09)

The durability ratings listed in Table 5-16 are specified for the USB 3.1 connectors.

Table 5-16. Durability Ratings

[tbl-50.md](tbl-50.md)

The durability test shall be done at a maximum rate of 200 cycles per hour and no physical damage to any part of the connector or cable assembly shall occur.

### 5.7.1.4 Cable Flexing (EIA 364-41, Condition I)

No physical damage or discontinuity over 1 ms during flexing shall occur to the cable assembly with Dimension X = 3.7 times the cable diameter and 100 cycles in each of two planes.

### 5.7.1.5 Cable Pull-Out (EIA 364-38, Condition A)

No physical damage to the cable assembly shall occur when it is subjected to a 40 N axial load for a minimum of 1 minute while clamping one end of the cable plug.

### 5.7.1.6 Peel Strength (USB 3.1 Micro Connector Family Only)

No visible physical damage shall be noticed to a soldered receptacle when it is pulled up from the PCB in the vertical direction with a minimum force of 150 N.

### 5.7.1.7 4-Axes Continuity Test (USB 3.1 Micro Connector Family Only)

The USB 3.1 Micro connector family shall be tested for continuity under stress using the test configurations shown below. Plugs shall be supplied in a cable assembly with a representative overmold. A USB 3.1 Micro-B or -AB receptacle shall be mounted on a 2-layer printed circuit board (PCB) between 0.8 and 1.0 mm thickness. The PCB shall be clamped on either side of the receptacle no further than 5 mm away from the solder tails. The PCB shall initially be placed in a

5-58

Mechanical

horizontal plane, and an 8-N tensile force shall be applied to the cable in a downward direction, perpendicular to the axis of insertion, for a period of at least 10 seconds.

The continuity across each contact shall be measured throughout the application of the tensile force. The PCB shall then be rotated 90 degrees such that the cable is still inserted horizontally and the 8 N tensile force will be applied again in the downward direction and continuity measured as before. This test is repeated for 180-degree and 270-degree rotations. Passing parts shall not exhibit any discontinuities greater than 1 μs duration in any of the four orientations.

One method for measuring the continuity through the contacts is to short all the wires at the end of the cable pigtail and apply a voltage through a pull-up to each of VBUS, D+, D-, ID, and the SuperSpeed pins, with the GND pins connected to ground.

When testing a USB 3.1 Micro-A plug, all the sense resistors shall stay pulled down for the length of the test. When testing a USB 3.1 Micro-B plug, the ID pin shall stay high and the other pins shall remain low for the duration of the test. Alternate methods are allowed to verify continuity through all pins.

The 4 axes continuity tests shall be done with a USB 3.1 Micro-B/-A plug in a USB 3.1 Micro-B/-AB receptacle and with a USB 2.0 Micro-B/-A plug in a USB 3.1 Micro-B/-AB receptacle, as illustrated in Figure 5-30.

5-59

Universal Serial Bus 3.1 Specification, Revision 1.0

![img-114.jpeg](img-114.jpeg)

Figure 5-30. 4-Axes Continuity Test

5-60

Mechanical

### 5.7.1.8 Wrenching Strength (Reference, USB 3.1 Micro Connector Family Only)

The wrenching strength test shall be performed using virgin parts. Perpendicular forces (Fp) are applied to a plug when inserted at a distance (L) of 15 mm from the edge of the receptacle. Testing conditions and method shall be agreed to by all parties. These forces shall be applied in all four directions (i.e., left, right, up, and down). Compliant connectors shall meet the following force thresholds:

- No plug or receptacle damage shall occur when a force of 0-25 N is applied.

The plug may be damaged, but only in such a way that the receptacle does not sustain damage when a force of 25-50 N is applied.

### 5.7.1.9 Lead Co-Planarity

Co-planarity of all SMT leads shall be within a 0.08 mm range.

### 5.7.1.10 Solderability

Solder shall cover a minimum of 95% of the surface being immersed, when soldered at a temperature 255 °C +/-5 °C for an immersion duration of 5 s.

### 5.7.1.11 Restriction of Hazardous Substances (RoHS) Compliance

It is recommended that components be RoHS compliant. Environmental Requirements

### 5.7.2 Environmental Requirements

The connector interface environmental tests shall follow EIA-364-1000.01, Environmental Test Methodology for Assessing the Performance of Electrical Connectors and Sockets Used in Business Office Applications.

Since the connector defined has far more than 0.127 mm wipe length, Test Group 6 in EIA 364-1000.01 is not required. The temperature life test duration and the mixed flowing gas test duration values are derived from EIA 364-1000.01 based on the field temperature per the following.

Table 5-17. Environmental Test Conditions

[tbl-51.md](tbl-51.md)

The pass/fail criterion for the low-level contact resistance (LLCR) is as defined in Section 5.6.2.1. The durability ratings are defined in Section 5.7.1.3.

5-61

Universal Serial Bus 3.1 Specification, Revision 1.0

### 5.7.3 Materials

This specification does not specify materials for connectors and cables. Connector and cable manufactures should select appropriate materials based on performance requirements. Table 5-18 below is provided for reference only.

Note:

Connector and cable manufacturers shall comply with contact plating requirements per the following options:

Option I

Receptacle

Contact area: (Min) 0.05 μm Au + (Min) 0.75 μm Ni-Pd on top of (Min) 2.0 μm Ni

Plug

Contact area: (Min) 0.05 μm Au + (Min) 0.75 μm Ni-Pd on top of (Min) 2.0 μm Ni

Option II

Receptacle

Contact area: (Min) 0.75 μm Au on top of (Min) 2.0 μm Ni

Plug

Contact area: (Min) 0.75 μm Au on top of (Min) 2.0 μm Ni.

Other material parameters, which connector and cable manufacturers select based on performance parameters, are listed below in Table 5-18 for reference only.

Table 5-18. Reference Materials¹

[tbl-52.md](tbl-52.md)

¹ Halogen-free materials should be considered for all plastics.

5-62

Mechanical

## 5.8 Implementation Notes and Design Guides

This section discusses a few implementation notes and design guides to help users design and use the USB 3.1 connectors and cables.

### 5.8.1 Mated Connector Dimensions

Figure 5-31, Figure 5-32, and Figure 5-33 show the mated plugs and receptacles for the USB 3.1 Standard-A, USB 3.1 Standard-B, and USB 3.1 Micro connectors, respectively. The distance between the receptacle front surface and the cable overmold should be observed by system designers to avoid interference between the system enclosure and the cable plug overmold.

Provisions shall be made in connectors and chassis to ground the connector metal shells to the metal chassis to reduce EMI and RFI.

![img-115.jpeg](img-115.jpeg)

FULLY MATED PLUG AND RECEPTACLE

Figure 5-31. Mated USB 3.1 Standard-A Connector

5-63

Universal Serial Bus 3.1 Specification, Revision 1.0

![img-116.jpeg](img-116.jpeg)

FULLY MATED PLUG AND RECEPTACLE

Figure 5-32. Mated USB 3.1 Standard-B Connector

5-64

Mechanical

![img-117.jpeg](img-117.jpeg)

Figure 5-33. Mated USB 3.1 Micro-B Connector

### 5.8.2 EMI and RFI Management

Systems that include USB 3.1 connectors and cable assemblies need to meet the relevant EMI/EMC regulations.

5-65

Universal Serial Bus 3.1 Specification, Revision 1.0

Connector and cable assembly designers, as well as system implementers should pay attention to receptacle and cable plug shielding to ensure a low-impedance grounding path. The following are guidelines for EMI and RFI management:

- The quality of raw cables should be ensured. The intra-pair skew or the differential to common mode conversion of the SuperSpeed pairs has a significant impact on cable EMI performance and should be controlled within the limits of this specification.
- The cable external braid should be terminated to the cable plug metal shell as close to 360° as possible. Without appropriate shielding termination, even a perfect cable with zero intra-pair skew may not meet EMI requirements.
- The wire termination contributes to the differential-to-common-mode conversion. The breakout distance for the wire termination should be kept as small as possible for EMI, RFI, and signal integrity. If possible, symmetry should be maintained for the two lines within a differential pair.
- The mating interface between the receptacle and cable plug should have a sufficient number of grounding fingers, or springs, to provide a continuous return path from the cable plug to system ground. Friction locks should not compromise ground return connections.
- The receptacle connectors should be designed with a back-shield as part of the receptacle connector metal shell. The back-shield should have connections to adjacent shell surfaces and provide multiple connections for ground termination. The back-shield should be designed with a short return path to the chassis ground.
- The receptacle connectors should be connected to metal chassis or enclosures through grounding fingers, screws, or any other way to mitigate EMI and RFI.
- Plug connectors should have back-shields when possible.
- Outer connector shell surfaces in the mated configuration should have a maximum aperture size of 2 mm. This applies to both mounted connectors (e.g., soldered to a circuit board) and connectors used in cable assemblies. See Figure 5-34.

Aperture

![img-118.jpeg](img-118.jpeg)

Aperture

![img-119.jpeg](img-119.jpeg)

Aperture

Figure 5-34. Examples of Connector Apertures

5-66

Mechanical

### 5.8.3 Stacked Connectors

Stacked USB connectors are commonly used in PC systems. This specification does not explicitly define the stacked USB 3.1 Standard-A receptacles, but they are allowed. The following are a few points that should be taken into account when designing a stacked USB 3.1 connector:

- A stacked connector introduces additional crosstalk between the top and bottom connectors. Such crosstalk should be minimized when designing a stacked USB 3.1 connector. Enhanced SuperSpeed Gen 2 Standard-A stacked connectors should limit the total crosstalk sum from all sources within the connector to -40 dB (up to the fundamental frequency of 5.0 GHz and limiting the power sum to include agressors having a magnitude greater than or equal to -50 dB).
- Due to the additional electrical length, the top connector generally does not perform as well as the bottom connector. Connector designers should carefully design the top connector contact geometries and materials to minimize impedance discontinuity.
- Regardless of how many connectors within a stack one may choose to design, the electrical requirements defined in Section 5.6 shall be met.

5-67

Universal Serial Bus 3.1 Specification, Revision 1.0

5-68

6

Physical Layer

![img-120.jpeg](img-120.jpeg)

Figure 6-1. SuperSpeed Physical Layer

## 6.1 Physical Layer Overview

The physical layer defines the signaling technology for the SuperSpeed and SuperSpeedPlus busses. This chapter defines the electrical requirements of the SuperSpeed and SuperSpeedPlus physical layers.

This section defines the electrical-layer parameters required for operation of SuperSpeed and SuperSpeedPlus components. Normative specifications are required. Informative specifications may assist product designers and testers in understanding the intended behavior of the SuperSpeed and SuperSpeedPlus busses.

## 6.2 Physical Layer Functions

The functions of the physical layer are shown in Figure 6-2, Figure 6-3, Figure 6-4, and Figure 6-5.

6-1

Universal Serial Bus 3.1 Specification, Revision 1.0

![img-121.jpeg](img-121.jpeg)

Gen 1 transmitter

![img-122.jpeg](img-122.jpeg)

Gen 2 transmitter

Figure 6-2. Transmitter Block Diagram

6-2

Physical Layer

![img-123.jpeg](img-123.jpeg)

Figure 6-3. Gen 1 Receiver Block Diagram

6-3

Universal Serial Bus 3.1 Specification, Revision 1.0

![img-124.jpeg](img-124.jpeg)

Figure 6-4. Gen 2 Receiver Block Diagram

6-4

Physical Layer

![img-125.jpeg](img-125.jpeg)

![img-126.jpeg](img-126.jpeg)

![img-127.jpeg](img-127.jpeg)

Figure 6-5. Channel Models

### 6.2.1 Measurement Overview

The normative eye diagram is to be measured through compliance channels that represent long and short channels in order to cover the range of losses seen by real applications. These reference channels for testing at Gen 1 speed are described in the USB 3.0 SuperSpeed Equalizer Design Guidelines white paper. Reference channels for testing Gen 2 speed are described in a companion white paper posted on the USB-IF website. The eye diagram is measured using the appropriate clock recovery function described in Section 6.5.2.

Due to non-ideal channel characteristics, the eye diagram at the receiver may be completely closed. Informative receiver equalization functions are provided in Section 6.8.2 that are optimized for the compliance channels and are used to open the receiver eyes.

This methodology allows a silicon vendor to design the channel and the component as a matched pair. It is expected that a silicon component will have layout guidelines that must be followed in order for the component to meet the overall specification and the eye diagram at the end of the compliance channel.

Note that simultaneous USB 2.0 and SuperSpeed or SuperSpeedPlus operation is a testing requirement for compliance.

6-5

Universal Serial Bus 3.1 Specification, Revision 1.0

### 6.2.2 Channel Overview

A PHY is a transmitter and receiver that operate together and are located on the same component. A channel connects two PHYs together with two unidirectional differential pairs of pins for a total of four wires. The PHYs are required to be AC coupled. The AC coupling capacitors are associated with the transmitter.

## 6.3 Symbol Encoding

### 6.3.1 Gen 1 Encoding

The Gen 1 PHY uses the 8b/10b transmission code. The definition of this transmission code is identical to that specified in ANSI X3.230-1994 (also referred to as ANSI INCITS 230-1994), clause 11. As shown in Figure 6-6, ABCDE maps to abcdei and FGH maps to fghj.

![img-128.jpeg](img-128.jpeg)

Figure 6-6. Character to Symbol Mapping

#### 6.3.1.1 Serialization and Deserialization of Data

The bits of a Symbol are placed starting with bit “a” and ending with bit “j.” This is shown in Figure 6-7.

6-6

Physical Layer

![img-129.jpeg](img-129.jpeg)

Figure 6-7. Bit Transmission Order

### 6.3.1.2 Normative 8b/10b Decode Rules for Gen 1 Operation

1. A Transmitter is permitted to pick any disparity when first transmitting differential data after being in an Electrical Idle state. The Transmitter shall then follow proper 8b/10b encoding rules until the next Electrical Idle state is entered.
2. The initial disparity for a Receiver is the disparity of the first Symbol used to obtain Symbol lock.
3. Disparity may also be-reinitialized if Symbol lock is lost and regained during the transmission of differential information due to a burst error event.
4. All following received Symbols after the initial disparity is set shall be in the proper column corresponding to the current running disparity.
5. Receive disparity errors do not directly cause the link to retrain.
6. If a disparity error or 8b/10 Decode error is detected, the physical layer shall inform the link layer.

### 6.3.1.3 Gen 1 Data Scrambling

The scrambling function is implemented using a free running Linear Feedback Shift Register (LFSR). On the Transmit side, scrambling is applied to characters prior to the 8b/10b encoding. On the receive side, descrambling is applied to characters after 8b/10b decoding. The LFSR is reset whenever a COM symbol is sent or received.

The LFSR is graphically represented in Figure 6-8. Scrambling or unscrambling is performed by serially XORing the 8-bit (D0-D7) character with the 16-bit (D0-D15) output of the LFSR. An output of the LFSR, D15, is XORed with D0 of the data to be processed. The LFSR and data register are then serially advanced and the output processing is repeated for D1 through D7. The LFSR is advanced after the data is XORed.

The mechanism to notify the physical layer to disable scrambling is implementation specific and beyond the scope of this specification.

The data scrambling rules are as follows:

1. The LFSR implements the polynomial: $$G(X)=X^{16}+X^{5}+X^{4}+X^{3}+1$$
2. The LFSR value shall be advanced eight serial shifts for each Symbol except for SKP.
3. All 8b/10b D-codes, except those within the Training Sequence Ordered Sets shall be scrambled.
4. K codes shall not be scrambled.

6-7

Universal Serial Bus 3.1 Specification, Revision 1.0

5. The initialized value of an LFSR seed (D0-D15) shall be FFFFh. After COM leaves the Transmitter LFSR, the LFSR on the transmit side shall be initialized. Every time COM enters the Receive LFSR, the LFSR on the receive side shall be initialized. This also applies to the BRST sequence during loopback mode (see section 6.8.4.1).

![img-130.jpeg](img-130.jpeg)

Figure 6-8. LFSR with Scrambling Polynomial

# IMPLEMENTATION NOTE

# Disabling Scrambling

Disabling scrambling is intended to help simplify test and debug equipment. Control of the exact data patterns is useful in a test and debug environment. Since scrambling is reset at the physical layer, there is no reasonable way to reliably control the state of the data transitions through software. The Disable Scrambling bit is provided in the training sequence for this purpose.

The mechanism(s) and/or interface(s) used to notify the physical layer to disable scrambling is component implementation specific and beyond the scope of this specification.

For more information on scrambling, refer to Appendix B.

### 6.3.1.4 8b/10b Decode Errors for Gen 1 Operation

An 8b/10b Decode error shall occur when a received Symbol does not match any of the valid 8b/10b Symbols listed in Appendix A. Any received 8b/10b Symbol that does not match any of the valid 8b/10b Symbols listed in Appendix A shall be forwarded to the link layer by substituting a K28.4 symbol (refer to Table 6-1). 8b/10b errors may not directly initiate Recovery.

### 6.3.2 Gen 2 Encoding

A Gen 2 link, operating at 10Gb/s, shall use the encoding rules described in this subsection. The encoding is a scrambled 128b/132b encoding.

### 6.3.2.1 Serialization and Deserialization of Data

Data is serialized and transmitted from LSB to MSB as shown below. For Gen 2 operation a Symbol is defined to be 1 byte of information that may or may not be scrambled according to the scrambling rules.

6-8

Physical Layer

![img-131.jpeg](img-131.jpeg)

Figure 6-9. Gen 2 Serialization and Deserialization Order

![img-132.jpeg](img-132.jpeg)

Figure 6-10. Gen 2 Bit Transmission Order and Framing

### 6.3.2.2 Normative 128b/132b Decode Rules

The physical layer shall encode the data on a per block basis. Each block shall comprise a 4-bit Block Header and a 128-bit payload. The 4-bit header is set to 0011b for data and 1100b for control blocks. This header format allows for the correction of single bit errors in the header information.

Ordered sets are control blocks, and all data is sent in data blocks. The following is a list of the control blocks.

- TS1 Ordered Set
- TS2 Ordered Set

6-9

Universal Serial Bus 3.1 Specification, Revision 1.0

- TSEQ Ordered Set
- SYNC Ordered Set
- SKP Ordered Set
- SDS Ordered Set

### 6.3.2.3 Data Scrambling for Gen 2 Operation

The scrambler used for Gen 2 operation is different than the scrambler used for Gen 1 operation.

The LFSR uses the following polynomial: G(X) = X²³ + X²¹ + X¹⁶ + X⁸ + X⁵ + X² + 1.

The scrambler has the following modes of operation:

1. The scrambler advances and is XORed with the data.
2. The scrambler advances and is bypassed (not XORed with the data).
3. The scrambler does not advance and is bypassed (not XORed with the data).

The scrambling rules are as follows:

1. The 4 bits of the Block Header bypass and do not advance the scrambler.
2. TS1, TS2 and TSEQ:
  a. Symbol 0 of a TS1, TS2, or TSEQ Ordered Set bypass and advances the scrambler.
  b. Symbols 1 to 13 are scrambled.
  c. Symbols 14 and 15 bypass the scrambler and the scrambler advances if being used for DC balance. If they are not being used for DC balance then they are scrambled.
3. SKP Ordered Sets bypass and do not advance the scrambler.
4. SDS Ordered Sets bypass the scrambler, but the scrambler advances.
5. All symbols of a SYNC Ordered Set bypass the scrambler. The scrambling LFSR is initialized after the last Symbol of a SYNC Ordered Set is transmitted. The descrambling LFSR is initialized after the last Symbol of a SYNC Ordered Set is received.
6. Receivers evaluate Symbol 0 of Control Blocks to determine whether to advance their LFSR. If Symbol 0 of the Block is SKP or SKPEND then the LFSR is not advanced for any Symbol of that Block. Otherwise, the LFSR is advanced for all Symbols of the Block.
7. All 16 Symbols of a Data Block are scrambled and advance the scrambler.
8. For Symbols that need to be scrambled the least significant bit is scrambled first and the most significant bit is scrambled last.
9. The seed value for the LFSR is 1D BFBCh.
10. Every 16384 TSEQ sets a SYNC Ordered Set shall be inserted to reset scrambler and to aid in block alignment.

Figure 6-11 depicts the LFSR for the scrambling polynomial.

6-10

Physical Layer

![img-133.jpeg](img-133.jpeg)

Figure 6-11. LFSR for use in Gen 2 operation

6-11

Universal Serial Bus 3.1 Specification, Revision 1.0

### 6.3.2.4 128b/132b Decode Errors

The Block Header decode error rules are as follows:

1. Single bit errors in the Block Header shall be reported to the link layer and corrected.
2. Double bit errors in the Block Header shall be reported to the link layer.

### 6.3.3 Special Symbols for Framing and Link Management

The 8b/10b encoding scheme provides Special Symbols that are distinct from the Data Symbols used to represent characters. These Special Symbols are used for various Link Management mechanisms described later. Table 6-1 lists the Special Symbols used and provides a brief description for each. Special Symbols shall follow the proper 8b/10b disparity rules. The compliance tests are defined in the USB SuperSpeed Compliance Methodology white paper. For Gen 2 operation the block header identifies whether the following 16 symbols have special meaning or if they represent data. In Gen 2 operation a receiver shall always perform single bit error correction on the special symbols when they are part of a control block. For Gen 1 and Gen 2 the following special symbols are defined.

Table 6-1. Special Symbols

[tbl-53.md](tbl-53.md)

6-12

Physical Layer

[tbl-54.md](tbl-54.md)

## 6.4 Link Initialization and Training

### 6.4.1 Link Training

#### 6.4.1.1 Gen 1 Operation

This section defines the sequences that are used for configuration and initialization. The sequences are used by the Initialization State Machine (refer to Chapter 7) for the following functions:

- Configuring and initializing the link
- Bit-lock and symbol lock
- Rx equalization training
- Lane polarity inversion

Training sequences are composed of Ordered Sets used for initializing bit alignment, Symbol alignment and optimizing the equalization. Training sequence Ordered Sets are never scrambled but are always 8b/10b encoded.

Bit lock refers to the ability of the Clock/Data Recovery (CDR) circuit to extract the phase and frequency information from the incoming data stream. Bit lock is accomplished by sending a sufficiently long sequence of bits (D10.2 symbol containing alternating 0s and 1s) so the CDR roughly centers the clock within the bit.

Once the CDR is properly recovering data bits, the next step is to locate the start and end of a 10-bit symbol. For this purpose, the special K-Code called COMMA is selected from the 8b/10b codes. The bit pattern of the COMMA code is unique, so that it is never found in other data patterns, including any combination of a D-Code appended to any other D-Code or appended to any K-Code. This applies to any polarity of code. The only exception is for various bit patterns that include a bit error.

Training sequences (TS1 or TS2) are transmitted consecutively and can only be interrupted by SKP Ordered Sets occurring between Ordered Sets (between consecutive TS1 sets, consecutive TS2 sets, or when TS1 is followed by TS2).

##### 6.4.1.1.1 Normative Training Sequence Rules for Gen 1 Operation

Training sequences are composed of Ordered Sets used for initializing bit alignment, symbol alignment, and receiver equalization.

The following rules apply to the training sequences:

- Training sequence Ordered Sets shall be 8b/10b encoded.
- Transmission of a TS1 or TS2 Ordered Set shall not be interrupted by SKP Ordered Sets. SKP Ordered Sets shall be inserted before, or after, completion of any TS1 or TS2 Ordered Set.

6-13

Universal Serial Bus 3.1 Specification, Revision 1.0

- No SKP Ordered Sets are to be transmitted during the entire TSEQ time (65,536 ordered sets). This means that the PHY must manage its elasticity buffer differently than during normal operation.

Additional rules for the use of TSEQ, TS1, and TS2 Ordered Sets can be found in Chapter 7.

### 6.4.1.1.2 Training Control Bits for Gen 1 Operation

The training control bits are found in the Link Functionality symbol within the TS1 and TS2 ordered sets. They are described in Table 6-5.

Bit 0 and bit 2 of the link configuration field shall not be set to 1 simultaneously. If a receiver detects this condition in the received Link configuration field, then all of the training control bits shall be ignored.

### 6.4.1.1.3 Training Sequence Values for Gen 1 Operation

The TSEQ training sequence repeats 65,536 times to allow for testing many coefficient settings.

Table 6-2. Gen 1 TSEQ Ordered Set

[tbl-55.md](tbl-55.md)

Table 6-3. Gen 1 TS1 Ordered Set

[tbl-56.md](tbl-56.md)

6-14

Physical Layer

Table 6-4. Gen 1 TS2 Ordered Set

[tbl-57.md](tbl-57.md)

Table 6-5. Gen 1/Gen 2 Link Configuration

[tbl-58.md](tbl-58.md)

### 6.4.1.2 Gen 2 Operation

This section defines the sequences that are used for configuration and initialization of a link operating at Gen 2 rates. The sequences are used by the Initialization State Machine (refer to Chapter 7) for the following functions:

- Configuring and initializing the link
- Bit-lock and symbol lock
- Rx equalization training
- Lane polarity inversion
- Block alignment

Training sequences are composed of Ordered Sets used for initializing bit alignment, Symbol alignment, block alignment and optimizing the equalization.

Bit lock refers to the ability of the Clock/Data Recovery (CDR) circuit to extract the phase and frequency information from the incoming data stream. Bit lock is accomplished by sending a pattern sufficiently rich in transitions so that the CDR roughly centers the clock within the bit.

#### 6.4.1.2.1 Normative Training Sequence Rules for Gen 2 Operation

Training sequences are composed of Ordered Sets used for initializing bit alignment, symbol alignment, block alignment, scrambler synchronization and receiver equalization.

The following rules apply to the training sequences:

1. Training sequence Ordered Sets shall comprise 16 Symbols and be 128b/132b encoded.

6-15

Universal Serial Bus 3.1 Specification, Revision 1.0

2. Transmission of a TSEQ, TS1 or TS2 Ordered Set can only be interrupted by a SKP Ordered Set or a SYNC Ordered Set.
3. A SYNC Ordered Set shall be transmitted every 16384 TSEQ sets during a Gen 2 training session.
4. A SYNC Ordered Set shall be transmitted every 32 ordered sets in Gen 2 operation when sending TS1 or TS2 ordered sets (during Recovery, Polling.Active, Recovery.Configuration, Hot Reset and Polling.Config).

### 6.4.1.2.2 Training Sequence Values for Gen 2 Operation

Transmitters are required to track the running DC Balance of the bits transmitted on the wire (after scrambling) for TSEQ, TS1 and TS2 Ordered Sets. The running DC Balance is the difference between the number of 1s transmitted and the number of 0s transmitted.

The PHY shall be capable of tracking a difference of at least 511 bits in either direction: 511 more 1s than 0s, and 511 more 0s than 1s. Any counters used shall saturate at their limit (not roll-over) and continue to track reductions after their limit is reached. For example, a counter that can track a difference of 511 bits will saturate at 511 if a difference of 513 is detected, and then change to 509 if the difference is reduced by 2 in the future.

The running DC Balance is set to 0 at the start of Gen 2 data block transmission.

For every TSEQ, TS1 or TS2 Ordered Set transmitted, Transmitters shall evaluate the running DC Balance and transmit one of the DC Balance Symbols defined for Symbols 14 and 15 as defined by the algorithm below. If the number of 1s needs to be reduced, the DC Balance Symbols 20h (for Symbol 14) and 08h (for Symbol 15) are transmitted. If the number of 0s needs to be reduced, the DC Balance Symbols DFh (for Symbol 14) and F7h (for Symbol 15) are transmitted. If no change is required, the appropriate TS Identifier Symbol is transmitted. Any DC Balance Symbols transmitted for Symbols 14 or 15 bypass scrambling, while TS Identifier Symbols follow the standard scrambling rules. The following algorithm shall be used to control the DC Balance:

1. If the running DC Balance is \(>31\) at the end of Symbol 11 of the TS Ordered Set, transmit DFh for Symbol 14 and F7h for Symbol 15 to reduce the number of 0s, or 20h for Symbol 14 and 08h for Symbol 15 to reduce the number of 1s.
2. Else, if the running DC Balance is \(>15\) at the end of Symbol 11 of the TS Ordered Set, transmit F7h for Symbol 15 to reduce the number of 0s, or 08h for Symbol 15 to reduce the number of 1s. Transmit the normal TS Identifier Symbol (scrambled) for Symbol 14.
3. Else, transmit the normal TS Identifier Symbol (scrambled) for Symbols 14 and 15.

Receivers may check Symbols 14 and 15 for the following values when determining whether a TS Ordered Set is valid: The appropriate TS Identifier Symbol after de-scrambling, or a valid DC Balance Symbol of DFh or 20h before de-scrambling for Symbol 14, or a valid DC Balance Symbol of F7h or 08h before de-scrambling for Symbol 15.

A new ordered set required for Gen 2 operation is the Start of Data Stream (SDS) Ordered set. This is only defined for Gen 2 operation and does not have a Gen 1 counterpart. It shall be transmitted during Polling.Idle, Recovery.Idle, and Hot Reset.Exit to define the transition from Ordered Set Blocks to a Data Stream. It shall not be transmitted at any other time. While not in the Loopback state, the Block following an SDS Ordered Set shall be a Data Block and the first Symbol of that Data Block is the first Symbol of the Data Stream.

6-16

Physical Layer

Table 6-6. Gen 2 TS1 Ordered Set

[tbl-59.md](tbl-59.md)

Table 6-7. Gen 2 TS2 Ordered Set

[tbl-60.md](tbl-60.md)

Table 6-8. Gen 2 TSEQ Ordered Set

[tbl-61.md](tbl-61.md)

Table 6-9. Gen 2 SYNC Ordered Set

[tbl-62.md](tbl-62.md)

Table 6-10. SDS Ordered Set

[tbl-63.md](tbl-63.md)

### 6.4.1.2.3 Training Control Bits for Gen 2 Operation

The training control bits are found in the Link Functionality symbol within the TS1 and TS2 ordered sets. They are described in Table 6-5.

Bit 0 and bit 2 of the link configuration field shall not be set to 1 simultaneously. If a receiver detects this condition in the received Link configuration field, then all of the training control bits shall be ignored.

### 6.4.1.2.4 Informative Block Alignment for Gen 2 Operation

During Link training, the 132 bits of the SYNC block are a unique bit pattern that Receivers use to determine the location of the Block Headers in the received bit stream. Conceptually, Receivers

6-17

Universal Serial Bus 3.1 Specification, Revision 1.0

can be in three different phases of Block alignment: Unaligned, Aligned, and Locked. These phases are defined to illustrate the required behavior, but are not meant to specify a required implementation.

Unaligned Phase: Receivers enter this phase when they exit a low-power Link state, or if directed. In this phase, Receivers monitor the received bit stream for the SYNC OS. When one is detected, they adjust their alignment to it and proceed to the Aligned phase.

Aligned Phase: During this phase, receivers monitor the received bit stream for SYNC Ordered Sets. If a SYNC OS is detected with an alignment that does not match the current alignment, Receivers shall adjust its alignment to the newly received SYNC OS. Once an SDS OS is received, Receivers proceed to the Locked phase. Receivers are permitted to return to the Unaligned phase if an undefined Block Header is received. Receivers shall adjust the alignment in this phase as needed when receiving SKP ordered sets of lengths other than 16 symbols.

Locked Phase: Receivers shall not adjust their Block alignment while in this phase. Data Blocks are expected to be received with the given alignment, and adjusting the Block alignment would interfere with the processing of these Blocks. Receivers shall return to the Unaligned or Aligned phase if an undefined Block Header is received. Receivers shall adjust the alignment in this phase as needed when receiving SKP ordered sets of lengths other than 16 symbols.

Upon entering U1 a transmitter may send out nonintended data before powering down. These bits have no meaning and may arise due to a block boundary ending in the middle of a transmitter's internal parallel data path.

### 6.4.2 Lane Polarity Inversion

#### 6.4.2.1 Gen 1 Operation

During the TSEQ training sequence, the Receiver shall use the D10.2 Symbol within the TSEQ Ordered Set to determine lane polarity inversion (Rxp and Rxn are swapped). If polarity inversion has occurred, the D10.2 symbols within the TSEQ ordered set will be received as D21.5 instead of D10.2 and the receiver shall invert the polarity of the received bits. This shall be done before the TSEQ symbols 1-15 are used since these symbols are not all symmetric under inversion in the 8b/10b domain. If the receiver does not use the TSEQ training sequence then the polarity inversion may be checked against the D10.2 symbol in the TS1 ordered set.

#### 6.4.2.2 Gen 2 Operation

During reception of SYNC ordered sets the symbols of the SYNC Ordered Set shall be used to determine whether a polarity inversion has occurred. If the SYNC identifier (and symbols 2,4,6,8,10,12,14) are received as FFh instead of 00h then a polarity inversion has occurred and the receiver shall invert the polarity of the received bits.

### 6.4.3 Elasticity Buffer and SKP Ordered Set

The Enhanced SuperSpeed architecture supports a separate reference clock source on each side of the Enhanced SuperSpeed link. The accuracy of each reference clock is required to be within +- 300 ppm. This gives a maximum frequency difference between the two devices of the link of +- 600 ppm. In addition, SSC creates a frequency delta that has a maximum difference of 5000 ppm.

6-18

Physical Layer

The total magnitude of the frequency delta can range from -5300 to 300 ppm. This frequency delta is managed by an elasticity buffer that consumes or inserts SKP ordered sets.

SKP Ordered Sets shall be used to compensate for frequency differences between the two ends of the link. The transmitter sends SKP ordered sets at an average of every 354 symbols. However, SKP ordered sets shall not be inserted within any packet. The transmitter is allowed to buffer the SKP ordered sets up to a maximum of four SKP ordered sets. For Gen 1 operation the receiver shall implement an elasticity buffer capable of buffering (or starving) eight symbols of data. For Gen 2 operation, due to the presence of retimers along the signal path, a receiver shall tolerate not receiving any SKP Symbols for up to 180 blocks. Thus during Gen 2 operation a receiver must implement an elasticity buffer capable of buffering (or starving) twenty two symbols of data.

### 6.4.3.1 SKP Rules (Host/Device/Hub) for Gen 1 Operation

- The SKP Ordered Set shall consist of a SKP K-Symbol followed by a SKP K-Symbol. A SKP Ordered Set represents two Symbols that can be used for clock compensation.
- A device shall keep a running count of the number of transmitted symbols since the last SKP Ordered set. The value of this count will be referred to as Y. The value of Y is reset whenever the transmitter enters Polling.Active.
- Unless otherwise specified, a transmitter shall insert the integer result of Y/354 calculation Ordered sets immediately after each transmitted TS1, TS2 Ordered Set, LMP, TP Data Packet Payload, or Logical idle. During training only, a transmitter is allowed the option of waiting to insert 2 SKP ordered sets when the integer result of Y/354 reaches 2. A transmitter shall not transmit SKP Ordered Sets at any other time.

Note: The non-integer remainder of the Y/354 SKP calculation shall not be discarded and shall be used in the calculation to schedule the next SKP Ordered Set.

- SKP Commands do not count as interruptions when monitoring for Ordered Sets (i.e., consecutive TS1, TS2 Ordered Sets in Polling and Recovery).

Table 6-11. Gen 1 SKP Ordered Set Structure

[tbl-64.md](tbl-64.md)

### 6.4.3.2 SKP Rules (Host/Device/Hub) for Gen 2 Operation:

Table 6-12 describes the layout of the SKP Ordered Set when using 128b/132b encoding. A transmitted SKP Ordered Set always starts out as 16 Symbols long. The granularity for which SKP Symbols can be added or removed by a Port is two symbols. A port may add or remove more than 2 SKP symbols, but the number of SKP symbols that is added or removed shall be a multiple of two. This includes retimers within the signal path. Thus, a receiver may receive a SKP OS with anywhere from 0 to thirty six SKP symbols with the number of SKP symbols being a multiple of two. A SKP OS with 0 SKP symbols has only a SKPEND symbol followed by the three symbols that describe the LFSR state. Another impact of receiving variable length SKP OS is that a receiver is always allowed to add up to 12 SKP symbols to any SKP OS regardless of the length of the received SKP OS.

The SKPEND Symbol indicates the last four Symbols of SKP Ordered Set so that receivers can identify the location of the next Block Header in the bit stream. The three Symbols following the SKPEND Symbol contain different information depending on the LTSSM state.

6-19

Universal Serial Bus 3.1 Specification, Revision 1.0

A receiver must always perform single bit error correction on the SKP and SKPEND (and all other special) symbols. However, since the Hamming distance between the SKP and SKPEND symbols is 8, once a receiver has determined that it is dealing with a non-empty SKP OS (by proper detection of a first SKP symbol) it may be beneficial to use multiple bit (up to 3-bit) error correction in differentiating between a SKP and a SKPEND symbol.

Table 6-12. Gen 2 SKP Ordered Set

[tbl-65.md](tbl-65.md)

The following rules apply for SKP insertion for Gen 2 operation:

1. A transmitter shall keep a running count of the number of transmitted blocks since the last SKP Ordered set. The value of this count will be referred to as Y. The value of Y is reset whenever the transmitter enters Polling.Active or when a SKP OS is transmitted.
2. Once the count, Y, gets to 21 a transmitter must insert a SKP OS at the next legitimate opportunity. The fastest a transmitter can insert SKP OS is once every 22 blocks. Situations that delay the immediate insertion of a SKP OS are the following: a transmitter shall not interrupt a data packet or a SYNC OS to insert a SKP OS. In the worst case it may take 90 blocks before there is an opportunity to insert a SKP OS. In Gen 2 operation there is no accumulation of SKP OS, each time a SKP OS is transmitted the SKP counter, Y, is reset to 0.
3. SKP Ordered Sets do not count as interruptions when monitoring for Ordered Sets (i.e., consecutive TS1, TS2 Ordered Sets in Polling and Recovery).

6-20

Physical Layer

4. SYNC ordered sets have priority of SKP ordered sets. A SKP OS that is scheduled to be sent at the same time as a SYNC OS shall have to be delayed until the SYNC OS is transmitted.
5. The Data parity bit should be even parity for last three symbols in the SKP OS. The parity is a check of the LFSR seed value.

### 6.4.4 Compliance Pattern

Entry to the Polling.Compliance substate is described in Chapter 7. This initiates the transmission of the pseudo-random data pattern generated by the scrambled D0.0 compliance sequence. SKPs are not sent during the transmission of any compliance pattern. The compliance pattern shall be transmitted continuously or until a ping LFPS (refer to Section 6.9) is detected at the receiver. Upon detection of a ping LFPS, the compliance pattern shall advance to the next compliance pattern. Upon detection of a reset, LFPS the compliance pattern shall be terminated. The compliance pattern sequences are described in Table 6-13.

In the table, patterns CP0 through CP8 are transmitted at Gen 1 rate, while CP9 through CP12 are transmitted at Gen 2 rate.

Table 6-13. Compliance Pattern Sequences

[tbl-66.md](tbl-66.md)

Note: Unless otherwise noted, scrambling is disabled for compliance patterns.

### 6.4.4.1 Gen 2 Compliance Pattern CP9

The Gen 2 compliance pattern comprises a pseudo-random data pattern that is used to test transmitter and receiver compliance. The pattern repeats every 65536 symbols and starts with a SYNC Ordered Set so as to reset the scrambler and mark the beginning of the pattern.

6-21

Universal Serial Bus 3.1 Specification, Revision 1.0

Table 6-14. Gen 2 Compliance Pattern

[tbl-67.md](tbl-67.md)

## 6.5 Clock and Jitter

### 6.5.1 Informative Jitter Budgeting

The jitter for USB 3.1 is budgeted among the components that comprise the end to end connections: the transmitter, channel (including packaging, connectors, and cables), and the receiver. The jitter budget is derived at the silicon pads. The Dj distribution is the dual Dirac method. Table 6-15 lists Tx, Rx, and channel jitter budgets.

Table 6-15. Informative Jitter Budgeting at the Silicon Pads

[tbl-68.md](tbl-68.md)

Notes:

1. Rj is the sigma value assuming a Gaussian distribution.

2. Rj Total is computed as the Root Sum Square of the individual Rj components.

3. Dj budget is using the Dual Dirac method.

4. Tj at a 10$^{-12}$ BER is calculated as 14.068 * Rj + Dj.

5. The media budget includes the cancellation of ISI from the appropriate Rx equalization function.

6. Tx is measured after application of the JTF.

# NOTE

# Captive Cables

Captive cables must meet the mated connector requirements specified in Section 5.6.1.2. But a captive cable is not considered a stand-alone component. For electrical budgeting purposes, a captive cable is considered to be part of a device, and must meet the device jitter requirements listed in Table 6-15.

### 6.5.2 Normative Clock Recovery Function

The Tx Phase jitter measurement is performed using a standard clock recovery, shown in Figure 6-12. For information on the golden PLL measurement refer to the latest version of INCITS

6-22

Physical Layer

TR-35-2004, INCITS Technical Report for Information Technology – Fibre Channel – Methodologies for Jitter and Signal Quality Specification (FC-MJSQ).

The clock recovery function is given by Equations 1-3. A schematic of the general clock recovery function is shown in Figure 6-12. As shown, the clock recovery circuit has a low pass response. After the recovered clock is compared (subtracted) to the data, the overall clock recovery becomes a high pass function. This is shown with the appropriate bandwidths in Figure 6-13 for Gen 1 operation and in Figure 6-14 for Gen 2 operation.

![img-134.jpeg](img-134.jpeg)

Figure 6-12. Jitter Filtering – “Golden PLL” and Jitter Transfer Functions

6-23

Universal Serial Bus 3.1 Specification, Revision 1.0

![img-135.jpeg](img-135.jpeg)

Figure 6-13. "Golden PLL" and Jitter Transfer Functions for Gen 1 Operation

![img-136.jpeg](img-136.jpeg)

Figure 6-14. "Golden PLL" and Jitter Transfer Functions for Gen 2 Operation

6-24

Physical Layer

The equations for these functions are:

$$H_{CDR}(s) = \frac{2s\zeta\omega_n + \omega_n^2}{s^2 + 2s\zeta\omega_n + \omega_n^2} \tag{1}$$

and

$$JTF(s) = \frac{s^2}{s^2 + 2\zeta\omega_n s + \omega_n^2} \tag{2}$$

where $\omega_n$ is the natural frequency and $\zeta$ is the damping factor. The relationship to the 3 dB frequency is

$$\omega_{3dB} = \omega_n \left(1 + 2\zeta^2 + \left[(1 + 2\zeta^2)^2 + 1\right]^{\frac{1}{2}}\right)^{\frac{1}{2}} \tag{3}$$

As shown in Figure 6-13, for Gen 1 operation the corner frequency is $\omega_{3dB} = 2\pi 10^7$ and

$\zeta = 0.707$. For Gen 2 operation refer to Figure 6-14 with $\omega_{3dB} = 2\pi 1.5 \times 10^7$ and $\zeta = 0.707$.

These transfer functions have a maximum peaking of 2 dB.

### 6.5.3 Normative Spread Spectrum Clocking (SSC)

All ports are required to have Spread Spectrum Clocking (SSC) modulation. Providing the same SSC clock to two different components is allowed but not required, the SSC can be generated asynchronously. The SSC profile is not specified and is vendor specific. The SSC modulation requirement is listed in Table 6-16. The SSC modulation may not violate the phase slew rate described in Section 6.5.4.

Table 6-16. SSC Parameters

[tbl-69.md](tbl-69.md)

Note:

1. The data rate is modulated from 0 ppm to -5000 ppm of the nominal data rate frequency and scales with data rate.

2. This is measured below 2 MHz only.

An example of the period modulation from triangular SSC is shown in Figure 6-15.

6-25

Universal Serial Bus 3.1 Specification, Revision 1.0

![img-137.jpeg](img-137.jpeg)

Figure 6-15. Example of Period Modulation from Triangular SSC

### 6.5.4 Normative Slew Rate Limit

The CDR is a slew rate limited phase tracking device. The combination of SSC and all other jitter sources within the bandwidth of the CDR shall not exceed the maximum allowed slew rate.

This measurement is performed by filtering the phase jitter with the CDR transfer function and taking the first difference of the phase jitter to obtain the filtered period jitter. The peak of the period jitter shall not exceed TCDR_SLEW_MAX listed in Table 6-17.

Additional details on the slew rate measurement are available in the white paper titled USB 3.0 Jitter Budgeting.

## 6.6 Signaling

### 6.6.1 Eye Diagrams

The eye diagrams are a graphical representation of the voltage and time limits of the signal. This eye mask applies to jitter after the application of the appropriate jitter transfer function and reference receiver equalization. In all cases, the eye is to be measured for 10⁶ consecutive UI. The budget for the link is derived assuming a total 10⁻¹² bit error rate and is extrapolated to a measurement of 10⁶ UI assuming the random jitter is Gaussian.

Figure 6-16 shows the eye mask used for all eye diagram measurements. Referring to the figure, the time is measured from the crossing points of Txp/Txn. The time is called the eye width, and the voltage is the eye height. The eye height is to be measured at the maximum opening (at the center of the eye width ± 0.05 UI). Specific eye mask requirements are defined in Table 6-19.

The eye diagrams are to be centered using the jitter transfer function (JTF). The recovered clock is obtained from the data and processed by the JTF. The center of the recovered clock is used to position the center of the data in the eye diagram.

The eye diagrams are to be measured into 50-Ω single-ended loads.

6-26

Physical Layer

![img-138.jpeg](img-138.jpeg)

Gen 1 eye mask

![img-139.jpeg](img-139.jpeg)

Gen 2 eye mask

Figure 6-16. Eye Masks

6-27

Universal Serial Bus 3.1 Specification, Revision 1.0

### 6.6.2 Voltage Level Definitions

Referring to Figure 6-17, the differential voltage, $V_{DIFF}$, is the voltage on Txp (Rxp at the receiver) with respect to Txn (Rxn at the receiver). $V_{DIFF}$ is the same voltage as the swing on the single signal of one conductor. The differential voltage is

(4) $V_{DIFF} = Txp - Txn$

The total differential voltage swing is the peak to peak differential voltage, $V_{DIFF-PP}$. This is twice the differential voltage. The peak to peak differential voltage is

(5) $V_{DIFF-PP} = 2 * V_{DIFF}$

The Common Mode Voltage ($V_{CM}$) is the average voltage present on the same differential pair with respect to ground. This is measured, with respect to ground, as

(6) $V_{CM} = (Txp + Txn) / 2.$

DC is defined as all frequency components below $F_{DC} = 30$ kHz. AC is defined as all frequency components at or above $F_{DC} = 30$ kHz. These definitions pertain to all voltage and current specifications.

An example waveform is shown in Figure 6-17. In this waveform, the peak-to-peak differential voltage, $V_{DIFF-PP}$ is 800 mV. The differential voltage, $V_{DIFF}$, is 400 mVPP. Note that while the center crossing point for both Txp and Txn is shown at 300 mV, the corresponding crossover point for the differential voltage is at 0.0 V. The center crossing point at 300 mV is also the common mode voltage, $V_{CM}$. Note these waveforms include de-emphasis. The actual amount of de-emphasis can vary depending on the transmitter setting according to the allowed ranges in Table 6-17.

![img-140.jpeg](img-140.jpeg)

Figure 6-17. Single-ended and Differential Voltage Levels

6-28

Physical Layer

### 6.6.3 Tx and Rx Input Parasitics

Tx and Rx input parasitics are specified by the lumped circuit shown in Figure 6-18.

![img-141.jpeg](img-141.jpeg)

Figure 6-18. Device Termination Schematic

In this circuit, the input buffer is simplified to a termination resistance in parallel with a parasitic capacitor. This simplified circuit is the load impedance.

6-29

Universal Serial Bus 3.1 Specification, Revision 1.0

## 6.7 Transmitter Specifications

### 6.7.1 Transmitter Electrical Parameters

Peak (p) and peak-peak (p-p) are defined in Section 6.6.2.

Table 6-17. Transmitter Normative Electrical Parameters

[tbl-70.md](tbl-70.md)

Notes:

1. Measured over a 0.5μs interval using CP10. The measurements shall be low pass filtered using a filter with 3 dB cutoff frequency that is 60 times the modulation rate. The filter stopband rejection shall be greater or equal to a second order low-pass of 20 dB per decade. Evaluation of the maximum df/dt is achieved by inspection of the low-pass filtered waveform.

The values in Table 6-18 are informative and not normative. They are included in this document to provide some guidance beyond the normative requirements in Table 6-17 for transmitter design and development. A transmitter can be fully compliant with the normative requirements of the specification and not meet all the values in this table (many of which are immeasurable in a finished product). Similarly, a transmitter that meets all the values in this table is not guaranteed to be in full compliance with the normative part of this specification.

6-30

Physical Layer

Table 6-18. Transmitter Informative Electrical Parameters at Silicon Pads

[tbl-71.md](tbl-71.md)

### 6.7.2 Low Power Transmitter

In addition to the full swing transmitter specification, an optional low power swing transmitter is also specified for SuperSpeed applications. A low power swing transmitter is typically used in systems that are sensitive to power and noise interference, and have a relatively short channel. The requirement as to whether a transmitter needs to support full swing, low power swing, or both swings, is dependent on its usage model. All SuperSpeed transmitters must support full swing, while support for low power swing is optional. The method by which the output swing is selected is not defined in the specification, and is implementation specific.

While two different transmitters are specified, only a single receiver specification is defined. This implies that receiver margins (as specified in Table 6-21) shall be met if a low power transmitter is used.

6-31

Universal Serial Bus 3.1 Specification, Revision 1.0

### 6.7.3 Transmitter Eye

The eye mask is measured using the compliance data patterns as described in Section 6.4.3.2. The transmitter compliance test for Gen 1 uses compliance patterns CP0 and CP1 for TJ and RJ, respectively. The transmitter compliance test for Gen 2 uses compliance patterns CP9 and CP10 for TJ and RJ, respectively. Eye height is measured for 10⁶ consecutive UI. Jitter is extrapolated from 10⁶ UI to 10⁻¹² BER.

Table 6-19. Normative Transmitter Eye Mask at Test Point TP1

[tbl-72.md](tbl-72.md)

Notes:

1. Measured over 10⁶ consecutive UI and extrapolated to 10⁻¹² BER.

2. Measured after receiver equalization function.

3. Measured at end of reference channel and cables at TP1 in Figure 6-19.

4. The eye height is to be measured at the minimum opening over the range from the center of the eye ± 0.05 UI.

5. The Rj specification is calculated as 14.069 times the RMS random jitter for 10⁻¹² BER.

The compliance testing setup is shown in Figure 6-19. All measurements are made at the test point (TP1), and the Tx specifications are applied after processing the measured data with the compliance reference equalizer transfer function described in the next section.

![img-142.jpeg](img-142.jpeg)

U-026

Figure 6-19. Tx Normative Setup with Reference Channel

### 6.7.4 Tx Compliance Reference Receiver Equalize Function

The normative transmitter eye is captured at the end of the reference channel. At this point the eye may be closed. To open the eye so it can be measured a reference Rx equalizer, is applied to the signal. Details of the reference equalizer are contained in Section 6.8.2.

6-32

Physical Layer

### 6.7.5 Informative Transmitter De-emphasis

#### 6.7.5.1 Gen 1 (5GT/s)

The channel budgets and eye diagrams were derived using a V_TX-DE-RATIO of transmit de-emphasis for both the Host and the Device reference channels. An example differential peak-to-peak de-emphasis waveform is shown in Figure 6-20.

![img-143.jpeg](img-143.jpeg)

Figure 6-20. De-Emphasis Waveform

#### 6.7.5.2 Gen 2 (10GT/s)

Gen 2 transmitters employ a 3-tap FIR-based equalizer, the structure of which is shown in Figure 6-21. An example waveform from the 3-tap equalizer is shown in Figure 6-22. In the figure, the pre-cursor (Vc) is referred to as pre-shoot, while the post-cursor (Vb) is referred to as de-emphasis. This convention allows pre-shoot and de-emphasis to be defined independently of one another. The maximum swing, Vd, is also shown to illustrate that, when both C+1 and C-1 are nonzero, the swing of Va does not reach the maximum as defined by Vd. Figure 6-22 is shown as an example of TxEQ and is not intended to represent the signal as it would appear for measurement purposes.

Table 6-20 provides recommended (informative) tap coefficient values (C-1 and C1) along with the corresponding pre-shoot, de-emphasis and output amplitudes. The host/device loss referred to in the table refers to the differential insertion loss in the conductor path from the silicon die pad to the connector, and includes parasitic I/O capacitance, the chip package (routing, vias and I/O pins), and printed circuit board (routing and vias).

6-33

Universal Serial Bus 3.1 Specification, Revision 1.0

![img-144.jpeg](img-144.jpeg)

Figure 6-21. 3-tap Transmit Equalizer Structure

![img-145.jpeg](img-145.jpeg)

Preshoot = 20log(Vc/Vb)
De-emphasis = 20log(Vb/Va)

Figure 6-22. Example Output Waveform for 3-tap Transmit Equalizer

6-34

Physical Layer

Table 6-20. Informative Gen 2 Transmitter Equalization Settings

[tbl-73.md](tbl-73.md)

### 6.7.6 Entry into Electrical Idle, U1

Electrical Idle is a steady state condition where the Transmitter Txp and Txn voltages are held constant at the same value and the Receiver Termination is within the range specified by Z$_{RX-DC}$. Electrical Idle is used in the power saving state of U1.

The low impedance common mode and differential Receiver terminations values (see Table 6-21) must be met in Electrical Idle. The Transmitter can be in either a low or high impedance mode during Electrical Idle.

## 6.8 Receiver Specifications

### 6.8.1 Receiver Equalization Training

The receiver equalization training sequence, detailed in Section 6.4.1.1 for Gen 1 operation and in Section 6.4.1.2 for Gen 2 operation, can be used to train the receiver equalizer. The TSEQ training sequence is designed to provide spectrally rich data patterns that are useful for training typical receiver equalization architectures. For Gen 1 operation, a high edge density pattern is interleaved with the data to help the CDR maintain bit lock. For Gen 2 operation the sequence is deemed sufficiently rich on its own.

During Gen 1 operation the TSEQ training sequence repeats 65536 times to allow for testing many coefficient settings. Also during Gen 1 operation no SKPs are inserted during the TSEQ training sequence. The frequency spectrum of the TSEQ sequence is shown in Figure 6-23.

During Gen 2 operation, the training period is ~8ms. The training pattern is periodic with a period of 16384 132-bit blocks (2162688UI). The much longer pattern greatly increases the richness of the pattern compared to Gen 1. The Gen 2 training pattern spectrum is essentially white. Due to the length of the Gen 2 training interval and the potential desire to examine the data, SKPs are inserted during polling.TSEQ.

Receiver equalization training is implementation specific.

6-35

Universal Serial Bus 3.1 Specification, Revision 1.0

![img-146.jpeg](img-146.jpeg)

Figure 6-23. Frequency Spectrum of TSEQ

### 6.8.2 Informative Receiver CTLE Function

USB 3.1 allows the use of receiver equalization to meet system timing and voltage margins. For long cables and channels the eye at the Rx is closed, and there is no meaningful eye without first applying an equalization function. The Rx equalizer may be required to adapt to different channel losses using the Rx EQ training period. The exact Rx equalizer and training method is implementation specific.

#### 6.8.2.1 Gen 1 Reference CTLE

The equation for the continuous time linear equalizer (CTLE) used to develop the specification is the compliance Rx EQ transfer function described below.

$$H(s) = \frac{A_{dc} \omega_{p1} \omega_{p2}}{\omega_z} \cdot \frac{s + \omega_z}{(s + \omega_{p1})(s + \omega_{p2})}$$

where $A_{dc}$ is the DC gain

$\omega_z = 2\pi f_z$ is the zero frequency

$\omega_{p1} = 2\pi f_{p1}$ is the first pole frequency

$\omega_{p2} = 2\pi f_{p2}$ is the second pole frequency

Figure 6-24 is a plot of the Compliance EQ transfer functions with the values for each of the input parameters.

6-36

Physical Layer

![img-147.jpeg](img-147.jpeg)

Figure 6-24. Gen 1 Tx Compliance Rx EQ Transfer Function

### 6.8.2.2 Gen 2 Reference Equalizer Function

#### 6.8.2.2.1 Reference CTLE

Equation (11) describes the frequency response for the Gen 2 reference continuous time linear equalizer (CTLE) that is used for compliance testing. The equation describes the same first order CTLE as contained in equation (10).

$$H(s) = A_{ac} \omega_{p2} \frac{s + \frac{A_{dc}}{A_{ac}} \omega_{p1}}{(s + \omega_{p1})(s + \omega_{p2})}$$

where $A_{ac}$ is the high frequency peak gain

$A_{dc}$ is the DC gain

$\omega_{p1} = 2\pi f_{p1}$ is the first pole frequency

$\omega_{p2} = 2\pi f_{p2}$ is the second pole frequency

6-37

Universal Serial Bus 3.1 Specification, Revision 1.0

Figure 6-25 is a plot of the Compliance EQ transfer functions with the values for each of the input parameters.

![img-148.jpeg](img-148.jpeg)

Figure 6-25. Gen 2 Compliance Rx EQ Transfer Function

### 6.8.2.2.2 Reference DFE

In addition to the 1st order CTLE, a one-tap reference DFE is used in transmitter compliance testing. The DFE behavior is described by equation (12) and Figure 6-26. The limits on dI are 0 to 50mV.

(12) $$y_k = x_k - d_1 \operatorname{sgn}(y_{k-1})$$

where yk is the DFE differential output voltage

y*k is the decision function output voltage, |y*k| = 1

xk is the DFE differential input voltage

dI is the DFE feedback coefficient

k is the sample index in UI

6-38

Physical Layer

![img-149.jpeg](img-149.jpeg)

Figure 6-26. Gen 2 reference DFE Function

### 6.8.3 Receiver Electrical Parameters

Normative specifications are to be measured at the connector. Peak (p) and peak- peak (p-p) are defined in Section 6.6.2.

Table 6-21. Receiver Normative Electrical Parameters

[tbl-74.md](tbl-74.md)

Note

1. Only DC Input CM Input Impedance for V >0 is specified. DC Input CM Input Impedance for V <0 is not guaranteed and could be as low as 0 Ω.

The values in Table 6-22 are informative and not normative. They are included in this document to provide some guidance beyond the normative requirements in Table 6-21 for receiver design and development. A receiver can be fully compliant with the normative requirements of the

6-39

Universal Serial Bus 3.1 Specification, Revision 1.0

specification and not meet all the values in this table (many of which are not measurable in a finished product). Similarly, a receiver that meets all the values in this table is not guaranteed to be in full compliance with the normative part of this specification.

Table 6-22. Receiver Informative Electrical Parameters

[tbl-75.md](tbl-75.md)

### 6.8.4 Receiver Loopback

The entry and exit process for receiver loopback is described in Chapter 7.

Receiver loopback must be retimed. Direct connection from the Rx amplifier to the transmitter is not allowed for loopback mode. The receiver shall continue to process SKPs as appropriate. SKP symbols shall be consumed or inserted as required for proper clock tolerance compensation. Over runs or under runs of the clock tolerance buffers will reset the buffers to the neutral position.

During loopback the receiver shall process the Bit Error Rate Test (BERT) commands.

Loopback shall occur in the 10-bit domain for Gen 1 operation and in the 132-bit domain for Gen 2 operation. No error correction is allowed. All symbols shall be transmitted as received with the exception of SKP and BERT commands.

#### 6.8.4.1 Loopback BERT for Gen 1 Operation

During loopback the receiver processes the BERT ordered sets BRST, BDAT, and BERC. These ordered sets are described in Table 6-23 through Table 6-26. BRST and BDAT are looped back as received. BERC ordered sets are not looped back but are replaced with BCNT ordered sets. Any time a BRST is received, the error count register EC is set to 0 and the scrambling LFSR is set to 0FFFFh. Any number of consecutive BRST ordered sets may be received.

6-40

Physical Layer

BRST followed by BDAT starts the bit error rate test. The BDAT sequence is the output of the scrambler and is equivalent to the logical idle sequence. It consists of scrambled 0 as described in Appendix B. As listed in Appendix B, the first 16 characters of the sequence are reprinted here:

[tbl-76.md](tbl-76.md)

The receiver shall compare the received data to the BDAT sequence. Errors increment the error count register (EC) by 1. EC may not roll over but shall be held at FFh. The LFSR is advanced once for every character except SKPs. The LFSR rolls over after 2¹⁶-1 symbols. SKPs shall be inserted or deleted as necessary for clock tolerance compensation.

The BERC command does not increment the error count register. The LFSR is advanced. The BERC ordered set is replaced by the BCNT ordered set. The BCNT ordered set includes the non-scrambled 8b/10b encoded error count (EC) register based on the running disparity. Following the return of the BCNT ordered set, the loopback slave shall continue to repeat symbols as received.

BERC may be sent multiple times. The EC register is not cleared by BERC ordered sets.

BERT continues until the loopback mode is terminated as described in Chapter 7.

Table 6-23. BRST

[tbl-77.md](tbl-77.md)

Table 6-24. BDAT

[tbl-78.md](tbl-78.md)

Table 6-25. BERC

[tbl-79.md](tbl-79.md)

Table 6-26. BCNT

[tbl-80.md](tbl-80.md)

6-41

Universal Serial Bus 3.1 Specification, Revision 1.0

### 6.8.5 Normative Receiver Tolerance Compliance Test

The receiver tolerance test is tested using the appropriate compliance reference channel for Gen 1 or Gen 2 operation depending upon the rate being tested. A pattern generator shall send the rate appropriate compliance test pattern with added jitter through the compliance reference channels to the receiver. The receiver shall loop back the data and any difference in the pattern sent from the pattern generator and returned will be an error. When running the compliance tests, the receiver shall be put into loopback mode.

Additional details on the receiver compliance test are contained in the reference document, USB SuperSpeed Compliance Methodology.

![img-150.jpeg](img-150.jpeg)

Figure 6-27. Rx Tolerance Setup

![img-151.jpeg](img-151.jpeg)

Figure 6-28. Jitter Tolerance Curve

6-42

Physical Layer

The jitter components used to test the receiver shall meet the requirements of Table 6-27.

Table 6-27. Input Jitter Requirements for Rx Tolerance Testing

[tbl-81.md](tbl-81.md)

Notes:

1. All parameters measured at TP1. The test point is shown in Figure 6-19.

2. Due to time limitations at compliance testing, only a subset of frequencies can be tested. However, the Rx is required to tolerate Pj at all frequencies between the compliance test points.

3. During the Rx tolerance test, SSC is generated by test equipment and present at all times. Each J$_{Pi}$ source is then added and tested to the specification limit one at a time.

4. Random jitter is also present during the Rx tolerance test, though it is not shown in Figure 6-20.

5. The JTOL specs for Gen 2 comprehend jitter peaking with re-timers in the system and has a 25dB/decade slope.

## 6.9 Low Frequency Periodic Signaling (LFPS)

Low frequency periodic signaling (LFPS) is used for side band communication between the two ports across a link that is in a low power link state. It is also used when a link is under training, or when a downstream port issues Warm Reset to reset the link.

### 6.9.1 LFPS Signal Definition

Table 6-28 defines the LFPS electrical specification at the transmitter. An example differential LFPS waveform is shown in Figure 6-29. tPeriod is the period of an LFPS cycle. An LFPS burst is the transmission of continuous LFPS signal over a period of time defined by tBurst. An LFPS sequence is defined by the transmission of a single LFPS burst of duration tBurst over a period of time defined by tRepeat. The link is in electrical idle between the two contiguous LFPS bursts.

6-43

Universal Serial Bus 3.1 Specification, Revision 1.0

An LFPS message is encoded based on the variation of tBurst. tRepeat is defined as a time interval when the next LFPS message is transmitted. The LFPS messages include Polling.LFPS and Ping.LFPS, as defined in Table 6-29. There are also LFPS signaling defined by a for U1/U2 and Loopback exit, U3 wakeup, and Warm Reset.

The detailed use of LFPS signaling is specified in the following sections and Chapter 7.

![img-152.jpeg](img-152.jpeg)

Figure 6-29. LFPS Signaling

Table 6-28. Normative LFPS Electrical Specification

[tbl-82.md](tbl-82.md)

6-44

Physical Layer

Table 6-29. LFPS Transmitter Timing for SuperSpeed Designs¹

[tbl-83.md](tbl-83.md)

Notes:

1. If the transmission of an LFPS signal does not meet the specification, the receiver behavior is undefined.

2. Only Ping.LFPS has a requirement for minimum number of LFPS cycles.

3. The declaration of Ping.LFPS depends on only the Ping.LFPS burst.

4. Warm Reset, U1/U2/Loopback Exit, and U3 Wakeup are all single burst LFPS signals. tRepeat is not applicable.

5. The minimum duration of an LFPS burst shall be transmitted as specified. The LFPS handshake process and timing are defined in Section 6.9.2.

6. A Port in U2 or U3 is not required to keep its transmitter DC common mode voltage. When a port begins U2 exit or U3 wakeup, it may start sending LFPS signal while establishing its transmitter DC common mode voltage. To make sure its link partner receives a proper LFPS signal, a minimum of 80 μs tBurst shall be transmitted. The same consideration also applies to a port receiving LFPS U2 exit or U3 wakeup signal.

7. A port is still required to detect U1 LFPS exit signal at a minimum of 300ns. The extra 300ns is provided as the guard band for successful U1 LFPS exit handshake.

8. This requirement applies to SuperSpeed only designs (are only capable of operating at 5Gb/s).

9. This requirement applies to SuperSpeedPlus designs (capable of operating at 10Gb/s and higher speeds).

### IMPLEMENTATION NOTE

Detect and differentiate between Ping.LFPS and U1 LFPS exit signaling for a downstream port in U1 or U2

When a downstream port is in U1, it may receive either a Ping.LFPS as a message from its link partner to inform its presence, or an U1 LFPS exit signal to signal that its link partner is attempting exit from U1. This will also occur when a downstream port is in U2, since there are situations where a downstream port enters U2 from U1 when its U2 inactivity timer times out, and its link partner is still in U1.

Upon detecting the break of electrical idle due to receiving an LFPS signal, a downstream port may start a timer to measure the duration of the LFPS signal. If an electrical idle condition does not occur when the timer expires at 300 ns, a downstream port can declare the received LFPS signal is U1 exit and then respond to U1 exit by sending U1 LFPS exit handshake signal. If an electrical idle condition is detected before the timer reaches 300 ns, a downstream port can declare that the received LFPS signal is Ping.LFPS.

6-45

Universal Serial Bus 3.1 Specification, Revision 1.0

### 6.9.2 Example LFPS Handshake for U1/U2 Exit, Loopback Exit, and U3 Wakeup

The LFPS signal used for U1/U2 exit, Loopback exit, and U3 wakeup is defined the same as continuous LFPS signals with the exception of timeout values defined in Table 6-30. The handshake process for U1/U2 exit and U3 wakeup is illustrated in Figure 6-30. The timing requirements are different for U1 exit, U2 exit, Loopback exit, and U3 wakeup. They are listed in Table 6-30.

![img-153.jpeg](img-153.jpeg)

t10 – When Link Partner 1 starts to transmit LFPS, in initiating exit from either U1/U2/U3/Loopback.
t11 – When Link Partner 2 validates the received LFPS for the required t11-t10 duration and starts to transmit LFPS in response.
t12 – When Link Partner 1 validates the received LFPS of the required t12-t11 and t12-t10 durations and starts to transmit SS signaling.
t13 – When Link Partner 2 transmits LFPS of meeting the required t13-t11 duration and starts to transmit SS signaling.

U-033A

Figure 6-30. U1 Exit, U2 Exit, and U3 Wakeup LFPS Handshake Timing Diagram

Note: the timing diagram in Figure 6-22 is for illustration of the LFPS handshake process only.

The handshake process is as follows:

- Link partner 1 initiates exit by transmitting LFPS at time t10 (see Figure 6-30). LFPS transmission shall continue until the handshake is declared either successful or failed.
- Link partner 2 detects valid LFPS on its receiver and responds by transmitting LFPS at time t11. LFPS transmission shall continue until the handshake is declared either successful or failed.
- A successful handshake is declared for link partner 1 if the following conditions are met within “tNoLFPSResponseTimeout” after t10 (see Figure 6-30 and Table 6-30):

1. Valid LFPS is received from link partner 2.

Note: in case of concurrent U1 exit, where both ports initiate U1 exit simultaneously, both ports will assume to be Link partner 1. Both ports will start receiving LFPS signal before

6-46

Physical Layer

t10. And received U1 LFPS exit signal may be validated around t10. This may result in a minimum duration of U1 exit LFPS signal. To ensure successful U1 exit under such situations, both ports shall transmit U1 LFPS exit signal for 600ns before exiting U1.

2. For U1 exit, U2 exit, U3 Wakeup and not Loopback exit, link partner 1 is ready to transmit the training sequences and the maximum time gap after an LFPS transmitter stops transmission and before a SuperSpeed transmitter starts transmission is 20 ns.

Note: There is no Near End Cross Talk (NEXT) specification for SuperSpeed transmitters and receivers. Therefore, when a port enters Recovery and starts transmitting TS1 Ordered Sets and its link partner is in electrical idle after successful LFPS handshake, a port may potentially train its receiver using its own TS1 Ordered Sets due to NEXT. The intention of adding the second exit condition is to prevent a port from electrical idle before transitioning to Recovery.

- A successful handshake is declared for link partner 2 if the following conditions are met:

1. Link partner 2 has transmitted the minimum LFPS defined as (t13 – t11) in Table 6-30.
2. For U1 exit, U2 exit, U3 Wakeup, and not Loopback exit, link partner 2 is ready to transmit the training sequences and the maximum time gap after an LFPS transmitter stops transmission and before a SuperSpeed transmitter starts transmission is 20 ns.

- A U1 exit, U2 exit, Loopback exit, and U3 wakeup handshake failure shall be declared if the conditions for a successful handshake are not met.
- Link partner 1 shall declare a failed handshake if its successful handshake conditions were not met.
- Link partner 2 shall declare a failed handshake if its successful handshake conditions were not met.

Note: Except for Ping.LFPS, when an upstream port in Ux or Loopback.Active receives an LFPS signal, it shall proceed with U1/U2 exit, or U3 wakeup, or Loopback exit handshake even if the LFPS is later determined to be a Warm Reset. If the LFPS is a Warm Reset, an upstream port, if in Ux, will enter Recovery and then times out to SS.Inactive, or if in Loopback Active, will enter Rx.Detect and then transitions to Polling.LFPS. When Warm Reset is detected, an upstream port will enter Rx.Detect.

Table 6-30. LFPS Handshake Timing for U1/U2 Exit, Loopback Exit, and U3 Wakeup

[tbl-84.md](tbl-84.md)

Note:

1. There are two sets of maximum timing requirements. The set with short timing requirement applies to normal operations when U2_Inactivity_Timer is disabled. The set with relaxed timing requirement applies to operations when U2_Inactivity_Timer is enabled. It also includes one corner case where U2_Inactivity_Timer is disabled and the port, upon entry to U1, initiating U1 exit immediately.

2. In a case where U2_Inactivity_Timer is enabled, it is the responsibility of each link partner to respond accordingly depending on its U1 or U2 state. For example, when link partner 1 initiates exit in U1 and link partner 2 is in U2, it is expected that both link partners will eventually enter U0 with respective timings starting from different U1/U2 states.

6-47

Universal Serial Bus 3.1 Specification, Revision 1.0

Essentially, t12-t10 of link partner 1 follows U1 Exit tBurst timing and t13-t11 of link partner 2 follows U2 Exit tBurst timing.

### 6.9.3 Warm Reset

A Warm Reset is a reset generated only by a downstream port to an upstream port. A downstream port may issue a Warm Reset at any Link states except SS.Disabled. An upstream port is required to detect a Warm Reset at any link states except SS.Disabled.

Note: Warm Reset is defined to be able to reset a hardware failure of a device, such as the LTSSM hanging. Under this assumption, Warm Reset may be detected in any link states except SS.Disabled.

A Warm Reset shares the same continuous LFPS signal as a low power Link state exit handshake signal. In order for an upstream port to be able to differentiate between the two signals, the tBurst of a Warm Reset is extended, as is defined in Table 6-20.

The Warm Reset assertion is asynchronous between a downstream port and an upstream port since it has to take a certain period of time for an upstream port to declare that a Warm Reset is detected. However, the de-assertion of the Warm Reset between a downstream port and an upstream port shall be made synchronous. Figure 6-31 shows a timing diagram of Warm Reset generation and detection when a port is U3. Once a Warm Reset is issued by a downstream port, it will take at least tResetDelay for an upstream port to declare the detection of Warm Reset. Once a Warm Reset is detected, an upstream port shall continue to assert the Warm Reset until it no longer receives any LFPS signals from a downstream port.

- An upstream port shall declare the detection of Warm Reset within tResetDelay. The minimum tResetDelay shall be 18 ms; the maximum tResetDelay shall be 50 ms.

![img-154.jpeg](img-154.jpeg)

Figure 6-31. Example of Warm Reset Out of U3

### 6.9.4 SuperSpeedPlus Capability Declaration

SuperSpeedPlus Capability Declaration (SCD) is a step for a SuperSpeedPlus port, while in the Polling.LFPS substate, to identify itself as SuperSpeedPlus capable by transmitting Polling.LFPS signals with specific patterns unique to SuperSpeedPlus ports. This section defines SuperSpeedPlus specific patterns in SCD1 and SCD2. The use of SCD1 and SCD2 is described in Chapter 7.

6-48

Physical Layer

### 6.9.4.1 Binary Representation of Polling.LFPS

Binary representation of Polling.LFPS refers to logic presentation based on Polling.LFPS signal by the measure of tRepeat duration. As shown in Table 6-31, logic '0' is represented with tRepeat varying between 6~9us, and logic '1' is represented with tRepeat varying between 11~14us. tRepeat between 9~11us is defined as a guard band.

Figure 6-32 is an example of Polling.LFPS based binary representation in the time domain.

Table 6-31. Binary Representation of Polling.LFPS

[tbl-85.md](tbl-85.md)

![img-155.jpeg](img-155.jpeg)

Figure 6-32. Example of Binary Representation based on Polling.LFPS

### 6.9.4.2 SCD1/SCD2 Definitions and Transmission

SCD1 is defined as "0010" and SCD2 is defined as "1101". The transmission of SCD1/SCD2 shall be based on the following.

- The transmission shall be LSb first, and consecutive SCD1/SCD2 shall be transmitted back to back.
- The transmission shall be completed with and extra tBurst followed by electrical idle (EI) of at least 2x the maximum allowable tRepeat value.

Figure 6-33 is an example of SCD1/SCD2 waveform in the time domain.

6-49

Universal Serial Bus 3.1 Specification, Revision 1.0

![img-156.jpeg](img-156.jpeg)

![img-157.jpeg](img-157.jpeg)

Figure 6-33. SCD1/SCD2 transmission

6-50

Physical Layer

### 6.9.5 SuperSpeedPlus LFPS Based PWM Message (LBPM)

LBPM is defined as a low power signaling mechanism for two SuperSpeedPlus ports to communicate with each other based on LFPS signals. The adoption of Pulse Width Modulation (PWM) is to embed the transmitting clock in data and to allow for easy data recovery at the receiver based on LFPS clock defined in Table 6-28. This section describes the concept and construction of LBPM. Refer to Chapter 7 for use of LBPM.

#### 6.9.5.1 Introduction to LFPS Based PWM Signaling (LBPS)

LBPS is based on PWM with embedded transmit clock and is basically constructed with two distinctive electrical states, which are LFPS signaling state and EI state. As is shown in Figure 6-34, two logic states are defined based on LBPS.

- Logic '0' is defined within the unit interval of tPWM as one-third of LFPS signal followed by two-third of EI.
- Logic '1' is defined within the unit interval of tPWM as two-third of LFPS signal followed by one-third of EI.

The specification of the transmit and receive LBPS is defined in Table 6-32.

![img-158.jpeg](img-158.jpeg)

Figure 6-34. Logic Representation of LBPS

Table 6-32. LBPS Transmit and Receive Specification

[tbl-86.md](tbl-86.md)

6-51

Universal Serial Bus 3.1 Specification, Revision 1.0

### 6.9.5.2 LBPM Definition and Transmission

LBPM is byte based with LSb transmitted first. A port may transmit a single LBPM, or consecutive LBPMs. The transmission of LBPM shall adhere to the following conventions.

- A LBPM delimiter is defined with one tPWM of LFPS followed by one tPWM of EI.
- The LPBM transmission shall start with a LBPM delimiter.
- The LBPM transmission shall end with a LBPM delimiter.
- The transmission of LBPM shall be LSb first.
- Consecutive LBPM transmission shall be LSB first with LBPM delimiter in between each LBPMs.

Examples of LBPM transmission are shown in Figure 6-35.

![img-159.jpeg](img-159.jpeg)

(a). Single LBPM Transmission

![img-160.jpeg](img-160.jpeg)

(b). Consecutive LBPMs Transmitted Back to Back

Figure 6-35. LBPM Transmission Examples

6-52

Physical Layer

## 6.10 Transmitter and Receiver DC Specifications

### 6.10.1 Informative ESD Protection

It is recommended that all signal and power pins withstand a minimum ESD value using the human body model and the charged device model, without damage, as defined by the semiconductor industry.

This is a suggested ESD tolerance. The ASIC designer is expected to apply current technology and knowledge of ESD prevention circuits to protect from environmental hazards that could create long term failure, and possibly, catastrophic failure in a system. It is up to the designer to use good design practices to implement appropriate ESD protection. With ESD protection in place, the ASIC design shall meet the other electrical requirements of this specification.

### 6.10.2 Informative Short Circuit Requirements

All Transmitters and Receivers shall support surprise hot insertion/removal without damage to the component. The Transmitter and Receiver shall be capable of withstanding sustained short circuit to ground of Txp (Rxp) and Txn (Rxn).

### 6.10.3 Normative High Impedance Reflections

During an asynchronous reset event, one device may be reset while the other device is transmitting. The device under reset is required to disconnect the receiver termination. During this time, the device under reset may be receiving active data. Since the data is not terminated, the differential voltage into the receiver will be doubled. For a short channel, the receiver may experience a total of 2* VDIFF.

The receiver shall tolerate this doubling of the negative voltage that can occur if the Rx termination is disconnected. A part shall tolerate a 20 ms event that doubles the voltage on the receiver input when the termination is disconnected 10,000 times over the life time of the part.

## 6.11 Receiver Detection

### 6.11.1 Rx Detect Overview

The Receiver Detection circuit is implemented as part of a Transmitter and shall correctly detect whether a load impedance equivalent to a DC impedance RRX-DC (Table 6-21) is present. The Rx detection operates on the principle of the RC time constant of the circuit. This time constant changes based on the presence of the receiver termination. This is conceptually illustrated in Figure 6-36. In this figure, R_Detect is the implementation specific charging resistor. C_AC is the AC capacitor that is in the circuit only if R_Term is also present, otherwise, only C_Parasitic is present.

6-53

Universal Serial Bus 3.1 Specification, Revision 1.0

![img-161.jpeg](img-161.jpeg)

![img-162.jpeg](img-162.jpeg)

U-035

Figure 6-36. Rx Detect Schematic

The left side of Figure 6-36 shows the Receiver Detection circuit with no termination present. The right side of the figure is the same circuit with termination.

Detect voltage transition must be common mode. Detect voltage transition shall conform to V_TX_RCV_DETECT as described in Table 6-17.

The receiver detect sequence shall be in the positive common mode direction only. Negative receiver detection is not allowed.

### 6.11.2 Rx Detect Sequence

The recommended behavior of the Receiver Detection sequence is:

1. A Transmitter shall start at a stable voltage prior to the detect common mode shift.
2. A Transmitter changes the common mode voltage on Txp and Txn consistent with detection of Receiver high impedance which is bounded by parameter Z_RX-HIGH-IMP-DC-POS listed in Table 6-21.
3. A Receiver is detected based on the rate that the lines change to the new voltage.

- The Receiver is not present if the voltage at the Transmitter charges at a rate dictated only by the Transmitter impedance and the capacitance of the interconnect and series capacitor.
- The Receiver is present if the voltage at the Transmitter charges at a rate dictated by the Transmitter impedance, the series capacitor, the interconnect capacitance, and the Receiver termination.

Any time Electrical Idle is exited the detect sequence does not have to execute or may be aborted. During the Device connect, the Device receiver has to guarantee it is always in high impedance state while its power plane is stabilizing. This is required to avoid the Host falsely detecting the Device and starting the training sequence before the Device is ready. Similarly a disabled port has to keep its receiver termination in high impedance which is bounded by parameters Z_RX-HIGH-IMP-DC-POS until directed by higher layer to exit from the Disabled state. In contrast, a port which is at U1/U2/U3 Electrical Idle shall have its Receiver Termination turned on and meet the R_RX-DC specification.

6-54

Physical Layer

### 6.11.3 Upper Limit on Channel Capacitance

The interconnect total capacitance to ground seen by the Receiver Detection circuit shall not exceed 3 nF to ground, including capacitance added by attached test instrumentation. This limit is needed to guarantee proper operation during Receiver detect. Note that this capacitance is separate and distinct from the AC coupling capacitance value.

### 6.12 Retimers

Requirements for estimers are defined in Appendix E.

6-55

Universal Serial Bus 3.1 Specification, Revision 1.0

6-56

# 7 Link Layer

The Enhanced SuperSpeed USB consists of SuperSpeed USB operating at the Gen 1 speed, and SuperSpeedPlus USB operating at the Gen 2 speed. The link layer of the Enhanced SuperSpeed USB has the responsibility of maintaining the link connectivity so that successful data transfers between the two link partners are ensured. A robust link flow control is defined based on packets and link commands. Packets are prepared in the link layer to carry data and different information between the host and a device. Link commands are defined for communications between the two link partners. Packet frame ordered sets and link command ordered sets are also constructed such that they are tolerant to one symbol error. In addition, error detection capabilities are also incorporated into a packet and a link command to verify packet and link command integrity.

![img-163.jpeg](img-163.jpeg)

Figure 7-1. Link Layer

The link layer also facilitates link training, link testing/debugging, and link power management. This is accomplished by the introduction of Link Training Status State Machine (LTSSM).

The focus of this chapter is to address the following in detail:

- Packet Framing
- Link command definition and usage
- Link initialization and flow control
- Link power management
- Link error rules/recovery
- Resets
- LTSSM specifications

7-1

Universal Serial Bus 3.1 Specification

## 7.1 Byte Ordering

Multiple byte fields in a packet or a link command are moved over to the bus in little-endian order, i.e., the least significant byte (LSB) first, and the most significant byte (MSB) last. Figure 7-2 shows an example of byte ordering.

![img-164.jpeg](img-164.jpeg)

Figure 7-2. Byte Ordering

### 7.1.1 SuperSpeed USB Line Code

Each byte of a packet or link command will be encoded in the physical layer using 8b/10b encoding. Refer to Section 6.3.1.3 regarding 8b/10b encoding and bit ordering.

### 7.1.2 SuperSpeedPlus USB Line Code

To improve the effective throughput for SuperSpeedPlus USB, 128b/132b line code is employed to replace 8b/10b line code used in SuperSpeed USB. Two block types are defined based on 128b/132b line code. A control block is defined to transmit TSEQ, TS1, TS2, SYNC, SDS, and SKP ordered sets. A data block is defined to transmit packets, link commands, and Idle Symbols. Refer to Section 6.3 for 128b/132b block definition and bit ordering. Each symbol within a data block is scrambled by default, unless disabled otherwise by the Disabling Scrambling bit asserted in the TS2 ordered set received in Polling.Configuration or Recovery.Configuration. Refer to Sections 7.5.4.9 and 7.5.10.4 for details.

7-2

Link Layer

## 7.2 Link Management and Flow Control

This section contains information regarding link data integrity, flow control, and link power management.

- The packet and packet framing section defines packet types, packet structures, and CRC requirements for each packet.
- The link command section defines special link command structures that control various functionalities at the link level.
- The logical idle defines a special symbol used in U0.
- The flow control defines a set of handshake rules for packet transactions.

### 7.2.1 Packets and Packet Framing

The Enhanced SuperSpeed USB uses packets to transfer information. Detailed packet formats for Link Management Packets (LMP), Transaction Packets (TP), Isochronous Timestamp Packets (ITP), and Data Packets (DP) are defined in Section 8.2.

#### 7.2.1.1 Header Packet Structure

For SuperSpeed USB, all header packets are 20 symbols long, as is formatted in Figure 7-3. This includes LMPs, TPs, ITPs, and DPHs. A header packet consists of three parts, a header packet framing, a packet header, and a Link Control Word.

For SuperSpeedPlus USB, all header packets except for non-deferred DPH are the same as SuperSpeed USB. The non-deferred SuperSpeedPlus DPH is a header packet with its own framing ordered set, and contains a length field replica immediately after the Link Control word. The purpose of this special construction is to allow the non-deferred SuperSpeedPlus DPH to be processed differently from all other header packets and to achieve single bit error tolerance in its length field. The non-deferred SuperSpeedPlus DPH format is shown in Figure 7-4.

##### 7.2.1.1.1 Header Packet Framing

Header packet framing, HPSTART ordered set, is a four-symbol header packet starting frame ordered set. For SuperSpeed USB, it is defined as three consecutive K symbols of SHP followed by a single K-symbol of EPF. For SuperSpeedPlus USB, HPSTART ordered set is the framing ordered set for all header packets except for non-deferred DPH, and is defined as three consecutive symbols of SHP followed by a single symbol of EPF. A non-deferred SuperSpeedPlus DPH uses DPHSTART ordered set, which is defined as three consecutive symbols of DPHP followed by a single symbol of EPF. Refer to Table 6-1 for framing symbol definition.

- All header packets except for non-deferred SuperSpeedPlus data packet header shall always begin with HPSTART ordered set.
- A non-deferred SuperSpeedPlus data packet header shall always begin with DPHSTART ordered set.
- A deferred SuperSpeedPlus data packet header shall always begin with HPSTART ordered set and it shall contain the length field replica.

The construction of the header packet framing is to achieve one symbol error tolerance.

7-3

Universal Serial Bus 3.1 Specification

![img-165.jpeg](img-165.jpeg)

Figure 7-3. Enhanced SuperSpeed Header Packet with HPSTART, Packet Header, and Link Control Word

![img-166.jpeg](img-166.jpeg)

Figure 7-4. SuperSpeedPlus DPH Format

7-4

Link Layer

### 7.2.1.1.2 Packet Header

A packet header consists of 14 bytes as formatted in Figure 7-5. It includes 12 bytes of header information and a 2-byte CRC-16. CRC-16 is used to protect the data integrity of the 12-byte header information.

![img-167.jpeg](img-167.jpeg)

Figure 7-5. Packet Header

The implementation of CRC-16 on the packet header is defined below:

- The polynomial for CRC-16 shall be 100Bh.
Note: The CRC-16 polynomial is not the same as the one used for USB 2.0.
- The initial value of CRC-16 shall be FFFFh.
- CRC-16 shall be calculated for all 12 bytes of the header information, not inclusive of any packet framing symbols.
- CRC-16 calculation shall begin at byte 0, bit 0 and continue to bit 7 of each of the 12 bytes.
- The remainder of CRC-16 shall be complemented.
- The residual of CRC-16 shall be F6AAh.

Note: The inversion of the CRC-16 remainder adds an offset of FFFFh that will create a constant CRC-16 residual of F6AAh at the receiver side.

Figure 7-6 is an illustration of CRC-16 remainder generation. The output bit ordering is listed in Table 7-1.

7-5

Universal Serial Bus 3.1 Specification

![img-168.jpeg](img-168.jpeg)

Figure 7-6. CRC-16 Remainder Generation

Table 7-1. CRC-16 Mapping

[tbl-87.md](tbl-87.md)

7-6

Link Layer

### 7.2.1.1.3 Link Control Word

The 2-byte Link Control Word is formatted as shown in Figure 7-7. It is used for both link level and end-to-end flow control.

The Link Control Word shall contain a 3-bit Header Sequence Number, 3-bit Reserved, a 3-bit Hub Depth Index, a Delayed bit (DL), a Deferred bit (DF), and a 5-bit CRC-5.

![img-169.jpeg](img-169.jpeg)

Figure 7-7. Link Control Word

CRC-5 protects the data integrity of the Link Control Word. The implementation of CRC-5 is defined below:

- The CRC-5 polynomial shall be 00101b.
- The Initial value for the CRC-5 shall be 11111b.
- CRC-5 is calculated for the remaining 11 bits of the Link Control Word.
- CRC-5 calculation shall begin at bit 0 and proceed to bit 10.
- The remainder of CRC-5 shall be complemented, with the MSb mapped to bit 11, the next MSb mapped to bit 12, and so on, until the LSb mapped to bit 15 of the Link Control Word.
- The residual of CRC-5 shall be 01100b.

Note: The inversion of the CRC-5 remainder adds an offset of 11111b that will create a constant CRC-5 residual of 01100b at the receiver side.

Figure 7-8 is an illustration of CRC-5 remainder generation.

7-7

Universal Serial Bus 3.1 Specification

![img-170.jpeg](img-170.jpeg)

Figure 7-8. CRC-5 Remainder Generation

### 7.2.1.2 Data Packet Payload Structure

Data packets are a special type of packet consisting of a Data Packet Header (DPH) and a Data Packet Payload (DPP). The DPH is defined in Section 7.2.1.1. The DPP, on the other hand, consists of a data packet payload framing, and a variable length of data followed by 4 bytes of CRC-32. Figure 7-9 describes the format of a DPP.

#### 7.2.1.2.1 Data Packet Payload Framing

DPP framing ordered sets consist of a starting framing ordered set called DPPSTART OS, and one of two ending framing ordered sets called DPPEND OS or DPPABORT OS. As indicated by Figure 7-9, a DPPSTART ordered set, which is a DPP starting frame ordered set, consists of three consecutive symbols of SDP followed by a single symbol of EPF. A DPP ending frame ordered set has two different types. The first type, DPPEND ordered set, is a DPP ending frame ordered set which consists of three consecutive symbol of END followed by a single symbol of EPF. The second type, DPPABORT ordered set, is a DPP aborting frame ordered set which consists of three consecutive symbol of EDB (end of nullified packet) followed by a single symbol of EPF. The DPPEND ordered set is used to indicate a normal ending of a complete DPP. For SuperSpeed USB, the DPPABORT ordered set is used to indicate an abnormal ending of a DPP. For SuperSpeedPlus USB, a DPPABORT OS is used to notify either a partially nullified DPP or nullified DPP.

![img-171.jpeg](img-171.jpeg)

Figure 7-9. Data Packet Payload with CRC-32 and Framing

7-8

Link Layer

### 7.2.1.2.2 Data Packet Payload

The DPP section consists of 0 to 1024 bytes of data payload followed by 4 bytes CRC-32.

CRC-32 protects the data integrity of the data payload. CRC-32 is as follows:

- The CRC-32 polynomial shall be 04C1 1DB7h.
- The CRC-32 Initial value shall be FFFF FFFFh.
- CRC-32 shall be calculated for all bytes of the DPP, not inclusive of any packet framing symbols.
- CRC-32 calculation shall begin at byte 0, bit 0 and continue to bit 7 of each of the bytes of the DPP.
- The remainder of CRC-32 shall be complemented.
- The residual of CRC-32 shall be C704DD7Bh.

Note: The inversion of the CRC-32 remainder adds an offset of FFFF FFFFh that will create a constant CRC-32 residual of C704DD7Bh at the receiver side.

Figure 7-10 is an illustration of CRC-32 remainder generation. The output bit ordering is listed in Table 7-2.

![img-172.jpeg](img-172.jpeg)

Figure 7-10. CRC-32 Remainder Generation

7-9

Universal Serial Bus 3.1 Specification

Table 7-2. CRC-32 Mapping

[tbl-88.md](tbl-88.md)

For SuperSpeed USB, any premature termination of a DPP shall end with a DPPABORT ordered set.

For SuperSpeedPlus USB, a port shall always preserve the DPP boundary by completing the DPP transmission meeting the length field specification defined in its associated DPH except for the following conditions.

1. A downstream port is directed to issue a Warm Reset.

Note: An upstream port, before declaring the detection of Warm Reset, may already enter Recovery.

2. A port is directed to enter Recovery.

Note: A port may also complete the DPP transmission under any of the above conditions.

In all other cases, a port in SuperSpeedPlus operation shall perform one of the following.

- It shall append DPPEND OS upon completing the transmission of DPP.
- In the case of a nullified DPP, it shall append DPPABORT OS immediately after its DPH.

7-10

Link Layer

- In the case of partially nullified DPP, it shall append DPPABORT OS after completing the DPP as defined by the length field in its associated DPH, similar to normal ending of DPP. A port shall fill with Idle Symbols in DPP if intended data for transmission are not available. The condition to transmit a partially nullified DPP is implementation specific.

### 7.2.1.2.3 Data Payload Structure and Spacing between DPH and DPP

There shall be no spacing between a DPH and its corresponding DPP. This is illustrated in Figure 7-11.

![img-173.jpeg](img-173.jpeg)

(a). SuperSpeed DP Format

![img-174.jpeg](img-174.jpeg)

(b). SuperSpeedPlus DP Format

Figure 7-11. Data Packet with Data Packet Header Followed by Data Packet Payload. (a) SuperSpeed DP; (b). SuperSpeedPlus DP

Additional details on how header packets are transmitted and received at the link level are described in Section 7.2.4.

7-11

Universal Serial Bus 3.1 Specification

### 7.2.1.3 SuperSpeedPlus Packet Placement

For SuperSpeedPlus USB, packet placement shall meet the following rules:

- All packets shall be placed in data blocks.
- The placement of a packet may start in any symbol position within a data block, and may cross over to the next consecutive data blocks.

Refer to Appendix D for examples of SuperSpeedPlus packet placement.

### 7.2.2 Link Commands

Link commands are used for link level data integrity, flow control and link power management. Link commands are a fixed length of eight symbols and contain repeated symbols to increase the error tolerance. Refer to Section 7.3 for more details. Link command names have the L-preface to differentiate their link level usage and to avoid confusion with packets.

### 7.2.2.1 Link Command Structure

Link command shall be eight symbols long and constructed with the following format shown in Figure 7-12. The first four symbols, LCSTART, are the link command starting frame ordered set consisting of three consecutive SLCs followed by EPF. The second four symbols consist of a two-symbol link command word and its replica. Table 7-3 summarizes the link command structure.

Table 7-3. Link Command Ordered Set Structure

[tbl-89.md](tbl-89.md)

![img-175.jpeg](img-175.jpeg)

Figure 7-12. Link Command Structure

7-12

Link Layer

### 7.2.2.2 Link Command Word Definition

Link command word is 16 bits long with the 11-bit link command information protected by a 5-bit CRC-5 (see Figure 7-13). The 11-bit link command information is defined in Table 7-4. The calculation of CRC-5 is the same as Link Control Word illustrated in Figure 7-7.

![img-176.jpeg](img-176.jpeg)

Figure 7-13. Link Command Word Structure

7-13

Universal Serial Bus 3.1 Specification

Table 7-4. Link Command Bit Definitions

[tbl-90.md](tbl-90.md)

Link commands are defined for four usage cases. First, link commands are used to ensure the successful transfer of a packet. Second, link commands are used for link flow control. Third, link commands are used for link power management. And finally, special link commands are defined for a port to signal its presence in U0.

Successful header packet transactions between the two link partners require proper header packet acknowledgement. Rx Header Buffer Credit exchange facilitates link flow control. Header packet acknowledgement and Rx Header Buffer Credit exchange are realized using different link

7-14

Link Layer

commands. LGOOD_n (n = 0 to 7) and LBAD are used to acknowledge whether a header packet has been received properly or not. LRTY is used to signal that a header packet is re-sent.

For SuperSpeed USB, LCRD_A, LCRD_B, LCRD_C, and LCRD_D are the link commands used to signal the availability of Rx Header Buffers in terms of Credit.

For SuperSpeedPlus USB, Type 1 and Type 2 traffic classes are defined. Type 1 traffic class, or namely Type 1 packet, includes the following packet types: periodic DPs, TPs, ITPs, and LMPs. Type 2 traffic class, or namely Type 2 packet, includes only the asynchronous DPs. LCRD1_A, LCRD1_B, LCRD1_C, and LCRD1_D are link commands used for Type 1 traffic class to signal the availability of Rx Buffers for Type 1 header packets or data packets in terms of Credit. LCRD2_A, LCRD2_B, LCRD2_C, and LCRD2_D are link commands used for Type 2 traffic class to signal the availability of Rx Buffers for Type 2 packets in terms of Credit.

In the following sections, LCRD_x or LCRD1_x/LCRD2_x is used with x denoting either A, B, C, or D. See Table 7-5 for details. LGOOD_n uses an explicit numerical index called Header Sequence Number to represent the sequencing of a header packet. The Header Sequence Number starts from 0 and is incremented by one based on modulo-8 addition with each header packet. The index corresponds to the received Header Sequence Number and is used for flow control and detection of lost or corrupted header packets.

LCRD_x and LCRD1_x/LCRD2_x use an explicit alphabetical index. The index A, B, C, D, A, B, C... is advanced by one with each header packet being processed and an Rx Header Buffer Credit is available. The index is used to ensure Rx Header Buffer Credits are received in order such that missing of an LCRD_x or LCRD1_x/LCRD2_x can be detected. The index operations of LCRD1_x and LCRD2_x are independent.

LBAD and LRTY do not use indexes.

LGO_U1, LGO_U2, LGO_U3, LAU, LXU, and LPMA are link commands used for link power management.

LDN and LUP are special link commands used by a downstream port and an upstream port to indicate their port presence in U0. The usage of LDN and LUP is described in Table 7-5.

Additional requirements and examples on the use of link commands are found in Section 7.2.4.

Table 7-5. Link Command Definitions

[tbl-91.md](tbl-91.md)

7-15

Universal Serial Bus 3.1 Specification

[tbl-92.md](tbl-92.md)

7-16

Link Layer

### 7.2.2.3 Link Command Placement

The link command placement shall meet the following rules:

- Link commands shall not be placed inside header packet structures (i.e., within LMPs, TPs, ITPs, or DPHs).
- Link commands shall not be placed within the DPP of a DP structure.
- Link commands shall not be placed between the DPH and the DPP.
- Link commands may be placed before and after a header packet with the exception that they shall not be placed in between a DPH and its DPP.
- Multiple link commands are allowed to be transmitted back to back.
- Link commands shall not be sent until all scheduled SKP ordered sets have been transmitted.

Note: Additional rules regarding scheduling of link commands are found in Section 10.9.

For SuperSpeedPlus USB, the link command placement shall meet the following additional rules:

- All link commands shall be placed in data blocks.
- The placement of a link command may start in any symbol position within a data block, and may cross over to the next consecutive data blocks.

Refer to Appendix D for examples of SuperSpeedPlus link command placement.

### 7.2.3 Logical Idle

Logical Idle is defined to be a period of one or more symbol periods when no information (packets or link commands) is being transferred on the link. For SuperSpeed USB, a special D-Symbol (00h), is defined as Idle Symbol (IS). For SuperSpeedPlus USB, a special symbol (5Ah) is defined as Idle Symbol. Idle Symbol shall be transmitted by a port at any time in U0 meeting the logical idle definition.

By default, the IS shall be scrambled according to rules described in Section 6.3.

Table 7-6. Logical Idle Definition

[tbl-93.md](tbl-93.md)

### 7.2.4 Link Command Usage for Flow Control, Error Recovery, and Power Management

Link commands are used for link level header packet flow control, to identify lost/corrupted header packets and to initiate/acknowledge link level power management transitions. The construction and descriptions for each link command are found in Section 7.2.2.

#### 7.2.4.1 Header Packet Flow Control and Error Recovery

Header packet flow control is used for all header packets. It requires each side of the link to follow specific header buffer and transmission ordering constraints to guarantee a successful packet transfer and link interoperability. This section describes, in detail, the rules of packet flow control.

7-17

Universal Serial Bus 3.1 Specification

### 7.2.4.1.1 Initialization

The link initialization refers to initialization of a port once a link transitions to U0 from Polling, Recovery, or Hot Reset. The initialization, for SuperSpeed USB, includes the Header Sequence Number Advertisement and the Rx Header Buffer Credit Advertisement between the two ports before a header packet can be transmitted. For SuperSpeedPlus USB, the initialization includes the Header Sequence Number Advertisement, the Type 1 Rx Buffer Credit Advertisement, and the Type 2 Rx Buffer Credit Advertisement.

- The following requirements shall be applied to a port:

1. A port shall maintain two Tx Header Sequence Numbers. One is the Tx Header Sequence Number that is defined as the Header Sequence Number that will be assigned to a header packet when it is first transmitted (not a re-transmission). The other is the ACK Tx Header Sequence Number that is defined as the expected Header Sequence Number to be acknowledged with LGOOD_n that is sent by a port receiving the header packet.

2. A port shall have an Rx Header Sequence Number. It is defined as the expected Header Sequence Number when a header packet is received.

3. A port in SuperSpeed operation shall maintain two Rx Header Buffer Credit Counts. One is the Local Rx Header Buffer Credit Count that is defined as the number of the available Rx Header Buffer Credits of its receiver. The other is the Remote Rx Header Buffer Credit Count that is defined as the number of the available Rx Header Buffer Credits from its link partner. A port in SuperSpeedPlus operation shall maintain two Type 1 Rx Buffer Credit Counts for Type 1 traffic class. One is the Local Type 1 Rx Buffer Credit Count that is defined as the number of the available Rx Buffer Credits of its receiver. The other is the Remote Type 1 Rx Buffer Credit Count that is defined as the number of the available Rx Buffer Credits from its link partner. A port in SuperSpeedPlus operation shall also maintain two Type 2 Rx Buffer Credit Counts for Type 2 traffic class. One is the Local Type 2 Rx Buffer Credit Count that is defined as the number of the available Rx Buffer Credits of its receiver. The other is the Remote Type 2 Rx Buffer Credit Count that is defined as the number of the available Rx Buffer Credits from its link partner.

4. A port in SuperSpeed operation shall have enough Tx Header Buffers in its transmitter to hold up to four unacknowledged header packets. A port in SuperSpeedPlus operation shall have enough Type 1/Type 2 Tx Header Buffers in its transmitter to hold up to four unacknowledged header packets of Type 1 traffic class, and another four unacknowledged data packet headers of Type 2 traffic class.

5. A port in SuperSpeed operation shall not transmit any header packet if its Remote Rx Header Buffer Credit Count is zero. A port in SuperSpeedPlus operation shall not transmit any Type 1 packets if its Remote Type 1 Rx Buffer Credit Count is zero, or any Type 2 packets if its Remote Type 2 Rx Buffer Credit Count is zero.

6. A port in SuperSpeed operation shall have enough Rx Header Buffers in its receiver to receive up to four header packets. A port in SuperSpeedPlus operation shall have enough Rx Buffers in its receiver to receive up to four Type 1 packets of maximum DPP size, and another four Type 2 packets of maximum DPP size.

7. Upon entry to U0, the following shall be performed in the sequence presented:

a. A port in SuperSpeed operation shall start the PENDING_HP_TIMER and CREDIT_HP_TIMER in expectation of the Header Sequence Number Advertisement, and the Rx Header Buffer Credit Advertisement. A port in SuperSpeedPlus operation shall start the PENDING_HP_TIMER and Type 1 and Type 2 CREDIT_HP_TIMER

7-18

Link Layer

in expectation of the Header Sequence Number Advertisement, and the Type 1 and Type 2 Rx Buffer Credit Advertisements

- b. A port shall initiate the Header Sequence Number Advertisement.
- c. A port in SuperSpeed operation shall initiate the Rx Header Buffer Credit Advertisement. A port in SuperSpeedPlus operation shall initiate the Type 1 and Type 2 Rx Buffer Credit Advertisements.- • The Header Sequence Number Advertisement refers to ACK Tx Header Sequence Number initialization by exchanging Header Sequence Numbers between the two ports. This Header Sequence Number is the Header Sequence Number of the last header packet a port has received properly. The main purpose of the Header Sequence Number Advertisement is to maintain the link flow before and after Recovery such that a port upon re-entry to U0 is aware what the last header packet is that was sent successfully prior to Recovery, and decides what header packets in its Tx Header Buffers or Type 1/Type 2 Tx Header Buffers that can be flushed or need to be retransmitted. The following rules shall be applied during the Header Sequence Number Advertisement:
  1. 1. A port shall set its initial Rx Header Sequence Number defined in the following:
     1. a. If a port enters U0 from Polling or Hot Reset, the Rx Header Sequence Number is zero.
     2. b. If a port enters U0 from Recovery, the Rx Header Sequence Number is the header Sequence Number of the next expected header packet.
  2. 2. A port shall set its initial Tx Header Sequence Number defined in the following:
     1. a. If a port enters U0 from Polling or Hot Reset, its Tx Header Sequence Number is zero.
     2. b. If a port enters U0 from Recovery, its Tx Header Sequence Number is the same as the Tx Header Sequence Number before Recovery.Note: A header packet that is re-transmitted shall maintain its originally assigned Header Sequence Number.
  3. 3. A port shall initiate the Header Sequence Number Advertisement by transmitting LGOOD\_n with “n” equal to the Rx Header Sequence Number minus one.Note: The decrement is based on modulo-8 operation.
  4. 4. A port shall set its initial ACK Tx Header Sequence Number to the Sequence Number received during the Rx Header Sequence Number Advertisement plus one.Note: The increment is based on modulo-8 operation.
  5. 5. A port in SuperSpeed operation shall not send any header packets until the Header Sequence Number Advertisement has been received and a Remote Rx Header Buffer Credit is available. A port in SuperSpeedPlus operation shall not send any Type 1 or Type 2 packet until the Header Sequence Number Advertisement has been received and their respective Remote Type 1 or Type 2 Rx Buffer Credit is available.
  6. 6. A port shall not request for a low power link state entry before receiving and sending the Header Sequence Number Advertisement.Note: The rules of Low Power Link State Initiation (refer to Section 7.2.4.2) still apply.
  7. 7. A port shall flush the header packets in its Tx Header Buffers or Type 1/Type 2 Tx Header Buffers upon receiving the Header Sequence Number Advertisement. A port shall do one of the following:
     1. a. If a port enters U0 from Polling or Hot Reset, it shall flush all the header packets in its Tx Header Buffers or Type 1/Type 2 Tx Header Buffers.

7-19

Universal Serial Bus 3.1 Specification

b. If a port enters U0 from Recovery, it shall flush all the header packets in its Tx Header Buffers or Type 1/Type 2 Tx Header Buffers that have been sent before Recovery except for those with the Header Sequence Number greater than (modulo 8) the Header Sequence Number received in Header Sequence Number Advertisement.

Note: If for example, the Header Sequence Number Advertisement of LGOOD_1 is received, a port shall flush the header packets in its Tx Header Buffers or Type 1/Type 2 Tx Header Buffers with Header Sequence Numbers of 1, 0, 7, 6.

- For SuperSpeed USB, the Rx Header Buffer Credit Advertisement refers to Remote Rx Header Buffer Credit Count Initialization by exchanging the number of available Local Rx Header Buffer Credits between the two ports. The main purpose of this advertisement is for a port to align its Remote Rx Header Buffer Credit Count with its link partner upon entry to U0. The following rules shall be applied during the Rx Header Buffer Credit Advertisement:

1. A port shall initiate the Rx Header Buffer Credit Advertisement after sending LGOOD_n during Header Sequence Number Advertisement.
2. A port shall initialize the following before sending the Rx Header Buffer Credit:

a. A port shall initialize its Tx Header Buffer Credit index to A.
b. A port shall initialize its Rx Header Buffer Credit index to A.
c. A port shall initialize its Remote Rx Header Buffer Credit Count to zero.
d. A port shall continue to process those header packets in its Rx Header Buffers that have been either acknowledged with LGOOD_n prior to entry to Recovery, or validated during Recovery, and then update the Local Rx Header Buffer Credit Count.
e. A port shall set its Local Rx Header Buffer Credit Count defined in the following:

1. If a port enters U0 from Polling or Hot Reset, its Local Rx Header Buffer Credit Count is 4.
2. If a port enters U0 from Recovery, its Local Rx Header Buffer Credit Count is the number of Rx Header Buffers available for incoming header packets.

3. A port shall perform the Rx Header Buffer Credit Advertisement by transmitting LCRD_x to notify its link partner. A port shall transmit one of the following based on its Local Rx Header Buffer Credit Count:

a. LCRD_A if the Local Rx Header Buffer Credit Count is one.
b. LCRD_A and LCRD_B if the Local Rx Header Buffer Credit Count is two.
c. LCRD_A, LCRD_B, and LCRD_C if the Local Rx Header Buffer Credit Count is three.
d. LCRD_A, LCRD_B, LCRD_C and LCRD_D if the Local Rx Header Buffer Credit Count is four.

4. A port receiving LCRD_x from its link partner shall increment its Remote Rx Header Buffer Credit Count by one each time an LCRD_x is received up to four.
5. A port shall not transmit any header packet if its Remote Rx Header Buffer Credit Count is zero.
6. A port shall not request for a low power link state entry before receiving and sending LCRD_x during the Rx Header Buffer Credit Advertisement.

Note: The rules of Low Power Link State Initiation (refer to Section 7.2.4.2) still apply.

7-20

Link Layer

- For SuperSpeedPlus USB, the process of the Type 1/Type 2 Rx Buffer Credit Advertisements is the same as the process of the Rx Header Buffer Credit Advertisement defined for SuperSpeed USB. There is no specific order requirement to perform the Rx Buffer Credit Advertisement between the two traffic classes. Mixture of LCRD1_x and LCRD2_x may be sent. The following rules shall be applied to SuperSpeedPlus USB during the Type 1/Type 2 Rx Buffer Credit Advertisements:

1. A port shall initiate the Type 1/Type 2 Rx Buffer Credit Advertisement after sending LGOOD_n during Header Sequence Number Advertisement.
2. A port shall initialize the following before sending the Type 1/Type 2 Rx Buffer Credit:

a. A port shall initialize its Type 1/Type 2 Tx Header Buffer Credit index to A.
b. A port shall initialize its Type 1/Type 2 Rx Buffer Credit index to A.
c. A port shall initialize its Remote Type 1/Type 2 Rx Buffer Credit Count to zero.
d. A port shall continue to process the packets in its Type 1/Type 2 Rx Buffers that have been either acknowledged with LGOOD_n prior to entry to Recovery, or validated during Recovery, and then update the Local Type 1/Type 2 Rx Buffer Credit Count.
e. A port shall set its Local Type 1/Type 2 Rx Buffer Credit Count defined in the following:

1. If a port enters U0 from Polling or Hot Reset, its Local Type 1/Type 2 Rx Buffer Credit Count is 4.
2. If a port enters U0 from Recovery, its Local Type 1/Type 2 Rx Buffer Credit Count is the number of Type 1/Type 2 Rx Buffers available for incoming packets.

3. A port shall perform the Type 1/Type 2 Rx Buffer Credit Advertisement by transmitting LCRD1_x/LCRD2_x to notify its link partner. A port shall transmit one of the following based on its Local Type 1/Type 2 Rx Buffer Credit Count:

a. LCRD1_A/LCRD2_A if the Local Type 1/Type 2 Rx Buffer Credit Count is one.
b. LCRD1_A and LCRD1_B/LCRD2_A and LCRD2_B if the Local Type 1/Type 2 Rx Buffer Credit Count is two.
c. LCRD1_A, LCRD1_B, and LCRD1_C/LCRD2_A, LCRD2_B, and LCRD2_C if the Local Type 1/Type 2 Rx Buffer Credit Count is three.
d. LCRD1_A, LCRD1_B, LCRD1_C and LCRD1_D/LCRD2_A, LCRD2_B, LCRD2_C and LCRD2_D if the Local Type 1/Type 2 Rx Buffer Credit Count is four.

4. A port receiving LCRD1_x/LCRD2_x from its link partner shall increment its respective Remote Type 1/Type 2 Rx Buffer Credit Count by one each time a LCRD1_x/LCRD2_x is received up to four.
5. A port in shall not transmit any Type 1 or Type 2 packet if the respective Remote Type 1 or Type 2 Rx Buffer Credit Count is zero.
6. A port shall not request for a low power link state entry before receiving and sending LCRD1_x and LCRD2_x during the Type 1 and Type 2 Rx Buffer Credit Advertisements.

Note: The rules of Low Power Link State Initiation (refer to Section 7.2.4.2) still apply.

- The following rules shall be applied additionally when a port enters U0 from Recovery:

1. A port sending LBAD before Recovery shall not expect to receive LRTY before a retried header packet from its link partner upon entry to U0.

7-21

Universal Serial Bus 3.1 Specification

2. A port receiving LBAD before Recovery shall not send LRTY before a retried header packet to its link partner upon entry to U0.

Note: There exists a situation where an LBAD was sent by a port before Recovery and it may or may not be received properly by its link partner. Under this situation, the rules of LBAD/LRTY do not apply. Refer to Sections 7.2.4.1.4 and 7.2.4.1.12 for details.

- Upon entry to Recovery and the next state is Hot Reset or Loopback, a port may optionally continue its processing of all the packets received properly.

### 7.2.4.1.2 General Rules of LGOOD_n and LCRD_x/LCRD1_x/LCRD2_x Usage

- For SuperSpeed USB, the Rx Header Buffer Credit shall be transmitted in the alphabetical order of LCRD_A, LCRD_B, LCRD_C, LCRD_D, and back to LCRD_A. LCRD_x received out of alphabetical order is considered as missing of a link command, and transition to Recovery shall be initiated.
- For SuperSpeedPlus USB, the Type 1 Rx Buffer Credit shall be transmitted in the alphabetical order of LCRD1_A, LCRD1_B, LCRD1_C, LCRD1_D, and back to LCRD1_A. LCRD1_x received out of alphabetical order is considered as missing of a link command, and transition to Recovery shall be initiated. The same shall apply to the Type 2 Rx Buffer Credit based on LCRD2_x.
- Header packets shall be sent with the Header Sequence Number in the numerical order from 0 to 7, and back to 0. LGOOD_n received out of the numerical order is considered as missing of a link command, and the transition to Recovery shall be initiated.
- Header packet transmission may be delayed. When this occurs, the DL bit shall be set in the Link Control Word by a hub and optionally by a peripheral device or host. Some, but not necessarily all, of the conditions that will cause this delay follow:

1. When a header packet is resent.

2. When the link is in Recovery.

3. For SuperSpeed USB, when the Remote Rx Header Buffer Credit Count is zero. For SuperSpeedPlus USB, when the Remote Type 1 or Type 2 Rx Buffer Credit Count is zero.

4. For SuperSpeed USB when the Tx Header Buffer is not empty. For SuperSpeedPlus USB when the Type 1/Type 2 Tx Header Buffer is not empty

Note: The delayed bit only has significance if it is set in an ITP. If a device uses the ITP to synchronize its internal clock, then it should ignore any ITPs with the delayed bit set.

### 7.2.4.1.3 Transmitting Packets

This Section describes header packet transmission in SuperSpeed operation, and Type 1/Type 2 packet transmission in SuperSpeedPlus operation.

- Before sending a header packet or a Type 1/Type 2 Packet, a port shall add the Tx Header Sequence Number corresponding to the Header Sequence Number field in the Link Control Word.
- Transmission of a header packet or a Type 1/Type 2 Packet shall consume a Tx Header Buffer or a Type 1/Type 2 Tx Header Buffer. Accordingly, the Tx Header Sequence Number shall be incremented by one after the transmission or roll over to zero if the maximum Header sequence number is reached.
- Transmission of a retried header packet or a Type 1/Type 2 Packet shall not consume an additional Tx Header Buffer or Type 1/Type 2 Tx Header Buffer and the Tx Header Sequence Number shall remain unchanged.

7-22

Link Layer

- Upon receiving LBAD, a port shall send LRTY followed by resending all the header packets that have not been acknowledged with LGOOD_n except for Recovery. Refer to Section 7.2.4.1.1 for additional rules applicable when a port enters U0 from Recovery.
- Prior to resending a header packet, a port shall set the Delay bit within the Link Control word and re-calculate CRC-5.
- Note: CRC-16 within header packet remains unchanged.
- For SuperSpeed USB, the Remote Rx Header Buffer Credit Count shall be incremented by one if a valid LCRD_x is received.
- For SuperSpeedPlus USB, the Remote Type 1 Rx Buffer Credit Count shall be incremented by one if a valid LCRD1_x is received. The Remote Type 2 Rx Buffer Credit shall be incremented by one if a valid LCRD2_x is received.
- For SuperSpeed USB, the Remote Rx Header Buffer Credit Count shall be decremented by one if a header packet is sent for the first time after entering U0, including when it is resent following Recovery.
- For SuperSpeedPlus USB, Remote Type 1 Rx Buffer Credit Count shall be decremented by one if a Type 1 packet is sent for the first time after entering U0, including when it is resent following Recovery. The same operation applies to Remote Type 2 Rx Buffer Credit Count with regard to Type 2 packet.
- The Remote Rx Header Buffer Credit Count or the Remote Type 1/Type 2 Rx Buffer Credit Count shall not be changed when a header packet is retried following LRTY.

### 7.2.4.1.4 Deferred DPH

The Deferred DPH shall be treated as a TP for buffering and credit purposes. Refer to Section 7.2.1.1.1 for deferred DPH format.

### 7.2.4.1.5 Receiving Header Packets

This section covers receiving all header packets except for SuperSpeedPlus DPH, which is described in Section 7.2.4.1.6.

- Upon receiving a header packet, the following verifications shall be performed:

1. CRC-5
2. CRC-16
3. Matching between the Header Sequence Number in the received header packet and the Rx Header Sequence Number
4. The availability of an Rx Header Buffer to store a header packet

- A header packet is defined as “received properly” when it has passed all four criteria described above.

- When a header packet has been received properly, a port shall issue a single LGOOD_n with “n” corresponding to the Rx Header Sequence Number and increment the Rx Header Sequence Number by one (or roll over to 0 if the maximum Header Sequence Number is reached).

- In SuperSpeed operation, a port shall consume one Rx Header Buffer until it has been processed.

- In SuperSpeedPlus operation, a port shall consume one Type 1 Rx Buffer Credit until it has been processed.

- When a header packet is not “received properly”, one of the following shall occur:

1. If the header packet has one or more CRC-5 or CRC-16 errors, a port shall issue a single LBAD. A port shall ignore all the header packets received subsequently until an LRTY

7-23

Universal Serial Bus 3.1 Specification

has been received, or the link has entered Recovery. Refer to Section 7.2.4.1.1 for additional rules applicable when a port enters U0 from Recovery.

2. If the Header Sequence Number in the received header packet does not match the Rx Header Sequence Number, or a port does not have an Rx Header Buffer available to store a header packet, a port shall transition to Recovery.

- In SuperSpeed operation, after transmitting LBAD, a port shall continue to issue LCRD_x if an Rx Header Buffer Credit is made available.
- In SuperSpeedPlus operation, after transmitting LBAD, a port shall continue to issue LCRD1_x/LCRD2_x if its respective Type 1/Type 2 Rx Buffer Credit is made available.
- A port shall transition directly to Recovery if it fails to receive a header packet three consecutive times. A port shall not issue the third LBAD upon the third error.

### 7.2.4.1.6 Receiving Data Packet Header in SuperSpeedPlus Operation

- Upon receiving a DPH, the following verifications shall be performed by a port:

1. CRC-5
2. CRC-16
3. Matching between the Header Sequence Number in the received header packet and the Rx Header Sequence Number
4. The availability of an Rx Buffer to store a header packet or a data packet.

- A DPH is defined as "received properly" when it has passed all four criteria described above. A port shall ignore the length field replica.
- When a DPH has been received properly, a port shall issue a single LGOOD_n with "n" corresponding to the Rx Header Sequence Number and increment the Rx Header Sequence Number by one (or roll over to 0 if the maximum Header Sequence Number is reached).
- A port shall consume one Type 1 or Type 2 Rx Buffer Credit until it has been processed and a Rx Buffer is available.
- When a DPH is not "received properly", one of the following shall occur:

1. If the DPH has one or more CRC-5 or CRC-16 errors, but the two length field replica are valid and identical, a port shall issue a single LBAD and track the associated DPP that immediately follows the DPH. A port shall ignore all the packets received subsequently until an LRTY has been received, or the link has entered Recovery. Refer to Section 7.2.4.1.1 for additional rules applicable when a port enters U0 from Recovery.

Note: a valid length field is 0~1024. Refer to Section 7.2.1.2 for details.

2. If any one of the following conditions occurs, a port shall transition to Recovery.

a. The two length field replica is not identical.
b. The Header Sequence Number in the received DPH does not match the Rx Header Sequence Number.
c. The Rx Buffer does not have enough space to store the received DP

- After transmitting LBAD, a port shall continue to issue LCRD1_x or LCRD2_x if its corresponding Type 1 or Type 2 Rx Buffer Credit is made available.
- A port shall transition directly to Recovery if it fails to receive a data packet header three consecutive times. A port shall not issue the third LBAD upon the third error.

7-24

Link Layer

### 7.2.4.1.7 SuperSpeed Rx Header Buffer Credit

Each port is required to have four Rx Header Buffer Credits in its receiver. This is referred to the Local Rx Header Buffer Credit. The number of the Local Rx Header Buffer Credits represents the number of header packets a port can accept and is managed by the Local Rx Header Buffer Credit Count.

- A port shall consume one Local Rx Header Buffer Credit if a header packet is "received properly". The Local Rx Header Buffer Credit Count shall be decremented by one.
- Upon completion of a header packet processing, a port shall restore a Local Rx Header Buffer Credit by:

1. Sending a single LCRD_x
2. Advancing the Credit index alphabetically (or roll over to A if the Header Buffer Credit index of D is reached) and
3. Incrementing the Local Rx Header Buffer Credit Count by one.

Note: The LCRD_x index is used to ensure Rx Header Buffer Credits are sent in an alphabetical order such that missing of an LCRD_x can be detected.

### 7.2.4.1.8 SuperSpeedPlus Type 1/Type 2 Rx Buffer Credit

Each port shall have the following two classes of Rx Buffer Credits.

- A port shall have four Type 1 Rx Buffer Credits for Type 1 traffic class in its receiver. This is referred to the Local Type 1 Rx Buffer Credit.
- A port shall have four Type 2 Rx Buffer Credits for Type 2 traffic class in its receiver. This is referred to the Local Type 2 Rx Buffer Credit.

The operation rules of the Local Type 1 and Type 2 Rx Buffer Credits are the same. They each represent the number of Type 1 or Type 2 packets a port can accept and are managed by their respective Local Type 1 and Type 2 Rx Buffer Credit Count. The following descriptions refer to the Local Type 1/Type 2 Rx Buffer Credit management.

- A port shall consume one Local Type 1 or Type 2 Rx Buffer Credit if the respective Type 1 or Type 2 packet is "received properly". The Local Type 1/Type 2 Rx Buffer Credit Count shall be decremented by one.
- Upon completion of a Type 1 or Type 2 packet processing, and the respective Type 1 or Type 2 Rx Buffer is made available, a port shall restore accordingly a Local Type 1 or Type 2 Rx Buffer Credit by:

1. Sending a single LCRD1_x or LCRD2_x
2. Advancing the Credit index alphabetically (or roll over to A if the Rx Buffer Credit index of D is reached) and
3. Incrementing the Local Type 1 or Type 2 Rx Buffer Credit Count by one.

### 7.2.4.1.9 Receiving Data Packet Payload

For SuperSpeed USB, the processing of DPP shall adhere to the following rules:

- A DPP processing shall be started if the following two conditions are met:

1. A DPH is received properly.
2. A DPPSTART ordered set is received properly immediately after its DPH.

- The DPP processing shall be completed when a valid DPPEND ordered set is detected.
- The DPP processing shall be aborted when one of the following conditions is met:

1. A valid DPPABORT ordered set is detected.

7-25

Universal Serial Bus 3.1 Specification

2. A K-symbol that does not belong to a valid DPPEND or DPPABORT ordered set is detected before a valid DPPEND or DPPABORT ordered set. A port shall then ignore the corresponding DPPEND or DPPABORT ordered set associated with the DPP.
3. A DPP of length exceeding sDataSymbolsBabble (see Table 10-19) has been reached and no valid DPPEND or DPPABORT ordered set is detected.

- A DPP shall be dropped if its DPH is corrupted.
- A DPP shall be dropped when it does not immediately follow its DPH.

For SuperSpeedPlus USB, the processing of DPP shall adhere to the following rules:

- A DPP processing shall be started if the following conditions are met.

1. A DPH is received properly or a DPH is not received properly but a valid DPP length field replica is declared.
2. A DPPSTART ordered set or DPPABORT ordered set is received immediately after its DPH.

- The DPP processing shall adhere to the following rules:

1. The DPP processing shall be completed when a valid DPPEND OS or DPPABORT OS is detected at the expected end of DPP indicated by valid length field plus 4.
2. The DPP processing shall be aborted if a DPPEND ordered set or a DPPABORT ordered set is not detected at the expected end of DPP indicated by valid length field plus 4. The port shall transition to Recovery.
3. The DPP processing shall be completed if a DPPABORT ordered set is detected immediately after DPH without DPPSTART ordered set.

### 7.2.4.1.10 Receiving LGOOD_n

- A port shall maintain every header packet transmitted within its Tx Header Buffer or Type 1/Type 2 Tx Header Buffer until it receives an LGOOD_n. Upon receiving LGOOD_n, a port shall do one of the following:

1. If LGOOD_n is the Header Sequence Number Advertisement and a port is entering U0 from Recovery, a port shall flush all the header packets retained in its Tx Header Buffers or Type 1/Type 2 Tx Header Buffers that have their Header Sequence Numbers equal to or less than the received Header Sequence Number, and initialize its ACK Tx Header Sequence Number to be the received Header Sequence Number plus one.

Note: The comparison and increment are based on modulo-8 operation.

2. If a port receives an LGOOD_n and this LGOOD_n is not Header Sequence Number Advertisement, it shall flush the header packet in its Tx Header Buffer or Type 1/Type 2 Tx Header Buffer with its Header Sequence Number matching the received Header Sequence Number and increment the ACK Tx Header Sequence Number by one based on modulo-8 operation.
3. If a port receives an LGOOD_n and this LGOOD_n is not Header Sequence Number Advertisement, it shall transition to Recovery if the received Header Sequence Number does not match the ACK Tx Header Sequence Number. The ACK Tx Header Sequence Number shall be unchanged.

Note: A port that has received an out of order LGOOD_n implies a lost or corrupted link command and shall initiate transition to Recovery.

7-26

Link Layer

### 7.2.4.1.11 Receiving LCRD_x/LCRD1_x/LCRD2_x

- A port in SuperSpeed operation shall adjust its Remote Rx Header Buffer Credit Count based on the received LCRD_x:

1. A port shall increment its Remote Rx Header Buffer Credit Count by one upon receipt of LCRD_x.
2. A port shall transition to Recovery if it receives an out of order LCRD_x.

Note: A port that has received an out of order credit implies a lost or corrupted link command and shall transition to Recovery.

- A port in SuperSpeedPlus operation shall adjust accordingly its Remote Type 1 and Type 2 Rx Buffer Credit Count based on the received LCRD1_x and LCRD2_x:

1. A port shall increment accordingly its Remote Type 1 or Type 2 Rx Buffer Credit Count by one upon receipt of LCRD1_x or LCRD2_x.
2. A port shall transition to Recovery if it receives an out of order LCRD1_x or LCRD2_x.

### 7.2.4.1.12 Receiving LBAD

Upon receipt of LBAD, a port shall send a single LRTY before retransmitting all the header packets in the Tx Header Buffers or Type 1/Type 2 Tx Header Buffers that have not been acknowledged with LGOOD_n. Additional rules in the following shall apply.

1. A hub shall set the DL bit in the Link Control Word on all resent header packets and recalculate CRC-5. When retransmitting a DP in SuperSpeed operation, a hub shall drop the DPP. When retransmitting a DP in SuperSpeedPlus operation, a hub shall drop the DPP and replace it with a nullified DPP. Refer to Section 7.2.1.2.2 for definition of a nullified DPP.
2. The host or a peripheral device may optionally set the DL bit in the Link Control Word on any resent header packets and recalculate CRC-5. If the retried packet is a DP and the DL bit in DPH is clear, the DPH shall be followed by a DPP.

Note: Resending an ITP invalidates the isochronous timestamp value. CRC-16 is unchanged in a retried header packet.

Upon receipt of LBAD, a port shall send a single LRTY if there is no unacknowledged header packet in the Tx Header Buffers or Type 1/Type 2 Tx Header Buffers.

Note: This is an error condition where LBAD is created due to a link error.

### 7.2.4.1.13 Transmitter Timers

A PENDING_HP_TIMER is specified to cover the period of time from when a header packet is sent to a link partner, to when the header packet is acknowledged by a link partner. The purpose of this time limit is to allow a port to detect if the header packet acknowledgement sent by its link partner is lost or corrupted. The timeout value for the PENDING_HP_TIMER is listed in Table 7-7. The operation of the PENDING_HP_TIMER shall be based on the following rules:

- A port shall have a PENDING_HP_TIMER that is active only in U0 and if one of the following conditions is met:

1. A port has a header packet transmitted but not acknowledged by its link partner, except during the period between receipt of LBAD and retransmission of the oldest header packet in the Tx Header Buffer or Type 1/Type 2 Tx Header Buffer.
2. A port is expecting the Header Sequence Number Advertisement from its link partner.

- The PENDING_HP_TIMER shall be started if one of the following conditions is met:

1. When a port enters U0 in expectation of the Header Sequence Number Advertisement.

7-27

Universal Serial Bus 3.1 Specification

2. When a header packet is transmitted and there are no prior header packets transmitted but unacknowledged in the Tx Header Buffers or Type 1/Type 2 Tx Header Buffers.
3. When the oldest header packet is retransmitted in response to LBAD.

- The PENDING_HP_TIMER shall be reset and restarted when a header packet is acknowledged with LGOOD_n and there are still header packets transmitted but unacknowledged in the Tx Header Buffers or or Type 1/Type 2 Tx Header Buffers.

- The PENDING_HP_TIMER shall be reset and stopped if one of the following conditions is met:

1. When a Header Sequence Number Advertisement is received.
2. When a header packet acknowledgement of LGOOD_n is received and all the transmitted header packets in the Tx Header Buffers or Type 1/Type 2 Tx Header Buffers are acknowledged.
3. When a header packet acknowledgement of LBAD is received.

- A port shall transition to Recovery if the following two conditions are met:

1. PENDING_HP_TIMER times out.
2. Additionally for SuperSpeed USB, the transmission of an outgoing header packet is completed or the transmission of an outgoing DPP is either completed with DPPEND or terminated with DPPABORT.

Note: This is to allow a graceful transition to Recovery without a header packet being truncated.

For SuperSpeed USB, a CREDIT_HP_TIMER is also specified to cover the period of time from when a header packet has been transmitted and its Remote Rx Header Buffer Credit count is less than four, to when a Remote Rx Header Buffer Credit is received and its Remote Rx Header Buffer Credit count is back to four. The purpose of this timer is to make sure that a Remote Rx Header Buffer Credit is received within a reasonable time limit. This will allow a port sending the header packet to reclaim a Remote Rx Header Buffer Credit within a time limit in order to continue the process of packet transmission. This will also allow a port receiving the header packet enough time to process the header packet.

Similarly for SuperSpeedPlus USB, two CREDIT_HP_TIMERs are specified. A Type 1 CREDIT_HP_TIMER is specified to cover the period of time from when a Type 1 packet has been transmitted and its Remote Type 1 Rx Buffer Credit count is less than four, to when a Remote Type 1 Rx Buffer Credit is received and its Remote Type 1 Rx Buffer Credit count is back to four. A Type 2 CREDIT_HP_TIMER is specified to cover the period of time from when a Type 2 packet has been transmitted and its Remote Type 2 Rx Buffer Credit count is less than four, to when a Remote Type 2 Rx Buffer Credit is received and its Remote Type 2 Rx Buffer Credit count is back to four. The timeout value for the CREDIT_HP_TIMER is listed in Table 7-7.

For SuperSpeed USB, the operation of the CREDIT_HP_TIMER shall be based on the following rules:

- A port shall have a CREDIT_HP_TIMER that is active only in U0 and if one of the following conditions is met:

1. A port has its Remote Rx Header Buffer Credit Count less than four.
2. A port is expecting the Header Sequence Number Advertisement and the Rx Header Buffer Credit Advertisement from its link partner.

- The CREDIT_HP_TIMER shall be started when a header packet or a retried header packet is sent, or when a port enters U0.

7-28

Link Layer

- The CREDIT_HP_TIMER shall be reset when a valid LCRD_x is received.
- The CREDIT_HP_TIMER shall be restarted if a valid LCRD_x is received and the Remote Rx Header Buffer Credit Count is less than four.
- A port shall transition to Recovery if the following two conditions are met:

1. CREDIT_HP_TIMER times out.

2. The transmission of an outgoing header packet is completed or the transmission of an outgoing DPP is either completed with DPPEND or terminated with DPPABORT.

Note: This is to allow a graceful transition to Recovery without a header packet being truncated.

For SuperSpeedPlus USB, the operation of the Type 1/Type 2 CREDIT_HP_TIMERs shall be based on the following rules:

- A port shall have its Type 1/Type 2 CREDIT_HP_TIMERs that are active only in U0 and if one of the following conditions is met:

1. A port has its respective Remote Type 1/Type 2 Rx Buffer Credit Count less than four.
2. A port is expecting the Header Sequence Number Advertisement and the Type 1/Type 2 Rx Buffer Credit Advertisements from its link partner.

- The Type 1/Type 2 CREDIT_HP_TIMERs shall be started when their respective packet or retried packet is sent, or when a port enters U0.
- The Type 1 or Type 2 CREDIT_HP_TIMER shall be reset when the respective LCRD1_x or LCRD2_x is received.
- The Type 1 or Type 2 CREDIT_HP_TIMER shall be restarted if a valid LCRD1_x or LCRD2_x is received and the respective Remote Type 1 or Type 2 Rx Buffer Credit Count is less than four.
- A port shall transition to Recovery if the Type 1 or Type 2 CREDIT_HP_TIMER times out.

Table 7-7. Transmitter Timers Summary

[tbl-94.md](tbl-94.md)

### 7.2.4.2 Link Power Management and Flow

Requests to transition to low power link states are done at the link level during U0. Link commands LGO_U1, LGO_U2, and LGO_U3 are sent by a port as a request to enter a low power link state. LAU or LXU is sent by the other port as the response. LPMA is sent by a port in response only to LAU. Details on exit/wake from a low power link state are described in Sections 7.5.7, 7.5.8, and 7.5.9.

#### 7.2.4.2.1 Power Management Link Timers

A port shall have three timers for link power management. First, a PM_LC_TIMER is used for a port initiating an entry request to a low power link state. It is designed to ensure a prompt entry to a low power link state. Second, a PM_ENTRY_TIMER is used for a port accepting the entry request to a low power link state. It is designed to ensure that both ports across the link are in the same low power link state regardless if the LAU or LPMA is lost or corrupted. Finally, a Ux_EXIT_TIMER is used for a port to initiate the exit from U1 or U2. It is specified to ensure that the duration of U1

7-29

Universal Serial Bus 3.1 Specification

or U2 exit is bounded and the latency of a header packet transmission is not compromised. The timeout values of the three timers are specified in Table 7-8.

A port shall operate the PM_LC_TIMER based on the following rules:

- A port requesting a low power link state entry shall start the PM_LC_TIMER after the last symbol of the LGO_Ux link command is sent.
- A port requesting a low power link state entry shall disable and reset the PM_LC_TIMER upon receipt of the LAU or LXU.

A port shall operate the PM_ENTRY_TIMER based on the following rules:

- A port accepting the request to enter a low power link state shall start the PM_ENTRY_TIMER after the last symbol of the LAU is sent.
- A port accepting the request to enter a low power link state shall disable and reset the PM_ENTRY_TIMER upon receipt of an LPMA or a TS1 ordered set.

A port shall operate the Ux_EXIT_TIMER based on the following rules.

- A port initiating U1 or U2 exit shall start the Ux_EXIT_TIMER when it starts to send LFPS Exit handshake signal.
- A port initiating U1 or U2 exit shall disable and reset the Ux_EXIT_TIMER upon entry to U0.

Table 7-8. Link Flow Control Timers Summary

[tbl-95.md](tbl-95.md)

### 7.2.4.2.2 Low Power Link State Initiation

- A port shall not send a LGO_U1, LGO_U2 or LGO_U3 unless it meets all of the following:

1. It has transmitted LGOOD_n and LCRD_x or LCRD1_x/LCRD2_x for all the packets received.
2. It has received LGOOD_n and LCRD_x or LCRD1_x/LCRD2_x for all the packets transmitted.

Note: This implies all credits must be received and returned before a port can initiate a transition to a low power link state.

3. It has no pending packets for transmission.
4. It has completed the Header Sequence Number Advertisement and the Rx Header Buffer Credit Advertisement or Type 1/Type 2 Rx Buffer Credit Advertisements upon entry to U0.

Note: This implies that a port has sent the Header Sequence Number Advertisement and the Rx Header Buffer Credit Advertisement or Type 1/Type 2 Rx Buffer Credit Advertisements to its link partner, and also received the Header Sequence Number Advertisement and the Rx Header Buffer Credit Advertisement or Type 1/Type 2 Rx Buffer Credit Advertisements from its link partner.

5. It is directed by a higher layer to initiate entry. Examples of when a higher layer may direct the link layer to initiate entry are: (a) the U1 or U2 inactivity timer expires (refer to PORT_U1_TIMEOUT, PORT_U2_TIMEOUT in Chapter 10); (b) reception of a

7-30

Link Layer

SetPortFeature(PORT_LINK_STATE) request; and (c) device implementation specific mechanisms.

6. It has met higher layer conditions for initiating entry. Examples are: (a) U1_enable/U2_enable is set or U1_TIMEOUT/U2_TIMEOUT is not equal zero; (b) device has received an ACK TP for each and every previously transmitted packet; (c) device is not waiting for a TP following a PING; and (d) device is not waiting for a timestamp following a timestamp request (for these and any other examples, refer to Chapter 8).

- A port shall do one of the following in response to receiving an LGO_U1 or LGO_U2:

1. A port shall send an LAU if the Force Link PM Accept field is asserted due to having received a Set Link Function LMP.
2. A port shall send an LAU if all of the following conditions are met:

a. It has transmitted an LGOOD_n, LCRD_x or LCRD1_x/LCRD2_x sequence for all packets received.
b. It has received an LGOOD_n, LCRD_x or LCRD1_x/LCRD2_x sequence for all packets transmitted.
c. It has no pending packets for transmission.
d. It is not directed by a higher layer to reject entry. Examples of when a higher layer may direct the link layer to reject entry are: (1) Downstream port is not enabled for U1 or U2 (i.e., PORT_U1_TIMEOUT or PORT_U2_TIMEOUT reset to zero); (2) When a device has not received an ACK TP for a previously transmitted packet (refer to Chapter 8); and (3) When a device receives a ping TP (refer to the ping packet definition in Chapter 8 for more information).

3. A port shall send an LXU if any of the above conditions are not met.

### 7.2.4.2.3 U1/U2 Entry Flow

Either a downstream port or an upstream port may initiate U1/U2 entry or exit. Entry to a low power U1 or U2 link state is accomplished by using the link commands defined in Table 7-5.

- A port shall send a single LGO_U1 or LGO_U2 to request a transition to a low power link state.
- Upon issuing LGO_Ux, a port shall start its PM_LC_TIMER.
- A port shall either accept LGO_Ux with a single LAU or shall reject LGO_U1 or LGO_U2 with a single LXU and remain in U0.
- Upon sending LGO_U1 or LGO_U2, a port shall not send any packets until it has received LXU or re-entered U0.
- Upon sending LGO_U1 or LGO_U2, a port shall continue receiving and processing packets and link commands.
- Upon receiving LXU, a port shall remain in U0.
- A port shall initiate transition to Recovery if a single LAU or LXU is not received upon PM_LC_TIMER timeout.
- Upon issuing LAU, a port shall start PM_ENTRY_TIMER.
- Upon receiving LAU, a port shall send a single LPMA and then enter the requested low power link state.
- Upon issuing LAU or LPMA, a port shall not send any packets or link commands.
- A port that sends LAU shall enter the corresponding low power link state upon receipt of LPMA before PM_ENTRY_TIMER timeout.

7-31

Universal Serial Bus 3.1 Specification

- A port that sends LAU shall enter the requested low power link state upon PM_ENTRY_TIMER timeout and if all of the following conditions are met:

1. LPMA is not received.
2. No TS1 ordered set is received.

Note: This implies LPMA is corrupted and the port issuing LGO_Ux has entered Ux.

- A port that has sent LAU shall enter Recovery before PM_ENTRY_TIMER timeout if a TS1 ordered set is received.

Note: This implies LAU was corrupted and the port issuing LGO_Ux has entered Recovery.

- A port that has sent LAU shall not respond with Ux LFPS exit handshake defined in Section 6.9.2 before PM_ENTRY_TIMER timeout and if LFPS Ux_Exit signal is received.

Note: This implies LPMA was corrupted and the port issuing LGO_Ux has initiated Ux exit. Under this situation, the port sending LAU shall complete the low power link state entry process and then respond to Ux exit.

There also exists a situation where a port transitions from U1 to U2 directly.

- A port in U1 shall enter U2 directly if the following two conditions are met:

1. The port's U2 inactivity timer is enabled.
2. The U2 inactivity timer times out and no U1 LFPS exit signal is received.

7-32

Link Layer

### 7.2.4.2.4 U3 Entry Flow

Only a downstream port can initiate U3 entry. An upstream port shall not reject U3 entry.

- Upon directed, a downstream port shall initiate U3 entry process by sending LGO_U3.
- Upon issuing LGO_U3, a downstream port shall start PM_LC_TIMER.
- An upstream port shall send LAU in response to LGO_U3 request by a downstream port.
- An upstream port shall not send any packets or link commands subsequent to sending an LAU.
- Upon issuing LGO_U3, a downstream port shall ignore any packets sent by an upstream port.

Note: This is a corner condition that an upstream port is sending a header packet before receiving LGO_U3.

- Upon Receiving LGO_U3, an upstream port shall respond with an LAU. The processing of all the unacknowledged packets shall be aborted.
- Upon issuing LAU, an upstream port shall start PM_ENTRY_TIMER.
- A downstream port shall send a single LPMA and then transition to U3 when LAU is received.
- A downstream port shall transition to Recovery and reinitiate U3 entry after re-entry to U0 if all of the following three conditions are met:

1. The PM_LC_TIMER times out.
2. LAU is not received.
3. The number of consecutive U3 entry attempts is less than three.

- An upstream port shall transition U3 when one of the following two conditions is met:

1. LPMA is received
2. The PM_ENTRY_TIMER times out and LPMA is not received

- A downstream port shall transition to eSS.Inactive when it fails U3 entry on three consecutive attempts.

### 7.2.4.2.5 Concurrent Low Power Link Management Flow

Concurrent low power link management flow applies to situations where a downstream port and an upstream port both issue a request to enter a low power link state.

- If a downstream port has sent an LGO_U1, LGO_U2, or LGO_U3 and also received an LGO_U1 or LGO_U2, it shall send an LXU.
- If an upstream port has sent an LGO_U1 or LGO_U2 and also received an LGO_U1, LGO_U2, it shall wait until receipt of an LXU and then send either an LAU or LXU.
- If an upstream port has sent an LGO_U1 or LGO_U2 and also received an LGO_U3 from a downstream port, it shall wait until the reception of an LXU and then send an LAU.
- If a downstream port is directed by a higher layer to initiate a transition to U3, and a transition to U1 or U2 has been initiated but not yet completed, the port shall first complete the in-process transition to U1 or U2, then return to U0 and request entry to U3.

### 7.2.4.2.6 Concurrent Low Power Link Management and Recovery Flow

Concurrent low power link management and Recovery flow applies to situations where a port issues a low power link state entry and another port issues Recovery. The port that issues the low power link state entry shall meet the following rules:

- Upon issuing LGO_Ux, the port shall transition to Recovery if a TS1 ordered set is received.

7-33

Universal Serial Bus 3.1 Specification

- The port shall reinitiate low power link state entry process described in Section 7.2.4.2.3 and 7.2.4.2.4 upon re-entry to U0 from Recovery if the conditions to enter a low power link state are still valid.

### 7.2.4.2.7 Low Power Link State Exit Flow

Exit from a low power link state refers to exit from U1/U2, or wakeup from U3. It is accomplished by the LFPS Exit signaling defined in Section 6.9.2. A successful LFPS handshake process will lead both a downstream port and an upstream port to Recovery.

A Ux_EXIT_TIMER defined in Section 7.2.4.2.1 is only applied when a port is attempting an exit from U1 or U2. It shall not be applied when a port is initiating a U3 wakeup.

The exit from U1/U2 shall meet the following flow. The U3 wakeup follows the same flow with the exception that Ux_EXIT_TIMER is disabled during U3 wakeup.

- If a port is initiating U1/U2 Exit, it shall start sending U1/U2 LFPS Exit handshake signal defined in Section 6.9.2 and start the Ux_EXIT_TIMER.
- If a port is initiating U3 wakeup, it shall start sending U3 LFPS wakeup handshake signal defined in Section 6.9.2.
- A port upon receiving U1/U2 Exit or U3 wakeup LFPS handshake signal shall start U1/U2 exit or U3 wakeup by responding with U1/U2 Exit or U3 wakeup LFPS signal defined in Section 6.9.2.
- Upon a successful LFPS handshake before tNoLFPSResponseTimeout defined in Table 6-30, a port shall transition to Recovery.
- A port initiating U1 or U2 Exit shall transition to eSS.Inactive if one of the following two conditions is met:

1. Upon tNoLFPSResponseTimeout and the condition of a successful LFPS handshake is not met.
2. Upon Ux_EXIT_TIMER timeout, the link has not transitioned to U0.

- A port initiating U3 wakeup shall remain in U3 when the condition of a successful LFPS handshake is not met upon tNoLFPSResponseTimeout and it may initiate U3 wakeup again after a minimum of 100-ms delay.

- A root port not able to respond to U3 LFPS wakeup within tNoLFPSResponseTimeout shall initiate U3 LFPS wakeup when it is ready to return to U0.

## 7.3 Link Error Rules/Recovery

### 7.3.1 Overview of Enhanced SuperSpeed Bit Errors

The Enhanced SuperSpeed timing budget is based on a link's statistical random bit error probability less than 10⁻¹². Packet framings and link command framing are tolerant to one symbol error. Details on bit error detection under link flow control are described in Section 7.2.4.

### 7.3.2 Link Error Types, Detection, and Recovery

Data transfers between the two link partners are carried out using the form of a packet. A set of link commands is defined to ensure the successful packet flow across the link. Other link commands are also defined to manage the link connectivity. When symbol errors occur on the link, the integrity of a packet or a link command can be compromised. Therefore, not only a packet or a link command needs to be constructed to increase the error tolerance, but the link data integrity

7-34

Link Layer

handling also needs to be specified such that any errors that will invalidate or corrupt a packet or a link command can be detected and a link error can be recovered.

There are various types of errors at the link layer. This includes an error on a packet or a link command, or an error during the link training process, or an error when a link is in transition from one state to another. The detection and recovery from those link errors are described with details in this section.

### 7.3.3 Link Error Statistics

To facilitate the quality of the link operation, two counts of link error statistics are implemented and accessible by the upper layer for its decision if port re-configuration is needed.

#### 7.3.3.1 Link Error Count

The Link Error Count is defined to record the number of events when a port transitions from U0 to Recovery to recover an error event. Except for the upstream port in SuperSpeed operation, all ports shall implement the Link Error Count.

The operation of Link Error count shall adhere to the following rules.

- A port in SuperSpeedPlus operation shall implement the Link Error Count that counts up to 65,535 error events. The Link Error Count shall saturate if it has reached its maximum count value.
- The Link Error Count shall be reset to zero in any one of the following conditions.

1. PowerOn Reset
2. Entry to Polling.Idle
3. Directed
4. Hot Reset

- The Link Error Count shall be incremented by one each time a port transitions from U0 to Recovery to recover an error event.

#### 7.3.3.2 Soft Error Count

The Soft Error Count is defined to record the number of error events that are either correctable or detectable and do not require the link to recover through transition to Recovery. Only a port in SuperSpeedPlus operation may optionally implement the Soft Error Count.

The operation of the Soft Error Count shall adhere to the following rules.

- A port in SuperSpeedPlus operation shall count up to 65,535 error events. The Soft Error Count shall saturate if it has reached its maximum count value
- The Soft Error Count shall be reset to zero in any one of the following conditions.

1. PowerOn Reset
2. Entry to Polling.Idle
3. Directed
4. Hot Reset

- The Soft Error Count shall increment by one if any of the following errors is detected.

1. Single-bit error in the block header.
2. CRC-5 or CRC-16 or CRC-32 error.

7-35

Universal Serial Bus 3.1 Specification

3. Single symbol framing error.
4. Idle Symbol error.
5. Single SKP symbol error.
6. Optionally for error in the length field replica of DPH.

### 7.3.4 Header Packet Errors

Several types of header packet errors are detected. They are:

1. Missing of a header packet
2. Invalid header packet due to CRC errors
3. Mismatch of a Rx Header Sequence Number

Regardless, the Link Error Count is incremented for only one class of errors in the link layer, and those are errors which will cause the link to transition to Recovery. For errors that will not cause the link to enter Recovery, the Link Error Count shall remain unchanged.

#### 7.3.4.1 Packet Framing Error

A packet framing ordered set is constructed such that any single symbol corruption within the ordered set will not prevent its packet framing recognition.

Header packet framing and DPP framing are all constructed using four symbol ordered sets. A header packet contains only one packet framing ordered set at the beginning of the packet defined in Section 7.2.1. A DPP begins with start packet framing ordered set and ends with end packet framing ordered set as defined in Section 7.2.2.

- A valid HPSTART ordered set, or a valid DPHSTART ordered set, or a valid DPP framing ordered set shall be declared if the following two conditions are met:

1. At least three of the four symbols in the four consecutive symbol periods are valid packet framing symbols.
2. The four symbols are in the order defined in Table 7-9.

Note: If an HPSTART ordered set or a DPHSTART ordered set has two or more symbols corrupted, a header packet will not be detectable and, therefore, result in missing of a header packet. Similarly, if a DPP framing ordered set is corrupted in SuperSpeed operation, it will result in missing of a data packet payload. For SuperSpeed operation, a corruption of a DPP framing ordered set will result in the loss of data packet payload boundary.

- Missing of a header packet shall result in a port transitioning to Recovery depending on which one of the following conditions becomes true first:

1. A port transmitting the header packet upon its PENDING_HP_TIMER timeout.
2. A port receiving the header packet upon detection of a Rx Header Sequence Number error.

- Missing of a DPP framing ordered set in SuperSpeedPlus operation shall result in a port transitioning to Recovery.

- The Link Error Count shall be incremented by one each time a transition to Recovery occurs.

7-36

Link Layer

Table 7-9. Valid Packet Framing Symbol Order (Sx is One of SHP, DPHP, SDP, END or EDB)

[tbl-96.md](tbl-96.md)

### 7.3.4.2 Header Packet Error

Each header packet contains a CRC-5 and a CRC-16 to ensure that the data integrity of a header packet can be verified. A CRC-5 is used to detect bit errors in the Link Control Word. A CRC-16 is used to detect bit errors in the packet header. A header packet error can be detected using CRC-5 or CRC-16 checks.

- A header packet error shall be declared if the following conditions are true:
  1. A valid HPSTART ordered set or DPHSTART ordered set is detected.
  2. Either CRC-5 or CRC-16 check fails as defined in Section 7.2.1 or additionally for SuperSpeed USB, any K-symbol occurrence in the packet header or Link Control Word that prevents CRC-5 or CRC-16 checks from being completed.
- A port receiving the header packet shall send an LBAD as defined in Section 7.2.4.1 if it detects a header packet error. The Link Error Count shall remain unchanged.
- If a port fails to receive a header packet for three consecutive times, it shall transition to Recovery. The Link Error Count shall be incremented by one. Refer to Section 7.2.4.1.4 for details.

### 7.3.4.3 Rx Header Sequence Number Error

Each port contains an Rx Header Sequence Number that is defined in Section 7.2.4.1 and initialized upon entry to U0. Upon receiving a header packet, a port is required to compare the Header Sequence Number embedded in the header packet with the Rx Header Sequence Number stored in its receiver. This ensures that header packets are transmitted and received in an orderly manner. A missing or corrupted header packet can be detected.

- An Rx Header Sequence Number error shall occur if the following conditions are met:
  1. A header packet is received and no header packet error is detected.
  2. The Header Sequence Number in the received header packet does not match the Rx Header Sequence Number.
- A port detecting an Rx Header Packet Sequence Number error shall transition to Recovery.
- The Link Error Count shall be incremented by one each time a transition to Recovery occurs.

### 7.3.5 Link Command Errors

A link command consists of four-symbol link command frame ordered set, LCSTART, followed by a two-symbol link command word, and its repeat. A link command is constructed such that any single symbol corruption within the link command frame ordered set will not invalidate the recognition of a link command. Additionally for SuperSpeedPlus USB, any single-bit error in the two link command words will not corrupt the correct parsing of a link command.

- A detection of a link command shall be declared if the following two conditions are met:

7-37

Universal Serial Bus 3.1 Specification

1. At least three of the four symbols in four consecutive symbol periods are valid link command symbols.
2. The four symbols are in the order described in Table 7-10.

- For SuperSpeed USB, a valid link command is declared if both link command words are the same, they both contain valid link command information as defined in Table 7-4, and they both pass the CRC-5 check.
- For SuperSpeedPlus USB, a valid link command is declared if one of the following conditions is met:

1. Both link command words are the same, they contain valid link command information as defined in Table 7-4, and they pass the CRC-5 check.
2. One of the link command words contains valid link command information as defined in Table 7-4, and passes the CRC-5 check, and the other link command word either contains invalid link command information, or fails the CRC-5 check.

- An invalid link command is declared upon detection of a link command and the conditions to meet a valid link command are not met.
- An invalid link command shall be ignored.
- A port detecting missing of LGOOD_n or LCRD_x or LCRD1_x/LCRD2_x shall transition to Recovery.

Note: Missing LGOOD_n is declared when two consecutive LGOOD_n received are not in numerical order. Missing LGOOD_n, or LBAD, or LRTY can also be inferred upon PENDING_HP_TIMER timeout. Missing LCRD_x or LCRD1_x/LCRD2_x is declared when two consecutive LCRD_x or LCRD1_x/LCRD2_x received are not in alphabetical order, or upon CREDIT_HP_TIMER or Type 1/Type 2 CREDIT_HP_TIMER times out and LCRD_x or LCRD1_x/LCRD2_x is not received.

- A port detecting missing of LGO_Ux, or LAU, or LXU shall transition to Recovery.

Note: Detection of missing LGO_Ux, or LAU, or LXU is declared upon PM_LC_TIMER timeout and LAU or LXU is not received.

- A downstream port detecting missing of LUP shall transition to Recovery (refer to Section 7.5.6 for LUP detection).

Note: Missing of LPMA will not transition the link to Recovery. It will only cause an Ux entry delay for the port accepting LGO_Ux (refer to Section 7.2.4.2 for details).

- An upstream port detecting missing of LDN shall transition to Recovery (refer to Section 7.5.6 for LDN detection).
- The Link Error Count shall be incremented by one each time a transition to Recovery occurs due to an error.

Table 7-10. Valid Link Command Symbol Order

[tbl-97.md](tbl-97.md)

7-38

Link Layer

### 7.3.6 ACK Tx Header Sequence Number Error

Each port has an ACK Tx Header Sequence Number that is defined in Section 7.2.4.1. The ACK Tx Header Sequence Number is initialized during the Header Sequence Number Advertisement. After a header packet is transmitted, a port is expecting to receive an LGOOD_n from its link partner as an explicit acknowledgement that the header packet is received properly. Upon receiving LGOOD_n, the Header Sequence Number contained in LGOOD_n will be compared with the ACK Tx Header Sequence Number. The outcome of the comparison will determine if an ACK Tx Header Sequence Number error has occurred.

- An ACK Tx Header Sequence Number error shall be declared if the following conditions are met:
  1. A valid LGOOD_n is received.
  2. The Header Sequence Number in the received LGOOD_n does not match the ACK Tx Header Sequence Number.
  3. The LGOOD_n is not for Header Sequence Number Advertisement.
- A port detecting an ACK Tx Header Sequence Number error shall transition to Recovery.
- The Link Error Count shall be incremented by one each time a transition to Recovery occurs.

### 7.3.7 Header Sequence Number Advertisement Error

Each port is required to first perform a Header Sequence Number Advertisement upon entry to U0. The details of a Header Sequence Number Advertisement are described in Section 7.2.4. A Header Sequence Number Advertisement is the first step of the link initialization to ensure that the link flow is maintained un-interrupted before and after Recovery. Any errors occurred during the Header Sequence Number Advertisement must be detected and proper error recovery must be initiated.

- A Header Sequence Number Advertisement error shall occur if one of the following conditions is true:

1. Upon PENDING_HP_TIMER timeout and the Header Sequence Number Advertisement not received
2. A header packet received before sending Header Sequence Number Advertisement
3. LCRD_x or LCRD1_x/LCRD2_x or LGO_Ux received before receiving Header Sequence Number Advertisement

- A port detecting any Header Sequence Number Advertisement error shall transition to Recovery.

- The Link Error Count shall be incremented by one each time a transition to Recovery occurs.

### 7.3.8 SuperSpeed Rx Header Buffer Credit Advertisement Error

Each port is required to perform the Rx Header Buffer Credit Advertisement after Header Sequence Number Advertisement upon entry to U0. The details of Rx Header Buffer Credit Advertisement are described in Section 7.2.4.

- An Rx Header Buffer Credit Advertisement error shall occur if one of the following conditions is true:

1. Upon CREDIT_HP_TIMER timeout and no LCRD_x received.
2. A header packet received before sending LCRD_x.
3. LGO_Ux received before receiving LCRD_x.

7-39

Universal Serial Bus 3.1 Specification

- A port detecting an Rx Header Buffer Credit Advertisement Error shall transition to Recovery.
- The Link Error Count shall be incremented by one each time a transition to Recovery occurs.

### 7.3.9 SuperSpeedPlus Type 1/Type 2 Rx Buffer Credit Advertisement Error

For SuperSpeedPlus USB, the operation of Type 1 Rx Buffer Credit Advertisement error detection is the same as Type 2 Rx Buffer Credit Advertisement.

Each port is required to perform the Type 1 and Type 2 Rx Buffer Credit Advertisements after Header Sequence Number Advertisement upon entry to U0. The details of Type 1/Type 2 Rx Buffer Credit Advertisements are described in Section 7.2.4.

- A Type 1/Type 2 Rx Buffer Credit Advertisement error shall occur if one of the following conditions is true:
  1. Upon Type 1 or Type 2 CREDIT_HP_TIMER timeout and its respective LCRD1_x or LCRD2_x is not received.
  2. A Type 1 packet received before sending LCRD1_x, or Type 2 packet received before sending LCRD2_x.
  3. LGO_Ux received before receiving LCRD1_x or LCRD2_x.
- A port detecting a Type 1/Type 2 Rx Buffer Credit Advertisement Error shall transition to Recovery.
- The Link Error Count shall be incremented by one each time a transition to Recovery occurs.

### 7.3.10 Training Sequence Error

Symbol corruptions during the TS1 and TS2 ordered sets in Polling.Active, Polling.Configuration, Recovery.Active, and Recovery.Configuration substates are expected until the requirements are met to transition to the next state. A timeout from any one of these substates is considered a Training Sequence error.

- A timeout from either Polling.Active, Polling.Configuration, Recovery.Active, or Recovery.Configuration substate shall result in a Training Sequence error.
- For SuperSpeedPlus operation, upon detecting a Training Sequence error in Polling.Active or Polling.Configuration, the port shall transition to Polling.PortMatch to negotiate for SuperSpeed operation. Refer to Section 7.5.4 for details.
- For SuperSpeed operation, upon detecting a Training Sequence error, one of the following link state transitions shall be followed:

1. A downstream port shall transition to Rx.Detect if a Training Sequence error occurs during Polling and cPollingTimeout is less than two.
2. A downstream port shall transition to eSS.Inactive if a Training Sequence error occurs during Polling and cPollingTimeout is two.
3. An upstream port of a hub shall transition to Rx.Detect if a Training Sequence error occurs during Polling.
4. An upstream port of a peripheral device shall transition to eSS.Disabled if a Training Sequence error occurs during Polling.
5. A downstream port shall transition to eSS.Inactive if a Training Sequence error occurs during Recovery and the transition to Recovery is not an attempt for Hot Reset.

7-40

Link Layer

6. A downstream port shall transition to Rx.Detect if a Training Sequence error occurs during Recovery.Active and Recovery.Configuration and the transition to Recovery is an attempt for Hot Reset.
7. An upstream port shall transition to eSS.Inactive if a Training Sequence error occurs during Recovery.
- The Link Error Count shall remain unchanged.

### 7.3.11 SuperSpeed 8b/10b Errors

There are two types of errors when a receiver decodes 8b/10b symbols. One is a disparity error that is declared when the running disparity of the received 8b/10b symbols is not +2, or 0, or -2. The other is a decode error when an unrecognized 8b/10b symbol is received.

Upon receiving notification of an 8b/10b error:

- A port may optionally do the following:
  1. If the link is receiving a header packet, it shall send LBAD.
  2. If the link is receiving a link command, it shall ignore the link command.
  3. If the link is receiving a DPP, it shall drop the DPP.
- The Link Error Count shall remain unchanged.

### 7.3.12 SuperSpeedPlus Block Header Errors

There are two types of block header errors, a correctable single bit block header error, and a detectable but not correctable two-bit block header error.

- Upon detecting a single-bit block header error, the PHY shall correct it and report the error event to the link layer. The Soft Error Count shall be incremented by one if the Soft Error Count is implemented.
- Upon detecting two-bit block header error, the PHY shall report the error event to the link layer. The port shall transition Recovery. The Link Error Count shall be incremented by one.

### 7.3.13 Summary of Error Types and Recovery

Table 7-11 summarizes the link error types, error count, and different error paths to restore the link.

- The link error shall be counted each time a link transitions to Recovery due to an error.
- The link error shall be counted by a downstream port.
- The Link Error Count shall be reset upon PowerOn Reset, Warm Reset, Hot Reset, or whenever a port enters Polling.Idle.

Situations also exist where an unexpected link command or header packet is received. These include but are not limited to the following:

1. Receiving an unexpected link command such as LBAD, LRTY, LAU, LXU, or LPMA before receiving the Header Sequence Number Advertisement and the Remote Rx Header Buffer Credit Advertisement or Type 1/Type 2 Rx Buffer Credit Advertisements.
2. Receiving the Header Sequence Number Advertisement after entry to U0 from Recovery with its ACK Tx Header Sequence Number not corresponding to any header packets in the Tx Header Buffers or Type 1/Type 2 Tx Header Buffers.
3. Receiving LRTY without sending LBAD.
4. Receiving LGOOD_n that is neither a Header Sequence Number Advertisement, nor for header packet acknowledgement.

7-41

Universal Serial Bus 3.1 Specification

5. Receiving LAU, or LXU without sending LGO_Ux.
6. Receiving LPMA without sending LAU.
7. Receiving an unexpected header packet during link initialization.

These error situations are largely not due to link errors. A port's behavior under these situations is undefined and implementation specific. It is recommended that a port ignore those unexpected link commands or header packets.

If the ports are directed to different link states based on TS2 ordered set, the downstream port's TS2 ordered set overrides the upstream port's TS2 ordered set. For example, if a downstream port issues Hot Reset in its TS2 ordered set, and an upstream port issues Loopback mode, Hot Reset overrides Loopback. The ports shall enter Hot Reset.

Table 7-11. Error Types and Recovery

[tbl-98.md](tbl-98.md)

7-42

Link Layer

[tbl-99.md](tbl-99.md)

## 7.4 PowerOn Reset and Inband Reset

There are two categories of reset associated with a link. The first, PowerOn Reset, restores storage elements, registers, or memories to predetermined states when power is applied. Upon PowerOn Reset, the LTSSM (described in Section 7.5) shall enter Rx.Detect. The second, Inband Reset, uses Enhanced SuperSpeed or LFPS signaling to propagate the reset across the link. There are two mechanisms to complete an Inband Reset, Hot Reset and Warm Reset. Upon completion of either a PowerOn Reset or an Inband Reset, the link shall transition to U0 as described in Section 7.4.2.

7-43

Universal Serial Bus 3.1 Specification

### 7.4.1 PowerOn Reset

PowerOn Reset restores a storage element, register, or memory to a predetermined state when power is applied (refer to Section 9.1.1.2 for clarification of when power is applied for self-powered devices). A port must be responsible for its own internal Reset signaling and timing.

The following shall occur when PowerOn Reset is asserted or while VBUS is off:

1. Receiver termination shall meet the ZRX-HIGH-IMP-DC-POS specification defined in Table 6-21.
2. Transmitters shall hold a constant DC common mode voltage (VTX-DC-CM) defined in Table 6-18.

The following shall occur when PowerOn Reset is completed and VBUS is valid:

1. The LTSSM of a port shall be initialized to Rx.Detect.
2. The LTSSM and the PHY level variables (such as Rx equalization settings) shall be reset to their default values.
3. The receiver termination of a port shall meet the RRX-DC specification defined in Table 6-21.
Note: Rx termination shall always be maintained throughout operation except for eSS.Disabled

### 7.4.2 Inband Reset

An Inband Reset shall be generated by a downstream port only when it is directed.

There are two mechanisms to generate an Inband Reset. The first mechanism; Hot Reset, is defined by sending TS2 ordered sets with the Reset bit asserted. A Hot Reset shall cause the LTSSM to transition to the Hot Reset state. Upon completion of Hot Reset, the following shall occur:

- A downstream port shall reset its Link Error Count.
- The port in SuperSpeedPlus operation shall reset the Soft Error Count if implemented.
- The port shall reset its PM timers and the associated U1 and U2 timeout values to zero.
- The port configuration information of an upstream port shall remain unchanged. Refer to Sections 8.4.5 and 8.4.6 for details.
- The PHY level variables (such as Rx equalization settings) shall remain unchanged.
- The LTSSM of a port shall transition to U0.

The second mechanism of an Inband Reset is Warm Reset. The signaling of a Warm Reset is defined as an LFPS signaling meeting the tReset requirements (see Table 6-29). A Warm Reset will cause the LTSSM to transition to Rx.Detect, retrain the link including the receiver equalizer, reset an upstream port, and then transition to U0. An upstream port shall enable its LFPS receiver and Warm Reset detector in all link states except eSS.Disabled. A completion of a Warm Reset shall result in the following.

- A downstream port shall reset its Link Error Count.
- Port configuration information of an upstream port shall be reset to default values. Refer to Sections 8.4.5 and 8.4.6 for details.
- The PHY level variables (such as Rx equalization settings) shall be reinitialized or retrained.
- The LTSSM of a port shall transition to U0 through RxDetect and Polling.

A downstream port may be directed to reset the link in two ways, "PORT_RESET", or "BH_PORT_RESET" as described in Section 10.3.1.6. When a "PORT_RESET" is directed, a downstream port shall issue either a Hot Reset, or a Warm Reset, depending on its LTSSM state. When a "BH_PORT_RESET" is directed, a downstream port shall issue a Warm Reset in any of its LTSSM states except eSS.Disabled.

7-44

Link Layer

If a “PORT_RESET” is directed, a downstream port shall issue either a Hot Reset or a Warm Reset based on the following conditions:

- If the downstream port is U3, or Loopback, or Compliance Mode, or eSS.Inactive, it shall use Warm Reset.
- If the downstream port is in U0, it shall use Hot Reset.
- If a downstream port is in a transitory state of Polling or Recovery, it shall use Hot Reset.
- If the downstream port is in U1 or U2, it shall exit U1 or U2 using the LFPS exit handshake, transition to Recovery and then transition to Hot Reset. The following two additional rules apply when the downstream port fails to enter Hot Reset.
  1. If a Hot Reset fails due to an LFPS handshake timeout in U1 or U2, a downstream port shall transition to eSS.Inactive until software intervention or upon detection of removal of an upstream port.
  2. If a Hot Reset fails due to a TS1/TS2 handshake timeout, a downstream port shall transition to Rx.Detect and attempt a Warm Reset.
- If the downstream port is in eSS.Disabled, an Inband Reset is prohibited.

If a “BH_PORT_RESET” is directed, Warm Reset shall be issued, and the following shall occur:

- A downstream port shall initiate a Warm Reset in all the link states except eSS.Disabled and transition to Rx.Detect.
- An upstream port shall enable its LFPS receiver and Warm Reset detector in all the link states except eSS.Disabled.
- An upstream port receiving Warm Reset shall transition to Rx.Detect. Refer to Section 6.9.3 for Warm Reset Detection.

## 7.5 Link Training and Status State Machine (LTSSM)

Link Training and Status State Machine (LTSSM) is a state machine defined for link connectivity and the link power management. LTSSM consists of 12 different link states that can be characterized based on their functionalities. First, there are four operational link states, U0, U1, U2, and U3. U0 is a state where an Enhanced SuperSpeed link is enabled. Packet transfers are in progress or the link is idle. U1 is low power link state where no packet transfer is carried out and the Enhanced SuperSpeed link connectivity can be disabled to allow opportunities for saving the link power. U2 is also a low power link state. Compared with U1, U2 allows for further power saving opportunities with a penalty of increased exit latency. U3 is a link suspend state where aggressive power saving opportunities are possible.

Second, there are four link states, Rx.Detect, Polling, Recovery, and Hot Reset, that are introduced for link initialization and training. Rx.Detect represents the initial power-on link state where a port is attempting to determine if its Enhanced SuperSpeed link partner is present. Upon detecting the presence of an Enhanced SuperSpeed link partner, the link training process will be started. Polling is a link state that is defined for the two link partners to have their Enhanced SuperSpeed transmitters and receivers trained, synchronized, and ready for packet transfer. Recovery is a link state defined for retraining the link when the two link partners exit from a low power link state, or when a link partner has detected that the link is not operating in U0 properly and the link needs to be retrained, or when a link partner decides to change the mode of link operation. Hot Reset is a state defined to allow a downstream port to reset its upstream port.

Third, two other link states, Loopback and Compliance Mode, are introduced for bit error test and transmitter compliance test. Finally, two more link states are defined. eSS.Inactive is a link error

7-45

Universal Serial Bus 3.1 Specification

state where a link is in a non-operable state and software intervention is needed. eSS.Disabled is a link state where Enhanced SuperSpeed connectivity is disabled and the link may operate under USB 2.0 mode.

Configuration information and requests to initiate LTSSM state transitions are mainly controlled by software. All LTSSM references to “directed” refers to upper layer mechanisms.

There are also various timers defined and implemented for LTSSM in order to ensure the successful operation of LTSSM. The timeout values are summarized in Table 7-12. All timers used in the link layer have a tolerance of 0~+50% accuracy with exception of the U2 inactivity timer (refer to Section 10.4.1 for U2 inactivity timer accuracy). All timeout values must be set to the specified values after PowerOn Reset or Inband Reset. All counters must be also initialized after PowerOn Reset or Inband Reset.

In the state machine descriptions, lists of state entry and exit conditions are not prioritized.

State machine diagrams are overviews and may not include all the transition conditions.

Table 7-12. LTSSM State Transition Timeouts

[tbl-100.md](tbl-100.md)

7-46

Link Layer

[tbl-101.md](tbl-101.md)

Notes:

1. Implementations are recommended to consider system states when choosing when to use a larger value of the tRxDetectQuietTimeoutDFP timer. Using a smaller value when the system is active and a larger value when the system is in a standby/sleep or other idle state allows for higher responsiveness to connect events during active states while enabling power savings in an idle system state.

2. Upon Polling timeout, a port shall transition to different states. Refer to Section 7.5.4.3 for details.

3. The accuracy of U2 inactivity timer is specified in Section 10.4.1.

All state machines diagrams have descriptions for transition conditions. These descriptions are informative only. The exact implementation of the state transitions shall follow the description in each section.

7-47

Universal Serial Bus 3.1 Specification

![img-177.jpeg](img-177.jpeg)

Note: Transition conditions are illustrative only. Not all of the transition conditions are listed.

U-047A

Figure 7-14. State Diagram of the Link Training and Status State Machine

7-48

Link Layer

### 7.5.1 eSS.Disabled

eSS.Disabled is a state with a port's low-impedance receiver termination removed. It is a state where a port's Enhanced SuperSpeed connectivity is disabled. Refer to Section 10.18 for details regarding the behavior of a peripheral device. Refer to Sections 10.3 to 10.6 for behaviors regarding a hub's upstream port and downstream port.

eSS.Disabled does not contain any substates in the case of downstream ports and hub upstream ports. For a peripheral upstream port, it contains two substates, eSS.Disabled.Default and eSS.Disabled.Error.

eSS.Disabled is also a logical power-off state for a self-powered hub upstream port.

eSS.Disabled.Default is also a logical power-off state for a self-powered peripheral upstream port.

A downstream port shall transition to this state from any other state when directed.

A self-powered hub or peripheral upstream port shall transition to this state when VBUS is not valid.

#### 7.5.1.1 eSS.Disabled for Downstream Ports and Hub Upstream Ports

eSS.Disabled for Downstream Ports and Hub Upstream Ports does not contain any substates.

##### 7.5.1.1.1 eSS.Disabled Requirements

- VBUS may be present during eSS.Disabled.
- The port's receiver termination shall present high impedance to ground of $Z_{RX-HIGH-IMP-DC-POS}$ defined in Table 6-21.
- The port shall be disabled from transmitting and receiving LFPS and Enhanced SuperSpeed signals.

##### 7.5.1.1.2 Exit from eSS.Disabled

- A downstream port shall transition to Rx.Detect when directed.
- An upstream port shall transition to Rx.Detect only when VBUS transitions to valid or a USB 2.0 bus reset is detected.

#### 7.5.1.2 eSS.Disabled for Upstream Ports of Peripheral Devices

eSS.Disabled of a peripheral device operates similarly to hub upstream ports, except that it only attempts a limited number of Enhanced SuperSpeed attempts upon USB 2.0 bus reset.

##### 7.5.1.2.1 eSS.Disabled Substate Machine

eSS.Disabled of a peripheral device has two substates shown in Figure 7-15.

- eSS.Disabled.Default
- eSS.Disabled.Error

eSS.Disabled.Default is a logical power-off state for a self-powered peripheral device.

7-49

Universal Serial Bus 3.1 Specification

### 7.5.1.2.2 eSS.Disabled Requirements

The requirements of a peripheral upstream port are the same as defined in Section 7.5.1.1.1. In addition, a peripheral upstream port shall implement a tDisabledCount counter. The operation of the tDisabledCount counter shall meet the following requirement.

- The tDisabledCount counter shall be reset to zero upon one of the following two conditions:

1. Invalid VBUS
2. Successful port configuration exchange

- The tDisabledCount counter shall be incremented upon entry to eSS.Disabled.Default.

### 7.5.1.2.3 Exit from eSS.Disabled.Default

- A peripheral upstream port shall transition to Rx.Detect if one of the following conditions are met:

1. When VBUS transitions to valid.
2. When a USB 2.0 bus reset is detected and tDisabledCount is less than 3.

- A peripheral upstream port shall transition to eSS.Disabled.Error if tDisabledCount is 3.

### 7.5.1.2.4 Exit from eSS.Disabled.Error

- A peripheral upstream port shall transition to Rx.Detect upon PowerOn reset.
- A self-powered peripheral upstream port shall transition to eSS.Disabled.Default upon detection of invalid VBUS.
- A peripheral upstream port shall remain in eSS.Disabled.Error upon detection of USB 2.0 bus reset.

![img-178.jpeg](img-178.jpeg)

Figure 7-15. eSS.Disabled Substate Machine

7-50

Link Layer

### 7.5.2 eSS.Inactive

eSS.Inactive is a state where a link has failed Enhanced SuperSpeed operation. A downstream port can only exit from this state when directed, or upon detection of an absence of a far-end receiver termination (R_RX-DC) specified in Table 6-21, or upon a Warm Reset. An upstream port can only exit to Rx.Detect upon a Warm Reset, or upon detecting an absence of a far-end receiver termination (R_RX-DC) specified in Table 6-21.

During eSS.Inactive, a port periodically performs a far-end receiver termination detection. If a disconnection is detected, a port will return to Rx.Detect. If a disconnect is not detected, the link will stay in eSS.Inactive until software intervention.

#### 7.5.2.1 eSS.Inactive Substate Machines

eSS.Inactive contains the following substate machines shown in Figure 7-16:

- eSS.Inactive.Disconnect.Detect
- eSS.Inactive.Quiet

#### 7.5.2.2 eSS.Inactive Requirements

- VBUS shall be present.
- The receiver termination shall meet the requirement (R_RX-DC) specified in Table 6-21.
- The transmitter common mode is not required to be within specification during this state.

#### 7.5.2.3 eSS.Inactive.Quiet

eSS.Inactive.Quiet is a substate defined in which a port has disabled its far-end receiver termination detection so that extra power can be saved while waiting for software intervention.

##### 7.5.2.3.1 eSS.Inactive.Quiet Requirements

- The function of the far-end receiver termination detection shall be disabled.
- A 12-ms timer (teSSInactiveQuietTimeout) shall be started upon entry to the substate.

##### 7.5.2.3.2 Exit from eSS.Inactive.Quiet

- The port shall transition to eSS.Inactive.Disconnect.Detect upon the 12-ms timer timeout (teSSInactiveQuietTimeout).
- A downstream port shall transition to eSS.Disabled when directed.
- A downstream port shall transition to Rx.Detect when Warm Reset is issued.
- An upstream port shall transition to Rx.Detect upon detection of Warm Reset.

#### 7.5.2.4 eSS.Inactive.Disconnect.Detect

eSS.Inactive.Disconnect.Detect is a substate in which a port will perform the far-end receiver termination detection in order to determine if its link partner is disconnected during eSS.Inactive, or if the transition to eSS.Inactive is due to a disconnect from its link partner.

##### 7.5.2.4.1 eSS.Inactive.Disconnect.Detect Requirements

The transmitter shall perform the far-end receiver termination detection described in Section 6.11.

##### 7.5.2.4.2 Exit from eSS.Inactive.Disconnect.Detect

- The port shall transition to Rx.Detect when a far-end low-impedance receiver termination (R_RX-DC) meeting specification defined in Table 6-21 is not detected.

7-51

Universal Serial Bus 3.1 Specification

- The port shall transition to eSS.Inactive.Quiet when a far-end low-impedance receiver termination (R_RX-DC) meeting specification defined in Table 6-21 is detected.

![img-179.jpeg](img-179.jpeg)

Figure 7-16. eSS.Inactive Substate Machine

### 7.5.3 Rx.Detect

Rx.Detect is the power on state of the LTSSM for both a downstream port and an upstream port. It is also the state for a downstream port upon issuing a Warm Reset, and the state for an upstream port upon detecting a Warm Reset from any other link state except eSS.Disabled. The purpose of Rx.Detect is to detect the impedance of far-end receiver termination to ground. Rx.Detect.Reset is a default reset state used by the two ports to synchronize the operation after a Warm Reset; this substate exits immediately if Warm Reset is not present. Rx.Detect.Active is a substate for far-end receiver termination detection. Rx.Detect.Quiet is a power saving substate in which the function of a far-end receiver termination detection is disabled. A port will perform the far-end receiver termination detection periodically during Rx.Detect.

#### 7.5.3.1 Rx.Detect Substate Machines

Rx.Detect contains a substate machine shown in Figure 7-17 with the following substates:

- Rx.Detect.Reset
- Rx.Detect.Active
- Rx.Detect.Quiet

#### 7.5.3.2 Rx.Detect Requirements

- The transmitter common mode is not required to be within specification during this state.
- The low-impedance receiver termination (R_RX-DC) defined in Table 6-21 shall be maintained.

7-52

Link Layer

### 7.5.3.3 Rx.Detect.Reset

Rx.Detect.Reset is a substate designed for the two ports to synchronize their operations on Warm Reset. In this substate, a downstream port shall generate Warm Reset when directed. If an upstream port enters Rx.Detect upon detection of Warm Reset, it shall remain in this substate until the completion of Warm Reset.

For a port entering Rx.Detect not due to a Warm Reset, it shall exit immediately.

#### 7.5.3.3.1 Rx.Detect.Reset Requirements

If a port enters Rx.Detect upon a Warm Reset, the following requirements shall be applied. Refer to Section 6.9.3 for details.

- A downstream port shall transmit Warm Reset for the duration of tReset as defined in Table 6-29.

Note: This includes the case when Hot Reset attempt fails in Recovery. Refer to Section 7.4.2 for details.

- An upstream port shall remain in this state until it detects the completion of Warm Reset.

#### 7.5.3.3.2 Exit from Rx.Detect.Reset

- The port shall transition directly to Rx.Detect.Active if the entry to Rx.Detect is not due to a Warm Reset.

Note: Warm Reset is not present during power-on.

- A downstream port shall transition to Rx.Detect.Active after it transmits Warm Reset for the duration of tReset as defined in Table 6-29.

- A downstream port shall transition to eSS.Disabled when directed.

- An upstream port shall transition to Rx.Detect.Active when it receives no more LFPS Warm Reset signaling from the downstream port as defined in Section 6.9.3.

### 7.5.3.4 Rx.Detect.Active

Rx.Detect.Active is a substate to detect the presence of an Enhanced SuperSpeed link partner. A port will perform a far-end receiver termination detection as defined in Section 6.11.

### 7.5.3.5 Rx.Detect.Active Requirements

- The transmitter shall initiate a far-end receiver termination detection described in Section 6.11.

- The number of far-end receiver termination detection events shall be counted by an upstream port. The detection of far-end receiver termination is defined in Section 6.11.

Note: This count value is used by a peripheral device to determine when it needs to transition to eSS.Disabled. It is also used by a hub to control its downstream port state machine. Refer to Section 10.3.1.1 for details.

### 7.5.3.6 Exit from Rx.Detect.Active

- The port shall transition to Polling upon detection of a far-end low-impedance receiver termination ($R_{RX-DC}$) defined in Table 6-21.

- A downstream port shall transition to Rx.Detect.Quiet when a far-end low-impedance receiver termination ($R_{RX-DC}$) defined in Table 6-21 is not detected.

- A downstream port shall transition to eSS.Disabled when directed.

7-53

Universal Serial Bus 3.1 Specification

- An upstream port of a hub shall transition to Rx.Detect.Quiet when a far-end low-impedance receiver termination (R_RX-DC) defined in Table 6-21 is not detected.
- An upstream port of a peripheral device shall transition to Rx.Detect.Quiet when the following two conditions are met:

1. A far-end low-impedance receiver termination (R_RX-DC) defined in Table 6-21 is not detected.
2. The number of far-end receiver termination detection events is less than eight.

- An upstream port of a peripheral device shall transition to eSS.Disabled when the following two conditions are met:

1. A far-end low-impedance receiver termination (R_RX-DC) defined in Table 6-21 is not detected.
2. The number of far-end receiver termination detection events has reached eight.

Note: This limit on the number of the far-end receiver termination detections is to allow an Enhanced SuperSpeed peripheral device on a legacy platform to transition to USB 2.0 after 80 ms.

### 7.5.3.7 Rx.Detect.Quiet

Rx.Detect.Quiet is a substate where a port has disabled its far-end receiver termination detection.

#### 7.5.3.7.1 Rx.Detect.Quiet Requirements

- The far-end receiver termination detection shall be disabled.
- A downstream port shall start a timer (tRxDetectQuietTimeoutDFP) with a timeout between 12ms and 120ms upon entry to the substate.
- An upstream port shall start a timer (tRxDetectQuietTimeoutUFP) with a timeout of 12ms upon entry to the substate.

#### 7.5.3.7.2 Exit from Rx.Detect.Quiet

- A downstream port shall transition to Rx.Detect.Active upon the timeout of the tRxDetectQuietTimeoutDFP timer (12 ms to 120ms).
- An upstream port shall transition to Rx.Detect.Active upon the timeout of the tRxDetectQuietTimeoutUFP timer (12 ms).
- A downstream port shall transition to eSS.Disabled when directed.

7-54

Link Layer

![img-180.jpeg](img-180.jpeg)

Note: Transition conditions are illustrative only. Not all of the transition conditions are listed.

U-049

Figure 7-17. Rx.Detect Substate Machine

### 7.5.4 Polling

Polling is a state for port capability negotiation and link training. During Polling, a Polling.LFPS handshake shall take place between the two ports in SuperSpeed operation before the link training is started. Similarly for SuperSpeedPlus operation, Polling.LFPS based SCD1/SCD2 handshakes, LBPM based port capability negotiation and match, and subsequent port configuration shall take place before SuperSpeedPlus link training is started. Bit lock, block alignment for SuperSpeedPlus operation, symbol lock, lane polarity inversion, and Rx equalization trainings are achieved using TSEQ, SYNC, TS1, and TS2 training ordered sets.

#### 7.5.4.1 Polling Substate Machines

Polling contains a substate machine shown in Figure 7-18 with the following substates:

- Polling.LFPS
- Polling.LFPSPlus
- Polling.PortMatch
- Polling.PortConfig
- Polling.RxEQ
- Polling.Active
- Polling.Configuration
- Polling.Idle

#### 7.5.4.2 Polling Requirements

- The port shall maintain its low-impedance receiver termination (R_RX-DC) defined in Table 6-21.

7-55

Universal Serial Bus 3.1 Specification

- A downstream port shall implement a counter (cPollingTimeout) to count the number of consecutive transition events from any Polling substate to Rx.Detect due to timeout. The operation of cPollingTimeout shall adhere to the following rules.

1. It shall be reset to zero upon any of the following conditions.

i. PowerOn Reset.
ii. Warm Reset on the upstream port.
iii. Upon exit to eSS.Disabled, or eSS.Inactive, or U0.
iv. Upon detection of the removal of far-end low-impedance receiver termination (R_RX-DC) defined in Table 6-21.

2. It shall be incremented by one or saturated at two if a transition to Rx.Detect is due to timeout in any of the Polling substates.

### 7.5.4.3 Polling.LFPS

Polling.LFPS is a substate designed to establish the PHY's DC operating point, and to synchronize the operations between the two link partners after exiting from Rx.Detect. This is also a substate for a port to identify itself based on various Polling.LFPS signatures.

#### 7.5.4.3.1 Polling.LFPS Requirements

- Upon entry, a LFPS receiver shall be enabled to receive the Polling.LFPS signals defined in Section 6.9.1.
- Upon entry, a port shall establish its LFPS operating condition within 80 μs.
- A downstream port shall disable its transition path to Compliance Mode upon PowerOn Reset or Warm Reset.
- A downstream port shall enable its transition path to Compliance Mode, if directed.
- An upstream port always has its transition path to Compliance Mode enabled upon PowerOn Reset.
- A port in SuperSpeed operation shall transmit Polling.LFPS.
- An upstream port in SuperSpeedPlus operation shall transmit SCD1 defined in Table 6-32. If no signature of SCD1 is found in sixteen consecutive Polling.LFPS received, the port shall switch to SuperSpeed operation and transmit Polling.LFPS instead of SCD1.
- A downstream port in SuperSpeedPlus operation shall transmit SCD1 defined in Table 6-32 if Compliance Mode is disabled. If no signature of SCD1 is found in sixteen consecutive Polling.LFPS received, the port shall switch to SuperSpeed operation and transmit Polling.LFPS instead of SCD1.
- A downstream port in SuperSpeedPlus operation shall transmit SCD2 if Compliance Mode is enabled.

Note: In case a retimer is connected to the downstream port, SCD2 is used for the retimer to enable Compliance Mode. Refer to Appendix E for details.

- A port in SuperSpeedPlus operation shall implement a 60-us timer (tPollingSCDLFPSTimeout) to monitor the absence of LFPS signal after the completion of SuperSpeed Polling.LFPS handshake.
- A port in SuperSpeedPlus operation shall be ready for SuperSpeed operation if it has detected that its link partner operates at SuperSpeed.

Note: There is no time allocated for a SuperSpeedPlus port to re-configure itself for SuperSpeed operation upon detection of its link partner operating at SuperSpeed. A SuperSpeedPlus port shall switch to SuperSpeed operation as quickly as possible for its

7-56

Link Layer

receiver equalization training. Any time for configuration will result in receiving fewer TSEQ ordered sets from its link partner.

- A port shall disable its transition path to Compliance Mode when it has successfully completed Polling.LFPS handshake or has entered Compliance Mode.
- A 360-ms timer (tPollingLFPSTimeout) shall be started upon entry to the substate.
- The operating condition of an eSS PHY shall be established when a port is ready to exit to Polling.RxEQ.
- An eSS receiver in SuperSpeed operation may optionally be enabled to receive TSEQ ordered sets for receiver equalizer training.

Note: The port first entering Polling.RxEQ will start transmitting TSEQ ordered sets while the other port is still in Polling.LFPS. Enabling a SuperSpeed receiver in Polling.LFPS will allow a port to start the receiver equalizer training while completing the requirement for Polling.LFPS exit handshake.

### 7.5.4.3.2 Exit from Polling.LFPS

- The port in SuperSpeed operation shall transition to Polling.RxEQ when the following three conditions are met:

1. At least 16 consecutive Polling.LFPS bursts meeting the Polling.LFPS specification defined in Section 6.9 are sent.
2. Two consecutive Polling.LFPS bursts are received.
3. Four consecutive Polling.LFPS bursts are sent after receiving one Polling.LFPS burst.

- The port in SuperSpeedPlus operation shall transition to Polling.LFPSPlus if two SCD1 are transmitted after one SCD1 or SCD2 as defined in Section 6.9.4.2 is received.
- The port in SuperSpeedPlus operation shall transition to Polling.RxEQ and switch to SuperSpeed operation if the following conditions are met:

1. At least two consecutive Polling.LFPS bursts are received.
2. Twenty Polling.LFPS bursts are transmitted, and no SCD1 is detected.

Note: This condition guarantees that, in the case of a port in SuperSpeedPlus operation connecting to a port in SuperSpeed operation, a port in SuperSpeed operation will receive twenty consecutive Polling.LFPS to exit from this substate if it is unable to recognize Polling.LFPS with varying tRepeat in SCD1.

3. No LFPS signal for more than tPollingSCDLFPSTimeout is observed.

Note: This condition implies the SuperSpeed link partner has entered Polling.RxEQ transmitting TSEQ ordered sets.

- An upstream port shall transition to Compliance Mode upon the 360-ms timer timeout (tPollingLFPSTimeout) and the following two conditions are met:

1. The port has never successfully completed Polling.LFPS after PowerOn Reset.
2. The condition to transition to Polling.RxEQ or Polling.LFPSPlus is not met.

Note: If the very first attempt in Polling.LFPS handshake fails after PowerOn Reset, it implies that a passive test load may be present and compliance test should be initiated. If the very first attempt in Polling.LFPS handshake succeeds after PowerOn Reset, it implies the presence of the Enhanced SuperSpeed ports on each side of the link and no compliance test is intended. Therefore, any subsequent handshake timeout in Polling.LFPS when the link is retrained is only an indication of link training failure, not a signal to enter Compliance Mode.

7-57

Universal Serial Bus 3.1 Specification

- A downstream port shall transition to Compliance Mode upon the 360-ms timer timeout (tPollingLFPSTimeout) if the following three conditions are met:

1. The Compliance Mode is enabled.
2. The port has never successfully completed Polling.LFPS handshake after Compliance Mode is enabled.
3. The condition to transition to Polling.RxEQ or Polling.LFPSPlus is not met.

Note: In case Compliance mode is disabled, a downstream port may enter Rx.Detect attempting Polling.LFPS handshake again, or enter eSS.Inactive for SW intervention based on the count value of cPollingTimeout.

- A downstream port shall transition to Rx.Detect upon the 360-ms timer timeout (tPollingLFPSTimeout) if cPollingTimeout is less than two and Compliance Mode is disabled.
- A downstream port shall transition to eSS.Inactive upon the 360-ms timer timeout (tPollingLFPSTimeout) and cPollingTimeout is two.
- An upstream port of a hub shall transition to Rx.Detect upon the 360-ms timeout (tPollingLFPSTimeout) after having trained once since PowerOn Reset and the conditions to transition to Polling.RxEQ are not met.
- A peripheral device shall transition to eSS.Disabled upon the 360-ms timeout (tPollingLFPSTimeout) after having trained once since PowerOn Reset and the conditions to transition to Polling.RxEQ are not met.
- A downstream port shall transition to eSS.Disabled when directed.
- A downstream port shall transition to Rx.Detect when directed to issue Warm Reset.
- An upstream port shall transition to Rx.Detect when Warm Reset is detected.

### 7.5.4.4 Polling.LFPSPlus

Polling.LFPSPlus is a substate where the port SuperSpeedPlus operation performs SCD2 handshake, for additional confirmation of the SuperSpeedPlus capability of its link partner.

#### 7.5.4.4.1 Polling.LFPSPlus Requirements

- The port in SuperSpeedPlus operation shall transmit SCD2 defined in Table 6-32. If SCD2 cannot be found in sixteen consecutive Polling.LFPS received, it shall transmit Polling.LFPS instead of SCD2.

Note: This is an extreme case where a port in SuperSpeed operation transmits Polling.LFPS coinciding with SCD1 and remains in Polling.LFPS.

- The operation of the 360-ms timer (tPollingLFPSTimeout) shall continue without reset upon entry to this substate from Polling.LFPS.
- A port in SuperSpeedPlus operation shall be ready for SuperSpeed operation if it has detected that its link partner operates at SuperSpeed.
- A port in SuperSpeedPlus operation shall implement a 60-us timer (tPollingSCDLFPSTimeout) to monitor the absence of LFPS signal after the completion of SuperSpeed Polling.LFPS handshake.

#### 7.5.4.4.2 Exit from Polling.LFPSPlus

- The port in SuperSpeedPlus operation shall transition to Polling.PortMatch if two SCD2 are transmitted after one SCD2 as defined in Section 6.9.4.2 is received.
- A port in SuperSpeedPlus operation shall transition to Polling.RxEQ and switch to SuperSpeed operation if the following two conditions are met:

7-58

Link Layer

1. No LFPS signal for more than tPollingSCDLFPSTimeout is observed.

Note: This condition implies the SuperSpeed link partner has entered Polling.RxEQ transmitting TSEQ ordered sets.

2. Twenty Polling.LFPS bursts are transmitted, after finding no SCD2 is detected.

Note: This condition guarantees that, in the case of a port in SuperSpeedPlus operation connecting to a port in SuperSpeed operation, a port in SuperSpeed operation will receive twenty consecutive Polling.LFPS to exit from this substate if it is unable to recognize Polling.LFPS with varying tRepeat in SCD1 and SCD2, and it happens to transmit Polling.LFPS matching SCD1.

- A downstream port shall transition to Rx.Detect upon the 360-ms timer timeout (tPollingLFPSTimeout) and cPollingTimeout is less than two.
- A downstream port shall transition to eSS.Inactive upon the 360-ms timer timeout (tPollingLFPSTimeout) and cPollingTimeout is two.
- An upstream port of a hub shall transition to Rx.Detect upon the 360-ms timeout (tPollingLFPSTimeout).
- A peripheral device shall transition to eSS.Disabled upon the 360-ms timeout (tPollingLFPSTimeout).
- A downstream port shall transition to eSS.Disabled when directed.
- A downstream port shall transition to Rx.Detect when directed to issue Warm Reset.
- An upstream port shall transition to Rx.Detect when Warm Reset is detected.

### 7.5.4.5 Polling.PortMatch

Polling.PortMatch is a substate where the two ports in SuperSpeedPlus operation perform the LBPM handshake, for announcing, matching, and deciding the operation on the highest common capability between the two link partners. The LBPM handshake includes two stages of operation. The first stage is to announce LBPM PHY Capability as defined in Table 7-13 below. The second stage is for each port to decode LBPM PHY Capability and adjust to the highest common PHY Capability by transmitting PHY Capability Match.

#### 7.5.4.5.1 PHY Capability LBPM Definition

SuperSpeedPlus PHY Capability is defined based on the following LBPM. Refer to Section 6.9.5 for LBPM details.

Table 7-13. PHY Capability LBPM

[tbl-102.md](tbl-102.md)

Two types of LBPM are defined. PHY Capability LBPM is used to announce a port's PHY capabilities. The initial value shall describe a port's highest PHY capabilities. The announced capabilities may later be adjusted in order to match the link partner's capabilities or if the link fails to reach U0 during training and the two ports need to fall back to a lower rate.

7-59

Universal Serial Bus 3.1 Specification

PHY Ready LBPM is defined for a port to send a notification that it has completed its PHY re-configuration and ready for link training at the matched port capability defined by PHY Capability LBPM. Refer to Section 7.5.4.6 for use of PHY Ready LBPM.

### 7.5.4.5.2 Polling.PortMatch Requirements

- A 12-ms timer (tPollingLBPMLFPSTimeout) shall be started upon entry to the substate.
- Upon entry to this substate from Polling.LFPSPlus, the port shall transmit continuous PHY Capability LBPMs defined in Table 7-13 to announce its highest PHY Capability.
- Upon entry to this substate from Polling.Active, or Polling.Configuration, or Polling.Idle, the port shall transmit continuous PHY Capability LBPMs defined in Table 7-13 to announce its next highest PHY Capability from its previous PHY Capability.
- The port shall decode received PHY Capability LBPM or PHY Ready LBPM and compare to its own PHY Capability.
- The port with higher PHY capability shall adjust its PHY capability by transmitting PHY Capability LBPM that matches its link partner's.
- The port with lower PHY capability shall continue transmitting its own PHY Capability LBPMs and monitoring the PHY Capability LBPMs from its link partner.
- The two ports shall continue the interactive process of PHY Capability LBPM exchange as described above until they match the PHY Capability.

### 7.5.4.5.3 Exit from Polling.PortMatch

- The port shall transition to Polling.PortConfig when four consecutive and matched PHY Capability LBPMs are sent after two consecutive and matched PHY Capability LBPMs or PHY Ready LBPMs are received.
Note: A port exiting from Polling.PortMatch and ready for PHY operation without re-configuration may immediately transmit PHY Ready LBPMs.
- A downstream port shall transition to Rx.Detect upon the 12-ms timer timeout (tPollingLBPMLFPSTimeout) and cPollingTimeout is less than two.
- A downstream port shall transition to eSS.Inactive upon the 12-ms timer timeout (tPollingLBPMLFPSTimeout) and cPollingTimeout is two.
- An upstream port of a hub shall transition to Rx.Detect upon the 12-ms timer timeout (tPollingLBPMLFPSTimeout) and the conditions to transition to Polling.PortConfig are not met.
- A peripheral device shall transition to eSS.Disabled upon the 12-ms timer timeout (tPollingLBPMLFPSTimeout) and the conditions to transition to Polling.PortConfig are not met.
- A downstream port shall transition to eSS.Disabled when directed.
- A downstream port shall transition to Rx.Detect when directed to issue Warm Reset.
- An upstream port shall transition to Rx.Detect when Warm Reset is detected.

### 7.5.4.6 Polling.PortConfig

Polling.PortConfig is a substate where a port configures its PHY according to PHY Capability LBPM matched in Polling.PortMatch, and synchronizes with its link partner in exiting from this substate to Polling.RxEQ. Depending on matched PHY Capability LBPM, a port may configure its PHY for SuperSpeed operation or SuperSpeedPlus operation.

7-60

Link Layer

### 7.5.4.6.1 Polling.PortConfig Requirements

- The operation of the 12-ms timer (tPollingLBPMLFPSTimeout) shall continue without reset upon entry to the substate from Polling.PortMatch.
- Upon entry to this state, the port shall place its transmitter in electrical idle if it is preparing its PHY re-configuration according to PHY Capability LBPM negotiated in Polling.PortMatch. The port shall perform the following PHY re-configuration.

1. The transmitter DC common mode voltage shall be within specification (VTX-CM-DCACTIVE-IDLE-DELTA) defined in Table 6-18.
2. The port shall maintain its low-impedance receiver termination (RRX-DC) defined in Table 6-21.
3. The port shall be ready to transmit TSEQ OS.
4. The port shall be ready to receive TSEQ OS for receiver equalization training.

- Upon completion of PHY re-configuration, the port shall transmit consecutive PHY Ready LBPMs to notify its link partner. Refer to Table 7-13 for PHY Ready LBPM definition.

### 7.5.4.6.2 Exit from Polling.PortConfig

- The port shall transition to Polling.RxEQ when four consecutive and matched PHY Ready LBPMs are sent after two consecutive and matched PHY Ready LBPMs are received.
- A downstream port shall transition to Rx.Detect upon the 12-ms timer timeout (tPollingLBPMLFPSTimeout) and cPollingTimeout is less than two.
- A downstream port shall transition to eSS.Inactive upon the 12-ms timer timeout (tPollingLBPMLFPSTimeout) and cPollingTimeout is two.
- An upstream port of a hub shall transition to Rx.Detect upon the 12-ms timer timeout (tPollingLBPMLFPSTimeout) and the conditions to transition to Polling.RxEQ are not met.
- A peripheral device shall transition to eSS.Disabled upon the 12-ms timer timeout (tPollingLBPMLFPSTimeout) and the conditions to transition to Polling.RxEQ are not met.
- A downstream port shall transition to eSS.Disabled when directed.
- A downstream port shall transition to Rx.Detect when directed to issue Warm Reset.
- An upstream port shall transition to Rx.Detect when Warm Reset is detected.

### 7.5.4.7 Polling.RxEQ

Polling.RxEQ is a substate for receiver equalization training. A port is required to complete its receiver equalization training.

### 7.5.4.7.1 Polling.RxEQ Requirements

- The detection and correction of the lane polarity inversion in SuperSpeed operation shall be enabled, as is described in Section 6.4.2.
- The port shall transmit the corresponding TSEQ ordered sets defined in Table 6-2.
- The port shall complete receiver equalizer training upon exit from this substate.

Note: A situation may exist where the port entering Polling.RxEQ earlier is transmitting TSEQ ordered sets while its link partner is still sending Polling.LFPS to satisfy the exit conditions from Polling.LFPS or Polling.LFPSPlus to Polling.RxEQ. In this situation, if its link partner is in electrical idle, near-end cross talk may cause the port to train its Rx equalizer using its own TSEQ ordered sets. To avoid a receiver from training itself, a port may either ignore the beginning part (about 30 μs) of the TSEQ ordered sets, or continue the equalizer training until it completes the transmission of TSEQ ordered sets.

7-61

Universal Serial Bus 3.1 Specification

### 7.5.4.7.2 Exit from Polling.RxEQ

- The port in SuperSpeed operation shall transition to Polling.Active after 65,536 consecutive TSEQ ordered sets defined in Table 6-2 are transmitted.
- The port in SuperSpeedPlus operation shall transition to Polling.Active after 262,143 TSEQ ordered sets defined in Table 6-8 are transmitted. Refer to Section 6.4.1.2.1 for SYNC ordered set insertion while transmitting TSEQ ordered sets.
- A downstream port shall transition to eSS.Disabled when directed.
- A downstream port shall transition to Rx.Detect when directed to issue Warm Reset.
- An upstream port shall transition to Rx.Detect when Warm Reset is detected.

### 7.5.4.8 Polling.Active

Polling.Active is a substate that continues the link's Enhanced SuperSpeed training.

#### 7.5.4.8.1 Polling.Active Requirements

- A 12-ms timer (tPollingActiveTimeout) shall be started upon entry to this substate.
- The port shall transmit TS1 ordered sets.
- The port in SuperSpeedPlus operation shall insert a SYNC ordered set every 32 TS1 ordered sets.
- The port in SuperSpeedPlus operation shall perform block alignment and scrambler synchronization as defined in sections 6.3.2.3 and 6.4.1.2.4 of Chapter 6.
- Lane polarity detection and correction shall be completed.
- The port that fails to achieve a successful training with its link partner shall reconfigure itself for the next capability it supports.
- Note: An example of this is, when a SuperSpeedPlus port fails to reach successful handshake with its link partner, it shall re-configure itself for SuperSpeed operation.
- The receiver is in training using TS1 or TS2 ordered sets.
- Note: Depending on the link condition and different receiver implementations, one port's receiver may train faster than the other. When this occurs, the port whose receiver trains first will enter Polling.Configuration and start transmitting TS2 ordered sets while the port whose receiver is not yet trained is still in Polling.Active using TS2 ordered sets to train its receiver.

#### 7.5.4.8.2 Exit from Polling.Active

- The port in SuperSpeed operation shall transition to Polling.Configuration upon receiving eight consecutive and identical TS1 or TS2 ordered sets.
- The port in SuperSpeedPlus operation shall transition to Polling.Configuration upon receiving eight consecutive and identical TS1 or TS2 ordered sets, excluding symbols 14 and 15 of TS1 or TS2 ordered sets.
Note: SYNC OS and SKP OS in between TS1 OS and/or TS2 OS do not disqualify the consecutive detection of TS1 OS and TS2 OS. Symbols 14 and 15 are used for TS1 or TS2 ordered set identifier or DC balance adjustment.
- A downstream port in SuperSpeed operation shall transition to Rx.Detect upon the 12-ms timer timeout (tPollingActiveTimeout) and the following two conditions are met.
1. The conditions to transition to Polling.Configuration are not met.
2. cPollingTimeout is less than two.
- A downstream port in SuperSpeed operation shall transition to eSS.Inactive upon the 12-ms timer timeout (tPollingActiveTimeout) and the following two conditions are met.

7-62

Link Layer

1. The conditions to transition to Polling.Configuration are not met.
2. cPollingTimeout is two.

- An upstream port of a hub in SuperSpeed operation shall transition to Rx.Detect upon the 12-ms timer timeout (tPollingActiveTimeout) and the conditions to transition to Polling.Configuration are not met.
- An upstream port of a peripheral device in SuperSpeed operation shall transition to eSS.Disabled upon the 12-ms timer timeout (tPollingActiveTimeout) and the conditions to transition to Polling.Configuration are not met.
- A downstream port in SuperSpeedPlus operation shall transition to Polling.PortMatch to negotiate for alternative operation upon the 12-ms timer timeout (tPollingActiveTimeout) and the conditions to transition to Polling.Configuration are not met.
- An upstream port of a hub in SuperSpeedPlus operation shall transition to Polling.PortMatch to negotiate for alternative operation upon the 12-ms timer timeout (tPollingActiveTimeout) and the conditions to transition to Polling.Configuration are not met.
- An upstream port of a peripheral device in SuperSpeedPlus operation shall transition to Polling.PortMatch to negotiate for alternative operation upon the 12-ms timer timeout (tPollingActiveTimeout) and the conditions to transition to Polling.Configuration are not met.
- A downstream port shall transition to eSS.Disabled when directed.
- A downstream port shall transition to Rx.Detect when directed to issue Warm Reset.
- An upstream port shall transition to Rx.Detect when Warm Reset is detected.

### 7.5.4.9 Polling.Configuration

Polling.Configuration is a substate where the two link partners complete the Enhanced SuperSpeed training.

#### 7.5.4.9.1 Polling.Configuration Requirements

- The port shall transmit identical TS2 ordered sets upon entry to this substate and set the link configuration field in the TS2 ordered set based on the following.

1. When directed, a downstream port shall set Reset bit in the TS2 ordered set.

Note: An upstream port can only set the Reset bit in the TS2 ordered set when in Hot Reset. Active. Refer to Section 7.5.12.3 for details.

2. When directed, the port shall set Loopback bit in the TS2 ordered set.
3. When directed, the port shall set the Disabling Scrambling bit in the TS2 ordered set.

- The port in SuperSpeedPlus operation shall insert a SYNC ordered set every 32 TS2 ordered sets.
- The port in SuperSpeedPlus operation shall perform block alignment and scrambler synchronization as defined in Sections 6.3.2.3 and 6.4.1.2.4 of Chapter 6.
- The port that fails to achieve a successful training with its link partner shall reconfigure itself for the next capability it supports.

Note: An example of this is, when a SuperSpeedPlus port fails to reach successful handshake with its link partner, it shall re-configure itself for SuperSpeed operation.

- A 12-ms timer (tPollingConfigurationTimeout) shall be started upon entry to this substate.

#### 7.5.4.9.2 Exit from Polling.Configuration

- The port in SuperSpeed operation shall transition to Polling.Idle when the following two conditions are met:

7-63

Universal Serial Bus 3.1 Specification

1. Eight consecutive and identical TS2 ordered sets are received.
2. Sixteen TS2 ordered sets are sent after receiving the first of the eight consecutive and identical TS2 ordered sets.

- The port in SuperSpeedPlus operation shall transition to Polling.Idle when the following two conditions are met:

1. Eight consecutive and identical TS2 ordered sets, excluding symbols 14 and 15, are received.
2. Sixteen TS2 ordered sets are sent after receiving the first of the eight consecutive and identical TS2 ordered sets, excluding symbols 14 and 15.

Note: SYNC OS and SKP OS in between TS2 OS do not disqualify the consecutive detection of TS2 OS.

- A downstream port in SuperSpeed operation shall transition to Rx.Detect upon the 12-ms timer timeout (tPollingConfigurationTimeout) and the following two conditions are met.

1. The conditions to transition to Polling.Idle are not met.
2. cPollingTimeout is less than two.

- A downstream port in SuperSpeed operation shall transition to eSS.Inactive upon the 12-ms timer timeout (tPollingConfigurationTimeout) and the following two conditions are met.

1. The conditions to transition to Polling.Idle are not met.
2. cPollingTimeout is two.

- An upstream port of a hub in SuperSpeed operation shall transition to Rx.Detect upon the 12-ms timer timeout (tPollingConfigurationTimeout) and the conditions to transition to Polling.Idle are not met.

- An upstream port of a peripheral device in SuperSpeed operation shall transition to eSS.Disabled upon the 12-ms timer timeout (tPollingConfigurationTimeout) and the conditions to transition to Polling.Idle are not met.

- A downstream port in SuperSpeedPlus operation shall transition to Polling.PortMatch to negotiate for alternative operation upon the 12-ms timer timeout (tPollingConfigurationTimeout) and the conditions to transition to Polling.Idle are not met.

- An upstream port of a hub in SuperSpeedPlus operation shall transition to Polling.PortMatch to negotiate for alternative operation upon the 12-ms timer timeout (tPollingConfigurationTimeout) and the conditions to transition to Polling.Idle are not met.

- An upstream port of a peripheral device in SuperSpeedPlus operation shall transition to Polling.PortMatch to negotiate for alternative operation upon the 12-ms timer timeout (tPollingConfigurationTimeout) and the conditions to transition to Polling. Idle are not met.

- A downstream port shall transition to eSS.Disabled when directed.

- A downstream port shall transition to Rx.Detect when directed to issue Warm Reset.

- An upstream port shall transition to Rx.Detect when Warm Reset is detected.

### 7.5.4.10 Polling.Idle

Polling.Idle is a substate where the port decodes the TS2 ordered set received in Polling.Configuration and determines the next state.

### 7.5.4.10.1 Polling.Idle Requirements

- The port shall decode the TS2 ordered set received during Polling.Configuration and proceeds to the next state.
- A downstream port shall reset its Link Error Count.

7-64

Link Layer

- An upstream port shall reset its port configuration information to default values. Refer to Sections 8.4.5 and 8.4.6 for details.
- The port in SuperSpeed operation shall enable the scrambling by default if the Disabling Scrambling bit is not asserted in the TS2 ordered set received in Polling.Configuration.
- The port in SuperSpeed operation shall disable the scrambling if directed, or if the Disabling Scrambling bit is asserted in the TS2 ordered set received in Polling.Configuration.
- The port in SuperSpeed operation shall transmit Idle Symbols if the next state is U0. The port may transmit Idle Symbols if the next state is Loopback or HotReset.
- The port in SuperSpeedPlus operation shall transmit a single SDS ordered set before the start of the data blocks with Idle Symbols if the next state is U0. The port may transmit SDS ordered set if the next state is Loopback or Hot Reset.

Note: Under situation where a SKP ordered set is also scheduled at the same time with SDS ordered set, SKP ordered set shall be transmitted first.

- The port in SuperSpeedPlus operation may ignore SDS ordered set if corrupted and continue to process the following data block. The port may optionally choose to recover SDS ordered set if error is detected.
- The port in SuperSpeedPlus operation shall disable the scrambling upon completion of SDS ordered set transmission if directed, or if the Disabling Scrambling bit is asserted in the TS2 ordered set received in Polling.Configuration.
- The port that fails to achieve a successful training with its link partner shall reconfigure itself for the next capability it supports.

Note: An example of this is, when a SuperSpeedPlus port fails to reach successful handshake with its link partner, it shall re-configure itself for SuperSpeed operation.

- A 2-ms timer (tPollingIdleTimeout) shall be started upon entry to this state.
- The port shall be able to receive the Header Sequence Number Advertisement from its link partner.

Note: The exit time difference between the two ports will result in one port entering U0 first and starting the Header Sequence Number Advertisement while the other port is still in Polling.Idle.

### 7.5.4.10.2 Exit from Polling.Idle

- The port shall transition to Loopback when directed as a loopback master and the port is capable of being a loopback master. Refer to Section 7.5.11 for details.
- The port shall transition to Loopback as a loopback slave if the Loopback bit is asserted in the TS2 ordered set received in Polling.Configuration. Refer to Section 7.5.4.9 for details.
- A downstream port shall transition to Hot Reset when directed.
- An upstream port shall transition to Hot Reset when the Reset bit is asserted in the TS2 ordered set received in Polling.Configuration.
- The port shall transition to U0 when the following two conditions are met:

1. Eight consecutive Idle Symbols are received.
2. Sixteen Idle Symbols are sent after receiving one Idle Symbol.

- A downstream port in SuperSpeed operation shall transition to eSS.Disabled when directed.

- A downstream port in SuperSpeed operation shall transition to Rx.Detect upon the 2-ms timer timeout (tPollingIdleTimeout) and the following two conditions are met.

1. The conditions to transition to U0 are not met.
2. cPollingTimeout is less than two.

7-65

Universal Serial Bus 3.1 Specification

- A downstream port in SuperSpeed operation shall transition to eSS.Inactive upon the 2-ms timer timeout (tPollingIdleTimeout) and the following two conditions are met.

1. The conditions to transition to U0 are not met.
2. cPollingTimeout is two.

- An upstream port of a hub in SuperSpeed operation shall transition to Rx.Detect upon the 2-ms timer timeout (tPollingIdleTimeout) and the conditions to transition to U0 are not met.
- An upstream port of a peripheral device in SuperSpeed operation shall transition to eSS.Disabled upon the 2-ms timer timeout (tPollingIdleTimeout) and the conditions to transition to U0 are not met.
- A downstream port in SuperSpeedPlus operation shall transition to Polling.PortMatch to negotiate for alternative operation upon the 2-ms timer timeout (tPollingIdleTimeout) and the conditions to transition U0 are not met.
- An upstream port of a hub in SuperSpeedPlus operation shall transition to Polling.PortMatch to negotiate for alternative operation upon the 2-ms timer timeout (tPollingIdleTimeout) and the conditions to transition to U0 are not met.
- An upstream port of a peripheral device in SuperSpeedPlus operation shall transition to Polling.PortMatch to negotiate for alternative operation upon the 2-ms timer timeout (tPollingIdleTimeout) and the conditions to transition to U0 are not met.
- A downstream port shall transition to Rx.Detect when Warm Reset is directed.
- An upstream port shall transition to Rx.Detect when Warm Reset is detected.

7-66

Link Layer

![img-181.jpeg](img-181.jpeg)

Note: Transition conditions are illustrative only. Not all of the transition conditions are listed.

Figure 7-18. Polling Substate Machine

### 7.5.5 Compliance Mode

Compliance Mode is used to test the transmitter for compliance to voltage and timing specifications. Several different test patterns are transmitted as defined in Table 6-13. Compliance Mode does not contain any substate machines.

Note that for a downstream port, the default setting for entry to Compliance Mode is disabled. It may optionally be enabled when directed. This is to prevent the automatic entry to Compliance Mode due to connection of a bad device that fails to exit from Polling.LFPS upon power-on, or a downstream port fails to respond in time.

#### 7.5.5.1 Compliance Mode Requirements

- The port shall maintain its low-impedance receiver termination (R_RX-DC) defined in Table 6-21.

7-67

Universal Serial Bus 3.1 Specification

- The LFPS receiver is used to control the test pattern sequencing.
- Upon entry to Compliance Mode, the port shall wait until its eSS Tx DC common mode voltage meets the VTX-DC-CM specification defined in Table 6-18 before it starts to send the first compliance test pattern defined in Table 6-13.
- The port shall transmit the next compliance test pattern continuously upon detection of a Ping.LFPS as defined in Section 6.9.1.
- The port shall transmit the first compliance test pattern continuously upon detection of a Ping.LFPS and the test pattern has reached the final test pattern.

### 7.5.5.2 Exit from Compliance Mode

- A downstream port shall transition to Rx.Detect when directed to issue Warm Reset.
- An upstream port shall transition to Rx.Detect upon detection of Warm Reset.
- A downstream port shall transition to eSS.Disabled when directed.

### 7.5.6 U0

U0 is the normal operational state where packets can be transmitted and received. U0 does not contain any substate machines.

### 7.5.6.1 U0 Requirements

- The port shall meet the transmitter specifications defined in Table 6-17.
- The port shall maintain the low-impedance receiver termination (RRX-DC) defined in Table 6-21.
- The LFPS receiver shall be enabled.
- The port shall enable a 1-ms timer (tU0RecoveryTimeout) to measure the time interval between two consecutive link commands. This timer will be reset and restarted every time a link command is received.
- The port shall enable a 10-μs timer (tU0LTimeout). This timer shall be reset when the first symbol of any link command or packet is sent and restarted after the last symbol of any link command or packet is sent. This timer shall be active when the link is in logical idle.
- A downstream port shall transmit a single LDN when the 10-μs timer (tU0LTimeout) expires.
- An upstream port shall transmit a single LUP when the 10-μs timer (tU0LTimeout) expires.

### 7.5.6.2 Exit from U0

- The port shall transition to U1 upon successful completion of LGO_U1 entry sequence. Refer to Section 7.2.4.2 for details.
- The port shall transition to U2 upon successful completion of LGO_U2 entry sequence. Refer to Section 7.2.4.2 for details.
- The port shall transition to U3 upon successful completion of LGO_U3 entry sequence. Refer to Section 7.2.4.2 for details.
- A downstream port shall transition to eSS.Inactive when it fails U3 entry on three consecutive attempts.
- The port shall transition to Recovery upon any errors stated in Section 7.3 that will cause a link to transition to Recovery.
- The port shall transition to Recovery upon detection of a TS1 ordered set.
- The port shall transition to Recovery when directed.

7-68

Link Layer

- The port shall transition to eSS.Inactive when PENDING_HP_TIMER times out for the fourth consecutive time.

Note: This implies the link has transitioned to Recovery for three consecutive times and each time the transition to Recovery is due to PENDING_HP_TIMER timeout.

- A downstream port shall transition to eSS.Disabled when directed.
- A downstream port shall transition to eSS.Inactive when directed.
- An upstream port shall transition to eSS.Disabled when directed.

Note: After entry to U0 and the successful completion of training and link initialization, both ports are required to exchange port capabilities information using Port Capability LMPs within tPortConfiguration time as defined in Section 8.4.5. This includes the following scenarios:

1. Entry to U0 from polling directly;
2. Entry to U0 indirectly from Polling through Hot Reset;
3. Entry to U0 from Recovery and port configuration has not been successfully completed after exiting from Polling. In this case, both ports shall continue the port configuration process by completing the remaining LMP exchanges.

If the port has not received a Port Capability LMP within tPortConfiguration time, a downstream port shall be directed to transition to eSS.Inactive and an upstream port shall be directed to transition to eSS.Disabled.

- A downstream port shall transition to Recovery upon not receiving any link commands within 1 ms (tU0RecoveryTimeout).

Note: Not receiving any link commands including LUP within 1 ms implies either a link is under serious error condition, or an upstream port has been removed. To accommodate for both situations, a downstream port will transition to Recovery and attempt to retrain the link. If the retraining fails, it will then transition to eSS.Inactive. During eSS.Inactive, a downstream port will attempt a far-end receiver termination detection. If it determines that a far-end low-impedance receiver termination ($R_{RX-DC}$) defined in Table 6-21 is not present, it will enter Rx.Detect. Otherwise, it will wait for software intervention.

- An upstream port shall transition to Recovery if it does not receive any link command or any packet (as specified in Section 7.2.4.1.4) within 1 ms (tU0RecoveryTimeout).
- A downstream port shall transition to Rx.Detect when directed to issue Warm Reset.
- An upstream port shall transition to Rx.Detect when Warm Reset is detected.
- An upstream port shall transition to eSS.Disabled upon detection of VBUS off.

Note: this condition only applies to a self-powered upstream port. eSS.Disabled is a logical power-off state for a self-powered upstream port.

7-69

Universal Serial Bus 3.1 Specification

### 7.5.7 U1

U1 is a low power state where no packets are to be transmitted and both ports agree to enter a link state where an Enhanced SuperSpeed PHY can be placed into a low power state.

U1 does not contain any substates. Transitions to other states are shown in Figure 7-19.

#### 7.5.7.1 U1 Requirements

- The Enhanced SuperSpeed transmitter DC common mode voltage shall be within specification (VTX-CM-DC-ACTIVE-IDLE-DELTA) defined in Table 6-18.
- The port shall maintain its low-impedance receiver termination (RRX-DC) defined in Table 6-21.
- The port shall enable its U1 exit detect functionality as defined in Section 6.9.2.
- The port shall enable its LFPS transmitter when it initiates the exit from U1.
- The port shall enable its U2 inactivity timer upon entry to this state if the U2 inactivity timer has a non-zero timeout value.
- A downstream port shall enable its Ping.LFPS detection.
- A downstream port shall enable a 300-ms timer (tU1PingTimeout). This timer will be reset and restarted when a Ping.LFPS is received.
- An upstream port shall transmit Ping.LFPS as defined in Table 6-29.

#### 7.5.7.2 Exit from U1

- A downstream port shall transition to eSS.Disabled when directed.
- A downstream port shall transition to Rx.Detect when the 300-ms timer (tU1PingTimeout) expires.
- A downstream port shall transition to Rx.Detect when directed to issue Warm Reset.
- An upstream port shall transition to Rx.Detect when Warm Reset is detected.
- A self-powered upstream port shall transition to eSS.Disabled upon not detecting valid Vbus as defined in Section 11.4.5.
- The port shall transition to U2 upon the timeout of the U2 inactivity timer defined in Sections 10.4.2.4 and 10.6.2.4.
- The port shall transition to Recovery upon successful completion of a LFPS handshake meeting the U1 LFPS exit handshake signaling in Section 6.9.2.
- The port shall transition to eSS.Inactive upon the 2-ms (tNoLFPSResponseTimeout) LFPS handshake timer timeout and a successful LFPS handshake meeting the U1 LFPS exit handshake signaling in Section 6.9.2 is not achieved.

7-70

Link Layer

![img-182.jpeg](img-182.jpeg)

Note: Transition conditions are illustrative only. Not all of the transition conditions are listed.

U-051

Figure 7-19. U1

### 7.5.8 U2

U2 is a link state where more power saving opportunities are allowed compare to U1, but with an increased exit latency.

U2 does not contain any substates. The transitions to other states are shown in Figure 7-20.

#### 7.5.8.1 U2 Requirements

- The Enhanced SuperSpeed transmitter DC common mode voltage does not need to be within specification (VTX-CM-DC-ACTIVE-IDLE-DELTA) defined in Table 6-18.
- The port shall maintain its low-impedance receiver termination (RRX-DC) defined in Table 6-21.
- When a downstream port is in U2, its upstream port may be in U1 or U2. If the upstream port is in U1, it will send Ping.LFPS periodically. A downstream port shall differentiate between Ping.LFPS and U1 LFPS exit handshake signaling.
- The port shall enable its U2 exit detect functionality as defined in Section 6.9.2.
- The port shall enable its LFPS transmitter when it initiates the exit from U2.
- A downstream port shall perform a far-end receiver termination detection every 100 ms (tU2RxdetDelay).

#### 7.5.8.2 Exit from U2

- A downstream port shall transition to eSS.Disabled when directed.
- A downstream port shall transition to Rx.Detect upon detection of a far-end high-impedance receiver termination (ZRX-HIGH-IMP-DC-POS) defined in Table 6-21.
- A downstream port shall transition to Rx.Detect when directed to issue Warm Reset.
- An upstream port shall transition to Rx.Detect when Warm Reset is detected.
- A self-powered upstream port shall transition to eSS.Disabled upon not detecting valid Vbus as defined in Section 11.4.5.
- The port shall transition to Recovery upon successful completion of a LFPS handshake meeting the U2 LFPS exit signaling defined in Section 6.9.2.

7-71

Universal Serial Bus 3.1 Specification

- The port shall transition to eSS.Inactive upon the 2-ms LFPS handshake timer timeout (tNoLFPSResponseTimeout) and a successful LFPS handshake meeting the U2 LFPS exit handshake signaling in Section 6.9.2 is not achieved.

![img-183.jpeg](img-183.jpeg)

Note: Transition conditions are illustrative only, Not all of the transition conditions are listed.

Figure 7-20. U2

### 7.5.9 U3

U3 is a link state where a device is put into a suspend state. Significant link and device powers are saved.

U3 does not contain any substates. Transitions to other states are shown in Figure 7-21.

### 7.5.9.1 U3 Requirements

- The Enhanced SuperSpeed transmitter DC common mode voltage does not need to be within specification (VTX-CM-DC-ACTIVE-IDLE-DELTA) defined in Table 6-18.
- The port shall maintain its low-impedance receiver termination (RRX-DC) defined in Table 6-21.
- LFPS Ping detection shall be disabled.
- The port shall enable its U3 wakeup detect functionality as defined in Section 6.9.2.
- The port shall enable its LFPS transmitter when it initiates the exit from U3.
- A downstream port shall perform a far-end receiver termination detection every 100 ms (tU3RxdetDelay).
- The port not able to respond to U3 LFPS wakeup within tNoLFPSResponseTimeout may initiate U3 LFPS wakeup when it is ready to return to U0.

### 7.5.9.2 Exit from U3

- A downstream port shall transition to eSS.Disabled when directed.
- A downstream port shall transition to Rx.Detect upon detection of a far-end high-impedance receiver termination ($Z_{RX-HIGH-IMP-DC-POS}$) defined in Table 6-21.
- A downstream port shall transition to Rx.Detect when directed to issue Warm Reset.
- An upstream port shall transition to Rx.Detect when Warm Reset is detected.

7-72

Link Layer

- A self-powered upstream port shall transition to eSS.Disabled upon not detecting valid Vbus as defined in Section 11.4.5.
- The port shall transition to Recovery upon successful completion of a LFPS handshake meeting the U3 wakeup signaling defined in Section 6.9.2.
- The port shall remain in U3 when the 10-ms LFPS handshake timer times out (tNoLFPSResponseTimeout) and a successful LFPS handshake meeting the U3 wakeup handshake signaling in Section 6.9.2 is not achieved. 100 ms (tU3WakeupRetryDelay) after an unsuccessful LFPS handshake and the requirement to exit U3 still exists, then the port shall initiate the U3 wakeup LFPS Handshake signaling to wake up the host.

![img-184.jpeg](img-184.jpeg)

Note: Transition conditions are illustrative only, Not all of the transition conditions are listed.

Figure 7-21. U3

### 7.5.10 Recovery

The Recovery link state is entered to retrain the link, or to perform Hot Reset, or to switch to Loopback mode. In order to retrain the link and also minimize the recovery latency, the two link partners do not train the receiver equalizers. Instead, the last trained equalizer configurations are maintained. Only TS1 and TS2 ordered sets are transmitted to synchronize the link and to exchange the link configuration information defined in Table 6-5.

#### 7.5.10.1 Recovery Substate Machines

Recovery contains a substate machine shown in Figure 7-22 with the following substates:

- Recovery.Active
- Recovery.Configuration
- Recovery.Idle

#### 7.5.10.2 Recovery Requirements

- The port shall meet the transmitter specifications as defined in Table 6-17.
- The port shall maintain the low-impedance receiver termination (RRX-DC) as defined in Table 6-21.

7-73

Universal Serial Bus 3.1 Specification

- For SuperSpeed USB, all header packets in the Tx Header Buffers and the Rx Header Buffers shall be handled based on the requirements specified in Section 7.2.4.
- For SuperSpeedPlus USB, all header packets and data packet headers in the Type 1/Type 2 Tx Header Buffers and the Type 1/Type 2 Rx Buffers shall be handled based on the requirements specified in Section 7.2.4.

### 7.5.10.3 Recovery.Active

Recovery.Active is a substate to train the Enhanced SuperSpeed link by transmitting the TS1 ordered sets.

#### 7.5.10.3.1 Recovery.Active Requirements

- A 12-ms timer (tRecoveryActiveTimeout) shall be started upon entry to this substate.
- The port shall transmit the TS1 ordered sets upon entry to this substate.
- The port shall train its receiver with TS1 or TS2 ordered sets.

Note: Depending on the link condition and different receiver implementations, one port's receiver may train faster than the other. When this occurs, the port whose receiver trains first will enter Recovery.Configuration and start transmitting TS2 ordered sets while the port whose receiver is not yet trained is still in Recovery.Active using the TS2 ordered sets to train its receiver.

- The port in SuperSpeedPlus operation shall insert a SYNC ordered set every 32 TS1 ordered sets.
- The port in SuperSpeedPlus operation shall perform block alignment and scrambler synchronization as defined in Sections 6.3.2.3 and 6.4.1.2.4 of Chapter 6.

#### 7.5.10.3.2 Exit from Recovery.Active

- The port in SuperSpeed operation shall transition to Recovery.Configuration after eight consecutive and identical TS1 or TS2 ordered sets are received.
- The port in SuperSpeedPlus operation shall transition to Recovery.Configuration upon receiving eight consecutive and identical TS1 or TS2 ordered sets, excluding symbols 14 and 15 of TS1 or TS2 ordered sets.

Note: SYNC OS and SKP OS in between TS1 OS and/or TS2 OS do not disqualify the consecutive detection of TS1 OS and TS2 OS. Symbols 14 and 15 are used for TS1 or TS2 ordered set identifier or DC balance adjustment.

- The port shall transition to eSS.Inactive when the following conditions are met:

1. Either the Ux_EXIT_TIMER or the 12-ms timer (tRecoveryActiveTimeout) times out.
2. For a downstream port, the transition to Recovery is not to attempt a Hot Reset.

- A downstream port shall transition to Rx.Detect when the following conditions are met:

1. Either the Ux_EXIT_TIMER or the 12-ms timer (tRecoveryActiveTimeout) times out.
2. The transition to Recovery is to attempt a Hot Reset.

- A downstream port shall transition to eSS.Disabled when directed.
- A downstream port shall transition to Rx.Detect when directed to issue Warm Reset.
- An upstream port shall transition to Rx.Detect when Warm Reset is detected.

### 7.5.10.4 Recovery.Configuration

Recovery.Configuration is a substate designed to allow the two link partners to achieve the Enhanced SuperSpeed handshake by exchanging the TS2 ordered sets.

7-74

Link Layer

### 7.5.10.4.1 Recovery.Configuration Requirements

- The port shall transmit identical TS2 ordered sets upon entry to this substate and set the link configuration field in the TS2 ordered set based on the following:

1. When directed, a downstream port shall set Reset bit in the TS2 ordered set.

Note: An upstream port can only set the Reset bit in the TS2 ordered set when in Hot Reset. Active. Refer to Section 7.5.12.3 for details.

2. When directed, the port shall set Loopback bit in the TS2 ordered set.
3. When directed, the port shall set the Disabling Scrambling bit in the TS2 ordered set.

- A 6-ms timer (tRecoveryConfigurationTimeout) shall be started upon entry to this substate.
- The port in SuperSpeedPlus operation shall insert a SYNC ordered set every 32 TS2 ordered sets.
- The port in SuperSpeedPlus operation shall perform block alignment and scrambler synchronization as defined in Sections 6.3.2.3 and 6.4.1.2.1 of Chapter 6.

### 7.5.10.4.2 Exit from Recovery.Configuration

- The port in SuperSpeed operation shall transition to Recovery.Idle after the following two conditions are met:

1. Eight consecutive and identical TS2 ordered sets are received.
2. Sixteen TS2 ordered sets are sent after receiving the first of the eight consecutive and identical TS2 ordered sets.

- The port in SuperSpeedPlus operation shall transition to Recovery.Idle when the following two conditions are met:

1. Eight consecutive and identical TS2 ordered sets, excluding symbols 14 and 15, are received.
2. Sixteen TS2 ordered sets are sent after receiving the first of the eight consecutive and identical TS2 ordered sets, excluding symbols 14 and 15.

- The port shall transition to eSS.Inactive when the following conditions are met:

1. Either the Ux_EXIT_TIMER or the 6-ms timer (tRecoveryConfigurationTimeout) times out.
2. For a downstream port, the transition to Recovery is not to attempt a Hot Reset.

- A downstream port shall transition to Rx.Detect when the following conditions are met:

1. Either the Ux_EXIT_TIMER or the 6-ms timer (tRecoveryConfigurationTimeout) times out.
2. The transition to Recovery is to attempt a Hot Reset.

- A downstream port shall transition to eSS.Disabled when directed.
- A downstream port shall transition to Rx.Detect when directed to issue Warm Reset.
- An upstream port shall transition to Rx.Detect when Warm Reset is detected.

### 7.5.10.5 Recovery.Idle

Recovery.Idle is a substate where a port decodes the link configuration field defined in the TS2 ordered set received during Recovery.Configuration and determines the next state.

### 7.5.10.5.1 Recovery.Idle Requirements

- A 2-ms timer (tRecoveryIdleTimeout) shall be started upon entry to this substate.
- The port in SuperSpeed operation shall transmit Idle Symbols if the next state is U0. The port may transmit Idle Symbols if the next state is Loopback or HotReset.

7-75

Universal Serial Bus 3.1 Specification

- The port shall decode the link configuration field defined in the TS2 ordered sets received during Recovery.Configuration and proceed to the next state.
- The port in SuperSpeed operation shall enable the scrambling by default if the Disabling Scrambling bit is not asserted in the TS2 ordered set received in Recovery.configuration.
- The port in SuperSpeed operation shall disable the scrambling if directed, or if the Disabling Scrambling bit is asserted in the TS2 ordered set received in Recovery.configuration.
- The port in SuperSpeedPlus operation shall transmit a single SDS ordered set before the start of the data blocks with Idle Symbols if the next state is U0. The port may transmit SDS ordered set if the next state is Loopback or Hot Reset.

Note: Under situation where a SKP ordered set is also scheduled at the same time with SDS ordered set, SKP ordered set shall be transmitted first.

- The port in SuperSpeedPlus operation shall disable the scrambling upon completion of SDS ordered set transmission if directed, or if the Disabling Scrambling bit is asserted in the TS2 ordered set received in Recovery.Configuration.
- The port in SuperSpeedPlus operation may ignore SDS ordered set if corrupted and continue to process the following data block. The port may optionally choose to recover SDS ordered set if error is detected.
- The port shall be able to receive the Header Sequence Number Advertisement from its link partner.

Note: The exit time difference between the two ports will result in one port entering U0 first and starting the Header Sequence Number Advertisement while the other port is still in Recovery.Idle.

### 7.5.10.5.2 Exit from Recovery.Idle

- The port shall transition to Loopback when directed as a loopback master and the port is capable of being a loopback master.
- The port shall transition to Loopback as a loopback slave if the Loopback bit is asserted in TS2 ordered sets.
- The port shall transition to U0 when the following two conditions are met:

1. Eight consecutive Idle Symbols are received.
2. Sixteen Idle Symbols are sent after receiving one Idle Symbol.

- The port shall transition to eSS.Inactive when one of the following timers times out and the conditions to transition to U0 are not met:

1. Ux_EXIT_TIMER
2. The 2-ms timer (tRecoveryIdleTimeout)

- A downstream port shall transition to Hot Reset when directed.
- A downstream port shall transition to eSS.Disabled when directed.
- A downstream port shall transition to Rx.Detect when directed to issue Warm Reset.
- An upstream port shall transition to Rx.Detect when Warm Reset is detected.
- An upstream port shall transition to Hot Reset if the Reset bit is asserted in TS2 ordered sets.

7-76

Link Layer

![img-185.jpeg](img-185.jpeg)

Note: Transition conditions are illustrative only. Not all transition conditions are listed.

Figure 7-22. Recovery Substate Machine

### 7.5.11 Loopback

Loopback is intended for test and fault isolation. Loopback includes a bit error rate test (BERT) state machine, described in Chapter 6.

A loopback master is the port requesting loopback. A loopback slave is the port that retransmits the symbols received from the loopback master.

During Loopback.Active, the loopback slave must support the BERT protocol described in Chapter 6. The loopback slave must respond to the command for BERT error counter reset and BERT report error count. The loopback slave must check the incoming data for the loopback data pattern.

#### 7.5.11.1 Loopback Substate Machines

Loopback contains a substate machine shown in Figure 7-23 with the following substates:

- Loopback.Active
- Loopback.Exit

7-77

Universal Serial Bus 3.1 Specification

### 7.5.11.2 Loopback Requirements

- There shall be one loopback master and one loopback slave. The loopback master is the port that has the Loopback bit asserted in TS2 ordered sets.
- The port shall maintain its transmitter specifications defined in Table 6-17.
- The port shall maintain its low-impedance receiver termination (R_RX-DC) defined in Table 6-21.

### 7.5.11.3 Loopback.Active

Loopback.Active is a substate where the loopback test is active. The loopback master is sending data/commands to its loopback slave. The loopback slave is either looping back the data or detecting/executing the commands it received from the loopback master.

#### 7.5.11.3.1 Loopback.Active Requirements

- The loopback master shall send valid symbols with SKPs as necessary.
- The loopback slave shall retransmit the received symbols.
- The loopback slave shall not modify the received symbols, other than lane polarity inversion if necessary, and SKP ordered set, which may be added or dropped as required.

Note: For SuperSpeed operation this implies that the loopback slave should disable or bypass its own 8b/10b encoder/decoder and scrambler/descrambler. For SuperSpeedPlus operation this implies that the loopback slave should disable or bypass its own scrambler/descrambler.

- The loopback slave must process the BERT commands as defined in Section 6.8.4.
- The LFPS receiver shall be enabled.

#### 7.5.11.3.2 Exit from Loopback.Active

- A downstream port shall transition to eSS.Disabled when directed.
- A downstream port shall transition to Rx.Detect when directed to issue Warm Reset.
- An upstream port shall transition to Rx.Detect when Warm Reset is detected.
- When directed, the loopback master shall transition to Loopback.Exit.
- The loopback slave shall transition to Loopback.Exit upon detection of Loopback LFPS exit handshake signal meeting Loopback LFPS exit signaling defined in Section 6.9.2.

### 7.5.11.4 Loopback.Exit

Loopback.Exit is a substate where a loopback master has completed the loopback test and starts the exit from Loopback.

#### 7.5.11.4.1 Loopback.Exit Requirements

- A 2-ms timer (tLoopbackExitTimeout) shall be started upon entry to the substate.
- The LFPS transmitter and the LFPS receiver shall be enabled.
- The port shall transmit and receive Loopback LFPS exit handshake signal defined in Section 6.9.2.

#### 7.5.11.4.2 Exit from Loopback.Exit

- The port shall transition to Rx.Detect upon a successful Loopback LFPS exit handshake defined in Section 6.9.2.
- The port shall transition to eSS.Inactive upon the 2-ms timer timeout (tLoopbackExitTimeout) and the condition to transition to Rx.Detect is not met.
- A downstream port shall transition to eSS.Disabled when directed.
- A downstream port shall transition to Rx.Detect when directed to issue Warm Reset.

7-78

Link Layer

- An upstream port shall transition to Rx.Detect when Warm Reset is detected.

![img-186.jpeg](img-186.jpeg)

Note: Transition conditions are illustrative only. Not all of the transition conditions are listed.

U-055

Figure 7-23. Loopback Substate Machine

### 7.5.12 Hot Reset

Only a downstream port can be directed to initiate a Hot Reset.

When the downstream port initiates reset, it shall transmit TS2 ordered sets with the Reset bit asserted. The upstream port shall respond by sending the TS2 ordered sets with Reset bit asserted. Upon completion of Hot Reset processing, the upstream port shall signal the downstream port by sending the TS2 ordered sets with the Reset bit de-asserted. The downstream port shall respond with the Reset bit de-asserted in the TS2 ordered sets. Once both ports receive the TS2 ordered sets with the Reset bit de-asserted, they shall exit from Hot Reset.Active and transition to Hot Reset.Exit. Once a successful idle symbol handshake is achieved, the port shall return to U0.

#### 7.5.12.1 Hot Reset Substate Machines

Hot Reset contains a substate machine shown in Figure 7-24 with the following substates:

- Hot Reset Active
- Hot Reset.Exit

#### 7.5.12.2 Hot Reset Requirements

- A downstream port shall reset its Link Error Count as defined in Section 7.4.2.
- A downstream port shall reset its PM timers and the associated U1 and U2 timeout values to zero.
- The port in SuperSpeedPlus operation shall reset the Soft Error Count if implemented.
- The port Configuration information shall remain unchanged (refer to Section 8.4.6 for details).

7-79

Universal Serial Bus 3.1 Specification

- The port shall maintain its transmitter specifications defined in Table 6-17.
- The port shall maintain its low-impedance receiver termination (R$_{RX-DC}$) defined in Table 6-21.

### 7.5.12.3 Hot Reset.Active

Hot Reset.Active is a substate where a port will perform the reset as defined in Section 7.4.2.

#### 7.5.12.3.1 Hot Reset.Active Requirements

- Upon entry to this substate, the port shall first transmit at least 16 TS2 ordered sets continuously with the Reset bit asserted.

Note: Depending on the time delay between the two ports entering Hot Reset, when the downstream port is transmitting the first 16 TS2 ordered sets with the Reset bit asserted, it may still receive part of the TS2 ordered sets from the upstream port exiting from Polling.Configuration or Recovery.Configuration. The downstream port shall ignore those TS2 ordered sets. Also upon entry to this substate, both ports shall ignore the Disabling Scrambling bit in the link configuration field of the TS2 Ordered Set. This bit is only decoded in Polling.Idle or Recovery.Idle.

- A 12-ms timer (tHotResetActiveTimeout) shall be started upon entry to this substate.
- A downstream port shall continue to transmit TS2 ordered sets with the Reset bit asserted until the upstream port transitions from sending TS2 ordered sets with the Reset bit asserted to sending the TS2 ordered sets with the Reset bit de-asserted.
- An upstream port shall transmit TS2 ordered sets with the Reset bit asserted while performing the Hot Reset.
- An upstream port shall transmit TS2 ordered sets with the Reset bit de-asserted after completing the Hot Reset.
- The port shall perform Hot Reset described in Hot Reset requirement of this section.

#### 7.5.12.3.2 Exit from Hot Reset.Active

- The port shall transition to Hot Reset.Exit when the following three conditions are met.

1. At least 16 TS2 ordered sets with the Reset bit asserted are transmitted.
2. Two consecutive TS2 ordered sets are received with the Reset bit de-asserted.
3. Four consecutive TS2 ordered sets with the Reset bit de-asserted are sent after receiving one TS2 ordered set with the Reset bit de-asserted.

- The port shall transition to eSS.Inactive upon the 12-ms timer timeout (tHotResetActiveTimeout) and the conditions to transition to Hot Reset.Exit are not met.
- The port in SuperSpeedPlus operation may ignore SDS OS if corrupted.
- A downstream port shall transition to eSS.Disabled when directed.
- A downstream port shall transition to Rx.Detect when directed to issue Warm Reset.
- An upstream port shall transition to Rx.Detect when Warm Reset is detected.

### 7.5.12.4 Hot Reset.Exit

Hot Reset.Exit is a substate where the port has completed Hot Reset and is ready to exit from Hot Reset.

#### 7.5.12.4.1 Hot Reset.Exit Requirements

- The port in SuperSpeed operation shall transmit idle symbols.

7-80

Link Layer

- The port in SuperSpeedPlus operation shall transmit a single SDS ordered set before the start of the data block with Idle Symbols.
- The port in SuperSpeedPlus operation may ignore SDS ordered set if corrupted and continue to process the following data block. The port may optionally choose to recover SDS ordered set if error is detected.
- A 2-ms timer (tHotResetExitTimeout) shall be started upon entry to this substate.
- The port shall be able to receive the Header Sequence Number Advertisement from its link partner.

Note: The exit time difference between the two ports will result in one port entering U0 first and starting the Header Sequence Number Advertisement while the other port is still in Hot Reset.Exit.

### 7.5.12.4.2 Exit from Hot Reset.Exit

- The port shall transition to U0 when the following two conditions are met:

1. Eight consecutive Idle Symbols are received.
2. Sixteen Idle Symbols are sent after receiving one Idle Symbol.

- The port shall transition to eSS.Inactive upon the 2-ms timer timeout (tHotResetExitTimeout) and the conditions to transition to U0 are not met.
- A downstream port shall transition to eSS.Disabled when directed.
- A downstream port shall transition to Rx.Detect when directed to issue Warm Reset.
- An upstream port shall transition to Rx.Detect when Warm Reset is detected.

![img-187.jpeg](img-187.jpeg)

Note: Transition conditions are illustrative only. Not all of the transition conditions are listed.

U-056

Figure 7-24. Hot Reset Substate Machine

7-81

Universal Serial Bus 3.1 Specification

7-82

8

# Protocol Layer

The protocol layer manages the end-to-end flow of data between a device and its host. This layer is built on the assumption that the link layer guarantees delivery of header packets and this layer adds on end to end reliability for the rest of the packets depending on the transfer type.

Where not specifically noted, requirements apply to both the SuperSpeed and SuperSpeedPlus architectures. Gen 2 speed capable devices operating at Gen 1 speed, regardless of their additional capabilities (e.g. Gen 2 speed), shall only use features of the SuperSpeed architecture.

The chapter describes the following in detail:

- Types of packets
- Format of the packets
Expected responses to packets sent by the host and a device
- The four USB defined transfer types
- Support for Streams for the bulk transfer type
- Timing parameters for the various responses and packets the host or a device may receive or transmit

![img-188.jpeg](img-188.jpeg)

Figure 8-1. Protocol Layer Highlighted

8-1

Universal Serial Bus 3.1 Specification, Revision 1.0

## 8.1 Enhanced SuperSpeed Transactions

The Enhanced SuperSpeed Bus defines multiple speeds at which the bus can operate. The rules for transactions on a SuperSpeed bus instance are defined in Section 8.1.1. The rules for transactions on a SuperSpeedPlus bus instance are defined in Section 8.1.2.

### 8.1.1 Transactions on a SuperSpeed Bus Instance

Transactions are initiated by the host when it either requests or sends data to an endpoint on a device and are completed when the endpoint sends the data or acknowledges receipt of the data. A transfer on the SuperSpeed bus instance is a request for data made by a device application to the host which then breaks it up into one or more burst transactions. A host may initiate one or more OUT bus transactions to one or more endpoints while it waits for the completion of the current bus transaction. However, a host shall not initiate another IN bus transaction to any endpoint on the same SuperSpeed bus instance until the host:

- For non-isochronous endpoint
  1. receives all requested Data Packets (DPs) or
  2. receives a short packet or
  3. receives a DP with EOB flag set or
  4. receives an NRDY or a STALL Transaction Packet (TP) or
  5. times out the transaction for the current ACK TP
- For isochronous endpoint
  1. receives all the DPs that were requested or
  2. receives a short packet or
  3. receives a DP with last packet flag field set or
  4. times out the transaction for the current ACK TP.

For non-isochronous transactions, an endpoint may respond to valid transactions by:

- Returning an NRDY Transaction Packet
- Accepting it by returning an ACK Transaction Packet in the case of an OUT transaction
- Returning one or more data packets in the case of an IN transaction
- Returning a STALL Transaction Packet if there is an internal endpoint error

An NRDY Transaction Packet (TP) response indicates that an endpoint is not ready to sink or source data. This allows the links between the device and the host to be placed in a reduced power state until an endpoint is ready to receive or send data. However, as mentioned in Section 8.10.1, the host may continue to perform transactions with the endpoint on the device even before the endpoint notifies the host that it is ready. When ready, the endpoint asynchronously sends an ERDY TP to the host to tell it that it is now ready to move data and the host responds by rescheduling the request. Note that isochronous transactions do not use ERDY or NRDY TPs as they are serviced by the host at periodic intervals. Additionally, data packets sent to or received from an isochronous endpoint are not acknowledged, i.e., no ACK TPs are sent to acknowledge the receipt of data packets.

Endpoints only respond to requests made by the host. The host is responsible for scheduling transactions on the bus and maintaining the priority and fairness of the data movement on the bus; it does this by the timing and ordering of IN and OUT requests. Transactions are not broadcast;

8-2

Protocol Layer

packets traverse a direct path between the host and device. Any unused links may be placed into reduced power states making the bus amenable to aggressive power management.

### 8.1.2 Transactions on a SuperSpeedPlus Bus Instance

Transactions on a SuperSpeedPlus bus instance follow the rules defined in Section 8.1.1 with the following modifications:

- A SuperSpeedPlus host may issue simultaneous IN requests
- A SuperSpeedPlus host should pipeline Isochronous IN transactions as described in Section 8.12.6.3.1
- A SuperSpeedPlus device shall support simultaneous IN requests to different endpoints
- Transactions may arrive/complete in a different order than they were initiated

#### 8.1.2.1 Simultaneous IN Transactions

A SuperSpeedPlus host may initiate simultaneous IN transactions. However, a SuperSpeedPlus host shall not initiate simultaneous IN transactions to:

- The same endpoint
- A SuperSpeed bus instance

Note: an ACK TP to continue a burst does not constitute a new IN transaction.

#### 8.1.2.2 Transaction Reordering

Packets (DPs and TPs) may be delivered to the intended recipient in a different order than they were originated. This may happen due to the following:

- A SuperSpeedPlus hub may reorder due to the SuperSpeedPlus packet ordering rules. Refer to Section 10.8.6.
- A SuperSpeedPlus device may reorder asynchronous and periodic IN requests.
- SuperSpeedPlus devices and hubs will transmit TPs before DPs (for both periodic and asynchronous packets)

8-3

Universal Serial Bus 3.1 Specification, Revision 1.0

## 8.2 Packet Types

Enhanced SuperSpeed USB uses four basic packet types each with one or more subtypes. The four packet types are:

- Link Management Packets (LMP) only travel between a pair of links (e.g., a pair of directly connected ports) and is primarily used to manage that link.
- Transaction Packets (TP) traverse all the links directly connecting the host to a device. They are used to control the flow of data packets, configure devices, and hubs, etc. Transaction Packets have no data payload.
- Data Packets (DP) traverse all the links directly connecting the host to a device. Data Packets have two parts: a Data Packet Header (DPH) and a Data Packet Payload (DPP).
- Isochronous Timestamp Packets (ITP) are multicast on all the active links.

All packets consist of a 14-byte header, followed by a 2-byte Link Control Word at the end of the packet (16 bytes total). All headers have a Type field that is used by the receiving entity (e.g., host, hub, or device) to determine how to process the packet. All headers include a 2-byte CRC (CRC-16).

All devices (including hubs) and the host consume the LMPs they receive.

If the value of the Type field is Transaction Packet or Data Packet Header, the Route String and Device Address fields follow the Type field. The Route String field is used by hubs to route packets which appear on their upstream port to the appropriate downstream port. Packets flowing from a device to the host are always routed from a downstream port on a hub to its upstream port. The Device Address field is provided to the host so that it can identify the source of a packet. All other fields are discussed further in this chapter.

![img-189.jpeg](img-189.jpeg)

Figure 8-2. Example Transaction Packet

Data Packets include additional information in the header that describes the data block. The Data Block is always followed by a 4-byte CRC-32 used to determine the correctness of the data. The Data Block and the CRC-32 together are referred to as the Data Packet Payload.

8-4

Protocol Layer

### 8.3 Packet Formats

Packet byte and bit definitions in this section are described in an un-encoded data format. The effects of symbols added to the serial stream (i.e., to frame packets or control or modify the link), bit encoding, bit scrambling, and link level framing have been removed for the sake of clarity. Refer to Chapters 6 and 7 for detailed information.

#### 8.3.1 Fields Common to all Headers

All Enhanced SuperSpeed headers start with the Type field that is used to determine how to interpret the packet. At a high level this tells the recipient of the packet what to do with it: either to use it to manage the link or to move and control the flow of data between a device and the host.

##### 8.3.1.1 Reserved Values and Reserved Field Handling

Reserved fields and Reserved values shall not be used in a vendor-specific manner.

A transmitter shall set all Reserved fields to zero and a receiver shall ignore any Reserved field.

A transmitter shall not set a defined field to a reserved value and a receiver shall ignore any packet that has any of its defined fields set to a reserved value. Note that the receiver shall acknowledge the packet and return credit for the same as per the requirement specified in Section 7.2.4.1.

Note: SuperSpeedPlus hosts, hubs and devices use some fields previously marked as Reserved.

##### 8.3.1.2 Type Field

The Type field is a 5-bit field that identifies the format of the packet. The type is used to determine how the packet is to be used or forwarded by intervening links.

Table 8-1. Type Field Description

[tbl-103.md](tbl-103.md)

##### 8.3.1.3 CRC-16

All header packets have a 16-bit CRC field. This field is the CRC calculated over the preceding 12 bytes in the header packet. Refer to Section 7.2.1.1.2 for the polynomial used to calculate this value.

8-5

Universal Serial Bus 3.1 Specification, Revision 1.0

### 8.3.1.4 Link Control Word

The usage of the Link Control Word is defined in Section 7.2.1.1.3.

[tbl-104.md](tbl-104.md)

U-092

Figure 8-3. Link Control Word Detail

Table 8-2. Link Control Word Format

[tbl-105.md](tbl-105.md)

8-6

Protocol Layer

### 8.4 Link Management Packet (LMP)

Packets that have the Type field set to Link Management Packet are referred to as LMPs. These packets are used to manage a single link. They carry no addressing information and as such are not routable. They may be generated as the result of hub port commands. For example, a hub port command is used to set the U2 inactivity timeout. In addition, they are used to exchange port capability information and may be used for testing purposes.

![img-190.jpeg](img-190.jpeg)

Figure 8-4. Link Management Packet Structure

#### 8.4.1 Subtype Field

The value in the LMP Subtype field further identifies the content of the LMP.

Table 8-3. Link Management Packet Subtype Field

[tbl-106.md](tbl-106.md)

8-7

Universal Serial Bus 3.1 Specification, Revision 1.0

### 8.4.2 Set Link Function

The Set Link Function LMP shall be used to configure functionality that can be changed without leaving the active (U0) state.

Upon receipt of an LMP with the Force_LinkPM_Accept bit asserted, the port shall accept all LGO_U1 and LGO_U2 Link Commands until the port receives an LMP with the Force_LinkPM_Accept bit de-asserted. After port receives an LMP with the Force_LinkPM_Accept bit de-asserted, port will function in normal mode doing power management based on packet pending state of device's endpoints.

The device must stay in U1 or U2 until the downstream port initiates exit to U0. Software must ensure that there are no pending packets at the link level before issuing a SetPortFeature command that generates an LGO_U1 or LGO_U2 link command.

During normal operation, this feature shall only be used if all other means of lowering the link state from U0 to U1 or U2 fail.

This LMP is sent by a hub to a device connected on a specific port when it receives a SetPortFeature (FORCE_LINKPM_ACCEPT) command. Refer to Section 10.16.2.2 and Section 10.16.2.10 for more details.

Note: Improper use of the Force_LinkPM_Accept functionality can impact the performance of the link significantly and in some cases (when used during normal operation only) may lead to the device being unable to return to proper operation.

![img-191.jpeg](img-191.jpeg)

Figure 8-5. Set Link Function LMP

8-8

Protocol Layer

Table 8-4. Set Link Function

[tbl-107.md](tbl-107.md)

### 8.4.3 U2 Inactivity Timeout

The U2 Inactivity Timeout LMP shall be used to define the timeout from U1 to U2. Refer to Section 10.6 for details on this LMP.

![img-192.jpeg](img-192.jpeg)

Figure 8-6. U2 Inactivity Timeout LMP

Table 8-5. U2 Inactivity Timer Functionality

[tbl-108.md](tbl-108.md)

8-9

Universal Serial Bus 3.1 Specification, Revision 1.0

### 8.4.4 Vendor Device Test

Use of this LMP is intended for vendor-specific device testing and shall not be used during normal operation of the link.

![img-193.jpeg](img-193.jpeg)

Figure 8-7. Vendor Device Test LMP

Table 8-6. Vendor-specific Device Test Function

[tbl-109.md](tbl-109.md)

### 8.4.5 Port Capabilities

The Port Capability LMP describes each port's link capabilities and is sent by both link partners after the successful completion of training and link initialization. After the port enters U0 from Polling, the port shall send Port Capability LMP within tPortConfiguration time once link initialization (refer to Section 7.2.4.1.1) is completed. Note the port may not always transition directly from Polling to U0, but may transition through other intermediate states (e.g., Recovery or Hot Reset) before entering U0. Regardless of states passed through between Polling and entry into U0, the device shall send a Port Capability LMP immediately upon entering U0.

If a link partner does not receive this LMP within tPortConfiguration time then:

- If the link partner has downstream capability, it shall signal an error as described in Section 10.16.2.6.
- If the link partner only supports upstream capability, see Sections 10.5 and 10.18 which define the hub and peripheral upstream port connect states.

8-10

Protocol Layer

![img-194.jpeg](img-194.jpeg)

Figure 8-8. Port Capability LMP

Table 8-7. Port Capability LMP Format

[tbl-110.md](tbl-110.md)

8-11

Universal Serial Bus 3.1 Specification, Revision 1.0

After exchanging Port Capability LMPs, the link partners shall determine which of the link partners shall be configured as the downstream facing port as specified in Table 8-8.

Table 8-8. Port Type Selection Matrix

[tbl-111.md](tbl-111.md)

Note: $^{1}$If the TieBreaker field contents are equal, then the two link partners shall exchange Port Capability LMPs again with new and different value in the TieBreaker field. The sequence of TieBreaker field values generated by a port shall be sufficiently random.

### 8.4.6 Port Configuration

Only the fields that are different from the Port Capability LMP are described in this section.

All Enhanced SuperSpeed ports that support downstream port capability shall be capable of sending this LMP.

If the port that was to be configured in the upstream facing mode does not receive this LMP within tPortConfiguration time after link initialization, then the upstream port shall transition to eSS.Disabled and a peripheral device shall try and connect at the other speeds this device supports.

![img-195.jpeg](img-195.jpeg)

Figure 8-9. Port Configuration LMP

8-12

Protocol Layer

Table 8-9. Port Configuration LMP Format (Differences with Port Capability LMP)

[tbl-112.md](tbl-112.md)

A port configured in the downstream mode shall send the Port Configuration LMP to the upstream port. The port sending this LMP shall select only one bit for the **Link Speed** field. The **Link Speed** field shall only be used when the port is operating at Gen 1 speed.

If a downstream capable port cannot work with its link partner, then the downstream capable port shall signal an error as described in Section 10.16.2.6.

### 8.4.7 Port Configuration Response

This LMP is sent by the upstream port in response to a Port Configuration. It is used to indicate acceptance or rejection of the Port Configuration LMP. Only the fields that are different from the Port Capability LMP are described in this section.

All Enhanced SuperSpeed ports that support upstream port capability shall be capable of sending this LMP.

If the downstream port does not receive this LMP within tPortConfiguration time, it shall signal an error as described in Section 10.16.2.6.

![img-196.jpeg](img-196.jpeg)

Figure 8-10. Port Configuration Response LMP

8-13

Universal Serial Bus 3.1 Specification, Revision 1.0

Table 8-10. Port Configuration Response LMP Format (Differences with Port Capability LMP)

[tbl-113.md](tbl-113.md)

If the Response Code indicates that the Link Speed was rejected by the upstream port, the downstream port shall signal an error as described in Section 10.16.2.6.

### 8.4.8 Precision Time Measurement

PTM enables USB devices to have more precise notion of time by providing a method of precisely characterizing link delays, and the propagation delays through a hub. The PTM capability is discovered by software through the PTM Capability Descriptor described in Section 9.6.2.6.

Precision Time Measurement consists of two separate mechanisms: Link Delay Measurement (LDM) and Hub Delay Measurement (HDM). These mechanisms complement each other to provide highly accurate bus interval boundary timing for devices; however, HDM may be used to improve device bus interval boundary timing accuracy even if LDM timing information is not available.

SuperSpeedPlus hosts and hubs shall support PTM. PTM support is optional normative for all peripheral devices and SuperSpeed only hosts and hubs. Ideally, PTM is supported by all components of a USB topology; however, PTM capable hubs will still improve the overall accuracy of a device's notion of the bus interval boundary timing.

#### 8.4.8.1 PTM Bus Interval Boundary Counters

A bus interval boundary shall be defined as a pair of counters, referred to as the PTM Bus Interval Boundary Counters, that use a format similar to the 27-bit Isochronous Timestamp of an ITP:

- PTM Delta Counter, 13 bits.
- PTM Bus Interval Counter, 14 bits.

The PTM Clock has a period of tIsochTimestampGranularity units.

The PTM Delta Counter shall be incremented by the PTM Clock to measure the delay from present time to the previous bus interval boundary. The PTM Delta Counter is a modulus 7500 counter, wrapping on microframe boundaries, i.e. incrementing from 0 to 7499 (~125 μs), then wrapping back to 0.

8-14

Protocol Layer

The PTM Bus Interval Counter shall be incremented when the PTM Delta Counter wraps. The PTM Bus Interval Counter is a modulus 16k counter, i.e. incrementing from 0 to 16,383, then wrapping back to 0.

The time synchronization mechanism within the device of the PTM Clock to the bus interval boundary is implementation-specific.

Hosts shall implement a set of PTM Bus Interval Boundary Counters. The host is the source of the bus interval boundary for a PTM Domain.

Hubs are not required to implement PTM Bus Interval Boundary Counters.

PTM capable devices shall implement PTM Bus Interval Boundary Counters.

### 8.4.8.2 LDM Protocol

The LDM protocol is executed with a series of Exchanges between a Requester and a Responder, and ITPs transmitted by Responders to measure the LDM Link Delay illustrates the LDM Timestamp Exchanges.

The following rules apply to LDM Requesters and Responders:

- A LDM Requester is an upstream facing port.
- A LDM Responder is a downstream facing port.
- A LDM Requester and a LDM Responder are paired on a USB link.

![img-197.jpeg](img-197.jpeg)

Figure 8-11. Link Delay Measurement Protocol

The following rules apply to LDM Requests and Responses, and LDM Requesters and Responders:

- When a LDM Requester transmits a LDM Request LMP, it uses the value of its PTM Local Time Source as the t1 timestamp. When the LDM Requester receives a LDM Response LMP it uses the value of its PTM Local Time Source as the t4 timestamp.

8-15

Universal Serial Bus 3.1 Specification, Revision 1.0

- When a LDM Responder receives a LDM Request LMP it uses the value of its PTM Local Time Source as the t2 timestamp, and when it transmits a LDM Response LMP it uses the value of its PTM Local Time Source as the t3 timestamp.
- Each LDM Exchange defines a set of timestamps which the LDM Requester may use to calculate the LDM Link Delay.
- If an LDM Message is received by a port that does not support PTM, then the Message shall be treated as an unsupported LMP by the port and silently dropped. Note that the port shall acknowledge the packet and return credit for the same as per the requirement specified in Section 7.2.4.1.
- LDM timestamps shall reference the first framing symbol of a received or transmitted LDM LMP.

![img-198.jpeg](img-198.jpeg)

Figure 8-12. PTM ITP Protocol

The following rules apply to ITPs and PTM capable hosts, hubs, and devices:

- The tITDFP timestamp represents the time that a PTM downstream facing port transmits an ITP.
- The tITUFP timestamp represents the time that a PTM upstream facing port receives an ITP.

### 8.4.8.2.1 LDM Timestamp Exchange

A Timestamp Exchange consists of a LDM Request LMP being generated by a LDM Requester and the LDM Responder returning a LDM Response LMP.

As illustrated in Figure 8-11, the timestamps t1, t2, t3 and t4 are created by the Requester and the Responder.

At time t4 in a Timestamp Exchange, a LDM Requester has all the information that it needs to compute the LDM Link Delay. In the example of Figure 8-11, at time t4, the Requester has recorded timestamps for t1 and t4, and received Response Delay from the Responder. Refer to Section 8.4.8.3 for how these timestamps are used to compute the LDM Link Delay.

8-16

Protocol Layer

### 8.4.8.2.2 PTM ITP Transfer

Once a LDM Timestamp Exchange is complete, the Link Delay may be computed and PTM may be applied by a Requester to received ITPs. A PTM ITP Transfer consists of an ITP being generated by a LDM Responder and being received by a LDM Requester.

As illustrated in Figure 8-19, the timestamps tITDFP and tITUFP are recorded by the Requester and Responder.

At time tITUFP in a PTM ITP Transfer a LDM Requester has all the information that it needs to compute the bus interval boundary. In the example of Figure 8-12, at time tITUFP the Requester has recorded timestamp for tITUFP and received timestamp tITDFP (encoded in the Isochronous Timestamp and Correction fields of an ITP) from the Responder. Refer to Section 8.4.8.4 for how these timestamps are used to compute the bus interval boundary.

### 8.4.8.3 LDM State Machines

The LDM state machines utilize the following notation:

![img-199.jpeg](img-199.jpeg)

Figure 8-13. LDM State Machine Notation

Where the State Name is an informative name defined for the state, the Status Flags values are:

LDM Enabled and LDM Valid, respectively, e.g. the Status Flags value 0,0 is interpreted as LDM Enabled = false (0) and LDM Valid = false (0).

Note: Transitions associated with a large bubble may occur from any state defined within the bubble as long as the Conditions match.

Note: The figures in this section are provided to illustrate state transition conditions and actions; however, refer to the textual descriptions of the respective states in the sections below for their explicit definition.

8-17

Universal Serial Bus 3.1 Specification, Revision 1.0

### 8.4.8.3.1 Requester Operation

This section describes the Timestamp Exchange operations that a Requester (Upstream Facing Port) performs to participate in the LDM protocol.

![img-200.jpeg](img-200.jpeg)

Figure 8-14. LDM Requester State Machine

The LDM Requester State Machine shall maintain the following local variable: Init Response Timeout Counter.

The LDM Requester State Machine shall maintain the following local timer: Response Timer. All local timers are set to 0 when they are “started”.

#### 8.4.8.3.1.1 Init Request

This is the initial state of the Requester after power-up, Hot Reset, or Warm Reset.

Upon entering this state, the Requester shall set the LDM Enabled flag to 1.

The Init Response Timeout Counter shall be initialized to 0 at power up, or if the Init Request state is entered from the LDM Disabled or Timestamp Response states. If the Init Request state is entered from the Init Response state, then the Init Response Timeout Counter shall not be changed.

8-18

Protocol Layer

In this state the LDM Protocol is enabled (LDM Enabled = 1); the local copy of the bus interval boundary is Invalid (LDM Valid = 0) and the Requester waits for a Trigger Event.

Trigger Event – When a Trigger Event occurs, the Requester shall transmit a LDM TS Request LMP to the Responder, save timestamp t1 from the Local Time Source in the LDM Context to record the time that the LDM Request was transmitted, and transition to the Init Response state.

A typical Trigger Event for the Requester Init Request state would be the transition of the device to the Address state.

### 8.4.8.3.1.2 Init Response

Upon entering this state, the Requester shall increment the Init Response Timeout Counter, start the Response Timer and wait for a TS Response LMP or a timeout.

LDM TS Response LMP & DL=0 – If a LDM TS Response LMP and LCW Delayed (DL) = 0 is received, the Requester shall save timestamp t4 from the Local Time Source in the LDM Context to record the time that the LDM Response was received, then calculate the LDM Link Delay (refer to Section 8.4.8.4) and set the LDM Valid flag to 1, and transition to the Timestamp Request state.

LDM TS Response LMP & DL=1 – If a LDM TS Response LMP and LCW Delayed (DL) = 1 is received, the Requester shall consider the Response Delay field of the LDM TS Response LMP invalid, invalidate the LDM Context t1, t2, and t3 timestamps, immediately generate a Trigger Event to initiate another Exchange, and transition to the Timestamp Request state. Refer to Sections 7.2.4.1.2 and 7.2.4.1.12 for the conditions that may set the Delayed bit.

Init Response Timeout(1-2) – If an Init Response Timeout (tLDMRequestTimeout) occurs and the Init Response Timeout Counter is less than 3, then the Requester shall increment the Init Response Timeout Counter and transition to the Init Request state.

Init Response Timeout(3) – If an Init Response Timeout occurs and the Init Response Timeout Counter is equal to 3, then the Requester shall transition to the LDM Disabled state

### 8.4.8.3.1.3 Timestamp Request

Upon entering this state, the Requester shall wait for a Trigger Event.

Trigger Event – When a Trigger Event occurs, the Requester shall transmit a LDM Timestamp (TS) Request LMP to the Responder, save timestamp t1 from the Local Time Source in the LDM Context to record the time that the LDM Request was transmitted, and transition to the Timestamp Response state.

A typical Trigger Event for the Requester Timestamp Request state would be to first transition to the Timestamp Request state, or execute an (averaging) algorithm to improve the accuracy of the Link Delay.

Note: Timestamp t1 shall be adjusted for the TS Delay. Refer to Section 8.4.8.6 for more information.

8-19

Universal Serial Bus 3.1 Specification, Revision 1.0

### 8.4.8.3.1.4 Timestamp Response

Upon entering this state, the Requester shall start the Response Timer and wait for a LDM TS Response LMP or a timeout.

LDM TS Response LMP & DL=0 – If a LDM TS Response LMP is received and the LCW Delayed (DL) flag is zero, the Requester shall save timestamp t4 from the Local Time Source in the LDM Context to record the time that the LDM Response was received, then calculate the LDM Link Delay (refer to Section 8.4.8.4), set the LDM Valid flag to 1, and transition to the Timestamp Request state.

LDM TS Response LMP & DL=1 – If a LDM TS Response LMP is received and the LCW Delayed (DL) flag is one, the Requester shall consider the Response Delay field of the LDM TS Response LMP invalid, invalidate the LDM Context t1, t2, t3 timestamps, immediately generate a Trigger Event to initiate another Timestamp Exchange, and transition to the Timestamp Request state. Refer to Sections 7.2.4.1.2 and 7.2.4.1.12 for the conditions that may set the Delayed bit.

Response Timeout – If a Response Timeout occurs the Requester shall transition to the Init Request state, where the LDM state machine will attempt to retry the Timestamp Exchange with the Responder.

Note: Timestamp t4 shall be adjusted for the TS Delay. Refer to Section 8.4.8.6 for more information.

### 8.4.8.3.1.5 LDM Disabled

Upon entering this state, the Requester shall clear the LDM_ENABLE flag and terminate all LDM protocol activity.

CLEAR_FEATURE(LDM_ENABLE) – When this request is received by the device it shall transition from any other LDM state to the LDM Disabled state.

SET_FEATURE(LDM_ENABLE) – If this request is received by the device it shall transition to the Init Request state.

### 8.4.8.3.2 Responder Operation

This section describes the operations that a Responder (i.e. the Downstream Facing Port of a hub or host controller) performs to participate in the LDM protocol.

8-20

Protocol Layer

![img-201.jpeg](img-201.jpeg)

Figure 8-15. LDM Responder State Machine

The LDM Responder State Machine shall maintain the following local variable: Responder Response Delay Overflow.

### 8.4.8.3.2.1 Responder Disabled

This is the initial state of the Responder after power-up, Hot Reset, or Warm Reset.

Upon entering this state the Responder shall terminate all LDM protocol activity.

LDM Enabled=0 – If LDM Enabled equals 0, then the Responder shall transition from any other LDM state to the Responder Disabled state.

LDM Enabled=1 – If LDM Enabled equal 1, then the Responder shall transition to the Timestamp Request state.

### 8.4.8.3.2.2 Timestamp Request

Upon entering this state, the Responder shall wait for a LDM TS Request LMP.

LDM TS Request LMP – If a LDM TS Request LMP is received, the Responder shall capture timestamp t2 from the PTM Local Time Source to record the time that the LDM TS Request was received and transition to the Timestamp Response state.

Note: Timestamp t2 shall be adjusted for the TS Delay. Refer to Section 8.4.8.6 for more information.

### 8.4.8.3.2.3 Timestamp Response

Upon entering this state the Responder shall wait for a Trigger Event.

Trigger Event – When a Trigger Event occurs, the Responder shall capture timestamp t3 from the PTM Local Time Source to record the time that the LDM Response was transmitted. If the value

8-21

Universal Serial Bus 3.1 Specification, Revision 1.0

t3 - t2 is less than tLDMResponseDelay, the Responder shall form a LDM TS Response LMP by initializing the Response Delay field with the value t3 - t2, transmit the LDM TS Response LMP to the Requester, and transition to the Timestamp Request state. If the value t3 - t2 is equal to or greater than tLDMResponseDelay, then the Responder shall transition to the Timestamp Request state.

A typical Trigger Event for the Responder Timestamp Response state would be the next opportunity to schedule a LDM TS Response LMP on its downstream link after a LDM TS Request LMP has been received.

Note: The Timestamp t3 shall be adjusted for the TS Delay. Refer to Section 8.4.8.6 for more information.

Note: A Responder shall set the LCW Delayed (DL) flag and re-calculate CRC-5 if a LDM TS Response LMP is delayed if its adjusted Response Delay value exceeds tLDMRequestTimeout. Refer to Section 8.4.8.6 for more information.

### 8.4.8.4 LDM Link Delay

LDM defines the set of PTM capabilities which support the measurement of the LDM Link Delay.

LDM Link Delay identifies the delay between the first symbol of a packet being transmitted on a Responder's downstream facing port and the first symbol of the same packet being received on the Requester's upstream facing port. In a hub or device the LDM Link Delay is derived from Timestamp Exchanges with its upstream Responder.

A Requester may execute multiple Timestamp Exchanges to refine its LDM Link Delay value through averaging.

Note: Field, or subfield names that reference a received ITP shall use the subscript (RxITP) and field, or subfield names that reference a transmitted ITP shall use the subscript (TxITP).

### 8.4.8.4.1 Calculation

The LDM Link Delay is calculated by the Requester when a Timestamp Exchange completes. The LDM Link Delay is the measured link delay adjusted to ensure compatibility with non-PTM aware software.

The TP Transmission Time is the time it takes to transmit a TP including framing and encoding at UI nominal.

Where UI nominal is defined as:

$$UI \text{ nominal} = \frac{(UI \text{ max}) + (UI \text{ min})}{2}$$

Refer to Section 6.7 for the definition of UI min and UI max.

The TP Transmission Time for a link operating at Gen 1 speed is 200 UI * UI nominal (i.e. 40 ns @ 5 Gbps).

It takes either 164 or 168 UI, depending on block alignment, to transfer a TP over a link operating at Gen 2 speed. The statistical average is 165 UI. Therefore, the TP Transmission Time for a link operating at Gen 2 speed is 165 UI * UI nominal (i.e. 16.5 ns @ 10 Gbps).

8-22

Protocol Layer

If LDM Valid is zero, then the LDM Link Delay shall be calculated using the following formula:

$$LDM \text{ Link Delay} = TP \text{ Transmission Time} - tTP \text{ Transmission Delay}$$

If LDM Valid is one, then the received LDM TS Response LMP of a Timestamp Exchange provides the Requester with the Response Delay field which defines the delay between when the LDM Request was received and the LDM Response was transmitted by the Responder ((t3 - t2).

When the LDM TS Response LMP of a Timestamp Exchange is received, a Requester has accumulated the timestamps t1 and t4 that can be combined with the Response Delay (t3 - t2 timestamp) received from the Responder to calculate the value of LDM Link Delay using the following formula:

$$LDM \text{ Link Delay} = \frac{(t4 - t1) - (\text{Response Delay})}{2} + TP \text{ Transmission Time} - tTP \text{ Transmission Delay}$$

The values t1, t4, and Response Delay indicate the timestamps captured during the LDM Exchanges as illustrated in Figure 8-11. The default TP transmission time (tTPTransmissionDelay) is corrected by the actual TP Transmission Time of the link. After the LDM Link Delay calculation is complete, the values of timestamps t1 and t4 in the Requester LDM Context will be overwritten with the values of the next Timestamp Exchange.

### 8.4.8.5 PTM Bus Interval Boundary Device Calculation

The bus interval boundary is calculated by a device when an ITP is received.

An ITP provides a device with three values:

- The Bus Interval Counter(RxITP) subfield contains the current Frame Number.
- The Delta(RxITP) subfield contains the delay from the start of the currently received ITP to the previous bus interval boundary.
- The Correction(RxITP) field contains any negative delay that the ITP accumulated as it passed through hubs.

If Delta(RxITP) is greater than or equal to 7500, the device shall ignore the ITP.

If Delta(RxITP) is less than 7500, the device shall apply Delta(RxITP) and Correction(RxITP) values and the LDM Link Delay (determined from preceding TS Exchanges) to set the value of the PTM Delta Counter at the time an ITP is received (tITUFP) using the following formula:

$$PTM \text{ Delta Counter}_{(\text{tITUFP})} =$$

$$\text{MODULUS}(\text{ISOCH\_DELAY} + \text{LDM Link Delay} + \text{Delta}_{(\text{RxITP})} - \text{Correction}_{(\text{RxITP})}, 7500)$$

Where MODULUS(number, divisor) returns the integer remainder after number is divided by divisor and ISOCH_DELAY is the value written to the device by a SET_ISOCH_DELAY request.

At the same time, a device shall use the values of Bus Interval Counter(RxITP) and Delta(RxITP) subfields received in the ITP to set the value of the PTM Bus Interval Counter at the time an ITP is received (tITUFP) using the following formula:

$$PTM \text{ Bus Interval Counter}_{(\text{tITUFP})} =$$

$$\text{Bus Interval Counter}_{(\text{RxITP})} + \text{ROUNDDOWN}((\text{LDM Link Delay} + \text{Delta}_{(\text{RxITP})}) / 7500))$$

8-23

Universal Serial Bus 3.1 Specification, Revision 1.0

Where ROUNDDOWN (n) rounds n down, towards zero, to the nearest integer value.

This combination of setting the PTM Delta Counter and the PTM Bus Interval Counter defines the bus interval boundary time in the device.

The time synchronization mechanism within the device itself (e.g. to the PTM Local Time Source) is implementation-specific.

Figure 8-12 illustrates the tITUFP and tITDFP timing points of an ITP transaction.

### 8.4.8.6 PTM Bus Interval Boundary Host Calculation

A host shall maintain a PTM Delta Counter and a PTM Bus Interval Counter. The host shall transmit downstream ITPs using these current values for the ITP Isochronous Timestamp Bus Interval Counter(TxITP) and Delay(TxITP) fields, and set the Correction(TxITP) field to zero.

### 8.4.8.7 PTM Hub ITP Regeneration

A hub shall maintain an ITP Delay Counter that is incremented by the PTM Clock.

If an ITP is received by a PTM capable hub and the Delayed (DL) bit is not set, then the hub shall apply the following rules:

- Set the ITP Delay Counter to zero.

A PTM capable hub shall apply the following rules independently for each downstream port in U0:

- When an ITP is received, then the hub shall queue an ITP for transmission on this downstream facing port.

- When transmitting an ITP, a hub shall:

1. Copy the value of Bus Interval Boundary(RxITP) to the Bus Interval Boundary(TxITP) subfield of the Isochronous Timestamp field in the downstream ITP.

2. Calculate the value of Delta(TxITP) subfield using the following method:
Determine the Delta value at time the ITP shall be transmitted (tITPDFP) using the formula:

$$Delta_{(tITPDFP)} =$$

$$LDM \text{ Link Delay} + Delta_{(RxITP)} + (ITP \text{ Delay Counter} - wHubDelay) - Correction_{(RxITP)}$$

Where Delta(tITPDFP) is the Delta value at time tITPDFP.

If Delta(tITPDFP) is greater than or equal to zero and less than 7500, the hub shall set Delta(TxITP) equal to Delta(tITPDFP) and the Correction(TxITP) value to zero.

If Delta(tITPDFP) is greater than or equal to 7500, the hub shall set Delta(TxITP) equal to 7500.

If Delta(tITPDFP) is negative the hub shall set Delta(TxITP) to zero and calculate the Correction(TxITP) value using the following formula:

$$Correction_{(TxITP)} = -Delta_{(tITPDFP)}$$

3. Re-calculate the CRC-16 for the modified ITP.

8-24

Protocol Layer

If an ITP is received by a PTM capable hub and the Delayed (DL) bit is set, then the hub shall apply the following rules:

- Forward the received ITP without modification.

The Isochronous Timestamp values used in the ITP being transmitted shall be the values present at the time of transmission; e.g., if other packets are queued for transmission at the time the ITP is queued, the values used shall not be the values present at the time of queuing, but adjusted for the actual time of transmission (tITPDFP). Refer to Section 8.4.8.6 for more information.

8-25

Universal Serial Bus 3.1 Specification, Revision 1.0

### 8.4.8.8 Performance

Figure 8-16 illustrates the various components of a LDM Exchange path that contribute to the overall performance of the LDM mechanism. The Requester to Responder and Responder to Requester paths apply to LDM TS Request and TS Response LMPs, respectively. The Requester Rx path applies to ITPs received by an upstream facing port and the Responder Tx path applies to ITPs transmitted by a downstream facing port.

![img-202.jpeg](img-202.jpeg)

Figure 8-16. PTM Path Performance Contributors

The following requirements should be met to achieve optimal propagation delay measurement:

- The Link Delay between Requester and Responder should be symmetric.
- Timestamp values are assigned to ITPs and TS LMPs to capture when the packet was actually received or transmitted on the Link. LDM timestamp values are also captured in ITPs (Bus Interval Counter/Delta fields) and TS Response LMPs (Response Delay) when they are transmitted.
- An implementation dependent TS Delay occurs between assigning Timestamp values to an ITP, or LDM LMP, and the packet actually being received or transmitted on the Link. Each Timestamp value should be adjusted for the respective TS Delay so that the Timestamp captured for a LDM LMP or ITP approximates the actual time that the last symbol of the respective packet crosses the boundary between a Requester or Responder and the Link.
- A port may contain asymmetric delays in its timestamp mechanism or protocol path (e.g. Rx/Tx Asymmetry). If these asymmetries are not negligible:

8-26

Protocol Layer

1. The Responder shall adjust the TS Response LMP Response Delay (t3-t2 Timestamp) value appropriately for its Rx/Tx Asymmetry, such that its t2 and t3 Timestamps appear to have been captured at equal TS Delays from the Link boundary.
2. The Requester shall account for its Rx/Tx Asymmetry when computing the t4 Timestamp.

- The Link Delay between Requester and Responder should be constant over the time interval between LDM Request and Response LMPs.
- The worst case delay fluctuation (Uncertainty) of timestamps shall be bounded by tPropagationDelayJitterLimit.
- Delay fluctuation (Uncertainty) of timestamps due to link components and due to the protocol stack within clocks should be reduced by two techniques:

1. The Timestamp Measurement Planes used in PTM should be generated as close to the physical Link boundary as practical for a given clock implementation, i.e. minimize TS Delay.

2. Remaining delay fluctuation (Uncertainty) introduced by the protocol stack and by link components can be reduced by averaging Link Delay values over multiple Timestamp Exchanges. The averaging algorithms are outside the scope of this specification.

- The inherent stability and precision of a clock's oscillator must be within the clock accuracy requirements defined for the Unit Interval in Table 6-17.

# IMPLEMENTATION NOTE

# LDM Timestamp Capture Mechanisms

LDM uses services from both the Data Link and Transaction Layers. LDM accuracy requires that time measurements be taken as close to the Physical Layer as possible. Conversely, the messaging protocol itself properly belongs to the Transaction Layer. The LDM message protocol applies to a single Link, where the Upstream Facing Port is the Requestor and the Downstream Facing Port is the Responder.

For most implementations, the logic within the Transaction Layer and Data Link Layers is essentially non-deterministic. Implementation details and current conditions have considerable impact on exactly when a particular packet may encounter any particular processing step. This makes it effectively impossible to capture any timestamp that accurately records the time of a particular physical event within these layers.

Ideally time measurements should be taken with the symbol level accuracy as close to the D+/D- outputs of the Transmitter Differential Driver block (Figure 6-2), or the D+/D- inputs of the Differential Receiver and Equalization block (Figure 6-3). Typically this will require an implementation specific adjustment to compensate for the inability to directly measure the time at the actual pins, because the time will typically be measured (i.e. the Timestamp captured) at some internal point in the Rx or Tx path. The designer should approximate these delays and accommodate them by the timestamp values that they record and the time values that they generate (e.g. the Response Delay value in a LDM TS Response) appropriately. The accuracy and consistency of this measurement are not bounded by this specification, but it is strongly recommended that the highest practical level of accuracy and consistency be achieved.

### 8.4.8.9 LDM Rules

A Responder shall respond to each LDM Request LMP with a LDM Response LMP according to the following rules:

- A Responder shall not send a LDM Response without first receiving a LDM Request LMP.

8-27

Universal Serial Bus 3.1 Specification, Revision 1.0

- A Responder shall capture the PTM Local Clock Source timestamps (t2 and t3) when transmitting LDM Response and when receiving LDM Request LMPs.
- A Responder shall issue LDM Response LMP when it possesses the timing values required to populate the LDM Response LMP: timestamps (t2 -t3 in Figure 8-11).
- A Requester shall capture t1 timestamps upon transmitting the last symbol of a LDM Request.
- A Responder shall capture t2 timestamps upon receiving the last symbol of a LDM Request.
- A Responder shall capture t3 timestamps upon transmitting the last symbol of a LDM Response.
- A Requester shall capture t4 timestamps upon receiving the last symbol of a LDM Response.

Note that these rules assume that the Tx and Rx TS Delays in Figure 8-16 are zero, i.e. the Timestamp Measurement Planes and the TS LMP link boundary transmit and receive times are identical. Refer to Section 8.4.8.8 for how to adjust for actual Timestamp Delays.

### 8.4.8.10 LDM and Hubs

A hub is both a Requester and a Responder, and acts as intermediary between its Upstream and Downstream Facing Ports. As a Requester, a hub utilizes the PTM LDM mechanism to issue LDM Requests on its Upstream Facing Port to identify the LDM Link Delay between itself and its upstream Responder. A hub utilizes the PTM HDM mechanism to update the Isochronous Timestamps of ITPs that it forwards downstream.

A hub implementation has LDM Enabled and LDM Valid flags. Their states are determined by the Hub's Requester State Machine. The values of the LDM Enabled or LDM Valid flags in the hub's Responder State Machines track the Requester State Machine values; e.g., if LDM Enabled or LDM Valid in the Requester State Machine transition to 0, then all of the hub's Responder State Machine shall transition to the Responder Disabled state. When both LDM Enabled and LDM Valid in the Requester State Machine transition to 1, then all of the hub's Responder State Machine shall transition to the Init Request state. A hub does not have LDM Enabled or LDM Valid flags per downstream facing port Responder State Machine.

The USB topology is enumerated from the Root Hub port down; i.e., a hub must be in the Configured state before its downstream ports are active. The PTM timing parameters are selected so that, for typical enumeration sequences, the LDM Link Delay is established in a hub before it transitions to the Configured state. This means that the hub's Responder State Machines should be in the Init Request state as soon as its downstream ports are operational and that no software intervention is required to enable LDM. If the Requester of a device attached to a Downstream Facing Port is unable to establish the LDM Link Delay in timely manner, it may transition to the LDM Disabled state and require software to manually start LDM Exchanges. An alternative is for PTM aware enumeration software to verify that PTM capable hubs have established the LDM Link Delay before configuring them.

8-28

Protocol Layer

##### 8.4.8.11 Link Delay Measurement (LDM) LMP

LDM LMPs shall be used in a LDM Timestamp Exchange to measure the link delay on an upstream facing port.

![img-203.jpeg](img-203.jpeg)

Figure 8-17. LDM LMP

Table 8-11. LDM LMP

[tbl-114.md](tbl-114.md)

### 8.5 Transaction Packet (TP)

Transaction Packets (TPs) traverse the direct path between the host and a device. TPs are used to control data flow and manage the end-to-end connection. The value in the Type field shall be set to Transaction Packet. The Route String field is used by hubs to route a packet that appears on its upstream port to the correct downstream port. The route string is set to zero for a TP sent by a device. When the host sends a TP, the Device Address field contains the address of the intended recipient. When a device sends a TP to the host then it sets the Device Address field to its own address. This field is used by the host to identify the source of the TP. The SubType field in a TP is used by the recipient to determine the format and usage of the TP.

8-29

Universal Serial Bus 3.1 Specification, Revision 1.0

Table 8-12. Transaction Packet Subtype Field

[tbl-115.md](tbl-115.md)

8-30

Protocol Layer

#### 8.5.1 Acknowledgement (ACK) Transaction Packet

This TP is used for two purposes:

- For IN endpoints, this TP is sent by the host to request data from a device as well as to acknowledge the previously received data packet.
- For OUT endpoints, this TP is sent by a device to acknowledge receipt of the previous data packet sent by the host, as well as to inform the host of the number of data packet buffers it has available after receipt of this packet.

![img-204.jpeg](img-204.jpeg)

Figure 8-18. ACK Transaction Packet

8-31

Universal Serial Bus 3.1 Specification, Revision 1.0

Table 8-13. ACK TP Format

[tbl-116.md](tbl-116.md)

8-32

Protocol Layer

[tbl-117.md](tbl-117.md)

8-33

Universal Serial Bus 3.1 Specification, Revision 1.0

### 8.5.2 Not Ready (NRDY) Transaction Packet

This TP can only be sent by a device for a non-isochronous endpoint. An OUT endpoint sends this TP to the host if it has no packet buffer space available to accept the DP sent by the host. An IN endpoint sends this TP to the host if it cannot return a DP in response to an ACK TP sent by the host.

Only the fields that are different from an ACK TP are described in this section.

![img-205.jpeg](img-205.jpeg)

Figure 8-19. NRDY Transaction Packet

Table 8-14. NRDY TP Format (Differences with ACK TP)

[tbl-118.md](tbl-118.md)

### 8.5.3 Endpoint Ready (ERDY) Transaction Packet

This TP can only be sent by a device for a non-isochronous endpoint. It is used to inform the host that an endpoint is ready to send or receive data packets. Only the fields that are different from an ACK TP are described in this section.

![img-206.jpeg](img-206.jpeg)

Figure 8-20. ERDY Transaction Packet

8-34

Protocol Layer

Table 8-15. ERDY TP Format (Differences with ACK TP)

[tbl-119.md](tbl-119.md)

#### 8.5.4 STATUS Transaction Packet

This TP can only be sent by the host. It is used to inform a control endpoint that the host has initiated the Status stage of a control transfer. This TP shall only be sent to a control endpoint. Only the fields that are different from an ACK TP are described in this section.

![img-207.jpeg](img-207.jpeg)

Figure 8-21. STATUS Transaction Packet

Table 8-16. STATUS TP Format (Differences with ACK TP)

[tbl-120.md](tbl-120.md)

8-35

Universal Serial Bus 3.1 Specification, Revision 1.0

### 8.5.5 STALL Transaction Packet

This TP can only be sent by an endpoint on the device. It is used to inform the host that the endpoint is halted or that a control transfer is invalid. Only the fields that are different from an ACK TP are described in this section.

![img-208.jpeg](img-208.jpeg)

Figure 8-22. STALL Transaction Packet

Table 8-17. STALL TP Format (Differences with ACK TP)

[tbl-121.md](tbl-121.md)

### 8.5.6 Device Notification (DEV_NOTIFICATION) Transaction Packet

This TP can only be sent by a device. It is used by devices to inform the host of an asynchronous change in a device or interface state, e.g., to identify the function within a device that caused the device to perform a remote wake operation. This TP is not sent from a particular endpoint but from the device in general. Only the fields that are different from an ACK TP are described in this section.

![img-209.jpeg](img-209.jpeg)

Figure 8-23. Device Notification Transaction Packet

8-36

Protocol Layer

Table 8-18. Device Notification TP Format (Differences with ACK TP)

[tbl-122.md](tbl-122.md)

### 8.5.6.1 Function Wake Device Notification

![img-210.jpeg](img-210.jpeg)

Figure 8-24. Function Wake Device Notification

Table 8-19. Function Wake Device Notification

[tbl-123.md](tbl-123.md)

$^{1}$ This Notification Type value shall be reserved for OTG use. Refer to Section 5.5 of the USB 3.0 OTG and EH Supplement for the definition of the respective Device Notification TP.

$^{2}$ This Device Notification is required for devices not operating at Gen 1 Speed. This Device Notification is optional for devices operating at Gen 1 speed.

8-37

Universal Serial Bus 3.1 Specification, Revision 1.0

### 8.5.6.2 Latency Tolerance Message (LTM) Device Notification

Latency Tolerance Message Device Notification is an optional normative feature enabling more power efficient platform operation.

![img-211.jpeg](img-211.jpeg)

Figure 8-25. Latency Tolerance Message Device Notification

Table 8-20. Latency Tolerance Message Device Notification

[tbl-124.md](tbl-124.md)

8-38

Protocol Layer

### 8.5.6.3 Bus Interval Adjustment Message Device Notification

The Bus Interval Adjustment Message Device Notification is only defined for devices operating at Gen 1 speed.

![img-212.jpeg](img-212.jpeg)

Figure 8-26. Bus Interval Adjustment Message Device Notification

Table 8-21. Bus Interval Adjustment Message Device Notification

[tbl-125.md](tbl-125.md)

### 8.5.6.4 Function Wake Notification

A function may signal that it wants to exit from device suspend (after transitioning the link to U0) or function suspend by sending a Function Wake Device Notification to the host if it is enabled for remote wakeup. Refer to Section 9.2.5 for more details.

### 8.5.6.5 Latency Tolerance Messaging

Latency Tolerance Messaging is an optional normative USB power management feature that utilizes reported BELT (Best Effort Latency Tolerance) values to enable more power efficient platform operation.

The BELT value is the maximum time (factoring in the service needs of all configured endpoints) for leaving a device without service from the host. Specifically, the BELT value is the time between the host's receipt of an ERDY from a device, and the host's transmission of the response to the ERDY.

Devices indicate whether they are capable of sending LTM TPs using the LTM Capable field in the SUPERSPEED_USB Device Capability descriptor in the BOS descriptor (refer to Section 9.6.2). The LTM Enable (refer to Section 9.4.10) feature selector enables (or disables) an LTM capable device to send LTM TPs.

8-39

Universal Serial Bus 3.1 Specification, Revision 1.0

### 8.5.6.5.1 Optional Normative LTM and BELT Requirements

# **General Device Requirements**

- LTM TPs shall be originated only by peripheral devices.
- LTM TPs apply to all endpoint types except for isochronous endpoints. For interrupt endpoints the BELT value only applies while the endpoint is in a flow control condition.
- Once a BELT value has been sent to the host by a device, all configured endpoints for that device shall expect to be serviced within the specified BELT time.
- A device shall send an LTM TP with a value of tBELTdefault in the BELT field in response to any change in state of LTM_Enable within the timing specified by tMinLTMStateChange.
- A device shall ensure that its BELT value is determined frequently enough that it is able to provide reasonable estimate of the device's service latency tolerance prior to its need to change BELT value. In addition, the following conditions shall be met:

1. The maximum number of LTM TPs is bounded by tBeltRepeat.

2. Each LTM TP shall have a different BELT value.

- The system shall default to a BELT of 1 ms for all devices (refer to Table 8-36).
- The minimum value for a BELT is 125 μs (refer to Table 8-36).

# **Device Requirements Governing Establishment of BELT Value**

- The LTM mechanism shall utilize U1SEL and U2SEL to provide devices with system latency information (see Section 9.4.12 – Set SEL). In this context, the system latency is the time between when a device transmits an ERDY and when it will receive a transaction packet (type is direction-specific) from the host when the deepest allowed link state is U1 or U2. These values are used by the device to properly adjust their BELT value, factoring in their location within the USB link topology.

1. Devices that allow their link to enter U1, but not U2, shall subtract the U1 System Exit Latency (U1SEL) from its total latency tolerance and send the resultant value as the BELT field value in an LTM TP.
2. Devices that allow their link to enter U1 and U2, shall subtract U2SEL from its total latency tolerance and send the resulting value as the BELT field value in an LTM TP.

### 8.5.6.6 Bus Interval Adjustment Message

The Bus Interval Adjustment Message may be sent only by devices operating at Gen 1 speed and shall be ignored by hosts that are not operating at Gen 1 speed. Note that this notification will be deprecated in a future release.

This device notification may be sent by a device to request an increase or decrease in the length of the bus interval. This would typically be used by a device trying to synchronize the host's bus interval clock with an external clock. Bus interval adjustment requests are relative to the current bus interval. For example, if a device requests an increase of one

BusIntervalAdjustmentGranularity unit and then later requests an increase of two BusIntervalAdjustmentGranularity units the overall increase by the host would be three BusIntervalAdjustmentGranularity units.

The host shall support adjustments through an absolute range of -37268 to 37267 BusIntervalAdjustmentGranularity units. A device shall not request adjustments more than once every eight bus intervals. A device shall not send another bus interval adjustment request until it has waited long enough to accurately observe the effect of the previous bus interval adjustment

8-40

Protocol Layer

request on the timestamp value in subsequent ITPs. A device shall not make a single BusIntervalAdjustment request for more than ±4096 units. A device may make multiple BusIntervalAdjustment requests over time for a combined total of more than 4096 units. A device shall not request a bus interval adjustment unless the device received an ITP within the past 125 μs, the ITP contained a Bus Interval Adjustment Control field with a value equal to zero or the device's address and the device is in the Address or Configured state.

Only one device can control the bus interval length at a time. The host controller implements a first come first serve policy for handling bus interval adjustment requests as described in this section. When the host controller begins operation it shall transmit ITPs with the Bus Interval Adjustment Control field set to zero. When the host controller first receives a bus interval adjustment control request, it shall set the Bus Interval Adjustment Control field in subsequent ITPs to the address of the device that sent the request. The host shall ignore bus interval adjustment requests from all other devices once the Bus Interval Adjustment Control field is set to a non-zero address. If the controlling device is disconnected, the host controller shall reset the Bus Interval Adjustment Control field to zero. The host controller may provide a way for software to override default bus interval adjustment control field behavior and select a controlling device. The host controller shall begin applying bus interval adjustments within two bus intervals from when the bus interval adjustment request is received.

The smallest bus interval adjustment (one BusIntervalAdjustmentGranularity) requires the host to make an average adjustment of eight high speed bit times every 4096 bus intervals. The host is allowed to make this adjustment in a single bus interval such that the clock used to generate ITP times and bus interval boundaries does not need a period smaller than eight high speed bit times. The host shall make bus interval adjustments at regular intervals. When the host is required to make an average of one or more eight high speed bit time adjustments every 4096 bus intervals the adjustments shall be evenly distributed as defined by the following constraints:

- Intervals that contain one more eight high speed bit time adjustment than other intervals are referred to as maximum adjustment bus intervals.
- The number of eight high speed bit time adjustments made in any bus interval shall not be more than one greater than the number of high speed bit time adjustments made in any other bus interval.
- The distance in bus intervals between consecutive maximum adjustment bus intervals shall not vary by more than one bus interval.

The even distribution and average adjustment requirements for bus interval adjustments shall apply from one bus interval after a bus interval adjustment request is received by the host until the bus interval where a subsequent valid bus interval adjustment request is received by the host.

The following is an example of valid host behavior for a specific bus interval adjustment request. After power on, the host receives a bus interval adjustment request for a bus interval decrease of 10 BusIntervalAdjustmentGranularity units in bus interval X-1. The host controller uses a clock with a period of eight high speed bit times to drive a counter that produces timestamps and bus interval boundaries. The host controller adds an extra eight high speed bit time clock tick to its counter in each of the following bus intervals: X+409, X+819, X+1228, X+1638, X+2048, X+2457, X+2867, X+3276, X+3686, X+4096, X+4505,...

8-41

Universal Serial Bus 3.1 Specification, Revision 1.0

### 8.5.6.7 Sublink Speed Device Notification

Sublink Speed Device Notification TPs are reported by the device to identify the characteristics of its link connection. Sublink Speed Device Notification TPs shall be generated by Enhanced SuperSpeed devices not operating at Gen 1 speed upon entering the Address USB Device State.

Lane Speed = Lane Speed Mantissa * 1000$^{Lane Speed Exponent}$

Sublink Speed = Lane Speed * (Lane Count + 1)

- The device shall inform the host that a Device Notification TP shall follow a SET_ADDRESS request by setting the TP Follows (TPF) flag in the Status stage ACK TP.
- The Rx Sublink Speed Device Notification TP shall be the next TP transmitted by a device after setting the TP Follows (TPF) flag in a Status stage ACK TP.
- The device shall inform the host that a second Device Notification TP shall follow the Rx Sublink Speed Device Notification TP by setting the TP Follows (TPF) flag in the Rx Sublink Speed Device Notification TP.
- The Tx Sublink Speed Device Notification TP shall be the next TP transmitted by a device after setting the TP Follows (TPF) flag in the Rx Sublink Speed Device Notification TP.

Asymmetric Lane Types may only be reported by SuperSpeed Interchip (SSIC) devices. A Symmetric link is one that has the same Lane Speed and number of lanes for both the Rx and Tx Sublinks. Enhanced SuperSpeed devices shall only support Symmetric links and shall only support one lane per sublink.

![img-213.jpeg](img-213.jpeg)

U-108A

Figure 8-27. Sublink Speed Device Notification

Table 8-22. Sublink Speed Device Notification

[tbl-126.md](tbl-126.md)

8-42

Protocol Layer

[tbl-127.md](tbl-127.md)

### NOTE

This specification includes features to support SSIC capabilities, such as asymmetric link speeds and multiple lanes.

The Enhanced SuperSpeed bus does not support Asymmetric link speeds or multiple lanes. An Enhanced SuperSpeed device shall only set the **Sublink Type** to Symmetric and shall set the **Lane Count** field to zero.

8-43

Universal Serial Bus 3.1 Specification, Revision 1.0

### 8.5.7 PING Transaction Packet

This TP can only be sent by the host. It is used by the host to transition all links in the path to a device back to U0 prior to initiating an isochronous transfer. Refer to Appendix C for details on the usage of this TP. Only the fields that are different from an ACK TP are described in this section.

A device shall respond to the PING TP by sending a PING_RESPONSE TP (refer to Section 8.5.8) to the host within the tPingResponse time (refer to Table 8-36). Note that the device shall not validate the EP_NUM and Direction fields and simply copy them to the respective fields in the PING_RESPONSE TP.

A device shall keep its link in U0 until it receives a subsequent packet from the host, or until the tPingTimeout time (refer to Table 8-36) elapses.

![img-214.jpeg](img-214.jpeg)

Figure 8-28. PING Transaction Packet

Table 8-23. PING TP Format (differences with ACK TP)

[tbl-128.md](tbl-128.md)

### 8.5.8 PING_RESPONSE Transaction Packet

This TP can only be sent by a device in response to a PING TP sent by the host. A PING_RESPONSE TP shall be sent for each PING TP received. Refer to Appendix C for details on the usage of this TP. Only the fields that are different from an ACK TP are described in this section.

8-44

Protocol Layer

![img-215.jpeg](img-215.jpeg)

U-110

Figure 8-29. PING_RESPONSE Transaction Packet

Table 8-24. PING_RESPONSE TP Format (Differences with ACK TP)

[tbl-129.md](tbl-129.md)

### 8.6 Data Packet (DP)

This packet can be sent by either the host or a device. The host uses this packet to send data to a device. Devices use this packet to return data to the host in response to an ACK TP. All data packets are comprised of a Data Packet Header and a Data Packet Payload. Only the fields that are different from an ACK TP are described in this section.

Data packets traverse the direct path between the host and a device. Note that it is permissible to send a data packet with a zero length data block; however, it shall have a CRC-32.

8-45

Universal Serial Bus 3.1 Specification, Revision 1.0

![img-216.jpeg](img-216.jpeg)

Figure 8-30. Example Data Packet

8-46

Protocol Layer

Table 8-25. Data Packet Format (Differences with ACK TP)

[tbl-130.md](tbl-130.md)

8-47

Universal Serial Bus 3.1 Specification, Revision 1.0

[tbl-131.md](tbl-131.md)

8-48

Protocol Layer

## 8.7 Isochronous Timestamp Packet (ITP)

The Isochronous Timestamp Packet (ITP) shall be multicast on all links in U0 that have completed Port Configuration.

The value in the Type field is Isochronous Timestamp Packet for an ITP. ITPs are used to deliver timestamps from the host to all active devices. ITPs carry no addressing or routing information and are multicast by hubs to all of their downstream ports with links in the U0 state and that have completed Port Configuration. A device shall not respond to an ITP. ITPs are used to provide host timing information to devices for synchronization. Note that any device or hub may receive an ITP. The host shall transmit an ITP on a root port link if and only if the link is already in U0. Only the host shall initiate an ITP transmission. The host shall not bring a root port link to U0 for the purpose of transmitting an ITP. The host shall transmit an ITP in every bus interval within tTimestampWindow from a bus interval boundary if the root port link is in U0. The host shall begin transmitting ITPs within tIsochronousTimestampStart from when the host root port's link enters U0 from the polling state. An ITP may be transmitted in between packets in a burst. If a device receives an ITP with the delayed flag (DL) set in the link control word, the timestamp value may be significantly inaccurate and may be ignored by the device.

![img-217.jpeg](img-217.jpeg)

Figure 8-31. Isochronous Timestamp Packet

8-49

Universal Serial Bus 3.1 Specification, Revision 1.0

Table 8-26. Isochronous Timestamp Packet Format

[tbl-132.md](tbl-132.md)

The ITS value in the ITP shall have an accuracy of ±1 tIsochTimestampGranularity units of the value of the host clock (for ITP generation) measured when the first framing symbol of the ITP is transmitted by the host. The requirements with respect to ITPs for a hub that supports Precision Time Management (PTM) are described in Section 10.9.4.4.1.

## 8.8 Addressing Triple

Data Packets and most Transaction Packets provide access to specific data flow using a composite of three fields. They are the **Device Address**, the **Endpoint Number**, and the **Direction** fields.

Upon reset and power-up, a device's address defaults to a value of zero and shall be programmed by the host during the enumeration process with a value in the range from 1 to 127. Device address zero is reserved as the default address and may not be assigned to any other use.

Devices may support up to a maximum of 15 IN and 15 OUT endpoints (as indicated by the **Direction** field) apart from the required default control endpoint that has an endpoint number set to zero.

## 8.9 Route String Field

The **Route String** is a 20-bit field in downstream directed packets that the hub uses to route each packet to the designated downstream port. It is composed of a concatenation of the downstream port numbers (4 bits per hub) for each hub traversed to reach a device. The hub uses a Hub Depth value multiplied by four as an offset into the Route String to locate the bits it uses to determine the

8-50

Protocol Layer

downstream port number. The Hub Depth value is determined and assigned to every hub during the enumeration process.

![img-218.jpeg](img-218.jpeg)

Figure 8-32. Route String Detail

In Figure 8-32, the value in Hub@Tier1 field is the downstream port number of the hub connected directly to one of the root ports on the host to which a second hub is attached and so on.

#### 8.9.1 Route String Port Field

This 4-bit wide field in the Route String represents the port in the hub being addressed.

#### 8.9.2 Route String Port Field Width

The Route String Port field width is fixed at 4 bits, limiting the maximum number of ports a hub may support to 15.

#### 8.9.3 Port Number

The specific port on a hub to which the packet is directed is identified by the value in the Route String Port field. When addressing the hub controller then the Port Number field at the hub's tier level shall be set to zero in the Route String. The hub's downstream ports are addressed beginning with one and count up sequentially.

### 8.10 Transaction Packet Usages

TPs are used to report the status of data transactions and can return values indicating successful reception of data packets, command acceptance or rejection, flow control, and halt conditions.

#### 8.10.1 Flow Control Conditions

This section describes the interaction between the host and a device when an endpoint returns a flow control response. The flow control is at an end-to-end level between the host and the endpoint on the device. Only bulk, control and interrupt endpoints may send flow control responses. Isochronous endpoints shall not send flow control responses.

An IN endpoint shall be considered to be in a flow control condition if it returns one of the following responses to an ACK TP:

- Responding with an NRDY TP; note that an endpoint shall wait until it receives an ACK TP for the last DP it transmitted before it can send an NRDY TP
- Sending a DP with the EOB field set to 1 in the DPH

8-51

Universal Serial Bus 3.1 Specification, Revision 1.0

An OUT endpoint shall be considered to be in a flow control condition if it returns one of the following responses to a DP:

- Responding with an NRDY TP
- Sending an ACK TP with the NumP field set to 0

The Packets Pending field is only valid when set by the host and does not affect whether or not an endpoint enters the flow control state. Refer to Section 8.11 for further details on host and device TP responses.

When an endpoint is in a flow control condition, it shall send an ERDY TP to be moved back into the active state. Further, if the endpoint is an IN endpoint, then it shall wait until it receives an ACK TP for the last DP it transmitted before it can send an ERDY TP. When an endpoint is not in a flow control condition, it shall not send an ERDY TP unless the endpoint is a Bulk endpoint that supports streams. Refer to Section 8.12.1.4.2 and Section 8.12.1.4.3 for further information about when a Bulk endpoint that supports streams can send an ERDY TP. The host may resume transactions to any endpoint – even if the endpoint had not returned an ERDY TP after returning a flow control response. To ensure that the host and the device continue to operate normally, a host shall ignore ERDY TPs from an endpoint that is not in a flow control state. If the host continues, or resumes, transactions to an endpoint, the endpoint shall re-evaluate its flow control state and respond appropriately.

### 8.10.2 Burst Transactions

The Enhanced SuperSpeed architecture allows bursting of DPs between a host and device.

SuperSpeedPlus architecture has features that create additional burst conditions for DPs:

- Multiple simultaneous IN transactions
- Hubs with additional buffering and with local arbitration decisions
- Hubs with different speed downstream facing port links.

### 8.10.2.1 Enhanced SuperSpeed Burst Transactions

The Enhanced SuperSpeed USB protocol allows the host to continually send data to a device or receive data from a device as long as the device can receive the data or transmit the data. The number of packets an endpoint on a device can send or receive at a time without an intermediate ACK TP is reported by the device in the endpoint companion descriptor (refer to Section 9.6.7) for that endpoint. An endpoint that reports more than one packet in its maximum burst size is considered to be able to support “Burst” Transactions.

While bursting the following rules apply:

- The maximum number of packets that can be sent in a burst prior to receiving an acknowledgement is limited to the minimum of the maximum burst size (see the definition of bMaxBurst in Table 9-28) of the endpoint and the value of the NumP field in the last ACK TP or ERDY received by the endpoint or the host, minus the number of packets that the endpoint or the host has already sent after the packet acknowledged by the last ACK TP.

Note that host may re-initialize the maximum number of DPs that can be sent/received in a burst to the maximum burst size of the endpoint whenever the endpoint is initialized or the host is resuming transactions to an endpoint after a flow control condition.

8-52

Protocol Layer

- Each individual packet in the burst shall have a data payload of maximum packet size. Only the last packet in a burst may be of a size smaller than the reported maximum packet size. If the last one is smaller, then the same rules for short packets apply to a short packet at the end of a burst (refer to Section 8.10.2).
- The burst transaction continues as long as the NumP field in the ACK TP is not set to zero and each packet has a data payload of maximum packet size.
- The NumP field can be incremented at any time by the host or a device sending the ACK TP as long as the device or host wants to continue receiving data. The only requirement is that the NumP field shall not have a value greater than the maximum burst supported by the device. However, for an ISOC IN endpoint, refer to Section 8.12.6, for additional requirements on how to change NumP for each burst.
- If a device or host sending an ACK TP decrements the NumP field, then it shall do so by no more than one. For example, if the previous ACK TP had a value of five in the NumP field, then the next ACK TP to acknowledge the next packet received shall have a value of no less than four in the NumP field. The only exceptions to this rule are:

1. If the device can receive the data but cannot accept any more data, then it shall send an ACK TP with the NumP field set to zero.
2. The host shall send an ACK TP with the NumP field set to zero in response to a device sending a DP with the EOB field set or that is a short packet (see Section 8.10.2). However, if the host receives a short packet with EOB = 0 and the host has another transfer to initiate with the same endpoint, then the host may instead send an ACK TP with the NumP field set to a non-zero value.
3. The host may send an ACK TP with the rty bit set to one and the NumP field set to any value less than the maximum burst that the endpoint is capable of, including zero, in response to a device sending a DP with a DPP error (See Section 8.11.2).

### 8.10.2.2 SuperSpeedPlus Burst Transactions

The SuperSpeedPlus architecture has the following additional requirements for burst transactions.

The SuperSpeedPlus architecture defines signaling rates faster than SuperSpeed. In order to maximize performance of the bus, when operating at Gen 2 speed, Enhanced SuperSpeed devices and hosts shall be limited to tGen2MaxBurstInterval for the time between DPs being bursted from a device endpoint to the host or from the host to a device endpoint.

Since the SuperSpeedPlus architecture allows multiple INs, a single SuperSpeedPlus device can be ready to burst multiple DPs from multiple endpoints whenever the link is available. A SuperSpeedPlus device operating at Gen 2 speed shall be limited to tGen2MaxDeviceMultiPacketInterval for the time between DPs being concurrently bursted from different device endpoints to the host.

In the SuperSpeedPlus architecture, DPs for different endpoints or devices can be buffered and reordered with respect to each other as they pass through SuperSpeedPlus hubs, due to other traffic that may be contending for use of path. When a SuperSpeedPlus hub has several DPs buffered for a link operating at Gen 2 speed, it shall transmit those DPs with a maximum of tGen2MaxHubMultiPacketInterval for the time between DPs, whether those DPs are for the same or different devices or endpoints.

8-53

Universal Serial Bus 3.1 Specification, Revision 1.0

### 8.10.3 Short Packets

Enhanced SuperSpeed retains the semantics of short packet behavior that USB 2.0 supports. When the host or a device receives a DP with the Data Length field shorter than the maximum packet size for that endpoint it shall deem that that transfer is complete.

In the case of an IN transfer, a device shall stop sending DPs after sending a short DP. The host shall respond to the short DP with an ACK TP with the NumP field set to zero unless it has another transfer for the same endpoint in which case it may set the NumP field as mentioned in Section 8.10.2. The host shall schedule transactions to the endpoint on the device when another transfer is initiated for that endpoint.

In the case of an OUT transaction, the host may stop sending DPs after sending a short DP. The host shall schedule transactions to an endpoint on the device when another transfer is initiated for that endpoint. Note that this shall be the start of a new burst to the endpoint.

### 8.10.4 SuperSpeedPlus Transaction Reordering

On a SuperSpeedPlus bus instance, TPs shall be transmitted before DPs (for both periodic and asynchronous packets), if there are TPs and DPs ready for transmission.

TPs use Type 1 Link Credits.

Hosts and devices shall set the Transfer Type (TT) field in ACK and Data Packet Header (DPH) packets that they originate on SuperSpeedPlus bus instances. Upward flowing DPHs from an Asynchronous endpoint have an Arbitration Weight (AW) field. SuperSpeedPlus Devices shall set the AW field to zero.

SuperSpeedPlus hubs and devices shall select periodic data packets before asynchronous data packets for transmission on the link.

Periodic DPs use Type 1 Link Credits. Asynchronous DPs use Type 2 Link Credits.

The order that DPs are returned is independent of the order in which the IN transactions from different endpoints were initiated on the bus. TPs and DPs involving the same endpoint shall be delivered in the order they were transmitted from the host or device.

8-54

Protocol Layer

BULK IN

![img-219.jpeg](img-219.jpeg)

Figure 8-33. Sample Concurrent BULK IN Transactions

8-55

Universal Serial Bus 3.1 Specification, Revision 1.0

# BULK IN and ISOC IN

![img-220.jpeg](img-220.jpeg)

Figure 8-34. Sample Concurrent BULK and Isochronous IN Transactions

8-56

Protocol Layer

### 8.11 TP or DP Responses

Transmitting and receiving devices shall return DPs or TPs as detailed in Table 8-27 through Table 8-29. Not all TPs are allowed, depending on the transfer type and depending on the direction of flow of the TP.

#### 8.11.1 Device Response to TP Requesting Data

Table 8-27 shows the possible ways a device shall respond to a TP requesting data for bulk, control, and interrupt endpoints. A TP is considered to be invalid if one or more of the following conditions exist:

- It has an incorrect Device Address
- Its endpoint number and direction does not refer to an endpoint that is part of the current configuration
- It does not have the expected sequence number
- Its TT does not match the endpoint type (for a device not operating at Gen 1 speed).

Table 8-27. Device Responses to TP Requesting Data (Bulk, Control, and Interrupt Endpoints)

[tbl-133.md](tbl-133.md)

An IN endpoint shall wait until it receives an ACK TP for the last DP it transmitted before it can send an STALL TP.

#### 8.11.2 Host Response to Data Received from a Device

Table 8-28 shows the host responses to data received from a device for bulk, control, and interrupt endpoints. The host is able to return only an ACK TP. A DPH is considered to be invalid if any of the following conditions exist:

- It has an incorrect Device Address
- Its endpoint number and direction does not refer to an endpoint that is part of the current configuration

8-57

Universal Serial Bus 3.1 Specification, Revision 1.0

- It does not have the expected sequence number
- Its Data length in the DPH is greater than the endpoint's maximum packet size
- Its TT does not match the endpoint type (from a device not operating at Gen 1 speed).

In Table 8-28, DPP Error may be due to one or more of the following:

- CRC incorrect
- DPP aborted
- DPP missing
- Data length in the DPH does not match the actual data payload length

Table 8-28. Host Responses to Data Received from a Device (Bulk, Control, and Interrupt Endpoints)

[tbl-134.md](tbl-134.md)

### 8.11.3 Device Response to Data Received from the Host

TP responses by a device to data received from the host for bulk, control, and interrupt endpoints are shown in Table 8-29. A DPH is considered to be invalid if one or more of the following conditions exist:

- It has an incorrect Device Address
- Its endpoint number and direction does not refer to an endpoint that is part of the current configuration
- It does not have the expected sequence number
- Its Data length in the DPH is greater than the endpoint's maximum packet size
- Its TT does not match the endpoint type (for a device not operating at Gen 1 speed).

In Table 8-29, DPP Error may be due to one or more of the following:

- CRC incorrect
- DPP aborted
- DPP missing
- Data length in the DPH does not match the actual data payload length

8-58

Protocol Layer

Note: Receipt of an ACK TP indicates to the host the DP with the previous sequence number was successfully received by a device as well as the number of data packet buffers the device has available to receive any pending DPs the host has. A device shall send an ACK TP for each DP successfully received.

Table 8-29. Device Responses to OUT Transactions (Bulk, Control, and Interrupt Endpoints)

[tbl-135.md](tbl-135.md)

8-59

Universal Serial Bus 3.1 Specification, Revision 1.0

### 8.11.4 Device Response to a SETUP DP

A SETUP DP is a special DP that is identified by the Setup field set to one and addressed to any control endpoint. SETUP is a special type of host-to-device data transaction that permits the host to initiate a command that the device shall perform. Upon receiving a SETUP DP, a device shall respond as shown in Table 8-30.

A SETUP DPH shall be considered invalid if it has any one of the following:

- Incorrect Device Address
- Endpoint number and direction does not refer to an endpoint that is part of the current configuration
- Endpoint number does not refer to a control endpoint
- Non-zero sequence number
- Data length is not set to eight
- TT does not match the endpoint type (for a device not operating at Gen 1 speed).

In Table 8-30, DPP Error may be due to one or more of the following:

- CRC incorrect
- DPP aborted
- DPP missing
- Data length in the Setup DPH does not match the actual data payload length.

Table 8-30. Device Responses to SETUP Transactions (Only for Control Endpoints)

[tbl-136.md](tbl-136.md)

8-60

Protocol Layer

### 8.12 TP Sequences

The packets that comprise a transaction vary depending on the endpoint type. There are four endpoint types: bulk, control, interrupt, and isochronous.

#### 8.12.1 Bulk Transactions

The bulk transaction type is characterized by its ability to guarantee error-free delivery of data between the host and a device by means of error detection and retry. Bulk transactions use a two-phase transaction consisting of TPs and DPs. Under certain flow control and halt conditions, the data phase may be replaced with a TP. The TT field shall be set to Bulk by hosts and peripheral devices operating above Gen 1 speed; see Table 8-13.

##### 8.12.1.1 State Machine Notation Information

This section shows detailed host and device endpoint state machines required to advance the Protocol on an IN or OUT pipe. The diagrams should not be taken as a required implementation, but to specify the required behavior.

Figure 8-35 shows the legend for the state machine diagrams. A circle with a three line border indicates a reference to another (hierarchical) state machine. A circle with a two-line border indicates an initial state. A circle with a single line border is a simple state.

A diamond (joint) is used to join several transitions to a common point. A joint allows a single input transition with multiple output transitions or multiple input transitions and a single output transition. All conditions on the transitions of a path involving a joint must be true for the path to be taken. A path is simply a sequence of transitions involving one or more joints.

A transition is labeled with a block with a line in the middle separating the (upper) condition and the (lower) actions. A transition without a line is a condition only. The condition is required to be true to take the transition. The actions are performed if the transition is taken. The syntax for actions and conditions is VHDL. A circle includes a name in bold and optionally one or more actions that are performed upon entry to the state.

Transitions using a solid arrow are generated by the host. Transitions using a dashed arrow are generated by a device. Transitions using a dot-dot-dash arrow are generated by the either a device or the host.

8-61

Universal Serial Bus 3.1 Specification, Revision 1.0

![img-221.jpeg](img-221.jpeg)

Figure 8-35. Legend for State Machines

### 8.12.1.2 Bulk IN Transactions

When the host is ready to receive bulk data, it sends an ACK TP to a device indicating the sequence number and number of packets it expects from the device. A Bulk endpoint shall respond as defined in Section 8.11.1.

The host shall send an ACK TP for each valid DP it receives from a device. A device does not need to wait for the ACK TP to send the next DP to the host if the previous ACK TP indicated that the host expected the device to send more than one DP (depending on the value of the Number of Packets field in the TP). The ACK TP implicitly acknowledges the last DP with the previous sequence number as being successfully received by the host and also indicates to the device the next DP with the sequence number and number of packets the host expects from the device. If the host detects an error while receiving any of the DPs, it shall send an ACK TP with the sequence number value set to the first DP that was received with an error with the Retry bit set, even if subsequent packets in the burst asked for by the host were received without error. A device is required to resend all DPs starting from the sequence number set in the ACK TP in which the Retry bit set.

8-62

Protocol Layer

The host expects the first DP to have a sequence number set to zero when it starts the first transfer from an endpoint after the endpoint has been initialized (via a Set Configuration, Set Interface, or a ClearFeature (ENDPOINT_HALT) command – refer to Chapter 9 for details on these commands). The second DP sent by the device from that endpoint shall have a sequence number set to one; the third DP has a sequence number set to two, and so on until sequence number 31. The next DP after sequence number 31 uses a sequence number of zero. An endpoint on the device keeps incrementing the sequence number of the packets it transmits unless it receives an ACK TP with the Retry bit set to one that indicates that it has to retransmit an earlier DP.

If the host asks for multiple DPs from a device and the device does not have that number of DPs available to send at the time, the device shall send the last DP with the End Of Burst flag in the DPH set to one. Note that it is not necessary to set the End Of Burst flag if the DP sent to the host has a payload that is less than the MaxPacketSize for that endpoint.

A transfer is complete when a device sends all the data that is expected by the host or it sends a DP with a payload that is less than the MaxPacketSize. When the host wants to start a new transfer, it shall send another ACK TP with the next sequence number and number of DPs expected from a device. For example, if the DP with the payload less than MaxPacketSize was two, the host shall initiate the next transfer by sending an ACK TP with the expected sequence number set to three.

### 8.12.1.3 Bulk OUT Transactions

When the host is ready to transmit bulk data, it sends one or more DPs to a device. If a DPH with valid values (valid device address, endpoint number, and direction as well as the expected sequence number) is received by a device, it shall respond as defined in Section 8.11.3.

The host always initializes the first DP sequence number to zero in the first transfer it performs to an endpoint after the endpoint is initialized (via a Set Configuration, Set Interface, or ClearFeature (ENDPOINT_HALT) command – refer to Chapter 9 for details on these commands). The second DP has a sequence number set to one; the third DP has a sequence number set to two; and so on until 31. The next DP after sequence number 31 uses a sequence number of zero. The host keeps incrementing the sequence number of the DPs it transmits unless it receives an ACK TP with the Retry bit set to one that indicates that it has to retransmit an earlier packet.

A transfer is complete when the host sends all the data it has to a device; however, the last DP of the transfer may or may not have a payload which is equal to the MaxPacketSize of the endpoint. When the host wants to start a new transfer it shall send another DP, with the next sequence number, targeted at an endpoint in the device.

8-63

Universal Serial Bus 3.1 Specification, Revision 1.0

![img-222.jpeg](img-222.jpeg)

Figure 8-36. Sample BULK IN Sequence

8-64

Protocol Layer

![img-223.jpeg](img-223.jpeg)

Figure 8-37. Sample BULK OUT Sequence

### 8.12.1.4 Bulk Streaming Protocol

The Stream Protocol adheres to the semantics of the standard Enhanced SuperSpeed Bulk protocol, so the packet exchanges on an Enhanced SuperSpeed bulk pipe that supports Streams are indistinguishable from an Enhanced SuperSpeed bulk pipe that does not. The Stream Protocol is managed strictly through manipulation of the Stream ID field in the packet header.

Note: Device Class defined methods are used for coordinating the Stream IDs that are used by the host to select Endpoint Buffers and by the device to select the Function Data associated with a particular Stream. Typically this is done via an out-of-band mechanism (e.g., another endpoint) that is used to pass the list of "Active Stream IDs" between the host and the device.

Note: The Stream state machines illustrate a 1:1 relationship between sending a DP and receiving an ACK. Logically this is true; however, Enhanced SuperSpeed burst capabilities allows up to MaxBurst outstanding ACKs between the host and a device so temporally there may be a "many to

8-65

Universal Serial Bus 3.1 Specification, Revision 1.0

1" relationship. Bursts are managed on a Stream pipe identically to how they are managed on a normal Bulk pipe. Refer to Section 8.10.2 for more information on Burst Transactions.

Note: As described in this section, the Stream Protocol applies to the state of the “pipe” and is described as single entity. In reality, the Stream Protocol is being tracked independently by the host at one end of the pipe and the device at the other. So at any instant in time the two ends may momentarily be out of phase due to packet propagation delays between the host and the device.

Note: If a Retry is requested and the host cannot continue retransmission of a DP during the current burst, the host shall return to the endpoint at the next available opportunity within the constraints of the transfer type.

![img-224.jpeg](img-224.jpeg)

Figure 8-38. General Stream Protocol State Machine (SPSM)

Figure 8-38 illustrates the basic state transitions of the Stream Protocol State Machine (SPSM). This section describes the general transitions of the SPSM as they apply to both IN and OUT endpoints. Detailed operation of the SPSM for IN and OUT endpoints is described in subsequent sections.

Disabled – This is the initial state of the pipe after it is configured, as well as the state that is transitioned to if an error is detected in any of the other states. The first time an Endpoint Buffer is assigned to the pipe, the host shall transition the SPSM to the Prime Pipe state. If the Disabled state was entered due to an error, then the error condition must be removed by software intervention before the state may be exited.

Note that an error (e.g., Stall) or a SetFeature(ENDPOINT_HALT) request shall transition any SPSM state to the Disabled state. If an error condition is detected by the host (e.g., Stall,

8-66

Protocol Layer

tHostTransactionTimeouts, etc.), the host shall transition its SPSM for the endpoint to the Disabled state. In the case where the host detects an error, not asserted by device (e.g., tHostTransactionTimeouts), the host shall transition the device's SPSM to the Disabled state by issuing a SetFeature(ENDPOINT_HALT) request to the device.

**Prime Pipe** – A transition to this state is always initiated by host, and informs a device that an Endpoint Buffer set has been added or modified by software. After exiting this state, any Active Stream IDs previously considered Not Ready by the device shall now be considered Ready.

Note: To minimize bus transactions, the host controller limits transitions to the Prime Pipe state to one transition per Idle state entry. This means that while in the Idle state only a single transition to the Prime Pipe state will be generated even if Endpoint Buffers for multiple streams become ready. And since the Prime Pipe state does not specify which Stream(s) are ready, all Active Stream IDs are set to Ready by a Prime Pipe. The device is responsible for testing all Active Stream IDs (as described above) by sending the appropriate ERDYs after returning to Idle. Note that Device Class defined constraints may be used to limit the number of Active Stream IDs that need to be tested at any point in time.

**Idle** – A transition to this state indicates that there is no Current Stream (CStream) selected. In this state, the SPSM is waiting for a transition to Prime Pipe or Move Data initiated by the Host, or a transition to Start Stream initiated by the Device. The object of the Host and Device Initiated transitions is to start moving data for a Stream. A host initiated transition to Move Data is referred to as a Host Initiated Move Data or HIMD. All Active Stream IDs are set to Ready by a HIMD.

**Start Stream** – This state is always initiated by a Device, and informs the host that the device wants to begin moving data on a selected Stream. The device may initiate a transition to this state anytime it has a Ready Stream ID. If the device selected Stream is accepted by the host, then the pipe enters the Move Data state. If the device selected Stream ID is rejected by the host, the pipe returns to Idle state and the selected Stream ID shall temporarily be considered Not Ready by the device. Note that a device maintains a list of the "Active" Stream IDs. An Active Stream ID may be Ready or Not Ready. The device is informed of the Active Stream IDs by the host through an out-of-band mechanism (typically a separate OUT endpoint).

**Move Data** – In this state, Stream data is transferred. The Current Stream is set when the SPSM transitions to this state. The SPSM transitions to the Idle state when the Stream transfer is complete, or if the host or device decides to terminate the Stream transfer because they have temporarily exhausted their data or buffer space. The transition to Idle invalidates the Current Stream for the pipe.

Note: The general rule is that a Stream state machine advances only due to the reception of a good DP or TP. For example, if a DP is received with a bad DPP, a Stream state machine shall perform any retries in the current state, and advance only if a good packet is transferred.

### 8.12.1.4.1 Stream IDs

A 16-bit field *Stream ID* field is reserved in DP headers and in ACK, NRDY, and ERDY TPs for passing SIDs between the host and a device. Specific SID values that are reserved by the Stream Protocol and other SID notations are:

- **NoStream** – This SID indicates that no Stream ID is associated with the respective bus packet and the Stream ID field should not be interpreted as referencing a valid Stream. The *NoStream* SID value is FFFFh.

8-67

Universal Serial Bus 3.1 Specification, Revision 1.0

- **Prime** – This SID is used to define transitions into and out of the Prime Pipe state. As with *NoStream*, no Stream ID is associated with the respective bus packet and the Stream ID field should not be interpreted as referencing a valid Stream. The *Prime* SID value is FFFEh.
- **Stream n** – Where n is a value between 1 and 65533 (FFFDh). This notation is used to reference a valid Stream ID. The Stream ID field in the packet header is valid if it uses this notation. Valid *Stream n* SID values are between 1 and 65533 (FFFDh), where the numeric value is identical to *n*.
- **Stream 0** – This value is reserved and not used by a pipe that supports Streams. The *Stream 0* SID value is 0000h. Its use is required by a standard bulk pipe.
- **CStream** – represents the value of the “Current” Stream ID assigned to the pipe. A *CStream* value is maintained by both the host and a device. The Stream Protocol ensures that the *CStream* values are consistent in the host and the device. Valid values are *NoStream* or *Stream n*.
- **LCStream** – represents the value of the CStream SID assigned to the pipe before the last state transition. An *LCStream* value is maintained by the host. Valid values are *Prime*, *NoStream*, or *Stream n*. For example, while the pipe in the Move Data state CStream = Stream n, when the pipe transitions from Move Data to Idle state, LCStream is set to *Stream n*, and CStream is set to *NoStream*, thus LCStream records the “Last CStream” value.

*Stream n* SID values are assigned by the host and passed to a device (typically through an out-of-band, Device Class defined method). The value of a *Stream n* SID shall be treated as a “logical value” by a device, i.e., the device should not infer any meaning from the value or modify it.

Note: The Bulk IN and OUT Stream Protocols below describe simplified state machines that do not explicitly detail the burst feature of Enhanced SuperSpeed endpoints which allows DPs to be sent without receiving an ACK. An implementation shall extend these state machines to manage bursting.

The following Sections (8.12.1.4.2 to 8.12.1.4.5) separate the Stream state machines into four cases for the device and host ends of a Stream pipe. Sections 8.12.1.4.2 and 8.12.1.4.3 describe the device end state machines. Sections 8.12.1.4.4 and 8.12.1.4.5 describe the host end state machines. And for each end of the pipe a separate section describes the respective IN and OUT operations.

The subsections in each Stream state machine section describe the state machine’s respective states. The subsections begin with a description of the purpose and general characteristics of the state, followed by a discussion of each of the state’s exit transitions. A paragraph that describes a state’s exit transition is preceded with a unique *condition* or *action* label of the associated exit transition in the previous state diagram figure.

Note: The U1 or U2 Timeouts in the path between the host and a device should be set to values that will prevent a transition to a U1 or U2 state for normal responses to Data Transactions. Refer to Section 8.13 for more Data Transaction timing information.

Note: In the Stream state machine sections, the state names are overloaded, e.g., The **Idle** state is defined in all four state machine descriptions. The **INMvData Host** state is defined in both the device and host IN state machine sections, etc. The states are related in that they may occur at either end of a Stream pipe; however, each Stream state machine section describes an independent state machine, so the conditions and actions associated with the states are distinct in each section.

8-68

Protocol Layer

Note: A transition condition that is italicized shall be interpreted as a comment, not a required condition. For example, the “Stream n Active and Ready” text of the Idle to Start Stream transition of Figure 8-39.

Note: Any CStream data payload may be zero-length. The use of zero-length DPs on a Stream pipe (other than for Prime Pipe or Start Stream reject operations) is defined by the Device Class associated with the endpoint.

Note: An IN Data or Burst Transaction is terminated with an ACK TP with NumP = 0. This ACK TP is referred to as a "Terminating ACK" in the following sections.

### 8.12.1.4.2 Device IN Stream Protocol

This section defines the Enhanced SuperSpeed packet exchanges that transition the device side of the Stream Protocol from one state to another on an IN bulk endpoint.

In the following text, a Device IN Stream state transition is assumed to occur at the point the device sends the first bit of the first symbol of a state machine related message to the host, or at the point the device first decodes state machine related message from the host.

For an IN pipe, Endpoint Buffers in the host receive Function Data from a device.

8-69

Universal Serial Bus 3.1 Specification, Revision 1.0

![img-225.jpeg](img-225.jpeg)

Figure 8-39. Device IN Stream Protocol State Machine (DISPSM)

### 8.12.1.4.2.1 Disabled

After an endpoint is configured or receives a SetFeature(ENDPOINT_HALT) request, the pipe is in the Disabled state.

ACK(Prime, NumP>0, PP=0) - If an ACK TP with the Stream ID field set to Prime is received, then the device shall transition the pipe to the Prime Pipe state. This transition occurs after the initial Endpoint Buffers are assigned to the pipe by system software.

ACK(Deferred) - If an ACK with the Deferred (DF) flag set is received, then the device shall transition the pipe to the Deferred Prime Pipe state. This packet is received when the link has transitioned to a U1 or U2 state while waiting for the initial Endpoint Buffer assignment.

### 8.12.1.4.2.2 Prime Pipe

The Prime Pipe state informs the device that the Endpoint Buffers have been assigned to one or more Streams; however, it does not specify which Stream(s). In this state, the device shall set all Active Streams to Ready. After returning to the Idle state the device shall issue an ERDY to start a specific Stream from its list of Active Streams.

8-70

Protocol Layer

NRDY(Prime) - Upon entering the **Prime Pipe** state, the device shall generate an NRDY TP with its Stream ID field set to *Prime* and transition to the **Idle** state.

### 8.12.1.4.2.3 Deferred Prime Pipe

The **Deferred Prime Pipe** state informs the device that the Endpoint Buffers have been assigned to one or more Streams; however, the link has transitioned to a U1 or U2 state while waiting. In this state, the device shall set all Active Streams to Ready. After returning to the **Idle** state the device shall issue an ERDY to start a specific Stream from its list of Active Streams.

No Condition - Upon entering the **Deferred Prime Pipe** state, the device shall immediately transition to the **Idle** state. This is the only **Deferred Prime Pipe** exit transition in Figure 8-39.

### 8.12.1.4.2.4 Idle

In the **Idle** state, the pipe is waiting for a Stream selection (e.g., a transition to **Start Stream** or **Move Data**) or a notification from the host that a Stream Endpoint Buffer has been added or modified for the pipe (i.e., transition to **Prime Pipe**). Note that upon the initial entry in to **Idle** (i.e., from **Disabled**), only the device may initiate a Stream selection.

ERDY(Stream n, NumP>0) - To initiate a Stream selection, the device generates an ERDY TP with its Stream ID set to *Stream n* and a NumP value > 0, and transitions to the **Start Stream** state, where *Stream n* is the Stream ID proposed by the device. A device may initiate this transition when it wishes to start a Stream transfer, regardless of whether the pipe is in a flow control condition or not. The device maintains a list of *Active and Ready* Streams that it may generate ERDYs for. The method that a device uses for Stream selection is outside the scope of this specification and is normally defined by the Device Class associated with the pipe. Note that the value of the ERDY NumP field reflects the amount of Endpoint Data the device has available for *Stream n*.

ACK(Prime, NumP>0, PP=0) - If an ACK TP with a Stream ID equal to *Prime* is received from the host, the device shall transition to the **Prime Pipe** state.

ACK(Stream x, NumP>0) - With this transition the host proposes the Stream ID *Stream x* to the device. If an ACK TP with a Stream ID not equal to *Prime* is received from the host, the device shall transition to the **Move Data** state. The host may initiate this transition when it wishes to start a Stream transfer and is referred to as a *Host Initiated Move Data* or **HIMD**. A HIMD indicates the specific Stream that the Endpoint Buffer had been changed for. The device shall set *Stream x* to Ready due to this transition. After entering the **Move Data** state, the device may reject the proposed Stream with an NRDY or accept the proposed Stream with a DP. Upon transitioning to the **Move Data** state the device sets *CStream* to the value of the received Stream ID (*Stream x*). Typically *Stream x* will be equal to the Stream ID (*Stream n*) in the last ERDY generated by the device. *Stream x* may not be equal to *Stream n* if one of the race conditions described below occurs, because the host drops ERDYs under these conditions. PP should equal 1.

ACK(Deferred) - If an ACK with the Deferred (DF) flag set is received, then the device shall transition the pipe to the **Deferred Prime Pipe** state. This packet is received when the link has transitioned to a U1 or U2 state and the host has attempted a HIMD.

8-71

Universal Serial Bus 3.1 Specification, Revision 1.0

### 8.12.1.4.2.5 Start Stream

In the **Start Stream** state, the device is waiting for the host to accept or reject the Active and Ready Stream selection that it has proposed.

ACK(Stream n, NumP>0) - If an ACK TP with a Stream ID equal to *Stream n* is received, the host has accepted the device's proposal for starting *Stream n* and the device shall transition to the **Move Data** state. Upon transitioning to the **Move Data** state the device sets *CStream* to the value of the received Stream ID (*Stream n*). PP should equal 1.

ACK(NoStream, NumP=0, PP=0) - If an ACK TP with a Stream ID equal to *NoStream* is received, the host has rejected the device's proposal for starting *Stream n* and the device shall transition to the **Idle** state. The device shall set *Stream n* to Not Ready due to this transition. The host shall reject a proposal from a device if there are no Endpoint Buffers available for it.

ACK(Prime, NumP>0, PP=0) - If an ACK TP with a Stream ID equal to *Prime* is received, a race condition has occurred. The host has entered the **Prime Pipe** state to inform the device that the Endpoint Buffers for one or more Streams have been updated, at the same time that the device has attempted to initiate a Stream transfer, and their respective messages have passed each other on the link. During this condition, the device is in the **Start Stream** state and the host is in the **Prime Pipe** state. To resolve this condition, the device shall transition to the **Prime Pipe** state.

ACK(Stream x, NumP>0) - If an ACK TP with a Stream ID equal to *Stream x* is received, a race condition has occurred. The host has entered the **Move Data** state to initiate a transfer on *Stream x*, at the same time that the device has attempted to initiate a transfer on *Stream n*, and their respective messages have passed each other on the link. During this condition, the device is in the **Start Stream** state and the host is in the **Move Data** state. To resolve this condition, the device shall transition to the **Move Data** state. The device shall set *Stream x* to Ready due to this transition. Upon transitioning to the **Move Data** state the device sets *CStream* to the value of the received Stream ID (*Stream x*). PP should equal 1.

ACK(Deferred) - If an ACK with the Deferred (DF) flag set is received, then the device shall transition the pipe to the **Deferred Prime Pipe** state. This packet is received when the link has transitioned to a U1 or U2 state while waiting for a host response to the Start Stream request. Note that this transition can occur only if the tERDYTimeout has been exceeded.

Note: The statement "PP should equal 1' in the **Idle** and **Start Stream** states, does not require the device to verify that PP equals 1 for the respective transition; however, if a device does check the condition it should halt the EP if PP is not equal to 1.

8-72

Protocol Layer

### 8.12.1.4.2.6 Move Data

In the Device IN Move Data state, CStream is set to the same value at both ends of the pipe and the pipe may actively move data. The details of the bus transactions executed in the Move Data state and its exit conditions are defined in the Device IN Move Data State Machine defined below.

![img-226.jpeg](img-226.jpeg)

Figure 8-40. Device IN Move Data State Machine (DIMDSM)

The Device IN Move Data State Machine (DIMDSM) is entered from the Start Stream or Idle states as described above. The entry into the DIMDSM immediately transitions to the INMvData Device state. The DIMDSM allows either the device to terminate the Move Data operation because it has exhausted its Function Data associated with a Stream or the host to terminate the Move Data operation because it has exhausted its Endpoint Buffer space associated with a Stream.

The DIMDSM always exits to the Idle state. The Retry (Rty=1) flag shall never be set in a packet that causes a DIMDSM exit. A Stream pipe remains in the Move Data state during packet retries.

Note: The Stream ID value shall be CStream for all packets exchanged in the Move Data state. If a Stream ID value other than CStream is detected while in the DIMDSM, the device should halt the endpoint.

Note: if CStream is not Active upon initially entering the Move Data state, the device may reject the Stream proposal with an NRDY or STALL the pipe, as defined by the associated Device Class.

8-73

Universal Serial Bus 3.1 Specification, Revision 1.0

### 8.12.1.4.2.7 INMvData Device

This state is initially entered from the **Start Stream** state or the **Idle** state. In this state the device prepares a DP to send to the host or may reject a HIMD from the host.

DP(CStream, EOB=0) - If the device's Endpoint Data for *CStream* is greater than one Max Packet Size, then the device may send a DP to the host with EOB = 0 and transition to the **INMvData Host** state. The DPP shall contain *CStream* data.

DP(CStream, EOB=1) - If the device's Endpoint Data for *CStream* is less than or equal to one Max Packet Size, then the device may send a DP to the host with EOB = 1 and transition to the **INMvData Device Terminate** state. The DPP shall contain *CStream* data.

NRDY(CStream) - The device may reject further *CStream* transfers by sending an NRDY with its Stream ID set to *CStream* and transition to the **Idle** state, exiting the DIMDSM. The device may generate this transition upon initial entry into the DIMDSM to reject a HIMD, or during a Stream transfer due to unexpected internal conditions where it wants to flow control *CStream*.

### 8.12.1.4.2.8 INMvData Host

In this state the device has just sent a DP to the host and has more Function Data available for *CStream*. The device waits in this state for an acknowledgement from the host for the last DP that it sent.

ACK(CStream, NumP>0, PP=1) - If the device receives an ACK with NumP > 0 and PP = 1, then it shall transition to the **INMvData Device** state. This is the host response if the current burst is not complete and it has more Endpoint Buffer space available for a *CStream* DP from the device. Note that the Retry (Rty=1) flag may be set in this packet if the host detected an error in the last DP from the device. If Rty is set, then the device shall return the DP with the appropriate Sequence Number the next time it sends a DP. If a DP error is detected, the host may continue the current burst until all retries are exhausted or a good DP is received. If the host cannot continue the current burst, the host shall initiate another burst to this endpoint at the next available opportunity within the constraints of the transfer type.

ACK(CStream, NumP=0, PP=1) - If the device receives an ACK with NumP = 0 and PP = 1, then it shall transition to the **INMvData Burst End** state. This is the host response if it has more Endpoint Buffer space available for another *CStream* DP; however, it must terminate the current burst from the device. Note that during the **INMvData Host** to **INMvData Device** transitions, the device should see NumP decrement towards 0 as the burst reaches completion. Note that the Retry (Rty=1) flag may be set in this packet if the host detected an error in the last DP from the device.

ACK(CStream, NumP=0, PP=0) - If the device receives an ACK with NumP = 0, and PP = 0, then it shall transition to the **Idle** state, exiting the DIMDSM. This is the host response to a DP when it has accepted the last DP because it has exhausted its *CStream* Endpoint Buffer space. The device shall set *CStream* to Not Ready due to this transition. During the **INMvData Host** to **INMvData Device** transitions, the device should see NumP decrement towards 0 as the Endpoint Buffer is exhausted.

Note: Receiving an ACK with NumP > 0 and PP = 0 is an illegal combination in the **INMvData Host** state and the device should halt the EP if detected.

8-74

Protocol Layer

### 8.12.1.4.2.9 INMvData Device Terminate

This state is entered because the device has just sent the last DP that it has available for CStream, e.g., it has exhausted its CStream Function Data. In this state the device waits for an acknowledgement from the host for the last DP of the Move Data transfer.

ACK(CStream, NumP=0, No Rty) - If the device receives an ACK with NumP = 0 and Rty = 0, then it shall transition to the Idle state, exiting the DIMDSM. This is the normal host response (Terminating ACK) for acknowledging the successful reception of the last DP for CStream from the device.

ACK(CStream, NumP>0, PP=1, Rty) - If the device receives an ACK with Rty = 1, then it shall transition to the INMvData Device state and resend the appropriate DP. This is the host response if an error was detected on the DP from the device and the burst was not complete.

ACK(CStream, NumP=0, PP=1, Rty) - If the device receives an ACK with Rty = 1 and NumP = 0, then it shall transition to the INMvData Burst End state and wait for the host to initiate the next burst. This is the host response if an error was detected on the DP from the device but the burst was complete. The host shall continue the retry process in the next burst.

### 8.12.1.4.2.10 INMvData Burst End

This state is entered because the host has terminated a burst on a stream pipe. In this state the device waits for an ACK TP that signifies the start of another burst.

ACK(CStream, NumP>0, PP=1) - If the device receives an ACK with NumP > 0 and PP = 1, then it shall transition to the INMvData Device state. Note, if the Rty flag was set when the state was entered, then it shall be set upon exit.

ACK(Deferred) - If an ACK with the Deferred (DF) flag set is received, then the device shall transition to the Idle state, exiting the DIMDSM. This transition occurs when the link has entered to a U1 or U2 state while waiting for the host to restart a burst, and this transition becomes more likely as the transfer activity associated with other devices increases.

### 8.12.1.4.3 Device OUT Stream Protocol

This section defines the Enhanced SuperSpeed packet exchanges that transition the device side of the Stream Protocol from one state to another on an OUT bulk endpoint.

In the following text, a Device OUT Stream state transition is assumed to occur at the point the device sends the first bit of the first symbol of a state machine related message to the host, or at the point the device first decodes a state machine related message from the host.

For an OUT pipe, Endpoint Data in the host is transmitted to Function Buffers in a device. Unless otherwise stated, a DP will contain Endpoint Data.

8-75

Universal Serial Bus 3.1 Specification, Revision 1.0

![img-227.jpeg](img-227.jpeg)

Figure 8-41. Device OUT Stream Protocol State Machine (DOSPSM)

### 8.12.1.4.3.1 Disabled

After an endpoint is configured or receives a SetFeature(ENDPOINT_HALT) request, the pipe is in the Disabled state.

DP(Prime, PP=0) - If a DP with the Stream ID field set to Prime is successfully received, then the device shall transition the pipe to the Prime Pipe state. The DPP shall contain a zero-length data payload. This transition occurs after the initial Endpoint Buffers are assigned to the pipe by system software. Note, if an error is detected in the DP data (even though it is zero-length) the device shall remain in the Disabled state, and issue ACK(Prime, NumP>0, Rty) packets, retrying until a DP(Prime) is successfully received. This case is not illustrated in the figure above.

DPH(Deferred) - If a DP with the Deferred (DF) flag set is received, then the device shall transition the pipe to the Deferred Prime Pipe state. This packet is received when the link has transitioned to a U1 or U2 state while waiting for the initial Endpoint Data assignment.

8-76

Protocol Layer

### 8.12.1.4.3.2 Prime Pipe

The **Prime Pipe** state informs the device that the Endpoint Data has been assigned to one or more Streams; however, it does not specify which Stream(s). After returning to the **Idle** state the device shall issue an ERDY to start a specific Stream from its list of Active and Ready Streams.

NRDY(Prime) - Upon entering the **Prime Pipe** state, the device shall return an NRDY TP with its Stream ID field set to *Prime* and immediately transition to the **Idle** state.

### 8.12.1.4.3.3 Deferred Prime Pipe

The **Deferred Prime Pipe** state informs the device that the Endpoint Data has been assigned to one or more Streams; however, the link has transitioned to a U1 or U2 state while waiting.

No Condition - Upon entering the **Deferred Prime Pipe** state, the device shall immediately transition to the **Idle** state.

### 8.12.1.4.3.4 Idle

In the **Idle** state, the pipe is waiting for a Stream selection (e.g., a transition to **Start Stream** or **Move Data**) or a notification from the host that Endpoint Data has been added or modified for the pipe (i.e., transition to **Prime Pipe**). Note that upon the initial entry in to **Idle**, only the device may initiate a Stream selection.

ERDY(Stream n, NumP>0) - To initiate a Stream selection, the device generates an ERDY TP with its Stream ID set to *Stream n* and a NumP value > 0, and transitions to the **Start Stream** state, where *Stream n* is the Stream ID proposed by the device. A device may initiate this transition when it wishes to start a Stream transfer, regardless of whether the pipe is in a flow control condition or not. The device maintains a list of *Active and Ready* Streams that it may generate ERDYs for. The method that a device uses for Stream selection is outside the scope of this specification and is normally defined by the Device Class associated with the pipe. Note that the value of ERDY NumP reflects the amount of Endpoint Buffer space the device has available for *Stream n*.

DP(Prime, PP=0) - If a DP with a Stream ID equal to *Prime* is successfully received, the device shall transition to the **Prime Pipe** state. The DPP shall contain a zero-length data payload. Note, if an error is detected in the DP data the device shall remain in the **Idle** state, and issue ACK(Prime, NumP>0, Rty) packets, retrying until a DP(Prime) is successfully received. This case is not illustrated in the Figure above. The DPP shall contain a zero-length data payload.

DP(Stream x) - With this transition the host proposes the Stream ID *Stream x* to the device. If a DP with a Stream ID not equal to *Prime* is received from the host, the device shall transition to the **Move Data** state. The host may initiate this transition when it wishes to start a Stream transfer and is referred to as a *Host Initiated Move Data* or **HIMD**. A HIMD indicates the specific Stream that the Endpoint Data had been changed for. The device shall set *Stream x* to Ready due to this transition. After entering the **Move Data** state, the device may reject the proposed Stream with an NRDY or accept the proposed Stream with an ACK TP. Upon transitioning to the **Move Data** state the device sets *CStream* to the value of the received Stream ID (*Stream x*). The DPP shall contain the first data payload for the Stream. Typically *Stream x* will be equal to the Stream ID (*Stream n*) in the last ERDY generated by the device. *Stream x* may not be equal to *Stream n* if one of the race conditions described below occurs, because the host drops ERDYs under these conditions.

8-77

Universal Serial Bus 3.1 Specification, Revision 1.0

DPH(Deferred) - If a DPH with the Deferred (DF) flag set is received, then the device shall transition to the Deferred Prime Pipe state. This packet may be received when the link has transitioned to a U1 or U2 state and the host has attempted a transition to Prime Pipe or Move Data (a HIMD).

### 8.12.1.4.3.5 Start Stream

In the Start Stream state, the device is waiting for the host to accept or reject the Active and Ready Stream selection that it has proposed.

DP(Stream n) - If a DP with a Stream ID equal to Stream n is received: the host has accepted the device's proposal for starting Stream n and provided the first packet of Stream n data, and the device shall transition to the Move Data state. Upon transitioning to the Move Data state the device sets CStream to the value of the received Stream ID (Stream n). The DPP shall contain the first data payload for CStream.

DP(NoStream, PP=0) - If a DP with a Stream ID equal to NoStream is successfully received, the host has rejected the device's proposal for starting Stream n and the device shall transition to the Start Stream End state. The DPP shall contain a zero-length data payload. The host shall reject a proposal from a device if there is no Endpoint Data available for the Stream. The device shall set Stream n to Not Ready due to this transition. Note, if an error is detected in the DP data the device shall remain in the Start Stream state, and issue ACK(NoStream, NumP>0, Rty) packets, retrying until a DP(NoStream) is successfully received. This case is not illustrated in the Figure above.

DP(Prime, PP=0) - If a DP with a Stream ID equal to Prime is received, a race condition has occurred. The host has entered the Prime Pipe state to inform the device that Endpoint Data for one or more Streams has been posted, at the same time that the device has attempted to initiate a Stream transfer, and their respective messages have passed each other on the link. The DPP shall contain a zero-length data payload. During this condition, the device is in the Start Stream state and the host is in the Prime Pipe state. To resolve this condition, the device shall transition to the Prime Pipe state. Note, if an error is detected in the DP data the device shall transition to the Prime Pipe state and perform any retries there.

DP(Stream x) - If a DP with a Stream ID not equal to Stream n, Prime or NoStream (e.g., equal to Stream x) is received, a race condition has occurred. The host has entered the Move Data state to initiate a transfer on Stream x, at the same time that the device has attempted to initiate a transfer on Stream n, and their respective messages have passed each other on the link. During this condition, the device is in the Start Stream state and the host is in the Move Data state. To resolve this condition, the device shall transition to the Move Data state. The device shall set Stream x to Ready due to this transition. Upon transitioning to the Move Data state the device sets CStream to the value of the received Stream ID (Stream x). The DPP shall contain the first data payload for CStream. The device may accept or reject the Stream proposed by the host when in the Move Data state.

DPH(Deferred) - If a DPH with the Deferred (DF) flag set is received, then the device shall transition the pipe to the Idle state. This packet is received when the link has transitioned to a U1 or U2 state while waiting for a host response to the Start Stream request. Note that this transition is highly unlikely because it can only occur if the tERDYTimeout has been exceeded. The device is expected to retry with an ERDY in this case. There is no DPP associated with a deferred DPH.

8-78

Protocol Layer

### 8.12.1.4.3.6 Start Stream End

In the **Start Stream End** state, the device has received a rejection of the Stream selection that it has proposed, and must respond to the DP from the host. The Bulk protocol requires an ACK or NRDY response for any DP sent. The Streams protocol specifies that an NRDY is sent.

NRDY(NoStream) - The device shall generate an NRDY with the Stream ID equal to *NoStream* and transition to the **Idle** state.

### 8.12.1.4.3.7 Move Data

In the Device OUT **Move Data** state, *CStream* is set to the same value at both ends of the pipe and the pipe may actively move data. The details of the bus transactions executed in the **Move Data** state and its exit conditions are defined in the Device OUT Move Data State Machine defined below.

![img-228.jpeg](img-228.jpeg)

Figure 8-42. Device OUT Move Data State Machine (DOMDSM)

The Device OUT Move Data State Machine (DOMDSM) is entered from the **Start Stream** or **Idle** states as described above.

8-79

Universal Serial Bus 3.1 Specification, Revision 1.0

The DOMDSM allows either the device to terminate the Move Data operation because it has exhausted its Function Buffer space associated with a Stream or the host to terminate the Move Data operation because it has exhausted its Endpoint Data associated with a Stream.

PP=0 - Upon entry into the DOMDSM, if the host has only one packet of Endpoint Data available for the Stream then PP will equal 0 in the first DP received by the Device, and it shall transition to the OUTMvData Device Terminate state.

PP = 1 - Upon entry into the DOMDSM, if the host has more than one packet of Endpoint Data available for the Stream then PP will equal 1 in the first DP received by the Device, and it shall transition to the OUTMvData Device state.

The DOMDSM always exits to the Idle state. The Retry (Rty=1) flag shall never be set in a packet that causes a DOMDSM exit. A Stream pipe remains in the Move Data state during packet retries.

Note: The Stream ID value shall be CStream for all packets exchanged in the Move Data state. If a Stream ID value other than CStream is detected while in the DOMDSM the device should halt the endpoint.

Note: if CStream is not Active upon initially entering the Move Data state, the device may reject the Stream proposal with an NRDY or STALL the pipe, as defined by the associated Device Class.

# 8.12.1.4.3.8 OUTMvData Device

This state is initially entered from the Start Stream state or the Idle state. In this state the device acknowledges the last DP sent by the host or it may reject a HIMD from the host.

ACK(CStream, NumP>0) - If the device has more Function Buffer space available for CStream, then it shall send an ACK TP to the host with NumP > 0 and transition to the OUTMvData Host state. Note that the Retry (Rty) flag may be set in this packet if the device detected an error in the last DP from the host. The host shall continue the current burst until all retries are exhausted or a positive acknowledgement (Rty=0) is received. This transition shall indicate that the data payload of the previously received DP has been accepted by the endpoint for CStream.

ACK(CStream, NumP=0) - If the device has no more Endpoint Buffer space available for CStream, then it shall generate an ACK TP with NumP = 0, exit the DOMDSM and transition to the Idle state. This transition allows the device to exit from the Move Data state if its Endpoint Buffer space is exhausted. This transition shall indicate that the data payload of the previously received DP has been accepted by the endpoint for CStream.

NRDY(CStream) - The device may also terminate further CStream transfers by sending an NRDY with its Stream ID set to CStream, transitioning to the Idle state, exiting the DOMDSM. The device may generate this transition upon initial entry into the DOMDSM to reject a HIMD, or during a Stream transfer due to unexpected internal conditions where it wants to flow control CStream. This transition shall indicate that the data payload of the previously received DP has been dropped.

8-80

Protocol Layer

### 8.12.1.4.3.9 OUTMvData Host

In this state the host has just received an ACK TP from the device for a previous DP and has more Endpoint Data available for CStream. The host generates a DP in this state. The pipe will also wait in this state between bursts from the host.

DP(CStream, PP=1) - If the device receives a DP with PP = 1, then it shall transition to the OUTMvData Device state. The DPP shall contain a CStream data payload. This is the host response if it has more than one Max Packet Size of Endpoint Data available for CStream.

DP(CStream, PP=0) - If the device receives a DP with PP = 0, then it shall transition to the OUTMvData Host Terminate state. The DPP shall contain a CStream data payload. This is the host response if it has exhausted the Endpoint Data that it has available for CStream. The length of the DP will be less than or equal to one Max Packet Size.

DPH(Deferred) - If a DPH with the Deferred (DF) flag set is received, then the device shall transition to the Idle state, exiting the DOMDSM. This packet is received when the link has transitioned to a U1 or U2 state while waiting for the next DP from the host. There is no DPP associated with a deferred DPH.

### 8.12.1.4.3.10 OUTMvData Host Terminate

This state is entered because the host has just sent the last DP that it has available for CStream, e.g., it has exhausted its CStream Endpoint Data. In this state the device acknowledges the last DP from the host for the Move Data transfer.

ACK(CStream, NumP=0) - If the device has also exhausted its Function Buffer space, then it shall generate an ACK TP with NumP = 0 and transition to the Idle state, exiting the DOMDSM.

ACK(CStream, NumP>0) - If the device has not exhausted its Function Buffer space, then it shall generate an ACK TP with NumP > 0, and transition to the Idle state, exiting the DOMDSM. The device shall set CStream to Not Ready due to this transition.

ACK(CStream, NumP>0, Rty) - If an error was detected on the last DP by the device, then it shall generate an ACK TP with NumP > 0 and Rty = 1, so that the host will retry the last DP. The device shall then transition to the OUTMvData Host state.

NRDY(CStream) - The device may flow control on the last CStream transfer by sending an NRDY with its Stream ID set to CStream and transition to the Idle state, exiting the DOMDSM. The device may generate this transition due to unexpected internal conditions where it wants to flow control CStream.

### 8.12.1.4.4 Host IN Stream Protocol

This section defines the Enhanced SuperSpeed packet exchanges that transition the host side of the Stream Protocol from one state to another on an IN bulk endpoint.

In the following text, a Host IN Stream state transition is assumed to occur at the point the host sends the first bit of the first symbol of a state machine related message to the device, or at the point the host first decodes state machine related message from the device.

For an IN pipe, Endpoint Buffers in the host receive Function Data from a device.

8-81

Universal Serial Bus 3.1 Specification, Revision 1.0

![img-229.jpeg](img-229.jpeg)

Figure 8-43. Host IN Stream Protocol State Machine (HISPSM)

### 8.12.1.4.4.1 Disabled

After an endpoint is configured or an endpoint error condition (Stall, tHostTransactionTimeout, etc.) request, the pipe is in the **Disabled** state and *LCStream* is initialized to *NoStream*.

ACK(Prime, NumP>0, PP=0) - When the initial Endpoint Buffers are assigned to the pipe by system software, the host shall send an ACK TP with the Stream ID field set to *Prime* to the device, and transition the pipe to the **Prime Pipe** state.

### 8.12.1.4.4.2 Prime Pipe

The **Prime Pipe** state informs the device that the Endpoint Buffers have been assigned to one or more Streams.

NRDY(Prime) – If the host receives an NRDY TP with its Stream ID field set to *Prime*, it shall transition to the **Idle** state. This transition is the normal termination of a Prime Pipe operation.

ACK(Deferred) - If an ACK with the Deferred (DF) flag set is received, then the host shall transition the pipe to the **Idle** state. This packet may be received when the link has transitioned to a

8-82

Protocol Layer

U1 or U2 state while the pipe was waiting for its initial Endpoint Buffer assignment. e.g. after an ACK(Prime, NumP>0, PP=0) has been generated in the Disabled state.

ERDY() - If an ERDY is received, a race condition has occurred. During this condition, the device is in the Start Stream state and the host is in the Prime Pipe state. The host has entered the Prime Pipe state to inform the device that the Endpoint Buffers for one or more Streams have been updated, at the same time that the device has attempted to initiate a Stream transfer, and their respective messages have passed each other on the link. To resolve this condition, the host shall remain in the Prime Pipe state and wait for an NRDY(Prime) from the device.

### 8.12.1.4.4.3 Idle

In the Idle state, the pipe is waiting for a Stream selection (e.g., a transition to Start Stream or Move Data) or a notification from the host that Stream Endpoint Data has been added or modified for the pipe (i.e., transition to Prime Pipe). Note that upon the initial entry in to Idle (i.e., from Disabled), only the device may initiate a Stream selection.

ERDY(Stream n, NumP>0) -If an ERDY is received, the host shall transition to the Start Stream state. The device generates an ERDY to select a specific Stream (Stream n) that it expects the host to begin IN transactions on. A device may initiate this transition when it wishes to start a Stream transfer, regardless of whether it had previously flow controlled the pipe or not. Note that the value of the ERDY NumP field reflects the amount of Endpoint Data the device has available for Stream n. The value of the ERDY NumP is informative and the method that a device uses for Stream selection is outside the scope of this specification and is normally defined by the Device Class associated with the pipe. Upon transitioning to the Start Stream state the host sets LCStream to the value of Stream n.

ACK(Deferred) - If an ACK with the Deferred (DF) flag set is received, then the host shall remain in the Idle state. This packet is received if the link has transitioned to a U1 or U2 state when the host rejects a Start Stream request from the device (i.e., due to an ACK( NoStream, NumP=0, PP=0)). This case only occurs if tERDYTimeout is exceeded.

Stream x EP Buffer Change - This transition occurs if the state of one or more Endpoint Buffers has changed in the host. The host evaluates (at the Joint “&”) the ID of the Stream that software presents to the host controller (Stream x) and transitions to the Prime Pipe or Move Data states. This is an optimization that allows the host to transition the Stream pipe directly to the Move Data state, rather than going through the Prime Pipe, Start Stream, Move Data sequence, and is referred to as a Host Initiated Move Data or HIMD. The specific algorithm used to make this decision is host specific.

&

ACK(Prime, NumP>0, PP=0) - If the transition to Prime Pipe is selected, then the host shall generate a ACK TP with the Stream ID = Prime, NumP > 0, and PP = 0, and transition to the Prime Pipe state. Note that the host asserts a non-zero NumP value so that the device may respond with an NRDY. If NumP = 0, the device would consider it a Terminating ACK and not respond. Typically the Prime Pipe transition will be selected when the Stream that has just had its host Endpoint Buffers modified is not the same Stream that the device has last selected, e.g., Stream x != LCStream.

ACK(Stream x, NumP>0) - If the transition to Move Data is selected, then the host shall generate a ACK TP with the Stream ID = Stream x and NumP > 0, and transition to the Move

8-83

Universal Serial Bus 3.1 Specification, Revision 1.0

Data state. Upon transitioning to the Move Data state the host sets CStream to the value of Stream x. Typically the Move Data transition will be selected when the Stream that has just had its Endpoint buffers modified is the same Stream as the one that the device last selected, e.g., Stream x = LCStream. PP shall equal 1 because the host is capable of receiving another DP from the device. This transition optionally may be disabled in some hosts, and some Device Classes may not process this transition (e.g., Mass Storage UASP).

### 8.12.1.4.4.4 Start Stream

In the Start Stream state, the device has sent an ERDY proposing to the host that it initiate an IN transfer for Stream n and it is waiting for the host to accept or reject the Stream selection.

ACK(Stream n, NumP>0) - If the host has accepted the device's proposal for starting Stream n, then it shall transmit an ACK TP with a Stream ID equal to Stream n, and transition to the Move Data state. Upon transitioning to the Move Data state the host sets CStream to the value of Stream n. The host shall accept a Stream proposal from a device if there are Endpoint Buffers available to receive the Function Data for the Stream. PP shall equal 1 because the host is capable of receiving another DP from the device.

ACK(NoStream, NumP=0, PP = 0) - If the host rejects the device's proposal for starting Stream n, then it shall transmit an ACK TP with a Stream ID equal to NoStream, and transition to the Idle state. The host shall reject a Stream proposal from a device if there are no Endpoint Buffers available to receive the Function Data for the Stream.

8-84

Protocol Layer

### 8.12.1.4.4.5 Move Data

In the Host IN Move Data state, CStream is set to the same value at both ends of the pipe and the pipe may actively move data. The details of the bus transactions executed in the Move Data state and its exit conditions are defined in the Host IN Move Data State Machine defined below.

![img-230.jpeg](img-230.jpeg)

Figure 8-44. Host IN Move Data State Machine (HIMDSM)

The Host IN Move Data State Machine (HIMDSM) is entered from the Start Stream or Idle states as described above. The entry into the HIMDSM immediately transitions to the INMvData Device state. The HIMDSM allows either the device to terminate the Move Data operation because it has exhausted its Function Data associated with a Stream or the host to terminate the Move Data operation because it has exhausted its Endpoint Buffer space associated with a Stream.

The HIMDSM always exits to the Idle state. The Retry (Rty=1) flag shall never be set in a packet that causes a HIMDSM exit. A Stream pipe remains in the Move Data state during packet retries.

Note: The Stream ID value shall be CStream for all packets exchanged in the Move Data state, except the INMvData Device substate ERDY transition. For the identified substates, if a Stream ID value other than CStream is detected while in the HIMDSM the host should halt the endpoint.

8-85

Universal Serial Bus 3.1 Specification, Revision 1.0

### 8.12.1.4.4.6 INMvData Device

This state is initially entered from the **Start Stream** state or the **Idle** state. In this state the host is waiting for a DP from the device or a rejection of a HIMD.

DP(CStream, EOB=0) - If the host receives a DP with EOB = 0, it shall copy the DP data to the Endpoint Buffer associated with the Stream and transition to the **INMvData Host** state. The DPP shall contain a *CStream* data payload. This transition occurs when the device returns IN data and has more Function Data to send. Upon transitioning to the **INMvData Host** state the host sets *LCStream* to the value of *CStream*. This action updates *LCStream* with the value of *CStream* if the device accepts a HIMD, i.e., *LCStream* records the last Stream that was of interest to the device.

DP(CStream, EOB=1) - If the host receives a DP with EOB = 1, it shall copy the DP data to the Endpoint Buffer associated with the Stream and transition to the **INMvData Device Terminate** state. The DPP shall contain a *CStream* data payload. This transition occurs when device returns IN data and has no more Function Data to send, e.g., it is terminating the Move Data operation because this DP exhausts the Function Data available for this Stream. Upon transitioning to the **INMvData Device Terminate** state the host sets *LCStream* to the value of *CStream*. This action updates *LCStream* with the value of *CStream* if the device accepts a HIMD, i.e., *LCStream* records the last Stream that was of interest to the device.

NRDY(CStream) - If the host receives an NRDY, it shall exit the HIMDSM and transition to the **Idle** state. This transition may occur upon initial entry into the HIMDSM when the device rejects a HIMD, or during a Stream transfer due to unexpected internal device conditions where it wants to flow control *CStream*.

ACK(Deferred) - If the host receives an ACK with the Deferred (DF) flag set, then it shall exit the HIMDSM and transition to the **Idle** state. This packet shall be received if a link in the path between the host and the device has transitioned to a U1 or U2 state. There are two cases when this transition may occur: 1) the host has attempted a HIMD, and 2) between bursts. Case 1 is likely to occur if there has been a long host delay in obtaining buffers for the Stream. Case 2 may occur if there is a lot of endpoint activity on other devices delaying the time between bursts. The device treats this transition like a Prime Pipe and will send an ERDY to restart the stream when it receives the Deferred ACK forwarded to it by a hub.

ERDY() - If an ERDY is received, a race condition has occurred. During this condition, the device is in the **Start Stream** state and the host is in the **Move Data** state. The host has entered the **Move Data** state as the result of a HIMD, at the same time that the device has attempted to initiate a Stream transfer, and their respective messages have passed each other on the link. To resolve this condition, the host shall remain in the **INMvData Device** state and wait for a DP or an NRDY from the device.

### 8.12.1.4.4.7 INMvData Host

In this state the host has received a DP from a device that has more Function Data available for *CStream*. The host responds with an acknowledgement after copying the received data to the Endpoint Buffer space associated with the Stream.

ACK(CStream, NumP>0, PP=1) - If more Endpoint Buffer space is available for the Stream and the host is continuing the current burst to the device, then the host shall generate an ACK TP with NumP > 0 and PP = 1, and transition to the **INMvData Device** state. If the host detected an error

8-86

Protocol Layer

on the last DP from the device, then the Rty flag shall be set. The host may continue the INMvData Host to INMvData Device loop until all retries are exhausted or a good packet is received by the device. If the current burst terminates before all retries are exhausted, the host may transition to the INMvData Burst End state (with Rty=1) and return to the INMvData Device state (with Rty=1) at the next available opportunity to continue the retry process within the constraints of the endpoint type.

ACK(CStream, NumP=0, PP=1) - If more Endpoint Buffer space is available for the Stream; however, the host must terminate the current burst to the device, then the host shall generate an ACK TP with NumP = 0 and PP = 1, and transition to the INMvData Burst End state. If the host detected an error on the last DP from the device, then the Rty flag shall be set.

ACK(CStream, NumP=0, PP=0) - If the host did not detect an error on the last DP received from the device and the Endpoint Buffer space available for the Stream is exhausted, then the host shall generate an ACK TP with NumP = 0 and PP = 0, and transition to the Idle state, exiting the HIMDSM. This transition informs the device the host has exhausted its Endpoint Buffer space for the Stream.

###### 8.12.1.4.4.8 INMvData Burst End

This state is entered because the host has terminated a burst on a stream pipe. The host will exit this state when it is ready to start another burst. If this state was entered while retrying (Rty = 1), then the host shall continue the retry process within the constraints of the endpoint when exiting the state.

ACK(CStream, NumP>0, PP=1) - When ready to start another burst to the device on CStream, the host shall generate an ACK with NumP > 0 and PP = 1 and transition to the INMvData Device state. Note, if the Rty flag was set when the state was entered, then it shall be set upon exit.

###### 8.12.1.4.4.9 INMvData Device Terminate

In this state the host has received the last DP from a device for this Move Data operation because the device has exhausted the Function Data it has available for CStream. The host responds with an acknowledgement after copying the received data to the Endpoint Buffer space associated with the Stream and exits the HIMDSM. If the DP received from the device is bad, then retries may be performed within the constraints of the endpoint type.

ACK(CStream, NumP=0, No Rty) - If the DP received from the device is good, then the host generates an ACK with NumP = 0 and Rty = 0, and transitions to the Idle state, exiting the HIMDSM.

ACK(CStream, NumP>0, PP=1, Rty) - If the DP received from the device is bad and the current burst is not complete, then the host shall generate an ACK with NumP > 0, PP = 1 and Rty = 1, and transition to the INMvData Device state. The host may continue the INMvData Device Terminate to INMvData Device loop until all retries are exhausted or a good packet is received.

ACK(CStream, NumP=0, PP=1, Rty) - If the DP received from the device is bad and the current burst is complete, then the host shall generate an ACK with NumP = 0, PP = 1 and Rty = 1, and transition to the INMvData Burst End state. The host shall continue the retry process in the next burst.

8-87

Universal Serial Bus 3.1 Specification, Revision 1.0

### 8.12.1.4.5 Host OUT Stream Protocol

This section defines the Enhanced SuperSpeed packet exchanges that transition the host side of the Stream Protocol from one state to another on an OUT bulk endpoint.

In the following text, a Host OUT Stream state transition is assumed to occur at the point the host sends the first bit of the first symbol of a state machine related message to the device, or at the point the host first decodes state machine related message from the device.

For an OUT pipe, Function Buffers in the device receive Endpoint Data from the host.

![img-231.jpeg](img-231.jpeg)

Figure 8-45. Host OUT Stream Protocol State Machine (HOSPSM)

#### 8.12.1.4.5.1 Disabled

After an endpoint is configured or receives a SetFeature(ENDPOINT_HALT) request, the pipe is in the Disabled state and LCStream is initialized to NoStream.

DP(Prime, PP=0) - When the initial Endpoint Data is assigned to the pipe by system software, the host shall send a zero-length DP with the Stream ID field set to Prime to the device, and transition the pipe to the Prime Pipe state. The DPP shall contain a zero-length data payload.

8-88

Protocol Layer

### 8.12.1.4.5.2 Prime Pipe

The **Prime Pipe** state informs the device that Endpoint Buffers have been assigned to one or more Streams. Note, this state is entered when the host transmits a DP(Prime) from the **Disabled** or the **Idle** state. If an error is detected in the DP data by the device, the device shall issue ACK(Prime, NumP>0, Rty) packet, retrying until a DP(Prime) is successfully received. The host may retransmit the DP(Prime) and shall remain in the **Prime Pipe** state until the device successfully receives the DP(Prime) and returns an NRDY(Prime), or the retries for the pipe are exhausted and the host halts the pipe. This case is not illustrated in the Figure above.

NRDY(Prime) - If the host receives an NRDY TP with its Stream ID field set to *Prime*, it shall transition to the **Idle** state. This transition is the normal termination of a Prime Pipe operation.

DPH(Deferred) - If a DPH with the Deferred (DF) flag set is received, then the host shall transition the pipe to the **Idle** state. This packet may be received when the link has transitioned to the U1 or U2 state while the pipe waiting for its initial Endpoint Buffer assignment, e.g., after a DP(Prime, PP=0) has been generated in the **Disabled** state. There is no DPP associated with a deferred DPH.

ERDY() - If an ERDY is received, a race condition has occurred. During this condition, the device is in the **Start Stream** state and the host is in the **Prime Pipe** state. The host has entered the **Prime Pipe** state to inform the device that the Endpoint Buffers for one or more Streams have been updated, at the same time that the device has attempted to initiate a Stream transfer, and their respective messages have passed each other on the link. To resolve this condition, the host shall remain in the **Prime Pipe** state and wait for an NRDY from the device.

### 8.12.1.4.5.3 Idle

In the **Idle** state, the pipe is waiting for a Stream selection (e.g., a transition to **Start Stream** or **Move Data**) or a notification from the host that Stream Endpoint Data has been added or modified for the pipe (i.e., transition to **Prime Pipe**). Note that upon the initial entry in to **Idle** (i.e., from **Disabled**), only the device may initiate a Stream selection.

ERDY(Stream n, NumP>0) - If an ERDY is received, the host shall transition to the **Start Stream** state. The device generates an ERDY to select a specific Stream (*Stream n*) that it expects the host to begin OUT transactions on. A device may initiate this transition when it wishes to start a Stream transfer, regardless of whether it had previously flow controlled the pipe or not. Note that the value of the ERDY NumP field reflects the amount of Endpoint Buffer space the device has available for *Stream n*. The method that a device uses for Stream selection is outside the scope of this specification and is normally defined by the Device Class associated with the pipe. Upon transitioning to the **Start Stream** state the host sets *LCStream* to the value of *Stream n*.

*Stream x EP Buffer Change* - This transition occurs if Endpoint Data has been posted for one or more Streams in the host. The host evaluates (at the Joint "&") the ID of the Stream that software presents to the host controller (*Stream x*) and transitions to the **Prime Pipe** or **Move Data** states. This is an optimization that allows the host to transition the Stream pipe directly to the **Move Data** state, rather than going through the **Prime Pipe**, **Start Stream**, **Move Data** sequence, and is referred to as a *Host Initiated Move Data* or **HIMD**. The specific algorithm used to make this decision is host specific.

8-89

Universal Serial Bus 3.1 Specification, Revision 1.0

&

DP(Prime, PP=0) - If the transition to Prime Pipe is selected, then the host shall generate a DP with the Stream ID = Prime and PP = 0, and transition to the Prime Pipe state. The DPP shall contain a zero-length data payload. Typically, the Prime Pipe transition will be selected when the Stream that has just had its Endpoint Data modified is not the same Stream that the device has last selected, e.g., Stream x != LCStream.

DP(Stream x) - If the transition to Move Data is selected, then the host shall generate a DP with the Stream ID = Stream x, and transition to the Move Data state. Upon transitioning to the Move Data state the host sets CStream to the value of Stream x. The DPP shall contain the first data payload for CStream. Typically the Move Data transition will be selected when the Stream that has just had its Endpoint Data modified is the same Stream as the one that the device last selected, e.g., Stream x = LCStream. The value of PP shall depend on the amount of Endpoint data the host has available. If the host has more than Max Packet Size Endpoint Data available for the Stream, then PP = 1 else PP = 0. This transition may be optionally be disabled in some hosts, and some Device Classes may not process this transition (e.g., Mass Storage UASP).

### 8.12.1.4.5.4 Start Stream

In the Start Stream state, the device has sent an ERDY proposing to the host that it initiate an OUT transfer for Stream n and it is waiting for the host to accept or reject the Stream selection.

DP(Stream n) - If the host has accepted the device's proposal for starting Stream n, then it shall transmit a DP with a Stream ID equal to Stream n, and transition to the Move Data state. Upon transitioning to the Move Data state the host sets CStream to the value of Stream n. The DPP shall contain the first data payload for CStream. The host shall accept a Stream proposal from a device if there is Endpoint Data available for the Stream.

DP(NoStream, PP = 0) - If the host rejects the device's proposal for starting Stream n, then it shall transmit a DP with a Stream ID equal to NoStream, and transition to the Start Stream End state. The DPP shall contain a zero-length data payload. The host shall reject a Stream proposal from a device if there is no Endpoint Data available to send for the Stream.

### 8.12.1.4.5.5 Start Stream End

In the Start Stream End state, the host has rejected a proposed Stream ID from the device because there was no Endpoint Data available for Stream n. Note, this state is entered when the host transmits a DP(NoStream) from the Start Stream state. If an error is detected in the DP data by the device, the device shall issue ACK(NoStream, NumP>0, Rty) packet, retrying until a DP(NoStream) is successfully received. The host may retransmit the DP(NoStream) and shall remain in the Start Stream End state until the device successfully receives the DP(NoStream) and returns an NRDY(NoStream), or the retries for the pipe are exhausted and the host halts the pipe. This case is not illustrated in the Figure above.

NRDY(NoStream) - If an NRDY with the Stream ID equal to NoStream is received, the host shall transition to the Idle state.

DPH(Deferred) - If a DPH with the Deferred (DF) bit set is received, the host shall transition to the Idle state. This packet is received when the link has transitioned to a U1 or U2 state while waiting

8-90

Protocol Layer

for a host response to the Start Stream request. Note that this transition can occur only if the tERDYTimeout has been exceeded. There is no DPP associated with a deferred DPH.

### 8.12.1.4.5.6 Move Data

In the Host OUT Move Data state, CStream is set to the same value at both ends of the pipe and the pipe may actively move data. The details of the bus transactions executed in the Move Data state and its exit conditions are defined in the Host OUT Move Data State Machine defined below.

![img-232.jpeg](img-232.jpeg)

Figure 8-46. Host OUT Move Data State Machine (HOMDSM)

The Host OUT Move Data State Machine (HOMDSM) is entered from the Start Stream or Idle states as described above. The entry into the HOMDSM immediately transitions to the OUTMvData Device state. The HOMDSM allows either the device to terminate the Move Data operation because it has exhausted its Function Buffer space associated with a Stream or the host to terminate the Move Data operation because it has exhausted its Endpoint Data associated with a Stream.

PP = 0 - Upon entry into the HOMDSM, if the host has only one packet of Endpoint Data available for the Stream then PP will equal 0 in the first DP sent to the Device, and it shall transition to the OUTMvData Device Terminate state.

8-91

Universal Serial Bus 3.1 Specification, Revision 1.0

PP = 1 - Upon entry into the HOMDSM, if the host has more than one packet of Endpoint Data available for the Stream then PP will equal 1 in the first DP sent to the Device, and it shall transition to the OUTMvData Device state.

The HOMDSM always exits to the Idle state. The Retry (Rty=1) flag shall never be set in a packet that causes a HOMDSM exit. A Stream pipe remains in the Move Data state during packet retries.

Note: The Stream ID value shall be CStream for all packets exchanged in the Move Data state, except the OUTMvData Device substate ERDY transition. For the identified substates, if a Stream ID value other than CStream is detected while in the HOMDSM the host should halt the endpoint.

### 8.12.1.4.5.7 OUTMvData Device

This state is initially entered from the Start Stream state or the Idle state. In this state the host is waiting for an ACK TP or a rejection of a HIMD from the device.

ACK(CStream, NumP>0) - If the host receives an ACK TP with NumP > 0, it shall transition to the OUTMvData Host state. This transition occurs when device has more Function Buffer space available for the stream. If the device detected an error on the last DP from the host, then the Retry (Rty) flag shall be set. If a Retry is requested, the host shall continue the current burst until all retries are exhausted or a good packet is transmitted. The host shall set LCStream = CStream. This action updates LCStream with the value of Stream x if the device accepts a HIMD, i.e., LCStream records the last Stream that was of interest to the device.

ACK(CStream, NumP=0) - If the host receives an ACK TP with NumP = 0, it shall transition to the Idle state, exiting the HOMDSM. This transition occurs when device has no more Function Buffer space available for the Stream, e.g., it is terminating the Move Data operation because the last DP exhausted its Function Buffer space. The host shall set LCStream = CStream. This action updates LCStream with the value of Stream x if the device accepts a HIMD, i.e., LCStream records the last Stream that was of interest to the device.

NRDY(CStream) - If the host receives an NRDY, it shall transition to the Idle state, exiting the HOMDSM. This transition may occur upon initial entry into the HOMDSM when the device rejects a HIMD, or during a Stream transfer due to unexpected internal device conditions where it wants to flow control CStream.

DPH(Deferred) - If the host receives a DPH with the Deferred (DF) flag set, then it shall transition to the Idle state, exiting the HOMDSM. This packet may be received when the link has transitioned to a U1 or U2 state and the host has attempted a HIMD or between bursts on the OUT pipe, if there is a lot of endpoint activity on other devices and the Ux Timeouts in the path to this device are set to short values. When this transition occurs the host will wait in the Idle state for an ERDY from the device to restart the stream. There is no DPP associated with a deferred DPH.

ERDY() - If an ERDY is received, a race condition has occurred. During this condition, the device is in the Start Stream state and the host is in the Move Data state. The host has entered the Move Data state as the result of a HIMD, at the same time that the device has attempted to initiate a Stream transfer, and their respective messages have passed each other on the link. To resolve this condition, the host shall remain in the OUTMvData Device state and wait for an ACK or an NRDY from the device.

8-92

Protocol Layer

### 8.12.1.4.5.8 OUTMvData Host

In this state the host has received an ACK TP from a device and the device has more Function Buffer space available for CStream. The host responds with a DP containing Endpoint Data associated with the Stream. The pipe will also wait in this state between bursts from the host. Note, that the DP retry process may span bursts.

DP(CStream, PP=1) - If more Endpoint Data is available for the Stream and the host is continuing the current burst to the device, then the host shall generate a DP with PP = 1, and transition to the OUTMvData Device state. The DPP shall contain a CStream data payload. If the Rty flag was set in the last ACK from the device, then the host shall resend the appropriate DP until all retries are exhausted or a good DP is acknowledged by the device.

DP(CStream, PP=0) - If the Endpoint Data available for the Stream is exhausted by transmitting this DP, then the host shall generate a DP with PP = 0, and transition to the OUTMvData Host Terminate state. The DPP shall contain a CStream data payload. This transition informs the device the host has exhausted its Endpoint Data for the Stream.

### 8.12.1.4.5.9 OUTMvData Host Terminate

In this state the host has just exhausted the Endpoint Data that it has available for CStream and sent the last DP for the Stream. The host is waiting for an acknowledgement for the last DP of the Stream.

ACK(CStream, NumP=0) - If the host receives and ACK TP with NumP = 0 and Rty = 0, then the host shall transition to the Idle state, exiting the HOMDSM. This transition occurs when the device has successfully received the last DP, and both the host and the device have exhausted their respective Endpoint Data and Function Buffer space at the same time.

ACK(CStream, NumP>0, No Rty) - If the host receives an ACK TP with NumP > 0, PP = 0, and Rty = 0, then the host shall transition to the Idle state, exiting the HOMDSM. This transition occurs when the device has successfully received the last DP, and the host has exhausted its Endpoint Data for the CStream, but the device still has more Function Buffer space available.

ACK(CStream, NumP>0, Rty) - If the host receives an ACK TP with NumP > 0 and Rty = 1, then the host shall transition the OUTMvData Host state and resend the appropriate DP. This transition occurs when the last packet received by the device was bad, and a Retry is required. The host shall continue the OUTMvData Host Terminate to OUTMvData Host loop until all retries are exhausted or a good DP is acknowledged by the device.

NRDY(CStream) - If the host receives an NRDY, it shall transition to the Idle state, exiting the HOMDSM. This transition may occur during a Stream transfer due to unexpected internal device conditions where it wants to flow control CStream.

DPH(Deferred) - If a DPH with the Deferred (DF) flag set is received, then the host shall transition to the Idle state, exiting the HOMDSM. This packet is received when the link had transitioned to the U1 or U2 state before the last DP was sent by the host. There is no DPP associated with a deferred DPH.

8-93

Universal Serial Bus 3.1 Specification, Revision 1.0

## 8.12.2 Control Transfers

Control transfers have a minimum of two transaction stages: Setup and Status. A control transfer may optionally contain a Data stage between the Setup and Status stages. The direction of the Data stage is indicated by the **bmRequestType** field which is present in the first byte of the data payload of the Setup packet. During the Setup stage, a SETUP transaction is used to transmit information to a control endpoint of the device. SETUP transactions are similar in format to a Bulk OUT transaction but have the **Setup** field set to one in the DPH along with the **Data Length** field set to eight. In addition, the Setup packet always uses a Data sequence number of zero. A device receiving a Setup packet shall respond as defined in Section 8.11.4. The **Direction** field shall be set to zero in TPs or DPs exchanged between the host and any control endpoint on the device regardless of the stage or direction of the control transfer. The **TT** field shall be set to Control by hosts and devices operating above Gen 1 speed; see Table 8-13.

If the endpoint successfully received the SETUP packet, it may return an ACK TP with the **NumP** field set to zero if it wants to flow control the control transfer. A device shall send an ERDY when it is ready to resume the control transfer (either the Data or Status stage). Note that an endpoint may return an ACK TP with the **NumP** field set to zero in response to a SETUP packet if it wants to flow control the control transfer. A device must send an ERDY to start the Data or Status stage. Note that the host may resume transactions to any endpoint – even if the endpoint had not returned an ERDY TP after returning a flow control response.

The Data stage, if present, of a control transfer consists of one or more IN or OUT transactions and follows the same protocol rules as bulk transfers except that the **Direction** field shall always be set to zero. The Data stage always starts with the sequence number set to zero. All the transactions in the Data stage shall be in the same direction (i.e., all INs or all OUTs). The maximum amount of data to be sent during the data stage and its direction are specified during the Setup stage. If the amount of data exceeds the data packet size, the data is sent in multiple data packets that carry the maximum packet size. Any remaining data is sent as a residual in the last data packet.

Note that all control endpoints only support a burst of one and hence the host can only send or receive one packet at a time to or from a control endpoint.

The Status stage of a control transfer is the last transaction in the sequence. The status stage transaction is identified by a TP with the SubType set to *STATUS*. In response to a STATUS TP with zero in the **Deferred** bit, a device shall send an NRDY, STALL, or ACK TP. If a device sends an NRDY TP, the host shall wait for it to send an ERDY TP for that control endpoint before sending another STATUS TP to the device. However, the host may resume transactions to any endpoint – even if the endpoint had not returned an ERDY TP after returning a flow control response. If the **Deferred** bit is set in the STATUS TP, then the device shall send an ERDY TP to indicate to the host that is ready to complete the status stage of the control transfer.

8-94

Protocol Layer

Figure 8-47 and Figure 8-48 show the transaction order, the data sequence number value, and the data packet types for control read and write sequences.

![img-233.jpeg](img-233.jpeg)

Figure 8-47. Control Read Sequence

8-95

Universal Serial Bus 3.1 Specification, Revision 1.0

![img-234.jpeg](img-234.jpeg)

Figure 8-48. Control Write Sequence

When a STALL TP is sent by a control endpoint in either the Data or Status stages of a control transfer, a STALL TP shall be returned on all succeeding accesses to that endpoint until a SETUP DP is received. An endpoint shall return an ACK TP when it receives a subsequent SETUP DP. For control endpoints, if an ACK TP is returned for the SETUP transaction, the host expects that the endpoint has automatically recovered from the condition that caused the STALL and the endpoint shall operate normally.

### 8.12.2.1 Reporting Status Results

During the Status stage, a device reports to the host the outcome of the previous Setup and Data stages of the transfer. Three possible results may be returned:

- The command sequence completed successfully.
- The command sequence failed to complete.
- The device is still busy completing the command.

Status reporting is always in the device-to-host direction. Table 8-31 summarizes the type of responses required for each. All Control transfers return status in the TP that is returned to the host in response to a STATUS TP transaction.

8-96

Protocol Layer

Note that even though the status reporting is always in the device-to-host direction, the STATUS TP shall be treated as an OUT transaction. A host may start performing IN transactions to another endpoint without waiting for the response for the STATUS TP.

Table 8-31. Status Stage Responses

[tbl-137.md](tbl-137.md)

The host shall send a STATUS TP to the control pipe to initiate the Status stage. The pipe's handshake response to this TP indicates the current status. An NRDY TP indicates that a device is still processing the command and that the device shall send an ERDY TP when it completes the command. An ACK TP indicates that a device has completed the command and is ready to accept a new command. A STALL TP indicates that a device has an error that prevents it from completing the command.

The NumP field of the ACK TP sent by a control endpoint on the device shall be set to zero. However, this is not considered a flow control condition for a control endpoint.

If during a Data stage a control pipe is sent more data or is requested to return more data than was indicated in the Setup stage, it shall return a STALL TP. If a control pipe returns a STALL TP during the Data stage, there shall not be a Status stage for that control transfer.

### 8.12.2.2 Variable-length Data Stage

A control pipe may have a variable-length data phase in which the host requests more data than is contained in the specified data structure. When all of the data structure is returned to the host, a device indicates that the Data stage is ended by returning a DP that has a payload less than the maximum packet size for that endpoint.

Note that if the amount of data in the data structure that is returned to the host is less than the amount requested by the host and is an exact multiple of maximum packet size then a control endpoint shall send a zero length DP to terminate the data stage.

### 8.12.2.3 STALL TPs Returned by Control Pipes

Control pipes have the unique ability to return a STALL TP due to problems in control transfers. If a device is unable to complete a command, it returns a STALL TP in the Data and/or Status stages of the control transfer. Unlike the case of a functional stall, protocol stall does not indicate an error with the device. The protocol STALL condition lasts until the receipt of the next SETUP DP, and the device shall return a STALL TP in response to any IN or OUT transaction on the pipe until the SETUP DP is received. In general, protocol stall indicates that the request or its parameters are not understood by a device and thus provides a mechanism for extending USB requests.

Devices do not support functional stall on a control pipe.

8-97

Universal Serial Bus 3.1 Specification, Revision 1.0

### 8.12.3 Bus Interval and Service Interval

For all periodic (interrupt and isochronous) endpoints, the interval at which an endpoint must be serviced is called a “Service Interval”. In this specification the term “Bus Interval” is used to refer to a one Microframe interval as defined in the USB 2.0 specification.

### 8.12.4 Interrupt Transactions

The interrupt transfer type is used for infrequent data transfers with a bounded service period. It supports a reliable data transport with guaranteed bounded latency. It offers guaranteed constant data rate as long as data is available. If an error is detected in the data delivered, the host is not required to retry the transaction in the same service interval. However, if a device is momentarily unable to transmit or receive the data (i.e., responds with an NRDY TP), the host shall resume transactions to an endpoint only after it receives an ERDY TP from that device for that endpoint.

Interrupt transactions are very similar to bulk transactions – but are limited to a burst of three DPs in each service interval. The TT field shall be set to Interrupt by hosts and devices operating above Gen 1 speed; see Table 8-13. The host shall continue to perform transactions to an interrupt endpoint at the agreed upon service interval as long as a device accepts data (in the case of OUT endpoints) or returns data (in the case of IN endpoints). The host is required to send an ACK TP for every DP successfully received in the service interval even if it is the last DP in that service interval. The final ACK TP shall acknowledge the last DP received and shall have the Number of Packets field set to zero. If an error occurs while performing transactions to an interrupt endpoint in the current service interval, then the host is not required to retry the transaction in the current service interval but the host shall retry the transaction in the next service interval at the latest.

#### 8.12.4.1 Interrupt IN Transactions

When the host wants to start an Interrupt IN transaction to an endpoint, it sends an ACK TP to the endpoint with the expected sequence number and the number of packets it expects to receive from the endpoint. If an interrupt endpoint is able to send data in response to the ACK TP from the host, it may send up to the number of packets requested by the host within the same service interval. The host shall respond to each of the DPs with an ACK TP indicating successful reception of the data or an ACK TP requesting the DP to be retried in case the DPP was corrupted.

Note that the host expects the first DP to have its sequence number set to zero when it starts the first transfer from a specific endpoint, after the endpoint has been initialized (via a Set Configuration or Set Interface or ClearFeature (ENDPOINT_HALT) command – refer to Chapter 9 for details on these commands).

An interrupt endpoint shall respond to TPs received from the host as described in Section 8.11.1. As long as a device returns data in response to the host sending ACK TPs and the transfer is not complete, the host shall continue to send ACK TPs to the device during every service interval for that endpoint.

The host shall stop performing transactions to an endpoint on the device when any of the following happen:

- The endpoint responds with an NRDY or STALL TP.
- All the data for the transfer is successfully received.
- The endpoint sets the EOB flag in the last DP sent to the host.

8-98

Protocol Layer

When an endpoint receives an ACK TP from the host and cannot respond by sending data, it shall send an NRDY (or STALL in case of an internal endpoint or device error) TP to the host. The host shall not perform any more transactions to the endpoint in subsequent service intervals.

The host shall resume interrupt transactions to an endpoint that responded with a flow control response in a previous service interval only after it receives an ERDY TP from the endpoint. This notifies the host about the endpoint's readiness to transmit data again. Once the host receives the ERDY TP, it shall send an IN request (via an ACK TP) to the endpoint no later than twice the service interval as determined by the value of the bInterval field in the interrupt endpoint descriptor. An interrupt endpoint responds by returning either the DP (the sequence number of the packet being one more than the sequence number of the last successful data sent) or, should it be unable to return data, an NRDY or a STALL TP.

If a device receives a deferred interrupt IN TP, and the device needs to send interrupt IN data, the device shall respond with an ERDY TP and keep its link in U0 until it receives the subsequent interrupt transaction from the host, or until tPingTimeout (refer to Table 8-36) time elapses.

As in the case of Bulk transactions, the sequence number is continually incremented with each packet sent by an interrupt endpoint. When the sequence number reaches 31 it wraps around to zero.

![img-235.jpeg](img-235.jpeg)

Figure 8-49. Host Sends Interrupt IN Transaction in Each Service Interval

8-99

Universal Serial Bus 3.1 Specification, Revision 1.0

![img-236.jpeg](img-236.jpeg)

Figure 8-50. Host Stops Servicing Interrupt IN Transaction Once NRDY is Received

![img-237.jpeg](img-237.jpeg)

Figure 8-51. Host Resumes IN Transaction after Device Sent ERDY

![img-238.jpeg](img-238.jpeg)

Figure 8-52. Endpoint Sends STALL TP

8-100

Protocol Layer

![img-239.jpeg](img-239.jpeg)

Figure 8-53. Host Detects Error in Data and Device Resends Data

Note: In Figure 8-53 the host retries the data packet received with an error in the same service interval. It is not required to do so and may retry the transaction in the next service interval.

### 8.12.4.2 Interrupt OUT Transactions

When the host wants to start an Interrupt OUT transaction to an endpoint, it sends the first DP with the expected sequence number. The host may send more packets to the endpoint in the same service interval if the endpoint supports a burst size greater than one. If an endpoint was able to receive that data from the host, it sends an ACK TP to acknowledge the successful receipt of data.

Note that the host always initializes the first DP sequence number to zero in the first transfer it performs to an endpoint after the endpoint is initialized (via a Set Configuration or Set Interface or ClearFeature (ENDPOINT_HALT) command – refer to Chapter 9 for details on these commands).

As long as a device returns ACK TPs in response to the host sending data packets and the transfer is not complete, the host shall continue to send data to the device during every service interval for that endpoint. A device shall acknowledge the successful reception of the DP or ask the host to retry the transaction if the data packet was corrupted.

In response to the OUT data sent by the host an interrupt endpoint shall respond as described in Section 8.11.3.

8-101

Universal Serial Bus 3.1 Specification, Revision 1.0

When an endpoint receives data from the host, and it cannot receive data momentarily, it shall send an NRDY (or STALL in case of an internal endpoint or device error) TP to the host. The host shall not perform any more transactions to the endpoint in subsequent service intervals.

A host shall only resume interrupt transactions to an endpoint that responded with a flow control response after it receives an ERDY TP from that endpoint. This notifies the host about the endpoint's readiness to receive data again. Once the host receives an ERDY TP, the host shall transmit the data packet to the endpoint no later than twice the service interval as determined by the value of the bInterval field in the interrupt endpoint descriptor for that endpoint.

If a device receives a deferred interrupt OUT DPH, and the device needs to receive interrupt OUT data, the device shall respond with an ERDY TP and keep its link in U0 until it receives the subsequent interrupt transaction from the host, or until tPingTimeout (see Table 8-36) elapses.

As in the case of Bulk transactions, the sequence number is continually incremented with each packet sent by host. When the sequence number reaches 31 it wraps around to zero.

![img-240.jpeg](img-240.jpeg)

Figure 8-54. Host Sends Interrupt OUT Transaction in Each Service Interval

8-102

Protocol Layer

![img-241.jpeg](img-241.jpeg)

Figure 8-55. Host Stops Servicing Interrupt OUT Transaction Once NRDY is Received

![img-242.jpeg](img-242.jpeg)

Figure 8-56. Host Resumes Sending Interrupt OUT Transaction After Device Sent ERDY

8-103

Universal Serial Bus 3.1 Specification, Revision 1.0

![img-243.jpeg](img-243.jpeg)

Figure 8-57. Device Detects Error in Data and Host Resends Data

Note: In Figure 8-57 the host retries the data packet received with an error in the same service interval. It is not required to do so and may retry the transaction in the next service interval.

![img-244.jpeg](img-244.jpeg)

Figure 8-58. Endpoint Sends STALL TP

### 8.12.5 Host Timing Information

USB 3.0 host controllers do not broadcast regular start of frame (SOF) packets to all devices on a Enhanced SuperSpeed USB link. Host timing information is sent by the host via isochronous timestamp packets (ITP) when the root port link is in U0 around a bus interval boundary. Hubs forward isochronous timestamp packets (with any necessary modifications as described in Section 10.9.4.4) to any downstream port with a link in U0 and which has completed Port Configuration. The host shall provide isochronous timestamps based on a non-spread clock. Devices are responsible for keeping the link in U0 around bus interval boundaries when isochronous timestamps are required for device operation. A device should never keep the link in U0 for the sole purpose of receiving timestamps unless the timestamps are required for device operation.

Note: A device will receive an isochronous timestamp if its link is in U0 around a bus interval boundary. This means that devices without any isochronous endpoints or need for synchronization may discard isochronous timestamp packets without negative side effects.

8-104

Protocol Layer

The timing information is sent in an isochronous timestamp packet around each bus interval boundary and communicates the current bus interval and the time from the start of the timestamp packet to the previous bus interval. Isochronous endpoints request a service interval of one Bus Interval * 2ⁿ μs, where n is an integer value from 0 to 15 inclusive.

ITPs communicate timing information such that all isochronous endpoints receive the same bus interval boundaries. The host shall keep service interval boundaries aligned for all endpoints at all times unless the host link enters U3. ITPs issued after the host root port link exits U3 may be aligned with boundaries from before the host root port link entered U3. The host shall begin transmitting ITPs within IsochronousTimestampStart from when the host root port's link enters U0 after the link was in U3. Figure 8-59 shows an example with an active isochronous IN endpoint and isochronous OUT endpoint connected below the same USB 3.0 host controller. The service interval for the isochronous IN endpoint is X and the service interval for the isochronous OUT endpoint is 2X. Note that the host is free to schedule an isochronous IN (via an ACK TP) or isochronous OUT data anywhere within the appropriate service interval. A device will detect the start of new service interval by detecting the rollover of least significant bits in the Bus Interval Counter. The number of bits that need to be monitored for rollover is defined by bInterval. For example, if service interval is equal to two Bus Intervals, the beginning of the service interval is defined by the transition of the least significant bit of the Bus Interval Counter to '0'. If service interval is 4 Bus Intervals, the service interval is defined by the transition of the least significant two bits of the Bus Interval Counter to '0', and so on.

If bInterval is one, a device will detect the start of the service interval when the value of the least significant bit of Bus Interval Counter changes.

A device shall not assume that transactions occur at the same location within each service interval. The host shall schedule isochronous transactions such that they do not cross service interval boundaries.

8-105

Universal Serial Bus 3.1 Specification, Revision 1.0

![img-245.jpeg](img-245.jpeg)

Figure 8-59. Multiple Active Isochronous Endpoints with Aligned Service Interval Boundaries

### 8.12.6 Isochronous Transactions

The following sections define the Isochronous transaction protocols for SuperSpeed and SuperSpeedPlus devices. The SuperSpeedPlus protocol relaxes restrictions on how a host may schedule Isochronous transactions to/from a SuperSpeedPlus device and adds the ability to pipeline transaction requests to an endpoint in order to improve the efficiency of the bus.

### 8.12.6.1 Enhanced SuperSpeed Isochronous Transactions

IN isochronous transactions are shown in Figure 8-60 and OUT isochronous transactions are shown in Figure 8-61. For INs, the host issues an ACK TP followed by a data phase in which the endpoint transmits data for INs. For OUTs, the host simply transmits data when there is data to be sent in the current service interval. Isochronous transactions do not support retry capability. The TT field shall be set to Isochronous by hosts and peripheral devices operating above Gen 1 speed; see Table 8-13.

8-106

Protocol Layer

![img-246.jpeg](img-246.jpeg)

Figure 8-60. Enhanced SuperSpeed Isochronous IN Transaction Format

![img-247.jpeg](img-247.jpeg)

Figure 8-61. Enhanced SuperSpeed Isochronous OUT Transaction Format

The first DP or ACK TP in each service interval shall start with the sequence number set to 0.

8-107

Universal Serial Bus 3.1 Specification, Revision 1.0

For isochronous transactions that include multiple data packets in a service interval the sequence number is increased by one for each subsequent DP. The DP after sequence number 31 uses a sequence number of zero.

For IN transactions, the current ACK TP Seq Num field shall be set to the value of the sum of the Seq Num and NumP fields in the previous ACK TP as long as all the data for the service interval has not been returned. The equation used to set the current sequence is given below:

$$Seq Num[i + 1] = Seq Num[i] + NumP[i]$$

A device with an isochronous endpoint shall be able to send or receive the number of packets indicated in its endpoint and endpoint companion descriptors per service interval. The host shall be able to accept and send up to 48 DPs per service interval for devices operating at Gen 1 speed and up to 96 DPs for devices operating at Gen 2 speed.

The last packet in the service interval shall be sent with the lpf field set to 1 and can be less than or equal to MaxPacketSize bytes. Each packet except the last packet in the service interval shall be sent with the lpf field set to 0 and shall be equal to MaxPacketSize bytes. If there is no data to send to an isochronous OUT endpoint during a service interval, the host does not send anything during the interval. If a device with an isochronous IN endpoint does not have data to send when an isochronous IN ACK TP is received from the host, it shall send a zero length data packet.

Figure 8-62 and Figure 8-63 show sample isochronous IN and OUT transactions for endpoints that have requested 2000 bytes of bandwidth per service interval (i.e., no more than two packets can be sent or received each service interval).

If the host is not able to send isochronous OUT data during the specified interval due to an error condition, the host discards the data and notifies host software of the error. If the host is not able to send an isochronous ACK TP during the specified service interval due to an error condition, the host notifies host software of the error.

8-108

Protocol Layer

![img-248.jpeg](img-248.jpeg)

Figure 8-62. Sample Enhanced SuperSpeed Isochronous IN Transaction

8-109

Universal Serial Bus 3.1 Specification, Revision 1.0

![img-249.jpeg](img-249.jpeg)

Figure 8-63. Sample Enhanced SuperSpeed Isochronous OUT Transaction

8-110

Protocol Layer

![img-250.jpeg](img-250.jpeg)

Figure 8-64. Sample Enhanced SuperSpeed Isochronous IN Transaction

8-111

Universal Serial Bus 3.1 Specification, Revision 1.0

![img-251.jpeg](img-251.jpeg)

Figure 8-65. Sample Enhanced SuperSpeed Isochronous OUT Transaction

### 8.12.6.1.1 Smart Isochronous Scheduling Protocol

Figure 8-66 and Figure 8-67 show sample isochronous IN and OUT transactions with smart Isochronous scheduling to endpoints that have service intervals of 8. In the isochronous IN example below the host is only sending one ACK TP with the SSI and DBI field set to non-zero values when asking for data from the endpoint. It should be noted that a host may send multiple

8-112

Protocol Layer

ACK TPs with only the last ACK TP in the current bus interval having the SSI and DBI fields set to non-zero values.

The SSI, WPA, DBI and NBI fields (described in Table 8-13) are provided in addition to the lpf to give devices more information about when the host plans to transfer isochronous data thus allowing them to more aggressively manage their upstream link. The DBI is used to tell the device that the host has no more data to transfer during the current bus interval. The WPA field, when set to one, informs the device that the host will send a PING TP to the device before it initiates a data transfer on the endpoint again.

The NBI value provides the device additional information (when DBI is set to one and WPA is set to zero) that it may use to more aggressively manage its upstream port. The value is used to determine the bus interval number (see Table 8-13) that the host will initiate another data transfer on the endpoint. In this case, the host will not be required to send a PING TP before it resumes transfers to the endpoint; it is the device's responsibility to manage its upstream port's link accordingly.

Note that the SSI and related fields are only valid and may only be used by a host to inform a device about the manner in which it will service a particular isochronous endpoint on a device within a service interval. A host is always required to send a PING and wait for a PING_RESPONSE before servicing an isochronous endpoint before the start of each service interval.

8-113

Universal Serial Bus 3.1 Specification, Revision 1.0

![img-252.jpeg](img-252.jpeg)

Figure 8-66. Sample Smart Enhanced SuperSpeed Isochronous IN Transaction

8-114

Protocol Layer

![img-253.jpeg](img-253.jpeg)

Figure 8-67. Sample Smart Enhanced SuperSpeed Isochronous OUT Transaction

8-115

Universal Serial Bus 3.1 Specification, Revision 1.0

### 8.12.6.2 Host Flexibility in Performing SuperSpeed Isochronous Transactions

A host targeting an endpoint on a SuperSpeed bus instance shall adhere to the requirements in this section.

The host is allowed some flexibility in performing isochronous service during a service interval. The host may transfer all the DPs to or from an endpoint as a single isochronous burst transaction or it may split the transfer into smaller bursts of two, four, or eight DPs followed by a final isochronous burst with the remaining DPs for that service interval. The host shall not perform isochronous transactions in any other way. For isochronous endpoints that have a multiplier value greater than one, these rules apply to the burst transactions associated with each multiplier value separately. A device shall support all possible host burst transactions allowed by these rules. For example, if an isochronous IN endpoint requests a maximum number of packets in a burst of 11 and the host has 11 packets to receive from the endpoint during a service interval there are four possible ways the host could perform the transaction:

- Request a single burst of 11 packets
- Request a burst of eight followed by a burst of three
- Request two bursts of four followed by a burst of three
- Request five bursts of two followed by a burst of one
- Request 11 bursts of one.

Taking the above example a step further, if the isochronous IN endpoint requests a maximum number of packets in a burst of 11 and a Mult of 2 (in essence requesting three bursts of 11) and the host has buffer space to receive 33 packets from the endpoint during a service interval, then the host can use any combination of the above mentioned options to transfer the three sets of 11 packets to the endpoint.

### 8.12.6.3 SuperSpeedPlus Isochronous Transactions

#### 8.12.6.3.1 Pipelined Isochronous IN Transactions

SuperSpeedPlus hosts may perform Isochronous transactions to an Enhanced SuperSpeed Isochronous endpoint following the rules outlined in Section 8.12.6.1. However, when performing IN transactions to SuperSpeedPlus endpoints, a SuperSpeedPlus host is allowed to send multiple IN ACK TPs requesting more data from the endpoint before the endpoint has returned all the data previously requested. The host shall not request more outstanding DPs than the max burst size reported in the endpoints' descriptors.

If a SuperSpeedPlus endpoint reports a Max Burst Size of 'M' in its descriptors then a SuperSpeedPlus host can send the following sequence of IN ACK TPs to the device without waiting for the device to return all the DPs asked for in the initial IN ACK TP:

8-116

Protocol Layer

Table 8-32. ACK TP and DPs for Pipelined Isochronous IN Transactions

[tbl-138.md](tbl-138.md)

As can be see in Table 8-32 the Seq Num field is updated in the same manner as it is SuperSpeedPlus Isochronous IN transactions however, they are "Pipelined". Pipelined refers to the ability of SuperSpeedPlus hosts to send the next IN ACK TP before the first one has completed. A SuperSpeedPlus host may continue to send Pipelined IN ACK TPs with the following three caveats:

- The number of outstanding packets requested from the endpoint cannot be greater than the Max Burst Size of the endpoint.
- The number of outstanding packets requested from the endpoint cannot exceed the total amount of data expected from the endpoint in that Service Interval.
- The SuperSpeedPlus host shall stop sending pipelined IN ACK TPs for the current service interval once it receives an end of data indication from the endpoint.

If at any time the endpoint returns a DP with the lpf bit set, the SuperSpeedPlus host shall not expect any more packets from the endpoint for this SI. The host shall treat this condition as the termination of Isochronous transactions for this SI for this endpoint. The endpoint shall discard any additional IN ACK TPs it had received or receives in this SI.

8-117

Universal Serial Bus 3.1 Specification, Revision 1.0

# SSP ISOC IN

![img-254.jpeg](img-254.jpeg)

Figure 8-68. Sample Pipeline Isochronous IN Transactions

8-118

Protocol Layer

### 8.12.6.4 Host Flexibility in Performing SuperSpeedPlus Isochronous Transactions

A SuperSpeedPlus host is allowed to perform Isochronous transactions without the restrictions mentioned in Section 8.12.6.2 when performing transfers to/from a SuperSpeedPlus Isochronous endpoint. The SuperSpeedPlus host may transfer all the DPs to or from an endpoint in bursts of any size as long as the number of outstanding packets is less than or equal to the max burst size advertised by the endpoint in its descriptors.

A device shall support all possible pipelined Isochronous IN transactions allowed by these rules.

### 8.12.6.5 Device Response to Isochronous IN Transactions

Table 8-33 lists the possible responses a device may make in response to an ACK TP. An ACK TP is considered to be invalid if any of the following conditions exist:

- It has an incorrect Device Address
- Its endpoint number and direction does not refer to an endpoint that is part of the current configuration
- It does not have the expected sequence number
- It has the deferred bit set in it
- Its TT does not match the endpoint type (for devices not operating at Gen 1 speed).

Table 8-33. Device Responses to Isochronous IN Transactions

[tbl-139.md](tbl-139.md)

### 8.12.6.6 Host Processing of Isochronous IN Transactions

Table 8-34 lists the host processing of data from an IN transaction. The host never returns a response to isochronous IN data received. In Table 8-34, DP Error may be due to one or more of the following:

- CRC-32 incorrect
- DPP aborted
- DPP missing
- DPH TT is not set to Isochronous (from a device not operating at Gen 1 speed)
- Data length in the DPH does not match the actual data payload length.

8-119

Universal Serial Bus 3.1 Specification, Revision 1.0

If the host receives a corrupted data packet, it discards the remaining data in the current service interval and informs host software of the error.

Table 8-34. Host Responses to IN Transactions

[tbl-140.md](tbl-140.md)

### 8.12.6.7 Device Response to an Isochronous OUT Data Packet

Table 8-35 lists the device processing of data from an OUT data packet. A device never returns a TP in response. In Table 8-35, DP Error may be due to one or more of the following:

- CRC-32 incorrect
- DPP aborted
- DPP missing
- DPH TT is not set to Isochmous (for a device not operating at Gen 1 speed)
- Data length in the DPH does not match the actual data payload length
- Deferred bit set in the DPH

Table 8-35. Device Responses to OUT Data Packets

[tbl-141.md](tbl-141.md)

8-120

Protocol Layer

### 8.13 Timing Parameters

Table 8-36 lists the minimum and/or maximum times a device shall adhere to when responding to various types of packets it receives. It also lists the default and minimum times a device may set in Latency Tolerance messages as well as the minimum time after receipt of certain TPs and when it can initiate a U1 or U2 entry. In addition, it lists the maximum time between DPs a device must adhere to while bursting.

All txxxResponse (e.g., tNRDYResponse), tMaxBurstInterval and tGen2MaxBurstInterval times are all timings that a host/device shall meet when the host/device has nothing else to send on its downstream/upstream link.

Table 8-36. Timing Parameters

[tbl-142.md](tbl-142.md)

8-121

Universal Serial Bus 3.1 Specification, Revision 1.0

[tbl-143.md](tbl-143.md)

8-122

Protocol Layer

[tbl-144.md](tbl-144.md)

¹ (tIsochTimestampGranularity/4096)

² This value was chosen to be greater than the link Pending HP Credit timeout (see Chapter 7)

8-123

Universal Serial Bus 3.1 Specification, Revision 1.0

8-124

# 9 Device Framework

A device may be divided into three layers:

- The bottom layer is a bus interface that transmits and receives packets.
- The middle layer handles routing data between the bus interface and various endpoints on the device. As in USB 2.0, the endpoint is the ultimate consumer or provider of data. It may be thought of as a source or sink for data. The characteristics of an endpoint; e.g., the endpoint's transfer type, the maximum payload (MaxPacketSize), and the number of packets (Burst Size) it can receive or send at a time are described in the endpoint's descriptor.
- The top layer is the functionality provided by the serial bus device, for instance, a mouse or video camera interface.

This chapter describes the common attributes and operations of the middle layer of a device. These attributes and operations are used by the function-specific portions of the device to communicate through the bus interface and ultimately with the host.

## 9.1 USB Device States

A device has several possible states. Some of these states are visible to the USB and the host, while others are internal to the device. This section describes those states.

### 9.1.1 Visible Device States

This section describes device states that are externally visible (see Figure 9-1). Table 9-1 summarizes the visible device states.

NOTE

Devices perform a reset operation in response to reset signaling on the upstream facing port. When reset signaling has completed, the device is reset. The reset signaling depends on the link state. Refer to Section 7.3 for details.

9-1

Universal Serial Bus 3.1 Specification, Revision 1.0

![img-255.jpeg](img-255.jpeg)

¹ Refer to Note 2 in Figure 10-26 Peripheral Device Upstream Port State Machine.

² Refer to sections 10.16.2.6 and 10.16.2.7 for the conditions that cause this transition.

Figure 9-1. Peripheral State Diagram and Hub State Diagram (Enhanced SuperSpeed Portion Only)

Figure 9-1, above, is a combined state diagram for both peripherals and hubs. Note that a USB Hub has two discrete state diagrams, one for the Enhanced SuperSpeed portion shown in Figure 9-1 and another for the non-SuperSpeed portion that may be found in Figure 9-1 in the USB 2.0 Specification.

9-2

Device Framework

**Table 9-1. Visible Enhanced SuperSpeed Device States**

[tbl-145.md](tbl-145.md)

$^{1}$Suspended from the Default, Address, or Configured state.

9-3

Universal Serial Bus 3.1 Specification, Revision 1.0

### 9.1.1.1 Attached

A device may be attached or detached from the USB. The state of a device when it is detached from the USB is not defined by this specification. This specification only addresses required operations and attributes once the device is attached.

### 9.1.1.2 Powered

Devices may obtain power from an external source and/or from the USB through the hub to which they are attached. Externally powered devices are termed self-powered. Although self-powered devices may already be powered before they are attached to the USB, they are not considered to be in the Powered state until they are attached to the USB and VBUS is applied to the device.

A device may support both self-powered and bus-powered configurations. Some device configurations support either power source. Other device configurations may be available only if the device is self-powered. Devices report their power source capability through the configuration descriptor. The current power source is reported as part of a device’s status. Devices may change their power source at any time, e.g., from self- to bus-powered. If a configuration is capable of supporting both power modes, the power maximum reported for that configuration is the maximum the device will draw from VBUS in either mode. The device shall observe this maximum, regardless of its mode. If a configuration supports only one power mode and the power source of the device changes, the device will lose its current configuration and address and return to the Powered state. If a device operating at Gen X speed is self-powered and its current configuration requires more than 150 mA, then if the device switches to being bus-powered, it shall return to the Powered state. Self-powered hubs that use VBUS to power the Hub Controller are allowed to remain in the Configured state if local power is lost. Note that the maximum power draw for a device operating at a USB 2.0 speed is governed by the limits set in the USB 2.0 specification.

A hub port shall be powered in order to detect port status changes, including attach and detach. Bus-powered hubs do not provide any downstream power until they are configured, at which point they will provide power as allowed by their configuration and power source. A device shall be able to be addressed within a specified time period from when power is initially applied (refer to Chapter 7). After an attachment to a port has been detected, the host may reset the port, which will also reset the device attached to the port.

While in the Powered state, a hub or peripheral device may be in one of two substates: “Far-end Receiver Termination” or “Link Training”.

#### 9.1.1.2.1 Far-end Receiver Termination Substate

A peripheral device shall transition to a USB 2.0 Device State as per the conditions defined in Note 2 of Figure 10-26 if Far-end Receiver Terminations are not detected.

A hub shall remain in the Far-end Receiver Termination substate if Far-end Receiver Terminations are not detected.

If Far-end Receiver Terminations are detected, a hub or peripheral device shall transition to the Link Training substate.

9-4

Device Framework

### 9.1.1.2.2 Link Training Substate

A peripheral device shall transition to USB 2.0 Device States if Link Training fails.

A hub shall transition to the Far-end Receiver Termination substate if Link Training fails.

If Link Training is successful, a hub or peripheral device shall transition to the Default state.

### 9.1.1.3 Default

When operating at Gen X speed, after the device has been powered, it shall not respond to any bus transactions until its link has successfully trained. The device is then addressable at the default address.

An Enhanced SuperSpeed device determines whether it will operate at Gen X speed as a part of the connection process (see the Device Connection State Diagram in Chapter 10 for more details).

A USB device shall reset successfully at one of the supported USB 2.0 speeds when in an USB 2.0 only electrical environment. After the device is successfully reset, the device shall also respond successfully to device and configuration descriptor requests and return appropriate information according to the requirements laid out in the USB 2.0 specification. The device may or may not be able to support its intended functionality when operating in the USB 2.0 mode.

A hub or peripheral device shall transition to the Powered::Far-end Receiver Termination substate if the hub or peripheral device receives a Warm Reset or the hub or device initiates a speed change or a speed change is initiated on the hub or peripheral device's upstream facing port.

A peripheral device shall transition to a USB 2.0 Device State if Port Configuration fails. Refer to Section 8.4.6

A hub shall transition to the Attached state if Port Configuration fails. Note that it is necessary to physically remove and reapply VBUS to transition a hub out of the Attached state.

### 9.1.1.4 Address

All devices use the default address when initially powered, or after the device has been reset. Each device is assigned a unique address by the host after reset. A device maintains its assigned address while suspended.

A device responds to requests on its default pipe whether the device is currently assigned a unique address or is using the default address.

A hub or peripheral device shall transition to the Powered::Far-end Receiver Termination substate if the hub or peripheral device receives a Warm Reset or the hub or device initiates a speed change or a speed change is initiated on the hub or peripheral device's upstream facing port.

### 9.1.1.5 Configured

Before a device's function may be used, the device shall be configured. From the device's perspective, configuration involves correctly processing a SetConfiguration() request with a non-zero configuration value. Configuring a device or changing an alternate setting causes all of the status and configuration values associated with all the endpoints in the affected interfaces to be set to their default values. This includes resetting the sequence numbers of any endpoint in the

9-5

Universal Serial Bus 3.1 Specification, Revision 1.0

affected interfaces to zero. On initial entry into the configured state a device shall default to the fully functional D0 State.

A hub or peripheral device shall transition to the Powered::Far-end Receiver Termination substate if the hub or peripheral device receives a Warm Reset or the hub or device initiates a speed change or a speed change is initiated on the hub or peripheral device's upstream facing port.

### 9.1.1.6 Suspended

In order to conserve power, devices automatically enter the Suspended state (one of Suspended Default, Address, or Configured) when they observe that their upstream link is being driven to the U3 state (refer to Section 7.2.4.2.4). Refer to Section 9.2.5.2 for the state that a device maintains while it is suspended.

Attached devices shall be prepared to suspend at any time from the Default, Address, or Configured states. A device shall enter the Suspended state when the hub port it is attached to is set to go into U3. This is referred to as selective suspend.

A device exits suspend mode when it observes wake-up signaling (refer to Section 6.9.1 and Section 7.5.9) on its upstream port. A device may also request the host to exit suspend mode or selective suspend by driving resume signaling (refer to Section 6.9.1 and Section 7.5.9) and sending a Function Wake Notification (refer to Section 8.5.6) on its upstream link to indicate remote wakeup. The ability of a device to signal remote wakeup is optional. If a device is capable of remote wakeup, the device shall support the ability of the host to enable and disable this capability. When the device is reset, remote wakeup shall be disabled. Refer to Section 9.2.5 for more information.

### 9.1.1.7 Error

This state is entered if the device is in the Default, Address, Configured, or Suspended state and its link exits the Recovery state due to a timeout. A Warm Reset or removal of Far-end Receiver Terminations shall recover from this error condition and transition the device to the Powered::Far-end Receiver Termination substate.

### 9.1.2 Bus Enumeration

When a device is attached to or removed from the USB, the host uses a process known as bus enumeration to identify and manage the device state changes necessary. When a device is attached to a powered port the following actions are taken (note, these actions apply whether the attached device is a peripheral device or hub device):

1. The hub to which the device is now attached informs the host of the event via a reply on its status change pipe (refer to Section 10.13.1). At this point, the device has been reset, is in the Default state and the port to which it is attached is enabled and ready to respond to control transfer requests on the default control pipe.
2. The host determines the exact nature of the change by querying the hub.
3. Now that the host knows the port to which the new device has been attached, the host then may reset the device again if it wishes, but it is not required to do so.
4. If the host resets the port, the hub performs the required reset processing for that port (refer to Section 10.3.1.6). When the reset is completed, the port will be back in the enabled state.

9-6

Device Framework

5. The device is now in the Default state and can draw no more than 150 mA from VBUS. All of its registers and state have been reset and it answers to the default address.
6. The host assigns a unique address to the device, moving the device to the Address state.
7. Before the device receives a unique address, its default control pipe is still accessible via the default address. The host reads the device descriptor to determine the actual maximum data payload size that can be used by this device's default pipe.
8. The host shall set the isochronous delay to inform the device of the delay from the time a host transmits a packet to the time it is received by the device.
9. The host shall inform the device of the system exit latency using the Set SEL request. Device shall accept a Set SEL request whether it is LTM capable or not and whether LTM is enabled or not.
10. The host reads the configuration information from the device by reading each configuration from zero to n-1, where n is the number of configurations. This process may take several milliseconds to complete.
11. Any time after this, the host can set the U1/U2 timeout for the downstream port on which the device is connected using the Set Port Feature (PORT_U1_TIMEOUT/PORT_U2_TIMEOUT).
12. Based on the configuration information and how the device will be used, the host assigns a configuration value to the device. The device is now in the Configured state and all of the endpoints in this configuration have taken on their described characteristics. The device may now draw the amount of VBUS power described in its descriptor for the selected configuration. From the device's point of view, it is now ready for use.

When the device is detached, the hub again sends a notification to the host. Detaching a device disables the port to which it had been attached and the port moves into the Disconnected state (refer to Section 10.3.1.2). Upon receiving the detach notification, the host will update its local topological information.

## 9.2 Generic Device Operations

All devices support a common set of operations. This section describes those operations.

### 9.2.1 Dynamic Attachment and Removal

Devices may be attached or detached at any time. The hub provides the attachment point or downstream port and is responsible for reporting any change in the state of the port.

The hub resets and enables the hub downstream port where the device is attached upon detection of an attachment, which also has the effect of resetting the device. A reset device has the following characteristics:

- Its USB address is set to zero (the default USB address)
- It is not configured
- It is not suspended

When a device is removed from a hub port, the hub disables the port where the device was attached, the port moves into the DSPORT.Disconnected state (refer to Section 10.3.1.2) and notifies the host of the removal.

9-7

Universal Serial Bus 3.1 Specification, Revision 1.0

### 9.2.2 Address Assignment

When a device is attached, the host is responsible for assigning a unique address to the device. Before assigning an address, the host may explicitly reset the device, however; note that the device implicitly gets reset during the connection process before the host is notified of a device being attached to the port.

### 9.2.3 Configuration

A device shall be configured before its function(s) may be used. The host is responsible for configuring a device. The host typically requests configuration information from the device to determine its capabilities.

As part of the configuration process, the host sets the device configuration and, where necessary, selects the appropriate alternate settings for the interfaces.

Within a single configuration, a device may support multiple interfaces. An interface is a related set of endpoints that present a single feature or function of the device to the host. The protocol used to communicate with this related set of endpoints and the purpose of each endpoint within the interface may be specified as part of a device class or vendor-specific definition.

In addition, an interface within a configuration may have alternate settings that redefine the number or characteristics of the associated endpoints. If this is the case, the device shall support the GetInterface() request to report the current alternate setting for the specified interface and SetInterface() request to select the alternate setting for the specified interface.

Within each configuration, each interface descriptor contains fields that identify the interface number and the alternate setting. Interfaces are numbered from zero to one less than the number of concurrent interfaces supported by the configuration. Alternate settings range from zero to one less than the number of alternate settings for a specific interface. The default setting when a device is initially configured is alternate setting zero.

In support of adaptive device drivers that are capable of managing a related group of devices, the device and interface descriptors contain Class, SubClass, and Protocol fields. These fields are used to identify the function(s) provided by a device and the protocols used to communicate with the function(s) on the device. A class code is assigned to a group of related devices that has been characterized as a part of a USB Class Specification. A class of devices may be further subdivided into subclasses and, within a class or subclass, a protocol code may define how the host software communicates with the device.

Note: The assignment of class, subclass, and protocol codes shall be coordinated but is beyond the scope of this specification.

### 9.2.4 Data Transfer

Data may be transferred between an endpoint within a device and the host in one of four ways. Refer to Chapter 4 for the definition of the four types of transfers. An endpoint number may be used for different types of data transfers in different alternate settings. However, once an alternate setting is selected (including the default setting of an interface), a device endpoint uses only one data transfer method until a different alternate setting is selected.

9-8

Device Framework

### 9.2.5 Power Management

Power management on devices involves the issues described in the following sections.

#### 9.2.5.1 Power Budgeting

USB bus power is a limited resource. During device enumeration, a host evaluates a device's power requirements. If the power requirements of a particular configuration exceed the power available to the device, host software shall not select that configuration.

Devices shall limit the power they consume from VBUS to one unit load or less until configured. When operating at Gen X speed, 150 mA equals one unit load. Suspended devices, whether configured or not, shall limit their bus power consumption as to the suspend mode power requirements in the USB 2.0 specification. Depending on the power capabilities of the port to which the device is attached, an Enhanced SuperSpeed device operating at Gen X speed may be able to draw up to six unit loads from VBUS after configuration. The amount of current draw for Enhanced SuperSpeed devices are increased to 150 mA for low-power devices and 900 mA for high-power devices when operating at Gen X speed.

Device power management is comprised of Device Suspend and Function Suspend. Device Suspend refers to a device-wide state that is entered when its upstream link is placed in U3. Function Suspend refers to a state of an individual function within a device. Suspending a device with more than one function effectively suspends all the functions within the device.

Note that placing all functions in the device into Function Suspend does not suspend the device. A device is suspended only when its upstream link is placed in U3.

#### 9.2.5.2 Changing Device Suspend State

Device Suspend is entered and exited intrinsically as part of the suspend entry and exit processes (refer to Section 9.1.1.6). The minimum device state information that shall be maintained through the duration of each Suspended USB Device State is listed in Table 9-2.

9-9

Universal Serial Bus 3.1 Specification, Revision 1.0

Table 9-2. Preserved USB Suspend State Parameters

[tbl-146.md](tbl-146.md)

$^{1}$ No parameters other than HSN, are preserved in the Default Suspended USB Device State.

$^{2}$ "Yes" indicates a parameter that shall be preserved in the respective Suspended USB Device State.

Some additional Class specific device state information may also be retained during suspend.

A device shall send a Function Wake Notification after driving resume signaling (refer to Section 6.9.1 and Section 7.5.9). If the device has not been accessed for longer than tNotification (refer to Section 8.13) since sending the last Function Wake Notification, the device shall send the Function Wake Notification again until it has been accessed.

Device classes may require additional information to be retained during suspend, beyond what is identified in this specification and is beyond the scope of this specification. Devices can optionally remove power from circuitry that is not needed while in suspend.

### 9.2.5.3 Function Suspend

The Function Suspend state is a reduced power state associated with an individual function. The function may or may not be part of a composite device.

A function may be placed into Function Suspend independently of other functions within a composite device. A device may be transitioned into Device Suspend regardless of the Function

9-10

Device Framework

Suspend state of any function within the device. Function Suspend state is retained while in Device Suspend and throughout the Device Suspend entry and exit processes.

### 9.2.5.4 Changing Function Suspend State

Functions are placed into Function Suspend using the FUNCTION_SUSPEND feature selector (see Table 9-7). The FUNCTION_SUSPEND feature selector also controls whether the function may initiate a function remote wakeup. Whether a function is capable of initiating a Function Remote Wake is determined by the status returned when the first interface in that function is queried using a Get Status command (refer to Section 9.4.5).

Remote wakeup (i.e., wakeup from a Device Suspend state) is enabled when any function within a device is enabled for function remote wakeup (note the distinction between “function remote wake” and “remote wake”). The DEVICE_REMOTE_WAKEUP feature selector is ignored and not used by Enhanced SuperSpeed devices.

A function may signal that it wants to exit from Function Suspend by sending a Function Wake Notification to the host if it is enabled for function remote wakeup. This applies to single function devices as well as multiple function (i.e., composite) devices. If the link is in a non-U0 state, then the device must transition the link to U0 prior to sending the remote wake message. If a remote wake event occurs in multiple functions, each function shall send a Function Wake Notification. If the function has not been accessed for longer than tNotification (refer to Section 8.13) since sending the last Function Wake Notification, the function shall send the Function Wake Notification again until it has been accessed.

When all functions within a device are in Function Suspend and the PORT_U2_TIMEOUT field (refer to Section 10.16.2.10) is programmed to 0xFF, the device shall initiate U2 after 10 ms of link inactivity.

### 9.2.6 Request Processing

With the exception of SetAddress() requests (refer to Section 9.4.6), a device may begin processing a request as soon as the device receives the Setup Packet. The device is expected to “complete” processing of the request before it allows the Status stage to complete successfully. Some requests initiate operations that take many milliseconds to complete. For such requests, the device class is required to define a method other than Status stage completion to indicate that the operation has completed. For example, a reset on a hub port may take multiple milliseconds to complete depending on the status of the link attached to the port. The SetPortFeature(PORT_RESET) (refer to Section 10.16.2.10) request “completes” when the reset on the port is initiated. Completion of the reset operation is signaled when the port’s status change is set to indicate that the port is now enabled. This technique prevents the host from having to poll for completion when it is known that the operation will take a relatively long period of time to complete.

#### 9.2.6.1 Request Processing Timing

All devices are expected to handle requests in a timely manner. USB sets an upper limit of 5 seconds for any command to be processed. This limit is not applicable in all instances. The limitations are described in the following sections. It should be noted that the limitations are intended to encompass a wide range of implementations. If all devices in a USB system used the maximum allotted time for request processing, the user experience would suffer. For this reason, implementations should strive to complete requests in times that are as short as possible.

9-11

Universal Serial Bus 3.1 Specification, Revision 1.0

### 9.2.6.2 Reset/Resume Recovery Time

After a port is successfully reset or resumed, the USB system software is allowed to access the device attached to the port immediately and it is expected to respond to data transfers.

### 9.2.6.3 Set Address Processing

After the reset or resume, when a device receives a SetAddress() request, the device shall be able to complete processing of the request and be able to successfully complete the Status stage of the request within 50 ms. In the case of the SetAddress() request, the Status stage successfully completes when the device sends an ACK Transaction Packet in response to Status stage STATUS Transaction Packet.

After successful completion of the Status stage, the device shall be able to accept Setup packets addressed to the new address. In addition, after successful completion of the Status stage, the device shall not respond to transactions sent to the old address (unless, of course, the old address and the new address are the same).

### 9.2.6.4 Standard Device Requests

For standard device requests that require no Data stage, a device shall be able to complete the request and be able to successfully complete the Status stage of the request within 50 ms of receipt of the request. This limitation applies to requests targeted to the device, interface, or endpoint.

For standard device requests that require a data stage transfer to the host, the device shall be able to return the first data packet to the host within 500 ms of receipt of the request. For subsequent data packets, if any, the device shall be able to return them within 500 ms of successful completion of the transmission of the previous packet. The device shall then be able to successfully complete the status stage within 50 ms after returning the last data packet.

For standard device requests that require a data stage transfer to the device, the 5-second limit applies. This means that the device shall be capable of accepting all data packets from the host and successfully completing the Status stage if the host provides the data at the maximum rate at which the device can accept it. Delays between packets introduced by the host add to the time allowed for the device to complete the request.

### 9.2.6.5 Class-specific Requests

Unless specifically exempted in the class document, all class-specific requests shall meet the timing limitations for standard device requests. If a class document provides an exemption, the exemption may only be specified on a request-by-request basis.

A class document may require that a device respond more quickly than is specified in this section. Faster response may be required for standard and class-specific requests.

### 9.2.6.6 Speed Dependent Descriptors

An Enhanced SuperSpeed device shall be capable of operating at one of the USB 2.0 defined speeds. The device always knows its operational speed as part of connection processing (refer to Section 10.1.1 or Section 10.1.2 for more details on the connection process). A device operates at a single speed after completing the reset sequence. In particular, there is no speed switch during normal operation. However, an Enhanced SuperSpeed device may have configurations that are

9-12

Device Framework

speed dependent. That is, it may have some configurations that are only possible when operating at Gen X speed or some that are only possible when operating at high-speed. Enhanced SuperSpeed devices shall support reporting the speeds at which they can operate. Note that a USB hub is the only device that is allowed to operate at both USB 2.0 and Gen X speed simultaneously.

An Enhanced SuperSpeed device responds with descriptor information that is valid for the current operating speed. For example, when a device is asked for configuration descriptors, it only returns those for the current operating speed (e.g., high speed). When operating at Gen X speed, the device shall report the other speeds it can operate via its BOS descriptor (refer to Section 9.6.2).

Note that when operating at USB 2.0 speeds, the device shall report the other USB 2.0 speeds it supports using the standard mechanism defined in the USB 2.0 specification in addition to reporting the other speeds supported by the device in its BOS descriptor. Devices with a value of at least 0210H in the bcdUSB field of their device descriptor shall support GetDescriptor (BOS Descriptor) requests.

# NOTE

These descriptors are not retrieved unless the host explicitly issues the corresponding GetDescriptor requests.

### 9.2.7 Request Error

When a request not defined for the device is inappropriate for the current setting of the device or has values that are not compatible with the request is received, a Request Error exists. The device deals with the Request Error by returning a STALL Transaction Packet in response to the next Data stage transaction or in the Status stage of the message. It is preferred that the STALL Transaction Packet be returned at the next Data stage transaction to avoid unnecessary bus activity.

9-13

Universal Serial Bus 3.1 Specification, Revision 1.0

## 9.3 USB Device Requests

All devices respond to requests from the host on the device's Default Control Pipe. These requests are made using control transfers. The request and the request's parameters are sent to the device in the Setup packet. The host is responsible for establishing the values passed in the fields listed in Table 9-3. Every Setup packet has 8 bytes.

Table 9-3. Format of Setup Data

[tbl-147.md](tbl-147.md)

### 9.3.1 bmRequestType

This bitmapped field identifies the characteristics of the specific request. In particular, this field identifies the direction of data transfer in the second stage of the control transfer. The state of the Direction bit is ignored if the wLength field is zero, signifying there is no Data stage.

USB defines a series of standard requests that all devices shall support. These are listed in Table 9-4. In addition, a device class may define additional requests. A device vendor may also define requests supported by the device.

Requests may be directed to the device, an interface on the device, or a specific endpoint on a device. This field also specifies the intended recipient of the request. When an interface is specified, the wIndex field identifies the interface. When an endpoint is specified, the wIndex field identifies the endpoint.

9-14

Device Framework

### 9.3.2 bRequest

This field specifies the particular request. The Type bits in the bmRequestType field modify the meaning of this field. This specification defines values for the bRequest field only when the bits are reset to zero, indicating a standard request (refer to Table 9-4).

### 9.3.3 wValue

The contents of this field vary according to the request. It is used to pass a parameter to the device, specific to the request.

### 9.3.4 wIndex

The contents of this field vary according to the request. It is used to pass a parameter to the device, specific to the request.

The wIndex field is often used in requests to specify an endpoint or an interface. Figure 9-2 shows the format of wIndex when it is used to specify an endpoint.

[tbl-148.md](tbl-148.md)

U-081

Figure 9-2. wIndex Format when Specifying an Endpoint

The Direction bit is set to zero to indicate the OUT endpoint with the specified Endpoint Number and to one to indicate the IN endpoint. In the case of a control pipe, the request should have the Direction bit set to zero but the device may accept either value of the Direction bit.

Figure 9-3 shows the format of wIndex when it is used to specify an interface.

[tbl-149.md](tbl-149.md)

U-082

Figure 9-3. wIndex Format when Specifying an Interface

9-15

Universal Serial Bus 3.1 Specification, Revision 1.0

### 9.3.5 wLength

This field specifies the length of the data transferred during the second stage of the control transfer. The direction of data transfer (host-to-device or device-to-host) is indicated by the *Direction* bit of the *bmRequestType* field. If this field is zero, there is no data transfer stage.

On an input request, a device shall never return more data than is indicated by the *wLength* value; it may return less. On an output request, *wLength* will always indicate the exact amount of data to be sent by the host. Device behavior is undefined if the host should send more or less data than is specified in *wLength*.

9-16

Device Framework

## 9.4 Standard Device Requests

This section describes the standard device requests defined for all devices. Table 9-4 outlines the standard device requests, while Table 9-5 and Table 9-6 give the standard request codes and descriptor types, respectively.

Devices shall respond to standard device requests, even if the device has not yet been assigned an address or has not been configured. If a standard request defines a persistent parameter that can be modified, the reset/default value for that parameter, unless otherwise specified, is zero.

Table 9-4. Standard Device Requests

[tbl-150.md](tbl-150.md)

9-17

Universal Serial Bus 3.1 Specification, Revision 1.0

Table 9-5. Standard Request Codes

[tbl-151.md](tbl-151.md)

9-18

Device Framework

Table 9-6. Descriptor Types

[tbl-152.md](tbl-152.md)

$^{1}$ The INTERFACE_POWER descriptor is defined in the current revision of the USB Interface Power Management Specification.

9-19

Universal Serial Bus 3.1 Specification, Revision 1.0

Feature selectors are used when enabling or setting features, such as function remote wakeup, specific to a device, interface, or endpoint. The values for the feature selectors are given in Table 9-7.

Table 9-7. Standard Feature Selectors

[tbl-153.md](tbl-153.md)

If an unsupported or invalid request is made to a device, the device responds by returning a STALL Transaction Packet in the Data or Status stage of the request. If the device detects the error in the Setup stage, it is preferred that the device returns a STALL Transaction Packet at the earlier of the Data or Status stage. Receipt of an unsupported or invalid request does not cause the Halt feature on the control pipe to be set. If, for any reason, the device becomes unable to communicate via its Default Control Pipe due to an error condition, the device shall be reset to clear the condition and restart the Default Control Pipe.

### 9.4.1 Clear Feature

This request is used to clear or disable a specific feature.

[tbl-154.md](tbl-154.md)

$^{2}$ This Feature Selector value shall be reserved for OTG use. Refer to Section 6.4 of the USB 3.0 OTG and EH Supplement for its definition.

9-20

Device Framework

Feature selector values in wValue shall be appropriate to the recipient. Only device feature selector values may be used when the recipient is a device, only interface feature selector values may be used when the recipient is an interface, and only endpoint feature selector values may be used when the recipient is an endpoint.

Refer to Table 9-7 for a definition of which feature selector values are defined for which recipients.

A ClearFeature() request that references a feature that cannot be cleared, that does not exist, or that references an interface or an endpoint that does not exist, will cause the device to respond with a Request Error.

If wLength is non-zero, then the device behavior is not specified.

Default state: Device behavior when this request is received while the device is in the Default state is not specified.

Address state: This request is valid when the device is in the Address state; references to interfaces, or to endpoints other than the Default Control Pipe, shall cause the device to respond with a Request Error.

Configured state: This request is valid when the device is in the Configured state.

# NOTE

The device shall process a Clear Feature (U1_Enable or U2_Enable or LTM_Enable) only if the device is in the configured state.

### 9.4.2 Get Configuration

This request returns the current device configuration value.

[tbl-155.md](tbl-155.md)

If the returned value is zero, the device is not configured.

If wValue, wIndex, or wLength are not as specified above, then the device behavior is not specified.

Default state: Device behavior when this request is received while the device is in the Default state is not specified.

Address state: The value zero shall be returned.

Configured state: The non-zero bConfigurationValue of the current configuration shall be returned.

9-21

Universal Serial Bus 3.1 Specification, Revision 1.0

### 9.4.3 Get Descriptor

This request returns the specified descriptor if the descriptor exists.

[tbl-156.md](tbl-156.md)

The wValue field specifies the descriptor type in the high byte (refer to Table 9-6) and the descriptor index in the low byte. The descriptor index is used to select a specific descriptor (only for configuration and string descriptors) when several descriptors of the same type are implemented in a device. For example, a device can implement several configuration descriptors. For other standard descriptors that can be retrieved via a GetDescriptor() request, a descriptor index of zero shall be used. The range of values used for a descriptor index is from 0 to one less than the number of descriptors of that type (excluding string descriptors) implemented by the device.

The wIndex field specifies the Language ID for string descriptors or is reset to zero for other descriptors. The wLength field specifies the number of bytes to return. If the descriptor is longer than the wLength field, only the initial bytes of the descriptor are returned. If the descriptor is shorter than the wLength field, the device indicates the end of the control transfer by sending a short packet when further data is requested.

The standard request to a device supports four types of descriptors: device, configuration, BOS (Binary device Object Store), and string. As noted in Section 9.2.6.6, a device operating at Gen X speed reports the other speeds it supports via the BOS descriptor and shall not support the device_qualifier and other_speed_configuration descriptors. A request for a configuration descriptor returns the configuration descriptor, all interface descriptors, endpoint descriptors and endpoint companion descriptors (when operating at Gen X speed) for all of the interfaces in a single request. The first interface descriptor follows the configuration descriptor. The endpoint descriptors for the first interface follow the first interface descriptor. In addition, Enhanced SuperSpeed devices shall return Endpoint Companion descriptors for each of the endpoints in that interface to return the endpoint capabilities required for Enhanced SuperSpeed devices, which would not fit inside the existing endpoint descriptor footprint. If there are additional interfaces, their interface descriptor, endpoint descriptors, and endpoint companion descriptors (when operating at Gen X speed) follow the first interface's endpoint and endpoint companion (when operating at Gen X speed) descriptors.

This specification also defines a flexible and extensible framework for describing and adding device-level capabilities to the set of USB standard specifications. The BOS descriptor (refer to Section 9.6.2) defines a root descriptor that is similar to the configuration descriptor, and is the base descriptor for accessing a family of related descriptors. A host can read a BOS descriptor and learn from the wTotalLength field the entire size of the device-level descriptor set, or it can read in the entire BOS descriptor set of device capabilities. There is no way for a host to read individual device capability descriptors. The entire set can only be accessed via reading the BOS descriptor with a GetDescriptor() request and using the length reported in the wTotalLength field.

Class-specific and/or vendor-specific descriptors follow the standard descriptors they extend or modify.

9-22

Device Framework

All devices shall provide a device descriptor and at least one configuration descriptor. If a device does not support a requested descriptor, it responds with a Request Error.

Default state: This is a valid request when the device is in the Default state.

Address state: This is a valid request when the device is in the Address state.

Configured state: This is a valid request when the device is in the Configured state.

### 9.4.4 Get Interface

This request returns the selected alternate setting for the specified interface.

[tbl-157.md](tbl-157.md)

Some devices have configurations with interfaces that have mutually exclusive settings. This request allows the host to determine the currently selected alternate setting.

If wValue or wLength are not as specified above, then the device behavior is not specified.

If the interface specified does not exist, then the device responds with a Request Error.

Default state: Device behavior when this request is received while the device is in the Default state is not specified.

Address state: A Request Error response is given by the device.

Configured state: This is a valid request when the device is in the Configured state.

### 9.4.5 Get Status

This request returns status for the specified recipient.

[tbl-158.md](tbl-158.md)

The Recipient bits of the bmRequestType field specify the desired recipient. The data returned is the current status of the specified recipient. If the recipient is an endpoint, then the lower byte of wIndex identifies the endpoint whose status is being queried. If the recipient is an interface, then the lower byte of wIndex identifies the interface whose status is being queried.

Only a Device is allowed as the Recipient for a PTM Status request.

The wValue field specifies the Status type in the low order byte (refer to Table 9-8) and the high order byte is reserved. The Status Type is used to select a specific status register when several types of status registers are implemented in a device.

9-23

Universal Serial Bus 3.1 Specification, Revision 1.0

Table 9-8. Standard Status Type Codes

[tbl-159.md](tbl-159.md)

If wLength is not as specified above or if wIndex is non-zero for a device status request, then the behavior of the device is not specified.

If an interface or an endpoint is specified that does not exist, then the device responds with a Request Error.

Default state: Device behavior when this request is received while the device is in the Default state is not specified.

Address state: If an interface or an endpoint other than the Default Control Pipe is specified, then the device responds with a Request Error.

Configured state: If an interface or an endpoint that does not exist is specified, then the device responds with a Request Error.

A GetStatus() request to a device returns the information shown in Figure 9-1.

[tbl-160.md](tbl-160.md)

U-083

Figure 9-4. Information Returned by a Standard GetStatus() Request to a Device

The status fields defined Figure 9-4 are returned by a STANDARD_STATUS type request to a Device recipient.

The Self Powered field indicates whether the device is currently self-powered. If D0 is reset to zero, the device is bus-powered. If D0 is set to one, the device is self-powered. The Self Powered field may not be changed by the SetFeature() or ClearFeature() requests.

The Remote Wakeup field is reserved and must be set to zero by Enhanced SuperSpeed devices. Enhanced SuperSpeed devices use the Function Remote Wake enable/disable field to indicate whether they are enabled for Remote Wake.

The U1 Enable field indicates whether the device is currently enabled to initiate U1 entry. If D2 is set to zero, the device is disabled from initiating U1 entry, otherwise; it is enabled to initiate U1 entry. The U1 Enable field can be modified by the SetFeature() and ClearFeature() requests using the U1_ENABLE feature selector. This field is reset to zero when the device is reset.

The U2 Enable field indicates whether the device is currently enabled to initiate U2 entry. If D3 is set to zero, the device is disabled from initiating U2 entry, otherwise; it is enabled to initiate U2

9-24

Device Framework

entry. The U2 Enable field can be modified by the SetFeature() and ClearFeature() requests using the U2_ENABLE feature selector. This field is reset to zero when the device is reset.

The LTM Enable field indicates whether the device is currently enabled to send Latency Tolerance Messages. If D4 is set to zero, the device is disabled from sending Latency Tolerance Messages, otherwise; it is enabled to send Latency Tolerance Messages. The LTM Enable field can be modified by the SetFeature() and ClearFeature() requests using the LTM_ENABLE feature selector. This field is reset to zero when the device is reset.

A GetStatus() request to the first interface in a function returns the information shown in Figure 9-5.

[tbl-161.md](tbl-161.md)

U-084

Figure 9-5. Information Returned by a Standard GetStatus() Request to an Interface

The status fields defined by Figure 9-5 are returned by a STANDARD_STATUS type request to an Interface recipient.

The Function Remote Wake Capable field indicates whether the function supports remote wake up. The Function Remote Wakeup field indicates whether the function is currently enabled to request remote wakeup. The default mode for functions that support function remote wakeup is disabled. If D1 is reset to zero, the ability of the function to signal remote wakeup is disabled. If D1 is set to one, the ability of the function to signal remote wakeup is enabled. The Function Remote Wakeup field can be modified by the SetFeature() requests using the FUNCTION_SUSPEND feature selector. This Function Remote Wakeup field is reset to zero when the function is reset.

A GetStatus() request to any other interface in a function shall return all zeros.

A GetStatus() request to an endpoint returns the information shown in Figure 9-6.

[tbl-162.md](tbl-162.md)

U-085

Figure 9-6. Information Returned by a Standard GetStatus() Request to an Endpoint

The status fields defined by Figure 9-6 are returned by a STANDARD_STATUS type request to an Endpoint recipient.

9-25

Universal Serial Bus 3.1 Specification, Revision 1.0

The Halt feature is required to be implemented for all interrupt and bulk endpoint types. If the endpoint is currently halted, then the Halt feature is set to one. Otherwise, the Halt feature is reset to zero. The Halt feature may optionally be set with the SetFeature(ENDPOINT_HALT) request. When set by the SetFeature() request, the endpoint exhibits the same stall behavior as if the field had been set by a hardware condition. If the condition causing a halt has been removed, clearing the Halt feature via a ClearFeature(ENDPOINT_HALT) request results in the endpoint no longer returning a STALL Transaction Packet. Regardless of whether an endpoint has the Halt feature set, a ClearFeature(ENDPOINT_HALT) request always results in the data sequence being reinitialized to zero, and if Streams are enabled, the Stream State Machine shall be reinitialized to the Disabled state. The Halt feature is reset to zero after either a SetConfiguration() or SetInterface() request even if the requested configuration or interface is the same as the current configuration or interface.

Enhanced SuperSpeed devices do not support functional stall on control endpoints and hence do not require the Halt feature be implemented for any control endpoints.

[tbl-163.md](tbl-163.md)

U-085a

Figure 9-7. Information Returned by a PTM GetStatus() Request to an Endpoint

The status fields defined by Figure 9-7 are returned by a PTM_STATUS type request to a Device recipient.

The LDM Enabled flag indicates whether the device is currently enabled to participate in Precision Time Measurement (PTM). If D5 is set to zero, the device is disabled from executing the LDM protocol and providing a local bus interval boundary reference, otherwise; it is enabled to execute the LDM protocol. The LDM Enabled flag can be modified by the SetFeature() and ClearFeature() requests using the LDM_ENABLE feature selector. This field shall be set to one when the device is reset, allowing a PTM capable device to automatically attempt to participate in LDM with its upstream partner. If a Requestor is unable to successfully establish LDM Timestamp Exchanges in its Responder, then the LDM Enabled field shall be cleared to zero.

The LDM Valid field indicates whether the LDM Link Delay is valid, otherwise; it is invalid. LDM Valid shall be zero if LDM Enabled is zero.

The LDM Link Delay field is in tIsochTimestampGranularity units. If LDM Valid is one, then the LDM Link Delay field defines the link delay value measured by the PTM LDM mechanism. If LDM Valid is one, then the LDM Link Delay field shall be set to zero. Refer to section 8.4.8.4.

9-26

Device Framework

### 9.4.6 Set Address

This request sets the device address for all future device accesses.

[tbl-164.md](tbl-164.md)

The wValue field specifies the device address to use for all subsequent accesses.

The Status stage after the initial Setup packet assumes the same device address as the Setup packet. The device does not change its device address until after the Status stage of this request is completed successfully. Note that this is a difference between this request and all other requests. For all other requests, the operation indicated shall be completed before the Status stage.

If the specified device address is greater than 127, or if wIndex or wLength is non-zero, then the behavior of the device is not specified.

Default state: If the address specified is non-zero, then the device shall enter the Address state; otherwise, the device remains in the Default state (this is not an error condition).

Address state: If the address specified is zero, then the device shall enter the Default state; otherwise, the device remains in the Address state but uses the newly-specified address.

Configured state: Device behavior when this request is received while the device is in the Configured state is not specified.

### 9.4.7 Set Configuration

This request sets the device configuration.

[tbl-165.md](tbl-165.md)

The lower byte of the wValue field specifies the desired configuration. This configuration value shall be zero or match a configuration value from a configuration descriptor. If the configuration value is zero, the device is placed in its Address state. The upper byte of the wValue field is reserved.

If wIndex, wLength, or the upper byte of wValue is non-zero, then the behavior of this request is not specified.

Default state: Device behavior when this request is received while the device is in the Default state is not specified.

Address state: If the specified configuration value is zero, then the device remains in the Address state. If the specified configuration value matches the configuration value from a configuration descriptor, then that configuration is selected and the device enters the Configured state. Otherwise, the device responds with a Request Error.

9-27

Universal Serial Bus 3.1 Specification, Revision 1.0

Configured state: If the specified configuration value is zero, then the device enters the Address state. If the specified configuration value matches the configuration value from a configuration descriptor, then that configuration is selected and the device remains in the Configured state. Otherwise, the device responds with a Request Error.

### 9.4.8 Set Descriptor

This request is optional and may be used to update existing descriptors or new descriptors may be added.

[tbl-166.md](tbl-166.md)

The wValue field specifies the descriptor type in the high byte (refer to Table 9-6) and the descriptor index in the low byte. The descriptor index is used to select a specific descriptor (only for configuration and string descriptors) when several descriptors of the same type are implemented in a device. For example, a device can implement several configuration descriptors. For other standard descriptors that can be set via a SetDescriptor() request, a descriptor index of zero shall be used. The range of values used for a descriptor index is from 0 to one less than the number of descriptors of that type (excluding string descriptors) implemented by the device.

The wIndex field specifies the Language ID for string descriptors or is reset to zero for other descriptors. The wLength field specifies the number of bytes to transfer from the host to the device.

The only allowed values for descriptor type are device, configuration, and string descriptor types.

If this request is not supported, the device will respond with a Request Error.

Default state: Device behavior when this request is received while the device is in the Default state is not specified.

Address state: If supported, this is a valid request when the device is in the Address state.

Configured state: If supported, this is a valid request when the device is in the Configured state.

### 9.4.9 Set Feature

This request is used to set or enable a specific feature.

[tbl-167.md](tbl-167.md)

Feature selector values in wValue shall be appropriate to the recipient. Only device feature selector values may be used when the recipient is a device; only interface feature selector values may be used when the recipient is an interface; and only endpoint feature selector values may be used when

9-28

Device Framework

the recipient is an endpoint. If the recipient is an endpoint, then the lower byte of wIndex identifies the endpoint.

Refer to Table 9-7 for a definition of which feature selector values are defined for which recipients.

The FUNCTION_SUSPEND feature is only defined for an interface recipient. The lower byte of wIndex shall be set to the first interface that is part of that function.

The U1/U2_ENABLE feature is only defined for a device recipient and wIndex shall be set to zero. Setting the U1/U2_ENABLE feature allows the device to initiate U1/U2 entry respectively. A device shall support the U1/U2_ENABLE feature when in the Configured state only. System software must not enable the device to initiate U1 if the time for U1 System Exit Latency initiated by Host plus one Bus Interval time is greater than the minimum of the service intervals of any periodic endpoints in the device. In addition, system software must not enable the device to initiate U2 if the time for U2 System Exit Latency initiated by Host plus one Bus Interval time is greater than the minimum of the service intervals of any periodic endpoints in the device.

The LTM_ENABLE feature is only defined for a device recipient and wIndex shall be set to zero. Setting the LTM_ENABLE feature allows the device to send Latency Tolerance Messages. A device shall support the LTM_ENABLE feature if it is in the Configured state and supports the LTM capability.

The LDM_ENABLE feature is only defined for a device recipient and wIndex shall be set to zero. Setting the LDM_ENABLE feature allows the device to execute the LDM protocol. A device shall support the LDM_ENABLE feature if it is in the Address or Configured states and supports the PTM capability.

A SetFeature() request that references a feature that cannot be set or that does not exist causes a STALL Transaction Packet to be returned in the Status stage of the request.

Table 9-9. Suspend Options

[tbl-168.md](tbl-168.md)

If the feature selector is FUNCTION_SUSPEND, then the most significant byte of wIndex is used to specify Suspend options. The recipient of a SetFeature (FUNCTION_SUSPEND...) shall be the first interface in the function; and, hence, the bmRequestType shall be set to one. The valid encodings for the FUNCTION_SUSPEND suspend options are listed in Table 9-9.

If wLength is non-zero, then the behavior of the device is not specified.

9-29

Universal Serial Bus 3.1 Specification, Revision 1.0

If an endpoint or interface is specified that does not exist, then the device responds with a Request Error.

Default state: Device behavior when this request is received while the device is in the Default state is not specified.

Address state: If an interface or an endpoint other than the Default Control Pipe is specified then the device responds with a Request Error. If the device receives a SetFeature(U1/U2 Enable or LTM Enable or LDM Enable or FUNCTION_SUSPEND), then the device responds with a Request Error.

Configured state: This is a valid request when the device is in the Configured state.

9-30

Device Framework

### 9.4.10 Set Interface

This request allows the host to select an alternate setting for the specified interface.

[tbl-169.md](tbl-169.md)

Some devices have configurations with interfaces that have mutually exclusive settings. This request allows the host to select the desired alternate setting. If a device only supports a default setting for the specified interface, then a STALL Transaction Packet may be returned in the Status stage of the request. This request cannot be used to change the set of configured interfaces (the SetConfiguration() request shall be used instead).

If the interface or the alternate setting does not exist, then the device responds with a Request Error. If wLength is non-zero, then the behavior of the device is not specified.

Default state: Device behavior when this request is received while the device is in the Default state is not specified.

Address state: The device shall respond with a Request Error.

Configured state: This is a valid request when the device is in the Configured state.

### 9.4.11 Set Isochronous Delay

This request informs the device of the delay from the time a host transmits a packet to the time it is received by the device.

[tbl-170.md](tbl-170.md)

The wValue field specifies a delay from 0 to 65535 ns. This delay represents the time from when the host starts transmitting the first framing symbol of the packet to when the device receives the first framing symbol of that packet. The wValue field shall be calculated as follows.

$$wValue = (sum \ of \ wHubDelay \ values) + (tTPTransmissionDelay \ * \ (number \ of \ hubs \ + \ 1))$$

Where, a wHubDelay value is provided by the Enhanced SuperSpeed Hub Descriptor of each hub in the path, respectively, and tTPTransmissionDelay is defined in Table 8-35.

If wIndex or wLength is non-zero, then the behavior of this request is not specified.

Default state: This is a valid request when the device is in the Default state.

Address state: This is a valid request when the device is in the Address state.

Configured state: This is a valid request when the device is in the Configured state.

9-31

Universal Serial Bus 3.1 Specification, Revision 1.0

### 9.4.12 Set SEL

This request sets both the U1 and U2 System Exit Latency and the U1 or U2 exit latency for all the links between a device and a root port on the host.

[tbl-171.md](tbl-171.md)

The latency values are sent to the device in the data stage of the control transfer in the following format:

[tbl-172.md](tbl-172.md)

Figure C-2 in Appendix C illustrates the total latency a device may experience. The components of latency include the following:

- t1: the time to transition all links in the path to the host to U0 when the transition is initiated by the device
- t2: the time for the ERDY to traverse the interconnect hierarchy from the device to the host
- t3: the time for the host to consume the ERDY and transmit a response to that request
- t4: the time for the response to traverse the interconnect hierarchy from the host to the device

The U1SEL and U2SEL values represent the total round trip path latency when transitioning the links between the device and host from U1 or U2 respectively to U0 under worst-case circumstances when the transition is initiated by the device. This is the sum of times t1, t2, and t4.

The U1PEL and U2PEL values represent the device to host latency to transition the entire path of links between the device and host from U1 or U2 respectively to U0 under worst-case circumstances when the transition is initiated by the device. This time includes only t1.

For more information, refer to Section C.1.5.1.

If wIndex or wValue is not set to zero or wLength is not six, then the behavior of the device is not specified.

Default state: Device behavior when this request is received while the device is in the Default state is not specified.

Address state: This is a valid request when the device is in the Address state.

Configured state: This is a valid request when the device is in the Configured state.

9-32

Device Framework

### 9.4.13 Synch Frame

This request is used to set and then report an endpoint's synchronization frame.

[tbl-173.md](tbl-173.md)

When an endpoint supports isochronous transfers, the endpoint may also require per-frame transfers to vary in size according to a specific pattern. The host and the endpoint must agree on which frame the repeating pattern begins. The number of the frame in which the pattern began is returned to the host.

If an Enhanced SuperSpeed device supports the Synch Frame request, it shall internally synchronize itself to the zero$^{th}$ microframe and have a time notion of classic frame. Only the frame number is used to synchronize and reported by the device endpoint (i.e., no microframe number). The endpoint must synchronize to the zero$^{th}$ microframe.

This value is only used for isochronous data transfers using implicit pattern synchronization. If wValue is non-zero or wLength is not two, then the behavior of the device is not specified.

If the specified endpoint does not support this request, then the device will respond with a Request Error.

Default state: Device behavior when this request is received while the device is in the Default state is not specified.

Address state: The device shall respond with a Request Error.

Configured state: This is a valid request when the device is in the Configured state.

### 9.4.14 Events and Their Effect on Device Parameters

This section lists the various parameters and the effect on those parameters when the device receives a control transfer command or when it observes a bus reset on the bus. An X denotes that the parameter is reset to its default value when the said event occurs. A Y denotes that the particular Parameter is modified by the event.

Control transfers and events not identified in the table shall not affect the value of parameters shown in Table 9-10.

9-33

Universal Serial Bus 3.1 Specification, Revision 1.0

Table 9-10. Device Parameters and Events

[tbl-174.md](tbl-174.md)

9-34

Device Framework

## 9.5 Descriptors

Devices report their attributes using descriptors. A descriptor is a data structure with a defined format. Each descriptor begins with a byte-wide field that contains the total number of bytes in the descriptor followed by a byte-wide field that identifies the descriptor type.

Using descriptors allows concise storage of the attributes of individual configurations because each configuration may reuse descriptors or portions of descriptors from other configurations that have the same characteristics. In this manner, the descriptors resemble individual data records in a relational database.

Where appropriate, descriptors contain references to string descriptors that provide displayable information describing a descriptor in human-readable form. The inclusion of string descriptors is optional. However, the reference fields within descriptors are mandatory. If a device does not support string descriptors, string reference fields shall be reset to zero to indicate no string descriptor is available.

If a descriptor returns with a value in its length field that is less than defined by this specification, the descriptor is invalid and should be rejected by the host. If the descriptor returns with a value in its length field that is greater than defined by this specification, the extra bytes are ignored by the host, but the next descriptor is located using the length returned rather than the length expected.

A device may return class- or vendor-specific descriptors in two ways:

1. If the class or vendor specific descriptors use the same format as standard descriptors (i.e., start with a length byte and followed by a type byte), they shall be returned interleaved with standard descriptors in the configuration information returned by a GetDescriptor(Configuration) request. In this case, the class or vendor-specific descriptors shall follow a related standard descriptor they modify or extend.
2. If the class or vendor specific descriptors are independent of configuration information or use a non-standard format, a GetDescriptor() request specifying the class or vendor specific descriptor type and index may be used to retrieve the descriptor from the device. A class or vendor specification will define the appropriate way to retrieve these descriptors.

## 9.6 Standard USB Descriptor Definitions

The standard descriptors defined in this specification may only be modified or extended by revision of this specification.

### 9.6.1 Device

A device descriptor describes general information about a device. It includes information that applies globally to the device and all of the device's configurations. A device has only one device descriptor.

The device descriptor of an Enhanced SuperSpeed device shall have a version number of 3.1 (0310H). The device descriptor of an Enhanced SuperSpeed device operating in one of the USB 2.0 modes shall have a version number of 2.1 (0210H).

9-35

Universal Serial Bus 3.1 Specification, Revision 1.0

The bcdUSB field contains a BCD version number. The value of the bcdUSB field is 0xJJMN for version JJ.M.N (JJ – major version number, M – minor version number, N – sub-minor version number), e.g., version 2.1.3 is represented with value 0213H and version 3.0 is represented with a value of 0300H.

The bNumConfigurations field indicates the number of configurations at the current operating speed. Configurations for the other operating speed are not included in the count. If there are specific configurations of the device for specific speeds, the bNumConfigurations field only reflects the number of configurations for a single speed, not the total number of configurations for both speeds.

If the device is operating at Gen X speed, the bMaxPacketSize0 field shall be set to 09H (see Table 9-11) indicating a 512-byte maximum packet. An Enhanced SuperSpeed device shall not support any other maximum packet sizes for the default control pipe (endpoint 0) control endpoint.

All devices have a default control pipe. The maximum packet size of a device's default control pipe is described in the device descriptor. Endpoints specific to a configuration and its interface(s) are described in the configuration descriptor. A configuration and its interface(s) do not include an endpoint descriptor for the default control pipe. Other than the maximum packet size, the characteristics of the default control pipe are defined by this specification and are the same for all Enhanced SuperSpeed devices.

The bNumConfigurations field identifies the number of configurations the device supports. Table 9-11 shows the standard device descriptor.

9-36

Device Framework

Table 9-11. Standard Device Descriptor

[tbl-175.md](tbl-175.md)

9-37

Universal Serial Bus 3.1 Specification, Revision 1.0

[tbl-176.md](tbl-176.md)

### 9.6.2 Binary Device Object Store (BOS)

This section defines a flexible and extensible framework for describing and adding device-level capabilities to the set of USB standard specifications. As mentioned above, there exists a device descriptor, but all device-level capability extensions are defined using the following framework.

The BOS descriptor defines a root descriptor that is similar to the configuration descriptor, and is the base descriptor for accessing a family of related descriptors. A host can read a BOS descriptor and learn from the wTotalLength field the entire size of the device-level descriptor set, or it can read in the entire BOS descriptor set of device capabilities. The host accesses this descriptor using the GetDescriptor() request. The descriptor type in the GetDescriptor() request is set to BOS (see Table 9-12). There is no way for a host to read individual device capability descriptors. The entire set can only be accessed via reading the BOS descriptor with a GetDescriptor() request and using the length reported in the wTotalLength field.

Table 9-12. BOS Descriptor

[tbl-177.md](tbl-177.md)

Individual technology-specific or generic device-level capabilities are reported via Device Capability descriptors. The format of the Device Capability descriptor is defined in Table 9-13. The Device Capability descriptor has a generic header, with a sub-type field (bDevCapabilityType) which defines the layout of the remainder of the descriptor. The codes for bDevCapabilityType are defined in Table 9-14.

9-38

Device Framework

Table 9-13. Format of a Device Capability Descriptor

[tbl-178.md](tbl-178.md)

Device Capability descriptors are always returned as part of the BOS information returned by a GetDescriptor(BOS) request. A Device Capability cannot be directly accessed with a GetDescriptor() or SetDescriptor() request.

Table 9-14. Device Capability Type Codes

[tbl-179.md](tbl-179.md)

The following section defines the USB 2.0 Extension Descriptor, the SuperSpeed USB Device Capability, the SuperSpeedPlus Capability and the Container ID (if supported) that a USB device shall return when operating at Gen X speed or in any of the USB 2.0 speeds.

9-39

Universal Serial Bus 3.1 Specification, Revision 1.0

### 9.6.2.1 USB 2.0 Extension

An Enhanced SuperSpeed device shall include the USB 2.0 Extension descriptor and shall support LPM when operating in USB 2.0 High-Speed mode.

Table 9-15. USB 2.0 Extension Descriptor

[tbl-180.md](tbl-180.md)

9-40

Device Framework

### 9.6.2.2 SuperSpeed USB Device Capability

This section defines the required device-level capabilities descriptor which shall be implemented by all Enhanced SuperSpeed devices. This capability descriptor cannot be directly accessed with a GetDescriptor() or SetDescriptor() request.

Table 9-16. SuperSpeed Device Capability Descriptor

[tbl-181.md](tbl-181.md)

9-41

Universal Serial Bus 3.1 Specification, Revision 1.0

[tbl-182.md](tbl-182.md)

9-42

Device Framework

### 9.6.2.3 Container ID

This section defines the device-level Container ID descriptor which shall be implemented by all USB hubs, and is optional for other devices. If this descriptor is provided when operating in one mode, it shall be provided when operating in any mode. This descriptor may be used by a host in order to identify a unique device instance across all operating modes. If a device can also connect to a host through other technologies, the same Container ID value contained in this descriptor should also be provided over those other technologies in a technology specific manner.

This capability descriptor cannot be directly accessed with a GetDescriptor() or SetDescriptor() request.

Table 9-17. Container ID Descriptor

[tbl-183.md](tbl-183.md)

### 9.6.2.4 Platform Descriptor

The Platform Descriptor contains a 128-bit UUID value that is defined and published independently by the platform/operating system vendor, and is used to identify a unique platform specific device capability. The descriptor may also contain one or more bytes of data associated with the capability.

Table 9-18. Platform Descriptor

[tbl-184.md](tbl-184.md)

9-43

Universal Serial Bus 3.1 Specification, Revision 1.0

### 9.6.2.5 SuperSpeedPlus USB Device Capability

This section defines the required device-level capabilities descriptor which shall be implemented by all SuperSpeedPlus devices. This capability descriptor cannot be directly accessed with a GetDescriptor() or SetDescriptor() request.

Table 9-19. SuperSpeedPlus Descriptor

[tbl-185.md](tbl-185.md)

9-44

Device Framework

[tbl-186.md](tbl-186.md)

9-45

Universal Serial Bus 3.1 Specification, Revision 1.0

### 9.6.2.6 Precision Time Measurement

This section defines the required device-level capabilities descriptor which shall be implemented by all hubs and devices that support the PTM capability. This capability descriptor cannot be directly accessed with a GetDescriptor() or SetDescriptor() request.

Table 9-20. PTM Capability Descriptor

[tbl-187.md](tbl-187.md)

### 9.6.3 Configuration

The configuration descriptor describes information about a specific device configuration. The descriptor contains a bConfigurationValue field with a value that, when used as a parameter to the SetConfiguration() request, causes the device to assume the described configuration.

The descriptor describes the number of interfaces provided by the configuration. Each interface may operate independently. For example, a Video Class device might be configured with two interfaces, each providing 64-MBps bi-directional channels that have separate data sources or sinks on the host. Another configuration might present the Video Class device as a single interface, bonding the two channels into one 128-MBps bi-directional channel.

When the host requests the configuration descriptor, all related interface, endpoint, and endpoint companion descriptors are returned (refer to Section 9.4.3).

A device has one or more configuration descriptors. Each configuration has one or more interfaces and each interface has zero or more endpoints. An endpoint is not shared among interfaces within a single configuration unless the endpoint is used by alternate settings of the same interface. Endpoints may be shared among interfaces that are part of different configurations without this restriction.

Once configured, devices may support limited adjustments to the configuration. If a particular interface has alternate settings, an alternate may be selected after configuration. Table 9-21 shows the standard configuration descriptor.

9-46

Device Framework

Table 9-21. Standard Configuration Descriptor

[tbl-188.md](tbl-188.md)

9-47

Universal Serial Bus 3.1 Specification, Revision 1.0

### 9.6.4 Interface Association

The Interface Association Descriptor is used to describe that two or more interfaces are associated to the same function. An “association” includes two or more interfaces and all of their alternate setting interfaces. A device must use an Interface Association descriptor for each device function that requires more than one interface. An Interface Association descriptor is always returned as part of the configuration information returned by a GetDescriptor(Configuration) request. An interface association descriptor cannot be directly accessed with a GetDescriptor() or SetDescriptor() request. An interface association descriptor must be located before the set of interface descriptors (including all alternate settings) for the interfaces it associates. All of the interface numbers in the set of associated interfaces must be contiguous. Table 9-22 shows the standard interface association descriptor. The interface association descriptor includes function class, subclass, and protocol fields. The values in these fields can be the same as the interface class, subclass, and protocol values from any one of the associated interfaces. The preferred implementation, for existing device classes, is to use the interface class, subclass, and protocol field values from the first interface in the list of associated interfaces.

Table 9-22. Standard Interface Association Descriptor

[tbl-189.md](tbl-189.md)

# NOTE

Since this particular feature was not included in earlier versions of the USB specification, there is an issue with how existing USB operating system implementations will support devices that use this descriptor. It is strongly recommended that device implementations utilizing the interface association descriptor use the Multi-interface Function Class codes in the device descriptor. This allows simple and easy identification of these devices and allows on some operating systems, installation of an upgrade driver that can parse and enumerate configurations that include the Interface Association Descriptor. The Multi-interface Function Class code is documented at http://www.usb.org/developers/docs.

9-48

Device Framework

### 9.6.5 Interface

The interface descriptor describes a specific interface within a configuration. A configuration provides one or more interfaces, each with zero or more endpoint descriptors. When a configuration supports more than one interface, the endpoint descriptors for a particular interface follow the interface descriptor in the data returned by the GetConfiguration() request. As mentioned earlier in this chapter, Enhanced SuperSpeed devices shall return Endpoint Companion descriptors for each of the endpoints in that interface to return additional information about its endpoint capabilities. The Endpoint Companion descriptor shall immediately follow the endpoint descriptor it is associated with in the configuration information. An interface descriptor is always returned as part of a configuration descriptor. Interface descriptors cannot be directly accessed with a GetDescriptor() or SetDescriptor() request.

An interface may include alternate settings that allow the endpoints and/or their characteristics to be varied after the device has been configured. The default setting for an interface is always alternate setting zero. The SetInterface() request is used to select an alternate setting or to return to the default setting. The GetInterface() request returns the selected alternate setting.

Alternate settings allow a portion of the device configuration to be varied while other interfaces remain in operation. If a configuration has alternate settings for one or more of its interfaces, a separate interface descriptor and its associated endpoint and endpoint companion (when reporting its Enhanced SuperSpeed configuration) descriptors are included for each setting.

If a device configuration supported a single interface with two alternate settings, the configuration descriptor would be followed by an interface descriptor with the bInterfaceNumber and bAlternateSetting fields set to zero and then the endpoint and endpoint companion (when reporting its Enhanced SuperSpeed configuration) descriptors for that setting, followed by another interface descriptor and its associated endpoint and endpoint companion descriptors. The second interface descriptor's bInterfaceNumber field would also be set to zero, but the bAlternateSetting field of the second interface descriptor would be set to one.

If an interface uses only the Default Control Pipe, no endpoint descriptors follow the interface descriptor. In this case, the bNumEndpoints field shall be set to zero.

An interface descriptor never includes the Default Control Pipe in the number of endpoints. Table 9-23 shows the standard interface descriptor.

9-49

Universal Serial Bus 3.1 Specification, Revision 1.0

Table 9-23. Standard Interface Descriptor

[tbl-190.md](tbl-190.md)

9-50

Device Framework

### 9.6.6 Endpoint

Each endpoint used for an interface has its own descriptor. This descriptor contains the information required by the host to determine the bandwidth requirements of each endpoint. An endpoint descriptor is always returned as part of the configuration information returned by a GetDescriptor(Configuration) request. An endpoint descriptor cannot be directly accessed with a GetDescriptor() or SetDescriptor() request. There is never an endpoint descriptor for endpoint zero. Table 9-24 shows the standard endpoint descriptor.

Table 9-24. Standard Endpoint Descriptor

[tbl-191.md](tbl-191.md)

9-51

Universal Serial Bus 3.1 Specification, Revision 1.0

[tbl-192.md](tbl-192.md)

9-52

Device Framework

The bmAttributes field provides information about the endpoint's Transfer Type (bits 1..0) and Synchronization Type (bits 3..2). For interrupt endpoints, the Usage Type bits (bits 5..4) indicate whether the endpoint is used for infrequent notifications that can tolerate varying latencies (bits 5..4 = 01b), or if it regularly transfers data in consecutive service intervals or is dependent on bounded latencies (bits 5..4 = 00b). For example, a hub's interrupt endpoint would specify that it is a notification type, while a mouse would specify a periodic type. For endpoints that sometimes operate in infrequent notification mode and at other times operate in periodic mode then this field shall be set to Periodic (bits 5..4 = 00b). These values may be used by software to determine appropriate power management settings. See Appendix C for details on how this value may effect power management. In addition, for isochronous endpoints the Usage Type bit (bits 5..4) indicate whether this is an endpoint used for normal data transfers (bits 5..4 = 00b), whether it is used to convey explicit feedback information for one or more data endpoints (bits 5..4 = 01b) or whether it is a data endpoint that also serves as an implicit feedback endpoint for one or more data endpoints (bits 5..4=10b).

If the endpoint is used as an explicit feedback endpoint (bits 5..4 = 01b), then the Transfer Type shall be set to isochronous (bits 1..0 = 01b) and the Synchronization Type shall be set to No Synchronization (bits 3..2 = 00b).

A feedback endpoint (explicit or implicit) needs to be associated with one (or more) isochronous data endpoints to which it provides feedback service. The association is based on endpoint number matching. A feedback endpoint always has the opposite direction from the data endpoint(s) it services. If multiple data endpoints are to be serviced by the same feedback endpoint, the data endpoints shall have ascending ordered—but not necessarily consecutive—endpoint numbers. The first data endpoint and the feedback endpoint shall have the same endpoint number (and opposite direction). This ensures that a data endpoint can uniquely identify its feedback endpoint by searching for the first feedback endpoint that has an endpoint number equal or less than its own endpoint number.

Example: Consider the extreme case where there is a need for five groups of OUT asynchronous isochronous endpoints and at the same time four groups of IN adaptive isochronous endpoints. Each group needs a separate feedback endpoint and the groups are composed as shown in Table 9-25.

Table 9-25. Example of Feedback Endpoint Numbers

[tbl-193.md](tbl-193.md)

9-53

Universal Serial Bus 3.1 Specification, Revision 1.0

The endpoint numbers can be intertwined as illustrated in Figure 9-8.

![img-256.jpeg](img-256.jpeg)

Figure 9-8. Example of Feedback Endpoint Relationships

For high-speed bulk and control OUT endpoints, the bInterval field is only used for compliance purposes; the host controller is not required to change its behavior based on the value in this field.

9-54

Device Framework

### 9.6.7 SuperSpeed Endpoint Companion

This descriptor shall only be returned by Enhanced SuperSpeed devices that are operating at Gen X speed. Each endpoint described in an interface is followed by a SuperSpeed Endpoint Companion descriptor. This descriptor is returned as part of the configuration information returned by a GetDescriptor(Configuration) request and cannot be directly accessed with a GetDescriptor() or SetDescriptor() request. The Default Control Pipe does not have an Endpoint Companion descriptor. The Endpoint Companion descriptor shall immediately follow the endpoint descriptor it is associated with in the configuration information.

Table 9-26. SuperSpeed Endpoint Companion Descriptor

[tbl-194.md](tbl-194.md)

9-55

Universal Serial Bus 3.1 Specification, Revision 1.0

[tbl-195.md](tbl-195.md)

9-56

Device Framework

[tbl-196.md](tbl-196.md)

9-57

Universal Serial Bus 3.1 Specification, Revision 1.0

### 9.6.8 SuperSpeedPlus Isochronous Endpoint Companion

This descriptor contains additional endpoint characteristics that are only defined for endpoints of devices operating at above Gen 1 speed. This descriptor shall only be returned (as part of the devices' complete configuration descriptor) by an Enhanced SuperSpeed device that is operating at above Gen 1 speed. This descriptor shall be returned for each Isochronous endpoint that requires more than 48K bytes per Service Interval.

This descriptor is returned as part of the configuration information returned by a GetDescriptor(Configuration) request and cannot be directly accessed with a GetDescriptor() or SetDescriptor() request.

The SuperSpeedPlus Isochronous Endpoint Companion descriptor shall immediately follow the SuperSpeed Endpoint Companion descriptor that follows the Isochronous endpoint descriptor in the configuration information.

When an alternate setting is selected that has an Isochronous endpoint that has a SuperSpeedPlus Isochronous Endpoint Companion descriptor the endpoint shall operate with the characteristics as described in the SuperSpeedPlus Isochronous Endpoint Companion descriptor.

Table 9-27. SuperSpeedPlus Isochronous Endpoint Companion Descriptor

[tbl-197.md](tbl-197.md)

9-58

Device Framework

### 9.6.9 String

String descriptors are optional. As noted previously, if a device does not support string descriptors, all references to string descriptors within device, configuration, and interface descriptors shall be reset to zero.

String descriptors use UNICODE UTF16LE encodings as defined by The Unicode Standard, Worldwide Character Encoding, Version 5.0, The Unicode Consortium, Addison-Wesley Publishing Company, Reading, Massachusetts (http://www.unicode.org). The strings in a device may support multiple languages. When requesting a string descriptor, the requester specifies the desired language using a 16-bit language ID (LANGID) defined by the USB-IF. The list of currently defined USB LANGIDs can be found at http://www.usb.org/developers/docs.html. String index zero for all languages returns a string descriptor that contains an array of 2-byte LANGID codes supported by the device. Table 9-28 shows the LANGID code array. A device may omit all string descriptors. Devices that omit all string descriptors shall not return an array of LANGID codes.

The array of LANGID codes is not NULL-terminated. The size of the array (in bytes) is computed by subtracting two from the value of the first byte of the descriptor.

Table 9-28. String Descriptor Zero, Specifying Languages Supported by the Device

[tbl-198.md](tbl-198.md)

The UNICODE string descriptor (shown in Table 9-29) is not NULL-terminated. The string length is computed by subtracting two from the value of the first byte of the descriptor.

Table 9-29. UNICODE String Descriptor

[tbl-199.md](tbl-199.md)

9-59

Universal Serial Bus 3.1 Specification, Revision 1.0

## 9.7 Device Class Definitions

All devices shall support the requests and descriptor definitions described in this chapter. Most devices provide additional requests and, possibly, descriptors for device-specific extensions. In addition, devices may provide extended services that are common to a group of devices. In order to define a class of devices, the following information shall be provided to completely define the appearance and behavior of the device class.

### 9.7.1 Descriptors

If the class requires any specific definition of the standard descriptors, the class definition shall include those requirements as part of the class definition. In addition, if the class defines a standard extended set of descriptors, they shall also be fully defined in the class definition. Any extended descriptor definitions shall follow the approach used for standard descriptors; for example, all descriptors shall begin with a length field.

### 9.7.2 Interface(s)

When a class of devices is standardized, the interfaces used by the devices shall be included in the device class definition. Devices may further extend a class definition with proprietary features as long as they meet the base definition of the class.

### 9.7.3 Requests

All of the requests specific to the class shall be defined.

9-60

# 10 Hub, Host Downstream Port, and Device Upstream Port Specification

This chapter describes the architectural requirements for a hub that supports both Enhanced SuperSpeed and USB 2.0 and is referred to as a “USB hub”. The chapter also describes differences between functional requirements for a host downstream port and a hub downstream port as well as differences between a peripheral upstream port and a hub upstream port. The chapter contains the description of the Enhanced SuperSpeed hub. An Enhanced SuperSpeed hub supports all Gen X speeds. This chapter includes descriptions of the SuperSpeed sub-blocks (the SuperSpeed repeater/forwarder and the SuperSpeed Hub Controller) as well as the SuperSpeedPlus sub-blocks (the SuperSpeedPlus Upstream Controller, the SuperSpeedPlus Downstream Controller and the SuperSpeedPlus Hub Controller). This chapter also describes the hub’s operation for error recovery, reset, suspend/resume, hub request behavior, and hub descriptors. The USB 2.0 hub sub-block is described in the Universal Serial Bus Specification, Revision 2.0.

The hub specification chapter along with the Universal Serial Bus Specification, Revision 2.0 supply the information needed for an implementer to design a hub that conforms to this revision of the USB specification.

## 10.1 Hub Feature Summary

Hubs provide the electrical interface between USB devices and the host. Hubs are directly responsible for supporting many of the attributes that make USB user friendly and hide its complexity from the user. Listed below are the major aspects of USB functionality that hubs support:

- Connectivity behavior
- Power management
- Device connect/disconnect detection
- Bus fault detection and recovery
- Enhanced SuperSpeed and USB 2.0 (high-speed, full-speed, and low-speed) device support

10-1

Universal Serial Bus 3.1 Specification, Revision 1.0

![img-257.jpeg](img-257.jpeg)

**Figure 10-1. USB Hub Architecture**

When a USB hub connects on its upstream facing port at Gen 1 speed, it shall operate (and be referred to) as a SuperSpeed hub (including operating its downstream ports at no higher than Gen 1 speed).

When a USB hub connects on its upstream facing port at a speed above Gen 1 speed, it shall operate (and be referred to) as a SuperSpeedPlus hub.

When the hub upstream facing port is attached to an electrical environment that is only operating at high-speed or full-speed, then Enhanced SuperSpeed connectivity is not available to devices attached to downstream facing ports.

Figure 10-1 shows a high level block diagram of a four port USB hub and the locations of its upstream and downstream facing ports. A USB hub is the logical combination of two hubs: a USB 2.0 hub and an Enhanced SuperSpeed hub. Each hub operates independently on a separate data bus. Typically, the only signal shared logic between them is to control VBUS. If either the USB 2.0 hub or Enhanced SuperSpeed hub controllers requires a downstream port to be powered, power is turned on for the port. A USB hub connects on both interfaces upstream whenever possible. All exposed downstream ports on a USB hub shall support both Enhanced SuperSpeed and USB 2.0 connections. Host controller ports may have different requirements.

10-2

Hub, Host Downstream Port, and Device Upstream Port Specification

Figure 10-2 shows the SuperSpeed portion of a USB hub consisting of a Hub Repeater/Forwarder section and a Hub Controller section.

The USB 2.0 portion of a USB hub shall meet all requirements of the USB 2.0 Specification unless specific exceptions are noted.

The SuperSpeed Hub Repeater/Forwarder is responsible for connectivity setup and tear-down. It also supports exception handling, such as bus fault detection and recovery and connect/disconnect detect. The SuperSpeed Hub Controller provides the mechanism for host-to-hub communication. Hub-specific status and control commands permit the host to configure a hub and to monitor and control its individual downstream facing ports.

![img-258.jpeg](img-258.jpeg)

Figure 10-2. SuperSpeed Portion of the USB Hub Architecture

10-3

Universal Serial Bus 3.1 Specification, Revision 1.0

As shown in Figure 10-3, the SuperSpeedPlus hub portion consists of three functional components: the SuperSpeedPlus Upstream Controller, the SuperSpeedPlus Downstream Controller and the SuperSpeedPlus Hub Controller. All subsequent references in this specification are to components of the Enhanced SuperSpeed hub unless otherwise noted.

The SuperSpeedPlus Upstream (SSP US) Controller is responsible for the behavior of the upstream port, buffering for packets being received from the upstream link, buffering and arbitrating packets waiting to be transmitted on the upstream link, and for routing packets to the appropriate downstream port's Downstream Controller (or to the hub controller).

The SuperSpeedPlus Downstream (SSP DS) Controller is responsible for the behavior of the downstream port, buffering for packets being received from the downstream link, buffering and arbitrating packets waiting to be transmitted on the downstream link and for routing packets to the Upstream Controller.

The SuperSpeedPlus Hub Controller provides the same mechanism for host-to-hub communication that the SuperSpeed Hub Controller does.

![img-259.jpeg](img-259.jpeg)

Figure 10-3. SuperSpeedPlus Portion of the Hub Architecture

Unlike USB peripheral devices, a USB hub connects upstream on both the Enhanced SuperSpeed bus and USB 2.0 bus. Connections may be enabled or disabled under the control of system software for a USB hub's downstream ports. If a USB hub upstream port is not connected on either USB 2.0 bus or Enhanced SuperSpeed bus, the hub does not provide power to the downstream ports unless it supports the USB Implementers Forum, Inc.'s Battery Charging Specification. Refer to Section 10.3.1.1 for a detailed discussion on when a hub is allowed to remove VBUS from a downstream facing port. This specification allows self-powered and bus-powered hubs.

10-4

Hub, Host Downstream Port, and Device Upstream Port Specification

The following sections present the typical flow for connection management in various types of systems for the simple topology shown in Figure 10-4 when the host system is first powered on.

Note: These connection examples outline cases where the system operates as expected. The handling of error cases are specified later in this chapter.

![img-260.jpeg](img-260.jpeg)

Figure 10-4. Simple USB Topology

### 10.1.1 Connecting to an Enhanced SuperSpeed Capable Host

When the host is powered off, the hub does not provide power to its downstream ports unless the hub supports charging applications (refer to Section 10.3.1.1).

When a hub is connected to a powered port and it detects Enhanced SuperSpeed connectivity, by default the following is the typical sequence of events:

- The upstream facing port will train at the fastest speed supported by its link partner as defined in the link chapter.
- Simultaneously, the hub powers its downstream ports and trains each link at the fastest speed supported by its link partner.
- If a downstream port trained at a higher speed than the upstream port then the downstream port shall retrain at a speed no faster than the upstream port.
- Hub connects both as an Enhanced SuperSpeed hub device and as a high-speed hub device.
- Host system begins hub enumeration at high-speed and Gen X speed.
- Host system begins device enumeration at Gen X speed.

10-5

Universal Serial Bus 3.1 Specification, Revision 1.0

### 10.1.2 Connecting to a USB 2.0 Host

When the host is powered off, the hub does not provide power to its downstream ports unless the hub supports charging applications (refer to Section 10.3.1.1).

When the host is powered on and there is no Gen X speed support, the following is the typical sequence of events:

- Hub detects VBUS and connects as a high-speed hub device.
- Host system begins hub enumeration at high-speed.
- Hubs power downstream ports when directed by software (USB 2.0) with Gen X connectivity disabled.
- Device connects at high-speed.
- Host system begins device enumeration at high-speed.

### 10.1.3 Hub Connectivity

Hubs exhibit different connectivity behavior depending on whether they are propagating data packet header/data packet payload traffic, other packet traffic, resume signaling, or are in an Idle state.

The hub contains one port that shall always connect in the upstream direction (referred to as the upstream facing port) and one or more downstream facing ports. Upstream connectivity/routing is defined as being towards the host and downstream connectivity/routing is defined as being towards a device.

There are differences in the packet connectivity/routing behavior for Enhanced SuperSpeed hubs operating at Gen 1 speed or at above Gen 1 speed.

Section 10.1.3.1 describes how a USB hub routes packets it receives. Section 10.1.3.2 describes the connectivity behavior for SuperSpeed hubs. Section 10.1.3.3 describes the packet routing behavior for SuperSpeedPlus hubs.

### 10.1.3.1 Routing Information

Packets received on the hub upstream port are routed based on information contained in a 20-bit field (Route String) in the packet header. The route string is used in conjunction with a hub depth value by the hub to identify the target port for a downstream directed packet. The hub depth value is assigned by software using the Set Hub Depth request. The hub shall ignore the route string and assume all packets are routed directly to the hub, until the hub enters the configured state and the hub's depth is set. The hub's upstream port shall be represented by port number zero while the downstream ports shall begin with port number one and count up sequentially.

The hub shall set the route string of upward flowing packets to;

- Zero, when the upward flowing packet was originated by the hub controller. These could be packets in response to a packet routed to the hub controller; e.g. DP in response to IN/ACK TP or packets such as an ERDY after a previous NRDY response by the hub controller.
- The route string value of a corresponding downward flowing packet, when the downward flowing packet has been marked as deferred by this hub controller.
- The aggregate arbitration weight of the hub, for a SuperSpeedPlus hub as described in Section 10.8.7.

10-6

Hub, Host Downstream Port, and Device Upstream Port Specification

Figure 10-5 illustrates the use of route strings in an example topology with five levels of four port USB hubs. The hub depth value for each level of hub is illustrated in the figure. Each hub and each device in the topology contains the route string that would be used to route a packet to that device/hub. For each hub depth, the octet in the route string that determines the routing target at that hub depth is shown in bold and a larger font size than the rest of the route string. The host root port is not included in the 20-bit route string.

![img-261.jpeg](img-261.jpeg)

Figure 10-5 Route String Example

10-7

Universal Serial Bus 3.1 Specification, Revision 1.0

### 10.1.3.2 SuperSpeed Hub Packet Signaling Connectivity

The SuperSpeed hub repeater/forwarder contains buffering for header and data packets. A SuperSpeed hub repeater/forwarder does not use the repeater-only model used for high-speed connectivity in a USB 2.0 hub. This change allows multiple downstream devices to send asynchronous messages simultaneously without data loss and for some traffic to be stored and delivered when it is directed to downstream ports when the links are not in U0.

Figure 10-6 shows the high level packet signaling connectivity behavior for SuperSpeed hubs in the upstream and downstream directions. Later sections describe the SuperSpeed hub internal buffering and connectivity in more detail. A SuperSpeed hub also has an Idle state, during which the SuperSpeed hub makes no connectivity. When in the Idle state, all of the SuperSpeed hub's ports (upstream plus downstream) are U1, U2 or in U0 receiving and transmitting logical idles waiting for the start of the next packet.

![img-262.jpeg](img-262.jpeg)

Figure 10-6. SuperSpeed Hub Signaling Connectivity

If a downstream facing port is enabled (i.e., in a state where it can propagate signaling through the hub) and the SuperSpeed hub detects the start of a packet on that port, the SuperSpeed hub begins to store the packet header. The SuperSpeed hub transmits the valid header packet received on the downstream port upstream, but not to any other downstream facing ports. This means that when a device operating at Gen 1 speed or a SuperSpeed hub transmits a packet upstream, only those SuperSpeed hubs in a direct line between the transmitting device and the host will see the packet.

All packets except Isochronous Timestamp Packets (ITP) are unicast in the downstream direction; SuperSpeed hubs operate using a direct connectivity model. This means that when the host or SuperSpeed hub transmits a packet downstream, only those SuperSpeed hubs in a direct line between the host and recipient device will see the packet.

10-8

Hub, Host Downstream Port, and Device Upstream Port Specification

### 10.1.3.3 SuperSpeedPlus Hub Packet Routing

The SuperSpeedPlus hub contains buffering for header and data packets. A SuperSpeedPlus hub does not use the repeater-only model used for high-speed connectivity in a USB 2.0 hub or the connectivity based repeater/forwarding model of a SuperSpeed hub. This change allows support for the additional features of SuperSpeedPlus operation.

If a downstream facing port is enabled (i.e., in a state where it can transmit and receive packets) and the hub detects the start of a packet on that port, the hub shall begin to store the packet header. The hub shall route the valid header packet received on the downstream port to the upstream port, but not to any other downstream facing ports. This means that when a device or a hub transmits a packet upstream, only those hubs in a direct line between the transmitting device and the host will see the packet.

All packets except Isochronous Timestamp Packets (ITP) are unicast in the downstream direction; hubs operate using a direct routing model. This means that when the host or hub transmits a packet downstream, only those hubs in a direct line between the host and recipient device will see the packet.

10-9

Universal Serial Bus 3.1 Specification, Revision 1.0

### 10.1.4 Resume Connectivity

Hubs exhibit different connectivity behaviors for upstream- and downstream-directed resume signaling. A hub does not propagate resume signaling from its upstream facing port to any of its downstream facing ports unless a downstream facing port is suspended and has received resume signaling since it was suspended. Figure 10-7 illustrates hub upstream and downstream resume connectivity.

![img-263.jpeg](img-263.jpeg)

Figure 10-7. Resume Connectivity

If a hub upstream port is suspended and the hub detects resume signaling from a suspended downstream facing port, the hub propagates that signaling upstream and does not reflect that signaling to any of the downstream facing ports (including the downstream port that originated resume signaling). If a hub upstream port is not suspended and the hub detects resume signaling from a suspended downstream facing port, the hub reflects resume signaling to the downstream port. Note that software shall not initiate a transition to U3 on the upstream port of a hub unless it has already initiated transitions to U3 on all enabled downstream ports. A detailed discussion of resume connectivity appears in Section 10.10.

### 10.1.5 Hub Fault Recovery Mechanisms

Hubs are the essential USB component for establishing connectivity between the host and other devices. It is vital that any connectivity faults be prevented if possible and detected in the unlikely event they occur.

Hubs must also be able to detect and recover from lost or corrupted packets that are addressed to the Hub Controller. Because the Hub Controller is, in fact, another USB device, it shall adhere to the same rules as other USB devices, as described in Chapter 8.

10-10

Hub, Host Downstream Port, and Device Upstream Port Specification

### 10.1.6 Hub Buffer Architecture

The buffering behaviors of an Enhanced SuperSpeed hub operating at Gen 1 or at above Gen 1 speeds are different. Section 10.1.6.1 summarizes the buffering behavior of the hub when operating at Gen 1 speed. Section 10.1.6.2 summarizes the buffering and arbitration behavior of the hub when operating at above Gen 1 Speed.

#### 10.1.6.1 SuperSpeed Hub Buffer Architecture

The SuperSpeed hub has header packet buffers associated with its upstream and downstream ports. It also has data packet payload (DPP) buffers for upstream and downstream data flows. See Section 10.7 or Section 10.7.4 for more details.

##### 10.1.6.1.1 SuperSpeed Hub Header Packet Buffer Architecture

Figure 10-8 shows the logical representation of a typical header packet buffer implementation for a SuperSpeed hub. Logically, a SuperSpeed hub has separate header packet buffers associated with each port for both upstream and downstream traffic. When a SuperSpeed hub receives a header packet on its upstream port, it routes the header packet to the appropriate downstream header packet buffer for transmission (unless the header packet is for the hub). When the SuperSpeed hub receives a non-LMP header packet on a downstream port, it routes the header packet to the upstream port header packet buffer for transmission. Header packets are kept in the SuperSpeed hub header packet buffers after transmission until link level acknowledgement (LGOOD_n) for the header packet is received. This allows the SuperSpeed hub to retry the header packets if necessary to ensure that header packets are received correctly at the link level. The header packet buffers also allow a SuperSpeed hub to store the header packets until they can be forwarded when the header packet is directed to a downstream link that is a low power link state. SuperSpeed hubs store the header packet and deliver it once the link becomes active.

![img-264.jpeg](img-264.jpeg)

![img-265.jpeg](img-265.jpeg)

U-146

Figure 10-8. Typical SuperSpeed Hub Header Packet Buffer Architecture

10-11

Universal Serial Bus 3.1 Specification, Revision 1.0

### 10.1.6.1.2 Hub Data Buffer Architecture

![img-266.jpeg](img-266.jpeg)

Figure 10-9. SuperSpeed Hub Data Buffer Traffic (Header Packet Buffer Only Shown for DS Port 1)

Figure 10-9 shows the logical representation of the data buffer architecture in a typical SuperSpeed hub. SuperSpeed hubs provide independent buffering for data packet payloads (DPP) in both the upstream and downstream directions. The Enhanced SuperSpeed Architecture allows concurrent transactions to occur in both the upstream and downstream directions. In the figure, two data packets are in progress in the downstream direction. The SuperSpeed hub can store more than one data packet payload at the same time. In rare occurrences where data packet payloads are discarded because buffering is unavailable, the end-to-end protocol will recover by retrying the transaction. The isochronous protocol does not include retries. However, discard errors are expected less frequently then bit errors on the physical bus.

Note: Data packet headers are stored and handled in the same fashion as other header packet packets using the header packet buffers. DPPs are handled using the separate data buffers.

### 10.1.6.2 SuperSpeedPlus Hub Buffer Architecture

The SuperSpeedPlus hub has significantly more data packet header (DPH) and data packet payload (DPP) buffering than a SuperSpeed hub. Downstream ports can operate at a different speed than the upstream port and there can be multiple DPs simultaneously in transit on different downstream ports-. Therefore, DPs may have to be buffered until they can be transmitted out of the hub. Since there can be multiple DPs buffered in a hub awaiting transmission on a port, the SuperSpeedPlus hub also has local arbitration rules to select the packet to be transmitted next on a port. There are specific buffering requirements for upstream and downstream traffic. See Section 10.8 for more details.

10-12

Hub, Host Downstream Port, and Device Upstream Port Specification

## 10.2 Hub Power Management

### 10.2.1 Link States

The hub is required to support U0, U1, U2, and U3 on all ports (upstream and downstream).

### 10.2.2 Hub Downstream Port U1/U2 Timers

The hub is required to have inactivity timers for both U1 and U2 on each downstream port. The timeout values are programmable and may be set by the host software. A timeout value of zero means the timer is disabled. The default value for the U1/U2 timeouts is zero. The U1 and U2 timeout values for all downstream ports reset to the default values on PowerOn Reset or when the hub upstream port is reset. The U1 and U2 timeout values for a downstream port reset to the default values when the port receives a SetPortFeature request for a port reset. The downstream port state machines presented in this chapter describe the specific operational rules when U1 and/or U2 timeouts are enabled.

- Hub downstream ports shall accept U1 or U2 entry initiated by a link partner except when the corresponding U1/U2 timeout is set to zero or there is pending traffic directed to the downstream port.
- If a hub has received a valid packet on its upstream port that is routed to a downstream port, it shall reject U1 or U2 link entry attempts on the downstream port until the packet has been successfully transmitted. A hub may also reject U1 or U2 link entry attempts on downstream ports if the hub is receiving a packet but has not determined the packet's destination. A hub implementation shall ensure no race condition exists where a header packet that has not been deferred is queued for transmission on a downstream port with a link that is in U1, U2, or is in the process of entering U1, U2.
- Hub downstream ports shall reject all U1 and U2 entry requests if the corresponding timeout is set to zero.
- The hub inactivity timers for U1 and U2 shall not be reset by an Isochronous Timestamp Packet (ITP).

10-13

Universal Serial Bus 3.1 Specification, Revision 1.0

### 10.2.3 Downstream/Upstream Port Link State Transitions

The hub shall evaluate the link power state of its downstream ports such that it propagates the highest link state of any of its downstream ports to its upstream port when there is no pending upstream traffic. U0 is the highest link state, followed by U1, then U2, then U3, then Rx.Detect, and then eSS.Disabled. The order of the other link states is undefined and implementation dependent. If an upstream port link state transition would result in an upstream port link state that has been disabled by software, the hub shall transition the upstream port link to the next highest U-state that is enabled. The hub never automatically attempts to transition the hub upstream port to U3 or lower state.

The downstream port state machines presented in this chapter provide the specific timing requirements for changing the upstream port link state in response to downstream port link state changes.

The hub also shall initiate a link state transition on the appropriate downstream port whenever it receives a packet that is routed to downstream port that is not in U0. The hub upstream port state machines provided in this chapter provide the specific timing requirements for these transitions.

If enabled, port status change interrupts, e.g., due to a connect event on a downstream port, will cause the upstream link to initiate a transition to U0.

### 10.3 Hub Downstream Facing Ports

The following sections provide a functional description of a state machine that exhibits the correct required behavior for a downstream facing port.

Figure 10-10 is an illustration of the downstream facing port state machine. Each of the states is described in Section 10.4.2. In the diagram below, some of the entry conditions into states are shown without origin. These conditions have multiple origin states and the individual transitions lines are not shown to simplify the diagram. The description of the entered state indicates from which states the transition is applicable.

# NOTE

For the root hub, the signals from the upstream facing port state machines are implementation dependent.

10-14

Hub, Host Downstream Port, and Device Upstream Port Specification

![img-267.jpeg](img-267.jpeg)

Port Status Field:

Notation Field Name

PP PORT_POWER

CCS PORT_CONNECTION

PR PORT_RESET

PLS PORT_LINK_STATE

PE PORT_ENABLE

Note:

Clear Port Feature (PORT_ENABLED) and Set Port Feature (PORT_ENABLED) are not used for SS Ports

1 This direct transition may only occur from a DSPORT state whose link is in the SS.Inactive, Rx.Detect.Active (during DSPORT.RESETTING), U1, U2, or U3 state.

Figure 10-10. Downstream Facing Hub Port State Machine

10-15

Universal Serial Bus 3.1 Specification, Revision 1.0

Table 10-1. Downstream Facing Hub Port State Machine Diagram Legend

[tbl-200.md](tbl-200.md)

10-16

Hub, Host Downstream Port, and Device Upstream Port Specification

[tbl-201.md](tbl-201.md)

### 10.3.1 Hub Downstream Facing Port State Descriptions

#### 10.3.1.1 DSPORT.Powered-off

The DSPORT.Powered-off state is a logical powered off state. This is a default state where DSPORT port will be after power-up if the hub supports power switching. The hub may still be required or choose to provide VBUS for a downstream port in the DSPORT.Powered-off state. Detailed requirements for presence of VBUS are covered later in this section.

A port shall transition into this state if any of the following situations occur:

- From any state when VBUS is removed from the hub upstream port and the hub supports power switching on the DS ports.
- Any "power-off" condition is met:
  - From any state when local power is lost to the port.
  - From any state if the hub's upstream port link transitions to the eSS.Disabled state and Upstream PORT VBUS is on.
  - From any state if the hub's upstream port link has attempted eight consecutive Rx.Detect events without detecting far-end receiver terminations and the receiver termination (near-end) of the hub's downstream port is ready to be turned off.

The downstream port's termination is considered to be ready to turn off when any of following conditions is met.

- Warm reset signaling has completed.
- The port is power switched.
- The port is in a powered on state and not performing a warm reset
- No device is connected.

A port shall remain in the DSPORT.Powered-off state until the following conditions are met.

- The hub's Upstream Port link has detected far-end receiver terminations. Note that this requires Upstream Port VBUS to be on.
- No "power-off" condition is true.
- No Overcurrent condition is active.

If a hub was configured while the local power supply was present and then if local power is lost, the hub shall place all ports in the Powered-off state if power remains to run the hub controller.

In the DSPORT.Powered-off state, the port's link is in the eSS.Disabled state.

Table 10-2 shows the allowed state of VBUS for hub downstream ports for possible states of the hub upstream port and logical port power for a downstream port. The table covers the case where the hub has adequate power to provide power for the downstream ports (local power source is present). For a hub that does not implement per port power control, all downstream ports that will be affected by removing VBUS shall be in a state where power may be off (refer to Table 10-2) before the hub removes VBUS.

Note: a hub may provide power to all its downstream ports all of the time to support applications such as battery charging from a USB port. Such hubs must ensure that Enhanced SuperSpeed

10-17

Universal Serial Bus 3.1 Specification, Revision 1.0

devices on its downstream-facing ports attempt Enhanced SuperSpeed connection once upstream VBUS is seen by the hub. The recommended method to achieve this is to cycle VBUS off for a duration or by actively discharging so that it is seen to be off by the downstream device.

Table 10-2. Downstream Port VBUS Requirements

[tbl-202.md](tbl-202.md)

* If the hub upstream port is unable to connect on the USB 2.0 bus, the downstream port VBUS may be off in this state.

### 10.3.1.2 DSPORT.Disconnected (Waiting for eSS Connect)

A port transitions to this state in any of the following situations:

- From the DSPORT.Powered-off state when the hub's Upstream Port link has detected far-end receiver terminations, Upstream Port VBUS is on (implied by receiver detection), no power-off condition is met and no overcurrent condition exists.
- From any state that can and does detect a disconnect, except from DSPORT.Powered-off-detect.
- From the DSPORT.Powered-off-reset state when conditions for Repowering defined in Section 10.3.1.10 are met and the DSPORT.Powered-off-reset state has been maintained for tReset.
- From the DSPORT.Powered-off-detect state when conditions for Repowering defined in Section 10.3.1.10 are met.
- From the DSPORT.Resetting state when a port's link times out from Rx.Detect.Active during a reset. That is, it detects a disconnect.
- From the DSPORT.Disabled state when a SetPortFeature(PORT_LINK_STATE) Rx.Detect request is received for the port.
- From the DSPORT.Disabled state when the hub's upstream port is reset. Note: The hub shall issue a Warm Reset on the downstream port, if a device is detected in the first Rx.Detect after entering this state, even if the upstream port reset is a hot reset.
- From the DSPORT.Powered-off state or DSPORT.Disabled state when the hub's upstream port is reset. Note: The hub shall issue a Warm Reset on the downstream port after it has transitioned the port to the DSPORT.RxDetect state and detected a far-end receiver, even if the upstream port reset is a hot reset
- From the DSPORT.Resetting state if the port's link times out from any Polling substate during a reset.
- From the DSPORT.Training state if the port's link times out from any Polling substate and the cPollingTimeout is less than 2 and the port is not enabled to enter compliance or Polling

10-18

Hub, Host Downstream Port, and Device Upstream Port Specification

substate which timed out is not Polling.LFPS. See definition of PollingTimeout in Section 7.5.4.2 and Section 10.16.2.10 defining Set Port Feature for enabling compliance entry.

- From the DSPORT.Loopback state if the port's link performs a successful LFPS handshake in Loopback.Exit.

In this state, the port's link shall be in the Rx.Detect state.

Note: The port's link shall still perform connection detection normally from the Rx.Detect if the hub upstream port's link is in U3.

### 10.3.1.3 DSPORT.Training

A port transitions to this state from the DSPORT.Disconnected state when far-end receiver terminations are detected.

In this state, the port's link shall be in the Polling state.

### 10.3.1.4 DSPORT.ERROR

A port shall transition to this state only when an Enhanced SuperSpeed device is connected and a serious error condition occurred while attempting to operate the link.

A port transitions to this state in any of the following situations:

- From the DSPORT.Enabled state if the link enters recovery and times out without recovering.
- From the DSPORT.Enabled state if U1 or U2 exit fails.
- From the DSPORT.Loopback state if the port is the loopback master and the LFPS handshake in Loopback.Exit fails.
- From DSPORT.Enabled if Port Configuration fails as described in Section 8.4.6.
- From the DSPORT.Training state if the port's link times out from any Polling substate and cPollingTimeout is 2. See 7.5.4.2 for details of SetioncPollingTimeout.

In this state, the port's link shall be in the eSS.Inactive state.

### 10.3.1.5 DSPORT.Enabled

A port transitions to this state in any of the following situations:

- From the Training state when the port's link successfully enters U0.
- From the DSPORT.Resetting state when a reset completes successfully.

A port in the DSPORT.Enabled state will propagate packets in both the upstream and the downstream direction after its Current Connect Status (CCS) is set. When the hub downstream port first transitions to the DSPORT.Enabled state after a power on or warm reset, it shall transmit a port configuration LMP as defined in Section 8.4.6. If CCS was set before entering the DSPORT.Enabled state, it will remain set. If CCS was not set, then it shall be set only after the port configuration LMP exchange succeeds.

When the hub downstream port first transitions to the DSPORT.Enabled state after a power on reset, the value for the U1 and U2 inactivity timers shall be reset to zero.

The link shall be in U0 when the enabled state is entered.

If the hub upstream port's link is in U3 when the downstream port enters DSPORT.Enabled and the hub is not enabled for remote wakeup, the downstream port shall initiate a transition to U3 on its link within tDSPortEnabledToU3.

Section 10.4 provides a state machine that shows a functionally correct implementation for a downstream port managing different link states within the DSPORT.Enabled state.

10-19

Universal Serial Bus 3.1 Specification, Revision 1.0

### 10.3.1.6 DSPORT.Resetting

A downstream port transitions to the DSPORT.Resetting state in any of the following situations:

- From the DSPORT.Error state when a SetPortFeature(PORT_RESET) request or SetPortFeature(BH_PORT_RESET) is received, the port shall send a warm reset on the downstream port link.
- From the DSPORT.Enabled state and the port's link is in any state when a SetPortFeature(BH_PORT_RESET) is received. In this situation the port shall initiate a Warm Reset on the downstream port link.
- From any state except for DSPORT-Powered-off-reset or DSPORT-Powered-off-detect or DSPORT-Powered-off or DSPORT.Disabled or DSPORT.Disconnected if the hub detects a Reset on its Upstream Port. In this situation, the port shall initiate a Hot/Warm Reset on the downstream port link depending on the type of Reset detected on the hub's upstream port and depending on the current state of the downstream port. This transition shall occur before the upstream port link transitions to U0.
- From any state except for DSPORT-Powered-off, DSPORT-Powered-off-reset, DSPORT-Powered-off-detect, DSPORT.Disabled or DSPORT.Disconnected when it receives a SetPortFeature(PORT_RESET) or SetPortFeature(BH_PORT_RESET). If the downstream port is in the DSPORT-Powered-off, DSPORT-Powered-off-reset, DSPORT-Powered-off-detect, DSPORT.Disabled or DSPORT.Disconnected state and it receives one of the above requests, the request is ignored.
- From the DSPORT.Enabled state and the port's link state is in any state other than U3 when a SetPortFeature(PORT_RESET) is received. In this situation the port shall initiate a Hot Reset on the downstream port link.
- From the DSPORT.Enabled state and the port's link state is in U3 when a SetPortFeature(PORT_RESET) is received. In this situation the port shall initiate a Warm Reset on the downstream port link.

Note: If the port initiates a hot reset on the link and the hot reset fails during the link Recovery state, a warm reset will be automatically tried. Refer to the Link Chapter for details on this process. The port stays in the DSPORT.Resetting state throughout this process until the warm reset completes.

When the downstream port link enters Rx.Detect.Active during a warm reset, the hub shall start a timer to count the time it is in Rx.Detect.Active or Rx.Detect.Quiet. If this timer exceeds tTimeForResetError while the link remains in Rx.Detect, the port shall transition to the DSPORT.Disconnected state.

### 10.3.1.7 DSPORT.Compliance

A port transitions to this state in any of the following situations:

- When the link enters the Compliance Mode state.

### 10.3.1.8 DSPORT.Loopback

A port transitions to this state in any of the following situations:

- From the DSPORT.Training state if the loopback bit is set in the received TS2 ordered sets.

In this state, the port's link shall be in the Loopback state.

10-20

Hub, Host Downstream Port, and Device Upstream Port Specification

### 10.3.1.9 DSPORT.Disabled

A port transitions to this state when the port receives a SetPortFeature(PORT_LINK_STATE) eSS.Disabled request.

In this state, the port's link shall be in the eSS.Disabled state.

### 10.3.1.10 DSPORT.Powered-off-detect

This state is entered when the downstream power state is logically off and an Enhanced SuperSpeed connection, rather than a USB 2.0 connection, is desired. To ensure that an Enhanced SuperSpeed connection is established, unlike the DSPORT.Powered-off state, terminations are maintained while in this state. This is the default DSPORT state at power-up if the hub does not support power switching. This state shall perform far-end receiver detection with the link in Rx.Detect, until any of the following conditions are true:

- A receiver is detected.
- Any condition to "power-off" is met.
- The conditions to "repower" the port as described below are met.

A port shall transition into this state from the DSPORT.Powered-off-reset state when tReset time has been met and the conditions to "repower" are not met.

All the following conditions shall be met for "repower":

- All "power" conditions are met.
- SetPortFeature(PORT_POWER) request is received,
  Or SetConfig(1) request is received,
  Or Upstream Port Reset is detected,
  Or Upstream Port VBUS transitioned from off to on.

Note that Upstream Port VBUS is considered to have transitioned from off to on when it is on at power-up.

When no "power-off" condition is met and any of the following conditions are true, this state is entered regardless of the previous state.

- Overcurrent condition is detected either on this port or globally and Upstream Port Far-end Receiver Terminations are present and Upstream VBUS is on. Note: If Upstream VBUS is turned off while overcurrent is active port transitions to Powered-off state immediately (without waiting for tReset to complete) if ds power switches are supported.
- Upstream Port VBUS is off and the hub does not support power switching.
- The hub receives a ClearPortFeature(PORT_POWER) request for this port. In this case, power is removed from the port only if it would not impact the low-speed, full-speed, or high-speed operation on any of the downstream ports on the hub and would not impact SS operation on any ports other than the target port.
- The hub upstream port receives a SetConfiguration(0) request. In this case the downstream port will stay in this state or transition between this state and DSPORT.Powered-off-reset state regardless of other conditions until the hub is reset or the hub upstream port receives a non-zero SetConfiguration request.

10-21

Universal Serial Bus 3.1 Specification, Revision 1.0

### 10.3.1.11 DSPORT.Powered-off-reset

This state is entered when the downstream power state is logically off and an Enhanced SuperSpeed connection, rather than a USB 2.0 connection, is desired. To ensure that an Enhanced SuperSpeed connection is established, unlike the DSPORT.Powered-off state, the terminations are maintained while in this state, and to avoid a link training failure, which would allow the downstream device to drop into Compliance Mode or USB 2.0 operation, Warm Reset signaling shall be driven for tReset duration. This state shall drive Warm Reset with the link in the Rx.Detect.Reset substate, until the tReset duration is met.

This state is entered from DSPORT.Powered-off-detect whenever a far end receiver is detected.

### 10.3.2 Disconnect Detect Mechanism

Disconnect detection mechanisms are covered in Section 7.5.

### 10.3.3 Labeling

USB system software uses port numbers to reference an individual port with a ClearPortFeature or SetPortFeature request. If a vendor provides a labeling to identify individual downstream facing ports, then each port connector shall be labeled with its respective port number. The port numbers assigned to a specific port by the hub shall be consistent between the USB 2.0 hub and Enhanced SuperSpeed hub.

### 10.4 Hub Downstream Facing Port Power Management

The following sections provide a functional description of a state machine that exhibits correct link power management behavior for a downstream facing port.

Figure 10-11 is an illustration of the downstream facing port power management state machine. Each of the states is described in Section 10.4.2. In Figure 10-11, some of the entry conditions into states are shown without origin. These conditions have multiple origin states and the individual transitions lines are not shown so that the diagram can be simplified. The description of the entered state indicates from which states the transition is applicable.

### 10.4.1 Downstream Facing Port PM Timers

Each downstream port maintains logical inactivity timers for keeping track of when U1 and U2 timeouts are exceeded. The U1 or U2 timeout values may be set by software with a SetPortFeature(PORT_U1_TIMEOUT) or SetPortFeature(PORT_U2_TIMEOUT) command at any time. The PM timers are reset to 0 every time a SetPortFeature(PORT_U1_TIMEOUT) or SetPortFeature(PORT_U2_TIMEOUT) request is received. The timers shall be reset every time a packet of any type except an isochronous timestamp packet is sent or received by the port's link. The U1 timer shall be accurate to +1/-0 μs. The U2 timer shall be accurate to +500/-0 μs. Other requirements for the timer are defined in the downstream port PM state machine descriptions.

10-22

Hub, Host Downstream Port, and Device Upstream Port Specification

![img-268.jpeg](img-268.jpeg)

Figure 10-11. Downstream Facing Hub Port Power Management State Machine

10-23

Universal Serial Bus 3.1 Specification, Revision 1.0

### 10.4.2 Hub Downstream Facing Port State Descriptions

#### 10.4.2.1 Enabled U0 States

There are four enabled U0 states that differ only in the values that are configured for the U1 and U2 timeouts. The port behaves as follows for the various combinations of U1 and U2 timeout values:

U1_TIMEOUT = 0, U2_TIMEOUT = 0

- This is the default state before the hub has received any SetPortFeature(PORT_U1/U2_TIMEOUT) requests for the port.
- The port's link shall reject all U1 or U2 transition requests by the link partner.
- The PM timers may be disabled and the PM timer values shall be ignored.
- The port's link shall not attempt to initiate transitions to U1 or U2.

U1_TIMEOUT = X > 0, U2_TIMEOUT = 0

- The port's link shall reject all U2 transition requests by the link partner.
- The PM timers shall be reset when this state is entered and is active.
- The port's link shall accept U1 entry requests by its link partner unless the hub has one or more packets/link commands to transmit on the port.
- If the U1 timeout is 0xFF, the port shall be disabled from initiating U1 entry but shall accept U1 entry requests by the link partner unless the hub has one or more packets/link commands to transmit on the port.
- If the U1 timeout is not 0xFF and the U1 timer reaches X, the port's link shall initiate a transition to U1.

U1_TIMEOUT = 0, U2_TIMEOUT = Y > 0

- The port's link shall reject all U1 transition requests by the link partner.
- The PM timers shall be reset when this state is entered and is active.
- The port's link shall accept U2 entry requests by its link partner unless the hub has one or more packets/link commands to transmit on the port.
- If the U2 timeout is 0xFF, the port shall be disabled from initiating U2 entry but shall accept U2 entry requests by the link partner unless the hub has one or more packets/link commands to transmit on the port.
- If the U2 timeout is not 0xFF and the U2 timer reaches Y, the port's link shall initiate a direct transition from U0 to U2. In this case, PORT_U2_TIMEOUT represents an amount of inactive time in U0.

U1_TIMEOUT = X > 0, U2_TIMEOUT = Y > 0

- The PM timers are reset when this state is entered and is active.
- The port's link shall accept U1 or U2 entry requests by its link partner unless the hub has one or more packets/link commands to transmit on the port.
- If the U1 timeout is 0xFF, the port shall be disabled from initiating U1 entry but shall accept U1 entry requests by the link partner unless the hub has one or more packets/link commands to transmit on the port.
- If the U1 timeout is not 0xFF and the U1 timer reaches X, the port's link shall initiate a transition to U1.

10-24

Hub, Host Downstream Port, and Device Upstream Port Specification

- If the U2 timeout is 0xFF, the port shall be disabled from initiating U2 entry but shall accept U2 entry requests by the link partner unless the hub has one or more packets/link commands to transmit on the port.

A port transitions to one of the Enabled U0 states (depending on the U1 and U2 Timeout values) in any of the following situations:

- From any state if the hub receives a SetPortFeature(PORT_LINK_STATE) U0 request.
- From U1 if the link partner successfully initiates a transition to U0.
- From U2 if the link partner successfully initiates a transition to U0.
- From U1 if the hub successfully initiates a transition to U0 after receiving a packet routed to the port.
- From U2 if the hub successfully initiates a transition to U0 after receiving a packet routed to the port
- From an attempt to transition from the U0 to the U1 state if the downstream port's link partner rejects the transition attempt
- From an attempt to transition from the U0 to the U2 state if the downstream port's link partner rejects the transition attempt
- From U3 if the upstream port of the hub receives wakeup signaling and the hub downstream port being transitioned received wakeup signaling while it was in U3.
- From U3 if the downstream port's link partner initiated wake signaling and the upstream hub port's link is not in U3.

Note: Refer to Section 10.1.4 for details on cases where a downstream port's link partner initiates remote wakeup signaling.

### 10.4.2.2 Attempt U0 – U1 Transition

In this state, the port attempts to transition its link from the U0 state to the U1 state.

A port shall attempt to transition to the U1 state in any of the following situations:

- The U1 timer reaches the U1 timeout value.
- The hub receives a SetPortFeature(PORT_LINK_STATE) U1 request.
- The downstream port's link partner initiates a U0-U1 transition.

If the transition attempt fails, the port returns to the appropriate enabled U0 state. However, if this state was entered due to a SetPortFeature request, the port continues to attempt the U0-U1 transition on its link.

Note: that the SetPortFeature request is typically only used for U1 entry for test purposes.

### 10.4.2.3 Attempt U0 – U2 Transition

In this state, the port attempts to transition the link from the U0 state to the U2 state.

A port shall attempt to transition to the U2 state in any of the following situations:

- The U2 timer reaches the U2 timeout value.
- The hub receives a SetPortFeature(PORT_LINK_STATE) U2 request.
- The downstream port's link partner initiates a U0-U2 transition.

If the transition attempt fails, the port returns to the appropriate enabled U0 state. However, if this state was entered due to a SetPortFeature request, the port continues to attempt the U0-U2 transition.

10-25

Universal Serial Bus 3.1 Specification, Revision 1.0

Note: that the SetPortFeature request is typically only used for U2 entry for test purposes.

### 10.4.2.4 Link in U1

Whenever a downstream port enters U1 and all downstream ports are now in the U1 or a lower power state, the hub shall initiate a transition to U1 on the upstream port within tHubPort2PortExitLat if the upstream port is enabled for U1.

The U2 timer is reset to zero and started when the Link enters U1.

If the U2 timeout is not 0xFF and the U2 timer reaches Y, the port's link shall initiate a direct transition from U1 to U2. In this case, PORT_U2_TIMEOUT represents an amount of time in U1.

Whenever a downstream port or its link partner initiates a transition from U1 to one of the Enabled U0 states and the upstream port is not in U0, the hub shall initiate a transition to U0 on the upstream port within tHubPort2PortExitLat of when the transition was initiated on the downstream port. If the upstream port is in U0, it shall remain in U0 while the downstream port transitions to U0.

### 10.4.2.5 Link in U2

The following rules apply when a downstream port enters U2:

- If all downstream ports are now in the U2 or a lower power state, the hub shall initiate a transition to U2 on the upstream port within tHubPort2PortExitLat, if the upstream port is enabled for U2. If U2 is not enabled on the upstream port, but U1 is enabled, the hub shall initiate a transition to U1 with the same timing requirements.
- If all downstream ports are now in the U1 or lower power state, the hub shall initiate a transition to U1 on the upstream port within tHubPort2PortExitLat, if the upstream port is enabled for U1.

Whenever a downstream port or its link partner initiates a transition from U2 to one of the Enabled U0 states and the hub upstream port is not in U0:

- If the hub upstream port's link is in U2, the hub shall initiate a transition to U0 on the upstream port's link within tHubPort2PortExitLat of when the transition was initiated on the downstream port.
- If the hub upstream port's link is in U1, the hub upstream port shall initiate a transition to U0 within tHubPort2PortExitLat + U2DevExitLat-U1DevExitLat of when the transition was initiated on the downstream port.

### 10.4.2.6 Link in U3

The following rules apply when a downstream port enters U3:

- If all downstream ports are now in the U2 or U3, the hub shall initiate a transition to the lowest enabled power state above U3 on the upstream port within tHubPort2PortExitLat.
- If all downstream ports are now in the U1 or lower power state, the hub shall initiate a transition to U1 on the upstream port within tHubPort2PortExitLat, if the upstream port is enabled for U1.

Refer to Section 10.3.1.5 for a detailed description of the transition from Enabled – U0 Only to the U3 state.

Note: If the upstream port of the hub receives a packet that is routed to a downstream port that is in U3, the packet is silently discarded. The hub shall perform normal link level acknowledgement of the header packet in this case.

10-26

Hub, Host Downstream Port, and Device Upstream Port Specification

## 10.5 Hub Upstream Facing Port

The following sections provide a functional description of a state machine that exhibits correct behavior for a hub upstream facing port. These sections also apply to the upstream facing port on a device unless exceptions are specifically noted. An upstream port shall only attempt to connect to the Enhanced SuperSpeed bus and the USB 2.0 bus as described by the upstream port state machine in the following sections.

Figure 10-12 is an illustration of the upstream facing port state machine. Each of the states is described in Section 10.5.1. In Figure 10-12, some of the entry conditions into states are shown without origin. These conditions have multiple origin states and the individual transitions lines are not shown so that the diagram can be simplified. The description of the entered state indicates from which states the transition is applicable.

10-27

Universal Serial Bus 3.1 Specification, Revision 1.0

![img-269.jpeg](img-269.jpeg)

¹ If Port Configuration fails, the port shall transition to the USPORT.Powered-off state with the link in eSS.Disabled state and USB Device in the Attached state. V_BUS may still be present on the upstream port. V_BUS must be toggled to transition to the USPORT.Powered state.

U-150A

Figure 10-12. Upstream Facing Hub Port State Machine

### 10.5.1 Upstream Facing Port State Descriptions

Refer to Figure 9-1 for hub USB states.

#### 10.5.1.1 USPORT.Powered-off

The USPORT.Powered-off state is the default state for an upstream facing port.

A port shall transition into this state if any of the following situations occur:

10-28

Hub, Host Downstream Port, and Device Upstream Port Specification

- From any state when VBUS is invalid.
- From any state if far-end receiver terminations are not detected.
- From the USPORT.Connected/Enabled state if the Port Configuration process fails.

In this state, the port's link shall be in the eSS.Disabled state and the corresponding hub USB state shall be Attached.

Note: If the port enters this state because far end receiver terminations are not detected and VBUS is present, it may immediately transition to USPORT.Powered on without removing near end terminations.

### 10.5.1.2 USPORT.Powered-on

A port shall transition into this state in any of the following situations:

- From the USPORT.Powered-off state when VBUS becomes valid.
- From the USPORT.Error state when the link receives a warm reset or if Far-end Terminations are removed.
- From the USPORT.Connected/Enabled state when the link receives a Warm Reset.
- From the USPORT.Training state if the port's link times out from any Polling substate or if the port receives a Warm (LFPS) Reset.

In this state, the port's link shall be in the Rx.Detect state. The corresponding hub USB state shall be Powered (Far-end Receiver Termination substate). While in this state, if the USB 2.0 portion of the hub enters the suspended state, the total hub current draw from VBUS shall not exceed the suspend current limit.

### 10.5.1.3 USPORT.Training

A port transitions to this state from the USPORT.Powered-on state when Enhanced SuperSpeed far-end receiver terminations are detected.

In this state, the port's link shall be in the Polling state. The corresponding hub USB state shall be Powered (Link Training substate).

### 10.5.1.4 USPORT.Connected/Enabled

A port transitions to this state from the USPORT.Training state when its link enters U0 from Polling.Idle. A port remains in this state during hot reset. When a hot reset is completed, the corresponding hub USB state shall transition to Default.

In this state, the port's link shall be in the U0, U1, U2, U3, or Recovery state. The corresponding hub USB state shall be Default, Address, or Configured.

When the link enters U0 the port shall start the port configuration process as defined in Section 8.4.6.

The port may send link management packets or link commands but shall not transmit any other packets except to respond to default control endpoint requests while in the USPORT.Connected state.

### 10.5.1.5 USPORT.Error

A port transitions to this state when a serious error condition occurred while attempting to operate the link. A port transitions to this state in any of the following situations:

10-29

Universal Serial Bus 3.1 Specification, Revision 1.0

- From the USPORT.Connected/Enabled state if the link enters Recovery and times out without recovering.

In this state, the port's link shall be in the eSS.Inactive state. The corresponding hub USB state shall be Error.

A port exits the Error state only if a Warm Reset is received on the link or if Far-end Receiver Terminations are removed.

### 10.5.2 Hub Connect State Machine

The following sections provide a functional description of a state machine that exhibits correct hub behavior for when to connect on the Enhanced SuperSpeed bus or the USB 2.0 bus. For a hub, the connection logic for the Enhanced SuperSpeed bus and the USB 2.0 bus are completely independent. The hub shall follow the USB 2.0 specification for connecting on USB 2.0. Figure 10-13 is an illustration of the hub connect state machine for an Enhanced SuperSpeed hub. Each of the states is described in Section 10.5.2.1.

![img-270.jpeg](img-270.jpeg)

Figure 10-13. Hub Connect (HCONNECT) State Machine

### 10.5.2.1 Hub Connect State Descriptions

### 10.5.2.2 HCONNECT.Powered-off

The HCONNECT.Powered-off state is the default state for a hub device. A hub device shall transition into this state if the following situation occurs:

- From any state when VBUS is removed.

In this state, the hub upstream port's link shall be in the eSS.Disabled state.

10-30

Hub, Host Downstream Port, and Device Upstream Port Specification

### 10.5.2.3 HCONNECT.Attempt ESS Connect

A hub shall transition into this state if any of the following situations occur:

- From the HCONNECT-Powered-off state when VBUS becomes valid (and local power is valid if required).
- From the HCONNECT.Connected on ESS state if Rx.Detect or Link Training time out.

In this state, the hub's upstream port Enhanced SuperSpeed link is in Rx.Detect or Polling.

### 10.5.2.4 HCONNECT.Connected on ESS

A port shall transition into this state if the following situation occurs:

- From the HCONNECT.Attempt ESS Connect when the link transitions from polling to U0.

In this state the hub's upstream port Enhanced SuperSpeed link is in U0, U1, U2, U3, Inactive, Rx.Detect, Recovery, or Polling.

## 10.6 Upstream Facing Port Power Management

The following sections provide a functional description of a state machine that exhibits correct link power management behavior for a hub upstream facing port.

Figure 10-14 is an illustration of the upstream facing port power management state machine. Each of the states is described in Section 10.6.2. In Figure 10-14, some of the entry conditions into states are shown without origin. These conditions have multiple origin states and the individual transitions lines are not shown so that the diagram can be simplified. The description of the entered state indicates from which states the transition is applicable.

If there is a status change on any downstream port, the hub shall initiate a transition on the upstream port's link to U0 if the upstream port is in U1 or U2.

If there is a status change on any downstream port and the hub upstream port's link is in U3, the hub behavior is specified by the current remote wakeup mask settings. Refer to Section 10.16.2.10 for more details.

10-31

Universal Serial Bus 3.1 Specification, Revision 1.0

![img-271.jpeg](img-271.jpeg)

Figure 10-14. Upstream Facing Hub Port Power Management State Machine

10-32

Hub, Host Downstream Port, and Device Upstream Port Specification

### 10.6.1 Upstream Facing Port PM Timer

The hub upstream port maintains a logical PM timer for keeping track of when the U2 inactivity timeout is exceeded. No standard U1 inactivity timeout is defined. The U2 inactivity timeout is set when a U2 Inactivity Timeout LMP is received. The PM timer is reset when the hub upstream port link enters U1. The PM timer shall be accurate to +500/-0 µs. Other requirements for the timer are defined in the upstream port PM state machine descriptions.

### 10.6.2 Hub Upstream Facing Port State Descriptions

#### 10.6.2.1 Enabled U0 States

There are four enabled U0 states that differ only in the U1 and U2 Enable settings. The following rules apply globally to all Enabled U0 states:

- The upstream port shall not initiate a transition to U1 or U2 if there are pending packets to transmit on the upstream port.
- The upstream port shall accept U1 or U2 transitions from the link partner if the Force_LinkPM_Accept bit is set to one (refer to Section 8.4.2).

The port behaves as follows for the various combinations of U1 and U2 Enable values:

U1_ENABLE = 0, U2_ENABLE = 0

- This is the default state before the hub has received any SetFeature(U1/U2_ENABLE) requests.
- The PM timer may be disabled and the PM timer values shall be ignored.
- The port's link shall accept U1 entry requests by its link partner unless the hub has one or more packets/link commands to transmit on the port or one or more of the hub downstream ports has a link in U0 or recovery.
- The port's link shall accept U2 entry requests by its link partner unless the hub has one or more packets/link commands to transmit on the port or one or more of the hub downstream ports has a link in U0, U1, or recovery.
- The port's link shall not attempt to initiate transitions to U1 or U2.

U1_ENABLE = 1, U2_ENABLE = 0

- The port's link shall not initiate a U2 transition.
- The port's link shall accept all U2 entry requests by the link partner unless the hub has one or more packets/link commands to transmit on the port or one or more of the hub downstream ports has a link in U0, U1 or recovery.
- The port's link shall accept U1 entry requests by its link partner unless the hub has one or more packets/link commands to transmit on the port or one or more of the hub downstream ports has a link in U0 or recovery.
- The PM timer may be disabled and the PM timer values shall be ignored.
- The port's link shall initiate a transition to U1 if all the hub downstream ports are in U1 or a lower link state.

U1_ENABLE = 0, U2_ENABLE = 1

- The port's link shall not initiate a U1 transition.
- The port's link shall accept all U1 entry requests by the link partner unless the hub has one or more packets/link commands to transmit on the port or one or more of the hub downstream ports has a link in U0 or recovery.

10-33

Universal Serial Bus 3.1 Specification, Revision 1.0

- The port's link shall accept U2 entry requests by its link partner unless the hub has one or more packets/link commands to transmit on the port or one or more of the hub downstream ports has a link in U0, U1, or recovery.
- The PM timer may be disabled and the PM timer values shall be ignored.
- The port's link shall initiate a transition to U2 if all the hub downstream ports are in U2 or a lower link state.

U1_ENABLE = 1, U2_ENABLE = 1

- The port's link shall accept U1 or U2 entry requests by its link partner unless the hub has one or more packets/link commands to transmit on the port.

A U1 entry request shall not be accepted if one or more of the hub downstream ports has a link in U0 or recovery.

A U2 entry request shall not be accepted if one or more of the hub downstream ports has a link in U0, U1, or recovery.

- The port's link shall initiate a transition to U1 if all the hub downstream ports are in U1 or a lower link state unless the conditions for U2 entry are satisfied.
- The port's link shall initiate a transition to U2 if all the hub downstream ports are in U2 or a lower link state. Note that if the port is already in U1, then the port shall transition to U0 before transitioning to U2.
- The PM timer may be disabled and the PM timer values shall be ignored.

A port transitions to one of the Enabled U0 states (depending on the U1 and U2 Enable values) in any of the following situations:

- From U1 if the link partner successfully initiates a transition to U0.
- From U2 if the link partner successfully initiates a transition to U0.
- From U1 if there is a status change on a downstream port.
- From U2 if there is a status change on a downstream port.
- From U1 if a hub downstream port's link initiates a transition to U0.
- From U2 if a hub downstream port's link initiates a transition to U0.
- From an attempt to transition from the U0 to the U1 state if the upstream port's link partner rejects the transition attempt
- From an attempt to transition from the U0 to the U2 state if the upstream port's link partner rejects the transition attempt
- From U3 if the upstream port of the hub receives wakeup signaling.
- From U3 if there is a status change on a downstream port or a local power status change and remote wakeup is enabled for the corresponding event type.

### 10.6.2.2 Attempt U0 – U1 Transition

In this state the port attempts to transition its link from the U0 state to the U1 state.

A port shall attempt to transition to the U1 state in any of the following situations:

- U1 entry is requested by the link partner and there is no pending traffic on the port and all the hub downstream port's links are in U1 or a lower state.
- All the hub downstream ports are in U1 or a lower link state and there is no pending traffic to transmit on the upstream port and U1_ENABLE is set to one.
- U1 entry is requested by the link partner and Force_LinkPM_Accept bit is set.

10-34

Hub, Host Downstream Port, and Device Upstream Port Specification

If the transition attempt fails (an LXU is received or the link goes to recovery), the port returns to the appropriate enabled U0 state.

### 10.6.2.3 Attempt U0 – U2 Transition

In this state, the port attempts to transition the link from the U0 state to the U2 state.

A port shall attempt to transition to the U2 state in any of the following situations:

- U2 entry is requested by the link partner and there is no pending traffic on the port and all the hub downstream port's links are in U2 or a lower state.
- All the hub downstream ports are in U2 or a lower link state and there is no pending traffic to transmit on the upstream port and U2_ENABLE is set to one.
- U2 entry is requested by the link partner and Force_LinkPM_Accept bit is set.

If the transition attempt fails (an LXU is received or the link goes to recovery), the port returns to the appropriate enabled U0 state.

### 10.6.2.4 Link in U1

The PM timer is reset when this state is entered and is active.

A port transitions to U1:

- After sending an LAU to accept a transition initiated by the link partner.
- After receiving an LAU from the link partner after initiating an attempt to transition the link to U1

If the U2 inactivity timeout is not 0xFF or 0x00, and the PM timer reaches the U2 inactivity timeout, the port's link shall initiate a transition from U1 to U2.

### 10.6.2.5 Link in U2

The link is in U2.

A port transitions to U2:

- After sending an LAU to accept a transition initiated by the link partner.
- After receiving an LAU from the link partner after initiating an attempt to transition the link to U2

### 10.6.2.6 Link in U3

The link is in U3.

A port transitions to U3:

- After sending an LAU to accept a transition initiated by the link partner.

10-35

Universal Serial Bus 3.1 Specification, Revision 1.0

## 10.7 SuperSpeed Hub Header Packet Forwarding and Data Repeater

The SuperSpeed Hub uses a store and forward model for header packets and a repeater model for data that combined provide the following general functionality.

In the downstream direction:

- Validates header packets
- Sets up connection to selected downstream port
- Forwards header packets to downstream ports
- Forwards data payload to downstream port if present
- Sets up and tears down connectivity on packet boundaries

In the upstream direction:

- Validates header packets
- Sets up connection to upstream port
- Forwards header packets to the upstream port
- Forwards data packet payload to upstream port if present
- Sets up and tears down connectivity on packet boundaries

### 10.7.1 SuperSpeed Hub Elasticity Buffer

There are no direct specifications for elasticity buffer behavior in a SuperSpeed hub. However, note that a SuperSpeed hub must meet the requirements in Section 10.7.3 for the maximum variation in propagation delay for header packets that are forwarded from the upstream port to a downstream port.

### 10.7.2 SKP Ordered Sets

A SuperSpeed hub transmits SKP ordered sets, following the rules for all transmitters in Chapter 6, for all transmissions.

### 10.7.3 Interpacket Spacing

When a SuperSpeed hub originates or forwards packets, Data packet headers and data packet payloads shall be sent as required in Section 7.2.1.

When a SuperSpeed hub forwards a header packet downstream and the downstream port link is in U0 when the header packet is received on the hub upstream port the propagation delay variation shall not be more than tPropagationDelayJitterLimit.

### 10.7.4 SuperSpeed Header Packet Buffer Architecture

The specification does not require a specific architecture for the header packet buffers in a SuperSpeed hub. An example architecture that meets the functional requirements of this specification is shown in Figure 10-15 and Figure 10-16 to illustrate the functional behavior of a SuperSpeed hub. Figure 10-15 shows a SuperSpeed hub with a four header packet Rx buffer for the upstream port and a four header packet Tx buffer for each of the downstream ports. Figure 10-16 shows a four header packet Rx buffer for each of the downstream ports and a four header

10-36

Hub, Host Downstream Port, and Device Upstream Port Specification

packet Tx buffer for the upstream port. The buffers shown in Figure 10-15 and Figure 10-16 are independent physical buffers.

![img-272.jpeg](img-272.jpeg)

Figure 10-15. Example SS Hub Header Packet Buffer Architecture - Downstream Traffic

![img-273.jpeg](img-273.jpeg)

Figure 10-16. Example SS Hub Header Packet Buffer Architecture - Upstream Traffic

The following lists functional requirements for a SuperSpeed hub buffer architecture with the assumption in each case that only the indicated port on the hub is receiving or transmitting header packets:

- A SuperSpeed hub starting with all header packet buffers empty shall be able to receive at least eight header packets directed to the same downstream port that is not in U0 before its upstream port runs out of header packet flow control credits.

10-37

Universal Serial Bus 3.1 Specification, Revision 1.0

- A SuperSpeed hub that receives a header packet on its upstream port that is routed to a downstream port shall immediately route the header packet to the appropriate downstream port header packet buffer (if space in that buffer is available) regardless of the state of any other downstream port header packet buffers or the state of the upstream port Rx header packet buffer. For example, a hub Tx header packet buffer for downstream port 1 is full and the hub has three more header packets routed to downstream port 1 in the hub upstream port Rx header packet buffer. If the hub now receives a header packet routed to downstream port 2, it must immediately route the header packet to the downstream port 2 Tx header packet buffer.
- A SuperSpeed hub starting with all header packet buffers empty shall be able to receive at least eight header packets on the same downstream port directed for upstream transmission when the upstream port is not in U0.
- Header packets transmitted by a downstream port shall be transmitted in the order they were received on the upstream port.
- Header packets transmitted by an upstream port from the same downstream port shall be transmitted in the order they were received on that downstream port.

Section 10.9 provides detailed functional state machines for the upstream and downstream port Tx and Rx header packet buffers in a hub implementation.

The SuperSpeed hub shall have at least 1080 bytes of buffering for data packets received on the upstream port.

The SuperSpeed hub shall have at least 1080 bytes of shared buffering for data packets received on all downstream ports.

### 10.7.5 SuperSpeed Packet Connectivity

The SuperSpeed hub packet repeater/forwarder must re-clock the packets in both directions. Re-clocking means that the repeater extracts the data from the received stream and retransmits the stream using its own local clock.

## 10.8 SuperSpeedPlus Store and Forward Behavior

The SuperSpeedPlus Hub provides the following general functionality.

In the downstream direction:

- Receives and validates packet
- Forwards packet to appropriate downstream port
- Selects next packet to transmit on (each) downstream port

In the upstream direction:

- Receives and validates packet
- Forwards packet to the upstream port
- Selects next packet to transmit on the upstream port

### 10.8.1 Hub Elasticity Buffer

There are no direct specifications for elasticity buffer behavior in a hub. However, note that a hub must meet the requirements in Section 10.7.3 for the maximum variation in propagation delay.

10-38

Hub, Host Downstream Port, and Device Upstream Port Specification

### 10.8.2 SKP Ordered Sets

A SuperSpeedPlus hub transmits SKP ordered sets, following the rules for all transmitters in Chapter 6, for all transmissions.

### 10.8.3 Interpacket Spacing

When a hub originates or forwards packets, DPHs and their corresponding DPPs shall be sent as required in Section 7.2.1.

The SuperSpeedPlus hub has several aspects to its store and forward behavior including buffering, arbitration among packets to be forwarded upstream, and modifications of packets during forwarding.

### 10.8.4 Upstream Flowing Buffering

The SuperSpeedPlus hub shall provide buffering for 16x 1KB Control/Bulk DPP buffers and 16x 1KB Interrupt/Isochronous DPP buffers for each DFP receiver. The SuperSpeedPlus hub shall provide buffering for 16x Control/Bulk header buffers and 16x TP/Interrupt/Isochronous header buffers per DFP receiver. These buffers shall be used to hold packets received from downstream ports that are awaiting transmission on the upstream port.

Buffer space is required for each downstream port since there can be packets simultaneously arriving on each downstream port while there is a packet being transmitted on the upstream port. Further, the hub arbitration rules (see Section 10.8.6) can delay when a packet received on a downstream port can be transmitted on the upstream port.

![img-274.jpeg](img-274.jpeg)

Figure 10-17. Logical Representation of Upstream Flowing Buffers

### 10.8.5 Downstream Flowing Buffering

The SuperSpeedPlus hub shall provide buffering for 18x 1KB Control/Bulk DPP buffers and 18x 1KB Interrupt/Isochronous DPP buffers per hub. The SuperSpeedPlus hub shall provide buffering for 18x Control/Bulk header buffers and 18x TP/Interrupt/Isochronous header buffers per hub.

Buffering for downstream flowing traffic is primarily present to provide a rate matching function due to the different possible upstream port and downstream port speeds. Therefore, it is provided

10-39

Universal Serial Bus 3.1 Specification, Revision 1.0

for each hub and not for each downstream port. However, the organization and function of this buffering shall allow packets to be received from the upstream port and then subsequently transmitted on multiple downstream ports simultaneously and in a different order than the order in which they were received. That is, this buffering cannot be organized as a single, simple FIFO.

![img-275.jpeg](img-275.jpeg)

Figure 10-18. Logical Representation of Downstream Flowing Buffers

### 10.8.6 SuperSpeedPlus Hub Arbitration of Packets

#### 10.8.6.1 Arbitration Weight

The iᵗʰ downstream facing port (DFPi) has an arbitration weight (AW) associated with it. This weight shall be set to;

DFPi.AW = DFPi.link_speed / ArbitrationWeightBase

For example, a port link operating at 5Gb/s will have an AW of 4. A port link operating at 10Gb/s will have an AW of 8.

#### 10.8.6.2 Direction Independent Packet Selection

When there are multiple packets buffered that are ready to be transmitted out of the hub, the SuperSpeedPlus hub has to select which packet to transmit next.

There are several selection rules that are independent of direction of packet flow.

The SuperSpeedPlus hub has additional rules that are specific for upstream and downstream flowing packet reception and selection (see the next two sections).

A TP shall only be considered as a possible candidate after it has been fully received and validated.

10-40

Hub, Host Downstream Port, and Device Upstream Port Specification

A buffered TP shall be selected for transmission before any buffered DPs. TPs shall be selected in the order in which they were buffered for a port (e.g. FIFO). When selecting a TP to transmit on the hub upstream facing port, there is no specific ordering requirement for TPs buffered from different downstream ports.

A buffered Interrupt or Isochronous DP shall be selected for transmission before any buffered Control or Bulk DPs.

Once a hub starts transmitting a packet on a port, it shall continue transmitting that packet until the packet transmission is complete. With respect to the following arbitration rules, there is no “pre-emption” of the transmission of one packet for the transmission of another packet.

If a DP is being received on a port and the port to which it is to be routed has no other packets buffered nor has a packet currently being transmitted, the hub shall begin transmitting the packet on the destination port before the DP is fully received. Transmission of the DP shall not begin transmission until sufficient bytes have been received, so that transmitter under-run is avoided.

### 10.8.6.3 Downstream Flowing Packet Reception and Selection

For downstream flowing traffic, buffered Isochronous and Interrupt DPs destined to be transmitted on the same downstream port shall be selected to be transmitted in the same order as they were received on the upstream port. Control and Bulk DPs buffered for transmission on the same downstream port shall be selected for transmission in the same order as they were received on the upstream port. TPs buffered for transmission on the same downstream port shall be selected for transmission in the same order as they were received on the upstream port.

### 10.8.6.4 Upstream Flowing Packet Reception and Selection

When the Upstream Controller needs to select a packet to transmit on the upstream port, any fully buffered packets from downstream ports are candidates for the next packet to transmit. However, some packets still being received and not fully buffered can also be candidates.

To select the next DP for transmission on the upstream port, the Upstream Controller shall use:

- A weighted round robin arbitration behavior to select the next Control/Bulk DP buffered from the hub downstream ports.
- A simple round robin arbitration behavior to select the next Interrupt/Isochronous DP buffered from the hub downstream ports.

The next section describes when an incompletely buffered DP that is still being received can be a candidate. The section after that describes the upstream weighted round robin arbitration mechanism.

#### 10.8.6.4.1 Partially Buffered DP Selection Candidate

A DP (call it RCV_DP) shall be considered as a possible candidate, after the DPH has been fully received and validated and all of the following conditions are true:

- Let ALT_P be the candidate packet that would have been selected from the current set of fully buffered packets (i.e. when not considering RCV_DP as a possible candidate). RCV_DP would be selected when compared to ALT_P.
- The time remaining to fully receive this DPP is less than the time it will take to transmit ALT_P.

10-41

Universal Serial Bus 3.1 Specification, Revision 1.0

- Enough of the DPP has been received to ensure that upstream port transmitter under-run will not occur during the transmission of this packet.

For example, if there are only buffered Bulk DPs from other downstream ports and an Isochronous DP is being received on one downstream port, the Upstream Controller shall select the Isochronous DP as the next packet to transmit on the upstream port; as long as the remaining time to receive the Isochronous DP is less than the time required to transmit the Bulk DP and there is a sufficient amount of the Isochronous DPP already received.

### 10.8.6.4.2 Upstream Weighted Round Robin Arbitration

When the Upstream Controller needs to select the next Control/Bulk DP to transmit on the upstream port, the Upstream Controller uses the following selectPacket() algorithm to determine the next DP.

In the selectPacket() algorithm pseudo code, once a packet is selected, the algorithm is complete and any remaining steps in the algorithm are ignored for the selection of the current packet to transmit upstream.

Across invocations of the selectPacket algorithm, retain the value of i and curr_weight. Initial values of i=-1 and curr_weight=0.

The i$^{th}$ downstream facing port is DFPi. The candidate packet for the i$^{th}$ DFP is CPi.
selectPacket() algorithm:

1) If there are no buffered packets, set i=-1 and curr_weight=0 and don't select a packet.
Note: The upstream port will await the arrival of a packet on some DFPi.
2) For each DFPi, identify a candidate packet CPi for the DFPi:
   a. if there is a Control or Bulk DP buffered, set CPi to be the first one that had been buffered.
3) If there is only one DFPi with packets buffered for upstream transmission:
   a. Set i = port index
   b. Set cw = CPi.AW
   c. Select CPi
   d. exit
4) While true
   a. i = (i + 1) mod num_ports
   b. if (i == 0) then
      i. compute the Greatest Common Divisor (GCD) of all the buffered CPi.AW
      ii. curr_weight = curr_weight - GCD
      iii. if (curr_weight <= 0) then
         1. curr_weight = max of CPi.AWs for all buffered CPi
         2. if (curr_weight == 0) then there is no packet to select
   c. if (DFPi.AW >= curr_weight) then
      i. select CPi
      ii. exit

10-42

Hub, Host Downstream Port, and Device Upstream Port Specification

### 10.8.7 SuperSpeedPlus Upstream Flowing Packet Modifications

When the upstream port of a SuperSpeedPlus hub is operating at greater than Gen 1 speed and the hub Downstream Controller receives a valid IN/ACK TP that is routed to a downstream port (DFPi) that is operating at Gen 1 speed, the Downstream Controller shall:

1) Save the transfer type (SAVE_TT) of the TP for that DFPi.

When the hub Downstream Controller receives a valid DPH packet from DFPi, the Downstream Controller shall:

1) If the transfer type for this DFPi has been saved and the DPH is not a deferred DPH, set the transfer type of the DP to the saved value (DFPi.SAVE_TT).
2) If the AW field value of the received DPH is zero and the transfer type is Control or Bulk, modify the AW field of the received DPH by setting the DPH.AW field to DFPi.AW
3) If the DPH was modified, recompute the CRC-16 for the DPH.

This packet modification shall be done when the packet is received.

When the hub Upstream Controller selects (as described in Section 10.8.6.4) a Control/Bulk packet (S_DP) to transmit on the upstream port and there are multiple downstream ports (DFPi) with buffered Control/Bulk DPs awaiting transmission, the Upstream Controller shall:

1) For each DFPi, determine a candidate buffered Control/Bulk DP (C_DPi) for that DFPi that would be selected for upstream transmission if there were no other DFPi's with buffered Control/Bulk DPs.
2) Compute the sum (SUM_AW) of the AWs of the C_DPi's.
3) If the SUM_AW is different than the current value of the S_DP DPH.AW, modify the AW field of the S_DP DPH by replacing the AW value with SUM_AW
4) If the DPH was modified, recompute the CRC-16 for the S_DP DPH.

This modification shall be done before the packet is routed to the upstream port for transmission. Note that in the above descriptions, a packet may appear to have its CRC-16 recomputed twice. Hub implementations are encouraged to be structured so that the correct CRC-16 value only needs to be computed once after all required modifications have been made.

### 10.8.8 SuperSpeedPlus Downstream Controller

The Downstream Controller for each downstream port shall be responsible for updating the ITP fields as described in Section 8.4.8.8 before forwarding the ITP on all downstream ports in U0. See Chapter 8 for the format of an ITP.

### 10.9 Port State Machines

In the following descriptions of port state machines, there are references to the first or last symbol of a header packet. The first symbol of a header packet is the first DPHP or SHP (Section 7.2.1.1.1). The last symbol of a SuperSpeedPlus DPH header packet is the last byte of the replicated length (if present) or the last byte of the LCW (if the replicated length field is not present). The last symbol of a SuperSpeedPlus non-DPH header packet and all SuperSpeed header packets is the last byte of the LCW.

10-43

Universal Serial Bus 3.1 Specification, Revision 1.0

### 10.9.1 Port Transmit State Machine

This section describes the functional requirements of the upstream and downstream facing port Transmit (Tx) state machines. Upstream and downstream ports shall adhere to all requirements of the link layer (see Chapter 7).

10-44

Hub, Host Downstream Port, and Device Upstream Port Specification

![img-276.jpeg](img-276.jpeg)

Figure 10-19. Port Transmit State Machine

10-45

Universal Serial Bus 3.1 Specification, Revision 1.0

## 10.9.2 Port Transmit State Descriptions

### 10.9.2.1 Tx IDLE

In the Tx IDLE state, the port transmitter is actively transmitting idle symbols. A port transmitter shall transition to the Tx IDLE state in any of the following situations:

- From the Tx Data, Tx Data Abort, or Tx Header state after packet transmission is completed.
- From the Tx Link Command state after a link command is transmitted and there are no other link commands awaiting transmission.
- As the default state when the link enters U0.

### 10.9.2.2 Tx Header

In the Tx Header state, the port transmitter is actively transmitting a header packet.

A port transmitter shall transition to the Tx Header state in any of the following situations:

- From the Tx IDLE state when there are one or more header packets queued for transmission and there are no link commands queued for transmission.

### 10.9.2.3 Tx Data

In the Tx Data state, the port transmitter is actively transmitting a DPP. After transmitting the DPP, the port transmitter may remove the DPP from hub storage. A hub shall not retransmit a DPP under any circumstances.

A port transmitter shall transition to the Tx Data state from the Tx Header state when there is a DPP associated with the DPH that was transmitted. The DPP transmission shall begin immediately after transmission of the last symbol of the DPH.

### 10.9.2.4 Tx Data Abort

In the Tx Data abort state, the port transmitter aborts the normal transmission of a DPP by performing speed specific abort processing (see Section 7.2.1.2.2). The port transmitter then removes the DPP from hub storage.

In the case where the hub is simultaneously receiving a DPP into the hub and transmitting the same DPP out of the hub:

- An upstream port transmitter shall transition to the Tx Data Abort state from the Tx Data state when the downstream port receiving the DPP detects a speed specific abort indication.
- A downstream port transmitter shall transition to the Tx Data Abort state from the Tx Data state when the upstream port receiving the DPP detects a speed specific abort indication.

### 10.9.2.5 Tx Link Command

In the Tx Link Command state, the port transmitter is actively transmitting a link command.

A port transmitter shall transition to the Tx Link Command state in any of the following situations:

- From the Tx IDLE state when there are one or more link commands queued for transmission.
- From the Tx Link Command state when there are additional link commands queued for transmission.

10-46

Hub, Host Downstream Port, and Device Upstream Port Specification

### 10.9.3 Port Receive State Machine

This section describes the functional requirements of the upstream and downstream facing port receiver (Rx) state machine.

![img-277.jpeg](img-277.jpeg)

Figure 10-20. Upstream Facing Port Rx State Machine

### 10.9.4 Port Receive State Descriptions

#### 10.9.4.1 Rx Default

In the Rx Default state, the port receiver is actively receiving symbols and looking for the speed specific beginning of a valid packet or a link command.

A port receiver shall transition to the Rx Default state in any of the following situations:

- From the Rx Data state when a speed specific end of packet or abort indication is detected.
- From the Rx Header state when the last symbol of the header packet is received.
- After receiving a link command.

10-47

Universal Serial Bus 3.1 Specification, Revision 1.0

- As the default state when the link enters U0.

### 10.9.4.2 Rx Data

In the Rx Data state, the port receiver is actively processing symbols and looking for the speed specific indication of the end of a packet or the occurrence of an abort condition.

A port shall transition to the Rx Data state when it receives a speed specific start of packet indication.

When the port detects an error before the end of the DPP as defined in Section 7.2.4.1.6, it performs speed specific abort processing (see Section 7.2.1.2.2).

In the case where the hub is simultaneously receiving a DPP into the hub and transmitting the same DPP out of the hub, the corresponding port transmitter shall be given an indication of the abort condition so that it can perform speed specific abort processing.

If the DPP is not being actively transmitted out of the hub,

- For an upstream port receiver, the hub shall buffer a speed specific aborted DP for the appropriate downstream port.
- For a downstream port receiver, the hub shall buffer a speed specific aborted DP on the upstream port.

### 10.9.4.3 Rx Header

In the Rx header state, the port receiver is actively processing received symbols until the last header packet symbol is received.

A port shall transition to the Rx Header state when it detects the speed specific beginning of a header packet.

The port shall validate CRC-16, the Link Control Word CRC-5, check the route string (only if this is an upstream port) and header packet type within four symbol times after the last symbol of the header packet is received.

Implementations may have to begin the CRC calculation as the header is being received and check the route string before the header packet is verified to meet this requirement.

### 10.9.4.4 Process Header Packet

When the last symbol of a header packet is received the port shall perform all processing necessary for the header packet. Any such processing shall not block the port from immediately returning to the Rx Default state.

As described in the link chapter, when the last symbol of a header packet is received in the Rx header packet state and either the header packet CRC-16 or Link Control Word CRC-5 is determined to be invalid, the link layer won't pass the header packet to the hub.

Table 10-3 summarizes the actions of the hub when it receives a packet on its upstream port that is targeted for a valid downstream port.

10-48

Hub, Host Downstream Port, and Device Upstream Port Specification

Table 10-3. Downstream Flowing Header Packet Processing Actions

[tbl-203.md](tbl-203.md)

The steps described in the next 4 sections depend on:

- whether the hub is operating as a SuperSpeed hub or a SuperSpeedPlus hub, and
- whether the port processing is being done for an upstream or downstream facing port.

#### 10.9.4.4.1 SuperSpeed Hub Upstream Facing Port

- The header packet is not an ITP and not a PING and is routed to a downstream port that is in U1 or in U2:
  1. The hub initiates U0 entry on the appropriate downstream port link. U0 entry shall be initiated no later than tDownLinkStateChange from when the hub received the first symbol of the header packet.
  2. If the header packet is not already marked deferred:
     a) The header packet is marked deferred and the Link Control Word CRC-5 is re-calculated for the deferred header packet. If the deferred header packet is a DPH, the corresponding DPP is silently discarded.
     b) A copy of the header packet is modified to include the hub's hub depth, marked as deferred and with the Link Control Word CRC-5 recalculated is queued for transmission on the upstream port. Note that the route string in this deferred header packet is preserved and not set to zero.
  3. The deferred header packet (see Section 7.2.4.1.4) is queued for transmission on the appropriate downstream port.
- If the header packet is a PING and is routed to a downstream port that is in U0 or is in U1 or is in U2 or is in Recovery:
  1. If the appropriate downstream port link is in U1 or in U2, the hub initiates U0 entry on the appropriate downstream port link. U0 entry shall be initiated no later than tDownLinkStateChange from when the hub received the first symbol of the header packet.
  2. The header packet is queued for transmission on the appropriate downstream port.
- If the header packet is not an ITP and not a PING and is routed to a downstream port that is in U0 or in Recovery:
  1. If the downstream port Tx header packet buffer queue is not empty (there is at least one header packet in the queue that has not been completely transmitted) or no link credit is available for transmission on the downstream port, the header packet is marked delayed and the Link Control Word CRC-5 is re-calculated for the modified header packet.
  2. The header packet is queued for transmission on the appropriate downstream port.

10-49

Universal Serial Bus 3.1 Specification, Revision 1.0

Note: If the queue for the appropriate downstream port is full, the header packet is queued as soon as a space is available for the appropriate downstream port. The hub shall process subsequent header packets while a downstream port buffer is full if they are directed to a different downstream port.

- If the header packet is an ITP then for each downstream port:

1. The ITP is silently discarded for any downstream port with a link not in U0 and not in Recovery.
2. The Delta and Correction fields in the ITP shall be updated to account for the measured delay of propagating the ITP through the hub.
a) If the delay introduced by the hub exceeds the tPropagationDelayJitterLimit, then the header packet shall be marked Delayed (DL) and the correct Link Control Word CRC-5 is re-calculated for modified header packet.
b) If the Delta subfield overflowed, the ITP shall not be queued, otherwise the header packet shall be queued for transmission on each downstream port that has completed Port Configuration and is in U0 or in Recovery.

Note: If the queue for the appropriate downstream port is full, the header packet is queued as soon as a space is available in the appropriate downstream port queue. The hub shall process subsequent header packets while a downstream port queue is full if they are directed to a different downstream port.

- If the header packet is routed to a disabled or nonexistent downstream port or to a downstream port that is in not in U0 and not in U1 and not in U2 and not in Recovery:

1. The header packet is removed from the RX header packet queue.
2. The header packet is silently discarded.
3. If the header packet is a DPH the corresponding DPP is silently discarded.

- If the header packet is routed to the hub controller:

1. The header packet is processed by the hub controller.
2. The header packet is removed from the RX header packet queue.
3. A response to the header packet is queued for transmission on the upstream port, if required.

### 10.9.4.4.2 SuperSpeedPlus Hub Upstream Facing Port

- The header packet is not an ITP and not a PING and is routed to a downstream port that is in U1 or in U2:

1. The hub initiates U0 entry on the appropriate downstream port link. U0 entry shall be initiated no later than tDownLinkStateChange from when the hub received the first symbol of the header packet.
2. If the header packet is not already marked deferred:

a) The header packet is marked deferred and the Link Control Word CRC-5 is re-calculated for the deferred header packet. If the deferred header packet is a DPH, the corresponding DPP is silently discarded.
b) A copy of the header packet is modified to include the hub's hub depth, marked as deferred and with the Link Control Word CRC-5 recalculated is buffered awaiting arbitration for transmission on the upstream port. Note that the route string in this deferred header packet is preserved and not set to zero.

3. The deferred header packet (see Section 7.2.4.1.4) is buffered awaiting arbitration (see Section 10.8.6.4) for transmission on the appropriate downstream port.

10-50

Hub, Host Downstream Port, and Device Upstream Port Specification

- If the header packet is a PING and is routed to a downstream port that is in U0 or is in U1 or is in U2 or is in Recovery:

1. If the appropriate downstream port link is in U1 or in U2, the hub initiates U0 entry on the appropriate downstream port link. U0 entry shall be initiated no later than tDownLinkStateChange from when the hub received the first symbol of the header packet.
2. The header packet is buffered awaiting arbitration for transmission on the appropriate downstream port.

- If the header packet is not an ITP and not a PING and is routed to a downstream port that is in U0 or in Recovery:

1. If the downstream port is currently transmitting a packet or there is at least one packet buffered that will be selected before this packet or no link credit is available for transmission on the downstream port, the header packet is marked delayed and the Link Control Word CRC-5 is re-calculated for modified header packet.
2. The header packet is buffered awaiting arbitration for transmission on the appropriate downstream port.

- If the header packet is an ITP then for each downstream port:

1. The ITP is silently discarded for any downstream port with a link not in U0 and not in Recovery.
2. The Delta and Correction fields in the ITP shall be updated to account for the measured delay of propagating the ITP through the hub.

a) If the delay introduced by the hub exceeds the tPropagationDelayJitterLimit, then the header packet shall be marked Delayed (DL) and the correct Link Control Word CRC-5 is re-calculated for modified header packet.
b) If the Delta subfield overflowed, the ITP shall not be buffered, otherwise the header packet is buffered awaiting arbitration for transmission on each downstream port that has completed Port Configuration and is in U0 or in Recovery.

- If the header packet is routed to a disabled or nonexistent downstream port or to a downstream port that is in not in U0 and not in U1 and not in U2 and not in Recovery:

1. The header packet is removed from the Upstream Receive buffer.
2. The header packet is silently discarded.
3. If the header packet is a DPH the corresponding DPP is silently discarded.

- If the downstream port to which the packet is being routed is operating at Gen 1 speed and the header packet is a valid IN/ACK, save the transfer type (DFP.SAVE_TT) of the IN/ACK. The DFP.SAVE_TT is preserved until the next IN/ACK is received that is routed to the same downstream port. See Section 10.9.4.4.4.

- If the header packet is routed to the hub controller:

1. The header packet is processed by the hub controller.
2. The header packet is removed from the Upstream Receive buffer.
3. A response to the header packet is buffered awaiting arbitration for transmission on the upstream port if required.

### 10.9.4.4.3 SuperSpeed Hub Downstream Facing Port

- The header packet is queued for transmission on the upstream port.

If the queue for the upstream port is full, the header packet is queued as soon as a space is available in the upstream port queue. The hub shall process subsequent header packets while the upstream port queue is full. If header packets have been received on more than one downstream port or are queued to be sent by the hub controller when a space becomes available

10-51

Universal Serial Bus 3.1 Specification, Revision 1.0

in the upstream port header packet queue, the hub shall prioritize a non-data packet header over a data packet header packet if one is waiting at the front of a downstream queue or from the hub controller. Otherwise, the arbitration algorithm the hub uses is not specified.

Note: These arbitration requirements only apply across multiple downstream ports and the hub controller. For a single source (downstream port or hub controller), packets must be transmitted in the ordered received or generated.

### 10.9.4.4.4 SuperSpeedPlus Hub Downstream Facing Port

- If a valid DP is received then:

1. If the port is operating at Gen 1 speed then set the transfer type of the DP to the value of DFP.SAVE_TT. See Section 10.9.4.4.2.
2. If the transfer type is asynchronous and the AW field value is zero, modify the AW field of the received DPH by setting the DPH.AW field to DFP.AW. See Section 10.8.6.

- The header packet is buffered awaiting arbitration for transmission on the upstream port (see Section 10.8.6).

### 10.9.4.5 Rx Link Command

In the Rx Link Command state, the port receiver is actively processing received symbols and looking for the speed specific indication of the end of a link command.

A port shall transition to the Rx Link Command state when it receives a valid speed specific indication of the beginning of a link command.

### 10.9.4.6 Process Link Command

Once the link command is received, the port shall perform all additional processing necessary for the link command. Any such processing shall not block the port from immediately returning to the Rx Default state.

## 10.10 Suspend and Resume

Hubs must support suspend and resume both as a USB device and in terms of propagating suspend and resume signaling. Global suspend/resume refers to the entire bus being suspended or resumed without affecting any hub's downstream facing port states; selective suspend/resume refers to a downstream facing port of a hub being suspended or resumed without affecting the hub state. Enhanced SuperSpeed hubs only support selective suspend and resume. They do not support global suspend and resume. Selective suspend/resume is implemented via requests to a hub. Device-initiated resume is called remote-wakeup.

The hub follows the same suspend requirements as an Enhanced SuperSpeed device on its upstream facing port.

When a hub downstream port link is in the U3 state, the following requirements apply to the hub if it receives wakeup signaling from its link partner on that downstream port:

- If the hub upstream port's link is not in U3, the hub shall drive remote wakeup signaling on the downstream link where the wakeup signaling was received in tHubDriveRemoteWakeDownstream.
- If the hub upstream port's link is in U3, the hub shall drive wakeup signaling on its upstream port in tHubPropRemoteWakeUpstream.

10-52

Hub, Host Downstream Port, and Device Upstream Port Specification

- If the hub upstream port is in the process of entering U3, the hub shall wait until the U3 entry is completed, before driving wakeup signaling on its upstream port in tHubPropRemoteWakeUpstream.

When a hub upstream port's link enters the U3 state and one of its downstream links is in U0/U1/U2/Recovery and has received a remote wake, the hub shall automatically drive remote wakeup on upstream port in tHubPropRemoteWakeUpstream.

When a hub upstream port's link is in the U3 state and it receives wakeup signaling from its link partner on the hub upstream port's link, the hub shall automatically drive remote wakeup to any downstream ports that are in U3 and have received remote wakeup signaling since entering U3.

If the hub upstream port's link is in U3, the hub shall drive wakeup signaling on its upstream port due to connect (when the downstream port enters DSPORT.Enabled), disconnect, or overcurrent events, if the hub is enabled for remote wakeup.

When the hub receives a SetPortFeature(PORT_LINK_STATE) U0 for a downstream port with a link in U3, the hub shall drive remote wakeup signaling on the link in tHubDriveRemoteWakeDownstream.

### 10.11 Hub Upstream Port Reset Behavior

Reset signaling to a hub is defined only in the downstream direction, which is at the hub's upstream facing port. The reset signaling mechanism required of the hub is described in Chapter 6.

A suspended hub shall interpret the start of reset as a wakeup event; it shall be awake and have completed its reset sequence by the end of reset signaling.

After completion of a Warm Reset, the entire hub returns to the default state.

After completion of a Hot Reset, the hub returns to the default state except port configuration information is maintained for the upstream port.

Irrespective of how the hub was reset, the hub needs to propagate reset as described in Section 10.3.1.6 and not just transition those downstream ports to the default state.

### 10.12 Hub Port Power Control

Self-powered hubs may have power switches that control delivery of power to downstream facing ports but it is not required. A hub with power switches can switch power to all ports as a group/gang, to each port individually, or have an arbitrary number of gangs of one or more ports.

A hub indicates whether or not it supports power switching by the setting of the Logical Power Switching Mode field in wHubCharacteristics. If a hub supports per-port power switching, then the power to a port is turned on or off as specified in Table 10-2. If a hub supports ganged power switching, then the power to all ports in a gang is turned on when power is required to be on for any port in the gang. The power to a gang is not turned off unless all ports in a gang are in a state that allows power to be removed as specified in Table 10-2. The power to a port is not turned on by a SetPortFeature(PORT_POWER) if both C_HUB_LOCAL_POWER and Local Power Status (in wHubStatus) are set to one at the time when the request is executed and the PORT_POWER feature would be turned on. A hub that supports charging applications may keep power on at other times. Refer to Section 10.3.1.1 for more details on allowed behavior for a hub that supports charging applications.

10-53

Universal Serial Bus 3.1 Specification, Revision 1.0

Although a self-powered hub is not required to implement power switching, the hub shall support the Powered-off states for all ports.

For a hub with no power switches, bPwrOn2PwrGood shall be set to zero.

### 10.12.1 Multiple Gangs

A hub may implement any number of power and/or over-current gangs. A hub that implements more than one over-current and/or power switching gang shall set both the Logical Power Switching Mode and the Over-current Reporting Mode to indicate that power switching and over-current reporting are on a per port basis (these fields are in wHubCharacteristics).

When an over-current condition occurs on an over-current protection device, the over-current is signaled on all ports that are protected by that device. When the over-current is signaled, all the ports in the group are placed in the DSPORT-Powered-off or the DSPORT-Powered-off-reset state, and the C_PORT_OVER_CURRENT field is set to one on all the ports. When port status is read from any port in the group, the PORT_OVER_CURRENT field will be set to one as long as the over-current condition exists. The C_PORT_OVER_CURRENT field shall be cleared in each port individually.

When multiple ports share a power switch, setting PORT_POWER on any port in the group will cause the power to all ports in the group to turn on. It will not, however, because the other ports in that group to leave the DSPORT-Powered-off or the DSPORT-Powered-off-reset state. When all the ports in a group are in the DSPORT-Powered-off state or the hub is not configured, the power to the ports is turned off.

If a hub implements both power switching and over-current, it is not necessary for the over-current groups to be the same as the power switching groups.

If an over-current condition occurs and power switches are present, then all power switches associated with an over-current protection circuit shall be turned off. If multiple over-current protection devices are associated with a single power switch, then that switch will be turned off when any of the over-current protection circuits indicates an over-current condition.

### 10.13 Hub Controller

The Hub Controller is logically organized as shown in Figure 10-21.

10-54

Hub, Host Downstream Port, and Device Upstream Port Specification

![img-278.jpeg](img-278.jpeg)

Figure 10-21. Example Hub Controller Organization

### 10.13.1 Endpoint Organization

The Hub Class defines one additional endpoint beyond the default control pipe, which is required for all hubs: the Status Change endpoint. This endpoint has the maximum burst size set to one. The host system receives port and hub status change notifications through the Status Change endpoint. The Status Change endpoint is an interrupt endpoint. If no hub or port status change bits are set, then the hub returns an NRDY when the Status Change endpoint receives an IN (via an ACK TP) request. When a status change bit is set, the hub will send an ERDY TP to the host. The host will subsequently ask the Status Change endpoint for the data, which will indicate the entity (hub or port) with a change bit set. The USB system software can use this data to determine which status registers to access in order to determine the exact cause of the status change interrupt.

### 10.13.2 Hub Information Architecture and Operation

Figure 10-22 shows how status, status change, and control information relate to device states. Hub descriptors and Hub/Port Status and Control are accessible through the default control pipe. The Hub descriptors may be read at any time. When a hub detects a change on a port or when the hub changes its own state, the Status Change endpoint transfers data to the host in the form specified in Section 10.13.4.

Hub or port status change bits can be set because of hardware or software events. When set, these bits remain set until cleared directly by the USB system software through a ClearPortFeature() request or by a hub reset. While a change bit is set, the hub continues to report a status change when the Status Change endpoint is read until all change bits have been cleared by the USB system software.

10-55

Universal Serial Bus 3.1 Specification, Revision 1.0

![img-279.jpeg](img-279.jpeg)

Figure 10-22. Relationship of Status, Status Change, and Control Information to Device States

The USB system software uses the interrupt pipe associated with the Status Change endpoint to detect changes in hub and port status.

10-56

Hub, Host Downstream Port, and Device Upstream Port Specification

### 10.13.3 Port Change Information Processing

Hubs report a port's status through port commands on a per-port basis. The USB system software acknowledges a port change by clearing the change state corresponding to the status change reported by the hub. The acknowledgment clears the change state for that port so future data transfers to the Status Change endpoint do not report the previous event. This allows the process to repeat for further changes (see Figure 10-23).

![img-280.jpeg](img-280.jpeg)

Figure 10-23. Port Status Handling Method

10-57

Universal Serial Bus 3.1 Specification, Revision 1.0

### 10.13.4 Hub and Port Status Change Bitmap

The Hub and Port Status Change Bitmap, shown in Figure 10-24, indicates whether the hub or a port has experienced a status change. This bitmap also indicates which port(s) have had a change in status. The hub returns this value on the Status Change endpoint. Hubs report this value in byte-increments. For example, if a hub has six ports, it returns a byte quantity, and reports a zero in the invalid port number field locations. The USB system software is aware of the number of ports on a hub (this is reported in the hub descriptor) and decodes the Hub and Port Status Change Bitmap accordingly. The hub reports any changes in hub status in bit zero of the Hub and Port Status Change Bitmap.

The Hub and Port Status Change Bitmap size is two bytes. Hubs report only as many bits as there are ports on the hub. A USB hub may have no more than nMaxHubPorts.

![img-281.jpeg](img-281.jpeg)

Figure 10-24. Hub and Port Status Change Bitmap

10-58

Hub, Host Downstream Port, and Device Upstream Port Specification

Any time any of the Status Changed bits are non-zero, an ERDY is returned (if an NRDY was previously sent) notifying the host that the Hub and Port Status Change Bitmap has changed. Figure 10-25 shows an example creation mechanism for hub and port change bits.

![img-282.jpeg](img-282.jpeg)

Figure 10-25. Example Hub and Port Change Bit Sampling

### 10.13.5 Over-current Reporting and Recovery

USB devices shall be designed to meet applicable safety standards. Usually, this will mean that a self-powered hub implements current limiting on its downstream facing ports. If an over-current condition occurs, it causes a status and state change in one or more ports. This change is reported to the USB system software so that it can take corrective action.

A hub may be designed to report over-current as either a port or a hub event. The hub descriptor field wHubCharacteristics is used to indicate the reporting capabilities of a particular hub (refer to Section 10.15.2.1). The over-current status bit in the hub or port status field indicates the state of the over-current detection when the status is returned. The over-current status change bit in the Hub or Port Change field indicates if the over-current status has changed.

When a hub experiences an over-current condition, it shall place all affected ports in the DSPORT-Powered-off-reset state. If a hub has per-port power switching and per-port current limiting, an over-current condition on one port may still cause the power on another port to fall below specified minimums. In this case, the affected port is placed in the DSPORT-Powered-off-reset state and C_PORT_OVER_CURRENT is set for the port, but PORT_OVER_CURRENT is not set. If the hub has over-current detection on a hub basis, then an over-current condition on the hub will cause all ports to enter any DSPORT-Powered-off-reset state. However, in this case, neither C_PORT_OVER_CURRENT nor PORT_OVER_CURRENT is set for the affected ports.

Host recovery actions for an over-current event should include the following:

1. Host gets change notification from hub with over-current event.
2. Host extracts appropriate hub or port change information (depending on the information in the change bitmap).
3. Host waits for over-current status bit to be cleared to 0.
4. Host cycles power to on for all of the necessary ports (e.g., issues a SetPortFeature(PORT_POWER) request for each port).
5. Host re-enumerates all affected ports.

10-59

Universal Serial Bus 3.1 Specification, Revision 1.0

### 10.13.6 Enumeration Handling

The hub device class commands are used to manipulate its downstream facing port state. When a device is attached, the device attach event is detected by the hub and reported on the Status Change endpoint. The host will accept the status change report and may request a SetPortFeature(PORT_RESET) on the port. The GetPortStatus request invoked by the host will return a PORT_CONNECTION indication along with the PORT_SPEED field set to zero if the downstream facing port has a Enhanced SuperSpeed device connected.

When the device is detached from the port, the port reports the status change through the Status Change endpoint. Then the process is ready to be repeated on the next device attach detect.

### 10.14 Hub Configuration

Hubs are configured through the standard USB device configuration commands. A hub that is not configured behaves like any other device that is not configured with respect to power requirements and addressing. A hub is required to power its downstream ports based on several factors, including whether the hub supports power switching and charging applications. Refer to Section 10.3.1.1 for details on when a hub is required to provide power to downstream ports. Configuring a hub enables the Status Change endpoint. Part of the configuration process is setting the hub depth which is used to compute an index (refer to Section 10.16.2.9) into the Route String (refer to Section 8.9). The hub depth is used to derive the offset into the Route String (in a TP or DP) that the hub shall use to route packets received on its upstream port. The USB system software may then issue commands to the hub to switch port power on and off at appropriate times.

The USB system software examines hub descriptor information to determine the hub's characteristics. By examining the hub's characteristics, the USB system software ensures that illegal power topologies are not allowed by not powering on the hub's ports if doing so would violate the USB power topology. The device status and configuration information can be used to determine whether the hub can be used in a given topology. Table 10-4 summarizes the information and how it can be used to determine the current power requirements of the hub.

**Table 10-4. Hub Power Operating Mode Summary**

[tbl-204.md](tbl-204.md)

10-60

Hub, Host Downstream Port, and Device Upstream Port Specification

[tbl-205.md](tbl-205.md)

A self-powered hub has a local power supply, but may optionally draw one unit load from its upstream connection. This allows the interface to function when local power is not available (refer to Section 11.4.1.1). When local power is removed (either a hub-wide over-current condition or local supply is off), a hub of this type remains in the Configured state but transitions all ports (whether removable or non-removable) to the Powered-off state. While local power is off, all port status and change information read as zero and all SetPortFeature() requests are ignored (request is treated as a no-operation). The hub will use the Status Change endpoint to notify the USB system software of the hub event (refer to Section 10.13.4 for details on hub status).

The MaxPower field in the configuration descriptor is used to report to the system the maximum power the hub will draw from VBUS when the configuration is selected. The external devices attaching to the hub will report their individual power requirements.

A compound device may power both the hub electronics and the permanently attached devices from VBUS. The entire load may be reported in the hubs' configuration descriptor with the permanently attached devices each reporting self-powered, with zero MaxPower in their respective configuration descriptors.

A bus powered hub shall be able to supply any power not used by the hub electronics or permanently attached devices for the selected configuration to the exposed downstream ports. The hub shall be able to provide the power with any split across the exposed downstream ports (i.e., if the hub can provide 600 mA to two exposed downstream ports, it must be able to provide 450 mA to one and 150 mA to the other, 300 mA to each, etc.).

Note: Software shall ensure that at least 150 mA is available for each exposed downstream port on a bus powered hub.

10-61

Universal Serial Bus 3.1 Specification, Revision 1.0

## 10.15 Descriptors

Hub descriptors are derived from the general USB device framework. Hub descriptors describe a hub device and the ports on that hub. The host accesses hub descriptors through the hub's default control pipe.

The USB specification (refer to Chapter 8) defines the following descriptors:

- Device Level Descriptors
- Configuration
- Interface
- Endpoint
- String (optional)

The hub class defines additional descriptors (refer to Section 10.15.2). In addition, vendor-specific descriptors are allowed in the USB device framework. Hubs support standard USB device commands as defined in Chapter 8.

A hub is the only device that is allowed to function at high-speed and a Gen X speed at the same time. This specification only defines the descriptors a hub shall report on the Enhanced SuperSpeed bus.

Note that an Enhanced SuperSpeed hub shall always support the Get Descriptor (BOS) (refer to Section 9.6.2) when operating at either the Gen X speed or at USB 2.0 speeds.

### 10.15.1 Standard Descriptors for Hub Class

The hub class pre-defines certain fields in standard USB descriptors. Other fields are either implementation-dependent or not applicable to this class.

A hub has a device descriptor with a bDeviceProtocol field set to 3 and an interface descriptor with a bInterfaceProtocol field set to 0.

**Hub Descriptors for USB hub operating at Gen 1 speed**

Device Descriptor (SuperSpeed information)

[tbl-206.md](tbl-206.md)

10-62

Hub, Host Downstream Port, and Device Upstream Port Specification

BOS Descriptor

[tbl-207.md](tbl-207.md)

USB 2.0 Extension

[tbl-208.md](tbl-208.md)

SuperSpeed USB Device Capability

[tbl-209.md](tbl-209.md)

ContainerID

[tbl-210.md](tbl-210.md)

The hub shall also return SuperSpeedPlus USB Device Capability and Precision Time Measurement capability as defined for a hub operating at Gen 2 speeds.

10-63

Universal Serial Bus 3.1 Specification, Revision 1.0

Configuration Descriptor (SuperSpeed information)

[tbl-211.md](tbl-211.md)

Interface Descriptor

[tbl-212.md](tbl-212.md)

Endpoint Descriptor (for Status Change Endpoint)

[tbl-213.md](tbl-213.md)

Endpoint Companion Descriptor (for Status Change Endpoint)

[tbl-214.md](tbl-214.md)

10-64

Hub, Host Downstream Port, and Device Upstream Port Specification

### Hub Descriptors for USB hub operating at Gen 2 speed

Device Descriptor (SuperSpeedPlus information)

[tbl-215.md](tbl-215.md)

BOS Descriptor

[tbl-216.md](tbl-216.md)

USB 2.0 Extension

[tbl-217.md](tbl-217.md)

SuperSpeed USB Device Capability

[tbl-218.md](tbl-218.md)

10-65

Universal Serial Bus 3.1 Specification, Revision 1.0

SuperSpeedPlus USB Device Capability

[tbl-219.md](tbl-219.md)

ContainerID

[tbl-220.md](tbl-220.md)

Precision Time Measurement

[tbl-221.md](tbl-221.md)

Configuration Descriptor (SuperSpeedPlus information)

[tbl-222.md](tbl-222.md)

10-66

Hub, Host Downstream Port, and Device Upstream Port Specification

Interface Descriptor

[tbl-223.md](tbl-223.md)

Endpoint Descriptor (for Status Change Endpoint)

[tbl-224.md](tbl-224.md)

Endpoint Companion Descriptor (for Status Change Endpoint)

[tbl-225.md](tbl-225.md)

10-67

Universal Serial Bus 3.1 Specification, Revision 1.0

## 10.15.2 Class-specific Descriptors

### 10.15.2.1 Hub Descriptor

Table 10-5 outlines the various fields contained in the hub descriptor.

Table 10-5. Enhanced SuperSpeed Hub Descriptor

[tbl-226.md](tbl-226.md)

10-68

Hub, Host Downstream Port, and Device Upstream Port Specification

[tbl-227.md](tbl-227.md)

10-69

Universal Serial Bus 3.1 Specification, Revision 1.0

## 10.16 Requests

### 10.16.1 Standard Requests

Hubs have tighter constraints on request processing timing than specified in Section 9.2.6 for standard devices because they are crucial to the “time to availability” of all devices attached to the USB. The worst case request timing requirements are listed below (they apply to both Standard and Hub Class requests):

- Completion time for requests with no data stage: 50 ms
- Completion times for standard requests with data stage(s):
  Time from setup packet to first data stage: 50 ms
  Time between each subsequent data stage: 50 ms
  Time between last data stage and status stage: 50 ms

Because hubs play such a crucial role in bus enumeration, it is recommended that hubs average response times be less than 5 ms for all requests.

Table 10-6 outlines the various standard device requests.

Table 10-6. Hub Responses to Standard Device Requests

[tbl-228.md](tbl-228.md)

A hub is required to accept all “Standard” requests without error. A hub shall not respond with a request error to a well-formed SET_ISOCH_DELAY request. A hub is not required to retain or process the delay value. Optional requests that are not implemented shall return a STALL in the Data stage or Status stage of the request.

10-70

Hub, Host Downstream Port, and Device Upstream Port Specification

### 10.16.2 Class-specific Requests

The hub class defines requests to which hubs respond, as outlined in Table 10-7. Table 10-8 defines the hub class request codes. All requests in the table below except SetHubDescriptor() are mandatory.

Table 10-7. Hub Class Requests

[tbl-229.md](tbl-229.md)

10-71

Universal Serial Bus 3.1 Specification, Revision 1.0

Table 10-8. Hub Class Request Codes

[tbl-230.md](tbl-230.md)

Table 10-9 gives the valid feature selectors for the hub class. Refer to Section 10.16.2.1 and Section 10.16.2.8 for a description of the features.

Table 10-9. Hub Class Feature Selectors

[tbl-231.md](tbl-231.md)

10-72

Hub, Host Downstream Port, and Device Upstream Port Specification

### 10.16.2.1 Clear Hub Feature

This request resets a value reported in the hub status.

[tbl-232.md](tbl-232.md)

Clearing a feature disables that feature; refer to Table 10-9 for the feature selector definitions that apply to the hub as a recipient. If the feature selector is associated with a status change, clearing that status change acknowledges the change. This request format is used to clear either the C_HUB_LOCAL_POWER or C_HUB_OVER_CURRENT features.

It is a Request Error if wValue is not a feature selector listed in Table 10-9 or if wIndex or wLength are not as specified above.

If the hub is not configured, the hub's response to this request is undefined.

### 10.16.2.2 Clear Port Feature

This request resets a value reported in the port status.

[tbl-233.md](tbl-233.md)

The port number shall be a valid port number for that hub, greater than zero. The port field is located in bits 7..0 of the wIndex field.

Clearing a feature disables that feature or starts a process associated with the feature; refer to Table 10-9 for the feature selector definitions. If the feature selector is associated with a status change, clearing that status change acknowledges the change. This request format is used to clear the following features:

- PORT_POWER
- C_PORT_CONNECTION
- C_PORT_RESET
- C_PORT_OVER_CURRENT
- C_PORT_LINK_STATE
- C_PORT_CONFIG_ERROR
- C_BH_PORT_RESET
- FORCE_LINKPM_ACCEPT

Clearing the PORT_POWER feature causes the port to be placed in the DSPORT-Powered-off-reset state and may, subject to the constraints due to the hub's method of power switching, result in power being removed from the port. When in the DSPORT-Powered-off or the DSPORT-Powered-off-detect or the DSPORT-Powered-off-reset state, the only requests that are valid when this port is the recipient are Get Port Status (refer to Section 10.16.2.6) and Set Port Feature (PORT_POWER) (refer to Section 10.16.2.10).

Clearing the FORCE_LINKPM_ACCEPT feature causes the port to de-assert the Force_LinkPM_Accept bit in Set Link Function LMPs. If the Force_LinkPM_Accept bit is not asserted on the port, the hub shall treat this request as a functional no-operation.

It is a Request Error if wValue is not a feature selector listed in Table 10-9, if wIndex specifies a port that does not exist, or if wLength is not as specified above. It is not an error for this request to try to clear a feature that is already cleared (the hub shall treat this as a functional no-operation).

10-73

Universal Serial Bus 3.1 Specification, Revision 1.0

If the hub is not configured, the hub's response to this request is undefined.

### 10.16.2.3 Get Hub Descriptor

This request returns the hub descriptor.

[tbl-234.md](tbl-234.md)

The GetDescriptor() request for the hub class descriptor follows the same usage model as that of the standard GetDescriptor() request (refer to Chapter 9). The standard hub descriptor is denoted by using the value bDescriptorType defined in Section 10.15.2.1. All hubs are required to implement one hub descriptor, with descriptor index zero.

If wLength is larger than the actual length of the descriptor, then only the actual length is returned. If wLength is less than the actual length of the descriptor, then only the first wLength bytes of the descriptor are returned; this is not considered an error even if wLength is zero.

It is a Request Error if wValue or wIndex are other than as specified above.

If the hub is not configured, the hub's response to this request is undefined.

### 10.16.2.4 Get Hub Status

This request returns the current hub status and the states that have changed since the previous acknowledgment.

[tbl-235.md](tbl-235.md)

The first word of data contains the wHubStatus field (refer to Table 10-10). The second word of data contains the wHubChange field (refer to Table 10-11).

It is a Request Error if wValue, wIndex, or wLength are other than as specified above.

If the hub is not configured, the hub's response to this request is undefined.

10-74

Hub, Host Downstream Port, and Device Upstream Port Specification

Table 10-10. Hub Status Field, wHubStatus

[tbl-236.md](tbl-236.md)

There are no defined feature selector values for these status bits and they can neither be set nor cleared by the USB system software.

Table 10-11. Hub Change Field, wHubChange

[tbl-237.md](tbl-237.md)

Hubs may allow setting of these change bits with SetHubFeature() requests in order to support diagnostics. If the hub does not support setting of these bits, it shall either treat the SetHubFeature() request as a Request Error or as a functional no-operation. When set, these bits may be cleared by a ClearHubFeature() request. A request to set a feature that is already set or to clear a feature that is already clear has no effect and the hub shall treat this as a functional no-operation.

10-75

Universal Serial Bus 3.1 Specification, Revision 1.0

### 10.16.2.5 Get Port Error Count

This request returns the number of link errors detected by the hub on the port indicated by wIndex. This value is reset to zero whenever the device goes through a Reset (refer to Section 7.3) or at power up.

[tbl-238.md](tbl-238.md)

The port number shall be a valid port number for that hub, greater than zero.

It is a Request Error if wValue or wLength are other than as specified above or if wIndex specifies a port that does not exist.

If the hub is not configured, the behavior of the hub in response to this request is undefined.

### 10.16.2.6 Get Port Status

This request returns the current port status and the current value of the port status change bits.

[tbl-239.md](tbl-239.md)

The port number shall be a valid port number for that hub, greater than zero.

The first word of PORT_STATUS or EXT_PORT_STATUS data contains the wPortStatus field (refer to Table 10-13). The second word of PORT_STATUS or EXT_PORT_STATUS data contains the wPortChange field (refer to Table 10-14). An EXT_PORT_STATUS request shall return an additional dword of data that contains dwExtPortStatus field (refer to Table 10-15).

The bit locations in the wPortStatus and wPortChange fields correspond in a one-to-one fashion where applicable.

The wValue field specifies the Port Status Type in the low order byte (refer to Table 10-11 and the high order byte is reserved.

10-76

Hub, Host Downstream Port, and Device Upstream Port Specification

Table 10-12. Port Status Type Codes

[tbl-240.md](tbl-240.md)

It is a Request Error if the Port Status Type equals EXT_PORT_STATUS and the hub that does not define a SuperSpeedPlus USB Capability descriptor, or if the Port Status Type equals a reserved value, or if wValue or wLength are other than as specified in Table 10-7, or if wIndex specifies a port that does not exist.

If the hub is not configured, the behavior of the hub in response to this request is undefined.

$^{1}$ Refer to the USB Power Delivery Specification Revision 1.0

10-77

Universal Serial Bus 3.1 Specification, Revision 1.0

### 10.16.2.6.1 Port Status Bits

Table 10-13. Port Status Field, wPortStatus

[tbl-241.md](tbl-241.md)

10-78

Hub, Host Downstream Port, and Device Upstream Port Specification

[tbl-242.md](tbl-242.md)

## PORT_CONNECTION

This bit is set to one when the port in the DSPORT.Enabled state. In DSPORT.Resetting or DSPORT.Error state it maintains the value from prior state.

SetPortFeature(PORT_CONNECTION) and ClearPortFeature(PORT_CONNECTION) requests shall not be used by the USB system software and shall be treated as no-operation requests by hubs.

## PORT_ENABLE

This bit is set to one when the downstream port is in the DSPORT.Enabled state and is set to zero otherwise.

Note that the USB 2.0 ClearPortFeature (PORT_ENABLE) request is not supported by Enhanced SuperSpeed hubs and cannot be used by USB system software to disable a port.

## PORT_OVER_CURRENT

This bit is set to one while an over-current condition exists on the port and set to zero otherwise.

If the voltage on this port is affected by an over-current condition on another port, this bit is set to one and remains set to one until the over-current condition on the affecting port is removed. When the over-current condition on the affecting port is removed, this bit is set to zero.

Over-current protection is required on self-powered hubs (it is optional on bus-powered hubs) as outlined in Section 10.12.

The SetPortFeature(PORT_OVER_CURRENT) and ClearPortFeature(PORT_OVER_CURRENT) requests shall not be used by the USB system software and may be treated as no-operation requests by hubs.

10-79

Universal Serial Bus 3.1 Specification, Revision 1.0

# PORT_RESET

This bit is set to one while the port is in the DSPORT.Resetting state. This bit is set to zero in all other downstream port states.

A SetPortFeature(PORT_RESET or BH_PORT_RESET) request will initiate the DSPORT.Resetting state if the conditions in Section 10.3.1.6 are met.

The ClearPortFeature(PORT_RESET) request shall not be used by the USB system software and may be treated as a no-operation request by hubs.

# PORT_LINK_STATE

This field reflects the current state of the link.

The SetPortFeature(PORT_LINK_STATE) request may be issued by the USB system software at any time but will have an effect only as specified in Section 10.16.2.10.

The ClearPortFeature(PORT_LINK_STATE) requests shall not be used by the USB System software and may be treated as no-operation requests by hubs.

# PORT_POWER

This bit reflects the current logical power state of a port. This bit is implemented on all ports whether or not actual port power switching devices are present.

While this bit is zero, the port is in the DSPORT.Powered-off state, the DSPORT.Powered-off-detect state, or the DSPORT.Powered-off-reset state. Similarly, anything that causes this port to go to any of these three states will cause this bit to be set to zero.

A SetPortFeature(PORT_POWER) will set this bit to one unless both C_HUB_LOCAL_POWER and Local Power Status (in wHubStatus) are set to one in which case the request is treated as a functional no-operation.

# PORT_SPEED

This value in this field is only valid when the PORT_ENABLE bit is set to one and the Port Status Type is set to PORT_STATUS. A value of zero in this field indicates that an Enhanced SuperSpeed device is attached. All other values in this field are reserved.

System Software can determine the actual speed at which the device is operating by using the Get Port Status request with the Port Status Type set to EXT_PORT_STATUS (see Section 10.16.2.6.3).

This field can only be read by USB system software.

# 10.16.2.6.2 Port Status Change Bits

Port status change bits are used to indicate changes in port status bits that are not the direct result of requests. Port status change bits can be cleared with a ClearPortFeature() request or by a hub reset. Hubs may allow setting of the status change bits with a SetPortFeature() request for diagnostic purposes. If a hub does not support setting of the status change bits, it may either treat the request as a Request Error or as a functional no-operation. Table 10-14 describes the various bits in the wPortChange field.

10-80

Hub, Host Downstream Port, and Device Upstream Port Specification

Table 10-14. Port Change Field, wPortChange

[tbl-243.md](tbl-243.md)

10-81

Universal Serial Bus 3.1 Specification, Revision 1.0

# C_PORT_CONNECTION

This bit is set to one when the PORT_CONNECTION bit changes.

This bit shall be set to zero by a ClearPortFeature(C_PORT_CONNECTION) request or while logical port power is off.

# C_PORT_OVER_CURRENT

This bit is set to one when the PORT_OVER_CURRENT bit changes from zero to one or from one to zero. This bit is also set if the port is placed in the DSPORT-Powered-off-reset state due to an over-current condition on another port.

This bit shall be set to zero by a ClearPortFeature(C_PORT_OVER_CURRENT) request.

# C_PORT_RESET

This bit is set to one when the port transitions from the DSPORT.Resetting state to the DSPORT.Enabled state for any type of reset.

This bit shall be set to zero by a ClearPortFeature(C_PORT_RESET) request, or while logical port power is off.

# C_PORT_BH_RESET

This bit is set to one when the port transitions from the DSPORT.Resetting state to the DSPORT.Enabled state for a Warm Reset only.

This bit shall be cleared by a ClearPortFeature(C_PORT_BH_RESET) request, or while logical port power is off.

# C_PORT_LINK_STATE

This bit is set to one when the port's link completes a transition from the U3 state to the U0 state as a result of a SetPortFeature(Port_Link_State) request or completes a transition to Loopback state or to Compliance or to eSS.Inactive with Rx terminations present. This bit is not set to one due to transitions from U3 to U0 as a result of remote wakeup signaling received on a downstream facing port.

This bit will be cleared by a ClearPortFeature(C_PORT_LINK_STATE) request, or while logical port power is off.

# C_PORT_CONFIG_ERROR

This bit is set to one if the link connected to the port could not be successfully configured, e.g., if two downstream only capable ports are connected to each other or if the link configuration could not be completed. In addition, the port shall transition to the DSPORT.Error state when this occurs.

This bit will be cleared by a ClearPortFeature(C_PORT_CONFIG_ERROR) request, or while logical port power is off.

10-82

Hub, Host Downstream Port, and Device Upstream Port Specification

### 10.16.2.6.3 Extended Port Status Bits

The extended port status bits are returned only if the Port Status Type of a Get Port Status request is set to EXT_PORT_STATUS.

Note that for Enhanced SuperSpeed devices the “Port Speed” is the Link Speed multiplied by Lane Count.

Table 10-15. Extended Port Status Field, dwExtPortStatus

[tbl-244.md](tbl-244.md)

### TX_SUBLINK_SPEED_ID and RX_SUBLINK_SPEED_ID

The value in this field is only valid when the PORT_ENABLE bit is set to one. The Lane Speed (i.e. bit rate of a single lane) is determined by evaluating the parameters of the Sublink Speed Attribute in the SuperSpeedPlus USB Capability descriptor whose Sublink Speed Attribute ID value matches the Sublink Speed ID value, e.g. if the Sublink Speed Attribute LSE and LSM fields equal 3 and 10, respectively, then the link is operating at 10 Gb/s. All values not referenced by a Sublink Speed Attribute are reserved.

This field can only be read by USB system software.

### TX_LANE_COUNT and RX_LANE_COUNT

This value in this field is only valid when the PORT_ENABLE bit is set to one. The speed of a port is determined by multiplying the Sublink Speed (as defined by the SUBLINK_SPEED_ID) by the Lane Count.

This field can only be read by USB system software.

### 10.16.2.7 Set Hub Descriptor

This request overwrites the hub descriptor.

[tbl-245.md](tbl-245.md)

The SetDescriptor request for the hub class descriptor follows the same usage model as that of the standard SetDescriptor request (refer to the framework chapter). The standard hub descriptor is denoted by using the value bDescriptorType defined in Section 10.15.2.1. All hubs are required to implement one hub descriptor with descriptor index zero.

10-83

Universal Serial Bus 3.1 Specification, Revision 1.0

This request is optional. This request writes data to a class-specific descriptor. The host provides the data that is to be transferred to the hub during the data transfer stage of the control transaction. This request writes the entire hub descriptor at once.

Hubs shall buffer all the bytes received from this request to ensure that the entire descriptor has been successfully transmitted from the host. Upon successful completion of the bus transfer, the hub updates the contents of the specified descriptor.

It is a Request Error if wIndex is not zero or if wLength does not match the amount of data sent by the host. Hubs that do not support this request respond with a STALL during the Data stage of the request.

If the hub is not configured, the hub's response to this request is undefined.

### 10.16.2.8 Set Hub Feature

This request sets a value reported in the hub status.

[tbl-246.md](tbl-246.md)

Setting a feature enables that feature; refer to Table 10-9 for the feature selector definitions that apply to the hub as recipient. Status changes may not be acknowledged using this request.

It is a Request Error if wValue is not a feature selector listed in Table 10-9 or if wIndex or wLength are not as specified above.

If the hub is not configured, the hub's response to this request is undefined.

### 10.16.2.9 Set Hub Depth

This request sets the value that the hub uses to determine the index into the Route String Index for the hub.

[tbl-247.md](tbl-247.md)

wValue has the value of the Hub Depth. The Hub Depth left shifted by two is the offset into the Route String that identifies the lsb of the Route String Port Field for the hub.

It is a Request Error if wValue is greater than 4 or if wIndex or wLength are not as specified above.

If the hub is not configured, the hub's response to this request is undefined.

### 10.16.2.10 Set Port Feature

This request sets a value reported in the port status.

[tbl-248.md](tbl-248.md)

The port number shall be a valid port number for that hub, greater than zero. The port number is in the least significant byte (bits 7..0) of the wIndex field. The most significant byte of wIndex is zero,

10-84

Hub, Host Downstream Port, and Device Upstream Port Specification

except when the feature selector is PORT_U1_TIMEOUT or PORT_U2_TIMEOUT or PORT_LINK_STATE or PORT_REMOTE_WAKE_MASK.

Setting a feature enables that feature or starts a process associated with that feature; see Table 10-9 for the feature selector definitions that apply to a port as a recipient. Status change may not be acknowledged using this request. Features that can be set with this request are:

- PORT_RESET
- BH_PORT_RESET
- PORT_POWER
- PORT_U1_TIMEOUT
- PORT_U2_TIMEOUT
- PORT_LINK_STATE
- PORT_REMOTE_WAKE_MASK
- FORCE_LINKPM_ACCEPT

When the feature selector is PORT_U1_TIMEOUT, the most significant byte (bits 15..8) of the wIndex field specifies the Timeout value for the U1 inactivity timer. Refer to Section 10.4.2.1 for a detailed description of how the U1 inactivity timer value is used.

The following are permissible values:

Table 10-16. U1 Timeout Value Encoding

[tbl-249.md](tbl-249.md)

When the feature selector is PORT_U2_TIMEOUT, the most significant byte (bits 15..8) of the wIndex field specifies the Timeout value for the U2 inactivity timer. The port's link shall send an LMP to its link partner with the specified timeout value after receiving a Set Port Feature request with the PORT_U2_TIMEOUT feature selector. Refer to Section 10.4.2.1 for a detailed description of how the U2 inactivity timer value is used.

The following are permissible values:

Table 10-17. U2 Timeout Value Encoding

[tbl-250.md](tbl-250.md)

10-85

Universal Serial Bus 3.1 Specification, Revision 1.0

Note: It is the responsibility of software to properly set the U2 timeout for a downstream port that is connected to a hub. Inconsistent link states could result if the timeout is not set properly. It is recommended that software should set the upstream U2 timeout to at least twice the value of the U2 timeout of the downstream ports on the hub.

When the feature selector is PORT_LINK_STATE, the most significant byte (bits 15..8) of the wIndex field specifies the U state the host software wants to put the link connected to the port into. This request is only valid when the PORT_ENABLE bit is set and the PORT_LINK_STATE is not set to eSS.Disabled, Rx.Detect or eSS.Inactive except as noted below:

- If the value is 0, then the hub shall transition the link to U0 from any of the U states.
- If the value is 1, then host software wants to transition the link to the U1 State. The hub shall attempt to transition the link to U1 from U0. If the link is in any state other than U0 when a request is received with a value of 1, the behavior is undefined.
- If the value is 2, then the host software wants to transition the link to the U2 State. The hub shall attempt to transition the link to U2 from U0. If the link is in any state other than U0 when a request is received with a value of 2, the behavior is undefined.
- If the value is 3, then host software wants to selectively suspend the device connected to this port. The hub shall transition the link to U3 from any of the other U states using allowed link state transitions. If the port is not already in the U0 state, then it shall transition the port to the U0 state and then initiate the transition to U3. While this state is active, the hub does not propagate downstream-directed traffic to this port, but the hub will respond to resume signaling from the port.
- If the value is 4 (eSS.Disabled), the hub shall transition the link to eSS.Disabled. The request is valid at all times when the value is 4. The downstream port shall transition to the DSPORT.Disabled state after this request is received.
- If the value is 5 (Rx.Detect), the hub shall transition the link to Rx.Detect. This request is only valid when the downstream port is in the DSPORT.Disabled state. If the link is in any other state when a request is received with this value, the behavior is undefined. The downstream port shall transition to the DSPORT.Disconnected state after this request is received.
- If the value is 10 (Enable Compliance Mode), the hub shall enable entry into Compliance Mode for the next attach. This request is valid only when the downstream port is in the DSPORT.Disconnected state. If the link is in any other state when a request is received with this value, the behavior is undefined. Entry into Compliance Mode is disabled once the link enters Compliance Mode or Polling.LFPS succeeds.
- The hub shall respond with a Request Error if it sees any other value in the upper byte of the wIndex field.

When the feature selector is PORT_REMOTE_WAKE_MASK, the most significant byte (bits 15..8) of the wIndex field specifies the conditions that would cause the hub to signal a remote wake event on its upstream port. The encoding for the port remote wake mask is given below:

10-86

Hub, Host Downstream Port, and Device Upstream Port Specification

Table 10-18. Downstream Port Remote Wake Mask Encoding

[tbl-251.md](tbl-251.md)

Note that after power on or after the hub is reset, the remote wake mask is set to zero (i.e., the mask is enabled).

The hub shall meet the following requirements:

- If the port is in the Powered-off state, the hub shall treat a SetPortFeature(PORT_RESET) request as a functional no-operation.
- If the port is not in the Enabled state, the hub shall treat a SetPortFeature(PORT_LINK_STATE) U3 request as a functional no-operation.
- If the port is not in the Powered-off state, the hub shall treat a SetPortFeature(PORT_POWER) request as a functional no-operation.
- If the port is not in the Enabled state, the hub shall treat a SetPortFeature(FORCE_LINKPM_ACCEPT) request as a functional no-operation.

When the feature selector is BH_PORT_RESET, the hub shall initiate a warm reset (refer to Section 7.4.2) on the port that is identified by this command. The state of the port after this reset shall be the same as the state after a SetPortFeature(PORT_RESET). On completion of a BH_PORT_RESET, the hub shall set the C_BH_PORT_RESET field to one in the PortStatus for this port.

10-87

Universal Serial Bus 3.1 Specification, Revision 1.0

It is a Request Error if wValue is not a feature selector listed in Table 10-9, if wIndex specifies a port that does not exist, or if wLength is not as specified above.

If the hub is not configured, the hub's response to this request is undefined.

### 10.17 Host Root (Downstream) Ports

The root ports of a USB host have similar functional requirements to the downstream ports of a USB hub. This section summarizes which requirements also apply to the root port of a host and identifies any additional or different requirements.

A host root port shall follow the requirements for a downstream facing hub port in Section 10.2 except for Section 10.2.3.

A host root port shall follow the requirements for a downstream facing hub port in Section 10.3 with the following exceptions and additions:

- None of the transitions and/or transition conditions based on the state of the hub upstream port apply to a root port.
- A host shall have control mechanisms in the host interface that allow software to achieve equivalent behavior to hub downstream port behavior in response to SetPortFeature or ClearPortFeature requests documented in Section 10.3.
- A host shall implement port status bits consistent with the downstream port state descriptions in Section 10.3.
- A host is required to provide a mechanism to correlate each USB 2.0 port with any Enhanced SuperSpeed port that shares the same physical connector. Note that this is similar to the requirement for USB hubs in Section 10.3.3.

A host root port shall follow the requirements for a downstream facing hub port in Section 10.4 with the same general exceptions already noted in this section.

A host shall implement port status bits through the host interface that are equivalent to all port status bit definitions in this chapter.

A host shall have mechanisms to achieve equivalent control over its root ports as provided by the SetPortFeature, ClearPortFeature, and GetPortStatus requests documented in this chapter.

### 10.18 Peripheral Device Upstream Ports

The upstream port of a USB peripheral device has similar functional requirements to the upstream port of a USB hub. This section summarizes which requirements also apply to the upstream port of a peripheral device and identifies any additional or different requirements.

### 10.18.1 Peripheral Device Upstream Ports

A peripheral device shall follow the requirements for an upstream facing hub port in Section 10.5 with the following exceptions and additions:

- A peripheral device shall not attempt to connect on the USB 2.0 interface when the port is in the USPORT.Connected state.
- A peripheral device shall not attempt to connect on the USB 2.0 interface unless the port has entered the USPORT.Powered-off state and VBUS is still present as shown in Figure 10-12.

10-88

Hub, Host Downstream Port, and Device Upstream Port Specification

- If a device is connected on the USB 2.0 interface and it receives a USB 2.0 bus reset, the device shall enter the USPORT-Powered-On state within tCheckSuperSpeedOnReset time.
- After a USB 2.0 reset, if the Enhanced SuperSpeed port enters the USPORT.Training state, the device shall disconnect on the USB 2.0 interface within tUSB2SwitchDisconnect time.

A device shall follow the requirements for an upstream facing hub port in Section 10.6 with the following exceptions and additions:

- None of the conditions related to downstream port apply.
- A peripheral device initiates transitions to U1 or U2 when otherwise allowed based on vendor specific algorithms.

### 10.18.2 Peripheral Device Upstream Port State Machine

The following sections provide a functional description of a state machine that exhibits correct peripheral device behavior for when to connect on Enhanced SuperSpeed or USB 2.0. Figure 10-26 is an illustration of the peripheral device upstream port state machine.

10-89

Universal Serial Bus 3.1 Specification, Revision 1.0

![img-283.jpeg](img-283.jpeg)

¹ Peripheral Device must disconnect on USB2.0 within tUSB2SwitchDisconnect of entering this state.

² If USPORT-Powered on was entered from any state except USPORT.Disabled then this transition shall take place if Far-end Receiver Terminations (RRX-DC) are not detected after 8 successive Rx.Detect.Quiet to Rx.Detect.Active transitions. If USPORT-Powered on was entered from the USPORT.Disabled state, then this transition shall take place the first time that Far-end Receiver Terminations are not detected in the Rx.Detect.Active substate.

³ Disabled count is incremented each time the "Disabled" state is entered from the "Training Initiated" state. Disabled count is reset to '0' each time the link completes Port Configuration.

Figure 10-26. Peripheral Upstream Device Port State Machine

### 10.18.2.1 USDPORT-Powered-off

The USDPORT-Powered-off state is the default state for a peripheral device. A peripheral device shall transition into this state if any of the following situations occur:

- From any state when VBUS is invalid.

In this state, the port's link shall be in the eSS.Disabled state and the USB 2.0 pull-up is not applied. The corresponding peripheral USB state shall be Attached.

10-90

Hub, Host Downstream Port, and Device Upstream Port Specification

### 10.18.2.2 USDPORT.Powered on

A port shall transition into this state if any of the following situations occur:

- From the USDPORT.Powered-off state when VBUS becomes valid (and local power is valid if required).
- From the USDPORT.Error state when the link receives a warm reset or Far-end terminations are removed.
- From the USDPORT.Connected/Enabled state when the link receives a Warm Reset.
- From the USDPORT.Disabled state if the port receives a USB 2.0 reset.
- From the USDPORT.Training state when the link receives a Warm Reset.

In this state, the port's link shall be in the Rx.Detect state. The corresponding peripheral device USB state shall be Powered (Far-end Receiver Termination substate).

If the transition is from the USDPORT.Disabled state the USB 2.0 pull-up shall remain enabled. If the transition is from any other state the USB 2.0 pull-up shall not be enabled.

### 10.18.2.3 USDPORT.Training

A port transitions to this state from the USDPORT.Powered-on state when Enhanced SuperSpeed Far-end Receiver Terminations are detected.

In this state, the port's link shall be in the Polling state. The corresponding peripheral device USB state shall be Powered (Link Training substate).

As noted in Figure 10-26, the peripheral device shall disconnect on USB 2.0 within tUSB2SwitchDisconnect after entering this state.

### 10.18.2.4 USDPORT.Connected/Enabled

A port transitions to this state from the USDPORT.Training state when its link enters U0 from Polling.Idle. A port remains in this state during hot reset. When a hot reset is completed, the corresponding peripheral device USB state shall transition to Default.

In this state, the Enhanced SuperSpeed link is in U0, U1, U2, U3 or Recovery and the USB 2.0 pull-up is not applied. The corresponding peripheral device USB state shall be Default, Address, or Configured.

### 10.18.2.5 USDPORT.Error

A port transitions to this state when a serious error condition occurred while attempting to operate the link. A port transitions to this state if the following situation occurs:

- From the USDPORT.Connected/Enabled state if the link enters Recovery and times out without recovering.

In this state, the port's link shall be in the eSS.Inactive state. The corresponding peripheral device USB state shall be Error.

A port exits the USDPORT.Error state only if a Warm Reset is received on the link or if Far-end Receiver Terminations are removed.

10-91

Universal Serial Bus 3.1 Specification, Revision 1.0

### 10.18.2.6 USDPORT.Disabled

A port transitions to this state

- From the USDPORT.Powered on state when Far-end Receiver Terminations are not detected as per the rules described below:

If USDPORT.Powered on was entered from any state except USDPORT.Disabled then this transition shall take place if Far-end Receiver Terminations (RRX-DC) are not detected after eight successive Rx.Detect.Quiet to Rx.Detect.Active transitions.

If USDPORT.Powered on was entered from the USDPORT.Disabled state, then this transition shall take place the first time that Far-end Receiver Terminations are not detected in the Rx.Detect.Active substate.

- From the USDPort.Training state if a timeout occurs on any Polling substate (see Figure 7-18).
- From the USDPort.Connected state, if the Port Configuration process times out (see Section 8.4.6).

A count (Disabled_count) shall be maintained of each entry into the USDPort.Disabled state.

- Count is initialized to "0" upon power on reset.
- The count is incremented upon each entry into the USDPort.Disabled state from the USDPORT.Training Initiated state.
- If the count equals 3, the port transitions to the Disabled.Error state.
- The count is reset to "0" upon a successful completion of the Port Configuration process.

In this state, the port's link shall be in the eSS.Disabled state. The corresponding peripheral device USB state shall be USB 2.0 Device States.

### 10.18.2.7 USDPORT.Disabled_Error

A port transitions to this state from the USDPort.Disabled state when Disabled_Count = 3

- The port shall remain in USDPORT.Disabled_Error state if the port's link receives a USB 2.0 reset.

In this state, a fatal error has been detected on the port's link and the link shall be in the eSS.Disabled state. The corresponding peripheral device USB state shall be USB 2.0 Device States.

10-92

Hub, Host Downstream Port, and Device Upstream Port Specification

## 10.19 Hub Chapter Parameters

Table 10-19 includes a complete list of the parameters used in the hub chapter.

Table 10-19. Hub Parameters

[tbl-252.md](tbl-252.md)

10-93

Universal Serial Bus 3.1 Specification, Revision 1.0

[tbl-253.md](tbl-253.md)

10-94

# 11 Interoperability and Power Delivery

This chapter defines interoperability and power delivery requirements for USB 3.1. Areas covered include USB 3.1 host and device support for USB 2.0 operation, and USB 3.1 VBUS power consumption limits.

Table 11-1 lists the compatibility matrix for USB 3.1 and USB 2.0. The implication of identifying a host port as supporting USB 3.1 is that both hardware and software support for USB 3.1 is in place; otherwise the port shall only be identified as a USB 2.0 port.

Table 11-1. USB 3.0 and USB 2.0 Interoperability

[tbl-254.md](tbl-254.md)

It should be noted that USB 3.1 devices are not required to be backward compatible with USB 1.1 host ports although supporting full-speed and low-speed modes are allowed.

## 11.1 USB 3.1 Host Support for USB 2.0

USB 3.1-capable ports on hosts shall also support USB 2.0 operation in order to enable backward compatibility with USB 2.0 devices. It should be noted, however, that USB 3.1-capable hosts are not required to support Enhanced SuperSpeed operation on all of the ports available on the host, i.e., some USB 3.1-capable hosts may have a mix of USB 2.0-only and USB 3.1-capable ports.

To address the situation where a USB 3.1 device is connected to a USB 2.0-only port on a USB 3.1-capable host, after establishing a USB 2.0 high-speed connection with the device, it is recommended that the host inform the user that the device will support Enhanced SuperSpeed operation if it is moved to a USB 3.1-capable port on the same host. If a USB 3.1 device is connected to a USB 3.1-capable host via a USB 2.0 hub, it is recommended that the host inform the user that the device will support Enhanced SuperSpeed operation if it is moved to an appropriate host port or if the hub is replaced with a USB 3.1 hub.

When a USB 3.1 hub is connected to a host's USB 3.1-capable port, both USB 3.1 Enhanced SuperSpeed and USB 2.0 high-speed bus connections shall be allowed to connect and operate in parallel. There is no requirement for a USB 3.1-capable host to support multiple parallel connections to peripheral devices.

The USB 2.0 capabilities of a USB 3.1 host shall be designed to the USB 2.0 specification and shall meet the USB 2.0 compliance requirements.

11-1

Universal Serial Bus 3.1 Specification, Revision 1.0

## 11.2 USB 3.1 Hub Support for USB 2.0

All ports, both upstream and downstream, on USB 3.1 hubs shall support USB 2.0 operation in order to enable backward compatibility with USB 2.0 devices.

When another USB 3.1 hub is connected in series with a USB 3.1 hub, both SuperSpeed and USB 2.0 high-speed bus connections shall be allowed to connect and operate in parallel. There is no requirement for a USB 3.1 hub to support multiple parallel connections to peripheral devices.

Within a USB 3.1 hub, both the Enhanced SuperSpeed and USB 2.0 hub devices shall implement in the hub framework a common standardized ContainerID to enable software to identify the physical relationship of the hub devices. The ContainerID descriptor is a part of the BOS descriptor set.

The USB 2.0 capabilities of a USB 3.1 hub shall be designed to the USB 2.0 specification and shall meet the USB 2.0 compliance requirements.

## 11.3 USB 3.1 Device Support for USB 2.0

In most cases, backward compatible operation at USB 2.0 signaling is supported by USB 3.1 devices in order that higher capability devices are still useful with lesser capable hosts and hubs. For product installations where support for USB 3.1 operation can be independently assured between the device and the host, such as internal devices that are not user accessible, device support for USB 2.0 may not be necessary. USB 3.1 device certification requirements require support for USB 2.0 for all user attached devices.

For any given USB 3.1 peripheral device within a single physical package, only one USB connection mode, either Enhanced SuperSpeed or a USB 2.0 speed but not both, shall be established for operation with the host.

Peripheral devices may implement in the device framework a common standardized ContainerID to enable software to identify all of the functional components of a specific device and independent of which speed bus it appears on. All devices within a compound device that support ContainerID shall return the same ContainerID.

The USB 2.0 capabilities of a USB 3.1 device shall be designed to the USB 2.0 specification and shall meet the USB 2.0 compliance requirements. Note that a USB 3.1 device operating in one of the USB 2.0 modes must return 0210H in the bcd version field of the device descriptor.

## 11.4 Power Distribution

This section describes the USB 3.1 power distribution specification. The USB 2.0 power distribution requirements still apply when a USB 3.1 device is operating at high-speed, full-speed, or low-speed. Note that a USB 3.1 peripheral device shall not draw more than 100 mA until it detects far-end Rx terminations in the unconfigured state.

11-2

Interoperability and Power Delivery

### 11.4.1 Classes of Devices and Connections

USB 3.1 provides power over two connectors: the Standard-A connector and the MicroAB connector (when the ID pin is connected to ground). The following sections focus on the power delivery requirements for the Standard-A connector.

The power source and sink requirements of different device classes can be simplified with the introduction of the concept of a unit load. A unit load for Enhanced SuperSpeed has been redefined to be 150 mA. The number of unit loads a device can draw is an absolute maximum, not an average over time. A device may be either low-power at one unit load or high-power, consuming up to six unit loads. All devices default to low-power when first powered. The transition to high-power is under software control. It is the responsibility of software to ensure adequate power is available before allowing devices to consume high-power.

The USB supports a range of power sourcing and power consuming agents; these include the following:

- Root port hubs: Are directly attached to the USB Host Controller. Hub power is derived from the same source as the Host Controller. Systems that obtain operating power externally, either AC or DC, must be capable of supplying at least six unit loads to each port. Such ports are called high-power ports. Battery-powered systems may supply either one or six unit loads. Ports that can supply only one unit load are termed low-power ports.
- Self-powered hubs: Power for the internal functions and downstream facing ports does not come from VBUS. However, the USB interface of the hub may draw up to one unit load from VBUS on its upstream facing port to allow the interface to function when the remainder of the hub is powered down. Hubs that obtain operating power externally (not from VBUS) must supply six unit loads to each port.
- Low-power bus-powered devices: All power to these devices comes from VBUS. They may draw no more than one unit load at any time.
- High-power bus-powered devices: All power to these devices comes from VBUS. They must draw no more than one unit load upon power-up and may draw up to six unit loads after being configured.
- Ports may support the USB Charging Specification.
- Self-powered devices: May draw up to one unit load from VBUS to allow the USB interface to function when the remainder of the function is powered down. All other power comes from an external (not from VBUS) source.

No device shall supply (source) current on VBUS at its upstream facing port at any time. From VBUS on its upstream facing port, a device may only draw (sink) current. Devices must also ensure that the maximum operating current drawn by a device is one unit load until configured.

11-3

Universal Serial Bus 3.1 Specification, Revision 1.0

### 11.4.1.1 Self-powered Hubs

Self-powered hubs have a local power supply that furnishes power to any non-removable functions and to all downstream facing ports, as shown in Figure 11-1. Power for the Hub Controller, however, may be supplied from the upstream VBUS (a "hybrid" powered hub) or the local power supply. The advantage of supplying the Hub Controller from the upstream supply is that communication from the host is possible even if the device's power supply remains off. This makes it possible to differentiate between a disconnected and an unpowered device. If the hub draws power for its upstream facing port from VBUS, it may not draw more than one unit load.

![img-284.jpeg](img-284.jpeg)

Figure 11-1. Compound Self-powered Hub

The maximum number of ports that can be supported is limited by the capability of the local VBUS supply.

#### 11.4.1.1.1 Over-current Protection

The host and all self-powered hubs must implement over-current protection for safety reasons, and the hub must have a way to detect the over-current condition and report it to the USB software. Should the aggregate current drawn by a gang of downstream facing ports exceed a preset value, the over-current protection circuit removes or reduces power from all affected downstream facing ports. The over-current condition is reported through the hub to the Host Controller, as described in Section 10.13.5. The preset value cannot exceed 5.0 A and must be sufficiently higher than the maximum allowable port current or time delayed such that transient currents (e.g., during power up or dynamic attach or reconfiguration) do not trip the over-current protector. If an over-current condition occurs on any port, subsequent operation of the USB is not guaranteed, and once the condition is removed, it may be necessary to reinitialize the bus as would be done upon power-up. The over-current limiting mechanism must be resettable without user mechanical intervention.

11-4

Interoperability and Power Delivery

Polymeric PTCs and solid-state switches are examples of methods that can be used for over-current limiting.

### 11.4.1.2 Low-power Bus-powered Devices

A low-power device is one that draws up to one unit load from the USB cable when operational. Figure 11-2 shows a typical bus-powered, low-power device, such as a mouse. Low-power regulation can be integrated into the device silicon. Low-power devices must be capable of operating with input VBUS voltages as low as 4.00 V, measured at the plug end of the cable.

![img-285.jpeg](img-285.jpeg)

Figure 11-2. Low-power Bus-powered Function

### 11.4.1.3 High-power Bus-powered Devices

A device is defined as being high-power if, when fully powered, it draws over one but no more than six unit loads from the USB cable. A high-power device requires staged switching of power. It must first come up in a reduced power state of less than one unit load. At bus enumeration time, its total power requirements are obtained and compared against the available power budget. If sufficient power exists, the remainder of the device may be powered on. High-power devices shall be capable of operating with an input voltage as low as 4.00 V. They must also be capable of operating at full power (up to six unit loads) with an input voltage of 4.00 V measured at the device side of the B-series receptacle.

A typical high-power device is shown in Figure 11-3. The device's electronics have been partitioned into two sections. The device controller contains the minimum amount of circuitry necessary to permit enumeration and power budgeting. The remainder of the device resides in the function block.

![img-286.jpeg](img-286.jpeg)

Figure 11-3. High-power Bus-powered Function

11-5

Universal Serial Bus 3.1 Specification, Revision 1.0

### 11.4.1.4 Self-powered Devices

Figure 11-4 shows a typical self-powered device. The device controller is powered either from the upstream bus via a low-power regulator or from the local power supply. The advantage of the former scheme is that it permits detection and enumeration of a self-powered device whose local power supply is turned off. The maximum upstream power that the device controller can draw is one unit load, and the regulator block must implement inrush current limiting. The amount of power that the device block may draw is limited only by the local power supply. Because the local power supply is not required to power any downstream bus ports, it does not need to implement current limiting, soft start, or power switching.

![img-287.jpeg](img-287.jpeg)

Figure 11-4. Self-powered Function

### 11.4.2 Steady-State Voltage Drop Budget

The steady-state voltage drop budget is derived from the following assumptions:

- The nominal 5 V ± 5% source (host or hub) is 4.75 V to 5.25 V.
- The voltage supplied at the connector of hub or root ports shall be between 4.45 V to 5.25 V.
- The maximum voltage drop (for detachable cables) between the A-series plug and B-series plug on VBUS is 171 mV.
- The maximum current for the calculations is 0.9 A.
- The maximum voltage drop for all cables between upstream and downstream on GND is 171 mV.
- The maximum voltage drop for all mated connectors is 27 mV.
- All hubs and peripheral devices shall be able to provide configuration information with as little as 4.00 V at the device end of their B-series receptacle. Both low and high-power devices need to be operational with this minimum voltage.

Figure 11-5 shows the minimum allowable voltages. Note that under transient conditions, the supply at the device can drop to 3.67 V for a brief moment.

11-6

Interoperability and Power Delivery

![img-288.jpeg](img-288.jpeg)

Figure 11-5. Worst-case Voltage Drop Topology (Steady

State) Note: the following assumptions were used in Figure 11-5:

- 3 meter cable assembly with A-series and B-series plugs
- #22AWG wire used for power and ground (0.019 Ω/foot)
- A-series and B-series plug/receptacle pair have a contact resistance of 30 mΩ
- Wire ~380 mΩ series resistance
- IR Drop at device = (((2 * 30 mΩ) + 190 mΩ) * 900 mA) * 2 or 0.450 V

![img-289.jpeg](img-289.jpeg)

Figure 11-6. Worst-case Voltage Drop Analysis Using Equivalent Resistance

[tbl-255.md](tbl-255.md)

11-7

Universal Serial Bus 3.1 Specification, Revision 1.0

### 11.4.3 Power Control During Suspend/Resume

All USB devices may draw up to 2.5 mA during suspend. When configured, bus-powered compound devices may consume a suspend current of up to 12.5 mA. This 12.5 mA budget includes 2.5 mA suspend current for the internal hub plus 2.5 mA suspend current for each port on that internal hub having attached internal functions, up to a maximum of four ports. When computing suspend current, the current from VBUS through the bus pull-up and pull-down resistors must be included.

While in the Suspend state, a device may briefly draw more than the average current. The amplitude of the current spike cannot exceed the device power allocation 150 mA (or 900 mA). A maximum of 1.0 second is allowed for an averaging interval. The average current cannot exceed the average suspend current limit (ICCS, see Table 11-2) during any 1.0-second interval. The profile of the current spike is restricted so the transient response of the power supply (which may be an efficient, low-capacity, trickle power supply) is not overwhelmed. The rising edge of the current spike must be no more than 100 mA/μs. Downstream facing ports must be able to absorb the 900 mA peak current spike and meet the voltage droop requirements defined for inrush current during dynamic attach. Figure 11-7 illustrates a typical example profile for an averaging interval.

![img-290.jpeg](img-290.jpeg)

Figure 11-7. Typical Suspend Current Averaging Profile

Devices are responsible for handling the bus voltage reduction due to the inductive and resistive effects of the cable. When a hub is in the Suspend state, it must still be able to provide the maximum current per port (six unit loads per port for self-powered hubs). This is necessary to support remote wakeup-capable devices that will power-up while the remainder of the system is still suspended. Such devices, when enabled to do remote wakeup, must drive resume signaling upstream within 10 ms of starting to draw the higher, non-suspend current. Devices not capable of remote wakeup must not draw the higher current when suspended.

When devices wakeup, either by themselves (remote wakeup) or by seeing resume signaling, they must limit the inrush current on VBUS. The device must have sufficient on-board bypass capacitance or a controlled power-on sequence such that the current drawn from the hub does not exceed the maximum current capability of the port at any time while the device is waking up.

11-8

Interoperability and Power Delivery

### 11.4.4 Dynamic Attach and Detach

The act of plugging or unplugging a hub or peripheral device must not affect the functionality of another device on other segments of the network. Unplugging a device will stop any transactions in progress between that device and the host. However, the hub or root port to which this device was attached will recover from this condition and will alert the host that the port has been disconnected.

#### 11.4.4.1 Inrush Current Limiting

When a peripheral device or hub is plugged into the network, it has a certain amount of on-board capacitance between VBUS and ground. In addition, the regulator on the device may supply current to its output bypass capacitance and to the device as soon as power is applied. Consequently, if no measures are taken to prevent it, there could be a surge of current into the device which might pull the VBUS on the hub below its minimum operating level. Inrush currents can also occur when a high-power device is switched into its high-power mode. This problem must be solved by limiting the inrush current and by providing sufficient capacitance in each hub to prevent the power supplied to the other ports from going out of tolerance. An additional motivation for limiting inrush current is to minimize contact arcing, thereby prolonging connector contact life.

The maximum droop possible in the hub VBUS is 330 mV. In order to meet this requirement, the following conditions must be met:

- The maximum load (CRPB) that can be placed at the downstream end of a cable is 10 μF in parallel with as small as a 27 Ω resistance. The 10 μF capacitance represents any bypass capacitor directly connected across the VBUS lines in the device plus any capacitive effects visible through the regulator in the device. The 27 Ω resistance represents one unit load of current drawn by the device during connect.
- If more bypass capacitance is required in the device, then the device must incorporate some form of VBUS surge current limiting, such that it matches the characteristics of the above load.
- The hub downstream facing port VBUS power lines must be bypassed (CHPB) with no less than 120 μF of low-ESR capacitance per hub. Standard bypass methods should be used to minimize inductance and resistance between the bypass capacitors and the connectors to reduce droop. The bypass capacitors themselves should have a low dissipation factor to allow decoupling at higher frequencies.

The upstream facing port of a hub is also required to meet the above requirements.

A high-power bus-powered device that is switching from a lower power configuration to a higher power configuration must not cause droop >330 mV on the VBUS at its upstream hub. The device can meet this by ensuring that changes in the capacitive load it presents do not exceed 10 μF.

11-9

Universal Serial Bus 3.1 Specification, Revision 1.0

### 11.4.4.2 Dynamic Detach

When a device is detached from the network with power flowing in the cable, the inductance of the cable will cause a large flyback voltage to occur on the open end of the device cable. This flyback voltage is not destructive. Proper bypass measures on the hub ports will suppress any coupled noise. This will require some low capacitance, very low inductance bypass capacitors on each hub port connector. The flyback voltage and the noise it creates are also moderated by the bypass capacitance on the device end of the cable. Also, there must be some minimum capacitance on the device end of the cable to ensure that the inductive flyback on the open end of the cable does not cause the voltage on the device end to reverse polarity. A minimum of 1.0 μF is recommended for bypass across VBUS.

### 11.4.5 VBUS Electrical Characteristics

Table 11-2. DC Electrical Characteristics

[tbl-256.md](tbl-256.md)

### 11.4.6 Powered-B Connector

The Powered-B connector was defined by USB 3.0 has been deprecated.

11-10

Interoperability and Power Delivery

### 11.4.7 Wire Gauge Table

Table 11-3 is a table of VBUS/Gnd wire gauges showing the relationship between gauge and maximum length in order to achieve the previously cited voltage drop values. The user should note that these lengths are the maximum length possible to meet the voltage drop budget, thus gauges smaller and lengths greater than the table values will fail to deliver the expected voltage value.

Table 11-3. VBUS/Gnd Wire Gauge vs. Maximum Length

[tbl-257.md](tbl-257.md)

11-11

Universal Serial Bus 3.1 Specification, Revision 1.0

11-12

# A Gen 1 Symbol Encoding

Table A-1 shows the byte-to-Symbol encodings for data characters. Table A-2 shows the Symbol encodings for the Special Symbols. RD- and RD+ refer to the Running Disparity of the Symbol sequence on a per-Lane basis.

Table A-1. 8b/10b Data Symbol Codes

[tbl-258.md](tbl-258.md)

A-1

# Universal Serial Bus 3.1 Specification, Revision 1.0

[tbl-259.md](tbl-259.md)

A-2

Gen 1 Symbol Encoding

[tbl-260.md](tbl-260.md)

A-3

# Universal Serial Bus 3.1 Specification, Revision 1.0

[tbl-261.md](tbl-261.md)

A-4

Gen 1 Symbol Encoding

[tbl-262.md](tbl-262.md)

A-5

Universal Serial Bus 3.1 Specification, Revision 1.0

[tbl-263.md](tbl-263.md)

A-6

Gen 1 Symbol Encoding

[tbl-264.md](tbl-264.md)

A-7

Universal Serial Bus 3.1 Specification, Revision 1.0

Table A-2. 8b/10b Special Character Symbol Codes

[tbl-265.md](tbl-265.md)

Note: Only a small fraction of the possible K-characters are defined in this table. Any K-character that decodes to a value that is not in Table A-2 shall be returned as Decode_Error_Substitution (K28.4). Refer to Section 6.3.1.4 and Table 6-1 for more information.

A-8

# B Symbol Scrambling

## B.1 Data Scrambling

The following subroutines encode and decode an 8-bit value contained in “inbyte” with the LFSR. This is presented as one example only; there are many ways to obtain the proper output. This example demonstrates how to advance the LFSR eight times in one operation and how to XOR the data in one operation. Many other implementations are possible but they must all produce the same output as that shown here.

The following algorithm uses the “C” programming language conventions, where “<<” and “>>” represent the shift left and shift right operators, “>” is the compare greater than operator, and “^” is the exclusive or operator, and “&” is the logical “AND” operator.

/*
this routine implements the serial descrambling algorithm in parallel form
for the LSFR polynomial: x^16+x^5+x^4+x^3+1
this advances the LSFR 8 bits every time it is called
this requires fewer than 25 xor gates to implement (with a static register)

The XOR required to advance 8 bits/clock is:
bit 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15
8 9 10 11 12 13 14 15 0 1 2 3 4 5 6 7
8 9 10 11 12 13 14 15
8 9 10 11 12 13 14 15
8 9 10 11 12 13 14 15

The serial data is just the reverse of the upper byte:
bit 0 1 2 3 4 5 6 7
15 14 13 12 11 10 9 8
*/

B-1

Universal Serial Bus 3.1 Specification, Revision 1.0

int scramble_byte(int inbyte)
{
    static int scrambit[16];
    static int bit[16];
    static int bit_out[16];
    static unsigned short lfsr = 0xffff; // 16 bit short for polynomial
    int i, outbyte;

    if (inbyte == COMMA)    // if this is a comma
    {
        lfsr = 0xffff;        // reset the LFSR
        return (COMMA);      // and return the same data
    }

    if (inbyte == SKIP)      // don't advance or encode on skip
        return (SKIP);

    for (i=0; i<16;i++)      // convert LFSR to bit array for legibility
        bit[i] = (lfsr >> i) & 1;

    for (i=0; i<8; i++)      // convert byte to be scrambled for legibility
        scrambit[i] = (inbyte >> i) & 1;

    // apply the xor to the data
    if (! (inbyte & 0x100) &&    // if not a KCODE, scramble the data
        ! (TrainingSequence == TRUE))    // and if not in the middle of
    {                                   // a training sequence
        scrambit[0] ^= bit[15];
        scrambit[1] ^= bit[14];
        scrambit[2] ^= bit[13];
        scrambit[3] ^= bit[12];
        scrambit[4] ^= bit[11];
        scrambit[5] ^= bit[10];
        scrambit[6] ^= bit[9];
        scrambit[7] ^= bit[8];
    }

B-2

Symbol Scrambling

// Now advance the LFSR 8 serial clocks
bit_out[0] = bit[8];
bit_out[1] = bit[9];
bit_out[2] = bit[10];
bit_out[3] = bit[11] ^ bit[8];
bit_out[4] = bit[12] ^ bit[9] ^ bit[8];
bit_out[5] = bit[13] ^ bit[10] ^ bit[9] ^ bit[8];
bit_out[6] = bit[14] ^ bit[11] ^ bit[10] ^ bit[9];
bit_out[7] = bit[15] ^ bit[12] ^ bit[11] ^ bit[10];
bit_out[8] = bit[0] ^ bit[13] ^ bit[12] ^ bit[11];
bit_out[9] = bit[1] ^ bit[14] ^ bit[13] ^ bit[12];
bit_out[10] = bit[2] ^ bit[15] ^ bit[14] ^ bit[13];
bit_out[11] = bit[3]    ^ bit[15] ^ bit[14];
bit_out[12] = bit[4]    ^ bit[15];
bit_out[13] = bit[5];
bit_out[14] = bit[6];
bit_out[15] = bit[7];
lfsr = 0;
for (i=0; i < 16; i++) // convert the LFSR back to an integer
    lfsr += (bit_out[i] << i);

outbyte = 0;
for (i=0; i<8; i++) // convert data back to an integer
    outbyte += (scrambit[i] << i);

return outbyte;
}

/* NOTE THAT THE DESCRAMBLE ROUTINE IS IDENTICAL TO THE SCRAMBLE ROUTINE
this routine implements the serial descrambling algorithm in parallel form
this advances the lfsr 8 bits every time it is called
this uses fewer than 25 xor gates to implement (with a static register)
The XOR tree is the same as the scrambling routine
*/

B-3

Universal Serial Bus 3.1 Specification, Revision 1.0

int unscramble_byte(int inbyte)
{
    static int descrambit[8];
    static int bit[16];
    static int bit_out[16];
    static unsigned short lfsr = 0xffff; // 16 bit short for polynomial
    int outbyte, i;

    if (inbyte == COMMA) // if this is a comma
    {
        lfsr = 0xffff; // reset the LFSR
        return (COMMA); // and return the same data
    }

    if (inbyte == SKIP) // don't advance or encode on skip
        return (SKIP);

    for (i=0; i<16;i++) // convert the LFSR to bit array for legibility
        bit[i] = (lfsr >> i) & 1;

    for (i=0; i<8; i++) // convert byte to be de-scrambled for legibility
        descrambit[i] = (inbyte >> i) & 1;

    // apply the xor to the data
    if (! (inbyte & 0x100) && // if not a KCODE, scramble the data
        ! (TrainingSequence == TRUE)) // and if not in the middle of
    { // a training sequence
        descrambit[0] ^= bit[15];
        descrambit[1] ^= bit[14];
        descrambit[2] ^= bit[13];
        descrambit[3] ^= bit[12];
        descrambit[4] ^= bit[11];
        descrambit[5] ^= bit[10];
        descrambit[6] ^= bit[9];
        descrambit[7] ^= bit[8];
    }

B-4

Symbol Scrambling

// Now advance the LFSR 8 serial clocks
bit_out[0] = bit[8];
bit_out[1] = bit[9];
bit_out[2] = bit[10];
bit_out[3] = bit[11] ^ bit[8];
bit_out[4] = bit[12] ^ bit[9] ^ bit[8];
bit_out[5] = bit[13] ^ bit[10] ^ bit[9] ^ bit[8];
bit_out[6] = bit[14] ^ bit[11] ^ bit[10] ^ bit[9];
bit_out[7] = bit[15] ^ bit[12] ^ bit[11] ^ bit[10];
bit_out[8] = bit[0] ^ bit[13] ^ bit[12] ^ bit[11];
bit_out[9] = bit[1] ^ bit[14] ^ bit[13] ^ bit[12];
bit_out[10] = bit[2] ^ bit[15] ^ bit[14] ^ bit[13];
bit_out[11] = bit[3] ^ bit[15] ^ bit[14];
bit_out[12] = bit[4] ^ bit[15];
bit_out[13] = bit[5];
bit_out[14] = bit[6];
bit_out[15] = bit[7];
lfsr = 0;
for (i=0; i < 16; i++) // convert the LFSR back to an integer
    lfsr += (bit_out[i] << i);

outbyte = 0;
for (i=0; i<8; i++) // convert data back to an integer
    outbyte += (descrambit[i] << i);

return outbyte;

The initial 16-bit values of the LFSR for the first 128 LFSR advances following a reset are listed below:

[tbl-266.md](tbl-266.md)

B-5

Universal Serial Bus 3.1 Specification, Revision 1.0

An 8-bit value of 0 repeatedly encoded with the LFSR after reset produces the following consecutive 8-bit values:

[tbl-267.md](tbl-267.md)

B-6

# C Power Management

This appendix offers a system level overview of Enhanced SuperSpeed's power management features and capabilities. The following topics are also included:

- Examples of how end to end low power link state exit latencies are calculated
- A discussion of device-initiated link power management policies
- An example device implementation for Latency Tolerance Messaging
- System power considerations for SuperSpeed versus High Speed device interfaces

## C.1 SuperSpeed Power Management Overview

The SuperSpeed architecture has been defined with platform power efficiency as a primary objective. Some of the key power efficiency enhancements include:

- Elimination of continuous device polling
- Elimination of broadcast packet transmission through hubs
- Introduction of link power management states enabling aggressive power savings when idle
- Host and device initiated transition to low power states
- Device and individual Function level suspend capabilities enabling devices to remove power from all, or only those portions of their circuitry that are not in use

### C.1.1 Link Power Management

Link power management enables a link to be placed into a lower power state when the link partners are idle. The longer a pair of link partners remain idle, the deeper the power savings that can be achieved by progressing from U0 (link active) to U1 (link standby with fast exit), to U2 (link standby with slower exit), and finally to U3 (suspend).

After being configured by software, the U1 and U2 link states are entered and exited via hardware autonomous control. Hardware autonomous transitions for the U1 and U2 link states enable faster response times. This, in turn, translates to better power savings when entering a power saving state, and less impact on the operational state when exiting. The U3 link state however is entered only under software control, typically after a software inactivity timeout, and is exited either by software (host initiated exit) or hardware (remote wakeup). The U3 link state is directly coupled to the device's suspend state (refer to Section C.1.4).

C-1

Universal Serial Bus 3.1 Specification, Revision 1.0

### C.1.1.1 Summary of Link States

Table C-1 provides a summary characterization of the SuperSpeed link states.

Table C-1. Link States and Characteristics Summary

[tbl-268.md](tbl-268.md)

Notes:

1. It is possible, under system test conditions, to instrument software initiated U1 and U2 state transitions.

2. From a power efficiency perspective it is desirable for devices to turn off their clock generation circuitry (e.g., their PLL) during the U2 link state.

### C.1.1.2 U0 – Link Active

U0 is the fully operational, link active state. Packets of any type may be communicated over a link that is in the U0 State.

### C.1.1.3 U1 – Link Idle with Fast Exit

U1 is a power saving state this is characterized by fast transition time back to the U0 State. Note that the predominant latency, when transitioning from the U1 → U0 state is imposed by the time that is required to achieve symbol lock between the two link partners.

### C.1.1.3.1 U1 Entry

Either link partner for a given link can request a transition to the U1 link state. All downstream ports (hub or root ports) track inactivity using an inactivity timer mechanism. When a port's inactivity timer expires, if enabled, it requests transition to the U1 state. Upstream ports may also initiate U1 entry based on device specific policies.

When a port initiates U1 entry, its link partner may either accept or reject the request. The link level U0 → U1 transition process consists of one port transmitting an LGO_U1 link command, and its link partner responding with either an LAU (accept the request) or an LXU (reject the request) link command.

The most typical reason for rejecting a U1 transition request would be because the requesting port's link partner has some activity which will shortly require a packet transmission. Downstream ports would also reject a U1 transition request if not enabled to accept U1 transition requests. Rejection of a U1 transition request by an upstream port simply resets and restarts the requesting link partner's inactivity timer.

C-2

Power Management

System software configures and then enables each device to initiate U1 entry. The primary programming parameters involved in setting up hardware autonomous link state management include:

**U1DevExitLat** – Parameter used by devices to report their maximum U1 to U0 exit latency (refer to Chapter 9 for details).

**PORT_U1_TIMEOUT** – Sets the value for the downstream port’s U1 inactivity timer. When specifying a value between the range 0x01-0xFE it also enables the downstream port to send U1 entry transition requests to its link partner (refer to Chapter 10 for details).

**U1_Enable** – Enables an upstream port to initiate requests for transition into U1 (refer to Chapter 9 for details).

The U1_Enable feature controls whether that particular upstream port may initiate U1 entry. Regardless of whether the upstream port is enabled for U1 entry initiation or not, it still responds to requests for U1 entry from its link partner, either accepting or rejecting the transition request.

The following table illustrates the relationship between the downstream timeout and the upstream U1_Enable to configure the platform for any combination of port link state management. For example, if U1_Enable is enabled, and PORT_U1_TIMEOUT is set to FFH, then only the upstream port may initiate requests for transition to U1.

[tbl-269.md](tbl-269.md)

For detailed information regarding the specifics of the U1 entry process, refer to Chapter 7 of this specification.

### C.1.1.3.2 Exiting the U1 State

There are two ways to exit the U1 state. The link can return to the active U0 state or it can transition into a deeper power savings state (U2).

# **Transitioning from U1 → U0**

Either link partner can initiate a transition from U1 → U0. This transition is normally initiated when a packet needs to be transmitted, such as an IN message from the host, or an ERDY message from a device. The transition process is initiated by first signaling a Low Frequency Periodic Signaling (LFPS) handshake. This is followed by link recovery and training sequences. Refer to Chapter 6 and 7 respectively.

# **Transitioning from U1 → U2**

This transitions the link to an even lower power state and is triggered by a second inactivity timer (U2 inactivity timer). When a link enters U1, this starts the U2 inactivity timer. If the U2 inactivity timer expires while the link is still in U1, then both link partners transition silently from U1 → U2 without additional bus activity. The next sections discuss this in more detail.

C-3

Universal Serial Bus 3.1 Specification, Revision 1.0

### C.1.1.4 U2 – Link Idle with Slow Exit

The purpose of the U2 link state is to use less power than the U1 state, however at the cost of increased exit latency. For example, clock generation circuitry may be quiesced in order to save additional power in comparison with U1. Under some implementation-specific circumstances, this may not make sense. For example, a hub may share one PLL across all of its ports so the PLL cannot be quiesced unless all of its ports are in U2.

The primary parameters involved in configuring a port for U2 link transitions include:

U2DevExitLat – Parameter used by devices to report their maximum U2 to U0 exit latency (refer to Chapter 9 for details).

PORT_U2_TIMEOUT – Sets the value of a downstream port's U2 inactivity timer. When specified with a value in the range 0x01-0xFE it also enables the downstream port to initiate U2 entry transition requests to its link partner (refer to Chapter 10 for details).

U2_Enable – Enables an upstream port to initiate requests for transitions into U2 (refer to Chapter 9 for details).

The U2_Enable feature controls whether an upstream port may initiate U2 entry from U0. Regardless of whether the upstream port is enabled for U2 entry initiation or not, it still responds to requests for U2 entry from its link partner, either accepting or rejecting the transition request.

The following table illustrates the relationship between the downstream timeout and the upstream U2_Enable to configure the platform for any combination of port link state management. For example, if U2_Enable is enabled, and PORT_U2_TIMEOUT is set to FFH, then only the upstream port may initiate requests for transition to U2.

[tbl-270.md](tbl-270.md)

### Transitioning from U1 → U2

U2 is typically entered directly from U1 as mentioned earlier. The U2 inactivity timer starts when a link enters U1, and when the U2 inactivity timer expires both link partners silently transition from U1 → U2.

Both link partners must be configured with the same U2 inactivity timeout value. This is done by first having software program the U2 inactivity timeout in the downstream port. The downstream port then sends an LMP containing the U2 inactivity timeout value to its link partner. Any changes to this value on the downstream port are also updated with the link partner in the same manner (refer to Chapter 10).

Note that U2 inactivity timer synchronization between link partners can never be perfect so there can be brief periods of time where one port is in U2 while its link partner is still in U1. However given that the U1 → U0 and U2 → U0 state transition processes are compatible with one another this corner condition is handled cleanly.

C-4

Power Management

# Transitioning directly to U2 from U0

A downstream port can be configured for direct, hardware autonomous transition from U0 → U2 by programming its U1 inactivity timer to zero while programming its U2 inactivity timer with a non-zero value in the range 0x01- 0xFE. In this case, when the U2 inactivity timer expires, the downstream port initiates U2 entry from U0.

When a port initiates U2 entry from U0, its link partner may either accept or reject the request. The link level U0 → U2 transition process consists of one port transmitting an LGO_U2 Link Command, and its link partner responding with either an LAU (accept the request) or an LXU (reject the request) Link Command.

# Exiting U2

Exiting U2 can only result in a link state transition to U0. Either link partner can initiate U2 exit, which is initiated when a packet needs to be transmitted. The exit process is similar to that of a U1 → U0 transition, consisting of a Low Frequency Periodic Signaling handshake followed by link recovery and training.

# C.1.1.5 U3 – Link Suspend

The U3 state is a deep power saving state where portions of device power may be removed, except as needed to perform the following functions:

- For upstream ports in devices and hubs:

- Warm Reset signaling detection
- Wakeup signaling detection (for host initiated wakeup)
- Wakeup signaling transmission (for remote wakeup capable devices)

- For downstream ports in hubs and hosts:

- Warm Reset generation
- Disconnect event detection
- Wakeup signaling detection (for remote wakeup)
- Wakeup signaling transmission (for host initiated wakeup)

The purpose of U3 is to minimize power consumption during device or system suspend.

Vbus remains active during U3. Any power rail switching by devices is implementation specific and beyond the scope of this specification.

# Entering the U3 State

U3 entry may only be initiated by the host (refer to Chapter 10 for details). Software typically implements an inactivity timeout for the purpose of placing a function into suspend following a long period of inactivity.

When a downstream port initiates a U3 entry request, its link partner is not allowed to reject it. The downstream port sends an LGO_U3 Link Command, and its link partner responds with an LAU Link Command (refer to Chapter 7 for details).

C-5

Universal Serial Bus 3.1 Specification, Revision 1.0

# Exiting the U3 State

The only legitimate link state transition from U3 is U3 → U0, and either link partner can initiate it.

Host software initiates U3 exit on a downstream port by issuing a

SetPortFeature(PORT_LINK_STATE) request to the desired downstream port. Upstream ports (e.g., upstream port of a hub, or a peripheral device), initiate U3 exit in response to a remote wakeup event. An example of this would be an incoming Wake on LAN packet for a USB attached network interface device. The exit process consists of a Low Frequency Periodic Signaling (LFPS) handshake followed by link recovery and training.

# Device Initiated U3 Exit

If the exit was initiated by a device, the specific function within the device that initiated the wakeup would follow up the LFPS triggered transition to U0 by sending a Function Wake device notification packet to the host.

# Host initiated U3 Exit

For host initiated U3 exit, the LFPS handshake process allows devices up to 20 ms to complete, allowing sufficient time for a device to turn on a switched power rail if implemented (refer to Chapter 6 for details).

The software interface associated with U3 consists of a set of port controls and function controls. The port controls, e.g., initiating U3 on a hub downstream port, are described in Section C.1.2.3. The function controls, e.g., enabling a function (device) for remote wakeup, are described in Section C.1.4.1.

# C.1.2 Link Power Management for Downstream Ports

Hubs play several critical roles in link power management. They perform the following functions:

- Coordinate the upstream port link power management state with that of their downstream ports.
- Handle packet deferral, where the hub tells the host that a packet was sent to a downstream port that is not currently in U0.
- Provide inactivity timers on downstream ports to initiate U1 and U2 entry.

# C.1.2.1 Link State Coordination and Management

A hub monitors its downstream ports' link states and keeps its upstream port in the lowest power link state it can without allowing it to be in a lower power state than any of its downstream ports. The intent for this policy is to ensure that the path to the host, (i.e., the upstream port), is as active as the most active of its downstream ports.

When a device initiates a transition from a low power state back to U0 on a hub downstream port, the hub begins transitioning its upstream port to U0 immediately, in parallel with the downstream port.

For packets traveling downstream, hubs must first receive the packet, determine which of its downstream ports the packet is targeted at, and then only initiate a transition to U0 for that particular downstream port.

USB 3.0 hubs use a unicast packet transmission model and this improves the power efficiency of the platform in every instance where a hub is deployed. USB 3.1 hubs use a store and forward

C-6

Power Management

packet transmission model with multiple INs in flight. However, this does not impact the link power management as the packets are routed only through the ports directly between the host and device.

### C.1.2.2 Packet Deferring

Packet deferring is a mechanism that enables efficient bus utilization while supporting aggressive link power management. Packet deferring achieves this by enabling a hub to respond on behalf of a downstream device whose link is in a low power state. This allows the host to make forward progress while the device is brought back to the active state.

# **Hub's Role in Packet Deferring**

After receiving a header packet from the host and detecting a packet deferring condition, the hub informs the host of this by sending a deferred header packet back to the host. The hub also sends the original header packet to the device, with the deferred field asserted, once it is brought back to the U0 state. The host treats this deferred header packet as it would receipt of an NRDY, and so is then free to initiate transfers with other devices' endpoints instead of waiting for the sleeping link to return to U0 (refer to Chapter 10 for details).

# **Device's Role in Packet Deferring**

When a device receives an IN or an OUT header packet with the deferred field asserted, it prepares for the transfer, sends an ERDY to the host when ready, and keeps its link in U0 until the transfer occurs.

The host ultimately responds to the ERDY by rescheduling the original transfer.

### C.1.2.3 Software Interface

The software interface for downstream port power management consists of the following port controls and status fields:

- PORT_LINK_STATE feature and port status field
- PORT_REMOTE_WAKE_MASK feature
- C_PORT_LINK_STATE port status change bit
- PORT_U1_TIMEOUT feature
- PORT_U2_TIMEOUT feature

# **The PORT_LINK_STATE**

This feature is used to request a link state change from any current U-state to any next U-state. In a normal operating environment, this feature is used solely to request U0 → U3 and U3 → U0 transitions. It can be used for test purposes though, to request other state transitions.

# **The PORT_REMOTE_WAKE_MASK**

This feature is used to mask each remote wakeup event that might be originated at a downstream port.

Note that if remote wake notifications for connect, disconnect, or over current events are disabled, these events are still captured and reported as port status change events after the host or hub is resumed.

C-7

Universal Serial Bus 3.1 Specification, Revision 1.0

# C_PORT_LINK_STATE

This flag is used to signal completion of a transition from U3 → U0. Specifically, assertion of this flag results from a host initiated wakeup on a downstream port.

Once the C_PORT_LINK_STATE flag is set, a port status change event is sent to system software indicating that the downstream port and its link partner have completed the transition to the U0 state.

Note that C_PORT_LINK_STATE is not asserted in the event of a remote wakeup. As discussed previously, in the event of a Remote Wakeup the associated function sends the host a Function Wake device notification packet.

# PORT_U1_TIMEOUT

This feature is used to enable and disable U1 entry on downstream ports. It also specifies the U1 inactivity timeout value.

[tbl-271.md](tbl-271.md)

# PORT_U2_TIMEOUT

This feature is used to enable and disable U2 on downstream ports, and also to set an inactivity timeout for initiating a transition to U2.

[tbl-272.md](tbl-272.md)

Other hub port controls can impact link power management behavior, e.g., the PORT_RESET feature, but are not covered here (refer to Chapter 10 for details).

### C.1.3 Other Link Power Management Support Mechanisms

#### C.1.3.1 Packets Pending Flag

Devices may use the Packets Pending flag (refer to Chapter 8) to help decide when to place their link in a low power state. The Packets Pending flag provides an indication of whether the host controller has any additional packets to transfer on the schedule associated with a given non-Stream

C-8

Power Management

endpoint. When there are no more packets pending for all non-Stream endpoints on a device, the device may place its link in a low power state immediately.

For Stream endpoints, the Packet Pending flag is an indication of whether the host controller has any additional packets to transfer on the schedule associated with a given Stream. When there are no more packets pending for any Streams and for all endpoints on a device, the device may place its link in a low power state immediately.

### C.1.3.2 Support for Isochronous Transfers

If a link is in a low power state when an isochronous transfer is scheduled, the latency to transition to U0 from source to destination could potentially delay the transfer beyond its subscribed isochronous service interval.

To ensure that isochronous service contract guarantees are satisfied, a SuperSpeed mechanism (Ping) has been defined to bring all paths between the host and an isochronous endpoint to U0 as a routine step in servicing isochronous endpoints.

The host controller, with sufficient information to know how long any given path might take to become fully active, factors this link path exit latency into its isochronous service scheduler and uses the Ping protocol to ensure that the links are brought to a fully active state in time to meet the isochronous service contract.

The ping process consists of the following:

- The host sends a PING packet to a device.
- Hubs route the PING packet toward the targeted device.
- The device responds to the PING packet by sending a PING_RESPONSE packet to the host.
- The device keeps its link in U0 until it receives a subsequent packet from the host.

After sending a PING packet to one device and prior to receiving a PING_RESPONSE packet, the host may transfer data with other devices. Much like the Packet Deferring mechanism, the Ping mechanism enables efficient bus utilization while at the same time supporting significant power savings.

### C.1.3.3 Support for Interrupt Transfers

If any links between the host and a scheduled interrupt endpoint are in a low power state, the latency to transition the end to end pathway to U0 could potentially delay the transfer beyond the subscribed interrupt service interval. A host controller, possessing knowledge of link path exit latency between itself and any given device within the link hierarchy, is able to schedule interrupt transfers far enough in advance to compensate for these latencies.

### C.1.4 Device Power Management

Device power management is directed primarily under software control, with various hardware mechanisms to support it. Device power management consists of some function level mechanisms plus some device and hub mechanisms.

C-9

Universal Serial Bus 3.1 Specification, Revision 1.0

### C.1.4.1 Function Suspend

A function may be placed into function suspend independent of other functions using the FUNCTION_SUSPEND feature. The FUNCTION_SUSPEND feature is also used to enable function remote wakeup (refer to Chapter 9 for details).

If a composite device has at least one of its functions in suspend while other functions remain active, i.e., the device's upstream port is not in U3, a mechanism is needed for a suspended function to signal a remote wakeup. This is done with the Function Wake device notification packet (refer to Chapter 8 for details).

### C.1.4.2 Device Suspend

Device suspend is a device-wide state entered and exited intrinsically as a result of a device's upstream port entering and exiting the U3 state. A device may be transitioned into device suspend regardless of the function suspend state of any function within the device.

Devices may implement a switched power rail and remove power from large portions of the device while in suspend. Some device state information must be retained in a persistent state during suspend (refer to Chapter 9 for details).

### C.1.4.3 Host Initiated Suspend

#### Suspending a Device

The host transitions a device into the suspend state according to the following sequence:

- Enable remote wakeup, if needed
- A SetPortFeature(PORT_LINK_STATE, U3) request is issued to the downstream port of which the targeted device is its link partner.
- The downstream port initiates U3 entry by sending an LGO_U3 link command.
- The device sends an LAU link command (acceptance is non-negotiable).
- The downstream port sends an LPMA link command.
- Both link partners transition their transmitters to electrical idle and enter the U3 state (refer to Chapter 7 for details).

#### Suspending the USB Link Hierarchy

A link hierarchy of devices and hubs is placed into suspend on a device by device basis under host software control. First, all peripheral devices in the hierarchy are placed into suspend. Then the hubs connected to the peripheral devices are placed into suspend. This is repeated all the way up the hierarchy until reaching the root ports of the USB hierarchy.

Note that by using the same technique a select subset of a given USB link hierarchy could be suspended rather then the whole of it if so desired.

C-10

Power Management

### C.1.4.4 Host Initiated Wake from Suspend

Host initiated wake from suspend (U3 → U0) of an individual device, group of devices, or of the entire link hierarchy is accomplished using the same repetitive process, one link at a time.

Figure C-1 illustrates the Host initiated Wake Sequence.

![img-291.jpeg](img-291.jpeg)

Figure C-1. Flow Diagram for Host Initiated Wakeup

### C.1.4.5 Device Initiated Wake from Suspend

A device initiated transition from suspend (U3 → U0) follows the sequence outlined below:

1. The device transmits LFPS wakeup signaling to its link partner.
2. The LFPS signaling is propagated upstream until it reaches the root hub or a hub that is not in U3. This hub is referred to as the Controlling Hub.
3. The Controlling Hub then automatically reflects LFPS wakeup signaling on the downstream port which had received (from the opposite direction) the wakeup signaling.
4. Each hub in the direct path to the remote wakeup device propagates the wakeup signaling downstream on the hub downstream port that had received wakeup signaling. As the wakeup signaling is propagated downstream, each link completes the LFPS handshake and transitions to U0 (refer to Chapters 6 and 7 for details).
5. After all of the links between the Controlling Hub and the remote wakeup device transition to U0, the function within the remote wakeup device that had originated the remote wakeup sends a Function Wake device notification packet to the host. This in turn causes a software interrupt, and in the service of this interrupt the function suspend state is cleared for that function.

C-11

Universal Serial Bus 3.1 Specification, Revision 1.0

### C.1.5 Platform Power Management Support

The Latency Tolerance Message (LTM) feature allows a platform to make dynamic tradeoffs between power and performance. It enables this, in cooperation with devices, without imposing additional cost.

The LTM protocol enables USB devices to inform the host how long they can tolerate lack of service before experiencing unintended side effects. Each device provides this information in the form of a Best Effort Latency Tolerance (BELT) value. A given device's BELT value is derived considering all configured endpoints, typically conforming to the endpoint with the lowest latency tolerance.

LTM provides the ability for a device to dynamically change its BELT value to more accurately reflect, for example, long periods of anticipated idle time. The platform can potentially take advantage of this insight and, along with other system-related information, conserve more energy at the system level without running the risk of unintended side effects.

### C.1.5.1 System Exit Latency and BELT

A device's reported BELT value has to comprehend not only its own intrinsic design characteristics, such as its internal buffering, but also factor in other associated end to end latencies between itself and the host. These would include other latencies associated with the time required to awaken sleeping links, the number of hubs between the device and the host, host processing time, packet propagation delays, etc. The system provides the device with additional system latency information, through the SET_SEL request, such that the device's intrinsic BELT value can be adjusted downward to account for these other factors. Refer to Chapter 8 for detailed LTM specification and to Chapter 9 for specification details regarding the SET_SEL request.

Device implementation determines the total latency that a device can tolerate. The primary factors are the amount of data that the device is required to produce or consume, and the amount of buffering on the device. The total device latency tolerance must be allocated among different system components.

Figure C-2 illustrates the total latency a device may experience within the context of LTM. The latency is the sum of parameters t1, t2, t3, and t4:

- t1: the time to transition all links in the path to the host to U0 when the transition is initiated by the device
- t2: the time for the ERDY to traverse the interconnect hierarchy from the device to the host
- t3: the time for the host to consume the ERDY and transmit a response to that request
- t4: the time for the response to traverse the interconnect hierarchy from the host to the device

C-12

Power Management

![img-292.jpeg](img-292.jpeg)

Figure C-2. Device Total Intrinsic Latency Tolerance

Devices may calculate their BELT value by subtracting U1SEL or U2SEL (refer to the SET_SEL request in Chapter 9) from their total intrinsic latency tolerance. If the device allows its link to enter U2, then the device calculates its BELT by subtracting U2SEL from its total intrinsic latency tolerance. If the device does not allow its link to enter U2 but does allow its link to enter U1, then the device calculates its BELT by subtracting U1SEL from its total intrinsic latency tolerance.

U1SEL and U2SEL are calculated and programmed by host software. Example calculations for t1 are provided in Section C.2. For LTM purposes t2 and t4 should be calculated by host software as follows:

- For t2, a hub may delay forwarding the ERDY by up to one maximum packet size (approximately 2.1 μs including framing) when there is a transfer in progress. Each additional hub will delay forwarding the ERDY by up to approximately tHubDelay to transfer the packet. The value of t2 is determined as follows:

- If there are zero hubs in the direct path between the device and the host, then t2 is zero
- If there are one or more hubs in the direct path between the device and the host, then t2 is approximately 2.1 μs + tHubDelay * (number of hubs - 1)

- For t4, a hub may delay forwarding a packet by up to approximately tHubDelay. The value of t4 is approximately tHubDelay times the number of hubs in the direct path between the device and the host).

### C.1.5.2 Maximum Exit Latency and PING

The host controller is provided with a Maximum Exit Latency (MEL) value that it uses to schedule a PING relative to a periodic transfer. The Maximum Exit Latency must comprehend worst case round trip delay of sending a PING to a device and receiving the PING_RESPONSE from it.

The Maximum Exit Latency factors in the end to end latencies between host and the device. These would include other latencies associated with the time required to awaken sleeping links, the

C-13

Universal Serial Bus 3.1 Specification, Revision 1.0

number of hubs between the host and the device, device processing time, packet propagation delays, etc.

The Maximum Exit Latency (tMEL) is the sum of parameters tMEL1, tMEL2, tMEL3, and tMEL4.

### C.1.5.2.1 Maximum Exit Latency t1 (tMEL1)

The tMEL1 delay is the time to transition all links in the path to the device to U0 when the transition is initiated by the host. The method for calculating MEL t1 delay is described in Sections C.2.1.1 and C.2.2.1.

### C.1.5.2.2 Maximum Exit Latency t2 (tMEL2)

tMEL2 is the sum of the tHubDelay values for each hub in the path, and tTPTransmissionDelay across each link in the path is calculated as:

$$\text{tMEL2} = (\text{sum of wHubDelay values}) + (\text{tTPTransmissionDelay} * (\text{number of hubs} + 1)).$$

Where, a wHubDelay value is provided by the SuperSpeed Hub Descriptor of each hub in the path, respectively, and tTPTransmissionDelay is defined in Table 8-33.

### C.1.5.2.3 Maximum Exit Latency t3 (tMEL3)

The tMEL3 delay is the time for the device to receive the PING and generate the PING_RESPONSE, which is defined by tPingResponse. Refer to Table 8-33.

### C.1.5.2.4 Maximum Exit Latency t4 (tMEL4)

The tMEL4 delay is the time for the PING_RESPONSE to traverse the interconnect hierarchy from the device to the host. Since wHubDelay defines the downstream and upstream delay through a hub, the propagation delay of a PING_RESPONSE upstream is identical to that of a PING downstream delay (tMEL2), with one exception. In the upstream path a TP may be queued behind a Max Packet Size DP, so an additional 2.1 μs of delay is included to comprehend the “congestion jitter”. tMEL4 is calculated as:

$$\text{tMEL4} = \text{tMEL2} + 2.1 \text{ μs}.$$

C-14

Power Management

## C.2 Calculating U1 and U2 End to End Exit Latencies

This section provides examples of how to calculate the exit latency (i.e., time to transition from a non-U0 state to a U0 state) spanning the end to end path between a device and the host. Examples are given for both device initiated exit and host initiated exit.

Figure C-3 depicts a SuperSpeed hierarchy and calls out the relevant parameters used in the calculations that follow.

![img-293.jpeg](img-293.jpeg)

Figure C-3. Host to Device Path Exit Latency Calculation Examples

C-15

Universal Serial Bus 3.1 Specification, Revision 1.0

### C.2.1 Device Connected Directly to Host

#### C.2.1.1 Host Initiated Transition

In this example, a peripheral device (Dev1) and a host controller root port (RP1) are link partners communicating over a link (Link1).

![img-294.jpeg](img-294.jpeg)

Figure C-4. Device Connected Directly to a Host

C-16

Power Management

# U1 → U0 Transition Latency

The host initiates the transition by transmitting LFPS. At this point, both link partners' transitions from U1 → to U0 are executed in parallel.

The exit latency is characterized by the largest of the two device exit latencies: Dev1:U1DEL and RP1:U1DEL

# U2 → U0 Transition Latency

In this example it is assumed that at least one of the link partners (e.g., the RP1) is enabled for U2. The host initiates the transition by transmitting LFPS. At this point both link partners execute transition from U2 → to U0 in parallel.

The exit latency is characterized by the largest of the two device exit latencies: Dev1:U2DEL and RP1:U2DEL

# C.2.1.2 Device Initiated Transition

These transition latencies are the same as for the host initiated cases.

- U1 End to End Exit Latency is the larger of Dev1:U1DEL and RP1:U1DEL
- U2 End to End Exit Latency is the larger of Dev1:U2DEL and RP1:U2DEL

C-17

Universal Serial Bus 3.1 Specification, Revision 1.0

### C.2.2 Device Connected Through a Hub

In this example a peripheral device (Dev2) is connected to one of a hub's downstream ports (DP2) via a link (Link3), which in turn is connected to a host controller's root port (RP2) via a link (Link2).

![img-295.jpeg](img-295.jpeg)

Figure C-5. Device Connected Through a Hub

#### C.2.2.1 Host Initiated Transition

##### U1 → U0 Transition Latency

This example highlights the end to end latency incurred when transitioning both Link2 and Link3 from U1 → U0. For the purposes of this example, it is assumed that all link partners are enabled for U1, and that both Link2 and Link3 are currently in the U1 state.

C-18

Power Management

Figure C-6 shows the chronological sequence of events. Following the figure is a more detailed description of each stage of the multi-hop link state transition.

![img-296.jpeg](img-296.jpeg)

Figure C-6. Downstream Host to Device Path Exit Latency with Hub

1. The host is prepared to send a packet to Dev2, however it first needs to bring Link2 out of U1 before it is able to send the packet. The host begins the process by transmitting LFPS on RP2 to Hub1's upstream port (UP) which then starts both link partners transitioning in parallel towards U0. This latency is characterized by the larger of RP2:U1DEL and Hub1:U1DEL
2. Once the Link2 partners are in U0, the host schedules the packet targeting Dev2. After a Host Scheduling Delay (HSD) the packet is then sent over Link2 where it then is routed to Link3. This routing incurs the latency associated with the Hub having to parse the packet header to determine the target downstream port for the packet. This latency is characterized by the hub parameter HHDL.
3. The final hop requires Hub1:DP2 to signal LFPS over Link3 at which point the final component of the end to end latency is executed by the Link3 partners in parallel. This final ingredient to the end to end latency is characterized by the larger of Hub1:U1DEL and Dev2_UP:U1DEL.

The total latency for end to end link transition to U0 can be summarized as:

Max(RP2:U1DEL, Hub1:U1DEL) + HSD + HUB1:HHDL + Max(Hub1:U1DEL, Dev2_UP:U1DEL)

### U2 → U0 Transition Latency

This example highlights the end to end latency incurred when transitioning both Link2 and Link3 from U2 → U0. For the purposes of this example it is assumed that all link partners are enabled for U2 and that both Link2 and Link3 are currently in the U2 state.

1. The host is prepared to send a packet to Dev2, however it first needs to bring Link2 out of U2 before it is able to send the packet. The host begins the process by transmitting LFPS to Hub1:UP which then starts both link partners transitioning in parallel towards U0. This latency is characterized by the larger of RP2:U2DEL and Hub1:U2DEL.
2. Once the Link2 partners are in U0 the host sends its packet targeting Dev2 over Link2 where it then needs to be routed to Link3. This incurs the latency associated with the Hub having to parse the packet header to determine the target downstream port for the packet. This latency is characterized by the hub parameter HHDL.

C-19

Universal Serial Bus 3.1 Specification, Revision 1.0

3. The final hop requires Hub1:DP2 to signal LFPS over Link3 at which point the final component of the end to end latency is executed by the Link3 partners in parallel. This final ingredient to the end to end latency is characterized by the larger of Hub1:U2DEL and Dev2_UP:U2DEL.

The total exit latency for end to end link transition to U0 can be summarized as:

Max(RP2:U2DEL, Hub1:U2DEL) + HSD + Hub1:HHDL + Max(Hub1:U2DEL, Dev2_UP:U2DEL)

### C.2.2.2 Device Initiated Transition

This section provides some examples for calculating end to end exit latencies for device initiated exit.

### U1 → U0 Transition Latency

This example highlights the end to end latency incurred when transitioning both Link2 and Link3 from U1 → U0. For the purposes of this example it is assumed that all link partners are enabled for U1 and that both Link2 and Link3 are currently in the U1 state.

Figure C-7 depicts the end to end link state transition in chronological order. Following the figure a more detailed description of the sequence is provided.

![img-297.jpeg](img-297.jpeg)

Figure C-7. Upstream Device to Host Path Exit Latency with Hub

1. Dev2 is prepared to send a packet upstream to the host. However, it first needs to bring Link3 out of U1 and back to U0 before it is able to send the packet. Dev2 begins the process by transmitting LFPS to Hub1:DP2 which then starts both link partners transitioning in parallel towards U0. The Link3 exit latency (Link3_EL) is characterized by the larger of Dev2_UP:U1DEL and Hub1_DP2:U1DEL.
2. After a latency of tHubPort2PortU1EL, the time it takes the hub to determine that one of its downstream ports is awakening, the hub then begins signaling LFPS on Link2 to initiate transition of the Link2 partners (hub's upstream port and host controller root port RP2) to U0.

C-20

Power Management

3. The last component of the end to end exit latency is characterized by the larger of Hub1_UP:U1DEL and RP2:U1DEL which represents the Link2 exit latency (Link2_EL).

End to end exit latency = Max(Link3_EL, (Link2_EL + tHubPort2PortU1ExitLat))
U2 → U0 Transition Latency

This example highlights the end to end latency incurred when transitioning both Link2 and Link3 from U2 → U0. For the purposes of this example it is assumed that all link partners are enabled for U2 and that both Link2 and Link3 are currently in the U2 state.

1. Dev2 is prepared to send a packet upstream to the host. However, it first needs to bring Link3 out of U2 and back to U0 before it is able to send the packet. Dev2 begins the process by transmitting LFPS to Hub1:DP2 which then starts both link partners transitioning in parallel towards U0. The Link3 exit latency (Link3_EL) is characterized by the larger of Dev2_UP:U2DEL and Hu1b_DP2:U2DEL.
2. After a latency of tHubPort2PortU2EL, the time it takes the hub to determine that one of its downstream ports is awakening, the hub then begins signaling LFPS on Link2 to initiate transition of the Link2 partners (hub's upstream port and host controller root port RP2) to U0.
3. The last component of the end to end exit latency is characterized by the larger of Hub1_UP:U2DEL and RP2:U2DEL which represents the Link2 exit latency (Link2_EL).

End to end exit latency = Max(Link3_EL, Link2_EL + tHubPort2PortU2EL)

### C.3 Device-Initiated Link Power Management Policies

Power savings resulting from the effective use of link power management can have a significant impact on system power consumption. For example, without using link power management, the average battery life of a typical notebook computer could be decreased by as much as 15%.

Both devices and downstream ports can initiate U1 and U2 entry.

- Downstream ports have inactivity timers used to initiate U1 and U2 entry. Downstream port inactivity timeouts are programmed by system software.
- Devices may have additional information available that they can use to decide to initiate U1 or U2 entry more aggressively than inactivity timers.

This section describes policies for devices to initiate U1 or U2.

### C.3.1 Overview and Background Information

Devices can save significant power by initiating U1 or U2 more aggressively rather than waiting for downstream port inactivity timeouts. For example, an isochronous device may substantially increase U1 residency by initiating U1 upon completion of isochronous transfers within each service interval.

Devices can use the following information to help determine when to initiate U1 or U2 due to endpoint idle conditions:

- The type of device endpoints and related flags (refer to Chapter 8)

- Packets Pending flag, used with bulk endpoints
- End of Burst flag, used with interrupt endpoints
- Last Packet flag, used with isochronous endpoints

C-21

Universal Serial Bus 3.1 Specification, Revision 1.0

- Protocol level endpoint flow control conditions, e.g., an endpoint having sent an NRDY
- Device class and device implementation
- U1 and U2 device-to-host exit latencies

U1 and U2 device-to-host exit latencies are the total latency to transition all links in the path between the device and the host to U0, when exit is initiated by the device. The device may assume a device-to-host exit latency based on the worst case exit latency (device connected five hubs deep). The device may alternatively use the device-to-host exit latency provided with the U1PEL and U2PEL fields of the SET_SEL request (refer to Chapter 9).

### C.3.2 Entry Conditions for U1 and U2

A device should initiate U1 or U2 when idle conditions are met for all its endpoints. A device typically initiates U1. However, if a device is able to determine that its link will not be needed for a long time, then the device may be able to initiate U2. For example, WiFi has a protocol where its radio may be shut off for long periods, e.g., 100 ms, and since the link is not needed during this time it may be placed in U2.

A device should initiate U2 if it is able to determine its link is not needed for a period of time that exceeds the U2 device-to-host exit latency (plus an appropriate guard band). The device should initiate U1 in all other cases.

Devices should consider the device-to-host exit latency when determining whether to initiate U1 and U2 entry. The host-to-device exit latency and the device-to-host exit latency are both considered by host software when determining whether to enable U1 or U2 on each link. Devices are enabled to initiate U1 and U2 with the U1_Enable and U2_Enable feature selectors (refer to Chapter 9).

The following subsections offer recommendations for determining when an endpoint is idle, or does not need to use the link for a known period, based on endpoint type. Idle conditions may be determined in other implementation specific ways.

### C.3.2.1 Control Endpoints

A control endpoint is idle when all of the following conditions are met:

- Device is in the configured state
- Device is not in the midst of a control transfer
- Either an NRDY was sent, or the Packets Pending flag was set to zero in the last ACK packet received from the host
- Device does not have a pending ERDY

### C.3.2.2 Bulk Endpoints

A bulk endpoint is idle when both of the following conditions are met:

- Either an NRDY was sent, or the Packets Pending flag was set to zero in the last ACK packet received from the host
- Device does not have a pending ERDY

Some devices can also determine that their link is not needed for a known period of time. For example, a mass storage device may need to spin up a spindle to service a request. Since the spin up time can be hundreds of milliseconds, the device should place its link in U2.

C-22

Power Management

After a device has sent an ERDY associated with a bulk endpoint, the link should be kept in U0 until the host sends a request in response to the ERDY (or until the tERDYTimeout occurs, refer to Section 8.13).

### C.3.2.3 Interrupt Endpoints

An interrupt endpoint is idle when both of the following conditions are met:

- Either an NRDY was sent, or the Packets Pending flag was set to zero in the last ACK packet received from the host.

After a device has sent an ERDY associated with an interrupt endpoint, the link should be kept in U0 until the host sends a request in response to the ERDY (or until the tERDYTimeout occurs) in order to achieve the subscribed interrupt service latency. However, when all transfers for a given service interval have been completed, the endpoint will not need the link until the next service interval. The device may be able to place its link in U1 or U2 during this time. The End of Burst flag can be used to determine when all transfers for a given service interval are completed. Note that hosts are required to initiate interrupt transfers far enough ahead of a transfer window to meet subscribed service requirements.

### C.3.2.4 Isochronous Endpoints

An isochronous endpoint is idle when all transfers for a given service interval have been completed, as indicated by the Last Packet flag. The endpoint will not need the link until the next service interval. Note that the host is required to send a PING packet far enough ahead of a transfer window to meet subscribed service requirements.

### C.3.2.5 Devices That Need Timestamp Packets

When a device needs timestamp information, it needs to ensure that its link is in U0 when the next bus interval boundary is reached in order to receive a timestamp packet. If the device’s link is not in U0, it should transition to U0 prior to the next bus interval boundary. The device must track when the bus interval boundary will occur. The device initiates a transition to U0 a period of time before the bus interval boundary occurs, where the period of time is the device-to-host link exit latency.

## C.4 Latency Tolerance Message (LTM) Implementation Example

Computer systems typically maintain a high state of readiness to service devices even when the computer system is idle. LTM supports a mechanism for a system to reduce its state of readiness with the cooperation of Enhanced SuperSpeed devices. This may result in substantial system power savings without requiring additional cost to devices.

This section provides a device implementation example for LTM support. This example is based on a model using two device Latency Tolerance states, an active state and an idle state. Each state has a different Best Effort Latency Tolerance (BELT).

C-23

Universal Serial Bus 3.1 Specification, Revision 1.0

In the following subsections, first a description of BELT and its relationship to overall system exit latency is given. This is followed by a description of a device state machine implementation example.

### C.4.1 Device State Machine Implementation Example

This section describes an example of a typical device implementation. It assumes the device implementation supports both U1 and U2 in conjunction with LTM.

In this example, two device Latency Tolerance states (LT-states) are defined:

- LT-idle state: the device is idle and can tolerate a larger latency from the system (this is the default state).
- LT-active state: the device has determined a need to perform data transfers with the host and wants a shorter latency from the system.

A state machine is illustrated in Figure C-8.

![img-298.jpeg](img-298.jpeg)

Figure C-8. LT State Diagram

The device described by this implementation example is designed to accommodate the worst case value for U1SEL during LT-active, and the worst case value for U2SEL during LT-idle.

The following device design goals are to be met:

- Design for a minimum LTM BELT of 1 ms when in LT-idle
- Design for a minimum LTM BELT of 125 μs when in LT-active

#### C.4.1.1 LTM-Idle State BELT

The device determines its LT-idle state BELT value by subtracting U2SEL from the total latency it can tolerate. To achieve a minimum LT-idle state BELT of 1 ms, the total latency the device must be able to tolerate is 1 ms plus the worst case value for U2SEL, or a total of approximately 3.1 ms (refer to Section C.1.5.1). The worst case U2SEL is based on a worst case device-to-host U2 exit latency of 2.053 ms for t1 (2.047 ms device exit latency plus 1 μs for each of five hubs), plus 0.003 ms for t2, plus 0.001 ms for t4, plus some guard band.

For system implementations where U2SEL is less than its worst case value, the device reports a BELT value larger than 1 ms.

#### C.4.1.2 LTM-Active State BELT

The device determines its LT-active state BELT value by subtracting U1SEL from the total latency it can tolerate. To achieve a minimum LT-active state BELT of 125 μs, the total latency the device must be able to tolerate is 125 μs plus the maximum value for U1SEL, or a total of approximately 145 μs. The worst case U1SEL is based on a worst case device-to-host U1 exit latency of 15 μs for t1 (10 μs device exit latency plus 1 μs for each of five hubs), plus 3.1 μs for t2, plus 1.3 μs for t4,

C-24

Power Management

plus some guard band. This assumes the device will not allow its link to enter U2 prior to changing its state to LT-idle. If the device will allow its link to enter U2 when in LT-active, then the total latency the device must be able to tolerate is 125 μs plus the worst case value for U2SEL.

For system implementations where U1SEL is less than its worst case value, the device reports a BELT value larger than 125 μs.

### C.4.1.3 Transitioning Between LT-States

When a device transitions between LT-states, the device sends an LTM Transaction Packet (TP) with an updated BELT. The device should send all BELT updates as soon as possible after a change in LT-state.

### C.4.1.3.1 Transitioning From LT-idle to LT-active

Devices transition from LT-idle to LT-active when the device determines that a bulk or interrupt data transfer needs to occur. Some examples are given below:

- The host initiates a bulk OUT transfer with the Packets Pending flag asserted to a flash drive device. As a result of receiving this OUT request, the device transitions to LT-active and sends an updated BELT to the host.
- The host initiates a bulk IN transfer with the Packets Pending flag asserted to a hard disk drive device with is spindle currently spun down and the requested data not in a cache on the hard disk drive. As a result of receiving this IN request, the device determines that a bulk data transfer has been initiated by the host. However, the device will service the IN request after its spindle spins up, which may take substantially longer than the last reported BELT. The device may delay transitioning to LT-active. When the device determines that the spindle will complete its spin up within the last reported BELT, the device transitions to LT-active and sends an updated BELT to the host.
- A Network Interface Controller device begins receiving data on its network interface that requires a bulk IN data transfer with the host. As a result of receiving data on its network interface, the device transitions to LT-active, begins to transition its link to U0 (if not already in U0), and sends both an ERDY and an updated BELT to the host.
- A multi-touch Human Interface Device is set up with an interrupt endpoint. When human input is detected the device transitions to LT-active, begins transitioning its link to U0 (if not already in U0), and sends both an ERDY and an updated BELT to the host.

In some cases, a transition from LT-idle to LT-active is not appropriate even though the device needs to transmit to the host. For example:

- The host sends a GetStatus request to a device. Since it is a control transfer and not a bulk or an interrupt transfer, the device remains in the LT-idle state.

When the device transitions from LT-idle to LT-active, the device sends an LTM TP with a BELT of at least tBELTmin.

### C.4.1.3.2 Transitioning From LT-active to LT-idle

When a device determines that it is idle, it transitions from LT-active to LT-idle. The method used in this example for device idle detection is based on U2 entry. When the device is in LT-active, the device transitions to LT-idle just prior to when its link will enter U2.

C-25

Universal Serial Bus 3.1 Specification, Revision 1.0

In preparation for a transition from U0 to U2, a device in LT-active should perform the following actions:

1. The device transitions to LT-idle.
2. The device sends an LTM with a BELT value of at least tBELTdefault.
3. The device initiates a transition to U2 from U0.

In preparation for a transition from U1 to U2, a device in LT-active should perform the following actions:

1. The device transitions its link to U0 prior to U2 entry.
2. The device transitions to LT-idle.
3. The device sends an LTM with a BELT value of at least tBELTdefault.
4. The device initiates a transition to U2 from U0.

In the latter case, since the device must transition its link to U0 prior to U2 entry, the device must detect the U2 inactivity timer expiration enough in advance to avoid the possibility that its link partner will have already transitioned from U1 directly to U2. For example, the device may initiate a transition to U0 1 μs before the U2 inactivity timer expires.

### C.4.2 Other Considerations

The following are additional considerations associated with device support of LTM:

- The BELT represents a latency tolerance for an entire peripheral device. The BELT value must be aggregated across all endpoints within the device, including all functions within a composite device. The smallest BELT value across all endpoints should be selected. For LTM purposes, isochronous endpoints are ignored when determining the BELT value.
- If LTM is supported by a device, LTM should be disabled prior to placing the device into suspend (refer to the PORT_LINK_STATE feature selector in Chapter 10). Devices send an updated LTM when LTM is enabled, or immediately before LTM is disabled, as defined in Chapter 8. Disabling LTM in this way ensures that a suspended device does not keep the system in a high state of readiness, wasting power.

### C.5 SuperSpeed vs. High Speed Power Management Considerations

Some devices may operate well with a High Speed (480 Mbps) interface, but can substantially reduce system power consumption if implemented with a SuperSpeed interface. In addition to device power consumption, system power consumption should be considered when selecting the interface for a new device design.

When a device is actively transferring data, system components are also transferring that data. For some systems, the power consumption of system components is much larger than a USB device's contribution to the system's power consumption.

Under typical circumstances, the faster the data transfer completes, the faster system components can return to a low power state. Transferring data faster can save power, on average, over time. Examples of system components include a Host Controller, a DRAM controller, DRAM components, a microprocessor with a cache that needs to snoop DRAM accesses, etc.

C-26

Power Management

Figure C-9 illustrates a sample device that has an average data transfer rate of 20 MBps when actively in use. The figure shows the system power consumption when the device is operating in SuperSpeed mode and also in High Speed mode.

![img-299.jpeg](img-299.jpeg)

Figure C-9. System Power during SuperSpeed and High Speed Device Data Transfers

When no data transfer is taking place the system power consumption is P_IDLE. P_IDLE is approximated to be the same in both SuperSpeed and High Speed modes. Link power management considerations are ignored for simplicity of illustration.

When a data transfer is taking place, the system power is P_SS-ACTIVE and P_HS-ACTIVE for SuperSpeed and High Speed modes respectively. The difference between P_SS-ACTIVE and P_HS-ACTIVE is due to the physical layer interface power of the device and its link partner (no hubs present).

Data transfers complete roughly ten times faster in SuperSpeed mode than in High Speed mode. This causes the average system power in High Speed mode to be much larger than the average system power in SuperSpeed mode. The difference in average system power may be as high as 50% during a data transfer. This can have a major impact on the battery life of mobile systems.

C-27

Universal Serial Bus 3.1 Specification, Revision 1.0

C-28

## D Example Packets

[tbl-273.md](tbl-273.md)

U-164

Figure D-1. Sample ERDY Transaction Packet

[tbl-274.md](tbl-274.md)

U-165

Figure D-2. Sample Data Packet

D-1

Universal Serial Bus 3.1 Specification, Revision 1.0

[tbl-275.md](tbl-275.md)

Figure D-3. Example placement of Gen 2 SKP Block, Idle Symbols, Link Command and Header Packet

D-2

Power Management

[tbl-276.md](tbl-276.md)

Figure D-4. Example placement of Gen 2 Data Packets and Idle Symbols

D-3

Universal Serial Bus 3.1 Specification, Revision 1.0

D-4

# E Repeaters

This appendix is a placeholder for repeater requirements that will be completed after the release of the USB 3.1 specification.