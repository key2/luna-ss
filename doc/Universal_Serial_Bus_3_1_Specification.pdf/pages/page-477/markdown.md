Device Framework

### 9.6.9 String

String descriptors are optional. As noted previously, if a device does not support string descriptors, all references to string descriptors within device, configuration, and interface descriptors shall be reset to zero.

String descriptors use UNICODE UTF16LE encodings as defined by The Unicode Standard, Worldwide Character Encoding, Version 5.0, The Unicode Consortium, Addison-Wesley Publishing Company, Reading, Massachusetts (http://www.unicode.org). The strings in a device may support multiple languages. When requesting a string descriptor, the requester specifies the desired language using a 16-bit language ID (LANGID) defined by the USB-IF. The list of currently defined USB LANGIDs can be found at http://www.usb.org/developers/docs.html. String index zero for all languages returns a string descriptor that contains an array of 2-byte LANGID codes supported by the device. Table 9-28 shows the LANGID code array. A device may omit all string descriptors. Devices that omit all string descriptors shall not return an array of LANGID codes.

The array of LANGID codes is not NULL-terminated. The size of the array (in bytes) is computed by subtracting two from the value of the first byte of the descriptor.

Table 9-28. String Descriptor Zero, Specifying Languages Supported by the Device

[tbl-198.md](tbl-198.md)

The UNICODE string descriptor (shown in Table 9-29) is not NULL-terminated. The string length is computed by subtracting two from the value of the first byte of the descriptor.

Table 9-29. UNICODE String Descriptor

[tbl-199.md](tbl-199.md)

9-59