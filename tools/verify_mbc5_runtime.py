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
    MBC5_RUNTIME_STUB,
    RST_VECTOR_BASELINE,
    SETBANK9_ADDR,
)


def validate() -> list[str]:
    errors: list[str] = []
    cfg = json.loads((ROOT / "config" / "mbc5_runtime.json").read_text(encoding="utf-8"))

    if hashlib.sha256(RST_VECTOR_BASELINE).hexdigest() != cfg["verified_rst_vector_range"]["sha256"]:
        errors.append("RST-vector baseline hash mismatch")
    if len(RST_VECTOR_BASELINE) != 0x38:
        errors.append("verified RST-vector range must end before 0x0038")
    if len(MBC5_RUNTIME_STUB) > len(RST_VECTOR_BASELINE):
        errors.append("runtime stub does not fit verified vector space")
    if FARCALL9_ADDR != cfg["stage1"]["farcall9_address"]:
        errors.append("FarCall9 address mismatch")
    if SETBANK9_ADDR != cfg["stage1"]["setbank9_address"]:
        errors.append("SetBank9 address mismatch")
    if len(MBC5_RUNTIME_STUB) != cfg["stage1"]["stub_bytes"]:
        errors.append("runtime stub byte count mismatch")

    for opcode in (bytes((0xEA, 0x00, 0x20)), bytes((0xEA, 0x00, 0x30))):
        if opcode not in MBC5_RUNTIME_STUB:
            errors.append(f"runtime stub missing mapper write {opcode.hex()}")

    if cfg["stage1"]["fully_supported_executable_banks"] != [0, 255]:
        errors.append("stage1 executable-bank safety boundary changed")
    if cfg["stage1"]["high_bank_range"] != [256, 511]:
        errors.append("MBC5 high-bank range changed")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("BLUE MBC5 stage-1 runtime ABI: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
