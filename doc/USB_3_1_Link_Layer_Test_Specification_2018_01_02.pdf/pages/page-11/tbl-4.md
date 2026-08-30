|  Assertion # | Assertion Description | Test #  |
| --- | --- | --- |
|  Chapter 7 Test Assertions: Link Layer  |   |   |
|  Subsection reference: 7.2 Link Management and Flow Control  |   |   |
|  Subsection reference: 7.2.1 Packets and Packet Framing  |   |   |
|  Subsection reference: 7.2.1.1 Header Packet Structure  |   |   |
|  7.2.1.1#1 | For SuperSpeed USB, all header packets shall be 20 symbols long. This includes LMPs, TPs, ITPs, and DPHs. A header packet consists of three parts: a header packet framing, a packet header, and a Link Control Word. | BC  |
|  7.2.1.1#2 | For SuperSpeedPlus USB, all header packets except for non-deferred DPH shall be 20 symbols long. The non-deferred SuperSpeedPlus DPH is a header packet with its own framing ordered set, and contains a length field replica immediately after the Link Control Word. | BC  |
|  Subsection reference: 7.2.1.1.1 Header Packet Framing  |   |   |
|  7.2.1.1.1#1 | All header packets except for non-deferred SuperSpeedPlus DPH shall always begin with HPSTART ordered set. | BC  |
|  7.2.1.1.1#2 | A non-deferred SuperSpeedPlus data packet header shall always begin with DPHSTART ordered set. | BC  |
|  7.2.1.1.1#2 | A deferred SuperSpeedPlus data packet header shall always begin with HPSTART ordered set and it shall contain the length field replica. | BC  |
|  Subsection reference: 7.2.1.1.2 Packet Header  |   |   |
|  7.2.1.1.2#1 | A packet header shall consist of 12 bytes of header information and a 2-byte CRC-16. | BC  |
|  7.2.1.1.2#2 | The CRC-16 shall be calculated as specified when transmitted. | BC  |
|  Subsection reference: 7.2.1.1.3 Link Control Word  |   |   |
|  7.2.1.1.3#1 | The Link Control Word shall contain a 3-bit Header Sequence Number, 3-bit Reserved, a 3-bit Hub Depth Index, a Delayed bit (DL), a Deferred bit (DF), and a 5-bit CRC-5. | BC  |
|  7.2.1.1.3#2 | The CRC-5 shall be calculated as specified when transmitted. | BC  |
|  Subsection reference: 7.2.1.2 Data Packet Payload Structure  |   |   |
|  Subsection reference: 7.2.1.2.1 Data Packet Payload Framing  |   |   |