Power Management

System software configures and then enables each device to initiate U1 entry. The primary programming parameters involved in setting up hardware autonomous link state management include:

**U1DevExitLat** – Parameter used by devices to report their maximum U1 to U0 exit latency (refer to Chapter 9 for details).

**PORT_U1_TIMEOUT** – Sets the value for the downstream port’s U1 inactivity timer. When specifying a value between the range 0x01-0xFE it also enables the downstream port to send U1 entry transition requests to its link partner (refer to Chapter 10 for details).

**U1_Enable** – Enables an upstream port to initiate requests for transition into U1 (refer to Chapter 9 for details).

The U1_Enable feature controls whether that particular upstream port may initiate U1 entry. Regardless of whether the upstream port is enabled for U1 entry initiation or not, it still responds to requests for U1 entry from its link partner, either accepting or rejecting the transition request.

The following table illustrates the relationship between the downstream timeout and the upstream U1_Enable to configure the platform for any combination of port link state management. For example, if U1_Enable is enabled, and PORT_U1_TIMEOUT is set to FFH, then only the upstream port may initiate requests for transition to U1.

[tbl-269.md](tbl-269.md)

For detailed information regarding the specifics of the U1 entry process, refer to Chapter 7 of this specification.

### C.1.1.3.2 Exiting the U1 State

There are two ways to exit the U1 state. The link can return to the active U0 state or it can transition into a deeper power savings state (U2).

# **Transitioning from U1 → U0**

Either link partner can initiate a transition from U1 → U0. This transition is normally initiated when a packet needs to be transmitted, such as an IN message from the host, or an ERDY message from a device. The transition process is initiated by first signaling a Low Frequency Periodic Signaling (LFPS) handshake. This is followed by link recovery and training sequences. Refer to Chapter 6 and 7 respectively.

# **Transitioning from U1 → U2**

This transitions the link to an even lower power state and is triggered by a second inactivity timer (U2 inactivity timer). When a link enters U1, this starts the U2 inactivity timer. If the U2 inactivity timer expires while the link is still in U1, then both link partners transition silently from U1 → U2 without additional bus activity. The next sections discuss this in more detail.

C-3