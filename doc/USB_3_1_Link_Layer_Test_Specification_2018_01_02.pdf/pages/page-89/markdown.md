Chapter 5: Test Descriptions

1/17/2018

4. The LVS transmits an LPMA and then transitions to U3.
5. The test fails if the PUT does not transition to U3 when the PM_ENTRY_TIMER expires, if recovery is entered, or if the PUT sends any packet.
6. The LVS transmits the U3 Exit LFPS to transition to U0 and waits to receive U3 Exit LFPS to complete the U3 Exit LFPS handshake.
7. The test fails if the LFPS handshake does not conform to the following specifications from section 6.9.2:

a. Between 300ns - 10ms elapses between the start of the LVS U3 Exit LFPS and the start of the PUT U3 Exit LFPS.
b. The PUT U3 exit LFPS duration is within 80us - 10ms.
c. The PUT enters Recovery before tNoLFPSResponseTimeout deadline after the start of its U3 exit LFPS.

8. The test passes if all packets are successful, recovery is entered once, no extra packets or LFPS signals are received, and the PUT enters Recovery.

### TD.7.26 Transition to U0 from Recovery Test

This test verifies that the PUT transitions to U0 when it is in Recovery.

#### Covered Assertions

7.2.4.1.1#3,4,7,9
7.3.6#17.5.10.3.1#1
7.5.10.3.2#1
7.5.10.4.2#1
7.5.10.5.1#1
7.5.10.5.2#1

#### Overview of Test Steps

1. Both the LVS and the PUT go through the initial steps of the LTSSM to reach U0.
2. The LVS does not transmit the Header Sequence Advertisement and the Rx Header Buffer Credit Advertisement or Type 1 and Type 2 Rx Header Buffer Credit Advertisements. The PUT will then transition to Recovery because the PENDING_HP_TIMER will time out.
3. The test fails if the PUT transitions to Recovery before PENDING_HP_TIMER deadline or it does not transition to Recovery when the PENDING_HP_TIMER expires.
4. The test fails if any of the following occur:

a. The PUT does not transmit TS1 ordered sets.
b. The PUT transmits TS2s before the LVS sends eight consecutive and identical TS1s or TS2s.
c. The PUT interrupts a TS1 ordered set to transmit a SKP or SYNC (for Gen 2 only) Ordered Set (between TS1 ordered sets is OK).
d. The PUT transmits Idle Symbols or any other Packet.
e. The PUT continues to transmit TS1 ordered sets after tRecoveryActiveTimeout expires.

5. The LVS transmits TS2 ordered sets and readies to complete the Recovery.Configuration handshake.
6. The test fails if any of the following occur:

81

USB 3.1 Link Layer Test Specification