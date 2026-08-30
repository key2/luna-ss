Revision 1.1
June 2022

- 61 -

Universal Serial Bus 3.2
Specification

c. Symbols 14 and 15 bypass the scrambler and the scrambler advances if being used for DC balance. If they are not being used for DC balance then they are scrambled.
3. SKP Ordered Sets bypass and do not advance the scrambler.
4. SDS Ordered Sets bypass the scrambler, but the scrambler advances.
5. All symbols of a SYNC Ordered Set bypass the scrambler. The scrambling LFSR is initialized after the last Symbol of a SYNC Ordered Set is transmitted. The descrambling LFSR is initialized after the last Symbol of a SYNC Ordered Set is received.
6. Receivers evaluate Symbol 0 of Control Blocks to determine whether to advance their LFSR. If Symbol 0 of the Block is SKP or SKPEND then the LFSR is not advanced for any Symbol of that Block. Otherwise, the LFSR is advanced for all Symbols of the Block.
7. All 16 Symbols of a Data Block are scrambled and advance the scrambler.
8. For Symbols that need to be scrambled the least significant bit is scrambled first and the most significant bit is scrambled last.
9. The seed value for the LFSR is 1D BFBCh.
10. Every 16384 TSEQ sets a SYNC Ordered Set shall be inserted to reset scrambler and to aid in block alignment.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.