Chapter 5: Test Descriptions

1/17/2018

7.2.4.1.4#5

7.5.10.3.1#1

7.5.10.3.2#1

7.5.10.4.2#1

7.5.10.5.1#1

7.5.10.5.2#1

# Overview of Test Steps

1. Do steps 1 to 3 of the Link Initialization Sequence.

Note: LVS completes each step in a timely manner so as to not contribute to a tPortConfiguration timeout during steps 1-5.

2. The LVS and the PUT will exchange Port Configuration transactions, but the first packet sent by the LVS will have an invalid CRC-5.

a. LVS waits for the PUT's Port Capability LMP.
b. LVS verifies that the Port Capability LMP is valid.
c. LVS transmits its Port Capability LMP with an invalid CRC-5.
d. LVS verifies that the PUT replies with an LBAD.
e. LVS transmits an LRTY and then retransmits the packet with an invalid CRC-5.
f. LVS verifies that the PUT replies with an LBAD.
g. LVS transmits an LRTY and then retransmits the packet with an invalid CRC-5.
h. LVS verifies that the PUT initiates Recovery.

3. The test fails if any of the following occur:

a. The PUT does not reply with LBAD to the first two packets (which have invalid CRC-5s)
b. The PUT does not initiate Recovery in step g within tRecoveryTransition.
c. The PUT initiates Recovery before the third invalid packet is received.

4. The LVS and PUT transition through Recovery to U0.

5. The LVS and the PUT perform the Link Initialization Sequence and exchange all remaining Port Configuration transactions.
6. The test fails if the PUT retransmits its Port Capability LMP.
7. The LVS will keep the link active by sending Link Pollings (LUP when it is configured as an Upstream Port or LDN when it is configured as a Downstream Port) for 50ms.
8. The test passes if the exchanges are successful, no timeout is detected, recovery is entered once, all packets are successfully received by the PUT except for the packet with invalid CRC-5, all credits are restored and the link stays in U0 for at least 50ms.

# TD.7.31 Hot Reset Failure Test (Downstream Port Only)

This test verifies that the PUT initiates a Warm Reset when Hot Reset training fails.

# Covered Assertions

7.4.2#6,8,14

85

USB 3.1 Link Layer Test Specification