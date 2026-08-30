Hub, Host Downstream Port, and Device Upstream Port Specification

### 10.16.2.1 Clear Hub Feature

This request resets a value reported in the hub status.

[tbl-232.md](tbl-232.md)

Clearing a feature disables that feature; refer to Table 10-9 for the feature selector definitions that apply to the hub as a recipient. If the feature selector is associated with a status change, clearing that status change acknowledges the change. This request format is used to clear either the C_HUB_LOCAL_POWER or C_HUB_OVER_CURRENT features.

It is a Request Error if wValue is not a feature selector listed in Table 10-9 or if wIndex or wLength are not as specified above.

If the hub is not configured, the hub's response to this request is undefined.

### 10.16.2.2 Clear Port Feature

This request resets a value reported in the port status.

[tbl-233.md](tbl-233.md)

The port number shall be a valid port number for that hub, greater than zero. The port field is located in bits 7..0 of the wIndex field.

Clearing a feature disables that feature or starts a process associated with the feature; refer to Table 10-9 for the feature selector definitions. If the feature selector is associated with a status change, clearing that status change acknowledges the change. This request format is used to clear the following features:

- PORT_POWER
- C_PORT_CONNECTION
- C_PORT_RESET
- C_PORT_OVER_CURRENT
- C_PORT_LINK_STATE
- C_PORT_CONFIG_ERROR
- C_BH_PORT_RESET
- FORCE_LINKPM_ACCEPT

Clearing the PORT_POWER feature causes the port to be placed in the DSPORT-Powered-off-reset state and may, subject to the constraints due to the hub's method of power switching, result in power being removed from the port. When in the DSPORT-Powered-off or the DSPORT-Powered-off-detect or the DSPORT-Powered-off-reset state, the only requests that are valid when this port is the recipient are Get Port Status (refer to Section 10.16.2.6) and Set Port Feature (PORT_POWER) (refer to Section 10.16.2.10).

Clearing the FORCE_LINKPM_ACCEPT feature causes the port to de-assert the Force_LinkPM_Accept bit in Set Link Function LMPs. If the Force_LinkPM_Accept bit is not asserted on the port, the hub shall treat this request as a functional no-operation.

It is a Request Error if wValue is not a feature selector listed in Table 10-9, if wIndex specifies a port that does not exist, or if wLength is not as specified above. It is not an error for this request to try to clear a feature that is already cleared (the hub shall treat this as a functional no-operation).

10-73