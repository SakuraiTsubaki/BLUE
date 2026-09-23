# BLUE Original-ROM Expansion Architecture

## Runtime

BLUE remains a Game Boy program. GBA/Emerald is not the runtime.

Target cartridge envelope:

- MBC5+RAM+BATTERY
- 8 MiB ROM = 512 × 16 KiB banks
- 128 KiB SRAM = 16 × 8 KiB banks
- 16-bit expanded content IDs

## Source families

- Japanese Ao: 512 KiB, MBC1, 32 KiB SRAM
- English Blue: 1 MiB, MBC3, 32 KiB SRAM
- French/German/Italian/Spanish Blue: 1 MiB, MBC5, 32 KiB SRAM

Japanese legacy ROM banks are 0x000-0x01F. International legacy ROM banks are
0x000-0x03F. Expansion occupies the remaining banks through 0x1FF.

## Save preservation

SRAM banks 0x00-0x03 remain byte-for-byte legacy data.
Banks 0x04-0x0F are BLUE's versioned extension area.

## MBC5 runtime ABI

BLUE uses fixed-ROM hooks verified against all six supplied ROMs:

- `FarCall9 = 0x0000`
- `SetBank9 = 0x0010`
- `VBlank9 = 0x0020`
- `LegacyBank8 = 0x0043`

Bank low byte is written to 0x2000. Bank bit 8 is written to 0x3000 and tracked
separately in HRAM.

### Interrupt safety

VBlank is wrapped so the interrupted high bank bit is saved and restored.
Timer, Serial and Joypad were audited and do not require ROM-bank restoration
changes.

### Legacy synchronous switches

Direct ROM analysis found 89/91 exact `EA 00 20` sequences. Three per profile
are bank-8 data, not executable writes.

The executable instructions are replaced in-place with the same-size
`CALL 0x0043`:

- Japanese Ao: 86
- each international Blue: 88

LegacyBank8 preserves A and flags, clears MBC5 bank bit 8 and its BLUE shadow,
then performs the original low-byte bank write.

This opens all MBC5 banks 0x000-0x1FF to expanded executable code without
reinterpreting legacy one-byte bank fields.

## Expanded data model

Legacy Gen I byte IDs remain source-local values. New records use 16-bit IDs
for species, forms, moves, items, abilities, types, maps/locations, trainer
classes and evolution methods.

The next layer is allocation: reserve expansion banks for a versioned BLUE
metadata header and canonical ID registries, then map each source profile's
legacy IDs into those registries.

Generation 10 data itself is not guessed; only the structural namespace and
storage envelope are reserved.
