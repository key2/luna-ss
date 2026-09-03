#!/usr/bin/env python3
"""Capture both debug UARTs (uart0 link probe, uart1 wire checker /
pipe probe) with wall-clock timestamps.  One reader per tty.

The UARTs ride the quad FTDI's channels C and D; the tty NUMBERS are
volatile (any controller reset or device add/remove renumbers them --
session 15 lost two capture windows to stale ttyUSB4/5 nodes), so the
readers open the stable /dev/serial/by-id/ paths.

uart0 (tag L): <pclk> <lfps> <ts1> <ts2> <rx_com> <flags>
uart1 (tag C): wire checker -- ch0 retry-flagged ACKs, ch1/ch2 device-RX
DPP/header CRC failures, ch3 wire DPs (ep1), ch4 ACK TPs received;
flags = sticky framing-violation / payload-underrun / DPP-CRC / trained.
(Per-top loadouts vary; see the top.py uart comments.)

Usage: sudo python3 uart_capture.py <seconds> [outfile-prefix]
Writes <prefix>_both.txt, both UARTs interleaved.
"""
import sys
import time
import threading
import termios

DURATION = float(sys.argv[1]) if len(sys.argv) > 1 else 30
PREFIX = sys.argv[2] if len(sys.argv) > 2 else "/tmp/kilo/uartcap"

UART0 = "/dev/serial/by-id/usb-FTDI_Quad_RS232-HS-if02-port0"
UART1 = "/dev/serial/by-id/usb-FTDI_Quad_RS232-HS-if03-port0"


def reader(dev, tag, out, stop):
    fd = open(dev, "rb", buffering=0)
    # 115200 8N1 raw
    attrs = termios.tcgetattr(fd)
    attrs[0] = attrs[1] = attrs[3] = 0
    attrs[2] = termios.CS8 | termios.CREAD | termios.CLOCAL
    attrs[4] = attrs[5] = termios.B115200
    termios.tcsetattr(fd, termios.TCSANOW, attrs)
    buf = b""
    t0 = time.time()
    while not stop.is_set():
        data = fd.read(256)
        if not data:
            time.sleep(0.01)
            continue
        buf += data
        while b"\n" in buf:
            line, buf = buf.split(b"\n", 1)
            txt = line.decode("ascii", "replace").strip()
            if txt:
                out.write(f"{time.time()-t0:8.2f} {tag} {txt}\n")
                out.flush()
    fd.close()


stop = threading.Event()
with open(f"{PREFIX}_both.txt", "w") as out:
    threads = [
        threading.Thread(target=reader, args=(UART0, "L", out, stop)),
        threading.Thread(target=reader, args=(UART1, "C", out, stop)),
    ]
    for t in threads:
        t.daemon = True
        t.start()
    time.sleep(DURATION)
    stop.set()
    for t in threads:
        t.join(timeout=2)
print(f"captured to {PREFIX}_both.txt")
