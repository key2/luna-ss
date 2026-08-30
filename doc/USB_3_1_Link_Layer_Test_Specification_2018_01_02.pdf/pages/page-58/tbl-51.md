|  8.4.8.5#2 | If Delta(RxITP) is less than 7500, the device shall apply Delta(RxITP) and Correction(RxITP) values and the LDM Link Delay to set the value of the PTM Delta Counter at the time an ITP is received (tITUFP) using the formula shown (see section 8.4.8.5). | NT  |
| --- | --- | --- |
|  8.4.8.5#3 | If Delta(RxITP) is less than 7500, a device shall use the values of Bus Interval Counter(RxITP) and Delta(RxITP) subfields received in the ITP to set the value of the PTM But Interval Counter at the time an ITP is received (tITUFP) using the formula shown (see section 8.4.8.5). | NT  |
|  Subsection reference: 8.4.8.6 PTM Bus Interval Boundary Host Calculation  |   |   |
|  8.4.8.6#1 | A host shall maintain an ITP Delay Counter that is incremented by the PTM Clock. | NT  |
|  8.4.8.6#2 | The host shall transmit downstream ITPs using these current values for the ITP Isochronous Timestamp Bus Interval Counter(TxITP) and Delay(TxITP) fields, and set the Correction(TxITP) field to zero. | NT  |
|  Subsection reference: 8.4.8.7 PTM Hub ITP Regeneration  |   |   |
|  8.4.8.7#1 | A hub shall maintain an ITP Delay Counter that is incremented by the PTM Clock. | NT  |
|  8.4.8.7#2 | If an ITP is received by a PTM capable hub and the Delayed(DL) bit is not set, then the hub shall set the ITP Delay Counter to zero and for each downstream port in U0, the hub shall queue the ITP for transmission. | NT  |
|  8.4.8.7#3 | When a PTM capable hub transmits an ITP, it shall copy the value of Bus Interval Boundary(RxITP) to the BUS Interval Boundary(TxITP) subfield of the Isochronous Timestamp field in the downstream ITP. | NT  |
|  8.4.8.7#4 | When a PTM capable hub transmits an ITP, it shall calculate the value of Delta(TxITP) subfield using the formula shown (see section 8.4.8.7). | NT  |
|  8.4.8.7#5 | When a PTM capable hub transmits an ITP, it shall re-calculate the CRC-16 for the modified ITP. | NT  |
|  8.4.8.7#6 | If an ITP is received by a PTM capable hub and the Delayed (DL) bit is set, then the hub shall forward the received ITP without modification. | NT  |
|  8.4.8.7#7 | The Isochronous Timestamp values used in the ITP being transmitted shall be the values present at the time of transmission (not time queued for transmission but actual transmission, see section 8.4.8.6). | NT  |
|  Subsection reference: 8.4.8.9 LDM Rules  |   |   |
|  8.4.8.9#1 | A Responder shall not send a LDM Response without first receiving a LDM Request LMP. | NT  |