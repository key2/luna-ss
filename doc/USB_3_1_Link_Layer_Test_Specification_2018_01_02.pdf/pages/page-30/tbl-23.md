|  7.4.2#6 | An upstream port shall enable its LFPS receiver and Warm Reset detector in all link states except eSS.Disabled. | NT  |
| --- | --- | --- |
|  7.4.2#7 | Upon a completion of a Warm Reset, a downstream port shall reset its Link Error Count. | NT  |
|  7.4.2#8 | Upon a completion of a Warm Reset, Port Configuration information of an upstream port shall be reset to default values. | 7.31  |
|  7.4.2#9 | Upon a completion of a Warm Reset, the PHY level variables shall be reinitialized or retrained. | NT  |
|  7.4.2#10 | Upon a completion of a Warm Reset, the LTSSM of a port shall transition to U0 through Rx.Detect and Polling. | 7.31  |
|  7.4.2#11 | When a PORT_RESET is directed, when the downstream port is in U3, or Loopback, or Compliance Mode, or eSS.Inactive, it shall use Warm Reset. | 7.34  |
|  7.4.2#12 | When a PORT_RESET is directed, when the downstream port is in U0, it shall use Hot Reset. | 7.29  |
|  7.4.2#13 | When a PORT_RESET is directed, when the downstream port is in U1 or U2, it shall exit U1 or U2 using the LFPS exit handshake, transition to Recovery and then transition to Hot Reset. | NT  |
|  7.4.2#14 | When a PORT_RESET is directed, when a downstream port is in a transitory state of Polling or Recovery, it shall use Hot Reset. | NT  |
|  7.4.2#15 | When a PORT_RESET is directed, when a Hot Reset fails due to a LFPS handshake timeout, a downstream port shall transition to eSS.Inactive. | NT  |
|  7.4.2#16 | When a PORT_RESET is directed, when a Hot Reset fails due to a TS1/TS2 handshake timeout, a downstream port shall transition to Rx.Detect and attempt a Warm Reset. | 7.31  |
|  7.4.2#17 | When a PORT_RESET is directed, when the downstream port is in eSS.Disabled, an Inband Reset is prohibited. | NT  |
|  7.4.2#18 | When BH_PORT_RESET is directed, a downstream port shall initiate a Warm Reset in all the link states except eSS.Disabled and transition to Rx.Detect. | NT  |
|  7.4.2#19 | When BH_PORT_RESET is directed, an upstream port shall enable its LFPS receiver and Warm Reset detector in all the link states except eSS.Disabled. | NT  |
|  7.4.2#20 | When BH_PORT_RESET is directed, an upstream port receiving Warm Reset shall transition to Rx.Detect. | NT  |
|  Subsection reference: 7.5 Link Training and Status State Machine (LTSSM)  |   |   |
|  Subsection reference: 7.5.1 eSS.Disabled  |   |   |