Symbol Scrambling

// Now advance the LFSR 8 serial clocks
bit_out[0] = bit[8];
bit_out[1] = bit[9];
bit_out[2] = bit[10];
bit_out[3] = bit[11] ^ bit[8];
bit_out[4] = bit[12] ^ bit[9] ^ bit[8];
bit_out[5] = bit[13] ^ bit[10] ^ bit[9] ^ bit[8];
bit_out[6] = bit[14] ^ bit[11] ^ bit[10] ^ bit[9];
bit_out[7] = bit[15] ^ bit[12] ^ bit[11] ^ bit[10];
bit_out[8] = bit[0] ^ bit[13] ^ bit[12] ^ bit[11];
bit_out[9] = bit[1] ^ bit[14] ^ bit[13] ^ bit[12];
bit_out[10] = bit[2] ^ bit[15] ^ bit[14] ^ bit[13];
bit_out[11] = bit[3]    ^ bit[15] ^ bit[14];
bit_out[12] = bit[4]    ^ bit[15];
bit_out[13] = bit[5];
bit_out[14] = bit[6];
bit_out[15] = bit[7];
lfsr = 0;
for (i=0; i < 16; i++) // convert the LFSR back to an integer
    lfsr += (bit_out[i] << i);

outbyte = 0;
for (i=0; i<8; i++) // convert data back to an integer
    outbyte += (scrambit[i] << i);

return outbyte;
}

/* NOTE THAT THE DESCRAMBLE ROUTINE IS IDENTICAL TO THE SCRAMBLE ROUTINE
this routine implements the serial descrambling algorithm in parallel form
this advances the lfsr 8 bits every time it is called
this uses fewer than 25 xor gates to implement (with a static register)
The XOR tree is the same as the scrambling routine
*/

B-3