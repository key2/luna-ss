Revision 1.1
June 2022

- 529 -

Universal Serial Bus 3.2
Specification

○ The far-end low-impedance receiver termination (R_RX-DC) defined in Table 6-22 is detected at both ports of the config lane.
○ The Polling.LFPS signal is received at either port if the LFPS receiver in the LD is enabled.
○ When directed by RLSM. Note that the opposite sublink may have received Polling.LFPS implying the presence of R_RX-DC.

• The next state is Disabled if directed.

### E.6.3.4 Active

Active is a state where the re-driver is either forwarding the LFPS signal or SS signal. It maps the LTSSM states of Polling, U0, Recovery, Loopback, Hot Reset, Compliance Mode, and Rx.Detect sub-state of Rx.Detect.Reset. The re-driver shall meet the following requirement.

• It shall enable its low-impedance receiver termination (R_RX-DC) at config lane. It may enable its low-impedance receiver termination (R_RX-DC) at non-config lane in x1 operation.
• It shall forward the received LFPS on the config lane, and SS signal on both lanes if it is x2 operation.
• It shall monitor the input status and manage the LD and LRD operation during various LTSSM link state in Active.
• It shall implement a 24 ms tEITimeout timer to monitor the duration of EI. This timer shall be started when LFPS EI or the transition from SS signal to LFPS EI is detected. It shall be reset and disabled if an input signal is detected. Note that this timer is intended to ensure that the link enters U3 or eSS.Inactive, and to overcome any EI during Polling to remain in Active.
• It shall remain in this state if EI is declared and the tEITimeout timer has not expired.
• It shall monitor the duration of the LFPS signal. If it is Warm Reset, it shall perform the following at then of Warm Reset
  ○ It shall perform the far-end receiver termination detection at its DFP.
  ○ It shall block any Polling.LFPS signal it may receive at its DFP while performing the far-end receiver termination detection at its DFP.

The re-driver shall perform the state transition based on the following.

• The next state is Disabled if Directed.
• The next state is Slumber if directed or when the tEITimeout timer has expired and the input remains in EI.
• The next state is Connect if the far-end low-impedance receiver termination (R_RX-DC) defined in Table 6-22 is not detected.

### E.6.3.5 Slumber

Slumber is a state where the input is in EI and the re-driver is in a low power state. It maps the USB link states of U3, and eSS.Inactive. The re-driver shall meet the following requirement.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.