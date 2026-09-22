#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATCH = ROOT / "patches" / "pokeemerald-expansion" / "0001-widen-boxpokemon-content-ids.patch"


def load(path: str) -> dict:
    with (ROOT / path).open(encoding="utf-8") as f:
        return json.load(f)


def validate() -> list[str]:
    errors: list[str] = []
    budget = load("config/runtime_id_budget.json")
    limits = load("config/expansion_limits.json")
    engine = load("manifests/engine-base.json")

    if engine["upstream"]["baseline_ref"] != budget["source"]["ref"]:
        errors.append("runtime budget source ref disagrees with pinned engine")

    current = budget["measured_counts"]
    old = budget["pinned_engine_boxpokemon_before_blue_patch"]
    new = budget["blue_overlay_after_patch"]

    if not (current["species_num_species"] < old["species_capacity"]):
        errors.append("pinned species no longer fit the audited old BoxPokemon width")
    if not (current["items_count"] < old["held_item_capacity"]):
        errors.append("pinned items no longer fit the audited old BoxPokemon width")
    if not (current["moves_count_all"] < old["move_capacity"]):
        errors.append("pinned moves no longer fit the audited old BoxPokemon width")

    if new["save_record_growth_bytes"] != 0 or new["boxpokemon_bytes"] != 80 or new["pokemon_bytes"] != 100:
        errors.append("BLUE widening must not grow Pokemon save records")

    expected = {
        "species_capacity": 1 << new["species_bits"],
        "held_item_capacity": 1 << new["held_item_bits"],
        "move_capacity": 1 << new["move_bits"],
        "tera_type_capacity": 1 << new["tera_type_bits"],
    }
    for key, value in expected.items():
        if new[key] != value:
            errors.append(f"{key} does not match its bit width")

    runtime = limits["runtime_pinned_engine_budget"]
    if runtime["boxpokemon_abi_version"] != new["boxpokemon_abi_version"]:
        errors.append("expansion limits ABI version disagrees with runtime budget")
    for key in ("species_bits", "species_capacity", "held_item_bits", "held_item_capacity", "move_bits", "move_capacity", "tera_type_bits", "tera_type_capacity"):
        if runtime[key] != new[key]:
            errors.append(f"expansion limits {key} disagrees with runtime budget")

    text = PATCH.read_text(encoding="utf-8")
    required = [
        "u32 species:13",
        "u32 heldItem:12",
        "u32 move1:12",
        "u32 move2:12",
        "u32 move3:12",
        "u32 move4:12",
        "u32 evolutionTracker1:5",
        "u32 evolutionTracker2:5",
        "sizeof(struct BoxPokemon) == 80",
        "NUM_SPECIES <= (1 << 13)",
        "ITEMS_COUNT <= (1 << 12)",
        "MOVES_COUNT_ALL <= (1 << 12)",
    ]
    for needle in required:
        if needle not in text:
            errors.append(f"engine overlay is missing required invariant: {needle}")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("BLUE pinned-engine ID/save expansion audit: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
