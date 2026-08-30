Universal Serial Bus 3.1 Specification, Revision 1.0

- A Responder shall capture the PTM Local Clock Source timestamps (t2 and t3) when transmitting LDM Response and when receiving LDM Request LMPs.
- A Responder shall issue LDM Response LMP when it possesses the timing values required to populate the LDM Response LMP: timestamps (t2 -t3 in Figure 8-11).
- A Requester shall capture t1 timestamps upon transmitting the last symbol of a LDM Request.
- A Responder shall capture t2 timestamps upon receiving the last symbol of a LDM Request.
- A Responder shall capture t3 timestamps upon transmitting the last symbol of a LDM Response.
- A Requester shall capture t4 timestamps upon receiving the last symbol of a LDM Response.

Note that these rules assume that the Tx and Rx TS Delays in Figure 8-16 are zero, i.e. the Timestamp Measurement Planes and the TS LMP link boundary transmit and receive times are identical. Refer to Section 8.4.8.8 for how to adjust for actual Timestamp Delays.

### 8.4.8.10 LDM and Hubs

A hub is both a Requester and a Responder, and acts as intermediary between its Upstream and Downstream Facing Ports. As a Requester, a hub utilizes the PTM LDM mechanism to issue LDM Requests on its Upstream Facing Port to identify the LDM Link Delay between itself and its upstream Responder. A hub utilizes the PTM HDM mechanism to update the Isochronous Timestamps of ITPs that it forwards downstream.

A hub implementation has LDM Enabled and LDM Valid flags. Their states are determined by the Hub's Requester State Machine. The values of the LDM Enabled or LDM Valid flags in the hub's Responder State Machines track the Requester State Machine values; e.g., if LDM Enabled or LDM Valid in the Requester State Machine transition to 0, then all of the hub's Responder State Machine shall transition to the Responder Disabled state. When both LDM Enabled and LDM Valid in the Requester State Machine transition to 1, then all of the hub's Responder State Machine shall transition to the Init Request state. A hub does not have LDM Enabled or LDM Valid flags per downstream facing port Responder State Machine.

The USB topology is enumerated from the Root Hub port down; i.e., a hub must be in the Configured state before its downstream ports are active. The PTM timing parameters are selected so that, for typical enumeration sequences, the LDM Link Delay is established in a hub before it transitions to the Configured state. This means that the hub's Responder State Machines should be in the Init Request state as soon as its downstream ports are operational and that no software intervention is required to enable LDM. If the Requester of a device attached to a Downstream Facing Port is unable to establish the LDM Link Delay in timely manner, it may transition to the LDM Disabled state and require software to manually start LDM Exchanges. An alternative is for PTM aware enumeration software to verify that PTM capable hubs have established the LDM Link Delay before configuring them.

8-28