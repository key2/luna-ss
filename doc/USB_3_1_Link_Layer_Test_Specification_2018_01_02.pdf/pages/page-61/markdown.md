Chapter 4: Timing Definitions

1/17/2018

## 4 Timing Definitions

The USB 3.1 Specification defines the timers used in the Link Layer. To accurately test timer implementations, there are several considerations beyond the simple timer definition that factor into this document's timing scheme. Section 7.5 of the USB 3.1 Specification defines the link layer timers to have an implementation tolerance of +50%. Chapter 6 details an SSC Tolerance of -5300/+300ppm, the lower limit of which could add 0.5% time to any interval. Consideration for Physical Layer and Link Layer processing time (Tx and Rx latency time) is also applied.

The following expression is used for determining each timer's high-end value used in this specification:

$$\text{Spec Defined Timer value} \times \text{Additional50pctTolerance} \times \text{SSCFactor} + \text{tLinkTurnAround}$$

Spec Defined Timer value = the timer value defined in USB 3.1 specification.

Additional50pctTolerance = +50% tolerance defined in the Section 7.5 of the USB 3.1 specification.

SSCFactor = delay induced by SSC influenced clock with a maximum SSC of 5000ppm applied, equating to +0.5%.

tLinkTurnAround = tDHPResponse - tDPacket.

This is understood to be the maximum delay induced by the PHY and Link layers when a link event occurs, until the respective action is made, when there is no other packet processing occurring on the port. This is measured from the time a packet is received, until the time a response is generated on the transmit side.

For a Gen 1 port:

tLinkTurnaround = tDHPResponse - tDPacket = 2540ns - 2140ns = 400ns

For a Gen 2 port:

tLinkTurnaround = tDHPResponse - tDPacket = 1610ns - 910ns = 700ns

Note: Since captive re-timer delay is included in tDHPResponse and not factored out for tLinkTurnaround, a PUT that does not contain a captive re-timer can use the extra time for its Tx and Rx Data Paths.

Using their respective numerical values, the expression is presented again below:

$$\text{Spec Defined Timer value} \times 1.5 \times 1.005 + \text{tLinkTurnaround}$$

The expression above is applicable for Link Layer timers.

$$\text{Spec Defined Timer value} \times 1.005 + \text{tLinkTurnaround}$$

The expression above is applicable for PHY and protocol layer timers.

The following table lists the timers used in the Link Layer compliance tests and the window of compliant durations between the initial event that started the timer, and the expected response when the timer expires.

PORT_U2_TIMEOUT is not listed in the table because its value is programmable using the U2 Inactivity Timeout LMP. A calculation is needed as per the value programmed.

tPollingLFPSEstablishedTimeout was created from USB 3.1 Specification section 7.5.4.3.1: A Port shall establish its LFPS operating condition within 80us.

tRecoveryTimeout was created as a replacement for tLinkTurnaround when an error occurs that should result in a quick transition to Recovery. This mechanism may be implemented separately from tLinkTurnaround logic. Both Gen 1 and Gen 2 PUTs are given 1us to enter recovery for TDs 7.13, 7.14, 7.15, and 7.30.

[tbl-54.md](tbl-54.md)

53

USB 3.1 Link Layer Test Specification