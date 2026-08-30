Chapter 5: Test Descriptions

1/17/2018

13. The LVS and PUT continue the test with the Link Initialization Sequence starting at step two.

# Subtest 2 (TD 7.1.2):

1. The LVS transmits Polling.LFPS bursts with an SCD1 signature.
2. The test fails if a PUT that does not contain a captive re-timer does not transmit at least 16 Polling.LFPS bursts.
3. The LVS switches to regular Polling.LFPS bursts after transmitting 4 SCD1 and receiving 16 Polling.LFPS bursts, or after receiving 4 Polling.LFPS and tPollingSCDLFPSTimeout has expired – whichever comes first.
4. The test fails if any of the following occur:

a. The PUT does not transmit at least four consecutive Polling.LFPS bursts after receiving one Polling.LFPS burst (Note: The received Polling.LFPS burst may be part of an SCD1 from the LVS, or may be from a regular Polling.LFPS burst after the LVS transitions)
b. The PUT transitions away from Polling.LFPS before the LVS sends at least two consecutive Polling.LFPS bursts.
c. The PUT does not transition from Polling.LFPS before tPollingLFPSTimeout expires.

5. The test fails if the PUT has transmitted more than 6 LFPS after receiving 1 regular (non-SCD) Polling.LFPS burst and the Number of LFPS tx'd before receiving \(1 > 18\) - the Number of LFPS tx'd after receiving 1.
6. Continue to Subtest 1 (TD 7.1.1) step 5.

# Subtest 3 (TD 7.1.3)

1. The LVS transmits Polling.LFPS bursts.
2. The test fails if any of the following occur:

a. The PUT does not switch to SuperSpeed operation after transmitting 4 SCD1 and receiving 16 Polling.LFPS.
b. For a PUT with no captive re-timer, the PUT does not transmit 16 regular Polling.LFPS
c. The PUT does not transmit at least four consecutive regular Polling.LFPS bursts after receiving one Polling.LFPS burst.
d. For a PUT with no captive re-timer, the PUT does not transition to Polling.RxEQ after transmitting 16 regular Polling.LFPS.
e. For a PUT with a captive re-timer, the PUT does not transition to Polling.RxEQ after transmitting 4 regular Polling.LFPS.

3. Continue to Subtest 1 (TD 7.1.1) step 5.

# Subtest 4 (TD 7.1.4)

1. The LVS transmits Polling.LFPS bursts with an SCD1 signature.

62

USB 3.1 Link Layer Test Specification