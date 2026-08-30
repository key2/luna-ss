Chapter 5: Test Descriptions

1/17/2018

## 5 Test Descriptions

### 5.1 Link Initialization Sequence

Most of the following test descriptions (TDs) refer to the Link Initialization Sequence, described here. The purpose of the Link Initialization Sequence is to establish the link between the LVS and the PUT and check that link establishment and initialization is followed properly by the PUT.

Some tests are designed to follow the Link Initialization Sequence up to a certain point and then introduce different test steps. This is reflected in each specific TD.

Link training is different for Gen 1 and Gen 2 capable PUTs during Polling substates. The verification checks on these substates are performed during TD 7.1.

Covered Assertions

7.2.4.1.1#6,8,10-17,22

7.2.4.1.4#2

7.3.4#2

7.5.6.1#5,6

8.4.5#1

8.4.6#1,3 (downstream)

8.4.7#1 (upstream)

Link Initialization Sequence

1. The LVS and the PUT go through the initial steps of the LTSSM (eSS.Disabled, Rx.Detect, Polling) to reach U0.
2. Once in U0, the LVS will transmit the Header Sequence Number Advertisement and

a. In Gen 1 speed, the Rx Header Buffer Credit Advertisement.
b. In Gen 2 speeds, the Type 1 and Type 2 Rx Header Buffer Credit Advertisements.

3. The LVS verifies that:

a. The Header Sequence Number Advertisement transmitted by the PUT is LGOOD_7
b. A Gen 2 PUT transmits the following Type 1 and Type 2 Rx Header Buffer Credit Advertisements: LCRD1_A, LCRD1_B, LCRD1_C, LCRD1_D, LCRD2_A, LCRD2_B, LCRD2_C, LCRD2_D.
c. A Gen 1 PUT transmits the following Rx Header Buffer Credit Advertisements: LCRD_A, LCRD_B, LCRD_C and LCRD_D.

4. The LVS and the PUT will exchange Port Configuration transactions.

■ If the LVS is configured as a Downstream Port:

a. LVS waits for the PUT's Port Capability LMP.
b. LVS verifies that the Port Capability LMP is valid.
c. LVS transmits its Port Capability LMP.
d. LVS transmits a valid Port Configuration LMP to the PUT.

55

USB 3.1 Link Layer Test Specification