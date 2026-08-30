Chapter 5: Test Descriptions

1/17/2018

11. The LVS transmits an LPMA and then transitions to U1.
12. The test fails if the PUT does not transition to U1, or if the PUT sends any packet.

### TD.7.38 Port Capability Tiebreaker Test

This test verifies that the PUT accepts ports capable of both US and DS operation, and that a PUT capable of both US and DS operation resends its Port Capability info with a randomly generated tiebreaker after the first tiebreaker is the same value as its link partner's.

### Covered Assertions

TBD

### Overview of Test Steps

1. Perform steps 1 through 3 of the Link Initialization Sequence.
2. The LVS waits to receive the Port Capability LMP.
3. The test fails if the Port Capability LMP received is not valid.
4. If the LVS is configured as a Downstream Port:
  a. The LVS sends a Port Capability LMP indicating it is capable of both US and DS operation.
  b. The test continues at step 4.d. of the Link Initialization Sequence.

5. If the LVS is configured as an Upstream Port:

a. If the Port Capability LMP from the PUT indicates that the port only supports DS operation:
  i. The LVS sends a Port Capability LMP indicating it is capable of both US and DS operations.
  ii. The test continues at step 4.d of the Link Initialization Sequence.
b. If the Port Capability LMP from the PUT indicates that the port supports both US and DS operation:
  i. The test continues at step 6 of this test.

6. The LVS records the tiebreaker value on the received LMP as X, and initializes a counter to 1.

7. The LVS sends a Port Capability LMP with DS and US capability set to 1, and its tiebreaker value set to X.

8. The LVS waits to receive another Port Capability LMP.

a. The test fails if the LVS does not receive another Port Capability LMP within tPortConfigurationTimeout.
b. If the tiebreaker value is X and the counter value is less than 5:
  i. Increment the counter.
  ii. Go to step 7.
c. The test fails if the tiebreaker value is X and the counter value is 5.
d. If the tiebreaker value is not X, move to step 9.

9. The LVS sends a Port Capability LMP with DS and US capability set to 1, and its tiebreaker value set higher than the tiebreaker value on the received LMP.

10. Perform the Link Initialization Sequence starting at step 4.d with the LVS as a Downstream Port

90

USB 3.1 Link Layer Test Specification