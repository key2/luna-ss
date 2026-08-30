Revision 1.1  
June 2022

- 96 -

Universal Serial Bus 3.2  
Specification

### 6.8.4 Receiver Loopback

The entry and exit process for receiver loopback is described in Chapter 7.5.11.

Receiver loopback must be retimed. Direct connection from the Rx amplifier to the transmitter is not allowed for loopback mode. The receiver shall continue to process SKP Ordered Sets as appropriate. For Gen 1 operation, SKP symbols shall be consumed or inserted as required for proper clock tolerance compensation. For Gen 2 operation, the receiver can either add 4 SKPs, remove 4 SKPs or make no adjustment to the received SKP Ordered Set. The modified SKP Ordered Set shall meet the requirements specified in Section 6.4.3.2 (i.e. must contain between 4 and 36 SKPs followed by the SKPEND Symbol and 3 Symbols that proceed the SKPEND.) Over runs or under runs of the clock tolerance buffers will reset the buffers to the neutral position.

During loopback the receiver may process the Bit Error Rate Test (BERT) commands. The processing of BERT commands is optional for Gen 1 loopback. There are no BERT commands in Gen 2 operation.

Loopback shall occur in the 10-bit domain for Gen 1 operation and in the 132-bit domain for Gen 2 operation. No error correction is allowed. All symbols shall be transmitted as received with the exception of SKP and BERT commands.

#### 6.8.4.1 Loopback BERT for Gen 1 Operation

During loopback the receiver processes the BERT ordered sets BRST, BDAT, and BERC. These ordered sets are described in Table 6-24 through Table 6-27. BRST and BDAT are looped back as received. BERC ordered sets are not looped back but are replaced with BCNT ordered sets. Any time a BRST is received, the error count register EC is set to 0 and the scrambling LFSR is set to 0FFFFh. Any number of consecutive BRST ordered sets may be received.

BRST followed by BDAT starts the bit error rate test. The BDAT sequence is the output of the scrambler and is equivalent to the logical idle sequence. It consists of scrambled 0 as described in Appendix B. As listed in Appendix B, the first 16 characters of the sequence are reprinted here:

[tbl-63.md](tbl-63.md)

The receiver shall compare the received data to the BDAT sequence. Errors increment the error count register (EC) by 1. EC may not roll over but shall be held at FFh. The LFSR is advanced once for every character except SKPs. The LFSR rolls over after $2^{16}$-1 symbols. SKPs shall be inserted or deleted as necessary for clock tolerance compensation.

The BERC command does not increment the error count register. The LFSR is advanced. The BERC ordered set is replaced by the BCNT ordered set. The BCNT ordered set includes the non-scrambled 8b/10b encoded error count (EC) register based on the running disparity. Following the return of the BCNT ordered set, the loopback slave shall continue to repeat symbols as received.

BERC may be sent multiple times. The EC register is not cleared by BERC ordered sets.

BERT continues until the loopback mode is terminated as described in Chapter 7.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.