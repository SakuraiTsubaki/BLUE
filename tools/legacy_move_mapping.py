#!/usr/bin/env python3
"""Verified Gen I move byte -> BLUE canonical 16-bit move mapping."""
from __future__ import annotations

import hashlib
import struct
import zlib

MOVE_RECORD_BYTES = 6
LEGACY_MOVE_COUNT = 165
LEGACY_MOVE_CODES = 256
CANONICAL_MOVE_COUNT = 165
CANONICAL_ID_WIDTH_BITS = 16

MOVE_TABLE_FILE_OFFSET = 0x38000
MOVE_TABLE_ROM_BANK = 0x0E
MOVE_TABLE_CPU_ADDRESS = 0x4000
MOVE_TABLE_BYTES = MOVE_RECORD_BYTES * LEGACY_MOVE_COUNT

PROFILE_MOVE_TABLE_SHA256 = {
    "ao-jp": "766c1dd686627e6e7493817428c40578231b7757fb73737db510aa49304d514e",
    "blue-us-eu": "0c0d7a55f01f09c5f4859344d087cc824e516b2facc520e389e4bdcb8d14db1e",
    "blue-fr": "0c0d7a55f01f09c5f4859344d087cc824e516b2facc520e389e4bdcb8d14db1e",
    "blue-de": "0c0d7a55f01f09c5f4859344d087cc824e516b2facc520e389e4bdcb8d14db1e",
    "blue-it": "0c0d7a55f01f09c5f4859344d087cc824e516b2facc520e389e4bdcb8d14db1e",
    "blue-es": "0c0d7a55f01f09c5f4859344d087cc824e516b2facc520e389e4bdcb8d14db1e",
}

MAP_MAGIC = b"BLU1MOV\0"
MAP_SCHEMA_VERSION = 1
MAP_BANK_OFFSET = 0x0400
MAP_CPU_ADDRESS = 0x4400
MAP_HEADER_FORMAT = "<8sHHHHI"
MAP_HEADER_SIZE = struct.calcsize(MAP_HEADER_FORMAT)
MAP_PAYLOAD_CPU_ADDRESS = MAP_CPU_ADDRESS + MAP_HEADER_SIZE

LOOKUP_BANK_OFFSET = 0x0620
LOOKUP_CPU_ADDRESS = 0x4620


def validate_move_table_source(rom: bytes, profile: str) -> None:
    table = rom[MOVE_TABLE_FILE_OFFSET:MOVE_TABLE_FILE_OFFSET + MOVE_TABLE_BYTES]
    if len(table) != MOVE_TABLE_BYTES:
        raise ValueError(f"{profile}: move table is truncated")

    digest = hashlib.sha256(table).hexdigest()
    if digest != PROFILE_MOVE_TABLE_SHA256[profile]:
        raise ValueError(f"{profile}: verified move-table hash changed")

    for index in range(LEGACY_MOVE_COUNT):
        move_id = index + 1
        if table[index * MOVE_RECORD_BYTES] != move_id:
            raise ValueError(
                f"{profile}: move record {move_id} does not carry its expected ID byte"
            )


def legacy_move_to_canonical(legacy_move_id: int) -> int:
    if not 0 <= legacy_move_id <= 0xFF:
        raise ValueError("legacy move ID must fit one byte")
    return legacy_move_id if 1 <= legacy_move_id <= LEGACY_MOVE_COUNT else 0


def build_legacy_move_map_block() -> bytes:
    values = [legacy_move_to_canonical(i) for i in range(LEGACY_MOVE_CODES)]
    payload = struct.pack("<" + "H" * LEGACY_MOVE_CODES, *values)
    crc32 = zlib.crc32(payload) & 0xFFFFFFFF
    header = struct.pack(
        MAP_HEADER_FORMAT,
        MAP_MAGIC,
        MAP_SCHEMA_VERSION,
        LEGACY_MOVE_CODES,
        CANONICAL_MOVE_COUNT,
        CANONICAL_ID_WIDTH_BITS,
        crc32,
    )
    return header + payload


def build_lookup_routine() -> bytes:
    # Runtime ABI:
    #   input  A  = legacy move byte
    #   output DE = BLUE canonical 16-bit move ID
    #
    # A indexes a full 256-entry u16 table, so invalid/unused byte values
    # naturally map to 0 without branches.
    return bytes((
        0x5F,                         # ld e, a
        0x16, 0x00,                   # ld d, 0
        0xCB, 0x23,                   # sla e
        0xCB, 0x12,                   # rl d
        0x21, MAP_PAYLOAD_CPU_ADDRESS & 0xFF, MAP_PAYLOAD_CPU_ADDRESS >> 8,
        0x19,                         # add hl, de
        0x5E,                         # ld e, [hl]
        0x23,                         # inc hl
        0x56,                         # ld d, [hl]
        0xC9,                         # ret
    ))


def inspect_legacy_move_map_block(block: bytes) -> dict[str, int | str]:
    magic, version, codes, canonical_count, width, stored_crc = struct.unpack(
        MAP_HEADER_FORMAT, block[:MAP_HEADER_SIZE]
    )
    payload = block[MAP_HEADER_SIZE:MAP_HEADER_SIZE + codes * 2]
    return {
        "magic": magic.rstrip(b"\0").decode("ascii"),
        "schema_version": version,
        "codes": codes,
        "canonical_count": canonical_count,
        "id_width_bits": width,
        "crc32": stored_crc,
        "crc32_valid": int((zlib.crc32(payload) & 0xFFFFFFFF) == stored_crc),
    }
