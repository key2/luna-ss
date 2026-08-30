|  Symbol | Parameter | 5.0 GT/s | 10 GT/s | Units | Comments  |
| --- | --- | --- | --- | --- | --- |
|  t_{MIN-PULSE-Dj} | Deterministic min pulse | 0.96 | 0.96 | UI | Tx pulse width variation that is deterministic  |
|  t_{MIN-PULSE-Tj} | Tx min pulse | 0.90 | 0.90 | UI | Min Tx pulse at 10^{-12} including Dj and Rj  |
|  t_{TX-EYE} | Transmitter Eye | 0.625 (min) | 0.646 (min) | UI | Includes all jitter sources  |
|  t_{TX-Dj-DD} | Tx deterministic jitter | 0.205 (max) | 0.170 (max) | UI | Deterministic jitter only assuming the Dual Dirac distribution  |
|  C_{TX-PARASITIC} | Tx input capacitance for return loss | 1.25 (max) | 1.1 (max) | pf | Parasitic capacitance to ground  |
|  R_{TX-DC} | Transmitter DC common mode impedance | 18 (min) 30 (max) | 18 (min) 30 (max) | Ω | DC impedance limits to guarantee Receiver detect behavior. Measured with respect to AC ground over a voltage of 0-500 mV.  |
|  I_{TX-SHORT} | Transmitter short-circuit current limit | 60 (max) | 60 (max) | mA | The total current Transmitter can supply when shorted to ground.  |
|  V_{TX-CM-AC-PP_ACTIVE} | Tx AC common mode voltage active | 100 | 100 (max) | mV (p-p) | Maximum mismatch from Txp + Txn for both time and amplitude.  |
|  V_{TX-CM-DC-ACTIVE-IDLE-DELTA} | Absolute DC Common Mode Voltage between U1 and U0 | 200 (max) | 200 (max) | mV |   |
|  V_{TX-IDLE-DIFF-AC-PP} | Electrical Idle Differential Peak -Peak Output Voltage | 0 (min) 10 (max) | 0 (min) 10 (max) | mV |   |
|  V_{TX-IDLE-DIFF-DC} | DC Electrical Idle Differential Output Voltage | 0 (min) 10 (max) | 0 (min) 10 (max) | mV | Voltage shall be low pass filtered to remove any AC component. This limits the common mode error when resuming U1 to U0.  |