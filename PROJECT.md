# BLUE Project

## Canonical direction

ポケットモンスター 青 / Pokémon Blue를 **원본 Game Boy ROM 자체에서 확장**한다.

GBA, Emerald, pokeemerald-expansion은 BLUE의 런타임 기반이 아니다.

## Original baselines

현재 직접 검증한 입력은 6개다.

- Japanese Pocket Monsters Ao
- English Blue (USA/Europe)
- French Blue
- German Blue
- Italian Blue
- Spanish Blue

각 ROM은 독립 provenance를 유지한다. 일본판은 원전/기준 언어이고, 다른 지역판은 각자의 ROM 구조와
현지화 차이를 보존한다.

## Runtime target

- CPU/platform: original Game Boy family runtime
- cartridge target: MBC5+RAM+BATTERY
- maximum standard MBC5 ROM image: 8 MiB
- expanded battery SRAM: 128 KiB
- SGB flag: source value preserved
- original ROM/SAV bytes: preservation boundary maintained

## Generation 10 rule

Generation 10의 미공개 내용을 추측하지 않는다.
대신 새 콘텐츠가 공개되어도 다시 저장 형식 전체를 갈아엎지 않도록 확장 영역의 ID와 far reference를
미리 넓힌다.

새 전역 content IDs는 16-bit이며 기존 Gen I byte IDs는 source-local legacy ID로 남긴다.
