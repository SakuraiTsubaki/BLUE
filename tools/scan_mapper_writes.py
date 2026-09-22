#!/usr/bin/env python3
"""Scan a raw BLUE-family ROM for exact LD (nn),A mapper-control patterns.

This is a byte-pattern census only. Hits require control-flow verification
before they are treated as executable mapper writes.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import sys
from pathlib import Path

TARGETS = (0x0000, 0x2000, 0x3000, 0x4000, 0x6000)


def positions(data: bytes, address: int) -> list[int]:
    pattern = bytes((0xEA, address & 0xFF, address >> 8))
    return [i for i in range(len(data) - 2) if data[i:i + 3] == pattern]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("rom", type=Path)
    ap.add_argument("--profile", required=True)
    args = ap.parse_args()

    data = args.rom.read_bytes()
    writer = csv.writer(sys.stdout)
    writer.writerow(("profile", "sha256", "opcode", "target", "count", "positions"))
    for address in TARGETS:
        hits = positions(data, address)
        writer.writerow((
            args.profile,
            hashlib.sha256(data).hexdigest(),
            "EA",
            f"0x{address:04X}",
            len(hits),
            " ".join(f"0x{x:X}" for x in hits),
        ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
