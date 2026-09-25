# BLUE runtime species lookup adapter

The verified `BLU1SPC` table is now callable by the Game Boy runtime.

## FarCall9 ABI update

`FarCall9 = 0x0000` now preserves **A and flags** across the bank switch.

The 15-byte fixed-ROM sequence:

1. saves caller bank `DE`;
2. saves `AF`;
3. calls `SetBank9`;
4. restores `AF`;
5. pushes fixed return trampoline `0x000B`;
6. jumps to `HL`;
7. target returns to `0x000B`;
8. trampoline pops the saved caller bank directly into `BC`;
9. jumps to `SetBank9`, whose `RET` returns to the original caller.

This keeps the fixed RST-vector budget unchanged while making A available as an argument to banked adapters.

## LegacySpeciesToCanonical

Location: metadata bank, CPU `0x43A0`.

Call contract:

- A = Generation I internal species ID, 0..190
- BC = metadata bank for the current source profile
- DE = caller bank
- HL = 0x43A0
- call `FarCall9`
- return DE = canonical 16-bit species ID

The adapter indexes the 16-bit payload inside the `BLU1SPC` block at CPU
`0x4214`.

Special cases:

- input 0 → DE = 0
- one of the 39 MissingNo. internal slots → DE = 0
- real Gen I species → DE = official National Dex 1..151

The species directory entry at `0x4080` advertises this callable adapter with
the source profile's metadata bank and address `0x43A0`.

This is the first live bridge from an original one-byte Gen I ID into BLUE's
16-bit canonical namespace.
