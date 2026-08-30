Chapter 5: Test Descriptions

1/17/2018

# Covered Assertions

7.2.4.1.1#7,9

7.2.4.2.1#4

7.2.4.2.2#2,3

7.2.4.2.3#2,8,9

7.2.4.2.7#2,3

7.5.5.1#2

7.5.5.2#2

7.5.7.1#2

7.5.7.2#2

8.4.2#1

# Overview of Test Steps

1. Do steps 1 to 4 of the Link Initialization Sequence.
2. The LVS transmits the Set Link Function LMP with the Force_LinkPM_Accept bit asserted.
3. The LVS transmits an LGO_U1 and waits to receive an LAU from the PUT.
4. The test fails if the PUT does not transmit an LAU before PM_LC_TIMER deadline, or recovery is entered.
5. The LVS transmits an LPMA and then transition to U1.
6. The test fails if the PUT does not transition to U1 when the PM_ENTRY_TIMER expires, if recovery is entered, or if the PUT sends any packet.
7. The LVS transmits a U1 Exit LFPS to transition to U0 and waits to receive U1 Exit LFPS to complete the U1 Exit LFPS handshake.
8. The test fails if the LFPS handshake does not conform to the following specifications from section 6.9.2:

a. Between 300ns - 2us elapses between the start of the LVS U1 Exit LFPS and the start of the PUT U1 Exit LFPS.
b. The PUT U1 Exit LFPS duration is within 0.9us - 1.2us.
c. The PUT enters Recovery before tNoLFPSResponseTimeout deadline after the start of its U1 exit LFPS.
d. The PUT enters U0 before Ux_EXIT_TIMER deadline.

9. The test passes if all packets are successful, recovery is entered once, no extra packets or LFPS signals are received, and the PUT returns to U0.

# TD.7.24 Accepted Power Management Transaction for U2 Test (Upstream Port Only)

This test verifies that the PUT transitions to U2 if it receives an LGO_U2.

# Covered Assertions

7.2.4.1.1#7,9

7.2.4.2.1#4

7.2.4.2.2#2,3

7.2.4.2.3#2,8,9

79

USB 3.1 Link Layer Test Specification