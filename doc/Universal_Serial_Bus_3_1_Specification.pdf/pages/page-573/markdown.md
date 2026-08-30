# 11 Interoperability and Power Delivery

This chapter defines interoperability and power delivery requirements for USB 3.1. Areas covered include USB 3.1 host and device support for USB 2.0 operation, and USB 3.1 VBUS power consumption limits.

Table 11-1 lists the compatibility matrix for USB 3.1 and USB 2.0. The implication of identifying a host port as supporting USB 3.1 is that both hardware and software support for USB 3.1 is in place; otherwise the port shall only be identified as a USB 2.0 port.

Table 11-1. USB 3.0 and USB 2.0 Interoperability

[tbl-254.md](tbl-254.md)

It should be noted that USB 3.1 devices are not required to be backward compatible with USB 1.1 host ports although supporting full-speed and low-speed modes are allowed.

## 11.1 USB 3.1 Host Support for USB 2.0

USB 3.1-capable ports on hosts shall also support USB 2.0 operation in order to enable backward compatibility with USB 2.0 devices. It should be noted, however, that USB 3.1-capable hosts are not required to support Enhanced SuperSpeed operation on all of the ports available on the host, i.e., some USB 3.1-capable hosts may have a mix of USB 2.0-only and USB 3.1-capable ports.

To address the situation where a USB 3.1 device is connected to a USB 2.0-only port on a USB 3.1-capable host, after establishing a USB 2.0 high-speed connection with the device, it is recommended that the host inform the user that the device will support Enhanced SuperSpeed operation if it is moved to a USB 3.1-capable port on the same host. If a USB 3.1 device is connected to a USB 3.1-capable host via a USB 2.0 hub, it is recommended that the host inform the user that the device will support Enhanced SuperSpeed operation if it is moved to an appropriate host port or if the hub is replaced with a USB 3.1 hub.

When a USB 3.1 hub is connected to a host's USB 3.1-capable port, both USB 3.1 Enhanced SuperSpeed and USB 2.0 high-speed bus connections shall be allowed to connect and operate in parallel. There is no requirement for a USB 3.1-capable host to support multiple parallel connections to peripheral devices.

The USB 2.0 capabilities of a USB 3.1 host shall be designed to the USB 2.0 specification and shall meet the USB 2.0 compliance requirements.

11-1