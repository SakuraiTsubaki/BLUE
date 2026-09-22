# BLUE Original-ROM Expansion Policy

BLUE is not a GBA remake runtime.

## Preserve

- each verified original ROM as independent provenance;
- Japanese original as the master reference;
- original story, maps, scripts, events, graphics, audio, and version differences;
- original 32 KiB save bytes during migration;
- original SGB capability flag.

## Expand

- cartridge mapper capability to MBC5 where needed;
- ROM address space to 8 MiB;
- battery SRAM to 128 KiB;
- new global content IDs to 16-bit;
- far references to cover all 512 ROM banks.

## Compatibility

Legacy Gen I structures are not silently reinterpreted as widened structures.
Compatibility adapters translate legacy byte IDs into expanded registries.

## Future data

Only verified official content is added. Generation 10 capacity is structural; unreleased content is not invented.
