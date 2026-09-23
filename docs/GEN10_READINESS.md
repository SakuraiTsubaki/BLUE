# Generation 10 Readiness — BLUE

## Cartridge / mapper

- [x] six Blue ROM baselines verified
- [x] source mapper families identified: MBC1 / MBC3 / MBC5
- [x] target mapper: MBC5
- [x] target ROM: 8 MiB / 512 banks
- [x] target SRAM: 128 KiB / 16 banks
- [x] Japanese and international preservation ranges defined
- [x] mapper writes grouped by ROM bank and role
- [x] all six ROMs verified to share the same unused 0x0000-0x0037 RST-vector block
- [x] 9-bit MBC5 SetBank9 routine implemented
- [x] 9-bit FarCall9 trampoline implemented
- [x] banks 0x000-0x0FF opened as ordinary executable expansion space
- [ ] ROM bank bit 8 integrated into interrupt bank-state bookkeeping
- [ ] VBlank bank save/restore widened to 9 bits
- [ ] Timer/Serial bank save/restore widened to 9 bits
- [ ] all legacy bankswitch/homecall paths audited for high-bit restore
- [ ] banks 0x100-0x1FF enabled for ordinary long-running executable code

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

Continue from the new 9-bit trampoline into the interrupt/bank-state migration. Do not restart from capacity planning.
