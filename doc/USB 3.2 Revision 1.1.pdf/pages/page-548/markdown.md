Revision 1.1
June 2022

- 517 -

Universal Serial Bus 3.2
Specification

### E.3.11 Recovery

The re-timer operations in Recovery are largely the same as its operations in Polling.TSx, and Polling.Idle. Recovery contains two substates, Recovery.TSx and Recovery.Idle as shown in Figure E-14.

#### E.3.11.1 Exit from Recovery.TSx

- The re-timer shall transition to Recovery.Idle upon observing successful TS2 handshake.
- The re-timer shall transition to Rx.Detect if either one of the following two conditions is met.
  - Upon the expiration of the tRecoveryActiveTimeout timer and no successful TS1 OS handshake has been observed.
  - Upon the expiration of the tRecoveryConfigurationTimeout timer and no successful TS2 OS handshake has been observed.
- The re-timer shall transition to Rx.Detect if Warm Reset is detected. Refer to Section E.3.1 for Warm Reset detection.

#### E.3.11.2 Recovery.TSx

Recovery.TSx is a substate for re-timers to participate link training with host and device. It combines Recovery.Active and Recovery.Configuration LTSSM substates.

##### E.3.11.2.1 Recovery.TSx Requirements

- If entry to Recovery is due to detecting TS1 OS, TS1A OS, or TS1B OS, and bit-lock/symbol lock are still preserved in both directions, a bit-level re-timer shall forward the received OS and monitor the progression of LTSSM. A SRIS re-timer shall transmit local TS1 OS instead of the received TS1A OS or TS1B OS until TS1 OS is received. Note that entry to Recovery under this condition may be due to the need for host to reset the device based on Hot Reset, or other operation modes, or due to bit errors that result in link layer initiating entry to Recovery. The bit-lock and symbol lock are preserved and no link training to acquire bit/symbol lock is required.
- If entry to Recovery is due to the timeout of the tU0RecoveryTimeout timer, or loss of bit-lock and symbol lock, the re-timer shall perform link training as defined in Section E.3.4.4.
- The re-timer shall participate the link training and monitor the status and progression of LTSSM.
- A SRIS re-timer shall preserve the OS boundary when performing OS switch from the local TS1 OS to recovered TS1 OS or TS2 OS. A SRIS re-timer shall not forward any TS2 OS until both received clocks are recovered.
- A SRIS re-timer shall perform the clock offset compensation based on the following.
  - For SS operation, it shall perform the clock offset compensation as defined in Section E.4.1.
  - For SSP operation, it shall perform the clock offset compensation as defined in Section 6.4.3.
- Upon entry to this substate, a bit-level re-timer shall perform its link training and complete the clock and OS switching per Section E.3.4.4.1. Additionally, a bit-level re-timer shall perform the clock and OS switching meeting the following timing requirements.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.