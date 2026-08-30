|  Class |   | Type | b6~4 | Sub-Type  |   |
| --- | --- | --- | --- | --- | --- |
|  b10~9 | Link Command | b8~7 |   | b3~0  |   |
|  00 | LGOOD_n LRTY LBAD LCRD_x LCRD1_x LCRD2_x | 00: LGOOD_n | Reserved (000) | SuperSpeed operation: b3: Reserved; b2~0: HP Sequence Number 000: LGOOD_0, 001: LGOOD_1, ...111: LGOOD_7 SuperSpeedPlus operation: b3~0: HP Sequence Number 0000: LGOOD_0, 0001: LGOOD_1, ... 1111: LGOOD_15  |   |
|   |   |  01: LCRD_x LCRD1_x LCRD2_x |   | Gen 1x1, Gen 1x2, Gen 2x1: b3: Reserved b2: Credit series 0: LCRD_x or LCRD1_x 1: LCRD2_x b1~0: Rx Header Buffer Credit 00: LCRD_A/LCRD1_A/LCRD2_A 01: LCRD_B/LCRD1_B/LCRD2_B 10: LCRD_C/LCRD1_C/LCRD2_C 11: LCRD_D/LCRD1_D/LCRD2_D | Gen 2x2: b3: Credit series 0: LCRD1_x 1: LCRD2_x b2~0: Rx Header Buffer Credit 000: LCRD1_A/LCRD2_A 001: LCRD1_B/LCRD2_B 010: LCRD1_C/LCRD2_C 011: LCRD1_D/LCRD2_D 100: LCRD1_E/LCRD2_E 101: LCRD1_F/LCRD2_F 110: LCRD1_G/LCRD2_G  |
|   |   |  10: LRTY 11: LBAD |   | Reserved (0000)  |   |