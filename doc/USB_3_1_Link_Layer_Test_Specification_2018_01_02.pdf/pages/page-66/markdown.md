Chapter 5: Test Descriptions

1/17/2018

# Covered Assertions

(No Physical Layer assertions defined)

# Overview of Test Steps

1. Configure the LVS with an SSC clock of -5300ppm.
2. Bring the link to U0 using the Link Initialization Sequence.
3. The test passes if the Link Initialization Sequence passes.
4. Repeat the above steps with an SSC clock of +300ppm.

# TD.6.4 LFPS Frequency Test

This test verifies that the PUT's LFPS detector supports the required frequency range. The periods to be tested are:

A. tPeriod = 10 MHz (min)
B. SS: tPeriod = 50 MHz, SSP: tPeriod = 40 MHz (max)

# Covered Assertions

(No Physical Layer assertions defined)

# Overview of Test Steps

1. The LVS and the PUT go through the initial steps of the LTSSM (eSS.Disabled, Rx.Detect) to reach Polling.LFPS.
2. The LVS will start generating a Polling.LFPS signal having durations of tBurst = 1 us and tRepeat = 10 us. The burst period will be set to the first period listed above.
3. The test passes if the PUT moves successfully to Polling.RxEQ according to section 7.5.4.3.2 of the USB 3.1 specification.
4. Repeat the steps with the other period listed above.

# TD.6.5 Polling.LFPS Duration Test

This test verifies that the PUT's Polling.LFPS detector supports the required duration range. Here are the durations to be tested:

A. tBurst = 0.6 us and tRepeat = 6 us
B. tBurst = 0.6 us and tRepeat = 14 us
C. tBurst = 1.4 us and tRepeat = 6 us
D. tBurst = 1.4 us and tRepeat = 14 us

# Covered Assertions

(No Physical Layer assertions defined)

# Overview of Test Steps

1. The LVS and the PUT go through the initial steps of the LTSSM (eSS.Disabled, Rx.Detect) to reach Polling.LFPS.
2. The LVS will start generating a Polling.LFPS signal having the first duration specified in the list above.

58

USB 3.1 Link Layer Test Specification