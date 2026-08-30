|  Error Type | Description/Example | Error Recovery Path | Update Link Error Count? | Update Soft Error Count? (SuperSpeedPlus USB)  |
| --- | --- | --- | --- | --- |
|  Training Sequence Error | 1. Timeout from Polling to Rx.Detect or eSS.Disabled without reaching U0. 2. Timeout from Recovery to eSS.Inactive without reaching U0. 3. Timeout from Recovery to Rx.Detect without reaching U0. 4. Timeout from Polling.Active or Polling.Configuration to Polling.PortMatch (SuperSpeedPlus USB only) | Timeout from Recovery to eSS.Inactive requires software intervention. | No | No  |
|  Invalid link command | Valid link command framing but invalid link command word. | Ignored | No | Yes  |
|  Missing link command | No valid link command framing is detected. | Delayed transition to Recovery if missing LGOOD_n or LCRD_x or LCRD1_x/LCRD2_x | Yes | No  |
|  8b/10b Error (SuperSpeed USB) | Detected in the PHY layer | N.A. | No | N.A.  |
|  128b/132b Soft Error (SuperSpeedPlus USB) | Detected and corrected in PHY layer | Correctable | No | Yes  |
|  128b/132b Two-bit Error (SuperSpeedPlus USB) | Detectable | Recovery | Yes | No  |
|  Single Bit SKP/SKPEND Error (SuperSpeedPlus USB) | Detectable | Correctable | No | Yes  |