#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_json(path: str) -> dict:
    with (ROOT / path).open(encoding="utf-8") as f:
        return json.load(f)


def validate() -> list[str]:
    errors: list[str] = []

    limits = load_json("config/expansion_limits.json")
    save = load_json("config/save_schema.json")
    storage = load_json("config/storage_baseline.json")

    contract = limits["persistent_id_contract"]
    if contract["minimum_width_bits"] < 16:
        errors.append("persistent IDs must be at least 16-bit")
    if contract["reserved_invalid_id"] != 0xFFFF:
        errors.append("0xFFFF must remain reserved invalid ID")
    if contract["allocation"] != "append-only" or contract["renumber_existing_ids"]:
        errors.append("persistent ID allocation must remain append-only without renumbering")

    ns = limits["namespace_policy"]
    if ns["fixed_preallocated_generation_sized_tables"]:
        errors.append("generation-sized fixed tables must remain disabled")
    if ns["capacity_numbers_before_engine_audit"] != "forbidden":
        errors.append("capacity numbers must not be guessed before engine audit")

    legacy = storage["legacy_blue"]["battery_sram"]
    if legacy["raw_bytes"] != 32768 or legacy["bank_bytes"] != 8192 or legacy["bank_count"] != 4:
        errors.append("legacy Blue SRAM boundary must remain 32 KiB / four 8 KiB banks")

    runtime = storage["target_gba_engine"]["flash"]
    if runtime["sector_size"] * runtime["sector_count"] != 131072:
        errors.append("GBA target flash must resolve to 128 KiB")
    if runtime["sector_data_bytes"] + runtime["saveblock3_chunk_bytes"] + runtime["sector_footer_bytes"] != runtime["sector_size"]:
        errors.append("GBA sector components do not add up to one sector")

    policy = storage["blue_policy"]
    if policy["extend_legacy_gb_save_in_place"]:
        errors.append("legacy GB save must not be extended in place")

    if save["legacy_import"]["expected_bytes_from_rom_header"] != legacy["raw_bytes"]:
        errors.append("save schema legacy size disagrees with ROM-derived SRAM size")
    if save["runtime_target"]["flash_bytes"] != runtime["sector_size"] * runtime["sector_count"]:
        errors.append("runtime save schema disagrees with engine storage baseline")

    with (ROOT / "research" / "blue-rom-baseline.csv").open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 6:
        errors.append("expected six verified Blue ROM baseline rows")
    for row in rows:
        if row["ram_size_code"] != "0x03" or int(row["ram_bytes"]) != 32768:
            errors.append(f"{row['release_id']}: unexpected cartridge RAM boundary")
        if row["checksums_valid"].lower() != "true":
            errors.append(f"{row['release_id']}: ROM checksums are not marked valid")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("BLUE ROM/save-grounded expansion contract: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
