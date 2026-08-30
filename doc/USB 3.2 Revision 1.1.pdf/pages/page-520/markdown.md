Revision 1.1
June 2022

- 489 -

Universal Serial Bus 3.2
Specification

# E Repeaters

# E.1 Overview

The introduction of the Gen 2 data rate that doubles the Gen 1 data rate has led to increased channel loss which increases the need for repeaters. This includes the use of a repeater on some platforms in order to compensate for this channel loss and preserve the system routing requirement in terms of signal integrity. Likewise, there is a growing need for longer cables that require repeaters in the cable itself to support the extended lengths. As a result, new connectivity models emerge in USB 3.1 that include multiple repeaters between the host and device.

While the presence of repeaters effectively address the signal integrity needs of a system, they also introduce propagation delay that needs to be accounted for in both Gen 1 and Gen 2 data rates. In this Appendix, the link delay is defined for the pertinent system elements including the host, device, repeaters, and active cables. In addition, the details of a re-timer, a specific type of repeater architecture, are provided.

# E.1.1 Term Definitions

In this document, the following definitions apply:

Repeater refers to any active component that acts on a signal in order to increase the physical lengths and/or interconnect loss over which the signal can be transmitted successfully. The category of repeaters includes both re-timers and re-drivers, which are defined below.

Re-timer refers to a component that contains a clock-data recovery (CDR) circuit that "retimes" the signal. The re-timer latches the signal into a synchronous memory element before re-transmitting it. It is used to extend the physical length of the system without accumulating high frequency jitter by creating separate clock domains on either side of the re-timer. Furthermore, a re-timer can be implemented based on one of the following architectures.

- SRIS (Separate Reference clock Independent SSC) re-timer refers to a re-timer implementation that has it's transmit clock derived from a local reference clock and is independent of the recovered clock at its receiver.
- Bit-level re-timer refers to a re-timer implementation that has it's transmit clock derived from the recovered clock at its receiver, except during part of link training.

A single-lane re-timer refers to a re-timer implementation capable of both Gen 1x1 and Gen 2x1 operation.

A dual-lane re-timer refers to a re-timer implementation capable of both Gen 1x2 and Gen 2x2 operation.

Both SRIS re-timer and bit-level re-timer are implemented with protocol awareness (refer to Section E.2.2.2 for details). In this Appendix, unless otherwise specified, a re-timer refers to either a SRIS re-timer or a bit-level re-timer.

Re-driver refers to an analog component that operates on the signal without re-timing it. This may include equalization, amplification, and transmitter. The re-driver does not include a CDR, and as a result, it does not cancel completely the jitter from the input, but only to compensate partially for the channel loss through equalization and amplification. Note that a re-driver in Gen 1 operation may employ a limiting re-driver that does not maintain the linearity of its input signal. However, a re-driver in Gen 2 operation is required to be a linear re-driver to preserve the linearity of its input signal. In this Appendix, a

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.