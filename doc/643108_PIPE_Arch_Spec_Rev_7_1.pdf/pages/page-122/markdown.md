intel®

Table 8-1. USB4 PHY Power States (Sheet 2 of 2)

[tbl-130.md](tbl-130.md)

1. LFPS detector enablement is controlled by the MAC in the case that the PHY implements the "RxEIDetectDisable" control wire.

2. The total latency is defined as the time interval to enter a state and exit back to P0. The intention is to ensure the return to a fully active state in the case of wake event race scenario. Budget includes turn OFF and ON of PLL when the power state allows. In the case that the PHY has completed the entry phase, this delay can be considered as the exit latency budget in which the PHY can take extra power optimizations.

Additional descriptions of each power state are:

- P0: Fully active the power state. The transmitter and receiver are ON.
- P0rx: Transmitter only power state. The receiver is OFF. Suitable for unidirectional traffic (for instance, transmitting the tunneled DisplayPort traffic).
- P1: Transmitter and receiver are OFF. This power state provides power savings while meeting low latency exit requirements.
- P2: Similar to P1 but with an increased total latency budget. The MAC is permitted to turn off the PLL in this state.
- P3: Shutdown mode, this is the lowest power consumption state. The link is virtually disconnected (CLd). Wake events are propagated via a sideband channel so common mode and LFPS detector are turned off. This state is suitable for deep sleep.
- P4: Transmitter and receiver are OFF with a total latency of up to 100 us delay. This state is suitable where higher exit latencies are tolerated (for example, storage devices).
- P0tx: Receiver only mode, the transmitter is OFF. Suitable for unidirectional traffic (for example, receiving tunneled DP traffic).

### 8.3.4 Power Management – SATA Mode

The power management signals allow the PHY to minimize power consumption. The PHY must meet all timing constraints provided in the SATA specification regarding clock recovery and link training for the various power states. The PHY must also meet all termination requirements for transmitters and receivers.

122

Reference Number: 643108, Revision: 7.1