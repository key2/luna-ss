Revision 1.1
June 2022

- 140 -

Universal Serial Bus 3.2
Specification

- A port shall have a PENDING_HP_TIMER that is active only in U0 and if one of the following conditions is met:
1. A port has a header packet transmitted but not acknowledged by its link partner, except during the period between receipt of LBAD and retransmission of the oldest header packet in the Tx Header Buffer or Type 1/Type 2 Tx Header Buffer.
2. A port is expecting the Header Sequence Number Advertisement from its link partner.

- The PENDING_HP_TIMER shall be started if one of the following conditions is met:

1. When a port enters U0 in expectation of the Header Sequence Number Advertisement.
2. When a header packet is transmitted and there are no prior header packets transmitted but unacknowledged in the Tx Header Buffers or Type 1/Type 2 Tx Header Buffers.
3. When the oldest header packet is retransmitted in response to LBAD.

- The PENDING_HP_TIMER shall be reset and restarted when a header packet is acknowledged with LGOOD_n and there are still header packets transmitted but unacknowledged in the Tx Header Buffers or Type 1/Type 2 Tx Header Buffers.

- The PENDING_HP_TIMER shall be reset and stopped if one of the following conditions is met:

1. When a Header Sequence Number Advertisement is received.
2. When a header packet acknowledgement of LGOOD_n is received and all the transmitted header packets in the Tx Header Buffers or Type 1/Type 2 Tx Header Buffers are acknowledged.
3. When a header packet acknowledgement of LBAD is received.

- A port shall transition to Recovery if the following two conditions are met:

1. PENDING_HP_TIMER times out.
2. Additionally for SuperSpeed USB, the transmission of an outgoing header packet is completed or the transmission of an outgoing DPP is either completed with DPPEND or terminated with DPPABORT.

Note: This is to allow a graceful transition to Recovery without a header packet being truncated.

For SuperSpeed USB, a CREDIT_HP_TIMER is also specified to cover the period of time from when a header packet has been transmitted and its Remote Rx Header Buffer Credit count is less than four, to when a Remote Rx Header Buffer Credit is received and its Remote Rx Header Buffer Credit count is back to four. The purpose of this timer is to make sure that a Remote Rx Header Buffer Credit is received within a reasonable time limit. This will allow a port sending the header packet to reclaim a Remote Rx Header Buffer Credit within a time limit in order to continue the process of packet transmission. This will also allow a port receiving the header packet enough time to process the header packet.

Similarly for SuperSpeedPlus USB, two CREDIT_HP_TIMERs are specified. A Type 1 CREDIT_HP_TIMER is specified to cover the period of time from when a Type 1 packet has been transmitted and its Remote Type 1 Rx Buffer Credit count is less than four (Gen 1x2 or Gen 2x1) or seven (Gen 2x2), to when a Remote Type 1 Rx Buffer Credit is received and its Remote Type 1 Rx Buffer Credit count is back to four or seven. A Type 2 CREDIT_HP_TIMER is specified to cover the period of time from when a Type 2 packet has been transmitted and

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.