# Generation 10 Readiness — BLUE

## Cartridge / mapper

- [x] six Blue ROM baselines verified
- [x] source mapper families identified: MBC1 / MBC3 / MBC5
- [x] target mapper: MBC5
- [x] target ROM: 8 MiB / 512 banks
- [x] target SRAM: 128 KiB / 16 banks
- [x] Japanese and international preservation ranges defined
- [x] mapper writes grouped by ROM bank and role
- [x] all six ROMs share the verified unused 0x0000-0x0037 RST block
- [x] 9-bit SetBank9 implemented
- [x] 9-bit FarCall9 implemented
- [x] BLUE high ROM-bank bit tracked in HRAM
- [x] VBlank interrupt made high-bit-safe
- [x] Timer / Serial / Joypad interrupt bank behavior audited
- [x] every exact legacy 0x2000 write classified as code or data
- [x] 86 Japanese / 88 per international executable writes migrated through LegacyBank8
- [x] three bank-8 data false positives per profile preserved
- [x] banks 0x000-0x1FF opened for executable BLUE code through the 9-bit ABI

## IDs

- [x] new global species/form/move/item/ability/type IDs: 16-bit
- [x] new map/location/trainer/evolution IDs: 16-bit
- [x] legacy Gen I byte IDs remain source-local compatibility values

## Save

- [x] physical legacy boundary: 32 KiB / four banks
- [x] extension boundary: banks 0x04-0x0F
- [x] 128 KiB save scaffold
- [x] first 32 KiB preserved byte-for-byte
- [ ] Japanese Ao real save sample audited
- [ ] English Blue real save sample audited
- [ ] French/German/Italian/Spanish real save samples audited
- [ ] region-specific legacy checksum parsers added

## Next active work

Continue from **expanded allocation + canonical registry bootstrap**.

The mapper-selection, 8 MiB sizing, 128 KiB save sizing, RST-vector discovery,
FarCall9, VBlank migration, and legacy 8-bit bank-switch migration are already
completed gates and must not be restarted.
