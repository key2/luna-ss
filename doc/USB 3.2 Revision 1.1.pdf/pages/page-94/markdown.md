Revision 1.1
June 2022

- 63 -

Universal Serial Bus 3.2
Specification

For Gen 2x2 operation, both lanes use the LFSR in Figure 6-12. Details of scrambling for Gen 2x2 mode are contained in Section 6.13.5.

#### 6.3.2.4 128b/132b Decode Errors

The Block Header decode error rules are as follows:

1. Single bit errors in the Block Header shall be reported to the link layer and corrected.
2. Double bit errors in the Block Header shall be reported to the link layer.

#### 6.3.3 Special Symbols for Framing and Link Management

The 8b/10b encoding scheme provides Special Symbols that are distinct from the Data Symbols used to represent characters. These Special Symbols are used for various Link Management mechanisms described later. Table 6-2 lists the Special Symbols used and provides a brief description for each. Special Symbols shall follow the proper 8b/10b disparity rules. The compliance tests are defined in the USB SuperSpeed Compliance Methodology white paper. For Gen 2 operation the block header identifies whether the following 16 symbols have special meaning or if they represent data. In Gen 2 operation a receiver shall always perform single bit error correction on the special symbols when they are part of a control block. For Gen 1 and Gen 2 the following special symbols are defined.

Table 6-2. Special Symbols

[tbl-36.md](tbl-36.md)

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.