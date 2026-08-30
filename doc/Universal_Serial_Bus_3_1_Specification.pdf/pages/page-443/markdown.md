Device Framework

entry. The U2 Enable field can be modified by the SetFeature() and ClearFeature() requests using the U2_ENABLE feature selector. This field is reset to zero when the device is reset.

The LTM Enable field indicates whether the device is currently enabled to send Latency Tolerance Messages. If D4 is set to zero, the device is disabled from sending Latency Tolerance Messages, otherwise; it is enabled to send Latency Tolerance Messages. The LTM Enable field can be modified by the SetFeature() and ClearFeature() requests using the LTM_ENABLE feature selector. This field is reset to zero when the device is reset.

A GetStatus() request to the first interface in a function returns the information shown in Figure 9-5.

[tbl-161.md](tbl-161.md)

U-084

Figure 9-5. Information Returned by a Standard GetStatus() Request to an Interface

The status fields defined by Figure 9-5 are returned by a STANDARD_STATUS type request to an Interface recipient.

The Function Remote Wake Capable field indicates whether the function supports remote wake up. The Function Remote Wakeup field indicates whether the function is currently enabled to request remote wakeup. The default mode for functions that support function remote wakeup is disabled. If D1 is reset to zero, the ability of the function to signal remote wakeup is disabled. If D1 is set to one, the ability of the function to signal remote wakeup is enabled. The Function Remote Wakeup field can be modified by the SetFeature() requests using the FUNCTION_SUSPEND feature selector. This Function Remote Wakeup field is reset to zero when the function is reset.

A GetStatus() request to any other interface in a function shall return all zeros.

A GetStatus() request to an endpoint returns the information shown in Figure 9-6.

[tbl-162.md](tbl-162.md)

U-085

Figure 9-6. Information Returned by a Standard GetStatus() Request to an Endpoint

The status fields defined by Figure 9-6 are returned by a STANDARD_STATUS type request to an Endpoint recipient.

9-25