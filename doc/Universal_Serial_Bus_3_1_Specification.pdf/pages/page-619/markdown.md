Power Management

3. The last component of the end to end exit latency is characterized by the larger of Hub1_UP:U1DEL and RP2:U1DEL which represents the Link2 exit latency (Link2_EL).

End to end exit latency = Max(Link3_EL, (Link2_EL + tHubPort2PortU1ExitLat))
U2 → U0 Transition Latency

This example highlights the end to end latency incurred when transitioning both Link2 and Link3 from U2 → U0. For the purposes of this example it is assumed that all link partners are enabled for U2 and that both Link2 and Link3 are currently in the U2 state.

1. Dev2 is prepared to send a packet upstream to the host. However, it first needs to bring Link3 out of U2 and back to U0 before it is able to send the packet. Dev2 begins the process by transmitting LFPS to Hub1:DP2 which then starts both link partners transitioning in parallel towards U0. The Link3 exit latency (Link3_EL) is characterized by the larger of Dev2_UP:U2DEL and Hu1b_DP2:U2DEL.
2. After a latency of tHubPort2PortU2EL, the time it takes the hub to determine that one of its downstream ports is awakening, the hub then begins signaling LFPS on Link2 to initiate transition of the Link2 partners (hub's upstream port and host controller root port RP2) to U0.
3. The last component of the end to end exit latency is characterized by the larger of Hub1_UP:U2DEL and RP2:U2DEL which represents the Link2 exit latency (Link2_EL).

End to end exit latency = Max(Link3_EL, Link2_EL + tHubPort2PortU2EL)

### C.3 Device-Initiated Link Power Management Policies

Power savings resulting from the effective use of link power management can have a significant impact on system power consumption. For example, without using link power management, the average battery life of a typical notebook computer could be decreased by as much as 15%.

Both devices and downstream ports can initiate U1 and U2 entry.

- Downstream ports have inactivity timers used to initiate U1 and U2 entry. Downstream port inactivity timeouts are programmed by system software.
- Devices may have additional information available that they can use to decide to initiate U1 or U2 entry more aggressively than inactivity timers.

This section describes policies for devices to initiate U1 or U2.

### C.3.1 Overview and Background Information

Devices can save significant power by initiating U1 or U2 more aggressively rather than waiting for downstream port inactivity timeouts. For example, an isochronous device may substantially increase U1 residency by initiating U1 upon completion of isochronous transfers within each service interval.

Devices can use the following information to help determine when to initiate U1 or U2 due to endpoint idle conditions:

- The type of device endpoints and related flags (refer to Chapter 8)

- Packets Pending flag, used with bulk endpoints
- End of Burst flag, used with interrupt endpoints
- Last Packet flag, used with isochronous endpoints

C-21