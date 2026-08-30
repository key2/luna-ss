Revision 1.1  
June 2022

- 1 -

Universal Serial Bus 3.2  
Specification

# 1 Introduction

## 1.1 Background

The original Universal Serial Bus (USB) was driven by the need to provide a user-friendly plug-and-play way to attach external peripherals to a Personal Computer (PC). USB has gone beyond just being a way to connect peripherals to PCs. Printers use USB to interface directly to cameras. Mobile devices use USB connected keyboards and mice. USB technology commonly finds itself in automobiles, televisions, and set-top boxes. USB, as a protocol, is also being picked up and used in many nontraditional applications such as industrial automation. And USB as a source of power has become the mobile device charging solution endorsed by international communities across the globe.

Initially, USB provided two speeds (12 Mbps and 1.5 Mbps) that peripherals could use. As PCs became increasingly powerful and able to process larger amounts of data, users needed to get more and more data into and out of their PCs. This led to the definition of the USB 2.0 specification in 2000 to provide a third transfer rate of 480 Mbps while retaining backward compatibility. By 2006, two things in the environment happened: the transfer rates of HDDs exceeded 100 MB/sec, far outstripping USB 2.0's ~32 MB/sec bandwidth and the amount of digital content users were creating was an ever increasing pace. USB 3.0 was the USB community's response and provided users with the ability to move data at rates up to 450 MB/sec while retaining backward compatibility with USB 2.0.

In 2013, with the continued trend for more bandwidth driven by larger and faster storage solutions, higher resolution video, and broader use of USB as an external expansion/docking solution, USB 3.1 extended the performance range of USB up to 1 GB/sec by doubling the SuperSpeed USB clock rate to 10 Gbps and enhancing data encoding efficiency.

Now, with the addition of USB Type-C® to the USB connector/cable ecosystem, USB 3.2 extends the performance range of USB up to 2 GB/sec by enabling two lanes of SuperSpeed signaling to be used in combination over two sets of SuperSpeed pins/wires across the USB Type-C standard connector/cable solution.

## 1.2 Objective of the Specification

This document defines the latest generation USB industry-standard, USB 3.2. The specification describes the protocol definition, types of transactions, bus management, and the programming interface required to design and build systems and peripherals that are compliant with this specification. USB 3.2 is primarily a performance enhancement to USB 3.1 to provide more bandwidth for devices such as Solid State Drives and High Definition displays by adding dual-lane support to the USB Type-C cable and connector.

This specification refers to Enhanced SuperSpeed as a collection of features or requirements that apply to USB 3.x bus operation. Additionally, where specific differences exist with regard to the USB 3.0 definition of SuperSpeed features or requirements, those differences will be uniquely identified as SuperSpeedPlus (or SSP) features or requirements.

USB 3.2's goal is to enable devices from different vendors to interoperate in an open architecture, while maintaining and leveraging the existing USB infrastructure (device drivers, software interfaces, etc.). The specification is intended as an enhancement to the PC architecture, spanning portable, business desktop, and home environments, as well as simple device-to-device communications. It is intended that the specification allow system OEMs and peripheral developers adequate room for product versatility and market differentiation without the burden of carrying obsolete interfaces or losing compatibility.

Copyright © 2022 USB 3.0 Promoter Group. All rights reserved.