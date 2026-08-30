Hub, Host Downstream Port, and Device Upstream Port Specification

Table 10-10. Hub Status Field, wHubStatus

[tbl-236.md](tbl-236.md)

There are no defined feature selector values for these status bits and they can neither be set nor cleared by the USB system software.

Table 10-11. Hub Change Field, wHubChange

[tbl-237.md](tbl-237.md)

Hubs may allow setting of these change bits with SetHubFeature() requests in order to support diagnostics. If the hub does not support setting of these bits, it shall either treat the SetHubFeature() request as a Request Error or as a functional no-operation. When set, these bits may be cleared by a ClearHubFeature() request. A request to set a feature that is already set or to clear a feature that is already clear has no effect and the hub shall treat this as a functional no-operation.

10-75