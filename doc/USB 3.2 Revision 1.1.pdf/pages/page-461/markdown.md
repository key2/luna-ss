Revision 1.1  
June 2022

- 430 -

Universal Serial Bus 3.2  
Specification

The USB system software examines hub descriptor information to determine the hub's characteristics. By examining the hub's characteristics, the USB system software ensures that illegal power topologies are not allowed by not powering on the hub's ports if doing so would violate the USB power topology. The device status and configuration information can be used to determine whether the hub can be used in a given topology. Table 10-4 summarizes the information and how it can be used to determine the current power requirements of the hub.

**Table 10-4. Hub Power Operating Mode Summary**

[tbl-212.md](tbl-212.md)

A traditional self-powered hub has a local power source, but may optionally draw one unit load from its upstream connection. This allows the interface to function when local power is not available (refer to Section 11.4.1.1). When local power is removed (either a hub-wide over-current condition or local supply is off), a hub of this type remains in the Configured state but transitions all ports (whether removable or non-removable) to the Powered-off state. While local power is off, all port status and change information read as zero and all SetPortFeature() requests are ignored (request is treated as a no-operation). The hub will use the Status Change endpoint to notify the USB system software of the hub event (refer to Section 10.13.4 for details on hub status).

The *MaxPower* field in the configuration descriptor is used to report to the system the maximum power the hub will draw from USB power when the configuration is selected. The external devices attaching to the hub will report their individual power requirements.

A hub that draws power from USB PD (via its upstream port) or from USB Type-C Current shall report its operating power using the PD Consumer Port Descriptor capability in its BOS Descriptor. System software can determine the current power contract by querying the downstream port on which such a hub is connected. A compound device may power both the hub electronics and the permanently attached devices from USB power or from USB PD (via UFP) or from USB Type-C Current. The entire load may be reported in the hubs'

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.