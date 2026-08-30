Chapter 5: Test Descriptions

1/17/2018

### TD.7.5 Header Packet Framing Robustness Test

This test verifies that the PUT does not invalidate header packets having one symbol error in the HPSTART framing. The combinations to be tested:

A. ERR SHP SHP EPF
B. SHP ERR SHP EPF
C. SHP SHP ERR EPF
D. SHP SHP SHP ERR

The Port Configuration transaction will be used for this purpose.

#### Covered Assertions

7.2.4.1.4#1

#### Overview of Test Steps

1. Perform the Link Initialization Sequence, but transmit all Header Packets with an error in the first HPSTART symbol.
2. The test passes if the Link Initialization Sequence passes.
3. Repeat the above steps with an error in the second, third, and fourth HPSTART symbols, as shown above.

### TD.7.6 Data Payload Packet Framing Robustness Test

This test verifies that the PUT does not invalidate data payload packets having a single character framing error in DPPSTART and DPPEND. The combinations to be tested:

A. ERR SDP SDP EPF
B. SDP ERR SDP EPF
C. SDP SDP ERR EPF
D. SDP SDP SDP ERR
E. ERR END END EPF
F. END ERR END EPF
G. END END ERR EPF
H. END END END ERR

When the LVS is a Downstream Port, it will place framing errors on Setup DP Packets.

When the LVS is an Upstream Port, it will reply to the GetDeviceDescriptor request with a DPP containing framing errors.

If the DUT is a Gen 1 device, the LVS also verifies that the PUT can handle Gen2 Transaction Packets in which several Gen1 Reserved bits are in use. The verification includes various configurations in the TPS and TT fields of the Gen2 Transaction Packet.

#### Covered Assertions

7.2.4.1.6#1,2

7.3.4.1#3

66

USB 3.1 Link Layer Test Specification