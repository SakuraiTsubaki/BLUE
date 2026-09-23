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
- [x] low bank byte tracked through legacy hLoadedROMBank
- [x] BLUE high bank bit state assigned in HRAM
- [x] VBlank interrupt wrapped to clear/restore MBC5 bank bit 8
- [x] Timer interrupt audited: no bank switch
- [x] Serial interrupt handler audited: no bank switch
- [x] Joypad interrupt audited: immediate RETI
- [ ] synchronous legacy ROM-bank write paths made high-bit-safe
- [ ] high-bank code allowed to use legacy homecall/bankswitch paths
- [ ] banks 0x100-0x1FF enabled for unrestricted executable code

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

## Exact continuation point

Continue at the synchronous legacy `LD (0x2000),A` paths. Do not restart from mapper selection, ROM sizing, save sizing, RST-vector discovery, FarCall9, or VBlank migration.
