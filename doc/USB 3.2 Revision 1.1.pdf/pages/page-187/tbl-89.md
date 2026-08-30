|  Error Type | Description/Example | Error Recovery Path | Update Link Error Count? | Update Soft Error Count? (SuperSpeedPlus USB)  |
| --- | --- | --- | --- | --- |
|  Header Sequence Number Advertisement Error | LGOOD_n not received upon PENDING_HP_TIMER timeout. A header packet received before sending LGOOD_n. LCRD_x or LCRD1_x/LCRD2_x or LGO_Ux received before receiving LGOOD_n. | Recovery | Yes | No  |
|  Rx Header Buffer Credit Advertisement Error (SuperSpeed USB) | LCRD_x not received upon CREDIT_HP_TIMER timeout. A header packet received before sending LCRD_x. LGO_Ux received before receiving LCRD_x. | Recovery | Yes | No  |
|  Type 1/Type 2 Rx Buffer Credit Advertisement Error (SuperSpeedPlus USB) | LCRD1_x/LCRD2_x not received upon Type 1/Type 2 CREDIT_HP_TIMER timeout. A packet received before sending LCRD1_x/LCRD2_x. LGO_Ux received before receiving LCRD1_x/LCRD2_x. | Recovery | Yes | No  |
|  Training Sequence Error | Timeout from Polling to Rx.Detect or eSS.Disabled without reaching U0. Timeout from Recovery to eSS.Inactive without reaching U0. Timeout from Recovery to Rx.Detect without reaching U0. Timeout from Polling.Active or Polling.Configuration to Polling.PortMatch (SuperSpeedPlus USB only) | Timeout from Recovery to eSS.Inactive requires software intervention. | No | No  |
|  Invalid link command | Valid link command framing but invalid link command word. | Ignored | No | Yes  |
|  Missing link command | No valid link command framing is detected. | Delayed transition to Recovery if missing LGOOD_n or LCRD_x or LCRD1_x/LCRD2_x | Yes | No  |
|  8b/10b Error (Gen 1) | Detected in the PHY layer | N.A. | No | N.A.  |
|  Gen 2x1 Block Header Single-bit Error | Detected and corrected in PHY layer | Correctable | No | Yes  |