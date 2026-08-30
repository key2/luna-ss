Universal Serial Bus 3.1 Specification, Revision 1.0

![img-103.jpeg](img-103.jpeg)

Figure 5-23. Illustration of Cable Assembly with Reference Host and Device

The USB 3.1 specification defines the standard reference hosts and devices in the form of S-parameter files, which are available for download from the USB website. The measured S-parameters of the Gen 2 speed cable assembly (with fixture effects removed) are cascaded with the S-parameters of the reference hosts and reference devices, resulting in frequency responses for total channels. The pass/fail criteria of the Gen 2 speed cable assembly are based on the channel frequency responses, as described in the following subsections.

### 5.6.1.3.2.3 Channel Metrics

There are three signal integrity impairments that impact the end-to-end link performance: attenuation, reflection, and crosstalk. Three parameters are used as the channel metrics to represent these three impairments: insertion loss fit at Nyquist frequency (ILfitatNq), integrated multi-reflection (IMR), and integrated crosstalk (IXT).

To obtain the channel insertion loss fit at Nyquist frequency (5 GHz for SuperSpeed Gen 2), the measured (cascaded) differential insertion loss, $IL(f)$, is fitted with a smoothing function:

$$ILfit(f) = a + b\sqrt{f} + cf + d\sqrt{f^3}, \tag{5-1}$$

where $f$ is frequency and $a$, $b$, $c$, and $d$ are fitting coefficients. Figure 5-24 shows an example of $IL(f)$ and $ILfit(f)$ plotted together; ILfitatNq = -20.6 dB, measured at 5 Ghz along $ILfit(f)$.

5-50