|  Subsection reference: 7.2.4.2.3 U1/U2 Entry Flow  |   |   |
| --- | --- | --- |
|  7.2.4.2.3#1 | A port shall send a signal LGO_U1 or LGO_U2 to request a transition to a low power link state. | 7.18-19  |
|  7.2.4.2.3#2 | A port shall either accept LGO_Ux with a single LAU or shall reject LGO_U1 or LGO_U2 with a single LXU and remain in U0. | 7.23-24  |
|  7.2.4.2.3#3 | Upon sending LGO_U1 or LGO_U2, a port shall not send any packets until it has received LXU or re-entered U0. | 7.18-19  |
|  7.2.4.2.3#4 | Upon sending LGO_U1 or LGO_U2, a port shall continue receiving and processing packets and link commands. | 7.18-19  |
|  7.2.4.2.3#5 | Upon receiving LXU, a port shall remain in U0. | NT  |
|  7.2.4.2.3#6 | A port shall initiate transition to Recovery when a single LAU or LXU is not received upon PM_LC_TIMER timeout. | 7.21  |
|  7.2.4.2.3#7 | Upon receiving LAU, a port shall send a single LMPA and then the requested low power link state. | 7.18-19  |
|  7.2.4.2.3#8 | Upon issuing LAU or LPMA, a port shall not send any packets or link commands. | 7.18-19 7.22 7.23-24  |
|  7.2.4.2.3#9 | A port that sends LAU shall enter the corresponding low power link state upon receipt of LPMA before PM_ENTRY_TIMER timeout. | 7.23-24  |
|  7.2.4.2.3#10 | A port that sends LAU shall enter the low power link state upon PM_ENTRY_TIMER timeout and all of the following conditions are met: • LPMA is not received. • No TS1 ordered set is received. | 7.22  |
|  7.2.4.2.3#11 | A port that sent LAU shall enter Recovery before PM_ENTRY_TIMER timeout when a TS1 ordered set is received. | NT  |
|  7.2.4.2.3#12 | A port that has sent LAU shall not respond with Ux_LFPS exit handshake before PM_ENTRY_TIMER timeout. | 7.22  |
|  7.2.4.2.3#13 | A port in U1 shall enter U2 directly when the following two conditions are met: • The port's U2 inactivity timer is enabled. • The U2 inactivity timer times out and no U1 LFPS exit signal is received. | NT  |
|  Subsection reference: 7.2.4.2.4 U3 Entry Flow  |   |   |
|  7.2.4.2.4#1 | When directed, a downstream port shall initiate U3 entry process by sending LGO_U3. | 7.35 7.36  |