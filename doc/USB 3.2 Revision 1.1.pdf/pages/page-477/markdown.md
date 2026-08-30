Revision 1.1
June 2022

- 446 -

Universal Serial Bus 3.2
Specification

[tbl-250.md](tbl-250.md)

### PORT_CONNECTION

This bit is set to one when the port in the DSPORT.Enabled state. In DSPORT.Resetting or DSPORT.Error state it maintains the value from prior state.

SetPortFeature(PORT_CONNECTION) and ClearPortFeature(PORT_CONNECTION) requests shall not be used by the USB system software and shall be treated as no-operation requests by hubs.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.