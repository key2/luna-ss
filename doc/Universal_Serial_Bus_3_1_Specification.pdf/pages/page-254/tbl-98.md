|  Error Type | Description/Example | Error Recovery Path | Update Link Error Count? | Update Soft Error Count? (SuperSpeedPlus USB)  |
| --- | --- | --- | --- | --- |
|  Missing Header Packet Framing | Only a valid packet framing ordered set will be declared in the receiver side. | Delayed transition to Recovery | Yes | No  |
|  Header Packet Error | Any header packet CRC is bad. | Header packet retry process | No | Yes  |
|  Rx Header Sequence Number Error | The Header Sequence Number in the received header packet does not match the Rx Header Sequence Number. | Recovery | Yes | No  |
|  ACK Tx Header Sequence Number Error | The Header Sequence Number in the received LGOOD_n (not Header Sequence Number Advertisement) does not match ACK Tx Header Sequence Number. | Recovery | Yes | No  |
|  Header Sequence Number Advertisement Error | 1. LGOOD_n not received upon PENDING_HP_TIMER timeout. 2. A header packet received before sending LGOOD_n. 3. LCRD_x or LCRD1_x/LCRD2_x or LGO_Ux received before receiving LGOOD_n. | Recovery | Yes | No  |
|  Rx Header Buffer Credit Advertisement Error (SuperSpeed USB) | 1. LCRD_x not received upon CREDIT_HP_TIMER timeout. 2. A header packet received before sending LCRD_x. 3. LGO_Ux received before receiving LCRD_x. | Recovery | Yes | No  |
|  Type 1/Type 2 Rx Buffer Credit Advertisement Error (SuperSpeedPlus USB) | 1. LCRD1_x/LCRD2_x not received upon Type 1/Type 2 CREDIT_HP_TIMER timeout. 2. A packet received before sending LCRD1_x/LCRD2_x. 3. LGO_Ux received before receiving LCRD1_x/LCRD2_x. | Recovery | Yes | No  |