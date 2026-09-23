import unittest

from tools.expand_blue_rom import (
    FARCALL9_ADDR,
    MBC5_RUNTIME_STUB,
    RST_VECTOR_BASELINE,
    SETBANK9_ADDR,
    install_mbc5_runtime,
)


class Mbc5RuntimeTests(unittest.TestCase):
    def test_verified_vector_space_is_56_bytes(self):
        self.assertEqual(len(RST_VECTOR_BASELINE), 0x38)

    def test_runtime_stub_fits_without_touching_rst38(self):
        self.assertLess(len(MBC5_RUNTIME_STUB), 0x38)
        rom = bytearray(RST_VECTOR_BASELINE + b"\xA5")
        install_mbc5_runtime(rom)
        self.assertEqual(rom[:len(MBC5_RUNTIME_STUB)], MBC5_RUNTIME_STUB)
        self.assertEqual(rom[0x38], 0xA5)

    def test_runtime_entry_points(self):
        self.assertEqual(FARCALL9_ADDR, 0x0000)
        self.assertEqual(SETBANK9_ADDR, 0x0010)

    def test_runtime_writes_both_mbc5_bank_registers(self):
        self.assertIn(b"\xEA\x00\x20", MBC5_RUNTIME_STUB)
        self.assertIn(b"\xEA\x00\x30", MBC5_RUNTIME_STUB)


if __name__ == "__main__":
    unittest.main()
