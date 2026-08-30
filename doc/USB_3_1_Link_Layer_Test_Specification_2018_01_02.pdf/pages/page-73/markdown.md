Chapter 5: Test Descriptions

1/17/2018

### TD.7.3 Link Commands CRC-5 Robustness Test

This test verifies that a Gen 1 PUT will ignore link commands with a CRC-5 error, even if only one of the Link Command Words has a CRC-5 error. The test verifies that a Gen 2 device will accept link commands with one CRC-5 error and ignore link commands with both LCWs containing a CRC-5 error. The Port Configuration transaction will be used for this purpose.

The tested CRC-5 error robustness conditions are:

A. Incorrect CRC-5 in first Link Command Word
B. Incorrect CRC-5 in second Link Command Word
C. Both Link Command Words have an incorrect CRC-5.

# Covered Assertions

7.3.4#2

# Overview of Test Steps

1. Perform the Link Initialization Sequence but transmit all LCRD_X or LCRD1_X with condition A above.
2. The test passes if:
   a. A Gen 1 PUT enters recovery when CREDIT_HP_TIMER expires.
   b. A Gen 2 PUT stays in U0 for 50ms.
3. Repeat the above steps for condition B listed above.
4. Perform the Link Initialization Sequence but transmit all LCRD_X or LCRD1_X with condition C above.
5. The test passes if the PUT enters recovery when the CREDIT_HP_TIMER or the Type 1 CREDIT_HP_TIMER expires.

### TD.7.4 Invalid Link Commands Test

This test verifies that the PUT will ignore Link Commands with link command information in the first LCW not the same as link command information in the second LCW, and both pass the CRC5 check.

# Covered Assertions

7.3.4#2

# Overview of Test Steps

1. Do steps 1 to 5 of the Link Initialization Sequence.
2. The LVS sends a link command with LGO_U1 in the first LCW and LGO_U2 in the second LCW, with good CRC-5 calculations on both.
3. The test fails if the PUT responds with an LAU or LXU.
4. The LVS will keep the link active by sending Link Pollings (LUP when it is configured as an Upstream Port or LDN when it is configured as a Downstream Port) for 50ms.
5. The test passes if the link command is ignored, all exchanges are successful, no timeout is detected, no recovery is entered, all packets are successfully received by the PUT, all credits are restored and the link stays in U0 for at least 50ms.

65

USB 3.1 Link Layer Test Specification