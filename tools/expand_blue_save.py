#!/usr/bin/env python3
"""Expand a 32 KiB BLUE-family battery save to 128 KiB.

Banks 0-3 are preserved byte-for-byte. Bank 4 receives a versioned extension
header and all other new bytes remain 0xFF.

Exact regional legacy checksums are deliberately not guessed without real
save samples.
"""
from __future__ import annotations

import argparse
import hashlib
import struct
import zlib
from pathlib import Path

SOURCE_SIZE = 0x8000
TARGET_SIZE = 0x20000
BANK_SIZE = 0x2000
EXT_BANK = 4
EXT_OFFSET = EXT_BANK * BANK_SIZE
MAGIC = b"BLU10EXT"
SCHEMA_VERSION = 1

PROFILE_IDS = {
    "ao-jp": 1,
    "blue-us-eu": 2,
    "blue-fr": 3,
    "blue-de": 4,
    "blue-it": 5,
    "blue-es": 6,
}


def expand_save(data: bytes, profile: str) -> bytes:
    if len(data) != SOURCE_SIZE:
        raise ValueError(f"expected 32 KiB source save, got {len(data)} bytes")
    if profile not in PROFILE_IDS:
        raise ValueError(f"unknown profile: {profile}")

    out = bytearray(b"\xFF" * TARGET_SIZE)
    out[:SOURCE_SIZE] = data

    source_crc32 = zlib.crc32(data) & 0xFFFFFFFF
    source_sha_prefix = hashlib.sha256(data).digest()[:16]
    payload_length = 0
    payload_crc32 = zlib.crc32(b"") & 0xFFFFFFFF
    header = struct.pack(
        "<8sHBBIIII16s",
        MAGIC,
        SCHEMA_VERSION,
        PROFILE_IDS[profile],
        0,
        SOURCE_SIZE,
        source_crc32,
        payload_length,
        payload_crc32,
        source_sha_prefix,
    )
    out[EXT_OFFSET:EXT_OFFSET + len(header)] = header
    return bytes(out)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("source", type=Path)
    ap.add_argument("output", type=Path)
    ap.add_argument("--profile", choices=tuple(PROFILE_IDS), required=True)
    args = ap.parse_args()

    source = args.source.read_bytes()
    expanded = expand_save(source, args.profile)
    if expanded[:SOURCE_SIZE] != source:
        raise SystemExit("legacy 32 KiB preservation check failed")
    args.output.write_bytes(expanded)
    print(f"{args.profile}: {len(source)} -> {len(expanded)} bytes; legacy SRAM banks preserved")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
