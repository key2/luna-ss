Chapter 5: Test Descriptions

1/17/2018

# Overview of Test Steps

1. Perform the Link Initialization Sequence to bring the LVS and PUT link to U0. The PUT host controller machine enumerates the LVS.
2. The LVS software prompts the test operator to put the PUT host controller machine to sleep or, if the DUT is an Embedded Host and power is lost to the host during sleep, to U3.
3. The LVS waits to receive an LGO_U3 from the PUT.
4. The LVS sends an LAU when it receives an LGO_U3 from the PUT.
5. The LVS waits to receive an LPMA from the PUT.
6. The test fails if any of the following occur:

a. The LVS does not receive an LGO_U3
b. The LVS does not receive an LPMA before PM_ENTRY_TIMER deadline.

7. The LVS prompts the test operator to verify that the host controller machine is in a sleep state.
8. The LVS prompts the test operator to wake the host controller machine.
9. The LVS waits to receive a U3 Exit LFPS from PUT.
10. The test fails if no U3 Exit LFPS is received.
11. The LVS sends a U3 Exit LFPS 5ms after detecting an LFPS from the PUT.
12. The LVS and PUT transition through Recovery to U0.
13. The LVS will keep the link active by sending Link Pollings (LUP when it is configured as an Upstream Port or LDN when it is configured as a Downstream Port) for 50ms.

# TD.7.37 Packet Pending Test (Upstream Port Only)

This test verifies that the PUT releases its Packet Pending flag at the end of a Control Transfer.

# Covered Assertions

8.6#1

# Overview of Test Steps

1. Perform the Link Initialization Sequence to bring the LVS and PUT link to U0. The LVS enumerates the PUT to a configured state.
2. If the PUT is an US port of a hub, the LVS issues a SetPortFeature(PLS=4) for each DS port on the hub.
3. The LVS software issues a GetDescriptor request SETUP packet, with the PP bit set to 1.
4. The LVS sends an ACK TP, with the PP bit set to 1, to start the IN stage of the GetDescriptor request.
5. The LVS waits to receive IN data from the PUT.
6. The LVS software issues a GetDescriptor STATUS packet, with a PP bit set to 0.
7. The LVS waits to receive ACK TP from the PUT, concluding the GetDescriptor request.
8. The test fails if the GetDescriptor request is not completed.
9. The LVS sends an LGO_U1 and waits to receive LAU from the PUT.
10. The test fails if the PUT does not send an LAU.

89

USB 3.1 Link Layer Test Specification