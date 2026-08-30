|  Symbol | Name | Gen 1 Symbol | Gen 2 Symbol | Description  |
| --- | --- | --- | --- | --- |
|  SKP | Skip | K28.1 | CCh | Compensates for different bit rates between two communicating ports. SKPs may be dynamically inserted or removed from the data stream. For SuperSpeedPlus operation, unscrambled  |
|  SKPEND | Skip End | Not applicable | 33h | Marks the boundary between SKP symbols and the remainder of the SKP OS. Unscrambled.  |
|  SDP | Start Data Packet | K28.2 | 96h | Marks the start of a Data Packet Payload. For SuperSpeedPlus operation, scrambled and transmitted only in data block.  |
|  EDB | End Bad | K28.3 | 69h | Marks the end of a nullified Packet. For SuperSpeedPlus operation, scrambled and transmitted only in data block.  |
|  SUB | Decode Error Substitution | K28.4 | Not applicable | Symbol substituted by the 8b/10b decoder when a Decode error is detected.  |
|  COM | Comma | K28.5 | Not applicable | Used for symbol alignment.  |
|  --- | --- | K28.6 | Not applicable | Reserved  |
|  SHP | Start Header Packet | K27.7 | 9Ah | Marks the start of a Data Packet (Gen 1 operation only), Transaction Packet or Link Management Packet. For SuperSpeedPlus operation, scrambled and transmitted only in data block.  |
|  DPHP | Start Data Packet Header | Not applicable | 95h | Marks the start of a Data Packet (SuperSpeedPlus only). Scrambled and transmitted only in data block.  |
|  END | End | K29.7 | 65h | Marks the end of a packet. For SuperSpeedPlus operation, scrambled and transmitted only in data block.  |
|  SLC | Start Link Command | K30.7 | 5Ah | Marks the start of a Link Command. For SuperSpeedPlus operation, scrambled and transmitted only in data block.  |