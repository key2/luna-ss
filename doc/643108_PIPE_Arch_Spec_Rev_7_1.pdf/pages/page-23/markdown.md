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