Revision 1.1
June 2022

- 479 -

Universal Serial Bus 3.2
Specification

## B Symbol Scrambling

### B.1 Data Scrambling

The following subroutines encode and decode an 8-bit value contained in "inbyte" with the LFSR. This is presented as one example only; there are many ways to obtain the proper output. This example demonstrates how to advance the LFSR eight times in one operation and how to XOR the data in one operation. Many other implementations are possible but they must all produce the same output as that shown here.

The following algorithm uses the "C" programming language conventions, where "<<" and ">>" represent the shift left and shift right operators, ">" is the compare greater than operator, and "^" is the exclusive or operator, and "&" is the logical "AND" operator.

/*
this routine implements the serial descrambling algorithm in parallel form
for the LSFR polynomial: x^16+x^5+x^4+x^3+1
this advances the LSFR 8 bits every time it is called
this requires fewer than 25 xor gates to implement (with a static register)

The XOR required to advance 8 bits/clock is:
bit 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15
8 9 10 11 12 13 14 15 0 1 2 3 4 5 6 7
8 9 10 11 12 13 14 15
8 9 10 11 12 13 14 15
8 9 10 11 12 13 14 15

The serial data is just the reverse of the upper byte:
bit 0 1 2 3 4 5 6 7
15 14 13 12 11 10 9 8
*/

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.