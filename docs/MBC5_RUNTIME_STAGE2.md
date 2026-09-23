# BLUE MBC5 Runtime Stage 2 — VBlank-safe high bank state

Stage 1 introduced 9-bit MBC5 bank writes in fixed ROM0. Stage 2 makes the asynchronous VBlank path preserve bank bit 8.

## State

- legacy low bank byte: `hLoadedROMBank = 0xFFB8`
- BLUE high bank bit: `0xFFFA`

The low byte remains compatible with the original game. BLUE stores only MBC5 bit 8 in the new HRAM byte.

## VBlank wrapper

Each verified ROM has a different original VBlank entry/exit address. The expansion tool pins those addresses by ROM hash.

The interrupt vector at `0x0040` is redirected to `VBlank9 = 0x0020`.

VBlank9:

1. clears hardware MBC5 ROM bank bit 8;
2. calls the original VBlank handler;
3. reads BLUE's saved high bit from HRAM;
4. restores MBC5 ROM bank bit 8;
5. executes `RETI`.

The original handler's final `RETI` is changed to `RET`, so the wrapper owns the final interrupt return.

The original handler continues to save and restore the low bank byte exactly as before.

## Verified profile addresses

| Profile | Original VBlank | Original RETI |
| --- | ---: | ---: |
| ao-jp | 0x200A | 0x208E |
| blue-us-eu | 0x2024 | 0x20AE |
| blue-fr | 0x2020 | 0x20AA |
| blue-de | 0x2024 | 0x20AE |
| blue-it | 0x2024 | 0x20AE |
| blue-es | 0x2023 | 0x20AD |

The patcher refuses to proceed if the expected vector or RETI byte does not match.

## Remaining restriction

VBlank is now high-bit-safe, but synchronous legacy bank-switch helpers still only understand an 8-bit bank number.

Therefore code in banks `0x100–0x1FF` is still restricted: it must not enter an unpatched legacy bank-switch path that expects to restore only the low byte.

Next work is the executable `0x2000` write-path migration.
