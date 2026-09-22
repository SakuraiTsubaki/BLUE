# BLUE ROM / Save Expansion Basis

## Direct ROM evidence

Six supplied ROMs were directly hashed and header-validated.

All six report RAM size code `0x03`, corresponding to 32 KiB external cartridge RAM.

The mapper families differ:

- Japanese Ao: MBC1
- English Blue: MBC3
- French/German/Italian/Spanish Blue: MBC5

This is why BLUE cannot assume one original bank-switch implementation.

## Save evidence

No actual `.sav` sample is currently accessible.

Therefore BLUE does not claim exact player/party/box/checksum offsets for every region yet.

What can be established from the verified ROMs is the physical legacy save boundary:

- 32 KiB total SRAM
- four 8 KiB banks

The expansion design preserves that entire 32 KiB unchanged and adds twelve new 8 KiB banks under MBC5.

## Expansion target

- ROM: 8 MiB = 512 × 16 KiB
- SRAM: 128 KiB = 16 × 8 KiB
- mapper: MBC5+RAM+BATTERY

This is an original-ROM expansion. There is no GBA save conversion layer.

## Next save step

When actual saves are accessible, inspect each profile independently: file SHA-256, bank hashes, legacy checksums, player/party/dex/current-box offsets, PC box boundaries, unused/constant ranges, and regional structural differences.

Those observations will define parsers inside banks 0–3. They do not change the extension-bank boundary.
