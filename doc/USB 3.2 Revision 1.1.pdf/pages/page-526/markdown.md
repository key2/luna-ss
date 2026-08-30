Revision 1.1
June 2022

- 495 -

Universal Serial Bus 3.2
Specification

### **E.2.2.1 Physical Layer Requirements**

A re-timer shall conform to the following requirement at the physical layer.

- It shall meet all the physical layer requirements defined in Chapter 6.
- For a bit level re-timer, it shall meet additional jitter transfer function requirement defined in Section E.5.

### **E.2.2.2 Link Layer Requirements**

The purpose for re-timers to implement partial link layer function is to achieve protocol awareness such that the re-timer operation is in concert with the host and device. A re-timer shall implement the following capabilities.

- LFPS based Polling.LFPS, SCD1/SCD2, and LBPM tracking and decoding. A re-timer shall monitor Polling.LFPS and SCD1/SCD2 to determine SuperSpeedPlus operation and decode LBPM to determine port configuration negotiated between the host and device. Refer to Section E.3.4 for details.
- TS2 ordered set decoding. A re-timer shall decode the link configuration field in TS2 ordered set to determine the link operation during Polling.Idle or Recovery.Idle. Refer to Sections E.3.4.5 and E.3.11 for details.
- Link command tracking. A re-timer shall track the link command and HPs to synchronize its link operation with the host and device. This includes but is not limited to determining the re-timer's upstream port to host and downstream port to device and tracking link power management. Refer to Section E.3.7 for details.
- Packet boundary tracking. A SRIS re-timer in SS operation shall track the packet boundary to perform the clock offset compensation. Refer to Section E.4.1 for details.

### **E.2.2.3 x2 Re-timer Requirements**

In addition to meeting the general re-timer requirements defined in Sections E.2.2.1 and E.2.2.2, a re-timer in x2 operation shall also meet the following requirement.

- It shall establish the Configuration Lane when directed. Note that it is implementation specific for a captive re-timer or a re-timer in an active cable to determine the Configuration Lane.
- The re-timer shall perform the lane-to-lane deskew meeting requirements defined in Table 6-34. Specifically,
  - The re-timer shall complete the lane-to-lane deskew before switching from the local TS1 OS to received TS1 or TS2 OS. The re-timer may perform the lane-to-lane deskew based on either TS1 OS, TS2 OS, or SKP OS in Gen 1x2 operation, or SYNC OS in Gen 2x2 operation.
  - The re-timer shall preserve the OS boundary when switching from the local TS1 OS to received TS1 OS or TS2 OS to maintain transmitter lane-to-lane skew.
- The far-end receiver termination detection and the LFPS based operation shall be performed only on the Configuration Lane.
- The maximum re-timer delay (tDRe-timer) shall be 300 ns in Gen 1x2 operation, and 200 ns in Gen 2x2 operation.

### **E.3 Re-timer Training and Status State Machine (RTSSM)**

The primary responsibility of a re-timer is to maintain connectivity between the host and device. This includes but is not limited to monitoring the state of connectivity between the

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.