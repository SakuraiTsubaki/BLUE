# Generation 10 Readiness — BLUE

## Cartridge / mapper

- [x] six Blue ROM baselines verified
- [x] source mapper families identified: MBC1 / MBC3 / MBC5
- [x] target mapper: MBC5
- [x] target ROM: 8 MiB / 512 banks
- [x] target SRAM: 128 KiB / 16 banks
- [x] 9-bit SetBank9 / FarCall9 implemented
- [x] VBlank high-bit restoration implemented
- [x] every exact legacy 0x2000 write classified as executable or data
- [x] legacy executable low-bank writes made high-bit-safe
- [x] all banks 0x000-0x1FF available through BLUE's 9-bit ABI

## Expanded ROM allocation

- [x] Japanese metadata bank reserved at 0x020
- [x] international metadata bank reserved at 0x040
- [x] first ordinary content banks set to 0x021 / 0x041
- [x] `BLU10ROM` metadata header schema 2 implemented
- [x] registry directory implemented at CPU 0x4080
- [x] legacy species mapping block implemented at CPU 0x4200
- [x] source-ROM SHA-256 prefix embedded for provenance

## Species canonicalization

- [x] PokedexOrder located exactly once in all six verified ROMs
- [x] all six PokedexOrder tables byte-identical
- [x] 190 internal slots verified
- [x] 151 official species verified
- [x] 39 MissingNo. slots preserved as unmapped/0
- [x] canonical Generation I species IDs fixed to National Dex 1..151
- [x] 190-entry legacy byte ID → 16-bit canonical species map generated
- [x] mapping payload versioned and CRC-protected in expanded ROM
- [ ] runtime lookup routine wired to consume BLU1SPC mapping block

## Other IDs

- [x] expanded global IDs are 16-bit and append-only
- [x] legacy Gen I byte IDs remain source-local compatibility values
- [ ] move legacy→canonical mapping generated
- [ ] item legacy→canonical mapping generated
- [ ] type legacy→canonical mapping generated
- [ ] map/location/trainer/evolution mappings generated
- [ ] post-Gen-I official registries imported

## Save

- [x] physical legacy boundary: 32 KiB / four banks
- [x] extension boundary: banks 0x04-0x0F
- [x] 128 KiB save scaffold
- [x] first 32 KiB preserved byte-for-byte
- [ ] Japanese Ao real save sample audited
- [ ] English Blue real save sample audited
- [ ] French/German/Italian/Spanish real save samples audited
- [ ] region-specific legacy checksum parsers added

## Exact continuation point

Continue from the **runtime species lookup adapter**, then the verified legacy
move/item/type mappings. Do not restart mapper, save sizing, MBC5, VBlank,
legacy bank-switch, expansion-bank, or Gen I species mapping work.
