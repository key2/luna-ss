|  8.4.6#1 | All Enhanced SuperSpeed ports that supports downstream port capability shall be capable of sending the Port Configuration LMP. | 5.1  |
| --- | --- | --- |
|  8.4.6#2 | When the port that was to be configured in the upstream facing mode does not receive the Port Configuration LMP within tPortConfiguration time after link initialization, the upstream port shall transition to eSS.Disabled and try and connect at the other speeds this device supports. | 7.17  |
|  8.4.6#3 | A port configured in the downstream mode shall send the Port Configuration LMP to the upstream port. | 7.17  |
|  8.4.6#4 | The port sending the Port Configuration LMP shall select only one bit for the Link Speed field. | NT  |
|  8.4.6#5 | The Link Speed field shall only be used when the port is operating at Gen 1 speed. | TBD  |
|  8.4.6#6 | When a downstream capable port cannot work with its link partner, it shall signal an error as described in Section 10.14.2.6. | NT  |
|  Subsection reference: 8.4.7 Port Configuration Response  |   |   |
|  8.4.7#1 | All Enhanced SuperSpeed ports that supports upstream port capability shall be capable of sending the Port Configuration Response LMP. | 5.1  |
|  8.4.7#2 | When the downstream port does not receive the Port Configuration Response LMP within tPortConfiguration time, it shall signal an error as described in Section 10.14.2.6. | NT  |
|  8.4.7#3 | When the Response Code indicates that the Link Speed was rejected by the upstream port, the downstream port shall signal an error as described in Section 10.14.2.6. | NT  |
|  Subsection reference: 8.4.8 Precision Time Measurement  |   |   |
|  Subsection reference: 8.4.8.1 PTM Bus Interval Boundary Counters  |   |   |
|  8.4.8.1#1 | The PTM Delta Counter shall be incremented by the PTM Clock to measure the delay from present time to the previous bus interval boundary. | NT  |
|  8.4.8.1#2 | The PTM Bus Interval Counter shall be incremented when the PTM Delta Counter wraps. | NT  |
|  8.4.8.1#3 | Hosts shall implement a set of PTM Bus Interval Boundary Counters. | NT  |
|  8.4.8.1#4 | PTM capable devices shall implement PTM Bus Interval Boundary Counters. | NT  |
|  Subsection reference: 8.4.8.2 LDM Protocol  |   |   |
|  8.4.8.2#1 | If an LDM Message is received by a port that does not support PTM, then the packet shall be dropped. Note that the port shall | NT  |