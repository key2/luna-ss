Device Framework

### 9.4.10 Set Interface

This request allows the host to select an alternate setting for the specified interface.

[tbl-169.md](tbl-169.md)

Some devices have configurations with interfaces that have mutually exclusive settings. This request allows the host to select the desired alternate setting. If a device only supports a default setting for the specified interface, then a STALL Transaction Packet may be returned in the Status stage of the request. This request cannot be used to change the set of configured interfaces (the SetConfiguration() request shall be used instead).

If the interface or the alternate setting does not exist, then the device responds with a Request Error. If wLength is non-zero, then the behavior of the device is not specified.

Default state: Device behavior when this request is received while the device is in the Default state is not specified.

Address state: The device shall respond with a Request Error.

Configured state: This is a valid request when the device is in the Configured state.

### 9.4.11 Set Isochronous Delay

This request informs the device of the delay from the time a host transmits a packet to the time it is received by the device.

[tbl-170.md](tbl-170.md)

The wValue field specifies a delay from 0 to 65535 ns. This delay represents the time from when the host starts transmitting the first framing symbol of the packet to when the device receives the first framing symbol of that packet. The wValue field shall be calculated as follows.

$$wValue = (sum \ of \ wHubDelay \ values) + (tTPTransmissionDelay \ * \ (number \ of \ hubs \ + \ 1))$$

Where, a wHubDelay value is provided by the Enhanced SuperSpeed Hub Descriptor of each hub in the path, respectively, and tTPTransmissionDelay is defined in Table 8-35.

If wIndex or wLength is non-zero, then the behavior of this request is not specified.

Default state: This is a valid request when the device is in the Default state.

Address state: This is a valid request when the device is in the Address state.

Configured state: This is a valid request when the device is in the Configured state.

9-31