Chapter 5: Test Descriptions

1/17/2018

▪ If the LVS is configured as an Upstream Port:

a. The LVS prompts the test operator to have the PUT send a GetDeviceDescriptor request through USB30CV and then press “OK”.
b. The test fails if no GetDeviceDescriptor request is received and the test operator has pressed “OK”.
c. LVS transmits all LCRD2_X responses associated with the GetDeviceDescriptor request 200ns prior to the type 2 CREDIT_HP_TIMER deadline.

5. The LVS will keep the link active by sending Link Pollings (LUP when it is configured as an Upstream Port or LDN when it is configured as a Downstream Port) for 50ms.

6. The test passes if the exchanges are successful, no timeout is detected, no recovery is entered, all packets are successfully received, all credits are restored and the link stays in U0 for at least 50ms.

### TD.7.11 PENDING_HP_TIMER Timeout Test

This test verifies that the PUT will go to recovery when the PENDING_HP_TIMER expires.

#### Covered Assertions

7.2.4.1.10#1

#### Overview of Test Steps

1. Do steps 1 to 3 of the Link Initialization Sequence.
2. The LVS and the PUT will exchange the Port Configuration transaction, but the LVS will respond (with an LGOOD) to the first LMP packet sent by the PUT after expiration of the PENDING_HP_TIMER.

▪ If the LVS is configured as a Downstream Port:

a. LVS waits for the PUT’s Port Capability LMP.
b. LVS verifies that the Port Capability LMP is valid.
c. LVS will not respond to the PUT with an LGOOD.
d. LVS transmits its Port Capability LMP and Port Configuration LMP.

▪ If the LVS is configured as an Upstream Port:

a. LVS waits for the PUT to transmit its Port Capability LMP.
b. LVS verifies that the Port Capability LMP is valid.
c. LVS transmits its PUT Port Capability LMP.
d. LVS will not respond to the PUT with an LGOOD.

3. The LVS will keep the link active by sending Link Pollings (LUP when it is configured as an Upstream Port, LDN when it is configured as a Downstream Port).

4. The test passes if the PUT goes to recovery after the PENDING_HP_TIMER deadline and before the PENDING_HP_TIMER expires.

### TD.7.12 CREDIT_HP_TIMER Timeout Test

This test verifies that the PUT will go to recovery when the CREDIT_HP_TIMER expires.

71

USB 3.1 Link Layer Test Specification