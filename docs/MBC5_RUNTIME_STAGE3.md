# BLUE MBC5 Runtime Stage 3 — legacy bank-switch migration

Stage 3 removes the remaining 8-bit synchronous ROM-bank hazard.

## Direct ROM classification

Every exact `EA 00 20` byte sequence was rechecked in each verified ROM.

Three matches per profile occur in bank 8 data and are not executable mapper writes. They are preserved byte-for-byte.

Executable write counts:

- Japanese Ao: 86
- English Blue: 88
- French Blue: 88
- German Blue: 88
- Italian Blue: 88
- Spanish Blue: 88

The patcher stores the exact three data offsets for every profile and refuses to proceed if counts or bytes change.

## LegacyBank8

BLUE uses `0x0043–0x004E`, identical unused vector/padding bytes in all six verified ROMs.

Entry: `0x0043`.

Input:

- A = legacy 8-bit target ROM bank

Effects:

1. preserves A and flags;
2. clears MBC5 ROM bank bit 8 at `0x3000`;
3. clears BLUE's high-bank shadow at `0xFFFA`;
4. restores A and flags;
5. writes A to the MBC5 low ROM-bank register at `0x2000`;
6. returns.

Every verified executable `LD (0x2000),A` is replaced with the same-size three-byte `CALL 0x0043`.

This keeps instruction footprint stable and prevents a legacy low-bank switch executed from bank 0x100–0x1FF from accidentally selecting bank 0x1xx.

## LCD vector use

The 12-byte helper region includes the otherwise unused LCD STAT vector at `0x0048`.

Retail initialization enables VBlank, Timer and Serial interrupts, not LCD STAT. The supplementary international source contains no path that enables `IE_STAT`. BLUE therefore reserves LCD STAT interrupt use while this helper occupies the vector.

## VBlank interaction

VBlank9 now saves the high-bit shadow on the CPU stack before invoking the legacy VBlank handler. This matters because legacy writes inside VBlank are also routed through LegacyBank8 and clear the live shadow.

After the legacy handler returns, VBlank9 restores both the shadow and hardware MBC5 bit 8, then executes `RETI`.

## Result

The ROM bank namespace `0x000–0x1FF` is now available to executable BLUE code through the 9-bit ABI.

This does not mean arbitrary legacy one-byte bank fields suddenly become 9-bit. New expanded code/data must use BLUE's 16-bit/far-reference formats, while legacy records retain their original meaning.
