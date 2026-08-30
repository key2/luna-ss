Revision 1.1
June 2022

- 113 -

Universal Serial Bus 3.2
Specification

## 7 Link Layer

The Enhanced SuperSpeed USB consists of SuperSpeed USB based on Gen 1x1 operation, and SuperSpeedPlus USB based on Gen 2 operation (Gen 2x1 or Gen 2x2) or Gen 1x2 operation. The link layer of the Enhanced SuperSpeed USB has the responsibility of maintaining the link connectivity so that successful data transfers between the two link partners are ensured. A robust link flow control is defined based on packets and link commands. Packets are prepared in the link layer to carry data and different information between the host and a device. Link commands are defined for communications between the two link partners. Packet frame ordered sets and link command ordered sets are also constructed such that they are tolerant to one symbol error. In addition, error detection capabilities are also incorporated into a packet and a link command to verify packet and link command integrity.

Figure 7-1. Link Layer

![img-61.jpeg](img-61.jpeg)

(1) Definition is Gen X dependent

The link layer also facilitates link training, link testing/debugging, and link power management. This is accomplished by the introduction of Link Training Status State Machine (LTSSM).

The focus of this chapter is to address the following in detail:

- Packet Framing
- Link command definition and usage
- Link initialization and flow control
- Link power management
- Link error rules/recovery
- Resets
- LTSSM specifications

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.