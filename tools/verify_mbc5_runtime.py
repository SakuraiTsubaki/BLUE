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
    H_CURRENT_ROM_BANK_HIGH,
    H_LOADED_ROM_BANK_LOW,
    PROFILE_RUNTIME,
    RST_VECTOR_BASELINE,
    SETBANK9_ADDR,
    VBLANK9_ADDR,
    build_mbc5_runtime,
)


def validate() -> list[str]:
    errors: list[str] = []
    cfg = json.loads((ROOT / "config" / "mbc5_runtime.json").read_text(encoding="utf-8"))

    if hashlib.sha256(RST_VECTOR_BASELINE).hexdigest() != cfg["verified_rst_vector_range"]["sha256"]:
        errors.append("RST-vector baseline hash mismatch")
    if len(RST_VECTOR_BASELINE) != 0x38:
        errors.append("verified RST-vector range must end before 0x0038")

    for profile, meta in PROFILE_RUNTIME.items():
        runtime = build_mbc5_runtime(meta["vblank_target"])
        if len(runtime) != 0x38:
            errors.append(f"{profile}: runtime vector image size changed")
        call = bytes((0xCD, meta["vblank_target"] & 0xFF, meta["vblank_target"] >> 8))
        if call not in runtime[VBLANK9_ADDR:]:
            errors.append(f"{profile}: VBlank wrapper does not call verified handler")

    stage = cfg["stage2"]
    if (stage["farcall9_address"], stage["setbank9_address"], stage["vblank9_address"]) != (
        FARCALL9_ADDR, SETBANK9_ADDR, VBLANK9_ADDR
    ):
        errors.append("runtime entry-point manifest mismatch")

    if cfg["hram"]["legacy_loaded_rom_bank_low"] != f"0xFF{H_LOADED_ROM_BANK_LOW:02X}":
        errors.append("legacy low-bank HRAM address mismatch")
    if cfg["hram"]["blue_current_rom_bank_high"] != f"0xFF{H_CURRENT_ROM_BANK_HIGH:02X}":
        errors.append("BLUE high-bank HRAM address mismatch")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("BLUE MBC5 stage-2 VBlank bank-state ABI: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
