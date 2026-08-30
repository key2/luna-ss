|   | • The four symbols are in the order defined in Table 7-9. |   |
| --- | --- | --- |
|  7.3.4.1#2 | Missing of a header packet shall result in a port transitioning to Recovery depending on which one of the following conditions becomes true first: • A port transmitting the header packet upon its PENDING_HP_TIMER timeout. • A port receiving the header packet upon detection of a Rx Header Sequence Number error. | 7.6 7.7  |
|  7.3.4.1#3 | Missing of a DPP framing ordered set in SuperSpeedPlus operation shall result in a port transitioning to Recovery. | 7.6  |
|  7.3.4.1#4 | The Link Error Count shall be incremented by one each time a transition to Recovery occurs. | NT  |
|  Subsection reference: 7.3.5 Link Commands Errors  |   |   |
|  7.3.5#1 | A port shall detect a link command when receiving a LCSTART framing with at least three valid symbols out of four in the correct order, and ignore the link command otherwise. | 7.2  |
|  7.3.5#2 | For SuperSpeed USB, a valid link command is declared if both link command words are the same, they both contain valid link command information as defined in Table 7-4 and they both pass CRC-5 check. | 5.1 7.2 7.3 7.4  |
|  7.3.5#2 | For SuperSpeedPlus USB, a valid link command is declared if both link command words are the same, they both contain valid link command information as defined in Table 7-4 and they both pass CRC-5 check, or if one of the link command words contains valid link command information and passes the CRC-5 check, and the other link command word either contains invalid link command information or fails the CRC-5 check. | 5.1 7.2 7.3 7.4  |
|  7.3.5#4 | A port shall transition to Recovery upon detection of an LGOOD_n ordering error. | 7.14  |
|  7.3.5#5 | A port shall transition to Recovery upon detection of an LCRD_x or LCRD1_x/LCRD2_x ordering error. | 7.15  |
|  7.3.5#6 | A port shall transition to Recovery upon its PM_LC_TIMER timeout. | 7.21  |
|  7.3.5#7 | A downstream port shall transition to Recovery upon detection of a missing LUP. | 7.16  |
|  7.3.5#8 | An upstream port shall transition to Recovery upon detection of a missing LDN | 7.16  |
|  Subsection reference: 7.3.6 ACK Tx Header Sequence Number Errors  |   |   |
|  7.3.6#1 | An ACK Tx Header Sequence Number error shall be declared when the Header Sequence Number in the received LGOOD_n does not match the ACK Tx Header Sequence Number. | 7.13  |