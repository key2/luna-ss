Chapter 5: Test Descriptions

1/17/2018

7.5.3.3.1#1

7.5.10.3.2#5

10.3.1.6#6

# Overview of Test Steps

1. Perform the Link Initialization Sequence to bring the LVS and PUT link to U0.
2. The LVS software prompts the test operator to initiate a Hot Reset on the PUT through USB30CV.
3. The LVS waits for the PUT to send TS1s.
4. The test fails if the TS1 Ordered Sets have the Reset bit set.
5. The LVS does not transmit anything in response to the PUT.
6. The test fails if the PUT does not transmit a Warm Reset LFPS after tRecoveryActiveTimeout expires.
7. The LVS responds to the Warm Reset LFPS by entering Rx.Detect.
8. The LVS and PUT perform the Link Initialization Sequence to bring the link to U0.
9. The LVS will keep the link active by sending Link Pollings (LUP when it is configured as an Upstream Port or LDN when it is configured as a Downstream Port) for 50ms.
10. The test passes if the exchanges are successful, the PUT initiates a Warm Reset LFPS after tRecoveryActiveTimeout in Recovery.Active and the link reaches U0 with a correct Port Configuration Transaction and stays there for at least 50ms.

# TD.7.32 Warm Reset Rx.Detect Timeout Test (Hub Downstream Port Only)

This test has been deleted. The assert has been covered in TD 10.109.

# TD.7.33 Exit Compliance Mode Test (Upstream Port Only)

This test verifies that a device exits Compliance Mode when it receives a Warm Reset LFPS.

# Covered Assertions

7.4.2#9

7.5.4.3.2#1

7.5.5.1#2

7.5.5.2#2

# Overview of Test Steps

1. The LVS makes sure VBUS is off to assure a PowerOn Reset.
2. The LVS prompts the test operator to power cycle a self-powered device.
3. The LVS turns on VBUS, bringing the link to Rx.Detect.
4. The LVS presents Terminations and waits for the PUT to present Terminations.
5. When the LVS detects Terminations from the PUT, the LVS starts a timer for tPollingLFPSTimeout and does not transmit an LFPS.

86

USB 3.1 Link Layer Test Specification