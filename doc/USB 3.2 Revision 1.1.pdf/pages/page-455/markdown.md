Revision 1.1  
June 2022

- 424 -

Universal Serial Bus 3.2  
Specification

Irrespective of how the hub was reset, the hub needs to propagate reset as described in Section 10.3.1.6 and not just transition those downstream ports to the default state.

### **10.12 Hub Port Power Control**

Self-powered hubs may have power switches that control delivery of power to downstream facing USB Standard-A ports but it is not required. A hub with power switches can switch power to all USB Standard-A ports as a group/gang, to each USB Standard-A port individually, or have an arbitrary number of gangs of one or more USB Standard-A ports. A hub shall have individual power switches for all USB Type-C ports.

A hub indicates whether or not it supports power switching by the setting of the Logical Power Switching Mode field in *wHubCharacteristics*. If a hub supports per-port power switching, then the power to a port is turned on or off as specified in Section 10.3.1.1. If a hub supports ganged power switching, then the power to all ports in a gang is turned on when power is required to be on for any port in the gang. The power to a gang is not turned off unless all ports in a gang are in a state that allows power to be removed as specified in Table 10-2. The power to a port (a USB Standard-A port or a USB Type-C port in an Attached State) is not turned on by a SetPortFeature(PORT_POWER) if both C_HUB_LOCAL_POWER and Local Power Source (in *wHubStatus*) are set to one at the time when the request is executed. A hub that supports power applications may keep power on at other times. Refer to Section 10.3.1.1 for more details on allowed behavior for a hub that supports power applications.

Although a self-powered hub is not required to implement power switching (except for all downstream USB Type-C ports), the hub shall support the Powered-off states for all ports.

For a hub with no power switches, *bPwrOn2PwrGood* shall be set to zero.

#### **10.12.1 Multiple Gangs (Only supported for downstream USB Standard-A ports)**

A hub may implement any number of power and/or over-current gangs. A hub that implements more than one over-current and/or power switching gang shall set both the Logical Power Switching Mode and the Over-current Reporting Mode to indicate that power switching and over-current reporting are on a per port basis (these fields are in *wHubCharacteristics*).

When an over-current condition occurs on an over-current protection device, the over-current is signaled on all ports that are protected by that device. When the over-current is signaled, all the ports in the group are placed in the DSPORT-Powered-off or the DSPORT-Powered-off-reset state, and the C_PORT_OVER_CURRENT field is set to one on all the ports. When port status is read from any port in the group, the PORT_OVER_CURRENT field will be set to one as long as the over-current condition exists. The C_PORT_OVER_CURRENT field shall be cleared in each port individually.

When multiple ports share a power switch, setting PORT_POWER on any port in the group will cause the power to all ports in the group to turn on. It will not, however, cause the other ports in that group to leave the DSPORT-Powered-off or the DSPORT-Powered-off-reset state. When all the ports in a group are in the DSPORT-Powered-off state or the hub is not configured, the power to the ports is turned off.

If a hub implements both power switching and over-current, it is not necessary for the over-current groups to be the same as the power switching groups.

If an over-current condition occurs and power switches are present, then all power switches associated with an over-current protection circuit shall be turned off. If multiple over-current protection devices are associated with a single power switch, then that switch will

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.