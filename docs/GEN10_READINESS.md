# Generation 10 Readiness — BLUE

Readiness means reserving enough address/ID/storage structure before future official content arrives.

## Cartridge

- [x] six Blue ROM baselines verified
- [x] source mapper families identified: MBC1 / MBC3 / MBC5
- [x] target mapper selected: MBC5
- [x] target ROM size selected: 8 MiB / 512 banks
- [x] target SRAM selected: 128 KiB / 16 banks
- [x] Japanese original ROM preservation range defined
- [x] international original ROM preservation range defined
- [x] mapper-write byte-pattern census recorded
- [ ] mapper-write hits classified by executable control flow
- [ ] MBC1 -> MBC5 compatibility routines implemented
- [ ] MBC3 -> MBC5 compatibility routines implemented
- [ ] 9-bit MBC5 far-bank switch routine implemented and tested

## IDs

- [x] new global species ID: 16-bit
- [x] new form ID: 16-bit
- [x] new move ID: 16-bit
- [x] new item ID: 16-bit
- [x] new ability ID: 16-bit
- [x] new type ID: 16-bit
- [x] new map/location/trainer/evolution IDs: 16-bit
- [x] legacy Gen I byte IDs kept as source-local compatibility values

## Save

- [x] physical legacy save boundary: 32 KiB / 4 banks
- [x] expansion boundary: banks 0x04–0x0F
- [x] 128 KiB save scaffold defined
- [x] first 32 KiB preserved byte-for-byte by expansion tool
- [ ] Japanese Ao real save sample audited
- [ ] English Blue real save sample audited
- [ ] French/German/Italian/Spanish real save samples audited
- [ ] region-specific legacy checksum parsers added

## Content

Generation 10 species/moves/items/abilities are not guessed.

When official data exists, append it into the widened registries and allocate ROM/SRAM records without renumbering existing expanded IDs.
