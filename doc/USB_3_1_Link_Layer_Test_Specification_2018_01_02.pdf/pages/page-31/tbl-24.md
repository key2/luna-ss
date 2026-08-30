|  7.5.1#1 | A downstream port shall transition to eSS.Disabled from any other state when directed. | NT  |
| --- | --- | --- |
|  7.5.1#2 | An upstream port shall transition to eSS.Disabled when VBUS is not valid. | NT  |
|  Subsection reference: 7.5.1.1 eSS.Disabled for Downstream Ports and Hub Upstream Ports  |   |   |
|  Subsection reference: 7.5.1.1.1 eSS.Disabled Requirements  |   |   |
|  7.5.1.1.1#1 | The port's receiver termination shall present high impedance to ground of ZRX-HIGH-IMP-DC-POS when in SS.Disabled. | NT  |
|  7.5.1.1.1#2 | The port shall be disabled from transmitting and receiving LFPS and Enhanced SuperSpeed signals when in SS.Disabled. | NT  |
|  Subsection reference: 7.5.1.1.2 Exit from eSS.Disabled  |   |   |
|  7.5.1.1.2#1 | A downstream port shall transition to Rx.Detect when directed. | NT  |
|  7.5.1.1.2#2 | An upstream port shall transition to Rx.Detect only when VBUS transition to valid or a USB2.0 bus reset is detected. | NT  |
|  Subsection reference: 7.5.1.2 eSS.Disabled for Upstream Ports of Peripheral Devices  |   |   |
|  Subsection reference: 7.5.1.2.2 eSS.Disabled Requirements  |   |   |
|  7.5.1.2.2#1 | The requirements from section 7.5.1.1.1 apply. | NT  |
|  7.5.1.2.2#2 | A peripheral upstream port shall implement a tDisabledCount counter that shall be reset to zero upon invalid Vbus or a successful port configuration exchange. | NT  |
|  7.5.1.2.2#3 | The tDisabledCount counter shall be incremented upon entry to eSS.Disabled.Default | NT  |
|  Subsection reference: 7.5.1.2.3 Exit from eSS.Disabled.Default  |   |   |
|  7.5.1.2.3#1 | A peripheral upstream port shall transition to Rx.Detect when Vbus transitions to valid. | NT  |
|  7.5.1.2.3#2 | A peripheral upstream port shall transition to Rx.Detect when a USB 2.0 bus reset is detected and tDisabledCount is less than three. | NT  |
|  7.5.1.2.3#3 | A peripheral upstream port shall transition to eSS.Disabled.Error if tDisabledCount is three. | NT  |
|  Subsection reference: 7.5.1.2.4 Exit from eSS.Disabled.Error  |   |   |
|  7.5.1.2.4#1 | A peripheral upstream port shall transition to Rx.Detect upon PowerOn reset. | NT  |
|  7.5.1.2.4#2 | A self-powered peripheral upstream port shall transition to eSS.Disabled.Default upon detection of invalid Vbus. | NT  |