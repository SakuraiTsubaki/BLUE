# BLUE

Pocket Monsters Ao / Pokémon Blue를 현대 Generation III / GBA 계열 엔진에서 재구성하는 프로젝트입니다.

## 현재 단계 — ROM/save 근거 기반 확장

BLUE의 확장은 추측으로 먼저 숫자를 크게 잡지 않습니다.

1. 실제 Blue ROM을 조사한다.
2. 원본 battery save/SRAM 구조를 조사한다.
3. 대상 GBA 엔진의 실제 save/ID 구조를 조사한다.
4. 그 차이를 import/migration 계층으로 분리한다.
5. 그 뒤 Species/Form/Move/Ability/Item/Type 등 실제 엔진 제한을 제거한다.

### 확인된 원본 ROM 기준

현재 6개 Blue 계열 ROM을 직접 검사했습니다.

- Japanese Pocket Monsters Ao: 512 KiB ROM, MBC1+RAM+BATTERY
- English Blue: 1 MiB ROM, MBC3+RAM+BATTERY
- French/German/Italian/Spanish Blue: 1 MiB ROM, MBC5+RAM+BATTERY
- 6개 전부 cartridge RAM size code `0x03` = **32 KiB battery SRAM**
- 6개 전부 SGB flag `0x03`
- header/global checksum 검증 통과

해시와 header 값은 `research/blue-rom-baseline.csv`에 기록합니다.

### Save 확장 원칙

원본 Game Boy save를 그 자리에서 억지로 확장하지 않습니다.

```text
original 32 KiB Blue SRAM
        ↓
legacy parser / validation
        ↓
canonical import model
        ↓
BLUE GBA runtime save
```

원본 save는 import source로 취급하며 raw bytes와 원래 ID 의미를 보존합니다.

현재 활성 작업공간에는 실제 `.sav` 파일이 없어 **실제 save sample의 byte layout을 검사했다고 주장하지 않습니다**. ROM header가 요구하는 32 KiB SRAM과 공개 Red/Blue save source를 교차 확인해 legacy boundary를 먼저 고정했습니다. 실제 save sample이 접근 가능해지면 `tools/analyze_blue_inputs.py`로 즉시 구조 검증을 추가합니다.

### 대상 엔진 save 기준

현재 engine candidate인 `rh-hideout/pokeemerald-expansion`의 pinned source 기준:

- 128 KiB Flash
- 4 KiB sector × 32
- main save slot 14 sectors × 2
- sector data 3968 bytes
- SaveBlock3 chunk 116 bytes
- footer 12 bytes

자세한 근거와 확장 결정은 `docs/ROM_SAVE_EXPANSION_BASIS.md`를 참조합니다.

## 검증

```sh
python tools/verify_expansion_contract.py
python tools/analyze_blue_inputs.py path/to/rom.gb path/to/save.sav
python -m unittest discover -s tests -v
```

ROM/save 바이너리는 GitHub에 올리지 않습니다.
