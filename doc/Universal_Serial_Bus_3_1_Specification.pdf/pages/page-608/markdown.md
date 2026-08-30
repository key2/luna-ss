Universal Serial Bus 3.1 Specification, Revision 1.0

### C.1.4.1 Function Suspend

A function may be placed into function suspend independent of other functions using the FUNCTION_SUSPEND feature. The FUNCTION_SUSPEND feature is also used to enable function remote wakeup (refer to Chapter 9 for details).

If a composite device has at least one of its functions in suspend while other functions remain active, i.e., the device's upstream port is not in U3, a mechanism is needed for a suspended function to signal a remote wakeup. This is done with the Function Wake device notification packet (refer to Chapter 8 for details).

### C.1.4.2 Device Suspend

Device suspend is a device-wide state entered and exited intrinsically as a result of a device's upstream port entering and exiting the U3 state. A device may be transitioned into device suspend regardless of the function suspend state of any function within the device.

Devices may implement a switched power rail and remove power from large portions of the device while in suspend. Some device state information must be retained in a persistent state during suspend (refer to Chapter 9 for details).

### C.1.4.3 Host Initiated Suspend

#### Suspending a Device

The host transitions a device into the suspend state according to the following sequence:

- Enable remote wakeup, if needed
- A SetPortFeature(PORT_LINK_STATE, U3) request is issued to the downstream port of which the targeted device is its link partner.
- The downstream port initiates U3 entry by sending an LGO_U3 link command.
- The device sends an LAU link command (acceptance is non-negotiable).
- The downstream port sends an LPMA link command.
- Both link partners transition their transmitters to electrical idle and enter the U3 state (refer to Chapter 7 for details).

#### Suspending the USB Link Hierarchy

A link hierarchy of devices and hubs is placed into suspend on a device by device basis under host software control. First, all peripheral devices in the hierarchy are placed into suspend. Then the hubs connected to the peripheral devices are placed into suspend. This is repeated all the way up the hierarchy until reaching the root ports of the USB hierarchy.

Note that by using the same technique a select subset of a given USB link hierarchy could be suspended rather then the whole of it if so desired.

C-10