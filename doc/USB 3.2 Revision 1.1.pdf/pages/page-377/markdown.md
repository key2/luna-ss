Revision 1.1
June 2022

- 346 -

Universal Serial Bus 3.2
Specification

For returning the current status of the FW update allowed/disallowed state:

[tbl-176.md](tbl-176.md)

For returning the current hash using SHA256 algorithm:

[tbl-177.md](tbl-177.md)

The implementation of this command must be equivalent to a ROM based implementation such that future updates to the device FW should not result into changes in the behavior of this command execution. Such an implementation is necessary to ensure that if the updateable portion of the device FW is updated by malware it can be detected by higher level SW using this command.

In order to minimize the latency associated with actual execution of this command the hash can be pre-computed and stored in a persistent storage that is only accessible to the hardened code. This will require the device to disallow writes to the address space storing the hash prior to the exiting the ROM based code execution.

If SW determines that the received hash does not match the expected hash value, it may use FW update to ensure that the firmware is updated to a gold state. The device may continue to reuse the existing protocol for firmware update.

### 9.4.16 Events and Their Effect on Device Parameters

This section lists the various parameters and the effect on those parameters when the device receives a control transfer command or when it observes a bus reset on the bus. An X denotes that the parameter is reset to its default value when the said event occurs. A Y denotes that the particular Parameter is modified by the event.

Control transfers and events not identified in the table shall not affect the value of parameters shown in Table 9-10.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.