# luna-ss — dual-rate SuperSpeed fork of LUNA

**This is a fork** of [greatscottgadgets/luna](https://github.com/greatscottgadgets/luna)
(base `82a8f733`, BSD-3-Clause — upstream license and copyright headers
retained) that turns the SuperSpeed stack into a first-class dual-rate
(Gen1 5 Gbps + Gen2 10 Gbps) device stack for the Gowin GTR12 SerDes
environment, running on our own DK_USB GW5AT-LV60UG225 bench board.

What this fork adds on top of upstream:

* 36 numbered stack fixes found during ten hardware bring-up sessions
  (see the commit series and `HANDOVER.md`): TX-path integrity,
  handshake-arbitration robustness, recovery-retransmit conformance,
  bMaxBurst>1 burst engines both directions, synthesis hardening.
* `luna/gateware/interface/serdes_phy/gowin_gtr12.py` — PIPE adapter
  for the gw_usb3 soft PHY; 64-bit PIPE extension.
* `luna/gateware/usb/usb3/endpoints/ss_stream_out.py` — the bulk OUT
  endpoint (missing upstream).
* Submodules: [`gw_usb3/`](https://github.com/key2/gw_usb3) (the
  Amaranth port of the Gowin USB3.1 PHY, equivalence-proven, Gen1+Gen2
  silicon-proven) and
  [`gowin-serdes/`](https://github.com/key2/gowin-serdes) (GTR12
  generator + board platform + vendor-stack A/B baseline example).
* `examples/gowin/` — the hardware example ladder (enum, ACM echo,
  bulk loopback, 3-pair multiep at 283 MB/s aggregate BURST=2).
* `sim/` — the link-partner simulation battery (38 entries;
  `pdm run battery`).
* `doc/` — specs (USB 3.2 markdown is the conformance reference),
  `HANDOVER.md` (bench log, §10o onward lives here), `prompt.md`
  (active mission), `doc/gen2_design.md` (the Gen2 design note).

Getting started on the bench:

```console
git clone --recurse-submodules https://github.com/key2/luna-ss
cd luna-ss && pdm install
pdm run pytest            # gw_usb3 suite (104 tests)
pdm run battery           # full 38-entry regression battery
pdm run python examples/gowin/luna-multiep/top.py    # build bitstream
```

The frozen pre-fork bench workspace (vendor reference design, hybrid
A/B rig, bug-report packages) lives at
[key2/gw_usb3-archive](https://github.com/key2/gw_usb3-archive)
(`~/Downloads/GW_USB3` on the bench).

---

# LUNA: an Amaranth HDL library for USB ![Simulation Status](https://github.com/greatscottgadgets/luna/workflows/simulations/badge.svg) [![Documentation Status](https://readthedocs.org/projects/luna/badge/?version=latest)](https://luna.readthedocs.io/en/latest/?badge=latest)

LUNA is a toolkit for working with USB using FPGA technology, providing gateware and software to enable USB applications.

Some things you can use LUNA for, currently:

- **Protocol analysis for Low-, Full-, or High- speed USB.** LUNA provides gateware that allow passive USB monitoring when combined with [Cynthion](https://github.com/greatscottgadgets/cynthion-hardware) and [Packetry](https://github.com/greatscottgadgets/packetry).
- **Creating your own Low-, Full-, High-, or (experimentally) Super- speed USB device.** LUNA provides a collection of Amaranth gateware that allows you to easily create USB devices in gateware, software, or a combination of the two.
- **Building USB functionality into a new or existing System-on-a-Chip (SoC).** LUNA is capable of generating custom peripherals targeting the common Wishbone bus; allowing it to easily be integrated into SoC designs; and the [luna-soc](https://github.com/greatscottgadgets/luna-soc) library provides simple automation for developing simple SoC designs.

Some things you'll be able to use LUNA for in the future:

- **Man-in-the-middle'ing USB communications.** The LUNA toolkit will be able to act
  as a *USB proxy*, transparently modifying USB data as it flows between a host and a device.
- **USB reverse engineering and security research.** The LUNA toolkit will serve as an ideal
  backend for tools like [Facedancer](https://github.com/usb-tools/facedancer); allowing easy
  emulation and rapid prototyping of compliant and non-compliant USB devices.

## Project Structure

This project is broken down into several directories:

* `luna` -- the primary LUNA python toolkit; generates gateware and provides USB functionality
  * `luna/gateware` -- the core gateware components for LUNA; and utilities for stitching them together
* `examples` -- simple LUNA-related examples; mostly gateware-targeted, currently
* `docs` -- sources for the LUNA Sphinx documentation
* `contrib` -- contributed/non-core components; such as udev rules
* `applets` -- pre-made gateware applications that provide useful functionality on their own (e.g., are more than examples)

## Project Documentation

LUNA's documentation is captured on [Read the Docs](https://luna.readthedocs.io/en/latest/). Raw documentation sources
are in the `docs` folder.

## Related Projects

* [Cynthion](https://github.com/greatscottgadgets/cynthion-hardware): an open source hardware USB test instrument
* [Apollo](https://github.com/greatscottgadgets/apollo): the firmware that runs on Cynthion's debug controller and which is responsible for configuring its FPGA
* [Saturn-V](https://github.com/greatscottgadgets/saturn-v): a DFU bootloader created for Cynthion
* [Packetry](https://github.com/greatscottgadgets/packetry): software for USB analysis
* [Facedancer](https://github.com/greatscottgadgets/facedancer): software to create USB devices in Python
