Chapter 5: Test Descriptions

1/17/2018

# Overview of Test Steps

1. Do steps 1 to 3 of the Link Initialization Sequence.
2. The LVS and the PUT will exchange Port Configuration transactions, but the first packet sent by the LVS will be invalid.

▪ If the LVS is configured as a Downstream Port:

a. The LVS waits for the PUT's Port Capability LMP.
b. LVS verifies that the Port Capability LMP is valid.
c. LVS transmits its Port Capability LMP with the first invalid condition listed above.
d. LVS verifies that the PUT replies with an LBAD.
e. LVS transmits a LRTY and then retransmits the packet.
f. LVS transmits the Port Configuration LMP.
g. LVS waits for the PUT's Port Configuration Response LMP.
h. LVS verifies the PUT's Port Configuration Response LMP.

▪ If the LVS is configured as an Upstream Port:

a. LVS waits for the PUT's Port Capability LMP.
b. LVS verifies that the Port Capability LMP is valid.
c. LVS transmits its Port Capability LMP with the first invalid condition listed above.
d. LVS verifies the PUT replies with an LBAD.
e. LVS transmits a LRTY and then retransmits the packet.
f. LVS waits for the PUT's Port Configuration LMP.
g. LVS verifies the PUT's Port Configuration LMP.
h. LVS transmits its Port Configuration Response LMP.

3. The LVS will keep the link active by sending Link Pollings (LUP when the LVS is configured as Upstream Port, or LDN when the LVS is configured as a Downstream Port) for 50ms.
4. The test passes if the exchanges are successful, no timeout is detected, no recovery is entered, the PUT responds to the invalid packets with an LBAD, all other packets are successfully received, all credits are restored and the link stays in U0 for at least 50ms.
5. Repeat the above steps for each of the invalid conditions listed above.
6. For a Gen 1 device, skip the remaining steps.
7. The LVS and PUT complete the Link Initialization Sequence.

▪ If the LVS is configured as a Downstream Port:

a. LVS issues a GetDeviceDescriptor() request for the PUT, but transmits the SETUP packet with Condition A listed above.

▪ If the LVS is configured as an Upstream Port:

a. The LVS prompts the test operator to have the PUT send a GetDeviceDescriptor request through USB30CV and then press "OK".
b. The test fails if no GetDeviceDescriptor request is received and the test operator has pressed "OK".
c. LVS will transmit the IN DP with Condition A listed above.

68

USB 3.1 Link Layer Test Specification