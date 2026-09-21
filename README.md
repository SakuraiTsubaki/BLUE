# BLUE

Pokémon Blue / Pocket Monsters Ao를 현대 3세대 계열 엔진 위에서 재구성하는 프로젝트입니다.

## Current phase — future-generation expansion foundation

스토리/맵 이식보다 먼저, 이후 세대가 추가되어도 데이터 구조를 다시 깨지 않도록 확장 ABI와 저장 호환 규칙을 고정합니다.

현재 기반:

- 실행 엔진 계열: Generation III / GBA
- 확장 엔진 후보: `rh-hideout/pokeemerald-expansion`
- canonical species representation: `species_id + form_id`
- runtime/content IDs: fixed-width 16-bit where persistent
- ID allocation: append-only; 기존 ID 재번호 금지
- save data: versioned schema + explicit migration
- mechanics/content generation: 서로 분리
- generation ceiling: 특정 세대로 하드코딩하지 않음

확장 규격은 다음 파일이 기준입니다.

- `config/expansion_limits.json`
- `config/save_schema.json`
- `manifests/engine-base.json`
- `docs/EXPANSION_ARCHITECTURE.md`
- `docs/GEN10_READINESS.md`
- `tools/verify_expansion_contract.py`

검증:

```sh
python tools/verify_expansion_contract.py
python -m unittest discover -s tests -v
```

ROM 바이너리는 저장소에 올리지 않습니다.
