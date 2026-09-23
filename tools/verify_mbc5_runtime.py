#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from expand_blue_rom import (
    FARCALL9_ADDR,
    LEGACY_BANK8_ADDR,
    LEGACY_BANK_HELPER_BASELINE,
    PROFILE_RUNTIME,
    RST_VECTOR_BASELINE,
    SETBANK9_ADDR,
    VBLANK9_ADDR,
    build_mbc5_runtime,
    legacy_bank8_helper,
)


def validate() -> list[str]:
    errors: list[str] = []
    cfg = json.loads((ROOT / "config" / "mbc5_runtime.json").read_text(encoding="utf-8"))

    if hashlib.sha256(RST_VECTOR_BASELINE).hexdigest() != cfg["verified_rst_vector_range"]["sha256"]:
        errors.append("RST-vector baseline hash mismatch")
    if hashlib.sha256(LEGACY_BANK_HELPER_BASELINE).hexdigest() != cfg["legacy_bank8_helper_region"]["original_sha256"]:
        errors.append("legacy helper source-region hash mismatch")
    if len(legacy_bank8_helper()) != 12:
        errors.append("LegacyBank8 helper must remain exactly 12 bytes")

    for profile, meta in PROFILE_RUNTIME.items():
        runtime = build_mbc5_runtime(meta["vblank_target"])
        if len(runtime) != 0x38:
            errors.append(f"{profile}: runtime vector image size changed")
        call = bytes((0xCD, meta["vblank_target"] & 0xFF, meta["vblank_target"] >> 8))
        if call not in runtime[VBLANK9_ADDR:]:
            errors.append(f"{profile}: VBlank wrapper does not call verified handler")

    stage = cfg["stage3"]
    entries = tuple(int(stage[key], 16) for key in (
        "farcall9_address",
        "setbank9_address",
        "vblank9_address",
        "legacy_bank8_address",
    ))
    if entries != (FARCALL9_ADDR, SETBANK9_ADDR, VBLANK9_ADDR, LEGACY_BANK8_ADDR):
        errors.append("runtime entry-point manifest mismatch")

    for profile, expected in stage["patched_executable_rom_bank_writes"].items():
        actual = PROFILE_RUNTIME[profile]["rom_bank_write_count"] - len(
            PROFILE_RUNTIME[profile]["rom_bank_data_false_positives"]
        )
        if actual != expected:
            errors.append(f"{profile}: executable bank-write count mismatch")

    if stage["normal_executable_banks"] != [0, 511]:
        errors.append("full MBC5 executable namespace is not enabled")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("BLUE MBC5 stage-3 legacy bankswitch migration: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
