Revision 1.1
June 2022

- 84 -

Universal Serial Bus 3.2
Specification

### 6.7.2 Low Power Transmitter

In addition to the full swing transmitter specification, an optional low power swing transmitter is also specified for SuperSpeed applications. A low power swing transmitter is typically used in systems that are sensitive to power and noise interference, and have a relatively short channel. The requirement as to whether a transmitter needs to support full swing, low power swing, or both swings, is dependent on its usage model. All SuperSpeed transmitters must support full swing, while support for low power swing is optional. The method by which the output swing is selected is not defined in the specification, and is implementation specific.

While two different transmitters are specified, only a single receiver specification is defined. This implies that receiver margins (as specified in Table 6-22) shall be met if a low power transmitter is used.

### 6.7.3 Transmitter Eye

The eye mask is measured using the compliance data patterns as described in Section 6.4.3.2. The transmitter compliance test for Gen 1 uses compliance patterns CP0 and CP1 for TJ and RJ, respectively. The transmitter compliance test for Gen 2 uses compliance patterns CP9 and CP10 for TJ and RJ, respectively. Eye height is measured for 10⁶ consecutive UI. Jitter is extrapolated from 10⁶ UI to 10⁻¹² BER.

Table 6-20. Normative Transmitter Eye Mask at Test Point TP4

[tbl-57.md](tbl-57.md)

Notes:

1. Measured over 10⁶ consecutive UI and extrapolated to 10⁻¹² BER.

2. Measured after receiver equalization function.

3. Measured at end of reference channel and cables at TP4 in Figure 6-20.

4. The eye height is to be measured at the minimum opening over the range from the center of the eye ± 0.05 UI.

5. The Rj specification is calculated as 14.069 times the RMS random jitter for 10⁻¹² BER.

6. Measured at the output of the compliance breakout board without embedding the compliance cable and load board.

The compliance testing setup is shown in Figure 6-20. All measurements are made at the test point (TP4), and the Tx specifications are applied after processing the measured data with the compliance reference equalizer transfer function described in the next section.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.