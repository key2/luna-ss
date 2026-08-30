intel®

- The standard PHY interface enables multiple IP sources for the PCIe logical layer and provides a target interface for PCIe PHY vendors.
- Support for 2.5 GT/s only, or 2.5 GT/s and 5.0 GT/s, or 2.5 GT/s, 5.0 GT/s and 8.0 GT/s, or 2.5 GT/s, 5.0 GT/s, 8.0 GT/s, and 16 GT/s, or 2.5 GT/s, 5.0 GT/s, 8.0 GT/s and 16 GT/s and 32 GT/s, or 2.5 GT/s, 5.0 GT/s, 8.0 GT/s, 16 GT/s, 32 GT/s, 64 GT/s, and 128 GT/s serial data transmission rate.
- It utilizes 8-bit, 16-bit, or 32-bit parallel interfaces to transmit and receive PCIe data. Additionally, it supports a 64-bit interface (in SerDes architecture only).
- Allowed integration of high-speed components into a single functional block as seen by the endpoint device designer
- Data and clock recovery from serial stream on the PCIe bus
- Holding registers to stage transmit (Tx) and receive (Rx) data
- Support of direct disparity control for use in transmitting compliance patterns
- 8b/10b encoding and decoding, and error indication (original PIPE)
- 128b/130b encoding and decoding, and error indication (original PIPE)
- Receiver detection
- Beacon transmission and reception
- Selectable Tx margining, Tx de-emphasis and signal swing values
- Lane margining at the receiver
- Polarity (original PIPE)
- Electrical Idle entry and exit detection (Squelch)

## 2.2 USB PHY Layer

The USB PHY layer handles the low-level USB protocol and signaling. This includes features such as analog buffers, receiver detection, data serialization and de-serialization, 8b/10b encoding and decoding, 128b/132b encoding and decoding (10 GT/s), and elastic buffers. The primary focus of this block is to shift the clock domain of the data from the USB rate to one that is compatible with the general logic in the ASIC.

Some key features of the USB PHY are:

- Standard PHY interface that enables multiple IP sources to the USB link layer and provides a target interface for USB PHY vendors
- Support for 5.0 GT/s and/or 10 GT/s serial data transmission rate
- Utilizes 8-bit, 16-bit or 32-bit parallel interfaces to transmit and receive USB data
- Allowing the integration of high-speed components into a single functional block as seen in the device designer
- Data and clock recovery from serial stream on the USB bus
- Register holding to stage the Tx and Rx data
- 8b/10b encoding and decoding, and error indication
- 128b/132b encoding and decoding and error indication
- Receiver detection
- Low Frequency Periodic Signaling (LFPS)

Reference Number: 643108, Revision: 7.1

21