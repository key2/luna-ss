Revision 1.1  
June 2022

- 97 -

Universal Serial Bus 3.2  
Specification

**Table 6-24. BRST**

[tbl-64.md](tbl-64.md)

**Table 6-25. BDAT**

[tbl-65.md](tbl-65.md)

**Table 6-26. BERC**

[tbl-66.md](tbl-66.md)

**Table 6-27. BCNT**

[tbl-67.md](tbl-67.md)

### 6.8.5 Normative Receiver Tolerance Compliance Test

The receiver tolerance test is tested using the appropriate compliance reference channel for Gen 1 or Gen 2 operation depending upon the rate being tested. A pattern generator shall send the rate appropriate compliance test pattern with added jitter through the compliance reference channels to the receiver. The receiver shall loop back the data and any difference in the pattern sent from the pattern generator and returned will be an error. When running the compliance tests, the receiver shall be put into loopback mode.

Additional details on the receiver compliance test are contained in the reference document, *USB SuperSpeed Compliance Methodology*.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.