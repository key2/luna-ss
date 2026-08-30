Chapter 5: Test Descriptions

1/17/2018

# Covered Assertions

7.2.4.1.10#6

# Overview of Test Steps

1. Do steps 1 to 4 of the Link Initialization Sequence with the exception that the LVS will not send any LCRD_X or LCRD1_X.
2. The LVS will keep the link active by sending Link Pollings (LUP when it is configured as an Upstream Port, LDN when it is configured as a Downstream Port).
3. The test passes if the PUT goes to recovery after the CREDIT_HP_TIMER deadline and before the CREDIT_HP_TIMER expires. For a Gen 2 PUT, this refers to the Type 1 CREDIT_HP_TIMER.
4. For a Gen 1 device, skip the remaining steps.
5. The LVS and PUT complete the Link Initialization Sequence.

■ If the LVS is configured as a Downstream Port:

a. LVS issues a GetDeviceDescriptor() request for the PUT.
b. LVS will not send any LCRD2_X.

■ If the LVS is configured as an Upstream Port:

a. The LVS prompts the test operator to have the PUT send a GetDeviceDescriptor request through USB30CV and then press "OK".
b. The test fails if no GetDeviceDescriptor request is received and the test operator has pressed "OK".
c. LVS will not send any LCRD2_X.

6. The LVS will keep the link active by sending Link Pollings (LUP when it is configured as an Upstream Port, LDN when it is configured as a Downstream Port).

7. The test passes if the PUT goes to recovery after the type 2 CREDIT_HP_TIMER deadline and before the type 2 CREDIT_HP_TIMER expires.

### TD.7.13 Wrong Header Sequence Test

This test verifies that the PUT will go to recovery when it receives a wrong header sequence.

# Covered Assertions

7.3.5#1

# Overview of Test Steps

1. Do steps 1 to 4 of the Link Initialization Sequence, with the exception that the LVS will send two LMP packets with Header Sequence Numbers that are not sequential.
2. The test passes if the PUT goes to recovery within tRecoveryTransition after reception of the LMP packet with a Header Sequence Number that is not sequential.

### TD.7.14 Wrong LGOOD_N Sequence Test

This test verifies that the PUT will go to recovery when it receives an incorrect LGOOD_N sequence.

72

USB 3.1 Link Layer Test Specification