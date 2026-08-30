Power Management

plus some guard band. This assumes the device will not allow its link to enter U2 prior to changing its state to LT-idle. If the device will allow its link to enter U2 when in LT-active, then the total latency the device must be able to tolerate is 125 μs plus the worst case value for U2SEL.

For system implementations where U1SEL is less than its worst case value, the device reports a BELT value larger than 125 μs.

### C.4.1.3 Transitioning Between LT-States

When a device transitions between LT-states, the device sends an LTM Transaction Packet (TP) with an updated BELT. The device should send all BELT updates as soon as possible after a change in LT-state.

### C.4.1.3.1 Transitioning From LT-idle to LT-active

Devices transition from LT-idle to LT-active when the device determines that a bulk or interrupt data transfer needs to occur. Some examples are given below:

- The host initiates a bulk OUT transfer with the Packets Pending flag asserted to a flash drive device. As a result of receiving this OUT request, the device transitions to LT-active and sends an updated BELT to the host.
- The host initiates a bulk IN transfer with the Packets Pending flag asserted to a hard disk drive device with is spindle currently spun down and the requested data not in a cache on the hard disk drive. As a result of receiving this IN request, the device determines that a bulk data transfer has been initiated by the host. However, the device will service the IN request after its spindle spins up, which may take substantially longer than the last reported BELT. The device may delay transitioning to LT-active. When the device determines that the spindle will complete its spin up within the last reported BELT, the device transitions to LT-active and sends an updated BELT to the host.
- A Network Interface Controller device begins receiving data on its network interface that requires a bulk IN data transfer with the host. As a result of receiving data on its network interface, the device transitions to LT-active, begins to transition its link to U0 (if not already in U0), and sends both an ERDY and an updated BELT to the host.
- A multi-touch Human Interface Device is set up with an interrupt endpoint. When human input is detected the device transitions to LT-active, begins transitioning its link to U0 (if not already in U0), and sends both an ERDY and an updated BELT to the host.

In some cases, a transition from LT-idle to LT-active is not appropriate even though the device needs to transmit to the host. For example:

- The host sends a GetStatus request to a device. Since it is a control transfer and not a bulk or an interrupt transfer, the device remains in the LT-idle state.

When the device transitions from LT-idle to LT-active, the device sends an LTM TP with a BELT of at least tBELTmin.

### C.4.1.3.2 Transitioning From LT-active to LT-idle

When a device determines that it is idle, it transitions from LT-active to LT-idle. The method used in this example for device idle detection is based on U2 entry. When the device is in LT-active, the device transitions to LT-idle just prior to when its link will enter U2.

C-25