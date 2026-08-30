|  7.2.1.2.1#1 | A data payload packet shall always begin with DPPSTART ordered set. | IOP  |
| --- | --- | --- |
|  7.2.1.2.1#2 | A data payload packet shall always end with DPPEND ordered set to indicate normal ending. | IOP  |
|  7.2.1.2.1#3 | A data payload packet shall always end with DPPABORT ordered set to indicate an abnormal ending. | NT  |
|  Subsection reference: 7.2.1.2.2 Data Packet Payload  |   |   |
|  7.2.1.2.2#1 | The DPP section shall consist of 0 to 1024 bytes of data payload followed by the 4-byte CRC-32. | IOP  |
|  7.2.1.2.2#2 | The CRC-32 shall be calculated as specified when transmitted. | IOP  |
|  7.2.1.2.2#3 | The CRC-32 for a 0 bytes payload shall be 0x00000000. | NT  |
|  7.2.1.2.2#4 | For SuperSpeed USB, any premature termination of a DPP shall end with a DPPABORT ordered set. | NT  |
|  7.2.1.2.2#5 | For SuperSpeedPlus USB, a usb port shall always preserve the DPP boundary by completing the DPP transmission meeting the length field specification defined in its associated DPH except if a downstream port is directed to issue a Warm Reset, or a port is directed to enter Recovery. | NT  |
|  7.2.1.2.2#6 | In all other cases besides the exceptions specified, a port in SuperSpeedPlus operation shall append DPPEND OS upon completing the transmission of DPP, of in the case of a nullified DPP, it shall append DPPABORT OS immediately after its DPH, or in the case of a partially nullified DPP, it shall append DPPABORT OS after completing the DPP as defined by the length field in its associated DPH. | IOP partial coverage  |
|  7.2.1.2.2#7 | A port shall fill with Idle Symbols in DPP if intended data for transmission are not available. | NT  |
|  Subsection reference: 7.2.1.2.3 Data Payload Structure and Spacing between DPH and DPP  |   |   |
|  7.2.1.2.3#1 | There shall be no spacing between a DPH and its corresponding DPP. | IOP  |
|  Subsection reference: 7.2.1.3 SuperSpeedPlus Packet Placement  |   |   |
|  7.2.1.3#1 | For SuperSpeedPlus USB, all packets shall be placed in data blocks and the placement of a packet may start in any symbol position within a data block, and may cross over into the next consecutive data block. | BC  |
|  Subsection reference: 7.2.2 Link Commands  |   |   |
|  Subsection reference: 7.2.2.1 Link Command Structure  |   |   |
|  7.2.2.1#1 | A link command shall be eight symbols long and begin with LCSTART ordered set. | BC  |