Universal Serial Bus 3.1 Specification, Revision 1.0

t3 - t2 is less than tLDMResponseDelay, the Responder shall form a LDM TS Response LMP by initializing the Response Delay field with the value t3 - t2, transmit the LDM TS Response LMP to the Requester, and transition to the Timestamp Request state. If the value t3 - t2 is equal to or greater than tLDMResponseDelay, then the Responder shall transition to the Timestamp Request state.

A typical Trigger Event for the Responder Timestamp Response state would be the next opportunity to schedule a LDM TS Response LMP on its downstream link after a LDM TS Request LMP has been received.

Note: The Timestamp t3 shall be adjusted for the TS Delay. Refer to Section 8.4.8.6 for more information.

Note: A Responder shall set the LCW Delayed (DL) flag and re-calculate CRC-5 if a LDM TS Response LMP is delayed if its adjusted Response Delay value exceeds tLDMRequestTimeout. Refer to Section 8.4.8.6 for more information.

### 8.4.8.4 LDM Link Delay

LDM defines the set of PTM capabilities which support the measurement of the LDM Link Delay.

LDM Link Delay identifies the delay between the first symbol of a packet being transmitted on a Responder's downstream facing port and the first symbol of the same packet being received on the Requester's upstream facing port. In a hub or device the LDM Link Delay is derived from Timestamp Exchanges with its upstream Responder.

A Requester may execute multiple Timestamp Exchanges to refine its LDM Link Delay value through averaging.

Note: Field, or subfield names that reference a received ITP shall use the subscript (RxITP) and field, or subfield names that reference a transmitted ITP shall use the subscript (TxITP).

### 8.4.8.4.1 Calculation

The LDM Link Delay is calculated by the Requester when a Timestamp Exchange completes. The LDM Link Delay is the measured link delay adjusted to ensure compatibility with non-PTM aware software.

The TP Transmission Time is the time it takes to transmit a TP including framing and encoding at UI nominal.

Where UI nominal is defined as:

$$UI \text{ nominal} = \frac{(UI \text{ max}) + (UI \text{ min})}{2}$$

Refer to Section 6.7 for the definition of UI min and UI max.

The TP Transmission Time for a link operating at Gen 1 speed is 200 UI * UI nominal (i.e. 40 ns @ 5 Gbps).

It takes either 164 or 168 UI, depending on block alignment, to transfer a TP over a link operating at Gen 2 speed. The statistical average is 165 UI. Therefore, the TP Transmission Time for a link operating at Gen 2 speed is 165 UI * UI nominal (i.e. 16.5 ns @ 10 Gbps).

8-22