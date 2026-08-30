Chapter 5: Test Descriptions

1/17/2018

10. The LVS will keep the link active by sending Link Pollings (LUP when it is configured as an Upstream Port or LDN when it is configured as a Downstream Port) for 50ms.
11. The test fails if the Port Configuration exchange sequences are not successful or the link does not stay in U0 for at least 50ms.

### TD.7.28 Hot Reset Detection in U0 Test (Upstream Port Only)

This test verifies that the PUT detects the Hot Reset in U0 and does not start the Port Configuration Sequences.

# Covered Assertions

7.2.4.1.1#6,8,17,22

7.4.2#2,4

7.5.10.4.1#1

7.5.12.3.1#1,2

7.5.12.3.2#1

7.5.12.4.1#1

7.5.12.4.2#1

# Overview of Test Steps

1. Do steps 1 to 5 of the Link Initialization Sequence.
2. The LVS transmits TS1 ordered set to transition to Recovery.
3. The LVS waits to receive TS1 ordered sets.
4. The test fails if the PUT does not transmit TS1s before tU0RecoveryTimeout expires.
5. The LVS initiates a Hot Reset by transmitting TS2 ordered sets with the Reset bit asserted.
6. The test fails if the PUT does not transmit at least sixteen TS2 ordered sets with the Reset bit asserted followed by two consecutive TS2 ordered sets with the Reset bit de-asserted.
7. The LVS transmits four consecutive TS2 ordered sets with the Reset bit de-asserted, and then transmits Idle Symbols for Gen 1, or SDS Ordered Set followed by Idle Symbols for Gen 2.
8. The test fails if upon entering U0, the PUT does not transmit the Header Sequence Number Advertisement and the (Type 1/Type 2) Rx Header Buffer Credit Advertisement before their respective timeouts, PENDING_HP_TIMER and (Type 1/Type 2) CREDIT_HP_TIMER, expire.
9. The LVS will keep the link active by sending Link Pollings (LUP when it is configured as an Upstream Port or LDN when it is configured as a Downstream Port) for 50ms.
10. The test fails if the PUT retransmits Port Capability or Port Configuration LMPs.
11. The test fails if the Port Configuration exchange sequences are not successful and the link does not stay in U0 for at least 50ms.

### TD.7.29 Hot Reset Initiation in U0 Test (Downstream Port Only)

This test verifies that the PUT initiates Hot Reset in U0.

83

USB 3.1 Link Layer Test Specification