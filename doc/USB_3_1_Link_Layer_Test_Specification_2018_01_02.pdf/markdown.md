# **Universal Serial Bus 3.1**## **Link Layer Test Specification**

**Date:** January 2, 2018

**Revision:** 0.94

Chapter 1: Introduction

Revision 0.94

1/2/2017

Copyright © 2013-2018, USB Implementers Forum, Inc.

All rights reserved.

A LICENSE IS HEREBY GRANTED TO REPRODUCE THIS SPECIFICATION FOR INTERNAL USE ONLY. NO OTHER LICENSE, EXPRESS OR IMPLIED, BY ESTOPPEL OR OTHERWISE, IS GRANTED OR INTENDED HEREBY.

USB-IF AND THE AUTHORS OF THIS SPECIFICATION EXPRESSLY DISCLAIM ALL LIABILITY FOR INFRINGEMENT OF INTELLECTUAL PROPERTY RIGHTS, RELATING TO IMPLEMENTATION OF INFORMATION IN THIS SPECIFICATION. USB-IF AND THE AUTHORS OF THIS SPECIFICATION ALSO DO NOT WARRANT OR REPRESENT THAT SUCH IMPLEMENTATION(S) WILL NOT INFRINGE THE INTELLECTUAL PROPERTY RIGHTS OF OTHERS.

THIS SPECIFICATION IS PROVIDED "AS IS" AND WITH NO WARRANTIES, EXPRESS OR IMPLIED, STATUTORY OR OTHERWISE. ALL WARRANTIES ARE EXPRESSLY DISCLAIMED. NO WARRANTY OF MERCHANTABILITY, NO WARRANTY OF NON-INFRINGEMENT, NO WARRANTY OF FITNESS FOR ANY PARTICULAR PURPOSE, AND NO WARRANTY ARISING OUT OF ANY PROPOSAL, SPECIFICATION, OR SAMPLE.

IN NO EVENT WILL USB-IF OR USB-IF MEMBERS BE LIABLE TO ANOTHER FOR THE COST OF PROCURING SUBSTITUTE GOODS OR SERVICES, LOST PROFITS, LOSS OF USE, LOSS OF DATA OR ANY INCIDENTAL, CONSEQUENTIAL, INDIRECT, OR SPECIAL DAMAGES, WHETHER UNDER CONTRACT, TORT, WARRANTY, OR OTHERWISE, ARISING IN ANY WAY OUT OF THE USE OF THIS SPECIFICATION, WHETHER OR NOT SUCH PARTY HAD ADVANCE NOTICE OF THE POSSIBILITY OF SUCH DAMAGES.

USB 3.1 Link Layer Test Specification

Chapter 1: Introduction

Revision 0.94

1/2/2017

# Revision History

[tbl-0.md](tbl-0.md)

USB 3.1 Link Layer Test Specification

Chapter 1: Introduction

Revision 0.94

1/2/2017

Significant Contributors:

[tbl-1.md](tbl-1.md)

# Contents

1 INTRODUCTION ... 1
2 TERMS AND ABBREVIATIONS ... 2
3 TEST ASSERTIONS ... 3

Chapter 7 Test Assertions: Link Layer ... 3

Subsection reference: 7.2 Link Management and Flow Control ... 3

Subsection reference: 7.2.1 Packets and Packet Framing ... 3

Subsection reference: 7.2.1.1 Header Packet Structure ... 3

Subsection reference: 7.2.1.1.1 Header Packet Framing ... 3

Subsection reference: 7.2.1.1.2 Packet Header ... 3

Subsection reference: 7.2.1.1.3 Link Control Word ... 3

Subsection reference: 7.2.1.2 Data Packet Payload Structure ... 3

Subsection reference: 7.2.1.2.1 Data Packet Payload Framing ... 3

Subsection reference: 7.2.1.2.2 Data Packet Payload ... 4

Subsection reference: 7.2.1.2.3 Data Payload Structure and Spacing between DPH and DPP ... 4

Subsection reference: 7.2.1.3 SuperSpeedPlus Packet Placement ... 4

Subsection reference: 7.2.2 Link Commands ... 4

Subsection reference: 7.2.2.1 Link Command Structure ... 4

Subsection reference: 7.2.2.2 Link Command Word Definition ... 5

Subsection reference: 7.2.2.3 Link Command Placement ... 5

Subsection reference: 7.2.3 Logical Idle ... 5

Subsection reference: 7.2.4 Link Command Usage for Flow Control, Error Recovery, and Power Management ... 5

Subsection reference: 7.2.4.1 Header Packet Flow Control and Error Recovery ... 5

Subsection reference: 7.2.4.1.1 Initialization ... 5

Subsection reference: 7.2.4.1.2 General Rules of LGOOD_n and LCRD_x Usage ... 9

Subsection reference: 7.2.4.1.3 Transmitting Header Packets ... 9

Subsection reference: 7.2.4.1.4 Deferred DPH ... 10

USB 3.1 Link Layer Test Specification

Chapter 1: Introduction

Revision 0.94

1/2/2017

Subsection reference: 7.2.4.1.5 Receiving Header Packets ... 10
Subsection reference: 7.2.4.1.6 Receiving Data Packet Header in SuperSpeedPlus Operation ... 11
Subsection reference: 7.2.4.1.7 SuperSpeed Rx Header Buffer Credit ... 11
Subsection reference: 7.2.4.1.8 SuperSpeedPlus Type 1/Type 2 Rx Buffer Credit ... 12
Subsection reference: 7.2.4.1.9 Receiving Data Packet Payload ... 12
Subsection reference: 7.2.4.1.10 Receiving LGOOD_n ... 13
Subsection reference: 7.2.4.1.11 Receiving LCRD_x/LCRD1_x/LCRD2_x ... 13
Subsection reference: 7.2.4.1.12 Receiving LBAD ... 13
Subsection reference: 7.2.4.1.13 Transmitting Timers ... 13
Subsection reference: 7.2.4.2.1 Power Management Link Timers ... 14
Subsection reference: 7.2.4.2.2 Low Power Link State Initiation ... 15
Subsection reference: 7.2.4.2.3 U1/U2 Entry Flow ... 16
Subsection reference: 7.2.4.2.4 U3 Entry Flow ... 16
Subsection reference: 7.2.4.2.5 Concurrent Low Power Link Management Flow ... 17
Subsection reference: 7.2.4.2.6 Concurrent Low Power Link Management and Recovery Flow ... 17
Subsection reference: 7.2.4.2.7 Low Power Link State Exit Flow ... 17
Subsection reference: 7.3 Link Error Rules/Recovery ... 18
Subsection reference: 7.3.3 Link Error Statistics ... 18
Subsection reference: 7.3.3.1 Link Error Count ... 18
Subsection reference: 7.3.4.1 Packet Framing Errors ... 18
Subsection reference: 7.3.5 Link Commands Errors ... 19
Subsection reference: 7.3.6 ACK Tx Header Sequence Number Errors ... 19
Subsection reference: 7.3.7 Header Sequence Number Advertisement Error ... 20
Subsection reference: 7.3.8 SuperSpeed Rx Header Buffer Credit Advertisement Error ... 20
Subsection reference: 7.3.9 SuperSpeedPlus Type 1/Type 2 Rx Buffer Credit Advertisement Error ... 20
Subsection reference: 7.3.10 Training Sequence Error ... 20
Subsection reference: 7.4 PowerOn Reset and Inband Reset ... 21
Subsection reference: 7.4.1 Power On Reset ... 21
Subsection reference: 7.4.2 Inband Reset ... 21
Subsection reference: 7.5 Link Training and Status State Machine (LTSSM) ... 22
Subsection reference: 7.5.1 eSS.Disabled ... 22
Subsection reference: 7.5.1.1 eSS.Disabled for Downstream Ports and Hub Upstream Ports ... 23
Subsection reference: 7.5.1.1.1 eSS.Disabled Requirements ... 23
Subsection reference: 7.5.1.1.2 Exit from eSS.Disabled ... 23
Subsection reference: 7.5.1.2 eSS.Disabled for Upstream Ports of Peripheral Devices ... 23
Subsection reference: 7.5.1.2.2 eSS.Disabled Requirements ... 23
Subsection reference: 7.5.1.2.3 Exit from eSS.Disabled.Default ... 23
Subsection reference: 7.5.1.2.4 Exit from eSS.Disabled.Error ... 23
Subsection reference: 7.5.2 eSS.Inactive ... 24
Subsection reference: 7.5.2.3 eSS.Inactive.Quiet ... 24
Subsection reference: 7.5.2.3.1 eSS.Inactive.Quiet Requirement ... 24
Subsection reference: 7.5.2.3.2 Exit from eSS.Inactive.Quiet ... 24
Subsection reference: 7.5.2.4 eSS.Inactive.Disconnect.Detect ... 24
Subsection reference: 7.5.2.4.1 eSS.Inactive.Disconnect.Detect Requirements ... 24
Subsection reference: 7.5.2.4.2 Exit from eSS.Inactive.Disconnect.Detect ... 24
Subsection reference: 7.5.3 Rx.Detect ... 24
Subsection reference: 7.5.3.3 Rx.Detect.Reset ... 24
Subsection reference: 7.5.3.3.1 Rx.Detect.Reset Requirements ... 24
Subsection reference: 7.5.3.3.2 Exit from Rx.Detect.Reset ... 24
Subsection reference: 7.5.3.4 Rx.Detect.Active ... 25
Subsection reference: 7.5.3.5 Rx.Detect.Active Requirement ... 25
Subsection reference: 7.5.3.6 Exit from Rx.Detect.Active ... 25
Subsection reference: 7.5.3.7 Rx.Detect.Quiet ... 25
Subsection reference: 7.5.3.7.1 Rx.Detect.Quiet Requirements ... 25
Subsection reference: 7.5.3.7.2 Exit from Rx.Detect.Quiet ... 25
Subsection reference: 7.5.4 Polling ... 26

USB 3.1 Link Layer Test Specification

Chapter 1: Introduction

Revision 0.94

1/2/2017

Subsection reference: 7.5.4.2 Polling Requirements ...26
Subsection reference: 7.5.4.3 Polling.LFPS ...26
Subsection reference: 7.5.4.3.1 Polling.LFPS Requirements ...26
Subsection reference: 7.5.4.3.2 Exit from Polling.LFPS ...27
Subsection reference: 7.5.4.4 Polling.LFPSPlus ...28
Subsection reference: 7.5.4.4.1 Polling.LFPSPlus Requirements ...28
Subsection reference: 7.5.4.4.2 Exit from Polling.LFPSPlus ...28
Subsection reference: 7.5.4.5 Polling.PortMatch ...29
Subsection reference: 7.5.4.5.2 Polling.PortMatch Requirements ...29
Subsection reference: 7.5.4.5.3 Exit from Polling.PortMatch ...29
Subsection reference: 7.5.4.6 Polling.PortConfig ...30
Subsection reference: 7.5.4.6.1 Polling.PortConfig Requirements ...30
Subsection reference: 7.5.4.6.2 Exit from Polling.PortConfig ...30
Subsection reference: 7.5.4.7 Polling.RxEQ ...31
Subsection reference: 7.5.4.7.1 Polling.RxEQ Requirements ...31
Subsection reference: 7.5.4.7.2 Exit from Polling.RxEQ ...31
Subsection reference: 7.5.4.8 Polling.Active ...31
Subsection reference: 7.5.4.8.1 Polling.Active Requirements ...31
Subsection reference: 7.5.4.8.2 Exit from Polling.Active ...31
Subsection reference: 7.5.4.9 Polling.Configuration ...32
Subsection reference: 7.5.4.9.1 Polling.Configuration Requirements ...32
Subsection reference: 7.5.4.9.2 Exit from Polling.Configuration ...33
Subsection reference: 7.5.4.10 Polling.Idle ...34
Subsection reference: 7.5.4.10.1 Polling.Idle Requirements ...34
Subsection reference: 7.5.4.10.2 Exit form Polling.Idle ...34
Subsection reference: 7.5.5 Compliance Mode ...35
Subsection reference: 7.5.5.1 Compliance Mode Requirements ...36
Subsection reference: 7.5.5.2 Exit from Compliance Mode ...36
Subsection reference: 7.5.6 U0 ...36
Subsection reference: 7.5.6.1 U0 Requirements ...36
Subsection reference: 7.5.6.2 Exit from U0 ...36
Subsection reference: 7.5.7 U1 ...37
Subsection reference : 7.5.7.1 U1 Requirements ...37
Subsection reference: 7.5.7.2 Exit from U1 ...37
Subsection reference: 7.5.8 U2 ...38
Subsection reference: 7.5.8.1 U2 Requirements ...38
Subsection reference: 7.5.8.2 Exit from U2 ...38
Subsection reference: 7.5.9 U3 ...38
Subsection reference: 7.5.9.1 U3 Requirements ...39
Subsection reference: 7.5.9.2 Exit from U3 ...39
Subsection reference: 7.5.10 Recovery ...39
Subsection reference: 7.5.10.3 Recovery.Active ...39
Subsection reference: 7.5.10.3.1 Recovery.Active Requirements ...39
Subsection reference: 7.5.10.3.2 Exit from Recovery.Active ...40
Subsection reference: 7.5.10.4 Recovery.Configuration ...40
Subsection reference: 7.5.10.4.1 Recovery.Configuration Requirements ...40
Subsection reference: 7.5.10.4.2 Exit from Recovery.Configuration ...40
Subsection reference: 7.5.10.5 Recovery.Idle ...41
Subsection reference: 7.5.10.5.1 Recovery.Idle Requirements ...41
Subsection reference: 7.5.10.5.2 Exit from Recovery.Idle ...42
Subsection reference: 7.5.11 Loopback ...42
Subsection reference: 7.5.11.3.1 Loopback.Active Requirements ...42
Subsection reference: 7.5.11.3.2 Exit from Loopback.Active ...42
Subsection reference: 7.5.11.4 Loopback.Exit ...43
Subsection reference: 7.5.11.4.1 Loopback.Exit Requirements ...43
Subsection reference: 7.5.11.4.2 Exit from Loopback.Exit ...43

USB 3.1 Link Layer Test Specification

Chapter 1: Introduction

Revision 0.94

1/2/2017

Subsection reference: 7.5.12 Hot Reset...43
Subsection reference: 7.5.12.2 Hot Reset Requirements...43
Subsection reference: 7.5.12.3 Hot Reset.Active...43
Subsection reference: 7.5.12.3.1 Hot Reset.Active Requirements...43
Subsection reference: 7.5.12.3.2 Exit from Hot Reset.Active...44
Subsection reference: 7.5.12.4 Hot Reset.Exit...44
Subsection reference: 7.5.12.4.1 Hot Reset.Exit Requirements...44
Subsection reference: 7.5.12.4.2 Exit from Hot Reset.Exit...44

# Chapter 8 Test Assertions: Protocol Layer...45

