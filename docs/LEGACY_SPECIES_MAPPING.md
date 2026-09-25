# Gen I legacy species ID → BLUE canonical species ID

BLUE keeps original Generation I internal species IDs as source-local compatibility values.

They are **not** used as the expanded global species namespace.

## Direct ROM evidence

The 190-byte Gen I `PokedexOrder` table was found exactly once in each of the six verified ROMs.

| Profile | File offset | ROM bank | CPU address |
| --- | ---: | ---: | ---: |
| ao-jp | 0x42784 | 0x10 | 0x6784 |
| blue-us-eu | 0x41024 | 0x10 | 0x5024 |
| blue-fr | 0x40FAA | 0x10 | 0x4FAA |
| blue-de | 0x40F96 | 0x10 | 0x4F96 |
| blue-it | 0x40FB6 | 0x10 | 0x4FB6 |
| blue-es | 0x40FB4 | 0x10 | 0x4FB4 |

The table bytes are identical across all six profiles.

SHA-256:

`878d381c0c488f05629c90f4bfbf046c6c029779adfa98f81f78aa9cb62246c6`

The 190 internal slots contain:

- 151 official species mappings;
- 39 zero entries corresponding to MissingNo. slots.

The 151 nonzero values are exactly the set **1 through 151, each once**.

## Canonical rule

For Generation I species:

```text
BLUE canonical species ID = official National Pokédex number
```

So canonical IDs `1..151` are grounded in the verified retail ROM mapping rather than in the internal Gen I species byte order.

`legacy_species_id = 0` and the 39 MissingNo. slots map to canonical ID `0` and are not silently promoted to official species.

Forms remain a separate 16-bit namespace.

## ROM metadata block

Each expanded ROM stores a versioned mapping block in its profile-relative metadata bank at CPU address `0x4200`.

Block:

- magic: `BLU1SPC`
- schema version: 1
- source slots: 190
- canonical official species count: 151
- ID width: 16 bit
- CRC32 of mapping payload
- 190 little-endian 16-bit canonical IDs

This means old party/box/trainer species bytes can be translated deterministically before expanded species data is introduced.
