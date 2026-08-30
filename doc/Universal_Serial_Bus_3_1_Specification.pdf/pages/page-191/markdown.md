Physical Layer

Table 6-20. Informative Gen 2 Transmitter Equalization Settings

[tbl-73.md](tbl-73.md)

### 6.7.6 Entry into Electrical Idle, U1

Electrical Idle is a steady state condition where the Transmitter Txp and Txn voltages are held constant at the same value and the Receiver Termination is within the range specified by Z$_{RX-DC}$. Electrical Idle is used in the power saving state of U1.

The low impedance common mode and differential Receiver terminations values (see Table 6-21) must be met in Electrical Idle. The Transmitter can be in either a low or high impedance mode during Electrical Idle.

## 6.8 Receiver Specifications

### 6.8.1 Receiver Equalization Training

The receiver equalization training sequence, detailed in Section 6.4.1.1 for Gen 1 operation and in Section 6.4.1.2 for Gen 2 operation, can be used to train the receiver equalizer. The TSEQ training sequence is designed to provide spectrally rich data patterns that are useful for training typical receiver equalization architectures. For Gen 1 operation, a high edge density pattern is interleaved with the data to help the CDR maintain bit lock. For Gen 2 operation the sequence is deemed sufficiently rich on its own.

During Gen 1 operation the TSEQ training sequence repeats 65536 times to allow for testing many coefficient settings. Also during Gen 1 operation no SKPs are inserted during the TSEQ training sequence. The frequency spectrum of the TSEQ sequence is shown in Figure 6-23.

During Gen 2 operation, the training period is ~8ms. The training pattern is periodic with a period of 16384 132-bit blocks (2162688UI). The much longer pattern greatly increases the richness of the pattern compared to Gen 1. The Gen 2 training pattern spectrum is essentially white. Due to the length of the Gen 2 training interval and the potential desire to examine the data, SKPs are inserted during polling.TSEQ.

Receiver equalization training is implementation specific.

6-35