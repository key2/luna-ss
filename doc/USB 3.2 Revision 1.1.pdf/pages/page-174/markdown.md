Revision 1.1
June 2022

- 143 -

Universal Serial Bus 3.2
Specification

- A port accepting the request to enter a low power link state shall disable and reset PM_ENTRY_TIMER upon receipt of the last symbol of LPMA or detection of a TS1 ordered set at its receiver. Note that if LPMA is corrupted, the port may lose bit-lock at its receiver before PM_ENTRY_TIMER times out. Under this situation, the port shall not initiate entry to Recovery due to bit errors, but continue to remain in U0 until PM_ENTRY_TIMER times out.

A port shall operate Ux_EXIT_TIMER based on the following rules.

- A port initiating U1 or U2 exit shall start Ux_EXIT_TIMER when it starts to send LFPS Exit handshake signal.
- A port initiating U1 or U2 exit shall disable and reset Ux_EXIT_TIMER upon entry to U0.

Table 7-8. Link Flow Control Timers Summary

[tbl-85.md](tbl-85.md)

### 7.2.4.2.2 Low Power Link State Initiation

- A port shall not send a LGO_U1, LGO_U2 or LGO_U3 unless it meets all of the following:

1. It has transmitted LGOOD_n and LCRD_x or LCRD1_x/LCRD2_x for all the packets received.
2. It has received LGOOD_n and LCRD_x or LCRD1_x/LCRD2_x for all the packets transmitted.

Note: This implies all credits must be received and returned before a port can initiate a transition to a low power link state.

3. It has no pending packets for transmission.
4. It has completed the Header Sequence Number Advertisement and the Rx Header Buffer Credit Advertisement or Type 1/Type 2 Rx Buffer Credit Advertisements upon entry to U0.

Note: This implies that a port has sent the Header Sequence Number Advertisement and the Rx Header Buffer Credit Advertisement or Type 1/Type 2 Rx Buffer Credit Advertisements to its link partner, and also received the Header Sequence Number Advertisement and the Rx Header Buffer Credit Advertisement or Type 1/Type 2 Rx Buffer Credit Advertisements from its link partner.

5. It is directed by a higher layer to initiate entry. Examples of when a higher layer may direct the link layer to initiate entry are: (a) the U1 or U2 inactivity timer expires (refer to PORT_U1_TIMEOUT, PORT_U2_TIMEOUT in Chapter 10); (b) reception of a SetPortFeature(PORT_LINK_STATE) request; and (c) device implementation specific mechanisms.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.