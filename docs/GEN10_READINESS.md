# Generation 10 Readiness — BLUE

## Cartridge / mapper

- [x] six Blue ROM baselines verified
- [x] target MBC5 / 8 MiB ROM / 128 KiB SRAM
- [x] 9-bit SetBank9 / FarCall9
- [x] VBlank high-bit restoration
- [x] legacy executable low-bank writes made high-bit-safe
- [x] all banks 0x000-0x1FF available through BLUE's 9-bit ABI
- [x] FarCall9 preserves A/flags for canonical lookup adapters

## Expanded ROM allocation

- [x] Japanese metadata bank 0x020
- [x] international metadata bank 0x040
- [x] `BLU10ROM` metadata header
- [x] registry directory at 0x4080
- [x] legacy species map at 0x4200
- [x] runtime species lookup adapter at 0x43A0

## Species canonicalization

- [x] PokedexOrder located exactly once in all six verified ROMs
- [x] 190 internal slots / 151 official / 39 MissingNo.
- [x] canonical Gen I species IDs fixed to National Dex 1..151
- [x] 190-entry byte→16-bit mapping block
- [x] mapping CRC protection
- [x] runtime LegacySpeciesToCanonical adapter implemented
- [x] species directory points to the callable adapter

## Other IDs

- [x] expanded global IDs are 16-bit and append-only
- [x] legacy byte IDs remain source-local compatibility values
- [ ] move legacy→canonical mapping generated
- [ ] item legacy→canonical mapping generated
- [ ] type legacy→canonical mapping generated
- [ ] map/location/trainer/evolution mappings generated
- [ ] post-Gen-I official registries imported

## Save

- [x] legacy 32 KiB / 4-bank physical boundary
- [x] expansion SRAM banks 0x04-0x0F
- [x] 128 KiB save scaffold preserving first 32 KiB
- [ ] real regional save samples audited
- [ ] region-specific checksum parsers added

## Exact continuation point

Continue from **verified legacy move/item/type mappings**. Species canonicalization,
including the live runtime lookup adapter, is now a completed gate.
