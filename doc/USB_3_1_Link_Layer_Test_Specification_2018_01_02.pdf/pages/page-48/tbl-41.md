|  7.5.10.3.1#4 | The port in SuperSpeedPlus operation shall perform block alignment and scrambler synchronization. | BC  |
| --- | --- | --- |
|  Subsection reference: 7.5.10.3.2 Exit from Recovery.Active  |   |   |
|  7.5.10.3.2#1 | A port in SuperSpeed operation shall transition from Recovery.Active to Recovery.Configuration after eight consecutive and identical TS1 or TS2 ordered sets are received. | 7.267.30  |
|  7.5.10.3.2#2 | A port in SuperSpeedPlus operation shall transition from Recovery.Active to Recovery.Configuration after eight consecutive and identical TS1 or TS2 ordered sets are received, excluding symbols 14 and 15 of TS1 or TS2 ordered sets. | 7.267.30  |
|  7.5.10.3.2#3 | A port shall transition from Recovery.Active to eSS.Inactive when either the Ux_EXIT TIMER or the 12-ms timer times out. | NT  |
|  7.5.10.3.2#4 | A downstream port shall transition from Recovery.Active to eSS.Inactive when the transition to Recovery is not to attempt a Hot Reset AND the 12ms timer or Ux_EXIT_TIMER times out. | NT  |
|  7.5.10.3.2#5 | A downstream port shall transition from Recovery.Active to Rx.Detect when the transition to Recovery is to attempt a Hot Reset AND the 12ms timer or the Ux_EXIT_TIMER times out. | 7.31  |
|  7.5.10.3.2#6 | A downstream port shall transition from Recovery.Active to Rx.Detect when directed to issue Warm Reset. | NT  |
|  7.2.10.3.2#7 | An upstream port shall transition from Recovery.Active to Rx.Detect when Warm Reset is detected. | NT  |
|  Subsection reference: 7.5.10.4 Recovery.Configuration  |   |   |
|  Subsection reference: 7.5.10.4.1 Recovery.Configuration Requirements  |   |   |
|  7.5.10.4.1#1 | The port shall transmit identical TS2 ordered sets upon entry to Recovery.Configurationand set the Reset bit, when directed. | 7.287.29  |
|  7.5.10.4.1#2 | If port that has Loopback Master Capability and is directed to go to Loopback, it shall transmit identical TS2 ordered sets with the Loopback bit set upon entry to Recovery.Configuration. | NT  |
|  7.5.10.4.1#3 | If directed to disable scrambling, a port shall transmit identical TS2 ordered sets upon entry to this Recovery.Configuration with the Disabling Scrambling bit set. | NT  |
|  7.5.10.4.1#4 | The port in SuperSpeedPlus operation shall insert a SYNC ordered set every 32 TS2 ordered sets. | BC  |
|  7.5.10.4.1#5 | The port in SuperSpeedPlus operation shall perform block alignment and scrambler synchronization. | BC  |
|  Subsection reference: 7.5.10.4.2 Exit from Recovery.Configuration  |   |   |
|  7.5.10.4.2#1 | The port in SuperSpeed operation shall transition from Recovery.Configuration to Recovery.Idle after the following two conditions are met: | 7.267.30  |