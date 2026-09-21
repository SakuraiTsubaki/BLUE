# BLUE Expansion Architecture

## Goal

BLUE must accept later-generation content without another fundamental ID/save rewrite. The expansion layer therefore treats generation labels as data provenance, not as storage ABI.

This document defines the contract before game source import begins.

## 1. Stable IDs

Persistent content IDs use fixed-width 16-bit storage.

Rules:

1. ID 0 is the NONE / absent value where the namespace needs one.
2. 0xFFFF is invalid/reserved.
3. Existing IDs are never renumbered.
4. Deleted/retired IDs become tombstones; they are not recycled.
5. New content is appended or mapped through an explicit registry.
6. Capacity values are namespace ceilings, not instructions to allocate full-size arrays.

The concrete ceilings live in `config/expansion_limits.json`.

## 2. Species and forms

Canonical BLUE data does not flatten every form into an unrelated species identity.

Persistent identity is:

```text
(species_id, form_id)
```

This supports regional forms, gender forms, battle forms, temporary forms and future forms without requiring a global species-ID rewrite.

An upstream engine may internally represent a form with a dedicated species constant. The integration layer is responsible for mapping that representation to the canonical BLUE pair.

Variants driven by personality, pattern seed or other parameters do not have to consume thousands of form IDs.

## 3. Content generation vs mechanics generation

These are separate axes.

Examples:

- A Generation I map/story can use a current battle-mechanics profile.
- A compatibility profile can preserve an older mechanic without changing species/item IDs.
- A future generation can append content without changing the save schema merely because its generation number changed.

No code should use `GEN_10` (or any generation constant) as an array bound or serialized-format width.

## 4. Tables

Counts are generated from actual registries.

Do not use generation-sized fixed arrays such as:

```c
Entry table[GENERATION_X_SPECIES_COUNT];
```

Prefer generated tables and explicit counts:

```c
extern const struct Entry gEntries[];
extern const u16 gEntriesCount;
```

Optional per-species/per-form data may be sparse.

## 5. Save compatibility

The extended save format is versioned independently from the game build.

Persistent data is encoded field-by-field rather than by dumping compiler C structs. Every extended save block carries a schema version and content-registry version, and migrations are explicit.

Appending a new species, move, item, ability or form must not change the meaning of an existing save value.

See `config/save_schema.json`.

## 6. Engine base

The initial modern-engine candidate is pinned in `manifests/engine-base.json`.

The pin is a reproducibility baseline, not a permanent prohibition on upgrades. Updating the expansion engine requires:

- passing the expansion contract validator;
- reviewing persistent-ID mapping;
- reviewing save migration;
- verifying BLUE overlays still apply;
- recording the new upstream commit.

## 7. What this foundation does not claim

This commit does not implement future-generation content and does not claim knowledge of unreleased species, moves, mechanics or formats.

It prevents those additions from forcing another foundational rewrite.
