Chapter 5: Test Descriptions

1/17/2018

# Overview of Test Steps

1. Do steps 1 to 4 of the Link Initialization Sequence.
2. The LVS application prompts the test operator to enable and configure the U1 and U2 inactivity timers through USB30CV. CV will set the U1 Timeout field to 7Fh and the U2 Timeout field to 00h.
3. The LVS waits to receive an LGO_U1 from the PUT.
4. The LVS transmits an LAU tLinkTurnAround before the PM_LC_TIMER deadline.
5. The test fails if the PUT does not transmit an LPMA after receiving the LAU.
6. After the LVS completes this test case, clear the U1/U2 registers through the CV prompt.

# TD.7.21 PM_LC_TIMER Timeout Test (Downstream Port Only)

This test verifies that the PUT transitions to Recovery when the PM_LC_TIMER expires.

# Covered Assertions

7.2.4.2.1#1

7.2.4.2.3#6

7.3.4#6

# Overview of Test Steps

1. Do steps 1 to 3 of TD.7.18.
2. The LVS does not transmit LAU when it receives the LGO_U1.
3. The test fails if the PUT does not transition to Recovery when the PM_LC_TIMER expires.
4. After the LVS completes this test case, clear the U1/U2 registers through the CV prompt.

# TD.7.22 PM_ENTRY_TIMER Timeout Test (Upstream Port Only)

This test verifies that the PUT transitions to a low power state when the PM_ENTRY_TIMER expires.

# Covered Assertions

7.2.4.2.1#37.2.4.2.3#8,10,12

# Overview of Test Steps

1. Do steps 1 to 4 of TD.7.23.
2. The LVS does not transmit LPMA when it receives LAU.
3. The test fails if the PUT does not transition to U1 when the PM_ENTRY_TIMER expires, the PUT does not transmit LAU, or if the PUT sends any packet or LFPS.

# TD.7.23 Accepted Power Management Transaction for U1 Test (Upstream Port Only)

This test verifies that the PUT transitions to U1 if it receives LGO_U1.

78

USB 3.1 Link Layer Test Specification