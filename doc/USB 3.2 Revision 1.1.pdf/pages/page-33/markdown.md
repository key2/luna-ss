Revision 1.1
June 2022

- 2 -

Universal Serial Bus 3.2
Specification

### 1.3 Scope of the Document

The specification is primarily targeted at peripheral developers and platform/adapter developers, but provides valuable information for platform operating system/BIOS/device driver, adapter IHVs/ISVs, and system OEMs. This specification can be used for developing new products and associated software.

Product developers using this specification are expected to know and understand the USB 2.0 Specification. Specifically, USB 3.x devices must implement device framework commands and descriptors as defined in the USB 2.0 Specification. Devices operating at the 10 Gbps (Gen 2) speed must implement the SuperSpeedPlus enhancements defined in this version of the specification.

### 1.4 USB Product Compliance

Adopters of the USB 3.x specification have signed the USB 3.0 Adopters Agreement, which provides them access to a royalty-free reasonable and nondiscriminatory (RAND) license from the Promoters and other Adopters to certain intellectual property contained in products that are compliant with the USB 3.2 specification. Adopters can demonstrate compliance with the specification through the testing program as defined by the USB Implementers Forum (USB-IF). Products that demonstrate compliance with the specification will be granted certain rights to use the USB-IF logos as defined in the logo license.

Starting with USB 3.1, product compliance requirements were tightened up to prohibit non-certified cables and connectors. Use of any registered icons or logos on products, documentation or packaging will require a license and license requirements will include passing specific product certification.

### 1.5 Document Organization

Chapters 1 through 4 provide an overview for all readers, while Chapters 5 through 11 contain detailed technical information defining USB 3.2.

Readers should contact operating system vendors for operating system bindings specific to USB 3.2.

### 1.6 Design Goals

USB 3.1 was and USB 3.2 is an evolutionary step to increase the bandwidth. The goal remains the same; end users view these the same as they viewed USB 2.0 and USB 3.0, just higher in performance. Several key design areas to meet this goal are listed below:

- Preserve the USB model of smart host and simple device.
- Leverage the existing USB infrastructure. There are a vast number of USB products in use today. A large part of their success can be traced to the existence of stable software interfaces, easily developed software device drivers, and a number of generic standard device class drivers (HID, mass storage, audio, etc.). Enhanced SuperSpeed USB devices are designed to keep this software infrastructure intact so that developers of peripherals can continue to use the same interfaces and leverage all of their existing development work.
- Significantly improve power management. Reduce the active power when sending data and reduce idle power by providing a richer set of power management mechanisms to allow devices to drive the bus into lower power states.
- Ease of use has always been and remains a key design goal for all varieties of USB.
- Preserve the investment. There are a large number of PCs in use that support only USB 2.0. There are a larger number of USB 2.0 peripherals in use. Retaining

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.