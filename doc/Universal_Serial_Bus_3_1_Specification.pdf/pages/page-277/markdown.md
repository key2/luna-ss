Link Layer

- An upstream port shall reset its port configuration information to default values. Refer to Sections 8.4.5 and 8.4.6 for details.
- The port in SuperSpeed operation shall enable the scrambling by default if the Disabling Scrambling bit is not asserted in the TS2 ordered set received in Polling.Configuration.
- The port in SuperSpeed operation shall disable the scrambling if directed, or if the Disabling Scrambling bit is asserted in the TS2 ordered set received in Polling.Configuration.
- The port in SuperSpeed operation shall transmit Idle Symbols if the next state is U0. The port may transmit Idle Symbols if the next state is Loopback or HotReset.
- The port in SuperSpeedPlus operation shall transmit a single SDS ordered set before the start of the data blocks with Idle Symbols if the next state is U0. The port may transmit SDS ordered set if the next state is Loopback or Hot Reset.

Note: Under situation where a SKP ordered set is also scheduled at the same time with SDS ordered set, SKP ordered set shall be transmitted first.

- The port in SuperSpeedPlus operation may ignore SDS ordered set if corrupted and continue to process the following data block. The port may optionally choose to recover SDS ordered set if error is detected.
- The port in SuperSpeedPlus operation shall disable the scrambling upon completion of SDS ordered set transmission if directed, or if the Disabling Scrambling bit is asserted in the TS2 ordered set received in Polling.Configuration.
- The port that fails to achieve a successful training with its link partner shall reconfigure itself for the next capability it supports.

Note: An example of this is, when a SuperSpeedPlus port fails to reach successful handshake with its link partner, it shall re-configure itself for SuperSpeed operation.

- A 2-ms timer (tPollingIdleTimeout) shall be started upon entry to this state.
- The port shall be able to receive the Header Sequence Number Advertisement from its link partner.

Note: The exit time difference between the two ports will result in one port entering U0 first and starting the Header Sequence Number Advertisement while the other port is still in Polling.Idle.

### 7.5.4.10.2 Exit from Polling.Idle

- The port shall transition to Loopback when directed as a loopback master and the port is capable of being a loopback master. Refer to Section 7.5.11 for details.
- The port shall transition to Loopback as a loopback slave if the Loopback bit is asserted in the TS2 ordered set received in Polling.Configuration. Refer to Section 7.5.4.9 for details.
- A downstream port shall transition to Hot Reset when directed.
- An upstream port shall transition to Hot Reset when the Reset bit is asserted in the TS2 ordered set received in Polling.Configuration.
- The port shall transition to U0 when the following two conditions are met:

1. Eight consecutive Idle Symbols are received.
2. Sixteen Idle Symbols are sent after receiving one Idle Symbol.

- A downstream port in SuperSpeed operation shall transition to eSS.Disabled when directed.

- A downstream port in SuperSpeed operation shall transition to Rx.Detect upon the 2-ms timer timeout (tPollingIdleTimeout) and the following two conditions are met.

1. The conditions to transition to U0 are not met.
2. cPollingTimeout is less than two.

7-65