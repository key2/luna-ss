Chapter 5: Test Descriptions

1/17/2018

# Overview of Test Steps

1. Perform the Link Initialization Sequence.
2. At this stage the Downstream Port is expected to issue a GetDeviceDescriptor request.

▪ If the LVS is configured as an Upstream Port:

a. The LVS prompts the test operator to have the PUT send a GetDeviceDescriptor request through USB30CV and then press “OK”.
b. The test fails if no GetDeviceDescriptor request is received and the test operator has pressed “OK”.
c. When the LVS receives a GetDeviceDescriptor request, it closes the prompt. The LVS will respond to the request with a DPP containing the Device Descriptor data which includes the first framing error listed above.

▪ If the LVS is configured as a Downstream Port, it will issue a GetDeviceDescriptor request, but will send the SETUP DP with the first framing error listed above.

3. The LVS will keep the link active by sending Link Pollings (LUP when it is configured as an Upstream Port or LDN when it is configured as a Downstream Port) for 50ms.
4. The test fails if the data exchange fails on the protocol level.
5. The test passes if the exchanges are successful, no timeout is detected, no recovery is entered, all packets are successfully received by the PUT, all credits are restored and the link stays in U0 for at least 50ms.
6. Repeat for each condition listed above.

# TD.7.7 RX Header Packet Retransmission Test

This test verifies that the PUT will send an LBAD if an invalid header packet is received, and that the retransmission will be correctly handled.

The tested conditions invalidating a header packet are:

A. Incorrect CRC-16
B. Incorrect CRC-5
C. K28.2 SDP symbol in HP data
D. K28.3 EDB symbol in HP data
E. K28.4 SUB symbol in HP data
F. K28.6 Reserved K-symbol in HP data
G. K27.7 SHP symbol in HP data
H. K29.7 END symbol in HP data
I. K30.7 SLC symbol in HP data
J. K23.7 EPF symbol in HP data

Conditions C – J are tested for Gen 1 PUTs only. Each of the conditions C – J in the following positions, one case at a time:

1. Position 2: SHP SHP SHP EPF DX.X KX.X DX.X DX.X
2. Position 5: SHP SHP SHP EPF DX.X DX.X DX.X DX.X KX.X

# Covered Assertions

7.2.4.1.4#3, 4

67

USB 3.1 Link Layer Test Specification