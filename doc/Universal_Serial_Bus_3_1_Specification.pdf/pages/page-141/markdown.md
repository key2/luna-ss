Mechanical

where NEXT(f) is the near-end crosstalk between the SuperSpeed Gen 2 signal pairs. The contribution of USB 2 D+/D- pair to SuperSpeed signal pairs is relatively small and is not included in IXT for simplicity.

More detailed discussion of ILfitatNq, IMR and IXT is given in a USB-IF whitepaper Establishing USB SuperSpeed Gen 2 Channel and Cable Assembly High Speed Compliance Specification. The USB-IF also provides a standard tool to convert measured cable assembly S-parameters into ILfitatNq, IMR and IXT.

### 5.6.1.3.2.4 Pass/Fail Criteria

SuperSpeed Gen 2 channel performance is based on ILfitatNq, IMR, and IXT. In general, a channel with more loss, more reflection, and more crosstalk has less margin. Channel margin is measured with BER (bit error ratio) eye height (eH) and eye width (eW) at BER=10⁻¹². The correlation between eH and eW and the channel metrics ILfitatNq, IMR, and IXT is established following the methodology described in the USB-IF whitepaper Establishing USB SuperSpeed Gen 2 Channel and Cable Assembly High Speed Compliance Specification. For each channel with a metrics ILfitatNq, IMR, and IXT, eH and eW is calculated:

$$eH = f_H (ILfitatNq, IMR, IXT) \tag{5-5}$$

$$eW = f_W (ILfitatNq, IMR, IXT)$$

Note that the effect of Tx and Rx equalization, jitter, and sampling noise is included in the eye height and eye width calculations. The pass/fail criteria are then expressed as

$$eH = f_H (ILfitatNq, IMR, IXT) > 0 \tag{5-6}$$

$$eW = f_W (ILfitatNq, IMR, IXT) > 0$$

and

$$ILfitatNq \ge -22 \text{ dB}$$

$$IMR \le 60 \text{ mV} \tag{5-7}$$

$$IXT \le 25 \text{ mV}$$

Equation (5-6) is an open-eye (at BER=10⁻¹²) requirement, while Equation (5-7) constrains the maximum channel loss, multi-reflection, and crosstalk. A SuperSpeed Gen 2 cable assembly is considered pass if both Equations (5-6) and (5-7) are satisfied. Figure 5-26 shows pass and fail examples.

5-53