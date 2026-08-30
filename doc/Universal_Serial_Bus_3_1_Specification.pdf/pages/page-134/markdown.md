Universal Serial Bus 3.1 Specification, Revision 1.0

### 5.6.1.1.2 Intra-Pair Skew

The intra-pair skew for the SDP pairs is recommended to be less than 15 ps/m. It should be measured with a Time Domain Transmission (TDT) in a differential mode using a 200 ps (10%-90%) rise time with a crossing at 50% of the input voltage.

### 5.6.1.1.3 Differential Insertion Loss

Cable loss depends on wire gauges, plating and dielectric materials. Table 5-13 and Table 5-14 show examples of average differential insertion loss for the SDP pairs for Enhanced SuperSpeed Gen 2 speed. To meet the cable assembly differential insertion loss target, support of the Gen 2 speed requires better performance from the raw cable than required for support of the Gen 1 speed.

Table 5-13. SDP Differential Insertion Loss Examples for Gen 2 speed

[tbl-45.md](tbl-45.md)

Table 5-14. SDP Differential Insertion Loss Examples for Gen 2 speed with Coaxial Construction

[tbl-46.md](tbl-46.md)

### 5.6.1.2 Mated Connector Impedance

SuperSpeed signal routing on the PCB should minimize the stub length and minimize impedance discontinuities in the signal path. It is recommended that the SuperSpeed signals be routed on the opposite side of the PCB from the side the lead is inserted for through-hole implementations. It is recommended that the SuperSpeed signals be routed on the same side of the PCB as the solder pads for SMT implementations.

For Enhanced SuperSpeed Gen 2 speed applications, electrical optimization is required to achieve the best performance. The PCB stack up, lead geometry, and solder pad geometry should be modeled in three dimensions. Example ground voids under pads shown in Figure 5-20 are based on pad geometry, mounting type, and PCB stack up.

5-46