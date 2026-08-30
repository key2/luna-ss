Universal Serial Bus 3.1 Specification, Revision 1.0

Table 5-11 shows the wire connections for the USB 3.1 Micro-A to USB 3.1 Micro-B cable assembly. The ID pin on a USB 3.1 Micro-A plug shall be connected to the GND pin. The ID pin on a USB 3.1 Micro-B plug shall be a no-connect or connected to ground by a resistance of greater than Rb_PLUG_ID (1 MΩ minimum). See the Universal Serial Bus Power Delivery Specification for additional details regarding electrical connections to ID pins. An OTG device is required to be able to detect whether a USB 3.1 Micro-A or USB 3.1 Micro-B plug is inserted by determining if the ID pin resistance to ground is less than Ra_PLUG_ID (10 Ω maximum) or if the resistance to ground is greater than Rb_PLUG_ID. Any ID resistance less than Ra_PLUG_ID shall be treated as ID = FALSE and any resistance greater than Rb_PLUG_ID shall be treated as ID = TRUE.

Table 5-11. USB 3.1 Micro-A to USB 3.1 Micro-B Cable Assembly Wiring

[tbl-43.md](tbl-43.md)

Notes:

1. Connect to the GND.

2. No connect or connect to ground by a resistance greater than 1 MΩ minimum.

5-42