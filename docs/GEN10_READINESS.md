# Future / Generation 10 Readiness

BLUE does not invent unreleased content. Readiness means the GBA runtime can accept appended official content without another foundational rewrite.

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

- [x] pinned runtime species count measured: 1,573
- [x] pinned move count measured: 935
- [x] pinned ability count measured: 320
- [x] pinned item count measured: 874
- [x] BoxPokemon Species serialization audited: 11-bit bottleneck found
- [x] BoxPokemon held-item serialization audited: 10-bit bottleneck found
- [x] BoxPokemon move serialization audited: 11-bit bottleneck found
- [x] ability persistence model audited: 2-bit slot, concrete ability derived from species/form
- [x] type/Tera serialization audited: 5 bits
- [x] SaveBlock2 measured: 3,884 / 3,968 bytes, 84 bytes free
- [x] SaveBlock1 hard ceiling measured: 15,872 bytes
- [x] PokemonStorage hard ceiling measured: 35,712 bytes
- [x] SaveBlock3 hard ceiling measured: 1,624 bytes
- [x] zero-growth BoxPokemon widening designed
- [x] BoxPokemon runtime budget: Species 13 / Item 12 / Move 12 bits
- [ ] patched upstream full ARM build passes
- [ ] exact compiled SaveBlock1 free bytes measured
- [ ] exact compiled PokemonStorage free bytes measured
- [ ] exact compiled SaveBlock3 free bytes measured
- [ ] battle scripts audited for implicit 8-bit truncation
- [ ] menu/UI selectors audited for implicit 8-bit truncation
- [ ] Pokédex flags/count calculations audited

## Phase 2 — stable registries

- [ ] define stable species registry
- [ ] define canonical species + form mapping table
- [ ] define move registry
- [ ] define ability registry
- [ ] define item registry
- [ ] define type registry
- [ ] preserve existing IDs; append/tombstone only
- [ ] generate runtime counts from registries

## Phase 3 — runtime save ABI

- [x] BoxPokemon ABI v2 defined without record-size growth
- [ ] runtime save ABI marker/version integrated
- [ ] unpatched expansion-save migration fixture added
- [ ] patched save round-trip regression fixture added

## Phase 4 — legacy Blue save import

- [ ] identify exact Japanese Blue save offsets/checksums from real sample
- [ ] identify exact localized differences from real samples
- [ ] parse player / party / dex / current box
- [ ] parse all PC boxes
- [ ] validate legacy checksums
- [ ] retain unparsed bytes
- [ ] map Gen I IDs into canonical BLUE registries
- [ ] migration fixtures and round-trip provenance tests

## Future content gate

When new official content exists:

1. append canonical registry entries;
2. verify they fit the current runtime encoding budget;
3. if the budget is insufficient, change the runtime ABI explicitly rather than truncating;
4. update mechanics tables;
5. add assets/localization;
6. run the patched ARM build and save regression tests;
7. never renumber an old persistent ID.
