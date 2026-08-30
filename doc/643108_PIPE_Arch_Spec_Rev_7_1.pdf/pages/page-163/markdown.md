intel®

Table 8-10. Lane Margining at the Receiver Sequences (Sheet 4 of 4)

[tbl-150.md](tbl-150.md)

1. Writes to RxMarginStatus.SampleCount are only applicable if Sample Count is supported. Writes to RxMarginStatus.ErrorCount are only applicable if Error Count is supported.

### 8.31 Short Channel Power Control

For short reach (for instance, MCP applications), there should be a provision to revert the ShortChannelPowerControl[1:0] signal to normal operation mode for situations where an optimized mode setting prevents link up. For example, if a particular setting is not compatible with a 2.5 GT/s link speed and works only at higher link speeds, the expectation is that the ShortChannelPowerControl[1:0] signal would be set to normal operation mode to bring the link up initially before changing the value to an optimized power control setting while transitioning to higher link speeds.

Reference Number: 643108, Revision: 7.1

163