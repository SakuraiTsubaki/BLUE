#!/usr/bin/env python3
"""Verified Gen I internal species ID -> BLUE canonical species mapping."""
from __future__ import annotations

import struct
import zlib

POKEDEX_ORDER = bytes.fromhex(
    "707320231564225002676c66585e1d1f686f833b97825a485c7b78097f720000"
    "3a5f16104f404b71437a6a6b182f36604c007e007d526d003856328000000053"
    "3095000000543c7c9290918434620000002526191a000093948c8d747500001b1c"
    "8a8b2728858887864229172e3d3e0d0e0f00553933315700000a0b0c44003761"
    "2a968f8100005900635b0065246e3569005d3f4111127901034900767700000000"
    "4d4e1314211e4a898e005100000407050806000000002b2c2d454647"
)

POKEDEX_ORDER_SHA256 = "878d381c0c488f05629c90f4bfbf046c6c029779adfa98f81f78aa9cb62246c6"
LEGACY_SPECIES_SLOTS = 190
MISSINGNO_SLOTS = 39
CANONICAL_SPECIES_COUNT = 151
CANONICAL_ID_WIDTH_BITS = 16

PROFILE_POKEDEX_ORDER = {
    "ao-jp": {"file_offset": 0x42784, "rom_bank": 0x10, "cpu_address": 0x6784},
    "blue-us-eu": {"file_offset": 0x41024, "rom_bank": 0x10, "cpu_address": 0x5024},
    "blue-fr": {"file_offset": 0x40FAA, "rom_bank": 0x10, "cpu_address": 0x4FAA},
    "blue-de": {"file_offset": 0x40F96, "rom_bank": 0x10, "cpu_address": 0x4F96},
    "blue-it": {"file_offset": 0x40FB6, "rom_bank": 0x10, "cpu_address": 0x4FB6},
    "blue-es": {"file_offset": 0x40FB4, "rom_bank": 0x10, "cpu_address": 0x4FB4},
}

MAP_MAGIC = b"BLU1SPC\0"
MAP_SCHEMA_VERSION = 1
MAP_BANK_OFFSET = 0x0200
MAP_CPU_ADDRESS = 0x4200
MAP_HEADER_FORMAT = "<8sHHHHI"
MAP_HEADER_SIZE = struct.calcsize(MAP_HEADER_FORMAT)
MAP_PAYLOAD_CPU_ADDRESS = MAP_CPU_ADDRESS + MAP_HEADER_SIZE

LOOKUP_BANK_OFFSET = 0x03A0
LOOKUP_CPU_ADDRESS = 0x43A0


def validate_static_mapping() -> None:
    if len(POKEDEX_ORDER) != LEGACY_SPECIES_SLOTS:
        raise ValueError("Gen I species table must contain 190 internal slots")
    if POKEDEX_ORDER.count(0) != MISSINGNO_SLOTS:
        raise ValueError("Gen I species table must retain 39 MissingNo slots")
    official = sorted(value for value in POKEDEX_ORDER if value)
    if official != list(range(1, CANONICAL_SPECIES_COUNT + 1)):
        raise ValueError("official Gen I species must map exactly once to National Dex 1..151")


def validate_pokedex_order_source(rom: bytes, profile: str) -> None:
    validate_static_mapping()
    meta = PROFILE_POKEDEX_ORDER[profile]
    offset = meta["file_offset"]
    actual = rom[offset:offset + LEGACY_SPECIES_SLOTS]
    if actual != POKEDEX_ORDER:
        raise ValueError(f"{profile}: verified PokedexOrder bytes changed")

    first = rom.find(POKEDEX_ORDER)
    if first != offset:
        raise ValueError(f"{profile}: PokedexOrder first match moved to 0x{first:X}")
    if rom.find(POKEDEX_ORDER, first + 1) != -1:
        raise ValueError(f"{profile}: PokedexOrder is no longer unique")


def legacy_species_to_canonical(legacy_species_id: int) -> int:
    if legacy_species_id == 0:
        return 0
    if not 1 <= legacy_species_id <= LEGACY_SPECIES_SLOTS:
        raise ValueError("legacy species ID must be 0..190")
    return POKEDEX_ORDER[legacy_species_id - 1]


def build_legacy_species_map_block() -> bytes:
    validate_static_mapping()
    payload = struct.pack("<" + "H" * LEGACY_SPECIES_SLOTS, *POKEDEX_ORDER)
    crc32 = zlib.crc32(payload) & 0xFFFFFFFF
    header = struct.pack(
        MAP_HEADER_FORMAT,
        MAP_MAGIC,
        MAP_SCHEMA_VERSION,
        LEGACY_SPECIES_SLOTS,
        CANONICAL_SPECIES_COUNT,
        CANONICAL_ID_WIDTH_BITS,
        crc32,
    )
    return header + payload


def build_lookup_routine() -> bytes:
    # Runtime ABI:
    #   input  A  = legacy Gen I species ID (0..190)
    #   output DE = BLUE canonical species ID (0..151)
    #
    # The routine lives in the same metadata bank as the BLU1SPC table and is
    # entered through FarCall9, which preserves A.
    return bytes((
        0xA7,                         # and a
        0x28, 0x10,                   # jr z, .zero
        0x3D,                         # dec a
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
        0x11, 0x00, 0x00,             # .zero: ld de, 0
        0xC9,                         # ret
    ))


def inspect_legacy_species_map_block(block: bytes) -> dict[str, int | str]:
    header = block[:MAP_HEADER_SIZE]
    magic, version, slots, canonical_count, width, stored_crc = struct.unpack(
        MAP_HEADER_FORMAT, header
    )
    payload = block[MAP_HEADER_SIZE:MAP_HEADER_SIZE + slots * 2]
    return {
        "magic": magic.rstrip(b"\0").decode("ascii"),
        "schema_version": version,
        "slots": slots,
        "canonical_count": canonical_count,
        "id_width_bits": width,
        "crc32": stored_crc,
        "crc32_valid": int((zlib.crc32(payload) & 0xFFFFFFFF) == stored_crc),
    }


validate_static_mapping()
