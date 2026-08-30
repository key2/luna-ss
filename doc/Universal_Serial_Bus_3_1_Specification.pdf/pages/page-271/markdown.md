Link Layer

1. No LFPS signal for more than tPollingSCDLFPSTimeout is observed.

Note: This condition implies the SuperSpeed link partner has entered Polling.RxEQ transmitting TSEQ ordered sets.

2. Twenty Polling.LFPS bursts are transmitted, after finding no SCD2 is detected.

Note: This condition guarantees that, in the case of a port in SuperSpeedPlus operation connecting to a port in SuperSpeed operation, a port in SuperSpeed operation will receive twenty consecutive Polling.LFPS to exit from this substate if it is unable to recognize Polling.LFPS with varying tRepeat in SCD1 and SCD2, and it happens to transmit Polling.LFPS matching SCD1.

- A downstream port shall transition to Rx.Detect upon the 360-ms timer timeout (tPollingLFPSTimeout) and cPollingTimeout is less than two.
- A downstream port shall transition to eSS.Inactive upon the 360-ms timer timeout (tPollingLFPSTimeout) and cPollingTimeout is two.
- An upstream port of a hub shall transition to Rx.Detect upon the 360-ms timeout (tPollingLFPSTimeout).
- A peripheral device shall transition to eSS.Disabled upon the 360-ms timeout (tPollingLFPSTimeout).
- A downstream port shall transition to eSS.Disabled when directed.
- A downstream port shall transition to Rx.Detect when directed to issue Warm Reset.
- An upstream port shall transition to Rx.Detect when Warm Reset is detected.

### 7.5.4.5 Polling.PortMatch

Polling.PortMatch is a substate where the two ports in SuperSpeedPlus operation perform the LBPM handshake, for announcing, matching, and deciding the operation on the highest common capability between the two link partners. The LBPM handshake includes two stages of operation. The first stage is to announce LBPM PHY Capability as defined in Table 7-13 below. The second stage is for each port to decode LBPM PHY Capability and adjust to the highest common PHY Capability by transmitting PHY Capability Match.

#### 7.5.4.5.1 PHY Capability LBPM Definition

SuperSpeedPlus PHY Capability is defined based on the following LBPM. Refer to Section 6.9.5 for LBPM details.

Table 7-13. PHY Capability LBPM

[tbl-102.md](tbl-102.md)

Two types of LBPM are defined. PHY Capability LBPM is used to announce a port's PHY capabilities. The initial value shall describe a port's highest PHY capabilities. The announced capabilities may later be adjusted in order to match the link partner's capabilities or if the link fails to reach U0 during training and the two ports need to fall back to a lower rate.

7-59