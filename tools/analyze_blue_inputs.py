#!/usr/bin/env python3
"""Analyze Pokémon Blue-family ROM and save inputs without storing binaries."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

RAM_SIZE_BYTES = {
    0x00: 0,
    0x01: 2 * 1024,
    0x02: 8 * 1024,
    0x03: 32 * 1024,
    0x04: 128 * 1024,
    0x05: 64 * 1024,
}

MAPPER = {
    0x03: "MBC1+RAM+BATTERY",
    0x13: "MBC3+RAM+BATTERY",
    0x1B: "MBC5+RAM+BATTERY",
}

GB_SRAM_BANK = 0x2000
GBA_SECTOR = 0x1000
GBA_SECTOR_COUNT = 32
GBA_SAVE_BYTES = GBA_SECTOR * GBA_SECTOR_COUNT
GBA_SECTOR_ID_OFFSET = 0xFF4
GBA_SECTOR_CHECKSUM_OFFSET = 0xFF6
GBA_SECTOR_SIGNATURE_OFFSET = 0xFF8
GBA_SECTOR_COUNTER_OFFSET = 0xFFC


def digest(data: bytes) -> dict[str, str]:
    return {
        "sha1": hashlib.sha1(data).hexdigest(),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def gb_header_checksum(data: bytes) -> int:
    x = 0
    for b in data[0x134:0x14D]:
        x = (x - b - 1) & 0xFF
    return x


def gb_global_checksum(data: bytes) -> int:
    return (sum(data[:0x14E]) + sum(data[0x150:])) & 0xFFFF


def analyze_rom(path: Path, data: bytes) -> dict[str, Any]:
    if len(data) < 0x150:
        raise ValueError("file is too small to be a Game Boy ROM")

    title = data[0x134:0x144].split(b"\0", 1)[0].decode("ascii", "replace")
    cart_type = data[0x147]
    ram_code = data[0x149]
    stored_global = int.from_bytes(data[0x14E:0x150], "big")

    return {
        "kind": "game-boy-rom",
        "file": path.name,
        "size": len(data),
        **digest(data),
        "header": {
            "title": title,
            "sgb_flag": f"0x{data[0x146]:02X}",
            "cart_type": f"0x{cart_type:02X}",
            "mapper": MAPPER.get(cart_type, "unknown"),
            "rom_size_code": f"0x{data[0x148]:02X}",
            "ram_size_code": f"0x{ram_code:02X}",
            "ram_bytes": RAM_SIZE_BYTES.get(ram_code),
            "destination_code": f"0x{data[0x14A]:02X}",
            "version": data[0x14C],
            "header_checksum": f"0x{data[0x14D]:02X}",
            "header_checksum_valid": data[0x14D] == gb_header_checksum(data),
            "global_checksum": f"0x{stored_global:04X}",
            "global_checksum_valid": stored_global == gb_global_checksum(data),
        },
    }


def bank_stats(data: bytes, bank_size: int) -> list[dict[str, Any]]:
    out = []
    for index in range((len(data) + bank_size - 1) // bank_size):
        chunk = data[index * bank_size : (index + 1) * bank_size]
        out.append(
            {
                "bank": index,
                "offset": index * bank_size,
                "size": len(chunk),
                **digest(chunk),
                "zero_bytes": chunk.count(0x00),
                "ff_bytes": chunk.count(0xFF),
            }
        )
    return out


def analyze_gba_sector_save(data: bytes) -> dict[str, Any]:
    sectors = []
    for index in range(GBA_SECTOR_COUNT):
        s = data[index * GBA_SECTOR : (index + 1) * GBA_SECTOR]
        sectors.append(
            {
                "physical_sector": index,
                "id": int.from_bytes(s[GBA_SECTOR_ID_OFFSET:GBA_SECTOR_ID_OFFSET + 2], "little"),
                "checksum": int.from_bytes(s[GBA_SECTOR_CHECKSUM_OFFSET:GBA_SECTOR_CHECKSUM_OFFSET + 2], "little"),
                "signature": f"0x{int.from_bytes(s[GBA_SECTOR_SIGNATURE_OFFSET:GBA_SECTOR_SIGNATURE_OFFSET + 4], 'little'):08X}",
                "counter": int.from_bytes(s[GBA_SECTOR_COUNTER_OFFSET:GBA_SECTOR_COUNTER_OFFSET + 4], "little"),
                **digest(s),
            }
        )
    return {"candidate_format": "gba-128k-sector-save", "sectors": sectors}


def analyze_save(path: Path, data: bytes) -> dict[str, Any]:
    result: dict[str, Any] = {
        "kind": "save",
        "file": path.name,
        "size": len(data),
        **digest(data),
    }

    if len(data) == 32 * 1024:
        result["candidate_format"] = "pokemon-blue-raw-battery-sram"
        result["banks"] = bank_stats(data, GB_SRAM_BANK)
    elif len(data) == GBA_SAVE_BYTES:
        result.update(analyze_gba_sector_save(data))
    else:
        result["candidate_format"] = "unknown"
        result["8k_chunks"] = bank_stats(data, GB_SRAM_BANK)

    return result


def analyze(path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    if path.suffix.lower() in {".gb", ".gbc"}:
        return analyze_rom(path, data)
    return analyze_save(path, data)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--compact", action="store_true")
    args = parser.parse_args()

    results = [analyze(path) for path in args.paths]
    print(json.dumps(results, ensure_ascii=False, indent=None if args.compact else 2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
