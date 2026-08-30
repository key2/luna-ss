|  7.2.4.1.3#6 | For SuperSpeed USB, the Remote Rx Header Buffer Credit Count shall be incremented by one if a valid LCRD_x is received. | BC  |
| --- | --- | --- |
|  7.2.4.1.3#7 | For SuperSpeedPlus USB, the Remote Type 1 Rx Buffer Credit Count shall be incremented by one if a valid LCRD1_x is received. The Remote Type 2 Rx Buffer Credit Count shall be incremented by one if a valid LCRD2_x is received. | BC  |
|  7.2.4.1.3#8 | For SuperSpeed USB, the Remote Rx Header Buffer Credit Count shall be decremented by one if a header packet is sent for the first time after entering U0, including when it is resent following Recovery. | NT/BC  |
|  7.2.4.1.3#9 | For SuperSpeedPlus USB, Remote Type 1 Rx Buffer Credit Count shall be decremented by one if a Type 1 packet is sent for the first time after entering U0, including when it is resent following Recovery. The same operation applies to Remote Type 2 Rx Buffer Credit Count with regard to Type 2 packet. | NT/BC  |
|  7.2.4.1.3#10 | The Remote Rx Header Buffer Credit Count or Remote Type 1/Type 2 Rx Header Buffer Credit Count shall not be changed when a header packet is retried following LRTY. | NT/BC  |
|  Subsection reference: 7.2.4.1.4 Deferred DPH  |   |   |
|  7.2.4.1.4#1 | The Deferred DPH shall be treated as a TP for buffering and credit purposes. | NT  |
|  Subsection reference: 7.2.4.1.5 Receiving Header Packets  |   |   |
|  7.2.4.1.5#1 | A port receiving a header packet shall send an LGOOD_n when the CRC-5 is valid, the CRC-16 is valid, the Header Sequence Number matches, and an Rx Header Buffer is available to store it. | BC  |
|  7.2.4.1.5#2 | In SuperSpeed operation, a port shall consume one Rx Header Buffer until it has been processed. | BC  |
|  7.2.4.1.5#3 | In SuperSpeedPlus operation, a port shall consume one Type 1 Rx Header Buffer until it has been processed. | BC  |
|  7.2.4.1.5#4 | If the header packet has one or more CRC-5 or CRC-16 errors, a port shall issue a single LBAD and ignore all subsequent header packets received until an LRTY has been received or the link has entered Recovery. | BC  |
|  7.2.4.1.5#5 | If the Header Sequence Number in the received header packet does not match the Rx Header Sequence Number or a port does not have an Rx Header Buffer available to store the packet, the port shall transition to Recovery. | 7.13  |
|  7.2.4.1.5#6 | In SuperSpeed operation, after transmitting LBAD, a port shall continue to issue LCRD_x if an Rx Header Buffer Credit is made available. | 7.7  |
|  7.2.4.1.5#7 | In SuperSpeedPlus operation, after transmitting LBAD, a port shall continue to issue LCRD1_x/LCRD2_x if its respective Type 1/Type 2 Rx Buffer Credit is made available. | 7.7  |