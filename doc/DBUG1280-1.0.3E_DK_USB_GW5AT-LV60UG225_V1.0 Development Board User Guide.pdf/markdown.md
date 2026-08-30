![img-0.jpeg](img-0.jpeg)

DK_USB_GW5AT-LV60UG225_V1.0

## User Guide

DBUG1280-1.0.3E, 03/13/2026

Copyright © 2026 Guangdong Gowin Semiconductor Corporation. All Rights Reserved.

![Gowin Semiconductor logo]() is the trademark of Guangdong Gowin Semiconductor Corporation and is registered in China, the U.S. Patent and Trademark Office, and other countries. All other words and logos identified as trademarks or service marks are the property of their respective holders. No part of this document may be reproduced or transmitted in any form or by any means, electronic, mechanical, photocopying, recording or otherwise, without the prior written consent of GOWINSEMI.

### **Disclaimer**

GOWINSEMI assumes no liability and provides no warranty (either expressed or implied) and is not responsible for any damage incurred to your hardware, software, data, or property resulting from usage of the materials or intellectual property except as outlined in the GOWINSEMI Terms and Conditions of Sale. GOWINSEMI may make changes to this document at any time without prior notice. Anyone relying on this documentation should contact GOWINSEMI for the current documentation and errata.

Revision History

[tbl-0.md](tbl-0.md)

Contents

# Contents

[tbl-1.md](tbl-1.md)

DBUG1280-1.0.3E

i

Contents

3.4.1 Introduction ... 9
3.4.2 Pin Distribution... 10
3.5 DDR3 ... 10
3.5.1 Introduction ... 10
3.5.2 Pin Distribution... 11
3.6 HDMI-RX Interface ... 13
3.6.1 Introduction ... 13
3.6.2 Pin Distribution... 13
3.7 MIPI Interface ... 14
3.7.1 Introduction ... 14
3.7.2 Pin Distribution... 15
3.8 I2C Interface ... 18
3.8.1 Introduction ... 18
3.8.2 Pin Distribution... 18
3.9 Key & LED ... 18
3.9.1 Introduction ... 18
3.9.2 Pin Distribution... 19
3.10 Type-C Interface ... 20
3.10.1 Introduction ... 20
3.10.2 Pin Distribution... 21
3.11 SDI Interface ... 22
3.11.1 Introduction ... 22
3.11.2 Pin Distribution... 22

DBUG1280-1.0.3E

ii

List of Figures

# List of Figures

Figure 2-1 DK_USB_GW5AT-LV60UG225_V1.0 Development Board ... 3
Figure 2-2 A Development Board Kit ... 4
Figure 2-3 PCB Components... 5
Figure 2-4 System Block Diagram ... 5
Figure 3-1 Power Distribution Diagram ... 8
Figure 3-2 Connection Diagram of Download ... 9
Figure 3-3 Clock Connection Diagram ... 10
Figure 3-4 Hardware Connection Diagram of DDR3... 11
Figure 3-5 Connection Diagram of HDMI-RX Interface... 13
Figure 3-6 Connection Diagram of MIPI CPHY & DPHY Hard Core Interfaces ... 14
Figure 3-7 Connection Diagram of I2C Interface... 18
Figure 3-8 Connection Diagram of Key ... 19
Figure 3-9 Connection Diagram of LED ... 19
Figure 3-10 Connection Diagram of Type-C Interface... 20
Figure 3-11 Connection Diagram of SDI Interface... 22

DBUG1280-1.0.3E

iii

List of Tables

# List of Tables

Table 1-1 Terminology and Abbreviations...2
Table 3-1 JTAG Pin Distribution...9
Table 3-2 Clock Pin Distribution...10
Table 3-3 DDR3 Configuration...10
Table 3-4 DDR3 Pin Distribution...11
Table 3-5 Pin Distribution of DP-RX Interface...13
Table 3-6 Pin Distribution of MIPI CPHY & DPHY Hard core Interface...15
Table 3-7 J21 Pin Distribution of I2C Interface...18
Table 3-8 Pin Distribution of Key...19
Table 3-9 Pin Distribution of LED...19
Table 3-10 Pin Distribution of Type-C Interface...21
Table 3-11 Pin Distribution of SDI Interface...22

DBUG1280-1.0.3E

iv

1 About This Guide

1.1 Purpose

# 1 About This Guide

## 1.1 Purpose

The DK_USB_GW5AT-LV60UG225_V1.0 development board (hereinafter referred to as “the development board”) user guide consists of following three parts:

- A brief introduction to the features of the development board.
- An introduction to the development board system architecture and hardware resources.
- An introduction to the hardware circuits, functions and pin distribution.

