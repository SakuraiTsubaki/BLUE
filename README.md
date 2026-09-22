# BLUE

**ポケットモンスター 青 / Pokémon Blue**를 **원본 Game Boy ROM 자체에서 확장**하는 프로젝트입니다.

BLUE는 GBA/Emerald 엔진으로 옮기지 않습니다. 실행 기준은 사용자가 제공한 각 지역의 Blue ROM이며,
10세대까지의 공식 콘텐츠를 수용할 수 있도록 원본 카트리지 구조를 확장합니다.

## 확인된 원본

| 프로필 | ROM | Mapper | SRAM |
| --- | ---: | --- | ---: |
| ao-jp | 512 KiB | MBC1+RAM+BATTERY | 32 KiB |
| blue-us-eu | 1 MiB | MBC3+RAM+BATTERY | 32 KiB |
| blue-fr | 1 MiB | MBC5+RAM+BATTERY | 32 KiB |
| blue-de | 1 MiB | MBC5+RAM+BATTERY | 32 KiB |
| blue-it | 1 MiB | MBC5+RAM+BATTERY | 32 KiB |
| blue-es | 1 MiB | MBC5+RAM+BATTERY | 32 KiB |

정확한 SHA-1/SHA-256과 헤더 값은 `research/blue-rom-baseline.csv`에 있습니다.

## 확장 목표

- runtime: **original Game Boy ROM**
- mapper target: **MBC5+RAM+BATTERY**
- ROM: **8 MiB / 512 × 16 KiB banks**
- SRAM: **128 KiB / 16 × 8 KiB banks**
- 원본 ROM 영역은 mapper/size/checksum header 필드를 제외하고 그대로 보존
- 원본 SRAM 32 KiB는 byte-for-byte 보존
- 새 persistent content ID는 16-bit
- 새 far ROM reference는 9-bit bank를 수용
- ROM/SAV 바이너리는 GitHub에 커밋하지 않음

### 판본별 ROM 확장 영역

- Japanese Ao: original banks `0x000–0x01F`, expansion `0x020–0x1FF`
- International Blue: original banks `0x000–0x03F`, expansion `0x040–0x1FF`

### Save

모든 확인된 ROM header는 32 KiB SRAM을 요구합니다.

- SRAM banks `0x00–0x03`: 원본 save 영역
- SRAM banks `0x04–0x0F`: BLUE versioned extension 영역

현재 접근 가능한 실제 `.sav` 샘플은 없으므로 지역별 legacy offset/checksum을 봤다고 주장하지 않습니다.
확장 도구는 원본 32 KiB를 변경하지 않고 새 SRAM bank만 추가합니다.

## 도구

- `tools/expand_blue_rom.py` — 검증된 Blue ROM → 8 MiB MBC5 image scaffold
- `tools/expand_blue_save.py` — 32 KiB save → 128 KiB versioned save scaffold
- `tools/scan_mapper_writes.py` — mapper-control absolute-store 패턴 census
- `tools/verify_expansion_contract.py` — 구조/보존 규칙 검증

헤더 확장만으로 MBC1/MBC3 코드가 자동으로 MBC5-compatible이 되는 것은 아닙니다.
실제 bank-switch control flow를 검증하고 patch한 뒤에 0x100 이상의 ROM bank를 사용합니다.
