intel®

## 2.3 USB4 PHY Layer

The USB4 PHY Layer handles the low level USB4 protocol and signaling. This includes features such as data serialization and de-serialization, analog buffers, and receiver detection.

Some key features of the USB4 PHY:

- A standard PHY interface enables multiple IP sources for USB4 Link Layer and provides a target interface for USB4 PHY vendors
- Supports 10 GT/s and/or 20 GT/s serial data transmission rate in combination with a 40-bit parallel interface to transmit and receive USB4 data using PAM2 signaling
- Supports 40 GT/s serial data transmission rate in combination with a 56-bit parallel interface to transmit and receive USB4 data using PAM3 signaling
- Data and clock recovery from serial stream on the USB4 bus
- Holding registers to stage transmit and receive data
- Low Frequency Periodic Signaling (LFPS)

## 2.4 SATA PHY Layer

The SATA PHY layer handles the low-level SATA protocol and signaling. This includes features such as analog buffers, data serialization and deserialization, 8b/10b encoding and decoding, and elastic buffers. The primary focus of this block is to shift the clock domain of the data from the SATA rate to one that is compatible with the general logic in the ASIC.

Some key features of the SATA PHY are:

- A standard PHY interface that enables multiple IP sources for SATA controllers and provides a target interface for SATA PHY vendors
- Support of 1.5 GT/s only, or 1.5 GT/s and 3.0 GT/s, or 1.5 GT/s, or 3.0 GT/s, and 6.0 GT/s serial data transmission rate
- Utilizes 8-bit, 16-bit, or 32-bit parallel interface to transmit and receive SATA data
- Allows integration of high-speed components into a single functional block as seen in the device designer
- Data and clock recovery from serial stream on the SATA bus
- Holding registers to stage transmit and receive data
- 8b/10b encode/decode and error indication
- COMINIT and COMRESET transmission and reception

## 2.5 DisplayPort PHY Layer

The DisplayPort PHY layer handles the low-level DisplayPort protocol and signaling. This includes features such as data serialization and de-serialization, and analog buffers.

Some key features of the DisplayPort PHY include the following:

- A standard PHY interface that enables multiple IP sources for the DisplayPort link layer and provides a target interface for the DisplayPort PHY vendors

22

Reference Number: 643108, Revision: 7.1