Subsection reference: 8.3 Packet Formats...45
Subsection reference: 8.3.1 Fields Common to all Headers...45
Subsection reference: 8.3.1.1 Reserved Values and Reserved Field Handling...45
Subsection reference: 8.4 Link Management Packet (LMP)...45
Subsection reference: 8.4.2 Set Link Function...45
Subsection reference: 8.4.4 Vendor Device Test...45
Subsection reference: 8.4.5 Port Capabilities...45
Subsection reference: 8.4.6 Port Configuration...45
Subsection reference: 8.4.7 Port Configuration Response...46
Subsection reference: 8.4.8 Precision Time Measurement...46
Subsection reference: 8.4.8.1 PTM Bus Interval Boundary Counters...46
Subsection reference: 8.4.8.2 LDM Protocol...46
Subsection reference: 8.4.8.3 LDM State Machines...47
Subsection reference: 8.4.8.3.1 Requester Operation...47
Subsection reference: 8.4.8.3.1.1 Init Request...47
Subsection reference: 8.4.8.3.1.2 Init Response...47
Subsection reference: 8.4.8.3.1.3 Timestamp Request...48
Subsection reference: 8.4.8.3.1.4 Timestamp Response...48
Subsection reference: 8.4.8.3.1.5 LDM Disabled...48
Subsection reference: 8.4.8.3.2 Responder Operation...48
Subsection reference: 8.4.8.3.2.1 Responder Disabled...49
Subsection reference: 8.4.8.3.2.2 Timestamp Request...49
Subsection reference: 8.4.8.3.2.3 Timestamp Response...49
Subsection reference: 8.4.8.5 PTM Bus Interval Boundary Device Calculation...49
Subsection reference: 8.4.8.6 PTM Bus Interval Boundary Host Calculation...50
Subsection reference: 8.4.8.7 PTM Hub ITP Regeneration...50
Subsection reference: 8.4.8.9 LDM Rules...50
Subsection reference: 8.4.8.10 LDM and Hubs...51
Subsection reference: 8.6 Data Packet (DP)...51

# Chapter 10 Test Assertions: Hub, Host Downstream Port, and Device Upstream Port Specification ...51

Subsection reference: 10.2 Hub Power Management...51
Subsection reference: 10.2.2 Hub Downstream Port U1/U2 Timers...51
Subsection reference: 10.3: Hub Downstream Facing Ports...51
Subsection reference: 10.3.1: Hub Downstream Facing Port State Descriptions...51
Subsection reference: 10.3.1.6: DSPORT.Resetting...51
Subsection reference: 10.4 Hub Downstream Facing Port Power Management...52
Subsection reference: 10.4.2 Hub Downstream Facing Port State Descriptions...52
Subsection reference: 10.4.2.1 Enabled U0 States...52

# XHCI Specification Chapter 5 Test Assertions: Register Interface...52

Subsection reference: xHCI 5.4 Host Controller Operational Registers...52
Subsection reference: xHCI 5.4.8 Port Status and Control Register (PORTSC)...52

USB 3.1 Link Layer Test Specification

Chapter 1: Introduction

Revision 0.94

1/2/2017

# **4 TIMING DEFINITIONS... 53**

# **5 TEST DESCRIPTIONS... 55**

# **5.1 Link Initialization Sequence ... 55**

# **5.2 Physical Layer... 56**

# **5.3 Link Layer... 60**

TD.7.1 Link Bring-up Test ... 60
TD.7.2 Link Commands Framings Robustness Test... 64
TD.7.3 Link Commands CRC-5 Robustness Test ... 65
TD.7.4 Invalid Link Commands Test ... 65
TD.7.5 Header Packet Framing Robustness Test... 66
TD.7.6 Data Payload Packet Framing Robustness Test... 66
TD.7.7 RX Header Packet Retransmission Test ... 67
TD.7.8 TX Header Packet Retransmission Test ... 69
TD.7.9 PENDING_HP_TIMER Deadline Test ... 70
TD.7.10 CREDIT_HP_TIMER Deadline Test ... 70
TD.7.11 PENDING_HP_TIMER Timeout Test ... 71
TD.7.12 CREDIT_HP_TIMER Timeout Test ... 71
TD.7.13 Wrong Header Sequence Test... 72
TD.7.14 Wrong LGOOD_N Sequence Test ... 72
TD.7.15 Wrong LCRD_X Sequence Test... 73
TD.7.16 Link Command Missing Test (Upstream Port Only)... 74
TD.7.17 tPortConfiguration Time Timeout Test ... 74
TD.7.18 Low Power initiation for U1 test (Downstream Port Only)... 76
TD.7.19 Low Power initiation for U2 test (Downstream Port Only)... 76
TD.7.20 PM_LC_TIMER Deadline Test (Downstream Port Only) ... 77
TD.7.21 PM_LC_TIMER Timeout Test (Downstream Port Only) ... 78
TD.7.22 PM_ENTRY_TIMER Timeout Test (Upstream Port Only) ... 78
TD.7.23 Accepted Power Management Transaction for U1 Test (Upstream Port Only)... 78
TD.7.24 Accepted Power Management Transaction for U2 Test (Upstream Port Only)... 79
TD.7.25 Accepted Power Management Transaction for U3 Test (Upstream Port Only)... 80
TD.7.26 Transition to U0 from Recovery Test ... 81
TD.7.27 Hot Reset Detection in Polling Test (Upstream Port Only) ... 82
TD.7.28 Hot Reset Detection in U0 Test (Upstream Port Only)... 83
TD.7.29 Hot Reset Initiation in U0 Test (Downstream Port Only)... 83
TD.7.30 Recovery on three consecutive failed RX Header Packets Test ... 84
TD.7.31 Hot Reset Failure Test (Downstream Port Only)... 85
TD.7.32 Warm Reset Rx.Detect Timeout Test (Hub Downstream Port Only)... 86
TD.7.33 Exit Compliance Mode Test (Upstream Port Only)... 86
TD.7.34 Exit Compliance Mode Test (Downstream Port Only)... 87
TD.7.35 Exit U3 by Reset Test (Downstream Port Only)... 88
TD.7.36 Exit U3 Test (Host Downstream Port Only)... 88
TD.7.37 Packet Pending Test (Upstream Port Only) ... 89
TD.7.38 Port Capability Tiebreaker Test ... 90
TD.7.39 PortMatch Retry Test (Gen 2 Only)... 91
TD.7.40 Polling Retry Test (Downstream Port Only) ... 92
TD.7.41 SetAddress TPF Bit Test (Gen 2 Upstream Port Only) ... 93
TD.7.42 Symbol to Block Alignment Test (Gen 2 Only) ... 93

USB 3.1 Link Layer Test Specification

Chapter 1: Introduction

1/17/2018

# 1 Introduction

This document provides the compliance criteria and test descriptions for Enhanced SuperSpeed USB 3.1 Link Layer implementations. It is relevant for anyone building an Enhanced SuperSpeed host, hub or device. The document is divided into two major sections. The first section lists the compliance criteria and the second section lists the test descriptions used to verify a port's conformance to these criteria.

Compliance criteria are provided as a list of assertions that describe specific characteristics or behaviors that must be met. Each assertion provides a reference to the USB 3.1 specification or other documents from which the assertion was derived. In addition, each assertion provides a reference to the specific test description(s) where the assertion is tested.

Each test assertion is formatted as follows:

[tbl-2.md](tbl-2.md)

Assertion#: Unique identifier for each spec requirement. The identifier is in the form USB31_SPEC_SECTION_NUMBER#X, where X is a unique integer for a requirement in that section.

Assertion Description: Specific requirement from the specification

Test #: A label for a specific test description in this specification that tests this requirement. Test # can have one of the following values:

NT This item is not explicitly tested in a test description. Items can be labeled NT for several reasons – including items that are not testable, not important to test for interoperability, or are indirectly tested by other operations performed by the compliance test.

X.X This item is covered by the test described in test description X.X in this specification.

IOP This assertion is verified by the USB 3.0 Interoperability Test Suite.

BC This assertion is applied as a background check in all test descriptions.

Test descriptions provide a high level overview of the tests that are performed to check the compliance criteria. The descriptions are provided with enough detail so that a reader can understand what the test does. The descriptions do not describe the actual step-by-step procedure to perform the test.

Host tests are performed with a Windows 8 machine with all the latest Microsoft updates. The Compliance driver is loaded for most of the Host tests. The Compliance Driver is provided with USB30CV from the usb.org website. One of the Host tests requires the vendor driver for the host controller to be loaded.

Some of the downstream port tests require USB30CV test supplements to perform the test. If a test requires USB30CV, it will be noted in the description later in this document. To run the LVS (Link Validation System) and USB30CV together, always start the USB30CV test prior to the LVS test.

For questions about this document, please contact ssusbcompliance@usb.org. For questions regarding the test matrix or equipment please contact techadmin@usb.org.

1

USB 3.1 Link Layer Test Specification

Chapter 2: Terms and Abbreviations

1/17/2018

## 2 Terms and Abbreviations

This chapter lists and defines terms and abbreviations used throughout this specification. Terms and Abbreviations specified in the USB 3.0 specifications are not duplicated here.

[tbl-3.md](tbl-3.md)

2

USB 3.1 Link Layer Test Specification

Chapter 3: Test Assertions

1/17/2018

### 3 Test Assertions

Unless otherwise noted, subsection references point to the USB 3.1 specification.

[tbl-4.md](tbl-4.md)

3

USB 3.1 Link Layer Test Specification

Chapter 3: Test Assertions

1/17/2018

[tbl-5.md](tbl-5.md)

4

USB 3.1 Link Layer Test Specification

Chapter 3: Test Assertions

1/17/2018

[tbl-6.md](tbl-6.md)

5

USB 3.1 Link Layer Test Specification

Chapter 3: Test Assertions

1/17/2018

[tbl-7.md](tbl-7.md)

6

USB 3.1 Link Layer Test Specification

Chapter 3: Test Assertions

1/17/2018

[tbl-8.md](tbl-8.md)

7

USB 3.1 Link Layer Test Specification

Chapter 3: Test Assertions

1/17/2018

[tbl-9.md](tbl-9.md)

8

USB 3.1 Link Layer Test Specification

Chapter 3: Test Assertions

1/17/2018

[tbl-10.md](tbl-10.md)

9

USB 3.1 Link Layer Test Specification

Chapter 3: Test Assertions

1/17/2018

[tbl-11.md](tbl-11.md)

10

USB 3.1 Link Layer Test Specification

Chapter 3: Test Assertions

1/17/2018

[tbl-12.md](tbl-12.md)

11

USB 3.1 Link Layer Test Specification

Chapter 3: Test Assertions

1/17/2018

[tbl-13.md](tbl-13.md)

12

USB 3.1 Link Layer Test Specification

Chapter 3: Test Assertions

1/17/2018

[tbl-14.md](tbl-14.md)

13

USB 3.1 Link Layer Test Specification

Chapter 3: Test Assertions

1/17/2018

[tbl-15.md](tbl-15.md)

14

USB 3.1 Link Layer Test Specification

Chapter 3: Test Assertions

1/17/2018

[tbl-16.md](tbl-16.md)

15

USB 3.1 Link Layer Test Specification

Chapter 3: Test Assertions

1/17/2018

[tbl-17.md](tbl-17.md)

16

USB 3.1 Link Layer Test Specification

Chapter 3: Test Assertions

1/17/2018

[tbl-18.md](tbl-18.md)

17

USB 3.1 Link Layer Test Specification

Chapter 3: Test Assertions

1/17/2018

[tbl-19.md](tbl-19.md)

18

USB 3.1 Link Layer Test Specification

Chapter 3: Test Assertions

1/17/2018

[tbl-20.md](tbl-20.md)

19

USB 3.1 Link Layer Test Specification

Chapter 3: Test Assertions

1/17/2018

[tbl-21.md](tbl-21.md)

20

USB 3.1 Link Layer Test Specification

Chapter 3: Test Assertions

1/17/2018

[tbl-22.md](tbl-22.md)

21

USB 3.1 Link Layer Test Specification

Chapter 3: Test Assertions

1/17/2018

[tbl-23.md](tbl-23.md)

22

USB 3.1 Link Layer Test Specification

Chapter 3: Test Assertions

1/17/2018

[tbl-24.md](tbl-24.md)

23

USB 3.1 Link Layer Test Specification

Chapter 3: Test Assertions

1/17/2018

[tbl-25.md](tbl-25.md)

24

USB 3.1 Link Layer Test Specification

Chapter 3: Test Assertions

1/17/2018

[tbl-26.md](tbl-26.md)

25

USB 3.1 Link Layer Test Specification

Chapter 3: Test Assertions

1/17/2018

[tbl-27.md](tbl-27.md)

26

USB 3.1 Link Layer Test Specification

Chapter 3: Test Assertions

1/17/2018

[tbl-28.md](tbl-28.md)

27

USB 3.1 Link Layer Test Specification

Chapter 3: Test Assertions

1/17/2018

[tbl-29.md](tbl-29.md)

28

USB 3.1 Link Layer Test Specification

Chapter 3: Test Assertions

1/17/2018

[tbl-30.md](tbl-30.md)

29

USB 3.1 Link Layer Test Specification

Chapter 3: Test Assertions

1/17/2018

[tbl-31.md](tbl-31.md)

30

USB 3.1 Link Layer Test Specification

Chapter 3: Test Assertions

1/17/2018

[tbl-32.md](tbl-32.md)

31

USB 3.1 Link Layer Test Specification

Chapter 3: Test Assertions

1/17/2018

[tbl-33.md](tbl-33.md)

32

USB 3.1 Link Layer Test Specification

Chapter 3: Test Assertions

1/17/2018

[tbl-34.md](tbl-34.md)

33

USB 3.1 Link Layer Test Specification

Chapter 3: Test Assertions

1/17/2018

[tbl-35.md](tbl-35.md)

34

USB 3.1 Link Layer Test Specification

Chapter 3: Test Assertions

1/17/2018

[tbl-36.md](tbl-36.md)

35

USB 3.1 Link Layer Test Specification

Chapter 3: Test Assertions

1/17/2018

[tbl-37.md](tbl-37.md)

36

USB 3.1 Link Layer Test Specification

Chapter 3: Test Assertions

1/17/2018

[tbl-38.md](tbl-38.md)

37

USB 3.1 Link Layer Test Specification

Chapter 3: Test Assertions

1/17/2018

[tbl-39.md](tbl-39.md)

38

USB 3.1 Link Layer Test Specification

Chapter 3: Test Assertions

1/17/2018

[tbl-40.md](tbl-40.md)

39

USB 3.1 Link Layer Test Specification

Chapter 3: Test Assertions

1/17/2018

[tbl-41.md](tbl-41.md)

40

USB 3.1 Link Layer Test Specification

Chapter 3: Test Assertions

1/17/2018

[tbl-42.md](tbl-42.md)

41

USB 3.1 Link Layer Test Specification

Chapter 3: Test Assertions

1/17/2018

[tbl-43.md](tbl-43.md)

42

USB 3.1 Link Layer Test Specification

Chapter 3: Test Assertions

1/17/2018

[tbl-44.md](tbl-44.md)

43

USB 3.1 Link Layer Test Specification

Chapter 3: Test Assertions

1/17/2018

[tbl-45.md](tbl-45.md)

44

USB 3.1 Link Layer Test Specification

Chapter 3: Test Assertions

1/17/2018

[tbl-46.md](tbl-46.md)

45

USB 3.1 Link Layer Test Specification

Chapter 3: Test Assertions

1/17/2018

[tbl-47.md](tbl-47.md)

46

USB 3.1 Link Layer Test Specification

Chapter 3: Test Assertions

1/17/2018

[tbl-48.md](tbl-48.md)

47

USB 3.1 Link Layer Test Specification

Chapter 3: Test Assertions

1/17/2018

[tbl-49.md](tbl-49.md)

48

USB 3.1 Link Layer Test Specification

Chapter 3: Test Assertions

1/17/2018

[tbl-50.md](tbl-50.md)

49

USB 3.1 Link Layer Test Specification

Chapter 3: Test Assertions

1/17/2018

[tbl-51.md](tbl-51.md)

50

USB 3.1 Link Layer Test Specification

Chapter 3: Test Assertions

1/17/2018

[tbl-52.md](tbl-52.md)

51

USB 3.1 Link Layer Test Specification

Chapter 3: Test Assertions

1/17/2018

