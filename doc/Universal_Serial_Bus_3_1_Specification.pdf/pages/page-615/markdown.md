Power Management

# U1 → U0 Transition Latency

The host initiates the transition by transmitting LFPS. At this point, both link partners' transitions from U1 → to U0 are executed in parallel.

The exit latency is characterized by the largest of the two device exit latencies: Dev1:U1DEL and RP1:U1DEL

# U2 → U0 Transition Latency

In this example it is assumed that at least one of the link partners (e.g., the RP1) is enabled for U2. The host initiates the transition by transmitting LFPS. At this point both link partners execute transition from U2 → to U0 in parallel.

The exit latency is characterized by the largest of the two device exit latencies: Dev1:U2DEL and RP1:U2DEL

# C.2.1.2 Device Initiated Transition

These transition latencies are the same as for the host initiated cases.

- U1 End to End Exit Latency is the larger of Dev1:U1DEL and RP1:U1DEL
- U2 End to End Exit Latency is the larger of Dev1:U2DEL and RP1:U2DEL

C-17