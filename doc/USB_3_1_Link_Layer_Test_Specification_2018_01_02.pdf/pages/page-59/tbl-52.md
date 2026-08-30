|  8.4.8.9#2 | A Responder shall capture the PTM Local Clock Source timestamps (t2 and t3) when transmitting LDM Response and when receiving LDM request LMPs. | NT  |
| --- | --- | --- |
|  8.4.8.9#3 | A Responder shall issue LDM Response LMP when it possesses the timing values required to populate the LDM Response LMP: timestamps (t2-t3 in Figure 8-11). | NT  |
|  8.4.8.9#4 | A Requester shall capture t1 timestamps upon transmitting the last symbol of a LDM Request. | NT  |
|  8.4.8.9#5 | A Responder shall capture t2 timestamps upon receiving the last symbol of a LDM Request. | NT  |
|  8.4.8.9#6 | A Responder shall capture t3 timestamps upon transmitting the last symbol of a LDM Response. | NT  |
|  8.4.8.9#7 | A Requester shall capture t4 timestamps upon receiving the last symbol of a LDM Response. | NT  |
|  Subsection reference: 8.4.8.10 LDM and Hubs  |   |   |
|  8.4.8.10#1 | On a hub, when both LDM Enabled and LDM Valid in the Requester State Machine transition to 1, then all of the hub's Responder State Machine shall transition to the Init Request state. | NT  |
|  Subsection reference: 8.6 Data Packet (DP)  |   |   |
|  8.6#1 | If no endpoints on this device have packets pending, then the device can use this information to aggressively manage its upstream link, e.g., set the link to a lower power U1 or U2 state. | 7.37  |
|  Chapter 10 Test Assertions: Hub, Host Downstream Port, and Device Upstream Port Specification  |   |   |
|  Subsection reference: 10.2 Hub Power Management  |   |   |
|  Subsection reference: 10.2.2 Hub Downstream Port U1/U2 Timers  |   |   |
|  10.2.2#6 | If a hub has received a valid packet on its upstream port that is routed to a downstream port, it shall reject U1 or U2 link entry attempts on the downstream port until the packet has been successfully transmitted. | NT  |
|  10.2.2#7 | Hub implementation ensures no race condition when a header packet that has not been deferred is queued for transmission on a downstream port with a link that is in U1, U2, or is in the process of entering U1, U2 | NT  |
|  Subsection reference: 10.3: Hub Downstream Facing Ports  |   |   |
|  Subsection reference: 10.3.1: Hub Downstream Facing Port State Descriptions  |   |   |
|  Subsection reference: 10.3.1.6: DSPORT.Resetting  |   |   |