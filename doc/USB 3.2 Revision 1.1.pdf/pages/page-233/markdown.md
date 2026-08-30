Revision 1.1
June 2022

- 202 -

Universal Serial Bus 3.2
Specification

Figure 7-26. Loopback Substate Machine

![img-92.jpeg](img-92.jpeg)

Note: Transition conditions are illustrative only. Not all of the transition conditions are listed.

### 7.5.12 Hot Reset

Only a downstream port can be directed to initiate a Hot Reset.

When the downstream port initiates reset, it shall transmit on each negotiated lane the TS2 ordered sets with the Reset bit asserted. The upstream port shall respond on each negotiated lane by sending the TS2 ordered sets with Reset bit asserted. Upon completion of Hot Reset processing, the upstream port shall signal the downstream port by sending the TS2 ordered sets with the Reset bit de-asserted. The downstream port shall respond with the Reset bit de-asserted in the TS2 ordered sets. Once both ports receive the TS2 ordered sets with the Reset bit de-asserted, they shall exit from Hot Reset.Active and transition to Hot Reset.Exit. Once a successful idle symbol handshake is achieved, the port shall return to U0.

#### 7.5.12.1 Hot Reset Substate Machines

Hot Reset contains a substate machine shown in Figure 7-27 with the following substates:

- Hot Reset Active
- Hot Reset.Exit

#### 7.5.12.2 Hot Reset Requirements

- A downstream port shall reset its Link Error Count as defined in Section 7.4.2.
- A downstream port shall reset its PM timers and the associated U1 and U2 timeout values to zero.
- The port in SuperSpeedPlus operation shall reset the Soft Error Count if implemented.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.