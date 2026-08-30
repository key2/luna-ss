Revision 1.1
June 2022

- 154 -

Universal Serial Bus 3.2
Specification

### 7.3.11 Gen 1 8b/10b Errors

There are two types of errors when a receiver decodes 8b/10b symbols. One is a disparity error that is declared when the running disparity of the received 8b/10b symbols is not +2, or 0, or -2. The other is a decode error when an unrecognized 8b/10b symbol is received.

Upon receiving notification of an 8b/10b error:

- A port may optionally do the following:
  1. If the link is receiving a header packet, it shall send LBAD.
  2. If the link is receiving a link command, it shall ignore the link command.
  3. If the link is receiving a DPP, it shall drop the DPP.
- The Link Error Count shall remain unchanged.

### 7.3.12 Gen 2x1 Block Header Errors

There are two types of block header errors, a correctable single bit block header error, and a detectable but not correctable two-bit block header error.

- Upon detecting a single-bit block header error, the PHY shall correct it and report the error event to the link layer. The Soft Error Count shall be incremented by one.
- Upon detecting two-bit block header error, the PHY shall report the error event to the link layer. The port shall transition to Recovery.

### 7.3.13 Gen 2x2 Block Header Errors

Refer to Section 6.13.4 regarding data striping in Gen 2x2 operation. BH0 is the block header transmitted on lane 0 and BH1 is the block header transmitted on lane 1. Since BH0 and BH1 are identical, further enhancement of the block header error detection and correction is possible if the PHY associates BH0 and BH1. The implementation of this association is optional.

- The PHY shall declare the reception of valid block headers if either of the following conditions is true.
  - BH0 and BH1 are valid and identical. If single-bit error correction is performed, it shall report the error event to the link layer. The port shall increment the Soft Error Count accordingly by one.
  - If the PHY associates BH0 and BH1, and if one block header is valid and the other block header is invalid. If single-bit error correction is performed, it shall report the error event accordingly to the link layer. The port shall increment the Soft Error Count by one.
- The PHY shall declare the reception of invalid block headers if either of the following conditions is true.
  - BH0 and BH1 are both invalid. The PHY shall report the error event to the link layer. The port shall transition to Recovery.
  - BH0 and BH1 are both valid but not identical. The PHY shall report the error event to the link layer. The port shall transition to Recovery.
  - If the PHY does not associate between BH0 and BH1, and if one of the block headers is invalid. The PHY shall report the error event to the link layer. The port shall transition to Recovery.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.