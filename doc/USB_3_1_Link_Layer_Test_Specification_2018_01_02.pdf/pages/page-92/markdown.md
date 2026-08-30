Chapter 5: Test Descriptions

1/17/2018

# Covered Assertions

7.2.4.1.1#6,8,17,22

7.4.2#2,4,10

7.5.4.6.1#1

7.5.4.7.2#3

7.5.10.4.1#1

7.5.12.3.1#1,2

7.5.12.3.2#1

7.5.12.4.1#1

7.5.12.4.2#1

# Overview of Test Steps

1. Do steps 1 to 5 of the Link Initialization Sequence.
2. The LVS prompts the test operator to initiate a Hot Reset on the PUT through USB30CV.
3. The LVS waits for the PUT to send TS1s.
4. The test fails if the PUT does not transmit TS1s before tU0RecoveryTimeout expires.
5. The LVS transmits TS1 ordered sets and waits to receive TS2 ordered sets with the Reset bit asserted.
6. The test fails if the PUT does not transmit at least sixteen TS2 ordered sets with Reset bit asserted.
7. The LVS transmits at least sixteen TS2 ordered sets with the Reset bit asserted, and then transmits two consecutive TS2 ordered sets with the Reset bit de-asserted.
8. The test fails if any of the following occur:
  a. After LVS transmitted TS2 ordered sets with Reset bit de-asserted, the PUT does not transmit four consecutive TS2 ordered sets with the Reset bit de-asserted, when tHotResetActiveTimeout expires
  b. The PUT transmits anything other than TS2 ordered sets, before the LVS transmits TS2 ordered sets with the Reset bit de-asserted.
9. The LVS transmits Idle Symbols for Gen 1, or SDS Ordered Set followed by Idle Symbols for Gen 2.
10. The test fails if upon entering U0, the PUT does not transmit the Header Sequence Number Advertisement and the (Type 1/Type 2) Rx Header Buffer Credit Advertisement before their respective timeouts, PENDING_HP_TIMER and (Type 1/Type 2) CREDIT_HP_TIMER, expire.
11. The LVS will keep the link active by sending Link Pollings (LUP when it is configured as an Upstream Port or LDN when it is configured as a Downstream Port) for 50ms.
12. The test fails if the PUT retransmits Port Capability or Port Configuration LMPs.
13. The test fails if the Port Configuration exchange sequences are not successful and the link does not stay in U0 for at least 50ms.

### TD.7.30 Recovery on three consecutive failed RX Header Packets Test

This test verifies that the PUT will enter Recovery if it fails to receive a header packet three consecutive times.

# Covered Assertions

7.2.4.1.1#7,9

84

USB 3.1 Link Layer Test Specification