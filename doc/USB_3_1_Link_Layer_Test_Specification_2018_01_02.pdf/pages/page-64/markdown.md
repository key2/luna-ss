Chapter 5: Test Descriptions

1/17/2018

e. LVS waits for the PUT Port Configuration Response LMP.
f. LVS verifies that the Port Configuration Response LMP is valid.

■ If the LVS is configured as an Upstream Port:

a. LVS waits for the PUT's Port Capability LMP.
b. LVS verifies that the Port Capability LMP is valid.
c. LVS transmits its Port Capability LMP.
d. LVS waits for the PUT to transmit the Port Configuration LMP.
e. LVS verifies that the Port Configuration LMP is valid.
f. LVS transmits a Port Configuration Response LMP to the device.

5. The test fails if the Port Configuration transaction is not completed before tPortConfiguration expires.
6. The LVS will keep the link active by sending Link Pollings (LUP when it is configured as an Upstream Port or LDN when it is configured as a Downstream Port) for 50ms.
7. The Link Initialization Sequence passes if the exchanges are successful, no timeout is detected, no recovery is entered, all packets are successfully received, all credits are restored and the link stays in U0 for at least 50ms.

### 5.2 Physical Layer

#### TD.6.1 Lane Polarity Inversion Test

This test verifies that the PUT can successfully handle reception of lane polarity inversion.

##### Covered Assertions

(No Physical Layer assertions defined)

7.5.4.4.1#1

##### Overview of Test Steps

1. Invert the LVS TX lane polarity.
2. Bring the link to U0 using the Link Initialization Sequence.
3. The test passes if the Link Initialization Sequence passes.

#### TD.6.2 SKP Test

This test verifies that the PUT supports all possible skip (SKP) combinations.

Combinations to be tested for Gen 1 PUT:

A. Repetition of one skip ordered set followed by 354 symbols (word aligned)
B. Repetition of one skip ordered set followed by 353 symbols (word misaligned)
C. Repetition of two skip ordered sets followed by 708 symbols (word aligned)
D. Repetition of two skip ordered sets followed by 707 symbols (word misaligned)
E. Repetition of three skip ordered sets followed by 1,062 symbols (word aligned)
F. Repetition of three skip ordered sets followed by 1,061 symbols (word misaligned)

56

USB 3.1 Link Layer Test Specification