[tbl-53.md](tbl-53.md)

52

USB 3.1 Link Layer Test Specification

Chapter 4: Timing Definitions

1/17/2018

## 4 Timing Definitions

The USB 3.1 Specification defines the timers used in the Link Layer. To accurately test timer implementations, there are several considerations beyond the simple timer definition that factor into this document's timing scheme. Section 7.5 of the USB 3.1 Specification defines the link layer timers to have an implementation tolerance of +50%. Chapter 6 details an SSC Tolerance of -5300/+300ppm, the lower limit of which could add 0.5% time to any interval. Consideration for Physical Layer and Link Layer processing time (Tx and Rx latency time) is also applied.

The following expression is used for determining each timer's high-end value used in this specification:

$$\text{Spec Defined Timer value} \times \text{Additional50pctTolerance} \times \text{SSCFactor} + \text{tLinkTurnAround}$$

Spec Defined Timer value = the timer value defined in USB 3.1 specification.

Additional50pctTolerance = +50% tolerance defined in the Section 7.5 of the USB 3.1 specification.

SSCFactor = delay induced by SSC influenced clock with a maximum SSC of 5000ppm applied, equating to +0.5%.

tLinkTurnAround = tDHPResponse - tDPacket.

This is understood to be the maximum delay induced by the PHY and Link layers when a link event occurs, until the respective action is made, when there is no other packet processing occurring on the port. This is measured from the time a packet is received, until the time a response is generated on the transmit side.

For a Gen 1 port:

tLinkTurnaround = tDHPResponse - tDPacket = 2540ns - 2140ns = 400ns

For a Gen 2 port:

tLinkTurnaround = tDHPResponse - tDPacket = 1610ns - 910ns = 700ns

Note: Since captive re-timer delay is included in tDHPResponse and not factored out for tLinkTurnaround, a PUT that does not contain a captive re-timer can use the extra time for its Tx and Rx Data Paths.

Using their respective numerical values, the expression is presented again below:

$$\text{Spec Defined Timer value} \times 1.5 \times 1.005 + \text{tLinkTurnaround}$$

The expression above is applicable for Link Layer timers.

$$\text{Spec Defined Timer value} \times 1.005 + \text{tLinkTurnaround}$$

The expression above is applicable for PHY and protocol layer timers.

The following table lists the timers used in the Link Layer compliance tests and the window of compliant durations between the initial event that started the timer, and the expected response when the timer expires.

PORT_U2_TIMEOUT is not listed in the table because its value is programmable using the U2 Inactivity Timeout LMP. A calculation is needed as per the value programmed.

tPollingLFPSEstablishedTimeout was created from USB 3.1 Specification section 7.5.4.3.1: A Port shall establish its LFPS operating condition within 80us.

tRecoveryTimeout was created as a replacement for tLinkTurnaround when an error occurs that should result in a quick transition to Recovery. This mechanism may be implemented separately from tLinkTurnaround logic. Both Gen 1 and Gen 2 PUTs are given 1us to enter recovery for TDs 7.13, 7.14, 7.15, and 7.30.

[tbl-54.md](tbl-54.md)

53

USB 3.1 Link Layer Test Specification

Chapter 4: Timing Definitions

1/17/2018

[tbl-55.md](tbl-55.md)

Table 4-1

Note +/- 100ns applies to Timer Expiration Times in Table 4-1 above.

54

USB 3.1 Link Layer Test Specification

Chapter 5: Test Descriptions

1/17/2018

## 5 Test Descriptions

### 5.1 Link Initialization Sequence

Most of the following test descriptions (TDs) refer to the Link Initialization Sequence, described here. The purpose of the Link Initialization Sequence is to establish the link between the LVS and the PUT and check that link establishment and initialization is followed properly by the PUT.

Some tests are designed to follow the Link Initialization Sequence up to a certain point and then introduce different test steps. This is reflected in each specific TD.

Link training is different for Gen 1 and Gen 2 capable PUTs during Polling substates. The verification checks on these substates are performed during TD 7.1.

Covered Assertions

7.2.4.1.1#6,8,10-17,22

7.2.4.1.4#2

7.3.4#2

7.5.6.1#5,6

8.4.5#1

8.4.6#1,3 (downstream)

8.4.7#1 (upstream)

Link Initialization Sequence

1. The LVS and the PUT go through the initial steps of the LTSSM (eSS.Disabled, Rx.Detect, Polling) to reach U0.
2. Once in U0, the LVS will transmit the Header Sequence Number Advertisement and

a. In Gen 1 speed, the Rx Header Buffer Credit Advertisement.
b. In Gen 2 speeds, the Type 1 and Type 2 Rx Header Buffer Credit Advertisements.

3. The LVS verifies that:

a. The Header Sequence Number Advertisement transmitted by the PUT is LGOOD_7
b. A Gen 2 PUT transmits the following Type 1 and Type 2 Rx Header Buffer Credit Advertisements: LCRD1_A, LCRD1_B, LCRD1_C, LCRD1_D, LCRD2_A, LCRD2_B, LCRD2_C, LCRD2_D.
c. A Gen 1 PUT transmits the following Rx Header Buffer Credit Advertisements: LCRD_A, LCRD_B, LCRD_C and LCRD_D.

4. The LVS and the PUT will exchange Port Configuration transactions.

■ If the LVS is configured as a Downstream Port:

a. LVS waits for the PUT's Port Capability LMP.
b. LVS verifies that the Port Capability LMP is valid.
c. LVS transmits its Port Capability LMP.
d. LVS transmits a valid Port Configuration LMP to the PUT.

55

USB 3.1 Link Layer Test Specification

Chapter 5: Test Descriptions

1/17/2018

e. LVS waits for the PUT Port Configuration Response LMP.
f. LVS verifies that the Port Configuration Response LMP is valid.

■ If the LVS is configured as an Upstream Port:

a. LVS waits for the PUT's Port Capability LMP.
b. LVS verifies that the Port Capability LMP is valid.
c. LVS transmits its Port Capability LMP.
d. LVS waits for the PUT to transmit the Port Configuration LMP.
e. LVS verifies that the Port Configuration LMP is valid.
f. LVS transmits a Port Configuration Response LMP to the device.

5. The test fails if the Port Configuration transaction is not completed before tPortConfiguration expires.
6. The LVS will keep the link active by sending Link Pollings (LUP when it is configured as an Upstream Port or LDN when it is configured as a Downstream Port) for 50ms.
7. The Link Initialization Sequence passes if the exchanges are successful, no timeout is detected, no recovery is entered, all packets are successfully received, all credits are restored and the link stays in U0 for at least 50ms.

### 5.2 Physical Layer

#### TD.6.1 Lane Polarity Inversion Test

This test verifies that the PUT can successfully handle reception of lane polarity inversion.

##### Covered Assertions

(No Physical Layer assertions defined)

7.5.4.4.1#1

##### Overview of Test Steps

1. Invert the LVS TX lane polarity.
2. Bring the link to U0 using the Link Initialization Sequence.
3. The test passes if the Link Initialization Sequence passes.

#### TD.6.2 SKP Test

This test verifies that the PUT supports all possible skip (SKP) combinations.

Combinations to be tested for Gen 1 PUT:

A. Repetition of one skip ordered set followed by 354 symbols (word aligned)
B. Repetition of one skip ordered set followed by 353 symbols (word misaligned)
C. Repetition of two skip ordered sets followed by 708 symbols (word aligned)
D. Repetition of two skip ordered sets followed by 707 symbols (word misaligned)
E. Repetition of three skip ordered sets followed by 1,062 symbols (word aligned)
F. Repetition of three skip ordered sets followed by 1,061 symbols (word misaligned)

56

USB 3.1 Link Layer Test Specification

Chapter 5: Test Descriptions

1/17/2018

G. Repetition of four skip ordered sets followed by 1,416 symbols (word aligned)
H. Repetition of four skip ordered sets followed by 1,415 symbols (word misaligned)

Combinations to be tested for Gen 2 PUT:

For Each SKP Symbol count x in X:

A. Repeat Sequence 01 with all SKP OSs containing x SKP symbols.
B. Repeat Sequence 01 with all SKP OSs containing x SKP symbols, with one SKP symbol including a bit error.
C. Repeat Sequence 02 with all SKP OSs containing x SKP symbols.
D. Repeat Sequence 02 with all SKP OSs containing x SKP symbols, with one SKP symbol including a bit error.

Received SKP symbol counts in Gen 2 PUT:

X = {4,8,12,16,20,24,28,32,36} if PUT includes no captive re-timer
X = {8,12,16,20,24,28,32} if PUT includes one captive re-timer

Sequences of Repetition for Gen 2 PUT:

Sequence 01:

a. Forty (40) blocks
b. One SKP OS

Sequence 02:

a. One hundred and nine (109) blocks
b. Two SKP OS
c. One block
d. One SKP OS

# Covered Assertions

(No Physical Layer assertions defined)

# Overview of Test Steps

1. Do steps 1 to 4 of the Link Initialization Sequence.
2. The LVS will keep the link active by sending Link Pollings (LUP when it is configured as an Upstream Port or LDN when it is configured as a Downstream Port) for 50ms. Skips will be generated according to Combination A described above.
3. The test passes if the exchanges are successful, no timeout is detected, no recovery is entered, all packets are successfully received, all credits are restored and the link stays in U0 for at least 50ms.
4. Repeat the steps with the next combination listed above.

### TD.6.3 Elasticity Buffer Test

This test verifies that the PUT's elasticity buffer supports the required frequency range, from -5,300 to 300ppm.

57

USB 3.1 Link Layer Test Specification

Chapter 5: Test Descriptions

1/17/2018

# Covered Assertions

(No Physical Layer assertions defined)

# Overview of Test Steps

1. Configure the LVS with an SSC clock of -5300ppm.
2. Bring the link to U0 using the Link Initialization Sequence.
3. The test passes if the Link Initialization Sequence passes.
4. Repeat the above steps with an SSC clock of +300ppm.

# TD.6.4 LFPS Frequency Test

This test verifies that the PUT's LFPS detector supports the required frequency range. The periods to be tested are:

A. tPeriod = 10 MHz (min)
B. SS: tPeriod = 50 MHz, SSP: tPeriod = 40 MHz (max)

# Covered Assertions

(No Physical Layer assertions defined)

# Overview of Test Steps

1. The LVS and the PUT go through the initial steps of the LTSSM (eSS.Disabled, Rx.Detect) to reach Polling.LFPS.
2. The LVS will start generating a Polling.LFPS signal having durations of tBurst = 1 us and tRepeat = 10 us. The burst period will be set to the first period listed above.
3. The test passes if the PUT moves successfully to Polling.RxEQ according to section 7.5.4.3.2 of the USB 3.1 specification.
4. Repeat the steps with the other period listed above.

# TD.6.5 Polling.LFPS Duration Test

This test verifies that the PUT's Polling.LFPS detector supports the required duration range. Here are the durations to be tested:

A. tBurst = 0.6 us and tRepeat = 6 us
B. tBurst = 0.6 us and tRepeat = 14 us
C. tBurst = 1.4 us and tRepeat = 6 us
D. tBurst = 1.4 us and tRepeat = 14 us

# Covered Assertions

(No Physical Layer assertions defined)

# Overview of Test Steps

1. The LVS and the PUT go through the initial steps of the LTSSM (eSS.Disabled, Rx.Detect) to reach Polling.LFPS.
2. The LVS will start generating a Polling.LFPS signal having the first duration specified in the list above.

58

USB 3.1 Link Layer Test Specification

Chapter 5: Test Descriptions

1/17/2018

3. The test passes if the PUT moves successfully to Polling.RxEQ according to section 7.5.4.3.2, and if the Polling.LFPS tPeriod, tBurst and tRepeat from the PUT are within the ranges specified in section 6.9.1.
4. Repeat the steps with the other durations listed above.

### TD.6.6 SCD Duration Test (Gen 2 Capable Only)

This test verifies that the PUT's Polling.LFPS detector supports the required duration range for SCD signals. Here are the durations to be tested:

A. tBurst = 0.6 us and '0' tRepeat = 6 us and '1' tRepeat = 11 us
B. tBurst = 0.6 us and '0' tRepeat = 6 us and '1' tRepeat = 14 us
C. tBurst = 0.6 us and '0' tRepeat = 9 us and '1' tRepeat = 11 us
D. tBurst = 0.6 us and '0' tRepeat = 9 us and '1' tRepeat = 14 us
E. tBurst = 1.4 us and '0' tRepeat = 6 us and '1' tRepeat = 11 us
F. tBurst = 1.4 us and '0' tRepeat = 6 us and '1' tRepeat = 14 us
G. tBurst = 1.4 us and '0' tRepeat = 9 us and '1' tRepeat = 11 us
H. tBurst = 1.4 us and '0' tRepeat = 9 us and '1' tRepeat = 14 us

### Covered Assertions

(No Physical Layer assertions defined)

### Overview of Test Steps

1. The LVS and the PUT go through the initial steps of the LTSSM (eSS.Disabled, Rx.Detect) to reach Polling.LFPS.
2. The LVS will start generating a Polling.LFPS SCD1 signal having the A parameters specified in the list above.
3. The LVS verifies that:
  a. The PUT moves successfully to Polling.LFPSPlus according to section 7.5.4.3.2.
  b. The SCD1 Polling.LFPSs transmitted from the PUT have tPeriod, tBurst, and tRepeat within the ranges specified in spec sections 6.9.1 and 6.9.4.1.
4. The LVS will generate Polling.LFPS SCD2 signals having the A parameters specified in the list above.
5. The test passes if the PUT moves successfully to Polling.PortMatch according to section 7.5.4.4.2, and if the SCD2 Polling.LFPSs transmitted from the PUT have tPeriod, tBurst and tRepeat within the ranges specified in section 6.9.1 and 6.9.4.1.
6. Repeat the steps with the other parameters listed above.

### TD.6.7 PWM Duration Test (Gen 2 Capable Only)

This test verifies that the PUT's Polling.LFPS detector supports the required duration range for PWM signals. Here are the durations to be tested:

A. tPWM = 2 us and tLFPS-0 = 0.5 us and tLFPS-1 = 1.33 us
B. tPWM = 2 us and tLFPS-0 = 0.5 us and tLFPS-1 = 1.8 us
C. tPWM = 2 us and tLFPS-0 = 0.8 us and tLFPS-1 = 1.33 us
D. tPWM = 2 us and tLFPS-0 = 0.8 us and tLFPS-1 = 1.8 us
E. tPWM = 2.4 us and tLFPS-0 = 0.5 us and tLFPS-1 = 1.33 us
F. tPWM = 2.4 us and tLFPS-0 = 0.5 us and tLFPS-1 = 1.8 us

59

USB 3.1 Link Layer Test Specification

Chapter 5: Test Descriptions

1/17/2018

G. tPWM = 2.4 us and tLFPS-0 = 0.8 us and tLFPS-1 = 1.33 us
H. tPWM = 2.4 us and tLFPS-0 = 0.8 us and tLFPS-1 = 1.8 us

# Covered Assertions

(No Physical Layer assertions defined)

# Overview of Test Steps

1. The LVS and the PUT go through the initial steps of the LTSSM (eSS.Disabled, Rx.Detect) to reach Polling.PortMatch.
2. The LVS will generate LBPM signals having the A parameters specified in the list above.
3. The LVS verifies that:

a. The PUT moves successfully to Polling.PortConfig according to section 7.5.4.5.2.
b. The PWM LFPSs transmitted from the PUT have tPWM, tLFPS-0, and tLFPS-1 within the ranges specified in spec sections 6.9.1 and 6.9.5.1.

