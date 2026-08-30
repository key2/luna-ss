|   | CRC-32 is valid, no K-symbol occurrence is detected, no 8b/10b error is detected and it is received immediately after its DPH. |   |
| --- | --- | --- |
|  7.2.4.1.6#3 | A port shall ignore a DPP when valid DPPSTART and DPPEND are detected and the CRC-32 check fails, there are less than four symbols, there are more than 1028 symbols, any K-symbol occurrence is detected, any 8b/10b error is detected or it is not preceded immediately by its DPH. | NT  |
|  Subsection reference: 7.2.4.1.10 Receiving LGOOD_n  |   |   |
|  7.2.4.1.10#1 | If a port receives an LGOOD_n and this LGOOD_n is not Header Sequence Number Advertisement, is shall transition to Recovery if the received Header Sequence Number does not match the ACK Tx Header Sequence Number. The ACK Tx Header Sequence Number shall be unchanged. | 7.14  |
|  Subsection reference: 7.2.4.1.11 Receiving LCRD_x/LCRD1_x/LCRD2_x  |   |   |
|  7.2.4.1.11#1 | A port shall transition to Recovery if it receives an out of order LCRD_x/LCRD1_x/LCRD2_x. | 7.15  |
|  Subsection reference: 7.2.4.1.12 Receiving LBAD  |   |   |
|  7.2.4.1.12#1 | Upon receiving LBAD, a port shall send a single LRTY before retransmitting all the header packets in the (Type 1/Type 2) Tx Header Buffers that have not been acknowledged with LGOOD_n. | 7.8  |
|  7.2.4.1.12#2 | A hub shall set the DL bit in the Link Control Word on all resent header packets and recalculate the CRC-5. | LVS  |
|  7.2.4.1.12#3 | When retransmitting a DP in SuperSpeed operation, a hub shall drop the DPP. When retransmitting a DP in SuperSpeedPlus operation, a hub shall drop the DPP and replace it with a nullified DPP. | IOP  |
|  7.2.4.1.12#4 | Upon receipt of an LBAD, a port shall send a single LRTY if there is no unacknowledged header packet in the (Type 1/Type 2) Tx Header Buffers. | 7.8  |
|  Subsection reference: 7.2.4.1.13 Transmitting Timers  |   |   |
|  7.2.4.1.13#1 | The PENDING_HP_TIMER shall be started when a port enters U0 in expectation of the Header Sequence Number Advertisement. | 7.26  |
|  7.2.4.1.13#2 | The PENDING_HP_TIMER shall be started when the oldest header packet is retransmitted in response to LBAD. | 7.8  |
|  7.2.4.1.13#3 | The PENDING_HP_TIMER shall be started when a header packet is transmitted and there are no prior header packets transmitted but unacknowledged in the (Type 1/Type 2) Tx Header Buffers. | 7.11  |
|  7.2.4.1.13#4 | The PENDING_HP_TIMER shall be reset and restarted when a header packet is acknowledged with LGOOD_n and there are | 7.9  |