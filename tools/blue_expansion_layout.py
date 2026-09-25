#!/usr/bin/env python3
"""BLUE expanded-ROM metadata and canonical registry bootstrap."""
from __future__ import annotations

import struct
import zlib

try:
    from legacy_species_mapping import (
        CANONICAL_SPECIES_COUNT,
        MAP_BANK_OFFSET,
        MAP_CPU_ADDRESS,
        build_legacy_species_map_block,
    )
except ModuleNotFoundError:
    from tools.legacy_species_mapping import (
        CANONICAL_SPECIES_COUNT,
        MAP_BANK_OFFSET,
        MAP_CPU_ADDRESS,
        build_legacy_species_map_block,
    )

ROM_BANK_BYTES = 0x4000
MAGIC = b"BLU10ROM"
SCHEMA_VERSION = 2
HEADER_SIZE = 64
DIRECTORY_BANK_OFFSET = 0x80
DIRECTORY_CPU_ADDRESS = 0x4080
DIRECTORY_ENTRY_SIZE = 16
UNALLOCATED = 0xFFFF
REGISTRY_FLAG_NAMESPACE_RESERVED = 0x0001

PROFILE_LAYOUT = {
    "ao-jp": {"profile_id": 1, "metadata_bank": 0x020},
    "blue-us-eu": {"profile_id": 2, "metadata_bank": 0x040},
    "blue-fr": {"profile_id": 3, "metadata_bank": 0x040},
    "blue-de": {"profile_id": 4, "metadata_bank": 0x040},
    "blue-it": {"profile_id": 5, "metadata_bank": 0x040},
    "blue-es": {"profile_id": 6, "metadata_bank": 0x040},
}

REGISTRY_DOMAINS = (
    ("species", 1),
    ("form", 2),
    ("move", 3),
    ("item", 4),
    ("ability", 5),
    ("type", 6),
    ("map", 7),
    ("location", 8),
    ("trainer_class", 9),
    ("evolution_method", 10),
)

HEADER_FORMAT = "<8s16H16sII"
DIRECTORY_FORMAT = "<8H"


def build_header(profile: str, source_sha256: str) -> bytes:
    cfg = PROFILE_LAYOUT[profile]
    fields = (
        SCHEMA_VERSION,
        HEADER_SIZE,
        cfg["profile_id"],
        0,
        cfg["metadata_bank"],
        cfg["metadata_bank"] + 1,
        0x01FF,
        0x0004,
        0x000F,
        0x0000,
        0x0010,
        0x0020,
        0x0043,
        DIRECTORY_CPU_ADDRESS,
        len(REGISTRY_DOMAINS),
        DIRECTORY_ENTRY_SIZE,
    )
    source_prefix = bytes.fromhex(source_sha256)[:16]
    raw = struct.pack(
        HEADER_FORMAT,
        MAGIC,
        *fields,
        source_prefix,
        0,
        MAP_CPU_ADDRESS,
    )
    if len(raw) != HEADER_SIZE:
        raise AssertionError("BLUE expansion header size changed")
    crc32 = zlib.crc32(raw) & 0xFFFFFFFF
    return struct.pack(
        HEADER_FORMAT,
        MAGIC,
        *fields,
        source_prefix,
        crc32,
        MAP_CPU_ADDRESS,
    )


def build_directory() -> bytes:
    entries = []
    for name, domain_id in REGISTRY_DOMAINS:
        if name == "species":
            flags = REGISTRY_FLAG_NAMESPACE_RESERVED
            count = CANONICAL_SPECIES_COUNT
        else:
            flags = 0
            count = 0

        entries.append(struct.pack(
            DIRECTORY_FORMAT,
            domain_id,
            flags,
            count,
            0,
            UNALLOCATED,
            UNALLOCATED,
            1,
            0,
        ))
    return b"".join(entries)


def metadata_file_offset(profile: str) -> int:
    return PROFILE_LAYOUT[profile]["metadata_bank"] * ROM_BANK_BYTES


def install_expansion_metadata(out: bytearray, profile: str, source_sha256: str) -> None:
    base = metadata_file_offset(profile)
    end = base + ROM_BANK_BYTES
    if any(value != 0xFF for value in out[base:end]):
        raise ValueError(f"{profile}: metadata bank is not blank expansion space")

    header = build_header(profile, source_sha256)
    directory = build_directory()
    legacy_species_map = build_legacy_species_map_block()

    out[base:base + len(header)] = header
    directory_start = base + DIRECTORY_BANK_OFFSET
    out[directory_start:directory_start + len(directory)] = directory
    map_start = base + MAP_BANK_OFFSET
    out[map_start:map_start + len(legacy_species_map)] = legacy_species_map


def inspect_header(data: bytes, profile: str) -> dict[str, int | str]:
    base = metadata_file_offset(profile)
    values = struct.unpack(HEADER_FORMAT, data[base:base + HEADER_SIZE])
    magic = values[0]
    fields = values[1:17]
    source_prefix = values[17]
    crc32 = values[18]
    legacy_species_map_cpu_address = values[19]

    raw = bytearray(data[base:base + HEADER_SIZE])
    raw[56:60] = b"\x00" * 4
    expected_crc = zlib.crc32(raw) & 0xFFFFFFFF

    return {
        "magic": magic.decode("ascii"),
        "schema_version": fields[0],
        "header_size": fields[1],
        "profile_id": fields[2],
        "metadata_bank": fields[4],
        "first_content_bank": fields[5],
        "last_rom_bank": fields[6],
        "directory_cpu_address": fields[13],
        "directory_count": fields[14],
        "directory_entry_size": fields[15],
        "source_sha256_prefix": source_prefix.hex(),
        "crc32": crc32,
        "crc32_valid": int(crc32 == expected_crc),
        "legacy_species_map_cpu_address": legacy_species_map_cpu_address,
    }
