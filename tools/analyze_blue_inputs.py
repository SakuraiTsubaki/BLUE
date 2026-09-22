#!/usr/bin/env python3
"""Analyze BLUE-family Game Boy ROM/save inputs without storing binaries."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

RAM_SIZE_BYTES = {0x00: 0, 0x01: 2*1024, 0x02: 8*1024, 0x03: 32*1024, 0x04: 128*1024, 0x05: 64*1024}
MAPPER = {0x03: "MBC1+RAM+BATTERY", 0x13: "MBC3+RAM+BATTERY", 0x1B: "MBC5+RAM+BATTERY"}
GB_SRAM_BANK = 0x2000


def digest(data: bytes) -> dict[str, str]:
    return {"sha1": hashlib.sha1(data).hexdigest(), "sha256": hashlib.sha256(data).hexdigest()}


def gb_header_checksum(data: bytes) -> int:
    x = 0
    for b in data[0x134:0x14D]:
        x = (x - b - 1) & 0xFF
    return x


def gb_global_checksum(data: bytes) -> int:
    return (sum(data[:0x14E]) + sum(data[0x150:])) & 0xFFFF


def bank_stats(data: bytes, bank_size: int) -> list[dict[str, Any]]:
    out = []
    for index in range((len(data) + bank_size - 1) // bank_size):
        chunk = data[index*bank_size:(index+1)*bank_size]
        out.append({
            "bank": index,
            "offset": index * bank_size,
            "size": len(chunk),
            **digest(chunk),
            "zero_bytes": chunk.count(0),
            "ff_bytes": chunk.count(0xFF),
        })
    return out


def analyze_rom(path: Path, data: bytes) -> dict[str, Any]:
    if len(data) < 0x150:
        raise ValueError("file is too small to be a Game Boy ROM")
    title = data[0x134:0x144].split(b"\0", 1)[0].decode("ascii", "replace")
    stored_global = int.from_bytes(data[0x14E:0x150], "big")
    return {
        "kind": "game-boy-rom",
        "file": path.name,
        "size": len(data),
        **digest(data),
        "header": {
            "title": title,
            "sgb_flag": f"0x{data[0x146]:02X}",
            "cart_type": f"0x{data[0x147]:02X}",
            "mapper": MAPPER.get(data[0x147], "unknown"),
            "rom_size_code": f"0x{data[0x148]:02X}",
            "ram_size_code": f"0x{data[0x149]:02X}",
            "ram_bytes": RAM_SIZE_BYTES.get(data[0x149]),
            "version": data[0x14C],
            "header_checksum_valid": data[0x14D] == gb_header_checksum(data),
            "global_checksum_valid": stored_global == gb_global_checksum(data),
        },
    }


def analyze_save(path: Path, data: bytes) -> dict[str, Any]:
    return {
        "kind": "game-boy-save",
        "file": path.name,
        "size": len(data),
        **digest(data),
        "candidate": "legacy-blue-32k-sram" if len(data) == 0x8000 else ("expanded-blue-128k-sram" if len(data) == 0x20000 else "unknown"),
        "8k_banks": bank_stats(data, GB_SRAM_BANK),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+", type=Path)
    args = ap.parse_args()
    results = []
    for path in args.paths:
        data = path.read_bytes()
        results.append(analyze_rom(path, data) if path.suffix.lower() in {".gb", ".gbc"} else analyze_save(path, data))
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
