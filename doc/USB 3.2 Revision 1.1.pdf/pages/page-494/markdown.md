Revision 1.1  
June 2022

- 463 -

Universal Serial Bus 3.2  
Specification

Within a USB 3.2 hub, both the Enhanced SuperSpeed and USB 2.0 hub devices shall implement in the hub framework a common standardized ContainerID to enable software to identify the physical relationship of the hub devices. The ContainerID descriptor is a part of the BOS descriptor set.

The USB 2.0 capabilities of a USB 3.2 hub shall be designed to the USB 2.0 specification and shall meet the USB 2.0 compliance requirements.

### **11.3 USB 3.2 Device Support for USB 2.0**

In most cases, backward compatible operation at USB 2.0 signaling is supported by USB 3.2 devices in order that higher capability devices are still useful with lesser capable hosts and hubs. For product installations where support for USB 3.2 operation can be independently assured between the device and the host, such as internal devices that are not user accessible, device support for USB 2.0 may not be necessary. USB 3.2 device certification requirements require support for USB 2.0 for all user attached devices.

For any given USB 3.2 peripheral device within a single physical package, only one USB connection mode, either Enhanced SuperSpeed or a USB 2.0 speed but not both, shall be established for operation with the host.

Peripheral devices may implement in the device framework a common standardized ContainerID to enable software to identify all of the functional components of a specific device and independent of which speed bus it appears on. All devices within a compound device that support ContainerID shall return the same ContainerID.

The USB 2.0 capabilities of a USB 3.2 device shall be designed to the USB 2.0 specification and shall meet the USB 2.0 compliance requirements. Note that a USB 3.2 device operating in one of the USB 2.0 modes must return 0210H in the bcd version field of the device descriptor.

### **11.4 Power Distribution**

This section describes the USB 3.2 power distribution specification. The USB 2.0 power distribution requirements still apply when a USB 3.2 device is operating at high-speed, full-speed, or low-speed. Note that a USB 3.2 peripheral device shall not draw more than 100 mA until it detects far-end Rx terminations in the unconfigured state.

#### **11.4.1 Classes of Devices and Connections**

USB 3.2 provides power over three connectors: the USB Standard-A connector, the USB Micro-AB connector (when the ID pin is connected to ground), and the USB Type-C connector (when operating as the Source).

The following sections focus on the power delivery requirements as described for the USB Type-A and USB Type-B family of connectors. For USB Type-C connector power delivery requirements, refer to the USB Type-C Specification and when requirement references are made back to this specification, interpretation of the following requirements need to be interpreted in the context of the USB Type-C definitions of Source and Sink.

The power source and sink requirements of different device classes can be simplified with the introduction of the concept of a unit load. A unit load for Enhanced SuperSpeed for single-lane operation is 150 mA. The number of unit loads a device can draw is an absolute maximum, not an average over time. A device may be either low-power at one unit load or high-power, consuming up to six unit loads. All devices default to low-power when first powered. The transition to high-power is under software control. It is the responsibility of software to ensure adequate power is available before allowing devices to consume high-power.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.