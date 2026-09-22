import unittest

from tools.expand_blue_save import EXT_OFFSET, MAGIC, SOURCE_SIZE, TARGET_SIZE, expand_save
from tools.scan_mapper_writes import positions


class BlueOriginalRomToolTests(unittest.TestCase):
    def test_save_expansion_preserves_legacy_region(self):
        source = bytes((i * 13 + 7) & 0xFF for i in range(SOURCE_SIZE))
        expanded = expand_save(source, "ao-jp")
        self.assertEqual(len(expanded), TARGET_SIZE)
        self.assertEqual(expanded[:SOURCE_SIZE], source)
        self.assertEqual(expanded[EXT_OFFSET:EXT_OFFSET + 8], MAGIC)

    def test_each_profile_can_create_extension_header(self):
        source = bytes([0xFF]) * SOURCE_SIZE
        for profile in ("ao-jp", "blue-us-eu", "blue-fr", "blue-de", "blue-it", "blue-es"):
            expanded = expand_save(source, profile)
            self.assertEqual(expanded[:SOURCE_SIZE], source)

    def test_mapper_write_scan(self):
        blob = b"\x00\xEA\x00\x20\xEA\x00\x30\xEA\x00\x20"
        self.assertEqual(positions(blob, 0x2000), [1, 7])
        self.assertEqual(positions(blob, 0x3000), [4])


if __name__ == "__main__":
    unittest.main()
