Revision 1.1
June 2022

- 359 -

Universal Serial Bus 3.2
Specification

### 9.6.2.6 Precision Time Measurement

This section defines the required device-level capabilities descriptor which shall be implemented by all hubs and devices that support the PTM capability. This capability descriptor cannot be directly accessed with a GetDescriptor() or SetDescriptor() request.

Table 9-20. PTM Capability Descriptor

[tbl-191.md](tbl-191.md)

### 9.6.2.7 Configuration Summary Descriptor

The Configuration Summary Descriptor may be implemented by a device with more than one configuration, and identifies a single function presented by the device along with a list of the configuration descriptor indices that include the function. If implemented, each function presented by the device shall be represented by a separate Configuration Summary Descriptor. However, a function's Configuration Summary Descriptor may be omitted if the function is present in all possible configurations. Configuration Summary Descriptors should be included in the BOS descriptor in order of descending preference.

Configuration Summary Descriptors may be used by the host to select the most appropriate/preferred configuration for the device.

Table 9-21. Configuration Summary Descriptor

[tbl-192.md](tbl-192.md)

### 9.6.2.8 FWStatus Capability

This section defines the required device level capabilities descriptor which shall be implemented by all hubs and devices that support the FWStatus capability. This capability descriptor cannot be directly accessed with GetDescriptor() or SetDescriptor() request.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.