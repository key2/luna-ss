Revision 1.1
June 2022

- 17 -

Universal Serial Bus 3.2
Specification

### 3.1.1 USB 3.2 Mechanical

The mechanical specifications for USB cables and connector assemblies are provided in separate USB electro-mechanical specifications: the USB Type-C Cable and Connector specification and the USB 3.1 Legacy Cable and Connector specification. Chapter 5 of this specification provides a summary of cables and connectors that are applicable for USB 3.2 use.

All USB devices have an upstream connection. Hosts and hubs have one or more downstream connections. For USB legacy connectors, upstream and downstream connectors are not mechanically interchangeable, thus eliminating illegal loopback connections at hubs. For USB Type-C connectors, upstream and downstream behaviors are established using the configuration features of the USB Type-C functional architecture.

For USB legacy connectors, USB 3.1 receptacles (both upstream and downstream) are backward compatible with USB 2.0 connector plugs. USB 3.1 cables and plugs are not intended to be compatible with USB 2.0 upstream receptacles. For USB Type-C, legacy adaptation cables and adapter assemblies are defined to support backward compatibility.

### 3.1.2 USB 3.2 Power

The specification covers two aspects of power:

- Power distribution over the USB deals with the issues of how USB devices consume power provided by the downstream ports to which they are connected. USB 3.2 power distribution is similar to USB 2.0, with increased supply budgets for devices operating on an Enhanced SuperSpeed bus, with additional consideration if the bus operation is two-lane versus single-lane.
- Power management defines how hosts, devices, hubs, and the USB system software interact to provide power efficient operation of the bus. The power management of the USB 2.0 bus portion is unchanged.

For USB Type-C, additional power options are defined in the USB Type-C and USB Power Delivery specifications.

### 3.1.3 USB 3.2 System Configuration

USB 3.2 allows USB devices to be attached or detached at any time, therefore system software must accommodate dynamic changes in the physical bus topology. The architectural elements for the device discovery on USB 3.2 are identical to those in USB 2.0. Enhancements are provided to manage the specifics of the Enhanced SuperSpeed bus for configuration and power management.

The independent, dual-bus architecture allows for activation of each of the buses independently.

### 3.1.4 Architectural Differences between USB 3.2 and USB 2.0

Table 3-1 summarizes the key architectural differences between an Enhanced SuperSpeed bus and a USB 2.0 bus.

Table 3-1. Comparing Enhanced SuperSpeed Bus to USB 2.0 Bus

[tbl-30.md](tbl-30.md)

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.