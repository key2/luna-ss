Revision 1.1
June 2022

- 501 -

Universal Serial Bus 3.2
Specification

○ LBPM
○ Warm Reset

• The re-timer shall forward the LFPS signals meeting the electrical and timing requirements defined in Section 6.9. The re-timer shall perform the following when forwarding the LFPS signals.

○ If the received signal is Polling.LFPS or SCD1/SCD2, the re-timer shall qualify between Polling.LFPS and SCD1/SCD2. The re-timer may buffer the maximum of one Polling.LFPS for implementation specific need.
○ If the received signal is Polling Warm Reset, it shall ensure that the forwarded Warm Reset meets the timing specification defined in Section 6.9. Note that if a re-timer does store and forward one Polling.LFPS, it is allowed to truncate the starting part of LFPS of Warm Reset, but the truncation shall be less than 20 μs.

• The re-timer shall participate the PHY capability negotiation between a hub DFP and a device UFP. It shall monitor and decode the received PHY Capability LBPM and perform the following.

○ A x1 only re-timer shall reset bits[7:4] of received PHY Capability LBPM.
○ A re-timer shall monitor [b3:b2] of the received PHY Capability LBPM. If the highest port capability defined in [b3:b2] is not "00" or "01", it shall update [b3:b2] to match its highest data rate before forwarding the PHY Capability LBPM.
○ If the re-timer's PHY capability is lower than the PHY capability specified in the received PHY Capability LBPM, it shall modify the received PHY Capability LBPM to match its highest PHY capability.
○ If the re-timer's PHY capability is equal to or higher than the PHY capability specified in the received PHY Capability LBPM, it shall forward the received PHY Capability LBPM as is.
○ The re-timer may store, update, and forward the received LBPM with maximum delay of one LBPM.
○ If the received LBPM does not match PHY Capability LBPM, i.e. bits[1:0] of the received LBPM is not "00", but "01", or "10", or "11", the re-timer shall forward the LBPM with the rest of the bit field reset to "00,0000". Note that this requirement does not apply when the re-timer is Polling.PortConfig.

• The re-timer shall continue the tPollingLFPSTimeout timer upon entry to this sub-state.
• The re-timer shall start the tPollingLBPMLFPSTimeout timer upon observing LBPM.
• The re-timer shall implement a tPollingSCDLFPSTimeout timer at both ports to monitor the absence of LFPS signal at both ports after the completion of SuperSpeed Polling.LFPS handshake at its receivers.
• The re-timer shall disable the tPollingSCDLFPSTimeout timer upon detecting successful SCD2 handshake.

### E.3.4.1.2 Exit from Polling.SpeedDetect

• The re-timer shall transition to Polling.RxEQ for SS operation if the following two conditions are met.

○ Re-timer successfully observed on each port that at least four consecutive Polling.LFPS bursts are transmitted after receiving one.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.