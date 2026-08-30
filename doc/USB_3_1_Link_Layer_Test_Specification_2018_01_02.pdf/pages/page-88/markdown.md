Chapter 5: Test Descriptions

1/17/2018

7.2.4.2.7#2, 3
7.5.8.1#2
7.5.8.2#5
8.4.2#1

# Overview of Test Steps

1. Do steps 1 to 4 of the Link Initialization Sequence.
2. The LVS transmits the Set Link Function LMP with the Force_LinkPM_Accept bit asserted.
3. The LVS transmits an LGO_U2 and waits to receive an LAU from the PUT.
4. The test fails if the PUT does not transmit an LAU before PM_LC_TIMER deadline, or if recovery is entered.
5. The LVS transmits an LPMA and then transitions to U2.
6. The test fails if the PUT does not transition to U2 when the PM_ENTRY_TIMER expires, recovery is entered, or if the PUT sends any packet.
7. The LVS transmits the U2 Exit LFPS to transition to U0 and waits to receive U2 Exit LFPS to complete the U2 Exit LFPS handshake.
8. The test fails if the LFPS handshake does not conform to the following specifications from section 6.9.2:
  a. Between 300ns – 2ms elapses between the start of the LVS U2 Exit LFPS and the start of the PUT U2 Exit LFPS.
  b. The PUT U2 Exit LFPS duration is within 80us – 2ms.
  c. The PUT enters Recovery before tNoLFPSResponseTimeout deadline after the start of its U2 exit LFPS.
  d. The PUT enters U0 before Ux_EXIT_TIMER deadline
9. The test passes if all packets are successful, recovery is entered once, no extra packets or LFPS signals are received, and the PUT enters Recovery.

### TD.7.25 Accepted Power Management Transaction for U3 Test (Upstream Port Only)

This test verifies that the PUT transitions to U3 if it receives an LGO_U3.

# Covered Assertions

7.2.4.1.1#7,97.2.4.2.1#4
7.2.4.2.4#2,3,7
7.2.4.2.7#2,3
7.5.9.1#3
7.5.9.2#5

# Overview of Test Steps

1. Do steps 1 to 4 of the Link Initialization Sequence.
2. The LVS transmits an LGO_U3 and waits to receive an LAU from PUT.
3. The test fails if the PUT does not transmit an LAU before PM_LC_TIMER deadline, or if recovery is entered..

80

USB 3.1 Link Layer Test Specification