|  Symbol | Parameter | Gen 1 (5.0 GT/s) | Gen 2 (10 GT/s) | Units | Comments  |
| --- | --- | --- | --- | --- | --- |
|  UI | Unit Interval | 199.94 (min) 200.06 (max) | 99.97 (min) 100.03 (max) | ps | UI does not account for SSC caused variations.  |
|  R_{RX-DC} | Receiver DC common mode impedance | 18 (min) 30 (max) | 18 (min) 30 (max) | Ω | DC impedance limits are needed to guarantee Receiver detect. Measured with respect to ground over a voltage of 500 mV maximum.  |
|  R_{RX-DIFF-DC} | DC differential impedance | 72 (min) 120 (max) | 72 (min) 120 (max) | Ω |   |
|  Z_{RX-HIGH-IMP-DC-POS}^{1} | DC Input CM Input Impedance for V>0 during Reset or power down | 10k (min) | 10k (min) | Ω | Rx low frequency CM impedance with the Rx terminations not powered. Defined at the transmitter side of the AC cap as min(delta_V/delta_I) upon application of a positive Tx step of any size up to +500mV from steady state.  |
|  V_{RX-LFPS-DET-DIFFp-p} | LFPS Detect Threshold | 100 (min) 300 (max) | 100 (min) 300 (max) | mV | Below the minimum is noise. Must wake up above the maximum.  |
|  C_{RX-AC-COUPLING} | AC Coupling Capacitor | 297 (min) 363 (max) | 297 (min) 363 (max) | nF | Receivers may be AC coupled if desired. If used, the AC coupling is required to be either within the media or within the receiving component.  |