4. The LVS will generate LBPM signals having the A parameters specified in the list above.
5. The test passes if the PUT moves successfully to Polling.RxEQ according to section 7.5.4.6.2, and if the PWM LFPSs transmitted from the PUT have tPWM, tLFPS-0 and tLFPS-1 within the ranges specified in section 6.9.1 and 6.9.4.1.
6. Repeat the steps with the other parameters listed above.

### 5.3 Link Layer

#### TD.7.1 Link Bring-up Test

This test verifies that the Link Verification System (LVS) and the Port under Test (PUT) can reach U0 successfully.

As the test progresses it is divided into four subtests. Ports with Gen 1 capability and not Gen 2 capability must be tested with subtests 1 and 2. Ports with Gen 2 capability must be tested with subtests 3, 4 and 5.

# Covered Assertions

Refer to the list of covered assertions for the Link Initialization Sequence

# Overview of Test Steps

1. The LVS starts the link process.

- If the LVS is configured as a Downstream Port, the LVS asserts VBUS. The PUT should move from eSS.Disabled to Rx.Detect.
- If the LVS is configured as an Upstream Port, the LVS asserts Terminations. The PUT should already be in Rx.Detect.

2. The test fails if the PUT does not transmit Polling.LFPS bursts before tRxDetectQuietTimeout + tPollingLFPSEstablishedTimeout expires.

# Continue to Required Subtest

60

USB 3.1 Link Layer Test Specification

Chapter 5: Test Descriptions

1/17/2018

# Subtest 1 (TD 7.1.1):

1. The LVS waits to receive Polling.LFPS bursts.
2. The LVS transmits four Polling.LFPS bursts.
3. The test fails if any of the following occur:

a. If the PUT does not contain a captive re-timer, it does not transmit at least sixteen consecutive Polling.LFPS bursts.
b. If the PUT contains a captive re-timer, it does not transmit at least four consecutive Polling.LFPS bursts.
c. The PUT does not transmit at least four consecutive Polling.LFPS bursts after receiving one Polling.LFPS bursts.
d. The PUT transitions away from Polling.LFPS before the LVS sends at least two consecutive Polling.LFPS bursts.
e. The PUT does not transition from Polling.LFPS before tPollingLFPSTimeout expires.

4. The test fails if the PUT has transmitted more than 6 LFPS after receiving 1 LFPS and the Number of LFPS tx'd before receiving 1 > 18 – the Number of LFPS tx'd after receiving 1.
5. The LVS transmits 65,536 TSEQ ordered sets.
6. The test fails if any of the following occur:

a. The PUT does not transmit TSEQ ordered sets.
b. The PUT transmits SKP Ordered Sets, Idle Symbols, or any other Packet, Symbol or Ordered Set during TSEQ transmission or between training ordered sets.

7. The LVS transmits TS1 ordered sets and waits to receive eight consecutive and identical TS1 or TS2 ordered sets from the PUT.
8. The test fails if any of the following occur:

a. The PUT does not transmit TS1 ordered sets.
b. The PUT transmits TS2s before the LVS sends eight consecutive and identical TS1s or TS2s.
c. The PUT interrupts a TS1 ordered set to transmit a SKP ordered set (between TS1 ordered sets is OK).
d. The PUT transmits Idle Symbols or any other Packet.
e. The PUT continues to transmit TS1 ordered sets after tPollingActiveTimeout expires.

9. The LVS transmits TS2 ordered sets and readies to complete the Polling.Configuration handshake.

10. The test fails if any of the following occur:

a. The PUT does not transmit at least sixteen consecutiveTS2 ordered sets after receiving one TS2 ordered set.
b. The PUT sends Idle symbols before the LVS sends at least eight consecutive TS2 ordered sets.
c. The PUT interrupts transmission of a TS2 ordered set to transmit a SKP ordered set (between TS2 ordered sets is OK).
d. The PUT continues to transmit TS2 ordered sets after tPollingConfigurationTimeout expires.

11. The LVS transmits Idle symbols.

12. The test fails if upon entering U0, the PUT does not transmit the Header Sequence Number Advertisement and the Rx Header Buffer Credit Advertisement before their respective timeouts, PENDING_HP_TIMER and CREDIT_HP_TIMER, expire.

61

USB 3.1 Link Layer Test Specification

Chapter 5: Test Descriptions

1/17/2018

13. The LVS and PUT continue the test with the Link Initialization Sequence starting at step two.

# Subtest 2 (TD 7.1.2):

1. The LVS transmits Polling.LFPS bursts with an SCD1 signature.
2. The test fails if a PUT that does not contain a captive re-timer does not transmit at least 16 Polling.LFPS bursts.
3. The LVS switches to regular Polling.LFPS bursts after transmitting 4 SCD1 and receiving 16 Polling.LFPS bursts, or after receiving 4 Polling.LFPS and tPollingSCDLFPSTimeout has expired – whichever comes first.
4. The test fails if any of the following occur:

a. The PUT does not transmit at least four consecutive Polling.LFPS bursts after receiving one Polling.LFPS burst (Note: The received Polling.LFPS burst may be part of an SCD1 from the LVS, or may be from a regular Polling.LFPS burst after the LVS transitions)
b. The PUT transitions away from Polling.LFPS before the LVS sends at least two consecutive Polling.LFPS bursts.
c. The PUT does not transition from Polling.LFPS before tPollingLFPSTimeout expires.

5. The test fails if the PUT has transmitted more than 6 LFPS after receiving 1 regular (non-SCD) Polling.LFPS burst and the Number of LFPS tx'd before receiving \(1 > 18\) - the Number of LFPS tx'd after receiving 1.
6. Continue to Subtest 1 (TD 7.1.1) step 5.

# Subtest 3 (TD 7.1.3)

1. The LVS transmits Polling.LFPS bursts.
2. The test fails if any of the following occur:

a. The PUT does not switch to SuperSpeed operation after transmitting 4 SCD1 and receiving 16 Polling.LFPS.
b. For a PUT with no captive re-timer, the PUT does not transmit 16 regular Polling.LFPS
c. The PUT does not transmit at least four consecutive regular Polling.LFPS bursts after receiving one Polling.LFPS burst.
d. For a PUT with no captive re-timer, the PUT does not transition to Polling.RxEQ after transmitting 16 regular Polling.LFPS.
e. For a PUT with a captive re-timer, the PUT does not transition to Polling.RxEQ after transmitting 4 regular Polling.LFPS.

3. Continue to Subtest 1 (TD 7.1.1) step 5.

# Subtest 4 (TD 7.1.4)

1. The LVS transmits Polling.LFPS bursts with an SCD1 signature.

62

USB 3.1 Link Layer Test Specification

Chapter 5: Test Descriptions

1/17/2018

2. The test fails if the PUT does not transmit two SCD1 after one SCD1 or SCD2 is received.
3. The LVS transitions to transmitting Polling.LFPS bursts with an SCD2 signature after transmitting two SCD1 after receiving 1 SCD1 or SCD2 from the PUT
4. The test fails if the PUT does not transmit two SCD2 after one SCD2 is received.
5. The LVS transmits continuous PHY Capability LBPMs to announce its 10Gbps capability.
6. The test fails if the PUT does not continuously transmit its PHY Capability LBPMs.
7. If the LVS has a PHY Capability greater than the PUT, then:

a. The LVS adjusts its PHY Capability by transmitting PHY Capability LBPMs that match the PUT.
b. The test fails if the PUT does not continuously transmit its PHY Capability LBPMs.

8. The test fails if the PUT does not transmit four consecutive and matched PHY Capability LBPMs after receiving two consecutive and matched PHY Capability LBPMs or PHY Ready LBPMs.
9. The LVS transmits 524,288 TSEQ Ordered Sets, inserting a SYNC Ordered Set every 16,384 Ordered Sets.
10. The test fails if any of the following occur:

a. The PUT does not transmit TSEQ Ordered Sets.
b. The PUT does not transmit a SYNC Ordered Set for every 16,384 TSEQ Ordered Sets.
c. The PUT transmits Idle Symbols, or any other Packet, Symbol or Ordered Set besides SYNC or SKP Ordered Sets, during TSEQ transmission or between TSEQ Ordered Sets.

11. The LVS transmits TS1 Ordered Sets, inserting a SYNC Ordered Set every 32 Ordered Sets, and inserting SKP Ordered Sets periodically when necessary.
12. The LVS waits to receive eight consecutive and identical TS1 or TS2 Ordered Sets from the PUT. Note: SYNC and SKP Ordered Sets do not disqualify consecutive TS1s / TS2s. Symbols 14-15 of the TS1 / TS2 Ordered Sets do not need to be identical.
13. The test fails if any of the following occur:

a. The PUT does not transmit TS1 ordered sets.
b. The PUT transmits TS2s before the LVS transmits eight consecutive and identical TS1s or TS2s.
c. The PUT interrupts a TS1 Ordered Set to transmit a SKP or SYNC Ordered Set (between TS1 ordered sets is OK).
d. The PUT transmits Idle Symbols or any other Packet.
e. The PUT continues to transmit TS1 Ordered Sets after tPollingActiveTimeout expires.

14. The LVS transmits TS2 Ordered Sets, inserting a SYNC Ordered Set every 32 Ordered Sets, and inserting SKP Ordered Sets periodically when necessary.
15. The test fails if any of the following occur:

a. The PUT does not transmit at least 16 consecutive TS2 ordered sets after receiving one TS2 ordered set.
b. The PUT transmits Idle symbols before the LVS transmits eight consecutive and identical TS2s.

63

USB 3.1 Link Layer Test Specification

Chapter 5: Test Descriptions

1/17/2018

c. The PUT interrupts a TS1 Ordered Set to transmit a SKP or SYNC Ordered Set (between TS2 Ordered Sets is OK).
d. The PUT continues to transmit TS2 Ordered Sets after tPollingConfigurationTimeout expires.

16. The LVS transmits a single SDS Ordered Set and then data blocks with Idle Symbols.
17. The test fails if upon entering U0, the PUT does not transmit the Header Sequence Number Advertisement and the Type 1 and Type 2 Rx Header Buffer Credit Advertisements before their respective timeouts, PENDING_HP_TIMER and Type 1 and Type 2 CREDIT_HP_TIMERs, expire.
18. The LVS and PUT continue the Link Initialization Sequence starting at step two.

# Subtest 5 (TD 7.1.5)

1. The LVS waits to receive Polling.LFPS bursts (as components of the SCD1)
2. The LVS transmits four regular Polling.LFPS bursts and transitions to Polling.RxEQ
3. The test fails if any of the following occur:

a. The PUT does not switch to SuperSpeed operation and Polling.RxEQ state after tPollingSCDLFPSTimeout
b. The PUT does not continue to send Polling.LFPS up until tPollingSCDLFPSTimeout.

4. Continue to Subtest 1 (TD 7.01.1) step 5.

### TD.7.2 Link Commands Framings Robustness Test

This test verifies that the PUT can tolerate link commands having one symbol error in the LCSTART framing. Here are the combinations to be tested:

A. ERR SLC SLC EPF
B. SLC ERR SLC EPF
C. SLC SLC ERR EPF
D. SLC SLC SLC ERR

The Port Configuration transaction will be used for this purpose.

# Covered Assertions

7.3.4#1,2

# Overview of Test Steps

1. Perform the Link Initialization Sequence, but transmit all LCRD_X or LCRD1_X with an error in the first LCSTART symbol.
2. The test passes if the Link Initialization Sequence passes.
3. Repeat the above steps with an error in the second, third, and fourth LCSTART symbols as shown above.

64

USB 3.1 Link Layer Test Specification

Chapter 5: Test Descriptions

1/17/2018

### TD.7.3 Link Commands CRC-5 Robustness Test

This test verifies that a Gen 1 PUT will ignore link commands with a CRC-5 error, even if only one of the Link Command Words has a CRC-5 error. The test verifies that a Gen 2 device will accept link commands with one CRC-5 error and ignore link commands with both LCWs containing a CRC-5 error. The Port Configuration transaction will be used for this purpose.

The tested CRC-5 error robustness conditions are:

A. Incorrect CRC-5 in first Link Command Word
B. Incorrect CRC-5 in second Link Command Word
C. Both Link Command Words have an incorrect CRC-5.

# Covered Assertions

7.3.4#2

# Overview of Test Steps

1. Perform the Link Initialization Sequence but transmit all LCRD_X or LCRD1_X with condition A above.
2. The test passes if:
   a. A Gen 1 PUT enters recovery when CREDIT_HP_TIMER expires.
   b. A Gen 2 PUT stays in U0 for 50ms.
3. Repeat the above steps for condition B listed above.
4. Perform the Link Initialization Sequence but transmit all LCRD_X or LCRD1_X with condition C above.
5. The test passes if the PUT enters recovery when the CREDIT_HP_TIMER or the Type 1 CREDIT_HP_TIMER expires.

### TD.7.4 Invalid Link Commands Test

This test verifies that the PUT will ignore Link Commands with link command information in the first LCW not the same as link command information in the second LCW, and both pass the CRC5 check.

# Covered Assertions

7.3.4#2

# Overview of Test Steps

1. Do steps 1 to 5 of the Link Initialization Sequence.
2. The LVS sends a link command with LGO_U1 in the first LCW and LGO_U2 in the second LCW, with good CRC-5 calculations on both.
3. The test fails if the PUT responds with an LAU or LXU.
4. The LVS will keep the link active by sending Link Pollings (LUP when it is configured as an Upstream Port or LDN when it is configured as a Downstream Port) for 50ms.
5. The test passes if the link command is ignored, all exchanges are successful, no timeout is detected, no recovery is entered, all packets are successfully received by the PUT, all credits are restored and the link stays in U0 for at least 50ms.

65

USB 3.1 Link Layer Test Specification

Chapter 5: Test Descriptions

1/17/2018

### TD.7.5 Header Packet Framing Robustness Test

This test verifies that the PUT does not invalidate header packets having one symbol error in the HPSTART framing. The combinations to be tested:

A. ERR SHP SHP EPF
B. SHP ERR SHP EPF
C. SHP SHP ERR EPF
D. SHP SHP SHP ERR

The Port Configuration transaction will be used for this purpose.

#### Covered Assertions

7.2.4.1.4#1

#### Overview of Test Steps

1. Perform the Link Initialization Sequence, but transmit all Header Packets with an error in the first HPSTART symbol.
2. The test passes if the Link Initialization Sequence passes.
3. Repeat the above steps with an error in the second, third, and fourth HPSTART symbols, as shown above.

### TD.7.6 Data Payload Packet Framing Robustness Test

This test verifies that the PUT does not invalidate data payload packets having a single character framing error in DPPSTART and DPPEND. The combinations to be tested:

A. ERR SDP SDP EPF
B. SDP ERR SDP EPF
C. SDP SDP ERR EPF
D. SDP SDP SDP ERR
E. ERR END END EPF
F. END ERR END EPF
G. END END ERR EPF
H. END END END ERR

When the LVS is a Downstream Port, it will place framing errors on Setup DP Packets.

When the LVS is an Upstream Port, it will reply to the GetDeviceDescriptor request with a DPP containing framing errors.

If the DUT is a Gen 1 device, the LVS also verifies that the PUT can handle Gen2 Transaction Packets in which several Gen1 Reserved bits are in use. The verification includes various configurations in the TPS and TT fields of the Gen2 Transaction Packet.

#### Covered Assertions

7.2.4.1.6#1,2

7.3.4.1#3

66

USB 3.1 Link Layer Test Specification

Chapter 5: Test Descriptions

1/17/2018

# Overview of Test Steps

1. Perform the Link Initialization Sequence.
2. At this stage the Downstream Port is expected to issue a GetDeviceDescriptor request.

