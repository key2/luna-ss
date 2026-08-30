Universal Serial Bus 3.1 Specification, Revision 1.0

## 11.2 USB 3.1 Hub Support for USB 2.0

All ports, both upstream and downstream, on USB 3.1 hubs shall support USB 2.0 operation in order to enable backward compatibility with USB 2.0 devices.

When another USB 3.1 hub is connected in series with a USB 3.1 hub, both SuperSpeed and USB 2.0 high-speed bus connections shall be allowed to connect and operate in parallel. There is no requirement for a USB 3.1 hub to support multiple parallel connections to peripheral devices.

Within a USB 3.1 hub, both the Enhanced SuperSpeed and USB 2.0 hub devices shall implement in the hub framework a common standardized ContainerID to enable software to identify the physical relationship of the hub devices. The ContainerID descriptor is a part of the BOS descriptor set.

The USB 2.0 capabilities of a USB 3.1 hub shall be designed to the USB 2.0 specification and shall meet the USB 2.0 compliance requirements.

## 11.3 USB 3.1 Device Support for USB 2.0

In most cases, backward compatible operation at USB 2.0 signaling is supported by USB 3.1 devices in order that higher capability devices are still useful with lesser capable hosts and hubs. For product installations where support for USB 3.1 operation can be independently assured between the device and the host, such as internal devices that are not user accessible, device support for USB 2.0 may not be necessary. USB 3.1 device certification requirements require support for USB 2.0 for all user attached devices.

For any given USB 3.1 peripheral device within a single physical package, only one USB connection mode, either Enhanced SuperSpeed or a USB 2.0 speed but not both, shall be established for operation with the host.

Peripheral devices may implement in the device framework a common standardized ContainerID to enable software to identify all of the functional components of a specific device and independent of which speed bus it appears on. All devices within a compound device that support ContainerID shall return the same ContainerID.

The USB 2.0 capabilities of a USB 3.1 device shall be designed to the USB 2.0 specification and shall meet the USB 2.0 compliance requirements. Note that a USB 3.1 device operating in one of the USB 2.0 modes must return 0210H in the bcd version field of the device descriptor.

## 11.4 Power Distribution

This section describes the USB 3.1 power distribution specification. The USB 2.0 power distribution requirements still apply when a USB 3.1 device is operating at high-speed, full-speed, or low-speed. Note that a USB 3.1 peripheral device shall not draw more than 100 mA until it detects far-end Rx terminations in the unconfigured state.

11-2