Revision 1.1
June 2022

- 349 -

Universal Serial Bus 3.2
Specification

The bNumConfigurations field indicates the number of configurations at the current operating speed. Configurations for the other operating speed are not included in the count. If there are specific configurations of the device for specific speeds, the bNumConfigurations field only reflects the number of configurations for a single speed, not the total number of configurations for both speeds.

An Enhanced SuperSpeed device shall set the bMaxPacketSize0 field to 09H (see Table 9-11) indicating a 512-byte maximum packet. An Enhanced SuperSpeed device shall not support any other maximum packet sizes for the default control pipe (endpoint 0) control endpoint.

All devices have a default control pipe. The maximum packet size of a device's default control pipe is described in the device descriptor. Endpoints specific to a configuration and its interface(s) are described in the configuration descriptor. A configuration and its interface(s) do not include an endpoint descriptor for the default control pipe. Other than the maximum packet size, the characteristics of the default control pipe are defined by this specification and are the same for all Enhanced SuperSpeed devices.

The bNumConfigurations field identifies the number of configurations the device supports. Table 9-11 shows the standard device descriptor.

Table 9-11. Standard Device Descriptor

[tbl-179.md](tbl-179.md)

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.