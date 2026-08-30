Chapter 5: Test Descriptions

1/17/2018

### TD.7.35 Exit U3 by Reset Test (Downstream Port Only)

This test verifies that a downstream port instructed to Reset during U3 initiates a Warm Reset.

# Covered Assertions

7.2.4.2.4#1,4,5

7.5.9.2#2

# Overview of Test Steps

1. Perform the Link Initialization Sequence to bring the LVS and PUT link to U0.
2. The LVS software prompts the test operator to Suspend the PUT to U3 through USB30CV.
3. The LVS waits to receive an LGO_U3 from the PUT.
4. The LVS sends an LAU when it receives an LGO_U3 from the PUT.
5. The LVS waits to receive an LPMA from the PUT.
6. The test fails if any of the following occur:

a. The LVS does not receive an LGO_U3
b. The LVS does not receive an LPMA before PM_ENTRY_TIMER deadline.
c. The PUT fails to transition to U3 after PM_ENTRY_TIMER expires.

7. The LVS prompts the test operator to Reset the PUT through USB30CV and then hit "OK" on the prompt.
8. The LVS waits to receive a Warm Reset LFPS from PUT.
9. The test fails if no Warm Reset LFPS is received by the LVS before the test operator hits "OK".
10. When the LVS receives a Warm Reset LFPS the prompt is closed automatically.
11. The LVS transitions to Rx.Detect.Reset for the duration of the Warm Reset LFPS.
12. The LVS transitions to Rx.Detect and the LVS and PUT transition through Polling to U0.
13. The LVS will keep the link active by sending Link Pollings (LUP when it is configured as an Upstream Port or LDN when it is configured as a Downstream Port) for 50ms.
14. The test passes after the Port Configuration exchange is successful and the link stays in U0 for 50ms.

### TD.7.36 Exit U3 Test (Host Downstream Port Only)

This test verifies that a downstream port initiates U3 exit with a U3 exit LFPS.

Note: This test is performed on host silicon only. This test is not performed on end products. The operator must install the Product-Specific host controller driver to perform this test. It cannot be tested with the Compliance driver. The LVS is configured to appear to the host controller as a device.

# Covered Assertions

7.2.4.2.4#1,4,5

7.2.4.2.7#1

7.5.9.1#4

7.5.9.2#5

88

USB 3.1 Link Layer Test Specification