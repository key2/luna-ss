|   | - Eight consecutive and identical TS2 ordered sets are received. - Sixteen TS2 ordered sets are sent after receiving the first of the eight consecutive and identical TS2 ordered sets. |   |
| --- | --- | --- |
|  7.5.10.4.2#2 | The port in SuperSpeedPlus operation shall transition from Recovery.Configuration to Recovery.Idle after the following two conditions are met: - Eight consecutive and identical TS2 ordered sets, excluding symbols 14 and 15, are received. - Sixteen TS2 ordered sets are sent after receiving the first of the eight consecutive and identical TS2 ordered sets, excluding symbols 14 and 15. | 7.26 7.30  |
|  7.5.10.4.2#3 | A port shall transition from Recovery.Active to eSS.Inactive when either the Ux_EXIT TIMER or the 6-ms timer times out. | NT  |
|  7.5.10.4.2#4 | A downstream port shall transition from Recovery.Active to eSS.Inactive when the transition to Recovery is not to attempt a Hot Reset AND the 6ms timer or Ux_EXIT_TIMER times out. | NT  |
|  7.5.10.3.2#5 | A downstream port shall transition from Recovery.Active to Rx.Detect when the transition to Recovery is to attempt a Hot Reset AND the 6ms timer or the Ux_EXIT_TIMER times out. | 7.31  |
|  7.5.10.4.2#6 | A downstream port shall transition from Recovery.Configuration to Rx.Detect when directed to issue Warm Reset. | NT  |
|  7.5.10.4.2#7 | An upstream port shall transition from Recovery.Configuration to Rx.Detect when Warm Reset is detected. | NT  |
|  Subsection reference: 7.5.10.5 Recovery.Idle  |   |   |
|  Subsection reference: 7.5.10.5.1 Recovery.Idle Requirements  |   |   |
|  7.5.10.5.1#1 | A port in SuperSpeed operation shall transmit Idle Symbols in Recovery.Idle if the next state is U0. | 7.26 7.30  |
|  7.5.10.5.1#2 | A port in SuperSpeed operation shall enable scrambling by default in Recovery.Idle. | 7.26 7.30  |
|  7.5.10.5.1#3 | A port in SuperSpeed operation shall disable the scrambling when directed, or when the Disabling Scrambling bit is asserted in the TS2 ordered set received in Recovery.configuration. | NT  |
|  7.5.10.5.1#4 | A port in SuperSpeedPlus operation shall transmit a single SDS ordered set before the start of the data blocks with Idle Symbols if the next state is U0. | BC  |
|  7.5.10.5.1#5 | A port in SuperSpeedPlus operation shall disable the scrambling upon completion of SDS ordered set transmission if directed or if the Disabling Scrambling bit is asserted in the TS2 ordered set received in Recovery.Configuration. | NT  |