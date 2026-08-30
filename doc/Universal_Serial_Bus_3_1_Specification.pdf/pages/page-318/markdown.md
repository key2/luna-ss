Universal Serial Bus 3.1 Specification, Revision 1.0

Where ROUNDDOWN (n) rounds n down, towards zero, to the nearest integer value.

This combination of setting the PTM Delta Counter and the PTM Bus Interval Counter defines the bus interval boundary time in the device.

The time synchronization mechanism within the device itself (e.g. to the PTM Local Time Source) is implementation-specific.

Figure 8-12 illustrates the tITUFP and tITDFP timing points of an ITP transaction.

### 8.4.8.6 PTM Bus Interval Boundary Host Calculation

A host shall maintain a PTM Delta Counter and a PTM Bus Interval Counter. The host shall transmit downstream ITPs using these current values for the ITP Isochronous Timestamp Bus Interval Counter(TxITP) and Delay(TxITP) fields, and set the Correction(TxITP) field to zero.

### 8.4.8.7 PTM Hub ITP Regeneration

A hub shall maintain an ITP Delay Counter that is incremented by the PTM Clock.

If an ITP is received by a PTM capable hub and the Delayed (DL) bit is not set, then the hub shall apply the following rules:

- Set the ITP Delay Counter to zero.

A PTM capable hub shall apply the following rules independently for each downstream port in U0:

- When an ITP is received, then the hub shall queue an ITP for transmission on this downstream facing port.

- When transmitting an ITP, a hub shall:

1. Copy the value of Bus Interval Boundary(RxITP) to the Bus Interval Boundary(TxITP) subfield of the Isochronous Timestamp field in the downstream ITP.

2. Calculate the value of Delta(TxITP) subfield using the following method:
Determine the Delta value at time the ITP shall be transmitted (tITPDFP) using the formula:

$$Delta_{(tITPDFP)} =$$

$$LDM \text{ Link Delay} + Delta_{(RxITP)} + (ITP \text{ Delay Counter} - wHubDelay) - Correction_{(RxITP)}$$

Where Delta(tITPDFP) is the Delta value at time tITPDFP.

If Delta(tITPDFP) is greater than or equal to zero and less than 7500, the hub shall set Delta(TxITP) equal to Delta(tITPDFP) and the Correction(TxITP) value to zero.

If Delta(tITPDFP) is greater than or equal to 7500, the hub shall set Delta(TxITP) equal to 7500.

If Delta(tITPDFP) is negative the hub shall set Delta(TxITP) to zero and calculate the Correction(TxITP) value using the following formula:

$$Correction_{(TxITP)} = -Delta_{(tITPDFP)}$$

3. Re-calculate the CRC-16 for the modified ITP.

8-24