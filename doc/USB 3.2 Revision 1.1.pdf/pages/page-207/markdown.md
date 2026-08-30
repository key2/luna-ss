Revision 1.1
June 2022

- 176 -

Universal Serial Bus 3.2
Specification

PHY capability may later be adjusted in order to match the link partner's capability or if the link fails to reach U0 during training and the two ports need to fall back to a lower rate.

PHY Ready LBPM is defined to serve two purposes. One is for a port to send a notification that it has completed its PHY re-configuration and ready for link training at the matched port capability defined by PHY Capability LBPM. The other is for a re-timer in x2 operation to announce its presence during PHY Ready LBPM handshake. Refer to Section 7.5.4.6 for use of PHY Ready LBPM. Note that there are two types of PHY Ready LBPM handshakes. The first type is with bit-7 of the DFP PHY Ready LBPM asserted. This is to indicate that after completing the re-timer presence announcement, there is an option in future revisions that a DFP may want to address the re-timers. This is referred to RT Config. The second type is with bit-7 of the DFP PHY Ready LBPM de-asserted. This is to indicate that DFP has either RT Config completed and is ready to exit, or bypasses RT Config and proceeds directly to exit. Refer to Section 7.5.4.6.1 for details

- The port shall rank its PHY capability in the order of Gen 2x2, Gen 2x1, Gen 1x2, and Gen 1x1. The start-up PHY capability is defined in Table 7-14.

Table 7-14. Start-up PHY Capability Match

[tbl-94.md](tbl-94.md)

- If a SuperSpeedPlus port's highest PHY capability is Gen 2x2, it shall follow the PHY capability fallback order shown in Table 7-15. Note that if the port falls back from Gen 2x2 to Gen 2x1, or Gen 1x2 to Gen 1x1, it shall operate in Gen 2x1 or Gen 1x1 on the Configuration Lane.
- If a SuperSpeedPlus port's highest PHY capability is Gen 2x1, its next advertised PHY capability shall be Gen 1x1.
- If a SuperSpeedPlus port's highest PHY capability is Gen 1x2, its next advertised PHY capability shall be Gen 1x1.

Table 7-15. Gen 2x2 PHY Capability Fallback Order

[tbl-95.md](tbl-95.md)

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.