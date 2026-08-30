Universal Serial Bus 3.1 Specification, Revision 1.0

### 10.18.2.6 USDPORT.Disabled

A port transitions to this state

- From the USDPORT.Powered on state when Far-end Receiver Terminations are not detected as per the rules described below:

If USDPORT.Powered on was entered from any state except USDPORT.Disabled then this transition shall take place if Far-end Receiver Terminations (RRX-DC) are not detected after eight successive Rx.Detect.Quiet to Rx.Detect.Active transitions.

If USDPORT.Powered on was entered from the USDPORT.Disabled state, then this transition shall take place the first time that Far-end Receiver Terminations are not detected in the Rx.Detect.Active substate.

- From the USDPort.Training state if a timeout occurs on any Polling substate (see Figure 7-18).
- From the USDPort.Connected state, if the Port Configuration process times out (see Section 8.4.6).

A count (Disabled_count) shall be maintained of each entry into the USDPort.Disabled state.

- Count is initialized to "0" upon power on reset.
- The count is incremented upon each entry into the USDPort.Disabled state from the USDPORT.Training Initiated state.
- If the count equals 3, the port transitions to the Disabled.Error state.
- The count is reset to "0" upon a successful completion of the Port Configuration process.

In this state, the port's link shall be in the eSS.Disabled state. The corresponding peripheral device USB state shall be USB 2.0 Device States.

### 10.18.2.7 USDPORT.Disabled_Error

A port transitions to this state from the USDPort.Disabled state when Disabled_Count = 3

- The port shall remain in USDPORT.Disabled_Error state if the port's link receives a USB 2.0 reset.

In this state, a fatal error has been detected on the port's link and the link shall be in the eSS.Disabled state. The corresponding peripheral device USB state shall be USB 2.0 Device States.

10-92