▪ If the LVS is configured as an Upstream Port:

a. The LVS prompts the test operator to have the PUT send a GetDeviceDescriptor request through USB30CV and then press “OK”.
b. The test fails if no GetDeviceDescriptor request is received and the test operator has pressed “OK”.
c. When the LVS receives a GetDeviceDescriptor request, it closes the prompt. The LVS will respond to the request with a DPP containing the Device Descriptor data which includes the first framing error listed above.

▪ If the LVS is configured as a Downstream Port, it will issue a GetDeviceDescriptor request, but will send the SETUP DP with the first framing error listed above.

3. The LVS will keep the link active by sending Link Pollings (LUP when it is configured as an Upstream Port or LDN when it is configured as a Downstream Port) for 50ms.
4. The test fails if the data exchange fails on the protocol level.
5. The test passes if the exchanges are successful, no timeout is detected, no recovery is entered, all packets are successfully received by the PUT, all credits are restored and the link stays in U0 for at least 50ms.
6. Repeat for each condition listed above.

# TD.7.7 RX Header Packet Retransmission Test

This test verifies that the PUT will send an LBAD if an invalid header packet is received, and that the retransmission will be correctly handled.

The tested conditions invalidating a header packet are:

A. Incorrect CRC-16
B. Incorrect CRC-5
C. K28.2 SDP symbol in HP data
D. K28.3 EDB symbol in HP data
E. K28.4 SUB symbol in HP data
F. K28.6 Reserved K-symbol in HP data
G. K27.7 SHP symbol in HP data
H. K29.7 END symbol in HP data
I. K30.7 SLC symbol in HP data
J. K23.7 EPF symbol in HP data

Conditions C – J are tested for Gen 1 PUTs only. Each of the conditions C – J in the following positions, one case at a time:

1. Position 2: SHP SHP SHP EPF DX.X KX.X DX.X DX.X
2. Position 5: SHP SHP SHP EPF DX.X DX.X DX.X DX.X KX.X

# Covered Assertions

7.2.4.1.4#3, 4

67

USB 3.1 Link Layer Test Specification

Chapter 5: Test Descriptions

1/17/2018

# Overview of Test Steps

1. Do steps 1 to 3 of the Link Initialization Sequence.
2. The LVS and the PUT will exchange Port Configuration transactions, but the first packet sent by the LVS will be invalid.

▪ If the LVS is configured as a Downstream Port:

a. The LVS waits for the PUT's Port Capability LMP.
b. LVS verifies that the Port Capability LMP is valid.
c. LVS transmits its Port Capability LMP with the first invalid condition listed above.
d. LVS verifies that the PUT replies with an LBAD.
e. LVS transmits a LRTY and then retransmits the packet.
f. LVS transmits the Port Configuration LMP.
g. LVS waits for the PUT's Port Configuration Response LMP.
h. LVS verifies the PUT's Port Configuration Response LMP.

▪ If the LVS is configured as an Upstream Port:

a. LVS waits for the PUT's Port Capability LMP.
b. LVS verifies that the Port Capability LMP is valid.
c. LVS transmits its Port Capability LMP with the first invalid condition listed above.
d. LVS verifies the PUT replies with an LBAD.
e. LVS transmits a LRTY and then retransmits the packet.
f. LVS waits for the PUT's Port Configuration LMP.
g. LVS verifies the PUT's Port Configuration LMP.
h. LVS transmits its Port Configuration Response LMP.

3. The LVS will keep the link active by sending Link Pollings (LUP when the LVS is configured as Upstream Port, or LDN when the LVS is configured as a Downstream Port) for 50ms.
4. The test passes if the exchanges are successful, no timeout is detected, no recovery is entered, the PUT responds to the invalid packets with an LBAD, all other packets are successfully received, all credits are restored and the link stays in U0 for at least 50ms.
5. Repeat the above steps for each of the invalid conditions listed above.
6. For a Gen 1 device, skip the remaining steps.
7. The LVS and PUT complete the Link Initialization Sequence.

▪ If the LVS is configured as a Downstream Port:

a. LVS issues a GetDeviceDescriptor() request for the PUT, but transmits the SETUP packet with Condition A listed above.

▪ If the LVS is configured as an Upstream Port:

a. The LVS prompts the test operator to have the PUT send a GetDeviceDescriptor request through USB30CV and then press "OK".
b. The test fails if no GetDeviceDescriptor request is received and the test operator has pressed "OK".
c. LVS will transmit the IN DP with Condition A listed above.

68

USB 3.1 Link Layer Test Specification

Chapter 5: Test Descriptions

1/17/2018

8. The LVs will keep the link active by sending Link Pollings (LUP when it is configured as an Upstream Port, LDN when it is configured as a Downstream Port).
9. The test passes if the exchanges are successful, no timeout is detected, no recovery is entered, the PUT responds to the invalid packets with an LBAD, all other packets are successfully received, all credits are restored and the link stays in U0 for at least 50ms.
10. Repeat steps 7 through 9 for Condition B listed above.

### TD.7.8 TX Header Packet Retransmission Test

This test verifies that the PUT will correctly retransmit a header packet on receipt of an LBAD.

#### Covered Assertions

7.2.4.1.3#1, 2

#### Overview of Test Steps

1. Do steps 1 to 3 of the Link Initialization Sequence.
2. The LVS and the PUT will exchange the Port Configuration transaction, but in this case the LVS will respond to the first packet sent by the PUT with an LBAD.

■ If the LVS is configured as a Downstream Port:

a. LVS waits for the PUT's Port Capability LMP.
b. LVS verifies that the Port Capability LMP is valid.
c. LVS responds to the PUT with an LBAD.
d. LVS waits for the PUT to transmit an LRTY.
e. LVS waits for the retransmitted packet.
f. LVS verifies that the retransmitted packet is the same as the first packet sent by the device.
g. LVS transmits its Port Capability LMP and Port Configuration LMP.
h. LVS waits for the PUT Port Configuration Response LMP.
i. LVS verifies the PUT's Port Configuration Response LMP.

■ If the LVS is configured as an Upstream Port:

a. LVS waits for the PUT's Port Capability LMP.
b. LVS verifies that the Port Capability LMP is valid.
c. LVS transmits its Port Capability LMP.
d. LVS responds to the PUT with an LBAD.
e. LVS waits for the PUT to transmit an LRTY.
f. LVS waits for the retransmitted packet.
g. LVS verifies that the retransmitted packet is the same as the first packet sent by the device.
h. LVS waits for the PUT's Port Configuration LMP.
i. LVS verifies that the Port Configuration LMP is valid.
j. LVS transmits its Port Configuration Response LMP.

69

USB 3.1 Link Layer Test Specification

Chapter 5: Test Descriptions

1/17/2018

3. The LVS will keep the link active by sending Link Pollings (LUP when it was configured as an Upstream Port, LDN when it was configured as a Downstream Port) for 50ms.
4. The test passes if the exchanges are successful, no timeout is detected, no recovery is entered, the packet that the LVS responded to with an LBAD is retransmitted correctly, all other packets are received successfully, all credits are restored and the link stays in U0 for at least 50ms.

### TD.7.9 PENDING_HP_TIMER Deadline Test

This test verifies that:

1) The PUT will accept an LGOOD_N sent at the maximum link delay budget before PENDING_HP_TIMER deadline. The Port Configuration transaction will be used for this purpose.
2) The PUT adheres to tLinkTurnaround as defined in Ch 7 and Appendix E.

Covered Assertions

7.2.4.1.10#2

Overview of Test Steps

1. Perform the Link Initialization Sequence, but transmit LGOOD_N responses for Port Capability LMP 200ns prior to the PENDING_HP_TIMER deadline.
2. The LVS verifies that for each LGOOD_n received from the PUT, the first symbol of the LGOOD_n is received within tLinkTurnaround of the last symbol of the Header Packet that is acknowledged by the LGOOD_n.
3. The LVS will keep the link active by sending Link Pollings (LUP when it is configured as an Upstream Port or LDN when it is configured as a Downstream Port) for 50ms.
4. The test passes if the exchanges are successful, no timeout is detected, no recovery is entered, all packets are successfully received, all credits are restored and the link stays in U0 for at least 50ms.

### TD.7.10 CREDIT_HP_TIMER Deadline Test

This test verifies that the PUT will accept an LCRD_X, LCRD1_X or LCRD2_X sent at the CREDIT_HP_TIMER deadline. The Port Configuration transaction will be used for this purpose.

Covered Assertions

7.2.4.1.10#7

Overview of Test Steps

1. Perform the Link Initialization Sequence but transmit all LCRD_X or LCRD1_X responses tLinkTurnAround prior to the CREDIT_HP_TIMER or type 1 CREDIT_HP_TIMER deadline.
2. The LVS will keep the link active by sending Link Pollings (LUP when it is configured as an Upstream Port or LDN when it is configured as a Downstream Port) for 50ms.
3. For a Gen 1 PUT continue to step 6.
4. For a Gen 2 PUT:

If the LVS is configured as a Downstream Port:

a. LVS issues a GetDeviceDescriptor() request for the PUT.
b. LVS transmits all LCRD2_X responses 200ns prior to the CREDIT_HP_TIMER deadline.

70

USB 3.1 Link Layer Test Specification

Chapter 5: Test Descriptions

1/17/2018

▪ If the LVS is configured as an Upstream Port:

a. The LVS prompts the test operator to have the PUT send a GetDeviceDescriptor request through USB30CV and then press “OK”.
b. The test fails if no GetDeviceDescriptor request is received and the test operator has pressed “OK”.
c. LVS transmits all LCRD2_X responses associated with the GetDeviceDescriptor request 200ns prior to the type 2 CREDIT_HP_TIMER deadline.

5. The LVS will keep the link active by sending Link Pollings (LUP when it is configured as an Upstream Port or LDN when it is configured as a Downstream Port) for 50ms.

6. The test passes if the exchanges are successful, no timeout is detected, no recovery is entered, all packets are successfully received, all credits are restored and the link stays in U0 for at least 50ms.

### TD.7.11 PENDING_HP_TIMER Timeout Test

This test verifies that the PUT will go to recovery when the PENDING_HP_TIMER expires.

#### Covered Assertions

7.2.4.1.10#1

#### Overview of Test Steps

1. Do steps 1 to 3 of the Link Initialization Sequence.
2. The LVS and the PUT will exchange the Port Configuration transaction, but the LVS will respond (with an LGOOD) to the first LMP packet sent by the PUT after expiration of the PENDING_HP_TIMER.

▪ If the LVS is configured as a Downstream Port:

a. LVS waits for the PUT’s Port Capability LMP.
b. LVS verifies that the Port Capability LMP is valid.
c. LVS will not respond to the PUT with an LGOOD.
d. LVS transmits its Port Capability LMP and Port Configuration LMP.

▪ If the LVS is configured as an Upstream Port:

a. LVS waits for the PUT to transmit its Port Capability LMP.
b. LVS verifies that the Port Capability LMP is valid.
c. LVS transmits its PUT Port Capability LMP.
d. LVS will not respond to the PUT with an LGOOD.

3. The LVS will keep the link active by sending Link Pollings (LUP when it is configured as an Upstream Port, LDN when it is configured as a Downstream Port).

4. The test passes if the PUT goes to recovery after the PENDING_HP_TIMER deadline and before the PENDING_HP_TIMER expires.

### TD.7.12 CREDIT_HP_TIMER Timeout Test

This test verifies that the PUT will go to recovery when the CREDIT_HP_TIMER expires.

71

USB 3.1 Link Layer Test Specification

Chapter 5: Test Descriptions

1/17/2018

# Covered Assertions

7.2.4.1.10#6

# Overview of Test Steps

1. Do steps 1 to 4 of the Link Initialization Sequence with the exception that the LVS will not send any LCRD_X or LCRD1_X.
2. The LVS will keep the link active by sending Link Pollings (LUP when it is configured as an Upstream Port, LDN when it is configured as a Downstream Port).
3. The test passes if the PUT goes to recovery after the CREDIT_HP_TIMER deadline and before the CREDIT_HP_TIMER expires. For a Gen 2 PUT, this refers to the Type 1 CREDIT_HP_TIMER.
4. For a Gen 1 device, skip the remaining steps.
5. The LVS and PUT complete the Link Initialization Sequence.

■ If the LVS is configured as a Downstream Port:

a. LVS issues a GetDeviceDescriptor() request for the PUT.
b. LVS will not send any LCRD2_X.

■ If the LVS is configured as an Upstream Port:

a. The LVS prompts the test operator to have the PUT send a GetDeviceDescriptor request through USB30CV and then press "OK".
b. The test fails if no GetDeviceDescriptor request is received and the test operator has pressed "OK".
c. LVS will not send any LCRD2_X.

6. The LVS will keep the link active by sending Link Pollings (LUP when it is configured as an Upstream Port, LDN when it is configured as a Downstream Port).

7. The test passes if the PUT goes to recovery after the type 2 CREDIT_HP_TIMER deadline and before the type 2 CREDIT_HP_TIMER expires.

### TD.7.13 Wrong Header Sequence Test

This test verifies that the PUT will go to recovery when it receives a wrong header sequence.

# Covered Assertions

7.3.5#1

# Overview of Test Steps

1. Do steps 1 to 4 of the Link Initialization Sequence, with the exception that the LVS will send two LMP packets with Header Sequence Numbers that are not sequential.
2. The test passes if the PUT goes to recovery within tRecoveryTransition after reception of the LMP packet with a Header Sequence Number that is not sequential.

### TD.7.14 Wrong LGOOD_N Sequence Test

This test verifies that the PUT will go to recovery when it receives an incorrect LGOOD_N sequence.

72

USB 3.1 Link Layer Test Specification

Chapter 5: Test Descriptions

1/17/2018

# Covered Assertions

7.3.4#4

# Overview of Test Steps

1. Do steps 1 to 4 of the Link Initialization Sequence, with the exception that the LVS will send an LGOOD_0 for the first LMP packet as expected, but will send an LGOOD_n with n ≠ 1 for the second LMP packet.
2. The test passes if the PUT goes to recovery within tRecoveryTransition after reception of the incorrect LGOOD_n.

# TD.7.15 Wrong LCRD_X Sequence Test

This test verifies that the PUT will go to recovery when it receives an incorrect LCRD_X or LCRD1_X sequence.

# Covered Assertions

7.3.4#5

# Overview of Test Steps

1. Do steps 1 to 4 of the Link Initialization Sequence, with the exception that the LVS will send an LCRD_A or LCRD1_A for the first LMP packet as expected, but will send an LCRD_X or LCRD1_X with X ≠ B for the second LMP packet.
2. The test passes if the PUT goes to recovery within tRecoveryTransition after reception of the incorrect LCRD_X or LCRD1_X.
3. For a Gen 1 device, skip the remaining steps.
4. The LVS and PUT complete the Link Initialization Sequence.

■ If the LVS is configured as a Downstream Port:

a. LVS issues a GetDeviceDescriptor() request for the PUT.
b. LVS transmits an LCRD2_A in response to the IN DP.
c. LVS issues a GetDeviceDescriptor() request for the PUT.
d. LVS transmits an LCRD2_X with X ≠ B for the IN DP.

■ If the LVS is configured as an Upstream Port:

a. The LVS prompts the test operator to have the PUT send two GetDeviceDescriptor requests through USB30CV and then press “OK”.
b. The test fails if two GetDeviceDescriptor requests have not been received and the test operator has pressed “OK”.
c. LVS transmits an LCRD2_A in response to the first SETUP DP.
d. LVS transmits an LCRD2_X with X ≠ B for the second SETUP DP.

