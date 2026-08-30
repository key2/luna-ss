Revision 1.1
June 2022

- 226 -

Universal Serial Bus 3.2
Specification

- The Delta(RxITP) subfield contains the delay from the start of the currently received ITP to the previous bus interval boundary.
- The Correction(RxITP) field contains any negative delay that the ITP accumulated as it passed through hubs.

If Delta(RxITP) is greater than or equal to 7500, the device shall ignore the ITP.

If Delta(RxITP) is less than 7500, the device shall apply Delta(RxITP) and Correction(RxITP) values and the LDM Link Delay (determined from preceding TS Exchanges) to set the value of the PTM Delta Counter at the time an ITP is received (tITUFP) using the following formula:

$$PTM\ Delta\ Counter_{(tITUFP)} =$$

$$MODULUS(ISOCH\_DELAY + LDM\ Link\ Delay + Delta(RxITP) - Correction(RxITP), 7500)$$

Where MODULUS(number, divisor) returns the integer remainder after number is divided by divisor and ISOCH_DELAY is the value written to the device by a SET_ISOCH_DELAY request.

At the same time, a device shall use the values of Bus Interval Counter(RxITP) and Delta(RxITP) subfields received in the ITP to set the value of the PTM Bus Interval Counter at the time an ITP is received (tITUFP) using the following formula:

$$PTM\ Bus\ Interval\ Counter_{(tITUFP)} =$$

$$Bus\ Interval\ Counter(RxITP) + ROUNDDOWN((LDM\ Link\ Delay + Delta(RxITP)) / 7500))$$

Where ROUNDDOWN (n) rounds n down, towards zero, to the nearest integer value.

This combination of setting the PTM Delta Counter and the PTM Bus Interval Counter defines the bus interval boundary time in the device.

The time synchronization mechanism within the device itself (e.g. to the PTM Local Time Source) is implementation-specific.

Figure 8-12 illustrates the tITUFP and tITDFP timing points of an ITP transaction.

#### 8.4.8.6 PTM Bus Interval Boundary Host Calculation

A host shall maintain a PTM Delta Counter and a PTM Bus Interval Counter. The host shall transmit downstream ITPs using these current values for the ITP Isochronous Timestamp Bus Interval Counter(TxITP) and Delay(TxITP) fields, and set the Correction(TxITP) field to zero.

#### 8.4.8.7 PTM Hub ITP Regeneration

A hub shall maintain an ITP Delay Counter that is incremented by the PTM Clock.

If an ITP is received by a PTM capable hub and the Delayed (DL) bit is not set, then the hub shall apply the following rules:

- Set the ITP Delay Counter to zero.

A PTM capable hub shall apply the following rules independently for each downstream port in U0:

- When an ITP is received, then the hub shall queue an ITP for transmission on this downstream facing port.
- When transmitting an ITP, a hub shall:

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.