|  Compliance Pattern | Value | Description  |
| --- | --- | --- |
|  CP0 | D0.0 scrambled | A pseudo-random data pattern that is exactly the same as logical idle (refer to Chapter 7) but does not include SKP sequences.  |
|  CP1 | D10.2 | Nyquist frequency  |
|  CP2 | D24.3 | Nyquist/2  |
|  CP3 | K28.5 | COM pattern  |
|  CP4 | LFPS | The low frequency periodic signaling pattern  |
|  CP5 | K28.7 | With de-emphasis  |
|  CP6 | K28.7 | Without de-emphasis  |
|  CP7 | 50-250 1's and 0's | With de-emphasis. Repeating 50-250 1's and then 50-250 0's.  |
|  CP8 | 50-250 1's and 0's | With without de-emphasis. Repeating 50-250 1's and then 50-250 0's.  |
|  CP9 |  | Pseudo-random data pattern (see section 6.4.4.1)  |
|  CP10 | AAh | Nyquist pattern at 10Gb/s. This is not 128b132b encoded.  |
|  CP11 | CCh | Nyquist/2 at 10Gb/s. This is not 128b132b encoded.  |
|  CP12 | LFSR15 | Uncoded LFSR15 for PHY level testing and fault isolation. This is not 128b132b encoded.  |