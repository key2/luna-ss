Revision 1.1
June 2022

- 387 -

Universal Serial Bus 3.2
Specification

- From the DSPORT.Disabled state when a SetPortFeature(PORT_LINK_STATE)
  Rx.Detect request is received for the port.
- From the DSPORT.Disabled state when the hub's upstream port is reset. Note: The
  hub shall issue a Warm Reset on the downstream port, if a device is detected in the
  first Rx.Detect after entering this state, even if the upstream port reset is a hot reset.
- From the DSPORT-Powered-off state or DSPORT.Disabled state when the hub's
  upstream port is reset. Note: The hub shall issue a Warm Reset on the downstream
  port after it has transitioned the port to the DSPORT.RxDetect state and detected a
  far-end receiver, even if the upstream port reset is a hot reset
- From the DSPORT.Resetting state if the port's link times out from any Polling
  substate during a reset.
- From the DSPORT.Training state if the port's link times out from any Polling substate
  and the cPollingTimeout is less than 2 and the port is not enabled to enter
  compliance or Polling substate which timed out is not Polling.LFPS. See definition of
  PollingTimeout in Section 7.5.4.2 and Section 10.16.2.10 defining Set Port Feature
  for enabling compliance entry.
- From the DSPORT.Loopback state if the port's link performs a successful LFPS
  handshake in Loopback.Exit.

In this state, the port's link shall be in the Rx.Detect state.

Note: The port's link shall still perform connection detection normally from the Rx.Detect if
the hub upstream port's link is in U3.

#### **10.3.1.3 DSPORT.Training**

A port transitions to this state from the DSPORT.Disconnected state when far-end receiver
terminations are detected.

In this state, the port's link shall be in the Polling state.

#### **10.3.1.4 DSPORT.ERROR**

A port shall transition to this state only when an Enhanced SuperSpeed device is connected
and a serious error condition occurred while attempting to operate the link.

A port transitions to this state in any of the following situations:

- From the DSPORT.Enabled state if the link enters recovery and times out without
  recovering.
- From the DSPORT.Enabled state if U1 or U2 exit fails.
- From the DSPORT.Loopback state if the port is the loopback master and the LFPS
  handshake in Loopback.Exit fails.
- From DSPORT.Enabled if Port Configuration fails as described in Section 8.4.6.
- From the DSPORT.Training state if the port's link times out from any Polling substate
  and cPollingTimeout is 2. See 7.5.4.2 for details of cPollingTimeout.

In this state, the port's link shall be in the eSS.Inactive state.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.