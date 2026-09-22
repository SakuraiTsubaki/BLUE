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
    capacity = load_json("config/capacity.json")
    limits = load_json("config/expansion_limits.json")
    storage = load_json("config/storage_baseline.json")
    remake = load_json("config/remake.json")

    if capacity["runtime"] != "original-game-boy-rom":
        errors.append("BLUE runtime must remain the original Game Boy ROM")
    if remake.get("gbaEngineDependency") is not False:
        errors.append("BLUE must not depend on a GBA/Emerald engine")

    expanded = capacity["expanded"]
    if expanded["mapper"] != "MBC5+RAM+BATTERY":
        errors.append("expanded mapper must be MBC5+RAM+BATTERY")
    if expanded["rom_bytes"] != 0x800000 or expanded["rom_banks"] != 512:
        errors.append("expanded ROM must be 8 MiB / 512 banks")
    if expanded["sram_bytes"] != 0x20000 or expanded["sram_banks"] != 16:
        errors.append("expanded SRAM must be 128 KiB / 16 banks")

    if limits["rom"]["bank_id_bits"] != 9:
        errors.append("MBC5 ROM bank namespace must expose 9 bits")
    if limits["persistent_id_contract"]["minimum_width_bits"] < 16:
        errors.append("expanded persistent IDs must be at least 16-bit")

    legacy = storage["legacy_blue"]["battery_sram"]
    if (legacy["raw_bytes"], legacy["bank_bytes"], legacy["bank_count"]) != (32768, 8192, 4):
        errors.append("legacy save boundary must stay 32 KiB / four 8 KiB banks")

    with (ROOT / "research" / "blue-rom-baseline.csv").open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 6:
        errors.append("expected all six verified BLUE ROM profiles")
    for row in rows:
        if row["ram_size_code"] != "0x03" or int(row["ram_bytes"]) != 32768:
            errors.append(f"{row['release_id']}: unexpected legacy SRAM boundary")
        if row["checksums_valid"].lower() != "true":
            errors.append(f"{row['release_id']}: ROM checksum baseline is not valid")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("BLUE original-ROM Generation-10 expansion contract: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
