Universal Serial Bus 3.1 Specification, Revision 1.0

- TSEQ Ordered Set
- SYNC Ordered Set
- SKP Ordered Set
- SDS Ordered Set

### 6.3.2.3 Data Scrambling for Gen 2 Operation

The scrambler used for Gen 2 operation is different than the scrambler used for Gen 1 operation.

The LFSR uses the following polynomial: G(X) = X²³ + X²¹ + X¹⁶ + X⁸ + X⁵ + X² + 1.

The scrambler has the following modes of operation:

1. The scrambler advances and is XORed with the data.
2. The scrambler advances and is bypassed (not XORed with the data).
3. The scrambler does not advance and is bypassed (not XORed with the data).

The scrambling rules are as follows:

1. The 4 bits of the Block Header bypass and do not advance the scrambler.
2. TS1, TS2 and TSEQ:
  a. Symbol 0 of a TS1, TS2, or TSEQ Ordered Set bypass and advances the scrambler.
  b. Symbols 1 to 13 are scrambled.
  c. Symbols 14 and 15 bypass the scrambler and the scrambler advances if being used for DC balance. If they are not being used for DC balance then they are scrambled.
3. SKP Ordered Sets bypass and do not advance the scrambler.
4. SDS Ordered Sets bypass the scrambler, but the scrambler advances.
5. All symbols of a SYNC Ordered Set bypass the scrambler. The scrambling LFSR is initialized after the last Symbol of a SYNC Ordered Set is transmitted. The descrambling LFSR is initialized after the last Symbol of a SYNC Ordered Set is received.
6. Receivers evaluate Symbol 0 of Control Blocks to determine whether to advance their LFSR. If Symbol 0 of the Block is SKP or SKPEND then the LFSR is not advanced for any Symbol of that Block. Otherwise, the LFSR is advanced for all Symbols of the Block.
7. All 16 Symbols of a Data Block are scrambled and advance the scrambler.
8. For Symbols that need to be scrambled the least significant bit is scrambled first and the most significant bit is scrambled last.
9. The seed value for the LFSR is 1D BFBCh.
10. Every 16384 TSEQ sets a SYNC Ordered Set shall be inserted to reset scrambler and to aid in block alignment.

Figure 6-11 depicts the LFSR for the scrambling polynomial.

6-10