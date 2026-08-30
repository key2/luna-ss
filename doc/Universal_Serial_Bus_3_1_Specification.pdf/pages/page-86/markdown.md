Universal Serial Bus 3.1 Specification, Revision 1.0

service interval. Note, if an endpoint has no isochronous data to transmit when accessed by the host, it shall send a zero length packet in response to the request for data.

The host may access an endpoint at any point during the appropriate service interval. The isochronous endpoint should not assume a fixed spacing between transaction attempts. The isochronous endpoint can assume only that it will receive a transaction attempt within the service interval bound. Errors may prevent the successful exchange of data within the service interval bound; however, since the packets in an isochronous transaction are not acknowledged, a host/device has no way of knowing which packets were not received successfully and hence will not retry packets.

### 4.4.8.3 Isochronous Transfer Data Sequences

Isochronous endpoints always transmit data packets starting with sequence number zero in each service interval. Each successive data packet transmitted in the same service interval is sent with the next higher sequence number. The sequence number shall roll over from thirty one to zero when transmitting the thirty second packet. Isochronous endpoints do not support retries and cannot respond with flow control responses.

### 4.4.8.4 Special Considerations for Isochronous Transfers

For a general overview of isochronous data movements over USB, USB clock model, clock synchronization, and the different types of USB-defined synchronization types and their specific requirements, refer to the USB 2.0 Specification, Section 5.12. The following section presents the information necessary to implement Enhanced SuperSpeed isochronous endpoints that need an explicit feedback isochronous endpoint.

#### 4.4.8.4.1 Explicit Feedback

An Enhanced SuperSpeed asynchronous isochronous sink endpoint must provide explicit feedback to the host by indicating accurately what its desired data rate ($F_f$) is, relative to the USB bus interval frequency. This allows the host to continuously adjust the number of samples sent to the sink so that neither underflow, nor overflow, of the data buffer occurs. Likewise, an Enhanced SuperSpeed adaptive source endpoint must receive explicit feedback from the host so that it can accurately generate the number of samples required by the host. Feedback endpoints can be specified as described in Section 9.6.6 for the bmAttributes field of the endpoint descriptor.

To generate the desired data rate $F_f$, the device must measure its actual sampling rate $F_s$, referenced to the USB notion of time, i.e., the USB bus interval frequency. This specification requires the data rate $F_f$ to be resolved to better than one sample per second (1 Hz) in order to allow a high-quality source rate to be created and to tolerate delays and errors in the feedback loop. To achieve this accuracy, the measurement time $T_{meas}$ must be at least 1 second. Therefore:

$$T_{meas} = 2^K$$

where $T_{meas}$ is now expressed in USB bus intervals and $K \ge 13$ for Enhanced SuperSpeed devices (125 $\mu$s bus intervals). However, in most devices, the actual sampling rate $F_s$ is derived from a master clock $F_m$ through a binary divider. Therefore:

$$F_m = F_s * 2^P$$

where $P$ is a positive integer (including 0 if no higher-frequency master clock is available). The measurement time $T_{meas}$ can now be decreased by measuring $F_m$ instead of $F_s$ and:

4-16