Revision 1.1
June 2022

- 361 -

Universal Serial Bus 3.2
Specification

[tbl-195.md](tbl-195.md)

### 9.6.4 Interface Association

The Interface Association Descriptor is used to describe that two or more interfaces are associated to the same function. An "association" includes two or more interfaces and all of their alternate setting interfaces. A device must use an Interface Association descriptor for each device function that requires more than one interface. An Interface Association descriptor is always returned as part of the configuration information returned by a GetDescriptor(Configuration) request. An interface association descriptor cannot be directly accessed with a GetDescriptor() or SetDescriptor() request. An interface

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.