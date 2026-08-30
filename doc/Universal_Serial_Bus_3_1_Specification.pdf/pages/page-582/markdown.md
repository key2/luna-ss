Universal Serial Bus 3.1 Specification, Revision 1.0

### 11.4.4.2 Dynamic Detach

When a device is detached from the network with power flowing in the cable, the inductance of the cable will cause a large flyback voltage to occur on the open end of the device cable. This flyback voltage is not destructive. Proper bypass measures on the hub ports will suppress any coupled noise. This will require some low capacitance, very low inductance bypass capacitors on each hub port connector. The flyback voltage and the noise it creates are also moderated by the bypass capacitance on the device end of the cable. Also, there must be some minimum capacitance on the device end of the cable to ensure that the inductive flyback on the open end of the cable does not cause the voltage on the device end to reverse polarity. A minimum of 1.0 μF is recommended for bypass across VBUS.

### 11.4.5 VBUS Electrical Characteristics

Table 11-2. DC Electrical Characteristics

[tbl-256.md](tbl-256.md)

### 11.4.6 Powered-B Connector

The Powered-B connector was defined by USB 3.0 has been deprecated.

11-10