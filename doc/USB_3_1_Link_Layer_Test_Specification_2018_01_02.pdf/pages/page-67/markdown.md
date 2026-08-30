Chapter 5: Test Descriptions

1/17/2018

3. The test passes if the PUT moves successfully to Polling.RxEQ according to section 7.5.4.3.2, and if the Polling.LFPS tPeriod, tBurst and tRepeat from the PUT are within the ranges specified in section 6.9.1.
4. Repeat the steps with the other durations listed above.

### TD.6.6 SCD Duration Test (Gen 2 Capable Only)

This test verifies that the PUT's Polling.LFPS detector supports the required duration range for SCD signals. Here are the durations to be tested:

A. tBurst = 0.6 us and '0' tRepeat = 6 us and '1' tRepeat = 11 us
B. tBurst = 0.6 us and '0' tRepeat = 6 us and '1' tRepeat = 14 us
C. tBurst = 0.6 us and '0' tRepeat = 9 us and '1' tRepeat = 11 us
D. tBurst = 0.6 us and '0' tRepeat = 9 us and '1' tRepeat = 14 us
E. tBurst = 1.4 us and '0' tRepeat = 6 us and '1' tRepeat = 11 us
F. tBurst = 1.4 us and '0' tRepeat = 6 us and '1' tRepeat = 14 us
G. tBurst = 1.4 us and '0' tRepeat = 9 us and '1' tRepeat = 11 us
H. tBurst = 1.4 us and '0' tRepeat = 9 us and '1' tRepeat = 14 us

### Covered Assertions

(No Physical Layer assertions defined)

### Overview of Test Steps

1. The LVS and the PUT go through the initial steps of the LTSSM (eSS.Disabled, Rx.Detect) to reach Polling.LFPS.
2. The LVS will start generating a Polling.LFPS SCD1 signal having the A parameters specified in the list above.
3. The LVS verifies that:
  a. The PUT moves successfully to Polling.LFPSPlus according to section 7.5.4.3.2.
  b. The SCD1 Polling.LFPSs transmitted from the PUT have tPeriod, tBurst, and tRepeat within the ranges specified in spec sections 6.9.1 and 6.9.4.1.
4. The LVS will generate Polling.LFPS SCD2 signals having the A parameters specified in the list above.
5. The test passes if the PUT moves successfully to Polling.PortMatch according to section 7.5.4.4.2, and if the SCD2 Polling.LFPSs transmitted from the PUT have tPeriod, tBurst and tRepeat within the ranges specified in section 6.9.1 and 6.9.4.1.
6. Repeat the steps with the other parameters listed above.

### TD.6.7 PWM Duration Test (Gen 2 Capable Only)

This test verifies that the PUT's Polling.LFPS detector supports the required duration range for PWM signals. Here are the durations to be tested:

A. tPWM = 2 us and tLFPS-0 = 0.5 us and tLFPS-1 = 1.33 us
B. tPWM = 2 us and tLFPS-0 = 0.5 us and tLFPS-1 = 1.8 us
C. tPWM = 2 us and tLFPS-0 = 0.8 us and tLFPS-1 = 1.33 us
D. tPWM = 2 us and tLFPS-0 = 0.8 us and tLFPS-1 = 1.8 us
E. tPWM = 2.4 us and tLFPS-0 = 0.5 us and tLFPS-1 = 1.33 us
F. tPWM = 2.4 us and tLFPS-0 = 0.5 us and tLFPS-1 = 1.8 us

59

USB 3.1 Link Layer Test Specification