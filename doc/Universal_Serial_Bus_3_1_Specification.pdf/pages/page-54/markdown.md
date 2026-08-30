Universal Serial Bus 3.1 Specification, Revision 1.0

![img-1.jpeg](img-1.jpeg)

Figure 3-1. USB 3.1 Dual Bus System Architecture

- USB 3.1 interconnect
- USB 3.1 devices
- USB 3.1 host

The USB 3.1 interconnect is the manner in which USB 3.1 and USB 2.0 devices connect to and communicate with the USB 3.1 host. The USB 3.1 interconnect inherits core architectural elements from USB 2.0, although several are augmented to accommodate the dual bus architecture.

The baseline structural topology is the same as USB 2.0. It consists of a tiered star topology with a single host at tier 1 and hubs at lower tiers to provide bus connectivity to devices.

The USB 3.1 connection model accommodates backward and forward compatibility for connecting USB 3.1 or USB 2.0 devices into a USB 3.1 connector. Similarly, USB 3.1 devices

can be attached to a USB 2.0 connector. The mechanical and electrical backward/forward compatibility for USB 3.1 is accomplished via a composite cable and associated connector assemblies that form the mechanical infrastructure for the dual-bus architecture. USB 3.1 peripheral devices accomplish backward compatibility by including both Enhanced SuperSpeed and USB 2.0 interfaces. USB 3.1 hosts have both Enhanced SuperSpeed and USB 2.0 interfaces, which are essentially parallel buses that may be active simultaneously.

The USB 3.1 connection model allows for the discovery and configuration of USB devices at the highest signaling speed supported by the peripheral device, the highest signaling rate supported by hubs between the host and peripheral device, and the current host capability and configuration.

USB 3.1 hubs are a specific class of USB device whose purpose is to provide additional connection points to the bus beyond those provided by the host. In this specification, non-hub devices are referred to as peripheral devices in order to differentiate them from hub devices. In addition, in USB 2.0 the term “function” was sometimes used interchangeably with device. In this specification a function is a logical entity within a device, see Figure 3-4.

The architectural implications of Enhanced SuperSpeed bus support on hosts, hub devices and peripheral devices are described in detail in Section 3.2.

### 3.1.1 USB 3.1 Physical Interface

The physical interface of USB 3.1 is comprised of USB 2.0 and Enhanced SuperSpeed portions. The USB 2.0 definitions for Electrical can be found in Chapter 7 of the USB 2.0 specification. The Enhanced SuperSpeed definitions are contained in this USB 3.1 specification and comprised of Mechanical (Chapter 5), and Physical Layer (Chapter 6) specifications. The physical layer for the Enhanced SuperSpeed bus is described in Section 3.2.1.

3-2