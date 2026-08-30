|  Name | Initial State | Timeout to Next State | Timeout Values  |
| --- | --- | --- | --- |
|  teSSInactiveQuietTimeout | eSS.Inactive.Quiet | eSS.Inactive.Disconnect.Detect | 12 ms  |
|  tRxDetectQuietTimeoutDFP^{1} | Rx.Detect.Quiet | Rx.Detect.Active | 12 ms (min) 120 ms (max)  |
|  tRxDetectQuietTimeoutUFP | Rx.Detect.Quiet | Rx.Detect.Active | 12 ms  |
|  tPollingLFPSTimeout | Polling.LFPS /Polling.LFPSPlus^{2} | Compliance/Rx.Detect/ eSS.Disabled/eSS.Inactive | 360 ms  |
|  tPollingSCDLFPSTimeout (SuperSpeedPlus operation) | Polling.LFPS or Polling.LFPSPlus | Polling.RxEQ | 60 μs  |
|  tPollingLBPMLFPSTimeout (SuperSpeedPlus operation) | Polling.PortMatch or Polling.PortConfig | Rx.Detect/ eSS.Disabled/eSS.Inactive | 12 ms  |
|  tPollingActiveTimeout | Polling.Active^{2} | Rx.Detect/Polling.PortMatch/ eSS.Disabled/eSS.Inactive | 12 ms (x1) 24 ms (x2)  |
|  tPollingConfigurationTimeout | Polling.Configuration^{2} | Rx.Detect/Polling.PortMatch/ eSS.Disabled/eSS.Inactive | 12 ms (x1) 24 ms (x2)  |
|  tPollingIdleTimeout | Polling.Idle^{2} | Rx.Detect/Polling.PortMatch/ eSS.Disabled/ eSS.Inactive | 2 ms  |
|  tU0RecoveryTimeout | U0 | Recovery | 1 ms  |
|  tU0LTimeout | U0 | U0 | 10 μs  |
|  tNoLFPSResponseTimeout | U1 | eSS.Inactive | 2 ms  |
|  PORT_U2_TIMEOUT | U1^{3} | U2 | U2 Inactivity field set in LMP (refer to Section 8.4 for details)  |
|  tU1PingTimeout | U1 | Rx.Detect | 300 ms  |
|  tNoLFPSResponseTimeout | U2 | eSS.Inactive | 2 ms  |
|  tNoLFPSResponseTimeout | U3 | U3 | 10 ms  |
|  tRecoveryActiveTimeout | Recovery.Active | eSS.Inactive, Rx.Detect | 12 ms  |
|  tRecoveryConfigurationTimeout | Recovery.Configuration | eSS.Inactive, Rx.Detect | 6 ms  |
|  tRecoveryIdleTimeout | Recovery.Idle | eSS.Inactive | 2 ms  |
|  tLoopbackExitTimeout | Loopback.Exit | eSS.Inactive | 2 ms  |
|  tHotResetActiveTimeout | Hot Reset.Active | eSS.Inactive | 12 ms  |
|  tHotResetExitTimeout | Hot Reset.Exit | eSS.Inactive | 2 ms  |
|  tU3WakeupRetryDelay | U3 | U3 | 100 ms  |
|  tU2RxdetDelay | U2 | U2 | 100 ms  |
|  tU3RxdetDelay | U3 | U3 | 100 ms  |