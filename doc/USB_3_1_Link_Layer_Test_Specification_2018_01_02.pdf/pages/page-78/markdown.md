Chapter 5: Test Descriptions

1/17/2018

3. The LVS will keep the link active by sending Link Pollings (LUP when it was configured as an Upstream Port, LDN when it was configured as a Downstream Port) for 50ms.
4. The test passes if the exchanges are successful, no timeout is detected, no recovery is entered, the packet that the LVS responded to with an LBAD is retransmitted correctly, all other packets are received successfully, all credits are restored and the link stays in U0 for at least 50ms.

### TD.7.9 PENDING_HP_TIMER Deadline Test

This test verifies that:

1) The PUT will accept an LGOOD_N sent at the maximum link delay budget before PENDING_HP_TIMER deadline. The Port Configuration transaction will be used for this purpose.
2) The PUT adheres to tLinkTurnaround as defined in Ch 7 and Appendix E.

Covered Assertions

7.2.4.1.10#2

Overview of Test Steps

1. Perform the Link Initialization Sequence, but transmit LGOOD_N responses for Port Capability LMP 200ns prior to the PENDING_HP_TIMER deadline.
2. The LVS verifies that for each LGOOD_n received from the PUT, the first symbol of the LGOOD_n is received within tLinkTurnaround of the last symbol of the Header Packet that is acknowledged by the LGOOD_n.
3. The LVS will keep the link active by sending Link Pollings (LUP when it is configured as an Upstream Port or LDN when it is configured as a Downstream Port) for 50ms.
4. The test passes if the exchanges are successful, no timeout is detected, no recovery is entered, all packets are successfully received, all credits are restored and the link stays in U0 for at least 50ms.

### TD.7.10 CREDIT_HP_TIMER Deadline Test

This test verifies that the PUT will accept an LCRD_X, LCRD1_X or LCRD2_X sent at the CREDIT_HP_TIMER deadline. The Port Configuration transaction will be used for this purpose.

Covered Assertions

7.2.4.1.10#7

Overview of Test Steps

1. Perform the Link Initialization Sequence but transmit all LCRD_X or LCRD1_X responses tLinkTurnAround prior to the CREDIT_HP_TIMER or type 1 CREDIT_HP_TIMER deadline.
2. The LVS will keep the link active by sending Link Pollings (LUP when it is configured as an Upstream Port or LDN when it is configured as a Downstream Port) for 50ms.
3. For a Gen 1 PUT continue to step 6.
4. For a Gen 2 PUT:

If the LVS is configured as a Downstream Port:

a. LVS issues a GetDeviceDescriptor() request for the PUT.
b. LVS transmits all LCRD2_X responses 200ns prior to the CREDIT_HP_TIMER deadline.

70

USB 3.1 Link Layer Test Specification