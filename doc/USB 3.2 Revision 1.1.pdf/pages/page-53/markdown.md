Revision 1.1
June 2022

- 22 -

Universal Serial Bus 3.2
Specification

### 3.2.1.3 Dual-Lane Operation

Dual-lane operation is supported for USB Type-C-based applications only. Requirements specific to dual-lane operation include the following.

- Data Striping applies to data blocks but control blocks are duplicated on both lanes.
- Data Scrambling operates on a per lane basis with a different seed value defined for each lane.
- Ordered Sets are transmitted simultaneously on each lane within skew constraints. TS1 and TS2 transmit/receive sequences proceed in sync across both lanes and clock offset compensation using SKP ordered sets is performed on a per lane basis.
- At the receiver input, a maximum lane-to-lane skew of 6400 ps is allowed.

To manage dual-lane operation, the Configuration Lane is Lane 0 as established at each port by the CC pin decoding defined by the USB Type-C specification. All LFPS signaling and LBPM messaging is only transmitted on this lane. Receiver Detect is only required on this lane and Ux Exit functionality is only required in the Configuration Lane's receiver.

Compliance features also include support for dual-lane operation.

### 3.2.2 Link Layer

The Enhanced SuperSpeed link layer specifications are detailed in Chapter 7. An Enhanced SuperSpeed link is a logical and physical connection of two ports. The connected ports are called link partners. The link layer defines the logical portion of a port and the communications between link partners.

The link layer has:

- State machines for managing its end of the physical connection. These include physical layer initialization and event management, i.e., connect, removal, and power management. Also included is initializing and configuring dual-lane operation.
- State machines and buffering for managing information exchanges with the link partner. It implements protocols for flow control, reliable delivery (port to port) of packet headers, and link power management. The different link packet types are defined in Chapter 7.
- Buffering for data and protocol layer information elements.

The link layer also:

- Provides correct framing of sequences of bytes into packets during transmission; e.g., insertion of packet delimiters
- Detects received packets, including packet delimiters and error checks of received header packets (for reliable delivery)
- Provides an appropriate interface to the protocol layer for pass-through of protocol-layer packet information exchanges

The link layer:

- Manages the state of its PHY (i.e., its end of the physical connection), including power management and events (connection, removal, and wake).
- Transmits and receives byte streams, with additional signals that qualify the byte stream as control sequences or data. The physical layer includes discrete transmit and receive physical links, therefore, a port is able to simultaneously transmit and receive control and data information.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.