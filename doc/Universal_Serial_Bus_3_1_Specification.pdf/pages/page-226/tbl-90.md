|  Class |   | Type | b6~4 | Sub-Type  |
| --- | --- | --- | --- | --- |
|  b10~9 | Link Command | b8~7 |   | b3~0  |
|  00 | LGOOD_n LRTY LBAD LCRD_x LCRD1_x LCRD2_x | 00: LGOOD_n | Reserved (000) | b3: Reserved b2~0: HP Sequence Number 000: LGOOD_0 001: LGOOD_1 010: LGOOD_2 011: LGOOD_3 100: LGOOD_4 101: LGOOD_5 110: LGOOD_6 111: LGOOD_7  |
|   |   |  01: LCRD_x LCRD1_x LCRD2_x |   | b3: Reserved b2: Credit series 0: LCRD_x or LCRD1_x 1: LCRD2_x b1~0: Rx Header Buffer Credit 00: LCRD_A/LCRD1_A/LCRD2_A 01: LCRD_B/LCRD1_B/LCRD2_B 10: LCRD_C/LCRD1_C/LCRD2_C 11: LCRD_D/LCRD1_D/LCRD2_D  |
|   |   |  10: LRTY 11: LBAD |   | Reserved (0000)  |
|  01 | LGO_Ux LAU LXU LPMA | 00: LGO_Ux |   | 0001: LGO_U1 0010: LGO_U2 0011: LGO_U3 Others: Reserved  |
|   |   |  01: LAU 10: LXU 11: LPMA |   | Reserved (0000)  |
|  10 | LDN LUP | 00: LUP 11: LDN Others: Reserved |   | Reserved (0000)  |
|  11: Reserved | Reserved | Reserved (0000) |  | Reserved (0000)  |