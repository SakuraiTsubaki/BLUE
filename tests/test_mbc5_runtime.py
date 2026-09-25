import unittest

from tools.expand_blue_rom import (
    FARCALL9_ADDR,
    LEGACY_BANK8_ADDR,
    LEGACY_BANK_HELPER_BASELINE,
    RST_VECTOR_BASELINE,
    SETBANK9_ADDR,
    VBLANK9_ADDR,
    build_mbc5_runtime,
    legacy_bank8_helper,
)


class Mbc5RuntimeTests(unittest.TestCase):
    def test_verified_vector_space_is_56_bytes(self):
        self.assertEqual(len(RST_VECTOR_BASELINE), 0x38)

    def test_legacy_helper_region_is_12_verified_bytes(self):
        self.assertEqual(len(LEGACY_BANK_HELPER_BASELINE), 12)
        self.assertEqual(len(legacy_bank8_helper()), 12)

    def test_runtime_entry_points(self):
        self.assertEqual(FARCALL9_ADDR, 0x0000)
        self.assertEqual(SETBANK9_ADDR, 0x0010)
        self.assertEqual(VBLANK9_ADDR, 0x0020)
        self.assertEqual(LEGACY_BANK8_ADDR, 0x0043)

    def test_farcall9_preserves_af_and_uses_compact_return_trampoline(self):
        runtime = build_mbc5_runtime(0x2024)
        farcall = runtime[:0x10]
        self.assertEqual(farcall[:2], b"\xD5\xF5")
        self.assertIn(b"\xF1\x01\x0B\x00\xC5\xE9", farcall)
        self.assertEqual(farcall[0x0B:0x0F], b"\xC1\xC3\x10\x00")

    def test_setbank9_writes_both_mbc5_registers(self):
        runtime = build_mbc5_runtime(0x2024)
        self.assertIn(b"\xEA\x00\x20", runtime)
        self.assertIn(b"\xEA\x00\x30", runtime)

    def test_vblank_wrapper_saves_high_shadow_on_stack(self):
        runtime = build_mbc5_runtime(0x2024)
        wrapper = runtime[VBLANK9_ADDR:0x38]
        self.assertTrue(wrapper.startswith(b"\xF0\xFA\xF5"))
        self.assertIn(b"\xCD\x24\x20", wrapper)
        reti = wrapper.index(b"\xD9")
        self.assertEqual(wrapper[reti + 1:], b"\x00" * (len(wrapper) - reti - 1))

    def test_legacy_bank8_preserves_af_and_clears_high(self):
        helper = legacy_bank8_helper()
        self.assertEqual(helper[0], 0xF5)
        self.assertIn(b"\xEA\x00\x30", helper)
        self.assertIn(b"\xE0\xFA", helper)
        self.assertIn(b"\xF1\xEA\x00\x20", helper)
        self.assertEqual(helper[-1], 0xC9)


if __name__ == "__main__":
    unittest.main()
