|  Error Type | Description/Example | Error Recovery Path | Update Link Error Count? | Update Soft Error Count? (SuperSpeedPlus USB)  |
| --- | --- | --- | --- | --- |
|  Missing Header Packet Framing | Only a valid packet framing ordered set will be declared in the receiver side. | Delayed transition to Recovery | Yes | No  |
|  Header Packet Error | Any header packet CRC is bad. | Header packet retry process | No | Yes  |
|  Rx Header Sequence Number Error | The Header Sequence Number in the received header packet does not match the Rx Header Sequence Number. | Recovery | Yes | No  |
|  ACK Tx Header Sequence Number Error | The Header Sequence Number in the received LGOOD_n (not Header Sequence Number Advertisement) does not match ACK Tx Header Sequence Number. | Recovery | Yes | No  |