Revision 1.1
June 2022

- 365 -

Universal Serial Bus 3.2
Specification

[tbl-200.md](tbl-200.md)

The bmAttributes field provides information about the endpoint's Transfer Type (bits 1..0) and Synchronization Type (bits 3..2). For interrupt endpoints, the Usage Type bits (bits 5..4) indicate whether the endpoint is used for infrequent notifications that can tolerate varying latencies (bits 5..4 = 01b), or if it regularly transfers data in consecutive service intervals or is dependent on bounded latencies (bits 5..4 = 00b). For example, a hub's interrupt endpoint

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.