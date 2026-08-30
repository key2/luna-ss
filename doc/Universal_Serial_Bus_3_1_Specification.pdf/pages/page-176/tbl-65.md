|  Symbol Number | Value | Description  |
| --- | --- | --- |
|  0 through 2*N-1 [N can be 0 through 18] | CCh | SKP Symbol Symbol 0 is the SKP Ordered Set Identifier Note: for an empty SKP OS, the first symbol will be a SKPEND.  |
|  2*N | 33h | SKPEND Symbol  |
|  2*N+1 | 00-FFh | (i) If prior block was a Data Block: Bit[7] = Even Data Parity Bit[6:0] = LFSR[22:16] (ii) Else: Bit[7] = ~LFSR[22] Bit[6:0] = LFSR[22:16]  |
|  2*N+2 | 00-FFh | (i) If LTSSM state is Polling.Compliance: Error_Status[7:0] (ii) Else LFSR[15:8]  |
|  2*N+3 | 00-FFh | (i) If LTSSM state is Polling.Compliance: ~Error_Status[7:0] (ii) Else LFSR[7:0]  |