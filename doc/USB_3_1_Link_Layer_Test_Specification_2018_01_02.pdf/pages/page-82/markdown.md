Chapter 5: Test Descriptions

1/17/2018

### TD.7.16 Link Command Missing Test (Upstream Port Only)

This test verifies that the PUT will go to Recovery if no Link Commands are received for more than tU0RecoveryTimeout.

Please note that the downstream LVS port shall disable transmission of ITPs.

# Covered Assertions

7.3.4#7, 8

7.5.6.1#3

7.5.6.2#6

# Overview of Test Steps

1. Do steps 1 to 4 of the Link Initialization Sequence.
2. The LVS will not send LDNs or any other link commands.
3. The test fails if the PUT goes to Recovery before the tU0RecoveryTimeout deadline, or if it does not go to Recovery after tU0RecoveryTimeout expires.

### TD.7.17 tPortConfiguration Time Timeout Test

This test verifies that a downstream PUT will go to SS.Inactive if tPortConfiguration expires, and an upstream PUT will go to SS.Disabled if tPortConfiguration expires.

# Covered Assertions

7.5.6.2#10,11

8.4.5#1,3

8.4.6#2

# Overview of Test Steps

1. Do steps 1 to 3 of the Link Initialization Sequence.
2. The LVS does not transmit both the Port Capability LMP and Port Configuration LMP.
3. The test fails if any of the following occur:

a. The PUT transitions to eSS.Inactive (downstream PUT) or eSS.Disabled (upstream PUT) before tPortConfiguration deadline.

i. For a PUT with a captive re-timer, the PUT transitions to eSS.Inactive (downstream PUT) or eSS.Disabled (upstream PUT) before tU0Recovery deadline.

b. The PUT does not transition to eSS.Inactive (downstream PUT) or eSS.Disabled (upstream PUT) after tPortConfiguration expires.

i. For a PUT with a captive re-timer, the PUT does not transition to eSS.Inactive (downstream PUT) or eSS.Disabled (upstream PUT) after tU0Recovery expires.

74

USB 3.1 Link Layer Test Specification