5. The test passes if the PUT goes to Recovery within tRecoveryTransition after reception of the incorrect LCRD2_X.

73

USB 3.1 Link Layer Test Specification

Chapter 5: Test Descriptions

1/17/2018

### TD.7.16 Link Command Missing Test (Upstream Port Only)

This test verifies that the PUT will go to Recovery if no Link Commands are received for more than tU0RecoveryTimeout.

Please note that the downstream LVS port shall disable transmission of ITPs.

# Covered Assertions

7.3.4#7, 8

7.5.6.1#3

7.5.6.2#6

# Overview of Test Steps

1. Do steps 1 to 4 of the Link Initialization Sequence.
2. The LVS will not send LDNs or any other link commands.
3. The test fails if the PUT goes to Recovery before the tU0RecoveryTimeout deadline, or if it does not go to Recovery after tU0RecoveryTimeout expires.

### TD.7.17 tPortConfiguration Time Timeout Test

This test verifies that a downstream PUT will go to SS.Inactive if tPortConfiguration expires, and an upstream PUT will go to SS.Disabled if tPortConfiguration expires.

# Covered Assertions

7.5.6.2#10,11

8.4.5#1,3

8.4.6#2

# Overview of Test Steps

1. Do steps 1 to 3 of the Link Initialization Sequence.
2. The LVS does not transmit both the Port Capability LMP and Port Configuration LMP.
3. The test fails if any of the following occur:

a. The PUT transitions to eSS.Inactive (downstream PUT) or eSS.Disabled (upstream PUT) before tPortConfiguration deadline.

i. For a PUT with a captive re-timer, the PUT transitions to eSS.Inactive (downstream PUT) or eSS.Disabled (upstream PUT) before tU0Recovery deadline.

b. The PUT does not transition to eSS.Inactive (downstream PUT) or eSS.Disabled (upstream PUT) after tPortConfiguration expires.

i. For a PUT with a captive re-timer, the PUT does not transition to eSS.Inactive (downstream PUT) or eSS.Disabled (upstream PUT) after tU0Recovery expires.

74

USB 3.1 Link Layer Test Specification

Chapter 5: Test Descriptions

1/17/2018

c. An Upstream Facing PUT sends any other packets or LFPS signals.
d. A Downstream Facing PUT sends any other packets or LFPS signals besides a Warm Reset.
e. The PUT enters recovery.

4. Do steps 1 to 3 of the Link Initialization Sequence.

5. The LVS waits for the Port Capability LMP from the PUT.

6. LVS verifies that the Port Capability LMP is valid.

7. The LVS transmits the Port Capability LMP, but does not transmit the Port Configuration LMP (downstream LVS port) or Port Configuration Response LMP (upstream LVS port).

8. The test fails if any of the following occur:

a. The PUT does not transmit the Port Capability LMP.
b. The PUT transitions to eSS.Inactive (downstream PUT) or eSS.Disabled (upstream PUT) before tPortConfiguration deadline.

i. For a PUT with a captive re-timer, the PUT transitions to eSS.Inactive (downstream PUT) or eSS.Disabled (upstream PUT) before tPortConfiguration + tU0Recovery deadline.

c. The PUT does not transition to eSS.Inactive (downstream PUT) or eSS.Disabled (upstream PUT) after tPortConfiguration expires.

i. For a PUT with a captive re-timer, the PUT does not transition to eSS.Inactive (downstream PUT) or eSS.Disabled (upstream PUT) after tPortConfiguration + tU0Recovery expires.

d. An Upstream Facing PUT sends any other packets or LFPS signals.
e. A Downstream Facing PUT sends any other packets or LFPS signals besides a Warm Reset.
f. The PUT enters recovery.

9. Do steps 1 to 3 of the Link Initialization Sequence

10. The LVS does not transmit the Port Capability LMP, but does send the Port Configuration LMP (downstream LVS port) or Port Configuration Response LMP if a Port Configuration LMP is received (upstream LVS port).

11. The test fails if any of the following occur:

a. The PUT does not transmit the Port Capability LMP.
b. The PUT transitions to eSS.Inactive (downstream PUT) or eSS.Disabled (upstream PUT) before tPortConfiguration deadline.

i. For a PUT with a captive re-timer, the PUT transitions to eSS.Inactive (downstream PUT) or eSS.Disabled (upstream PUT) before tPortConfiguration + tU0Recovery deadline.

c. The PUT does not transition to eSS.Inactive (downstream PUT) or eSS.Disabled (upstream PUT) after tPortConfiguration expires.

i. For a PUT with a captive re-timer, the PUT does not transition to eSS.Inactive (downstream PUT) or eSS.Disabled (upstream PUT) after tPortConfiguration + tU0Recovery expires.

d. An Upstream Facing PUT sends any other packets or LFPS signals.
e. A Downstream Facing PUT sends any other packets or LFPS signals besides a Warm Reset.
f. The PUT enters recovery.

75

USB 3.1 Link Layer Test Specification

Chapter 5: Test Descriptions

1/17/2018

### TD.7.18 Low Power initiation for U1 test (Downstream Port Only)

This test verifies that the PUT initiates U1 state.

#### Covered Assertions

7.2.4.2.2#1

7.2.4.2.3#1,3,4,5,7,8

7.2.4.2.7#2,3

7.5.7.1#2

7.5.7.2#6

#### Overview of Test Steps

1. Do steps 1 to 4 of the Link Initialization Sequence.
2. The LVS application prompts the test operator to enable and configure the U1 and U2 inactivity timers through USB30CV. CV will set the U1 Timeout field to 7Fh and the U2 Timeout field to 00h.
3. The LVS waits to receive an LGO_U1 from the PUT. The LVS transmits an LXU, when it receives the LGO_U1.
4. The test fails if the PUT sends an LPMA, or if recovery is entered.
5. The LVS waits to receive an LGO_U1 from the PUT again.
6. The LVS transmits an LAU when it receives the LGO_U1.
7. The test fails if any of the following conditions occur:

a. The PUT does not transmit an LPMA before PM_ENTRY_TIMER deadline
b. The PUT enters recovery
c. The PUT does not transition to U1

8. The LVS transmits the U1 Exit LFPS to transition to U0 and waits to receive U1 Exit LFPS to complete the U1 Exit LFPS handshake.

9. The test fails if the LFPS handshake does not conform to the following specifications from section 6.9.2:

a. Between 300ns - 2us elapses between the start of the LVS U1 Exit LFPS and the start of the PUT U1 Exit LFPS.
b. The PUT U1 Exit LFPS duration is within 0.9us - 1.2us.
c. The PUT enters U0 before Ux_EXIT_TIMER deadline.
d. The PUT enters Recovery before tNoLFPSResponseTimeout deadline after the start of its U1 exit LFPS.

10. The test passes if all packets are successful, recovery is entered once, no extra packets or LFPS signals are received, and the PUT returns to U0.

11. After the LVS completes this test case, clear the U1/U2 registers through the CV prompt.

### TD.7.19 Low Power initiation for U2 test (Downstream Port Only)

This test verifies that the PUT initiates U2 state.

76

USB 3.1 Link Layer Test Specification

Chapter 5: Test Descriptions

1/17/2018

# Covered Assertions

7.2.4.2.2#1,
7.2.4.2.3#1,3,4,5,7,8
7.2.4.2.7#2,3
7.5.8.1#2
7.5.8.2#5

# Overview of Test Steps

1. Do steps 1 to 4 of the Link Initialization Sequence.
The LVS application prompts the test operator to enable and configure the U1 and U2 inactivity timers through USB30CV. CV will set the U1 Timeout field to 00h and the U2 Timeout field to 7Fh.
2. The LVS waits to receive an LGO_U2 from the PUT.
3. The LVS transmits an LXU when it receives the LGO_U2.
4. The test fails if the PUT sends an LPMA, or if recovery is entered.
5. The LVS waits to receive an LGO_U2 from the PUT again.
6. The LVS transmits an LAU when it receives the LGO_U2.
7. The test fails if any of the following occur:

a. The PUT does not transmit an LPMA before PM_ENTRY_TIMER deadline.
b. The PUT enters recovery
c. The PUT does transition to U2.

8. The test fails if the PUT does not transition to U2.
9. The LVS transmits the U2 Exit LFPS to transition to U0 and waits to receive U2 Exit LFPS to complete the U2 Exit LFPS handshake.
10. The test fails if the LFPS handshake does not conform to the following specifications from section 6.9.2:

a. Between 300ns – 2ms elapses between the start of the LVS U2 Exit LFPS and the start of the PUT U2 Exit LFPS.
b. The PUT U2 Exit LFPS duration is within 80us – 2ms.
c. The PUT enters U0 before Ux_EXIT_TIMER deadline.
d. The PUT enters Recovery before tNoLFPSResponseTimeout deadline after the start of its U2 exit LFPS.

11. The test passes if all packets are successful, recovery is entered once, no extra packets or LFPS signals are received, and the PUT returns to U0.
12. After the LVS completes this test case, clear the U1/U2 registers through the CV prompt.

# TD.7.20 PM_LC_TIMER Deadline Test (Downstream Port Only)

This test verifies that the PUT accepts an LGO_U1 sent at the PM_LC_TIMER deadline.

# Covered Assertions

7.2.4.2.1#1, 2

77

USB 3.1 Link Layer Test Specification

Chapter 5: Test Descriptions

1/17/2018

# Overview of Test Steps

1. Do steps 1 to 4 of the Link Initialization Sequence.
2. The LVS application prompts the test operator to enable and configure the U1 and U2 inactivity timers through USB30CV. CV will set the U1 Timeout field to 7Fh and the U2 Timeout field to 00h.
3. The LVS waits to receive an LGO_U1 from the PUT.
4. The LVS transmits an LAU tLinkTurnAround before the PM_LC_TIMER deadline.
5. The test fails if the PUT does not transmit an LPMA after receiving the LAU.
6. After the LVS completes this test case, clear the U1/U2 registers through the CV prompt.

# TD.7.21 PM_LC_TIMER Timeout Test (Downstream Port Only)

This test verifies that the PUT transitions to Recovery when the PM_LC_TIMER expires.

# Covered Assertions

7.2.4.2.1#1

7.2.4.2.3#6

7.3.4#6

# Overview of Test Steps

1. Do steps 1 to 3 of TD.7.18.
2. The LVS does not transmit LAU when it receives the LGO_U1.
3. The test fails if the PUT does not transition to Recovery when the PM_LC_TIMER expires.
4. After the LVS completes this test case, clear the U1/U2 registers through the CV prompt.

# TD.7.22 PM_ENTRY_TIMER Timeout Test (Upstream Port Only)

This test verifies that the PUT transitions to a low power state when the PM_ENTRY_TIMER expires.

# Covered Assertions

7.2.4.2.1#37.2.4.2.3#8,10,12

# Overview of Test Steps

1. Do steps 1 to 4 of TD.7.23.
2. The LVS does not transmit LPMA when it receives LAU.
3. The test fails if the PUT does not transition to U1 when the PM_ENTRY_TIMER expires, the PUT does not transmit LAU, or if the PUT sends any packet or LFPS.

# TD.7.23 Accepted Power Management Transaction for U1 Test (Upstream Port Only)

This test verifies that the PUT transitions to U1 if it receives LGO_U1.

78

USB 3.1 Link Layer Test Specification

Chapter 5: Test Descriptions

1/17/2018

# Covered Assertions

7.2.4.1.1#7,9

7.2.4.2.1#4

7.2.4.2.2#2,3

7.2.4.2.3#2,8,9

7.2.4.2.7#2,3

7.5.5.1#2

7.5.5.2#2

7.5.7.1#2

7.5.7.2#2

8.4.2#1

# Overview of Test Steps

1. Do steps 1 to 4 of the Link Initialization Sequence.
2. The LVS transmits the Set Link Function LMP with the Force_LinkPM_Accept bit asserted.
3. The LVS transmits an LGO_U1 and waits to receive an LAU from the PUT.
4. The test fails if the PUT does not transmit an LAU before PM_LC_TIMER deadline, or recovery is entered.
5. The LVS transmits an LPMA and then transition to U1.
6. The test fails if the PUT does not transition to U1 when the PM_ENTRY_TIMER expires, if recovery is entered, or if the PUT sends any packet.
7. The LVS transmits a U1 Exit LFPS to transition to U0 and waits to receive U1 Exit LFPS to complete the U1 Exit LFPS handshake.
8. The test fails if the LFPS handshake does not conform to the following specifications from section 6.9.2:

a. Between 300ns - 2us elapses between the start of the LVS U1 Exit LFPS and the start of the PUT U1 Exit LFPS.
b. The PUT U1 Exit LFPS duration is within 0.9us - 1.2us.
c. The PUT enters Recovery before tNoLFPSResponseTimeout deadline after the start of its U1 exit LFPS.
d. The PUT enters U0 before Ux_EXIT_TIMER deadline.

9. The test passes if all packets are successful, recovery is entered once, no extra packets or LFPS signals are received, and the PUT returns to U0.

# TD.7.24 Accepted Power Management Transaction for U2 Test (Upstream Port Only)

This test verifies that the PUT transitions to U2 if it receives an LGO_U2.

# Covered Assertions

7.2.4.1.1#7,9

7.2.4.2.1#4

7.2.4.2.2#2,3

7.2.4.2.3#2,8,9

79

USB 3.1 Link Layer Test Specification

Chapter 5: Test Descriptions

1/17/2018

7.2.4.2.7#2, 3
7.5.8.1#2
7.5.8.2#5
8.4.2#1

# Overview of Test Steps

1. Do steps 1 to 4 of the Link Initialization Sequence.
2. The LVS transmits the Set Link Function LMP with the Force_LinkPM_Accept bit asserted.
3. The LVS transmits an LGO_U2 and waits to receive an LAU from the PUT.
4. The test fails if the PUT does not transmit an LAU before PM_LC_TIMER deadline, or if recovery is entered.
5. The LVS transmits an LPMA and then transitions to U2.
6. The test fails if the PUT does not transition to U2 when the PM_ENTRY_TIMER expires, recovery is entered, or if the PUT sends any packet.
7. The LVS transmits the U2 Exit LFPS to transition to U0 and waits to receive U2 Exit LFPS to complete the U2 Exit LFPS handshake.
8. The test fails if the LFPS handshake does not conform to the following specifications from section 6.9.2:
  a. Between 300ns – 2ms elapses between the start of the LVS U2 Exit LFPS and the start of the PUT U2 Exit LFPS.
  b. The PUT U2 Exit LFPS duration is within 80us – 2ms.
  c. The PUT enters Recovery before tNoLFPSResponseTimeout deadline after the start of its U2 exit LFPS.
  d. The PUT enters U0 before Ux_EXIT_TIMER deadline
9. The test passes if all packets are successful, recovery is entered once, no extra packets or LFPS signals are received, and the PUT enters Recovery.

### TD.7.25 Accepted Power Management Transaction for U3 Test (Upstream Port Only)

This test verifies that the PUT transitions to U3 if it receives an LGO_U3.

# Covered Assertions

7.2.4.1.1#7,97.2.4.2.1#4
7.2.4.2.4#2,3,7
7.2.4.2.7#2,3
7.5.9.1#3
7.5.9.2#5

# Overview of Test Steps

1. Do steps 1 to 4 of the Link Initialization Sequence.
2. The LVS transmits an LGO_U3 and waits to receive an LAU from PUT.
3. The test fails if the PUT does not transmit an LAU before PM_LC_TIMER deadline, or if recovery is entered..

80

USB 3.1 Link Layer Test Specification

Chapter 5: Test Descriptions

1/17/2018

