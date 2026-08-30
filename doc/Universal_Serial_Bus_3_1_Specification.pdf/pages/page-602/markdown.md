Universal Serial Bus 3.1 Specification, Revision 1.0

### C.1.1.4 U2 – Link Idle with Slow Exit

The purpose of the U2 link state is to use less power than the U1 state, however at the cost of increased exit latency. For example, clock generation circuitry may be quiesced in order to save additional power in comparison with U1. Under some implementation-specific circumstances, this may not make sense. For example, a hub may share one PLL across all of its ports so the PLL cannot be quiesced unless all of its ports are in U2.

The primary parameters involved in configuring a port for U2 link transitions include:

U2DevExitLat – Parameter used by devices to report their maximum U2 to U0 exit latency (refer to Chapter 9 for details).

PORT_U2_TIMEOUT – Sets the value of a downstream port's U2 inactivity timer. When specified with a value in the range 0x01-0xFE it also enables the downstream port to initiate U2 entry transition requests to its link partner (refer to Chapter 10 for details).

U2_Enable – Enables an upstream port to initiate requests for transitions into U2 (refer to Chapter 9 for details).

The U2_Enable feature controls whether an upstream port may initiate U2 entry from U0. Regardless of whether the upstream port is enabled for U2 entry initiation or not, it still responds to requests for U2 entry from its link partner, either accepting or rejecting the transition request.

The following table illustrates the relationship between the downstream timeout and the upstream U2_Enable to configure the platform for any combination of port link state management. For example, if U2_Enable is enabled, and PORT_U2_TIMEOUT is set to FFH, then only the upstream port may initiate requests for transition to U2.

[tbl-270.md](tbl-270.md)

### Transitioning from U1 → U2

U2 is typically entered directly from U1 as mentioned earlier. The U2 inactivity timer starts when a link enters U1, and when the U2 inactivity timer expires both link partners silently transition from U1 → U2.

Both link partners must be configured with the same U2 inactivity timeout value. This is done by first having software program the U2 inactivity timeout in the downstream port. The downstream port then sends an LMP containing the U2 inactivity timeout value to its link partner. Any changes to this value on the downstream port are also updated with the link partner in the same manner (refer to Chapter 10).

Note that U2 inactivity timer synchronization between link partners can never be perfect so there can be brief periods of time where one port is in U2 while its link partner is still in U1. However given that the U1 → U0 and U2 → U0 state transition processes are compatible with one another this corner condition is handled cleanly.

C-4