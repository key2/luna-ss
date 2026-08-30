Chapter 5: Test Descriptions

1/17/2018

# Subtest 1 (TD 7.1.1):

1. The LVS waits to receive Polling.LFPS bursts.
2. The LVS transmits four Polling.LFPS bursts.
3. The test fails if any of the following occur:

a. If the PUT does not contain a captive re-timer, it does not transmit at least sixteen consecutive Polling.LFPS bursts.
b. If the PUT contains a captive re-timer, it does not transmit at least four consecutive Polling.LFPS bursts.
c. The PUT does not transmit at least four consecutive Polling.LFPS bursts after receiving one Polling.LFPS bursts.
d. The PUT transitions away from Polling.LFPS before the LVS sends at least two consecutive Polling.LFPS bursts.
e. The PUT does not transition from Polling.LFPS before tPollingLFPSTimeout expires.

4. The test fails if the PUT has transmitted more than 6 LFPS after receiving 1 LFPS and the Number of LFPS tx'd before receiving 1 > 18 – the Number of LFPS tx'd after receiving 1.
5. The LVS transmits 65,536 TSEQ ordered sets.
6. The test fails if any of the following occur:

a. The PUT does not transmit TSEQ ordered sets.
b. The PUT transmits SKP Ordered Sets, Idle Symbols, or any other Packet, Symbol or Ordered Set during TSEQ transmission or between training ordered sets.

7. The LVS transmits TS1 ordered sets and waits to receive eight consecutive and identical TS1 or TS2 ordered sets from the PUT.
8. The test fails if any of the following occur:

a. The PUT does not transmit TS1 ordered sets.
b. The PUT transmits TS2s before the LVS sends eight consecutive and identical TS1s or TS2s.
c. The PUT interrupts a TS1 ordered set to transmit a SKP ordered set (between TS1 ordered sets is OK).
d. The PUT transmits Idle Symbols or any other Packet.
e. The PUT continues to transmit TS1 ordered sets after tPollingActiveTimeout expires.

9. The LVS transmits TS2 ordered sets and readies to complete the Polling.Configuration handshake.

10. The test fails if any of the following occur:

a. The PUT does not transmit at least sixteen consecutiveTS2 ordered sets after receiving one TS2 ordered set.
b. The PUT sends Idle symbols before the LVS sends at least eight consecutive TS2 ordered sets.
c. The PUT interrupts transmission of a TS2 ordered set to transmit a SKP ordered set (between TS2 ordered sets is OK).
d. The PUT continues to transmit TS2 ordered sets after tPollingConfigurationTimeout expires.

11. The LVS transmits Idle symbols.

12. The test fails if upon entering U0, the PUT does not transmit the Header Sequence Number Advertisement and the Rx Header Buffer Credit Advertisement before their respective timeouts, PENDING_HP_TIMER and CREDIT_HP_TIMER, expire.

61

USB 3.1 Link Layer Test Specification