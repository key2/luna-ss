Power Management

endpoint. When there are no more packets pending for all non-Stream endpoints on a device, the device may place its link in a low power state immediately.

For Stream endpoints, the Packet Pending flag is an indication of whether the host controller has any additional packets to transfer on the schedule associated with a given Stream. When there are no more packets pending for any Streams and for all endpoints on a device, the device may place its link in a low power state immediately.

### C.1.3.2 Support for Isochronous Transfers

If a link is in a low power state when an isochronous transfer is scheduled, the latency to transition to U0 from source to destination could potentially delay the transfer beyond its subscribed isochronous service interval.

To ensure that isochronous service contract guarantees are satisfied, a SuperSpeed mechanism (Ping) has been defined to bring all paths between the host and an isochronous endpoint to U0 as a routine step in servicing isochronous endpoints.

The host controller, with sufficient information to know how long any given path might take to become fully active, factors this link path exit latency into its isochronous service scheduler and uses the Ping protocol to ensure that the links are brought to a fully active state in time to meet the isochronous service contract.

The ping process consists of the following:

- The host sends a PING packet to a device.
- Hubs route the PING packet toward the targeted device.
- The device responds to the PING packet by sending a PING_RESPONSE packet to the host.
- The device keeps its link in U0 until it receives a subsequent packet from the host.

After sending a PING packet to one device and prior to receiving a PING_RESPONSE packet, the host may transfer data with other devices. Much like the Packet Deferring mechanism, the Ping mechanism enables efficient bus utilization while at the same time supporting significant power savings.

### C.1.3.3 Support for Interrupt Transfers

If any links between the host and a scheduled interrupt endpoint are in a low power state, the latency to transition the end to end pathway to U0 could potentially delay the transfer beyond the subscribed interrupt service interval. A host controller, possessing knowledge of link path exit latency between itself and any given device within the link hierarchy, is able to schedule interrupt transfers far enough in advance to compensate for these latencies.

### C.1.4 Device Power Management

Device power management is directed primarily under software control, with various hardware mechanisms to support it. Device power management consists of some function level mechanisms plus some device and hub mechanisms.

C-9