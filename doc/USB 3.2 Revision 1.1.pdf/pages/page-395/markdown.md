Revision 1.1
June 2022

- 364 -

Universal Serial Bus 3.2
Specification

[tbl-198.md](tbl-198.md)

### 9.6.6 Endpoint

Each endpoint used for an interface has its own descriptor. This descriptor contains the information required by the host to determine the bandwidth requirements of each endpoint. An endpoint descriptor is always returned as part of the configuration information returned by a GetDescriptor(Configuration) request. An endpoint descriptor cannot be directly accessed with a GetDescriptor() or SetDescriptor() request. There is never an endpoint descriptor for endpoint zero. Table 9-26 shows the standard endpoint descriptor.

Table 9-26. Standard Endpoint Descriptor

[tbl-199.md](tbl-199.md)

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.