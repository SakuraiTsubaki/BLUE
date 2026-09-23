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
- [x] `BLU10ROM` versioned metadata header implemented
- [x] source-ROM SHA-256 prefix embedded for provenance
- [x] registry directory implemented at CPU 0x4080
- [x] species/form/move/item/ability/type/map/location/trainer/evolution domains registered
- [x] registry counts remain zero until actual data is allocated
- [x] unallocated far pointers use 0xFFFF:0xFFFF

## IDs

- [x] expanded global IDs are 16-bit
- [x] allocation is append-only
- [x] legacy Gen I byte IDs remain source-local compatibility values
- [ ] Generation I legacy→canonical mapping tables generated from verified source data
- [ ] current official post-Gen-I content registries imported
- [ ] registry records wired into runtime lookup code

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

Continue from **Generation I legacy ID → canonical 16-bit registry mappings** and
runtime lookup wiring. Do not restart mapper sizing, MBC5 migration, interrupt
migration, legacy bank-switch migration, or expansion-bank bootstrap.
