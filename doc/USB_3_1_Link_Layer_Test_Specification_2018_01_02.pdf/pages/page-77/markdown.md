Chapter 5: Test Descriptions

1/17/2018

8. The LVs will keep the link active by sending Link Pollings (LUP when it is configured as an Upstream Port, LDN when it is configured as a Downstream Port).
9. The test passes if the exchanges are successful, no timeout is detected, no recovery is entered, the PUT responds to the invalid packets with an LBAD, all other packets are successfully received, all credits are restored and the link stays in U0 for at least 50ms.
10. Repeat steps 7 through 9 for Condition B listed above.

### TD.7.8 TX Header Packet Retransmission Test

This test verifies that the PUT will correctly retransmit a header packet on receipt of an LBAD.

#### Covered Assertions

7.2.4.1.3#1, 2

#### Overview of Test Steps

1. Do steps 1 to 3 of the Link Initialization Sequence.
2. The LVS and the PUT will exchange the Port Configuration transaction, but in this case the LVS will respond to the first packet sent by the PUT with an LBAD.

■ If the LVS is configured as a Downstream Port:

a. LVS waits for the PUT's Port Capability LMP.
b. LVS verifies that the Port Capability LMP is valid.
c. LVS responds to the PUT with an LBAD.
d. LVS waits for the PUT to transmit an LRTY.
e. LVS waits for the retransmitted packet.
f. LVS verifies that the retransmitted packet is the same as the first packet sent by the device.
g. LVS transmits its Port Capability LMP and Port Configuration LMP.
h. LVS waits for the PUT Port Configuration Response LMP.
i. LVS verifies the PUT's Port Configuration Response LMP.

■ If the LVS is configured as an Upstream Port:

a. LVS waits for the PUT's Port Capability LMP.
b. LVS verifies that the Port Capability LMP is valid.
c. LVS transmits its Port Capability LMP.
d. LVS responds to the PUT with an LBAD.
e. LVS waits for the PUT to transmit an LRTY.
f. LVS waits for the retransmitted packet.
g. LVS verifies that the retransmitted packet is the same as the first packet sent by the device.
h. LVS waits for the PUT's Port Configuration LMP.
i. LVS verifies that the Port Configuration LMP is valid.
j. LVS transmits its Port Configuration Response LMP.

69

USB 3.1 Link Layer Test Specification