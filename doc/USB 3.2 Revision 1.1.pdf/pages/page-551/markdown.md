Revision 1.1
June 2022

- 520 -

Universal Serial Bus 3.2
Specification

# E.3.12.2 Exit from PassThrough Loopback

- The re-timer shall transition to Rx.Detect if any one of the following conditions is met.
  o Upon detecting successful Loopback LFPS exit handshake.
  o Upon timeout of the tLoopbackExitTimeout timer.
  o Upon detecting Warm Reset.

# E.3.13 Local Loopback

Local Loopback is the same as the Loopback state defined in LTSSM. The re-timer always operates as a loopback slave.

# E.3.13.1 Local Loopback Requirements

- The re-timer shall configure the two ports in the following.
  o It shall configure its port receiving TS2 OS with the Local Loopback bit (bit-4) within the link configuration field asserted.
  o It shall configure its other port in Rx.Detect.
- The re-timer shall implement the two substates defined in LTSSM.
- The re-timer operation shall meet the requirements defined in LTSSM.
- In x2 operations, the loopback operation is performed on a per lane basis. The transmitter lane to lane skew does not need to be maintained.

# E.3.13.2 Exit from Local Loopback.Active

- The re-timer shall transition to Rx.Detect upon detecting Warm Reset at its port in Rx.Detect. Note that the re-timer will not declare Warm Reset at its port in Local Loopback.Active since the beginning of the Warm Reset will be treated as the start of the Loopback LFPS exit signal.
- The re-timer shall transition to Local Loopback.Exit upon detection of Loopback LFPS exit signal.

# E.3.13.3 Exit from Local Loopback.Exit

- The re-timer shall transition to Rx.Detect if one of the following conditions is met.
  o Upon detecting Warm Reset.
  o Upon completing the Loopback LFPS exit handshake meeting Loopback LFPS exit signaling defined in Section 6.9.2.

# E.3.14 Hot Reset

Hot Reset is a state where no actions need to be taken by the re-timer. The re-timer's responsibility is to monitor the progression of Hot Reset until its completion. The re-timer does not need to implement two substates in Hot Reset.

# E.3.14.1 Hot Reset Requirements

- The re-timer shall track and monitor the progression of LTSSM.
- The re-timer in SS operation shall not delete any inbound TS2 OS with the Reset bit de-asserted in order to perform clock offset compensation. Note that the TS2 OS with the Reset bit de-asserted is used for Hot Reset.Active exit handshake.
- The re-timer shall start the tHotResetActiveTimeout timer upon entry to the state.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.