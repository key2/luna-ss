Chapter 5: Test Descriptions

1/17/2018

6. When the timer expires, the LVS verifies that the device is in Compliance Mode by sending Ping.LFPS until it can verify that the LVS is receiving a Compliance Pattern, (at most by the COMs in the 4th Compliance Pattern).
7. The test fails if the LVS cannot verify a Compliance Pattern coming from the PUT.
8. The LVS transmits a Reset.LFPS and enters Rx.Detect.
9. The LVS and PUT perform the Link Initialization Sequence to bring the LVS and PUT link to U0.
10. The LVS will keep the link active by sending Link Pollings (LUP when it is configured as an Upstream Port or LDN when it is configured as a Downstream Port) for 50ms.
11. The test passes if all exchanges are successful and the PUT stays in U0 for 50ms.

### TD.7.34 Exit Compliance Mode Test (Downstream Port Only)

This test verifies that a downstream port instructed to Reset while in Compliance Mode initiates a Warm Reset.

### Covered Assertions

7.4.2#9

7.5.4.3.2#2

7.5.5.1#2

7.5.5.2#1

### Overview of Test Steps

1. The LVS prompts the test operator to enable Compliance Mode through USB30CV. CV will send SetPortFeature(PORT_LINK_STATE) = Compliance Mode for the PUT.
2. The LVS presents termination to the PUT.
3. When the LVS detects VBUS and Terminations from the PUT, the LVS starts a timer for tPollingLFPSTimeout and does not transmit an LFPS.
4. When the timer expires, the LVS verifies that the device is in Compliance Mode by sending Ping.LFPS until it can verify that the LVS is receiving a Compliance Pattern, (at most by the COMs in the 4th Compliance Pattern).
5. The test fails if the LVS cannot verify a Compliance Pattern coming from the PUT.
6. The LVS prompts the test operator to Reset the PUT through USB30CV and then hit "OK".
7. The LVS waits to receive a Warm Reset LFPS from PUT.
8. The test fails if the LVS does not receive a Warm Reset LFPS before the test operator hits "OK"
9. The LVS closes the prompt automatically when it receives a Warm Reset LFPS.
10. The LVS transitions to Rx.Detect.Reset for the duration of the Warm Reset LFPS.
11. The LVS transitions to Rx.Detect and the LVS and PUT transition through Polling to U0.
12. The LVS will keep the link active by sending Link Pollings (LUP when it is configured as an Upstream Port or LDN when it is configured as a Downstream Port) for 50ms.
13. The test passes after the Port Configuration exchange is successful and the link stays in U0 for 50ms.

87

USB 3.1 Link Layer Test Specification