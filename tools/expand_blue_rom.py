#!/usr/bin/env python3
"""Expand a verified BLUE-family ROM to an 8 MiB MBC5 runtime image.

BLUE preserves the retail image except for explicitly verified runtime hook
locations, cartridge header fields, and checksums.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

TARGET_SIZE = 0x800000
TARGET_CART = 0x1B
TARGET_ROM_SIZE = 0x08
TARGET_RAM_SIZE = 0x04

RST_VECTOR_BASELINE = bytes.fromhex("ff00000000000000" * 7)

FARCALL9_ADDR = 0x0000
SETBANK9_ADDR = 0x0010
VBLANK9_ADDR = 0x0020

H_LOADED_ROM_BANK_LOW = 0xB8
H_CURRENT_ROM_BANK_HIGH = 0xFA

KNOWN = {
    "71a70e5f77c109177d21c998310ffe01a68e8cd2f41e72e7129093b890c7d3d1": ("ao-jp", 0x80000, 0x03, 0x04),
    "2a951313c2640e8c2cb21f25d1db019ae6245d9c7121f754fa61afd7bee6452d": ("blue-us-eu", 0x100000, 0x13, 0x05),
    "73dee67befed0c39cd0a6ed53a98ff5b98b3bddc3e7a0dae1d982776a4d0889b": ("blue-fr", 0x100000, 0x1B, 0x05),
    "2cfec2223090dc9f544aa36c99c48801be5018757a1366b88d8f40739541458e": ("blue-de", 0x100000, 0x1B, 0x05),
    "e197c7535135a516fe9bf92cf7821c9f72926bf90fce3a2a5742d1b0b6a0564b": ("blue-it", 0x100000, 0x1B, 0x05),
    "31317f74fed2935dfc5fbb6ada766cf8515949c85c6c6e8d32d0f752b85b8f9e": ("blue-es", 0x100000, 0x1B, 0x05),
}

PROFILE_RUNTIME = {
    "ao-jp": {"vblank_target": 0x200A, "vblank_reti": 0x208E},
    "blue-us-eu": {"vblank_target": 0x2024, "vblank_reti": 0x20AE},
    "blue-fr": {"vblank_target": 0x2020, "vblank_reti": 0x20AA},
    "blue-de": {"vblank_target": 0x2024, "vblank_reti": 0x20AE},
    "blue-it": {"vblank_target": 0x2024, "vblank_reti": 0x20AE},
    "blue-es": {"vblank_target": 0x2023, "vblank_reti": 0x20AD},
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def header_checksum(data: bytes) -> int:
    value = 0
    for offset in range(0x134, 0x14D):
        value = (value - data[offset] - 1) & 0xFF
    return value


def global_checksum(data: bytes) -> int:
    return (sum(data[:0x14E]) + sum(data[0x150:])) & 0xFFFF


def validate_source(data: bytes) -> str:
    digest = sha256(data)
    if digest not in KNOWN:
        raise ValueError(f"unverified BLUE-family ROM sha256: {digest}")
    profile, size, cart, rom_code = KNOWN[digest]
    if len(data) != size:
        raise ValueError("known hash has unexpected size")
    if data[0x134:0x144].split(b"\0", 1)[0] != b"POKEMON BLUE":
        raise ValueError("unexpected title")
    if data[0x147] != cart or data[0x148] != rom_code or data[0x149] != 0x03:
        raise ValueError("source cartridge header disagrees with verified profile")
    if data[0x14D] != header_checksum(data):
        raise ValueError("invalid source header checksum")
    if int.from_bytes(data[0x14E:0x150], "big") != global_checksum(data):
        raise ValueError("invalid source global checksum")
    if data[:0x38] != RST_VECTOR_BASELINE:
        raise ValueError("unexpected RST-vector contents; refusing runtime injection")

    runtime = PROFILE_RUNTIME[profile]
    if data[0x40] != 0xC3:
        raise ValueError("unexpected VBlank vector opcode")
    actual_vblank = data[0x41] | (data[0x42] << 8)
    if actual_vblank != runtime["vblank_target"]:
        raise ValueError("VBlank vector disagrees with verified profile")
    if data[runtime["vblank_reti"]] != 0xD9:
        raise ValueError("verified VBlank RETI byte is not present")

    return profile


def build_mbc5_runtime(vblank_target: int) -> bytes:
    out = bytearray(RST_VECTOR_BASELINE)

    farcall9 = bytes((
        0xD5,
        0xCD, 0x10, 0x00,
        0x01, 0x09, 0x00,
        0xC5,
        0xE9,
        0xD1,
        0x42,
        0x4B,
        0xCD, 0x10, 0x00,
        0xC9,
    ))

    setbank9 = bytes((
        0x79,
        0xE0, H_LOADED_ROM_BANK_LOW,
        0xEA, 0x00, 0x20,
        0x78,
        0xE6, 0x01,
        0xEA, 0x00, 0x30,
        0xE0, H_CURRENT_ROM_BANK_HIGH,
        0xC9,
    ))

    # While the original VBlank handler runs, force MBC5 bank bit 8 to zero.
    # The original handler already saves/restores the low byte. The high byte
    # remains in HRAM and is restored immediately before RETI.
    vblank9 = bytes((
        0xAF,
        0xEA, 0x00, 0x30,
        0xCD, vblank_target & 0xFF, (vblank_target >> 8) & 0xFF,
        0xF0, H_CURRENT_ROM_BANK_HIGH,
        0xE6, 0x01,
        0xEA, 0x00, 0x30,
        0xD9,
    ))

    out[FARCALL9_ADDR:FARCALL9_ADDR + len(farcall9)] = farcall9
    out[SETBANK9_ADDR:SETBANK9_ADDR + len(setbank9)] = setbank9
    out[VBLANK9_ADDR:VBLANK9_ADDR + len(vblank9)] = vblank9
    return bytes(out)


def install_mbc5_runtime(out: bytearray, profile: str) -> None:
    runtime = PROFILE_RUNTIME[profile]
    out[:0x38] = build_mbc5_runtime(runtime["vblank_target"])
    out[0x40:0x43] = bytes((0xC3, VBLANK9_ADDR & 0xFF, VBLANK9_ADDR >> 8))
    out[runtime["vblank_reti"]] = 0xC9


def expand_rom(data: bytes) -> bytes:
    profile = validate_source(data)
    out = bytearray(data)
    out.extend(b"\xFF" * (TARGET_SIZE - len(out)))
    install_mbc5_runtime(out, profile)
    out[0x147] = TARGET_CART
    out[0x148] = TARGET_ROM_SIZE
    out[0x149] = TARGET_RAM_SIZE
    out[0x14D] = header_checksum(out)
    out[0x14E:0x150] = b"\x00\x00"
    checksum = global_checksum(out)
    out[0x14E] = checksum >> 8
    out[0x14F] = checksum & 0xFF
    return bytes(out)


def preserved_legacy_bytes(source: bytes, expanded: bytes, profile: str) -> bool:
    runtime = PROFILE_RUNTIME[profile]
    ignored = set(range(0x38))
    ignored.update(range(0x40, 0x43))
    ignored.update((runtime["vblank_reti"], 0x147, 0x148, 0x149, 0x14D, 0x14E, 0x14F))
    return all(source[i] == expanded[i] for i in range(len(source)) if i not in ignored)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("source", type=Path)
    ap.add_argument("output", type=Path)
    args = ap.parse_args()

    source = args.source.read_bytes()
    profile = validate_source(source)
    expanded = expand_rom(source)
    if not preserved_legacy_bytes(source, expanded, profile):
        raise SystemExit("legacy ROM preservation check failed")
    args.output.write_bytes(expanded)
    print(
        f"{profile}: {len(source)} -> {len(expanded)} bytes; "
        f"MBC5 8 MiB / 128 KiB SRAM; FarCall9=0x{FARCALL9_ADDR:04X}; "
        f"VBlank9=0x{VBLANK9_ADDR:04X}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
