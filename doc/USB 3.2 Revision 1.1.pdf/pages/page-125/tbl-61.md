|  Symbol | Parameter | Gen 1 (5.0 GT/s) | Gen 2 (10 GT/s) | Units | Comments  |
| --- | --- | --- | --- | --- | --- |
|  V_{RX-DIFF-PP-POST-EQ} | Differential Rx peak-to-peak voltage | 30 (min) | 30 (min) | mV | Measured after the Rx EQ function (Section 6.8.2).  |
|  t_{RX-TJ} | Max Rx inherent timing error | 0.45 (max) | 0.394 (max) | UI | Measured after the Rx EQ function (Section 6.8.2).  |
|  t_{RX-DJ-DD} | Max Rx inherent deterministic timing error | 0.285 (max) | 0.21 (max) | UI | Maximum Rx inherent deterministic timing error  |
|  C_{RX-PARASITIC} | Rx input capacitance for return loss | 1.1 (max) | 1.0 (max) | pF |   |
|  V_{RX-CM-AC-P} | Rx AC common mode voltage | 150 (max) | 150 (max) | mV Peak | Measured at Rx pins into a pair of 50 Ω terminations into ground. Includes Tx and channel conversion, AC range up to 5 GHz  |
|  V_{RX-CM-DC-ACTIVE-IDLE-DELTA_P} | Rx AC common mode voltage during the U1 to U0 transition | 200 (max) | 200 (max) | mV Peak | Measured at Rx pins into a pair of 50 Ω terminations into ground. Includes Tx and channel conversion, AC range up to 5 GHz  |
|  V_{RX-CM-DC-CONN} (See notes 1 and 2) | Instantaneous DC common mode voltage coupled from the far-end Tx | -0.5 (min1) -0.3 (min2) 1.0 (max) | -0.5 (min1) -0.3 (min2) 1.0 (max) | V | Apply to all link states and during power-on, and power off. (min1, max) is observed at receiver side of the connector when Rx termination is equivalent of 200 KΩ, and (min2, max) when Rx termination is 50 Ω.  |