# Engine ID / Save Audit — 10th-generation readiness

Pinned engine: `rh-hideout/pokeemerald-expansion@75b806a3ab57a81ff1eb6179288981f0b3cc3050`.

This audit is source- and layout-driven. It does not guess Generation 10 content.

## Current pinned counts

The pinned constants evaluate to:

| Namespace | Current count |
| --- | ---: |
| Runtime species/form-species | 1,573 |
| Moves (including Z/Max move namespace) | 935 |
| Abilities | 320 |
| Items | 874 |
| Types including `TYPE_NONE` | 21 |

## Actual persistent bottleneck

The engine already uses 16-bit-capable enum storage in many runtime/save structures, but the encrypted `BoxPokemon` payload compresses three important IDs:

| Field | Pinned width | Capacity | Headroom at pin |
| --- | ---: | ---: | ---: |
| Species/form-species | 11 bit | 2,048 | 475 |
| Held item | 10 bit | 1,024 | 150 |
| Move | 11 bit | 2,048 | 1,113 |
| Tera type | 5 bit | 32 | 11 |

This is the first hard limit that would force a save-format rewrite if left unchanged.

The ability itself is **not** serialized as a 320-valued ability ID in `BoxPokemon`; the mon stores a 2-bit ability slot and derives the concrete ability from its species/form data.

## BLUE overlay

`patches/pokeemerald-expansion/0001-widen-boxpokemon-content-ids.patch` consumes existing spare bits rather than growing the record:

| Field | BLUE width | Capacity |
| --- | ---: | ---: |
| Species/form-species | 13 bit | 8,192 |
| Held item | 12 bit | 4,096 |
| Move | 12 bit | 4,096 |
| Tera type | 5 bit | 32 |

The evolution tracker remains 5 + 5 bits and all hyper-training bits remain present.

### Save-size invariant

The patch enforces these compile-time invariants:

- `sizeof(PokemonSubstruct0) == 12`
- `sizeof(PokemonSubstruct1) == 12`
- `sizeof(BoxPokemon) == 80`

Therefore each full `Pokemon` remains 100 bytes and PC storage does not expand just because IDs were widened.

## Why 13/12/12

These are not speculative content-count estimates. They are the **largest useful widths that fit the existing 12-byte secure substructures while preserving the currently used tracker/training fields**.

The canonical BLUE registry still uses at least 16-bit IDs. The narrower values above are the pinned GBA runtime encoding budget.

## Forms

The pinned engine represents many forms as distinct `enum Species` IDs. BLUE does not adopt that as its canonical identity model.

BLUE keeps:

```text
(species_id, form_id)  -> registry -> runtime form-species ID
```

This lets save/import/reference data retain a stable species/form identity while the GBA engine uses its existing form tables.

## Save-sector audit

Pinned Emerald-sector layout:

- payload per sector: 3,968 bytes
- SaveBlock2: `0xF2C` = 3,884 bytes → **84 bytes free**
- SaveBlock1 hard ceiling: 4 × 3,968 = **15,872 bytes**
- PokémonStorage hard ceiling: 9 × 3,968 = **35,712 bytes**
- SaveBlock3 hard ceiling: 14 × 116 = **1,624 bytes**

Actual free bytes for SaveBlock1, PokémonStorage and SaveBlock3 depend on compile-time configuration. BLUE therefore does not spend those bytes until the patched build reports/validates them.

## Compatibility

The secure substructure bit layout changes even though its byte size does not.

- Original Blue GB SRAM is unaffected; it is imported through the legacy parser.
- Saves produced by unpatched pokeemerald-expansion must not be silently interpreted as BLUE ABI v2.
- BLUE runtime saves must carry/derive a runtime ABI version before public save compatibility is declared stable.

## Build gate

`.github/workflows/engine-expansion.yml` checks out the exact pinned upstream, applies the BLUE patch, installs the same ARM GCC/binutils family used by upstream CI, and builds Emerald.

A passing build proves both that the overlay applies to the pinned source and that the compile-time layout/capacity assertions hold.
