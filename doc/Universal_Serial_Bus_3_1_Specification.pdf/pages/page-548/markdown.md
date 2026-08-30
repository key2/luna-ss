Universal Serial Bus 3.1 Specification, Revision 1.0

## 10.16 Requests

### 10.16.1 Standard Requests

Hubs have tighter constraints on request processing timing than specified in Section 9.2.6 for standard devices because they are crucial to the “time to availability” of all devices attached to the USB. The worst case request timing requirements are listed below (they apply to both Standard and Hub Class requests):

- Completion time for requests with no data stage: 50 ms
- Completion times for standard requests with data stage(s):
  Time from setup packet to first data stage: 50 ms
  Time between each subsequent data stage: 50 ms
  Time between last data stage and status stage: 50 ms

Because hubs play such a crucial role in bus enumeration, it is recommended that hubs average response times be less than 5 ms for all requests.

Table 10-6 outlines the various standard device requests.

Table 10-6. Hub Responses to Standard Device Requests

[tbl-228.md](tbl-228.md)

A hub is required to accept all “Standard” requests without error. A hub shall not respond with a request error to a well-formed SET_ISOCH_DELAY request. A hub is not required to retain or process the delay value. Optional requests that are not implemented shall return a STALL in the Data stage or Status stage of the request.

10-70