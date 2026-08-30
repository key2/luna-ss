Chapter 5: Test Descriptions

1/17/2018

# Covered Assertions

7.2.4.2.2#1,
7.2.4.2.3#1,3,4,5,7,8
7.2.4.2.7#2,3
7.5.8.1#2
7.5.8.2#5

# Overview of Test Steps

1. Do steps 1 to 4 of the Link Initialization Sequence.
The LVS application prompts the test operator to enable and configure the U1 and U2 inactivity timers through USB30CV. CV will set the U1 Timeout field to 00h and the U2 Timeout field to 7Fh.
2. The LVS waits to receive an LGO_U2 from the PUT.
3. The LVS transmits an LXU when it receives the LGO_U2.
4. The test fails if the PUT sends an LPMA, or if recovery is entered.
5. The LVS waits to receive an LGO_U2 from the PUT again.
6. The LVS transmits an LAU when it receives the LGO_U2.
7. The test fails if any of the following occur:

a. The PUT does not transmit an LPMA before PM_ENTRY_TIMER deadline.
b. The PUT enters recovery
c. The PUT does transition to U2.

8. The test fails if the PUT does not transition to U2.
9. The LVS transmits the U2 Exit LFPS to transition to U0 and waits to receive U2 Exit LFPS to complete the U2 Exit LFPS handshake.
10. The test fails if the LFPS handshake does not conform to the following specifications from section 6.9.2:

a. Between 300ns – 2ms elapses between the start of the LVS U2 Exit LFPS and the start of the PUT U2 Exit LFPS.
b. The PUT U2 Exit LFPS duration is within 80us – 2ms.
c. The PUT enters U0 before Ux_EXIT_TIMER deadline.
d. The PUT enters Recovery before tNoLFPSResponseTimeout deadline after the start of its U2 exit LFPS.

11. The test passes if all packets are successful, recovery is entered once, no extra packets or LFPS signals are received, and the PUT returns to U0.
12. After the LVS completes this test case, clear the U1/U2 registers through the CV prompt.

# TD.7.20 PM_LC_TIMER Deadline Test (Downstream Port Only)

This test verifies that the PUT accepts an LGO_U1 sent at the PM_LC_TIMER deadline.

# Covered Assertions

7.2.4.2.1#1, 2

77

USB 3.1 Link Layer Test Specification