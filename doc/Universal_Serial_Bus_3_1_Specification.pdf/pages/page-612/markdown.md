Universal Serial Bus 3.1 Specification, Revision 1.0

number of hubs between the host and the device, device processing time, packet propagation delays, etc.

The Maximum Exit Latency (tMEL) is the sum of parameters tMEL1, tMEL2, tMEL3, and tMEL4.

### C.1.5.2.1 Maximum Exit Latency t1 (tMEL1)

The tMEL1 delay is the time to transition all links in the path to the device to U0 when the transition is initiated by the host. The method for calculating MEL t1 delay is described in Sections C.2.1.1 and C.2.2.1.

### C.1.5.2.2 Maximum Exit Latency t2 (tMEL2)

tMEL2 is the sum of the tHubDelay values for each hub in the path, and tTPTransmissionDelay across each link in the path is calculated as:

$$\text{tMEL2} = (\text{sum of wHubDelay values}) + (\text{tTPTransmissionDelay} * (\text{number of hubs} + 1)).$$

Where, a wHubDelay value is provided by the SuperSpeed Hub Descriptor of each hub in the path, respectively, and tTPTransmissionDelay is defined in Table 8-33.

### C.1.5.2.3 Maximum Exit Latency t3 (tMEL3)

The tMEL3 delay is the time for the device to receive the PING and generate the PING_RESPONSE, which is defined by tPingResponse. Refer to Table 8-33.

### C.1.5.2.4 Maximum Exit Latency t4 (tMEL4)

The tMEL4 delay is the time for the PING_RESPONSE to traverse the interconnect hierarchy from the device to the host. Since wHubDelay defines the downstream and upstream delay through a hub, the propagation delay of a PING_RESPONSE upstream is identical to that of a PING downstream delay (tMEL2), with one exception. In the upstream path a TP may be queued behind a Max Packet Size DP, so an additional 2.1 μs of delay is included to comprehend the “congestion jitter”. tMEL4 is calculated as:

$$\text{tMEL4} = \text{tMEL2} + 2.1 \text{ μs}.$$

C-14