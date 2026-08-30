Revision 1.1
June 2022

- 225 -

Universal Serial Bus 3.2
Specification

Note: Field, or subfield names that reference a received ITP shall use the subscript (RxITP) and field, or subfield names that reference a transmitted ITP shall use the subscript (TxITP).

### 8.4.8.4.1 Calculation

The LDM Link Delay is calculated by the Requester when a Timestamp Exchange completes. The LDM Link Delay is the measured link delay adjusted to ensure compatibility with non-PTM aware software.

The LMP Transmission Time is the time it takes to transmit a TP including framing and encoding at UI nominal.

Where UI nominal is defined as:

$$UI \text{ nominal} = \frac{(UI \text{ max}) + (UI \text{ min})}{2}$$

Refer to Section 6.7 for the definition of UI min and UI max.

The LMP Transmission Time for a link operating at Gen 1x1 speed is 200 UI * UI nominal (i.e. 40 ns @ 5 Gbps). The LMP Transmission Time for a Link operating at Gen 1x2 is 20 ns.

It takes either 164 or 168 UI, depending on block alignment, to transfer a TP over a link operating at Gen 2x1 speed. The statistical average is 165 UI. Therefore, the LMP Transmission Time for a link operating at Gen 2x1 speed is 165 UI * UI nominal (i.e. 16.5 ns @ 10 Gbps). The LMP Transmission Time for a Link operating at Gen 2x2 is 8.25 ns.

If LDM Valid is zero, then the LDM Link Delay shall be calculated using the following formula:

$$LDM \text{ Link Delay} = LMP \text{ Transmission Time} - tLMP \text{ Transmission Delay}$$

If LDM Valid is one, then the received LDM TS Response LMP of a Timestamp Exchange provides the Requester with the Response Delay field which defines the delay between when the LDM Request was received and the LDM Response was transmitted by the Responder (t3 - t2).

When the LDM TS Response LMP of a Timestamp Exchange is received, a Requester has accumulated the timestamps t1 and t4 that can be combined with the Response Delay (t3 - t2 timestamp) received from the Responder to calculate the value of LDM Link Delay using the following formula:

$$LDM \text{ Link Delay} = \frac{(t4 - t1) - (\text{Response Delay})}{2} + LMP \text{ Transmission Time} - tLMP \text{ Transmission Delay}$$

The values t1, t4, and Response Delay indicate the timestamps captured during the LDM Exchanges as illustrated in Figure 8-11. The default LMP transmission time (tLMPTransmissionDelay) is corrected by the actual LMP Transmission Time of the link. After the LDM Link Delay calculation is complete, the values of timestamps t1 and t4 in the Requester LDM Context will be overwritten with the values of the next Timestamp Exchange.

### 8.4.8.5 PTM Bus Interval Boundary Device Calculation

The bus interval boundary is calculated by a device when an ITP is received.

An ITP provides a device with three values:

- The Bus Interval Counter(RxITP) subfield contains the current Frame Number.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.