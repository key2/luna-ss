intel®

Table 2-1. Phy Requirements for Legacy Pin Interface versus the Low Pin Count Interface, and Original PIPE versus SerDes Architecture Support

[tbl-5.md](tbl-5.md)

Note:

$^{1}$ To provide interoperability with PCIe and USB MACs that choose not to migrate to the SerDes architecture, PHYs are encouraged to provide support for original PIPE via a method where the associated logic can be easily optimized out. With this, designs that do not require a PHY which supports original PIPE are not burdened with any unneeded logic.

## 2.7 Support for Short Reach (SR) Applications

The PIPE specification supports short channel (also known as Short Reach [SR]) applications, for instance, for multi-chip package solutions. For such applications, the operating power can be reduced significantly by optimizing certain operational and environmental parameters for short channels. For example, the operating power for PCIe can potentially be reduced by up to roughly 50% compared to traditional PCIe applications. While specifying environmental parameters is outside the scope of the PIPE specification, PHY vendors are encouraged to advertise any such environmental knobs that can be changed in short channel applications to reduce power, for instance, reducing the PHY supply voltage. This specification provides hooks for tuning specific operational parameters for reduced power. These operational knobs are PHY vendor-dependent and may include channel loss, receiver equalization activity (including Decision Feedback Equalization [DFE] and Continuous Time Linear Equalization [CTLE]), Tx swing, and clock recovery strategy. PHY vendors that want to support power optimized, short reach applications should identify a useful set of operating points for these knobs that it advertises in its datasheet (via the ShortChannelPowerControlSettingsSupported parameter) that the customer can then select from using the PIPE control interface (via the ShortChannelPowerControl[1:0] signals).

In addition to the just mentioned potential power savings, Multi Chip Package (MCP) applications provide the opportunity for cost savings and additional operational optimization; specifically, it is strongly recommended that DC coupling is used, therefore saving on capacitor insertion cost. As part of the DC coupling support, the controller should bypass explicit receiver detection. For PCIe, the receiver detection operation in the PCIe LTSSM state Detect.Quiet should be bypassed and the LTSSM should automatically proceed to Polling. If the LTSSM transitions back to Detect from Polling due to timeout, it is recommended that a subsequent transition to Polling should occur either upon an electrical idle exit detection or after a 30 to 100 ms timeout. Further optimization based on DC coupling can be implemented to reduce power state (for instance, L1.2) exit latencies.

24

Reference Number: 643108, Revision: 7.1