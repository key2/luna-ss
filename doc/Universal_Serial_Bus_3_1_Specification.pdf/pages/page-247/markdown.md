Link Layer

handling also needs to be specified such that any errors that will invalidate or corrupt a packet or a link command can be detected and a link error can be recovered.

There are various types of errors at the link layer. This includes an error on a packet or a link command, or an error during the link training process, or an error when a link is in transition from one state to another. The detection and recovery from those link errors are described with details in this section.

### 7.3.3 Link Error Statistics

To facilitate the quality of the link operation, two counts of link error statistics are implemented and accessible by the upper layer for its decision if port re-configuration is needed.

#### 7.3.3.1 Link Error Count

The Link Error Count is defined to record the number of events when a port transitions from U0 to Recovery to recover an error event. Except for the upstream port in SuperSpeed operation, all ports shall implement the Link Error Count.

The operation of Link Error count shall adhere to the following rules.

- A port in SuperSpeedPlus operation shall implement the Link Error Count that counts up to 65,535 error events. The Link Error Count shall saturate if it has reached its maximum count value.
- The Link Error Count shall be reset to zero in any one of the following conditions.

1. PowerOn Reset
2. Entry to Polling.Idle
3. Directed
4. Hot Reset

- The Link Error Count shall be incremented by one each time a port transitions from U0 to Recovery to recover an error event.

#### 7.3.3.2 Soft Error Count

The Soft Error Count is defined to record the number of error events that are either correctable or detectable and do not require the link to recover through transition to Recovery. Only a port in SuperSpeedPlus operation may optionally implement the Soft Error Count.

The operation of the Soft Error Count shall adhere to the following rules.

- A port in SuperSpeedPlus operation shall count up to 65,535 error events. The Soft Error Count shall saturate if it has reached its maximum count value
- The Soft Error Count shall be reset to zero in any one of the following conditions.

1. PowerOn Reset
2. Entry to Polling.Idle
3. Directed
4. Hot Reset

- The Soft Error Count shall increment by one if any of the following errors is detected.

1. Single-bit error in the block header.
2. CRC-5 or CRC-16 or CRC-32 error.

7-35