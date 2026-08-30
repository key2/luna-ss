|  7.2.4.1.4#1 | A port shall detect a header packet when receiving an HPSTART framing with at least three valid symbols out of four, and ignore the packet otherwise. | BC 7.5  |
| --- | --- | --- |
|  7.2.4.1.4#2 | A port receiving a header packet shall send a LGOOD_n when a valid HPSTART is detected, the CRC-5 is valid, the CRC-16 is valid, no K-symbol occurrence is detected and no 8b/10b error is detected. | BC  |
|  7.2.4.1.4#3 | A port receiving a header packet shall send an LBAD when a valid HPSTART is detected and either CRC-5 or CRC-16 checks fail. | 7.7  |
|  7.2.4.1.4#4 | A port receiving a header packet shall send an LBAD when a valid HPSTART is detected and any K-symbol occurrence is detected or any 8b/10b error is detected. | 7.7  |
|  7.2.4.1.5#8 | A port shall transition directly to Recovery if it fails to receive a header packet three consecutive times. A port shall not issue the third LBAD upon the third error. | 7.30  |
|  Subsection reference: 7.2.4.1.6 Receiving Data Packet Header in SuperSpeedPlus Operation  |   |   |
|  7.2.4.1.6#1 | A port shall accept a DPP and issue an LGOOD_n when the CRC-5 and CRC-16 are valid, the Header Sequence Number matches, and an Rx Buffer is available to store the packet. In this case a port shall ignore the length field replica. | BC  |
|  7.2.4.1.6#2 | A port shall consume one Type 1 or Type 2 Rx Buffer Credit until it has been processed and an Rx Buffer is available. | BC  |
|  7.2.4.1.6#3 | If the DPH has one or more CRC-5 or CRC-16 errors, but the two length field replica are valid and identical, a port shall issue a single LBAD and track the associated DPP that immediately follows the DPH. After issuing the LBAD, a port shall ignore all subsequent packets until an LRTY has been received or the link has entered Recovery. | NT  |
|  7.2.4.1.6#4 | If the header number in the received DPH does not match the Rx Header Sequence Number or the Rx Buffer does not have space to store the DP, or the two length field replica are not identical, the port shall enter Recovery. | NT  |
|  7.2.4.1.6#5 | After transmitting LBAD, a port shall continue to issue LCRD1_x or LCRD2_x if its corresponding Type 1 or Type 2 Rx Buffer Credit is made available. | NT  |
|  7.2.4.1.6#6 | A port shall transition directly to Recovery if it fails to receive a data packet header three consecutive times. A port shall not issue the third LBAD upon the third error. | NT  |
|  Subsection reference: 7.2.4.1.7 SuperSpeed Rx Header Buffer Credit  |   |   |
|  7.2.4.1.7#1 | A port shall consume one Local Rx Header Buffer Credit if a header packet is "received properly". The Local Rx Header Buffer Credit Count shall be decremented by one. | NT  |
|  7.2.4.1.7#2 | Upon completion of a header packet processing, a port shall restore a Local Rx Header Buffer Credit by sending a single | BC  |