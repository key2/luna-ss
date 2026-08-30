intel®

## 6.2.2 Command Interface

Table 6-16. SerDes Only: Command Interface Input Signals

[tbl-48.md](tbl-48.md)

## 6.2.3 MacCLK Lane Signals

A MacCLK lane is an optional feature that is implemented only by PHYs that support MacCLK. The signals defined here are per MacCLK lane. These signals are independent of the other PIPE signals. Refer to Section 8.1.2 for more details. The MacCLK lane signals are in the MacCLKReset# domain. The MAC and the PHY must not rely on the signals being held at a valid value when MacCLKReset# is asserted. If default values are specified, the MAC and the PHY must guarantee that the signals they drive are stable and at their reset values when MacCLKReset# deasserts. The PHY specifies the minimum MacCLKReset# assertion pulse duration it requires via the paramater MinimumMacCLKReset#AssertionPulse.

70

Reference Number: 643108, Revision: 7.1