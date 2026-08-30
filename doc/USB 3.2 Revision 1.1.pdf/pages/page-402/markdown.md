Revision 1.1
June 2022

- 371 -

Universal Serial Bus 3.2
Specification

Table 9-31. UNICODE String Descriptor

[tbl-206.md](tbl-206.md)

### 9.7 Device Class Definitions

All devices shall support the requests and descriptor definitions described in this chapter. Most devices provide additional requests and, possibly, descriptors for device-specific extensions. In addition, devices may provide extended services that are common to a group of devices. In order to define a class of devices, the following information shall be provided to completely define the appearance and behavior of the device class.

### 9.7.1 Descriptors

If the class requires any specific definition of the standard descriptors, the class definition shall include those requirements as part of the class definition. In addition, if the class defines a standard extended set of descriptors, they shall also be fully defined in the class definition. Any extended descriptor definitions shall follow the approach used for standard descriptors; for example, all descriptors shall begin with a length field.

### 9.7.2 Interface(s)

When a class of devices is standardized, the interfaces used by the devices shall be included in the device class definition. Devices may further extend a class definition with proprietary features as long as they meet the base definition of the class.

### 9.7.3 Requests

All of the requests specific to the class shall be defined.

### 9.8 Constants

Table 9-32 lists the constants that are used in this chapter.

Table 9-32. Constants

[tbl-207.md](tbl-207.md)

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.