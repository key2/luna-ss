|  Symbol Number | Value | Description  |
| --- | --- | --- |
|  0 through 4*N-1 [N can be 0 through 9] | CCh | SKP Symbol Symbol 0 is the SKP Ordered Set Identifier  |
|  4*N | 33h | SKPEND Symbol  |
|  4*N+1 | 40-FFh | Bit[7] = ~LFSR[22] Bit[6:0] = LFSR[22:16]  |
|  4*N+2 | 00-FFh | LFSR[15:8]  |
|  4*N+3 | 00-FFh | LFSR[7:0]  |