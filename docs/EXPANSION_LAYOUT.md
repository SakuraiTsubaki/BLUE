# BLUE Expansion ROM Layout

## Profile-relative first expansion bank

BLUE does not overwrite retail content to create its registry root.

| Profile | Legacy end | Metadata bank | First content bank |
| --- | ---: | ---: | ---: |
| ao-jp | 0x01F | 0x020 | 0x021 |
| blue-us-eu | 0x03F | 0x040 | 0x041 |
| blue-fr | 0x03F | 0x040 | 0x041 |
| blue-de | 0x03F | 0x040 | 0x041 |
| blue-it | 0x03F | 0x040 | 0x041 |
| blue-es | 0x03F | 0x040 | 0x041 |

The metadata bank is reserved for BLUE format metadata and registry roots.
Ordinary expanded content begins in the following bank and may extend through
MBC5 bank 0x1FF.

## Header

The metadata bank begins at CPU address 0x4000 with a 64-byte little-endian
header whose magic is ASCII `BLU10ROM`.

Schema 2 records:

- source profile ID;
- physical metadata bank;
- first allocatable content bank;
- last MBC5 ROM bank;
- expansion SRAM bank range;
- FarCall9 / SetBank9 / VBlank9 / LegacyBank8 entry points;
- registry-directory address/count/entry size;
- legacy-species mapping address `0x4200`;
- the first 16 bytes of the verified source ROM SHA-256;
- header CRC32.

## Canonical registry directory

The directory begins at CPU address `0x4080`.

Each 16-byte directory record contains a 16-bit domain ID and a future far
pointer.

The species namespace now reserves canonical IDs `1..151`, grounded in the
verified Gen I PokedexOrder table. Species record storage itself remains
unallocated. Other domains remain count 0 until real data is imported.

Unallocated far pointers remain `0xFFFF:0xFFFF`.

## Legacy species map

CPU address `0x4200` contains the versioned `BLU1SPC` mapping block:

- 190 Generation I internal species slots;
- 151 official species mapped to canonical National Dex IDs 1..151;
- 39 MissingNo. slots mapped to canonical ID 0;
- 16-bit little-endian canonical IDs;
- payload CRC32.

This is verified against all six supplied Blue-family ROMs before expansion.

Generation 10 capacity remains structural. No unreleased species are invented.
