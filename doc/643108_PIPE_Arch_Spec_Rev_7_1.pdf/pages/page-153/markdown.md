intel®

1. See the PCIe base specification. In case of discrepancy, the PCIe base specification supersedes the PIPE specification.

## 8.23 Control Signal Decode Table – PCIe Mode

Table 8-5 summarizes the encodings of four of the seven control signals that cause different behaviors depending on power state. For the other three signals, Reset# always overrides any other PHY activity. TxCompliance and RxPolarity are only valid when the PHY is in P0 and is actively transmitting. Note that these rules only apply to lanes that have not been “turned off” as described in Section 10 (multi-lane PIPE).

For SerDes mode, the rules summarized in Table 8-5 apply to each of the TxElecIdle[3:0] bits independently for the P0 and P0s states. There is an expectation that entering Electrical Idle must occur from MSB to LSB, that is, valid values of TxElecIdle[3:0] are 1000b, 1100b, 1110b, 1111b, and 0000b. Figure 8-7 shows the various scenarios of valid TxElecIdle transitions. Transitions into Electrical Idle can include a single cycle of only a subset of data bytes driven to Electrical Idle followed by all data bytes in Electrical Idle; transitions out of Electrical Idle must be done simultaneously for all data bytes. For the P1 and P2 power states, all the bits of TxElecIdle[3:0] are expected to be driven to the same value so only TxElecIdle[0] needs to be decoded.

Table 8-5. Control Signal Decode Table – PCIe Mode

[tbl-141.md](tbl-141.md)

Reference Number: 643108, Revision: 7.1

153