## 1.2 Related Documents

The latest user guides are available on the GOWINSEMI Website. You can find the related documents at www.gowinsemi.com:

- DS981, GW5AT series of FPGA Products Data Sheet
- UG1222, GW5AT-60 Pinout
- UG983, GW5AT series of FPGA Products Package and Pinout User Guide
- UG718, Arora V 60K FPGA Products Programming and Configuration User Guide

DBUG1280-1.0.3E

1(23)

1 About This Guide

1.3 Terminology and Abbreviations

### 1.3 Terminology and Abbreviations

The terminology and abbreviations used in this manual are as shown in Table 1-1.

Table 1-1 Terminology and Abbreviations

[tbl-2.md](tbl-2.md)

### 1.4 Support and Feedback

Gowin Semiconductor provides customers with comprehensive technical support. If you have any questions, comments, or suggestions, please feel free to contact us directly using the information provided below.

Website: www.gowinsemi.com

E-mail: support@gowinsemi.com

DBUG1280-1.0.3E

2(23)

2 Development Board Introduction

2.1 Overview

# 2 Development Board Introduction

## 2.1 Overview

Figure 2-1 DK_USB_GW5AT-LV60UG225_V1.0 Development Board

![img-1.jpeg](img-1.jpeg)

Gowin GW5AT series of FPGA products are the 5 series products of Arora family, with abundant internal resources, high-performance DSP with a new architecture that supports AI operations, high-speed LVDS interface and abundant BSRAM resources. At the same time, it supports self-developed DDR3 and SerDes supporting multiple protocols and provides a variety of packages. It is suitable for applications such as low power, high

DBUG1280-1.0.3E

3(23)

2 Development Board Introduction

2.2 A Development Board Kit

performance and compatibility design.

DK_USB_GW5AT-LV60UG225_V1.0 development board applies to DDR3 high-speed storage, SDI and MIPI high-speed communication, integrates SDI-IN, SDI-OUT, MIPI CPHY, MIPI DPHY, HDMI, Type-C interfaces, supporting FPGA's MIPI C-PHY, MIPI D-PHY, USB 3.0, and 3G/6G SDI function evaluation, hardware verification, and software learning and debugging, etc.

The development board adopts Gowin GW5AT-LV60UG225 FPGA device. For the internal resources of the chip, see DS981, GW5AT series of FPGA Products Data Sheet.

## 2.2 A Development Board Kit

The development board kit includes the following items:

1. DK_USB_GW5AT-LV60UG225_V1.0 development board
2. 12V power (Input: AC 100-240V~50/60Hz 0.6A, output: DC12V 2A)
3. Mini USB-B Cable

Figure 2-2 A Development Board Kit

![img-2.jpeg](img-2.jpeg)

![img-3.jpeg](img-3.jpeg)

① DK_USB_GW5AT-LV60UG225_V1.0 development board
② 12V power supply adapter
③ Mini USB-B Cable

DBUG1280-1.0.3E

4(23)

2 Development Board Introduction

2.3 PCB Components

## 2.3 PCB Components

Figure 2-3 PCB Components

![img-4.jpeg](img-4.jpeg)

## 2.4 System Block Diagram

Figure 2-4 System Block Diagram

![img-5.jpeg](img-5.jpeg)

DBUG1280-1.0.3E

5(23)

2 Development Board Introduction

2.5 Features

## 2.5 Features

The key features are as follows:

● FPGA Device

- Gowin GW5AT-LV60UG225 FPGA

● Download and Boot

- Integrate USB download circuit on the development board, download through Mini USB-B interface
- External SPI Flash for storing FPGA configuration file

● Power

- External DC12V/2A Power
- The Power light is on after power on.
- The board generates 5V, 3.3V, 2.5V, 1.8V, 1.5V, 1.2V, 0.9V, 0.75V power.

● Clock System

- One 24MHz clock
- One 148.5MHz clock
- Two 200MHz clocks

● Memory Device

- 2Gbit DDR3 SDRAM
- 128Mbit NOR Flash

● HDMI Interface

- One HDMI-RX interface

● MIPI Interface

- One CPHY hard core interface, including 3lane
- One DPHY hard core interface, including 4 data (data) + 1 lane (clk)
- Eight GPIOs reserved

● Type-C Interface

- Support USB 2.0 and USB 3.0 protocols

● SDI Interface

- Two SDI-IN interfaces
- Two SDI-OUT interfaces
- Support 3G and 6G SDI interfaces

● I2C Interface

- One I2C interface

● Key & Indicator

- 1 Key
- 1 LED indicator

DBUG1280-1.0.3E

6(23)

3 Development Board Circuit

