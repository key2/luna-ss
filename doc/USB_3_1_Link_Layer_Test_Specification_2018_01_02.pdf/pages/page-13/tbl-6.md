|  7.2.2.1#2 | A link command shall consist of two identical consecutive Link Command Words. | BC  |
| --- | --- | --- |
|  Subsection reference: 7.2.2.2 Link Command Word Definition  |   |   |
|  7.2.2.2#1 | A link command word shall be 16 bits long, with the 11-bit link command information protected by a 5-bit CRC-5. | BC  |
|  7.2.2.2#2 | The CRC-5 shall be computed as specified when transmitted. | BC  |
|  7.2.2.2#3 | Any transmitted link command shall match one of the link commands presented in table 7-4 of USB 3.0 spec. | BC  |
|  Subsection reference: 7.2.2.3 Link Command Placement  |   |   |
|  7.2.2.3#1 | Link commands shall not be placed inside header packet structures. | BC  |
|  7.2.2.3#2 | Link commands shall not be placed within the DPP of a DP structure. | NT  |
|  7.2.2.3#3 | Link commands shall not be placed between the DPH and the DPP. | IOP  |
|  7.2.2.3#4 | Link commands may be placed before and after a header packet with the exception that they shall not be placed in between a DPH and its DPP. | BC IOP  |
|  7.2.2.3#5 | Link commands shall not be sent until all scheduled SKP ordered sets have been transmitted. | NT  |
|  7.2.2.3#6 | For SuperSpeedPlus USB, all link commands shall be placed in data blocks. | BC  |
|  7.2.2.3#7 | For SuperSpeedPlus USB, the placement of a link command may start in any symbol position within a data block, and may cross over to the next consecutive data block. | BC  |
|  Subsection reference: 7.2.3 Logical Idle  |   |   |
|  7.2.3#1 | Idle Symbol shall be transmitted by a port at any time in U0 meeting the logical idle definition. | BC  |
|  Subsection reference: 7.2.4 Link Command Usage for Flow Control, Error Recovery, and Power Management  |   |   |
|  Subsection reference: 7.2.4.1 Header Packet Flow Control and Error Recovery  |   |   |
|  Subsection reference: 7.2.4.1.1 Initialization  |   |   |
|  7.2.4.1.1#1 | A port shall maintain two Tx Header Sequence Numbers, one is the Tx Header Sequence Number which will be assigned to the next header packet to be transmitted (not re-transmitted), and one is the ACK Tx Header Sequence Number which is expected on the next received LGOOD_n acknowledging receipt of a header packet. | BC  |