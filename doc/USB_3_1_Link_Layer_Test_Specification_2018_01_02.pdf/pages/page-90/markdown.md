Chapter 5: Test Descriptions

1/17/2018

a. The PUT does not transmit at least sixteen consecutive TS2 ordered sets after receiving one TS2 ordered set.
b. The PUT sends Idle symbols before the LVS sends at least eight consecutive TS2 ordered sets.
c. The PUT interrupts transmission of a TS2 ordered set to transmit a SKP or SYNC (for Gen 2 only) ordered set (between TS2 ordered sets is OK).
d. The PUT continues to transmit TS2 ordered sets after tRecoveryConfigurationTimeout expires.

7. The LVS transmits Idle symbols. In Gen 2 operation the LVS transmits a single SDS Ordered Set and then data blocks with Idle Symbols.
8. The test fails if upon entering U0, the PUT does not transmit the Header Sequence Number Advertisement and the Rx Header Buffer Credit Advertisement or Type 1 and Type 2 Rx Header Buffer Credit Advertisement before their respective timeouts, PENDING_HP_TIMER and (Type 1 and Type 2) CREDIT_HP_TIMER, expire.
9. The LVS and PUT continue the test with the Link Initialization Sequence starting at step two.

### TD.7.27 Hot Reset Detection in Polling Test (Upstream Port Only)

This test verifies that the PUT detects the Hot Reset in Polling.

#### Covered Assertions

7.2.4.1.1#6,8,17,22

7.4.2#4

7.5.4.7.2#4

7.5.12.3.1#1,3,4

7.5.12.3.2#1

7.5.12.4.1#1

7.5.12.4.2#1

#### Overview of Test Steps

1. Both LVS and PUT detect each other and then transition through Polling to Polling.RxEQ.
2. Both LVS and PUT transmit the TS1 ordered sets during Polling.Active.
3. The LVS waits to receive TS2 ordered sets.
4. The test fails if the PUT does not transmit TS2s before tPollingActiveTimeout expires.
5. The LVS initiates a Hot Reset and transmits TS2 ordered sets with the Reset bit asserted.
6. The test fails if the PUT does not transmit at least sixteen TS2 ordered sets with the Reset bit asserted followed by two consecutive TS2 ordered sets with the Reset bit de-asserted.
7. The LVS transmits four consecutive TS2 ordered sets with the Reset bit de-asserted, and then transmits Idle Symbols for Gen 1, or an SDS Ordered Set followed by Idle Symbols for Gen 2.
8. The test fails if upon entering U0, the PUT does not transmit the Header Sequence Number Advertisement and the (Type 1 / Type 2) Rx Header Buffer Credit Advertisement before their respective timeouts, PENDING_HP_TIMER and (Type 1 / Type 2) CREDIT_HP_TIMER, expire.
9. The LVS and PUT exchange Port Configuration transactions.

82

USB 3.1 Link Layer Test Specification