# Future / Generation 10 Readiness

This checklist is deliberately content-agnostic. New official content can be added when known without changing the core ABI.

## Data model

- [x] species ID is not limited to an 8-bit field
- [x] form is a first-class persistent field
- [x] moves use persistent 16-bit IDs
- [x] abilities use persistent 16-bit IDs
- [x] items use persistent 16-bit IDs
- [x] types are table-driven and not hard-coded to the current official count
- [x] evolution methods have extension space
- [x] generation number is not used as storage ABI

## Runtime tables

- [x] namespace ceiling is separate from allocated table length
- [x] generated counts are required
- [x] sparse optional data is permitted
- [ ] imported engine source audited for hard-coded counts
- [ ] battle scripts audited for 8-bit truncation
- [ ] menu/UI selectors audited for 8-bit truncation
- [ ] Pokédex/storage/party code audited for form loss
- [ ] trainer/encounter formats audited for form loss

## Save

- [x] raw C-struct serialization is forbidden for new extended blocks
- [x] schema version is mandatory
- [x] registry version is mandatory
- [x] ID reuse is forbidden
- [x] migration chain is mandatory
- [ ] concrete extended save-block offsets chosen after engine import
- [ ] old-save migration tests added
- [ ] forward-addition regression fixtures added

## Assets and localization

- [ ] graphics registry separated from species IDs
- [ ] icon/front/back/palette/form assets mapped by registry
- [ ] cries mapped by registry rather than generation switch
- [ ] text keys separated from numeric IDs
- [ ] Japanese source terminology retained as provenance
- [ ] Korean/current localization layer integrated independently
- [ ] English and other official localizations mapped without ID changes

## Integration gate

Before importing any future generation:

1. append registry data;
2. do not renumber prior IDs;
3. add/update mechanics through a profile or table;
4. add assets/localization through registries;
5. bump content-registry version if persistent mappings changed;
6. add migration only when serialized layout changed;
7. run `tools/verify_expansion_contract.py` and tests.
