|  Width (bits) | Offset (DW:bit) | Description  |
| --- | --- | --- |
|  3 | 3:16 | **Header Sequence Number.** The valid values in this field are 0 through 7.  |
|  3 | 3:19 | **Reserved (R).**  |
|  3 | 3:22 | **Hub Depth.** This field is only valid when the **Deferred** bit is set and identifies to the host the hierarchical on the USB that the hub is located at in the deferred TP or DPH returned to the host. This informs the host that the port on which the packet was supposed to be forwarded on is currently in a low power state (either U1 or U2). The only valid values in this field are 0 through 4.  |
|  1 | 3:25 | **Delayed (DL).** This bit may be set if a Header Packet is re-sent or the transmission of a Header Packet is delayed. Chapter 7 and Chapter 10 provide more details on when this bit shall be set. This bit shall not be reset by any subsequent hub that this packet traverses.  |
|  1 | 3:26 | **Deferred (DF).** This bit may only be set by a hub. This bit shall be set when the downstream port on which the packet needs to be sent is in a power managed state. This bit shall not be reset by any subsequent hub that this packet traverses.  |