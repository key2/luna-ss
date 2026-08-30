Chapter 5: Test Descriptions

1/17/2018

c. The PUT interrupts a TS1 Ordered Set to transmit a SKP or SYNC Ordered Set (between TS2 Ordered Sets is OK).
d. The PUT continues to transmit TS2 Ordered Sets after tPollingConfigurationTimeout expires.

16. The LVS transmits a single SDS Ordered Set and then data blocks with Idle Symbols.
17. The test fails if upon entering U0, the PUT does not transmit the Header Sequence Number Advertisement and the Type 1 and Type 2 Rx Header Buffer Credit Advertisements before their respective timeouts, PENDING_HP_TIMER and Type 1 and Type 2 CREDIT_HP_TIMERs, expire.
18. The LVS and PUT continue the Link Initialization Sequence starting at step two.

# Subtest 5 (TD 7.1.5)

1. The LVS waits to receive Polling.LFPS bursts (as components of the SCD1)
2. The LVS transmits four regular Polling.LFPS bursts and transitions to Polling.RxEQ
3. The test fails if any of the following occur:

a. The PUT does not switch to SuperSpeed operation and Polling.RxEQ state after tPollingSCDLFPSTimeout
b. The PUT does not continue to send Polling.LFPS up until tPollingSCDLFPSTimeout.

4. Continue to Subtest 1 (TD 7.01.1) step 5.

### TD.7.2 Link Commands Framings Robustness Test

This test verifies that the PUT can tolerate link commands having one symbol error in the LCSTART framing. Here are the combinations to be tested:

A. ERR SLC SLC EPF
B. SLC ERR SLC EPF
C. SLC SLC ERR EPF
D. SLC SLC SLC ERR

The Port Configuration transaction will be used for this purpose.

# Covered Assertions

7.3.4#1,2

# Overview of Test Steps

1. Perform the Link Initialization Sequence, but transmit all LCRD_X or LCRD1_X with an error in the first LCSTART symbol.
2. The test passes if the Link Initialization Sequence passes.
3. Repeat the above steps with an error in the second, third, and fourth LCSTART symbols as shown above.

64

USB 3.1 Link Layer Test Specification