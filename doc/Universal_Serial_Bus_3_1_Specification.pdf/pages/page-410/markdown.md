Universal Serial Bus 3.1 Specification, Revision 1.0

### 8.12.6.2 Host Flexibility in Performing SuperSpeed Isochronous Transactions

A host targeting an endpoint on a SuperSpeed bus instance shall adhere to the requirements in this section.

The host is allowed some flexibility in performing isochronous service during a service interval. The host may transfer all the DPs to or from an endpoint as a single isochronous burst transaction or it may split the transfer into smaller bursts of two, four, or eight DPs followed by a final isochronous burst with the remaining DPs for that service interval. The host shall not perform isochronous transactions in any other way. For isochronous endpoints that have a multiplier value greater than one, these rules apply to the burst transactions associated with each multiplier value separately. A device shall support all possible host burst transactions allowed by these rules. For example, if an isochronous IN endpoint requests a maximum number of packets in a burst of 11 and the host has 11 packets to receive from the endpoint during a service interval there are four possible ways the host could perform the transaction:

- Request a single burst of 11 packets
- Request a burst of eight followed by a burst of three
- Request two bursts of four followed by a burst of three
- Request five bursts of two followed by a burst of one
- Request 11 bursts of one.

Taking the above example a step further, if the isochronous IN endpoint requests a maximum number of packets in a burst of 11 and a Mult of 2 (in essence requesting three bursts of 11) and the host has buffer space to receive 33 packets from the endpoint during a service interval, then the host can use any combination of the above mentioned options to transfer the three sets of 11 packets to the endpoint.

### 8.12.6.3 SuperSpeedPlus Isochronous Transactions

#### 8.12.6.3.1 Pipelined Isochronous IN Transactions

SuperSpeedPlus hosts may perform Isochronous transactions to an Enhanced SuperSpeed Isochronous endpoint following the rules outlined in Section 8.12.6.1. However, when performing IN transactions to SuperSpeedPlus endpoints, a SuperSpeedPlus host is allowed to send multiple IN ACK TPs requesting more data from the endpoint before the endpoint has returned all the data previously requested. The host shall not request more outstanding DPs than the max burst size reported in the endpoints' descriptors.

If a SuperSpeedPlus endpoint reports a Max Burst Size of 'M' in its descriptors then a SuperSpeedPlus host can send the following sequence of IN ACK TPs to the device without waiting for the device to return all the DPs asked for in the initial IN ACK TP:

8-116