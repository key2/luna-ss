Chapter 5: Test Descriptions

1/17/2018

### TD.7.18 Low Power initiation for U1 test (Downstream Port Only)

This test verifies that the PUT initiates U1 state.

#### Covered Assertions

7.2.4.2.2#1

7.2.4.2.3#1,3,4,5,7,8

7.2.4.2.7#2,3

7.5.7.1#2

7.5.7.2#6

#### Overview of Test Steps

1. Do steps 1 to 4 of the Link Initialization Sequence.
2. The LVS application prompts the test operator to enable and configure the U1 and U2 inactivity timers through USB30CV. CV will set the U1 Timeout field to 7Fh and the U2 Timeout field to 00h.
3. The LVS waits to receive an LGO_U1 from the PUT. The LVS transmits an LXU, when it receives the LGO_U1.
4. The test fails if the PUT sends an LPMA, or if recovery is entered.
5. The LVS waits to receive an LGO_U1 from the PUT again.
6. The LVS transmits an LAU when it receives the LGO_U1.
7. The test fails if any of the following conditions occur:

a. The PUT does not transmit an LPMA before PM_ENTRY_TIMER deadline
b. The PUT enters recovery
c. The PUT does not transition to U1

8. The LVS transmits the U1 Exit LFPS to transition to U0 and waits to receive U1 Exit LFPS to complete the U1 Exit LFPS handshake.

9. The test fails if the LFPS handshake does not conform to the following specifications from section 6.9.2:

a. Between 300ns - 2us elapses between the start of the LVS U1 Exit LFPS and the start of the PUT U1 Exit LFPS.
b. The PUT U1 Exit LFPS duration is within 0.9us - 1.2us.
c. The PUT enters U0 before Ux_EXIT_TIMER deadline.
d. The PUT enters Recovery before tNoLFPSResponseTimeout deadline after the start of its U1 exit LFPS.

10. The test passes if all packets are successful, recovery is entered once, no extra packets or LFPS signals are received, and the PUT returns to U0.

11. After the LVS completes this test case, clear the U1/U2 registers through the CV prompt.

### TD.7.19 Low Power initiation for U2 test (Downstream Port Only)

This test verifies that the PUT initiates U2 state.

76

USB 3.1 Link Layer Test Specification