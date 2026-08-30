Revision 1.1
June 2022

- 155 -

Universal Serial Bus 3.2
Specification

### 7.3.14 Summary of Error Types and Recovery

Table 7-11 summarizes the link error types, error count, and different error paths to restore the link.

Situations also exist where an unexpected link command or header packet is received. These include but are not limited to the following:

1. Receiving an unexpected link command such as LBAD, LRTY, LAU, LXU, or LPMA before receiving the Header Sequence Number Advertisement and the Remote Rx Header Buffer Credit Advertisement or Type 1/Type 2 Rx Buffer Credit Advertisements.
2. Receiving the Header Sequence Number Advertisement after entry to U0 from Recovery with its ACK Tx Header Sequence Number not corresponding to any header packets in the Tx Header Buffers or Type 1/Type 2 Tx Header Buffers.
3. Receiving LRTY without sending LBAD.
4. Receiving LGOOD_n that is neither a Header Sequence Number Advertisement, nor for header packet acknowledgement.
5. Receiving LAU, or LXU without sending LGO_Ux.
6. Receiving LPMA without sending LAU.
7. Receiving an unexpected header packet during link initialization.

These error situations are largely not due to link errors. A port's behavior under these situations is undefined and implementation specific. It is recommended that a port ignore those unexpected link commands or header packets.

If the ports are directed to different link states based on TS2 ordered set, the downstream port's TS2 ordered set overrides the upstream port's TS2 ordered set. For example, if a downstream port issues Hot Reset in its TS2 ordered set, and an upstream port issues Loopback mode, Hot Reset overrides Loopback. The ports shall enter Hot Reset.

Table 7-11. Error Types and Recovery

[tbl-88.md](tbl-88.md)

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.