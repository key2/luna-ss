Revision 1.1
June 2022

- 497 -

Universal Serial Bus 3.2
Specification

In the following subsections, the details of RTSSM are described. The operations that are common to LTSSM will not be elaborated.

It is worth mentioning that the main purpose of RTSSM is to describe and define the re-timer operation under various LTSSM states. The external behavior of the RTSSM shall reflect that of the LTSSM. The implementation may vary regarding RTSSM optimization.

### E.3.1 Warm Reset

Unlike devices that only need to detect Warm Reset, a re-timer has an added responsibility to detect and forward Warm Reset that complies with the electrical and timing specification defined in Section 6.9.3. The re-timer shall perform the following under different link states.

- In Rx.Detect, Polling, Recovery, U0, Hot Reset, Compliance Mode, or BLR Compliance Mode, if the LFPS signal is neither Polling.LFPS nor LBPM, the re-timer shall infer the reception of Warm Reset and forward the received LFPS signal within 200 μs.
- In U1 or U2, if the re-timer performs simultaneous Ux LFPS exit handshake, regardless of the Ux LFPS exit handshake status, the re-timer shall remain in Ux and continue the LFPS transmission at its downstream port if its upstream port continues to receive the LFPS signal. This is to ensure that the re-timer transmit continuous LFPS signal without interruption before resolving if the received LFPS signal at its upstream port is Ux LFPS exit handshake, or Warm Reset. The re-timer shall declare one of the following conditions.

- It shall infer Warm Reset if the duration of the LFPS signal is more than 2 ms.
- It shall declare the successful Ux LFPS exit handshake if the successful Ux LFPS exit handshakes are achieved at both ports and the duration of the received LFPS signal is less than 2 ms.
- It shall declare the failure of Ux LFPS exit handshake if it has not achieved the successful U1 or U2 LFPS exit handshake at either port within 2 ms.

- In U1, U2 or U3, if the re-timer forwards the LFPS signal, it shall forward the received LFPS signal regardless of the Ux LFPS exit handshake status. The re-timer shall declare one of the following conditions.

- It shall infer Warm Reset if the duration of the LFPS signal is more than 2 ms when exit from U1 or U2, or 10 ms when exit from U3.
- It shall declare the successful Ux LFPS exit handshake if the successful Ux LFPS exit handshakes are observed at both ports and the duration of the received LFPS signal is less than 2 ms when exit from U1 or U2, or 10 ms when exit from U3.
- It shall declare the failure of Ux LFPS exit handshake if the successful U1 or U2 LFPS exit handshake is not observed at either port within 2 ms when exit from U1 or U2, or 10 ms when exit from U3.

- In U3, if the beginning part of Warm Reset is treated as U3 LFPS exit signal from the host, and the re-timer is not ready to exit from U3, the re-timer shall transition to U3S and monitor the duration of the LFPS signal. It shall infer Warm Reset if the received LFPS signal is more than 15 ms. The re-timer shall forward the LFPS signal and complete the Warm Reset transmission meeting the timing specification defined in Section 6.9.3.

- In PassThrough Loopback or Local Loopback, there is no need to distinguish between Warm Reset and the Loopback LFPS exit handshake. The re-timer transitions to Rx.Detect in either condition.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.