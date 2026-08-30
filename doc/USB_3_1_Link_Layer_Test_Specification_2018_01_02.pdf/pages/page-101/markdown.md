Chapter 5: Test Descriptions

1/17/2018

14. The LVS does not transmit the TS1 ordered sets during Polling.Active.
15. The test fails if the PUT does not transition to Rx.Detect after tPollingActiveTimeout.
16. The LVS and PUT transition through Polling.LFPS to Polling.Configuration.
17. The LVS does not transmit the TS2 ordered sets during Polling.Configuration.
18. The test fails if the PUT does not transition to Rx.Detect after tPollingConfigurationTimeout.
19. The LVS and PUT transition through Polling.LFPS to Polling.Active.
20. The LVS does not transmit the TS1 ordered sets during Polling.Active.
21. The test fails if the PUT does not transition to eSS.Inactive after tPollingActiveTimeout.

### TD.7.41 SetAddress TPF Bit Test (Gen 2 Upstream Port Only)

This test verifies that the PUT sets the TPF bit at the end of a SetAddress Control Transfer.

#### Covered Assertions

8.5.6.7#2

#### Overview of Test Steps

1. Perform the Link Initialization Sequence to bring the LVS and PUT link to U0.
2. The LVS sends a SetAddress command to the PUT.
3. The test fails if:

a. The SetAddress control transfer does not complete.
b. The ACK response to the STATUS packet of the control transfer does not have the TPF bit set to 1.

### TD.7.42 Symbol to Block Alignment Test (Gen 2 Only)

Condition to be tested:

A. Start every Packet in the 0th symbol of a block.
B. Start every Packet in the 1st symbol of a block.
C. Start every Packet in the 2nd symbol of a block.
D. Start every Packet in the 3rd symbol of a block.
E. Start every Packet in the 4th symbol of a block.
F. Start every Packet in the 5th symbol of a block.
G. Start every Packet in the 6th symbol of a block.
H. Start every Packet in the 7th symbol of a block.
I. Start every Packet in the 8th symbol of a block.
J. Start every Packet in the 9th symbol of a block.
K. Start every Packet in the 10th symbol of a block.
L. Start every Packet in the 11th symbol of a block.
M. Start every Packet in the 12th symbol of a block.
N. Start every Packet in the 13th symbol of a block.
O. Start every Packet in the 14th symbol of a block.
P. Start every Packet in the 15th symbol of a block.

93

USB 3.1 Link Layer Test Specification