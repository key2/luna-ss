# C Power Management

This appendix offers a system level overview of Enhanced SuperSpeed's power management features and capabilities. The following topics are also included:

- Examples of how end to end low power link state exit latencies are calculated
- A discussion of device-initiated link power management policies
- An example device implementation for Latency Tolerance Messaging
- System power considerations for SuperSpeed versus High Speed device interfaces

## C.1 SuperSpeed Power Management Overview

The SuperSpeed architecture has been defined with platform power efficiency as a primary objective. Some of the key power efficiency enhancements include:

- Elimination of continuous device polling
- Elimination of broadcast packet transmission through hubs
- Introduction of link power management states enabling aggressive power savings when idle
- Host and device initiated transition to low power states
- Device and individual Function level suspend capabilities enabling devices to remove power from all, or only those portions of their circuitry that are not in use

### C.1.1 Link Power Management

Link power management enables a link to be placed into a lower power state when the link partners are idle. The longer a pair of link partners remain idle, the deeper the power savings that can be achieved by progressing from U0 (link active) to U1 (link standby with fast exit), to U2 (link standby with slower exit), and finally to U3 (suspend).

After being configured by software, the U1 and U2 link states are entered and exited via hardware autonomous control. Hardware autonomous transitions for the U1 and U2 link states enable faster response times. This, in turn, translates to better power savings when entering a power saving state, and less impact on the operational state when exiting. The U3 link state however is entered only under software control, typically after a software inactivity timeout, and is exited either by software (host initiated exit) or hardware (remote wakeup). The U3 link state is directly coupled to the device's suspend state (refer to Section C.1.4).

C-1