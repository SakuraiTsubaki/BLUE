# ROM / Save Expansion Basis

## Why this document exists

BLUE is a remake/modernization project. Expansion must start from what the original Blue cartridges and saves actually do, then map that into the Generation III runtime engine.

The project therefore separates three things:

1. original Blue ROM/cartridge constraints;
2. original Blue save/SRAM import constraints;
3. GBA runtime save constraints.

## Direct ROM evidence

Six locally supplied Blue-family ROMs were read byte-for-byte.

| Release | ROM | Mapper | Battery RAM |
| --- | ---: | --- | ---: |
| Pocket Monsters Ao (Japan) | 512 KiB | MBC1+RAM+BATTERY | 32 KiB |
| Blue (USA/Europe) | 1 MiB | MBC3+RAM+BATTERY | 32 KiB |
| Blue (France) | 1 MiB | MBC5+RAM+BATTERY | 32 KiB |
| Blue (Germany) | 1 MiB | MBC5+RAM+BATTERY | 32 KiB |
| Blue (Italy) | 1 MiB | MBC5+RAM+BATTERY | 32 KiB |
| Blue (Spain) | 1 MiB | MBC5+RAM+BATTERY | 32 KiB |

Every cartridge header reports RAM size code `0x03`, i.e. 32 KiB external RAM. Every checked ROM has a valid header/global checksum.

Exact hashes and header fields are in `research/blue-rom-baseline.csv`.

### Consequence

The original save boundary is **32 KiB raw battery SRAM**. Mapper differences mean the code used to select RAM banks differs by release family, so mapper behavior and logical save layout must not be conflated.

## Save evidence status

No `.sav` is accessible in the active runtime for this investigation. Therefore:

- we do **not** claim that exact offsets in Japanese/French/German/Italian/Spanish save samples were inspected;
- we do **not** claim regional save files are byte-identical;
- exact regional offsets/checksums remain an open verification item.

The repository now includes `tools/analyze_blue_inputs.py` so the actual files can be analyzed without changing this architecture again.

## Source cross-check for Red/Blue save organization

The public `pret/pokered` source was used only as supplementary evidence, not as a substitute for the missing save samples.

Observed in `ram/sram.asm` and `engine/menus/save.asm`:

- SRAM is banked;
- game/current-box data has a checksum;
- PC boxes span multiple SRAM banks;
- box banks have aggregate and per-box checksums;
- the clear-save path fills all four SRAM banks with `0xFF`.

This is consistent with the 32 KiB / four-bank cartridge header boundary.

## GBA runtime target evidence

The pinned `pokeemerald-expansion` source uses the Emerald sector save system.

From `include/save.h` and `src/save.c`:

- sector size: 4096 bytes;
- sector count: 32;
- total flash: 131072 bytes (128 KiB);
- per-sector normal data: 3968 bytes;
- SaveBlock3 chunk: 116 bytes;
- footer: 12 bytes;
- main save slot: 14 sectors;
- two alternating main save slots;
- sectors 28-31 are special-purpose sectors.

This is a very different persistence model from Game Boy SRAM.

## BLUE migration architecture

Do not stretch a Gen I `.sav` into the new runtime format.

```text
32 KiB raw GB SRAM
  ├─ identity (region / ROM hash)
  ├─ bank image preservation
  ├─ legacy checksum validation
  └─ parsed legacy records
             ↓
      canonical import model
             ↓
     GBA runtime structures
             ↓
128 KiB sector-based runtime save
```

The original file remains provenance. The runtime save is a migration target.

## Implication for 10th-generation readiness

The future-generation problem is not solved by inventing huge array lengths.

The correct order is:

1. audit actual upstream ID field widths;
2. audit every serialized Species/Form/Move/Ability/Item field;
3. measure SaveBlock1/2/3 and PokémonStorage free space;
4. remove 8-bit truncation and generation-count array bounds;
5. create stable registry mappings;
6. then assign capacity budgets backed by compiled-size/save-space measurements.

Until that audit is complete, fixed capacity numbers such as "8192 species" are not architectural facts and are intentionally not used by BLUE.

## Next verification

The next save-specific step is to run the analyzer against each corresponding `.sav` and record:

- exact size/hash;
- 8 KiB bank hashes;
- blank/unused ranges;
- checksums;
- player/party/current box/PC box boundaries;
- regional differences;
- whether saves are interchangeable or only structurally related.

After that, implement the legacy parser and migration fixtures.
