|  Term/Abbreviation | Definition  |
| --- | --- |
|  client | Software resident on the host that interacts with the USB system software to arrange data transfer between a function and the host. The client is often the data provider and consumer for transferred data.  |
|  component | A physical chip or circuit that contains a port.  |
|  configuring software | Software resident on the host that is responsible for configuring a USB device.  |
|  control endpoint | A pair of device endpoints with the same endpoint number that are used by a control pipe. Control endpoints transfer data in both directions and, therefore, use both endpoint directions of a device address and endpoint number combination. Thus, each control endpoint consumes two endpoint addresses.  |
|  control pipe | Same as a message pipe.  |
|  connected | A downstream device is connected to an upstream device when it is attached to the upstream device, and when the downstream device has asserted Rx terminations for SuperSpeed signaling or has asserted the D+ or D- data line in order to enter low-speed, full-speed, or high-speed signaling.  |
|  control transfer | One of the four USB transfer types. Control transfers support configuration/command/status type communications between client and function. See also transfer type.  |
|  Controlling Hub | A controlling hub is any hub whose upstream link is not in U3.  |
|  CRC | CRC-5, CRC-16, CRC-32. See Cyclic Redundancy Check.  |
|  Cyclic Redundancy Check (CRC) | A check performed on data to see if an error has occurred in transmitting, reading, or writing the data. The result of a CRC is typically stored or transmitted with the checked data. The stored or transmitted result is compared to a CRC calculated from the data to determine if an error has occurred.  |
|  D codes | The data type codes used in 8b/10b encoding.  |
|  D+ and D- | Differential pair defined in the USB 2.0 specification.  |
|  default address | An address defined by the USB Specification and used by a USB device when it is first powered or reset. The default address is 00H.  |
|  default pipe | The message pipe created by the USB system software to pass control and status information between the host and a USB device's endpoint zero.  |
|  descrambling | Restoring the pseudo-random 8-bit character to the original state. See scrambling.  |
|  detached | A downstream device is detached from an upstream device when the physical cable between the two is removed.  |
|  device | A logical or physical entity that performs one or more functions. The actual entity described depends on the context of the reference. At the lowest level, device may refer to a single hardware component, as in a memory device. At a higher level, it may refer to a collection of hardware components that perform a particular function, such as a USB interface device. At an even higher level, device may refer to the function performed by an entity attached to the USB. Devices may be physical, electrical, addressable, and logical. When used as a non-specific reference, a USB device is either a hub or a peripheral device.  |
|  device address | A 7-bit value representing the address of a device on the USB. The device address is the default address (00H) when the USB device is first powered or the device is reset. Devices are assigned a unique device address by the USB system software.  |
|  device endpoint | A uniquely addressable portion of a USB device that is the source or sink of information in a communication flow between the host and device. See also endpoint address.  |
|  device software | Software that is responsible for using a USB device. This software may or may not also be responsible for configuring the device for use.  |