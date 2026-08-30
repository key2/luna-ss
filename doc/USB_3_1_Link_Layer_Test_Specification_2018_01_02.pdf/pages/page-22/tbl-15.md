|   | still header packets transmitted but unacknowledged in the (Type 1/Type 2) Tx Header Buffers. |   |
| --- | --- | --- |
|  7.2.4.1.13#5 | The PENDING_HP_TIMER shall be reset and stopped when the Header Sequence Number Advertisement is received. | BC  |
|  7.2.4.1.13#6 | The PENDING_HP_TIMER shall be reset and stopped when a header packet acknowledgement of LGOOD_n is received and all the transmitted header packets in the (Type 1/Type 2) Tx Header Buffers are acknowledged. | BC  |
|  7.2.4.1.13#7 | The PENDING_HP_TIMER shall be reset and stopped when a header packet acknowledgement of LBAD is received. | 7.30  |
|  7.2.4.1.13#8 | A port in SuperSpeed operation shall transition to Recovery if the PENDING_HP_TIMER times out and the transmission of an outgoing header packet is completed or the transmission of an outgoing DPP is either completed with DPPEND or terminated with DPPABORT. | 7.11  |
|  7.2.4.1.13#9 | A port in SuperSpeedPlus operation shall transition to Recovery if the PENDING_HP_TIMER times out. | 7.11  |
|  7.2.4.1.13#10 | The (Type 1/Type 2) CREDIT_HP_TIMER shall be started when its respective packet or retried packet is sent, or when a port enters U0. | 7.12  |
|  7.2.4.1.13#11 | The (Type 1/Type 2) CREDIT_HP_TIMER shall be reset when its respective valid LCRD_x/LCRD1_x/LCRD2_x is received. | 7.10  |
|  7.2.4.1.13#12 | The (Type 1/Type 2) CREDIT_HP_TIMER shall be restarted if its respective valid LCRD_x/LCRD1_x/LCRD2_x is received and the respective Remote (Type 1/Type 2) Rx Buffer Credit Count is less than four. | NT  |
|  7.2.4.1.13#13 | A port in SuperSpeed operation shall transition to Recovery if the CREDIT_HP_TIMER times out and the transmission of an outgoing header packet is completed or the transmission of an outgoing DPP is either completed with DPPEND or terminated with DPPABORT. | 7.12  |
|  7.2.4.1.13#14 | A port in SuperSpeedPlus operation shall transition to Recovery if the Type 1 or Type 2 CREDIT_HP_TIMER times out. | 7.12  |
|  Subsection reference: 7.2.4.2.1 Power Management Link Timers  |   |   |
|  7.2.4.2.1#1 | A port shall start the PM_LC_TIMER after the last symbol of the LGO_Ux link command is sent. | 7.21  |
|  7.2.4.2.1#2 | A port shall disable and reset the PM_LC_TIMER upon receipt of the LAU or LXU. | 7.20  |
|  7.2.4.2.1#3 | A port shall start the PM_ENTRY_TIMER after the last symbol of the LAU is sent. | 7.22  |
|  7.2.4.2.1#4 | A port shall disable and reset the PM_ENTRY_TIMER upon receipt of an LPMA or a TS1 ordered set. | 7.23-25  |