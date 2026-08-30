Universal Serial Bus 3.1 Specification, Revision 1.0

In preparation for a transition from U0 to U2, a device in LT-active should perform the following actions:

1. The device transitions to LT-idle.
2. The device sends an LTM with a BELT value of at least tBELTdefault.
3. The device initiates a transition to U2 from U0.

In preparation for a transition from U1 to U2, a device in LT-active should perform the following actions:

1. The device transitions its link to U0 prior to U2 entry.
2. The device transitions to LT-idle.
3. The device sends an LTM with a BELT value of at least tBELTdefault.
4. The device initiates a transition to U2 from U0.

In the latter case, since the device must transition its link to U0 prior to U2 entry, the device must detect the U2 inactivity timer expiration enough in advance to avoid the possibility that its link partner will have already transitioned from U1 directly to U2. For example, the device may initiate a transition to U0 1 μs before the U2 inactivity timer expires.

### C.4.2 Other Considerations

The following are additional considerations associated with device support of LTM:

- The BELT represents a latency tolerance for an entire peripheral device. The BELT value must be aggregated across all endpoints within the device, including all functions within a composite device. The smallest BELT value across all endpoints should be selected. For LTM purposes, isochronous endpoints are ignored when determining the BELT value.
- If LTM is supported by a device, LTM should be disabled prior to placing the device into suspend (refer to the PORT_LINK_STATE feature selector in Chapter 10). Devices send an updated LTM when LTM is enabled, or immediately before LTM is disabled, as defined in Chapter 8. Disabling LTM in this way ensures that a suspended device does not keep the system in a high state of readiness, wasting power.

### C.5 SuperSpeed vs. High Speed Power Management Considerations

Some devices may operate well with a High Speed (480 Mbps) interface, but can substantially reduce system power consumption if implemented with a SuperSpeed interface. In addition to device power consumption, system power consumption should be considered when selecting the interface for a new device design.

When a device is actively transferring data, system components are also transferring that data. For some systems, the power consumption of system components is much larger than a USB device's contribution to the system's power consumption.

Under typical circumstances, the faster the data transfer completes, the faster system components can return to a low power state. Transferring data faster can save power, on average, over time. Examples of system components include a Host Controller, a DRAM controller, DRAM components, a microprocessor with a cache that needs to snoop DRAM accesses, etc.

C-26