import unittest

from tools.expand_blue_rom import (
    FARCALL9_ADDR,
    H_CURRENT_ROM_BANK_HIGH,
    H_LOADED_ROM_BANK_LOW,
    PROFILE_RUNTIME,
    RST_VECTOR_BASELINE,
    SETBANK9_ADDR,
    VBLANK9_ADDR,
    build_mbc5_runtime,
    install_mbc5_runtime,
)


class Mbc5RuntimeTests(unittest.TestCase):
    def test_verified_vector_space_is_56_bytes(self):
        self.assertEqual(len(RST_VECTOR_BASELINE), 0x38)

    def test_runtime_entry_points(self):
        self.assertEqual(FARCALL9_ADDR, 0x0000)
        self.assertEqual(SETBANK9_ADDR, 0x0010)
        self.assertEqual(VBLANK9_ADDR, 0x0020)

    def test_setbank9_writes_low_high_and_tracks_state(self):
        runtime = build_mbc5_runtime(0x2024)
        self.assertIn(bytes((0xE0, H_LOADED_ROM_BANK_LOW)), runtime)
        self.assertIn(b"\xEA\x00\x20", runtime)
        self.assertIn(b"\xEA\x00\x30", runtime)
        self.assertIn(bytes((0xE0, H_CURRENT_ROM_BANK_HIGH)), runtime)

    def test_vblank_wrapper_calls_profile_handler(self):
        runtime = build_mbc5_runtime(0x2024)
        self.assertIn(b"\xCD\x24\x20", runtime[VBLANK9_ADDR:0x38])
        self.assertEqual(runtime[0x37], 0)

    def test_install_patches_vector_and_original_reti(self):
        profile = "blue-us-eu"
        meta = PROFILE_RUNTIME[profile]
        rom = bytearray(b"\x00" * 0x3000)
        rom[:0x38] = RST_VECTOR_BASELINE
        rom[0x40:0x43] = bytes((0xC3, meta["vblank_target"] & 0xFF, meta["vblank_target"] >> 8))
        rom[meta["vblank_reti"]] = 0xD9
        install_mbc5_runtime(rom, profile)
        self.assertEqual(rom[0x40:0x43], b"\xC3\x20\x00")
        self.assertEqual(rom[meta["vblank_reti"]], 0xC9)


if __name__ == "__main__":
    unittest.main()
