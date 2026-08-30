Chapter 5: Test Descriptions

1/17/2018

11. The test fails if the PUT does not stay in U0 for 50ms.
12. If the PUT includes a captive re-timer:

a. For a DFP:

i. Use USBCV31 Link Layer helper TD 7.18 to initiate an entry to LGO_U1
ii. The test fails if the LVS does not receive an LGO_U1
iii. The LVS sends an LAU and enters U1 after receiving LPMA or PM_ENTRY_TIMER timeout
iv. The test fails if the LVS receives TS1s
v. Wait 1 second
vi. The test fails if the LVS does not receive Ping.LFPSs after 300ms with tBurst and tRepeat as defined in Table 6-30.

b. For a UFP:

i. The LVS sends LGO_U1
ii. The test fails if the LVS does not receive an LAU
iii. The LVS sends an LPMA and enters U1
iv. The test fails if the LVS receives TS1s.
v. Wait 1 second
vi. The test fails if the LVS receives any LFPS

### TD.7.39 PortMatch Retry Test (Gen 2 Only)

This test verifies that the PUT recovers to Polling.PortMatch when the tPollingActiveTimeout expires.

#### Covered Assertions

7.5.4.5.2#2

7.3.10#1

#### Overview of Test Steps

1. Both LVS and PUT detect each other and then transition through Polling to Polling.RxEQ.
2. The LVS does not transmit the TS1 ordered sets during Polling.Active.
3. The test fails if:

a) The PUT does not transition to Polling.PortMatch after tPollingActiveTimeout.
b) The PUT does not transmit the next highest PHY Capability from its previous PHY Capability in its PHY Capability LBPMs.

4. Both LVS and PUT transition through Polling.RxEQ
5. If the PHY Capability was not negotiated to 5Gbps, return to step 2.
6. Both LVS and PUT transmit the TS1 ordered sets during Polling.Active and proceed to U0.
7. The LVS will keep the link active by sending Link Pollings (LUP when it is configured as an Upstream Port or LDN when it is configured as a Downstream Port) for 50ms.

91

USB 3.1 Link Layer Test Specification