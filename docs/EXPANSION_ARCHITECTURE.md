# BLUE Original-ROM Expansion Architecture

## Runtime

BLUE remains a Game Boy program. GBA/Emerald is not the runtime.

All verified source ROMs are migrated toward one cartridge capability target:

- MBC5+RAM+BATTERY
- 8 MiB ROM
- 128 KiB SRAM

## Source families

### Japanese Ao

- 512 KiB
- MBC1+RAM+BATTERY
- 32 ROM banks
- 32 KiB SRAM

Legacy ROM banks: `0x000–0x01F`.

### English Blue

- 1 MiB
- MBC3+RAM+BATTERY
- 64 ROM banks
- 32 KiB SRAM

Legacy ROM banks: `0x000–0x03F`.

### Continental European Blue

French, German, Italian, and Spanish inputs are already MBC5+RAM+BATTERY with 64 ROM banks and 32 KiB SRAM.

## Preservation boundary

The complete legacy image is preserved except:

1. `0x0000–0x001A`: verified unused RST-vector space used by BLUE's MBC5 trampoline;
2. cartridge mapper/ROM-size/RAM-size header fields;
3. header/global checksum fields.

The remainder of the original ROM bytes are unchanged. New banks are initialized to `0xFF`.

SRAM banks `0x00–0x03` remain the byte-for-byte legacy save area. Banks `0x04–0x0F` are expansion storage.

## Mapper control-flow census

Direct ROM analysis grouped mapper writes by 16 KiB ROM bank.

Japanese Ao:

- `0x2000`: bank 0 = 84, bank 1 = 2, bank 8 = 3
- `0x4000`: bank 0 = 3, bank 1 = 1, bank 15 = 1, bank 28 = 14
- `0x6000`: bank 1 = 3, bank 28 = 22

Every international ROM has the same distribution:

- `0x2000`: 86 / 2 / 3 in banks 0 / 1 / 8
- `0x4000`: 3 / 1 / 1 / 14 in banks 0 / 1 / 15 / 28
- `0x6000`: 3 / 22 in banks 1 / 28

Bank 28 is the save/PC-box SRAM control cluster. The four retail continental MBC5 ROMs execute the same distribution, giving a real retail MBC5 compatibility reference for the international code family.

## 9-bit MBC5 ABI

BLUE installs a 27-byte fixed-ROM trampoline in the verified unused RST-vector region.

- `FarCall9 = 0x0000`
- `SetBank9 = 0x0010`
- bank low byte → `0x2000`
- bank bit 8 → `0x3000`

See `docs/MBC5_RUNTIME_STAGE1.md`.

Stage 1 treats banks 0x000-0x0FF as normal executable banks. Banks 0x100-0x1FF are reserved until interrupt/bank-state restoration is upgraded from 8 to 9 bits; controlled interrupt-safe access is possible through the new ABI.

## Expanded IDs

Legacy Gen I byte IDs remain source-local IDs.

New expansion records use 16-bit IDs for species, form, move, item, ability, type, map/location, trainer class, and evolution method.

## Generation 10

No unreleased count is guessed.

The current envelope is 8 MiB ROM + 128 KiB SRAM + 16-bit content IDs. Actual tables are appended only when official data exists.
