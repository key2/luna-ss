|   | asserted to sending the TS2 ordered sets with the Reset bit de-asserted. |   |
| --- | --- | --- |
|  7.5.12.3.1#3 | An upstream port shall transmit TS2 ordered sets with the Reset bit asserted while performing the Hot Reset. | 7.27-28  |
|  7.5.12.3.1#4 | An upstream port shall transmit TS2 ordered sets with the Reset bit de-asserted after completing the Hot Reset. | 7.27-28  |
|  Subsection reference: 7.5.12.3.2 Exit from Hot Reset.Active  |   |   |
|  7.5.12.3.2#1 | The port shall transition to Hot Reset.Exit when the following three conditions are met: - At least 16 TS2 ordered sets with the Reset bit asserted are transmitted. - Two consecutive TS2 ordered sets are received with the Reset bit de-asserted. - Four consecutive TS2 ordered set with the Reset bit de-asserted are sent after receiving one TS2 ordered set with the Reset bit de-asserted. | 7.27-29  |
|  7.5.12.3.2#2 | The port shall transition from Hot Reset.Active to eSS.Inactive upon the 12-ms timer timeout if the conditions to transition to Hot Reset.Exit are not met. | NT  |
|  7.5.12.3.2#3 | A downstream port shall transition from Hot Reset.Active to Rx.Detect when directed to issue Warm Reset. | NT  |
|  7.5.12.3.2#4 | An upstream port shall transition from Hot Reset.Active to Rx.Detect when Warm Reset is detected. | NT  |
|  Subsection reference: 7.5.12.4 Hot Reset.Exit  |   |   |
|  Subsection reference: 7.5.12.4.1 Hot Reset.Exit Requirements  |   |   |
|  7.5.12.4.1#1 | A port in SuperSpeed operation shall transmit idle symbols in Hot Reset.Exit. | 7.27-29  |
|  7.5.12.4.1#2 | A port in SuperSpeedPlus operation shall transmit a single SDS ordered set before the start of the data block with Idle Symbols. | 7.27-29  |
|  7.5.12.4.1#3 | The port shall be able to receive the Header Sequence Number Advertisement from its link partner in Hot Reset.Exit. | NT  |
|  Subsection reference: 7.5.12.4.2 Exit from Hot Reset.Exit  |   |   |
|  7.5.12.4.2#1 | The port shall transition from Hot Reset.Exit to U0 when the following two conditions are met: - Eight consecutive Idle Symbols are received. - Sixteen Idle Symbols are sent after receiving one Idle Symbol. | 7.27-29  |
|  7.5.12.4.2#2 | The port shall transition from Hot Reset.Exit to eSS.Inactive upon the 2-ms timer timeout if the conditions to transition to U0 are not met. | NT  |