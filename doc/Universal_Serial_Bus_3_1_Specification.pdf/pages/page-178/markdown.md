Universal Serial Bus 3.1 Specification, Revision 1.0

Table 6-14. Gen 2 Compliance Pattern

[tbl-67.md](tbl-67.md)

## 6.5 Clock and Jitter

### 6.5.1 Informative Jitter Budgeting

The jitter for USB 3.1 is budgeted among the components that comprise the end to end connections: the transmitter, channel (including packaging, connectors, and cables), and the receiver. The jitter budget is derived at the silicon pads. The Dj distribution is the dual Dirac method. Table 6-15 lists Tx, Rx, and channel jitter budgets.

Table 6-15. Informative Jitter Budgeting at the Silicon Pads

[tbl-68.md](tbl-68.md)

Notes:

1. Rj is the sigma value assuming a Gaussian distribution.

2. Rj Total is computed as the Root Sum Square of the individual Rj components.

3. Dj budget is using the Dual Dirac method.

4. Tj at a 10$^{-12}$ BER is calculated as 14.068 * Rj + Dj.

5. The media budget includes the cancellation of ISI from the appropriate Rx equalization function.

6. Tx is measured after application of the JTF.

# NOTE

# Captive Cables

Captive cables must meet the mated connector requirements specified in Section 5.6.1.2. But a captive cable is not considered a stand-alone component. For electrical budgeting purposes, a captive cable is considered to be part of a device, and must meet the device jitter requirements listed in Table 6-15.

### 6.5.2 Normative Clock Recovery Function

The Tx Phase jitter measurement is performed using a standard clock recovery, shown in Figure 6-12. For information on the golden PLL measurement refer to the latest version of INCITS

6-22