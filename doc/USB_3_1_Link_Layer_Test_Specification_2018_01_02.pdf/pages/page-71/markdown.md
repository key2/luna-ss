Chapter 5: Test Descriptions

1/17/2018

2. The test fails if the PUT does not transmit two SCD1 after one SCD1 or SCD2 is received.
3. The LVS transitions to transmitting Polling.LFPS bursts with an SCD2 signature after transmitting two SCD1 after receiving 1 SCD1 or SCD2 from the PUT
4. The test fails if the PUT does not transmit two SCD2 after one SCD2 is received.
5. The LVS transmits continuous PHY Capability LBPMs to announce its 10Gbps capability.
6. The test fails if the PUT does not continuously transmit its PHY Capability LBPMs.
7. If the LVS has a PHY Capability greater than the PUT, then:

a. The LVS adjusts its PHY Capability by transmitting PHY Capability LBPMs that match the PUT.
b. The test fails if the PUT does not continuously transmit its PHY Capability LBPMs.

8. The test fails if the PUT does not transmit four consecutive and matched PHY Capability LBPMs after receiving two consecutive and matched PHY Capability LBPMs or PHY Ready LBPMs.
9. The LVS transmits 524,288 TSEQ Ordered Sets, inserting a SYNC Ordered Set every 16,384 Ordered Sets.
10. The test fails if any of the following occur:

a. The PUT does not transmit TSEQ Ordered Sets.
b. The PUT does not transmit a SYNC Ordered Set for every 16,384 TSEQ Ordered Sets.
c. The PUT transmits Idle Symbols, or any other Packet, Symbol or Ordered Set besides SYNC or SKP Ordered Sets, during TSEQ transmission or between TSEQ Ordered Sets.

11. The LVS transmits TS1 Ordered Sets, inserting a SYNC Ordered Set every 32 Ordered Sets, and inserting SKP Ordered Sets periodically when necessary.
12. The LVS waits to receive eight consecutive and identical TS1 or TS2 Ordered Sets from the PUT. Note: SYNC and SKP Ordered Sets do not disqualify consecutive TS1s / TS2s. Symbols 14-15 of the TS1 / TS2 Ordered Sets do not need to be identical.
13. The test fails if any of the following occur:

a. The PUT does not transmit TS1 ordered sets.
b. The PUT transmits TS2s before the LVS transmits eight consecutive and identical TS1s or TS2s.
c. The PUT interrupts a TS1 Ordered Set to transmit a SKP or SYNC Ordered Set (between TS1 ordered sets is OK).
d. The PUT transmits Idle Symbols or any other Packet.
e. The PUT continues to transmit TS1 Ordered Sets after tPollingActiveTimeout expires.

14. The LVS transmits TS2 Ordered Sets, inserting a SYNC Ordered Set every 32 Ordered Sets, and inserting SKP Ordered Sets periodically when necessary.
15. The test fails if any of the following occur:

a. The PUT does not transmit at least 16 consecutive TS2 ordered sets after receiving one TS2 ordered set.
b. The PUT transmits Idle symbols before the LVS transmits eight consecutive and identical TS2s.

63

USB 3.1 Link Layer Test Specification