|  Symbol | Parameter | Gen 1 (5.0 GT/s) | Gen 2 (10 GT/s) | Units | Comments  |
| --- | --- | --- | --- | --- | --- |
|  UI | Unit Interval | 199.94 (min) 200.06 (max) | 99.97 (min) 100.03 (max) | ps | UI does not account for SSC caused variations.  |
|  R_{RX-DC} | Receiver DC common mode impedance | 18 (min) 30 (max) | 18 (min) 30 (max) | Ω | DC impedance limits are needed to guarantee Receiver detect. Measured with respect to ground over a voltage of 500 mV maximum.  |
|  R_{RX-DIFF-DC} | DC differential impedance | 72 (min) 120 (max) | 72 (min) 120 (max) | Ω |   |
|  Z_{RX-HIGH-IMP-DC-POS}^{1} | DC Input CM Input Impedance for V>0 during Reset or power down | 25k (min) | 25k (min) | Ω | Rx DC CM impedance with the Rx terminations not powered, measured over the range 0 – 500 mV with respect to ground.  |
|  V_{RX-LFPS-DET-DIFFp-p} | LFPS Detect Threshold | 100 (min) 300 (max) | 100 (min) 300 (max) | mV | Below the minimum is noise. Must wake up above the maximum.  |