3.1 FPGA

# 3 Development Board Circuit

## 3.1 FPGA

### 3.1.1 Overview

For the resources of GW5AT series of FPGA Products, refer to DS981, GW5AT series of FPGA Products Data Sheet.

### 3.1.2 I/O BANK Description

For the I/O BANK, package, and pinout information, see UG983, GW5AT series of FPGA Products Package and Pinout User Guide for more details.

## 3.2 Power Supply

### 3.2.1 Introduction

The development board needs to be powered by a 12V power adapter.

The input parameter of the adapter is AC 100-240V~50/60MHz 0.6A, and the output parameter is DC 12V 2A.

The input 12V power is regulated by the PMIC on the development board to generate 5V, 3.3V, 2.5V, 1.8V, 1.5V, 1.2V, 0.9V, and 0.75V power supplies, thus meeting the power supply requirements of the development board.

DBUG1280-1.0.3E

7(23)

3 Development Board Circuit

3.2 Power Supply

# 3.2.2 Power Distribution

Figure 3-1 Power Distribution Diagram

![img-6.jpeg](img-6.jpeg)

DBUG1280-1.0.3E

8(23)

3 Development Board Circuit

3.3 Download Module

### 3.3 Download Module

### 3.3.1 Introduction

The development board has a Mini USB-B download port (J11) designed to program the programs to external SPI FLASH or download them to SRAM.

The download connection diagram is show in Figure 3-2.

Figure 3-2 Connection Diagram of Download

![img-7.jpeg](img-7.jpeg)

### 3.3.2 Pin Distribution

Table 3-1 JTAG Pin Distribution

[tbl-3.md](tbl-3.md)

### 3.4 Clock

### 3.4.1 Introduction

The development board provides multiple FPGA clock sources, including one 24 MHz single-ended clock, one 148.5 MHz differential clock, and two 200 MHz differential clocks. Among them, the 148.5 MHz differential clock and one of the 200MHz differential clocks are connected the FPGA SerDes high-speed clock pins. The clock pin distribution is shown in Figure 3-3.

DBUG1280-1.0.3E

9(23)

3 Development Board Circuit

3.5 DDR3

Figure 3-3 Clock Connection Diagram

![img-8.jpeg](img-8.jpeg)

### 3.4.2 Pin Distribution

Table 3-2 Clock Pin Distribution

[tbl-4.md](tbl-4.md)

## 3.5 DDR3

### 3.5.1 Introduction

The development board includes one 2Gbit DDR3 chip. The signal of DDR3 chip is connected to the BANK8 and BANK9 of FPGA. The specific configurations of DDR3 are as shown in Table 3-3.

Table 3-3 DDR3 Configuration

[tbl-5.md](tbl-5.md)

DDR3 hardware design requires strict consideration of signal integrity.

DBUG1280-1.0.3E

10(23)

3 Development Board Circuit

3.5 DDR3

In the design of circuit and PCB, matching resistor/termination resistor, impedance control and equal length control of traces have been fully considered to ensure DDR3 works stably at high speed.

The hardware connection diagram of DDR3 is as show in Figure 3-4.

Figure 3-4 Hardware Connection Diagram of DDR3

![img-9.jpeg](img-9.jpeg)

## 3.5.2 Pin Distribution

Table 3-4 DDR3 Pin Distribution

[tbl-6.md](tbl-6.md)

DBUG1280-1.0.3E

11(23)

3 Development Board Circuit

3.5 DDR3

[tbl-7.md](tbl-7.md)

DBUG1280-1.0.3E

12(23)

3 Development Board Circuit

3.6 HDMI-RX Interface

[tbl-8.md](tbl-8.md)

## 3.6 HDMI-RX Interface

### 3.6.1 Introduction

The development board provides an HDMI receiver interface for the reception of HDMI signals through an internal FPGA IP. The connection diagram of the DP interfaces is as follows.

Note!

This HDMI-RX interface circuit can also be used for HDMI-TX communication.

Figure 3-5 Connection Diagram of HDMI-RX Interface

![img-10.jpeg](img-10.jpeg)

### 3.6.2 Pin Distribution

Table 3-5 Pin Distribution of DP-RX Interface

[tbl-9.md](tbl-9.md)

DBUG1280-1.0.3E

13(23)

3 Development Board Circuit

3.7 MIPI Interface

[tbl-10.md](tbl-10.md)

### 3.7 MIPI Interface

#### 3.7.1 Introduction

The development board leads one MIPI CPHY hard core interface and one MIPI DPHY hard core interface from the FPGA. The MIPI CPHY hard core interface, MIPI DPHY hard core interface, and eight 3.3V GPIOs are led to 80P AXK580147YG connector with 0.5mm pitch. The connection diagram is as follows.

