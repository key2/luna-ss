Universal Serial Bus 3.1 Specification

Table 7-2. CRC-32 Mapping

[tbl-88.md](tbl-88.md)

For SuperSpeed USB, any premature termination of a DPP shall end with a DPPABORT ordered set.

For SuperSpeedPlus USB, a port shall always preserve the DPP boundary by completing the DPP transmission meeting the length field specification defined in its associated DPH except for the following conditions.

1. A downstream port is directed to issue a Warm Reset.

Note: An upstream port, before declaring the detection of Warm Reset, may already enter Recovery.

2. A port is directed to enter Recovery.

Note: A port may also complete the DPP transmission under any of the above conditions.

In all other cases, a port in SuperSpeedPlus operation shall perform one of the following.

- It shall append DPPEND OS upon completing the transmission of DPP.
- In the case of a nullified DPP, it shall append DPPABORT OS immediately after its DPH.

7-10