4. The LVS transmits an LPMA and then transitions to U3.
5. The test fails if the PUT does not transition to U3 when the PM_ENTRY_TIMER expires, if recovery is entered, or if the PUT sends any packet.
6. The LVS transmits the U3 Exit LFPS to transition to U0 and waits to receive U3 Exit LFPS to complete the U3 Exit LFPS handshake.
7. The test fails if the LFPS handshake does not conform to the following specifications from section 6.9.2:

a. Between 300ns - 10ms elapses between the start of the LVS U3 Exit LFPS and the start of the PUT U3 Exit LFPS.
b. The PUT U3 exit LFPS duration is within 80us - 10ms.
c. The PUT enters Recovery before tNoLFPSResponseTimeout deadline after the start of its U3 exit LFPS.

8. The test passes if all packets are successful, recovery is entered once, no extra packets or LFPS signals are received, and the PUT enters Recovery.

### TD.7.26 Transition to U0 from Recovery Test

This test verifies that the PUT transitions to U0 when it is in Recovery.

#### Covered Assertions

7.2.4.1.1#3,4,7,9
7.3.6#17.5.10.3.1#1
7.5.10.3.2#1
7.5.10.4.2#1
7.5.10.5.1#1
7.5.10.5.2#1

#### Overview of Test Steps

1. Both the LVS and the PUT go through the initial steps of the LTSSM to reach U0.
2. The LVS does not transmit the Header Sequence Advertisement and the Rx Header Buffer Credit Advertisement or Type 1 and Type 2 Rx Header Buffer Credit Advertisements. The PUT will then transition to Recovery because the PENDING_HP_TIMER will time out.
3. The test fails if the PUT transitions to Recovery before PENDING_HP_TIMER deadline or it does not transition to Recovery when the PENDING_HP_TIMER expires.
4. The test fails if any of the following occur:

a. The PUT does not transmit TS1 ordered sets.
b. The PUT transmits TS2s before the LVS sends eight consecutive and identical TS1s or TS2s.
c. The PUT interrupts a TS1 ordered set to transmit a SKP or SYNC (for Gen 2 only) Ordered Set (between TS1 ordered sets is OK).
d. The PUT transmits Idle Symbols or any other Packet.
e. The PUT continues to transmit TS1 ordered sets after tRecoveryActiveTimeout expires.

5. The LVS transmits TS2 ordered sets and readies to complete the Recovery.Configuration handshake.
6. The test fails if any of the following occur:

81

USB 3.1 Link Layer Test Specification

Chapter 5: Test Descriptions

1/17/2018

a. The PUT does not transmit at least sixteen consecutive TS2 ordered sets after receiving one TS2 ordered set.
b. The PUT sends Idle symbols before the LVS sends at least eight consecutive TS2 ordered sets.
c. The PUT interrupts transmission of a TS2 ordered set to transmit a SKP or SYNC (for Gen 2 only) ordered set (between TS2 ordered sets is OK).
d. The PUT continues to transmit TS2 ordered sets after tRecoveryConfigurationTimeout expires.

7. The LVS transmits Idle symbols. In Gen 2 operation the LVS transmits a single SDS Ordered Set and then data blocks with Idle Symbols.
8. The test fails if upon entering U0, the PUT does not transmit the Header Sequence Number Advertisement and the Rx Header Buffer Credit Advertisement or Type 1 and Type 2 Rx Header Buffer Credit Advertisement before their respective timeouts, PENDING_HP_TIMER and (Type 1 and Type 2) CREDIT_HP_TIMER, expire.
9. The LVS and PUT continue the test with the Link Initialization Sequence starting at step two.

### TD.7.27 Hot Reset Detection in Polling Test (Upstream Port Only)

This test verifies that the PUT detects the Hot Reset in Polling.

#### Covered Assertions

7.2.4.1.1#6,8,17,22

7.4.2#4

7.5.4.7.2#4

7.5.12.3.1#1,3,4

7.5.12.3.2#1

7.5.12.4.1#1

7.5.12.4.2#1

#### Overview of Test Steps

1. Both LVS and PUT detect each other and then transition through Polling to Polling.RxEQ.
2. Both LVS and PUT transmit the TS1 ordered sets during Polling.Active.
3. The LVS waits to receive TS2 ordered sets.
4. The test fails if the PUT does not transmit TS2s before tPollingActiveTimeout expires.
5. The LVS initiates a Hot Reset and transmits TS2 ordered sets with the Reset bit asserted.
6. The test fails if the PUT does not transmit at least sixteen TS2 ordered sets with the Reset bit asserted followed by two consecutive TS2 ordered sets with the Reset bit de-asserted.
7. The LVS transmits four consecutive TS2 ordered sets with the Reset bit de-asserted, and then transmits Idle Symbols for Gen 1, or an SDS Ordered Set followed by Idle Symbols for Gen 2.
8. The test fails if upon entering U0, the PUT does not transmit the Header Sequence Number Advertisement and the (Type 1 / Type 2) Rx Header Buffer Credit Advertisement before their respective timeouts, PENDING_HP_TIMER and (Type 1 / Type 2) CREDIT_HP_TIMER, expire.
9. The LVS and PUT exchange Port Configuration transactions.

82

USB 3.1 Link Layer Test Specification

Chapter 5: Test Descriptions

1/17/2018

10. The LVS will keep the link active by sending Link Pollings (LUP when it is configured as an Upstream Port or LDN when it is configured as a Downstream Port) for 50ms.
11. The test fails if the Port Configuration exchange sequences are not successful or the link does not stay in U0 for at least 50ms.

### TD.7.28 Hot Reset Detection in U0 Test (Upstream Port Only)

This test verifies that the PUT detects the Hot Reset in U0 and does not start the Port Configuration Sequences.

# Covered Assertions

7.2.4.1.1#6,8,17,22

7.4.2#2,4

7.5.10.4.1#1

7.5.12.3.1#1,2

7.5.12.3.2#1

7.5.12.4.1#1

7.5.12.4.2#1

# Overview of Test Steps

1. Do steps 1 to 5 of the Link Initialization Sequence.
2. The LVS transmits TS1 ordered set to transition to Recovery.
3. The LVS waits to receive TS1 ordered sets.
4. The test fails if the PUT does not transmit TS1s before tU0RecoveryTimeout expires.
5. The LVS initiates a Hot Reset by transmitting TS2 ordered sets with the Reset bit asserted.
6. The test fails if the PUT does not transmit at least sixteen TS2 ordered sets with the Reset bit asserted followed by two consecutive TS2 ordered sets with the Reset bit de-asserted.
7. The LVS transmits four consecutive TS2 ordered sets with the Reset bit de-asserted, and then transmits Idle Symbols for Gen 1, or SDS Ordered Set followed by Idle Symbols for Gen 2.
8. The test fails if upon entering U0, the PUT does not transmit the Header Sequence Number Advertisement and the (Type 1/Type 2) Rx Header Buffer Credit Advertisement before their respective timeouts, PENDING_HP_TIMER and (Type 1/Type 2) CREDIT_HP_TIMER, expire.
9. The LVS will keep the link active by sending Link Pollings (LUP when it is configured as an Upstream Port or LDN when it is configured as a Downstream Port) for 50ms.
10. The test fails if the PUT retransmits Port Capability or Port Configuration LMPs.
11. The test fails if the Port Configuration exchange sequences are not successful and the link does not stay in U0 for at least 50ms.

### TD.7.29 Hot Reset Initiation in U0 Test (Downstream Port Only)

This test verifies that the PUT initiates Hot Reset in U0.

83

USB 3.1 Link Layer Test Specification

Chapter 5: Test Descriptions

1/17/2018

# Covered Assertions

7.2.4.1.1#6,8,17,22

7.4.2#2,4,10

7.5.4.6.1#1

7.5.4.7.2#3

7.5.10.4.1#1

7.5.12.3.1#1,2

7.5.12.3.2#1

7.5.12.4.1#1

7.5.12.4.2#1

# Overview of Test Steps

1. Do steps 1 to 5 of the Link Initialization Sequence.
2. The LVS prompts the test operator to initiate a Hot Reset on the PUT through USB30CV.
3. The LVS waits for the PUT to send TS1s.
4. The test fails if the PUT does not transmit TS1s before tU0RecoveryTimeout expires.
5. The LVS transmits TS1 ordered sets and waits to receive TS2 ordered sets with the Reset bit asserted.
6. The test fails if the PUT does not transmit at least sixteen TS2 ordered sets with Reset bit asserted.
7. The LVS transmits at least sixteen TS2 ordered sets with the Reset bit asserted, and then transmits two consecutive TS2 ordered sets with the Reset bit de-asserted.
8. The test fails if any of the following occur:
  a. After LVS transmitted TS2 ordered sets with Reset bit de-asserted, the PUT does not transmit four consecutive TS2 ordered sets with the Reset bit de-asserted, when tHotResetActiveTimeout expires
  b. The PUT transmits anything other than TS2 ordered sets, before the LVS transmits TS2 ordered sets with the Reset bit de-asserted.
9. The LVS transmits Idle Symbols for Gen 1, or SDS Ordered Set followed by Idle Symbols for Gen 2.
10. The test fails if upon entering U0, the PUT does not transmit the Header Sequence Number Advertisement and the (Type 1/Type 2) Rx Header Buffer Credit Advertisement before their respective timeouts, PENDING_HP_TIMER and (Type 1/Type 2) CREDIT_HP_TIMER, expire.
11. The LVS will keep the link active by sending Link Pollings (LUP when it is configured as an Upstream Port or LDN when it is configured as a Downstream Port) for 50ms.
12. The test fails if the PUT retransmits Port Capability or Port Configuration LMPs.
13. The test fails if the Port Configuration exchange sequences are not successful and the link does not stay in U0 for at least 50ms.

### TD.7.30 Recovery on three consecutive failed RX Header Packets Test

This test verifies that the PUT will enter Recovery if it fails to receive a header packet three consecutive times.

# Covered Assertions

7.2.4.1.1#7,9

84

USB 3.1 Link Layer Test Specification

Chapter 5: Test Descriptions

1/17/2018

7.2.4.1.4#5

7.5.10.3.1#1

7.5.10.3.2#1

7.5.10.4.2#1

7.5.10.5.1#1

7.5.10.5.2#1

# Overview of Test Steps

1. Do steps 1 to 3 of the Link Initialization Sequence.

Note: LVS completes each step in a timely manner so as to not contribute to a tPortConfiguration timeout during steps 1-5.

2. The LVS and the PUT will exchange Port Configuration transactions, but the first packet sent by the LVS will have an invalid CRC-5.

a. LVS waits for the PUT's Port Capability LMP.
b. LVS verifies that the Port Capability LMP is valid.
c. LVS transmits its Port Capability LMP with an invalid CRC-5.
d. LVS verifies that the PUT replies with an LBAD.
e. LVS transmits an LRTY and then retransmits the packet with an invalid CRC-5.
f. LVS verifies that the PUT replies with an LBAD.
g. LVS transmits an LRTY and then retransmits the packet with an invalid CRC-5.
h. LVS verifies that the PUT initiates Recovery.

3. The test fails if any of the following occur:

a. The PUT does not reply with LBAD to the first two packets (which have invalid CRC-5s)
b. The PUT does not initiate Recovery in step g within tRecoveryTransition.
c. The PUT initiates Recovery before the third invalid packet is received.

4. The LVS and PUT transition through Recovery to U0.

5. The LVS and the PUT perform the Link Initialization Sequence and exchange all remaining Port Configuration transactions.
6. The test fails if the PUT retransmits its Port Capability LMP.
7. The LVS will keep the link active by sending Link Pollings (LUP when it is configured as an Upstream Port or LDN when it is configured as a Downstream Port) for 50ms.
8. The test passes if the exchanges are successful, no timeout is detected, recovery is entered once, all packets are successfully received by the PUT except for the packet with invalid CRC-5, all credits are restored and the link stays in U0 for at least 50ms.

# TD.7.31 Hot Reset Failure Test (Downstream Port Only)

This test verifies that the PUT initiates a Warm Reset when Hot Reset training fails.

# Covered Assertions

7.4.2#6,8,14

85

USB 3.1 Link Layer Test Specification

Chapter 5: Test Descriptions

1/17/2018

7.5.3.3.1#1

7.5.10.3.2#5

10.3.1.6#6

# Overview of Test Steps

1. Perform the Link Initialization Sequence to bring the LVS and PUT link to U0.
2. The LVS software prompts the test operator to initiate a Hot Reset on the PUT through USB30CV.
3. The LVS waits for the PUT to send TS1s.
4. The test fails if the TS1 Ordered Sets have the Reset bit set.
5. The LVS does not transmit anything in response to the PUT.
6. The test fails if the PUT does not transmit a Warm Reset LFPS after tRecoveryActiveTimeout expires.
7. The LVS responds to the Warm Reset LFPS by entering Rx.Detect.
8. The LVS and PUT perform the Link Initialization Sequence to bring the link to U0.
9. The LVS will keep the link active by sending Link Pollings (LUP when it is configured as an Upstream Port or LDN when it is configured as a Downstream Port) for 50ms.
10. The test passes if the exchanges are successful, the PUT initiates a Warm Reset LFPS after tRecoveryActiveTimeout in Recovery.Active and the link reaches U0 with a correct Port Configuration Transaction and stays there for at least 50ms.

# TD.7.32 Warm Reset Rx.Detect Timeout Test (Hub Downstream Port Only)

This test has been deleted. The assert has been covered in TD 10.109.

# TD.7.33 Exit Compliance Mode Test (Upstream Port Only)

This test verifies that a device exits Compliance Mode when it receives a Warm Reset LFPS.

# Covered Assertions

7.4.2#9

7.5.4.3.2#1

7.5.5.1#2

7.5.5.2#2

# Overview of Test Steps

1. The LVS makes sure VBUS is off to assure a PowerOn Reset.
2. The LVS prompts the test operator to power cycle a self-powered device.
3. The LVS turns on VBUS, bringing the link to Rx.Detect.
4. The LVS presents Terminations and waits for the PUT to present Terminations.
5. When the LVS detects Terminations from the PUT, the LVS starts a timer for tPollingLFPSTimeout and does not transmit an LFPS.

86

USB 3.1 Link Layer Test Specification

Chapter 5: Test Descriptions

1/17/2018

6. When the timer expires, the LVS verifies that the device is in Compliance Mode by sending Ping.LFPS until it can verify that the LVS is receiving a Compliance Pattern, (at most by the COMs in the 4th Compliance Pattern).
7. The test fails if the LVS cannot verify a Compliance Pattern coming from the PUT.
8. The LVS transmits a Reset.LFPS and enters Rx.Detect.
9. The LVS and PUT perform the Link Initialization Sequence to bring the LVS and PUT link to U0.
10. The LVS will keep the link active by sending Link Pollings (LUP when it is configured as an Upstream Port or LDN when it is configured as a Downstream Port) for 50ms.
11. The test passes if all exchanges are successful and the PUT stays in U0 for 50ms.

### TD.7.34 Exit Compliance Mode Test (Downstream Port Only)

This test verifies that a downstream port instructed to Reset while in Compliance Mode initiates a Warm Reset.

### Covered Assertions

7.4.2#9

7.5.4.3.2#2

7.5.5.1#2

7.5.5.2#1

### Overview of Test Steps

