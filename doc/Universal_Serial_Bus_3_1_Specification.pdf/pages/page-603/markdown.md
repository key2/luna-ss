Power Management

# Transitioning directly to U2 from U0

A downstream port can be configured for direct, hardware autonomous transition from U0 → U2 by programming its U1 inactivity timer to zero while programming its U2 inactivity timer with a non-zero value in the range 0x01- 0xFE. In this case, when the U2 inactivity timer expires, the downstream port initiates U2 entry from U0.

When a port initiates U2 entry from U0, its link partner may either accept or reject the request. The link level U0 → U2 transition process consists of one port transmitting an LGO_U2 Link Command, and its link partner responding with either an LAU (accept the request) or an LXU (reject the request) Link Command.

# Exiting U2

Exiting U2 can only result in a link state transition to U0. Either link partner can initiate U2 exit, which is initiated when a packet needs to be transmitted. The exit process is similar to that of a U1 → U0 transition, consisting of a Low Frequency Periodic Signaling handshake followed by link recovery and training.

# C.1.1.5 U3 – Link Suspend

The U3 state is a deep power saving state where portions of device power may be removed, except as needed to perform the following functions:

- For upstream ports in devices and hubs:

- Warm Reset signaling detection
- Wakeup signaling detection (for host initiated wakeup)
- Wakeup signaling transmission (for remote wakeup capable devices)

- For downstream ports in hubs and hosts:

- Warm Reset generation
- Disconnect event detection
- Wakeup signaling detection (for remote wakeup)
- Wakeup signaling transmission (for host initiated wakeup)

The purpose of U3 is to minimize power consumption during device or system suspend.

Vbus remains active during U3. Any power rail switching by devices is implementation specific and beyond the scope of this specification.

# Entering the U3 State

U3 entry may only be initiated by the host (refer to Chapter 10 for details). Software typically implements an inactivity timeout for the purpose of placing a function into suspend following a long period of inactivity.

When a downstream port initiates a U3 entry request, its link partner is not allowed to reject it. The downstream port sends an LGO_U3 Link Command, and its link partner responds with an LAU Link Command (refer to Chapter 7 for details).

C-5