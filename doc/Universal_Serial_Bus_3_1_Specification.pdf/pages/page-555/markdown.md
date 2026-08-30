Hub, Host Downstream Port, and Device Upstream Port Specification

Table 10-12. Port Status Type Codes

[tbl-240.md](tbl-240.md)

It is a Request Error if the Port Status Type equals EXT_PORT_STATUS and the hub that does not define a SuperSpeedPlus USB Capability descriptor, or if the Port Status Type equals a reserved value, or if wValue or wLength are other than as specified in Table 10-7, or if wIndex specifies a port that does not exist.

If the hub is not configured, the behavior of the hub in response to this request is undefined.

$^{1}$ Refer to the USB Power Delivery Specification Revision 1.0

10-77