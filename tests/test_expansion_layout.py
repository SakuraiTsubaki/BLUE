import hashlib
import unittest

from tools.blue_expansion_layout import (
    DIRECTORY_ENTRY_SIZE,
    MAGIC,
    PROFILE_LAYOUT,
    REGISTRY_DOMAINS,
    ROM_BANK_BYTES,
    build_directory,
    build_header,
    inspect_header,
    install_expansion_metadata,
    metadata_file_offset,
)


class ExpansionLayoutTests(unittest.TestCase):
    def test_profile_metadata_banks(self):
        self.assertEqual(PROFILE_LAYOUT["ao-jp"]["metadata_bank"], 0x20)
        for profile in ("blue-us-eu", "blue-fr", "blue-de", "blue-it", "blue-es"):
            self.assertEqual(PROFILE_LAYOUT[profile]["metadata_bank"], 0x40)

    def test_directory_is_empty_but_versioned(self):
        directory = build_directory()
        self.assertEqual(len(directory), len(REGISTRY_DOMAINS) * DIRECTORY_ENTRY_SIZE)

    def test_install_uses_first_expansion_bank(self):
        source_sha = hashlib.sha256(b"blue-test").hexdigest()
        image = bytearray(b"\xFF" * (0x800000))
        install_expansion_metadata(image, "ao-jp", source_sha)
        base = metadata_file_offset("ao-jp")
        self.assertEqual(base, 0x20 * ROM_BANK_BYTES)
        self.assertEqual(image[base:base + 8], MAGIC)
        info = inspect_header(image, "ao-jp")
        self.assertEqual(info["first_content_bank"], 0x21)
        self.assertEqual(info["directory_count"], 10)
        self.assertEqual(info["crc32_valid"], 1)

    def test_international_content_starts_after_original_1mib(self):
        source_sha = hashlib.sha256(b"blue-intl").hexdigest()
        image = bytearray(b"\xFF" * 0x800000)
        install_expansion_metadata(image, "blue-us-eu", source_sha)
        info = inspect_header(image, "blue-us-eu")
        self.assertEqual(info["metadata_bank"], 0x40)
        self.assertEqual(info["first_content_bank"], 0x41)


if __name__ == "__main__":
    unittest.main()
