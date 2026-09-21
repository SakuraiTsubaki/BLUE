# Future / Generation 10 Readiness

BLUE does not guess unreleased content counts. Readiness means the current engine and save model can accept appended content without another fundamental rewrite.

## Phase 0 — evidence baseline

- [x] six Blue-family ROMs hashed and header-validated
- [x] original cartridge save boundary established from ROM headers: 32 KiB SRAM
- [x] mapper differences recorded: MBC1 / MBC3 / MBC5
- [x] target GBA engine save storage inspected: 128 KiB sector flash
- [x] legacy GB save and GBA runtime save separated architecturally
- [ ] actual Japanese Blue save sample inspected
- [ ] actual English Blue save sample inspected
- [ ] French/German/Italian/Spanish save samples inspected and compared

## Phase 1 — engine audit

Do not assign guessed namespace capacities before these are measured.

- [ ] audit every serialized Species field width
- [ ] audit every serialized Form field / form-loss path
- [ ] audit every serialized Move field width
- [ ] audit every serialized Ability field width
- [ ] audit every serialized Item field width
- [ ] audit Type storage and type-table assumptions
- [ ] audit Pokédex flags/count calculations
- [ ] audit party/storage/trainer/encounter formats
- [ ] audit battle scripts for 8-bit truncation
- [ ] measure SaveBlock1 free bytes
- [ ] measure SaveBlock2 free bytes
- [ ] measure SaveBlock3 free bytes
- [ ] measure PokemonStorage free bytes

## Phase 2 — stable registries

- [ ] define stable species registry
- [ ] define canonical species + form mapping
- [ ] define move registry
- [ ] define ability registry
- [ ] define item registry
- [ ] define type registry
- [ ] preserve existing IDs; append/tombstone only
- [ ] generate runtime counts from registries

## Phase 3 — legacy save import

- [ ] identify exact Japanese Blue save offsets/checksums from real sample
- [ ] identify exact localized differences from real samples
- [ ] parse player / party / dex / current box
- [ ] parse all PC boxes
- [ ] validate legacy checksums
- [ ] retain unparsed bytes
- [ ] map Gen I IDs into canonical BLUE registries
- [ ] migration fixtures and round-trip provenance tests

## Phase 4 — future content gate

When new official content exists:

1. append registry entries;
2. update mechanics tables;
3. add assets/localization;
4. verify serialized widths;
5. verify compiled save-block sizes;
6. add migration only when layout changes;
7. never renumber an old persistent ID.
