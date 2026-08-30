| Width (bits) | Offset (DW:bit) | Description |
| --- | --- | --- |
| 4 | 0:5 | **Subtype.** These 4 bits identify the Link Packet Subtype. |
| **Value** | **Type of LMP** |
| 0000b | Reserved |
| 0001b | Set Link Function |
| 0010b | U2 Inactivity Timeout |
| 0011b | Vendor Device Test |
| 0100b | Port Capability |
| 0101b | Port Configuration |
| 0110b | Port Configuration Response |
| 0111b | Precision Time Management |
| 1000b-1111b | Reserved |
| 16 | 3:0 | **CRC-16.** This field is the CRC calculated over the preceding 12 bytes. Refer to Section 7.2.1.1.2 for the polynomial used to calculate this value. |