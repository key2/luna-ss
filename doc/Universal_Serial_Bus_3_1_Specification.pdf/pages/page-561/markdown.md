Hub, Host Downstream Port, and Device Upstream Port Specification

### 10.16.2.6.3 Extended Port Status Bits

The extended port status bits are returned only if the Port Status Type of a Get Port Status request is set to EXT_PORT_STATUS.

Note that for Enhanced SuperSpeed devices the “Port Speed” is the Link Speed multiplied by Lane Count.

Table 10-15. Extended Port Status Field, dwExtPortStatus

[tbl-244.md](tbl-244.md)

### TX_SUBLINK_SPEED_ID and RX_SUBLINK_SPEED_ID

The value in this field is only valid when the PORT_ENABLE bit is set to one. The Lane Speed (i.e. bit rate of a single lane) is determined by evaluating the parameters of the Sublink Speed Attribute in the SuperSpeedPlus USB Capability descriptor whose Sublink Speed Attribute ID value matches the Sublink Speed ID value, e.g. if the Sublink Speed Attribute LSE and LSM fields equal 3 and 10, respectively, then the link is operating at 10 Gb/s. All values not referenced by a Sublink Speed Attribute are reserved.

This field can only be read by USB system software.

### TX_LANE_COUNT and RX_LANE_COUNT

This value in this field is only valid when the PORT_ENABLE bit is set to one. The speed of a port is determined by multiplying the Sublink Speed (as defined by the SUBLINK_SPEED_ID) by the Lane Count.

This field can only be read by USB system software.

### 10.16.2.7 Set Hub Descriptor

This request overwrites the hub descriptor.

[tbl-245.md](tbl-245.md)

The SetDescriptor request for the hub class descriptor follows the same usage model as that of the standard SetDescriptor request (refer to the framework chapter). The standard hub descriptor is denoted by using the value bDescriptorType defined in Section 10.15.2.1. All hubs are required to implement one hub descriptor with descriptor index zero.

10-83