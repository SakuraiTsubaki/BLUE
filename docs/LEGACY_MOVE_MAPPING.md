# Gen I move byte → BLUE canonical move ID

## Direct ROM evidence

All six verified Blue-family ROMs place the 165-record move table at:

- file offset: `0x38000`
- ROM bank: `0x0E`
- CPU address: `0x4000`
- record size: 6 bytes
- table size: 990 bytes

For every profile, byte 0 of records 1..165 is exactly the sequence
`0x01..0xA5`.

Therefore the legacy move byte is already a stable one-to-one identifier for
the 165 Generation I moves.

## Regional data difference

The Japanese Ao move table hash differs from all five localized Blue ROMs by
one byte.

At table offset `0x15D`, move 59 (Blizzard), the effect byte is:

- Japanese Ao: `0x23`
- localized Blue: `0x05`

This changes move behavior metadata, **not the move ID**.

## Canonical rule

BLUE reserves canonical move IDs `1..165` for the verified Generation I move
IDs with the same numeric value.

- legacy 0 → canonical 0
- legacy 1..165 → canonical 1..165
- legacy 166..255 → canonical 0/unmapped

Future official moves append in the 16-bit namespace; existing IDs are never
renumbered.

## Runtime block

Metadata bank CPU `0x4400` stores a versioned `BLU1MOV` block containing a
full 256-entry u16 translation table.

CPU `0x4620` stores the callable move adapter:

- input A = legacy move byte
- output DE = canonical 16-bit move ID
- call through FarCall9

The full 256-entry table means invalid/unused legacy byte values translate to
0 without branch-specific assumptions.
