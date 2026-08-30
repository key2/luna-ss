Chapter 5: Test Descriptions

1/17/2018

8. The test fails if the Port Configuration exchange sequences are not successful or the link does not stay in U0 for at least 50ms.

### TD.7.40 Polling Retry Test (Downstream Port Only)

This test verifies that the PUT recovers to Rx.Detect twice, and then eSS.Inactive when tPollingLFPSTimeout expires.

#### Covered Assertions

7.3.10#2,3

7.5.4.2#2

7.5.4.3.2#6,7

7.5.4.8.2#3,4

7.5.4.9.2#3

#### Overview of Test Steps

1. The LVS presents terminations and does not send any signal for the remainder of the test.
2. The test fails if the PUT does not transition to Polling.LFPS within 200ms.
3. For a PUT with a captive re-timer:

(1) The test fails if the PUT does not transition to Rx.Detect after 24 ms.
(2) The test fails if the PUT does not transition to Polling.LFPS within 8ms.
(3) The test fails if the PUT does not continue this cycle up to tPollingLFPSTimeout expiration.

4. The test fails if the PUT does not transition to Rx.Detect within tPollingLFPSTimeout expiration.
5. The test fails if the PUT does not transition to Polling.LFPS within 200ms.
6. For a PUT with a captive re-timer:

(1) The test fails if the PUT does not transition to Rx.Detect after 24 ms.
(2) The test fails if the PUT does not transition to Polling.LFPS within 8ms.
(3) The test fails if the PUT does not continue this cycle up to tPollingLFPSTimeout expiration.

7. The test fails if the PUT does not transition to Rx.Detect within tPollingLFPSTimeout expiration.
8. The test fails if the PUT does not transition to Polling.LFPS within 200ms.
9. For a PUT with a captive re-timer:

(1) The test fails if the PUT does not transition to Rx.Detect after 24 ms.
(2) The test fails if the PUT does not transition to Polling.LFPS within 8ms.
(3) The test fails if the PUT does not continue this cycle up to tPollingLFPSTimeout expiration.

10. The test fails if the PUT does not transition to eSS.Inactive within tPollingLFPSTimeout expiration.
11. If PUT is Gen 1, continue with the rest of the test steps.
12. The LVS removes terms for 200ms and presents terms.
13. The LVS and PUT transition through Polling.LFPS to Polling.Active.

92

USB 3.1 Link Layer Test Specification