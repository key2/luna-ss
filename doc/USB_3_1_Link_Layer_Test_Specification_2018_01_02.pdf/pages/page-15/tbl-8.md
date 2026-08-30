|  7.2.4.1.1#14 | Upon entry to U0, after starting the PENDING_HP_TIMER and (Type 1/Type 2) CREDIT_HP_TIMER timers, a port shall initiate the Header Sequence Number Advertisement. | 7.26 BC  |
| --- | --- | --- |
|  7.2.4.1.1#15 | Upon entry to U0, after the Header Sequence Number Advertisement, a port in SuperSpeed operation shall initiate the Rx Header Buffer Credit Advertisement. | 5.1 7.26  |
|  7.2.4.1.1#16 | Upon entry to U0, after the Header Sequence Number Advertisement, a port in SuperSpeedPlus operation shall initiate the Type 1 and Type 2 Rx Header Buffer Credit Advertisement. | 5.1 7.26  |
|  7.2.4.1.1#17 | A port shall set its initial Rx Header Sequence Number to zero when it enters U0 from Polling or Hot Reset. | 5.1 7.27 - 29  |
|  7.2.4.1.1#18 | A port shall set its initial Rx Header Sequence Number to the Header Sequence Number of the next expected header packet when it enters U0 from Recovery. | 5.1 7.30  |
|  7.2.4.1.1#19 | A port shall set its initial Tx Header Sequence Number to zero when it enters U0 from Polling or Hot Reset. | 5.1 7.27 – 7.29  |
|  7.2.4.1.1#20 | A port shall set its initial Tx Header Sequence Number to the same as the Tx Header Sequence Number before Recovery when it enters U0 from Recovery. | 7.26 7.30  |
|  7.2.4.1.1#21 | A header packet that is re-transmitted shall maintain its original Header Sequence Number. | 7.8  |
|  7.2.4.1.1#22 | A port shall initiate the Header Sequence Number Advertisement by transmitting LGOOD_n with "n" equal to the Rx Header Sequence Number minus one. | 5.1  |
|  7.2.4.1.1#23 | A port shall set its initial ACK Tx Header Sequence Number to the Sequence Number received during the Rx Header Sequence Number Advertisement plus one. | 5.1  |
|  7.2.4.1.1#24 | A port in SuperSpeed operation shall not send any header packets until the Header Sequence Number Advertisement has been received and a Remote Rx Header Buffer Credit is available. | 5.1  |
|  7.2.4.1.1#25 | A port in SuperSpeedPlus operation shall not send any Type 1 or Type 2 packet until the Header Sequence Number Advertisement has been received and the port's respective Remote Type 1 or Type 2 Rx Header Buffer Credit is available. | 5.1  |
|  7.2.4.1.1#26 | A port shall not request for low power link state entry before receiving and sending the Header Sequence Number Advertisement. | 5.1  |
|  7.2.4.1.1#27 | Upon receiving the Header Sequence Number Advertisement, a port shall flush all the header packets in its (Type 1/Type 2) Tx Header Buffers if the port entered U0 from Polling or Hot Reset. | NT  |