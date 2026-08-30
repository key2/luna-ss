Universal Serial Bus 3.1 Specification, Revision 1.0

### C.1.5 Platform Power Management Support

The Latency Tolerance Message (LTM) feature allows a platform to make dynamic tradeoffs between power and performance. It enables this, in cooperation with devices, without imposing additional cost.

The LTM protocol enables USB devices to inform the host how long they can tolerate lack of service before experiencing unintended side effects. Each device provides this information in the form of a Best Effort Latency Tolerance (BELT) value. A given device's BELT value is derived considering all configured endpoints, typically conforming to the endpoint with the lowest latency tolerance.

LTM provides the ability for a device to dynamically change its BELT value to more accurately reflect, for example, long periods of anticipated idle time. The platform can potentially take advantage of this insight and, along with other system-related information, conserve more energy at the system level without running the risk of unintended side effects.

### C.1.5.1 System Exit Latency and BELT

A device's reported BELT value has to comprehend not only its own intrinsic design characteristics, such as its internal buffering, but also factor in other associated end to end latencies between itself and the host. These would include other latencies associated with the time required to awaken sleeping links, the number of hubs between the device and the host, host processing time, packet propagation delays, etc. The system provides the device with additional system latency information, through the SET_SEL request, such that the device's intrinsic BELT value can be adjusted downward to account for these other factors. Refer to Chapter 8 for detailed LTM specification and to Chapter 9 for specification details regarding the SET_SEL request.

Device implementation determines the total latency that a device can tolerate. The primary factors are the amount of data that the device is required to produce or consume, and the amount of buffering on the device. The total device latency tolerance must be allocated among different system components.

Figure C-2 illustrates the total latency a device may experience within the context of LTM. The latency is the sum of parameters t1, t2, t3, and t4:

- t1: the time to transition all links in the path to the host to U0 when the transition is initiated by the device
- t2: the time for the ERDY to traverse the interconnect hierarchy from the device to the host
- t3: the time for the host to consume the ERDY and transmit a response to that request
- t4: the time for the response to traverse the interconnect hierarchy from the host to the device

C-12