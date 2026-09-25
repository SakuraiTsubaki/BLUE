# Generation 10 Readiness — BLUE

## Cartridge / mapper

- [x] six Blue ROM baselines verified
- [x] target MBC5 / 8 MiB ROM / 128 KiB SRAM
- [x] 9-bit SetBank9 / FarCall9
- [x] VBlank high-bit restoration
- [x] legacy executable low-bank writes high-bit-safe
- [x] all banks 0x000-0x1FF available through BLUE's 9-bit ABI
- [x] FarCall9 preserves A/flags for canonical adapters

## Species canonicalization

- [x] PokedexOrder verified in all six ROMs
- [x] 190 internal slots / 151 official / 39 MissingNo.
- [x] canonical species IDs 1..151
- [x] mapping block at 0x4200
- [x] runtime adapter at 0x43A0

## Move canonicalization

- [x] move table verified at 0x38000 / bank 0x0E in all six ROMs
- [x] 165 records × 6 bytes
- [x] record ID bytes verified as 0x01..0xA5 in every profile
- [x] Japanese/international one-byte Blizzard effect difference recorded
- [x] canonical move IDs 1..165 fixed to verified legacy IDs
- [x] full 256-byte-domain → u16 mapping block installed at 0x4400
- [x] runtime move adapter installed at 0x4620
- [x] move directory points to callable adapter

## Other IDs

- [x] expanded global IDs are 16-bit and append-only
- [x] legacy byte IDs remain source-local compatibility values
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

Continue from **verified legacy item and type mappings**. Species and move
canonicalization, including runtime adapters, are completed gates.
