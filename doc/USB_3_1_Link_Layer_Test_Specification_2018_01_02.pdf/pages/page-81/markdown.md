Chapter 5: Test Descriptions

1/17/2018

# Covered Assertions

7.3.4#4

# Overview of Test Steps

1. Do steps 1 to 4 of the Link Initialization Sequence, with the exception that the LVS will send an LGOOD_0 for the first LMP packet as expected, but will send an LGOOD_n with n ≠ 1 for the second LMP packet.
2. The test passes if the PUT goes to recovery within tRecoveryTransition after reception of the incorrect LGOOD_n.

# TD.7.15 Wrong LCRD_X Sequence Test

This test verifies that the PUT will go to recovery when it receives an incorrect LCRD_X or LCRD1_X sequence.

# Covered Assertions

7.3.4#5

# Overview of Test Steps

1. Do steps 1 to 4 of the Link Initialization Sequence, with the exception that the LVS will send an LCRD_A or LCRD1_A for the first LMP packet as expected, but will send an LCRD_X or LCRD1_X with X ≠ B for the second LMP packet.
2. The test passes if the PUT goes to recovery within tRecoveryTransition after reception of the incorrect LCRD_X or LCRD1_X.
3. For a Gen 1 device, skip the remaining steps.
4. The LVS and PUT complete the Link Initialization Sequence.

■ If the LVS is configured as a Downstream Port:

a. LVS issues a GetDeviceDescriptor() request for the PUT.
b. LVS transmits an LCRD2_A in response to the IN DP.
c. LVS issues a GetDeviceDescriptor() request for the PUT.
d. LVS transmits an LCRD2_X with X ≠ B for the IN DP.

■ If the LVS is configured as an Upstream Port:

a. The LVS prompts the test operator to have the PUT send two GetDeviceDescriptor requests through USB30CV and then press “OK”.
b. The test fails if two GetDeviceDescriptor requests have not been received and the test operator has pressed “OK”.
c. LVS transmits an LCRD2_A in response to the first SETUP DP.
d. LVS transmits an LCRD2_X with X ≠ B for the second SETUP DP.

5. The test passes if the PUT goes to Recovery within tRecoveryTransition after reception of the incorrect LCRD2_X.

73

USB 3.1 Link Layer Test Specification