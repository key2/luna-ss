Protocol Layer

If LDM Valid is zero, then the LDM Link Delay shall be calculated using the following formula:

$$LDM \text{ Link Delay} = TP \text{ Transmission Time} - tTP \text{ Transmission Delay}$$

If LDM Valid is one, then the received LDM TS Response LMP of a Timestamp Exchange provides the Requester with the Response Delay field which defines the delay between when the LDM Request was received and the LDM Response was transmitted by the Responder ((t3 - t2).

When the LDM TS Response LMP of a Timestamp Exchange is received, a Requester has accumulated the timestamps t1 and t4 that can be combined with the Response Delay (t3 - t2 timestamp) received from the Responder to calculate the value of LDM Link Delay using the following formula:

$$LDM \text{ Link Delay} = \frac{(t4 - t1) - (\text{Response Delay})}{2} + TP \text{ Transmission Time} - tTP \text{ Transmission Delay}$$

The values t1, t4, and Response Delay indicate the timestamps captured during the LDM Exchanges as illustrated in Figure 8-11. The default TP transmission time (tTPTransmissionDelay) is corrected by the actual TP Transmission Time of the link. After the LDM Link Delay calculation is complete, the values of timestamps t1 and t4 in the Requester LDM Context will be overwritten with the values of the next Timestamp Exchange.

### 8.4.8.5 PTM Bus Interval Boundary Device Calculation

The bus interval boundary is calculated by a device when an ITP is received.

An ITP provides a device with three values:

- The Bus Interval Counter(RxITP) subfield contains the current Frame Number.
- The Delta(RxITP) subfield contains the delay from the start of the currently received ITP to the previous bus interval boundary.
- The Correction(RxITP) field contains any negative delay that the ITP accumulated as it passed through hubs.

If Delta(RxITP) is greater than or equal to 7500, the device shall ignore the ITP.

If Delta(RxITP) is less than 7500, the device shall apply Delta(RxITP) and Correction(RxITP) values and the LDM Link Delay (determined from preceding TS Exchanges) to set the value of the PTM Delta Counter at the time an ITP is received (tITUFP) using the following formula:

$$PTM \text{ Delta Counter}_{(\text{tITUFP})} =$$

$$\text{MODULUS}(\text{ISOCH\_DELAY} + \text{LDM Link Delay} + \text{Delta}_{(\text{RxITP})} - \text{Correction}_{(\text{RxITP})}, 7500)$$

Where MODULUS(number, divisor) returns the integer remainder after number is divided by divisor and ISOCH_DELAY is the value written to the device by a SET_ISOCH_DELAY request.

At the same time, a device shall use the values of Bus Interval Counter(RxITP) and Delta(RxITP) subfields received in the ITP to set the value of the PTM Bus Interval Counter at the time an ITP is received (tITUFP) using the following formula:

$$PTM \text{ Bus Interval Counter}_{(\text{tITUFP})} =$$

$$\text{Bus Interval Counter}_{(\text{RxITP})} + \text{ROUNDDOWN}((\text{LDM Link Delay} + \text{Delta}_{(\text{RxITP})}) / 7500))$$

8-23