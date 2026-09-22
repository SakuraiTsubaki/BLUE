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

French, German, Italian, and Spanish inputs are already MBC5+RAM+BATTERY:

- 1 MiB
- 64 ROM banks
- 32 KiB SRAM

Legacy ROM banks: `0x000–0x03F`.

## Preservation

The ROM expansion tool copies the complete legacy image and changes only cartridge type, ROM size code, RAM size code, header checksum, and global checksum.

New banks are initialized to `0xFF`.

For saves, SRAM banks `0x00–0x03` are copied byte-for-byte. Banks `0x04–0x0F` are new expansion storage.

## Mapper migration

Changing a cartridge header is not enough for MBC1/MBC3 source code.

A direct byte-pattern census found:

- Japanese Ao: 89 exact `LD (0x2000),A`, 19 exact `LD (0x4000),A`, 25 exact `LD (0x6000),A`;
- English/international family: 91 exact `LD (0x2000),A`, 19 exact `LD (0x4000),A`, 25 exact `LD (0x6000),A`;
- no verified ROM contains an exact `LD (0x3000),A` pattern.

These are byte-pattern counts, not proof that every hit is executable.

Before using ROM bank `0x100` or above, BLUE must introduce a verified far-bank routine that writes both MBC5 ROM-bank registers:

- low 8 bits: `0x2000–0x2FFF`;
- ninth bit: `0x3000–0x3FFF`.

For Ao/English profiles, every legacy mapper-control path must be classified before mapper migration is declared complete.

## Expanded IDs

Legacy Gen I byte IDs remain source-local IDs.

New expansion records use 16-bit IDs for species, form, move, item, ability, type, map/location, trainer class, and evolution method.

A far ROM reference stores bank in 16 bits (valid `0x000–0x1FF`) plus a 16-bit CPU address.

## Generation 10

No unreleased count is guessed.

8 MiB ROM + 128 KiB SRAM + 16-bit content IDs provide the structural envelope. Actual tables are appended only when official data exists.
