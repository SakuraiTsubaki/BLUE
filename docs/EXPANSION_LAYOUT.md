# BLUE Expansion ROM Layout

## Profile-relative first expansion bank

| Profile | Legacy end | Metadata bank | First content bank |
| --- | ---: | ---: | ---: |
| ao-jp | 0x01F | 0x020 | 0x021 |
| blue-us-eu | 0x03F | 0x040 | 0x041 |
| blue-fr | 0x03F | 0x040 | 0x041 |
| blue-de | 0x03F | 0x040 | 0x041 |
| blue-it | 0x03F | 0x040 | 0x041 |
| blue-es | 0x03F | 0x040 | 0x041 |

Ordinary expanded content begins after the profile metadata bank and may extend
through MBC5 bank 0x1FF.

## Metadata services

- `0x4000`: `BLU10ROM` metadata header
- `0x4080`: registry directory
- `0x4200`: `BLU1SPC` 190-slot species byte→u16 map
- `0x43A0`: callable species adapter
- `0x4400`: `BLU1MOV` 256-code move byte→u16 map
- `0x4620`: callable move adapter

Species directory entry:

- count 151
- metadata-bank pointer to 0x43A0

Move directory entry:

- count 165
- metadata-bank pointer to 0x4620

Both adapters use the stage-4 FarCall9 ABI, which preserves A across the bank
switch and returns the canonical 16-bit ID in DE.

Other namespaces remain unallocated until their own ROM-backed mappings are
verified.

No unreleased Generation 10 content is invented.
