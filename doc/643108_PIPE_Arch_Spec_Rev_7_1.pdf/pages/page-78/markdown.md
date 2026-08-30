intel®

# 7 PIPE Message Bus Address Spaces

The PIPE specification defines 12-bit address spaces to enable the message bus interface; the MAC and the PHY each implement a unique 12-bit address space as shown in Figure 7-1. These address spaces are used to host registers associated with certain PIPE operations. The MAC and PHY access specific bits in the registers to initiate operations, to participate in handshakes, or to indicate status. The MAC initiates requests on the message bus interface to access registers hosted in the PHY address space. The PHY initiates requests on the message bus interface to access registers hosted in the MAC address space.

Each 12-bit address space is divided into four main regions: the receiver address region, the transmitter address region, the common address region, and the vendor-specific address region. The receiver address region is used to configure and report the status related to receiver operation; it spans the 1024-KB region from 12'h000 to 12'h3FF and supports up to two receivers with 512 KB allocated to each. The transmitter address region is used to configure and report status related to transmitter operation; it spans the 1024-KB region from 12'h400 to 12'h7FF and supports up to two transmitters: TX1 and TX2, with a 512 KB region associated with each. The common address region hosts the registers relevant to both receiver and transmitter operation; it spans the 1024-KB region from 12'h800 to 12'hBFF and supports up two sets of Rx/Tx pairs with 512 KB allocated towards the common registers for each pair. The vendor-specific address region is the 1024K region from 12'hC00 to 12'hFFF, which enables individual vendors to define registers as needed outside of those defined in this PIPE specification.

As noted in the previous paragraphs, the address space is defined to support configurable Rx/Tx pairs. Up to two differential pairs are assumed to be operational at any one time. Supported combinations are one Rx and one Tx pair, two Tx pairs, or two Rx pairs.

78

Reference Number: 643108, Revision: 7.1