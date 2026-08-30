intel®

• RxValid:

- The assertion of RxValid should continue to be affected by the Rx logic downstream of the loop back point. For instance, if alignment (8b/10b or 128/130b) must occur first before RxValid is asserted, then it must be required in NELB when the alignment logic is in the active Rx data path.
- In SerDes mode, RxValid must assert when the RxCLK is stable and the TxElecIdle is no longer asserted.

• RxElecIdle:

- The RxElecIdle signal must reflect the TxElecIdle signal with minimal delay, especially at the end of the data stream. If RxElecIdle is not asserted soon enough after TxElecIdle, this may result in false wakeups from L1. The RxElecIdle signal should not lag the RxData by more than normal operation would. RxElecIdle is permitted to precede the RxData if that is how normal operation would happen.

• RxStatus:

- For TxDetectRx functionality, see following entries.
- For error and skip adjustment status
  - If bad data will be transferred on initial EI exit, mark as required by protocol with RxStatus.
    - If the loopback point is in the analog or high speed digital domains that may be susceptible to bit errors, RxStatus should reflect these as required by the protocol mode.
    - Note: The PHY may need to be tuned to avoid errors if a loopback path in the analog or high-speed digital domain is selected.
  - If a skip adjustment is done, RxStatus must reflect such action.

• Tx Detect Receiver:

- The results of doing Tx receiver detect will be equal to the state of RXTermination (RxStatus of 3).
- If asynchronous TxDetectRx is supported in normal operation, it must also be supported in NELB mode.

• RxEqEval / RxEqTrain:

- Depending on loopback position, these operations may return fabricated dummy results. The PHY must indicate in its datasheet which loop back positions result in fabricated dummy results.
- To enable the MAC to consume the results in the same manner as it does in normal operation, the PHY must adhere to the following rules when returning fabricated dummy results:
  - Directional feedback must return no update required (0).
  - Figure of Merit Feedback must return a non-zero value.
    - It is recommended that the MAC have the ability to shorten its search algorithms in NELB mode.
  - RxEqEval / RxEqTrain response time in NELB mode must not exceed 10 us.

• Powerdown / Phystatus:

- This operates the same as in normal operation.

• RxStandby / RxStandbyStatus:

- This operates the same as in normal operation:

168

Reference Number: 643108, Revision: 7.1