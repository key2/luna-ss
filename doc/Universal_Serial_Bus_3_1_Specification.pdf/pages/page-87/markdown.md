USB 3.1 Enhanced SuperSpeed Data Flow Model

$$T_{meas} = \frac{2^K}{2^P} = 2^{(K-P)}$$

In this way, a new estimate for $F_f$ becomes available every $2^{(K-P)}$ bus intervals. $P$ is practically bound to be in the range [0,K] because there is no point in using a clock slower than $F_s$ ($P$=0), and no point in trying to update $F_f$ more than once per bus interval ($P$=K). A sink can determine $F_f$ by counting cycles of the master clock $F_m$ for a period of $2^{(K-P)}$ bus intervals. The counter is read into $F_f$ and reset every $2^{(K-P)}$ bus intervals. As long as no clock cycles are skipped, the count will be accurate over the long term.

Each bus interval, an adaptive source adds $F_f$ to any remaining fractional sample count from the previous bus interval, sources the number of samples in the integer part of the sum, and retains the fractional sample count for the next bus interval. The source can look at the behavior of $F_f$ over many bus intervals to determine an even more accurate rate, if it needs to.

$F_f$ is expressed in number of samples per bus interval. The $F_f$ value consists of an integer part that represents the (integer) number of samples per bus interval and a fractional part that represents the “fraction” of a sample that would be needed to match the sampling frequency $F_s$ to a resolution of 1 Hz or better. The fractional part requires at least K bits to represent the “fraction” of a sample to a resolution of 1 Hz or better. The integer part must have enough bits to represent the maximum number of samples that can ever occur in a single bus interval. Assuming that the minimum sample size is one byte, then this number is currently limited to 48*1024=49152 and 16 bits are needed.

For Enhanced SuperSpeed endpoints, the $F_f$ value shall be encoded in an unsigned 32.K ($K\ge13$) format, encoded into eight bytes (for future extensibility). The value shall be aligned into these eight bytes so that the binary point is located between the fourth and the fifth byte so that it has a 32.32 format. Only the first K bits behind the binary point are required. The lower 32-K bits may be optionally used to extend the precision of $F_f$, otherwise, they shall be reported as zero.

An endpoint needs to implement only the number of bits that it effectively requires for its maximum $F_f$.

The choice of $P$ is endpoint-specific. Use the following guidelines when choosing $P$:

- $P$ must be in the range [0,K].
- Larger values of $P$ are preferred, because they reduce the size of the frame counter and increase the rate at which $F_f$ is updated. More frequent updates result in a tighter control of the source data rate, which reduces the buffer space required to handle $F_f$ changes.
- $P$ should be less than $K$ so that $F_f$ is averaged across at least two frames in order to reduce SOF jitter effects.
- $P$ should not be zero in order to keep the deviation in the number of samples sourced to less than 1 in the event of a lost $F_f$ value.

Isochronous transfers are used to read $F_f$ from the feedback register. The desired reporting rate for the feedback should be $2^{(K-P)}$ bus intervals. $F_f$ will be reported at most once per update period. There is nothing to be gained by reporting the same $F_f$ value more than once per update period. The endpoint may choose to report $F_f$ only if the updated value has changed from the previous $F_f$ value. If the value has not changed, the endpoint may report the current $F_f$ value or a zero length data payload. It is strongly recommended that an endpoint always report the current $F_f$ value any time it is polled.

It is possible that the source will deliver one too many or one too few samples over a long period due to errors or accumulated inaccuracies in measuring $F_f$. The sink must have sufficient buffer

4-17