Figure 3-6 Connection Diagram of MIPI CPHY & DPHY Hard Core Interfaces

![img-11.jpeg](img-11.jpeg)

DBUG1280-1.0.3E

14(23)

3 Development Board Circuit

3.7 MIPI Interface

### 3.7.2 Pin Distribution

Table 3-6 Pin Distribution of MIPI CPHY & DPHY Hard core Interface

[tbl-11.md](tbl-11.md)

DBUG1280-1.0.3E

15(23)

3 Development Board Circuit

3.7 MIPI Interface

[tbl-12.md](tbl-12.md)

DBUG1280-1.0.3E

16(23)

3 Development Board Circuit

3.7 MIPI Interface

[tbl-13.md](tbl-13.md)

DBUG1280-1.0.3E

17(23)

3 Development Board Circuit

3.8 I2C Interface

### 3.8 I2C Interface

### 3.8.1 Introduction

The development board includes one I2C interface as the host communication interface. The host can monitor the voltages of FPGA VCC, MIPI, VCCX, SerDes, and each BANK through this interface. The connection diagram of I2C interface is shown in Figure 3-7.

Figure 3-7 Connection Diagram of I2C Interface

![img-12.jpeg](img-12.jpeg)

### 3.8.2 Pin Distribution

Table 3-7 J21 Pin Distribution of I2C Interface

[tbl-14.md](tbl-14.md)

### 3.9 Key & LED

### 3.9.1 Introduction

There is one user key on the development board. The user key is connected to the general IO of FPGA BANK8. The corresponding IO input voltage of the FPGA is low when the key is pressed while high when the key is not pressed. The connection diagram is shown in Figure 3-8.

DBUG1280-1.0.3E

18(23)

3 Development Board Circuit

3.9 Key & LED

Figure 3-8 Connection Diagram of Key

![img-13.jpeg](img-13.jpeg)

The development board includes one user LED. The user LED is connected to the IO of FPGA BANK8 and can be switched on and off via the program. The user LEDs will be on when the IO voltage is high. The user LEDs will be off when the IO voltage is low. The connection diagram is shown in Figure 3-8.

Figure 3-9 Connection Diagram of LED

![img-14.jpeg](img-14.jpeg)

## 3.9.2 Pin Distribution

Table 3-8 Pin Distribution of Key

[tbl-15.md](tbl-15.md)

Table 3-9 Pin Distribution of LED

[tbl-16.md](tbl-16.md)

DBUG1280-1.0.3E

19(23)

3 Development Board Circuit

3.10 Type-C Interface

## 3.10 Type-C Interface

### 3.10.1 Introduction

The development board leads a Type-C interface, supporting USB 2.0 and USB 3.0 data transmission. The USB 2.0 is implemented using the Gowin USB 2.0 SoftPHY IP solution, connected to the FPGA through an RC circuit. For detailed information on the peripheral circuitry, please refer to IPUG781, Gowin USB 2.0 SoftPHY IP user guide.

The Type-C interface on the development board connects two SerDes signals to the FPGA, USB 3.0 is implemented with the Gowin USB 3.0 PHY IP. As of November 2024, IP V1.2 supports one SerDes lane signal and only allows single-sided plug on the Type-C interface. Future updates will add support for reversible plug.

Note!

The CC circuit on the development board has not been verified. Use with caution!

Figure 3-10 Connection Diagram of Type-C Interface

![img-15.jpeg](img-15.jpeg)

DBUG1280-1.0.3E

20(23)

3 Development Board Circuit

3.10 Type-C Interface

## 3.10.2 Pin Distribution

Table 3-10 Pin Distribution of Type-C Interface

[tbl-17.md](tbl-17.md)

DBUG1280-1.0.3E

21(23)

3 Development Board Circuit

3.11 SDI Interface

### 3.11 SDI Interface

#### 3.11.1 Introduction

The development board includes two SDI-IN interfaces and two SDI-OUT interfaces, and the interface connectors are BNC, which can meet the performance evaluation needs of the 3G SDI and 6G SDI interfaces.

Figure 3-11 Connection Diagram of SDI Interface

![img-16.jpeg](img-16.jpeg)

#### 3.11.2 Pin Distribution

Table 3-11 Pin Distribution of SDI Interface

[tbl-18.md](tbl-18.md)

DBUG1280-1.0.3E

22(23)

3 Development Board Circuit

3.11 SDI Interface

[tbl-19.md](tbl-19.md)

DBUG1280-1.0.3E

23(23)

GOWIN
PROGRAMMING FOR THE FUTURE