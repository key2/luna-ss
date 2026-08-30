Chapter 5: Test Descriptions

1/17/2018

c. An Upstream Facing PUT sends any other packets or LFPS signals.
d. A Downstream Facing PUT sends any other packets or LFPS signals besides a Warm Reset.
e. The PUT enters recovery.

4. Do steps 1 to 3 of the Link Initialization Sequence.

5. The LVS waits for the Port Capability LMP from the PUT.

6. LVS verifies that the Port Capability LMP is valid.

7. The LVS transmits the Port Capability LMP, but does not transmit the Port Configuration LMP (downstream LVS port) or Port Configuration Response LMP (upstream LVS port).

8. The test fails if any of the following occur:

a. The PUT does not transmit the Port Capability LMP.
b. The PUT transitions to eSS.Inactive (downstream PUT) or eSS.Disabled (upstream PUT) before tPortConfiguration deadline.

i. For a PUT with a captive re-timer, the PUT transitions to eSS.Inactive (downstream PUT) or eSS.Disabled (upstream PUT) before tPortConfiguration + tU0Recovery deadline.

c. The PUT does not transition to eSS.Inactive (downstream PUT) or eSS.Disabled (upstream PUT) after tPortConfiguration expires.

i. For a PUT with a captive re-timer, the PUT does not transition to eSS.Inactive (downstream PUT) or eSS.Disabled (upstream PUT) after tPortConfiguration + tU0Recovery expires.

d. An Upstream Facing PUT sends any other packets or LFPS signals.
e. A Downstream Facing PUT sends any other packets or LFPS signals besides a Warm Reset.
f. The PUT enters recovery.

9. Do steps 1 to 3 of the Link Initialization Sequence

10. The LVS does not transmit the Port Capability LMP, but does send the Port Configuration LMP (downstream LVS port) or Port Configuration Response LMP if a Port Configuration LMP is received (upstream LVS port).

11. The test fails if any of the following occur:

a. The PUT does not transmit the Port Capability LMP.
b. The PUT transitions to eSS.Inactive (downstream PUT) or eSS.Disabled (upstream PUT) before tPortConfiguration deadline.

i. For a PUT with a captive re-timer, the PUT transitions to eSS.Inactive (downstream PUT) or eSS.Disabled (upstream PUT) before tPortConfiguration + tU0Recovery deadline.

c. The PUT does not transition to eSS.Inactive (downstream PUT) or eSS.Disabled (upstream PUT) after tPortConfiguration expires.

i. For a PUT with a captive re-timer, the PUT does not transition to eSS.Inactive (downstream PUT) or eSS.Disabled (upstream PUT) after tPortConfiguration + tU0Recovery expires.

d. An Upstream Facing PUT sends any other packets or LFPS signals.
e. A Downstream Facing PUT sends any other packets or LFPS signals besides a Warm Reset.
f. The PUT enters recovery.

75

USB 3.1 Link Layer Test Specification