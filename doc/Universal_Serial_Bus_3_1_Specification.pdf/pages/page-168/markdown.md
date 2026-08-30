Universal Serial Bus 3.1 Specification, Revision 1.0

### 6.3.2.4 128b/132b Decode Errors

The Block Header decode error rules are as follows:

1. Single bit errors in the Block Header shall be reported to the link layer and corrected.
2. Double bit errors in the Block Header shall be reported to the link layer.

### 6.3.3 Special Symbols for Framing and Link Management

The 8b/10b encoding scheme provides Special Symbols that are distinct from the Data Symbols used to represent characters. These Special Symbols are used for various Link Management mechanisms described later. Table 6-1 lists the Special Symbols used and provides a brief description for each. Special Symbols shall follow the proper 8b/10b disparity rules. The compliance tests are defined in the USB SuperSpeed Compliance Methodology white paper. For Gen 2 operation the block header identifies whether the following 16 symbols have special meaning or if they represent data. In Gen 2 operation a receiver shall always perform single bit error correction on the special symbols when they are part of a control block. For Gen 1 and Gen 2 the following special symbols are defined.

Table 6-1. Special Symbols

[tbl-53.md](tbl-53.md)

6-12