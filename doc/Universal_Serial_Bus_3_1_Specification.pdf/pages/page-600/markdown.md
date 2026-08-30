Universal Serial Bus 3.1 Specification, Revision 1.0

### C.1.1.1 Summary of Link States

Table C-1 provides a summary characterization of the SuperSpeed link states.

Table C-1. Link States and Characteristics Summary

[tbl-268.md](tbl-268.md)

Notes:

1. It is possible, under system test conditions, to instrument software initiated U1 and U2 state transitions.

2. From a power efficiency perspective it is desirable for devices to turn off their clock generation circuitry (e.g., their PLL) during the U2 link state.

### C.1.1.2 U0 – Link Active

U0 is the fully operational, link active state. Packets of any type may be communicated over a link that is in the U0 State.

### C.1.1.3 U1 – Link Idle with Fast Exit

U1 is a power saving state this is characterized by fast transition time back to the U0 State. Note that the predominant latency, when transitioning from the U1 → U0 state is imposed by the time that is required to achieve symbol lock between the two link partners.

### C.1.1.3.1 U1 Entry

Either link partner for a given link can request a transition to the U1 link state. All downstream ports (hub or root ports) track inactivity using an inactivity timer mechanism. When a port's inactivity timer expires, if enabled, it requests transition to the U1 state. Upstream ports may also initiate U1 entry based on device specific policies.

When a port initiates U1 entry, its link partner may either accept or reject the request. The link level U0 → U1 transition process consists of one port transmitting an LGO_U1 link command, and its link partner responding with either an LAU (accept the request) or an LXU (reject the request) link command.

The most typical reason for rejecting a U1 transition request would be because the requesting port's link partner has some activity which will shortly require a packet transmission. Downstream ports would also reject a U1 transition request if not enabled to accept U1 transition requests. Rejection of a U1 transition request by an upstream port simply resets and restarts the requesting link partner's inactivity timer.

C-2