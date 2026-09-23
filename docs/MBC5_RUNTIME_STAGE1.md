# BLUE MBC5 Runtime Stage 1

## Verified fixed-ROM injection window

All six verified Blue-family ROMs have identical bytes from 0x0000 through 0x0037:

```
ff00000000000000 × 7
```

SHA-256:

`5dba2cb910e9dbcb62c7e9e0b829f2e5e9fbf6eb183aaa1639f23998e27b791b`

The international Red/Blue source labels these RST vectors as unused. BLUE only consumes 27 bytes at 0x0000-0x001A and deliberately does not touch 0x0038 because the Japanese ROM differs there.

## FarCall9

Entry: `0x0000`

Inputs:

- `BC`: target ROM bank; C = low 8 bits, B bit 0 = bank bit 8
- `DE`: caller ROM bank in the same encoding
- `HL`: target address in the switchable window

The trampoline runs entirely from fixed ROM0, writes both MBC5 bank registers, jumps to the target, then restores the caller bank.

## SetBank9

Entry: `0x0010`

Input:

- `BC`: target ROM bank

Writes:

- C to `0x2000`
- B bit 0 to `0x3000`

## Stage-1 safety boundary

Banks 0x000-0x0FF are safe for ordinary executable expansion because MBC5 bank bit 8 remains zero and the legacy interrupt/bank-state code remains compatible.

Banks 0x100-0x1FF are physically addressable by the new trampoline, but long-running executable code there is **not enabled yet**. The original interrupt and legacy bank-switch bookkeeping stores only the low bank byte. An interrupt occurring while bank bit 8 is set could restore only the low byte and return with the wrong mapping.

Until stage 2:

- banks 0x100-0x1FF are reserved primarily for controlled high-bank data access;
- high-bank execution requires an explicitly interrupt-safe call site;
- no general gameplay routine is allocated there.

## Stage 2

The next runtime migration is to make bank state 9-bit across:

- VBlank
- Timer
- Serial
- generic bankswitch/homecall paths
- sprite decompression bank switching
- any other executable path that changes ROM banks

After those restore both MBC5 bank registers, banks 0x100-0x1FF can become ordinary executable banks.