1. The LVS prompts the test operator to enable Compliance Mode through USB30CV. CV will send SetPortFeature(PORT_LINK_STATE) = Compliance Mode for the PUT.
2. The LVS presents termination to the PUT.
3. When the LVS detects VBUS and Terminations from the PUT, the LVS starts a timer for tPollingLFPSTimeout and does not transmit an LFPS.
4. When the timer expires, the LVS verifies that the device is in Compliance Mode by sending Ping.LFPS until it can verify that the LVS is receiving a Compliance Pattern, (at most by the COMs in the 4th Compliance Pattern).
5. The test fails if the LVS cannot verify a Compliance Pattern coming from the PUT.
6. The LVS prompts the test operator to Reset the PUT through USB30CV and then hit "OK".
7. The LVS waits to receive a Warm Reset LFPS from PUT.
8. The test fails if the LVS does not receive a Warm Reset LFPS before the test operator hits "OK"
9. The LVS closes the prompt automatically when it receives a Warm Reset LFPS.
10. The LVS transitions to Rx.Detect.Reset for the duration of the Warm Reset LFPS.
11. The LVS transitions to Rx.Detect and the LVS and PUT transition through Polling to U0.
12. The LVS will keep the link active by sending Link Pollings (LUP when it is configured as an Upstream Port or LDN when it is configured as a Downstream Port) for 50ms.
13. The test passes after the Port Configuration exchange is successful and the link stays in U0 for 50ms.

87

USB 3.1 Link Layer Test Specification

Chapter 5: Test Descriptions

1/17/2018

### TD.7.35 Exit U3 by Reset Test (Downstream Port Only)

This test verifies that a downstream port instructed to Reset during U3 initiates a Warm Reset.

# Covered Assertions

7.2.4.2.4#1,4,5

7.5.9.2#2

# Overview of Test Steps

1. Perform the Link Initialization Sequence to bring the LVS and PUT link to U0.
2. The LVS software prompts the test operator to Suspend the PUT to U3 through USB30CV.
3. The LVS waits to receive an LGO_U3 from the PUT.
4. The LVS sends an LAU when it receives an LGO_U3 from the PUT.
5. The LVS waits to receive an LPMA from the PUT.
6. The test fails if any of the following occur:

a. The LVS does not receive an LGO_U3
b. The LVS does not receive an LPMA before PM_ENTRY_TIMER deadline.
c. The PUT fails to transition to U3 after PM_ENTRY_TIMER expires.

7. The LVS prompts the test operator to Reset the PUT through USB30CV and then hit "OK" on the prompt.
8. The LVS waits to receive a Warm Reset LFPS from PUT.
9. The test fails if no Warm Reset LFPS is received by the LVS before the test operator hits "OK".
10. When the LVS receives a Warm Reset LFPS the prompt is closed automatically.
11. The LVS transitions to Rx.Detect.Reset for the duration of the Warm Reset LFPS.
12. The LVS transitions to Rx.Detect and the LVS and PUT transition through Polling to U0.
13. The LVS will keep the link active by sending Link Pollings (LUP when it is configured as an Upstream Port or LDN when it is configured as a Downstream Port) for 50ms.
14. The test passes after the Port Configuration exchange is successful and the link stays in U0 for 50ms.

### TD.7.36 Exit U3 Test (Host Downstream Port Only)

This test verifies that a downstream port initiates U3 exit with a U3 exit LFPS.

Note: This test is performed on host silicon only. This test is not performed on end products. The operator must install the Product-Specific host controller driver to perform this test. It cannot be tested with the Compliance driver. The LVS is configured to appear to the host controller as a device.

# Covered Assertions

7.2.4.2.4#1,4,5

7.2.4.2.7#1

7.5.9.1#4

7.5.9.2#5

88

USB 3.1 Link Layer Test Specification

Chapter 5: Test Descriptions

1/17/2018

# Overview of Test Steps

1. Perform the Link Initialization Sequence to bring the LVS and PUT link to U0. The PUT host controller machine enumerates the LVS.
2. The LVS software prompts the test operator to put the PUT host controller machine to sleep or, if the DUT is an Embedded Host and power is lost to the host during sleep, to U3.
3. The LVS waits to receive an LGO_U3 from the PUT.
4. The LVS sends an LAU when it receives an LGO_U3 from the PUT.
5. The LVS waits to receive an LPMA from the PUT.
6. The test fails if any of the following occur:

a. The LVS does not receive an LGO_U3
b. The LVS does not receive an LPMA before PM_ENTRY_TIMER deadline.

7. The LVS prompts the test operator to verify that the host controller machine is in a sleep state.
8. The LVS prompts the test operator to wake the host controller machine.
9. The LVS waits to receive a U3 Exit LFPS from PUT.
10. The test fails if no U3 Exit LFPS is received.
11. The LVS sends a U3 Exit LFPS 5ms after detecting an LFPS from the PUT.
12. The LVS and PUT transition through Recovery to U0.
13. The LVS will keep the link active by sending Link Pollings (LUP when it is configured as an Upstream Port or LDN when it is configured as a Downstream Port) for 50ms.

# TD.7.37 Packet Pending Test (Upstream Port Only)

This test verifies that the PUT releases its Packet Pending flag at the end of a Control Transfer.

# Covered Assertions

8.6#1

# Overview of Test Steps

1. Perform the Link Initialization Sequence to bring the LVS and PUT link to U0. The LVS enumerates the PUT to a configured state.
2. If the PUT is an US port of a hub, the LVS issues a SetPortFeature(PLS=4) for each DS port on the hub.
3. The LVS software issues a GetDescriptor request SETUP packet, with the PP bit set to 1.
4. The LVS sends an ACK TP, with the PP bit set to 1, to start the IN stage of the GetDescriptor request.
5. The LVS waits to receive IN data from the PUT.
6. The LVS software issues a GetDescriptor STATUS packet, with a PP bit set to 0.
7. The LVS waits to receive ACK TP from the PUT, concluding the GetDescriptor request.
8. The test fails if the GetDescriptor request is not completed.
9. The LVS sends an LGO_U1 and waits to receive LAU from the PUT.
10. The test fails if the PUT does not send an LAU.

89

USB 3.1 Link Layer Test Specification

Chapter 5: Test Descriptions

1/17/2018

11. The LVS transmits an LPMA and then transitions to U1.
12. The test fails if the PUT does not transition to U1, or if the PUT sends any packet.

### TD.7.38 Port Capability Tiebreaker Test

This test verifies that the PUT accepts ports capable of both US and DS operation, and that a PUT capable of both US and DS operation resends its Port Capability info with a randomly generated tiebreaker after the first tiebreaker is the same value as its link partner's.

### Covered Assertions

TBD

### Overview of Test Steps

1. Perform steps 1 through 3 of the Link Initialization Sequence.
2. The LVS waits to receive the Port Capability LMP.
3. The test fails if the Port Capability LMP received is not valid.
4. If the LVS is configured as a Downstream Port:
  a. The LVS sends a Port Capability LMP indicating it is capable of both US and DS operation.
  b. The test continues at step 4.d. of the Link Initialization Sequence.

5. If the LVS is configured as an Upstream Port:

a. If the Port Capability LMP from the PUT indicates that the port only supports DS operation:
  i. The LVS sends a Port Capability LMP indicating it is capable of both US and DS operations.
  ii. The test continues at step 4.d of the Link Initialization Sequence.
b. If the Port Capability LMP from the PUT indicates that the port supports both US and DS operation:
  i. The test continues at step 6 of this test.

6. The LVS records the tiebreaker value on the received LMP as X, and initializes a counter to 1.

7. The LVS sends a Port Capability LMP with DS and US capability set to 1, and its tiebreaker value set to X.

8. The LVS waits to receive another Port Capability LMP.

a. The test fails if the LVS does not receive another Port Capability LMP within tPortConfigurationTimeout.
b. If the tiebreaker value is X and the counter value is less than 5:
  i. Increment the counter.
  ii. Go to step 7.
c. The test fails if the tiebreaker value is X and the counter value is 5.
d. If the tiebreaker value is not X, move to step 9.

9. The LVS sends a Port Capability LMP with DS and US capability set to 1, and its tiebreaker value set higher than the tiebreaker value on the received LMP.

10. Perform the Link Initialization Sequence starting at step 4.d with the LVS as a Downstream Port

90

USB 3.1 Link Layer Test Specification

Chapter 5: Test Descriptions

1/17/2018

11. The test fails if the PUT does not stay in U0 for 50ms.
12. If the PUT includes a captive re-timer:

a. For a DFP:

i. Use USBCV31 Link Layer helper TD 7.18 to initiate an entry to LGO_U1
ii. The test fails if the LVS does not receive an LGO_U1
iii. The LVS sends an LAU and enters U1 after receiving LPMA or PM_ENTRY_TIMER timeout
iv. The test fails if the LVS receives TS1s
v. Wait 1 second
vi. The test fails if the LVS does not receive Ping.LFPSs after 300ms with tBurst and tRepeat as defined in Table 6-30.

b. For a UFP:

i. The LVS sends LGO_U1
ii. The test fails if the LVS does not receive an LAU
iii. The LVS sends an LPMA and enters U1
iv. The test fails if the LVS receives TS1s.
v. Wait 1 second
vi. The test fails if the LVS receives any LFPS

### TD.7.39 PortMatch Retry Test (Gen 2 Only)

This test verifies that the PUT recovers to Polling.PortMatch when the tPollingActiveTimeout expires.

#### Covered Assertions

7.5.4.5.2#2

7.3.10#1

#### Overview of Test Steps

1. Both LVS and PUT detect each other and then transition through Polling to Polling.RxEQ.
2. The LVS does not transmit the TS1 ordered sets during Polling.Active.
3. The test fails if:

a) The PUT does not transition to Polling.PortMatch after tPollingActiveTimeout.
b) The PUT does not transmit the next highest PHY Capability from its previous PHY Capability in its PHY Capability LBPMs.

4. Both LVS and PUT transition through Polling.RxEQ
5. If the PHY Capability was not negotiated to 5Gbps, return to step 2.
6. Both LVS and PUT transmit the TS1 ordered sets during Polling.Active and proceed to U0.
7. The LVS will keep the link active by sending Link Pollings (LUP when it is configured as an Upstream Port or LDN when it is configured as a Downstream Port) for 50ms.

91

USB 3.1 Link Layer Test Specification

Chapter 5: Test Descriptions

1/17/2018

8. The test fails if the Port Configuration exchange sequences are not successful or the link does not stay in U0 for at least 50ms.

### TD.7.40 Polling Retry Test (Downstream Port Only)

This test verifies that the PUT recovers to Rx.Detect twice, and then eSS.Inactive when tPollingLFPSTimeout expires.

#### Covered Assertions

7.3.10#2,3

7.5.4.2#2

7.5.4.3.2#6,7

7.5.4.8.2#3,4

7.5.4.9.2#3

#### Overview of Test Steps

1. The LVS presents terminations and does not send any signal for the remainder of the test.
2. The test fails if the PUT does not transition to Polling.LFPS within 200ms.
3. For a PUT with a captive re-timer:

(1) The test fails if the PUT does not transition to Rx.Detect after 24 ms.
(2) The test fails if the PUT does not transition to Polling.LFPS within 8ms.
(3) The test fails if the PUT does not continue this cycle up to tPollingLFPSTimeout expiration.

4. The test fails if the PUT does not transition to Rx.Detect within tPollingLFPSTimeout expiration.
5. The test fails if the PUT does not transition to Polling.LFPS within 200ms.
6. For a PUT with a captive re-timer:

(1) The test fails if the PUT does not transition to Rx.Detect after 24 ms.
(2) The test fails if the PUT does not transition to Polling.LFPS within 8ms.
(3) The test fails if the PUT does not continue this cycle up to tPollingLFPSTimeout expiration.

7. The test fails if the PUT does not transition to Rx.Detect within tPollingLFPSTimeout expiration.
8. The test fails if the PUT does not transition to Polling.LFPS within 200ms.
9. For a PUT with a captive re-timer:

(1) The test fails if the PUT does not transition to Rx.Detect after 24 ms.
(2) The test fails if the PUT does not transition to Polling.LFPS within 8ms.
(3) The test fails if the PUT does not continue this cycle up to tPollingLFPSTimeout expiration.

10. The test fails if the PUT does not transition to eSS.Inactive within tPollingLFPSTimeout expiration.
11. If PUT is Gen 1, continue with the rest of the test steps.
12. The LVS removes terms for 200ms and presents terms.
13. The LVS and PUT transition through Polling.LFPS to Polling.Active.

92

USB 3.1 Link Layer Test Specification

Chapter 5: Test Descriptions

1/17/2018

14. The LVS does not transmit the TS1 ordered sets during Polling.Active.
15. The test fails if the PUT does not transition to Rx.Detect after tPollingActiveTimeout.
16. The LVS and PUT transition through Polling.LFPS to Polling.Configuration.
17. The LVS does not transmit the TS2 ordered sets during Polling.Configuration.
18. The test fails if the PUT does not transition to Rx.Detect after tPollingConfigurationTimeout.
19. The LVS and PUT transition through Polling.LFPS to Polling.Active.
20. The LVS does not transmit the TS1 ordered sets during Polling.Active.
21. The test fails if the PUT does not transition to eSS.Inactive after tPollingActiveTimeout.

### TD.7.41 SetAddress TPF Bit Test (Gen 2 Upstream Port Only)

This test verifies that the PUT sets the TPF bit at the end of a SetAddress Control Transfer.

#### Covered Assertions

8.5.6.7#2

#### Overview of Test Steps

1. Perform the Link Initialization Sequence to bring the LVS and PUT link to U0.
2. The LVS sends a SetAddress command to the PUT.
3. The test fails if:

a. The SetAddress control transfer does not complete.
b. The ACK response to the STATUS packet of the control transfer does not have the TPF bit set to 1.

### TD.7.42 Symbol to Block Alignment Test (Gen 2 Only)

Condition to be tested:

A. Start every Packet in the 0th symbol of a block.
B. Start every Packet in the 1st symbol of a block.
C. Start every Packet in the 2nd symbol of a block.
D. Start every Packet in the 3rd symbol of a block.
E. Start every Packet in the 4th symbol of a block.
F. Start every Packet in the 5th symbol of a block.
G. Start every Packet in the 6th symbol of a block.
H. Start every Packet in the 7th symbol of a block.
I. Start every Packet in the 8th symbol of a block.
J. Start every Packet in the 9th symbol of a block.
K. Start every Packet in the 10th symbol of a block.
L. Start every Packet in the 11th symbol of a block.
M. Start every Packet in the 12th symbol of a block.
N. Start every Packet in the 13th symbol of a block.
O. Start every Packet in the 14th symbol of a block.
P. Start every Packet in the 15th symbol of a block.

93

USB 3.1 Link Layer Test Specification

Chapter 5: Test Descriptions

1/17/2018

# Covered Assertions

7.2.1.3#1,2

# Overview of Test Steps

5. Do steps 1 to 4 of the Link Initialization Sequence.
6. The LVS will keep the link active by sending Link Pollings (LUP when it is configured as an Upstream Port or LDN when it is configured as a Downstream Port) for 50ms. All data blocks will be generated according to Condition A described above.
7. At this stage the Downstream Port is expected to issue a GetDeviceDescriptor request.

a. If the LVS is configured as an Upstream Port:

i. The LVS prompts the test operator to have the PUT send a GetDeviceDescriptor request through USB30CV and then press “OK”.
ii. The test fails if no GetDeviceDescriptor request is received and the test operator has pressed “OK”.
iii. When the LVS receives a GetDeviceDescriptor request, it closes the prompt, and responds to the request as appropriate.

b. If the LVS is configured as a Downstream Port, it will issue a GetDeviceDescriptor request, and complete the transaction as appropriate.

8. The test passes if the exchanges are successful, no timeout is detected, no recovery is entered, all packets are successfully received, all credits are restored and the link stays in U0 for at least 50ms.

9. Repeat the steps with the next combination listed above.

94

USB 3.1 Link Layer Test Specification