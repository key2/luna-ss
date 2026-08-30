Revision 1.1
June 2022

- 137 -

Universal Serial Bus 3.2
Specification

- Upon completion of a header packet processing, a port shall restore a Local Rx Header Buffer Credit by:

1. Sending a single LCRD_x
2. Advancing the Credit index alphabetically (or roll over to A if the Header Buffer Credit index of D is reached) and
3. Incrementing the Local Rx Header Buffer Credit Count by one.

Note: The LCRD_x index is used to ensure Rx Header Buffer Credits are sent in an alphabetical order such that missing of an LCRD_x can be detected.

### 7.2.4.1.8 SuperSpeedPlus Type 1/Type 2 Rx Buffer Credit

Each port shall have the following two classes of Rx Buffer Credits.

- A port shall have four or seven Type 1 Rx Buffer Credits for Type 1 traffic class in its receiver. This is referred to the Local Type 1 Rx Buffer Credit.
- A port shall have four or seven Type 2 Rx Buffer Credits for Type 2 traffic class in its receiver. This is referred to the Local Type 2 Rx Buffer Credit.

The operation rules of the Local Type 1 and Type 2 Rx Buffer Credits are the same. They each represent the number of Type 1 or Type 2 packets a port can accept and are managed by their respective Local Type 1 and Type 2 Rx Buffer Credit Count. The following descriptions refer to the Local Type 1/Type 2 Rx Buffer Credit management.

- A port shall consume one Local Type 1 or Type 2 Rx Buffer Credit if the respective Type 1 or Type 2 packet is "received properly". The Local Type 1/Type 2 Rx Buffer Credit Count shall be decremented by one.
- Upon completion of a Type 1 or Type 2 packet processing, and the respective Type 1 or Type 2 Rx Buffer is made available, a port shall restore accordingly a Local Type 1 or Type 2 Rx Buffer Credit by:

1. Sending a single LCRD1_x or LCRD2_x
2. Advancing the Credit index alphabetically (or roll over to A if the Rx Buffer Credit index of D (Gen 1x2 or Gen 2x1) or G (Gen 2x2) is reached) and
3. Incrementing the Local Type 1 or Type 2 Rx Buffer Credit Count by one.

### 7.2.4.1.9 Receiving Data Packet Payload

In Gen 1 operation, the processing of DPP shall adhere to the following rules:

- A DPP processing shall be started if the following two conditions are met:

1. A DPH is received properly.
2. A DPPSTART ordered set is received properly immediately after its DPH.

- The DPP processing shall be completed when a valid DPPEND ordered set is detected.

- The DPP processing shall be aborted when one of the following conditions is met:

1. A valid DPPABORT ordered set is detected.
2. A K-symbol that does not belong to a valid DPPEND or DPPABORT ordered set is detected before a valid DPPEND or DPPABORT ordered set. A port

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.