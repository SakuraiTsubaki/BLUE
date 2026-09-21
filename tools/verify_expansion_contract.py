#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIMITS = ROOT / "config" / "expansion_limits.json"
SAVE = ROOT / "config" / "save_schema.json"
ENGINE = ROOT / "manifests" / "engine-base.json"

MINIMUM_CAPACITY = {
    "species": 4096,
    "moves": 4096,
    "abilities": 1024,
    "items": 8192,
    "types": 64,
    "evolution_methods": 256,
}

PERSISTENT_NAMESPACES = {
    "species", "moves", "abilities", "items", "types"
}


def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def validate() -> list[str]:
    errors: list[str] = []
    limits = load(LIMITS)
    save = load(SAVE)
    engine = load(ENGINE)

    model = limits["id_model"]
    if model["persistent_id_width_bits"] != 16:
        errors.append("persistent IDs must remain 16-bit")
    if model["invalid_id"] != 0xFFFF:
        errors.append("0xFFFF must remain reserved as invalid")
    if model["renumber_existing_ids"]:
        errors.append("existing IDs must never be renumbered")
    if model["allocation"] != "append-only":
        errors.append("ID allocation must be append-only")

    form = limits["species_form_model"]
    if form["representation"] != "composite":
        errors.append("species/forms must use the canonical composite model")
    if form["species_id_width_bits"] != 16 or form["form_id_width_bits"] != 16:
        errors.append("species_id and form_id must remain 16-bit")

    namespaces = limits["namespaces"]
    for name, minimum in MINIMUM_CAPACITY.items():
        actual = namespaces[name]["capacity"]
        if actual < minimum:
            errors.append(f"{name} capacity {actual} is below future-ready minimum {minimum}")

    for name, cfg in namespaces.items():
        width = cfg["id_width_bits"]
        capacity = cfg["capacity"]
        if width != 16:
            errors.append(f"{name} ID width must be 16-bit")
        if capacity >= model["invalid_id"]:
            errors.append(f"{name} capacity collides with reserved invalid ID")

    save_ids = save["persistent_ids"]
    expected_save_fields = {
        "species_id_bits", "form_id_bits", "move_id_bits",
        "ability_id_bits", "item_id_bits", "type_id_bits"
    }
    for field in expected_save_fields:
        if save_ids.get(field) != 16:
            errors.append(f"save field {field} must be 16-bit")

    policy = save["format_policy"]
    if policy["serialize_raw_c_structs"]:
        errors.append("raw C struct serialization must stay disabled")
    if not policy["schema_version_required"] or not policy["migration_chain_required"]:
        errors.append("save versioning and migration chain are mandatory")

    target = engine["target"]
    if target["content_ceiling"] != "future":
        errors.append("engine content ceiling must remain future-facing")
    if not target["generation_number_is_not_an_abi"]:
        errors.append("generation number must not become storage ABI")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("BLUE future-generation expansion contract: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
