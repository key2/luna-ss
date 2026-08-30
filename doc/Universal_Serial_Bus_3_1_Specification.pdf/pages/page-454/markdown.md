Universal Serial Bus 3.1 Specification, Revision 1.0

The bcdUSB field contains a BCD version number. The value of the bcdUSB field is 0xJJMN for version JJ.M.N (JJ – major version number, M – minor version number, N – sub-minor version number), e.g., version 2.1.3 is represented with value 0213H and version 3.0 is represented with a value of 0300H.

The bNumConfigurations field indicates the number of configurations at the current operating speed. Configurations for the other operating speed are not included in the count. If there are specific configurations of the device for specific speeds, the bNumConfigurations field only reflects the number of configurations for a single speed, not the total number of configurations for both speeds.

If the device is operating at Gen X speed, the bMaxPacketSize0 field shall be set to 09H (see Table 9-11) indicating a 512-byte maximum packet. An Enhanced SuperSpeed device shall not support any other maximum packet sizes for the default control pipe (endpoint 0) control endpoint.

All devices have a default control pipe. The maximum packet size of a device's default control pipe is described in the device descriptor. Endpoints specific to a configuration and its interface(s) are described in the configuration descriptor. A configuration and its interface(s) do not include an endpoint descriptor for the default control pipe. Other than the maximum packet size, the characteristics of the default control pipe are defined by this specification and are the same for all Enhanced SuperSpeed devices.

The bNumConfigurations field identifies the number of configurations the device supports. Table 9-11 shows the standard device descriptor.

9-36