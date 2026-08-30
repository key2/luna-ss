Revision 1.1
June 2022

- 227 -

Universal Serial Bus 3.2
Specification

1. Copy the value of Bus Interval Boundary(RxITP) to the Bus Interval Boundary(TxITP) subfield of the Isochronous Timestamp field in the downstream ITP.
2. Calculate the value of Delta(TxITP) subfield using the following method: Determine the Delta value at time the ITP shall be transmitted (tITPDFP) using the formula:

$$Delta_{(tITPDFP)} =$$

$$\begin{array}{c} LDM \text{ Link Delay} + Delta_{(RxITP)} + \\ (ITP \text{ Delay Counter} - wHubDelay) - Correction_{(RxITP)} \end{array}$$

Where $Delta_{(tITPDFP)}$ is the $Delta$ value at time tITPDFP.

If $Delta_{(tITPDFP)}$ is greater than or equal to zero and less than 7500, the hub shall set $Delta(TxITP)$ equal to $Delta(tITPDFP)$ and the $Correction(TxITP)$ value to zero.

If $Delta(tITPDFP)$ is greater than or equal to 7500, the hub shall set $Delta(TxITP)$ equal to 7500.

If $Delta(tITPDFP)$ is negative the hub shall set $Delta(TxITP)$ to zero and calculate the $Correction(TxITP)$ value using the following formula:

$$Correction(TxITP) = - Delta_{(tITPDFP)}$$

3. Re-calculate the CRC-16 for the modified ITP.

If an ITP is received by a PTM capable hub and the Delayed (DL) bit is set, then the hub shall apply the following rules:

- Forward the received ITP without modification.

The Isochronous Timestamp values used in the ITP being transmitted shall be the values present at the time of transmission; e.g., if other packets are queued for transmission at the time the ITP is queued, the values used shall not be the values present at the time of queuing, but adjusted for the actual time of transmission (tITPDFP). Refer to Section 8.4.8.6 for more information.

### 8.4.8.8 Performance

Figure 8-16 illustrates the various components of a LDM Exchange path that contribute to the overall performance of the LDM mechanism. The Requester to Responder and Responder to Requester paths apply to LDM TS Request and TS Response LMPs, respectively. The Requester Rx path applies to ITPs received by an upstream facing port and the Responder Tx path applies to ITPs transmitted by a downstream facing port.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.