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

## Metadata header

CPU `0x4000`: 64-byte `BLU10ROM` schema-2 header.

It records source provenance, expansion ranges, runtime entry points, registry
directory shape, and the legacy species map address `0x4200`.

## Registry directory

CPU `0x4080`, 10 entries × 16 bytes.

The species entry is now live:

- canonical count: 151;
- flags: namespace-reserved + callable-adapter;
- bank: profile metadata bank (0x020 or 0x040);
- address: `0x43A0`.

Other domains remain unallocated until their verified mappings/data are added.

## Legacy species mapping

CPU `0x4200`: 400-byte `BLU1SPC` block.

Its 190 little-endian 16-bit entries map the original internal species byte
namespace to canonical IDs. The 151 official slots map to National Dex
1..151; 39 MissingNo. slots map to 0.

## Runtime species adapter

CPU `0x43A0`: `LegacySpeciesToCanonical`.

Input A is the original Gen I species ID. Output DE is the canonical 16-bit
species ID. It is called through `FarCall9`, whose stage-4 ABI preserves A
and flags while switching banks.

This makes the species canonicalization a live runtime service rather than a
manifest-only mapping.

No unreleased Generation 10 species are invented.
