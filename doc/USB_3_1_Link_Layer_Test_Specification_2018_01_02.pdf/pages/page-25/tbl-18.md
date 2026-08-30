|  7.2.4.2.4#2 | An upstream port shall send LAU in response to LGO_U3. | 7.25  |
| --- | --- | --- |
|  7.2.4.2.4#3 | An upstream port shall not send any packets or link commands subsequent to sending an LAU. | 7.25  |
|  7.2.4.2.4#4 | Upon issuing LGO_U3, a downstream port shall ignore any packets sent by an upstream port. | 7.35 7.36  |
|  7.2.4.2.4#5 | A downstream port shall send a single LPMA and then transition to U3 when LAU is received. | 7.35 7.36  |
|  7.2.4.2.4#6 | A downstream port shall transition to Recovery and reinitiate U3 entry after re-entry to U0 when all of the following three conditions are met: • PM_LC_TIMER timeout • LAU is not received. • The number of consecutive U3 entry attempts is less than three. | NT  |
|  7.2.4.2.4#7 | An upstream port shall transition to U3 when LPMA is received. | 7.25  |
|  7.2.4.2.4#8 | An upstream port shall transition to U3 when PM_ENTRY TIMER times out and LPMA is not received. | NT  |
|  7.2.4.2.4#9 | A downstream port shall transition to eSS.Inactive when it fails U3 entry on three consecutive attempts. | NT  |
|  Subsection reference: 7.2.4.2.5 Concurrent Low Power Link Management Flow  |   |   |
|  7.2.4.2.5#1 | When a downstream port has sent an LGO_U1, LGO_U2, LGO_U3 and also received an LGO_U1 or LGO_U2, it shall send an LXU. | NT  |
|  7.2.4.2.5#2 | When an upstream port has sent an LGO_U1 or LGO_U2 and also received an LGO_U1, LGO_U2, it shall wait until receipt of an LXU and then send either an LAU or LXU. | NT  |
|  7.2.4.2.5#3 | When an upstream port has sent an LGO_U1 or LGO_U2 and also received an LGO_U3, it shall wait until receipt of an LXU and then send an LAU. | NT  |
|  7.2.4.2.5#4 | When a downstream port is directed by a higher layer to initiate a transition to U3, and a transition to U1 or U2 has been initiated but not yet completed, the port shall first complete the in-process transition to U1 or U2, then return to U0 and request entry to U3. | NT  |
|  Subsection reference: 7.2.4.2.6 Concurrent Low Power Link Management and Recovery Flow  |   |   |
|  7.2.4.2.6#1 | Upon issuing LGO_Ux, the port shall transition to Recovery when a TS1 ordered set is received. | NT  |
|  Subsection reference: 7.2.4.2.7 Low Power Link State Exit Flow  |   |   |