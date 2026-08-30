Chapter 1: Introduction

1/17/2018

# 1 Introduction

This document provides the compliance criteria and test descriptions for Enhanced SuperSpeed USB 3.1 Link Layer implementations. It is relevant for anyone building an Enhanced SuperSpeed host, hub or device. The document is divided into two major sections. The first section lists the compliance criteria and the second section lists the test descriptions used to verify a port's conformance to these criteria.

Compliance criteria are provided as a list of assertions that describe specific characteristics or behaviors that must be met. Each assertion provides a reference to the USB 3.1 specification or other documents from which the assertion was derived. In addition, each assertion provides a reference to the specific test description(s) where the assertion is tested.

Each test assertion is formatted as follows:

[tbl-2.md](tbl-2.md)

Assertion#: Unique identifier for each spec requirement. The identifier is in the form USB31_SPEC_SECTION_NUMBER#X, where X is a unique integer for a requirement in that section.

Assertion Description: Specific requirement from the specification

Test #: A label for a specific test description in this specification that tests this requirement. Test # can have one of the following values:

NT This item is not explicitly tested in a test description. Items can be labeled NT for several reasons – including items that are not testable, not important to test for interoperability, or are indirectly tested by other operations performed by the compliance test.

X.X This item is covered by the test described in test description X.X in this specification.

IOP This assertion is verified by the USB 3.0 Interoperability Test Suite.

BC This assertion is applied as a background check in all test descriptions.

Test descriptions provide a high level overview of the tests that are performed to check the compliance criteria. The descriptions are provided with enough detail so that a reader can understand what the test does. The descriptions do not describe the actual step-by-step procedure to perform the test.

Host tests are performed with a Windows 8 machine with all the latest Microsoft updates. The Compliance driver is loaded for most of the Host tests. The Compliance Driver is provided with USB30CV from the usb.org website. One of the Host tests requires the vendor driver for the host controller to be loaded.

Some of the downstream port tests require USB30CV test supplements to perform the test. If a test requires USB30CV, it will be noted in the description later in this document. To run the LVS (Link Validation System) and USB30CV together, always start the USB30CV test prior to the LVS test.

For questions about this document, please contact ssusbcompliance@usb.org. For questions regarding the test matrix or equipment please contact techadmin@usb.org.

1

USB 3.1 Link Layer Test Specification