Chapter 5: Test Descriptions

1/17/2018

# Covered Assertions

7.2.1.3#1,2

# Overview of Test Steps

5. Do steps 1 to 4 of the Link Initialization Sequence.
6. The LVS will keep the link active by sending Link Pollings (LUP when it is configured as an Upstream Port or LDN when it is configured as a Downstream Port) for 50ms. All data blocks will be generated according to Condition A described above.
7. At this stage the Downstream Port is expected to issue a GetDeviceDescriptor request.

a. If the LVS is configured as an Upstream Port:

i. The LVS prompts the test operator to have the PUT send a GetDeviceDescriptor request through USB30CV and then press “OK”.
ii. The test fails if no GetDeviceDescriptor request is received and the test operator has pressed “OK”.
iii. When the LVS receives a GetDeviceDescriptor request, it closes the prompt, and responds to the request as appropriate.

b. If the LVS is configured as a Downstream Port, it will issue a GetDeviceDescriptor request, and complete the transaction as appropriate.

8. The test passes if the exchanges are successful, no timeout is detected, no recovery is entered, all packets are successfully received, all credits are restored and the link stays in U0 for at least 50ms.

9. Repeat the steps with the next combination listed above.

94

USB 3.1 Link Layer Test Specification