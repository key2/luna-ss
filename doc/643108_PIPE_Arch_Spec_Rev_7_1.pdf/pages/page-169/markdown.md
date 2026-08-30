intel®

- If RxStandbyStatus returns in response to RxStandby, it should continue to do so in NELB mode.
- If RxStandbyStatus is not supported (for instance, USB) or guaranteed, the same holds true in NELB mode.

- Rate Changes:

- This operates the same as in normal operation.
- The same combinations of Rate, Width, PCLK Rate, RxWIDTH, and so forth. It must be supported in NELB mode as in normal operation.
- Clock changes related to rate changes should remain the same as in normal operation.

- For instance, PclkChangeOk / PclkChangeAck should remain the same.

- TxDetectRx/Loopback must not be used to indicate follower loopback operation while NELB is enabled.

- Start of data transfer on Rx data path:

- If the PHY cannot guarantee all bits will be looped back when the Rx data path is exiting electrical idle, it must clearly specify in its datasheet when the first data will appear.

- For instance, the block aligner requires two EIEOSs to begin forwarding data and the data from the Tx data path up to the 2nd EIEOS would not be seen (similar thing for 8b/10b aligner).

- NELB must function when SRISEnable is high or low.

- No false or additional ppm is required to be applied if SRISEnable is high.

- RefClkRequired# must function as it does in normal operation.

- DataBusWidth must function as it does in normal operation.

- TxDeemph and TxSwing must continue to be consumed by the PHY. The PHY may choose to ignore them if the loopback point is not affected by the Tx EQ settings.

- The controller must not use the following functions while in NELB as the PHY may not return a response:

- Receiver Lane Margining
- TxMargin
- IORecal

- Elastic Buffer controls as defined in the message bus section (depth, run mode, and so forth) must continue to function the same as normal operation.

- BlockAlignControl functionality is expected to function the same as in normal operation.

- EncodeDecodeBypass must operate as it does in normal operation.

- RxPolarity functionality must continue to operate the same as in normal operation.

- PHY or MAC can implement implementation specific means to invert the data for increased test coverage.

- Local Preset Fetch bus must function as it does in normal operation.

- GetLocalPresetCoefficients, LocalPresetIndex, LocalFS, LocalLF, LocalG{5,4}FS, LocalG{5,4}LF, LocalTxPresetCoefficient

- FS and LF of link partner must continue to be reported as in normal operation.

Reference Number: 643108, Revision: 7.1

169