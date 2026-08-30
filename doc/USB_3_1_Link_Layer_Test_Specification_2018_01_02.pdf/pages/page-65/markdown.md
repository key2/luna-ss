Chapter 5: Test Descriptions

1/17/2018

G. Repetition of four skip ordered sets followed by 1,416 symbols (word aligned)
H. Repetition of four skip ordered sets followed by 1,415 symbols (word misaligned)

Combinations to be tested for Gen 2 PUT:

For Each SKP Symbol count x in X:

A. Repeat Sequence 01 with all SKP OSs containing x SKP symbols.
B. Repeat Sequence 01 with all SKP OSs containing x SKP symbols, with one SKP symbol including a bit error.
C. Repeat Sequence 02 with all SKP OSs containing x SKP symbols.
D. Repeat Sequence 02 with all SKP OSs containing x SKP symbols, with one SKP symbol including a bit error.

Received SKP symbol counts in Gen 2 PUT:

X = {4,8,12,16,20,24,28,32,36} if PUT includes no captive re-timer
X = {8,12,16,20,24,28,32} if PUT includes one captive re-timer

Sequences of Repetition for Gen 2 PUT:

Sequence 01:

a. Forty (40) blocks
b. One SKP OS

Sequence 02:

a. One hundred and nine (109) blocks
b. Two SKP OS
c. One block
d. One SKP OS

# Covered Assertions

(No Physical Layer assertions defined)

# Overview of Test Steps

1. Do steps 1 to 4 of the Link Initialization Sequence.
2. The LVS will keep the link active by sending Link Pollings (LUP when it is configured as an Upstream Port or LDN when it is configured as a Downstream Port) for 50ms. Skips will be generated according to Combination A described above.
3. The test passes if the exchanges are successful, no timeout is detected, no recovery is entered, all packets are successfully received, all credits are restored and the link stays in U0 for at least 50ms.
4. Repeat the steps with the next combination listed above.

### TD.6.3 Elasticity Buffer Test

This test verifies that the PUT's elasticity buffer supports the required frequency range, from -5,300 to 300ppm.

57

USB 3.1 Link Layer Test Specification