Revision 1.1
June 2022

- 214 -

Universal Serial Bus 3.2
Specification

### 8.4.5 Port Capabilities

The Port Capability LMP describes each port's link capabilities and is sent by both link partners after the successful completion of training and link initialization. After the port enters U0 from Polling, the port shall send Port Capability LMP within tPortConfiguration time once link initialization (refer to Section 7.2.4.1.1) is completed. Note the port may not always transition directly from Polling to U0, but may transition through other intermediate states (e.g., Recovery or Hot Reset) before entering U0. Regardless of states passed through between Polling and entry into U0, the device shall send a Port Capability LMP immediately upon entering U0.

If a link partner does not receive this LMP within tPortConfiguration time then:

- If the link partner has downstream capability, it shall signal an error as described in Section 10.16.2.6.
- If the link partner only supports upstream capability, see Sections 10.5 and 10.18 which define the hub and peripheral upstream port connect states.

Figure 8-8. Port Capability LMP

![img-101.jpeg](img-101.jpeg)

U-097

Table 8-7. Port Capability LMP Format

[tbl-103.md](tbl-103.md)

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.