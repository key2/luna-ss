Revision 1.1
June 2022

- 187 -

Universal Serial Bus 3.2
Specification

Figure 7-21. Polling Substate Machine

![img-87.jpeg](img-87.jpeg)

Note: Transition conditions are illustrative only. Not all of the transition conditions are listed.

### 7.5.5 Compliance Mode

Compliance Mode is used to test the transmitter for compliance to voltage and timing specifications. Several different test patterns are transmitted as defined in Table 6-14. Compliance Mode does not contain any substate machines.

Note that for a downstream port, the default setting for entry to Compliance Mode is disabled. It may optionally be enabled when directed. This is to prevent the automatic entry to Compliance Mode due to connection of a bad device that fails to exit from Polling.LFPS upon power-on, or a downstream port fails to respond in time.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.