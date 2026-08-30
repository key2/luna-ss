Protocol Layer

- Each individual packet in the burst shall have a data payload of maximum packet size. Only the last packet in a burst may be of a size smaller than the reported maximum packet size. If the last one is smaller, then the same rules for short packets apply to a short packet at the end of a burst (refer to Section 8.10.2).
- The burst transaction continues as long as the NumP field in the ACK TP is not set to zero and each packet has a data payload of maximum packet size.
- The NumP field can be incremented at any time by the host or a device sending the ACK TP as long as the device or host wants to continue receiving data. The only requirement is that the NumP field shall not have a value greater than the maximum burst supported by the device. However, for an ISOC IN endpoint, refer to Section 8.12.6, for additional requirements on how to change NumP for each burst.
- If a device or host sending an ACK TP decrements the NumP field, then it shall do so by no more than one. For example, if the previous ACK TP had a value of five in the NumP field, then the next ACK TP to acknowledge the next packet received shall have a value of no less than four in the NumP field. The only exceptions to this rule are:

1. If the device can receive the data but cannot accept any more data, then it shall send an ACK TP with the NumP field set to zero.
2. The host shall send an ACK TP with the NumP field set to zero in response to a device sending a DP with the EOB field set or that is a short packet (see Section 8.10.2). However, if the host receives a short packet with EOB = 0 and the host has another transfer to initiate with the same endpoint, then the host may instead send an ACK TP with the NumP field set to a non-zero value.
3. The host may send an ACK TP with the rty bit set to one and the NumP field set to any value less than the maximum burst that the endpoint is capable of, including zero, in response to a device sending a DP with a DPP error (See Section 8.11.2).

### 8.10.2.2 SuperSpeedPlus Burst Transactions

The SuperSpeedPlus architecture has the following additional requirements for burst transactions.

The SuperSpeedPlus architecture defines signaling rates faster than SuperSpeed. In order to maximize performance of the bus, when operating at Gen 2 speed, Enhanced SuperSpeed devices and hosts shall be limited to tGen2MaxBurstInterval for the time between DPs being bursted from a device endpoint to the host or from the host to a device endpoint.

Since the SuperSpeedPlus architecture allows multiple INs, a single SuperSpeedPlus device can be ready to burst multiple DPs from multiple endpoints whenever the link is available. A SuperSpeedPlus device operating at Gen 2 speed shall be limited to tGen2MaxDeviceMultiPacketInterval for the time between DPs being concurrently bursted from different device endpoints to the host.

In the SuperSpeedPlus architecture, DPs for different endpoints or devices can be buffered and reordered with respect to each other as they pass through SuperSpeedPlus hubs, due to other traffic that may be contending for use of path. When a SuperSpeedPlus hub has several DPs buffered for a link operating at Gen 2 speed, it shall transmit those DPs with a maximum of tGen2MaxHubMultiPacketInterval for the time between DPs, whether those DPs are for the same or different devices or endpoints.

8-53