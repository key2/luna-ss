Universal Serial Bus 3.1 Specification, Revision 1.0

### 5.3 Connector Mating Interfaces

This section defines the connector mating interfaces, including the connector interface drawings, pin assignments, and descriptions.

### 5.3.1 USB 3.1 Standard-A Connector

#### 5.3.1.1 Interface Definition

Figure 5-1 and Figure 5-2 show the USB 3.1 Standard-A receptacle and required ground spring mating areas, respectively. Figure 5-4 shows the Standard-A plug interface dimensions for USB 3.1. Only the dimensions that govern the mating interoperability are specified. All REF dimensions are informative.

The Universal Serial Bus Power Delivery Specification defines the mechanical and electrical requirements for the Insertion Detect feature to support cold socket capability. It may be implemented in a Standard-A receptacle or a PD Standard-A receptacle. Implementation is vendor-specific. The Insertion Detect feature shall be implemented for cold socket Standard-A applications and is optional for all other Standard-A implementations. See the Universal Serial Bus Power Delivery Specification for complete Insertion Detect requirements. Example connector configurations including Insertion Detect features are shown in Figure 5-3.

Although the USB 3.1 Standard-A connector has basically the same form factor as the USB 2.0 Standard-A connector, it has significant differences inside. Below are the key features and design areas that need attention:

- In addition to the Vbus, D-, D+, and GND pins that are required for USB 2.0, the USB 3.1 Standard-A connector includes five more pins: two differential signal pairs plus one ground (GND_DRAIN). The two added differential signal pairs are for SuperSpeed data transfer, supporting dual simplex SuperSpeed signaling. The added GND_DRAIN pin is for drain wire termination and managing EMI, RFI, and signal integrity.
- The contact areas of the five SuperSpeed pins are located towards the front of the receptacle as blades, while the four USB 2.0 pins towards the back of the receptacle as beams or springs. Accordingly, in the plug, the SuperSpeed contacts are beams located behind the USB 2.0 blades. In other words, the USB 3.1 Standard-A connector has a two-tier contact system.
- The tiered-contact approach within the Standard-A connector form factor results in less contact area as compared to the USB 2.0 Standard-A connector. The connector interface dimensions take into consideration contact mating requirements between the USB 3.1 Standard-A receptacle and USB 3.1 Standard-A plug, the USB 3.1 Standard-A receptacle and USB 2.0 Standard-A plugs, and the USB 2.0 Standard-A receptacles and USB 3.1 Standard-A plug.
- The connector interface definition avoids shorting between the SuperSpeed and USB 2.0 pins during insertion when plugging a USB 2.0 Standard-A plug into a USB 3.1 Standard-A receptacle or a USB 3.1 Standard-A plug into a USB 2.0 Standard-A receptacle.
- There may be some increase in the USB 3.1 Standard-A receptacle connector depth (into a system board) to support the two-tiered-contacts as compared to the USB 2.0 Standard-A receptacle.
- Drawings for stacked USB 3.1 Standard-A receptacles are not shown in this specification. They are allowed as long as they meet all the electrical and mechanical requirements defined in this specification. When designing a stacked USB 3.1 Standard-A receptacle, efforts need to be

5-4