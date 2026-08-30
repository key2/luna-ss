Revision 1.1
June 2022

- 77 -

Universal Serial Bus 3.2
Specification

The equations for these functions are:

$$H_{CDR}(s) = \frac{2s\zeta\omega_n + \omega_n^2}{s^2 + 2s\zeta\omega_n + \omega_n^2} \tag{1}$$

and

$$JTF(s) = \frac{s^2}{s^2 + 2\zeta\omega_n s + \omega_n^2} \tag{2}$$

where $\omega_n$ is the natural frequency and $\zeta$ is the damping factor. The relationship to the 3 dB frequency is

$$\omega_{3dB} = \omega_n \left( 1 + 2\zeta^2 + \left[ (1 + 2\zeta^2)^2 + 1 \right]^{\frac{1}{2}} \right)^{\frac{1}{2}} \tag{3}$$

As shown in Figure 6-14, for Gen 1 operation the corner frequency is $\omega_{3dB} = 2\pi 10^7$ and $\zeta = 0.707$. For Gen 2 operation refer to Figure 6-15 with $\omega_{3dB} = 2\pi 1.5 \times 10^7$ and $\zeta = 0.707$. These transfer functions have a maximum peaking of 2 dB.

### 6.5.3 Normative Spread Spectrum Clocking (SSC)

All ports are required to have Spread Spectrum Clocking (SSC) modulation. Providing the same SSC clock to two different components is allowed but not required, the SSC can be generated asynchronously. The SSC profile is not specified and is vendor specific. The SSC modulation requirement is listed in Table 6-17. The SSC modulation may not violate the phase slew rate described in Section 6.5.4.

Table 6-17. SSC Parameters

[tbl-53.md](tbl-53.md)

Note:

1. The data rate is modulated from 0 ppm to -5000 ppm of the nominal data rate frequency and scales with data rate.

2. This is measured below 2 MHz only.

An example of the period modulation from triangular SSC is shown in Figure 6-16.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.