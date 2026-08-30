Revision 1.1
June 2022

- xii -

Universal Serial Bus 3.2
Specification

7.3.4.3 Rx Header Sequence Number Error...150
7.3.5 Link Command Errors...150
7.3.6 ACK Tx Header Sequence Number Error...151
7.3.7 Header Sequence Number Advertisement Error...152
7.3.8 SuperSpeed Rx Header Buffer Credit Advertisement Error...152
7.3.9 SuperSpeedPlus Type 1/Type 2 Rx Buffer Credit Advertisement Error...153
7.3.10 Training Sequence Error...153
7.3.11 Gen 1 8b/10b Errors...154
7.3.12 Gen 2x1 Block Header Errors...154
7.3.13 Gen 2x2 Block Header Errors...154
7.3.14 Summary of Error Types and Recovery...155
7.4 PowerOn Reset and Inband Reset...157
7.4.1 PowerOn Reset...157
7.4.2 Inband Reset...158
7.5 Link Training and Status State Machine (LTSSM)...159
7.5.1 eSS.Disabled...161
7.5.1.1 eSS.Disabled for Downstream Ports and Hub Upstream Ports...162
7.5.1.2 eSS.Disabled for Upstream Ports of Peripheral Devices...162
7.5.2 eSS.Inactive...163
7.5.2.1 eSS.Inactive Substate Machines...164
7.5.2.2 eSS.Inactive Requirements...164
7.5.2.3 eSS.Inactive.Quiet...164
7.5.2.4 eSS.Inactive.Disconnect.Detect...164
7.5.3 Rx.Detect...165
7.5.3.1 Rx.Detect Substate Machines...165
7.5.3.2 Rx.Detect Requirements...166
7.5.3.3 Rx.Detect.Reset...166
7.5.3.4 Rx.Detect.Active...166
7.5.3.5 Rx.Detect.Active Requirements...166
7.5.3.6 Exit from Rx.Detect.Active...167
7.5.3.7 Rx.Detect.Quiet...167
7.5.4 Polling...168
7.5.4.1 Polling Substate Machines...168
7.5.4.2 Polling Requirements...169
7.5.4.3 Polling.LFPS...169
7.5.4.4 Polling.LFPSPlus...174
7.5.4.5 Polling.PortMatch...175
7.5.4.6 Polling.PortConfig...177
7.5.4.7 Polling.RxEQ...180
7.5.4.8 Polling.Active...181

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.