|  7.3.10#5 | For SuperSpeed operation, an upstream port of a peripheral device shall transition to eSS.Disabled when a Training Sequence error occurs during Polling. | NT  |
| --- | --- | --- |
|  7.3.10#6 | For SuperSpeed operation, a downstream port shall transition to eSS.Inactive when a Training Sequence error occurs during Recovery and the transition to Recovery is not an attempt for Hot Reset. | NT  |
|  7.3.10#7 | For SuperSpeed operation, a downstream port shall transition to Rx.Detect when a Training Sequence error occurs during Recovery.Active and Recovery.Configuration and the transition to Recovery is not an attempt for Hot Reset. | NT  |
|  7.3.10#8 | For SuperSpeed operation, an upstream port shall transition to eSS.Inactive when a Training Sequence error occurs during Recovery. | NT  |
|  Subsection reference: 7.4 PowerOn Reset and Inband Reset  |   |   |
|  Subsection reference: 7.4.1 Power On Reset  |   |   |
|  7.4.1#1 | Receiver termination shall meet the ZRX-HIGH-IMP-DC-POS when PowerOn Reset is asserted or while VBUS is OFF. | NT  |
|  7.4.1#2 | Transmitters shall hold a constant DC common mode voltage (VTX-DC-CM) when PowerOnReset is asserted or while VBUS is OFF. | NT  |
|  7.4.1#3 | The LTSSM of a port shall be initialized to Rx.Detect, when PowerOnReset is completed and VBUS is valid. | NT  |
|  7.4.1#4 | The LTSSM and the PHY level variables shall be reset to their default values, when PowerOnReset is completed and VBUS is valid | NT  |
|  7.4.1#5 | The receiver termination of a port shall meet RRX-DC, when PowerOnReset is completed and VBUS is valid. | NT  |
|  Subsection reference: 7.4.2 Inband Reset  |   |   |
|  7.4.2#1 | Upon completion of Hot Reset, a downstream port shall reset its Link Error Count. | NT  |
|  7.4.2#2 | Upon completion of Hot Reset, the port shall reset its PM timers and the associated U1 and U2 timeout values to zero. | LVS  |
|  7.4.2#3 | Upon completion of Hot Reset, the port configuration information of an upstream port shall remain unchanged. | 7.28 7.29  |
|  7.4.2#4 | Upon completion of Hot Reset, the PHY level variables shall remain unchanged. | NT  |
|  7.4.2#5 | Upon completion of Hot Reset, the LTSSM of a port shall transition to U0. | 7.27-29  |