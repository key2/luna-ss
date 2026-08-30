intel®

For the Nominal Empty buffer model, the PHY attempts to keep the elasticity buffer as close to empty as possible. In the Nominal Empty mode, the PHY uses the RxDataValid interface to tell the MAC when no data is available. The Nominal Empty buffer model provides a smaller worst case and average latency than the Nominal Half Full buffer model, but it requires the MAC to support the RxDataValid signal. The PHY removes all SKP symbols in Nominal Empty buffer mode.

For the Nominal Half Full buffer model, the PHY is responsible for inserting or removing SKP symbols, ordered sets, or ALIGNs in the received data stream to avoid elastic buffer overflow or underflow. The PHY monitors the receive data stream, and when a Skip ordered set or ALIGN is received, the PHY can add or remove one SKP symbol (PCIe Mode at 2.5 or 5 GT/s), four SKP symbols (PCIe Mode at 8 GT/s, 16 GT/s, or 32 GT/s), one SKP ordered set (USB Mode at 5 GT/s), or one ALIGN from each SKP or ALIGN as appropriate to manage its elastic buffer to keep the buffer as close to half full as possible. In USB mode at 5 GT/s, the PHY must only add or remove SKP ordered sets. In USB mode at 10 GT/s, the PHY must only add or remove multiples of four SKP symbols. Whenever the SKP symbols or an ordered set is added to or removed, the PHY will signal this to the MAC using the RxStatus[2:0] signals. These signals have a non-zero value for one clock cycle and indicate whether an SKP symbol or ordered set was added to or removed from the received SKP ordered sets. For PCIe, the timing of RxStatus[2:0] assertion depends on the operational rate since SKP ordered sets are encoded differently in 8b/10b mode versus 128/130b mode. In PCIe mode at 2.5 or 5 GT/s, RxStatus[2:0] must be asserted during the clock cycle when the COM symbol of the SKP ordered set is moved across the parallel interface. In PCIe mode at 8 GT/s, 16 GT/s, or 32 GT/s, RxStatus[2:0] must assert anytime between and including the start of the SKP ordered set and the SKP_END symbol. In SATA mode, whenever an ALIGN symbol is added or removed, the PHY will signal this to the MAC using the RxStatus[2:0] signals. These signals have a non-zero value for one clock cycle and indicate whether an ALIGN was added or removed. RxStatus must be asserted during the clock cycle when the first symbol of the added ALIGN is moved across the parallel interface.

In PCIe mode, the rules for operating in Nominal Empty buffer mode are as follows:

- Use of the RxDataValid is required.
- All SKP symbols of SOS are removed (8b/10b SKP or 128/130 AA).
- When an empty condition happens (caused by clock drift or SOS removal):
  - RxValid must remain high.
    - RxValid should only be dropped for symbol alignment loss or block alignment loss.
  - RxDataValid must be deasserted.
  - RxStatus must be 0.

- EB full can still occur and is considered an error.
- Notification of an SOS coming through the EB must be reported in the following manner:

- 8b/10b: COM of SOS must be passed with RxStatus = SKP removed (010), SKP symbols dropped.

- 128/130: Start of SOS block, with first byte SKP_END or SKP_END_CTRL, must be passed with RxStatus = SKP Removed (010), all AA SKP symbols dropped.

- The EB is permitted to start RxDataValid as soon as data is available, but should never assert faster than the usual RxDataValid rate.

Reference Number: 643108, Revision: 7.1

135