|  Name | Active Level | Description |   |   |   | Relevant Protocols  |
| --- | --- | --- | --- | --- | --- | --- |
|  PowerDown[3:0] DisplayPort mode | N/A | DisplayPort mode power states: [3][2][1][0] Description 0 0 0 0 POWER_STATE_0 operational state 0 0 0 1 POWER_STATE_1 PHY-specific 0 0 1 0 POWER_STATE_2 PHY-specific 0 0 1 1 POWER_STATE_3 PHY-specific 0 1 0 0 POWER_STATE_4 PHY-specific 0 1 0 1 POWER_STATE_5 PHY-specific 0 1 1 0 POWER_STATE_6 PHY-specific 0 1 1 1 POWER_STATE_7 PHY-specific 1 0 0 0 POWER_STATE_8 PHY-specific 1 0 0 1 POWER_STATE_9 PHY-specific 1 0 1 0 POWER_STATE_10 PHY-specific 1 0 1 1 POWER_STATE_11 PHY-specific 1 1 0 0 POWER_STATE_12 PHY-specific 1 1 0 1 POWER_STATE_13 PHY-specific 1 1 1 0 POWER_STATE_14 PHY-specific 1 1 1 1 POWER_STATE_15 PHY-specific A PIPE-compliant DPRx PHY is recommended to support the following power states, although the mapping to the above power state encodings is PHY implementation specific: |   |   |   | DisplayPort  |
|   |   |  Main Link Rx | Aux Link | Exit Latency | Required  |   |
|   |   |  Enabled | Enabled | N/A | Yes  |   |
|   |   |  Disabled | Enabled for differential signal monitoring | <1 ms | Yes  |   |
|   |   |  Disabled | Enabled for differential signal monitoring | <80 ms | No  |   |
|   |   |  Disabled | Enabled | <0.5 | Yes for eDP only  |   |
|   |   |  Disabled | Enabled | <20 us | Yes for eDP only  |   |
|   |   |  A PIPE compliant DPTX PHY is recommended to support the following power states, although the mapping to specific power state encodings is PHY implementation specific:  |   |   |   |   |
|   |   |  Main Link TX | Aux Link | DP_PWR  |   |   |
|   |   |  Enabled | Enabled | Enabled  |   |   |
|   |   |  Disabled | Enabled | Enabled  |   |   |
|   |   |  If PowerDown changes during IORecal, RxEqEval, or RxEqTraining operations, the PHY must abort the request and return the handshake acknowledgment.  |   |   |   |   |