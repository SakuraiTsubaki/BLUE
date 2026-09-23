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

It records:

- schema version;
- source profile ID;
- physical metadata bank;
- first allocatable content bank;
- last MBC5 ROM bank;
- expansion SRAM bank range;
- FarCall9 / SetBank9 / VBlank9 / LegacyBank8 entry points;
- registry-directory address/count/entry size;
- the first 16 bytes of the verified source ROM SHA-256;
- header CRC32.

## Canonical registry directory

The directory starts at CPU address 0x4080 in the metadata bank.

Each 16-byte directory record has a 16-bit domain ID and a future far pointer.
Initial count is **zero** and the pointer is `0xFFFF:0xFFFF` until that
domain's real storage is allocated.

Domains:

1. species
2. form
3. move
4. item
5. ability
6. type
7. map
8. location
9. trainer class
10. evolution method

All expanded canonical IDs are 16-bit and append-only. Generation I byte IDs
remain profile-local compatibility values and are not silently reinterpreted.

This bootstrap reserves the format, not fictitious Generation 10 content.
