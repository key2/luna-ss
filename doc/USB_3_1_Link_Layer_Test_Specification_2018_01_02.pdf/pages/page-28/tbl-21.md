|  Subsection reference: 7.3.7 Header Sequence Number Advertisement Error  |   |   |
| --- | --- | --- |
|  7.3.7#1 | A port shall transition to Recovery upon its PENDING_HP_TIMER timeout before the Header Sequence Number Advertisement is received. | 7.26  |
|  7.3.7#2 | A port shall transition to Recovery when a header packet is received before sending the Header Sequence Number Advertisement. | NT  |
|  7.3.7#3 | A port shall transition to Recovery when an LCRD_x or LCRD1_x/LCRD2_x or LGO_Ux is received before receiving the Header Sequence Number Advertisement. | NT  |
|  Subsection reference: 7.3.8 SuperSpeed Rx Header Buffer Credit Advertisement Error  |   |   |
|  7.3.8#1 | A port shall transition to Recovery upon its CREDIT_HP_TIMER timeout before the Header Buffer Credit Advertisement is received. | NT  |
|  7.3.8#2 | A port shall transition to Recovery when a header packet is received before sending the Header Buffer Credit Advertisement. | NT  |
|  7.3.8#3 | A port shall transition to Recovery when a LGO_Ux is received before receiving the Header Buffer Credit Advertisement. | NT  |
|  Subsection reference: 7.3.9 SuperSpeedPlus Type 1/Type 2 Rx Buffer Credit Advertisement Error  |   |   |
|  7.3.9#1 | A port shall transition to Recovery upon a Type 1/Type 2 CREDIT_HP_TIMER timeout and its respective LCRD1_x or LCRD2_x is not received. | NT  |
|  7.3.9#2 | A port shall transition to Recovery when a Type 1 packet is received before sending LCRD1_x, or a Type 2 packet is received before sending LCRD2_x. | NT  |
|  7.3.9#3 | A port shall transition to Recovery when LGO_Ux is received before receiving LCRD1_x or LCRD2_x. | NT  |
|  Subsection reference: 7.3.10 Training Sequence Error  |   |   |
|  7.3.10#1 | For SuperSpeedPlus operation, upon detecting a timeout in Polling.Active or Polling.Configuration, the port shall transition to Polling.PortMatch to negotiate for SuperSpeed operation. | 7.39  |
|  7.3.10#2 | For SuperSpeed operation, a downstream port shall transition to Rx.Detect when a Training Sequence error occurs during Polling and cPollingTimeout is less than two. | 7.40  |
|  7.3.10#3 | For SuperSpeed operation, a downstream port shall transition to eSS.Inactive when a Training Sequence error occurs during Polling and cPollingTimeout is two. | 7.40  |
|  7.3.10#4 | For SuperSpeed operation, an upstream port of a hub shall transition to Rx.Detect when a Training Sequence error occurs during Polling. | NT  |