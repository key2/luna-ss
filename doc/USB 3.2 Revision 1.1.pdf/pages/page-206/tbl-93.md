|  LBPM Type |   | LBPM Subtype  |   |   |   |   |   |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  b0 | b1 | b2 | b3 | b4 | b5 | b6 | b7  |
|  [b1:b0] = 00 : PHY Capability |   | [b3:b2] = 00 : 5 Gbps [b3:b2] = 01 : 10 Gbps [b3:b2] = 10/11 : Reserved |   | Reserved (00) |   | 0 : single-lane 1 : dual-lane | Reserved (00)  |
|  [b1:b0] = 01 : PHY Ready | In single-lane operation: Reserved (000000)  |   |   |   |   |   |   |
|   |   |  x2 re-timer to announce its presence: [b4:b2] = 000 : no re-timers [b4:b2] = 001 - 111 : number of re-timers and re-timer address index. Refer to Section E.3.4.2.1 for details. |   |   | Reserved (0) | x2 operation: 0 : UFP 1 : DFP | x2 operation: For DFP: 0 : Config Done. DFP ready to exit 1 : RT Config. DFP to address re-timers For UFP: Reserved (0)  |
|  [b1:b0] = 10/11 : Reserved |   | Reserved  |   |   |   |   |   |