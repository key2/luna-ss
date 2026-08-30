Chapter 5: Test Descriptions

1/17/2018

G. tPWM = 2.4 us and tLFPS-0 = 0.8 us and tLFPS-1 = 1.33 us
H. tPWM = 2.4 us and tLFPS-0 = 0.8 us and tLFPS-1 = 1.8 us

# Covered Assertions

(No Physical Layer assertions defined)

# Overview of Test Steps

1. The LVS and the PUT go through the initial steps of the LTSSM (eSS.Disabled, Rx.Detect) to reach Polling.PortMatch.
2. The LVS will generate LBPM signals having the A parameters specified in the list above.
3. The LVS verifies that:

a. The PUT moves successfully to Polling.PortConfig according to section 7.5.4.5.2.
b. The PWM LFPSs transmitted from the PUT have tPWM, tLFPS-0, and tLFPS-1 within the ranges specified in spec sections 6.9.1 and 6.9.5.1.

4. The LVS will generate LBPM signals having the A parameters specified in the list above.
5. The test passes if the PUT moves successfully to Polling.RxEQ according to section 7.5.4.6.2, and if the PWM LFPSs transmitted from the PUT have tPWM, tLFPS-0 and tLFPS-1 within the ranges specified in section 6.9.1 and 6.9.4.1.
6. Repeat the steps with the other parameters listed above.

### 5.3 Link Layer

#### TD.7.1 Link Bring-up Test

This test verifies that the Link Verification System (LVS) and the Port under Test (PUT) can reach U0 successfully.

As the test progresses it is divided into four subtests. Ports with Gen 1 capability and not Gen 2 capability must be tested with subtests 1 and 2. Ports with Gen 2 capability must be tested with subtests 3, 4 and 5.

# Covered Assertions

Refer to the list of covered assertions for the Link Initialization Sequence

# Overview of Test Steps

1. The LVS starts the link process.

- If the LVS is configured as a Downstream Port, the LVS asserts VBUS. The PUT should move from eSS.Disabled to Rx.Detect.
- If the LVS is configured as an Upstream Port, the LVS asserts Terminations. The PUT should already be in Rx.Detect.

2. The test fails if the PUT does not transmit Polling.LFPS bursts before tRxDetectQuietTimeout + tPollingLFPSEstablishedTimeout expires.

# Continue to Required Subtest

60

USB 3.1 Link Layer Test Specification