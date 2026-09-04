#
# This file is part of LUNA.
#
# Copyright (c) 2026 the luna-ss contributors
# SPDX-License-Identifier: BSD-3-Clause
""" SuperSpeedPlus descriptor helpers.

``usb_protocol`` (0.9.x) has no SuperSpeedPlus USB Device Capability
emitter; a device announcing ``bcdUSB`` 0310h without one draws a
Linux-host complaint at enumeration and under-describes its sublinks
[USB 3.2r1: 9.6.2.5].  This module builds the capability (and a full
SSP-ready BOS) as raw descriptor bytes, byte-compatible with the
``add_subordinate_descriptor`` API.

Field layout [Table 9-27], single-lane Gen 2x1 defaults; the sublink
speed attributes follow the RX/TX-pair convention observed on shipping
SSP silicon (one symmetric-RX and one symmetric-TX attribute per SSID;
SSID 0 = 5 Gbps SuperSpeed, SSID 1 = 10 Gbps SuperSpeedPlus, LSE=3 /
LSM in Gbps).
"""

import struct


def _sublink_speed_attribute(*, ssid, lse, tx, lp, lsm):
    """ One bmSublinkSpeedAttr dword [Table 9-27].

    Parameters
    ----------
    ssid: int
        Sublink Speed Attribute ID (shared by the RX/TX pair).
    lse: int
        Lane Speed Exponent (3 = Gb/s).
    tx: bool
        False = receive attribute, True = transmit attribute (ST field;
        symmetric link, so only bit 7 distinguishes the pair).
    lp: int
        Link Protocol: 0 = SuperSpeed, 1 = SuperSpeedPlus.
    lsm: int
        Lane Speed Mantissa (5 or 10).
    """
    return (
        (ssid & 0xF)
        | ((lse & 0x3) << 4)
        | ((1 if tx else 0) << 7)
        | ((lp & 0x3) << 14)
        | ((lsm & 0xFFFF) << 16)
    )


def ssp_device_capability(*, min_ssid=0, min_rx_lanes=1, min_tx_lanes=1,
                          attributes=None):
    """ Returns the SuperSpeedPlus USB Device Capability as bytes.

    The default is the single-lane Gen 2x1 shape: two sublink speed
    IDs (0 = 5 Gbps SS, 1 = 10 Gbps SSP), each with an RX and a TX
    attribute; full functionality at SSID 0 on 1+1 lanes.
    """
    if attributes is None:
        attributes = [
            _sublink_speed_attribute(ssid=0, lse=3, tx=False, lp=0, lsm=5),
            _sublink_speed_attribute(ssid=0, lse=3, tx=True,  lp=0, lsm=5),
            _sublink_speed_attribute(ssid=1, lse=3, tx=False, lp=1, lsm=10),
            _sublink_speed_attribute(ssid=1, lse=3, tx=True,  lp=1, lsm=10),
        ]

    ssac = len(attributes) - 1                      # attribute count - 1
    ssic = len({a & 0xF for a in attributes}) - 1   # ID count - 1
    bm_attributes = (ssac & 0x1F) | ((ssic & 0xF) << 5)
    w_functionality = ((min_ssid & 0xF)
                       | ((min_rx_lanes & 0xF) << 8)
                       | ((min_tx_lanes & 0xF) << 12))

    body = struct.pack(
        "<BBBBLHH",
        12 + 4 * len(attributes),   # bLength
        0x10,                       # bDescriptorType: DEVICE CAPABILITY
        0x0A,                       # bDevCapabilityType: SUPERSPEED_PLUS
        0,                          # bReserved
        bm_attributes,              # bmAttributes: SSAC / SSIC
        w_functionality,            # wFunctionalitySupport
        0,                          # wReserved
    )
    body += b"".join(struct.pack("<L", a) for a in attributes)
    return body


def add_superspeedplus_bos(descriptors):
    """ Adds an SSP-ready BOS (USB2 ext + SS cap + SSP cap) to a
    ``SuperSpeedDeviceDescriptorCollection`` -- the surface a Linux
    xHCI host expects from a ``bcdUSB`` 0310h device. """
    from usb_protocol.emitters.descriptors.standard import (
        USB2ExtensionDescriptorEmitter,
        SuperSpeedUSBDeviceCapabilityDescriptorEmitter)

    with descriptors.BOSDescriptor() as bos:
        bos.add_subordinate_descriptor(USB2ExtensionDescriptorEmitter())
        bos.add_subordinate_descriptor(
            SuperSpeedUSBDeviceCapabilityDescriptorEmitter())
        bos.add_subordinate_descriptor(ssp_device_capability())
