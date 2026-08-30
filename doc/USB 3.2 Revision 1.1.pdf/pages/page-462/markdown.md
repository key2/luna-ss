Revision 1.1
June 2022

- 431 -

Universal Serial Bus 3.2
Specification

configuration and/or BOS descriptor with the permanently attached devices each reporting self-powered, with zero MaxPower in their respective configuration descriptors.

A bus powered hub shall be able to supply any power not used by the hub electronics or permanently attached devices for the selected configuration to the exposed downstream ports. The hub shall be able to provide the power with any split across the exposed downstream ports (i.e., if the hub can provide 600 mA to two exposed downstream ports, it must be able to provide 450 mA to one and 150 mA to the other, 300 mA to each, etc.).

Note: Software shall ensure that at least ONE UNIT LOAD is available for each exposed downstream port on a bus powered hub.

A self-powered hub shall ensure that it is able to provide at least six unit loads for each exposed downstream port on the hub. In addition, depending on the type of self-powered hub, when the hub is attached to a USB downstream port, it shall:

- Traditional (non-USB connector e.g. barrel jack): The hub independently manages its power and shall move to the Powered state (as per Section 9.1) on both the USB 2.0 and the USB 3.2 hubs when external power is applied.
- USB PD powered [via its upstream port]: The hub draws power from the upstream port and shall move to the Powered state if it gets enough power to be a self-powered hub. If it cannot, then it shall use PD mechanisms to inform the system of a Capability mismatch with insufficient power.
- USB PD powered [via one of its downstream ports]: The hub draws power from one of its downstream ports and shall move to the Powered state if it gets enough power to be a self-powered hub. If it cannot, then it shall:

- Move only the USB 2.0 hub to the Powered state
- Set C_HUB_LOCAL_POWER and set the local power source field in the Hub Status to one
- Set Downstream PD Capability Mismatch field in the Hub Status to one

- USB Type-C current [via its upstream port]: The hub draws power from the upstream port and shall move to the Powered state if it gets enough power to be a self-powered hub. If it cannot, then it shall:

- Move only the USB 2.0 hub to the Powered state
- Set C_HUB_LOCAL_POWER and set the local power source field in the Hub Status to one
- Set Insufficient USB Type-C current field in the Hub Status to one

### 10.15 Descriptors

Hub descriptors are derived from the general USB device framework. Hub descriptors describe a hub device and the ports on that hub. The host accesses hub descriptors through the hub's default control pipe.

The USB specification (refer to Chapter 8) defines the following descriptors:

- Device Level Descriptors
- Configuration
- Interface
- Endpoint
- String (optional)

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.